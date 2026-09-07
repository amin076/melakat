# Phase Three Resource-Sensing-Only Evidence Note

## Experimental question

With the Phase Three center-patch resource geography fixed, total resource budget fixed, mutation rate fixed, hereditary availability of `SENSE_RESOURCE` matched, and evolved movement disabled in both conditions, does executing `SENSE_RESOURCE` alter measured digital-population dynamics?

## Causal isolation

- Conditions: `sensing-execution-off` vs `sensing-execution-on`.
- Matched seeds: 30.
- Ticks per run: 2000.
- Total runs: 60.
- Resource geography: identical `center_patch` configuration.
- Hereditary opcode availability: matched in both conditions.
- Movement: disabled in both conditions; observed maximum movement operations = 0 and maximum movement distance = 0.0.
- Observed sensing operations: control = 0; treatment = 233.
- Maximum absolute energy-balance error: 4e-09.
- Maximum absolute local-resource-balance error: 6.5e-09.
- Reproducibility: all three execution batches repeated their designated control seed identically.

## Paired results

| Metric | Mean difference (on - off) | Approx. 95% paired interval | Interval contains 0? | Seed directions (+ / 0 / -) |
| --- | ---: | ---: | :---: | ---: |
| Final active population | 0.233333 | [-1.12417, 1.59084] | yes | 5 / 22 / 3 |
| Births | -1.3 | [-5.97377, 3.37377] | yes | 4 / 23 / 3 |
| Deaths | -1.53333 | [-5.38327, 2.3166] | yes | 4 / 22 / 4 |
| Historical genotypes | -0.5 | [-1.14854, 0.148541] | yes | 1 / 24 / 5 |
| Blocked divisions | 0.3 | [-0.997639, 1.59764] | yes | 5 / 22 / 3 |
| Mean local neighbors | 0.102926 | [-0.321491, 0.527342] | yes | 5 / 21 / 4 |
| Mean nearest-neighbor distance | -0.0300503 | [-0.729422, 0.669322] | yes | 4 / 21 / 5 |
| Resource-sense operations | 7.76667 | [1.87004, 13.6633] | no | 14 / 16 / 0 |

## Interpretation

For `active_population`, `births`, `deaths`, `historical_genotypes`, `blocked_divisions`, `mean_local_neighbors`, `mean_nearest_neighbor_distance`, the approximate paired interval includes zero. The campaign therefore does not provide a clean directional effect estimate for those outcomes; their observed mean differences should be treated as small descriptive shifts in this finite computational campaign, not as established improvements or impairments.

No selected non-sensing population outcome has an approximate paired interval that excludes zero. The strongest supported conclusion is therefore that the sensing opcode executed as intended under strict causal isolation, while this 30-seed campaign did not establish a robust directional change in the selected population-level outcomes.

`resource_sense_operations` is a manipulation check rather than an ecological outcome: it should differ because the treatment explicitly enables execution of `SENSE_RESOURCE`.

## Claim boundary

This evidence supports statements about execution of the existing `SENSE_RESOURCE` opcode and its measured consequences inside the current Melakat Phase Three center-patch model. It does **not** establish resource-seeking movement, navigation, adaptation, biological fitness, intelligence, cooperation, open-ended evolution, or a general advantage of sensing.

The approximate intervals are descriptive paired intervals for this deterministic computational campaign. They are not claims of inference to biological populations.

## Evidence artifacts

- `experiments/phase-three/resource-sensing-only.json`
- `results/phase-three/resource-sensing-only/full/campaign.json`
- `results/phase-three/resource-sensing-only/full/validation.json`
- `results/phase-three/resource-sensing-only/full/campaign-verification.json`
- `results/phase-three/resource-sensing-only/full/paired-analysis.json`
- `results/phase-three/resource-sensing-only/full/SHA256SUMS.txt`
