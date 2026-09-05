from __future__ import annotations

import math
import random
from typing import Any, Callable

from .phase_two_vm import PhaseTwoVirtualMachine, mutate_phase_two_genome
from .phase_zero_engine import PhaseZeroEngine, PhaseZeroOrganism, mutate_genome
from .protocol import make_event
from .resources import LocalResourceField
from .spatial import (
    SPATIAL_RNG_STREAM,
    SUPPORTED_BOUNDARIES,
    apply_boundary,
    derive_spatial_seed,
    local_neighbor_count,
    local_radial_position,
    population_spatial_metrics,
)
from .vm import VirtualMachine
from .world_contract import (
    PHASE_TWO_MEASUREMENT_VERSION,
    SPATIAL_PLACEMENT_COMPAT_VERSION,
    WORLD_CONTRACT_VERSION,
)


class PhaseTwoEngine(PhaseZeroEngine):
    """Serial Phase Two reference engine.

    The homogeneous path remains the frozen Phase One control. Spatial mode can
    independently enable local birth placement, a conservative local resource
    field, and evolved sensing/movement primitives. No fitness function, social
    rule, diffusion, attack, cooperation, or machine-learning objective exists.
    """

    engine_version = "phase-two-vm-0.7"
    measurement_version = PHASE_TWO_MEASUREMENT_VERSION
    world_contract_version = WORLD_CONTRACT_VERSION

    def __init__(
        self,
        config: dict[str, Any],
        emit: Callable[[dict[str, Any]], None],
    ):
        self.spatial_enabled = bool(config.get("world.spatial_enabled", False))
        self.local_resources_enabled = bool(
            config.get("world.local_resources_enabled", False)
        )
        self.organism_actions_enabled = bool(
            config.get("world.organism_actions_enabled", False)
        )
        self.boundary_model = str(config.get("world.boundary_model", "reflective"))
        if self.spatial_enabled and self.boundary_model not in SUPPORTED_BOUNDARIES:
            raise ValueError(f"unsupported_boundary_model:{self.boundary_model}")
        if self.local_resources_enabled and not self.spatial_enabled:
            raise ValueError("local_resources_require_spatial")
        if self.organism_actions_enabled and not self.spatial_enabled:
            raise ValueError("organism_actions_require_spatial")

        self.boundary_contacts = 0
        self.resource_sense_operations = 0
        self.movement_operations = 0
        self.movement_distance = 0.0
        self.resource_field: LocalResourceField | None = None
        self.spatial_rng_seed = derive_spatial_seed(
            int(config["run.seed"]),
            SPATIAL_PLACEMENT_COMPAT_VERSION,
        )
        self.spatial_rng = random.Random(self.spatial_rng_seed)
        super().__init__(config, emit)
        if self.organism_actions_enabled:
            self.ledger.setdefault("energy_movement", 0.0)

        if self.local_resources_enabled:
            self.resource_field = LocalResourceField(
                width=float(self.config["world.width"]),
                height=float(self.config["world.height"]),
                cols=int(self.config["world.resource_grid_cols"]),
                rows=int(self.config["world.resource_grid_rows"]),
            )
            self.resource_field.seed_uniform(self.energy_pool)
            self.energy_pool = 0.0
            self.history = []
            self._record_history(force=True)

    def _spatial_distance(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
    ) -> float:
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        if self.boundary_model == "toroidal":
            width = float(self.config["world.width"])
            height = float(self.config["world.height"])
            dx = min(dx, max(0.0, width - dx))
            dy = min(dy, max(0.0, height - dy))
        return math.hypot(dx, dy)

    def _try_reproduction(self, parent: PhaseZeroOrganism) -> bool:
        if not self.spatial_enabled:
            return super()._try_reproduction(parent)
        if not bool(self.config["reproduction.enabled"]):
            self._set_reproduction_block_reason(parent, "disabled")
            return False

        if parent.pending_child_genome is None:
            if self.organism_actions_enabled:
                parent.pending_child_genome = mutate_phase_two_genome(
                    parent.genome,
                    self.rng,
                    float(self.config["mutation.substitution_rate"]),
                )
            else:
                parent.pending_child_genome = mutate_genome(
                    parent.genome,
                    self.rng,
                    float(self.config["mutation.substitution_rate"]),
                )

        child_genome = parent.pending_child_genome
        allocation = self._allocation_for_genome(child_genome)
        free_memory = self._free_memory()
        if free_memory < allocation:
            self._set_reproduction_block_reason(
                parent,
                "memory",
                free_memory=free_memory,
            )
            return False

        reproduction_cost = float(self.config["reproduction.cost"])
        offspring_energy = float(self.config["reproduction.offspring_energy"])
        total_required = reproduction_cost + offspring_energy
        if parent.energy < total_required:
            self._set_reproduction_block_reason(parent, "energy")
            return False

        parent.energy -= total_required
        self.ledger["energy_reproduction_cost"] += reproduction_cost
        self.ledger["energy_transferred_to_offspring"] += offspring_energy

        parent_hash = self.genome_hash(parent.genome)
        child_hash = self._record_genotype(child_genome, self.tick)
        mutated = child_hash != parent_hash
        if mutated:
            lineage_id = self.next_lineage
            self.next_lineage += 1
        else:
            lineage_id = parent.lineage_id

        width = float(self.config["world.width"])
        height = float(self.config["world.height"])
        self.rng.uniform(0, width)
        self.rng.uniform(0, height)
        child_x, child_y, contacts = local_radial_position(
            parent_x=parent.x,
            parent_y=parent.y,
            radius=float(self.config["world.offspring_dispersion_radius"]),
            width=width,
            height=height,
            rng=self.spatial_rng,
            boundary_model=self.boundary_model,
        )
        self.boundary_contacts += contacts

        child = PhaseZeroOrganism(
            organism_id=self.next_id,
            parent_id=parent.organism_id,
            lineage_id=lineage_id,
            generation=parent.generation + 1,
            birth_tick=self.tick,
            birth_energy=offspring_energy,
            x=child_x,
            y=child_y,
            energy=offspring_energy,
            age=0,
            genome=child_genome,
            vm_state=self._new_vm_state(child_genome),
        )
        self.organisms.append(child)
        parent.offspring_count += 1
        parent.pending_child_genome = None
        parent.reproduction_block_reason = None
        self._record_genealogy(parent)
        self._record_genealogy(child)
        self.next_id += 1
        self.births += 1
        self.max_population = max(self.max_population, len(self._active()))

        parent_vm = VirtualMachine(parent.genome, self.vm_config, parent.vm_state)
        parent_vm.reset_for_next_lifecycle()
        parent.vm_state = parent_vm.state

        self.emit(
            make_event(
                "organism_born",
                organism_id=child.organism_id,
                parent_id=parent.organism_id,
                generation=child.generation,
                lineage_id=child.lineage_id,
                mutated=mutated,
                genome_hash=child_hash,
                x=round(child.x, 6),
                y=round(child.y, 6),
                parent_child_distance=round(
                    self._spatial_distance(parent.x, parent.y, child.x, child.y), 6
                ),
                boundary_contacts=contacts,
                boundary_model=self.boundary_model,
            )
        )
        return True

    def _kill(self, organism: PhaseZeroOrganism, reason: str) -> None:
        released = max(0.0, organism.energy) if organism.alive else 0.0
        super()._kill(organism, reason)
        if self.resource_field is not None and released > 0.0:
            self.energy_pool -= released
            self.resource_field.release(organism.x, organism.y, released)

    def _capture_energy(self, organism: PhaseZeroOrganism) -> float:
        if self.resource_field is None:
            captured = min(self.energy_pool, 1.0)
            self.energy_pool -= captured
        else:
            captured = self.resource_field.capture(
                organism.x,
                organism.y,
                float(self.config["world.local_capture_limit"]),
            )
            if captured > 0.0:
                self.emit(
                    make_event(
                        "resource_captured",
                        organism_id=organism.organism_id,
                        amount=round(captured, 6),
                        x=round(organism.x, 6),
                        y=round(organism.y, 6),
                    )
                )
        organism.energy += captured
        self.ledger["energy_captured"] += captured
        return captured

    def _sense_resource(self, organism: PhaseZeroOrganism) -> float:
        if self.resource_field is not None:
            return self.resource_field.at(organism.x, organism.y)
        return self.energy_pool

    def _move_organism(
        self,
        organism: PhaseZeroOrganism,
        axis: str,
        requested: float,
    ) -> tuple[float, int]:
        maximum_step = max(0.0, float(self.config["world.movement_max_step"]))
        delta = max(-maximum_step, min(maximum_step, float(requested)))
        before_x, before_y = organism.x, organism.y
        if axis == "x":
            organism.x, contacts = apply_boundary(
                organism.x + delta,
                float(self.config["world.width"]),
                self.boundary_model,
            )
        elif axis == "y":
            organism.y, contacts = apply_boundary(
                organism.y + delta,
                float(self.config["world.height"]),
                self.boundary_model,
            )
        else:
            raise ValueError(f"invalid_movement_axis:{axis}")
        distance = abs(delta)
        self.boundary_contacts += contacts
        self.emit(
            make_event(
                "organism_moved",
                organism_id=organism.organism_id,
                axis=axis,
                requested=round(float(requested), 6),
                distance=round(distance, 6),
                from_x=round(before_x, 6),
                from_y=round(before_y, 6),
                x=round(organism.x, 6),
                y=round(organism.y, 6),
                boundary_contacts=contacts,
            )
        )
        return distance, contacts

    def _execute_one(self, organism: PhaseZeroOrganism) -> None:
        self._capture_energy(organism)
        maintenance = float(self.config["execution.maintenance_cost"])
        if not self._charge(organism, maintenance, "energy_maintenance"):
            self._kill(organism, "energy_exhausted_maintenance")
            return
        if organism.vm_state.division_requested:
            self._try_reproduction(organism)
            return

        movement_distance = 0.0
        if self.organism_actions_enabled:
            vm = PhaseTwoVirtualMachine(
                organism.genome,
                self.vm_config,
                organism.vm_state,
                sense_resource=lambda: self._sense_resource(organism),
                move=lambda axis, delta: self._move_organism(organism, axis, delta),
            )
            result = vm.run(int(self.config["execution.instructions_per_tick"]))
            organism.vm_state = vm.state
            self.resource_sense_operations += result.resource_sense_operations
            self.movement_operations += result.movement_operations
            self.movement_distance += result.movement_distance
            movement_distance = result.movement_distance
        else:
            vm = VirtualMachine(organism.genome, self.vm_config, organism.vm_state)
            result = vm.run(int(self.config["execution.instructions_per_tick"]))
            organism.vm_state = vm.state

        self.total_instructions_executed += result.instructions_executed
        execution_requested = (
            result.instructions_executed
            * float(self.config["execution.instruction_cost"])
        )
        if not self._charge(organism, execution_requested, "energy_execution"):
            self._kill(organism, "energy_exhausted_execution")
            return

        if movement_distance > 0.0:
            movement_requested = (
                movement_distance * float(self.config["world.movement_cost_per_unit"])
            )
            if not self._charge(organism, movement_requested, "energy_movement"):
                self._kill(organism, "energy_exhausted_movement")
                return

        if result.status == "fault":
            self._kill(organism, f"vm_fault:{result.fault}")
            return
        if result.status == "division_requested":
            self._try_reproduction(organism)

    def step(self) -> None:
        if self.resource_field is None:
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
        self.resource_field.renew_uniform(energy_input)
        self.ledger["energy_input"] += energy_input
        self.emit(
            make_event(
                "resource_renewed",
                amount=round(energy_input, 6),
                resource_total=round(self.resource_field.total(), 6),
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

    def energy_balance_error(self) -> float:
        dissipated = (
            self.ledger.get("energy_execution", 0.0)
            + self.ledger.get("energy_maintenance", 0.0)
            + self.ledger.get("energy_reproduction_cost", 0.0)
            + self.ledger.get("energy_movement", 0.0)
        )
        expected = (
            self.initial_total_energy
            + self.ledger.get("energy_input", 0.0)
            - dissipated
        )
        environmental = self.energy_pool
        if self.resource_field is not None:
            environmental += self.resource_field.total()
        actual = environmental + sum(
            organism.energy for organism in self.organisms if organism.alive
        )
        return expected - actual

    def _parent_child_distances(self) -> list[float]:
        by_id = {organism.organism_id: organism for organism in self.organisms}
        distances: list[float] = []
        for child in self.organisms:
            if child.parent_id is None:
                continue
            parent = by_id.get(child.parent_id)
            if parent is None:
                continue
            distances.append(
                self._spatial_distance(parent.x, parent.y, child.x, child.y)
            )
        return distances

    def snapshot(self) -> dict[str, Any]:
        snapshot = super().snapshot()
        snapshot["world_contract_version"] = self.world_contract_version
        snapshot["spatial_enabled"] = self.spatial_enabled
        if not self.spatial_enabled:
            return snapshot

        snapshot.update(
            {
                "boundary_model": self.boundary_model,
                "boundary_contacts": self.boundary_contacts,
                "offspring_dispersion_radius": float(
                    self.config["world.offspring_dispersion_radius"]
                ),
                "neighborhood_radius": float(
                    self.config["world.neighborhood_radius"]
                ),
                "spatial_rng_stream": SPATIAL_RNG_STREAM,
                "local_resources_enabled": self.local_resources_enabled,
                "organism_actions_enabled": self.organism_actions_enabled,
            }
        )
        active_by_id = {
            organism.organism_id: organism for organism in self._active()
        }
        width = float(self.config["world.width"])
        height = float(self.config["world.height"])
        for visible in snapshot.get("organisms", []):
            organism = active_by_id.get(int(visible["id"]))
            if organism is None:
                continue
            visible["local_neighbors"] = local_neighbor_count(
                organism,
                self.organisms,
                float(self.config["world.neighborhood_radius"]),
                width=width,
                height=height,
                boundary_model=self.boundary_model,
            )
            visible["local_resource"] = round(
                self._sense_resource(organism), 6
            )
        if self.resource_field is not None:
            snapshot["resource_grid"] = self.resource_field.snapshot()
        return snapshot

    def metrics(self) -> dict[str, Any]:
        metrics = super().metrics()
        metrics["world_contract_version"] = self.world_contract_version
        metrics["spatial_enabled"] = self.spatial_enabled
        if not self.spatial_enabled:
            return metrics

        distances = self._parent_child_distances()
        spatial_population = population_spatial_metrics(
            self.organisms,
            width=float(self.config["world.width"]),
            height=float(self.config["world.height"]),
            neighborhood_radius=float(self.config["world.neighborhood_radius"]),
            boundary_model=self.boundary_model,
        )
        metrics.update(
            {
                "boundary_model": self.boundary_model,
                "spatial_rng_stream": SPATIAL_RNG_STREAM,
                "spatial_births": len(distances),
                "boundary_contacts": self.boundary_contacts,
                "mean_parent_child_distance": round(
                    sum(distances) / len(distances), 6
                )
                if distances
                else 0.0,
                "max_parent_child_distance": round(max(distances), 6)
                if distances
                else 0.0,
                "local_resources_enabled": self.local_resources_enabled,
                "organism_actions_enabled": self.organism_actions_enabled,
                "resource_sense_operations": self.resource_sense_operations,
                "movement_operations": self.movement_operations,
                "movement_distance": round(self.movement_distance, 6),
                "movement_energy_cost": round(
                    self.ledger.get("energy_movement", 0.0), 6
                ),
                **spatial_population,
            }
        )
        if self.resource_field is not None:
            metrics.update(
                {
                    "local_resource_total": round(
                        self.resource_field.total(), 6
                    ),
                    "local_resource_minimum": round(
                        self.resource_field.minimum(), 6
                    ),
                    "local_resource_balance_error": round(
                        self.resource_field.balance_error(), 10
                    ),
                    "resource_ledger": self.resource_field.ledger(),
                }
            )
        else:
            metrics.update(
                {
                    "local_resource_total": 0.0,
                    "local_resource_minimum": 0.0,
                    "local_resource_balance_error": 0.0,
                    "resource_ledger": {},
                }
            )
        return metrics
