# Phase Three Movement-Only Evidence Note

## Experimental question

With the Phase Three center-patch resource geography fixed, total resource budget fixed, mutation rate fixed, hereditary availability of `MOVE_X`/`MOVE_Y` matched, and resource sensing disabled in both conditions, does executing `MOVE_X`/`MOVE_Y` alter measured digital-population dynamics?

## Causal isolation

- Conditions: `movement-execution-off` vs `movement-execution-on`.
- Matched seeds: 30.
- Ticks per run: 2000.
- Total runs: 60.
- Resource geography: identical `center_patch` configuration.
- Hereditary movement-opcode availability: matched in both conditions.
- Resource sensing: disabled in both conditions; observed total sensing operations = 0.
- Observed movement operations: control = 0; treatment = 257.
- Non-zero movement operations: control = 0; treatment = 6.
- Zero-step movement operations: control = 0; treatment = 251.
- Total realized movement distance: control = 0.0; treatment = 6.0.
- Total movement energy cost: control = 0.0; treatment = 0.6.
- Maximum absolute energy-balance error: 3.9e-09.
- Maximum absolute local-resource-balance error: 6.7e-09.
- Reproducibility: all designated repeated control runs were identical.

## Paired results

| Metric | Mean difference (on - off) | Approx. 95% paired interval | Interval contains 0? |
| --- | ---: | ---: | :---: |
| Final active population | 0.0 | [0.0, 0.0] | yes |
| Births | 0.233333 | [-0.224, 0.690667] | yes |
| Deaths | 0.233333 | [-0.224, 0.690667] | yes |
| Historical genotypes | 0.166667 | [-0.16, 0.493333] | yes |
| Blocked divisions | 0.0 | [0.0, 0.0] | yes |
| Mean local neighbors | 0.0117647 | [-0.0112941, 0.0348235] | yes |
| Mean nearest-neighbor distance | 0.0265738 | [-0.0255109, 0.0786585] | yes |
| Movement operations | 8.56667 | [3.36851, 13.7648] | no |
| Non-zero movement operations | 0.2 | [0.0544149, 0.345585] | no |
| Realized movement distance | 0.2 | [0.0544149, 0.345585] | no |

## Interpretation

The manipulation check succeeded: enabling movement execution caused `MOVE_X`/`MOVE_Y` instructions to execute, while the control condition had no movement execution. However, only 6 of 257 treatment movement operations produced non-zero displacement; 251 were zero-step operations. This means that movement semantics were active, but realized locomotion remained sparse under the current hereditary representation and mutation process.

For the selected population and spatial outcomes listed above, the approximate paired intervals contain zero. The campaign therefore does not establish a robust directional effect of movement execution on population size, turnover, genotype history, blocked divisions, or the selected spatial metrics in this model and regime.

The strongest supported conclusion is narrower: the movement opcodes executed under strict causal isolation, produced a small number of real displacements, conserved energy/resources within tolerance, and did not generate a clear population-level directional effect in this 30-seed campaign.

## Development implication

This campaign exposes an important representation bottleneck for the next Phase Three experiment: most evolved movement instructions inherit an effective step of zero, so movement is usually executed without locomotion. Before testing resource-seeking or navigation, Melakat should introduce and separately validate a heritable way for programs to generate non-zero movement commands at meaningful frequency, while preserving the existing control-flow and causal-isolation discipline.

This is a development inference from the measured mechanism counts, not evidence of adaptation or a biological analogue.

## Claim boundary

This evidence supports statements about execution of the existing `MOVE_X`/`MOVE_Y` semantics and their measured consequences inside the current Melakat Phase Three center-patch model. It does **not** establish navigation, resource-seeking behavior, adaptation, biological fitness, intelligence, cooperation, competition, niche formation, or open-ended evolution.

The approximate intervals are descriptive paired intervals for this deterministic computational campaign. They are not claims of inference to biological populations.

## Evidence artifacts

- `experiments/phase-three/movement-only.json`
- `results/phase-three/movement-only/full/campaign.json`
- `results/phase-three/movement-only/full/validation.json`
- `results/phase-three/movement-only/full/campaign-verification.json`
- `results/phase-three/movement-only/full/paired-analysis.json`
- `results/phase-three/movement-only/full/SHA256SUMS.txt`
