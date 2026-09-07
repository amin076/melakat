# مرحلهٔ چهار — حس‌کردن منبع محلی در حضور حرکت

## وضعیت

**پیش‌ثبتِ gate سازوکار و exposure.** این سند پیش از تفسیر campaign کامل، پرسش علّی، contrast آزمایشی، معیارهای smoke و مرزهای تفسیر علمی را تثبیت می‌کند.

## پرسش علمی

> آیا حس‌کردن منبع محلی، هنگامی که locomotion در دسترس است، اجرای حرکت تکامل‌یافته و پیامدهای فضایی/منبعی را تغییر می‌دهد؟

این پرسش عمداً ادعای **navigation toward resource** نیست.

`SENSE_RESOURCE` فقط یک مقدار scalar از resource در مکان فعلی organism را می‌خواند. این sensor هیچ `gradient`، جهت، مختصات هدف یا bearing مربوط به منبع را در اختیار organism قرار نمی‌دهد. همچنین `MOVE_X` و `MOVE_Y` مقدار گام درخواستی را از immediate operand خودشان می‌گیرند، نه از register حس‌شده.

با این حال sensing می‌تواند مسیر اجرای program را عوض کند، زیرا مقدار حس‌شده داخل register نوشته می‌شود و instructionهایی مانند `JUMP_IF_ZERO` می‌توانند تعیین کنند که execution بعداً به یک instruction حرکتی برسد یا نرسد.

بنابراین، اگر treatment اثر قابل‌اندازه‌گیری ایجاد کند، عبارت علمی مناسب **resource-conditioned behavior** است. این نتیجه به‌تنهایی directional navigation، resource seeking، adaptation یا optimality را اثبات نمی‌کند.

## contrast علّی

هر دو condition همهٔ سازوکارهای وراثتی و محیطی را مشترک دارند. تنها تفاوت، اجرای `SENSE_RESOURCE` است.

| ویژگی | Control | Treatment |
| --- | --- | --- |
| دسترسی وراثتی به `SENSE_RESOURCE` | ON | ON |
| دسترسی وراثتی به `MOVE_X` / `MOVE_Y` | ON | ON |
| اجرای movement | ON | ON |
| اجرای resource sensing | **OFF** | **ON** |
| `mutation.movement_step_rate` | 0.5 | 0.5 |
| atomic movement payment | ON | ON |
| resource distribution | center patch | center patch |
| patch fraction / contrast | 0.30 / 4.0 | 0.30 / 4.0 |
| boundary | reflective | reflective |

نام conditionها:

- `sensing-execution-off-movement-on`
- `sensing-execution-on-movement-on`

experiment plan باید به‌طور ماشینی تأیید کند که تنها تفاوت effective configuration، پارامتر `world.resource_sensing_enabled` است.

## specificationها

- Smoke: `experiments/phase-four/resource-sensing-with-movement-smoke.json`
  - ۸ seed تطبیق‌یافته
  - ۸۰۰ tick برای هر run
  - ۱۶ run اصلی، به‌علاوه replay قطعیِ reproducibility که experiment runner انجام می‌دهد
- Full: `experiments/phase-four/resource-sensing-with-movement.json`
  - ۳۰ seed تطبیق‌یافته
  - ۲۰۰۰ tick برای هر run
  - ۶۰ run اصلی، به‌علاوه replay مربوط به reproducibility

backend همچنان `phase-three-vm` باقی می‌ماند. مرحلهٔ چهار سؤال و intervention علمی را جلو می‌برد؛ semantics ماشین مجازی و atomic movement که قبلاً evidence گرفته‌اند، هم‌زمان تغییر نمی‌کنند.

## gateهای smoke

Smoke campaign یک آزمون سازوکار و exposure است و فقط وقتی پاس می‌شود که همهٔ موارد زیر برقرار باشند:

1. **Causal isolation:** effective configها فقط در `world.resource_sensing_enabled` متفاوت باشند.
2. **Matched hereditary alphabet:** قابلیت mutation برای sensing و movement در هر دو condition روشن باشد.
3. **Sensing exposure:** مجموع `resource_sense_operations` در control دقیقاً صفر و در treatment بزرگ‌تر از صفر باشد.
4. **Locomotion exposure:** هر دو condition دست‌کم یک non-zero committed movement operation ثبت کنند.
5. **Atomic accounting:** atomic movement payment در همهٔ runها روشن باشد و realized movement distance نسبت به `world.movement_cost_per_unit = 0.1` underpaid نباشد.
6. **Conservation:** خطای balance انرژی و local resource داخل toleranceهای پذیرفته‌شده بماند.
7. **Reproducibility:** replay تعیین‌شده کاملاً identical باشد.

پاس شدن Smoke **نیازی ندارد** که پیامدهای ecological یا spatial بین treatment و control متفاوت باشند.

## endpointهای campaign کامل

campaign کامل از matched-seed paired contrast استفاده می‌کند. پیامدهای مکانیکی اصلی:

- `resource_sense_operations`
- `movement_operations`
- `movement_nonzero_operations`
- `movement_zero_step_operations`
- `movement_distance`
- `movement_energy_cost`

پیامدهای فضایی/منبعی اصلی:

- `mean_local_neighbors`
- `mean_nearest_neighbor_distance`
- `occupied_spatial_bins`
- `spatial_occupancy_fraction`
- `local_resource_total`
- `local_resource_minimum`
- `resource_heterogeneity_cv`
- `local_resource_maximum`

پیامدهای ecological/population مانند active population، births، deaths، genotype diversity، lineage count و generation depth در این gate پیامدهای ثانویه هستند.

برای هر endpoint انتخاب‌شده، paired mean difference و uncertainty interval گزارش شود. صرفاً non-zero بودن point estimate به معنی وجود اثر مثبت نیست.

## قوانین تفسیر

### اگر sensing اجرا شود ولی interval پیامدهای paired از صفر عبور کند

نتیجه این است که سازوکار sensing + movement فعال و قابل‌اندازه‌گیری بوده، اما campaign در این مقیاس اثر sensing بر endpoint انتخاب‌شده را resolve نکرده است.

### اگر sensing اجرای حرکت یا پیامدهای فضایی/منبعی را تغییر دهد

قوی‌ترین عبارت مجاز این است که **local resource sensing اجرای حرکت تکامل‌یافته و/یا پیامدهای فضایی/منبعی را تغییر داده است** و نتیجه با resource-conditioned behavior سازگار است.

این نتیجه را navigation جهت‌دار ننامید، مگر اینکه در gate بعدی sensor اطلاعات directional محیطی فراهم کند و metric مستقل navigation حرکت نسبت به آن اطلاعات را نشان دهد.

### اگر sensing در treatment هرگز اجرا نشود

contrast علمی exposure کافی نداشته و نمی‌تواند پرسش علّی را پاسخ دهد. در این حالت باید با یک calibration از پیش تعریف‌شده exposure را اصلاح کرد، نه اینکه برابری outcomeها را به‌عنوان null effect تفسیر کرد.

### اگر realized movement در یکی از conditionها وجود نداشته باشد

gate دیگر «sensing در حضور locomotion واقعی» را آزمایش نمی‌کند و تا بازگرداندن locomotion exposure نباید به campaign کامل ارتقا یابد.

## اثبات مکانیکی مسیر control flow

یک regression micro-test از توالی زیر استفاده می‌کند:

1. `SENSE_RESOURCE -> R0`
2. `JUMP_IF_ZERO` روی `R0`
3. `MOVE_X +1`

وقتی sensing خاموش است، `R0` صفر می‌ماند و `MOVE` skip می‌شود. وقتی sensing روشن است و local resource مثبت است، branch عبور می‌کند و `MOVE` اجرا می‌شود. وقتی resource حس‌شده صفر است، `MOVE` دوباره skip می‌شود.

این test دقیقاً نشان می‌دهد scalar sensing چگونه می‌تواند تعیین کند که movement اجرا شود یا نه، در حالی که مرز مهم همچنان حفظ می‌شود: **sensor جهت حرکت را تعیین نمی‌کند؛ جهت +X در این مثال از immediate خود `MOVE_X` می‌آید.**
