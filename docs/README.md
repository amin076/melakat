# Melakat Documentation

[فارسی](README.fa.md) | English

This directory contains the canonical project documentation. Major scientific documents are maintained in parallel English and Farsi versions.

## Current research status

**Phase Zero, Phase One, and Phase Two are complete for their defined gates.**

The accepted Phase One homogeneous evidence archive contains 990 runs. The accepted Phase Two spatial/environment evidence archive contains 360 runs: 30 seeds across 12 matched conditions, each for 2000 ticks, with zero validation failures.

Current accepted Phase Two versions:

- world contract: `phase-two-spatial-0.7`
- engine: `phase-two-vm-0.7`
- measurement: `phase-two-measurement-0.1`

The Phase One homogeneous model remains the permanent control. Phase Two adds controlled topology, a conservative local resource mechanism, data-only sensing/movement primitives, spatial measurements, a controlled evidence matrix, and a desktop research interface. It does not add machine learning, fitness objectives, attack, cooperation, mating roles, or host-authored social strategies.

## Core documents

- [Phase Zero results — English](doc-english/phase-zero-results.md)
- [نتایج مرحلهٔ صفر — فارسی](doc-farsi/phase-zero-results.md)
- [Phase One roadmap — English](doc-english/phase-one-roadmap.md)
- [نقشهٔ راه مرحلهٔ یک — فارسی](doc-farsi/phase-one-roadmap.md)
- [Phase One evidence report — English](doc-english/phase-one-evidence-report.md)
- [گزارش شواهد مرحلهٔ یک — فارسی](doc-farsi/phase-one-evidence-report.md)
- [Phase One evidence archive](../results/phase-one/evidence-gate/README.md)
- [Phase Two roadmap — English](doc-english/phase-two-roadmap.md)
- [نقشهٔ راه مرحلهٔ دو — فارسی](doc-farsi/phase-two-roadmap.md)
- [Phase Two completion and evidence report — English](phase-2/phase-two-completion-report.md)
- [گزارش تکمیل و شواهد مرحلهٔ دو — فارسی](phase-2/phase-two-completion-report.fa.md)
- [Phase Two user test guide — English](phase-2/phase-two-user-test-guide.md)
- [راهنمای تست کاربر مرحلهٔ دو — فارسی](phase-2/phase-two-user-test-guide.fa.md)

Historical Phase Two contract milestones remain available:

- [World contract 0.1 — English](phase-2/phase-two-world-contract-0.1.md)
- [قرارداد جهان ۰.۱ — فارسی](phase-2/phase-two-world-contract-0.1.fa.md)
- [Spatial topology 0.2 — English](phase-2/phase-two-spatial-topology-0.2.md)
- [توپولوژی فضایی ۰.۲ — فارسی](phase-2/phase-two-spatial-topology-0.2.fa.md)

The authoritative current contract is implemented in `desktop/src/melakat_desktop/world_contract.py` and summarized in the Phase Two completion report.

## Accepted Phase Two evidence

The final Phase Two evidence gate records:

- 12 conditions;
- 30 seeds per condition;
- 360 completed runs;
- zero validation failures;
- maximum absolute energy-balance error `1.02e-08` under tolerance `1e-07`;
- maximum absolute local-resource error `4.2e-09` under tolerance `1e-07`;
- deterministic repeat PASS;
- source commit `ad5e21159baf0d6bd79a028799b9318ba144fed7`;
- workflow run `33969619473`.

Evidence is stored in `results/phase-two/evidence-gate/` with validation, performance, provenance, and SHA-256 checksums.

## Technical documents

- [Desktop lab architecture — English](desktop/desktop-lab-architecture.md)
- [معماری آزمایشگاه دسکتاپ — فارسی](desktop/desktop-lab-architecture.fa.md)
- [Phase Zero VM contract — English](desktop/phase-zero-vm.md)
- [قرارداد ماشین مجازی مرحلهٔ صفر — فارسی](desktop/phase-zero-vm.fa.md)

## Documentation policy

English and Farsi scientific documents are maintained as parallel records. Any change to a rule, measurement contract, experiment protocol, or acceptance criterion must be reflected in both languages or explicitly tracked as documentation follow-up.
