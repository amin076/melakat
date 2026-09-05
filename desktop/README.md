# Melakat Desktop Lab

This directory contains the first desktop interface scaffold for Melakat.

## Design goals

- The UI is schema-driven. Adding a parameter means adding a ParameterSpec, not redesigning the window.
- The simulation engine runs in a separate process from the UI.
- The UI sends commands and receives serializable events.
- The default GUI backend is the bounded Phase Zero VM.
- The demo engine remains available for architecture comparison.
- The Phase Zero VM is an execution substrate, not yet the final biological rule set.

## Stack

- Python
- PySide6
- PyQtGraph
- multiprocessing
- PyInstaller for Windows packaging

## Run locally

~~~powershell
cd desktop
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
cd ..
python -m melakat_desktop.main
~~~

The first window provides:

- grouped parameter editing;
- parameter search;
- start, pause, resume, step, stop and reset;
- a live world view;
- population and energy plots;
- event log;
- a process boundary between UI and engine.

## Engine boundary

The GUI now runs the bounded Phase Zero VM by default. The VM has finite registers, finite memory, finite word arithmetic, explicit faults, and an instruction budget. The DemoEngine remains available as a comparison backend.

The Phase Zero VM currently does not claim final biological behavior. Reproduction, mutation, genome copying, sensing, and the final Experiment 0 rules remain separate research and implementation steps.

## Planned growth

The parameter schema can grow from 20 to 50 or 200 fields without changing the main window. Later we can add:

- parameter presets and named experiments;
- genome and register inspectors;
- memory visualisation;
- lineage tree;
- snapshots and deterministic replay;
- multiple-run comparison;
- export to JSON, CSV and image;
- validated VM rule modules;
- optional Esbiko viewer integration.
