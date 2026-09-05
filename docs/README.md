# Melakat Documentation

[فارسی](README.fa.md) | English

This directory contains the canonical project documentation. Every major document has an English version and a Farsi version.

## Language directories

- [English documentation](doc-english/README.md)
- [Farsi documentation](doc-farsi/README.md)

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
- [Phase Two world contract 0.1 — English](phase-2/phase-two-world-contract-0.1.md)
- [قرارداد جهان مرحلهٔ دو نسخهٔ ۰.۱ — فارسی](phase-2/phase-two-world-contract-0.1.fa.md)
- [Phase Two spatial topology 0.2 — English](phase-2/phase-two-spatial-topology-0.2.md)
- [توپولوژی فضایی مرحلهٔ دو نسخهٔ ۰.۲ — فارسی](phase-2/phase-two-spatial-topology-0.2.fa.md)

## Current research gate

The Phase One implementation gate and scientific evidence gate are complete for the defined homogeneous baseline. The accepted archive contains 990 runs across 30 seeds, six controls, and 27 one-factor sensitivity cases.

Phase Two P2.1 and P2.2 are implemented. P2.2 activates exactly one spatial mechanism: local offspring placement in a continuous two-dimensional rectangular world with a reflective boundary. Spatial randomness is isolated from the historical engine RNG, and acceptance tests require the same-seed non-spatial dynamics to remain identical to the disabled-spatial control.

Movement, sensing, local resources, attack, cooperation, and explicit fitness rewards remain absent. The next scientific package is P2.3: one local-resource mechanism with explicit accounting and comparison against both P2.2 and the Phase One homogeneous control.

## Technical documents

- [Desktop lab architecture — English](desktop/desktop-lab-architecture.md)
- [معماری آزمایشگاه دسکتاپ — فارسی](desktop/desktop-lab-architecture.fa.md)
- [Phase Zero VM contract — English](desktop/phase-zero-vm.md)
- [قرارداد ماشین مجازی مرحلهٔ صفر — فارسی](desktop/phase-zero-vm.fa.md)

## Documentation policy

The English and Farsi documents are maintained as parallel documents. A change to a scientific rule, metric, experiment protocol, or acceptance criterion must be reflected in both language directories.

The Farsi documents use isolated code formatting for technical names and English terms. This keeps mixed-direction text readable in right-to-left prose.
