from __future__ import annotations

from copy import deepcopy
import random
from typing import Any, Callable

from .phase_three_contract import (
    PHASE_THREE_ATOMIC_MOVEMENT_ENGINE_VERSION,
    PHASE_THREE_ATOMIC_MOVEMENT_MEASUREMENT_VERSION,
    PHASE_THREE_ENGINE_VERSION,
    PHASE_THREE_MEASUREMENT_VERSION,
    PHASE_THREE_MOVEMENT_ENCODING_ENGINE_VERSION,
    PHASE_THREE_WORLD_CONTRACT_VERSION,
)
from .phase_two_engine import PhaseTwoEngine
from .phase_two_vm import (
    PhaseTwoOpcode,
    PhaseTwoVirtualMachine,
    mutate_phase_two_genome,
)
from .phase_zero_engine import PhaseZeroOrganism
from .protocol import make_event
from .spatial import apply_boundary
from .vm import Instruction

SUPPORTED_RESOURCE_DISTRIBUTIONS = {"uniform", "center_patch"}
MOVEMENT_OPCODES = {PhaseTwoOpcode.MOVE_X, PhaseTwoOpcode.MOVE_Y}


def mutate_phase_three_genome(
    genome: tuple[Instruction, ...],
    rng: random.Random,
    substitution_rate: float,
    *,
    sensing_enabled: bool,
    movement_enabled: bool,
    movement_step_rate: float,
) -> tuple[Instruction, ...]:
    """Phase Three mutation with an optional movement-step channel.

    Opcode substitution remains exactly the Phase Two implementation. When
    ``movement_step_rate`` is greater than zero, an instruction whose resulting
    opcode is ``MOVE_X`` or ``MOVE_Y`` can independently mutate its signed
    immediate to a unit step of -1 or +1. This intervention is disabled by
    default so accepted Phase Two and Phase Three 0.1 experiments retain their
    historical hereditary representation.
    """

    if not 0.0 <= movement_step_rate <= 1.0:
        raise ValueError("movement_step_rate must be between 0 and 1")

    mutated = mutate_phase_two_genome(
        genome,
        rng,
        substitution_rate,
        sensing_enabled=sensing_enabled,
        movement_enabled=movement_enabled,
    )
    if movement_step_rate <= 0.0:
        return mutated

    result: list[Instruction] = []
    for instruction in mutated:
        if (
            instruction.opcode in MOVEMENT_OPCODES
            and rng.random() < movement_step_rate
        ):
            current = int(instruction.b)
            choices = tuple(step for step in (-1, 1) if step != current)
            step = rng.choice(choices or (-1, 1))
            instruction = Instruction(
                opcode=instruction.opcode,  # type: ignore[arg-type]
                a=instruction.a,
                b=step,
            )
        result.append(instruction)
    return tuple(result)


class PhaseThreeEngine(PhaseTwoEngine):
    """Phase Three reference engine.

    Phase Three preserves the Phase Two VM, reproduction, spatial topology,
    resource capture, movement and accounting rules. The first intervention
    changes only how the same total initial and incoming local resource is
    allocated across the existing grid. Later optional interventions remain
    gated and default-off so earlier accepted experiments stay reproducible.
    """

    engine_version = PHASE_THREE_ENGINE_VERSION
    measurement_version = PHASE_THREE_MEASUREMENT_VERSION
    world_contract_version = PHASE_THREE_WORLD_CONTRACT_VERSION

    def __init__(
        self,
        config: dict[str, Any],
        emit: Callable[[dict[str, Any]], None],
    ):
        self.resource_distribution_mode = str(
            config.get("world.resource_distribution_mode", "uniform")
        )
        if self.resource_distribution_mode not in SUPPORTED_RESOURCE_DISTRIBUTIONS:
            raise ValueError(
                f"unsupported_resource_distribution:{self.resource_distribution_mode}"
            )

        self.resource_patch_fraction = float(
            config.get("world.resource_patch_fraction", 0.30)
        )
        self.resource_patch_contrast = float(
            config.get("world.resource_patch_contrast", 4.0)
        )
        if not 0.0 < self.resource_patch_fraction <= 1.0:
            raise ValueError("resource_patch_fraction_must_be_in_0_1")
        if self.resource_patch_contrast < 1.0:
            raise ValueError("resource_patch_contrast_must_be_at_least_one")

        self.movement_step_mutation_configured = (
            "mutation.movement_step_rate" in config
        )
        self.movement_step_mutation_rate = float(
            config.get("mutation.movement_step_rate", 0.0)
        )
        if not 0.0 <= self.movement_step_mutation_rate <= 1.0:
            raise ValueError("movement_step_rate must be between 0 and 1")

        self.atomic_movement_payment_configured = (
            "world.atomic_movement_payment_enabled" in config
        )
        self.atomic_movement_payment_enabled = bool(
            config.get("world.atomic_movement_payment_enabled", False)
        )
        self.movement_uncommitted_operations = 0
        self.movement_uncommitted_nonzero_operations = 0
        self.movement_uncommitted_distance = 0.0
        self.movement_uncommitted_execution_energy_batches = 0
        self.movement_uncommitted_movement_energy_batches = 0

        if self.movement_step_mutation_rate > 0.0:
            movement_alphabet_enabled = bool(
                config.get("world.movement_mutation_enabled", False)
                or config.get("world.movement_enabled", False)
                or config.get("world.organism_actions_enabled", False)
            )
            if not movement_alphabet_enabled:
                raise ValueError(
                    "movement_step_mutation_requires_movement_mutation"
                )
            if not bool(config.get("world.spatial_enabled", False)):
                raise ValueError("movement_step_mutation_requires_spatial")
            self.engine_version = PHASE_THREE_MOVEMENT_ENCODING_ENGINE_VERSION

        if self.atomic_movement_payment_enabled:
            if not bool(config.get("world.spatial_enabled", False)):
                raise ValueError("atomic_movement_payment_requires_spatial")
            movement_available = bool(
                config.get("world.movement_mutation_enabled", False)
                or config.get("world.movement_enabled", False)
                or config.get("world.organism_actions_enabled", False)
            )
            if not movement_available:
                raise ValueError("atomic_movement_payment_requires_movement")
            self.engine_version = PHASE_THREE_ATOMIC_MOVEMENT_ENGINE_VERSION
            self.measurement_version = PHASE_THREE_ATOMIC_MOVEMENT_MEASUREMENT_VERSION

        self.resource_weights: list[float] = []
        super().__init__(config, emit)

        if self.resource_distribution_mode != "uniform":
            if self.resource_field is None:
                raise ValueError(
                    "heterogeneous_resource_distribution_requires_local_resources"
                )
            self.resource_weights = self._build_center_patch_weights()
            self.resource_field.redistribute_weighted(self.resource_weights)
            # Replace the uniform initialization sample created by Phase Two with
            # the actual Phase Three starting state. No Phase Two code is changed.
            self.history = []
            self._record_history(force=True)

    def _try_reproduction(self, parent: PhaseZeroOrganism) -> bool:
        # Phase Two owns the accepted reproduction implementation. For the new
        # Phase Three representation intervention we precompute only the pending
        # child genome, then delegate every memory/energy/lineage/birth rule back
        # to the unchanged Phase Two path.
        if (
            self.movement_step_mutation_rate > 0.0
            and self.spatial_enabled
            and self.movement_mutation_enabled
            and bool(self.config["reproduction.enabled"])
            and parent.pending_child_genome is None
            and self.phase_two_vm_enabled
        ):
            parent.pending_child_genome = mutate_phase_three_genome(
                parent.genome,
                self.rng,
                float(self.config["mutation.substitution_rate"]),
                sensing_enabled=self.resource_sensing_mutation_enabled,
                movement_enabled=self.movement_mutation_enabled,
                movement_step_rate=self.movement_step_mutation_rate,
            )
        return super()._try_reproduction(parent)

    def _sense_resource_at(self, x: float, y: float) -> float:
        if self.resource_field is not None:
            return self.resource_field.at(x, y)
        return self.energy_pool

    def _record_uncommitted_movement(
        self,
        *,
        result: Any,
        reason: str,
    ) -> None:
        if result.movement_operations <= 0:
            return
        self.movement_uncommitted_operations += int(result.movement_operations)
        self.movement_uncommitted_nonzero_operations += int(
            result.movement_nonzero_operations
        )
        self.movement_uncommitted_distance += float(result.movement_distance)
        if reason == "execution_energy":
            self.movement_uncommitted_execution_energy_batches += 1
        elif reason == "movement_energy":
            self.movement_uncommitted_movement_energy_batches += 1
        self.emit(
            make_event(
                "movement_batch_uncommitted",
                reason=reason,
                movement_operations=int(result.movement_operations),
                movement_nonzero_operations=int(
                    result.movement_nonzero_operations
                ),
                movement_distance=round(float(result.movement_distance), 6),
            )
        )

    def _execute_one_atomic_movement(self, organism: PhaseZeroOrganism) -> None:
        """Run one organism with transactional movement world effects.

        The Phase Two VM is executed against a copied VM state and a shadow
        position. MOVE instructions can affect subsequent sensing/movement inside
        the same instruction budget through the shadow coordinates, but no
        position change, movement counter, boundary counter, or movement event is
        committed to the world until both aggregate execution energy and movement
        energy have been successfully charged.

        This is a Phase Three-only opt-in rule. The frozen Phase Two engine and
        historical Phase Three runs continue to use their accepted behavior.
        """

        self._capture_energy(organism)
        maintenance = float(self.config["execution.maintenance_cost"])
        if not self._charge(organism, maintenance, "energy_maintenance"):
            self._kill(organism, "energy_exhausted_maintenance")
            return
        if organism.vm_state.division_requested:
            self._try_reproduction(organism)
            return

        shadow_x = float(organism.x)
        shadow_y = float(organism.y)
        staged_moves: list[dict[str, Any]] = []

        def stage_move(axis: str, requested: float) -> tuple[float, int]:
            nonlocal shadow_x, shadow_y
            maximum_step = max(
                0.0,
                float(self.config["world.movement_max_step"]),
            )
            delta = max(-maximum_step, min(maximum_step, float(requested)))
            before_x, before_y = shadow_x, shadow_y

            if axis == "x":
                shadow_x, contacts = apply_boundary(
                    shadow_x + delta,
                    float(self.config["world.width"]),
                    self.boundary_model,
                )
            elif axis == "y":
                shadow_y, contacts = apply_boundary(
                    shadow_y + delta,
                    float(self.config["world.height"]),
                    self.boundary_model,
                )
            else:
                raise ValueError(f"invalid_movement_axis:{axis}")

            distance = abs(delta)
            staged_moves.append(
                {
                    "organism_id": organism.organism_id,
                    "axis": axis,
                    "requested": round(float(requested), 6),
                    "distance": round(distance, 6),
                    "from_x": round(before_x, 6),
                    "from_y": round(before_y, 6),
                    "x": round(shadow_x, 6),
                    "y": round(shadow_y, 6),
                    "boundary_contacts": contacts,
                }
            )
            return distance, contacts

        vm = PhaseTwoVirtualMachine(
            organism.genome,
            self.vm_config,
            deepcopy(organism.vm_state),
            sense_resource=lambda: self._sense_resource_at(shadow_x, shadow_y),
            move=stage_move,
            sensing_enabled=self.resource_sensing_enabled,
            movement_enabled=self.movement_enabled,
        )
        result = vm.run(int(self.config["execution.instructions_per_tick"]))

        # Read-only sensing and the instruction-attempt count retain the accepted
        # Phase Two accounting behavior. Movement world effects remain staged.
        self.resource_sense_operations += result.resource_sense_operations
        self.total_instructions_executed += result.instructions_executed

        execution_requested = (
            result.instructions_executed
            * float(self.config["execution.instruction_cost"])
        )
        if not self._charge(
            organism,
            execution_requested,
            "energy_execution",
        ):
            self._record_uncommitted_movement(
                result=result,
                reason="execution_energy",
            )
            self._kill(organism, "energy_exhausted_execution")
            return

        movement_requested = (
            float(result.movement_distance)
            * float(self.config["world.movement_cost_per_unit"])
        )
        if movement_requested > 0.0 and not self._charge(
            organism,
            movement_requested,
            "energy_movement",
        ):
            self._record_uncommitted_movement(
                result=result,
                reason="movement_energy",
            )
            self._kill(organism, "energy_exhausted_movement")
            return

        # All action costs have been paid. Commit the shadow VM/position and only
        # now publish movement as realized world behavior.
        organism.vm_state = vm.state
        organism.x = shadow_x
        organism.y = shadow_y
        self.movement_operations += result.movement_operations
        self.movement_nonzero_operations += result.movement_nonzero_operations
        self.movement_zero_step_operations += result.movement_zero_step_operations
        self.movement_distance += result.movement_distance
        self.boundary_contacts += result.boundary_contacts

        for movement in staged_moves:
            self.emit(make_event("organism_moved", **movement))

        if result.status == "fault":
            self._kill(organism, f"vm_fault:{result.fault}")
            return
        if result.status == "division_requested":
            self._try_reproduction(organism)

    def _execute_one(self, organism: PhaseZeroOrganism) -> None:
        if (
            not self.atomic_movement_payment_enabled
            or not self.movement_enabled
            or not self.phase_two_vm_enabled
        ):
            super()._execute_one(organism)
            return
        self._execute_one_atomic_movement(organism)

    def _build_center_patch_weights(self) -> list[float]:
        if self.resource_field is None:
            return []

        cols = self.resource_field.cols
        rows = self.resource_field.rows
        half_fraction = self.resource_patch_fraction / 2.0
        weights: list[float] = []
        inside_indices: list[int] = []
        closest_index = 0
        closest_distance = float("inf")

        for row in range(rows):
            y = (row + 0.5) / rows
            for col in range(cols):
                x = (col + 0.5) / cols
                index = row * cols + col
                dx = abs(x - 0.5)
                dy = abs(y - 0.5)
                distance = dx * dx + dy * dy
                if distance < closest_distance:
                    closest_distance = distance
                    closest_index = index
                inside = dx <= half_fraction and dy <= half_fraction
                if inside:
                    inside_indices.append(index)
                weights.append(self.resource_patch_contrast if inside else 1.0)

        # Very small patch fractions on coarse grids could otherwise select no
        # cell. Keep the intervention defined and deterministic by selecting the
        # single cell whose center is closest to the world center.
        if not inside_indices and weights:
            weights[closest_index] = self.resource_patch_contrast

        return weights

    def _resource_allocation_cv(self) -> float:
        """CV of the imposed renewal weights, not the evolving resource state."""

        if self.resource_distribution_mode == "uniform" or not self.resource_weights:
            return 0.0
        mean = sum(self.resource_weights) / len(self.resource_weights)
        if mean <= 0.0:
            return 0.0
        variance = sum(
            (weight - mean) ** 2 for weight in self.resource_weights
        ) / len(self.resource_weights)
        return variance ** 0.5 / mean

    def step(self) -> None:
        # The uniform Phase Three control deliberately delegates to the exact
        # Phase Two step path. Only heterogeneous renewal uses new dynamics.
        if self.resource_field is None or self.resource_distribution_mode == "uniform":
            super().step()
            return
        if self.finished:
            return
        maximum_ticks = int(self.config["run.max_ticks"])
        if self.tick >= maximum_ticks:
            self._finish("max_ticks")
            return

        self.tick += 1
        energy_input = float(self.config["world.energy_input_per_tick"])
        self.resource_field.renew_weighted(energy_input, self.resource_weights)
        self.ledger["energy_input"] += energy_input
        self.emit(
            make_event(
                "resource_renewed",
                amount=round(energy_input, 6),
                resource_total=round(self.resource_field.total(), 6),
                resource_distribution_mode=self.resource_distribution_mode,
            )
        )

        schedule = self._active()
        self.rng.shuffle(schedule)
        for organism in schedule:
            if organism.alive:
                organism.age += 1
                self._execute_one(organism)

        self.max_population = max(self.max_population, len(self._active()))
        self._record_history()
        if self.emit_snapshots:
            self.emit(
                make_event("tick", snapshot=self.snapshot(), metrics=self.metrics())
            )
        if self.tick >= maximum_ticks:
            self._finish("max_ticks")

    def snapshot(self) -> dict[str, Any]:
        snapshot = super().snapshot()
        snapshot["resource_distribution_mode"] = self.resource_distribution_mode
        if self.movement_step_mutation_configured:
            snapshot["movement_step_mutation_rate"] = round(
                self.movement_step_mutation_rate, 6
            )
        if self.atomic_movement_payment_configured:
            snapshot["atomic_movement_payment_enabled"] = (
                self.atomic_movement_payment_enabled
            )
        if self.resource_field is not None:
            snapshot["resource_distribution"] = {
                "mode": self.resource_distribution_mode,
                "patch_fraction": round(self.resource_patch_fraction, 6),
                "patch_contrast": round(self.resource_patch_contrast, 6),
                "allocation_cv": round(self._resource_allocation_cv(), 6),
            }
        return snapshot

    def metrics(self) -> dict[str, Any]:
        metrics = super().metrics()
        metrics["resource_distribution_mode"] = self.resource_distribution_mode
        metrics["resource_allocation_cv"] = round(
            self._resource_allocation_cv(), 6
        )
        if self.movement_step_mutation_configured:
            metrics["movement_step_mutation_rate"] = round(
                self.movement_step_mutation_rate, 6
            )
        if self.atomic_movement_payment_configured:
            metrics["atomic_movement_payment_enabled"] = (
                self.atomic_movement_payment_enabled
            )
        if self.atomic_movement_payment_enabled:
            metrics["movement_uncommitted_operations"] = (
                self.movement_uncommitted_operations
            )
            metrics["movement_uncommitted_nonzero_operations"] = (
                self.movement_uncommitted_nonzero_operations
            )
            metrics["movement_uncommitted_distance"] = round(
                self.movement_uncommitted_distance, 6
            )
            metrics["movement_uncommitted_execution_energy_batches"] = (
                self.movement_uncommitted_execution_energy_batches
            )
            metrics["movement_uncommitted_movement_energy_batches"] = (
                self.movement_uncommitted_movement_energy_batches
            )
        if self.resource_field is not None:
            # This is the observed resource-field state after organism capture,
            # death release and renewal. It is distinct from allocation_cv.
            metrics["resource_heterogeneity_cv"] = round(
                self.resource_field.coefficient_of_variation(), 6
            )
            metrics["local_resource_maximum"] = round(
                self.resource_field.maximum(), 6
            )
        else:
            metrics["resource_heterogeneity_cv"] = 0.0
            metrics["local_resource_maximum"] = 0.0
        return metrics
