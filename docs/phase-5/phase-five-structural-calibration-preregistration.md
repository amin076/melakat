# Phase Five Gate 5C — Structural Mutation Exposure Calibration

## Status

**Pre-registered before calibration data are inspected.**

This gate does not ask whether a structural mutation rate improves population performance, genome size, persistence, or any other evolutionary outcome. Its only purpose is to choose the **lowest** candidate non-zero rate that produces enough structural-event exposure for the later matched-seed inferential campaign to be interpretable.

## Fixed calibration design

Specification: `experiments/phase-five/structural-rate-calibration.json`

- backend: `phase-five-vm`
- 8 matched seeds per condition
- 1000 ticks per run
- balanced structural event type: duplication probability `0.5`
- substitution rate: `0.01`
- structural candidate rates: `0.00`, `0.01`, `0.05`, `0.10`, `0.20`
- homogeneous finite-energy/finite-memory Phase Five world
- spatial, local-resource, sensing and movement mechanisms disabled for causal isolation

The zero-rate condition is a calibration control and is not eligible for selection.

## Pre-registered promotion rule

Evaluate non-zero candidate rates in ascending order. Select the **first** candidate satisfying all of the following:

1. all 8 runs complete;
2. validation failures = `0`;
3. deterministic reproducibility replay = PASS for the campaign control;
4. total committed structural events across the 8 candidate runs >= `20`;
5. structural-event-exposed runs >= `6/8`;
6. total variable-length births across the 8 candidate runs >= `10`;
7. energy-balance error remains within the accepted `1e-7` tolerance;
8. no invalid empty genome is committed.

If no candidate satisfies the rule, Gate 5C fails and a new calibration design must be pre-registered. The threshold must not be relaxed after seeing results.

## Forbidden selection criteria

The chosen rate must **not** depend on:

- higher or lower final population;
- higher or lower genome length;
- more persistent variable-length lineages;
- more genotypes or lineages;
- fewer deaths or faults;
- higher generation depth;
- any result that looks biologically interesting or favorable.

Those are later scientific outcomes, not calibration criteria.

## Interpretation boundary

Passing Gate 5C establishes only that a pre-declared structural mutation rate gives sufficient exposure for Gate 5D. It is not evidence of complexity, adaptation, fitness improvement, or open-ended evolution.
