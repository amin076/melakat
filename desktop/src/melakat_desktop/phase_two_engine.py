from __future__ import annotations

import math
import random
from typing import Any, Callable

from .phase_zero_engine import (
    PhaseZeroEngine,
    PhaseZeroOrganism,
    mutate_genome,
)
from .protocol import make_event
from .spatial import (
    SPATIAL_RNG_STREAM,
    derive_spatial_seed,
    local_radial_position,
    population_spatial_metrics,
)
from .vm import VirtualMachine
from .world_contract import WORLD_CONTRACT_VERSION


class PhaseTwoEngine(PhaseZeroEngine):
    """Versioned Phase Two engine with one isolated P2.2 spatial mechanism.

    With ``world.spatial_enabled`` false, all scientific transitions are
    delegated to the frozen Phase One engine. With spatial rules enabled,
    initial positions remain the Phase One seeded positions, but each offspring
    is placed within a configurable radius of its parent and reflected at the
    rectangular boundary.

    Spatial placement uses an independently derived RNG stream. The historical
    engine RNG still consumes the two legacy child-position draws at each birth
    so scheduler and mutation randomness remain aligned with the homogeneous
    control. No movement, local resource field, sensing, or fitness rule exists
    in P2.2.
    """

    engine_version = "phase-two-vm-0.2"
    world_contract_version = WORLD_CONTRACT_VERSION

    def __init__(
        self,
        config: dict[str, Any],
        emit: Callable[[dict[str, Any]], None],
    ):
        self.spatial_enabled = bool(config.get("world.spatial_enabled", False))
        self.boundary_model = str(config.get("world.boundary_model", "reflective"))
        if self.spatial_enabled and self.boundary_model != "reflective":
            raise ValueError(f"unsupported_boundary_model:{self.boundary_model}")

        self.boundary_contacts = 0
        self.spatial_rng_seed = derive_spatial_seed(
            int(config["run.seed"]),
            self.world_contract_version,
        )
        self.spatial_rng = random.Random(self.spatial_rng_seed)
        super().__init__(config, emit)

    def _try_reproduction(self, parent: PhaseZeroOrganism) -> bool:
        if not self.spatial_enabled:
            return super()._try_reproduction(parent)

        if not bool(self.config["reproduction.enabled"]):
            self._set_reproduction_block_reason(parent, "disabled")
            return False

        if parent.pending_child_genome is None:
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

        # Preserve the exact Phase One engine-RNG call count/order. These two
        # values are intentionally discarded in spatial mode; the independent
        # spatial stream controls the actual P2.2 placement.
        self.rng.uniform(0, width)
        self.rng.uniform(0, height)

        child_x, child_y, contacts = local_radial_position(
            parent_x=parent.x,
            parent_y=parent.y,
            radius=float(self.config["world.offspring_dispersion_radius"]),
            width=width,
            height=height,
            rng=self.spatial_rng,
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

        parent_child_distance = math.hypot(
            child.x - parent.x,
            child.y - parent.y,
        )
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
                parent_child_distance=round(parent_child_distance, 6),
                boundary_contacts=contacts,
            )
        )
        return True

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
                math.hypot(
                    child.x - parent.x,
                    child.y - parent.y,
                )
            )
        return distances

    def snapshot(self) -> dict[str, Any]:
        snapshot = super().snapshot()
        snapshot["world_contract_version"] = self.world_contract_version
        snapshot["spatial_enabled"] = self.spatial_enabled
        if self.spatial_enabled:
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
                }
            )
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
        )
        metrics.update(
            {
                "boundary_model": self.boundary_model,
                "spatial_rng_stream": SPATIAL_RNG_STREAM,
                "spatial_births": len(distances),
                "boundary_contacts": self.boundary_contacts,
                "mean_parent_child_distance": round(
                    sum(distances) / len(distances),
                    6,
                )
                if distances
                else 0.0,
                "max_parent_child_distance": round(max(distances), 6)
                if distances
                else 0.0,
                **spatial_population,
            }
        )
        return metrics
