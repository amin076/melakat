from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from typing import Any, Iterator, Mapping

from . import experiment_runner
from .phase_three_contract import PHASE_THREE_WORLD_CONTRACT_VERSION
from .phase_three_engine import PhaseThreeEngine, SUPPORTED_RESOURCE_DISTRIBUTIONS

PHASE_THREE_ENGINE_BACKEND = "phase-three-vm"
PHASE_THREE_PARAMETER_DEFAULTS: dict[str, Any] = {
    "world.resource_distribution_mode": "uniform",
    "world.resource_patch_fraction": 0.30,
    "world.resource_patch_contrast": 4.0,
}
PHASE_THREE_PARAMETERS = frozenset(PHASE_THREE_PARAMETER_DEFAULTS)
PHASE_THREE_COMPACT_METRICS = (
    "resource_distribution_mode",
    "resource_allocation_cv",
    "resource_heterogeneity_cv",
    "local_resource_maximum",
)
PHASE_THREE_SUMMARY_METRICS = (
    "resource_allocation_cv",
    "resource_heterogeneity_cv",
    "local_resource_maximum",
)


def is_phase_three_spec(spec: Mapping[str, Any]) -> bool:
    base = spec.get("base_config", {})
    return isinstance(base, Mapping) and str(
        base.get("run.engine_backend", "phase-zero-vm")
    ) == PHASE_THREE_ENGINE_BACKEND


def _with_phase_three_defaults(spec: Mapping[str, Any]) -> dict[str, Any]:
    result = deepcopy(dict(spec))
    base = dict(result.get("base_config", {}))
    if str(base.get("run.engine_backend", "phase-zero-vm")) == PHASE_THREE_ENGINE_BACKEND:
        for key, value in PHASE_THREE_PARAMETER_DEFAULTS.items():
            base.setdefault(key, value)
        result["base_config"] = base
    return result


def validate_phase_three_config(config: Mapping[str, Any]) -> None:
    backend = str(config.get("run.engine_backend", ""))
    if backend != PHASE_THREE_ENGINE_BACKEND:
        raise ValueError("phase_three_experiment_requires_phase_three_backend")

    mode = str(
        config.get(
            "world.resource_distribution_mode",
            PHASE_THREE_PARAMETER_DEFAULTS["world.resource_distribution_mode"],
        )
    )
    if mode not in SUPPORTED_RESOURCE_DISTRIBUTIONS:
        raise ValueError(f"unsupported_resource_distribution:{mode}")

    fraction = config.get(
        "world.resource_patch_fraction",
        PHASE_THREE_PARAMETER_DEFAULTS["world.resource_patch_fraction"],
    )
    if isinstance(fraction, bool) or not isinstance(fraction, (int, float)):
        raise ValueError("resource_patch_fraction_must_be_numeric")
    if not 0.0 < float(fraction) <= 1.0:
        raise ValueError("resource_patch_fraction_must_be_in_0_1")

    contrast = config.get(
        "world.resource_patch_contrast",
        PHASE_THREE_PARAMETER_DEFAULTS["world.resource_patch_contrast"],
    )
    if isinstance(contrast, bool) or not isinstance(contrast, (int, float)):
        raise ValueError("resource_patch_contrast_must_be_numeric")
    if float(contrast) < 1.0:
        raise ValueError("resource_patch_contrast_must_be_at_least_one")

    if mode != "uniform" and not bool(config.get("world.local_resources_enabled", False)):
        raise ValueError("heterogeneous_resource_distribution_requires_local_resources")
    if mode != "uniform" and not bool(config.get("world.spatial_enabled", False)):
        raise ValueError("heterogeneous_resource_distribution_requires_spatial")


@contextmanager
def phase_three_experiment_support() -> Iterator[None]:
    """Temporarily extend the generic experiment runner for Phase Three.

    The extension is scoped to a context so Phase Two globals/defaults are not
    permanently modified in-process. Phase Three-only defaults are injected
    only for Phase Three specs before plan/config hashing.
    """

    original_known = experiment_runner.KNOWN_PARAMETERS
    original_supported = experiment_runner.SUPPORTED_ENGINES
    original_compact = experiment_runner.COMPACT_METRICS
    original_summary = experiment_runner.SUMMARY_METRICS
    original_world_contract = experiment_runner.WORLD_CONTRACT_VERSION
    original_engine_for = experiment_runner._engine_for
    original_load = experiment_runner.load_experiment_spec
    original_build = experiment_runner.build_experiment_plan

    def load_experiment_spec(path):
        spec = original_load(path)
        return _with_phase_three_defaults(spec)

    def engine_for(config, sink):
        if str(config["run.engine_backend"]) == PHASE_THREE_ENGINE_BACKEND:
            validate_phase_three_config(config)
            return PhaseThreeEngine(dict(config), sink)
        return original_engine_for(config, sink)

    def build_experiment_plan(spec, **kwargs):
        normalized = _with_phase_three_defaults(spec)
        plan = original_build(normalized, **kwargs)
        validate_phase_three_config(plan["base_config"])
        for condition in plan["conditions"]:
            config = dict(plan["base_config"])
            config.update(condition["overrides"])
            config = experiment_runner.CORE_SCHEMA.validate(config)
            validate_phase_three_config(config)
        return plan

    experiment_runner.KNOWN_PARAMETERS = original_known | PHASE_THREE_PARAMETERS
    experiment_runner.SUPPORTED_ENGINES = original_supported | {PHASE_THREE_ENGINE_BACKEND}
    experiment_runner.COMPACT_METRICS = tuple(
        dict.fromkeys((*original_compact, *PHASE_THREE_COMPACT_METRICS))
    )
    experiment_runner.SUMMARY_METRICS = tuple(
        dict.fromkeys((*original_summary, *PHASE_THREE_SUMMARY_METRICS))
    )
    experiment_runner.WORLD_CONTRACT_VERSION = PHASE_THREE_WORLD_CONTRACT_VERSION
    experiment_runner._engine_for = engine_for
    experiment_runner.load_experiment_spec = load_experiment_spec
    experiment_runner.build_experiment_plan = build_experiment_plan

    try:
        yield
    finally:
        experiment_runner.KNOWN_PARAMETERS = original_known
        experiment_runner.SUPPORTED_ENGINES = original_supported
        experiment_runner.COMPACT_METRICS = original_compact
        experiment_runner.SUMMARY_METRICS = original_summary
        experiment_runner.WORLD_CONTRACT_VERSION = original_world_contract
        experiment_runner._engine_for = original_engine_for
        experiment_runner.load_experiment_spec = original_load
        experiment_runner.build_experiment_plan = original_build
