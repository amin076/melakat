from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from .analysis import enrich_summary

RUN_ARTIFACT_FORMAT = "melakat-run-artifact-0.1"
SPATIAL_RUN_ARTIFACT_FORMAT = "melakat-run-artifact-0.2"
SUPPORTED_RUN_ARTIFACT_FORMATS = (
    RUN_ARTIFACT_FORMAT,
    SPATIAL_RUN_ARTIFACT_FORMAT,
)

HISTORY_FIELDS = (
    "world_contract_version",
    "spatial_enabled",
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
    "ledger",
)

SUMMARY_FIELDS = (
    "control",
    "seed",
    "config_hash",
    "engine_version",
    "measurement_version",
    "world_contract_version",
    "spatial_enabled",
    "mutation_events",
    "lineage_count",
    "genotype_count",
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
    enriched_summary = enrich_summary(summary)
    world_contract_version = enriched_summary.get("world_contract_version")
    artifact_format = (
        SPATIAL_RUN_ARTIFACT_FORMAT
        if world_contract_version
        else RUN_ARTIFACT_FORMAT
    )
    artifact = {
        "format": artifact_format,
        "config_hash": config_hash(config),
        "config": dict(config),
        "engine_version": enriched_summary.get("engine_version"),
        "measurement_version": enriched_summary.get("measurement_version"),
        "summary": enriched_summary,
    }
    if world_contract_version:
        artifact["world_contract_version"] = world_contract_version
    return artifact


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
    path.parent.mkdir(parents=True, exist_ok=True)
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
    path.parent.mkdir(parents=True, exist_ok=True)
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


def load_run_artifact(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Run artifact must contain a JSON object")
    if payload.get("format") not in SUPPORTED_RUN_ARTIFACT_FORMATS:
        raise ValueError(
            "Unsupported run artifact format: "
            f"{payload.get('format')!r}"
        )
    config = payload.get("config")
    if not isinstance(config, dict):
        raise ValueError("Run artifact is missing its configuration")
    expected_hash = config_hash(config)
    if payload.get("config_hash") != expected_hash:
        raise ValueError(
            "Run artifact configuration hash does not match its configuration"
        )
    summary = payload.get("summary")
    aggregate = payload.get("aggregate")
    if not isinstance(summary, dict) and not isinstance(aggregate, dict):
        raise ValueError("Run artifact is missing its summary or aggregate")
    if payload.get("format") == SPATIAL_RUN_ARTIFACT_FORMAT:
        version = payload.get("world_contract_version")
        if not isinstance(version, str) or not version:
            raise ValueError(
                "Spatial run artifact is missing its world contract version"
            )
    return payload
