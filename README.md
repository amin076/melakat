# Melakat

[فارسی](README.fa.md) | English

Melakat is a research-first project for studying whether a constrained computational world can support processes resembling digital life and evolution.

Small data-only programs live inside a bounded virtual machine. They consume finite energy and memory, copy their genomes, inherit blind variation, compete for shared resources, and may die.

The central question is not how to build an intelligent system. It is:

> If we define only simple rules, finite resources, incoming energy, imperfect copying, and death, what patterns emerge without being explicitly designed?

## Current status

Phase Zero has been implemented and validated in the desktop application.

The current backend is <code>phase-zero-vm-0.2</code>. It includes:

- bounded data-only VM execution;
- finite registers, words, and working memory;
- self-copy reproduction;
- energy capture and internal energy;
- computation, maintenance, and reproduction costs;
- finite structural memory;
- blind opcode-substitution mutation;
- heredity, generations, lineages, and genome hashes;
- births, deaths, and death reasons;
- energy and memory accounting;
- deterministic seeded runs;
- a desktop interface for observing live results.

The paired GUI control with substitution rate <code>0</code> removed the observed faults, while the nonzero mutation run produced multiple active genotypes and faults. The energy-balance error remained near floating-point zero.

This is implementation evidence, not a claim that biological life has been recreated.

## Research boundaries

The initial world is homogeneous, finite, energy-limited, and isolated inside a custom VM.

The project deliberately excludes, at this stage:

- machine learning and neural networks;
- an intelligence objective;
- an explicit fitness function;
- hand-selected successful organisms;
- cooperation, attack, parasites, or disease;
- spatial geography and environmental heterogeneity;
- complexity as a reward;
- filesystem, network, subprocess, host-runtime, or external API access.

The Python process is the host simulator. Organisms do not execute Python code.

## Bilingual documentation

The repository keeps parallel documentation:

- [English documentation](docs/doc-english/README.md)
- [مستندات فارسی](docs/doc-farsi/README.md)
- [Documentation index](docs/README.md)
- [فهرست مستندات فارسی](docs/README.fa.md)

The main project documents are:

- [Phase Zero results](docs/doc-english/phase-zero-results.md)
- [Phase One roadmap](docs/doc-english/phase-one-roadmap.md)
- [Desktop lab architecture](docs/desktop/desktop-lab-architecture.md)
- [Phase Zero VM contract](docs/desktop/phase-zero-vm.md)

Each scientific or engineering rule must be updated in both language versions.

## Repository map

- <code>desktop/</code> — PySide6 desktop application and Python engine;
- <code>desktop/src/melakat_desktop/vm.py</code> — bounded virtual machine;
- <code>desktop/src/melakat_desktop/phase_zero_engine.py</code> — Phase Zero world and organism rules;
- <code>desktop/src/melakat_desktop/worker.py</code> — process boundary and backend selection;
- <code>desktop/src/melakat_desktop/ui.py</code> — desktop presentation layer;
- <code>docs/doc-english/</code> — canonical English project documents;
- <code>docs/doc-farsi/</code> — canonical Farsi project documents.

## Run the desktop application

Use a stable CPython release rather than an old alpha build.

~~~powershell
cd desktop
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
cd ..
python -m melakat_desktop.main
~~~

Run the test suite:

~~~powershell
cd desktop
python -m unittest discover -s tests -v
~~~

## Phase One

Phase One will focus on evidence quality rather than adding complexity:

1. freeze the Phase Zero contract;
2. export configurations and results;
3. run reproducible multi-seed experiments;
4. inspect historical genotypes and lineages;
5. define blocked-division semantics;
6. improve run comparison and desktop inspection;
7. perform parameter sensitivity experiments;
8. gate any later spatial extension.

Read the [Phase One roadmap](docs/doc-english/phase-one-roadmap.md) before introducing new world rules.
