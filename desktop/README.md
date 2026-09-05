# Melakat Desktop Lab

This directory contains the first desktop interface scaffold for Melakat.

## Design goals

- The UI is schema-driven. Adding a parameter means adding a ParameterSpec, not redesigning the window.
- The simulation engine runs in a separate process from the UI.
- The UI sends commands and receives serializable events.
- The demo engine is deliberately small and is not yet the final scientific VM.
- The future VM and Experiment 0 rule set can replace the demo engine without changing the UI contract.

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

## Important scientific boundary

The current DemoEngine exists to validate the desktop architecture and event flow. Its reproduction rules are placeholders. It must not be used as a scientific result. The next implementation replaces it with the validated Melakat VM and Experiment 0 rules.

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
