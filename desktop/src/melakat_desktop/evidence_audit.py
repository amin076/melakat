from __future__ import annotations

from collections import defaultdict
from typing import Any, Mapping


def audit_campaign(campaign: Mapping[str, Any]) -> dict[str, Any]:
    """Run archive-level consistency checks beyond the primary gate.

    These checks use only the compact archived campaign. They verify population
    accounting, non-negative final resources, version consistency, and exact
    agreement whenever the same effective configuration and seed appear in
    more than one control or sensitivity case.
    """

    expected_engine = campaign.get("engine_version")
    expected_measurement = campaign.get("measurement_version")

    population_accounting_failures = 0
    negative_energy_pool_failures = 0
    negative_free_memory_failures = 0
    version_mismatch_failures = 0
    duplicate_config_result_mismatches = 0
    audited_runs = 0

    grouped_checksums: dict[tuple[str, int], set[str]] = defaultdict(set)

    def audit_condition(condition: Mapping[str, Any]) -> None:
        nonlocal population_accounting_failures
        nonlocal negative_energy_pool_failures
        nonlocal negative_free_memory_failures
        nonlocal version_mismatch_failures
        nonlocal audited_runs

        config = condition.get("config")
        if not isinstance(config, Mapping):
            return

        memory_capacity = int(config.get("world.memory_capacity", 0))
        working_memory = int(config.get("population.memory_per_organism", 0))
        requested_initial = int(config.get("population.initial_size", 0))
        default_genome_length = 8
        allocation = working_memory + default_genome_length
        initial_population = (
            min(requested_initial, memory_capacity // allocation)
            if allocation > 0
            else 0
        )

        runs = condition.get("runs", [])
        if not isinstance(runs, list):
            return

        for run in runs:
            if not isinstance(run, Mapping):
                continue
            audited_runs += 1

            expected_population = (
                initial_population
                + int(run.get("births", 0))
                - int(run.get("deaths", 0))
            )
            if int(run.get("active_population", -1)) != expected_population:
                population_accounting_failures += 1

            if float(run.get("energy_pool", 0.0)) < 0.0:
                negative_energy_pool_failures += 1
            if int(run.get("free_memory", 0)) < 0:
                negative_free_memory_failures += 1

            if (
                run.get("engine_version") != expected_engine
                or run.get("measurement_version") != expected_measurement
            ):
                version_mismatch_failures += 1

            config_hash = run.get("config_hash")
            seed = run.get("seed")
            checksum = run.get("result_checksum")
            if (
                isinstance(config_hash, str)
                and seed is not None
                and isinstance(checksum, str)
            ):
                grouped_checksums[(config_hash, int(seed))].add(checksum)

    controls = campaign.get("controls", {})
    if isinstance(controls, Mapping):
        for condition in controls.values():
            if isinstance(condition, Mapping):
                audit_condition(condition)

    sweeps = campaign.get("sweeps", {})
    if isinstance(sweeps, Mapping):
        for group in sweeps.values():
            if not isinstance(group, Mapping):
                continue
            cases = group.get("cases", {})
            if not isinstance(cases, Mapping):
                continue
            for condition in cases.values():
                if isinstance(condition, Mapping):
                    audit_condition(condition)

    for checksums in grouped_checksums.values():
        if len(checksums) > 1:
            duplicate_config_result_mismatches += 1

    passed = (
        population_accounting_failures == 0
        and negative_energy_pool_failures == 0
        and negative_free_memory_failures == 0
        and version_mismatch_failures == 0
        and duplicate_config_result_mismatches == 0
    )

    return {
        "passed": passed,
        "audited_runs": audited_runs,
        "unique_config_seed_pairs": len(grouped_checksums),
        "population_accounting_failures": population_accounting_failures,
        "negative_energy_pool_failures": negative_energy_pool_failures,
        "negative_free_memory_failures": negative_free_memory_failures,
        "version_mismatch_failures": version_mismatch_failures,
        "duplicate_config_result_mismatches": (
            duplicate_config_result_mismatches
        ),
    }
