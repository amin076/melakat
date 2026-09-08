# مستندات ملاکت

[English](README.md)

این پوشه مستندات canonical پروژه را نگهداری می‌کند. اسناد علمی مهم به‌صورت موازی در نسخه‌های فارسی و انگلیسی نگهداری می‌شوند.

## وضعیت پژوهشی فعلی

**مرحلهٔ صفر، مرحلهٔ یک و مرحلهٔ دو کامل شده‌اند. مرحلهٔ دو به‌عنوان مرجع پذیرفته‌شدهٔ spatial/local-resource منجمد است. زنجیرهٔ mechanism/evidence مرحلهٔ سه برای محیط، sensing و movement و نیز evidence gate مرحلهٔ چهار برای sensing در حضور movement کامل شده‌اند.**

Evidence تاریخی پذیرفته‌شده:

- مرحلهٔ یک: ۹۹۰ اجرای جهان همگن؛
- مرحلهٔ دو: ۳۶۰ اجرای spatial/environment؛
- مرحلهٔ سه: کارزار کامل ناهمگنی resource، sensing-only، movement-only، movement-step و evidence اصلاح‌شدهٔ atomic movement؛
- مرحلهٔ چهار: smoke ثبت‌شده، preflight تمام‌مدت و full campaign کامل با ۳۰ seed matched × ۲ condition × `2000 tick`.

نسخه‌های منجمد مرحلهٔ دو:

- قرارداد جهان: `phase-two-spatial-0.7`؛
- موتور: `phase-two-vm-0.7`؛
- اندازه‌گیری: `phase-two-measurement-0.1`.

نسخه‌های execution evidence استفاده‌شده در مرحلهٔ چهار:

- قرارداد جهان: `phase-three-environment-0.1`؛
- موتور: `phase-three-vm-0.3`؛
- اندازه‌گیری: `phase-three-measurement-0.3`.

مدل همگن مرحلهٔ یک کنترل دائمی باقی می‌ماند. مرحلهٔ دو مرجع منجمد فضا و resource محلی است. Evidenceهای بعدی به‌صورت versioned نگهداری می‌شوند و baselineهای پذیرفته‌شده را جایگزین نمی‌کنند.

## اسناد اصلی

- [نتایج مرحلهٔ صفر — فارسی](doc-farsi/phase-zero-results.md)
- [Phase Zero results — English](doc-english/phase-zero-results.md)
- [نقشهٔ راه مرحلهٔ یک — فارسی](doc-farsi/phase-one-roadmap.md)
- [Phase One roadmap — English](doc-english/phase-one-roadmap.md)
- [گزارش شواهد مرحلهٔ یک — فارسی](doc-farsi/phase-one-evidence-report.md)
- [Phase One evidence report — English](doc-english/phase-one-evidence-report.md)
- [آرشیو شواهد مرحلهٔ یک](../results/phase-one/evidence-gate/README.fa.md)
- [نقشهٔ راه مرحلهٔ دو — فارسی](doc-farsi/phase-two-roadmap.md)
- [Phase Two roadmap — English](doc-english/phase-two-roadmap.md)
- [گزارش تکمیل و شواهد مرحلهٔ دو — فارسی](phase-2/phase-two-completion-report.fa.md)
- [Phase Two completion and evidence report — English](phase-2/phase-two-completion-report.md)
- [خط پایهٔ منجمد مرحلهٔ دو — فارسی](phase-2/phase-two-frozen-baseline.fa.md)
- [Phase Two frozen baseline — English](phase-2/phase-two-frozen-baseline.md)
- [نقشهٔ راه مرحلهٔ سه — فارسی](phase-3/phase-three-roadmap.fa.md)
- [Phase Three roadmap — English](phase-3/phase-three-roadmap.md)
- [گیت sensing/movement مرحلهٔ چهار — فارسی](phase-4/phase-four-sensing-movement-gate.fa.md)
- [Phase Four pre-registered sensing/movement gate — English](phase-4/phase-four-sensing-movement-gate.md)
- [گزارش preflight مرحلهٔ چهار — فارسی](phase-4/phase-four-sensing-movement-preflight-report.fa.md)
- [Phase Four full-duration preflight report — English](phase-4/phase-four-sensing-movement-preflight-report.md)
- [گزارش تکمیل مرحلهٔ چهار — فارسی](phase-4/phase-four-completion-report.fa.md)
- [Phase Four completion report — English](phase-4/phase-four-completion-report.md)
- [راهنمای تست کاربر مرحلهٔ دو — فارسی](phase-2/phase-two-user-test-guide.fa.md)
- [Phase Two user test guide — English](phase-2/phase-two-user-test-guide.md)

اسناد تاریخی قرارداد مرحلهٔ دو نیز حفظ شده‌اند:

- [قرارداد جهان ۰.۱ — فارسی](phase-2/phase-two-world-contract-0.1.fa.md)
- [World contract 0.1 — English](phase-2/phase-two-world-contract-0.1.md)
- [توپولوژی فضایی ۰.۲ — فارسی](phase-2/phase-two-spatial-topology-0.2.fa.md)
- [Spatial topology 0.2 — English](phase-2/phase-two-spatial-topology-0.2.md)

## خلاصهٔ evidence پذیرفته‌شده

### مرحلهٔ یک

آرشیو پذیرفته‌شدهٔ مرحلهٔ یک شامل ۹۹۰ اجراست و baseline همگن باقی می‌ماند.

### مرحلهٔ دو

گیت نهایی مرحلهٔ دو ثبت می‌کند:

- ۱۲ condition؛
- ۳۰ seed در هر condition؛
- ۳۶۰ اجرای کامل؛
- صفر شکست validation؛
- بیشترین خطای مطلق energy balance برابر `1.02e-08` زیر tolerance `1e-07`؛
- بیشترین خطای مطلق local-resource برابر `4.2e-09` زیر tolerance `1e-07`؛
- deterministic repeat: PASS؛
- source commit: `ad5e21159baf0d6bd79a028799b9318ba144fed7`؛
- workflow run: `33969619473`.

Evidence در `results/phase-two/evidence-gate/` نگهداری می‌شود.

### مرحلهٔ چهار

Full campaign تکمیل‌شدهٔ مرحلهٔ چهار ثبت می‌کند:

- ۳۰ seed matched × ۲ condition × `2000 tick` = ۶۰ اجرای اصلی؛
- شکست validation: `0`؛
- deterministic replay: PASS؛
- sensing operation در control: `0`؛
- sensing operation در treatment: `508`؛
- runهای treatment دارای sensing: `15/30`؛
- runهای treatment دارای sensing + movement غیرصفر: `7/30`؛
- هیچ realized movement کم‌پرداخت‌شده‌ای وجود ندارد؛
- بیشترین خطای مطلق energy balance: `4.8e-09`؛
- بیشترین خطای مطلق local-resource: `6.3e-09`.

تمام intervalهای paired ثبت‌شدهٔ movement execution صفر را شامل کردند. سه outcome ثبت‌شدهٔ spatial/resource صفر را شامل نکردند: `mean_local_neighbors` کاهش یافت، `mean_nearest_neighbor_distance` افزایش یافت و `local_resource_total` در treatment بیشتر بود. یک endpoint ثانویهٔ `active_population` نیز در treatment کمتر بود.

تفسیر پذیرفته‌شده این است که sensing اسکالر محلی downstream ecological/spatial state را در این مدل به‌طور causal تغییر داد و نتیجه با `resource-conditioned dynamics` سازگار است. این campaign اثر حل‌شده‌ای بر locomotor execution نشان نداد و navigation جهت‌دار، resource seeking، adaptation، fitness advantage یا intelligence را اثبات نمی‌کند.

آرشیو canonical مرحلهٔ چهار:

`results/phase-four/resource-sensing-with-movement/full/`

## اسناد فنی

- [معماری آزمایشگاه دسکتاپ — فارسی](desktop/desktop-lab-architecture.fa.md)
- [Desktop lab architecture — English](desktop/desktop-lab-architecture.md)
- [قرارداد ماشین مجازی مرحلهٔ صفر — فارسی](desktop/phase-zero-vm.fa.md)
- [Phase Zero VM contract — English](desktop/phase-zero-vm.md)

## سیاست نگهداری مستندات

اسناد علمی فارسی و انگلیسی به‌صورت موازی نگهداری می‌شوند. هر تغییر در rule، measurement contract، experiment protocol یا acceptance criterion باید در هر دو زبان منعکس شود یا صریحاً به‌عنوان documentation follow-up ثبت شود.
