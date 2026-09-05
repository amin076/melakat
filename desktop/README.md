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

## Phase One v0.1 instrumentation

The first Phase One slice provides:

- versioned <code>melakat-run-artifact-0.1</code> JSON results;
- a canonical configuration hash;
- sampled metric history;
- active and historical genotype counts;
- lineage and generation records;
- death reasons and energy-ledger values;
- blocked-division and resource-waiting metrics;
- multi-seed control-suite summaries;
- GUI export for the current configuration and last completed run.

A completed division request remains pending when memory or energy is unavailable. The proposed child genome is held stable and retried on later ticks; memory and energy blocking remain separate measurements.

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
