# گزارش تکمیل مرحلهٔ چهار — حس‌کردن منبع محلی در حضور حرکت

[English](phase-four-completion-report.md)

## وضعیت

**دروازهٔ شواهد مرحلهٔ چهار: کامل شد.**

کارزار کامل ثبت‌شده اجرا، اعتبارسنجی، تحلیل paired، بررسی checksum و بایگانی شده است. پرسش مرحلهٔ چهار این بود که آیا اجرای حس‌کردن اسکالر منبع محلی، در حالی که حرکت در دسترس است و تمام سازوکارهای وراثتی و محیطی بین دو بازو matched هستند، اجرای حرکت تکامل‌یافته و پیامدهای فضایی/منبعی را تغییر می‌دهد یا نه.

پاسخ، ترکیبی و از نظر علمی مهم است:

- مداخلهٔ sensing با موفقیت در treatment در معرض اجرا قرار گرفت؛
- حرکت واقعی در هر دو وضعیت وجود داشت؛
- هیچ endpoint ثبت‌شدهٔ مربوط به اجرای حرکت interval تقریبی ۹۵٪ نداشت که صفر را کنار بگذارد؛
- سه endpoint فضایی/منبعی ثبت‌شده intervalی داشتند که صفر را شامل نمی‌کرد؛
- دو outcome ثانویهٔ جمعیتی نیز صفر را کنار گذاشتند؛
- بنابراین الگو با یک تغییر ناشی از sensing در وضعیت اکولوژیک/فضایی سازگار است، اما **اثر حل‌شده‌ای بر خود اجرای locomotion نشان نمی‌دهد**؛
- sensor فعلی هیچ اطلاعات جهتی نمی‌دهد، بنابراین این کارزار navigation یا resource seeking را آزمایش یا اثبات نمی‌کند.

## طراحی ثبت‌شده

مشخصات کامل:

`experiments/phase-four/resource-sensing-with-movement.json`

کارزار:

- ۳۰ `seed` تطبیق‌یافته؛
- ۲ وضعیت؛
- `2000 tick` برای هر اجرا؛
- ۶۰ اجرای اصلی به‌علاوهٔ replay قطعی ثبت‌شده.

وضعیت‌ها:

- کنترل: `sensing-execution-off-movement-on`؛
- treatment: `sensing-execution-on-movement-on`.

در هر دو وضعیت یکسان بود:

- امکان وراثتی `SENSE_RESOURCE`: روشن؛
- امکان وراثتی `MOVE_X` / `MOVE_Y`: روشن؛
- اجرای حرکت: روشن؛
- `mutation.movement_step_rate = 0.5`؛
- پرداخت اتمیک حرکت: روشن؛
- توزیع منبع `center_patch`؛
- بودجهٔ منابع، topology، reproduction، mutation، memory و قوانین execution.

تنها تفاوت اجرایی:

`world.resource_sensing_enabled`

بود.

`SENSE_RESOURCE` فقط مقدار اسکالر منبع در مکان فعلی organism را گزارش می‌کند. هیچ gradient، bearing، target coordinate یا جهت حرکت در اختیار organism قرار نمی‌دهد.

## سلامت کارزار و بازتولیدپذیری

تمام گیت‌های ساختاری پاس شدند:

- اجراهای کامل: `60/60`؛
- شکست validation: `0`؛
- replay قطعی: `PASS`؛
- موتور: `phase-three-vm-0.3`؛
- measurement: `phase-three-measurement-0.3`؛
- پرداخت اتمیک حرکت: در همهٔ runها روشن؛
- run دارای حرکت واقعی کم‌پرداخت‌شده: `0`؛
- بیشترین خطای مطلق تراز انرژی: `4.8e-09`؛
- بیشترین خطای مطلق تراز منبع محلی: `6.3e-09`؛
- tolerance پذیرفته‌شدهٔ هر دو ledger: `1e-07`؛
- بررسی نهایی checksum آرشیو: `PASS`.

## Exposure

Treatment در مجموع sensing قابل‌توجهی اجرا کرد، اما exposure بین seedها ناهمگن بود:

| شاخص | Control | Treatment |
| --- | ---: | ---: |
| کل عملیات sensing | 0 | 508 |
| runهای دارای sensing | 0/30 | 15/30 |
| runهای دارای هر نوع MOVE | 21/30 | 18/30 |
| runهای دارای حرکت غیرصفر | 17/30 | 15/30 |
| sensing + هر نوع MOVE در یک run | — | 8/30 |
| sensing + حرکت غیرصفر در یک run | — | 7/30 |

کارزار کامل نسبت به preflight هشت-seed co-exposure بیشتری ایجاد کرد، اما هم‌زمانی مستقیم sensing و locomotion غیرصفر همچنان محدود است. این موضوع قدرت نسبت‌دادن مکانیزم مستقیم را محدود می‌کند و باید همراه نتیجه گزارش شود.

## پیامدهای اجرای حرکت

هیچ endpoint از پیش ثبت‌شدهٔ حرکت، اثر paired حل‌شده‌ای نشان نداد.

| Endpoint | میانگین Control | میانگین Treatment | Delta میانگین (T-C) | interval تقریبی ۹۵٪ | حل‌شده؟ |
| --- | ---: | ---: | ---: | ---: | --- |
| `movement_operations` | 5.6000 | 5.1667 | -0.4333 | [-1.2234, 0.3567] | خیر |
| `movement_nonzero_operations` | 4.6000 | 4.1333 | -0.4667 | [-1.2514, 0.3181] | خیر |
| `movement_distance` | 4.6000 | 4.1333 | -0.4667 | [-1.2514, 0.3181] | خیر |
| `movement_energy_cost` | 0.4600 | 0.4164 | -0.0436 | [-0.1221, 0.0348] | خیر |
| `movement_zero_step_operations` | 1.0000 | 1.0333 | +0.0333 | [-0.1148, 0.1814] | خیر |

مجموع‌های خام فقط توصیفی هستند:

- کل movement operation در کنترل: `168`؛
- در treatment: `155`؛
- حرکت غیرصفر/مسافت در کنترل: `138 / 138`؛
- در treatment: `124 / 124`؛
- هزینهٔ حرکت کنترل: `13.8`؛
- هزینهٔ حرکت treatment: `12.490909`.

این اعداد به‌تنهایی نشان نمی‌دهند sensing حرکت را کاهش داده است، چون intervalهای paired ثبت‌شده صفر را شامل می‌کنند.

## پیامدهای فضایی و منبعی

سه endpoint ثبت‌شدهٔ فضایی/منبعی صفر را از interval کنار گذاشتند:

| Endpoint | میانگین Control | میانگین Treatment | Delta میانگین (T-C) | interval تقریبی ۹۵٪ |
| --- | ---: | ---: | ---: | ---: |
| `mean_local_neighbors` | 2.0854 | 1.5018 | -0.5836 | [-1.1521, -0.0150] |
| `mean_nearest_neighbor_distance` | 9.3449 | 10.0239 | +0.6790 | [0.0541, 1.3038] |
| `local_resource_total` | 32871.7912 | 33084.1853 | +212.3941 | [4.8831, 419.9051] |

endpointهای زیر حل‌نشده باقی ماندند:

- `occupied_spatial_bins`؛
- `spatial_occupancy_fraction`؛
- `resource_heterogeneity_cv`؛
- `local_resource_maximum`؛
- `local_resource_minimum`.

این الگو نشان می‌دهد روشن‌کردن sensing محلی، تحت همین طراحی ثبت‌شده، وضعیت فضایی/منبعی مدل را به‌طور causal تغییر داد. اما نشان نمی‌دهد organismها به سمت منبع حرکت کردند. خود endpointهای حرکت همچنان unresolved بودند.

## پیامدهای ثانویهٔ جمعیت

دو endpoint ثانویه نیز intervalی داشتند که صفر را شامل نمی‌کرد:

- `active_population`: میانگین کنترل `18.1333`، treatment `16.4333`، delta paired برابر `-1.7000`، interval برابر `[-3.3389, -0.0611]`؛
- `blocked_divisions`: میانگین کنترل `16.7000`، treatment `14.8000`، delta paired برابر `-1.9000`، interval برابر `[-3.6413, -0.1587]`.

Birth، death، تعداد historical genotype، active genotype، active lineage و بیشترین generation در intervalهای paired خود unresolved ماندند.

کاهش active population برای تفسیر بسیار مهم است: جمعیت کمتر می‌تواند خود باعث کاهش تعداد همسایهٔ محلی، افزایش فاصلهٔ نزدیک‌ترین همسایه و باقی‌ماندن resource بیشتر در محیط شود. بنابراین نباید سیگنال فضایی/منبعی را به‌صورت هدایت مستقیم locomotion روایت کنیم. یک زنجیرهٔ علّی ممکن این است:

`sensing execution -> تغییر trajectory برنامه/اکولوژی -> کاهش population/density -> تغییر spatial/resource state`

اما این campaign برای شناسایی یک mediation pathway یکتا طراحی نشده است.

## قرارداد آماری

همان قرارداد مرحلهٔ سه حفظ شد:

`paired mean treatment-minus-control ± 1.96 × sample_SD(delta) / sqrt(n)`

با `n = 30` seed matched.

این intervalها تقریبی و مبتنی بر normal approximation هستند؛ ادعای پوشش دقیق finite-sample یا correction برای multiple comparisons ندارند. Endpointها و قواعد تفسیر پیش از مشاهدهٔ full campaign ثبت شده بودند.

## نتیجهٔ علمی

مرحلهٔ چهار در مدل فعلی ملاکت این موارد را نشان می‌دهد:

1. sensing اسکالر محلی را می‌توان در حالی که availability وراثتی sensing/movement و اجرای حرکت matched باقی می‌مانند، به‌صورت causal جدا کرد؛
2. sensing در treatment واقعاً اجرا شد و در control اجرا نشد؛
3. هر دو وضعیت locomotion غیرصفر واقعی تحت atomic payment داشتند؛
4. sensing در این مقیاس تفاوت حل‌شده‌ای در endpointهای ثبت‌شدهٔ اجرای حرکت ایجاد نکرد؛
5. sensing در چند outcome فضایی/منبعی تفاوت حل‌شده ایجاد کرد و هم‌زمان active population ثانویه پایین‌تر بود؛
6. نتیجه با **resource-conditioned ecological/spatial dynamics** سازگار است و مطابق wording از پیش ثبت‌شده، در معنای گسترده با resource-conditioned behavior سازگار است؛
7. این evidence directional navigation، resource seeking، adaptation، fitness advantage، intelligence، cooperation، predation یا open-ended evolution را نشان نمی‌دهد.

مرز اصلی این است که sensor هیچ جهت یا gradientی نمی‌دهد. بنابراین حتی وجود یک treatment effect بازتولیدپذیر نیز navigation محسوب نمی‌شود.

## آرشیو شواهد

آرشیو canonical:

`results/phase-four/resource-sensing-with-movement/full/`

شامل خروجی‌های اصلی campaign و نیز:

- `campaign-verification.json`؛
- `paired-analysis.json`؛
- `merge-readiness.json`؛
- `README.md`؛
- `SHA256SUMS.txt`.

pre-registration، smoke evidence و preflight تمام‌مدت جداگانه حفظ شده‌اند و full campaign آنها را overwrite نکرده است.

## بسته‌شدن مرحلهٔ چهار

مرحلهٔ چهار به‌عنوان یک causal evidence checkpoint کامل است. مرحلهٔ بعد نباید این نتیجه را به navigation تعبیر کند. اگر بعداً بخواهیم navigation را آزمایش کنیم، باید اطلاعات محیطی جهت‌دار و metric اختصاصی navigation به‌صورت intervention جداگانه تعریف شوند. همچنین هر گسترش در evolvability باید به‌صورت نسخه‌گذاری‌شده و جدا از این evidence پذیرفته‌شده انجام شود.
