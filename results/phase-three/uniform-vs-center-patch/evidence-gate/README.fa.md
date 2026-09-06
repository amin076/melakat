# گیت شواهد مرحلهٔ سه — منابع یکنواخت در برابر لکهٔ مرکزی

وضعیت: **پذیرفته‌شده**

این پوشه رکورد repository-side نخستین کارزار کامل مرحلهٔ سه با `seed`های تطبیقی را حفظ می‌کند.

آزمایش:

- مشخصات: `experiments/phase-three/uniform-vs-center-patch.json`
- ۳۰ `seed` تطبیقی
- ۲ وضعیت: `uniform-control` و `center-patch`
- `2000 tick` برای هر اجرا
- ۶۰ اجرای کل
- شکست validation: ۰
- تکرار قطعی: PASS

شواهد حفظ‌شده در repository:

- `validation.json` — گیت پذیرش و نتیجهٔ reproducibility؛
- `summary.json` — aggregateهای دو وضعیت و اختلاف مستقیم آن‌ها؛
- `provenance.json` — provenance مربوط به workflow، runtime و source؛
- `SHA256SUMS.txt` — manifest checksum تولیدشده همراه artifact اصلی workflow؛
- `paired-results.csv` — مقادیر تطبیقی seed-به-seed و اختلاف patch منهای uniform برای معیارهای اصلی تحلیل؛
- `paired-analysis.json` — میانگین‌ها، medianها، بازه‌های توصیفی ۹۵٪ و شمارش جهت اختلاف میان seedها.

artifact اصلی GitHub Actions همچنین `campaign.json` کامل، `runs.csv` اصلی و `comparison.csv` را دارد. این artifact در workflow run شمارهٔ `34062567737` با artifact id برابر `9997969944` ساخته شد و digest آن این است:

`sha256:402dabae1b7f39d600ce26e3027ff2769ec8b37e94b707d38a8a13ba42121e70`

فایل `SHA256SUMS.txt` manifest خروجی کامل و اصلی همان workflow است؛ بنابراین نام فایل‌هایی را هم شامل می‌شود که همگی در این پوشه دوباره کپی نشده‌اند. commit منبع، specification آزمایش، provenance و checksumها نگهداری شده‌اند تا کارزار کامل دوباره تولید و verify شود.

تفسیر علمی در `docs/phase-3/phase-three-uniform-vs-center-patch-report.fa.md` ثبت شده است.
