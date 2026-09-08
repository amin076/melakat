from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path
from typing import Any


CANDIDATES = (0.01, 0.025, 0.05, 0.10)
CALIBRATION_THRESHOLDS = {
    "committed_events": 16,
    "exposed_runs": 6,
    "duplications": 4,
    "deletions": 4,
}

STRUCTURAL_ENDPOINTS = (
    "structural_mutation_operations",
    "structural_mutation_committed_operations",
    "instruction_duplication_operations",
    "instruction_deletion_operations",
    "structural_length_delta_total",
    "variable_length_births",
    "variable_length_reproducing_offspring",
    "variable_length_active_population",
    "genome_length_mean",
    "genome_length_median",
    "genome_length_minimum",
    "genome_length_maximum",
    "genome_length_variance",
    "distinct_genome_lengths",
)
COST_ENDPOINTS = (
    "genome_memory_used",
    "replication_copy_operations",
    "instructions_executed",
    "memory_used",
    "free_memory",
    "blocked_divisions",
    "waiting_for_memory",
    "waiting_for_energy",
)
SECONDARY_ENDPOINTS = (
    "active_population",
    "births",
    "deaths",
    "max_population",
    "historical_genotypes",
    "active_genotypes",
    "active_lineages",
    "max_generation",
    "faults",
)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _rate_from_condition(name: str) -> float:
    return float(name.rsplit("-", 1)[-1])


def calibrate(campaign_path: Path, output_path: Path, full_spec_path: Path) -> None:
    campaign = load(campaign_path)
    validation = campaign["validation"]
    if not validation.get("passed"):
        raise SystemExit("calibration validation failed")
    runs = campaign["runs"]
    rows: list[dict[str, Any]] = []
    selected: float | None = None
    for candidate in CANDIDATES:
        name = f"structural-rate-{candidate:.3f}".rstrip("0").rstrip(".")
        subset = [r for r in runs if abs(_rate_from_condition(str(r["condition"])) - candidate) < 1e-12]
        committed = sum(int(r.get("structural_mutation_committed_operations", 0)) for r in subset)
        duplications = sum(int(r.get("instruction_duplication_operations", 0)) for r in subset)
        deletions = sum(int(r.get("instruction_deletion_operations", 0)) for r in subset)
        exposed = sum(int(r.get("structural_mutation_committed_operations", 0)) > 0 for r in subset)
        passed = (
            len(subset) == 8
            and committed >= CALIBRATION_THRESHOLDS["committed_events"]
            and exposed >= CALIBRATION_THRESHOLDS["exposed_runs"]
            and duplications >= CALIBRATION_THRESHOLDS["duplications"]
            and deletions >= CALIBRATION_THRESHOLDS["deletions"]
        )
        rows.append(
            {
                "rate": candidate,
                "run_count": len(subset),
                "committed_events": committed,
                "exposed_runs": exposed,
                "duplications": duplications,
                "deletions": deletions,
                "passes_exposure_gate": passed,
            }
        )
        if selected is None and passed:
            selected = candidate
    if selected is None:
        raise SystemExit("no candidate structural event rate passed the pre-registered exposure gate")

    decision = {
        "format": "melakat-phase-five-calibration-decision-0.1",
        "experiment": campaign["experiment"],
        "selection_basis": "exposure_only",
        "candidate_rates": list(CANDIDATES),
        "thresholds": CALIBRATION_THRESHOLDS,
        "rows": rows,
        "selected_structural_event_rate": selected,
        "validation_passed": True,
        "reproducibility_identical": bool(validation["reproducibility"]["identical"]),
        "forbidden_selection_criteria_used": False,
    }
    dump(output_path, decision)

    base = dict(campaign["plan"]["base_config"])
    base["run.max_ticks"] = 2000
    base["mutation.structural_event_rate"] = 0.0
    full_spec = {
        "format": "melakat-experiment-spec-0.1",
        "name": "phase-five-variable-genome-full",
        "description": (
            "Gate 5D full matched-seed campaign. Control and treatment share the Phase Five "
            "length-robust substrate, substitution channel, energy, memory, execution and reproduction "
            "rules. The only intended causal difference is the pre-calibrated balanced structural event rate."
        ),
        "base_config": base,
        "seeds": {"start": 1, "count": 30},
        "conditions": [
            {
                "name": "structural-off",
                "overrides": {
                    "mutation.structural_event_rate": 0.0,
                    "mutation.structural_duplication_probability": 0.5,
                },
            },
            {
                "name": "structural-balanced-on",
                "overrides": {
                    "mutation.structural_event_rate": selected,
                    "mutation.structural_duplication_probability": 0.5,
                },
            },
        ],
        "reproducibility": {"condition": "structural-off", "seed": 1},
        "frozen_from_calibration": {
            "selected_structural_event_rate": selected,
            "selection_basis": "lowest candidate passing exposure-only gate",
            "calibration_decision": str(output_path),
        },
    }
    dump(full_spec_path, full_spec)


def paired_metric(control: dict[int, dict[str, Any]], treatment: dict[int, dict[str, Any]], metric: str) -> dict[str, Any]:
    seeds = sorted(set(control) & set(treatment))
    deltas = [float(treatment[s].get(metric, 0.0)) - float(control[s].get(metric, 0.0)) for s in seeds]
    cvals = [float(control[s].get(metric, 0.0)) for s in seeds]
    tvals = [float(treatment[s].get(metric, 0.0)) for s in seeds]
    n = len(deltas)
    mean = statistics.fmean(deltas) if deltas else 0.0
    sd = statistics.stdev(deltas) if n > 1 else 0.0
    se = sd / math.sqrt(n) if n else 0.0
    lo, hi = mean - 1.96 * se, mean + 1.96 * se
    return {
        "n": n,
        "control_mean": statistics.fmean(cvals) if cvals else 0.0,
        "treatment_mean": statistics.fmean(tvals) if tvals else 0.0,
        "mean_treatment_minus_control": mean,
        "paired_sample_sd": sd,
        "standard_error": se,
        "approx_95_interval": [lo, hi],
        "interval_crosses_zero": lo <= 0.0 <= hi,
        "positive_pairs": sum(d > 0 for d in deltas),
        "negative_pairs": sum(d < 0 for d in deltas),
        "zero_pairs": sum(d == 0 for d in deltas),
        "deltas_by_seed": {str(seed): delta for seed, delta in zip(seeds, deltas)},
    }


def analyze(campaign_path: Path, output_dir: Path) -> None:
    campaign = load(campaign_path)
    validation = campaign["validation"]
    if not validation.get("passed"):
        raise SystemExit("full campaign validation failed")
    runs = campaign["runs"]
    control = {int(r["seed"]): r for r in runs if r["condition"] == "structural-off"}
    treatment = {int(r["seed"]): r for r in runs if r["condition"] == "structural-balanced-on"}
    if len(control) != 30 or len(treatment) != 30:
        raise SystemExit("full campaign requires 30 matched seeds per condition")

    groups = {
        "structural_outcomes": STRUCTURAL_ENDPOINTS,
        "cost_outcomes": COST_ENDPOINTS,
        "secondary_outcomes": SECONDARY_ENDPOINTS,
    }
    analysis: dict[str, Any] = {
        "format": "melakat-phase-five-paired-analysis-0.1",
        "experiment": campaign["experiment"],
        "n_matched_seeds": 30,
        "interval_method": "paired mean treatment-minus-control +/- 1.96 * sample_SD(delta)/sqrt(n)",
        "groups": {},
    }
    for group, metrics in groups.items():
        analysis["groups"][group] = {
            metric: paired_metric(control, treatment, metric) for metric in metrics
        }

    treatment_total_events = sum(int(r.get("structural_mutation_committed_operations", 0)) for r in treatment.values())
    treatment_dup = sum(int(r.get("instruction_duplication_operations", 0)) for r in treatment.values())
    treatment_del = sum(int(r.get("instruction_deletion_operations", 0)) for r in treatment.values())
    treatment_variable_births = sum(int(r.get("variable_length_births", 0)) for r in treatment.values())
    treatment_reproducers = sum(int(r.get("variable_length_reproducing_offspring", 0)) for r in treatment.values())
    treatment_exposed = sum(int(r.get("structural_mutation_committed_operations", 0)) > 0 for r in treatment.values())
    treatment_variable_active = sum(int(r.get("variable_length_active_population", 0)) > 0 for r in treatment.values())
    max_energy_error = max(abs(float(r.get("energy_balance_error", 0.0))) for r in runs)

    evidence = {
        "format": "melakat-phase-five-full-verification-0.1",
        "completed_runs": len(runs),
        "expected_runs": 60,
        "validation_passed": bool(validation.get("passed")),
        "validation_failure_count": int(validation.get("failure_count", 0)),
        "reproducibility_identical": bool(validation["reproducibility"]["identical"]),
        "maximum_absolute_energy_balance_error": max_energy_error,
        "control_structural_events": sum(int(r.get("structural_mutation_committed_operations", 0)) for r in control.values()),
        "treatment_structural_events": treatment_total_events,
        "treatment_duplications": treatment_dup,
        "treatment_deletions": treatment_del,
        "treatment_structural_exposed_runs": treatment_exposed,
        "treatment_variable_length_births": treatment_variable_births,
        "treatment_variable_length_reproducing_offspring": treatment_reproducers,
        "treatment_runs_with_variable_length_active_population": treatment_variable_active,
        "heritable_variable_length_evidenced": treatment_variable_births > 0 and treatment_reproducers > 0,
        "complexity_claim_authorized": False,
        "open_ended_evolution_claim_authorized": False,
    }
    dump(output_dir / "paired-analysis.json", analysis)
    dump(output_dir / "campaign-verification.json", evidence)

    readiness = {
        "format": "melakat-phase-five-merge-readiness-0.1",
        "passed": (
            evidence["completed_runs"] == 60
            and evidence["validation_passed"]
            and evidence["reproducibility_identical"]
            and evidence["maximum_absolute_energy_balance_error"] <= 1e-7
            and evidence["control_structural_events"] == 0
            and evidence["treatment_structural_events"] > 0
            and evidence["treatment_duplications"] > 0
            and evidence["treatment_deletions"] > 0
            and evidence["heritable_variable_length_evidenced"]
        ),
        "scientific_boundary": (
            "Passing establishes auditable heritable variable genome length under blind structural mutation. "
            "Genome length is not a complexity metric and this campaign does not establish adaptation, intelligence, or open-ended evolution."
        ),
    }
    dump(output_dir / "merge-readiness.json", readiness)
    if not readiness["passed"]:
        raise SystemExit("Phase Five full evidence gate did not pass")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p_cal = sub.add_parser("calibrate")
    p_cal.add_argument("campaign", type=Path)
    p_cal.add_argument("decision", type=Path)
    p_cal.add_argument("full_spec", type=Path)
    p_an = sub.add_parser("analyze")
    p_an.add_argument("campaign", type=Path)
    p_an.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    if args.command == "calibrate":
        calibrate(args.campaign, args.decision, args.full_spec)
    else:
        analyze(args.campaign, args.output_dir)


if __name__ == "__main__":
    main()
