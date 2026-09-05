# Phase Two Spatial Topology 0.2

[فارسی](phase-two-spatial-topology-0.2.fa.md) | [P2.1 contract](phase-two-world-contract-0.1.md) | [Phase Two roadmap](../doc-english/phase-two-roadmap.md)

## Identity

- World contract: `phase-two-spatial-0.2`
- Engine: `phase-two-vm-0.2`
- Historical homogeneous reference: `phase-zero-vm-0.2`
- Measurement contract: `phase-one-measurement-0.1`
- Spatial run artifact: `melakat-run-artifact-0.2`
- Boundary model: `reflective`

P2.2 introduces the first active spatial mechanism. It does not introduce movement, local resources, sensing, cooperation, attack, fitness rewards, or any host-side behavior goal.

## Research question

Can Melakat introduce spatial heredity and a bounded topology while preserving the Phase One non-spatial dynamics for the same seed?

This is deliberately narrower than asking whether space changes evolution. In P2.2, position affects only where an offspring is created. It does not yet affect access to energy, computation, survival, mutation, or reproduction eligibility. Therefore population-level non-spatial state should remain identical between the enabled and disabled spatial runs for the same seed.

## Spatial activation

`world.spatial_enabled=false` remains the default and preserves the frozen homogeneous control.

When `world.spatial_enabled=true`, the P2.2 model activates:

- a continuous two-dimensional rectangular world;
- one explicit `reflective` boundary model;
- local offspring placement around the parent;
- spatial measurements and boundary-contact accounting.

Only `phase-two-vm` applies these rules. The historical `phase-zero-vm` engine remains unchanged.

## Initial positions

Initial organisms retain the existing Phase One seeded uniform `x` and `y` placement. This is intentional: the initial state is held constant across homogeneous and P2.2 comparisons.

Coordinates are abstract world units. They are not metres or biological cell diameters.

## Offspring placement

At a successful division in spatial mode:

1. the parent passes the same memory, energy, mutation, and VM checks as the homogeneous model;
2. the historical engine RNG consumes the same two child-position draws that Phase One consumed, but those values are discarded;
3. an independent spatial RNG draws a radial displacement uniformly by area inside `world.offspring_dispersion_radius`;
4. the attempted child position is added to the parent position;
5. if either coordinate crosses a boundary, it is reflected back into the rectangular domain;
6. the child is created at the reflected position.

The default dispersion radius is `1.0` abstract world unit.

No organism moves after birth in P2.2.

## Reflective boundary

For an axis with maximum coordinate `L`, an out-of-range coordinate is folded back into the closed interval `[0, L]`. The implementation supports overshoot larger than one world width by reducing the coordinate over a period of `2L` before reflection.

`boundary_contacts` counts axis crossings attempted by offspring placement. A single birth may therefore record zero, one, or two contacts.

No organism dies, loses energy, or gains a reward because of boundary contact in P2.2.

## RNG isolation

Spatial randomness uses a dedicated deterministic stream:

- stream: `offspring-placement-v1`;
- seed derivation: SHA-256 of `run.seed`, the world-contract version, and the stream identifier;
- the stream is separate from the historical engine RNG.

The engine also preserves the two historical child-position RNG calls on the original RNG stream. This is a scientific control, not an optimization detail. It prevents spatial placement from silently shifting scheduler and mutation randomness.

The acceptance test verifies that, for the same seed, enabling P2.2 leaves non-spatial population, birth, death, genotype, lineage, instruction, fault, memory, energy, ledger, genealogy, and genotype-catalog state identical to the disabled spatial control.

## Spatial measurements

When spatial mode is enabled, metrics and CSV exports add:

- `boundary_model`;
- `spatial_rng_stream`;
- `spatial_births`;
- `boundary_contacts`;
- `mean_parent_child_distance`;
- `max_parent_child_distance`;
- `mean_local_neighbors`;
- `mean_nearest_neighbor_distance`;
- `occupied_spatial_bins`;
- `spatial_occupancy_fraction`.

### Parent-child distance

This is Euclidean distance between the parent and the reflected final offspring position. Because there is no later movement, it is also the persistent parent-child separation for the P2.2 model.

### Local neighborhood

`world.neighborhood_radius` is an observation-only radius. Its default is `2.0`. It changes metrics only and does not affect organism behavior.

`mean_local_neighbors` is the average count of other active organisms within this Euclidean radius.

### Nearest-neighbor distance

`mean_nearest_neighbor_distance` is the mean Euclidean distance from each active organism to its nearest other active organism. It is a descriptive spatial statistic, not a claim of cooperation or competition.

### Occupancy

The world is divided only for measurement into a normalized `10 x 10` grid. `occupied_spatial_bins` counts bins containing at least one active organism, and `spatial_occupancy_fraction` divides that count by 100.

This grid is not the simulation substrate. Organisms remain in continuous coordinates.

## Persistence

P2.2 continues using `melakat-run-artifact-0.2`. JSON summaries retain the complete spatial metrics and snapshots retain organism coordinates plus active spatial-contract metadata. Summary and history CSV exports include the P2.2 spatial fields.

The loader continues accepting Phase One `melakat-run-artifact-0.1` files.

## Acceptance conditions

P2.2 passes only if:

- `phase-two-spatial-0.2` and `phase-two-vm-0.2` are explicit;
- reflective coordinate handling is unit-tested, including large overshoot;
- spatial mode is deterministic for a fixed seed;
- all organism positions remain inside the configured bounds;
- offspring final distance does not exceed the configured dispersion radius;
- the frozen Phase One fingerprint still passes with spatial mode disabled;
- enabled and disabled runs preserve all tested non-spatial dynamics for the same seed;
- spatial measurements are exposed in metrics and CSV exports;
- the archived Phase One evidence gate remains valid;
- the complete unit-test suite and Python compilation pass.

## Scientific limits

P2.2 does **not** show that spatial structure changes selection or adaptation. Because resources and behavior are still global/non-spatial, position currently changes spatial genealogy and clustering only.

Population growth is not evidence of adaptation. Lower occupancy is not evidence of cooperation. Spatial proximity is not an interaction until a later rule explicitly makes it causal.

## Next package

P2.3 may introduce exactly one local resource mechanism. That package must define a source/sink ledger and compare the local-resource world against both the P2.2 spatial control and the Phase One homogeneous control.
