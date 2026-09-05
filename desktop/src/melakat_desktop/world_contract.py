from __future__ import annotations

from typing import Any, Mapping

WORLD_CONTRACT_VERSION = "phase-two-spatial-0.7"
PHASE_TWO_ENGINE_VERSION = "phase-two-vm-0.7"
PHASE_TWO_MEASUREMENT_VERSION = "phase-two-measurement-0.1"
SPATIAL_PLACEMENT_COMPAT_VERSION = "phase-two-spatial-0.2"
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
    "measurement_version": PHASE_TWO_MEASUREMENT_VERSION,
    "coordinate_system": {
        "dimensions": 2,
        "unit": "abstract_world_unit",
        "x_domain": "0 <= x <= world.width",
        "y_domain": "0 <= y <= world.height",
        "homogeneous_control": (
            "When world.spatial_enabled=false all causal Phase Two mechanisms are disabled "
            "and the frozen Phase One scientific state is reproduced."
        ),
    },
    "observation_model": "sequential",
    "environment_update": "once_at_tick_start",
    "tick_order": [
        "environment_energy_input_or_uniform_local_resource_renewal",
        "active_schedule_shuffle",
        "organism_age_increment",
        "global_or_local_energy_capture",
        "maintenance_cost",
        "pending_division_retry_or_vm_execution",
        "phase_two_sensing_or_bounded_movement_if_enabled",
        "execution_cost",
        "movement_cost",
        "fault_or_energy_death",
        "division_attempt",
        "history_snapshot_and_finish",
    ],
    "boundary_models": {
        "reflective": "continuous reflection at rectangular bounds",
        "toroidal": "continuous wrap at rectangular bounds",
    },
    "offspring_placement_model": "local_radial_dispersion",
    "movement_model": {
        "enabled_by": "world.organism_actions_enabled",
        "opcodes": ["SENSE_RESOURCE", "MOVE_X", "MOVE_Y"],
        "maximum_effect": "world.movement_max_step per movement instruction",
        "cost": "world.movement_cost_per_unit times realized path distance",
    },
    "local_resource_model": {
        "enabled_by": "world.local_resources_enabled",
        "mechanism": "uniform-renewal grid with local capture",
        "initialization": "world.initial_energy distributed uniformly over all cells",
        "renewal": "world.energy_input_per_tick distributed uniformly once at tick start",
        "capture": "organism current cell only, capped by world.local_capture_limit",
        "death_release": "remaining organism energy returns to its current resource cell",
        "diffusion": "not implemented",
        "organism_production": "not implemented",
    },
    "spatial_randomness": {
        "offspring_stream": "offspring-placement-v1",
        "placement_compatibility_version": SPATIAL_PLACEMENT_COMPAT_VERSION,
        "independent_from_engine_rng": True,
        "legacy_engine_rng_position_draws_preserved": True,
    },
    "precision_and_conservation": {
        "energy_internal": "python_float_unrounded",
        "serialized_values": "rounded_for_output_only",
        "energy_balance_tolerance": 1e-7,
        "local_resource_balance_tolerance": 1e-7,
        "memory": "exact_nonnegative_integer_units",
    },
    "phase_two_exit_evidence": {
        "matrix": "matching multi-seed controls for space, resources, boundaries, movement cost, and scale",
        "performance": "runtime, ticks/sec, tracemalloc peak, event volume, summary size, deterministic repeat",
        "ui": "schema-driven controls plus organism/boundary/resource layers and local organism context",
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
            if key == "measurement_version" and item == PHASE_TWO_MEASUREMENT_VERSION:
                result[key] = BASELINE_MEASUREMENT_VERSION
                continue
            result[key] = _baseline_normalize(item)
        return result
    if isinstance(value, list):
        return [_baseline_normalize(item) for item in value]
    if isinstance(value, tuple):
        return [_baseline_normalize(item) for item in value]
    return value


def scientific_baseline_projection(summary: Mapping[str, Any]) -> dict[str, Any]:
    """Project disabled-spatial Phase Two output onto the frozen Phase One state."""

    projected = _baseline_normalize(summary, root=True)
    assert isinstance(projected, dict)
    return projected
