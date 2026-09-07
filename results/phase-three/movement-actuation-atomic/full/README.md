# Phase Three atomic movement-actuation evidence

This directory archives the full matched-seed evidence campaign for the Phase Three `phase-three-vm-0.3` atomic movement-payment semantics.

## Campaign

- 30 matched seeds;
- 2 conditions;
- 2000 ticks per run;
- 60 completed runs;
- control: movement execution off;
- treatment: movement execution on;
- hereditary movement availability and `mutation.movement_step_rate=0.5` matched in both conditions;
- resource sensing disabled in both conditions;
- `world.atomic_movement_payment_enabled=true` in both conditions.

## Mechanical result

The verification gate passed. The control committed no movement. The treatment committed 129 non-zero movement operations over 129.0 distance units and paid 12.9 movement-energy units. Four additional non-zero movement attempts (4.0 distance units) were rejected before commit because later execution-energy payment failed. No committed realized movement was underpaid.

Maximum absolute energy-balance error was 4.60e-09; maximum absolute local-resource balance error was 5.80e-09; deterministic reproducibility passed.

## Scientific interpretation

This campaign establishes the **movement execution/accounting mechanism**, not navigation or adaptation. The selected matched population/ecological outcomes have approximate 95% paired intervals that cross zero, so this campaign does not support a robust directional population effect from movement execution alone.

The result therefore opens the next controlled gate: a sensing-plus-movement experiment can now ask whether information coupled to locomotion changes spatial/resource outcomes. That future experiment must retain the v0.3 atomic-payment semantics and must not pre-program resource seeking.

See `campaign-verification.json`, `paired-analysis.json`, `merge-readiness.json`, `validation.json`, and `runs.csv` for machine-readable evidence.
