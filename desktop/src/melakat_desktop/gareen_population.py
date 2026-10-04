from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Callable, Iterable, Mapping


OffspringFactory = Callable[
    ["GareenMathematicalObject", str, float],
    "GareenMathematicalObject | None",
]


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
    research_accepted: bool = True
    value_components: Mapping[str, float | int | None] = field(default_factory=dict)
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
        research_accepted: bool = True,
        value_components: Mapping[str, float | int | None] | None = None,
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
            research_accepted=research_accepted,
            value_components=dict(value_components or {}),
        )

    def reproduce_clone(
        self, child_id: str, offspring_energy: float
    ) -> "GareenMathematicalObject":
        """Legacy lifecycle helper.

        Evolution runs should supply an offspring_factory so Gareen creates a
        mathematically distinct child. This method remains only for backwards
        compatibility with old lifecycle tests.
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
    """Resource selection for Gareen mathematical objects inside Melakat.

    Gareen owns conjecture generation and research-value assessment. Melakat
    turns that assessment into scarce resource allocation and population
    pressure. Reproduction can call back into Gareen through offspring_factory;
    when no factory is supplied, legacy clone reproduction is used.
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
        rejected_resource_weight: float = 0.10,
        offspring_factory: OffspringFactory | None = None,
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
        self.rejected_resource_weight = float(rejected_resource_weight)
        self.offspring_factory = offspring_factory
        self.tick = 0
        self.next_id = len(self.organisms) + 1
        self.births = 0
        self.deaths = 0
        self.events: list[dict[str, object]] = []

    def _fitness_weight(self, organism: GareenMathematicalObject) -> float:
        """Convert Gareen research value into a positive resource weight.

        Rejected/trivial candidates retain a small non-zero share, preserving
        diversity without letting them consume the main research budget.
        """
        base = max(0.25, organism.mathematical_value)
        if not organism.research_accepted:
            base *= self.rejected_resource_weight
        return base

    def _resource_allocations(
        self, active: list[GareenMathematicalObject]
    ) -> dict[str, float]:
        available = min(self.energy_pool, self.energy_input_per_tick)
        if not active or available <= 0:
            return {item.object_id: 0.0 for item in active}

        weights = {item.object_id: self._fitness_weight(item) for item in active}
        total = sum(weights.values())
        if total <= 0:
            share = available / len(active)
            return {item.object_id: share for item in active}
        return {
            object_id: available * weight / total
            for object_id, weight in weights.items()
        }

    @staticmethod
    def _reproduction_factor(value: float) -> float:
        return 1.0 + max(0.0, min(value, 40.0)) / 40.0

    def _threshold_for(self, organism: GareenMathematicalObject) -> float:
        threshold = self.reproduction_threshold / self._reproduction_factor(
            organism.mathematical_value
        )
        if not organism.research_accepted:
            threshold /= max(self.rejected_resource_weight, 0.01)
        return threshold

    def _make_child(
        self, organism: GareenMathematicalObject, child_id: str
    ) -> GareenMathematicalObject | None:
        if self.offspring_factory is not None:
            return self.offspring_factory(
                organism,
                child_id,
                self.offspring_energy,
            )
        return organism.reproduce_clone(child_id, self.offspring_energy)

    def step(self) -> None:
        self.tick += 1
        self.energy_pool += self.energy_input_per_tick

        active = [item for item in self.organisms if item.alive]
        allocations = self._resource_allocations(active)

        for original in active:
            captured = min(
                self.energy_pool,
                allocations.get(original.object_id, 0.0),
            )
            organism = replace(
                original,
                energy=original.energy + captured - self.maintenance_cost,
                age=original.age + 1,
            )
            self.energy_pool -= captured
            self.events.append(
                {
                    "type": "resource_allocation",
                    "tick": self.tick,
                    "object_id": organism.object_id,
                    "mathematical_value": organism.mathematical_value,
                    "research_accepted": organism.research_accepted,
                    "allocated_energy": round(captured, 6),
                }
            )

            threshold = self._threshold_for(organism)
            if (
                organism.energy >= threshold + self.reproduction_cost
                and len([item for item in self.organisms if item.alive])
                < self.max_population
            ):
                child_id = f"G{self.next_id}"
                child = self._make_child(organism, child_id)
                if child is not None:
                    if child.statement == organism.statement and self.offspring_factory is not None:
                        raise ValueError(
                            "Gareen offspring_factory returned the parent statement; "
                            "evolutionary offspring must be mathematically distinct."
                        )
                    organism = replace(
                        organism,
                        energy=organism.energy - self.reproduction_cost,
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
                            "parent_mathematical_value": organism.mathematical_value,
                            "child_mathematical_value": child.mathematical_value,
                            "statement_changed": child.statement != organism.statement,
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
        accepted = [item for item in active if item.research_accepted]
        return {
            "tick": self.tick,
            "active_population": len(active),
            "research_worthy_population": len(accepted),
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
                "research_accepted": item.research_accepted,
                "value_components": dict(item.value_components),
                "proof_status": item.proof_status,
                "energy": round(item.energy, 4),
                "age": item.age,
            }
            for item in self.organisms
            if item.alive
        ]
