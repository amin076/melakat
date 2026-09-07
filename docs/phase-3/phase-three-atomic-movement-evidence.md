# Phase Three atomic movement-actuation evidence

[فارسی](phase-three-atomic-movement-evidence.fa.md) | English

## Purpose

This report records the full Phase Three evidence gate for the `phase-three-vm-0.3` atomic movement-payment semantics. It follows the earlier movement-actuation diagnostic that exposed an accounting-order problem: a movement effect could be committed before the later aggregate execution-energy charge failed. The v0.3 intervention stages movement and commits it only after the relevant energy charges succeed.

This is a mechanism and accounting experiment. It is not a navigation, adaptation, resource-seeking, intelligence, cooperation, predation, or fitness experiment.

## Experimental contrast

The campaign used 30 matched seeds and two conditions, each for 2000 ticks, for 60 completed runs in total.

Both conditions used:

- `run.engine_backend=phase-three-vm`;
- `world.resource_distribution_mode=center_patch`;
- hereditary movement availability enabled;
- `mutation.movement_step_rate=0.5`;
- `world.atomic_movement_payment_enabled=true`;
- resource sensing disabled;
- the same resource, mutation, reproduction, memory, topology, and local-capture rules.

The only intended causal difference was movement execution:

- control: `world.movement_enabled=false`;
- treatment: `world.movement_enabled=true`.

The engine and measurement versions were `phase-three-vm-0.3` and `phase-three-measurement-0.3` in every run.

## Mechanical result

The campaign verification gate passed with zero recorded failures.

Across the 30 treatment runs:

- `movement_operations`: 256;
- committed non-zero movement operations: 129;
- committed zero-step movement operations: 127;
- committed movement distance: 129.0 units;
- movement-energy cost: 12.9 units.

The matched control committed no movement and paid no movement-energy cost.

Four additional non-zero movement attempts, totaling 4.0 distance units, were staged but not committed because a later execution-energy payment failed. These rejected attempts are recorded as uncommitted diagnostics rather than realized movement. No committed realized-movement run was underpaid.

The movement partition identity also held: committed movement operations equal committed non-zero plus committed zero-step operations.

## Conservation and reproducibility

The maximum absolute energy-balance error was `4.6e-09`, and the maximum absolute local-resource balance error was `5.8e-09`. Both are far below the existing `1e-07` tolerances.

Deterministic reproducibility passed.

## Paired analysis

The corrected paired analysis reads dynamic Phase Three metrics from `campaign.json`. The legacy `runs.csv` export does not yet contain all newer Phase Three-only fields, so it must not be used as the sole source for these metrics.

For movement execution itself, the treatment-minus-control mean number of `movement_operations` was `8.5333`, with an approximate 95% interval `[3.9809, 13.0858]`; 24 of 30 matched pairs were positive and six were zero.

Realized non-zero movement was sparse and highly skewed across seeds. Fourteen of 30 matched pairs produced positive realized movement and 16 produced none. The mean treatment-minus-control realized distance was `4.3` units, with an approximate normal 95% interval `[-0.1230, 8.7230]`. One seed produced a much larger movement response than most others. Therefore the mechanism is established by direct execution/accounting evidence, but the average realized-distance effect should not be described as a clean, normally distributed directional effect across seeds.

All selected population/ecological outcomes had approximate paired 95% intervals crossing zero:

- active population;
- births;
- deaths;
- historical genotypes;
- blocked divisions;
- mean local neighbors;
- mean nearest-neighbor distance.

The campaign therefore does not establish a robust directional population or ecological effect from movement execution alone.

## Scientific interpretation

The accepted interpretation is narrow:

1. Phase Three can execute inherited movement instructions under the v0.3 atomic-payment semantics.
2. Realized committed movement is energy-accounted; failed later payment does not leave a committed movement side effect.
3. Movement execution alone, in this campaign, does not show a robust directional effect on the selected population/ecological outcomes.
4. These findings do not establish navigation, adaptation, resource seeking, fitness advantage, intelligence, cooperation, predation, or open-ended evolution.

This result opens the next controlled gate: a sensing-plus-movement experiment may test whether information coupled to locomotion changes spatial or resource outcomes. That future experiment must preserve v0.3 atomic movement semantics and must not hard-code resource seeking.

## Evidence archive

Machine-readable evidence is stored under:

`results/phase-three/movement-actuation-atomic/full/`

Key files include:

- `campaign-verification.json`;
- `paired-analysis.json`;
- `merge-readiness.json`;
- `validation.json`;
- `campaign.json`;
- `runs.csv`;
- `summary.json`;
- `SHA256SUMS.txt`.

The evidence record is marked `READY_FOR_MERGE_REVIEW` after the campaign, conservation, reproducibility, atomic-payment, and selected-population interpretation gates passed.
