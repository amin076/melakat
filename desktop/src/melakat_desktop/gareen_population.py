from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable


@dataclass(frozen=True)
class GareenMathematicalObject:
    """A Gareen research candidate living inside Melakat's population."""

    object_id: str
    statement: str
    generation: int
    parent_id: str | None
    lineage_id: str
    mathematical_value: float
    proof_status: str
    energy: float
    age: int = 0
    alive: bool = True

    @classmethod
    def from_gareen(
        cls,
        *,
        object_id: str,
        statement: str,
        mathematical_value: float,
        proof_status: str = "unproved",
        generation: int = 0,
        parent_id: str | None = None,
        lineage_id: str | None = None,
        energy: float = 10.0,
    ) -> "GareenMathematicalObject":
        return cls(
            object_id=object_id,
            statement=statement,
            generation=generation,
            parent_id=parent_id,
            lineage_id=lineage_id or object_id,
            mathematical_value=float(mathematical_value),
            proof_status=proof_status,
            energy=float(energy),
        )

    def reproduce_clone(
        self, child_id: str, offspring_energy: float
    ) -> "GareenMathematicalObject":
        """Create a lifecycle child without changing mathematical meaning.

        Mathematical mutation belongs to Gareen and is not invented by Melakat.
        """
        return replace(
            self,
            object_id=child_id,
            generation=self.generation + 1,
            parent_id=self.object_id,
            lineage_id=self.lineage_id,
            energy=offspring_energy,
            age=0,
            alive=True,
        )


class GareenPopulationEngine:
    """Melakat population dynamics for Gareen mathematical objects.

    Gareen owns mathematical meaning and research-value scoring.
    Melakat owns population resources, age, reproduction, death, and lineage.
    """

    def __init__(
        self,
        population: Iterable[GareenMathematicalObject],
        *,
        initial_energy: float = 0.0,
        energy_input_per_tick: float = 12.0,
        maintenance_cost: float = 1.0,
        reproduction_threshold: float = 8.0,
        reproduction_cost: float = 2.0,
        offspring_energy: float = 3.0,
        max_age: int = 6,
        max_population: int = 40,
    ) -> None:
        self.organisms = list(population)
        self.energy_pool = float(initial_energy)
        self.energy_input_per_tick = float(energy_input_per_tick)
        self.maintenance_cost = float(maintenance_cost)
        self.reproduction_threshold = float(reproduction_threshold)
        self.reproduction_cost = float(reproduction_cost)
        self.offspring_energy = float(offspring_energy)
        self.max_age = int(max_age)
        self.max_population = int(max_population)
        self.tick = 0
        self.next_id = len(self.organisms) + 1
        self.births = 0
        self.deaths = 0
        self.events: list[dict[str, object]] = []

    @staticmethod
    def _reproduction_factor(value: float) -> float:
        return 1.0 + max(0.0, min(value, 20.0)) / 20.0

    def _reproduction_threshold(
        self, organism: GareenMathematicalObject
    ) -> float:
        return self.reproduction_threshold / self._reproduction_factor(
            organism.mathematical_value
        )

    def step(self) -> None:
        self.tick += 1
        self.energy_pool += self.energy_input_per_tick

        active = [item for item in self.organisms if item.alive]
        for organism in active:
            captured = min(self.energy_pool, 1.0)
            organism = replace(
                organism,
                energy=organism.energy + captured - self.maintenance_cost,
                age=organism.age + 1,
            )
            self.energy_pool -= captured

            threshold = self._reproduction_threshold(organism)
            if (
                organism.energy >= threshold + self.reproduction_cost
                and len([item for item in self.organisms if item.alive])
                < self.max_population
            ):
                organism = replace(
                    organism,
                    energy=organism.energy - self.reproduction_cost,
                )
                child = organism.reproduce_clone(
                    f"G{self.next_id}",
                    self.offspring_energy,
                )
                self.next_id += 1
                self.births += 1
                self.organisms.append(child)
                self.events.append(
                    {
                        "type": "birth",
                        "tick": self.tick,
                        "parent_id": organism.object_id,
                        "child_id": child.object_id,
                        "lineage_id": child.lineage_id,
                        "mathematical_value": child.mathematical_value,
                    }
                )

            if organism.energy <= 0 or organism.age >= self.max_age:
                organism = replace(organism, alive=False)
                self.deaths += 1
                self.events.append(
                    {
                        "type": "death",
                        "tick": self.tick,
                        "object_id": organism.object_id,
                        "lineage_id": organism.lineage_id,
                    }
                )

            for index, current in enumerate(self.organisms):
                if current.object_id == organism.object_id:
                    self.organisms[index] = organism
                    break

    def metrics(self) -> dict[str, object]:
        active = [item for item in self.organisms if item.alive]
        values = [item.mathematical_value for item in active]
        return {
            "tick": self.tick,
            "active_population": len(active),
            "births": self.births,
            "deaths": self.deaths,
            "mean_mathematical_value": (
                sum(values) / len(values) if values else 0.0
            ),
            "max_mathematical_value": max(values, default=0.0),
            "total_energy": sum(item.energy for item in active) + self.energy_pool,
            "distinct_lineages": len({item.lineage_id for item in active}),
        }

    def snapshot(self) -> list[dict[str, object]]:
        return [
            {
                "id": item.object_id,
                "parent_id": item.parent_id,
                "lineage_id": item.lineage_id,
                "generation": item.generation,
                "statement": item.statement,
                "mathematical_value": item.mathematical_value,
                "proof_status": item.proof_status,
                "energy": round(item.energy, 4),
                "age": item.age,
            }
            for item in self.organisms
            if item.alive
        ]
