# Melakat Desktop Lab

[فارسی](README.fa.md) | English

This directory contains the desktop research application and local Phase Zero engine.

## Current status

The default GUI backend is <code>phase-zero-vm-0.2</code>. The engine runs in a separate process from the PySide6 interface. The UI sends serializable commands and receives serializable snapshots, metrics, and lifecycle events.

The earlier <code>demo</code> backend remains available for architecture comparison. It is not a scientific Phase Zero result.

## Design goals

- The UI is schema-driven.
- Adding a parameter means adding a <code>ParameterSpec</code>, not redesigning the window.
- The engine and UI remain process-isolated.
- Scientific rules stay in the engine layer rather than the presentation layer.
- The parameter structure can grow from 50 to 200 fields.
- Saved configurations and results can become the interface between desktop and future web tools.

## Stack

- Python
- PySide6
- PyQtGraph
- multiprocessing
- PyInstaller for Windows packaging

## Run locally

Use a stable CPython release. An old alpha build such as <code>Python 3.12.0a4</code> can break modern packaging tools.

~~~powershell
cd desktop
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
cd ..
python -m melakat_desktop.main
~~~

Run tests:

~~~powershell
cd desktop
python -m unittest discover -s tests -v
~~~

Run the headless experiment runner:

~~~powershell
cd desktop
python -m melakat_desktop.phase_zero_experiment --runs 30 --ticks 2000 --output phase-zero-results.json
~~~

For research exports, use:

~~~powershell
python -m melakat_desktop.phase_zero_experiment --runs 30 --ticks 2000 --output phase-zero-results.json --summary-csv phase-zero-summary.csv --history-csv phase-zero-history.csv
~~~

## Phase One v0.2 implementation

The Phase One implementation gate is complete:

- versioned <code>melakat-run-artifact-0.1</code> results;
- independent artifact loading with configuration-hash validation;
- lineage, genotype, lifetime, death-reason, and mutation-event analysis;
- <code>--config</code> execution from an exported GUI configuration;
- multi-seed control and one-factor-at-a-time <code>--sweep</code> execution;
- <code>melakat-compare</code> plus GUI result comparison;
- saved-result reopening and selected-organism inspection;
- per-tick resource-ledger export in history <code>CSV</code> files;
- 30 passing unit tests covering the engine, VM, artifacts, experiments, and worker.

The full baseline and sensitivity campaign still needs to be run and archived as research evidence. The implementation is ready; the evidence campaign is not silently treated as complete.

## Interface

The research interface provides:

- grouped parameter editing;
- parameter search;
- start, pause, resume, step, stop, and reset;
- a live world view;
- population and energy plots;
- birth and death events;
- engine and measurement versions;
- configuration hash;
- active and historical genotype counts;
- lineage, blocked-division, and resource-waiting metrics;
- configuration and result export.

## Engine boundary

The VM accepts data-only instruction genomes. Organisms cannot execute host Python, import modules, access files, use the network, create subprocesses, or call external APIs.

The GUI must remain an observer and controller. It must not silently add rules that are absent from the engine contract.

## Planned Phase One growth

- lineage inspector and visualization;
- run comparison view;
- independent result reloading;
- parameter sensitivity matrices;
- deterministic replay;
- a concise event log with optional detailed inspection;
- optional Esbiko result viewing in a later integration phase.

## Documentation

- [Phase Zero results](../docs/doc-english/phase-zero-results.md)
- [Phase One roadmap](../docs/doc-english/phase-one-roadmap.md)
- [Desktop lab architecture](../docs/desktop/desktop-lab-architecture.md)
- [Phase Zero VM contract](../docs/desktop/phase-zero-vm.md)
