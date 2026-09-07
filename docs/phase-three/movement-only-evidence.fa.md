# یادداشت شواهد حرکتِ تنها در مرحلهٔ سه

## پرسش آزمایشی

اگر در مرحلهٔ سه، جغرافیای منابع `center_patch`، کل بودجهٔ منابع، نرخ mutation، دسترسی وراثتی به `MOVE_X` و `MOVE_Y` ثابت و matched باشند و sensing منابع در هر دو وضعیت خاموش باشد، آیا فقط فعال‌کردن اجرای `MOVE_X` و `MOVE_Y` دینامیک اندازه‌گیری‌شدهٔ جمعیت دیجیتال را تغییر می‌دهد؟

## جداسازی causal

- وضعیت‌ها: `movement-execution-off` در برابر `movement-execution-on`.
- تعداد seedهای matched: ۳۰.
- تعداد tick در هر run: ۲۰۰۰.
- مجموع runها: ۶۰.
- جغرافیای منابع: پیکربندی یکسان `center_patch`.
- دسترسی وراثتی به opcodeهای حرکت: در هر دو وضعیت یکسان.
- sensing منابع: در هر دو وضعیت خاموش؛ مجموع مشاهده‌شدهٔ sensing operations برابر ۰.
- movement operations: کنترل = ۰؛ مداخله = ۲۵۷.
- movement operations با جابه‌جایی غیرصفر: کنترل = ۰؛ مداخله = ۶.
- movement operations با گام صفر: کنترل = ۰؛ مداخله = ۲۵۱.
- مجموع فاصلهٔ واقعی حرکت: کنترل = ۰٫۰؛ مداخله = ۶٫۰.
- مجموع هزینهٔ انرژی حرکت: کنترل = ۰٫۰؛ مداخله = ۰٫۶.
- بیشترین خطای مطلق تراز انرژی: `3.9e-09`.
- بیشترین خطای مطلق تراز منابع محلی: `6.7e-09`.
- reproducibility: همهٔ runهای کنترل که برای تکرار تعیین شده بودند، خروجی یکسان داشتند.

## نتایج paired

| متریک | میانگین اختلاف (on - off) | بازهٔ تقریبی ۹۵٪ paired | شامل صفر؟ |
| --- | ---: | ---: | :---: |
| جمعیت فعال نهایی | 0.0 | [0.0, 0.0] | بله |
| تولدها | 0.233333 | [-0.224, 0.690667] | بله |
| مرگ‌ها | 0.233333 | [-0.224, 0.690667] | بله |
| genotypeهای تاریخی | 0.166667 | [-0.16, 0.493333] | بله |
| divisionهای blocked | 0.0 | [0.0, 0.0] | بله |
| میانگین همسایه‌های محلی | 0.0117647 | [-0.0112941, 0.0348235] | بله |
| میانگین فاصله تا نزدیک‌ترین همسایه | 0.0265738 | [-0.0255109, 0.0786585] | بله |
| movement operations | 8.56667 | [3.36851, 13.7648] | خیر |
| movement operations غیرصفر | 0.2 | [0.0544149, 0.345585] | خیر |
| فاصلهٔ واقعی حرکت | 0.2 | [0.0544149, 0.345585] | خیر |

## تفسیر

manipulation check موفق بود: با فعال‌شدن اجرای حرکت، دستورهای `MOVE_X` و `MOVE_Y` واقعاً اجرا شدند، در حالی که در کنترل هیچ اجرای حرکتی وجود نداشت. با این حال فقط ۶ مورد از ۲۵۷ movement operation در وضعیت مداخله واقعاً باعث جابه‌جایی غیرصفر شد و ۲۵۱ مورد گام صفر داشتند. بنابراین semantics حرکت فعال است، اما در representation وراثتی و mutation فعلی، locomotion واقعی بسیار کم رخ می‌دهد.

برای outcomeهای جمعیتی و فضایی منتخب در جدول بالا، بازه‌های تقریبی paired شامل صفر هستند. بنابراین این campaign اثر جهت‌دار و robustی برای اجرای حرکت بر اندازهٔ جمعیت، turnover، تاریخچهٔ genotype، divisionهای blocked یا spatial metrics منتخب نشان نمی‌دهد.

قوی‌ترین نتیجه‌ای که فعلاً پشتیبانی می‌شود محدودتر است: opcodeهای حرکت در شرایط causal isolation اجرا شدند، تعداد کمی جابه‌جایی واقعی ایجاد کردند، conservation انرژی و منابع را در tolerance مقرر حفظ کردند، و در این campaign سی-seed اثر جمعیتی جهت‌دار روشنی ایجاد نکردند.

## پیام توسعه‌ای

این campaign یک bottleneck مهم در representation را برای آزمایش بعدی مرحلهٔ سه آشکار می‌کند: اغلب دستورهای حرکتی تکامل‌یافته عملاً گام صفر به ارث می‌برند، بنابراین حرکت اجرا می‌شود ولی locomotion رخ نمی‌دهد. پیش از آزمایش resource-seeking یا navigation، ملاکت باید یک روش وراثتی و جداگانه‌قابل‌آزمایش برای تولید commandهای حرکت غیرصفر با فراوانی معنادار داشته باشد، بدون آنکه discipline مربوط به causal isolation و کنترل‌پذیری آزمایش شکسته شود.

این بخش یک inference توسعه‌ای از شمارش mechanismهاست و نباید به‌عنوان evidence برای adaptation یا مشابه‌سازی زیستی تفسیر شود.

## مرز ادعا

این شواهد فقط دربارهٔ اجرای semantics موجود `MOVE_X` و `MOVE_Y` و پیامدهای اندازه‌گیری‌شدهٔ آنها در مدل فعلی `center_patch` مرحلهٔ سهٔ ملاکت است. این campaign **navigation**، **resource-seeking**، adaptation، biological fitness، intelligence، cooperation، competition، niche formation یا open-ended evolution را اثبات نمی‌کند.

بازه‌های تقریبی، descriptive paired interval برای همین campaign محاسباتی deterministic هستند و ادعای inference به جمعیت‌های زیستی نیستند.

## artifactهای شواهد

- `experiments/phase-three/movement-only.json`
- `results/phase-three/movement-only/full/campaign.json`
- `results/phase-three/movement-only/full/validation.json`
- `results/phase-three/movement-only/full/campaign-verification.json`
- `results/phase-three/movement-only/full/paired-analysis.json`
- `results/phase-three/movement-only/full/SHA256SUMS.txt`
