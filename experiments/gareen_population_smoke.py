"""Run real Gareen research candidates through Melakat population dynamics.

Usage:
    python experiments/gareen_population_smoke.py --gareen-root ../gareen
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_gareen_candidates(gareen_root: Path, limit: int | None = None):
    root = str(gareen_root.resolve())
    if root not in sys.path:
        sys.path.insert(0, root)

    from artificial_mathematician import generate_research_conjectures
    from math_world import build_initial_knowledge
    from research_value import rank_research_conjectures

    state = build_initial_knowledge()
    conjectures = generate_research_conjectures(state)
    ranked = rank_research_conjectures(
        conjectures,
        state,
        min_reasoning_steps=3,
        min_score=14,
    )

    accepted = [item for item in ranked if item.assessment.accepted]
    selected = accepted[:limit]
    return [
        {
            "id": f"T{i + 1}",
            "statement": str(item.conjecture.statement),
            "mathematical_value": float(item.assessment.score),
            "proof_status": "unproved",
            "value_components": {
                "generality": item.assessment.variable_count,
                "reuse_potential": item.assessment.reuse_potential,
                "structural_richness": item.assessment.structural_richness,
                "known_derivation_distance": item.assessment.known_derivation_distance,
            },
        }
        for i, item in enumerate(selected)
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gareen-root", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--ticks", type=int, default=6)
    args = parser.parse_args()

    from melakat_desktop.gareen_population import (
        GareenMathematicalObject,
        GareenPopulationEngine,
    )

    all_records = load_gareen_candidates(args.gareen_root, None)
    records = all_records[: args.limit]
    if not records:
        raise SystemExit("No research-worthy Gareen candidates were produced.")

    population = [
        GareenMathematicalObject.from_gareen(
            object_id=item["id"],
            statement=item["statement"],
            mathematical_value=item["mathematical_value"],
            proof_status=item["proof_status"],
        )
        for item in records
    ]

    unused_records = all_records[args.limit :]
    used_statements = {item.statement for item in population}

    def gareen_offspring_factory(parent, child_id, offspring_energy):
        for item in unused_records:
            if item["statement"] == parent.statement:
                continue
            if item["statement"] in used_statements:
                continue
            used_statements.add(item["statement"])
            return GareenMathematicalObject.from_gareen(
                object_id=child_id,
                statement=item["statement"],
                mathematical_value=item["mathematical_value"],
                proof_status=item["proof_status"],
                generation=parent.generation + 1,
                parent_id=parent.object_id,
                lineage_id=parent.lineage_id,
                energy=offspring_energy,
                value_components=item["value_components"],
            )
        return None

    engine = GareenPopulationEngine(
        population,
        initial_energy=0,
        energy_input_per_tick=12,
        maintenance_cost=1,
        reproduction_threshold=8,
        reproduction_cost=2,
        offspring_energy=3,
        max_age=6,
        max_population=40,
    )

    history = [engine.metrics()]
    for _ in range(args.ticks):
        engine.step()
        history.append(engine.metrics())

    births = [event for event in engine.events if event["type"] == "birth"]\n    changed_births = [event for event in births if event["statement_changed"]]\n    if not changed_births:\n        raise SystemExit("No distinct Gareen offspring were born.")\n\n    report = {
        "integration": "gareen-objects-in-melakat-population",
        "gareen_candidates": records,
        "ticks": args.ticks,
        "final_metrics": engine.metrics(),
        "history": history,
        "events": engine.events,
        "final_population": engine.snapshot(),
        "mathematically_distinct_births": len(changed_births),\n        "generator_mode": "gareen_global_generator",\n        "parent_conditioned_mutation": "not_yet_implemented",
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
