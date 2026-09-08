from __future__ import annotations

import random
import statistics
from typing import Any, Callable

from .phase_five_contract import (
    PHASE_FIVE_ENGINE_VERSION,
    PHASE_FIVE_MEASUREMENT_VERSION,
    PHASE_FIVE_WORLD_CONTRACT_VERSION,
)
from .phase_five_vm import (
    PhaseFiveOpcode,
    PhaseFiveVMState,
    PhaseFiveVirtualMachine,
)
from .phase_zero_engine import PhaseZeroEngine, PhaseZeroOrganism
from .protocol import make_event
from .vm import Instruction, Opcode


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


class PhaseFiveEngine(PhaseZeroEngine):
    """Phase Five length-robust self-replication engine.

    Gate 5A intentionally inherits the homogeneous finite-energy/finite-memory
    world so representation robustness is isolated from spatial/sensing effects.
    Structural mutation is not implemented in this gate.
    """

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
        super().__init__(config, emit)

    @staticmethod
    def default_genome() -> tuple[Instruction, ...]:
        """Length-independent ancestor using sequential copy + template jumps.

        The two initial NOP_A instructions are the loop marker. COPY_NEXT sets
        register 0 to zero exactly when the current genome has been fully copied.
        The conditional A/B template exits to the complementary B/A marker; the
        unconditional B/B template loops to the complementary A/A marker. A
        neutral base NOP separates the inline B/B template from the later B/A
        target marker so template parsing is unambiguous. No genome length or
        absolute jump address is encoded.
        """

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

    def _copied_parent_genome(self, parent: PhaseZeroOrganism) -> tuple[Instruction, ...] | None:
        state = parent.vm_state
        if not isinstance(state, PhaseFiveVMState):
            return None
        vm = PhaseFiveVirtualMachine(parent.genome, self.vm_config, state)
        return vm.copied_genome()

    def _try_reproduction(self, parent: PhaseZeroOrganism) -> bool:
        if not bool(self.config["reproduction.enabled"]):
            self._set_reproduction_block_reason(parent, "disabled")
            return False

        if parent.pending_child_genome is None:
            copied = self._copied_parent_genome(parent)
            if copied is None:
                self._kill(parent, "vm_fault:division_without_complete_copy")
                return False
            parent.pending_child_genome = mutate_phase_five_genome(
                copied,
                self.rng,
                float(self.config["mutation.substitution_rate"]),
            )

        child_genome = parent.pending_child_genome
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
        parent.offspring_count += 1
        parent.pending_child_genome = None
        parent.reproduction_block_reason = None
        self._record_genealogy(parent)
        self._record_genealogy(child)
        self.next_id += 1
        self.births += 1
        self.max_population = max(self.max_population, len(self._active()))

        parent_vm = PhaseFiveVirtualMachine(parent.genome, self.vm_config, parent.vm_state)
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
                parent_genome_length=len(parent.genome),
                child_genome_length=len(child_genome),
            )
        )
        return True

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
        for row in snapshot["organisms"]:
            organism = next(
                item for item in self._active() if item.organism_id == row["id"]
            )
            if isinstance(organism.vm_state, PhaseFiveVMState):
                row["replication_read_position"] = organism.vm_state.replication_read_position
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
                "genome_length_variance": statistics.pvariance(lengths) if lengths else 0.0,
                "distinct_genome_lengths": len(set(lengths)),
            }
        )
        return metrics
