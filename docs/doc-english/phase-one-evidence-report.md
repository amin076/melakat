# Phase One Evidence Report

[فارسی](../doc-farsi/phase-one-evidence-report.md) | [Phase One roadmap](phase-one-roadmap.md) | [Documentation index](../README.md)

## Decision

The Phase One scientific evidence gate is accepted for the defined homogeneous baseline.

This decision means that the current Phase Zero/Phase One world has a reproducible, archived baseline suitable for controlled comparison with Phase Two. It does not mean that the model has reproduced biological life, that all parameter interactions are understood, or that future spatial results may be interpreted without matching controls.

## Provenance

The archived campaign used:

- engine version: <code>phase-zero-vm-0.2</code>;
- measurement version: <code>phase-one-measurement-0.1</code>;
- campaign format: <code>melakat-phase-one-evidence-0.1</code>;
- base configuration hash: <code>b90c2df4f218b285</code>;
- seeds: <code>1</code> through <code>30</code>;
- run length: <code>2000 ticks</code> per condition;
- six control conditions;
- nine one-factor sensitivity parameters with three values each;
- 27 sensitivity cases;
- 990 archived runs in total;
- one additional repeated baseline run for an exact same-seed reproducibility check.

The evidence archive is stored under:

<code>results/phase-one/evidence-gate/</code>

The archive contains the base configuration, campaign JSON, compact per-run CSV, validation result, and SHA-256 file checksums.

Each compact run record also stores a SHA-256 checksum of the complete enriched run summary before compaction. The checksum therefore covers the detailed history, genealogy, genotype catalog, and analysis that were produced by that run, even though those large structures are not repeated in the compact repository archive.

## Gate validation

The primary automated gate reported:

| Check | Result |
| --- | ---: |
| Campaign passed | yes |
| Seeds | 30 |
| Control conditions | 6 |
| Sensitivity parameters | 9 |
| Sensitivity cases | 27 |
| Total archived runs | 990 |
| Energy-invariant failures | 0 |
| Memory-invariant failures | 0 |
| Seed-coverage failures | 0 |
| Run-count failures | 0 |
| Configuration-hash failures | 0 |
| Result-checksum failures | 0 |
| Tick-count failures | 0 |
| Same-seed reproducibility failure | 0 |
| Maximum absolute energy-balance error | <code>2.5e-08</code> |
| Allowed energy tolerance | <code>1e-07</code> |

The repeated baseline run for seed <code>1</code> produced the same full-result checksum both times:

<code>77ce431d1686a9cb43dd503952991a778d28213bfbd5adbe56d8b4820a3a4b02</code>

A supplemental archive audit also checks population accounting, non-negative final resources, engine/measurement-version consistency, and repeated appearances of the same effective configuration and seed. Across 990 records and 690 unique <code>config_hash + seed</code> pairs, no mismatch was found.

## Baseline

The baseline uses:

- initial population: <code>12</code>;
- memory capacity: <code>500</code>;
- working memory per organism: <code>8</code>;
- default genome length: <code>8</code>;
- energy input: <code>10</code> units per tick;
- initial world energy: <code>1000</code>;
- instruction budget: <code>8</code> per tick;
- instruction cost: <code>0.05</code>;
- maintenance cost: <code>0.2</code>;
- reproduction cost: <code>12</code>;
- offspring energy: <code>8</code>;
- substitution rate: <code>0.01</code>.

Each default organism occupies <code>16</code> structural memory units: eight working-memory units plus an eight-instruction genome. A 500-unit world therefore supports at most 31 such active organisms, leaving four units unused.

Across 30 baseline seeds:

| Metric | Mean |
| --- | ---: |
| Final population | 31.00 |
| Births | 20.37 |
| Deaths | 1.37 |
| Maximum population | 31.00 |
| Active genotypes | 1.23 |
| Historical genotypes | 2.60 |
| Lineages | 1.73 |
| Mutation events | 1.60 |
| Faults | 1.17 |
| Waiting for memory | 30.90 |
| Waiting for energy | 0.00 |

No baseline run went extinct. The final population was 31 in every baseline seed, so final population alone hides substantial differences in mutation, faults, lineage history, births, and deaths.

## Control results

### Mutation-zero control

With substitution rate <code>0</code>, all 30 runs ended with:

- final population <code>31</code>;
- one active genotype;
- one historical genotype;
- one lineage;
- zero mutation events;
- zero VM faults;
- zero deaths.

This reproduces the earlier paired control at larger multi-seed scale: the observed mutation-derived genotype variation and mutation-associated faults disappear when substitution mutation is disabled.

### Abundant-energy control

With energy input increased to <code>1000</code> units per tick, mean final population remained <code>31</code>, and mean waiting-for-memory remained about <code>30.73</code>. Increasing energy therefore does not remove the dominant structural-memory bottleneck in this baseline.

### Abundant-memory control

With memory capacity increased to <code>1,000,000</code>, the system changed regime:

- mean final population: <code>29.73</code>;
- mean maximum population: <code>66.80</code>;
- mean births: <code>435.60</code>;
- mean deaths: <code>417.87</code>;
- mean historical genotypes: <code>30.20</code>;
- mean mutation events: <code>34.47</code>;
- mean faults: <code>25.43</code>;
- mean waiting for memory: <code>0</code>;
- mean waiting for energy: <code>25.40</code>.

Removing the memory bottleneck did not simply produce a much larger final population. Instead it enabled much greater birth/death turnover and genotype history, after which energy became the observable reproduction bottleneck.

### Zero-maintenance control

With maintenance cost <code>0</code>, final population remained <code>31</code> in all 30 runs and memory remained the dominant blocked-division state. Within this baseline regime, removing maintenance cost does not overcome the structural-memory ceiling.

### Zero-reproduction-cost control

The formal Phase Zero control <code>reproduction.cost = 0</code> was restored and run across all 30 seeds. Mean final population remained <code>31</code>, mean waiting for memory was about <code>30.97</code>, and no run went extinct. This control closes the previously missing campaign requirement; it does not imply that reproduction cost is universally unimportant outside the tested memory-limited regime.

## Sensitivity results

The sensitivity campaign varies one factor at a time. The following findings are observations within the tested ranges, not universal laws.

### Memory capacity

Memory capacity produced one of the clearest regime changes.

| Capacity | Mean final population | Mean births | Mean deaths | Mean historical genotypes | Mean memory waits | Mean energy waits |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 250 | 15.00 | 3.23 | 0.23 | 1.30 | 14.93 | 0.00 |
| 500 | 31.00 | 20.37 | 1.37 | 2.60 | 30.90 | 0.00 |
| 1000 | 30.67 | 435.70 | 417.03 | 30.37 | 0.00 | 25.37 |

At capacity <code>250</code>, the 16-unit structural allocation caps the active population at 15. At <code>500</code>, it caps the population at 31. At <code>1000</code>, memory waiting disappears and energy waiting appears, with much greater turnover and genotype history.

This is evidence that resource bottlenecks must be identified explicitly. More available memory does not imply a larger final population at a fixed observation time.

### Energy input

| Energy input/tick | Mean final population | Mean births | Mean deaths | Mean historical genotypes | Mean memory waits | Mean energy waits |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 15.87 | 171.87 | 168.00 | 12.87 | 0.00 | 13.87 |
| 10 | 31.00 | 20.37 | 1.37 | 2.60 | 30.90 | 0.00 |
| 20 | 31.00 | 20.17 | 1.17 | 2.57 | 30.73 | 0.00 |

At input <code>5</code>, the system becomes energy-limited, with lower final population but much greater turnover than the baseline. Raising input from <code>10</code> to <code>20</code> does not increase final population because structural memory remains saturated.

### Maintenance cost

At maintenance costs <code>0.1</code> and <code>0.2</code>, final population remained 31 and memory waiting dominated. At <code>0.4</code>, the system changed to an energy-limited high-turnover regime:

- mean final population: <code>18.43</code>;
- mean births: <code>286.60</code>;
- mean deaths: <code>280.17</code>;
- mean historical genotypes: <code>20.90</code>;
- mean mutation events: <code>21.83</code>;
- mean faults: <code>16.00</code>;
- memory waits: <code>0</code>;
- mean energy waits: <code>15.47</code>.

### Mutation substitution rate

| Substitution rate | Mean final population | Mean deaths | Mean historical genotypes | Mean mutation events | Mean faults |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 31.00 | 0.00 | 1.00 | 0.00 | 0.00 |
| 0.01 | 31.00 | 1.37 | 2.60 | 1.60 | 1.17 |
| 0.05 | 31.00 | 8.90 | 10.27 | 9.83 | 7.40 |

Increasing substitution rate increased observed genotype history, mutation events, faults, deaths, and replacement births, while the final population remained fixed at the memory ceiling. This is a direct demonstration of why population size alone is not a sufficient measure of evolutionary dynamics.

### Other tested parameters

Within the tested baseline ranges, changes in:

- instruction cost <code>0.02 / 0.05 / 0.1</code>;
- instruction budget <code>1 / 8 / 16</code>;
- reproduction cost <code>6 / 12 / 24</code>;
- offspring energy <code>4 / 8 / 16</code>;
- initial world energy <code>500 / 1000 / 2000</code>

produced comparatively small differences in the 2000-tick final summaries while the 500-unit memory ceiling remained active. This should be interpreted as masking by the dominant bottleneck within these tested conditions, not as proof that the parameters have no causal effect.

## Extinction result

None of the 990 campaign runs went extinct.

This is a valid observation for the tested parameter ranges and seeds. It must not be generalized into a claim that extinction is impossible in Melakat. More severe energy, cost, mutation, or future environmental conditions may produce extinction and must be retained as valid outcomes.

## Scientific interpretation

The campaign supports five bounded conclusions about the current model:

1. The homogeneous baseline is reproducible under fixed seeds and preserves its energy and memory invariants.
2. The baseline with 500 memory units is primarily memory-limited near its long-run population ceiling.
3. Removing that memory bottleneck can expose energy as the next limiting resource and substantially change birth/death and genotype turnover.
4. Mutation has reproducible observable effects that cannot be inferred from final population alone.
5. Resource constraints interact through bottleneck regimes, so a parameter's apparent effect depends on which resource is currently limiting.

These statements describe the implemented digital model. They are not claims that the same quantitative relationships hold in biological systems.

## Limitations

The evidence campaign has deliberate limits:

- it uses seeds <code>1–30</code>, not every possible seed;
- it uses one-factor-at-a-time sensitivity rather than a factorial interaction design;
- each condition is observed for <code>2000 ticks</code>;
- the archived repository record is compact and stores a checksum of each complete enriched result rather than duplicating all detailed per-run histories;
- the tested parameter ranges do not define universal safe or biological ranges;
- no spatial environment, local resource field, movement, learning, explicit fitness objective, cooperation, attack, or parasite is part of this campaign.

Future experiments may expose new regimes or failure modes. Such results would revise the scientific interpretation without invalidating this archived baseline as long as the versioned model and configuration remain identifiable.

## Phase One gate decision

Phase One is now complete in two distinct senses:

1. the implementation gate is complete: measurement, export, inspection, comparison, and reproducible execution exist;
2. the scientific evidence gate is complete for the defined homogeneous baseline: the required controls and sensitivity campaign have been executed, validated, and archived.

Phase Two may therefore begin with <code>P2.1</code>, provided the homogeneous Phase One model remains available unchanged as the permanent comparison control.
