from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from dataclasses import replace
from typing import Any, Iterator, Mapping

from . import experiment_runner
from .parameters import ParameterSchema, ParameterSpec
from .phase_five_contract import PHASE_FIVE_WORLD_CONTRACT_VERSION
from .phase_five_engine import PhaseFiveEngine

PHASE_FIVE_ENGINE_BACKEND = "phase-five-vm"
PHASE_FIVE_PARAMETER_DEFAULTS: dict[str, Any] = {
    "mutation.structural_event_rate": 0.0,
    "mutation.structural_duplication_probability": 0.5,
}
PHASE_FIVE_PARAMETERS = frozenset(PHASE_FIVE_PARAMETER_DEFAULTS)
PHASE_FIVE_COMPACT_METRICS = (
    "replication_copy_operations",
    "template_jump_operations",
    "genome_memory_used",
    "genome_length_mean",
    "genome_length_median",
    "genome_length_minimum",
    "genome_length_maximum",
    "genome_length_variance",
    "distinct_genome_lengths",
    "structural_event_rate",
    "structural_duplication_probability",
    "structural_rng_seed",
    "structural_mutation_operations",
    "structural_mutation_committed_operations",
    "structural_mutation_rejected_operations",
    "instruction_duplication_operations",
    "instruction_deletion_operations",
    "structural_length_delta_total",
    "variable_length_births",
    "variable_length_reproducing_offspring",
    "variable_length_active_population",
)
PHASE_FIVE_SUMMARY_METRICS = PHASE_FIVE_COMPACT_METRICS


def is_phase_five_spec(spec: Mapping[str, Any]) -> bool:
    base = spec.get("base_config", {})
    return isinstance(base, Mapping) and str(
        base.get("run.engine_backend", "phase-zero-vm")
    ) == PHASE_FIVE_ENGINE_BACKEND


def _with_phase_five_defaults(spec: Mapping[str, Any]) -> dict[str, Any]:
    result = deepcopy(dict(spec))
    base = dict(result.get("base_config", {}))
    if str(base.get("run.engine_backend", "phase-zero-vm")) == PHASE_FIVE_ENGINE_BACKEND:
        for key, value in PHASE_FIVE_PARAMETER_DEFAULTS.items():
            base.setdefault(key, value)
        result["base_config"] = base
    return result


def _phase_five_schema(original: ParameterSchema) -> ParameterSchema:
    specs: list[ParameterSpec] = []
    for spec in original.specs:
        if spec.path == "run.engine_backend":
            choices = tuple(dict.fromkeys((*spec.choices, PHASE_FIVE_ENGINE_BACKEND)))
            specs.append(replace(spec, choices=choices))
        else:
            specs.append(spec)
    specs.extend(
        (
            ParameterSpec(
                "mutation.structural_event_rate",
                "Structural event rate",
                "Mutation",
                "number",
                0.0,
                0.0,
                1.0,
                0.01,
                description=(
                    "Phase Five probability that one daughter proposal receives at most one length-changing event."
                ),
                advanced=True,
            ),
            ParameterSpec(
                "mutation.structural_duplication_probability",
                "Structural duplication probability",
                "Mutation",
                "number",
                0.5,
                0.0,
                1.0,
                0.05,
                description=(
                    "Conditional probability that an attempted Phase Five structural event is a tandem instruction duplication rather than a deletion."
                ),
                advanced=True,
            ),
        )
    )
    return ParameterSchema(tuple(specs))


def validate_phase_five_config(config: Mapping[str, Any]) -> None:
    if str(config.get("run.engine_backend", "")) != PHASE_FIVE_ENGINE_BACKEND:
        raise ValueError("phase_five_experiment_requires_phase_five_backend")
    for key in PHASE_FIVE_PARAMETERS:
        value = config.get(key, PHASE_FIVE_PARAMETER_DEFAULTS[key])
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{key}_must_be_numeric")
        if not 0.0 <= float(value) <= 1.0:
            raise ValueError(f"{key}_must_be_between_0_and_1")

    # The first Phase Five evidence gate intentionally isolates representation
    # and structural heredity in the homogeneous world inherited from Phase Zero.
    if bool(config.get("world.spatial_enabled", False)):
        raise ValueError("phase_five_initial_campaign_requires_nonspatial_world")
    if bool(config.get("world.local_resources_enabled", False)):
        raise ValueError("phase_five_initial_campaign_disables_local_resources")
    if bool(config.get("world.resource_sensing_enabled", False)):
        raise ValueError("phase_five_initial_campaign_disables_resource_sensing")
    if bool(config.get("world.movement_enabled", False)):
        raise ValueError("phase_five_initial_campaign_disables_movement")
    if bool(config.get("world.organism_actions_enabled", False)):
        raise ValueError("phase_five_initial_campaign_disables_organism_actions")


@contextmanager
def phase_five_experiment_support() -> Iterator[None]:
    """Temporarily extend the generic experiment runner for Phase Five."""

    original_schema = experiment_runner.CORE_SCHEMA
    original_known = experiment_runner.KNOWN_PARAMETERS
    original_supported = experiment_runner.SUPPORTED_ENGINES
    original_compact = experiment_runner.COMPACT_METRICS
    original_summary = experiment_runner.SUMMARY_METRICS
    original_world_contract = experiment_runner.WORLD_CONTRACT_VERSION
    original_engine_for = experiment_runner._engine_for
    original_load = experiment_runner.load_experiment_spec
    original_build = experiment_runner.build_experiment_plan

    phase_five_schema = _phase_five_schema(original_schema)

    def load_experiment_spec(path):
        spec = original_load(path)
        return _with_phase_five_defaults(spec)

    def engine_for(config, sink):
        if str(config["run.engine_backend"]) == PHASE_FIVE_ENGINE_BACKEND:
            validate_phase_five_config(config)
            return PhaseFiveEngine(dict(config), sink)
        return original_engine_for(config, sink)

    def build_experiment_plan(spec, **kwargs):
        normalized = _with_phase_five_defaults(spec)
        plan = original_build(normalized, **kwargs)
        validate_phase_five_config(plan["base_config"])
        for condition in plan["conditions"]:
            config = dict(plan["base_config"])
            config.update(condition["overrides"])
            config = experiment_runner.CORE_SCHEMA.validate(config)
            validate_phase_five_config(config)
        return plan

    experiment_runner.CORE_SCHEMA = phase_five_schema
    experiment_runner.KNOWN_PARAMETERS = original_known | PHASE_FIVE_PARAMETERS
    experiment_runner.SUPPORTED_ENGINES = original_supported | {PHASE_FIVE_ENGINE_BACKEND}
    experiment_runner.COMPACT_METRICS = tuple(
        dict.fromkeys((*original_compact, *PHASE_FIVE_COMPACT_METRICS))
    )
    experiment_runner.SUMMARY_METRICS = tuple(
        dict.fromkeys((*original_summary, *PHASE_FIVE_SUMMARY_METRICS))
    )
    experiment_runner.WORLD_CONTRACT_VERSION = PHASE_FIVE_WORLD_CONTRACT_VERSION
    experiment_runner._engine_for = engine_for
    experiment_runner.load_experiment_spec = load_experiment_spec
    experiment_runner.build_experiment_plan = build_experiment_plan

    try:
        yield
    finally:
        experiment_runner.CORE_SCHEMA = original_schema
        experiment_runner.KNOWN_PARAMETERS = original_known
        experiment_runner.SUPPORTED_ENGINES = original_supported
        experiment_runner.COMPACT_METRICS = original_compact
        experiment_runner.SUMMARY_METRICS = original_summary
        experiment_runner.WORLD_CONTRACT_VERSION = original_world_contract
        experiment_runner._engine_for = original_engine_for
        experiment_runner.load_experiment_spec = original_load
        experiment_runner.build_experiment_plan = original_build
