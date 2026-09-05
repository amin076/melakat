# Phase Two Roadmap

[فارسی](../doc-farsi/phase-two-roadmap.md) | [Documentation index](../README.md)

## Purpose

Phase Two extends Melakat from a validated homogeneous world into a controlled spatial and environmental laboratory.

The purpose is not to make the simulation look more realistic by adding arbitrary detail. The purpose is to introduce one new class of world rules at a time, measure its effect against the Phase One baseline, and preserve enough accounting to explain every change.

Phase Two begins with space and local environment as research variables. It does not begin with intelligence, machine learning, social roles, or a reward function.

## Entry gate

Phase Two may start only after these conditions are satisfied:

- the Phase One implementation gate is complete;
- the baseline configuration and artifacts are archived;
- repeated seeds are reproducible;
- the energy and memory invariants pass throughout the baseline;
- blocked division, waiting, fault, birth, and death states have explicit meanings;
- the Phase One baseline can be reloaded and compared without the original live process;
- every new spatial result can be compared with an unchanged homogeneous control.

If a Phase One invariant fails during this gate, the work returns to Phase One investigation instead of adding a new world rule.

## Research principles

1. Introduce one causal mechanism per experiment.
2. Keep the homogeneous world as a permanent control.
3. Version every rule that changes state, timing, resource flow, or observation.
4. Record the event order before interpreting a result.
5. Do not infer adaptation from population increase alone.
6. Treat extinction, stable low diversity, and resource starvation as valid outcomes.
7. Never use a user-interface feature to compensate for an undefined engine rule.

## Work packages

### P2.1 — Version the world model

Define a versioned world contract such as <code>phase-two-spatial-0.1</code>.

The contract must specify:

- coordinate units and bounds;
- the order of environment update, organism execution, movement, resource exchange, division, and death;
- whether all organisms observe the same tick or observe sequentially;
- boundary behavior;
- the precision and conservation rule for spatial resources;
- how snapshots and artifacts encode the new state.

Exit condition:

- the engine can run the Phase One rules with the new world model disabled and produce a baseline-equivalent result.

### P2.2 — Add space and topology as an isolated variable

Implement the smallest spatial layer that can answer a clear question. Candidate boundary models are bounded, reflective, absorbing, and toroidal. They must be separate configurations, not hidden branches inside one unexplained rule.

Initial measurements should include:

- position and displacement;
- boundary contacts;
- local neighborhood size;
- distance between parent and child;
- spatial clustering and occupancy;
- comparison with a well-mixed control.

No conclusion about cooperation or competition should be drawn from proximity alone.

### P2.3 — Add a local resource field

Introduce a resource field only after its accounting is specified. A first model may choose one of the following mechanisms as an explicit experiment:

- fixed resource cells;
- uniform resource renewal;
- local deposit and consumption;
- bounded diffusion.

The first implementation should select one mechanism, one unit system, and one update schedule. It should not combine renewal, diffusion, consumption, and organism-produced resources in the same first experiment.

Required invariants:

- resource cannot become negative;
- every source and sink is recorded;
- total resource error remains within a documented tolerance;
- the homogeneous energy-pool control remains available.

### P2.4 — Add movement and interaction primitives

Add the smallest data-only instructions needed for an organism to sense or move within the world. Each instruction needs:

- an explicit cost;
- a bounded effect;
- a deterministic result under a fixed seed;
- a fault behavior;
- a record in the event and resource ledgers.

Interaction should begin as observation and resource exchange, not as a hand-written social behavior. Do not add attack, cooperation, mating roles, parasites, or a fitness score in the first spatial release.

### P2.5 — Build the Phase Two experiment matrix

Every spatial feature must have controls:

- identical seed with spatial rules disabled;
- identical seed with spatial rules enabled;
- multiple seeds per condition;
- resource-abundant and resource-limited conditions;
- small and large world sizes;
- boundary-model comparison;
- movement-cost control;
- resource-field conservation control.

Report distributions rather than only final population. At minimum report population, births, deaths, active and historical genotypes, lineages, mutation events, faults, energy, memory, position, occupancy, and resource balance.

### P2.6 — Extend the desktop research interface

The interface should add spatial features without turning into a manually maintained form:

- schema-driven world and resource groups;
- a layer switch for organisms, boundaries, and resources;
- time-series selection for spatial metrics;
- selected-organism position and local-neighborhood inspection;
- event filtering by movement, boundary, resource, birth, and death;
- comparison of spatial and homogeneous artifacts;
- export of the exact configuration and world-model version.

The UI remains an observer and controller. The engine remains the authority for rules and measurements.

### P2.7 — Protect reproducibility and scale

Measure cost before increasing world size or organism count:

- execution time per tick;
- memory use;
- event-log volume;
- snapshot size;
- export time;
- deterministic behavior across repeated runs.

Introduce spatial indexing or parallelism only after a serial reference implementation exists. Optimized execution must be checked against the reference with the same configuration and seed.

## Proposed implementation order

1. Archive and accept the Phase One baseline.
2. Version the world-model contract.
3. Add a serial spatial layer with space disabled as the control path.
4. Add one boundary model and its tests.
5. Add one local resource mechanism and ledger checks.
6. Add bounded movement and observation instructions.
7. Run the controlled Phase Two matrix.
8. Add spatial inspection and comparison to the desktop UI.
9. Review evidence before adding another mechanism.

## Phase Two exit criteria

Phase Two is ready for a later research phase only when:

- the homogeneous control remains reproducible;
- spatial rules are versioned and independently reloadable;
- each spatial result has a matching control and seed list;
- resource and energy accounting pass at every sampled point;
- event order is documented and test-covered;
- movement and boundary behavior are observable;
- no result relies on an undocumented UI action;
- performance limits are measured;
- no intelligence, fitness, or complexity objective has been introduced without a separately approved research hypothesis.

## Explicit non-goals

The following are outside the first Phase Two release:

- machine learning;
- neural networks;
- a target intelligence score;
- a general-purpose language runtime inside organisms;
- automatic selection of “good” organisms;
- social behavior written by the host program;
- a large ecosystem model with many interacting resource types;
- web deployment or Esbiko integration.

These may become later hypotheses. They are not prerequisites for learning what spatial rules do to the existing digital world.
