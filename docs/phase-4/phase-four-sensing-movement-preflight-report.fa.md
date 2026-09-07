# مرحلهٔ چهار — گزارش full-duration exposure preflight برای sensing + movement

## وضعیت

**Preflight ساختاری و حسابداری: PASS.**

این گزارش شواهد calibration را پیش از campaign تطبیق‌یافتهٔ ۳۰-seed ثبت می‌کند. این یک تحلیل inferential برای treatment effect نیست.

## چرا preflight اضافه شد؟

Smoke اولیه با ۸ seed و ۸۰۰ tick نشان داد sensing و locomotion هر دو واقعاً کار می‌کنند، اما exposure متمرکز بود: در treatment فقط ۲ run از ۸ run دستور `SENSE_RESOURCE` را اجرا کردند و فقط ۱ run از ۸ run هم‌زمان هم sensing exposure و هم non-zero committed movement داشت.

به‌جای تفسیر این smoke کم‌exposure یا اجرای مستقیم campaign کامل ۶۰-run، همان هشت seed تطبیق‌یافتهٔ نخست را با مدت کامل campaign یعنی ۲۰۰۰ tick اجرا کردیم. بقیهٔ configuration با specification ثبت‌شدهٔ campaign کامل یکسان است.

## نتایج exposure در مدت کامل

برای ۸ seed تطبیق‌یافته در هر condition:

| Diagnostic | Control | Treatment |
| --- | ---: | ---: |
| `resource_sense_operations` | 0 | 139 |
| runهای دارای sensing exposure | 0 / 8 | 6 / 8 |
| runهای دارای non-zero committed movement | 4 / 8 | 4 / 8 |
| runهای دارای sensing و non-zero movement هم‌زمان | n/a | 2 / 8 |
| non-zero committed movement operations | 35 | 34 |
| committed movement distance | 35.0 | 34.0 |
| movement energy cost | 3.5 | 3.4 |
| uncommitted movement distance | 0.0 | 0.0 |

افزایش مدت اجرا از ۸۰۰ به ۲۰۰۰ tick باعث شد sensing exposure در treatment از ۲/۸ run به ۶/۸ run افزایش یابد و joint exposure برای sensing + non-zero movement از ۱/۸ به ۲/۸ run برسد. با این حال joint exposure هنوز محدود است.

## حسابداری و reproducibility

- campaign validation: PASS
- reproducibility replay: identical
- بیشینهٔ absolute energy balance error: `4.8e-09`
- بیشینهٔ absolute local-resource balance error: `6.3e-09`
- هیچ realized movement کمتر از هزینهٔ لازم پرداخت نشده است
- هیچ uncommitted movement distance ثبت نشده است

## تفسیر علمی

این preflight نشان می‌دهد سازوکار علّی موردنظر در مدت کامل واقعاً exposure دارد و sensing نسبت به smoke کوتاه بسیار بیشتر اجرا می‌شود. اما این داده **اثبات نمی‌کند** که sensing باعث اختلاف یک واحدی فاصلهٔ حرکت aggregate بین control و treatment شده است، و هیچ اختلاف ecological یا spatial را نیز نباید از این preflight به‌عنوان treatment effect تفسیر کرد. این اعداد فقط خروجی‌های توصیفی calibration هستند.

از آنجا که sensor فقط مقدار scalar از resource در مکان فعلی را می‌دهد، حتی اگر campaign بعدی یک treatment effect آماری resolve کند، عبارت علمی مجاز **resource-conditioned behavior** است، نه directional navigation یا resource seeking.

## تصمیم promotion

پس از مشاهدهٔ smoke هیچ numerical threshold دلخواهی برای promotion اختراع نشده است. preflight مدت کامل به‌عنوان شواهد توصیفی exposure نگهداری می‌شود. campaign ثبت‌شدهٔ ۳۰-seed می‌تواند اجرا شود، اما تحلیل آن باید:

1. sensing exposure و joint sensing/movement exposure را در کنار outcome contrastها گزارش کند؛
2. به‌جای raw aggregate difference از matched-seed paired uncertainty interval استفاده کند؛
3. joint exposure محدود را به‌عنوان محدودیت power و mechanism attribution صریحاً گزارش کند؛
4. تا زمانی که sensor جهت‌دار و metric مستقل navigation نداریم، از ادعای navigation/adaptation پرهیز کند.

منبع شواهد: `results/phase-four/resource-sensing-with-movement/preflight/`.
