# Melakat

[فارسی](README.fa.md) | English

Melakat is a research-first simulation for studying whether simple data-only digital organisms can exhibit evolutionary and ecological dynamics inside a constrained computational world.

Organisms run inside a bounded virtual machine. They consume finite energy and memory, copy genomes, inherit blind mutation, reproduce, and may die. Phase Two adds controlled spatial topology, local resources, sensing and bounded movement without adding a fitness objective or hand-written social behavior.

## Current status

**Phase Zero, Phase One, and Phase Two are complete for their defined research gates.**

Accepted Phase Two versions:

- world contract: `phase-two-spatial-0.7`
- engine: `phase-two-vm-0.7`
- measurement: `phase-two-measurement-0.1`
- artifact format: `melakat-run-artifact-0.2`

The Phase One homogeneous baseline remains available as a permanent frozen control. With `world.spatial_enabled=false`, the Phase Two compatibility path reproduces the accepted Phase One scientific baseline.

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

These are rules and measurements of the implemented digital model. They are not a claim that biological life, intelligence, or adaptive navigation has been recreated.

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

## Research boundaries

Melakat still deliberately excludes:

- machine learning and neural networks;
- an intelligence objective;
- an explicit fitness function;
- manual selection of successful organisms;
- host-authored attack or cooperation behavior;
- mating roles, parasites, or disease;
- complexity as a reward;
- resource diffusion or organism-produced resources in Phase Two;
- filesystem, network, subprocess, host-runtime, or external API access by organisms.

The Python process is the host simulator. Organisms do not execute Python code.

## Documentation

- [Documentation index](docs/README.md)
- [فهرست مستندات فارسی](docs/README.fa.md)
- [Phase One evidence report](docs/doc-english/phase-one-evidence-report.md)
- [Phase Two roadmap](docs/doc-english/phase-two-roadmap.md)
- [Phase Two completion and evidence report](docs/phase-2/phase-two-completion-report.md)
- [Phase Two user test guide](docs/phase-2/phase-two-user-test-guide.md)
- [Phase One evidence archive](results/phase-one/evidence-gate/README.md)
- `results/phase-two/evidence-gate/` — accepted Phase Two campaign, validation, performance, provenance and checksums

## Repository map

- `desktop/src/melakat_desktop/phase_zero_engine.py` — frozen homogeneous reference engine;
- `desktop/src/melakat_desktop/phase_two_engine.py` — Phase Two serial spatial/environment engine;
- `desktop/src/melakat_desktop/phase_two_vm.py` — Phase Two data-only sensing/movement VM extension;
- `desktop/src/melakat_desktop/resources.py` — conservative local-resource field;
- `desktop/src/melakat_desktop/spatial.py` — topology, placement and spatial measurements;
- `desktop/src/melakat_desktop/world_contract.py` — current versioned Phase Two contract;
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

For the first manual Phase Two test, choose `phase-two-vm`, enable spatial rules, use the `reflective` boundary, and initially leave local resources and evolved sensing/movement disabled. Then introduce those mechanisms one at a time.

See the [Phase Two user test guide](docs/phase-2/phase-two-user-test-guide.md) for the acceptance sequence and evidence commands.
