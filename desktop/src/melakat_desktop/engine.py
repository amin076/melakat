from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Callable

from .protocol import make_event


@dataclass
class DemoOrganism:
    organism_id: int
    parent_id: int | None
    lineage_id: int
    x: float
    y: float
    energy: float
    age: int = 0
    genome: list[int] = field(default_factory=lambda: [1, 2, 3, 4])
    alive: bool = True


class DemoEngine:
    """Architecture smoke engine, not the final scientific VM."""

    engine_version = "demo-0.1"

    def __init__(self, config: dict[str, Any], emit: Callable[[dict[str, Any]], None]):
        self.config = config
        self.emit = emit
        self.rng = random.Random(int(config["run.seed"]))
        self.tick = 0
        self.energy_pool = float(config["world.initial_energy"])
        self.next_id = 1
        self.next_lineage = 1
        self.births = 0
        self.deaths = 0
        self.finished = False
        self.organisms: list[DemoOrganism] = []
        self._make_initial_population()

    def _make_initial_population(self) -> None:
        width = float(self.config["world.width"])
        height = float(self.config["world.height"])
        capacity = int(self.config["world.memory_capacity"])
        per_organism = int(self.config["population.memory_per_organism"])
        maximum = max(1, capacity // max(1, per_organism))
        requested = int(self.config["population.initial_size"])
        for _ in range(min(requested, maximum)):
            self.organisms.append(
                DemoOrganism(
                    organism_id=self.next_id,
                    parent_id=None,
                    lineage_id=self.next_lineage,
                    x=self.rng.uniform(0, width),
                    y=self.rng.uniform(0, height),
                    energy=float(self.config["population.initial_energy"]),
                )
            )
            self.next_id += 1
            self.next_lineage += 1

    def _memory_used(self) -> int:
        return sum(
            int(self.config["population.memory_per_organism"])
            for organism in self.organisms
            if organism.alive
        )

    def _mutate_genome(self, genome: list[int]) -> list[int]:
        rate = float(self.config["mutation.substitution_rate"])
        result = list(genome)
        for index, value in enumerate(result):
            if self.rng.random() < rate:
                result[index] = self.rng.randint(0, 7)
        return result

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
        instruction_cost = float(self.config["execution.instruction_cost"])
        maintenance_cost = float(self.config["execution.maintenance_cost"])
        instruction_count = int(self.config["execution.instructions_per_tick"])

        alive = [organism for organism in self.organisms if organism.alive]
        for organism in alive:
            organism.age += 1
            organism.energy -= maintenance_cost + instruction_cost * instruction_count

            if self.energy_pool > 0:
                captured = min(self.energy_pool, 1.0)
                organism.energy += captured
                self.energy_pool -= captured

            capacity = int(self.config["world.memory_capacity"])
            per_organism = int(self.config["population.memory_per_organism"])
            has_memory = self._memory_used() + per_organism <= capacity
            can_reproduce = (
                self.config["reproduction.enabled"]
                and has_memory
                and organism.energy >= float(self.config["reproduction.threshold"])
                and organism.age % int(self.config["reproduction.interval"]) == 0
            )
            if can_reproduce:
                cost = float(self.config["reproduction.cost"])
                if organism.energy >= cost:
                    organism.energy -= cost
                    child = DemoOrganism(
                        organism_id=self.next_id,
                        parent_id=organism.organism_id,
                        lineage_id=organism.lineage_id,
                        x=max(0.0, min(float(self.config["world.width"]), organism.x + self.rng.uniform(-3, 3))),
                        y=max(0.0, min(float(self.config["world.height"]), organism.y + self.rng.uniform(-3, 3))),
                        energy=cost,
                        genome=self._mutate_genome(organism.genome),
                    )
                    self.next_id += 1
                    self.births += 1
                    self.organisms.append(child)
                    self.emit(make_event("organism_born", organism_id=child.organism_id, parent_id=organism.organism_id))

            if organism.energy <= 0 or organism.age >= int(self.config["population.max_age"]):
                organism.alive = False
                self.deaths += 1
                self.emit(make_event("organism_died", organism_id=organism.organism_id))

        snapshot = self.snapshot()
        self.emit(make_event("tick", snapshot=snapshot, metrics=self.metrics()))
        if self.tick >= maximum_ticks:
            self.finished = True
            self.emit(make_event("finished", reason="max_ticks", snapshot=snapshot))

    def snapshot(self) -> dict[str, Any]:
        visible = [
            {
                "id": organism.organism_id,
                "parent_id": organism.parent_id,
                "lineage_id": organism.lineage_id,
                "x": organism.x,
                "y": organism.y,
                "energy": round(organism.energy, 4),
                "age": organism.age,
                "alive": organism.alive,
                "genome": organism.genome,
            }
            for organism in self.organisms
            if organism.alive
        ][: int(self.config["visual.max_rendered_organisms"])]
        return {
            "tick": self.tick,
            "world_width": self.config["world.width"],
            "world_height": self.config["world.height"],
            "energy_pool": round(self.energy_pool, 4),
            "memory_used": self._memory_used(),
            "organisms": visible,
        }

    def metrics(self) -> dict[str, Any]:
        active = sum(1 for organism in self.organisms if organism.alive)
        return {
            "tick": self.tick,
            "active_population": active,
            "births": self.births,
            "deaths": self.deaths,
            "energy_pool": round(self.energy_pool, 4),
            "memory_used": self._memory_used(),
        }
