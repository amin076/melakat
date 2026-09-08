from __future__ import annotations

import hashlib
import random
import statistics
from dataclasses import dataclass
from typing import Any, Callable, Literal

from .phase_five_contract import (
    PHASE_FIVE_ENGINE_VERSION,
    PHASE_FIVE_MEASUREMENT_VERSION,
    PHASE_FIVE_STRUCTURAL_RNG_VERSION,
    PHASE_FIVE_WORLD_CONTRACT_VERSION,
)
from .phase_five_structural_contract import (
    PHASE_FIVE_STRUCTURAL_ENGINE_VERSION,
    PHASE_FIVE_STRUCTURAL_MEASUREMENT_VERSION,
)
from .phase_five_vm import (
    PhaseFiveOpcode,
    PhaseFiveVMState,
    PhaseFiveVirtualMachine,
)
from .phase_zero_engine import PhaseZeroEngine, PhaseZeroOrganism
from .protocol import make_event
from .vm import Instruction, Opcode


StructuralKind = Literal["duplication", "deletion"]


@dataclass(frozen=True)
class StructuralMutationResult:
    genome: tuple[Instruction, ...]
    attempted: bool
    committed: bool
    rejected: bool
    kind: StructuralKind | None
    index: int | None
    length_delta: int


def derive_structural_seed(seed: int) -> int:
    payload = f"{PHASE_FIVE_STRUCTURAL_RNG_VERSION}:{int(seed)}".encode("utf-8")
    digest = hashlib.sha256(payload).digest()
    return int.from_bytes(digest[:8], "big", signed=False)


def mutate_phase_five_genome(
    genome: tuple[Instruction, ...],
    rng: random.Random,
    rate: float,
) -> tuple[Instruction, ...]:
    """Blind opcode substitution over the Phase Zero + Phase Five alphabets."""

    if not 0.0 <= rate <= 1.0:
        raise ValueError("substitution_rate must be between 0 and 1")
    alphabet = [*list(Opcode), *list(PhaseFiveOpcode)]
    result: list[Instruction] = []
    for instruction in genome:
        if rng.random() < rate:
            alternatives = [opcode for opcode in alphabet if opcode != instruction.opcode]
            instruction = Instruction(
                opcode=rng.choice(alternatives),  # type: ignore[arg-type]
                a=instruction.a,
                b=instruction.b,
            )
        result.append(instruction)
    return tuple(result)


def apply_structural_mutation(
    genome: tuple[Instruction, ...],
    rng: random.Random,
    *,
    event_rate: float,
    duplication_probability: float,
) -> StructuralMutationResult:
    """Apply at most one blind length-changing event to one daughter proposal."""

    if not genome:
        raise ValueError("structural_mutation_requires_nonempty_genome")
    if not 0.0 <= event_rate <= 1.0:
        raise ValueError("structural_event_rate must be between 0 and 1")
    if not 0.0 <= duplication_probability <= 1.0:
        raise ValueError("structural_duplication_probability must be between 0 and 1")
    if event_rate <= 0.0 or rng.random() >= event_rate:
        return StructuralMutationResult(genome, False, False, False, None, None, 0)

    if rng.random() < duplication_probability:
        index = rng.randrange(len(genome))
        result = list(genome)
        result.insert(index + 1, genome[index])
        return StructuralMutationResult(
            tuple(result), True, True, False, "duplication", index, 1
        )

    if len(genome) == 1:
        return StructuralMutationResult(
            genome, True, False, True, "deletion", 0, 0
        )
    index = rng.randrange(len(genome))
    result = list(genome)
    del result[index]
    return StructuralMutationResult(
        tuple(result), True, True, False, "deletion", index, -1
    )


class PhaseFiveEngine(PhaseZeroEngine):
    """Phase Five length-robust replication plus opt-in structural variation."""

    engine_version = PHASE_FIVE_ENGINE_VERSION
    measurement_version = PHASE_FIVE_MEASUREMENT_VERSION
    world_contract_version = PHASE_FIVE_WORLD_CONTRACT_VERSION

    def __init__(
        self,
        config: dict[str, Any],
        emit: Callable[[dict[str, Any]], None],
    ) -> None:
        self.replication_copy_operations = 0
        self.template_jump_operations = 0
        self.ancestor_genome_length = len(self.default_genome())

        self.structural_mutation_configured = (
            "mutation.structural_event_rate" in config
            or "mutation.structural_duplication_probability" in config
        )
        self.structural_event_rate = float(
            config.get("mutation.structural_event_rate", 0.0)
        )
        self.structural_duplication_probability = float(
            config.get("mutation.structural_duplication_probability", 0.5)
        )
        if not 0.0 <= self.structural_event_rate <= 1.0:
            raise ValueError("structural_event_rate must be between 0 and 1")
        if not 0.0 <= self.structural_duplication_probability <= 1.0:
            raise ValueError(
                "structural_duplication_probability must be between 0 and 1"
            )
        self.structural_rng_seed = derive_structural_seed(int(config["run.seed"]))
        self.structural_rng = random.Random(self.structural_rng_seed)
        self.structural_mutation_operations = 0
        self.structural_mutation_committed_operations = 0
        self.structural_mutation_rejected_operations = 0
        self.instruction_duplication_operations = 0
        self.instruction_deletion_operations = 0
        self.structural_length_delta_total = 0
        self.variable_length_births = 0
        self.variable_length_reproducing_offspring = 0
        self._credited_variable_length_reproducers: set[int] = set()
        self._pending_structural_events: dict[int, StructuralMutationResult] = {}

        if self.structural_mutation_configured:
            self.engine_version = PHASE_FIVE_STRUCTURAL_ENGINE_VERSION
            self.measurement_version = PHASE_FIVE_STRUCTURAL_MEASUREMENT_VERSION
        super().__init__(config, emit)

    @staticmethod
    def default_genome() -> tuple[Instruction, ...]:
        """Length-independent ancestor using sequential copy + template jumps."""

        return (
            Instruction(PhaseFiveOpcode.NOP_A),  # type: ignore[arg-type]
            Instruction(PhaseFiveOpcode.NOP_A),  # type: ignore[arg-type]
            Instruction(Opcode.NOP),
            Instruction(PhaseFiveOpcode.COPY_NEXT),  # type: ignore[arg-type]
            Instruction(PhaseFiveOpcode.JUMP_TEMPLATE_IF_ZERO),  # type: ignore[arg-type]
            Instruction(PhaseFiveOpcode.NOP_A),  # type: ignore[arg-type]
            Instruction(PhaseFiveOpcode.NOP_B),  # type: ignore[arg-type]
            Instruction(PhaseFiveOpcode.JUMP_TEMPLATE),  # type: ignore[arg-type]
            Instruction(PhaseFiveOpcode.NOP_B),  # type: ignore[arg-type]
            Instruction(PhaseFiveOpcode.NOP_B),  # type: ignore[arg-type]
            Instruction(Opcode.NOP),
            Instruction(PhaseFiveOpcode.NOP_B),  # type: ignore[arg-type]
            Instruction(PhaseFiveOpcode.NOP_A),  # type: ignore[arg-type]
            Instruction(Opcode.DIVIDE),
        )

    def _new_vm_state(self, genome: tuple[Instruction, ...]) -> PhaseFiveVMState:
        return PhaseFiveVMState(
            registers=[0] * self.vm_config.register_count,
            memory=[0] * self.vm_config.memory_size,
            replication_buffer=[],
            replication_read_position=0,
        )

    def _copied_parent_genome(
        self, parent: PhaseZeroOrganism
    ) -> tuple[Instruction, ...] | None:
        state = parent.vm_state
        if not isinstance(state, PhaseFiveVMState):
            return None
        vm = PhaseFiveVirtualMachine(parent.genome, self.vm_config, state)
        return vm.copied_genome()

    def _prepare_pending_child(self, parent: PhaseZeroOrganism) -> None:
        copied = self._copied_parent_genome(parent)
        if copied is None:
            self._kill(parent, "vm_fault:division_without_complete_copy")
            return
        substituted = mutate_phase_five_genome(
            copied,
            self.rng,
            float(self.config["mutation.substitution_rate"]),
        )
        structural = apply_structural_mutation(
            substituted,
            self.structural_rng,
            event_rate=self.structural_event_rate,
            duplication_probability=self.structural_duplication_probability,
        )
        parent.pending_child_genome = structural.genome
        self._pending_structural_events[parent.organism_id] = structural
        if structural.attempted:
            self.structural_mutation_operations += 1
        if structural.committed:
            self.structural_mutation_committed_operations += 1
            self.structural_length_delta_total += structural.length_delta
            if structural.kind == "duplication":
                self.instruction_duplication_operations += 1
            elif structural.kind == "deletion":
                self.instruction_deletion_operations += 1
        if structural.rejected:
            self.structural_mutation_rejected_operations += 1
        if structural.attempted:
            self.emit(
                make_event(
                    "structural_mutation_proposed",
                    organism_id=parent.organism_id,
                    mutation_type=structural.kind,
                    committed=structural.committed,
                    rejected=structural.rejected,
                    instruction_index=structural.index,
                    parent_genome_length=len(parent.genome),
                    child_genome_length=len(structural.genome),
                    genome_length_delta=structural.length_delta,
                )
            )

    def _try_reproduction(self, parent: PhaseZeroOrganism) -> bool:
        if not bool(self.config["reproduction.enabled"]):
            self._set_reproduction_block_reason(parent, "disabled")
            return False

        if parent.pending_child_genome is None:
            self._prepare_pending_child(parent)
            if not parent.alive or parent.pending_child_genome is None:
                return False

        child_genome = parent.pending_child_genome
        structural = self._pending_structural_events.get(
            parent.organism_id,
            StructuralMutationResult(
                child_genome, False, False, False, None, None, 0
            ),
        )
        allocation = self._allocation_for_genome(child_genome)
        free_memory = self._free_memory()
        if free_memory < allocation:
            self._set_reproduction_block_reason(parent, "memory", free_memory=free_memory)
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

        child = PhaseZeroOrganism(
            organism_id=self.next_id,
            parent_id=parent.organism_id,
            lineage_id=lineage_id,
            generation=parent.generation + 1,
            birth_tick=self.tick,
            birth_energy=offspring_energy,
            x=self.rng.uniform(0, float(self.config["world.width"])),
            y=self.rng.uniform(0, float(self.config["world.height"])),
            energy=offspring_energy,
            age=0,
            genome=child_genome,
            vm_state=self._new_vm_state(child_genome),
        )
        self.organisms.append(child)
        if len(child_genome) != self.ancestor_genome_length:
            self.variable_length_births += 1
        if (
            len(parent.genome) != self.ancestor_genome_length
            and parent.organism_id not in self._credited_variable_length_reproducers
        ):
            self._credited_variable_length_reproducers.add(parent.organism_id)
            self.variable_length_reproducing_offspring += 1

        parent.offspring_count += 1
        parent.pending_child_genome = None
        parent.reproduction_block_reason = None
        self._pending_structural_events.pop(parent.organism_id, None)
        self._record_genealogy(parent)
        self._record_genealogy(child)
        self.next_id += 1
        self.births += 1
        self.max_population = max(self.max_population, len(self._active()))

        parent_vm = PhaseFiveVirtualMachine(
            parent.genome, self.vm_config, parent.vm_state  # type: ignore[arg-type]
        )
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
                parent_genome_hash=parent_hash,
                genome_hash=child_hash,
                parent_genome_length=len(parent.genome),
                child_genome_length=len(child_genome),
                genome_length_delta=len(child_genome) - len(parent.genome),
                structural_mutation_type=structural.kind,
                structural_mutation_index=structural.index,
                structural_mutation_committed=structural.committed,
            )
        )
        return True

    def _kill(self, organism: PhaseZeroOrganism, reason: str) -> None:
        self._pending_structural_events.pop(organism.organism_id, None)
        super()._kill(organism, reason)

    def _execute_one(self, organism: PhaseZeroOrganism) -> None:
        captured = min(self.energy_pool, 1.0)
        organism.energy += captured
        self.energy_pool -= captured
        self.ledger["energy_captured"] += captured

        maintenance = float(self.config["execution.maintenance_cost"])
        if not self._charge(organism, maintenance, "energy_maintenance"):
            self._kill(organism, "energy_exhausted_maintenance")
            return

        if organism.vm_state.division_requested:
            self._try_reproduction(organism)
            return

        if not isinstance(organism.vm_state, PhaseFiveVMState):
            self._kill(organism, "vm_fault:invalid_phase_five_vm_state")
            return
        vm = PhaseFiveVirtualMachine(organism.genome, self.vm_config, organism.vm_state)
        result = vm.run(int(self.config["execution.instructions_per_tick"]))
        organism.vm_state = vm.state
        self.total_instructions_executed += result.instructions_executed
        self.replication_copy_operations += result.replication_copy_operations
        self.template_jump_operations += result.template_jump_operations

        execution_requested = (
            result.instructions_executed
            * float(self.config["execution.instruction_cost"])
        )
        if not self._charge(organism, execution_requested, "energy_execution"):
            self._kill(organism, "energy_exhausted_execution")
            return
        if result.status == "fault":
            self._kill(organism, f"vm_fault:{result.fault}")
            return
        if result.status == "division_requested":
            self._try_reproduction(organism)

    def snapshot(self) -> dict[str, Any]:
        snapshot = super().snapshot()
        active_by_id = {item.organism_id: item for item in self._active()}
        for row in snapshot["organisms"]:
            organism = active_by_id[row["id"]]
            if isinstance(organism.vm_state, PhaseFiveVMState):
                row["replication_read_position"] = (
                    organism.vm_state.replication_read_position
                )
                row["replication_progress"] = sum(
                    item is not None for item in organism.vm_state.replication_buffer
                )
        snapshot["world_contract_version"] = self.world_contract_version
        return snapshot

    def metrics(self) -> dict[str, Any]:
        metrics = super().metrics()
        lengths = [len(organism.genome) for organism in self._active()]
        genome_memory_used = sum(lengths)
        metrics.update(
            {
                "world_contract_version": self.world_contract_version,
                "replication_copy_operations": self.replication_copy_operations,
                "template_jump_operations": self.template_jump_operations,
                "genome_memory_used": genome_memory_used,
                "genome_length_mean": statistics.fmean(lengths) if lengths else 0.0,
                "genome_length_median": statistics.median(lengths) if lengths else 0.0,
                "genome_length_minimum": min(lengths) if lengths else 0,
                "genome_length_maximum": max(lengths) if lengths else 0,
                "genome_length_variance": (
                    statistics.pvariance(lengths) if lengths else 0.0
                ),
                "distinct_genome_lengths": len(set(lengths)),
                "structural_event_rate": self.structural_event_rate,
                "structural_duplication_probability": (
                    self.structural_duplication_probability
                ),
                "structural_rng_version": PHASE_FIVE_STRUCTURAL_RNG_VERSION,
                "structural_rng_seed": self.structural_rng_seed,
                "structural_mutation_operations": self.structural_mutation_operations,
                "structural_mutation_committed_operations": (
                    self.structural_mutation_committed_operations
                ),
                "structural_mutation_rejected_operations": (
                    self.structural_mutation_rejected_operations
                ),
                "instruction_duplication_operations": (
                    self.instruction_duplication_operations
                ),
                "instruction_deletion_operations": self.instruction_deletion_operations,
                "structural_length_delta_total": self.structural_length_delta_total,
                "variable_length_births": self.variable_length_births,
                "variable_length_reproducing_offspring": (
                    self.variable_length_reproducing_offspring
                ),
                "variable_length_active_population": sum(
                    length != self.ancestor_genome_length for length in lengths
                ),
            }
        )
        return metrics
