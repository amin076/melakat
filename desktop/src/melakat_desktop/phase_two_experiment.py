from __future__ import annotations

import argparse
import hashlib
import json
import time
import tracemalloc
from pathlib import Path
from typing import Any, Iterable, Mapping

from .artifacts import (
    canonical_json,
    config_hash,
    make_run_artifact,
    write_json,
    write_summary_csv,
)
from .parameters import CORE_SCHEMA
from .phase_two_engine import PhaseTwoEngine
from .world_contract import WORLD_CONTRACT_VERSION

EVIDENCE_CAMPAIGN_FORMAT = "melakat-phase-two-evidence-0.1"
ENERGY_TOLERANCE = 1e-7
RESOURCE_TOLERANCE = 1e-7

PHASE_TWO_CONDITIONS: dict[str, dict[str, Any]] = {
    "homogeneous_control": {
        "world.spatial_enabled": False,
        "world.local_resources_enabled": False,
        "world.organism_actions_enabled": False,
    },
    "spatial_only": {
        "world.spatial_enabled": True,
        "world.local_resources_enabled": False,
        "world.organism_actions_enabled": False,
    },
    "local_resource": {
        "world.spatial_enabled": True,
        "world.local_resources_enabled": True,
        "world.organism_actions_enabled": False,
    },
    "movement_enabled": {
        "world.spatial_enabled": True,
        "world.local_resources_enabled": True,
        "world.organism_actions_enabled": True,
    },
    "resource_abundant": {
        "world.spatial_enabled": True,
        "world.local_resources_enabled": True,
        "world.organism_actions_enabled": False,
        "world.energy_input_per_tick": 20.0,
    },
    "resource_limited": {
        "world.spatial_enabled": True,
        "world.local_resources_enabled": True,
        "world.organism_actions_enabled": False,
        "world.energy_input_per_tick": 5.0,
    },
    "small_world": {
        "world.spatial_enabled": True,
        "world.local_resources_enabled": True,
        "world.width": 50,
        "world.height": 35,
    },
    "large_world": {
        "world.spatial_enabled": True,
        "world.local_resources_enabled": True,
        "world.width": 200,
        "world.height": 140,
    },
    "reflective_boundary": {
        "world.spatial_enabled": True,
        "world.local_resources_enabled": True,
        "world.boundary_model": "reflective",
    },
    "toroidal_boundary": {
        "world.spatial_enabled": True,
        "world.local_resources_enabled": True,
        "world.boundary_model": "toroidal",
    },
    "movement_cost_zero": {
        "world.spatial_enabled": True,
        "world.local_resources_enabled": True,
        "world.organism_actions_enabled": True,
        "world.movement_cost_per_unit": 0.0,
    },
    "movement_cost_high": {
        "world.spatial_enabled": True,
        "world.local_resources_enabled": True,
        "world.organism_actions_enabled": True,
        "world.movement_cost_per_unit": 0.5,
    },
}


def result_checksum(summary: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json(summary).encode("utf-8")).hexdigest()


def _run(
    config: Mapping[str, Any],
    events: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    validated = CORE_SCHEMA.validate(config)
    sink = events.append if events is not None else (lambda _event: None)
    engine = PhaseTwoEngine(validated, sink)
    while not engine.finished:
        engine.step()
    return engine.summary()


def _compact(
    condition: str,
    seed: int,
    config: Mapping[str, Any],
    summary: Mapping[str, Any],
) -> dict[str, Any]:
    keys = (
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
    record = {
        "condition": condition,
        "seed": seed,
        "config_hash": config_hash(config),
        "result_checksum": result_checksum(summary),
    }
    record.update({key: summary.get(key) for key in keys if key in summary})
    return record


def _condition_config(
    base: Mapping[str, Any],
    condition: str,
    seed: int,
) -> dict[str, Any]:
    config = dict(base)
    config.update(PHASE_TWO_CONDITIONS[condition])
    config["run.seed"] = int(seed)
    return CORE_SCHEMA.validate(config)


def run_phase_two_matrix(
    base_config: Mapping[str, Any],
    *,
    seeds: Iterable[int],
) -> dict[str, Any]:
    seeds = [int(seed) for seed in seeds]
    if not seeds:
        raise ValueError("phase_two_matrix_requires_seeds")
    base = CORE_SCHEMA.validate(base_config)
    base["run.engine_backend"] = "phase-two-vm"
    base["run.emit_snapshots"] = False

    runs: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    max_energy_error = 0.0
    max_resource_error = 0.0
    for condition in PHASE_TWO_CONDITIONS:
        for seed in seeds:
            config = _condition_config(base, condition, seed)
            summary = _run(config)
            error = abs(float(summary.get("energy_balance_error", 0.0)))
            max_energy_error = max(max_energy_error, error)
            if error > ENERGY_TOLERANCE:
                failures.append(
                    {
                        "condition": condition,
                        "seed": seed,
                        "kind": "energy",
                        "error": error,
                    }
                )
            if bool(config.get("world.local_resources_enabled", False)):
                resource_error = abs(
                    float(summary.get("local_resource_balance_error", 0.0))
                )
                max_resource_error = max(max_resource_error, resource_error)
                if resource_error > RESOURCE_TOLERANCE:
                    failures.append(
                        {
                            "condition": condition,
                            "seed": seed,
                            "kind": "resource",
                            "error": resource_error,
                        }
                    )
                if float(summary.get("local_resource_minimum", 0.0)) < -1e-12:
                    failures.append(
                        {
                            "condition": condition,
                            "seed": seed,
                            "kind": "negative_resource",
                        }
                    )
            snapshot = summary.get("final_snapshot", {})
            width = float(config["world.width"])
            height = float(config["world.height"])
            for organism in snapshot.get("organisms", []):
                if not (
                    0.0 <= float(organism["x"]) <= width
                    and 0.0 <= float(organism["y"]) <= height
                ):
                    failures.append(
                        {
                            "condition": condition,
                            "seed": seed,
                            "kind": "out_of_bounds",
                            "organism_id": organism.get("id"),
                        }
                    )
                    break
            runs.append(_compact(condition, seed, config, summary))

    reproducibility_condition = "movement_enabled"
    reproducibility_seed = seeds[0]
    reproducibility_config = _condition_config(
        base,
        reproducibility_condition,
        reproducibility_seed,
    )
    reference = next(
        run
        for run in runs
        if run["condition"] == reproducibility_condition
        and run["seed"] == reproducibility_seed
    )
    repeated_summary = _run(reproducibility_config)
    repeated_checksum = result_checksum(repeated_summary)
    reproducibility_identical = repeated_checksum == reference["result_checksum"]
    if not reproducibility_identical:
        failures.append(
            {
                "condition": reproducibility_condition,
                "seed": reproducibility_seed,
                "kind": "reproducibility",
            }
        )

    expected_runs = len(PHASE_TWO_CONDITIONS) * len(seeds)
    validation = {
        "passed": not failures and len(runs) == expected_runs,
        "failure_count": len(failures),
        "failures": failures,
        "energy_tolerance": ENERGY_TOLERANCE,
        "resource_tolerance": RESOURCE_TOLERANCE,
        "max_abs_energy_balance_error": max_energy_error,
        "max_abs_local_resource_balance_error": max_resource_error,
        "expected_runs": expected_runs,
        "total_runs": len(runs),
        "condition_count": len(PHASE_TWO_CONDITIONS),
        "seed_count": len(seeds),
        "reproducibility": {
            "condition": reproducibility_condition,
            "seed": reproducibility_seed,
            "reference_checksum": reference["result_checksum"],
            "repeat_checksum": repeated_checksum,
            "identical": reproducibility_identical,
        },
    }
    return {
        "format": EVIDENCE_CAMPAIGN_FORMAT,
        "world_contract_version": WORLD_CONTRACT_VERSION,
        "base_config_hash": config_hash(base),
        "seed_count": len(seeds),
        "seeds": seeds,
        "condition_count": len(PHASE_TWO_CONDITIONS),
        "runs_per_condition": len(seeds),
        "conditions": PHASE_TWO_CONDITIONS,
        "runs": runs,
        "validation": validation,
    }


def performance_probe(config: Mapping[str, Any]) -> dict[str, Any]:
    validated = CORE_SCHEMA.validate(config)
    validated["run.engine_backend"] = "phase-two-vm"
    validated["run.emit_snapshots"] = False
    events: list[dict[str, Any]] = []

    tracemalloc.start()
    started = time.perf_counter()
    first = _run(validated, events)
    runtime = max(time.perf_counter() - started, 1e-12)
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    repeat = _run(validated)
    deterministic = result_checksum(first) == result_checksum(repeat)
    ticks = int(first.get("tick", 0))

    serialization_started = time.perf_counter()
    summary_bytes = canonical_json(first).encode("utf-8")
    snapshot_bytes = canonical_json(first.get("final_snapshot", {})).encode("utf-8")
    artifact_bytes = canonical_json(make_run_artifact(validated, first)).encode("utf-8")
    event_bytes = canonical_json(events).encode("utf-8")
    serialization_seconds = max(time.perf_counter() - serialization_started, 0.0)
    return {
        "runtime_seconds": runtime,
        "ticks": ticks,
        "ticks_per_second": ticks / runtime if ticks else 0.0,
        "peak_tracemalloc_bytes": int(peak),
        "event_count": len(events),
        "event_log_json_bytes": len(event_bytes),
        "summary_json_bytes": len(summary_bytes),
        "final_snapshot_json_bytes": len(snapshot_bytes),
        "artifact_json_bytes": len(artifact_bytes),
        "serialization_seconds": serialization_seconds,
        "deterministic_repeat": deterministic,
        "reference_checksum": result_checksum(first),
        "repeat_checksum": result_checksum(repeat),
    }


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_phase_two_evidence(
    output_dir: Path,
    campaign: Mapping[str, Any],
    performance: Mapping[str, Any],
    base_config: Mapping[str, Any],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "campaign.json", campaign)
    write_json(output_dir / "validation.json", campaign["validation"])
    write_json(output_dir / "performance.json", performance)
    write_json(
        output_dir / "base-config.json",
        {
            "format": "melakat-phase-two-base-config-0.1",
            "config_hash": config_hash(base_config),
            "config": dict(base_config),
        },
    )
    write_summary_csv(output_dir / "runs.csv", campaign.get("runs", []))

    manifest_names = (
        "campaign.json",
        "validation.json",
        "performance.json",
        "base-config.json",
        "runs.csv",
    )
    manifest = "".join(
        f"{_file_sha256(output_dir / name)}  {name}\n"
        for name in manifest_names
    )
    (output_dir / "SHA256SUMS.txt").write_text(manifest, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the Melakat Phase Two evidence matrix"
    )
    parser.add_argument("--runs", type=int, default=30, help="Seeds per condition")
    parser.add_argument("--ticks", type=int, default=2000, help="Ticks per run")
    parser.add_argument("--seed-start", type=int, default=1)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/phase-two/evidence-gate"),
    )
    args = parser.parse_args()

    base = CORE_SCHEMA.defaults()
    base["run.engine_backend"] = "phase-two-vm"
    base["run.max_ticks"] = args.ticks
    base["run.emit_snapshots"] = False
    base = CORE_SCHEMA.validate(base)
    seeds = range(args.seed_start, args.seed_start + args.runs)
    campaign = run_phase_two_matrix(base, seeds=seeds)

    performance_config = dict(base)
    performance_config.update(
        {
            "world.spatial_enabled": True,
            "world.local_resources_enabled": True,
            "world.organism_actions_enabled": True,
            "run.seed": args.seed_start,
        }
    )
    performance = performance_probe(performance_config)
    write_phase_two_evidence(args.output_dir, campaign, performance, base)
    print(json.dumps(campaign["validation"], indent=2, sort_keys=True))
    print(json.dumps(performance, indent=2, sort_keys=True))
    if (
        not campaign["validation"]["passed"]
        or not performance["deterministic_repeat"]
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
