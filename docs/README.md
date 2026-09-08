# Melakat Documentation

[فارسی](README.fa.md) | English

This directory contains the canonical scientific and technical documentation for Melakat. Major research records are maintained in parallel English/Farsi versions.

## Current research status

**Phases Zero through Five are complete.** Phase Two remains a formally frozen spatial/local-resource reference. Later phases use separate versioned contracts and evidence archives.

The newest accepted milestone is **Phase Five genome evolvability**: length-robust self-replication plus blind single-instruction tandem duplication/deletion produced heritable variable genome lengths under finite energy/memory costs. The accepted full campaign contains 60 primary runs with zero validation failures and deterministic replay PASS. Variable-length organisms were born and some later reproduced. This is structural evolvability evidence, not evidence of increasing complexity or open-ended evolution.

## Core phase documents

### Phase Zero / One

- [Phase Zero results — English](doc-english/phase-zero-results.md)
- [نتایج مرحلهٔ صفر — فارسی](doc-farsi/phase-zero-results.md)
- [Phase One roadmap — English](doc-english/phase-one-roadmap.md)
- [نقشهٔ راه مرحلهٔ یک — فارسی](doc-farsi/phase-one-roadmap.md)
- [Phase One evidence report — English](doc-english/phase-one-evidence-report.md)
- [گزارش شواهد مرحلهٔ یک — فارسی](doc-farsi/phase-one-evidence-report.md)

### Phase Two

- [Phase Two roadmap — English](doc-english/phase-two-roadmap.md)
- [نقشهٔ راه مرحلهٔ دو — فارسی](doc-farsi/phase-two-roadmap.md)
- [Phase Two completion report — English](phase-2/phase-two-completion-report.md)
- [گزارش تکمیل مرحلهٔ دو — فارسی](phase-2/phase-two-completion-report.fa.md)
- [Phase Two frozen baseline — English](phase-2/phase-two-frozen-baseline.md)
- [خط پایهٔ منجمد مرحلهٔ دو — فارسی](phase-2/phase-two-frozen-baseline.fa.md)
- [Phase Two user test guide — English](phase-2/phase-two-user-test-guide.md)
- [راهنمای تست کاربر مرحلهٔ دو — فارسی](phase-2/phase-two-user-test-guide.fa.md)

### Phase Three

- [Phase Three roadmap — English](phase-3/phase-three-roadmap.md)
- [نقشهٔ راه مرحلهٔ سه — فارسی](phase-3/phase-three-roadmap.fa.md)

### Phase Four

- [Phase Four pre-registered sensing/movement gate — English](phase-4/phase-four-sensing-movement-gate.md)
- [گیت ثبت‌شدهٔ sensing/movement مرحلهٔ چهار — فارسی](phase-4/phase-four-sensing-movement-gate.fa.md)
- [Phase Four preflight report — English](phase-4/phase-four-sensing-movement-preflight-report.md)
- [گزارش preflight مرحلهٔ چهار — فارسی](phase-4/phase-four-sensing-movement-preflight-report.fa.md)
- [Phase Four completion report — English](phase-4/phase-four-completion-report.md)
- [گزارش تکمیل مرحلهٔ چهار — فارسی](phase-4/phase-four-completion-report.fa.md)

### Phase Five

- [Phase Five evolvability roadmap — English](phase-5/phase-five-evolvability-roadmap.md)
- [نقشهٔ راه evolvability مرحلهٔ پنج — فارسی](phase-5/phase-five-evolvability-roadmap.fa.md)
- [Phase Five completion report — English](phase-5/phase-five-completion-report.md)
- [گزارش تکمیل مرحلهٔ پنج — فارسی](phase-5/phase-five-completion-report.fa.md)

## Accepted evidence archives

- `results/phase-one/evidence-gate/` — Phase One homogeneous evidence
- `results/phase-two/evidence-gate/` — frozen Phase Two evidence
- `results/phase-four/resource-sensing-with-movement/full/` — Phase Four full causal evidence
- `results/phase-five/structural-event-rate-calibration/` — Phase Five exposure-only calibration
- `results/phase-five/variable-genome-full/` — Phase Five full matched-seed evidence

## Phase Five evidence summary

Gate 5C selected `mutation.structural_event_rate = 0.025` as the lowest candidate passing the pre-registered exposure-only threshold.

Gate 5D then ran 30 matched seeds × 2 conditions × 2000 ticks:

- `60/60` primary runs completed;
- validation failures `0`;
- deterministic replay PASS;
- maximum absolute energy error `4.36e-08` under tolerance `1e-07`;
- control structural events `0`;
- treatment structural events `97` (`42` duplications, `55` deletions);
- variable-length births `61`;
- variable-length organisms that later reproduced `12`.

The ancestor length is 14. Control active genomes remained length 14; treatment generated active lengths 13–15. Mean length stayed approximately 14. Thus Phase Five establishes a heritable genome-length dimension without demonstrating monotonic genome expansion or increased complexity.

## Technical architecture documents

- [Desktop lab architecture — English](desktop/desktop-lab-architecture.md)
- [معماری آزمایشگاه دسکتاپ — فارسی](desktop/desktop-lab-architecture.fa.md)
- [Phase Zero VM contract — English](desktop/phase-zero-vm.md)
- [قرارداد ماشین مجازی مرحلهٔ صفر — فارسی](desktop/phase-zero-vm.fa.md)

## Documentation policy

English and Farsi scientific documents are maintained as parallel records. A change to a scientific rule, measurement contract, experiment protocol, acceptance criterion, or claim boundary must be documented in both languages or explicitly tracked as follow-up work.
