# Phase One Roadmap

[فارسی](../doc-farsi/phase-one-roadmap.md) | [Evidence report](phase-one-evidence-report.md) | [Documentation index](../README.md)

## Purpose

Phase One moves Melakat from a validated Phase Zero substrate to a measurable, reproducible, and scientifically inspectable digital-evolution laboratory.

The goal is evidence quality, not intelligence, machine learning, a hand-written fitness objective, or visual complexity. Every observed change must be repeatable, exportable, and tied to an explicit world rule.

## Entry condition

Phase One entered after Phase Zero demonstrated bounded data-only VM execution, self-copy reproduction, finite energy and memory, heritable substitution mutation, births and deaths, near-zero energy-balance error, mutation-zero controls, and deterministic seeded runs.

## Non-goals

Phase One does not introduce:

- machine learning or neural networks;
- an intelligence objective;
- an explicit fitness score that directly rewards a desired outcome;
- hand-written selection of successful organisms;
- cooperation, attack, parasites, disease, or social roles;
- spatial geography before the homogeneous baseline is measured;
- complexity as a reward;
- host-language execution by organisms.

## Completed work packages

### P1 — Freeze the Phase Zero contract

Completed through the versioned <code>phase-zero-vm-0.2</code> engine contract, documented VM/opcode semantics, finite energy and memory units, explicit limits, and deterministic seed conventions.

### P2 — Reproducible experiment protocol

Completed with:

- schema-validated configuration;
- configuration export;
- headless execution from exported configuration;
- explicit seed lists;
- JSON and CSV outputs;
- versioned <code>melakat-run-artifact-0.1</code> results;
- canonical <code>config_hash</code> values;
- multi-seed controls and replicates.

### P3 — Measurement and inspection

Completed with:

- sampled tick history;
- active and historical genotype metrics;
- genealogy records;
- lineage summaries;
- death reasons;
- mutation maps;
- per-tick resource ledger;
- memory occupancy and free-memory history;
- selected-organism VM/genome inspection.

### P4 — Resource-boundary semantics

The baseline blocked-division policy is fixed:

1. a completed division request remains pending;
2. the proposed child genome is created once and held stable;
3. the request is retried on later ticks;
4. insufficient memory and insufficient energy are distinct states;
5. the pending state is visible in snapshots, metrics, events, and exports.

This prevents a completed replicator from entering an unexplained hidden state at a resource boundary.

### P5 — Mutation and lineage analysis

Completed with genotype cataloguing, parent-to-child mutation detection, historical genotype lifetimes, lineage summaries, mutation-event counts, and death/fault analysis.

### P6 — Parameter sensitivity

Completed for nine one-factor-at-a-time parameters:

- memory capacity;
- external energy input;
- initial energy pool;
- instruction budget;
- instruction cost;
- maintenance cost;
- reproduction cost;
- offspring energy;
- substitution mutation rate.

The accepted campaign used 30 seeds for every tested condition.

### P7 — Desktop research interface

Completed for the Phase One scope with schema-driven parameters, visible engine/configuration provenance, active/historical genotype metrics, blocked-division states, organism inspection, saved-result loading, result comparison, and exports.

### P8 — Gate later world extensions

Completed by executing and archiving the homogeneous evidence campaign before adding any new spatial rule.

## Scientific evidence campaign

The accepted campaign is described in the [Phase One evidence report](phase-one-evidence-report.md) and archived under <code>results/phase-one/evidence-gate/</code>.

Protocol:

- engine: <code>phase-zero-vm-0.2</code>;
- measurement: <code>phase-one-measurement-0.1</code>;
- evidence format: <code>melakat-phase-one-evidence-0.1</code>;
- base configuration hash: <code>b90c2df4f218b285</code>;
- seeds: <code>1–30</code>;
- <code>2000 ticks</code> per run;
- six controls, including the restored <code>reproduction.cost = 0</code> control;
- 27 sensitivity cases;
- 990 archived runs plus one exact repeated-seed check.

Primary gate result:

- energy-invariant failures: <code>0</code>;
- memory-invariant failures: <code>0</code>;
- seed-coverage failures: <code>0</code>;
- run-count failures: <code>0</code>;
- configuration-hash failures: <code>0</code>;
- result-checksum failures: <code>0</code>;
- tick-count failures: <code>0</code>;
- reproducibility failure: <code>false</code>;
- maximum absolute energy-balance error: <code>2.5e-08</code> under a <code>1e-07</code> tolerance.

A supplemental archive audit also passes population accounting, non-negative final resources, version consistency, and cross-condition equality whenever the same effective configuration and seed are repeated.

## Main evidence findings

The evidence campaign supports bounded conclusions about the implemented model:

- the 500-unit baseline is predominantly memory-limited near its population ceiling of 31 default organisms;
- the mutation-zero control removes observed mutation events, genotype diversification, VM faults, and deaths across all 30 tested seeds;
- higher mutation increases turnover, genotype history, and faults even when final population remains fixed at the memory ceiling;
- reducing energy input or increasing maintenance cost can move the world into an energy-limited regime;
- increasing memory can remove the memory bottleneck, expose an energy bottleneck, and greatly increase birth/death and genotype turnover without simply increasing final population;
- final population alone is therefore not a sufficient indicator of evolutionary dynamics.

No extinction occurred in the 990 campaign runs. This is an observation within the tested parameter ranges and seeds, not a claim that extinction is impossible.

## Phase One acceptance criteria

Phase One is accepted because:

- repeated seeded execution is deterministic;
- different seeds produce variation without violating recorded invariants;
- mutation controls are reproducible;
- births, deaths, genealogy, mutations, faults, blocked divisions, and resource waits are observable;
- energy and memory accounting pass the archived campaign;
- results are exportable, reloadable, and comparable;
- sensitivity protocols and exact seed lists are archived;
- no result depends on an unrecorded GUI action;
- no intelligence, fitness, or complexity objective was added.

## Limitations

The accepted evidence is deliberately bounded to seeds <code>1–30</code>, 2000-tick runs, the tested one-factor parameter ranges, and the homogeneous Phase One model. It does not measure all multi-parameter interactions, prove open-ended evolution, or establish quantitative correspondence with biology.

## Gate status

**Phase One implementation gate: complete.**

**Phase One scientific evidence gate: complete for the defined homogeneous baseline.**

Phase Two may now begin with <code>P2.1</code>. The homogeneous Phase One engine and accepted archive remain the permanent control, and no spatial or environmental rule may silently alter that baseline.
