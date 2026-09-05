from __future__ import annotations

import hashlib
import json
import random
from collections import Counter
from dataclasses import dataclass
from typing import Any, Callable

from .protocol import make_event
from .vm import (
    Instruction,
    Opcode,
    VMConfig,
    VMState,
    VirtualMachine,
    program_records,
)


@dataclass
class PhaseZeroOrganism:
    organism_id: int
    parent_id: int | None
    lineage_id: int
    generation: int
    birth_tick: int
    x: float
    y: float
    energy: float
    age: int
    genome: tuple[Instruction, ...]
    vm_state: VMState
    alive: bool = True
    death_tick: int | None = None
    death_reason: str | None = None
    offspring_count: int = 0


def mutate_genome(
    genome: tuple[Instruction, ...],
    rng: random.Random,
    rate: float,
) -> tuple[Instruction, ...]:
    """Apply blind substitution mutation to instruction opcodes only."""

    result: list[Instruction] = []
    opcodes = list(Opcode)
    for instruction in genome:
        if rng.random() < rate:
            alternatives = [opcode for opcode in opcodes if opcode != instruction.opcode]
            instruction = Instruction(
                opcode=rng.choice(alternatives),
                a=instruction.a,
                b=instruction.b,
            )
        result.append(instruction)
    return tuple(result)


class PhaseZeroEngine:
    """Complete baseline engine for the Digital Petri Dish.

    The baseline has a homogeneous well-mixed environment, finite memory,
    sequential energy input, costly bounded computation, costly reproduction,
    blind substitution mutation, heredity, genealogy, and death by resource
    exhaustion or invalid execution.

    It deliberately has no explicit fitness, learning, ML, injected parasite,
    attack, cooperation, geography, catastrophe, or fixed lifespan rule.
    """

    engine_version = "phase-zero-vm-0.2"

    def __init__(
        self,
        config: dict[str, Any],
        emit: Callable[[dict[str, Any]], None],
    ):
        self.config = config
        self.emit = emit
        self.emit_snapshots = bool(config.get("run.emit_snapshots", True))
        self.rng = random.Random(int(config["run.seed"]))
        self.tick = 0
        self.energy_pool = float(config["world.initial_energy"])
        self.next_id = 1
        self.next_lineage = 1
        self.births = 0
        self.deaths = 0
        self.faults = 0
        self.total_instructions_executed = 0
        self.max_population = 0
        self.finished = False
        self.death_reasons: Counter[str] = Counter()
        self.genealogy: dict[int, dict[str, Any]] = {}
        self.historical_genomes: set[str] = set()
        self.ledger: dict[str, float] = {
            "energy_input": 0.0,
            "energy_captured": 0.0,
            "energy_execution": 0.0,
            "energy_maintenance": 0.0,
            "energy_reproduction_cost": 0.0,
            "energy_transferred_to_offspring": 0.0,
            "energy_released_on_death": 0.0,
        }

        self.vm_config = VMConfig(
            word_bits=8,
            register_count=4,
            memory_size=max(1, int(config["population.memory_per_organism"])),
        )
        self.organisms: list[PhaseZeroOrganism] = []
        self._make_initial_population()
        self.initial_total_energy = self.energy_pool + sum(
            organism.energy for organism in self.organisms
        )
        self.max_population = len(self.organisms)

    @staticmethod
    def default_genome() -> tuple[Instruction, ...]:
        """Minimal self-replicator built from primitive VM operations.

        Register 0 is a countdown. Register 1 is the genome index. COPY uses
        register 1 to copy one program cell into the offspring buffer.
        """

        return (
            Instruction(Opcode.SET, a=0, b=8),
            Instruction(Opcode.SET, a=1, b=0),
            Instruction(Opcode.COPY),
            Instruction(Opcode.INC, a=1),
            Instruction(Opcode.DEC, a=0),
            Instruction(Opcode.JUMP_IF_ZERO, a=7),
            Instruction(Opcode.JUMP, a=2),
            Instruction(Opcode.DIVIDE),
        )

    @staticmethod
    def genome_hash(genome: tuple[Instruction, ...]) -> str:
        encoded = json.dumps(
            program_records(genome),
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()[:16]

    def _new_vm_state(self, genome: tuple[Instruction, ...]) -> VMState:
        return VMState(
            registers=[0] * self.vm_config.register_count,
            memory=[0] * self.vm_config.memory_size,
            replication_buffer=[None] * len(genome),
        )

    def _make_initial_population(self) -> None:
        genome = self.default_genome()
        allocation = self._allocation_for_genome(genome)
        capacity = int(self.config["world.memory_capacity"])
        requested = int(self.config["population.initial_size"])
        count = min(requested, capacity // max(1, allocation))
        genome_hash = self.genome_hash(genome)
        self.historical_genomes.add(genome_hash)

        for _ in range(count):
            organism = PhaseZeroOrganism(
                organism_id=self.next_id,
                parent_id=None,
                lineage_id=1,
                generation=0,
                birth_tick=0,
                x=self.rng.uniform(0, float(self.config["world.width"])),
                y=self.rng.uniform(0, float(self.config["world.height"])),
                energy=float(self.config["population.initial_energy"]),
                age=0,
                genome=genome,
                vm_state=self._new_vm_state(genome),
            )
            self.organisms.append(organism)
            self._record_genealogy(organism)
            self.next_id += 1

    def _record_genealogy(self, organism: PhaseZeroOrganism) -> None:
        self.genealogy[organism.organism_id] = {
            "organism_id": organism.organism_id,
            "parent_id": organism.parent_id,
            "lineage_id": organism.lineage_id,
            "generation": organism.generation,
            "birth_tick": organism.birth_tick,
            "death_tick": organism.death_tick,
            "death_reason": organism.death_reason,
            "genome_hash": self.genome_hash(organism.genome),
            "genome_length": len(organism.genome),
            "offspring_count": organism.offspring_count,
        }

    def _allocation_for_genome(self, genome: tuple[Instruction, ...]) -> int:
        working_memory = int(self.config["population.memory_per_organism"])
        return working_memory + len(genome)

    def _memory_used(self) -> int:
        return sum(
            self._allocation_for_genome(organism.genome)
            for organism in self.organisms
            if organism.alive
        )

    def _free_memory(self) -> int:
        return max(0, int(self.config["world.memory_capacity"]) - self._memory_used())

    def _active(self) -> list[PhaseZeroOrganism]:
        return [organism for organism in self.organisms if organism.alive]

    def _charge(
        self,
        organism: PhaseZeroOrganism,
        requested: float,
        ledger_key: str,
    ) -> bool:
        requested = max(0.0, float(requested))
        paid = min(organism.energy, requested)
        organism.energy -= paid
        self.ledger[ledger_key] += paid
        return paid >= requested - 1e-12

    def _kill(self, organism: PhaseZeroOrganism, reason: str) -> None:
        if not organism.alive:
            return
        released = max(0.0, organism.energy)
        organism.energy = 0.0
        organism.alive = False
        organism.death_tick = self.tick
        organism.death_reason = reason
        self.energy_pool += released
        self.ledger["energy_released_on_death"] += released
        self.deaths += 1
        self.death_reasons[reason] += 1
        if reason.startswith("vm_fault:"):
            self.faults += 1
        self._record_genealogy(organism)
        self.emit(
            make_event(
                "organism_died",
                organism_id=organism.organism_id,
                reason=reason,
                released_energy=round(released, 6),
            )
        )

    def _try_reproduction(self, parent: PhaseZeroOrganism) -> bool:
        if not bool(self.config["reproduction.enabled"]):
            return False

        child_genome = mutate_genome(
            parent.genome,
            self.rng,
            float(self.config["mutation.substitution_rate"]),
        )
        allocation = self._allocation_for_genome(child_genome)
        if self._free_memory() < allocation:
            return False

        reproduction_cost = float(self.config["reproduction.cost"])
        offspring_energy = float(self.config["reproduction.offspring_energy"])
        total_required = reproduction_cost + offspring_energy
        if parent.energy < total_required:
            return False

        parent.energy -= total_required
        self.ledger["energy_reproduction_cost"] += reproduction_cost
        self.ledger["energy_transferred_to_offspring"] += offspring_energy

        parent_hash = self.genome_hash(parent.genome)
        child_hash = self.genome_hash(child_genome)
        mutated = child_hash != parent_hash
        if mutated:
            lineage_id = self.next_lineage
            self.next_lineage += 1
        else:
            lineage_id = parent.lineage_id
        self.historical_genomes.add(child_hash)

        child = PhaseZeroOrganism(
            organism_id=self.next_id,
            parent_id=parent.organism_id,
            lineage_id=lineage_id,
            generation=parent.generation + 1,
            birth_tick=self.tick,
            x=self.rng.uniform(0, float(self.config["world.width"])),
            y=self.rng.uniform(0, float(self.config["world.height"])),
            energy=offspring_energy,
            age=0,
            genome=child_genome,
            vm_state=self._new_vm_state(child_genome),
        )
        self.organisms.append(child)
        parent.offspring_count += 1
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
            )
        )
        return True

    def _execute_one(self, organism: PhaseZeroOrganism) -> None:
        capture_limit = 1.0
        captured = min(self.energy_pool, capture_limit)
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

        vm = VirtualMachine(organism.genome, self.vm_config, organism.vm_state)
        result = vm.run(int(self.config["execution.instructions_per_tick"]))
        organism.vm_state = vm.state
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
            self._kill(organism, "energy_exhausted_execution")
            return

        if result.status == "fault":
            self._kill(organism, f"vm_fault:{result.fault}")
            return

        if result.status == "division_requested":
            self._try_reproduction(organism)

    def step(self) -> None:
        if self.finished:
            return

        maximum_ticks = int(self.config["run.max_ticks"])
        if self.tick >= maximum_ticks:
            self.finished = True
            self.emit(make_event("finished", reason="max_ticks", snapshot=self.snapshot()))
            return

        self.tick += 1
        energy_input = float(self.config["world.energy_input_per_tick"])
        self.energy_pool += energy_input
        self.ledger["energy_input"] += energy_input

        schedule = self._active()
        self.rng.shuffle(schedule)
        for organism in schedule:
            if organism.alive:
                self._execute_one(organism)

        self.max_population = max(self.max_population, len(self._active()))
        if self.emit_snapshots:
            self.emit(
                make_event(
                    "tick",
                    snapshot=self.snapshot(),
                    metrics=self.metrics(),
                )
            )
        if self.tick >= maximum_ticks:
            self.finished = True
            self.emit(
                make_event(
                    "finished",
                    reason="max_ticks",
                    snapshot=self.snapshot(),
                )
            )

    def energy_balance_error(self) -> float:
        dissipated = (
            self.ledger["energy_execution"]
            + self.ledger["energy_maintenance"]
            + self.ledger["energy_reproduction_cost"]
        )
        expected = self.initial_total_energy + self.ledger["energy_input"] - dissipated
        actual = self.energy_pool + sum(
            organism.energy for organism in self.organisms if organism.alive
        )
        return expected - actual

    def snapshot(self) -> dict[str, Any]:
        visible = [
            {
                "id": organism.organism_id,
                "parent_id": organism.parent_id,
                "lineage_id": organism.lineage_id,
                "generation": organism.generation,
                "birth_tick": organism.birth_tick,
                "x": organism.x,
                "y": organism.y,
                "energy": round(organism.energy, 6),
                "age": organism.age,
                "alive": organism.alive,
                "genome_hash": self.genome_hash(organism.genome),
                "genome_length": len(organism.genome),
                "genome": program_records(organism.genome),
                "instruction_pointer": organism.vm_state.instruction_pointer,
                "registers": list(organism.vm_state.registers),
                "memory": list(organism.vm_state.memory),
                "replication_progress": sum(
                    item is not None
                    for item in organism.vm_state.replication_buffer
                ),
                "division_requested": organism.vm_state.division_requested,
                "instructions_executed": organism.vm_state.instructions_executed,
                "fault": organism.vm_state.fault,
                "offspring_count": organism.offspring_count,
            }
            for organism in self._active()
        ][: int(self.config["visual.max_rendered_organisms"])]
        return {
            "tick": self.tick,
            "engine_version": self.engine_version,
            "world_width": self.config["world.width"],
            "world_height": self.config["world.height"],
            "energy_pool": round(self.energy_pool, 6),
            "memory_used": self._memory_used(),
            "memory_capacity": int(self.config["world.memory_capacity"]),
            "free_memory": self._free_memory(),
            "organisms": visible,
        }

    def metrics(self) -> dict[str, Any]:
        active = self._active()
        active_hashes = {
            self.genome_hash(organism.genome) for organism in active
        }
        executed = self.total_instructions_executed
        return {
            "engine_version": self.engine_version,
            "tick": self.tick,
            "active_population": len(active),
            "births": self.births,
            "deaths": self.deaths,
            "max_population": self.max_population,
            "active_genotypes": len(active_hashes),
            "historical_genotypes": len(self.historical_genomes),
            "instructions_executed": executed,
            "faults": self.faults,
            "energy_pool": round(self.energy_pool, 6),
            "memory_used": self._memory_used(),
            "free_memory": self._free_memory(),
            "energy_balance_error": round(self.energy_balance_error(), 10),
            "ledger": {key: round(value, 6) for key, value in self.ledger.items()},
        }

    def summary(self) -> dict[str, Any]:
        return {
            **self.metrics(),
            "death_reasons": dict(self.death_reasons),
            "genealogy_size": len(self.genealogy),
            "final_snapshot": self.snapshot(),
        }
