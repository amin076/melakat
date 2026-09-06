# Melakat Documentation

[فارسی](README.fa.md) | English

This directory contains the canonical project documentation. Major scientific documents are maintained in parallel English and Farsi versions.

## Current research status

**Phase Zero, Phase One, and Phase Two are complete. Phase Two is frozen as an accepted reference. Phase Three has started.**

The accepted Phase One homogeneous evidence archive contains 990 runs. The accepted Phase Two spatial/environment evidence archive contains 360 runs: 30 seeds across 12 matched conditions, each for 2000 ticks, with zero validation failures.

Frozen Phase Two versions:

- world contract: `phase-two-spatial-0.7`
- engine: `phase-two-vm-0.7`
- measurement: `phase-two-measurement-0.1`

Initial Phase Three versions:

- world contract: `phase-three-environment-0.1`
- engine: `phase-three-vm-0.1`
- measurement: `phase-three-measurement-0.1`

The Phase One homogeneous model remains the permanent control. Phase Two remains the frozen spatial/local-resource reference. Phase Three begins by introducing one isolated intervention: deterministic spatial heterogeneity in resource allocation while holding total resource input constant.

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
- [Phase Two frozen baseline — English](phase-2/phase-two-frozen-baseline.md)
- [خط پایهٔ منجمد مرحلهٔ دو — فارسی](phase-2/phase-two-frozen-baseline.fa.md)
- [Phase Three roadmap — English](phase-3/phase-three-roadmap.md)
- [نقشهٔ راه مرحلهٔ سه — فارسی](phase-3/phase-three-roadmap.fa.md)
- [Phase Two user test guide — English](phase-2/phase-two-user-test-guide.md)
- [راهنمای تست کاربر مرحلهٔ دو — فارسی](phase-2/phase-two-user-test-guide.fa.md)

Historical Phase Two contract milestones remain available:

- [World contract 0.1 — English](phase-2/phase-two-world-contract-0.1.md)
- [قرارداد جهان ۰.۱ — فارسی](phase-2/phase-two-world-contract-0.1.fa.md)
- [Spatial topology 0.2 — English](phase-2/phase-two-spatial-topology-0.2.md)
- [توپولوژی فضایی ۰.۲ — فارسی](phase-2/phase-two-spatial-topology-0.2.fa.md)

The frozen Phase Two contract remains implemented in `desktop/src/melakat_desktop/world_contract.py`. The new Phase Three contract is implemented separately in `desktop/src/melakat_desktop/phase_three_contract.py`; this separation is intentional so later work does not silently redefine the accepted Phase Two baseline.

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

Evidence is stored in `results/phase-two/evidence-gate/` with validation, performance, provenance, and SHA-256 checksums. Later Phase Three experiments do not replace this archive.

## Phase Three first gate

The first Phase Three evidence gate will compare a `uniform` control against a deterministic `center_patch` resource distribution while preserving matched seeds, total initial resource, total per-tick resource input, VM rules, mutation, reproduction, memory, topology and local capture semantics.

A difference between the two conditions may support a statement about the effect of spatial resource heterogeneity on recorded model dynamics. It is not by itself evidence of adaptation, cooperation, competition or niche formation.

## Technical documents

- [Desktop lab architecture — English](desktop/desktop-lab-architecture.md)
- [معماری آزمایشگاه دسکتاپ — فارسی](desktop/desktop-lab-architecture.fa.md)
- [Phase Zero VM contract — English](desktop/phase-zero-vm.md)
- [قرارداد ماشین مجازی مرحلهٔ صفر — فارسی](desktop/phase-zero-vm.fa.md)

## Documentation policy

English and Farsi scientific documents are maintained as parallel records. Any change to a rule, measurement contract, experiment protocol, or acceptance criterion must be reflected in both languages or explicitly tracked as documentation follow-up.
