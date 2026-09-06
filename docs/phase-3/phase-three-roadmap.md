# Phase Three Roadmap — Environmental Heterogeneity

[فارسی](phase-three-roadmap.fa.md)

## Status

Phase Three has started under contract `phase-three-environment-0.1`.

The first scientific question is deliberately narrow:

> If total resource input is held constant, does changing only the spatial distribution of those resources alter population and lineage dynamics?

## Frozen reference

Phase Three starts from the accepted Phase Two baseline and does not modify its scientific contract:

- `phase-two-spatial-0.7`
- `phase-two-vm-0.7`
- `phase-two-measurement-0.1`

The formal freeze record is `docs/phase-2/phase-two-frozen-baseline.md`.

## P3.1 — Resource heterogeneity mechanism

The first Phase Three engine is `phase-three-vm-0.1`.

It inherits the Phase Two VM, topology, reproduction, mutation, memory, local capture and movement semantics. Its first new causal mechanism is a deterministic `center_patch` resource allocation mode.

The control is `uniform`.

The intervention is `center_patch`.

For both conditions:

- the total initial environmental resource is identical;
- the total `world.energy_input_per_tick` is identical;
- no resource diffusion is introduced;
- capture remains cell-local;
- organism actions remain unchanged;
- the patch geometry adds no new random-number stream.

The patch changes only relative allocation weights across the existing grid. The allocation is normalized, so conservation totals remain matched.

## P3.2 — Matched control experiment

The first full Phase Three campaign will compare:

1. `uniform` resource allocation;
2. `center_patch` resource allocation.

The initial target configuration is based on the stable Phase Two local-resource regime around `world.energy_input_per_tick = 20.0`, because it allows non-trivial survival and turnover without the memory-saturated abundance regime dominating immediately.

Planned matched controls:

- same 30 seeds;
- same 2000 ticks;
- same initial organisms;
- same initial organism energy;
- same total initial environmental energy;
- same total energy input per tick;
- same resource grid;
- same local capture limit;
- same boundary model;
- same mutation rate;
- same reproduction rules;
- sensing/movement initially disabled so resource geography is isolated first.

## P3.3 — Measurements

Phase Three adds non-causal measurements for resource heterogeneity, including:

- resource-field coefficient of variation;
- maximum local cell resource;
- existing population, lineage, genotype, extinction and turnover metrics;
- existing energy and local-resource conservation checks.

Measurements do not alter organism behavior.

## P3.4 — Evidence gate

Before scientific interpretation, the Phase Three evidence gate must establish:

- deterministic repeat for the same seed/configuration;
- `360`-style matched-run discipline where appropriate, beginning with the two-condition 30-seed campaign;
- energy balance within `1e-7`;
- local-resource balance within `1e-7`;
- no negative local resource values;
- no out-of-bounds organisms;
- uniform Phase Three control preserves Phase Two dynamics for matched configurations apart from version/Phase-Three-only metadata.

## P3.5 — Interpretation boundary

A difference between `uniform` and `center_patch` may support a statement about the causal effect of spatial resource heterogeneity on recorded model dynamics.

It does **not** by itself establish:

- adaptation;
- resource-seeking evolution;
- cooperation;
- competition;
- niche formation;
- intelligence;
- open-ended evolution.

Those require later experiments designed specifically for those hypotheses.

## Deferred mechanisms

Phase Three v0.1 does not add:

- sensing improvements;
- programmed movement toward resources;
- predation;
- attack;
- cooperation rules;
- mating roles;
- disasters;
- seasons;
- resource diffusion;
- organism-produced resources;
- fitness functions or host selection.

These remain separate future interventions so causal attribution stays possible.
