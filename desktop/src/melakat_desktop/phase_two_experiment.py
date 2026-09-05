from __future__ import annotations

import argparse
import json
import time
import tracemalloc
from pathlib import Path
from typing import Any, Iterable, Mapping

from .artifacts import canonical_json, config_hash, write_json, write_summary_csv
from .parameters import CORE_SCHEMA
from .phase_two_engine import PhaseTwoEngine
from .world_contract import WORLD_CONTRACT_VERSION


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


def _run(config: Mapping[str, Any], events: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    validated = CORE_SCHEMA.validate(config)
    sink = events.append if events is not None else (lambda _event: None)
    engine = PhaseTwoEngine(validated, sink)
    while not engine.finished:
        engine.step()
    return engine.summary()


def _compact(condition: str, seed: int, config: Mapping[str, Any], summary: Mapping[str, Any]) -> dict[str, Any]:
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
    }
    record.update({key: summary.get(key) for key in keys if key in summary})
    return record


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
    for condition, overrides in PHASE_TWO_CONDITIONS.items():
        for seed in seeds:
            config = dict(base)
            config.update(overrides)
            config["run.seed"] = seed
            config = CORE_SCHEMA.validate(config)
            summary = _run(config)
            error = abs(float(summary.get("energy_balance_error", 0.0)))
            if error > 1e-7:
                failures.append({"condition": condition, "seed": seed, "kind": "energy", "error": error})
            if bool(config.get("world.local_resources_enabled", False)):
                resource_error = abs(float(summary.get("local_resource_balance_error", 0.0)))
                if resource_error > 1e-7:
                    failures.append(
                        {"condition": condition, "seed": seed, "kind": "resource", "error": resource_error}
                    )
                if float(summary.get("local_resource_minimum", 0.0)) < -1e-12:
                    failures.append(
                        {"condition": condition, "seed": seed, "kind": "negative_resource"}
                    )
            snapshot = summary.get("final_snapshot", {})
            width = float(config["world.width"])
            height = float(config["world.height"])
            for organism in snapshot.get("organisms", []):
                if not (0.0 <= float(organism["x"]) <= width and 0.0 <= float(organism["y"]) <= height):
                    failures.append(
                        {"condition": condition, "seed": seed, "kind": "out_of_bounds", "organism_id": organism.get("id")}
                    )
                    break
            runs.append(_compact(condition, seed, config, summary))

    return {
        "format": "melakat-phase-two-evidence-0.1",
        "world_contract_version": WORLD_CONTRACT_VERSION,
        "seed_count": len(seeds),
        "seeds": seeds,
        "condition_count": len(PHASE_TWO_CONDITIONS),
        "runs_per_condition": len(seeds),
        "runs": runs,
        "validation": {
            "passed": not failures,
            "failure_count": len(failures),
            "failures": failures,
            "energy_tolerance": 1e-7,
            "resource_tolerance": 1e-7,
        },
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
    deterministic = canonical_json(first) == canonical_json(repeat)
    ticks = int(first.get("tick", 0))
    encoded = canonical_json(first).encode("utf-8")
    return {
        "runtime_seconds": runtime,
        "ticks": ticks,
        "ticks_per_second": ticks / runtime if ticks else 0.0,
        "peak_tracemalloc_bytes": int(peak),
        "event_count": len(events),
        "summary_json_bytes": len(encoded),
        "deterministic_repeat": deterministic,
    }


def write_phase_two_evidence(output_dir: Path, campaign: Mapping[str, Any], performance: Mapping[str, Any]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "campaign.json", campaign)
    write_json(output_dir / "performance.json", performance)
    write_summary_csv(output_dir / "runs.csv", campaign.get("runs", []))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Melakat Phase Two evidence matrix")
    parser.add_argument("--runs", type=int, default=30, help="Seeds per condition")
    parser.add_argument("--ticks", type=int, default=2000, help="Ticks per run")
    parser.add_argument("--seed-start", type=int, default=1)
    parser.add_argument("--output-dir", type=Path, default=Path("results/phase-two/evidence-gate"))
    args = parser.parse_args()

    base = CORE_SCHEMA.defaults()
    base["run.engine_backend"] = "phase-two-vm"
    base["run.max_ticks"] = args.ticks
    base["run.emit_snapshots"] = False
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
    write_phase_two_evidence(args.output_dir, campaign, performance)
    print(json.dumps(campaign["validation"], indent=2, sort_keys=True))
    print(json.dumps(performance, indent=2, sort_keys=True))
    if not campaign["validation"]["passed"] or not performance["deterministic_repeat"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
