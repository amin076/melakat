# Phase One Evidence Archive

[فارسی](README.fa.md) | [Scientific report](../../../docs/doc-english/phase-one-evidence-report.md)

This directory is the accepted Phase One homogeneous-baseline evidence archive.

## Campaign

- engine: <code>phase-zero-vm-0.2</code>
- measurement: <code>phase-one-measurement-0.1</code>
- evidence format: <code>melakat-phase-one-evidence-0.1</code>
- base configuration hash: <code>b90c2df4f218b285</code>
- seeds: <code>1–30</code>
- ticks per condition: <code>2000</code>
- controls: <code>6</code>
- sensitivity parameters: <code>9</code>
- sensitivity cases: <code>27</code>
- archived runs: <code>990</code>

The gate passed with zero energy, memory, seed-coverage, run-count, configuration-hash, result-checksum, and tick-count failures. The largest absolute energy-balance error was <code>2.5e-08</code>, below the <code>1e-07</code> tolerance.

## Files

- <code>base-config.json</code> — exact baseline configuration;
- <code>campaign.json</code> — controls, sensitivity cases, aggregates, compact per-run records, protocol, and validation;
- <code>runs.csv</code> — flat per-run table for analysis;
- <code>validation.json</code> — primary automated evidence-gate result;
- <code>SHA256SUMS.txt</code> — checksums for the original generated archive files.

Each compact run record contains a SHA-256 checksum of the complete enriched result generated before compaction. The complete result checksum covers history, genealogy, genotype catalog, and analysis, enabling a detailed rerun to be compared with the archived record.

The two README files in this directory were added after the generated campaign and are therefore intentionally not listed in the original <code>SHA256SUMS.txt</code> manifest.

## Reproduction

The full campaign is intentionally not run on every push. Use the manually dispatched <code>Phase One evidence campaign</code> GitHub Actions workflow when the versioned Phase One baseline needs to be regenerated deliberately.

Any regenerated campaign must be compared with this archive before replacing the accepted baseline.
