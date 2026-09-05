from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Mapping

ParameterKind = Literal["integer", "number", "boolean", "choice"]


@dataclass(frozen=True)
class ParameterSpec:
    path: str
    label: str
    group: str
    kind: ParameterKind
    default: Any
    minimum: float | int | None = None
    maximum: float | int | None = None
    step: float | int = 1
    choices: tuple[str, ...] = ()
    description: str = ""
    advanced: bool = False

    def validate(self, value: Any) -> Any:
        if self.kind == "boolean":
            if not isinstance(value, bool):
                raise ValueError(f"{self.path} must be boolean")
            return value
        if self.kind == "choice":
            if value not in self.choices:
                raise ValueError(f"{self.path} must be one of {self.choices}")
            return value
        if self.kind == "integer":
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{self.path} must be integer")
        elif self.kind == "number":
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{self.path} must be numeric")
            value = float(value)
        if self.minimum is not None and value < self.minimum:
            raise ValueError(f"{self.path} is below minimum")
        if self.maximum is not None and value > self.maximum:
            raise ValueError(f"{self.path} is above maximum")
        return value


@dataclass(frozen=True)
class ParameterSchema:
    specs: tuple[ParameterSpec, ...]

    def defaults(self) -> dict[str, Any]:
        return {spec.path: spec.default for spec in self.specs}

    def validate(self, values: Mapping[str, Any]) -> dict[str, Any]:
        result = self.defaults()
        result.update(values)
        errors: dict[str, Any] = {}
        for spec in self.specs:
            try:
                result[spec.path] = spec.validate(result[spec.path])
            except ValueError as exc:
                errors[spec.path] = str(exc)
        if errors:
            raise ValueError(errors)
        return result

    def groups(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(spec.group for spec in self.specs))


CORE_SCHEMA = ParameterSchema(
    specs=(
        ParameterSpec(
            "run.engine_backend", "Engine backend", "Run", "choice", "phase-zero-vm",
            choices=("phase-zero-vm", "phase-two-vm", "demo"),
            description="Execution engine used by the GUI",
        ),
        ParameterSpec(
            "run.seed", "Seed", "Run", "integer", 1, 0, 2_147_483_647,
            description="Deterministic random seed",
        ),
        ParameterSpec("run.max_ticks", "Maximum ticks", "Run", "integer", 2000, 1, 10_000_000),
        ParameterSpec(
            "run.snapshot_interval", "History interval", "Run", "integer", 10, 1, 100_000,
            description="Interval for recorded metric history samples",
        ),
        ParameterSpec("world.width", "World width", "World", "integer", 100, 10, 10_000),
        ParameterSpec("world.height", "World height", "World", "integer", 70, 10, 10_000),
        ParameterSpec(
            "world.spatial_enabled", "Enable spatial rules", "World", "boolean", False,
            description="Enable Phase Two causal spatial rules; disabled preserves the Phase One control.",
            advanced=True,
        ),
        ParameterSpec(
            "world.boundary_model", "Boundary model", "World", "choice", "reflective",
            choices=("reflective", "toroidal"),
            description="Explicit rectangular boundary behavior for births and movement.",
            advanced=True,
        ),
        ParameterSpec(
            "world.offspring_dispersion_radius", "Offspring dispersion radius", "World", "number",
            1.0, 0.0, 10_000.0, 0.1,
            description="Maximum radial birth displacement from the parent.",
        ),
        ParameterSpec(
            "world.neighborhood_radius", "Neighborhood measurement radius", "World", "number",
            2.0, 0.0, 10_000.0, 0.1,
            description="Radius used for local-neighbor measurements and organism inspection.",
            advanced=True,
        ),
        ParameterSpec("world.memory_capacity", "Memory capacity", "World", "integer", 500, 1, 10_000_000),
        ParameterSpec(
            "world.initial_energy", "Initial energy pool", "World", "number", 1000.0,
            0.0, 1_000_000.0, 1.0,
        ),
        ParameterSpec(
            "world.energy_input_per_tick", "Energy input per tick", "World", "number", 10.0,
            0.0, 1_000_000.0, 0.1,
        ),
        ParameterSpec(
            "world.local_resources_enabled", "Enable local resource field", "Resources", "boolean", False,
            description=(
                "Route initial world energy and per-tick energy input through a spatial grid; organisms capture only from their current cell."
            ),
            advanced=True,
        ),
        ParameterSpec(
            "world.resource_grid_cols", "Resource grid columns", "Resources", "integer", 10, 1, 200,
            description="Measurement/resource cells across the world width.",
        ),
        ParameterSpec(
            "world.resource_grid_rows", "Resource grid rows", "Resources", "integer", 7, 1, 200,
            description="Measurement/resource cells across the world height.",
        ),
        ParameterSpec(
            "world.local_capture_limit", "Local capture limit", "Resources", "number", 1.0,
            0.0, 1_000_000.0, 0.1,
            description="Maximum energy an organism can capture from its current resource cell per tick.",
        ),
        ParameterSpec(
            "world.organism_actions_enabled", "Enable evolved sensing/movement", "Movement", "boolean", False,
            description="Enable Phase Two SENSE_RESOURCE, MOVE_X and MOVE_Y opcodes and their mutation alphabet.",
            advanced=True,
        ),
        ParameterSpec(
            "world.movement_max_step", "Maximum movement per instruction", "Movement", "number", 1.0,
            0.0, 1_000.0, 0.1,
            description="Absolute displacement cap for one MOVE_X or MOVE_Y instruction.",
        ),
        ParameterSpec(
            "world.movement_cost_per_unit", "Movement energy cost per unit", "Movement", "number", 0.1,
            0.0, 1_000_000.0, 0.01,
            description="Additional energy cost charged for realized movement distance.",
        ),
        ParameterSpec("population.initial_size", "Initial population", "Population", "integer", 12, 1, 10_000),
        ParameterSpec(
            "population.initial_energy", "Initial organism energy", "Population", "number", 25.0,
            0.0, 1_000_000.0, 0.1,
        ),
        ParameterSpec(
            "population.memory_per_organism", "Memory per organism", "Population", "integer", 8,
            1, 1_000_000,
        ),
        ParameterSpec(
            "population.max_age", "Maximum age (Demo only)", "Population", "integer", 500,
            1, 10_000_000, description="Not used by the Phase Zero baseline",
        ),
        ParameterSpec(
            "execution.instructions_per_tick", "Instructions per tick", "Execution", "integer", 8,
            1, 100_000,
        ),
        ParameterSpec(
            "execution.instruction_cost", "Instruction cost", "Execution", "number", 0.05,
            0.0, 1_000_000.0, 0.01,
        ),
        ParameterSpec(
            "execution.maintenance_cost", "Maintenance cost", "Execution", "number", 0.2,
            0.0, 1_000_000.0, 0.01,
        ),
        ParameterSpec(
            "reproduction.enabled", "Enable reproduction", "Reproduction", "boolean", True,
            description="Enable the Phase Zero division rule",
        ),
        ParameterSpec(
            "reproduction.threshold", "Reproduction threshold (reserved)", "Reproduction", "number", 35.0,
            0.0, 1_000_000.0, 0.1,
            description="Reserved for a future rule; not used by Phase Zero VM", advanced=True,
        ),
        ParameterSpec(
            "reproduction.cost", "Reproduction cost", "Reproduction", "number", 12.0,
            0.0, 1_000_000.0, 0.1,
        ),
        ParameterSpec(
            "reproduction.offspring_energy", "Offspring initial energy", "Reproduction", "number", 8.0,
            0.0, 1_000_000.0, 0.1,
        ),
        ParameterSpec(
            "reproduction.interval", "Reproduction interval (reserved)", "Reproduction", "integer", 25,
            1, 1_000_000,
            description="Reserved for a future rule; not used by Phase Zero VM", advanced=True,
        ),
        ParameterSpec(
            "mutation.substitution_rate", "Substitution rate", "Mutation", "number", 0.01,
            0.0, 1.0, 0.001,
        ),
        ParameterSpec(
            "visual.max_rendered_organisms", "Maximum rendered organisms", "Interface", "integer", 200,
            1, 10_000,
        ),
        ParameterSpec(
            "visual.show_organisms", "Show organisms", "Interface", "boolean", True,
            description="Render the organism layer in the desktop world view.",
        ),
        ParameterSpec(
            "visual.show_boundaries", "Show boundaries", "Interface", "boolean", True,
            description="Render the Phase Two world boundary layer.",
        ),
        ParameterSpec(
            "visual.show_resources", "Show resources", "Interface", "boolean", True,
            description="Render the local resource grid when present.",
        ),
    )
)
