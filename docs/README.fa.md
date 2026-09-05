# مستندات ملاکت

[English](README.md)

این پوشه مستندات اصلی پروژه را نگهداری می‌کند. اسناد علمی مهم به‌صورت موازی در نسخه‌های فارسی و انگلیسی نگهداری می‌شوند.

## وضعیت پژوهشی فعلی

**مرحلهٔ صفر، مرحلهٔ یک و مرحلهٔ دو برای گیت‌های تعریف‌شدهٔ خود کامل شده‌اند.**

آرشیو پذیرفته‌شدهٔ مرحلهٔ یک شامل ۹۹۰ اجرای جهان همگن است. آرشیو پذیرفته‌شدهٔ مرحلهٔ دو شامل ۳۶۰ اجرای فضایی/محیطی است: ۳۰ `seed` در ۱۲ وضعیت تطبیقی، با `2000 tick` برای هر اجرا و صفر شکست validation.

نسخه‌های پذیرفته‌شدهٔ فعلی مرحلهٔ دو:

- قرارداد جهان: `phase-two-spatial-0.7`
- موتور: `phase-two-vm-0.7`
- اندازه‌گیری: `phase-two-measurement-0.1`

مدل همگن مرحلهٔ یک کنترل دائمی باقی می‌ماند. مرحلهٔ دو توپولوژی کنترل‌شده، یک سازوکار محافظه‌کار منبع محلی، primitiveهای داده‌محور sensing/movement، متریک‌های فضایی، ماتریس آزمایش کنترل‌شده و رابط پژوهشی دسکتاپ را اضافه می‌کند. این مرحله شامل یادگیری ماشین، هدف `fitness`، حمله، همکاری، نقش جفت‌گیری یا استراتژی اجتماعی نوشته‌شده توسط host نیست.

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
- [راهنمای تست کاربر مرحلهٔ دو — فارسی](phase-2/phase-two-user-test-guide.fa.md)
- [Phase Two user test guide — English](phase-2/phase-two-user-test-guide.md)

اسناد تاریخی قرارداد مرحلهٔ دو نیز برای ردیابی تکامل طراحی حفظ شده‌اند:

- [قرارداد جهان ۰.۱ — فارسی](phase-2/phase-two-world-contract-0.1.fa.md)
- [World contract 0.1 — English](phase-2/phase-two-world-contract-0.1.md)
- [توپولوژی فضایی ۰.۲ — فارسی](phase-2/phase-two-spatial-topology-0.2.fa.md)
- [Spatial topology 0.2 — English](phase-2/phase-two-spatial-topology-0.2.md)

قرارداد فعلی authoritative در `desktop/src/melakat_desktop/world_contract.py` پیاده‌سازی شده و در گزارش تکمیل مرحلهٔ دو خلاصه شده است.

## شواهد پذیرفته‌شدهٔ مرحلهٔ دو

گیت نهایی شواهد مرحلهٔ دو ثبت می‌کند:

- ۱۲ وضعیت؛
- ۳۰ `seed` در هر وضعیت؛
- ۳۶۰ اجرای کامل؛
- صفر شکست validation؛
- بیشترین خطای مطلق تراز انرژی `1.02e-08` با تلورانس `1e-07`؛
- بیشترین خطای مطلق منبع محلی `4.2e-09` با تلورانس `1e-07`؛
- تکرار قطعی PASS؛
- commit منبع `ad5e21159baf0d6bd79a028799b9318ba144fed7`؛
- اجرای workflow شمارهٔ `33969619473`.

شواهد در `results/phase-two/evidence-gate/` همراه با validation، performance، provenance و checksumهای SHA-256 ذخیره شده‌اند.

## اسناد فنی

- [معماری آزمایشگاه دسکتاپ — فارسی](desktop/desktop-lab-architecture.fa.md)
- [Desktop lab architecture — English](desktop/desktop-lab-architecture.md)
- [قرارداد ماشین مجازی مرحلهٔ صفر — فارسی](desktop/phase-zero-vm.fa.md)
- [Phase Zero VM contract — English](desktop/phase-zero-vm.md)

## سیاست نگهداری مستندات

اسناد علمی فارسی و انگلیسی به‌صورت موازی نگهداری می‌شوند. هر تغییر در قانون، قرارداد اندازه‌گیری، پروتکل آزمایش یا معیار پذیرش باید در هر دو زبان منعکس شود یا صریحاً به‌عنوان کار مستندسازی بعدی ثبت شود.
