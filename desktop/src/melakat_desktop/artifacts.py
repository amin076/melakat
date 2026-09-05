from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

RUN_ARTIFACT_FORMAT = "melakat-run-artifact-0.1"

HISTORY_FIELDS = (
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
)

SUMMARY_FIELDS = (
    "seed",
    "config_hash",
    "engine_version",
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
)


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def config_hash(config: Mapping[str, Any]) -> str:
    digest = hashlib.sha256(canonical_json(dict(config)).encode("utf-8"))
    return digest.hexdigest()[:16]


def make_run_artifact(
    config: Mapping[str, Any],
    summary: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "format": RUN_ARTIFACT_FORMAT,
        "config_hash": config_hash(config),
        "config": dict(config),
        "engine_version": summary.get("engine_version"),
        "summary": dict(summary),
    }


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _csv_value(value: Any) -> Any:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return value


def write_summary_csv(
    path: Path,
    runs: Iterable[Mapping[str, Any]],
) -> None:
    rows = list(runs)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(SUMMARY_FIELDS))
        writer.writeheader()
        for run in rows:
            writer.writerow(
                {
                    field: _csv_value(run.get(field, ""))
                    for field in SUMMARY_FIELDS
                }
            )


def write_history_csv(
    path: Path,
    runs: Iterable[Mapping[str, Any]],
) -> None:
    fields = ("control", "seed", *HISTORY_FIELDS)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields))
        writer.writeheader()
        for run in runs:
            for sample in run.get("history", []):
                row = {
                    "control": run.get("control", ""),
                    "seed": run.get("seed", ""),
                }
                row.update(
                    {
                        field: _csv_value(sample.get(field, ""))
                        for field in HISTORY_FIELDS
                    }
                )
                writer.writerow(row)
