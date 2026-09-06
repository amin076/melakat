# Melakat

[فارسی](README.fa.md) | English

Melakat is a research-first simulation for studying whether simple data-only digital organisms can exhibit evolutionary and ecological dynamics inside a constrained computational world.

Organisms run inside a bounded virtual machine. They consume finite energy and memory, copy genomes, inherit blind mutation, reproduce, and may die. Phase Two added controlled spatial topology, local resources, sensing and bounded movement without adding a fitness objective or hand-written social behavior. Phase Three now begins from that frozen reference by changing only the spatial distribution of the same total local resource input.

## Current status

**Phase Zero, Phase One, and Phase Two are complete. Phase Two is formally frozen as a reference baseline. Phase Three has started.**

Frozen Phase Two versions:

- world contract: `phase-two-spatial-0.7`
- engine: `phase-two-vm-0.7`
- measurement: `phase-two-measurement-0.1`
- artifact format: `melakat-run-artifact-0.2`

Initial Phase Three versions:

- world contract: `phase-three-environment-0.1`
- engine: `phase-three-vm-0.1`
- measurement: `phase-three-measurement-0.1`

The Phase One homogeneous baseline remains available as a permanent frozen control. The accepted Phase Two implementation/evidence remains a second frozen reference for later spatial/environmental research.

### Phase Two capabilities

- continuous two-dimensional abstract space;
- explicit `reflective` and `toroidal` boundaries;
- local offspring placement and spatial measurements;
- conservative local energy-resource grid with uniform renewal and cell-local capture;
- data-only `SENSE_RESOURCE`, `MOVE_X`, and `MOVE_Y` instructions;
- bounded movement with explicit energy cost;
- spatial/resource/movement event and resource accounting;
- schema-driven desktop controls and organism/boundary/resource layers;
- selected-organism local inspection and spatial time-series metrics;
- saved-result comparison and versioned exports;
- controlled multi-seed evidence matrix;
- deterministic repeat and performance measurements.

### Phase Three v0.1 scope

Phase Three currently adds one causal intervention only: `center_patch` resource heterogeneity.

The matched control is `uniform` allocation. Both modes use the same total initial environmental resource and the same total `world.energy_input_per_tick`; only relative allocation across the existing resource grid changes. The patch is deterministic, so it does not add another random-number stream.

New non-causal measurements include resource-field coefficient of variation and maximum local cell resource. Phase Three v0.1 does not add resource diffusion, programmed resource-seeking, predation, cooperation, seasons, disasters, a fitness function, or host selection.

These are rules and measurements of the implemented digital model. They are not a claim that biological life, intelligence, adaptation, cooperation, competition, or niche formation has been recreated.

## Accepted evidence gates

### Phase One

The accepted Phase One campaign contains 990 runs: 30 seeds across six control conditions and 27 one-factor sensitivity cases, each for 2000 ticks. All recorded configuration, checksum, tick-count, energy and memory checks passed. Maximum absolute energy-balance error was `2.5e-08` under a `1e-07` tolerance.

### Phase Two

The accepted Phase Two campaign contains **360 runs**: 30 seeds across 12 matched spatial/environmental conditions, each for 2000 ticks.

Final Phase Two validation:

- validation failures: `0`;
- maximum absolute energy-balance error: `1.02e-08`;
- maximum absolute local-resource balance error: `4.2e-09`;
- tolerance for both ledgers: `1e-07`;
- deterministic repeat: PASS;
- accepted source commit: `ad5e21159baf0d6bd79a028799b9318ba144fed7`;
- evidence workflow run: `33969619473`.

The default local-resource experiments often reached extinction because energy can remain in unoccupied cells and Phase Two deliberately has no diffusion. Resource-abundant conditions can sustain populations but create much higher turnover. These are model outcomes, not invariant failures.

The formal freeze record is [Phase Two frozen baseline](docs/phase-2/phase-two-frozen-baseline.md). Later exploratory campaigns do not replace that accepted gate.

## Research boundaries

Melakat still deliberately excludes:

- machine learning and neural networks;
- an intelligence objective;
- an explicit fitness function;
- manual selection of successful organisms;
- host-authored attack or cooperation behavior;
- mating roles, parasites, or disease;
- complexity as a reward;
- resource diffusion or organism-produced resources in the current Phase Three v0.1 model;
- filesystem, network, subprocess, host-runtime, or external API access by organisms.

The Python process is the host simulator. Organisms do not execute Python code.

## Documentation

- [Documentation index](docs/README.md)
- [فهرست مستندات فارسی](docs/README.fa.md)
- [Phase One evidence report](docs/doc-english/phase-one-evidence-report.md)
- [Phase Two completion and evidence report](docs/phase-2/phase-two-completion-report.md)
- [Phase Two frozen baseline](docs/phase-2/phase-two-frozen-baseline.md)
- [Phase Three roadmap](docs/phase-3/phase-three-roadmap.md)
- [Phase One evidence archive](results/phase-one/evidence-gate/README.md)
- `results/phase-two/evidence-gate/` — accepted Phase Two campaign, validation, performance, provenance and checksums

## Repository map

- `desktop/src/melakat_desktop/phase_zero_engine.py` — frozen homogeneous reference engine;
- `desktop/src/melakat_desktop/phase_two_engine.py` — frozen Phase Two serial spatial/environment engine;
- `desktop/src/melakat_desktop/phase_two_vm.py` — Phase Two data-only sensing/movement VM extension;
- `desktop/src/melakat_desktop/phase_three_contract.py` — Phase Three environmental-heterogeneity contract;
- `desktop/src/melakat_desktop/phase_three_engine.py` — Phase Three v0.1 engine inheriting Phase Two rules and adding resource-allocation heterogeneity;
- `desktop/src/melakat_desktop/resources.py` — conservative local-resource field with Phase Two uniform and Phase Three weighted allocation primitives;
- `desktop/src/melakat_desktop/spatial.py` — topology, placement and spatial measurements;
- `desktop/src/melakat_desktop/world_contract.py` — frozen Phase Two world contract;
- `desktop/src/melakat_desktop/phase_two_experiment.py` — Phase Two evidence matrix and performance probe;
- `desktop/src/melakat_desktop/ui.py` — desktop research interface;
- `results/phase-one/evidence-gate/` — accepted Phase One evidence;
- `results/phase-two/evidence-gate/` — accepted Phase Two evidence.

## Run the desktop application

Use a stable CPython release; Python 3.12 is the reference CI version.

~~~powershell
git checkout main
git pull
cd desktop
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
python -m unittest discover -s tests -v
cd ..
python -m melakat_desktop.main
~~~

The desktop backend selector now recognizes `phase-three-vm`, but the first heterogeneous intervention is being validated headlessly before Phase Three-specific desktop controls and the general automated experiment runner are expanded. This keeps the initial scientific change small and preserves the frozen Phase Two configuration defaults.

See the [Phase Three roadmap](docs/phase-3/phase-three-roadmap.md) for the current scientific contract and next evidence gate.
