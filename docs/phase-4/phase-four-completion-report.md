# Phase Four Completion Report — Local Resource Sensing with Locomotion

[فارسی](phase-four-completion-report.fa.md)

## Status

**Phase Four evidence gate: COMPLETE.**

The registered full campaign has been executed, validated, paired-analyzed, checksum-verified, and archived. Phase Four asked whether executing local scalar resource sensing alters evolved movement execution and spatial/resource outcomes while locomotion is available and all hereditary/environmental mechanisms are matched.

The answer is mixed and scientifically informative:

- the sensing manipulation was successfully exposed;
- realized locomotion was present in both conditions;
- no registered movement-execution endpoint had an approximate paired 95% interval excluding zero;
- three registered spatial/resource endpoints did exclude zero;
- two secondary population endpoints also excluded zero;
- the pattern is therefore consistent with a sensing-caused change in ecological/spatial state, but **not** with a resolved effect on locomotor execution itself;
- the scalar sensor provides no direction, so this campaign does not test or establish navigation or resource seeking.

## Registered design

Full specification:

`experiments/phase-four/resource-sensing-with-movement.json`

Campaign:

- 30 matched seeds;
- 2 conditions;
- 2000 ticks per run;
- 60 primary runs plus the registered deterministic replay.

Conditions:

- control: `sensing-execution-off-movement-on`;
- treatment: `sensing-execution-on-movement-on`.

Matched in both conditions:

- hereditary `SENSE_RESOURCE` availability: ON;
- hereditary `MOVE_X` / `MOVE_Y` availability: ON;
- movement execution: ON;
- `mutation.movement_step_rate = 0.5`;
- atomic movement payment: ON;
- `center_patch` resource distribution;
- resource budget, topology, reproduction, mutation, memory and execution rules.

Only the execution flag `world.resource_sensing_enabled` differs.

`SENSE_RESOURCE` reports only the scalar resource amount at the organism's current location. It exposes no gradient, bearing, target coordinate, or directional cue.

## Integrity and reproducibility

The full campaign passed all structural gates:

- completed runs: `60/60`;
- validation failures: `0`;
- deterministic replay: `PASS`;
- engine: `phase-three-vm-0.3`;
- measurement: `phase-three-measurement-0.3`;
- atomic movement payment: enabled in all runs;
- underpaid realized-movement runs: `0`;
- maximum absolute energy-balance error: `4.8e-09`;
- maximum absolute local-resource-balance error: `6.3e-09`;
- accepted tolerance: `1e-07` for both ledgers;
- final archive checksum verification: `PASS`.

## Exposure diagnostics

The treatment executed `SENSE_RESOURCE` substantially, but exposure remained heterogeneous across seeds:

| Diagnostic | Control | Treatment |
| --- | ---: | ---: |
| Total sensing operations | 0 | 508 |
| Sensing-exposed runs | 0/30 | 15/30 |
| Any-MOVE-exposed runs | 21/30 | 18/30 |
| Non-zero-movement-exposed runs | 17/30 | 15/30 |
| Joint sensing + any MOVE | — | 8/30 |
| Joint sensing + non-zero movement | — | 7/30 |

The full campaign improved joint exposure over the eight-seed preflight, but direct co-exposure of sensing and realized locomotion is still sparse. This limits mechanistic attribution and must accompany all interpretation.

## Movement execution outcomes

No pre-registered movement endpoint resolved a paired treatment effect.

| Endpoint | Control mean | Treatment mean | Mean delta (T-C) | Approx. 95% interval | Resolved? |
| --- | ---: | ---: | ---: | ---: | --- |
| `movement_operations` | 5.6000 | 5.1667 | -0.4333 | [-1.2234, 0.3567] | No |
| `movement_nonzero_operations` | 4.6000 | 4.1333 | -0.4667 | [-1.2514, 0.3181] | No |
| `movement_distance` | 4.6000 | 4.1333 | -0.4667 | [-1.2514, 0.3181] | No |
| `movement_energy_cost` | 0.4600 | 0.4164 | -0.0436 | [-0.1221, 0.0348] | No |
| `movement_zero_step_operations` | 1.0000 | 1.0333 | +0.0333 | [-0.1148, 0.1814] | No |

Aggregate totals are descriptive only:

- control movement operations: `168`;
- treatment movement operations: `155`;
- control non-zero movement operations/distance: `138 / 138`;
- treatment non-zero movement operations/distance: `124 / 124`;
- control movement-energy cost: `13.8`;
- treatment movement-energy cost: `12.490909`.

These totals must not be interpreted as evidence that sensing reduces movement because the registered paired intervals include zero.

## Spatial/resource outcomes

Three registered spatial/resource endpoints had approximate paired intervals excluding zero:

| Endpoint | Control mean | Treatment mean | Mean delta (T-C) | Approx. 95% interval |
| --- | ---: | ---: | ---: | ---: |
| `mean_local_neighbors` | 2.0854 | 1.5018 | -0.5836 | [-1.1521, -0.0150] |
| `mean_nearest_neighbor_distance` | 9.3449 | 10.0239 | +0.6790 | [0.0541, 1.3038] |
| `local_resource_total` | 32871.7912 | 33084.1853 | +212.3941 | [4.8831, 419.9051] |

Other registered spatial/resource endpoints remained unresolved:

- `occupied_spatial_bins`;
- `spatial_occupancy_fraction`;
- `resource_heterogeneity_cv`;
- `local_resource_maximum`;
- `local_resource_minimum`.

The resolved pattern means that enabling local sensing causally changed recorded spatial/resource state under this registered model. It does **not** establish that organisms moved toward resources. In fact, the registered movement endpoints themselves remained unresolved.

## Secondary population outcomes

Two secondary endpoints also excluded zero:

- `active_population`: control mean `18.1333`, treatment mean `16.4333`, paired delta `-1.7000`, interval `[-3.3389, -0.0611]`;
- `blocked_divisions`: control mean `16.7000`, treatment mean `14.8000`, paired delta `-1.9000`, interval `[-3.6413, -0.1587]`.

Births, deaths, historical genotype count, active genotype count, active lineage count, and maximum generation remained unresolved under their approximate paired intervals.

The population result is important for interpretation: fewer active organisms can itself produce fewer local neighbors, greater nearest-neighbor distance, and more environmental resource left unconsumed. Therefore the spatial/resource signal should not be narrated as direct locomotor guidance. A plausible causal chain is sensing execution -> altered program/ecological trajectory -> lower active population/density -> altered spatial/resource state. This campaign was not designed to identify a unique mediation pathway.

## Statistical convention

The analysis retains the Phase Three convention:

`paired mean treatment-minus-control ± 1.96 × sample_SD(delta) / sqrt(n)`

with `n = 30` matched seeds.

These are approximate paired normal intervals, not a claim of exact finite-sample coverage and not a multiple-comparison-adjusted familywise inference procedure. The endpoints and interpretation rules were registered before the full campaign was interpreted.

## Scientific conclusion

Phase Four establishes all of the following within the implemented Melakat model:

1. local scalar resource sensing can be causally isolated while hereditary sensing/movement availability and movement execution remain matched;
2. sensing was executed in treatment and absent in control;
3. both conditions contained realized non-zero locomotion under atomic payment;
4. sensing did **not** resolve a difference in the registered movement-execution endpoints at this scale;
5. sensing **did** resolve differences in selected spatial/resource state, accompanied by a lower secondary active-population endpoint;
6. the result is consistent with **resource-conditioned ecological/spatial dynamics** and, under the pre-registered wording, with resource-conditioned behavior in the broad sense that sensing changed downstream model state;
7. the evidence does not demonstrate directional navigation, resource seeking, adaptation, fitness advantage, intelligence, cooperation, predation, or open-ended evolution.

The most important boundary is that the sensor has no direction. Therefore even a reproducible treatment effect cannot be called navigation.

## Evidence archive

Canonical archive:

`results/phase-four/resource-sensing-with-movement/full/`

It contains the generated campaign outputs plus:

- `campaign-verification.json`;
- `paired-analysis.json`;
- `merge-readiness.json`;
- `README.md`;
- `SHA256SUMS.txt`.

The pre-registration, smoke evidence, and full-duration preflight remain preserved separately and are not overwritten by the full campaign.

## Phase Four closure

Phase Four is complete as a causal evidence checkpoint. The next phase should not reinterpret this result as navigation. A later navigation-specific experiment would require directional environmental information and a dedicated navigation metric, while broader evolvability work should be introduced as a separately versioned intervention rather than silently altering this accepted evidence archive.
