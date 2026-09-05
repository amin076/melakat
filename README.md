# Melakat

[فارسی](README.fa.md) | English

Melakat is a research-first project for studying whether a constrained computational world can support processes resembling digital life and evolution.

Small data-only programs live inside a bounded virtual machine. They consume finite energy and memory, copy their genomes, inherit blind variation, compete for shared resources, and may die.

The central question is not how to build an intelligent system. It is:

> If we define only simple rules, finite resources, incoming energy, imperfect copying, and death, what patterns emerge without being explicitly designed?

## Current status

Phase Zero is implemented and validated. Phase One is complete at both the implementation gate and the scientific evidence gate for the defined homogeneous baseline.

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
- a desktop interface for live and saved-result inspection;
- versioned JSON and CSV experiment outputs;
- lineage, genotype, mutation, and death analysis;
- multi-seed control and sensitivity runners;
- saved-result comparison.

The accepted Phase One evidence campaign contains 990 runs: 30 seeds across six control conditions and 27 one-factor sensitivity cases, each run for 2000 ticks. The campaign passed all recorded energy, memory, seed-coverage, run-count, configuration-hash, result-checksum, and tick-count checks. The maximum absolute energy-balance error was <code>2.5e-08</code> under a <code>1e-07</code> tolerance.

The mutation-zero control produced one genotype, one lineage, zero mutation events, zero VM faults, and zero deaths across all 30 seeds. The sensitivity campaign also showed that the baseline 500-unit world is dominated by a structural-memory bottleneck, while higher memory or lower energy availability can expose an energy-limited high-turnover regime.

These are results of the implemented digital model, not a claim that biological life has been recreated.

## Research boundaries

The accepted Phase One baseline is homogeneous, finite, resource-limited, and isolated inside a custom VM.

The project deliberately excludes from this baseline:

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
- [Phase One evidence report](docs/doc-english/phase-one-evidence-report.md)
- [Phase One evidence archive](results/phase-one/evidence-gate/README.md)
- [Phase Two roadmap](docs/doc-english/phase-two-roadmap.md)
- [Desktop lab architecture](docs/desktop/desktop-lab-architecture.md)
- [Phase Zero VM contract](docs/desktop/phase-zero-vm.md)

Each scientific or engineering rule must be updated in both language versions.

## Repository map

- <code>desktop/</code> — PySide6 desktop application and Python engine;
- <code>desktop/src/melakat_desktop/vm.py</code> — bounded virtual machine;
- <code>desktop/src/melakat_desktop/phase_zero_engine.py</code> — homogeneous baseline world and organism rules;
- <code>desktop/src/melakat_desktop/phase_zero_experiment.py</code> — baseline, controls, and sensitivity execution;
- <code>desktop/src/melakat_desktop/phase_one_evidence.py</code> — accepted evidence-campaign protocol and primary gate;
- <code>desktop/src/melakat_desktop/evidence_audit.py</code> — supplemental archive consistency checks;
- <code>desktop/src/melakat_desktop/worker.py</code> — process boundary and backend selection;
- <code>desktop/src/melakat_desktop/ui.py</code> — desktop presentation layer;
- <code>results/phase-one/evidence-gate/</code> — accepted Phase One evidence archive;
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

## Phase One evidence reproduction

The full accepted campaign is intentionally not run on every push. It can be regenerated deliberately through the manual <code>Phase One evidence campaign</code> GitHub Actions workflow or with:

~~~powershell
melakat-phase-one-evidence --runs 30 --ticks 2000 --seed-start 1 --output-dir results/phase-one/evidence-gate
~~~

A regenerated campaign must be compared with the accepted archive before replacing it.

## Next step: Phase Two

Phase Two may now begin with <code>P2.1</code>, the versioned world-model contract and baseline-compatibility mode. The homogeneous Phase One baseline must remain available unchanged as the permanent control. Spatial boundaries, local resources, movement, and observation are introduced only in later isolated work packages after the <code>P2.1</code> compatibility contract passes.
