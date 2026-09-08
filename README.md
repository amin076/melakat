# Melakat

[فارسی](README.fa.md) | English

Melakat is a research-first digital-evolution simulator. Simple data-only organisms execute inside a bounded virtual machine, consume finite energy and memory, copy hereditary genomes, mutate, reproduce and die. Later phases added controlled space, local resources, environmental heterogeneity, scalar resource sensing, bounded movement, and now **heritable variable genome length**—without adding an explicit fitness function, machine-learning controller, manual selection, or hand-written social behavior.

## Current status

**Phases Zero through Five are complete.** Accepted older baselines remain frozen and reproducible; later phases extend them through separate versioned contracts rather than silently rewriting them.

Current major evidence milestones:

- **Phase Zero** — bounded VM, real self-copy/division, finite energy/memory, birth/death.
- **Phase One** — reproducible homogeneous-world instrumentation and a 990-run evidence campaign.
- **Phase Two** — 2D space, local resources, sensing/movement substrate, 360-run accepted spatial/environmental evidence; Phase Two is formally frozen.
- **Phase Three** — controlled resource heterogeneity, isolated sensing and movement mechanisms, evolvable non-zero movement encoding, and atomic movement payment.
- **Phase Four** — 60-run matched causal sensing-with-movement gate. Sensing altered downstream ecological/spatial state but did not establish a resolved effect on locomotor execution or directional navigation.
- **Phase Five** — length-robust replication plus blind tandem duplication/deletion. A 60-run matched full campaign established **heritable variable genome length**: variable-length organisms were born and some later reproduced.

## Current Phase Five versions

- world contract: `phase-five-evolvability-0.1`
- structural engine: `phase-five-vm-0.2`
- structural measurement: `phase-five-measurement-0.2`
- structural RNG: `phase-five-structural-rng-0.1`

The Phase Five replication substrate uses sequential `COPY_NEXT` self-copy and template-relative flow control (`NOP_A`, `NOP_B`, `JUMP_TEMPLATE`, `JUMP_TEMPLATE_IF_ZERO`) so the replication loop no longer hard-codes genome length or absolute loop addresses.

## Phase Five accepted evidence

### Gate 5C — exposure calibration

Candidate structural event rates were `0.01`, `0.025`, `0.05`, and `0.10`. The pre-registered rule selected the **lowest** rate with sufficient event exposure, not the rate producing a preferred biological/evolutionary outcome.

- `0.01`: 11 committed events — FAIL exposure threshold
- `0.025`: 26 committed events, 7/8 runs exposed, 12 duplications, 14 deletions — **selected**
- `0.05`: 50 committed events — PASS but deliberately not selected
- `0.10`: 83 committed events — PASS but deliberately not selected

### Gate 5D — full variable-genome campaign

- 30 matched seeds × 2 conditions × 2000 ticks = **60 primary runs**
- control structural event rate: `0.0`
- treatment structural event rate: `0.025`
- balanced duplication/deletion probability: `0.5`
- completed runs: `60/60`
- validation failures: `0`
- deterministic replay: PASS
- maximum absolute energy-balance error: `4.36e-08` under tolerance `1e-07`
- control structural events: `0`
- treatment structural events: `97`
- treatment duplications: `42`
- treatment deletions: `55`
- treatment structural-event exposure: `29/30` runs
- variable-length births: `61`
- variable-length organisms that later reproduced: `12`
- treatment runs ending with active variable-length organisms: `14/30`

The ancestor length is `14`. Control active genomes remained length `14`; treatment active genomes included lengths `13`, `14`, and `15`. Mean genome length remained approximately `14`, so the intervention opened a heritable length dimension without forcing monotonic expansion.

See [Phase Five completion report](docs/phase-5/phase-five-completion-report.md) and [Phase Five roadmap](docs/phase-5/phase-five-evolvability-roadmap.md).

## Scientific boundaries

Melakat deliberately does **not** reward genome size or complexity. Longer genomes naturally consume more structural memory and require more copying/execution work; shorter genomes may lose useful or essential instructions. The host does not protect critical instructions or select successful organisms.

Current evidence does **not** establish:

- increasing functional complexity;
- that larger genomes are better;
- adaptation or fitness advantage;
- intelligence;
- directional navigation/resource seeking;
- cooperation, predation, communication, or multicellularity;
- open-ended evolution.

**Variable genome length is not a complexity metric.** Any future complexity claim requires independent functional/algorithmic/behavioral measurements.

## Core capabilities

- bounded data-only VM;
- real self-copy and division;
- blind hereditary opcode mutation;
- Phase-Five blind single-instruction tandem duplication/deletion;
- variable-length heritable genomes;
- genealogy, lineages and genotype tracking;
- finite energy and structural memory;
- explicit execution, maintenance and reproduction costs;
- deterministic seeded runs and conservation ledgers;
- continuous 2D space with `reflective` / `toroidal` boundaries;
- conservative cell-local resources;
- deterministic `center_patch` heterogeneity;
- data-only `SENSE_RESOURCE`, `MOVE_X`, `MOVE_Y`;
- evolvable non-zero movement steps and atomic movement payment;
- versioned experiment specifications, JSON/CSV exports, provenance and SHA-256 manifests;
- matched-seed paired evidence analysis.

## Documentation and evidence

- [Documentation index](docs/README.md)
- [فهرست مستندات فارسی](docs/README.fa.md)
- [Phase Two frozen baseline](docs/phase-2/phase-two-frozen-baseline.md)
- [Phase Four completion report](docs/phase-4/phase-four-completion-report.md)
- [Phase Five evolvability roadmap](docs/phase-5/phase-five-evolvability-roadmap.md)
- [Phase Five completion report](docs/phase-5/phase-five-completion-report.md)
- `results/phase-one/evidence-gate/` — accepted Phase One evidence
- `results/phase-two/evidence-gate/` — accepted Phase Two evidence
- `results/phase-four/resource-sensing-with-movement/full/` — accepted Phase Four evidence
- `results/phase-five/structural-event-rate-calibration/` — Phase Five exposure calibration
- `results/phase-five/variable-genome-full/` — Phase Five full evidence

## Repository map

- `desktop/src/melakat_desktop/phase_zero_engine.py` — frozen homogeneous reference engine
- `desktop/src/melakat_desktop/phase_two_engine.py` — frozen spatial/local-resource engine
- `desktop/src/melakat_desktop/phase_three_engine.py` — environmental/sensing/movement evidence path
- `desktop/src/melakat_desktop/phase_five_vm.py` — length-robust replication VM
- `desktop/src/melakat_desktop/phase_five_engine.py` — Phase Five variable-genome engine
- `desktop/src/melakat_desktop/phase_five_experiment_support.py` — Phase Five experiment routing/metrics
- `desktop/src/melakat_desktop/experiment_runner.py` — generic reproducible experiment system
- `desktop/src/melakat_desktop/ui.py` — desktop research interface

## Run locally

Python 3.12 is the reference CI version.

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
