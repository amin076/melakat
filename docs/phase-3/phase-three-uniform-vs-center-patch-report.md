# Phase Three first scientific campaign: uniform vs center patch

## Status

**Accepted first Phase Three scientific campaign.**

This report records the first full matched-seed experiment under the Phase Three environmental-heterogeneity contract. It compares the frozen uniform local-resource control with a deterministic center-patch allocation while holding the total initial resource and total resource input per tick constant.

The experiment does **not** add resource sensing, movement, cooperation, predation, explicit fitness, or host-authored adaptive behavior. The only causal intervention is the spatial allocation rule for the same total resource input.

## Experiment

Specification: `experiments/phase-three/uniform-vs-center-patch.json`

- engine: `phase-three-vm-0.1`
- world contract: `phase-three-environment-0.1`
- measurement contract: `phase-three-measurement-0.1`
- seeds: 1–30, matched between conditions
- ticks per run: 2000
- conditions: `uniform-control`, `center-patch`
- total runs: 60
- initial local resource: 1000 in both conditions
- resource input per tick: 20 in both conditions
- organism actions: disabled
- movement: zero by construction in this campaign

The center-patch condition uses patch fraction `0.30` and contrast `4.0`. Allocation weights are normalized, so the intervention changes *where* resource enters the grid, not how much enters the world.

## Acceptance gate

- expected runs: 60
- completed runs: 60
- validation failures: 0
- deterministic repeat: PASS
- extinction: 0/30 in both conditions
- maximum absolute energy-balance error: `4.1e-09` under tolerance `1e-07`
- maximum absolute local-resource-balance error: `5.9e-09` under tolerance `1e-07`
- minimum local resource observed in final compact records: `0.0`

Reproducibility target:

- condition: `uniform-control`
- seed: 1
- reference checksum: `aa7167c5d19e230a819f434c269bcbaccdff84730856e600eec39e6fac312bbf`
- repeat checksum: `aa7167c5d19e230a819f434c269bcbaccdff84730856e600eec39e6fac312bbf`

## Matched-seed results

The table uses the 30 seed-wise paired differences. The interval is a descriptive 95% paired t interval for the mean difference across this seed set; this campaign did not preregister a confirmatory endpoint hierarchy, so these intervals should not be treated as a publication-level multiplicity-controlled significance analysis.

| Metric | Uniform mean | Center-patch mean | Paired mean Δ (patch − uniform) | 95% paired CI | Direction across 30 seeds |
|---|---:|---:|---:|---:|---|
| Final active population | 9.767 | 18.000 | +8.233 | [4.613, 11.853] | patch higher 25, same 1, lower 4 |
| Births | 143.567 | 107.200 | -36.367 | [-54.914, -17.819] | patch higher 6, same 0, lower 24 |
| Deaths | 145.800 | 101.200 | -44.600 | [-60.882, -28.318] | patch higher 4, same 0, lower 26 |
| Historical genotypes | 12.467 | 9.000 | -3.467 | [-5.635, -1.299] | patch higher 8, same 1, lower 21 |
| Max generation | 12.733 | 13.500 | +0.767 | [-2.306, 3.839] | patch higher 13, same 2, lower 15 |
| Blocked divisions | 8.333 | 16.633 | +8.300 | [5.071, 11.529] | patch higher 26, same 1, lower 3 |
| Waiting for energy | 6.567 | 11.500 | +4.933 | [2.038, 7.829] | patch higher 23, same 1, lower 6 |
| Memory used | 156.267 | 288.000 | +131.733 | [73.815, 189.652] | patch higher 25, same 1, lower 4 |
| Mean local neighbors | 0.574 | 1.974 | +1.400 | [0.337, 2.462] | patch higher 20, same 3, lower 7 |
| Mean nearest-neighbor distance | 16.814 | 9.580 | -7.234 | [-11.075, -3.393] | patch higher 10, same 0, lower 20 |
| Final local-resource total | 33927.296 | 32653.326 | -1273.970 | [-2232.171, -315.769] | patch higher 11, same 0, lower 19 |
| Evolving resource heterogeneity CV | 0.419 | 0.848 | +0.429 | [0.404, 0.454] | patch higher 30, same 0, lower 0 |

The imposed environmental heterogeneity is separately measured by `resource_allocation_cv`: `0.000000` for every uniform run and `0.668043` for every center-patch run. `resource_heterogeneity_cv` is different: it describes the evolving field after local capture, death release, and renewal, so it can be greater than zero even under uniform input.

## Mechanistic observations supported by this campaign

1. **The resource-allocation rule alone changed the population regime.** Final active population averaged `9.77` under uniform allocation and `18.00` under the center patch. The patch condition ended with more active organisms in 25 of 30 matched seeds.

2. **The higher final population did not come from more births.** Births were lower under the patch (`107.2` vs `143.57`), while deaths were lower by an even larger amount (`101.2` vs `145.8`). For this model and campaign, the patch therefore corresponds to lower population turnover and greater final persistence, not simply faster reproduction.

3. **Spatial concentration increased without movement.** Mean local-neighbor count increased and mean nearest-neighbor distance decreased in the patch condition even though movement operations and movement distance were zero. Under the current rules, this can arise from local birth plus differential survival/resource access; it is not evidence that organisms navigated toward the patch.

4. **Resource concentration introduced local constraints.** Blocked divisions and waiting-for-energy counts were higher in the patch condition despite the larger surviving population. This is consistent with a world in which resource abundance is spatially uneven and local crowding/access matters.

5. **The campaign does not show deeper evolution by itself.** Historical genotype count was lower in the patch condition (`9.0` vs `12.47`), and max-generation difference was small and inconsistent across seeds (paired mean `+0.77`, interval crossing zero). These results do not support a claim that the patch caused greater evolutionary complexity, adaptation, or innovation.

## Scientific interpretation boundary

This experiment supports the causal statement that, **within the implemented Melakat model and while holding total resource input fixed, changing only the spatial distribution of resource materially changes population persistence, turnover, spatial concentration, and local constraints.**

It does **not** establish:

- adaptation to the patch;
- intentional resource seeking;
- natural biological fitness;
- cooperation or competition strategies;
- increased evolutionary complexity;
- open-ended evolution.

Movement and sensing were disabled, so any stronger claim about navigation or evolved resource seeking would be unsupported.

## Provenance

- workflow: `Phase Three uniform vs center patch research`
- workflow run: `34062567737`
- source branch: `research/phase-three-uniform-vs-center-patch`
- source commit: `9314df691e2c01ee2b0fb60248ab7052ecec9c84`
- engine code parent on `main`: `ad0a15efd90445188ee0ef98c3bed526165fb2ab`
- Python: `3.12.14`
- source specification SHA-256: `912b374855db97edf1d265bb0a25da0944f8e13611f247a9fe0f50862459d5a4`
- GitHub artifact id: `9997969944`
- GitHub artifact digest: `sha256:402dabae1b7f39d600ce26e3027ff2769ec8b37e94b707d38a8a13ba42121e70`

The repository evidence record is archived under `results/phase-three/uniform-vs-center-patch/evidence-gate/`. The original full workflow artifact is identified by the artifact id and digest above.

## Next controlled question

The next scientific increment should not add many mechanisms at once. The clean follow-up is to keep the same matched environments and ask whether adding **minimal local resource sensing**, without yet adding host-authored goals or social behavior, changes the difference between uniform and patchy worlds. That should be treated as a new intervention and versioned separately.
