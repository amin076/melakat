from __future__ import annotations

import pytest

from melakat_desktop.gareen_population import (
    GareenMathematicalObject,
    GareenPopulationEngine,
)


def test_gareen_object_keeps_mathematical_identity_and_lineage():
    parent = GareenMathematicalObject.from_gareen(
        object_id="T1",
        statement="forall x, x + 0 = x",
        mathematical_value=18,
        proof_status="verified",
    )
    child = parent.reproduce_clone("G2", offspring_energy=3)

    assert child.statement == parent.statement
    assert child.parent_id == "T1"
    assert child.lineage_id == parent.lineage_id
    assert child.generation == 1


def test_higher_research_value_receives_more_scarce_energy():
    low = GareenMathematicalObject.from_gareen(
        object_id="T-low",
        statement="5 + 0 = 5",
        mathematical_value=2,
        research_accepted=False,
        energy=2,
    )
    high = GareenMathematicalObject.from_gareen(
        object_id="T-high",
        statement="forall x, x + 0 = x",
        mathematical_value=20,
        research_accepted=True,
        energy=2,
    )
    engine = GareenPopulationEngine(
        [low, high],
        energy_input_per_tick=10,
        maintenance_cost=0,
        reproduction_threshold=100,
        max_age=20,
    )
    engine.step()
    snapshot = {item["id"]: item for item in engine.snapshot()}

    assert snapshot["T-high"]["energy"] > snapshot["T-low"]["energy"]


def test_rejected_candidate_keeps_small_nonzero_resource_share():
    rejected = GareenMathematicalObject.from_gareen(
        object_id="T-ground",
        statement="5 + 0 = 5",
        mathematical_value=10,
        research_accepted=False,
        energy=1,
    )
    accepted = GareenMathematicalObject.from_gareen(
        object_id="T-general",
        statement="forall x, x + 0 = x",
        mathematical_value=10,
        research_accepted=True,
        energy=1,
    )
    engine = GareenPopulationEngine(
        [rejected, accepted],
        energy_input_per_tick=11,
        maintenance_cost=0,
        reproduction_threshold=100,
        rejected_resource_weight=0.1,
    )
    engine.step()
    allocations = {
        event["object_id"]: event["allocated_energy"]
        for event in engine.events
        if event["type"] == "resource_allocation"
    }

    assert allocations["T-ground"] > 0
    assert allocations["T-general"] > allocations["T-ground"]


def test_offspring_factory_must_create_new_mathematics():
    parent = GareenMathematicalObject.from_gareen(
        object_id="T1",
        statement="forall x, x + 0 = x",
        mathematical_value=20,
        energy=20,
    )

    def bad_factory(parent, child_id, offspring_energy):
        return GareenMathematicalObject.from_gareen(
            object_id=child_id,
            statement=parent.statement,
            mathematical_value=parent.mathematical_value,
            parent_id=parent.object_id,
            lineage_id=parent.lineage_id,
            generation=parent.generation + 1,
            energy=offspring_energy,
        )

    engine = GareenPopulationEngine(
        [parent],
        energy_input_per_tick=0,
        maintenance_cost=0,
        reproduction_threshold=1,
        reproduction_cost=1,
        offspring_factory=bad_factory,
    )
    with pytest.raises(ValueError, match="mathematically distinct"):
        engine.step()


def test_offspring_factory_can_birth_distinct_gareen_candidate():
    parent = GareenMathematicalObject.from_gareen(
        object_id="T1",
        statement="forall x, x + 0 = x",
        mathematical_value=20,
        energy=20,
    )

    def gareen_factory(parent, child_id, offspring_energy):
        return GareenMathematicalObject.from_gareen(
            object_id=child_id,
            statement="forall x, 0 + x = x",
            mathematical_value=24,
            parent_id=parent.object_id,
            lineage_id=parent.lineage_id,
            generation=parent.generation + 1,
            energy=offspring_energy,
            value_components={"generality": 1, "novelty": 8},
        )

    engine = GareenPopulationEngine(
        [parent],
        energy_input_per_tick=0,
        maintenance_cost=0,
        reproduction_threshold=1,
        reproduction_cost=1,
        offspring_factory=gareen_factory,
    )
    engine.step()

    child = next(item for item in engine.snapshot() if item["parent_id"] == "T1")
    assert child["statement"] != parent.statement
    assert child["mathematical_value"] == 24
    assert child["lineage_id"] == parent.lineage_id


def test_engine_preserves_gareen_proof_status_and_value_components():
    item = GareenMathematicalObject.from_gareen(
        object_id="T1",
        statement="candidate",
        mathematical_value=15,
        proof_status="unproved",
        value_components={"generality": 2, "reuse_potential": 3},
        energy=10,
    )
    engine = GareenPopulationEngine(
        [item],
        energy_input_per_tick=0,
        reproduction_threshold=100,
    )
    engine.step()

    snapshot = engine.snapshot()[0]
    assert snapshot["proof_status"] == "unproved"
    assert snapshot["value_components"]["generality"] == 2
