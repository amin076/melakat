from __future__ import annotations

from typing import Any, Mapping

WORLD_CONTRACT_VERSION = "phase-two-spatial-0.1"
PHASE_TWO_ENGINE_VERSION = "phase-two-vm-0.1"
BASELINE_ENGINE_VERSION = "phase-zero-vm-0.2"
BASELINE_MEASUREMENT_VERSION = "phase-one-measurement-0.1"
BASELINE_SEED = 1
BASELINE_CONFIG_HASH = "7d6516f717c33885"
BASELINE_SCIENTIFIC_SHA256 = (
    "ffafec2384fff475494f706163c2c59ee59c19ff71b4492f2778a231f033b13a"
)
BASELINE_SNAPSHOT_SHA256 = (
    "594d01654ac43d06245b18556b08394773cb848f62fdfd108a1f6abbf4eef112"
)

PHASE_TWO_WORLD_CONTRACT: dict[str, Any] = {
    "version": WORLD_CONTRACT_VERSION,
    "engine_version": PHASE_TWO_ENGINE_VERSION,
    "coordinate_system": {
        "dimensions": 2,
        "unit": "abstract_world_unit",
        "x_domain": "0 <= x <= world.width",
        "y_domain": "0 <= y <= world.height",
        "phase_one_semantics": (
            "Coordinates are inherited baseline state only; with spatial rules "
            "disabled they do not affect execution, resources, reproduction, or death."
        ),
    },
    "observation_model": "sequential",
    "environment_update": "once_at_tick_start",
    "tick_order": [
        "environment_update",
        "active_schedule_shuffle",
        "organism_age_increment",
        "global_energy_capture",
        "maintenance_cost",
        "pending_division_retry_or_vm_execution",
        "execution_cost",
        "fault_or_energy_death",
        "division_attempt",
        "history_snapshot_and_finish",
    ],
    "boundary_model": "inactive_when_spatial_disabled",
    "movement_model": "not_implemented_in_p2_1",
    "local_resource_model": "not_implemented_in_p2_1",
    "resource_precision": {
        "energy_internal": "python_float_unrounded",
        "energy_output": "rounded_for_serialization_only",
        "energy_balance_tolerance": 1e-7,
        "memory": "exact_nonnegative_integer_units",
    },
    "baseline_compatibility": {
        "engine_version": BASELINE_ENGINE_VERSION,
        "measurement_version": BASELINE_MEASUREMENT_VERSION,
        "seed": BASELINE_SEED,
        "config_hash": BASELINE_CONFIG_HASH,
        "scientific_sha256": BASELINE_SCIENTIFIC_SHA256,
        "final_snapshot_sha256": BASELINE_SNAPSHOT_SHA256,
    },
}

_NEW_METADATA_KEYS = {"world_contract_version", "spatial_enabled"}


def _baseline_normalize(value: Any, *, root: bool = False) -> Any:
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if key in _NEW_METADATA_KEYS:
                continue
            if key == "config_hash":
                if root:
                    continue
                result[key] = BASELINE_CONFIG_HASH
                continue
            if key == "engine_version" and item == PHASE_TWO_ENGINE_VERSION:
                result[key] = BASELINE_ENGINE_VERSION
                continue
            result[key] = _baseline_normalize(item)
        return result
    if isinstance(value, list):
        return [_baseline_normalize(item) for item in value]
    if isinstance(value, tuple):
        return [_baseline_normalize(item) for item in value]
    return value


def scientific_baseline_projection(summary: Mapping[str, Any]) -> dict[str, Any]:
    """Project a P2.1 disabled-spatial result onto the frozen Phase One state.

    Only configuration/version metadata introduced by P2.1 is normalized.
    Scientific state, history, genealogy, genotype records, VM state,
    coordinates, resource ledger, and final snapshot remain checksum-covered.
    """

    projected = _baseline_normalize(summary, root=True)
    assert isinstance(projected, dict)
    return projected
