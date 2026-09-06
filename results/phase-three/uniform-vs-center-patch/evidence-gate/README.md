# Phase Three evidence gate — uniform vs center patch

Status: **ACCEPTED**

This directory preserves the repository-side evidence record for the first full Phase Three matched-seed campaign.

Experiment:

- specification: `experiments/phase-three/uniform-vs-center-patch.json`
- 30 matched seeds
- 2 conditions: `uniform-control` and `center-patch`
- 2000 ticks per run
- 60 total runs
- validation failures: 0
- deterministic repeat: PASS

Repository-preserved evidence:

- `validation.json` — acceptance gate and reproducibility result;
- `summary.json` — condition aggregates and direct condition deltas;
- `provenance.json` — workflow/runtime/source provenance;
- `SHA256SUMS.txt` — checksum manifest produced with the original workflow artifact;
- `paired-results.csv` — seed-matched values and patch-minus-uniform deltas for the primary analysis metrics;
- `paired-analysis.json` — derived paired means, medians, descriptive 95% intervals, and seed-direction counts.

The original GitHub Actions artifact also contains the full `campaign.json`, original `runs.csv`, and `comparison.csv`. It was produced by workflow run `34062567737`, artifact id `9997969944`, with artifact digest:

`sha256:402dabae1b7f39d600ce26e3027ff2769ec8b37e94b707d38a8a13ba42121e70`

The `SHA256SUMS.txt` file is the manifest of that original complete workflow output; therefore it lists files that are not all duplicated in this repository directory. The source commit, experiment specification, provenance and checksums are retained so the full campaign can be regenerated and verified.

Scientific interpretation is documented in `docs/phase-3/phase-three-uniform-vs-center-patch-report.md`.
