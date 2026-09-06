# نقشهٔ راه مرحلهٔ سه — ناهمگنی محیطی

[English](phase-three-roadmap.md)

## وضعیت

مرحلهٔ سه با قرارداد `phase-three-environment-0.1` آغاز شده است.

اولین پرسش علمی عمداً بسیار محدود است:

> اگر مقدار کل منابع ثابت بماند، آیا فقط تغییر توزیع فضایی همان منابع، دینامیک جمعیت و lineageها را تغییر می‌دهد؟

## مرجع منجمد

مرحلهٔ سه از baseline پذیرفته‌شدهٔ مرحلهٔ دو شروع می‌شود و قرارداد علمی آن را تغییر نمی‌دهد:

- `phase-two-spatial-0.7`
- `phase-two-vm-0.7`
- `phase-two-measurement-0.1`

رکورد رسمی freeze در `docs/phase-2/phase-two-frozen-baseline.fa.md` قرار دارد.

## P3.1 — سازوکار ناهمگنی منابع

اولین موتور مرحلهٔ سه `phase-three-vm-0.1` است.

این موتور VM، topology، reproduction، mutation، memory، local capture و semantics حرکت مرحلهٔ دو را به ارث می‌برد. اولین سازوکار causal جدید آن یک حالت deterministic به نام `center_patch` برای توزیع منابع است.

کنترل: `uniform`

مداخله: `center_patch`

در هر دو وضعیت:

- مقدار کل منبع اولیهٔ محیط یکسان است؛
- مقدار کل `world.energy_input_per_tick` یکسان است؛
- resource diffusion اضافه نمی‌شود؛
- capture همچنان فقط از سلول محلی انجام می‌شود؛
- رفتار موجودات تغییر نمی‌کند؛
- هندسهٔ patch هیچ جریان تصادفی تازه‌ای وارد مدل نمی‌کند.

patch فقط وزن نسبی تخصیص منبع میان سلول‌های موجود شبکه را تغییر می‌دهد و تخصیص normalize می‌شود؛ در نتیجه مجموع منابع حفظ می‌شود.

## P3.2 — آزمایش کنترل‌شدهٔ matched

اولین campaign کامل مرحلهٔ سه این دو وضعیت را مقایسه خواهد کرد:

1. توزیع `uniform`؛
2. توزیع `center_patch`.

پیکربندی آغازین بر regime پایدارتر مرحلهٔ دو در حدود `world.energy_input_per_tick = 20.0` بنا می‌شود، چون این مقدار survival و turnover غیرtrivial ایجاد می‌کند بدون آنکه regime فراوانی و اشباع حافظه فوراً بر همه‌چیز غالب شود.

کنترل‌های برنامه‌ریزی‌شده:

- همان ۳۰ `seed`؛
- همان ۲۰۰۰ `tick`؛
- همان موجودات اولیه؛
- همان انرژی اولیهٔ موجودات؛
- همان کل انرژی اولیهٔ محیط؛
- همان کل ورودی انرژی در هر tick؛
- همان resource grid؛
- همان local capture limit؛
- همان boundary model؛
- همان mutation rate؛
- همان قوانین reproduction؛
- sensing/movement در ابتدا خاموش تا فقط geography منابع جداگانه آزمایش شود.

## P3.3 — اندازه‌گیری‌ها

مرحلهٔ سه measurementهای غیرcausal زیر را برای ناهمگنی منبع اضافه می‌کند:

- `coefficient of variation` میدان منبع؛
- بیشترین منبع در یک سلول؛
- متریک‌های موجود population، lineage، genotype، extinction و turnover؛
- کنترل‌های موجود conservation انرژی و منبع محلی.

این measurementها رفتار موجودات را تغییر نمی‌دهند.

## P3.4 — دروازهٔ شواهد

پیش از هر تفسیر علمی، gate مرحلهٔ سه باید نشان دهد:

- اجرای یک seed/configuration یکسان deterministic است؛
- discipline آزمایش matched حفظ شده است؛
- خطای تراز انرژی حداکثر `1e-7` است؛
- خطای تراز منابع محلی حداکثر `1e-7` است؛
- مقدار منبع محلی منفی وجود ندارد؛
- موجود خارج از bounds وجود ندارد؛
- کنترل `uniform` مرحلهٔ سه، برای پیکربندی matched، همان دینامیک مرحلهٔ دو را حفظ می‌کند؛ به‌جز metadata نسخه و measurementهای مخصوص مرحلهٔ سه.

## P3.5 — مرز تفسیر

اگر میان `uniform` و `center_patch` تفاوتی دیده شود، می‌توان دربارهٔ اثر causal ناهمگنی فضایی منابع بر دینامیک ثبت‌شدهٔ همین مدل صحبت کرد.

اما آن تفاوت به‌تنهایی وجود این موارد را اثبات نمی‌کند:

- adaptation؛
- resource-seeking evolution؛
- cooperation؛
- competition؛
- niche formation؛
- intelligence؛
- open-ended evolution.

برای هرکدام از این ادعاها آزمایش جداگانه لازم است.

## سازوکارهای به‌تعویق‌افتاده

مرحلهٔ سه نسخهٔ 0.1 این موارد را اضافه نمی‌کند:

- sensing بهتر؛
- حرکت برنامه‌ریزی‌شده به سمت منبع؛
- predation یا attack؛
- cooperation rules؛
- mating roles؛
- disasters؛
- seasons؛
- resource diffusion؛
- تولید resource توسط organism؛
- fitness function یا انتخاب توسط host.

این موارد در آینده به‌عنوان interventionهای جداگانه بررسی می‌شوند تا causal attribution قابل دفاع بماند.
