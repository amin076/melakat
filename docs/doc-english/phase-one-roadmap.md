# Phase One Roadmap

[فارسی](../doc-farsi/phase-one-roadmap.md) | [Documentation index](../README.md)

## Purpose

Phase One moves Melakat from a validated Phase Zero substrate to a measurable, reproducible, and scientifically inspectable digital-evolution laboratory.

The goal is not to add intelligence, machine learning, or visual complexity. The goal is to make every observed change explainable, repeatable, exportable, and tied to an explicit world rule.

## Entry condition

Phase One begins after the following Phase Zero results are recorded:

- the VM performs bounded data-only execution;
- self-copy reproduction works;
- births and deaths change population state;
- finite memory changes reproductive opportunity;
- mutation creates heritable genotype variation;
- the mutation-zero control removes the observed mutation faults;
- the energy-balance error remains near floating-point zero;
- seeded runs are repeatable.

## Non-goals

Phase One must not introduce:

- machine learning or neural networks;
- an intelligence objective;
- an explicit fitness score that directly rewards a desired outcome;
- hand-written selection of successful organisms;
- cooperation, attack, parasites, disease, or social roles;
- spatial geography before the homogeneous baseline is measured;
- complexity as a reward;
- host-language execution by organisms.

These features may be research questions in later phases, but they must not be used to hide an unexplained Phase Zero or Phase One result.

## Work packages

### P1. Freeze the Phase Zero contract

Deliverables:

- a versioned Phase Zero configuration;
- a documented opcode and VM contract;
- a fixed definition of energy and memory units;
- a record of known limitations;
- a reproducibility note containing seed and parameter conventions.

Exit condition:

- changing a GUI label or adding a display metric cannot silently change the engine rules.

### P2. Build a reproducible experiment protocol

Deliverables:

- named parameter presets;
- JSON configuration export;
- headless execution from the same configuration used by the GUI;
- replicate runner with explicit seed lists;
- JSON and CSV result export;
- summary statistics for births, deaths, population, genotypes, faults, energy, and memory.

Required comparisons:

- repeated identical seed;
- different seeds;
- mutation rate zero versus nonzero;
- low versus high memory capacity;
- low versus high energy input;
- instruction cost and maintenance cost sensitivity.

Exit condition:

- every published result includes configuration, engine version, seed list, and output checksum or archived result file.

### P3. Add measurement and inspection

Deliverables:

- time-series export for every tick or a documented sampling interval;
- separate active-genotype and historical-genotype metrics;
- lineage tree export;
- death-reason counts;
- per-lineage birth and survival summaries;
- per-tick energy ledger;
- memory occupancy and free-memory history;
- genome and VM inspector for a selected organism.

Exit condition:

- a user can explain why population changed between two sampled ticks without reading raw source code.

### P4. Resolve resource-boundary semantics

The 500-memory run exposed a meaningful boundary: 31 organisms occupied 496 of 500 units, and completed replicators could wait at division because a child required 16 units.

Phase One must specify and test exactly one baseline policy for this state. Candidate policies are:

1. keep a pending division request and retry;
2. abandon the completed copy and reset the lifecycle;
3. convert failed division into a documented energy cost;
4. allow a bounded replication queue;
5. define an explicit death rule for persistent inability to complete division.

The decision must be made from a documented hypothesis and tested against energy and memory invariants. It must not be selected only to maximize population or diversity.

Exit condition:

- no organism state can remain unexplained indefinitely;
- the UI reports blocked, waiting, and faulted states separately.

### P5. Analyse mutation and lineage dynamics

Deliverables:

- mutation event counts;
- genotype lifetime distributions;
- lineage persistence and extinction;
- parent-to-child mutation maps;
- survival after mutation;
- fault reason distributions;
- historical genotype archive.

Exit condition:

- the project can distinguish a mutation that is created, survives, reproduces, becomes dominant, or disappears.

### P6. Perform parameter-sensitivity experiments

The first sweep should vary one dimension at a time around the validated baseline:

- memory capacity;
- external energy input;
- initial energy pool;
- instruction budget;
- instruction cost;
- maintenance cost;
- reproduction cost;
- offspring energy;
- mutation substitution rate.

Each sweep should use multiple seeds and report uncertainty or run-to-run variation. A parameter is not considered meaningful merely because it changes the final population.

Exit condition:

- each parameter has a documented qualitative role and a safe tested range;
- conservation and population invariants remain valid throughout the sweep.

### P7. Improve the desktop research interface

Deliverables:

- clear separation of configuration, live metrics, and post-run results;
- visible engine version and configuration hash;
- active versus historical genotype labels;
- blocked-division indicator;
- lineage and organism inspector;
- run comparison view;
- export buttons for configuration and results;
- concise event log with an optional detailed log.

Exit condition:

- the interface supports a 50-to-200 parameter schema without becoming a hand-built form;
- a saved result can be reopened and interpreted without the original live process.

### P8. Gate optional world extensions

Only after P1–P7 pass should the project evaluate a spatial or environmental extension.

A spatial extension must be introduced as a separate experiment with:

- a new versioned rule set;
- a clear comparison to the homogeneous baseline;
- no silent change to existing Phase Zero results;
- tests for boundary conditions and resource accounting.

## Proposed implementation order

1. Freeze and tag the Phase Zero contract.
2. Add configuration and result export.
3. Add replicate and sensitivity runners.
4. Add historical genotype and lineage measurements.
5. Define and test blocked-division semantics.
6. Improve GUI inspection and comparison.
7. Run the Phase One experiment matrix.
8. Review the evidence before any spatial extension.

## Phase One acceptance criteria

Phase One is complete only when:

- repeated seeded runs are identical;
- different seeds produce variation without violating invariants;
- mutation controls are reproducible;
- every birth and death has a recorded reason and genealogy link;
- energy and memory accounting pass at every sampled point;
- blocked or waiting states have explicit semantics;
- results can be exported and independently reloaded;
- parameter sweeps have documented protocols;
- no result depends on an unrecorded GUI action;
- no explicit intelligence or complexity objective has been added.

## Research posture

A stable low-complexity population, repeated extinction, a dominant short genome, or failure to produce long-term diversity are all valid results. Phase One should improve the quality of evidence rather than force the system toward a preferred outcome.

## Phase One v0.2 implementation status

The Phase One implementation gate is complete. The code now covers the required measurement, export, comparison, and inspection paths while preserving the Phase Zero rules.

Implemented:

- versioned <code>melakat-run-artifact-0.1</code> JSON results;
- canonical configuration hashes and independent artifact loading with hash validation;
- summary analysis for lineages, genotypes, genotype lifetimes, death reasons, and parent-to-child mutation events;
- a one-factor-at-a-time sensitivity sweep over nine resource, execution, reproduction, and mutation parameters;
- saved-configuration execution through <code>--config</code>, using the same validated schema exported by the GUI;
- multi-seed control and sensitivity protocols with aggregate metrics;
- command-line result comparison through <code>melakat-compare</code>;
- GUI actions for opening a saved result and comparing two saved results;
- a selected-organism inspector in the desktop interface;
- per-tick resource-ledger data in the history <code>CSV</code> export;
- visible distinction between active and historical genotypes, active lineages, blocked divisions, and resource-waiting states.

Verification completed for this implementation slice:

- 31 unit tests pass;
- all desktop Python modules pass syntax compilation;
- a saved GUI configuration was executed successfully by the headless runner;
- a sensitivity-sweep smoke run produced 9 parameters, 27 cases, and the expected exports;
- identical uploaded artifacts compare as identical, while different seeds are detected as different results.

The scientific evidence campaign is intentionally separate from the implementation gate. The full multi-seed baseline and sensitivity matrix still needs to be executed, archived, and reviewed as a research run. This document does not claim that every scientific question has been answered.

The baseline blocked-division policy remains:

1. a completed division request remains pending;
2. the proposed child genome is created once and held stable while waiting;
3. the engine retries on later ticks;
4. insufficient memory and insufficient energy are reported as separate states;
5. the pending state is visible in snapshots, metrics, and exported history.

Phase One is ready for the evidence campaign. Phase Two must not change the Phase Zero baseline silently; it begins only after the baseline artifacts and invariants have been archived and accepted.
