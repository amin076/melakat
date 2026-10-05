"""Five-generation Gareen -> Melakat evolutionary campaign.

This runner deliberately keeps mathematical creativity outside Melakat.
Each generation consumes a batch of Gareen-verified children, lets Melakat
apply scarce-resource selection, and emits the surviving/reproductively
eligible parents for the next AI neighbourhood-generation round.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from melakat_desktop.gareen_population import GareenMathematicalObject, GareenPopulationEngine


def load_verified_batch(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload["candidates"] if isinstance(payload, dict) else payload
    return [r for r in records if r.get("proof_status") == "verified"]


def make_population(records: list[dict], initial_energy: float) -> list[GareenMathematicalObject]:
    population = []
    for i, r in enumerate(records):
        parent_ids = tuple(r.get("parent_ids") or ([r["parent_id"]] if r.get("parent_id") else []))
        population.append(
            GareenMathematicalObject(
                object_id=r.get("id", f"T{i+1}"),
                statement=r["statement"],
                generation=int(r.get("generation", 0)),
                parent_id=(parent_ids[0] if parent_ids else None),
                lineage_id=r.get("lineage_id") or (parent_ids[0] if parent_ids else r.get("id", f"T{i+1}")),
                parent_ids=parent_ids,
                mathematical_value=float(r["mathematical_value"]),
                proof_status="verified",
                energy=float(r.get("energy", initial_energy)),
                research_accepted=bool(r.get("research_accepted", True)),
                value_components=dict(r.get("value_components", {})),
            )
        )
    return population


def run_generation(records: list[dict], *, generation: int, max_population: int,
                   energy_input: float, ticks: int) -> dict:
    population = make_population(records, initial_energy=4.0)
    engine = GareenPopulationEngine(
        population,
        initial_energy=0,
        energy_input_per_tick=energy_input,
        maintenance_cost=1.0,
        reproduction_threshold=10**9,  # AI/Gareen, not Melakat, creates mathematics.
        max_age=max(ticks + 2, 6),
        max_population=max_population,
        offspring_factory=None,
    )
    history = [engine.metrics()]
    for _ in range(ticks):
        engine.step()
        history.append(engine.metrics())

    survivors = sorted(
        engine.snapshot(),
        key=lambda x: (-float(x["energy"]), -float(x["mathematical_value"]), x["id"]),
    )[:max_population]

    next_parent_requests = [
        {
            "parent_id": x["id"],
            "statement": x["statement"],
            "generation": generation,
            "mathematical_value": x["mathematical_value"],
            "energy": x["energy"],
            "request": "Generate one-step mathematical-neighbourhood conjectures around this verified parent.",
        }
        for x in survivors
    ]
    return {
        "generation": generation,
        "input_verified": len(records),
        "survivors": len(survivors),
        "history": history,
        "survivor_population": survivors,
        "next_ai_parent_requests": next_parent_requests,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--verified-batch", type=Path, required=True)
    p.add_argument("--generation", type=int, required=True)
    p.add_argument("--max-population", type=int, default=5000)
    p.add_argument("--energy-input", type=float, default=100.0)
    p.add_argument("--ticks", type=int, default=5)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()

    records = load_verified_batch(args.verified_batch)
    report = run_generation(
        records,
        generation=args.generation,
        max_population=args.max_population,
        energy_input=args.energy_input,
        ticks=args.ticks,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
