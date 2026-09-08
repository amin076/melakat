# مستندات ملاکت

[English](README.md)

این پوشه مستندات canonical علمی و فنی ملاکت را نگهداری می‌کند. اسناد پژوهشی اصلی به‌صورت موازی فارسی و انگلیسی نگهداری می‌شوند.

## وضعیت پژوهشی فعلی

**Phase Zero تا Phase Five کامل شده‌اند.** Phase Two همچنان مرجع رسمی frozen برای فضای دوبعدی و local resource است. مراحل بعدی با contractهای versioned مستقل و evidence archiveهای جداگانه توسعه یافته‌اند.

جدیدترین milestone پذیرفته‌شده **Phase Five genome evolvability** است: self-replication مقاوم به تغییر طول همراه با single-instruction tandem duplication/deletion کور، genomeهای variable-length وراثتی را تحت هزینه‌های محدود energy/memory ایجاد کرد. Full campaign شامل ۶۰ run اصلی، صفر validation failure و deterministic replay موفق بود. organismهای variable-length متولد شدند و تعدادی از آنها خودشان بعداً reproduction کردند. این evidence برای structural evolvability است، نه برای افزایش complexity یا open-ended evolution.

## اسناد اصلی مراحل

### Phase Zero / One

- [نتایج مرحلهٔ صفر — فارسی](doc-farsi/phase-zero-results.md)
- [Phase Zero results — English](doc-english/phase-zero-results.md)
- [نقشهٔ راه مرحلهٔ یک — فارسی](doc-farsi/phase-one-roadmap.md)
- [Phase One roadmap — English](doc-english/phase-one-roadmap.md)
- [گزارش شواهد مرحلهٔ یک — فارسی](doc-farsi/phase-one-evidence-report.md)
- [Phase One evidence report — English](doc-english/phase-one-evidence-report.md)

### Phase Two

- [نقشهٔ راه مرحلهٔ دو — فارسی](doc-farsi/phase-two-roadmap.md)
- [Phase Two roadmap — English](doc-english/phase-two-roadmap.md)
- [گزارش تکمیل مرحلهٔ دو — فارسی](phase-2/phase-two-completion-report.fa.md)
- [Phase Two completion report — English](phase-2/phase-two-completion-report.md)
- [خط پایهٔ منجمد مرحلهٔ دو — فارسی](phase-2/phase-two-frozen-baseline.fa.md)
- [Phase Two frozen baseline — English](phase-2/phase-two-frozen-baseline.md)
- [راهنمای تست کاربر مرحلهٔ دو — فارسی](phase-2/phase-two-user-test-guide.fa.md)
- [Phase Two user test guide — English](phase-2/phase-two-user-test-guide.md)

### Phase Three

- [نقشهٔ راه مرحلهٔ سه — فارسی](phase-3/phase-three-roadmap.fa.md)
- [Phase Three roadmap — English](phase-3/phase-three-roadmap.md)

### Phase Four

- [گیت ثبت‌شدهٔ sensing/movement مرحلهٔ چهار — فارسی](phase-4/phase-four-sensing-movement-gate.fa.md)
- [Phase Four pre-registered sensing/movement gate — English](phase-4/phase-four-sensing-movement-gate.md)
- [گزارش preflight مرحلهٔ چهار — فارسی](phase-4/phase-four-sensing-movement-preflight-report.fa.md)
- [Phase Four preflight report — English](phase-4/phase-four-sensing-movement-preflight-report.md)
- [گزارش تکمیل مرحلهٔ چهار — فارسی](phase-4/phase-four-completion-report.fa.md)
- [Phase Four completion report — English](phase-4/phase-four-completion-report.md)

### Phase Five

- [نقشهٔ راه evolvability مرحلهٔ پنج — فارسی](phase-5/phase-five-evolvability-roadmap.fa.md)
- [Phase Five evolvability roadmap — English](phase-5/phase-five-evolvability-roadmap.md)
- [گزارش تکمیل مرحلهٔ پنج — فارسی](phase-5/phase-five-completion-report.fa.md)
- [Phase Five completion report — English](phase-5/phase-five-completion-report.md)

## Evidence archiveهای پذیرفته‌شده

- `results/phase-one/evidence-gate/` — evidence جهان همگن Phase One
- `results/phase-two/evidence-gate/` — evidence frozen Phase Two
- `results/phase-four/resource-sensing-with-movement/full/` — full causal evidence Phase Four
- `results/phase-five/structural-event-rate-calibration/` — exposure-only calibration مرحلهٔ پنج
- `results/phase-five/variable-genome-full/` — full matched-seed evidence مرحلهٔ پنج

## خلاصهٔ evidence مرحلهٔ پنج

Gate 5C نرخ `mutation.structural_event_rate = 0.025` را به‌عنوان کمترین candidate پاس‌کنندهٔ threshold از پیش ثبت‌شدهٔ exposure انتخاب کرد.

Gate 5D سپس ۳۰ seed matched × ۲ condition × ۲۰۰۰ tick اجرا کرد:

- `60/60` run اصلی کامل؛
- validation failure برابر `0`؛
- deterministic replay برابر PASS؛
- بیشترین خطای مطلق energy برابر `4.36e-08` زیر tolerance `1e-07`؛
- structural event در control برابر `0`؛
- structural event در treatment برابر `97` شامل `42` duplication و `55` deletion؛
- variable-length birth برابر `61`؛
- organismهای variable-length که بعداً reproduction کردند برابر `12`.

طول ancestor برابر ۱۴ است. genomeهای فعال control همگی ۱۴ باقی ماندند؛ treatment طول‌های فعال ۱۳ تا ۱۵ ایجاد کرد. میانگین طول تقریباً ۱۴ باقی ماند. بنابراین Phase Five یک dimension وراثتی برای طول genome ایجاد کرده، بدون اینکه رشد یک‌طرفهٔ genome یا افزایش complexity را ثابت کند.

## اسناد فنی

- [معماری آزمایشگاه دسکتاپ — فارسی](desktop/desktop-lab-architecture.fa.md)
- [Desktop lab architecture — English](desktop/desktop-lab-architecture.md)
- [قرارداد ماشین مجازی مرحلهٔ صفر — فارسی](desktop/phase-zero-vm.fa.md)
- [Phase Zero VM contract — English](desktop/phase-zero-vm.md)

## سیاست مستندسازی

اسناد علمی فارسی و انگلیسی به‌صورت موازی نگهداری می‌شوند. هر تغییر در قانون علمی، measurement contract، experiment protocol، acceptance criterion یا مرز ادعا باید در هر دو زبان ثبت شود یا صریحاً به‌عنوان follow-up مستندسازی شود.
