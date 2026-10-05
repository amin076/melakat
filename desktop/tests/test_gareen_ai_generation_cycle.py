from melakat_desktop.gareen_population import GareenMathematicalObject
from pathlib import Path
import importlib.util

MODULE = Path(__file__).parents[2] / "experiments" / "gareen_ai_generation_cycle.py"
spec = importlib.util.spec_from_file_location("cycle", MODULE)
cycle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cycle)


def test_generation_cycle_selects_verified_population_and_emits_parent_requests():
    records = [
        {"id": "A", "statement": "A", "mathematical_value": 30, "proof_status": "verified", "research_accepted": True},
        {"id": "B", "statement": "B", "mathematical_value": 10, "proof_status": "verified", "research_accepted": True},
    ]
    report = cycle.run_generation(records, generation=1, max_population=2, energy_input=10, ticks=2)
    assert report["input_verified"] == 2
    assert report["survivors"] == 2
    assert len(report["next_ai_parent_requests"]) == 2
    assert report["next_ai_parent_requests"][0]["generation"] == 1


def test_multi_parent_provenance_is_preserved():
    records = [{
        "id": "C", "statement": "C", "mathematical_value": 20,
        "proof_status": "verified", "parent_ids": ["A", "B"], "generation": 2
    }]
    pop = cycle.make_population(records, 4)
    assert pop[0].parent_ids == ("A", "B")
