# Phase Two Frozen Baseline

[فارسی](phase-two-frozen-baseline.fa.md) | [Completion report](phase-two-completion-report.md)

## Status

**Phase Two is closed and frozen as the accepted spatial/local-resource reference for all later Melakat research.**

Frozen scientific versions:

- world contract: `phase-two-spatial-0.7`
- engine: `phase-two-vm-0.7`
- measurement contract: `phase-two-measurement-0.1`
- evidence format: `melakat-phase-two-evidence-0.1`
- spatial run artifact: `melakat-run-artifact-0.2`

The accepted Phase Two evidence gate remains the 12-condition × 30-seed × 2000-tick campaign documented in `phase-two-completion-report.md` and archived under `results/phase-two/evidence-gate/`.

## Freeze rule

Later phases must not silently reinterpret or overwrite Phase Two.

A later change may add code shared by newer phases only when the frozen Phase Two behavior and accepted evidence contract remain unchanged. Any actual correction to Phase Two itself requires a documented correction note, explicit version increment, regression evidence, and an explanation of why the accepted baseline changed.

In particular, Phase Three must not change the Phase Two definitions of:

- VM instruction semantics;
- reproduction and mutation rules;
- memory accounting;
- spatial topology and boundary rules;
- local cell capture semantics;
- uniform local-resource initialization and renewal;
- energy/resource conservation tolerances;
- the permanent Phase One homogeneous compatibility control.

## Accepted evidence

The final accepted Phase Two evidence campaign reports:

- conditions: `12`
- seeds per condition: `30`
- completed runs: `360 / 360`
- validation failures: `0`
- maximum absolute energy-balance error: `1.02e-08`
- maximum absolute local-resource balance error: `4.2e-09`
- tolerance: `1e-07`
- deterministic repeat: `PASS`
- repeated checksum: `858e5ffa6b77d7f71067af1e9422a7873f3cff85e4b26735987c5ee5162a4dd3`
- accepted source commit: `ad5e21159baf0d6bd79a028799b9318ba144fed7`
- evidence workflow run: `33969619473`

These values are the acceptance record for Phase Two. Later exploratory campaigns do not replace this gate.

## Scientific interpretation boundary

Phase Two demonstrated that spatial localization and local resource accessibility can create qualitatively different model regimes, including extinction under some local-resource conditions and survival with higher turnover under more abundant resource conditions. It did **not** establish adaptive navigation, cooperation, competition, niche formation, or open-ended evolution.

Those questions belong to later explicitly versioned phases.

## Handoff to Phase Three

Phase Three begins from this frozen baseline and introduces exactly one first causal intervention:

> spatially heterogeneous resource allocation while total initial resource and per-tick resource input remain matched to a uniform control.

The first Phase Three contract is `phase-three-environment-0.1`.
