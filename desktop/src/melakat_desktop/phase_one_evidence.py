from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from .artifacts import canonical_json, config_hash, write_json
from .parameters import CORE_SCHEMA
from .phase_zero_experiment import (
    CONTROL_PRESETS,
    SENSITIVITY_SWEEPS,
    aggregate,
    load_config_file,
    run_replicates,
    run_single,
)

EVIDENCE_CAMPAIGN_FORMAT = "melakat-phase-one-evidence-0.1"
ENERGY_BALANCE_TOLERANCE = 1e-7
DEFAULT_RUNS_PER_CONDITION = 30
DEFAULT_MAX_TICKS = 2_000

REQUIRED_CONTROL_NAMES = (
    "baseline",
    "mutation_zero",
    "abundant_energy",
    "abundant_memory",
    "maintenance_zero",
    "reproduction_cost_zero",
)

COMPACT_RUN_FIELDS = (
    "control",
    "seed",
    "config_hash",
    "engine_version",
    "measurement_version",
    "tick",
    "active_population",
    "births",
    "deaths",
    "max_population",
    "active_genotypes",
    "historical_genotypes",
    "active_lineages",
    "lineage_count",
    "genotype_count",
    "mutation_events",
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
    "death_reasons",
    "ledger",
)


def result_checksum(run: Mapping[str, Any]) -> str:
    """Checksum the complete scientific result, excluding campaign labels.

    The detailed history, genealogy, genotype catalog, and analysis remain part
    of the checksum even though they are omitted from the compact campaign
    archive. This lets a detailed rerun be verified against the archived
    evidence record without committing every large per-run payload.
    """

    payload = {
        key: value
        for key, value in run.items()
        if key not in {"control", "result_checksum"}
    }
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def compact_run_record(run: Mapping[str, Any]) -> dict[str, Any]:
    record = {field: run.get(field) for field in COMPACT_RUN_FIELDS}
    record["result_checksum"] = result_checksum(run)
    return record


def _effective_run_config(
    condition_config: Mapping[str, Any],
    seed: int,
) -> dict[str, Any]:
    """Validate a run without injecting defaults added after its archive.

    Phase One artifacts are historical records. Later schema growth, such as
    the Phase Two spatial switch, must not retroactively change their
    configuration hashes. Values are validated against the current schema,
    then projected back to the exact key set that existed in the archived
    condition plus the two runtime keys used by the Phase One runner.
    """

    run_config = dict(condition_config)
    run_config["run.seed"] = seed
    run_config["run.emit_snapshots"] = False
    validated = CORE_SCHEMA.validate(run_config)
    return {key: validated[key] for key in run_config}


def _run_condition(
    config: dict[str, Any],
    seeds: tuple[int, ...],
    label: str,
) -> dict[str, Any]:
    full_runs = run_replicates(config, seeds)
    for run in full_runs:
        run["control"] = label
    compact_runs = [compact_run_record(run) for run in full_runs]
    return {
        "config": dict(config),
        "config_hash": config_hash(config),
        "aggregate": aggregate(full_runs),
        "runs": compact_runs,
    }


def run_evidence_campaign(
    base_config: dict[str, Any],
    seeds: Iterable[int],
) -> dict[str, Any]:
    validated_base = CORE_SCHEMA.validate(dict(base_config))
    if validated_base.get("run.engine_backend") != "phase-zero-vm":
        raise ValueError(
            "Phase One evidence campaign requires "
            "run.engine_backend=phase-zero-vm"
        )

    seed_values = tuple(int(seed) for seed in seeds)
    if not seed_values:
        raise ValueError("Phase One evidence campaign requires at least one seed")
    if len(set(seed_values)) != len(seed_values):
        raise ValueError("Phase One evidence campaign seed list must be unique")

    controls: dict[str, dict[str, Any]] = {}
    for name in REQUIRED_CONTROL_NAMES:
        overrides = CONTROL_PRESETS[name]
        condition_config = dict(validated_base)
        condition_config.update(overrides)
        controls[name] = _run_condition(
            condition_config,
            seed_values,
            name,
        )

    sweeps: dict[str, dict[str, Any]] = {}
    for parameter, values in SENSITIVITY_SWEEPS.items():
        cases: dict[str, dict[str, Any]] = {}
        for value in values:
            condition_config = dict(validated_base)
            condition_config[parameter] = value
            label = f"{parameter}={value}"
            condition = _run_condition(
                condition_config,
                seed_values,
                label,
            )
            condition["parameter"] = parameter
            condition["value"] = value
            cases[str(value)] = condition
        sweeps[parameter] = {"cases": cases}

    first_seed = seed_values[0]
    repeated = run_single(validated_base, first_seed)
    repeated["control"] = "baseline"
    baseline_record = controls["baseline"]["runs"][0]
    repeat_checksum = result_checksum(repeated)
    reproducibility = {
        "seed": first_seed,
        "reference_checksum": baseline_record["result_checksum"],
        "repeat_checksum": repeat_checksum,
        "identical": repeat_checksum == baseline_record["result_checksum"],
    }

    payload: dict[str, Any] = {
        "format": EVIDENCE_CAMPAIGN_FORMAT,
        "engine_version": baseline_record.get("engine_version"),
        "measurement_version": baseline_record.get("measurement_version"),
        "base_config": validated_base,
        "base_config_hash": config_hash(validated_base),
        "seed_list": list(seed_values),
        "protocol": {
            "runs_per_condition": len(seed_values),
            "energy_balance_tolerance": ENERGY_BALANCE_TOLERANCE,
            "expected_control_conditions": len(REQUIRED_CONTROL_NAMES),
            "expected_sensitivity_parameters": len(SENSITIVITY_SWEEPS),
            "expected_cases_per_parameter": 3,
            "detailed_result_policy": (
                "Compact metrics are archived; each compact record stores a "
                "SHA-256 checksum of the complete enriched run summary, "
                "including history, genealogy, genotype catalog, and analysis."
            ),
        },
        "controls": controls,
        "sweeps": sweeps,
        "reproducibility_check": reproducibility,
    }
    payload["validation"] = validate_campaign(payload)
    return payload


def _iter_conditions(
    campaign: Mapping[str, Any],
) -> Iterable[tuple[str, Mapping[str, Any]]]:
    controls = campaign.get("controls", {})
    if isinstance(controls, Mapping):
        for name, condition in controls.items():
            if isinstance(condition, Mapping):
                yield f"control:{name}", condition

    sweeps = campaign.get("sweeps", {})
    if isinstance(sweeps, Mapping):
        for parameter, group in sweeps.items():
            if not isinstance(group, Mapping):
                continue
            cases = group.get("cases", {})
            if not isinstance(cases, Mapping):
                continue
            for value, condition in cases.items():
                if isinstance(condition, Mapping):
                    yield f"sweep:{parameter}={value}", condition


def validate_campaign(campaign: Mapping[str, Any]) -> dict[str, Any]:
    protocol = campaign.get("protocol", {})
    if not isinstance(protocol, Mapping):
        protocol = {}
    tolerance = float(
        protocol.get("energy_balance_tolerance", ENERGY_BALANCE_TOLERANCE)
    )
    seeds = tuple(int(seed) for seed in campaign.get("seed_list", []))
    expected_seed_set = set(seeds)
    expected_runs = int(protocol.get("runs_per_condition", len(seeds)))

    controls = campaign.get("controls", {})
    controls = controls if isinstance(controls, Mapping) else {}
    sweeps = campaign.get("sweeps", {})
    sweeps = sweeps if isinstance(sweeps, Mapping) else {}

    missing_controls = sorted(set(REQUIRED_CONTROL_NAMES) - set(controls))
    extra_controls = sorted(set(controls) - set(REQUIRED_CONTROL_NAMES))

    sensitivity_cases = 0
    malformed_sweep_parameters = 0
    for group in sweeps.values():
        if not isinstance(group, Mapping):
            malformed_sweep_parameters += 1
            continue
        cases = group.get("cases", {})
        if not isinstance(cases, Mapping):
            malformed_sweep_parameters += 1
            continue
        sensitivity_cases += len(cases)
        if len(cases) != 3:
            malformed_sweep_parameters += 1

    energy_failures = 0
    memory_failures = 0
    seed_coverage_failures = 0
    run_count_failures = 0
    config_hash_failures = 0
    checksum_failures = 0
    tick_failures = 0
    total_runs = 0
    max_abs_energy_error = 0.0

    for _name, condition in _iter_conditions(campaign):
        runs = condition.get("runs", [])
        if not isinstance(runs, list):
            run_count_failures += 1
            continue
        total_runs += len(runs)
        if len(runs) != expected_runs:
            run_count_failures += 1
        run_seed_set = {
            int(run.get("seed"))
            for run in runs
            if isinstance(run, Mapping) and run.get("seed") is not None
        }
        if run_seed_set != expected_seed_set:
            seed_coverage_failures += 1

        condition_config = condition.get("config")
        if isinstance(condition_config, Mapping):
            expected_condition_hash = config_hash(condition_config)
            if condition.get("config_hash") != expected_condition_hash:
                config_hash_failures += 1
            memory_capacity = int(
                condition_config.get("world.memory_capacity", 0)
            )
            expected_tick = int(condition_config.get("run.max_ticks", 0))
        else:
            memory_capacity = 0
            expected_tick = 0

        for run in runs:
            if not isinstance(run, Mapping):
                run_count_failures += 1
                continue
            error = abs(float(run.get("energy_balance_error", float("inf"))))
            max_abs_energy_error = max(max_abs_energy_error, error)
            if error > tolerance:
                energy_failures += 1

            if memory_capacity and int(run.get("memory_used", 0)) > memory_capacity:
                memory_failures += 1

            if expected_tick and int(run.get("tick", -1)) != expected_tick:
                tick_failures += 1

            checksum = run.get("result_checksum")
            if (
                not isinstance(checksum, str)
                or len(checksum) != 64
                or any(char not in "0123456789abcdef" for char in checksum)
            ):
                checksum_failures += 1

            if isinstance(condition_config, Mapping) and run.get("seed") is not None:
                effective = _effective_run_config(
                    condition_config,
                    int(run["seed"]),
                )
                if run.get("config_hash") != config_hash(effective):
                    config_hash_failures += 1

    reproducibility = campaign.get("reproducibility_check")
    reproducibility_failure = bool(
        isinstance(reproducibility, Mapping)
        and not reproducibility.get("identical", False)
    )

    structure_ok = (
        campaign.get("format") == EVIDENCE_CAMPAIGN_FORMAT
        and not missing_controls
        and not extra_controls
        and len(sweeps) == 9
        and sensitivity_cases == 27
        and malformed_sweep_parameters == 0
        and bool(seeds)
        and len(set(seeds)) == len(seeds)
    )
    passed = (
        structure_ok
        and energy_failures == 0
        and memory_failures == 0
        and seed_coverage_failures == 0
        and run_count_failures == 0
        and config_hash_failures == 0
        and checksum_failures == 0
        and tick_failures == 0
        and not reproducibility_failure
    )

    return {
        "passed": passed,
        "control_conditions": len(controls),
        "sensitivity_parameters": len(sweeps),
        "sensitivity_cases": sensitivity_cases,
        "total_runs": total_runs,
        "seed_count": len(seeds),
        "missing_controls": missing_controls,
        "extra_controls": extra_controls,
        "malformed_sweep_parameters": malformed_sweep_parameters,
        "energy_invariant_failures": energy_failures,
        "memory_invariant_failures": memory_failures,
        "seed_coverage_failures": seed_coverage_failures,
        "run_count_failures": run_count_failures,
        "config_hash_failures": config_hash_failures,
        "result_checksum_failures": checksum_failures,
        "tick_failures": tick_failures,
        "reproducibility_failure": reproducibility_failure,
        "max_abs_energy_balance_error": max_abs_energy_error,
        "energy_balance_tolerance": tolerance,
    }


def _csv_value(value: Any) -> Any:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return value


def write_campaign_files(output_dir: Path, campaign: Mapping[str, Any]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    campaign_path = output_dir / "campaign.json"
    validation_path = output_dir / "validation.json"
    config_path = output_dir / "base-config.json"
    runs_path = output_dir / "runs.csv"

    write_json(campaign_path, campaign)
    write_json(validation_path, campaign.get("validation", {}))
    write_json(
        config_path,
        {
            "format": "melakat-config-0.1",
            "config_hash": campaign.get("base_config_hash"),
            "config": campaign.get("base_config", {}),
        },
    )

    fields = (
        "section",
        "parameter",
        "value",
        *COMPACT_RUN_FIELDS,
        "result_checksum",
    )
    with runs_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields))
        writer.writeheader()
        controls = campaign.get("controls", {})
        if isinstance(controls, Mapping):
            for condition in controls.values():
                if not isinstance(condition, Mapping):
                    continue
                for run in condition.get("runs", []):
                    row = {
                        "section": "control",
                        "parameter": "",
                        "value": "",
                    }
                    row.update(
                        {
                            field: _csv_value(run.get(field, ""))
                            for field in (*COMPACT_RUN_FIELDS, "result_checksum")
                        }
                    )
                    writer.writerow(row)

        sweeps = campaign.get("sweeps", {})
        if isinstance(sweeps, Mapping):
            for parameter, group in sweeps.items():
                if not isinstance(group, Mapping):
                    continue
                cases = group.get("cases", {})
                if not isinstance(cases, Mapping):
                    continue
                for value, condition in cases.items():
                    if not isinstance(condition, Mapping):
                        continue
                    for run in condition.get("runs", []):
                        row = {
                            "section": "sensitivity",
                            "parameter": parameter,
                            "value": value,
                        }
                        row.update(
                            {
                                field: _csv_value(run.get(field, ""))
                                for field in (
                                    *COMPACT_RUN_FIELDS,
                                    "result_checksum",
                                )
                            }
                        )
                        writer.writerow(row)

    checksums: list[str] = []
    for path in (campaign_path, validation_path, config_path, runs_path):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        checksums.append(f"{digest}  {path.name}")
    (output_dir / "SHA256SUMS.txt").write_text(
        "\n".join(checksums) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run and archive the Melakat Phase One evidence gate."
    )
    parser.add_argument("--runs", type=int, default=DEFAULT_RUNS_PER_CONDITION)
    parser.add_argument("--ticks", type=int, default=DEFAULT_MAX_TICKS)
    parser.add_argument("--seed-start", type=int, default=1)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    if args.runs < 1:
        parser.error("--runs must be positive")
    if args.ticks < 1:
        parser.error("--ticks must be positive")

    if args.config:
        try:
            base_config = load_config_file(args.config)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            parser.error(str(exc))
    else:
        base_config = CORE_SCHEMA.defaults()

    base_config["run.max_ticks"] = args.ticks
    seeds = range(args.seed_start, args.seed_start + args.runs)

    print(
        "Running Phase One evidence campaign: "
        f"{args.runs} seeds, {len(REQUIRED_CONTROL_NAMES)} controls, "
        f"{len(SENSITIVITY_SWEEPS)} sensitivity parameters."
    )
    campaign = run_evidence_campaign(base_config, seeds)
    write_campaign_files(args.output_dir, campaign)
    validation = campaign["validation"]
    print(json.dumps(validation, indent=2, sort_keys=True))
    if not validation["passed"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
