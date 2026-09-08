# Melakat

[فارسی](README.fa.md) | English

Melakat is a research-first simulation for studying whether simple data-only digital organisms can exhibit evolutionary and ecological dynamics inside a constrained computational world.

Organisms run inside a bounded virtual machine. They consume finite energy and memory, copy genomes, inherit blind mutation, reproduce, and may die. Later phases added controlled spatial topology, local resources, environmental heterogeneity, scalar resource sensing and bounded movement without adding a fitness objective, machine learning controller, or hand-written social behavior.

## Current status

**Phase Zero, Phase One, and Phase Two are complete. Phase Two is formally frozen as a reference baseline. The Phase Three environmental/sensing/movement mechanism sequence is complete, and the Phase Four sensing-with-movement causal evidence gate is complete.**

Frozen Phase Two versions:

- world contract: `phase-two-spatial-0.7`
- engine: `phase-two-vm-0.7`
- measurement: `phase-two-measurement-0.1`
- artifact format: `melakat-run-artifact-0.2`

Current Phase Three execution evidence versions used by the completed Phase Four gate:

- world contract: `phase-three-environment-0.1`
- engine: `phase-three-vm-0.3`
- measurement: `phase-three-measurement-0.3`

The Phase One homogeneous baseline remains a permanent frozen control. The accepted Phase Two implementation/evidence remains the frozen spatial/local-resource reference. Later Phase Three/Phase Four evidence extends those references without silently rewriting them.

### Core capabilities now available

- bounded data-only virtual machine and primitive self-copy/division;
- blind hereditary mutation, genealogy, lineages and genotype tracking;
- finite energy, structural memory, execution, maintenance and reproduction costs;
- deterministic seeded execution and conservation ledgers;
- continuous two-dimensional abstract space;
- explicit `reflective` and `toroidal` boundaries;
- local offspring placement and spatial measurements;
- conservative local energy-resource grid with cell-local capture;
- deterministic `center_patch` environmental heterogeneity with matched total resource input;
- data-only `SENSE_RESOURCE`, `MOVE_X`, and `MOVE_Y` instructions;
- evolvable signed non-zero movement steps;
- bounded movement with explicit atomic energy payment;
- spatial/resource/movement events and measurements;
- schema-driven desktop controls and organism/boundary/resource layers;
- selected-organism local inspection and spatial time-series metrics;
- saved-result comparison and versioned exports;
- automated multi-condition/multi-seed experiment specifications;
- deterministic replay, provenance, validation, CSV/JSON archives and SHA-256 manifests;
- matched-seed paired evidence analysis.

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

The formal freeze record is [Phase Two frozen baseline](docs/phase-2/phase-two-frozen-baseline.md).

### Phase Three

Phase Three introduced resource-allocation heterogeneity and then isolated sensing and movement mechanisms before combining them.

Key accepted findings include:

- `uniform` versus `center_patch` resource allocation, with total resource input held fixed, causally changed population persistence/turnover and spatial concentration in the implemented model;
- sensing-only execution was successfully isolated without movement, but selected population/spatial intervals did not establish a robust directional advantage;
- movement-only execution was isolated and later given an evolvable non-zero step representation;
- a movement accounting bug discovered by a full campaign was rejected as final evidence and corrected with atomic movement payment;
- the corrected 30-seed atomic movement campaign established paid, reproducible realized locomotion without establishing navigation or adaptation.

### Phase Four

Phase Four tested the registered question:

> Does executing local scalar resource sensing alter evolved movement execution and spatial/resource outcomes when locomotion is available?

The full campaign used 30 matched seeds × 2 conditions × 2000 ticks = 60 primary runs. Both conditions had hereditary sensing/movement availability, movement execution, `movement_step_rate=0.5`, atomic movement payment and the same `center_patch` environment. The only intended causal difference was `world.resource_sensing_enabled`.

Integrity/exposure:

- completed runs: `60/60`;
- validation failures: `0`;
- deterministic replay: PASS;
- control sensing operations: `0`;
- treatment sensing operations: `508`;
- treatment sensing-exposed runs: `15/30`;
- treatment joint sensing + non-zero movement runs: `7/30`;
- underpaid realized movement runs: `0`;
- maximum absolute energy-balance error: `4.8e-09`;
- maximum absolute local-resource-balance error: `6.3e-09`.

No registered movement-execution endpoint had an approximate paired 95% interval excluding zero. However three registered spatial/resource endpoints did: treatment had fewer mean local neighbors, greater mean nearest-neighbor distance, and more local resource remaining. A secondary active-population endpoint was also lower in treatment.

The accepted interpretation is therefore narrow: local scalar sensing causally altered downstream ecological/spatial state in this model, consistent with resource-conditioned dynamics, but the campaign did **not** resolve a sensing effect on locomotor execution itself. Because `SENSE_RESOURCE` exposes no direction or gradient, this is not evidence of directional navigation or resource seeking.

See [Phase Four completion report](docs/phase-4/phase-four-completion-report.md).

## Research boundaries

Melakat still deliberately excludes:

- machine learning and neural networks;
- an intelligence objective;
- an explicit fitness function;
- manual selection of successful organisms;
- host-authored attack or cooperation behavior;
- mating roles, parasites, disease or predeclared predator/prey classes;
- complexity as a reward;
- directional resource-seeking logic;
- resource diffusion or organism-produced resources in the accepted current model;
- filesystem, network, subprocess, host-runtime, or external API access by organisms.

The Python process is the host simulator. Organisms do not execute Python code.

The current evidence does not establish navigation, adaptation, fitness advantage, intelligence, cooperation, predation, multicellularity or open-ended evolution.

## Documentation

- [Documentation index](docs/README.md)
- [فهرست مستندات فارسی](docs/README.fa.md)
- [Phase One evidence report](docs/doc-english/phase-one-evidence-report.md)
- [Phase Two completion and evidence report](docs/phase-2/phase-two-completion-report.md)
- [Phase Two frozen baseline](docs/phase-2/phase-two-frozen-baseline.md)
- [Phase Three roadmap](docs/phase-3/phase-three-roadmap.md)
- [Phase Four pre-registered gate](docs/phase-4/phase-four-sensing-movement-gate.md)
- [Phase Four preflight report](docs/phase-4/phase-four-sensing-movement-preflight-report.md)
- [Phase Four completion report](docs/phase-4/phase-four-completion-report.md)
- [Phase One evidence archive](results/phase-one/evidence-gate/README.md)
- `results/phase-two/evidence-gate/` — accepted Phase Two evidence archive
- `results/phase-four/resource-sensing-with-movement/full/` — accepted Phase Four full evidence archive

## Repository map

- `desktop/src/melakat_desktop/phase_zero_engine.py` — frozen homogeneous reference engine;
- `desktop/src/melakat_desktop/phase_two_engine.py` — frozen Phase Two serial spatial/environment engine;
- `desktop/src/melakat_desktop/phase_two_vm.py` — data-only sensing/movement VM extension;
- `desktop/src/melakat_desktop/phase_three_contract.py` — Phase Three environmental-heterogeneity contract;
- `desktop/src/melakat_desktop/phase_three_engine.py` — current Phase Three engine path, including later scoped sensing/movement/atomic semantics;
- `desktop/src/melakat_desktop/phase_three_experiment_support.py` — Phase Three-scoped experiment parameters and compatibility routing;
- `desktop/src/melakat_desktop/resources.py` — conservative local-resource field and weighted allocation primitives;
- `desktop/src/melakat_desktop/spatial.py` — topology, placement and spatial measurements;
- `desktop/src/melakat_desktop/world_contract.py` — frozen Phase Two world contract;
- `desktop/src/melakat_desktop/experiment_runner.py` — versioned automated experiment system;
- `desktop/src/melakat_desktop/ui.py` — desktop research interface;
- `results/phase-one/evidence-gate/` — accepted Phase One evidence;
- `results/phase-two/evidence-gate/` — accepted Phase Two evidence;
- `results/phase-four/resource-sensing-with-movement/` — Phase Four smoke, preflight and full evidence.

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

Headless scientific campaigns use the versioned `melakat-experiment` command and are archived separately from interactive desktop runs.
