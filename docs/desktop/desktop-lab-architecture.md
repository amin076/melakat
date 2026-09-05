# Desktop Lab Architecture

[فارسی](desktop-lab-architecture.fa.md) | [Documentation index](../README.md)

## Decision

Melakat is currently an independent Desktop Research Lab. Esbiko may become a future viewer or distribution surface, but it is not part of the current engine boundary.

The architecture separates scientific rules, process control, and presentation so that a larger parameter set and future interfaces do not require rewriting the simulation core.

## Runtime layers

### 1. Domain and engine

The engine layer owns:

- VM execution;
- organism state;
- genome copying and division;
- energy and memory rules;
- mutation and heredity;
- births, deaths, genealogy, and metrics;
- conservation accounting.

Current implementation files include:

- <code>vm.py</code>;
- <code>phase_zero_engine.py</code>;
- <code>phase_zero_experiment.py</code>.

This layer must not import PySide6 or calculate presentation-only values.

### 2. Process boundary

The engine runs in a separate process. The UI sends commands and receives serializable events.

Current command vocabulary includes:

- <code>start</code>;
- <code>pause</code>;
- <code>resume</code>;
- <code>step</code>;
- <code>reset</code>;
- <code>stop</code>.

Current event vocabulary includes:

- <code>ready</code>;
- <code>status</code>;
- <code>tick</code>;
- <code>organism_born</code>;
- <code>organism_died</code>;
- <code>finished</code>;
- <code>stopped</code>.

The process boundary prevents a long run from blocking the UI and gives future headless, desktop, or web clients the same engine contract.

### 3. Parameter schema

Every parameter is defined through a <code>ParameterSpec</code> with:

- path;
- label;
- group;
- kind;
- default;
- range;
- step;
- description;
- optional advanced flag.

The UI builds forms from the schema. Adding a parameter should normally be a data change rather than a layout rewrite.

For growth from 50 to 200 parameters:

- groups are required;
- search is required;
- validation remains centralized;
- configurations must be serializable and versioned;
- global variables must not carry experiment state;
- presets must be explicit and reviewable.

### 4. Presentation

The UI displays:

- parameter controls;
- the world view;
- live metrics;
- population and energy curves;
- event output.

The UI must not invent births, deaths, energy, memory, or fitness values. It renders values received from the engine.

Phase One should add an inspector for:

- a selected organism;
- genome and genome hash;
- instruction pointer and registers;
- memory;
- replication progress;
- division state;
- parent and lineage;
- death reason when available.

### 5. Persistence and reproducibility

Configurations, run results, snapshots, and event streams should become explicit artifacts.

A reproducible result must identify:

- engine version;
- configuration;
- seed;
- tick limit;
- parameter schema version;
- result format version.

The desktop and headless runner should consume the same configuration model.

## Current Phase Zero evidence

The architecture has now been exercised with the Phase Zero VM in the GUI.

The observed results demonstrate:

- births and deaths change population state;
- memory capacity changes reproductive opportunity;
- nonzero mutation can produce faults and multiple active genotypes;
- the mutation-zero control removes the observed faults;
- energy balance remains near zero;
- metrics satisfy population and memory invariants.

## Known boundary

With memory capacity 500 and an allocation of 16 units per default organism, 31 active organisms occupy 496 units. A completed replicator can then wait at the division boundary because a child needs 16 units and only 4 units remain.

This is a real engine state and is now a Phase One design question. The architecture must expose it explicitly rather than allowing the UI to make it look like unexplained inactivity.

## Extension rules

A new engine rule should be introduced through:

- a versioned configuration or rule set;
- a domain-level implementation;
- unit and integration tests;
- a metric or event that makes the rule observable;
- a bilingual documentation update;
- a reproducible experiment.

A new UI feature should normally be one of:

- a new schema-driven parameter;
- a new command or event;
- a new independent panel;
- a new metric or exporter.

A feature should not require rewriting <code>MainWindow</code> or duplicating scientific logic in the UI.

## Future integration

Saved JSON results can later be consumed by Esbiko or another viewer. That integration should remain downstream of the engine and should not change the scientific rules of the desktop laboratory.
