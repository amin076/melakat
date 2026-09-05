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
        self.organisms: list[DemoOrganism] = []
        self._make_initial_population()

    def _make_initial_population(self) -> None:
        width = float(self.config["world.width"])
        height = float(self.config["world.height"])
        for _ in range(int(self.config["population.initial_size"])):
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

    def _mutate_genome(self, genome: list[int]) -> list[int]:
        rate = float(self.config["mutation.substitution_rate"])
        result = list(genome)
        for index, value in enumerate(result):
            if self.rng.random() < rate:
                result[index] = self.rng.randint(0, 7)
        return result

    def step(self) -> None:
        if self.tick >= int(self.config["run.max_ticks"]):
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

            if (
                self.config["reproduction.enabled"]
                and organism.energy >= float(self.config["reproduction.threshold"])
                and organism.age % int(self.config["reproduction.interval"]) == 0
            ):
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

        self.emit(make_event("tick", snapshot=self.snapshot(), metrics=self.metrics()))

    def snapshot(self) -> dict[str, Any]:
        visible = [
            {
                "id": o.organism_id,
                "parent_id": o.parent_id,
                "lineage_id": o.lineage_id,
                "x": o.x,
                "y": o.y,
                "energy": round(o.energy, 4),
                "age": o.age,
                "alive": o.alive,
                "genome": o.genome,
            }
            for o in self.organisms
            if o.alive
        ][: int(self.config["visual.max_rendered_organisms"])]
        return {
            "tick": self.tick,
            "energy_pool": round(self.energy_pool, 4),
            "organisms": visible,
        }

    def metrics(self) -> dict[str, Any]:
        active = sum(1 for o in self.organisms if o.alive)
        return {
            "tick": self.tick,
            "active_population": active,
            "births": self.births,
            "deaths": self.deaths,
            "energy_pool": round(self.energy_pool, 4),
        }
