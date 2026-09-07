# Phase Four — Sensing + Movement Full-Duration Exposure Preflight

## Status

**Structural/accounting preflight: PASS.**

This report records calibration evidence collected before the planned 30-seed paired campaign. It is not an inferential treatment-effect analysis.

## Why the preflight was added

The 8-seed × 800-tick smoke campaign established that sensing and locomotion both functioned, but exposure was concentrated: treatment executed `SENSE_RESOURCE` in only 2 of 8 runs, and only 1 of 8 treatment runs had both sensing exposure and non-zero committed movement.

Rather than interpreting that sparse smoke or immediately launching the 60-run full campaign, the same first eight matched seeds were run at the full campaign duration of 2000 ticks. The configuration is otherwise identical to the registered full specification.

## Full-duration exposure results

Across 8 matched seeds per condition:

| Diagnostic | Control | Treatment |
| --- | ---: | ---: |
| `resource_sense_operations` | 0 | 139 |
| runs with sensing exposure | 0 / 8 | 6 / 8 |
| runs with non-zero committed movement | 4 / 8 | 4 / 8 |
| runs with both sensing and non-zero movement | n/a | 2 / 8 |
| non-zero committed movement operations | 35 | 34 |
| committed movement distance | 35.0 | 34.0 |
| movement energy cost | 3.5 | 3.4 |
| uncommitted movement distance | 0.0 | 0.0 |

The longer duration materially increased sensing exposure relative to the 800-tick smoke (2/8 to 6/8 treatment runs) and increased joint sensing-plus-nonzero-movement exposure from 1/8 to 2/8 treatment runs. Joint exposure nevertheless remains sparse.

## Accounting and reproducibility

- campaign validation: PASS
- reproducibility replay: identical
- maximum absolute energy balance error: `4.8e-09`
- maximum absolute local-resource balance error: `6.3e-09`
- no realized movement was underpaid
- no uncommitted movement distance was recorded

## Scientific interpretation

This preflight demonstrates that the intended causal mechanism is exposed at full duration and that sensing exposure is substantially less sparse than in the short smoke. It does **not** demonstrate that sensing caused the 1-unit aggregate difference in movement distance, or any ecological/spatial difference. Those quantities are descriptive calibration outputs only.

Because the sensor provides only a scalar measurement of resource at the current location, even a later statistically resolved treatment effect would support the wording **resource-conditioned behavior**, not directional navigation or resource seeking.

## Promotion decision

No numerical promotion threshold was invented after seeing the smoke. The full-duration preflight is retained as descriptive exposure evidence. The registered 30-seed campaign may proceed, but its analysis must:

1. report sensing exposure and joint sensing/movement exposure alongside outcome contrasts;
2. use matched-seed paired uncertainty intervals rather than raw aggregate differences;
3. treat low joint exposure as a limitation on power and mechanism attribution;
4. avoid navigation/adaptation language unless a future directional sensor and dedicated navigation metric justify it.

Evidence source: `results/phase-four/resource-sensing-with-movement/preflight/`.
