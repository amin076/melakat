from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Callable

from .protocol import make_event
from .vm import Instruction, Opcode, VMConfig, VMState, VirtualMachine


@dataclass
class PhaseZeroOrganism:
    organism_id: int
    x: float
    y: float
    energy: float
    age: int
    genome: tuple[Instruction, ...]
    vm_state: VMState
    alive: bool = True


class PhaseZeroEngine:
    """First engine layer using the bounded Phase Zero VM.

    This version intentionally excludes reproduction and mutation. It gives us
    a testable execution substrate before biological rules are added.
    """

    engine_version = "phase-zero-vm-0.1"

    def __init__(self, config: dict[str, Any], emit: Callable[[dict[str, Any]], None]):
        self.config = config
        self.emit = emit
        self.tick = 0
        self.rng = random.Random(int(config["run.seed"]))
        self.energy_pool = float(config["world.initial_energy"])
        self.births = 0
        self.deaths = 0
        self.finished = False
        memory_size = max(1, int(config["population.memory_per_organism"]))
        self.vm_config = VMConfig(
            word_bits=8,
            register_count=4,
            memory_size=memory_size,
        )
        self.organisms: list[PhaseZeroOrganism] = []
        self._make_initial_population()

    @staticmethod
    def default_genome() -> tuple[Instruction, ...]:
        # A bounded loop: set register 0, increment it, then loop.
        return (
            Instruction(Opcode.SET, a=0, b=1),
            Instruction(Opcode.INC, a=0),
            Instruction(Opcode.JUMP, a=1),
        )

    def _make_initial_population(self) -> None:
        capacity = int(self.config["world.memory_capacity"])
        per_organism = int(self.config["population.memory_per_organism"])
        maximum = capacity // max(1, per_organism)
        requested = int(self.config["population.initial_size"])
        count = min(requested, maximum)
        genome = self.default_genome()
        for organism_id in range(1, count + 1):
            self.organisms.append(
                PhaseZeroOrganism(
                    organism_id=organism_id,
                    x=self.rng.uniform(0, float(self.config["world.width"])),
                    y=self.rng.uniform(0, float(self.config["world.height"])),
                    energy=float(self.config["population.initial_energy"]),
                    age=0,
                    genome=genome,
                    vm_state=VMState(
                        registers=[0] * self.vm_config.register_count,
                        memory=[0] * self.vm_config.memory_size,
                    ),
                )
            )

    def _memory_used(self) -> int:
        return sum(
            self.vm_config.memory_size
            for organism in self.organisms
            if organism.alive
        )

    def step(self) -> None:
        if self.finished:
            return

        maximum_ticks = int(self.config["run.max_ticks"])
        if self.tick >= maximum_ticks:
            self.finished = True
            self.emit(make_event("finished", reason="max_ticks", snapshot=self.snapshot()))
            return

        self.tick += 1
        self.energy_pool += float(self.config["world.energy_input_per_tick"])
        budget = int(self.config["execution.instructions_per_tick"])
        instruction_cost = float(self.config["execution.instruction_cost"])
        maintenance_cost = float(self.config["execution.maintenance_cost"])

        for organism in [item for item in self.organisms if item.alive]:
            if self.energy_pool > 0:
                captured = min(self.energy_pool, 1.0)
                organism.energy += captured
                self.energy_pool -= captured

            vm = VirtualMachine(
                organism.genome,
                self.vm_config,
                organism.vm_state,
            )
            result = vm.run(budget)
            organism.vm_state = vm.state
            organism.age += 1
            organism.energy -= maintenance_cost + instruction_cost * result.instructions_executed

            if result.status == "fault" or organism.energy <= 0:
                organism.alive = False
                self.deaths += 1
                self.emit(
                    make_event(
                        "organism_died",
                        organism_id=organism.organism_id,
                        reason=result.fault or "energy_depleted",
                    )
                )
            elif organism.age >= int(self.config["population.max_age"]):
                organism.alive = False
                self.deaths += 1
                self.emit(
                    make_event(
                        "organism_died",
                        organism_id=organism.organism_id,
                        reason="maximum_age",
                    )
                )

        snapshot = self.snapshot()
        self.emit(
            make_event(
                "tick",
                snapshot=snapshot,
                metrics=self.metrics(),
            )
        )
        if self.tick >= maximum_ticks:
            self.finished = True
            self.emit(make_event("finished", reason="max_ticks", snapshot=snapshot))

    def snapshot(self) -> dict[str, Any]:
        return {
            "tick": self.tick,
            "engine_version": self.engine_version,
            "world_width": self.config["world.width"],
            "world_height": self.config["world.height"],
            "energy_pool": round(self.energy_pool, 4),
            "memory_used": self._memory_used(),
            "organisms": [
                {
                    "id": organism.organism_id,
                    "x": organism.x,
                    "y": organism.y,
                    "energy": round(organism.energy, 4),
                    "age": organism.age,
                    "alive": organism.alive,
                    "instruction_pointer": organism.vm_state.instruction_pointer,
                    "registers": list(organism.vm_state.registers),
                    "memory": list(organism.vm_state.memory),
                    "instructions_executed": organism.vm_state.instructions_executed,
                    "fault": organism.vm_state.fault,
                }
                for organism in self.organisms
                if organism.alive
            ],
        }

    def metrics(self) -> dict[str, Any]:
        active = sum(1 for organism in self.organisms if organism.alive)
        executed = sum(
            organism.vm_state.instructions_executed
            for organism in self.organisms
        )
        faults = sum(
            organism.vm_state.fault is not None
            for organism in self.organisms
        )
        return {
            "tick": self.tick,
            "active_population": active,
            "births": self.births,
            "deaths": self.deaths,
            "instructions_executed": executed,
            "faults": faults,
            "energy_pool": round(self.energy_pool, 4),
            "memory_used": self._memory_used(),
        }
