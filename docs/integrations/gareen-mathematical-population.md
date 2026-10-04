# Gareen objects in the Melakat simulation

This integration is the first vertical slice between the two projects.

## Responsibility boundary

- **Gareen** owns mathematical meaning:
  - conjecture generation
  - research-value scoring
  - statement identity
  - proof status
- **Melakat** owns evolutionary dynamics:
  - population
  - energy
  - age
  - reproduction
  - death
  - lineage
  - resource competition

The integration intentionally does not let Melakat invent mathematical
transformations.

## Current experiment

1. Build Gareen's initial mathematical knowledge.
2. Generate Gareen research conjectures.
3. Rank them with Gareen's existing research-value filter.
4. Convert accepted candidates into Melakat mathematical organisms.
5. Run several Melakat population ticks.
6. Give higher-value candidates better access to reproduction resources.
7. Record lineage and population metrics.

At this stage reproduction is **clone reproduction**. A child keeps the
parent's mathematical statement. This proves the population/lifecycle
integration without hiding a mathematical mutation algorithm inside Melakat.

## Important interpretation

This is not yet mathematical evolution.

It demonstrates:

Gareen candidate -> Melakat organism -> resource selection -> lineage

The next stage is:

parent theorem -> Gareen mutation/generalization -> new conjecture ->
value evaluation -> Melakat selection

That is where genuine mathematical evolution begins.

## Why the boundary matters

Melakat should not silently become a second theorem prover or conjecture
generator. Gareen remains the source of mathematical semantics, while
Melakat provides the experimental evolutionary environment.
