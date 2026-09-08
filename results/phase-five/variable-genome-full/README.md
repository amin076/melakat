# Phase Five Full Variable-Genome Evidence Archive

This directory is the accepted Gate 5D evidence archive for Phase Five.

## Experiment

`phase-five-variable-genome-full`

- 30 matched seeds per condition
- 2 conditions
- 2000 ticks per run
- 60 primary runs
- control: structural event rate `0.0`
- treatment: exposure-calibrated structural event rate `0.025`
- duplication probability `0.5`
- all other Phase Five substrate, mutation, resource, memory, execution and reproduction parameters matched

## Integrity

- completed: `60/60`
- validation failures: `0`
- deterministic replay: PASS
- maximum absolute energy-balance error: `4.36e-08` under tolerance `1e-07`
- control structural events: `0`
- treatment structural events: `97`
- treatment duplications: `42`
- treatment deletions: `55`

## Heredity gate

- variable-length births: `61`
- variable-length organisms that later reproduced: `12`
- treatment runs ending with active variable-length organisms: `14/30`

The heredity gate therefore passed: variable genome length was not merely generated; some length variants themselves reproduced.

## Scientific boundary

This archive supports **heritable variable genome length / structural evolvability** in the implemented model. It does not support a claim of increased complexity, adaptation, intelligence, or open-ended evolution. Genome length is not treated as a complexity metric.

## Files

- `campaign.json` — expanded campaign plus all run summaries
- `runs.csv` — tabular run summaries
- `summary.json` — condition aggregates
- `comparison.csv` — baseline deltas
- `validation.json` — invariant/replay validation
- `provenance.json` — source/workflow provenance
- `paired-analysis.json` — matched-seed endpoint analysis
- `campaign-verification.json` — Phase Five-specific integrity/heredity checks
- `merge-readiness.json` — final evidence acceptance gate
- `SHA256SUMS.txt` — checksum manifest

See `docs/phase-5/phase-five-completion-report.md` for the scientific interpretation.
