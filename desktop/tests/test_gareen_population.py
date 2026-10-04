from __future__ import annotations

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


def test_mathematical_value_changes_population_dynamics():
    low = GareenMathematicalObject.from_gareen(
        object_id="T-low",
        statement="low",
        mathematical_value=0,
        energy=0,
    )
    high = GareenMathematicalObject.from_gareen(
        object_id="T-high",
        statement="high",
        mathematical_value=20,
        energy=0,
    )

    engine = GareenPopulationEngine(
        [low, high],
        energy_input_per_tick=8,
        reproduction_threshold=4,
        reproduction_cost=1,
        offspring_energy=1,
        max_age=20,
        max_population=10,
    )
    engine.step()

    births_by_parent = {
        event["parent_id"]
        for event in engine.events
        if event["type"] == "birth"
    }
    assert "T-high" in births_by_parent
    assert "T-low" not in births_by_parent


def test_engine_preserves_gareen_proof_status():
    item = GareenMathematicalObject.from_gareen(
        object_id="T1",
        statement="candidate",
        mathematical_value=15,
        proof_status="unproved",
        energy=10,
    )
    engine = GareenPopulationEngine([item], energy_input_per_tick=0)
    engine.step()

    assert engine.snapshot()[0]["proof_status"] == "unproved"
