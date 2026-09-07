# Phase Four — Local Resource Sensing with Locomotion Available

## Status

**Pre-registered mechanism/exposure gate.** This document defines the causal question, experimental contrast, smoke criteria, and scientific interpretation boundaries before the full campaign is interpreted.

## Scientific question

> Does local resource sensing alter evolved movement execution and spatial/resource outcomes when locomotion is available?

This is intentionally **not** a navigation-toward-resource claim.

`SENSE_RESOURCE` reports a scalar measurement of resource at the organism's current location. It does not provide a resource gradient, bearing, target coordinate, or movement direction. `MOVE_X` and `MOVE_Y` obtain their requested step from their own immediate operand. Sensing can nevertheless alter program control flow because the sensed value is written to a register and base VM instructions such as `JUMP_IF_ZERO` can change which later instructions are reached.

Accordingly, an observed treatment effect may support the narrower phrase **resource-conditioned behavior**. It does not by itself demonstrate directional navigation, resource seeking, adaptation, or optimality.

## Causal contrast

The two conditions share all hereditary and environmental mechanisms. Only execution of `SENSE_RESOURCE` differs.

| Property | Control | Treatment |
| --- | --- | --- |
| Hereditary `SENSE_RESOURCE` availability | ON | ON |
| Hereditary `MOVE_X` / `MOVE_Y` availability | ON | ON |
| Movement execution | ON | ON |
| Resource-sensing execution | **OFF** | **ON** |
| `mutation.movement_step_rate` | 0.5 | 0.5 |
| Atomic movement payment | ON | ON |
| Resource distribution | center patch | center patch |
| Patch fraction / contrast | 0.30 / 4.0 | 0.30 / 4.0 |
| Boundary | reflective | reflective |

Condition names:

- `sensing-execution-off-movement-on`
- `sensing-execution-on-movement-on`

The experiment plan must verify that the only effective configuration difference is `world.resource_sensing_enabled`.

## Specifications

- Smoke: `experiments/phase-four/resource-sensing-with-movement-smoke.json`
  - 8 matched seeds
  - 800 ticks per run
  - 16 primary runs plus the experiment runner's deterministic reproducibility replay
- Full: `experiments/phase-four/resource-sensing-with-movement.json`
  - 30 matched seeds
  - 2000 ticks per run
  - 60 primary runs plus reproducibility replay

The backend remains `phase-three-vm`. Phase Four changes the scientific intervention, not the already-evidenced VM/atomic-movement semantics.

## Smoke gates

The smoke campaign is a mechanism and exposure test. It passes only if all of the following hold:

1. **Causal isolation:** effective configs differ only in `world.resource_sensing_enabled`.
2. **Matched hereditary alphabet:** sensing mutation availability and movement mutation availability are ON in both conditions.
3. **Sensing exposure:** control total `resource_sense_operations == 0`; treatment total `resource_sense_operations > 0`.
4. **Locomotion exposure:** both conditions record at least one non-zero committed movement operation.
5. **Atomic accounting:** every run has atomic movement payment enabled and realized movement distance is not underpaid relative to `world.movement_cost_per_unit = 0.1`.
6. **Conservation:** energy and local-resource balance errors remain within accepted numerical tolerances.
7. **Reproducibility:** the configured replay is identical.

Smoke success does **not** require a treatment-control difference in ecological or spatial outcomes.

## Full-campaign endpoints

The full campaign uses matched-seed paired contrasts. Primary mechanistic outcomes are:

- `resource_sense_operations`
- `movement_operations`
- `movement_nonzero_operations`
- `movement_zero_step_operations`
- `movement_distance`
- `movement_energy_cost`

Primary spatial/resource outcomes are:

- `mean_local_neighbors`
- `mean_nearest_neighbor_distance`
- `occupied_spatial_bins`
- `spatial_occupancy_fraction`
- `local_resource_total`
- `local_resource_minimum`
- `resource_heterogeneity_cv`
- `local_resource_maximum`

Ecological/population outcomes such as active population, births, deaths, genotype diversity, lineage counts, and generation depth remain secondary outcomes.

For each selected paired endpoint, report the paired mean difference and an uncertainty interval. Do not infer a positive effect merely from a non-zero point estimate.

## Interpretation rules

### If sensing executes but paired outcome intervals include zero

Conclude that the campaign demonstrated a functioning sensing-plus-movement mechanism but did not resolve an effect of sensing on the selected movement/spatial/resource outcome at this scale.

### If sensing changes movement or spatial/resource outcomes

The strongest allowed wording is that **local resource sensing altered evolved movement execution and/or spatial/resource outcomes**, consistent with resource-conditioned behavior.

Do not call the result directional navigation unless a later sensor/experiment supplies directional environmental information and a dedicated navigation metric establishes motion relative to that information.

### If sensing never executes in treatment

The scientific contrast is unexposed and cannot answer the causal question. Increase exposure through a pre-declared calibration step rather than interpreting outcome equality as a null sensing effect.

### If movement is absent in either condition

The gate does not test sensing in the presence of realized locomotion and must not be promoted to the full campaign until locomotion exposure is restored.

## Mechanistic control-flow proof

A regression micro-test uses the program sequence:

1. `SENSE_RESOURCE -> R0`
2. `JUMP_IF_ZERO` on `R0`
3. `MOVE_X +1`

With sensing disabled, `R0` remains zero and the MOVE is skipped. With sensing enabled and positive local resource, the branch falls through and the MOVE is reached. With sensed resource equal to zero, the MOVE is skipped.

This demonstrates the exact mechanism by which scalar sensing can condition whether movement executes while preserving the important boundary that sensing does not encode movement direction.
