# Phase Two Completion and Evidence Report

[فارسی](phase-two-completion-report.fa.md) | [User test guide](phase-two-user-test-guide.md) | [Roadmap](../doc-english/phase-two-roadmap.md)

## Status

**Phase Two is complete for the research scope defined in the Phase Two roadmap.**

Accepted versions:

- world contract: `phase-two-spatial-0.7`
- engine: `phase-two-vm-0.7`
- measurement contract: `phase-two-measurement-0.1`
- evidence format: `melakat-phase-two-evidence-0.1`
- spatial run artifact: `melakat-run-artifact-0.2`

The Phase One homogeneous world remains a permanent control. Disabling Phase Two causal spatial rules preserves the frozen Phase One scientific baseline rather than silently replacing it with a new model.

## Completed work packages

### P2.1 — Versioned world model

The world contract defines coordinate bounds, observation semantics, environment-update timing, tick order, resource accounting, artifact metadata, and the Phase One compatibility path.

### P2.2 — Space and topology

Phase Two provides a continuous two-dimensional rectangular world, local radial offspring placement, independent spatial randomness, spatial measurements, and explicit `reflective` and `toroidal` boundary models. Toroidal neighborhood distance uses the shortest wrapped path.

### P2.3 — Local resource field

A conservative uniform-renewal grid is available as the first local-resource mechanism. Initial energy and incoming energy are distributed over cells, organisms capture only from their current cell, remaining energy is returned locally on death, and diffusion and organism-produced resources remain deliberately absent.

### P2.4 — Observation and movement primitives

The Phase Two data-only mutation alphabet can include:

- `SENSE_RESOURCE`
- `MOVE_X`
- `MOVE_Y`

Movement is bounded, deterministic for a fixed state and seed, constrained by the selected boundary model, and charged through the energy ledger. These instructions do not prescribe a target behavior or a fitness objective.

### P2.5 — Controlled experiment matrix

The evidence campaign contains twelve matched conditions:

1. homogeneous control;
2. spatial-only;
3. local resource;
4. movement enabled;
5. resource abundant;
6. resource limited;
7. small world;
8. large world;
9. reflective boundary;
10. toroidal boundary;
11. zero movement cost;
12. high movement cost.

Each condition is run for the same 30 seeds and 2000 ticks per run.

### P2.6 — Desktop research interface

The desktop laboratory exposes schema-driven Phase Two parameters, organism/boundary/resource layers, selectable spatial time-series metrics, selected-organism local context, saved-result comparison, exact configuration export, and event inspection for birth/death, reproduction, movement and resource activity. Boundary contacts are observable in spatial metrics and in movement/birth event payloads.

### P2.7 — Reproducibility and scale measurements

The evidence tooling records deterministic repeat checks, execution time, ticks per second, Python allocation peak, event-log volume, snapshot size, summary size, artifact size, and serialization time before any future optimization or parallelism is introduced.

## Accepted evidence gate

The final accepted campaign was generated from source commit:

`ad5e21159baf0d6bd79a028799b9318ba144fed7`

GitHub Actions workflow run:

`33969619473`

Runtime used by the campaign:

- Python `3.12.14`
- GitHub Actions Linux runner

Campaign command:

~~~text
melakat-phase-two-evidence --runs 30 --ticks 2000 --seed-start 1 --output-dir results/phase-two/evidence-gate
~~~

Validation result:

- conditions: **12**
- seeds per condition: **30**
- expected runs: **360**
- completed runs: **360**
- validation failures: **0**
- energy tolerance: `1e-7`
- maximum absolute energy-balance error: `1.02e-08`
- local-resource tolerance: `1e-7`
- maximum absolute local-resource balance error: `4.2e-09`
- reproducibility check: **PASS**
- repeated checksum: `858e5ffa6b77d7f71067af1e9422a7873f3cff85e4b26735987c5ee5162a4dd3`

The accepted archive is stored under:

`results/phase-two/evidence-gate/`

It contains the campaign, compact run table, validation report, base configuration, performance report, provenance record, and SHA-256 manifest.

## Performance reference

For the recorded 2000-tick Phase Two performance probe on the CI runner:

- runtime: about `0.331 s`
- throughput: about `6044.5 ticks/s`
- peak traced Python allocation: `2,748,358 bytes`
- recorded events: `4,077`
- event-log JSON size: `993,985 bytes`
- final snapshot JSON size: `1,138 bytes`
- summary JSON size: `364,409 bytes`
- complete artifact JSON size: `369,035 bytes`
- serialization time: about `0.0281 s`
- deterministic repeat: **PASS**

These numbers describe this reference CI environment and configuration; they are not universal hardware-performance guarantees.

## Scientific observations from the Phase Two matrix

The evidence gate is primarily a validity and reproducibility gate, but it also produced several useful model observations.

The homogeneous control retained the familiar structural-memory ceiling near 31 active organisms. The spatial-only condition preserved the same population-level behavior while adding local placement and spatial measurements, which supports the intended isolation of space from the old homogeneous control.

Under the default local-resource configuration, many spatial-resource conditions reached extinction. This is not a failed invariant. It is a model outcome: energy is renewed across cells, organisms capture only from the cell they occupy, and there is no diffusion. Energy can therefore become inaccessible in unoccupied cells while organisms locally starve.

The resource-abundant condition avoided extinction across the tested seeds but produced much higher birth/death turnover. This shows that resource availability can move the model into a substantially different dynamical regime.

Movement and resource-sensing opcodes appeared only rarely in this blind-mutation campaign. Therefore Phase Two does **not** claim that adaptive navigation, cooperation, or resource-seeking behavior evolved. Those would require separately designed hypotheses and evidence.

## Preserved scientific boundaries

Phase Two does not add:

- machine learning or neural networks;
- an intelligence score;
- an explicit fitness objective;
- host-selected successful organisms;
- attack or cooperation rules;
- mating roles;
- parasites or disease;
- a host-authored social strategy;
- resource diffusion;
- organism-produced environmental resources.

The engine provides opportunities and constraints. It does not define a desired evolutionary outcome.

## Exit decision

All mandatory Phase Two exit criteria are satisfied for the defined scope:

- permanent homogeneous control preserved;
- versioned spatial rules and artifacts;
- matched multi-seed controls;
- energy and resource invariants within tolerance;
- documented/tested event order;
- observable movement and boundary behavior;
- reproducible evidence archive with provenance and checksums;
- measured reference performance;
- no introduced intelligence or fitness objective.

Phase Two is therefore accepted as complete. Later research should begin as a new phase and treat the Phase Two implementation and evidence archive as a frozen reference unless a documented correction is required.
