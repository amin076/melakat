# Phase Two User Test Guide

[فارسی](phase-two-user-test-guide.fa.md) | [Phase Two roadmap](../doc-english/phase-two-roadmap.md)

This guide is the manual acceptance path for the completed Phase Two release.

## 1. Update the repository

From the Melakat repository root:

~~~powershell
git checkout main
git pull
~~~

## 2. Create or refresh the Python environment

Use CPython 3.12 when available.

~~~powershell
cd desktop
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
~~~

## 3. Run the automated test suite

~~~powershell
python -m unittest discover -s tests -v
~~~

The suite must complete without failures before manual simulation testing.

## 4. Launch the desktop laboratory

From the repository root with the virtual environment still active:

~~~powershell
cd ..
python -m melakat_desktop.main
~~~

## 5. Phase One compatibility check

Run the default homogeneous control first:

- Engine backend: `phase-two-vm`
- Enable spatial rules: off
- Enable local resource field: off
- Enable evolved sensing/movement: off
- Seed: `1`
- Maximum ticks: `2000`

This is the permanent Phase One-compatible control path. Spatial metadata may be present, but the scientific state must remain baseline-equivalent.

## 6. Spatial topology check

Use:

- Engine backend: `phase-two-vm`
- Enable spatial rules: on
- Boundary model: `reflective`
- Offspring dispersion radius: `1.0`
- Enable local resource field: off
- Enable evolved sensing/movement: off
- Seed: `1`

Run a short simulation first, for example 200-500 ticks. Inspect organism positions, parent-child distance, local-neighbor measurements, occupancy, and boundary contacts.

Repeat with boundary model `toroidal`. In the toroidal world, neighborhood distance uses the shortest wrapped path across the world edge.

## 7. Local-resource check

Enable:

- Enable spatial rules: on
- Enable local resource field: on
- Resource grid columns: `10`
- Resource grid rows: `7`
- Local capture limit: `1.0`

Keep evolved sensing/movement off for this isolated test. The resource layer should be visible and no resource cell may become negative. `local_resource_balance_error` must remain within the documented `1e-7` tolerance.

## 8. Sensing and movement check

Then enable:

- Enable evolved sensing/movement: on
- Maximum movement per instruction: `1.0`
- Movement energy cost per unit: `0.1`

The Phase Two mutation alphabet can now contain `SENSE_RESOURCE`, `MOVE_X`, and `MOVE_Y`. Movement remains bounded by the selected boundary model and realized movement cost is recorded in the energy ledger.

Important: enabling these opcodes does not prescribe intelligence, cooperation, or a target behavior. Organisms may or may not evolve genomes that use them.

## 9. Interface checks

During a Phase Two run verify that you can inspect:

- organism, boundary, and resource visibility layers;
- selectable time-series spatial metrics;
- selected-organism position, local resource, and neighborhood information;
- movement, boundary, resource, birth, and death events;
- exact run configuration and world-contract metadata in saved artifacts.

## 10. Reproduce the Phase Two evidence gate

The accepted evidence campaign uses 30 seeds, 12 conditions, and 2000 ticks per run: 360 runs in total.

From the activated environment:

~~~powershell
melakat-phase-two-evidence --runs 30 --ticks 2000 --seed-start 1 --output-dir results/phase-two/evidence-gate
~~~

For a fast smoke test before the full campaign:

~~~powershell
melakat-phase-two-evidence --runs 2 --ticks 200 --seed-start 1 --output-dir results/phase-two/manual-smoke
~~~

Do not replace the accepted evidence archive with a manual run unless the outputs have been deliberately reviewed and accepted.

## Expected scientific boundaries

Phase Two adds spatial topology, local energy resources, observation and movement primitives, controlled comparisons, measurements, and a research interface. It does not add machine learning, a fitness objective, attack, cooperation, mating roles, parasites, or a host-authored social strategy.
