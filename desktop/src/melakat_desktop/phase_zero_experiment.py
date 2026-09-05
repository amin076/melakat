from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any, Iterable

from .artifacts import (
    RUN_ARTIFACT_FORMAT,
    config_hash,
    write_history_csv,
    write_json,
    write_summary_csv,
)
from .parameters import CORE_SCHEMA
from .phase_zero_engine import PhaseZeroEngine


CONTROL_PRESETS: dict[str, dict[str, Any]] = {
    "baseline": {},
    "mutation_zero": {
        "mutation.substitution_rate": 0.0,
    },
    "abundant_energy": {
        "world.energy_input_per_tick": 1_000.0,
    },
    "abundant_memory": {
        "world.memory_capacity": 1_000_000,
    },
    "maintenance_zero": {
        "execution.maintenance_cost": 0.0,
    },
}


def run_single(config: dict[str, Any], seed: int) -> dict[str, Any]:
    run_config = dict(config)
    run_config["run.seed"] = seed
    run_config["run.emit_snapshots"] = False
    run_config = CORE_SCHEMA.validate(run_config)
    engine = PhaseZeroEngine(run_config, lambda _event: None)
    while not engine.finished:
        engine.step()
    summary = engine.summary()
    summary.pop("final_snapshot", None)
    summary["seed"] = seed
    summary["config_hash"] = config_hash(run_config)
    return summary


def run_replicates(
    config: dict[str, Any],
    seeds: Iterable[int],
) -> list[dict[str, Any]]:
    return [run_single(config, seed) for seed in seeds]


def aggregate(runs: list[dict[str, Any]]) -> dict[str, Any]:
    if not runs:
        return {"runs": 0}

    return {
        "runs": len(runs),
        "extinction_runs": sum(
            run["active_population"] == 0 for run in runs
        ),
        "mean_final_population": mean(
            run["active_population"] for run in runs
        ),
        "mean_births": mean(run["births"] for run in runs),
        "mean_deaths": mean(run["deaths"] for run in runs),
        "mean_max_population": mean(
            run["max_population"] for run in runs
        ),
        "mean_active_genotypes": mean(
            run["active_genotypes"] for run in runs
        ),
        "mean_historical_genotypes": mean(
            run["historical_genotypes"] for run in runs
        ),
        "mean_blocked_divisions": mean(
            run["blocked_divisions"] for run in runs
        ),
        "mean_waiting_for_memory": mean(
            run["waiting_for_memory"] for run in runs
        ),
        "mean_waiting_for_energy": mean(
            run["waiting_for_energy"] for run in runs
        ),
        "mean_faults": mean(run["faults"] for run in runs),
        "mean_energy_balance_abs_error": mean(
            abs(run["energy_balance_error"]) for run in runs
        ),
    }


def run_control_suite(
    base_config: dict[str, Any],
    seeds: Iterable[int],
) -> dict[str, dict[str, Any]]:
    seed_values = tuple(seeds)
    results: dict[str, dict[str, Any]] = {}
    for name, overrides in CONTROL_PRESETS.items():
        config = dict(base_config)
        config.update(overrides)
        runs = run_replicates(config, seed_values)
        for run in runs:
            run["control"] = name
        results[name] = {
            "config": config,
            "config_hash": config_hash(config),
            "aggregate": aggregate(runs),
            "runs": runs,
        }
    return results


def _flatten_control_runs(
    controls: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        run
        for control in controls.values()
        for run in control["runs"]
    ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run headless Melakat Phase Zero replicates."
    )
    parser.add_argument("--runs", type=int, default=30)
    parser.add_argument("--ticks", type=int, default=2_000)
    parser.add_argument("--seed-start", type=int, default=1)
    parser.add_argument("--controls", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--summary-csv", type=Path)
    parser.add_argument("--history-csv", type=Path)
    args = parser.parse_args()

    if args.runs < 1:
        parser.error("--runs must be positive")
    if args.ticks < 1:
        parser.error("--ticks must be positive")

    config = CORE_SCHEMA.defaults()
    config["run.max_ticks"] = args.ticks
    seeds = range(args.seed_start, args.seed_start + args.runs)

    if args.controls:
        controls = run_control_suite(config, seeds)
        all_runs = _flatten_control_runs(controls)
        payload: dict[str, Any] = {
            "format": RUN_ARTIFACT_FORMAT,
            "experiment": "phase-zero-control-suite",
            "config": config,
            "config_hash": config_hash(config),
            "controls": controls,
        }
    else:
        runs = run_replicates(config, seeds)
        for run in runs:
            run["control"] = "baseline"
        all_runs = runs
        payload = {
            "format": RUN_ARTIFACT_FORMAT,
            "experiment": "phase-zero-baseline",
            "config": config,
            "config_hash": config_hash(config),
            "aggregate": aggregate(runs),
            "runs": runs,
        }

    if args.output:
        write_json(args.output, payload)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))

    if args.summary_csv:
        write_summary_csv(args.summary_csv, all_runs)
    if args.history_csv:
        write_history_csv(args.history_csv, all_runs)


if __name__ == "__main__":
    main()
