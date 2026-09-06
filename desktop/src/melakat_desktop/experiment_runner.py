from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import os
import platform
import re
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

from .artifacts import canonical_json, config_hash, write_json, write_summary_csv
from .parameters import CORE_SCHEMA
from .phase_two_experiment import ENERGY_TOLERANCE, RESOURCE_TOLERANCE, result_checksum
from .phase_two_engine import PhaseTwoEngine
from .phase_zero_engine import PhaseZeroEngine
from .world_contract import WORLD_CONTRACT_VERSION

EXPERIMENT_SPEC_FORMAT = "melakat-experiment-spec-0.1"
EXPERIMENT_CAMPAIGN_FORMAT = "melakat-experiment-campaign-0.1"
EXPERIMENT_SUMMARY_FORMAT = "melakat-experiment-summary-0.1"
EXPERIMENT_PROVENANCE_FORMAT = "melakat-experiment-provenance-0.1"

SUPPORTED_ENGINES = {"phase-zero-vm", "phase-two-vm"}
KNOWN_PARAMETERS = {spec.path for spec in CORE_SCHEMA.specs}

COMPACT_METRICS = (
    "engine_version",
    "measurement_version",
    "world_contract_version",
    "spatial_enabled",
    "local_resources_enabled",
    "organism_actions_enabled",
    "boundary_model",
    "tick",
    "active_population",
    "births",
    "deaths",
    "max_population",
    "active_genotypes",
    "historical_genotypes",
    "active_lineages",
    "max_generation",
    "instructions_executed",
    "faults",
    "blocked_divisions",
    "waiting_for_memory",
    "waiting_for_energy",
    "energy_pool",
    "memory_used",
    "free_memory",
    "energy_balance_error",
    "spatial_births",
    "boundary_contacts",
    "mean_parent_child_distance",
    "mean_local_neighbors",
    "mean_nearest_neighbor_distance",
    "occupied_spatial_bins",
    "spatial_occupancy_fraction",
    "local_resource_total",
    "local_resource_minimum",
    "local_resource_balance_error",
    "resource_sense_operations",
    "movement_operations",
    "movement_distance",
    "movement_energy_cost",
)

SUMMARY_METRICS = (
    "active_population",
    "births",
    "deaths",
    "max_population",
    "historical_genotypes",
    "active_genotypes",
    "max_generation",
    "instructions_executed",
    "faults",
    "blocked_divisions",
    "waiting_for_memory",
    "waiting_for_energy",
    "energy_pool",
    "memory_used",
    "free_memory",
    "mean_local_neighbors",
    "mean_nearest_neighbor_distance",
    "local_resource_total",
    "movement_operations",
    "movement_distance",
)


def _safe_name(value: Any) -> str:
    text = str(value).strip().replace(" ", "_")
    text = re.sub(r"[^A-Za-z0-9_.-]+", "_", text)
    return text or "value"


def _load_yaml(path: Path) -> Any:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "YAML experiment specs require PyYAML. Install the package with "
            "`python -m pip install PyYAML` or use JSON."
        ) from exc
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_experiment_spec(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        raw = json.loads(path.read_text(encoding="utf-8"))
    elif suffix in {".yaml", ".yml"}:
        raw = _load_yaml(path)
    else:
        raise ValueError("experiment_spec_must_be_json_or_yaml")
    if not isinstance(raw, dict):
        raise ValueError("experiment_spec_must_be_an_object")
    if raw.get("format") != EXPERIMENT_SPEC_FORMAT:
        raise ValueError(
            f"experiment_spec_format_must_be_{EXPERIMENT_SPEC_FORMAT}"
        )
    if not str(raw.get("name", "")).strip():
        raise ValueError("experiment_spec_requires_name")
    return raw


def _validate_overrides(overrides: Mapping[str, Any], *, label: str) -> dict[str, Any]:
    unknown = sorted(set(overrides) - KNOWN_PARAMETERS)
    if unknown:
        raise ValueError(f"{label}_contains_unknown_parameters:{','.join(unknown)}")
    return dict(overrides)


def resolve_seeds(spec: Mapping[str, Any]) -> list[int]:
    seed_spec = spec.get("seeds", {"start": 1, "count": 1})
    if isinstance(seed_spec, list):
        seeds = [int(value) for value in seed_spec]
    elif isinstance(seed_spec, dict):
        if "values" in seed_spec:
            seeds = [int(value) for value in seed_spec["values"]]
        else:
            start = int(seed_spec.get("start", 1))
            count = int(seed_spec.get("count", 1))
            if count < 1:
                raise ValueError("seed_count_must_be_positive")
            seeds = list(range(start, start + count))
    else:
        raise ValueError("seeds_must_be_a_list_or_object")
    if not seeds:
        raise ValueError("experiment_requires_at_least_one_seed")
    if len(set(seeds)) != len(seeds):
        raise ValueError("experiment_seeds_must_be_unique")
    return seeds


def _expand_conditions(spec: Mapping[str, Any]) -> list[dict[str, Any]]:
    expanded: list[dict[str, Any]] = []

    conditions = spec.get("conditions", [])
    if conditions is None:
        conditions = []
    if not isinstance(conditions, list):
        raise ValueError("conditions_must_be_a_list")
    for index, condition in enumerate(conditions):
        if not isinstance(condition, dict):
            raise ValueError(f"condition_{index}_must_be_an_object")
        name = str(condition.get("name", "")).strip()
        if not name:
            raise ValueError(f"condition_{index}_requires_name")
        overrides = _validate_overrides(
            condition.get("overrides", {}),
            label=f"condition_{name}",
        )
        expanded.append({"name": name, "overrides": overrides, "source": "condition"})

    sweeps = spec.get("sweeps", [])
    if sweeps is None:
        sweeps = []
    if not isinstance(sweeps, list):
        raise ValueError("sweeps_must_be_a_list")
    for index, sweep in enumerate(sweeps):
        if not isinstance(sweep, dict):
            raise ValueError(f"sweep_{index}_must_be_an_object")
        sweep_name = str(sweep.get("name", f"sweep_{index + 1}")).strip()
        base_overrides = _validate_overrides(
            sweep.get("base_overrides", {}),
            label=f"sweep_{sweep_name}_base",
        )

        if "parameters" in sweep:
            parameters = sweep["parameters"]
            if not isinstance(parameters, dict) or not parameters:
                raise ValueError(f"sweep_{sweep_name}_parameters_must_be_nonempty_object")
        elif "parameter" in sweep and "values" in sweep:
            parameters = {str(sweep["parameter"]): sweep["values"]}
        else:
            raise ValueError(
                f"sweep_{sweep_name}_requires_parameters_or_parameter_and_values"
            )

        parameter_names = list(parameters)
        _validate_overrides(
            {name: CORE_SCHEMA.defaults().get(name) for name in parameter_names},
            label=f"sweep_{sweep_name}",
        )
        value_lists: list[list[Any]] = []
        for parameter_name in parameter_names:
            values = parameters[parameter_name]
            if not isinstance(values, list) or not values:
                raise ValueError(
                    f"sweep_{sweep_name}_{parameter_name}_requires_nonempty_values"
                )
            value_lists.append(list(values))

        for combination in itertools.product(*value_lists):
            overrides = dict(base_overrides)
            parts: list[str] = []
            for parameter_name, value in zip(parameter_names, combination):
                overrides[parameter_name] = value
                parts.append(f"{parameter_name.rsplit('.', 1)[-1]}={_safe_name(value)}")
            condition_name = f"{sweep_name}__" + "__".join(parts)
            expanded.append(
                {
                    "name": condition_name,
                    "overrides": overrides,
                    "source": "sweep",
                    "sweep": sweep_name,
                }
            )

    if not expanded:
        expanded.append({"name": "base", "overrides": {}, "source": "base"})

    names = [condition["name"] for condition in expanded]
    if len(set(names)) != len(names):
        raise ValueError("condition_names_must_be_unique")
    return expanded


def build_experiment_plan(
    spec: Mapping[str, Any],
    *,
    seed_count_override: int | None = None,
    seed_start_override: int | None = None,
    ticks_override: int | None = None,
) -> dict[str, Any]:
    base_overrides = _validate_overrides(
        spec.get("base_config", {}),
        label="base_config",
    )
    base = CORE_SCHEMA.defaults()
    base.update(base_overrides)
    if ticks_override is not None:
        if ticks_override < 1:
            raise ValueError("ticks_override_must_be_positive")
        base["run.max_ticks"] = int(ticks_override)
    base = CORE_SCHEMA.validate(base)

    engine = str(base["run.engine_backend"])
    if engine not in SUPPORTED_ENGINES:
        raise ValueError(
            f"automated_experiments_support_engines:{','.join(sorted(SUPPORTED_ENGINES))}"
        )

    seeds = resolve_seeds(spec)
    if seed_start_override is not None:
        count = seed_count_override if seed_count_override is not None else len(seeds)
        if count < 1:
            raise ValueError("seed_count_override_must_be_positive")
        seeds = list(range(int(seed_start_override), int(seed_start_override) + count))
    elif seed_count_override is not None:
        if seed_count_override < 1:
            raise ValueError("seed_count_override_must_be_positive")
        if isinstance(spec.get("seeds"), dict) and "values" not in spec.get("seeds", {}):
            start = int(spec.get("seeds", {}).get("start", seeds[0]))
            seeds = list(range(start, start + int(seed_count_override)))
        else:
            seeds = seeds[: int(seed_count_override)]
            if len(seeds) < int(seed_count_override):
                raise ValueError("seed_count_override_exceeds_explicit_seed_list")

    conditions = _expand_conditions(spec)
    resolved_conditions: list[dict[str, Any]] = []
    for condition in conditions:
        config = dict(base)
        config.update(condition["overrides"])
        config = CORE_SCHEMA.validate(config)
        resolved_conditions.append(
            {
                **condition,
                "config_hash_without_seed": config_hash(config),
            }
        )

    return {
        "format": EXPERIMENT_SPEC_FORMAT,
        "name": str(spec["name"]),
        "description": str(spec.get("description", "")),
        "base_config": base,
        "base_config_hash": config_hash(base),
        "seeds": seeds,
        "conditions": resolved_conditions,
        "run_count": len(seeds) * len(resolved_conditions),
    }


def _engine_for(config: Mapping[str, Any], sink: Any) -> Any:
    backend = str(config["run.engine_backend"])
    if backend == "phase-zero-vm":
        return PhaseZeroEngine(config, sink)
    if backend == "phase-two-vm":
        return PhaseTwoEngine(config, sink)
    raise ValueError(f"unsupported_automated_experiment_backend:{backend}")


def _run(config: Mapping[str, Any]) -> dict[str, Any]:
    validated = CORE_SCHEMA.validate(config)
    engine = _engine_for(validated, lambda _event: None)
    while not engine.finished:
        engine.step()
    return engine.summary()


def _compact(
    condition: str,
    seed: int,
    config: Mapping[str, Any],
    summary: Mapping[str, Any],
) -> dict[str, Any]:
    record = {
        "condition": condition,
        "seed": int(seed),
        "config_hash": config_hash(config),
        "result_checksum": result_checksum(summary),
    }
    for key in COMPACT_METRICS:
        if key in summary:
            record[key] = summary.get(key)
    return record


def _validate_run(
    condition: str,
    seed: int,
    config: Mapping[str, Any],
    summary: Mapping[str, Any],
) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    energy_error = abs(float(summary.get("energy_balance_error", 0.0)))
    if energy_error > ENERGY_TOLERANCE:
        failures.append(
            {
                "condition": condition,
                "seed": seed,
                "kind": "energy_balance",
                "error": energy_error,
                "tolerance": ENERGY_TOLERANCE,
            }
        )

    if bool(config.get("world.local_resources_enabled", False)):
        resource_error = abs(float(summary.get("local_resource_balance_error", 0.0)))
        if resource_error > RESOURCE_TOLERANCE:
            failures.append(
                {
                    "condition": condition,
                    "seed": seed,
                    "kind": "local_resource_balance",
                    "error": resource_error,
                    "tolerance": RESOURCE_TOLERANCE,
                }
            )
        if float(summary.get("local_resource_minimum", 0.0)) < -1e-12:
            failures.append(
                {
                    "condition": condition,
                    "seed": seed,
                    "kind": "negative_local_resource",
                }
            )

    if bool(config.get("world.spatial_enabled", False)):
        snapshot = summary.get("final_snapshot", {})
        width = float(config["world.width"])
        height = float(config["world.height"])
        for organism in snapshot.get("organisms", []):
            x = float(organism["x"])
            y = float(organism["y"])
            if not (0.0 <= x <= width and 0.0 <= y <= height):
                failures.append(
                    {
                        "condition": condition,
                        "seed": seed,
                        "kind": "out_of_bounds",
                        "organism_id": organism.get("id"),
                        "x": x,
                        "y": y,
                    }
                )
                break
    return failures


def _numeric_values(runs: Iterable[Mapping[str, Any]], key: str) -> list[float]:
    values: list[float] = []
    for run in runs:
        value = run.get(key)
        if isinstance(value, bool) or value is None:
            continue
        if isinstance(value, (int, float)):
            values.append(float(value))
    return values


def summarize_runs(
    experiment_name: str,
    conditions: Iterable[Mapping[str, Any]],
    runs: list[dict[str, Any]],
) -> dict[str, Any]:
    condition_summaries: list[dict[str, Any]] = []
    for condition in conditions:
        name = str(condition["name"])
        selected = [run for run in runs if run["condition"] == name]
        row: dict[str, Any] = {
            "condition": name,
            "run_count": len(selected),
            "extinction_count": sum(
                1 for run in selected if int(run.get("active_population", -1)) == 0
            ),
        }
        row["extinction_fraction"] = (
            row["extinction_count"] / len(selected) if selected else 0.0
        )
        for metric in SUMMARY_METRICS:
            values = _numeric_values(selected, metric)
            if not values:
                continue
            row[f"{metric}_mean"] = statistics.fmean(values)
            row[f"{metric}_min"] = min(values)
            row[f"{metric}_max"] = max(values)
        condition_summaries.append(row)

    baseline = condition_summaries[0] if condition_summaries else None
    comparisons: list[dict[str, Any]] = []
    if baseline is not None:
        for row in condition_summaries[1:]:
            delta: dict[str, Any] = {
                "condition": row["condition"],
                "baseline_condition": baseline["condition"],
            }
            for metric in SUMMARY_METRICS:
                key = f"{metric}_mean"
                if key in baseline and key in row:
                    delta[f"{metric}_mean_delta"] = row[key] - baseline[key]
            delta["extinction_fraction_delta"] = (
                row["extinction_fraction"] - baseline["extinction_fraction"]
            )
            comparisons.append(delta)

    return {
        "format": EXPERIMENT_SUMMARY_FORMAT,
        "experiment": experiment_name,
        "condition_count": len(condition_summaries),
        "run_count": len(runs),
        "baseline_condition": baseline["condition"] if baseline else None,
        "conditions": condition_summaries,
        "comparisons": comparisons,
    }


def _select_reproducibility_target(
    spec: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> tuple[str, int]:
    requested = spec.get("reproducibility", {})
    condition_names = [str(item["name"]) for item in plan["conditions"]]
    condition = str(requested.get("condition", condition_names[0]))
    seed = int(requested.get("seed", plan["seeds"][0]))
    if condition not in condition_names:
        raise ValueError(f"reproducibility_condition_not_found:{condition}")
    if seed not in plan["seeds"]:
        raise ValueError(f"reproducibility_seed_not_in_plan:{seed}")
    return condition, seed


def run_experiment(
    spec: Mapping[str, Any],
    *,
    seed_count_override: int | None = None,
    seed_start_override: int | None = None,
    ticks_override: int | None = None,
    progress: bool = True,
) -> dict[str, Any]:
    plan = build_experiment_plan(
        spec,
        seed_count_override=seed_count_override,
        seed_start_override=seed_start_override,
        ticks_override=ticks_override,
    )

    runs: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    total = int(plan["run_count"])
    completed = 0

    for condition in plan["conditions"]:
        for seed in plan["seeds"]:
            completed += 1
            condition_name = str(condition["name"])
            config = dict(plan["base_config"])
            config.update(condition["overrides"])
            config["run.seed"] = int(seed)
            config = CORE_SCHEMA.validate(config)
            if progress:
                print(
                    f"[{completed}/{total}] condition={condition_name} seed={seed}",
                    flush=True,
                )
            try:
                summary = _run(config)
            except Exception as exc:
                failures.append(
                    {
                        "condition": condition_name,
                        "seed": seed,
                        "kind": "execution_error",
                        "error": f"{type(exc).__name__}:{exc}",
                    }
                )
                continue
            failures.extend(_validate_run(condition_name, seed, config, summary))
            runs.append(_compact(condition_name, seed, config, summary))

    reproducibility_condition, reproducibility_seed = _select_reproducibility_target(
        spec, plan
    )
    reference = next(
        (
            run
            for run in runs
            if run["condition"] == reproducibility_condition
            and run["seed"] == reproducibility_seed
        ),
        None,
    )
    repeated_checksum: str | None = None
    identical = False
    if reference is None:
        failures.append(
            {
                "condition": reproducibility_condition,
                "seed": reproducibility_seed,
                "kind": "reproducibility_reference_missing",
            }
        )
    else:
        target = next(
            condition
            for condition in plan["conditions"]
            if condition["name"] == reproducibility_condition
        )
        repeat_config = dict(plan["base_config"])
        repeat_config.update(target["overrides"])
        repeat_config["run.seed"] = reproducibility_seed
        repeated_summary = _run(CORE_SCHEMA.validate(repeat_config))
        repeated_checksum = result_checksum(repeated_summary)
        identical = repeated_checksum == reference["result_checksum"]
        if not identical:
            failures.append(
                {
                    "condition": reproducibility_condition,
                    "seed": reproducibility_seed,
                    "kind": "reproducibility_mismatch",
                }
            )

    expected_runs = total
    validation = {
        "passed": not failures and len(runs) == expected_runs,
        "failure_count": len(failures),
        "failures": failures,
        "expected_runs": expected_runs,
        "completed_runs": len(runs),
        "energy_tolerance": ENERGY_TOLERANCE,
        "resource_tolerance": RESOURCE_TOLERANCE,
        "reproducibility": {
            "condition": reproducibility_condition,
            "seed": reproducibility_seed,
            "reference_checksum": reference["result_checksum"] if reference else None,
            "repeat_checksum": repeated_checksum,
            "identical": identical,
        },
    }
    summary = summarize_runs(plan["name"], plan["conditions"], runs)
    return {
        "format": EXPERIMENT_CAMPAIGN_FORMAT,
        "world_contract_version": WORLD_CONTRACT_VERSION,
        "experiment": plan["name"],
        "description": plan["description"],
        "plan": plan,
        "runs": runs,
        "summary": summary,
        "validation": validation,
    }


def _write_dict_csv(path: Path, rows: list[Mapping[str, Any]]) -> None:
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_experiment_outputs(
    output_dir: Path,
    campaign: Mapping[str, Any],
    *,
    spec_path: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "campaign.json", campaign)
    write_json(output_dir / "summary.json", campaign["summary"])
    write_json(output_dir / "validation.json", campaign["validation"])
    write_summary_csv(output_dir / "runs.csv", campaign.get("runs", []))
    _write_dict_csv(
        output_dir / "comparison.csv",
        list(campaign["summary"].get("conditions", [])),
    )

    provenance = {
        "format": EXPERIMENT_PROVENANCE_FORMAT,
        "experiment": campaign["experiment"],
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "source_spec": str(spec_path),
        "source_spec_sha256": _file_sha256(spec_path),
        "repository": os.environ.get("GITHUB_REPOSITORY"),
        "source_commit": os.environ.get("GITHUB_SHA"),
        "source_branch": os.environ.get("GITHUB_REF_NAME"),
        "workflow": os.environ.get("GITHUB_WORKFLOW"),
        "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
    }
    write_json(output_dir / "provenance.json", provenance)

    names = (
        "campaign.json",
        "summary.json",
        "validation.json",
        "runs.csv",
        "comparison.csv",
        "provenance.json",
    )
    manifest = "".join(
        f"{_file_sha256(output_dir / name)}  {name}\n" for name in names
    )
    (output_dir / "SHA256SUMS.txt").write_text(manifest, encoding="utf-8")


def _run_command(args: argparse.Namespace) -> int:
    spec_path = Path(args.spec)
    spec = load_experiment_spec(spec_path)
    campaign = run_experiment(
        spec,
        seed_count_override=args.seed_count,
        seed_start_override=args.seed_start,
        ticks_override=args.ticks,
        progress=not args.quiet,
    )
    output_dir = Path(args.output_dir)
    write_experiment_outputs(output_dir, campaign, spec_path=spec_path)
    print(json.dumps(campaign["validation"], indent=2, sort_keys=True))
    print(json.dumps(campaign["summary"], indent=2, sort_keys=True))
    return 0 if campaign["validation"]["passed"] else 1


def _validate_command(args: argparse.Namespace) -> int:
    spec = load_experiment_spec(Path(args.spec))
    plan = build_experiment_plan(
        spec,
        seed_count_override=args.seed_count,
        seed_start_override=args.seed_start,
        ticks_override=args.ticks,
    )
    print(json.dumps(plan, indent=2, sort_keys=True))
    return 0


def _add_overrides(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--seed-count", type=int, default=None)
    parser.add_argument("--seed-start", type=int, default=None)
    parser.add_argument("--ticks", type=int, default=None)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run reproducible Melakat experiment specifications"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run an experiment campaign")
    run_parser.add_argument("spec", type=Path)
    run_parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/automated-experiments/latest"),
    )
    run_parser.add_argument("--quiet", action="store_true")
    _add_overrides(run_parser)

    validate_parser = subparsers.add_parser(
        "validate", help="Validate and expand an experiment specification"
    )
    validate_parser.add_argument("spec", type=Path)
    _add_overrides(validate_parser)

    args = parser.parse_args()
    if args.command == "run":
        raise SystemExit(_run_command(args))
    if args.command == "validate":
        raise SystemExit(_validate_command(args))
    raise SystemExit(2)


if __name__ == "__main__":
    main()
