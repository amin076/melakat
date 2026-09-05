from __future__ import annotations

import json
from collections import Counter, defaultdict
from typing import Any, Mapping


SUMMARY_METRICS = (
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


def _canonical(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def analyze_summary(summary: Mapping[str, Any]) -> dict[str, Any]:
    genealogy = [
        dict(record)
        for record in summary.get("genealogy", [])
    ]
    catalog = {
        record.get("genome_hash"): dict(record)
        for record in summary.get("genotype_catalog", [])
        if record.get("genome_hash")
    }
    by_id = {
        record.get("organism_id"): record
        for record in genealogy
        if record.get("organism_id") is not None
    }
    final_tick = int(summary.get("tick", 0))

    lineages: dict[Any, dict[str, Any]] = {}
    genotypes: dict[str, dict[str, Any]] = {}
    mutation_pairs: Counter[tuple[str, str]] = Counter()

    for record in genealogy:
        lineage_id = record.get("lineage_id")
        lineage = lineages.setdefault(
            lineage_id,
            {
                "lineage_id": lineage_id,
                "organism_count": 0,
                "births": 0,
                "deaths": 0,
                "active_count": 0,
                "root_count": 0,
                "first_birth_tick": None,
                "last_birth_tick": None,
                "last_death_tick": None,
                "max_generation": 0,
            },
        )
        birth_tick = int(record.get("birth_tick", 0))
        death_tick = record.get("death_tick")
        lineage["organism_count"] += 1
        lineage["births"] += 1
        lineage["first_birth_tick"] = (
            birth_tick
            if lineage["first_birth_tick"] is None
            else min(lineage["first_birth_tick"], birth_tick)
        )
        lineage["last_birth_tick"] = (
            birth_tick
            if lineage["last_birth_tick"] is None
            else max(lineage["last_birth_tick"], birth_tick)
        )
        lineage["max_generation"] = max(
            lineage["max_generation"],
            int(record.get("generation", 0)),
        )
        if record.get("parent_id") is None:
            lineage["root_count"] += 1
        if death_tick is None:
            lineage["active_count"] += 1
        else:
            lineage["deaths"] += 1
            lineage["last_death_tick"] = (
                int(death_tick)
                if lineage["last_death_tick"] is None
                else max(lineage["last_death_tick"], int(death_tick))
            )

        genome_hash = record.get("genome_hash")
        if not genome_hash:
            continue
        genotype = genotypes.setdefault(
            genome_hash,
            {
                "genome_hash": genome_hash,
                "organism_count": 0,
                "births": 0,
                "deaths": 0,
                "active_count": 0,
                "mutated_births": 0,
                "first_birth_tick": None,
                "last_birth_tick": None,
                "last_death_tick": None,
                "first_seen_tick": catalog.get(genome_hash, {}).get(
                    "first_seen_tick"
                ),
                "last_seen_tick": None,
                "parent_genome_hashes": set(),
                "genome": catalog.get(genome_hash, {}).get("genome", []),
            },
        )
        genotype["organism_count"] += 1
        genotype["births"] += 1
        genotype["first_birth_tick"] = (
            birth_tick
            if genotype["first_birth_tick"] is None
            else min(genotype["first_birth_tick"], birth_tick)
        )
        genotype["last_birth_tick"] = (
            birth_tick
            if genotype["last_birth_tick"] is None
            else max(genotype["last_birth_tick"], birth_tick)
        )
        genotype["last_seen_tick"] = max(
            genotype["last_seen_tick"] or 0,
            birth_tick,
            int(death_tick) if death_tick is not None else final_tick,
        )
        if death_tick is None:
            genotype["active_count"] += 1
        else:
            genotype["deaths"] += 1
            genotype["last_death_tick"] = (
                int(death_tick)
                if genotype["last_death_tick"] is None
                else max(genotype["last_death_tick"], int(death_tick))
            )

        parent_id = record.get("parent_id")
        parent = by_id.get(parent_id)
        parent_hash = parent.get("genome_hash") if parent else None
        if parent_hash and parent_hash != genome_hash:
            genotype["mutated_births"] += 1
            genotype["parent_genome_hashes"].add(parent_hash)
            mutation_pairs[(parent_hash, genome_hash)] += 1

    for genotype in genotypes.values():
        genotype["parent_genome_hashes"] = sorted(
            genotype["parent_genome_hashes"]
        )
        first_seen = genotype["first_seen_tick"]
        last_seen = genotype["last_seen_tick"]
        genotype["observed_lifetime_ticks"] = (
            None
            if first_seen is None or last_seen is None
            else max(0, last_seen - first_seen)
        )

    mutation_map = [
        {
            "parent_genome_hash": parent_hash,
            "child_genome_hash": child_hash,
            "events": count,
        }
        for (parent_hash, child_hash), count in sorted(mutation_pairs.items())
    ]
    analysis = {
        "lineages": [
            lineages[lineage_id]
            for lineage_id in sorted(lineages, key=lambda value: str(value))
        ],
        "genotypes": [
            genotypes[genome_hash]
            for genome_hash in sorted(genotypes)
        ],
        "mutation_events": sum(mutation_pairs.values()),
        "mutation_map": mutation_map,
        "death_reasons": dict(summary.get("death_reasons", {})),
    }
    return analysis


def enrich_summary(summary: Mapping[str, Any]) -> dict[str, Any]:
    enriched = dict(summary)
    analysis = analyze_summary(enriched)
    enriched["analysis"] = analysis
    enriched["mutation_events"] = analysis["mutation_events"]
    enriched["lineage_count"] = len(analysis["lineages"])
    enriched["genotype_count"] = len(analysis["genotypes"])
    return enriched


def _comparison_summary(artifact: Mapping[str, Any]) -> Mapping[str, Any]:
    summary = artifact.get("summary")
    if isinstance(summary, Mapping):
        return summary
    aggregate = artifact.get("aggregate")
    if isinstance(aggregate, Mapping):
        return aggregate
    return {}

def compare_artifacts(
    first: Mapping[str, Any],
    second: Mapping[str, Any],
) -> dict[str, Any]:
    first_config = dict(first.get("config", {}))
    second_config = dict(second.get("config", {}))
    config_keys = sorted(set(first_config) | set(second_config))
    config_differences = [
        {
            "key": key,
            "first": first_config.get(key),
            "second": second_config.get(key),
        }
        for key in config_keys
        if first_config.get(key) != second_config.get(key)
    ]

    first_summary = _comparison_summary(first)
    second_summary = _comparison_summary(second)
    metric_differences = [
        {
            "metric": metric,
            "first": first_summary.get(metric),
            "second": second_summary.get(metric),
        }
        for metric in SUMMARY_METRICS
        if first_summary.get(metric) != second_summary.get(metric)
    ]
    return {
        "same_artifact": _canonical(first) == _canonical(second),
        "same_config": not config_differences,
        "same_config_except_seed": (
            bool(config_differences)
            and all(item["key"] == "run.seed" for item in config_differences)
        ),
        "config_differences": config_differences,
        "metric_differences": metric_differences,
        "first": {
            "config_hash": first.get("config_hash"),
            "seed": first_config.get("run.seed"),
        },
        "second": {
            "config_hash": second.get("config_hash"),
            "seed": second_config.get("run.seed"),
        },
    }
