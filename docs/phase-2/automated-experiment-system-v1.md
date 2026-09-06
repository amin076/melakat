# Automated Experiment System v1

Melakat's desktop GUI is for observation, inspection, and reproducing individual runs. It is not the primary interface for large scientific campaigns. Automated Experiment System v1 provides a headless, reproducible batch runner for multi-condition, multi-seed experiments.

## Goals

The runner is designed to:

- define experiments as versioned JSON or YAML specifications;
- execute matched conditions without opening the desktop GUI;
- run explicit seed sets or contiguous seed ranges;
- expand one- or multi-parameter sweeps;
- validate energy, local-resource, and spatial invariants on every run;
- repeat one exact condition/seed pair to verify determinism;
- aggregate condition-level statistics;
- emit CSV/JSON artifacts with provenance and SHA-256 checksums;
- run small smoke campaigns in CI and larger research campaigns through GitHub Actions.

The runner does not change simulation rules. It only orchestrates existing engines.

## CLI

Install the desktop package, then validate a specification:

```powershell
cd desktop
python -m pip install -e .
cd ..
melakat-experiment validate experiments/phase-two/local-resource-energy-sweep.json
```

Run it:

```powershell
melakat-experiment run experiments/phase-two/local-resource-energy-sweep.json `
  --output-dir results/automated-experiments/local-resource-energy
```

CI-sized overrides can reduce the campaign without editing the scientific specification:

```powershell
melakat-experiment run experiments/phase-two/local-resource-energy-sweep.json `
  --seed-count 3 `
  --ticks 300 `
  --output-dir results/automated-experiments/smoke
```

`--seed-start` can also override the first seed.

## Experiment specification

The current format is:

```text
melakat-experiment-spec-0.1
```

A specification has:

- `name` and optional `description`;
- `base_config`: Melakat parameter overrides;
- `seeds`: either an explicit list or `{start, count}`;
- optional `conditions`: named matched conditions;
- optional `sweeps`: parameter grids expanded into conditions;
- optional `reproducibility`: the exact condition and seed to repeat.

Unknown Melakat parameter names are rejected rather than silently ignored.

JSON is supported without extra packages. YAML uses `PyYAML`, which is included in the normal desktop package dependencies.

## Sweep example

A sweep can vary one parameter:

```json
{
  "name": "local_resource_energy",
  "base_overrides": {
    "world.spatial_enabled": true,
    "world.local_resources_enabled": true,
    "world.organism_actions_enabled": false
  },
  "parameter": "world.energy_input_per_tick",
  "values": [10.4, 20.0, 40.0]
}
```

It can also define a Cartesian product:

```json
{
  "name": "resource_grid",
  "parameters": {
    "world.energy_input_per_tick": [10.4, 20.0],
    "world.local_capture_limit": [0.5, 1.0]
  }
}
```

## Output contract

Each completed campaign writes:

- `campaign.json` — resolved plan, compact per-run records, summary and validation;
- `runs.csv` — one row per run;
- `summary.json` — per-condition aggregate statistics and deltas from the first condition;
- `comparison.csv` — condition-level aggregate table;
- `validation.json` — invariant and reproducibility results;
- `provenance.json` — Python/platform/spec hash and GitHub metadata when available;
- `SHA256SUMS.txt` — checksums for all campaign outputs.

A campaign exits with a non-zero status if an invariant fails, a run raises an execution error, an expected run is missing, or the deterministic repeat does not match.

## Validation

Every run checks:

- global energy-balance error against the existing Phase Two tolerance;
- local-resource balance when local resources are enabled;
- absence of negative local-resource cells;
- final organism coordinates remain within world bounds when spatial rules are enabled.

One exact condition/seed pair is then run again and its full summary checksum must match.

## GitHub Actions

`.github/workflows/melakat-experiments.yml` has two modes:

1. **PR/main smoke** — 3 seeds × 300 ticks using the committed Phase Two energy sweep. This catches orchestration and regression failures quickly.
2. **Manual research campaign** — `workflow_dispatch` accepts a spec path, seed count and tick count. The default is 30 seeds × 2000 ticks.

Artifacts are uploaded to the workflow run instead of being committed automatically to `main`.

## First committed campaign

`experiments/phase-two/local-resource-energy-sweep.json` encodes the manual Phase Two local-resource experiment that motivated this system:

- spatial rules: on;
- local resources: on;
- evolved sensing/movement: off;
- resource grid: 10 × 7;
- world: 96 × 70;
- offspring dispersion radius: 1.4;
- energy input per tick: 10.4, 20.0, 40.0;
- seeds: 1–30;
- ticks: 2000.

The full specification therefore contains 90 runs. Its purpose is to measure how local energy renewal changes survival and turnover without introducing movement as a confound.

## Role of Keynu

This runner is intentionally the stable scientific boundary for future Keynu integration. A `MelakatDriver` should call this CLI and consume its artifacts rather than automating mouse clicks in the GUI. That keeps Melakat's repository, experiment specifications, and result artifacts as the scientific source of truth.
