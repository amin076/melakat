# گزارش شواهد حرکت اتمیک در مرحلهٔ سه

فارسی | [English](phase-three-atomic-movement-evidence.md)

## هدف

این گزارش گیت کامل شواهد مرحلهٔ سه برای semantics جدید پرداخت اتمیک حرکت در `phase-three-vm-0.3` را ثبت می‌کند. آزمایش تشخیصی قبلی حرکت نشان داده بود که یک اثر حرکتی ممکن است پیش از آن‌که پرداخت تجمیعی انرژی اجرای دستورها بررسی شود، در جهان commit شود؛ در نتیجه اگر پرداخت بعدی شکست می‌خورد، حرکت قبلاً رخ داده بود. در نسخهٔ `v0.3` حرکت ابتدا staged می‌شود و فقط پس از موفقیت پرداخت‌های لازم انرژی commit می‌شود.

این آزمایش دربارهٔ سازوکار و حسابداری حرکت است؛ نه دربارهٔ navigation، adaptation، resource seeking، intelligence، cooperation، predation یا fitness.

## تضاد آزمایشی

campaign شامل ۳۰ `seed` تطبیق‌یافته و دو condition بود. هر اجرا ۲۰۰۰ `tick` داشت؛ بنابراین در مجموع ۶۰ اجرای کامل انجام شد.

در هر دو condition موارد زیر یکسان بودند:

- `run.engine_backend=phase-three-vm`؛
- `world.resource_distribution_mode=center_patch`؛
- دسترس‌پذیری ارثی دستورهای حرکت فعال؛
- `mutation.movement_step_rate=0.5`؛
- `world.atomic_movement_payment_enabled=true`؛
- resource sensing غیرفعال؛
- قواعد منابع، mutation، reproduction، memory، topology و local capture یکسان.

تنها تفاوت علّیِ موردنظر، اجرای حرکت بود:

- کنترل: `world.movement_enabled=false`؛
- تیمار: `world.movement_enabled=true`.

نسخهٔ موتور و اندازه‌گیری در تمام اجراها به‌ترتیب `phase-three-vm-0.3` و `phase-three-measurement-0.3` بود.

## نتیجهٔ مکانیکی

گیت verification این campaign با صفر شکست PASS شد.

در مجموع ۳۰ اجرای treatment:

- `movement_operations`: تعداد ۲۵۶؛
- حرکت‌های غیرصفر commit‌شده: ۱۲۹؛
- حرکت‌های zero-step commit‌شده: ۱۲۷؛
- فاصلهٔ حرکتی commit‌شده: ۱۲۹٫۰ واحد؛
- هزینهٔ انرژی حرکت: ۱۲٫۹ واحد.

در کنترل تطبیق‌یافته هیچ حرکت commit نشد و هیچ هزینهٔ انرژی حرکت پرداخت نشد.

چهار تلاش دیگر برای حرکت غیرصفر، با مجموع فاصلهٔ ۴٫۰ واحد، staged شدند اما commit نشدند؛ زیرا پرداخت بعدی انرژی اجرای دستورها شکست خورد. این تلاش‌های ردشده به‌عنوان `uncommitted` diagnostic ثبت شده‌اند و جزو حرکت واقعی محسوب نمی‌شوند. هیچ اجرای دارای حرکت commit‌شده‌ای با پرداخت کمتر از هزینهٔ لازم مشاهده نشد.

همچنین هویت partition حرکت برقرار بود: تعداد کل حرکت‌های commit‌شده برابر بود با مجموع حرکت‌های non-zero و zero-step commit‌شده.

## بقای کمیت‌ها و تکرارپذیری

بیشترین خطای مطلق تراز انرژی `4.6e-09` و بیشترین خطای مطلق تراز منبع محلی `5.8e-09` بود. هر دو بسیار کمتر از tolerance موجود `1e-07` هستند.

تکرار deterministic نیز PASS شد.

## تحلیل تطبیقی

تحلیل paired اصلاح‌شده، metricهای جدید مرحلهٔ سه را از `campaign.json` می‌خواند. فایل قدیمی‌تر `runs.csv` هنوز همهٔ fieldهای جدید و مخصوص مرحلهٔ سه را export نمی‌کند؛ بنابراین برای این metricها نباید به‌تنهایی منبع تحلیل باشد.

برای خود اجرای حرکت، میانگین اختلاف treatment منهای control در `movement_operations` برابر `8.5333` بود و بازهٔ تقریبی ۹۵٪ آن `[3.9809, 13.0858]` بود؛ ۲۴ مورد از ۳۰ جفت مقدار مثبت داشتند و ۶ جفت صفر بودند.

اما حرکت واقعی non-zero میان seedها sparse و بسیار skewed بود. در ۱۴ جفت از ۳۰ جفت، حرکت واقعی مثبت دیده شد و در ۱۶ جفت هیچ حرکت واقعی رخ نداد. میانگین اختلاف فاصلهٔ حرکت `4.3` واحد بود و بازهٔ تقریبی ۹۵٪ نرمال آن `[-0.1230, 8.7230]` بود. یک seed پاسخ حرکتی بسیار بزرگ‌تری از بیشتر seedهای دیگر داشت. بنابراین وجود سازوکار حرکت و صحت حسابداری آن با شواهد مستقیم execution/accounting تثبیت شده است، اما نباید اثر میانگین فاصلهٔ حرکت را یک اثر جهت‌دار تمیز و تقریباً نرمال در تمام seedها توصیف کرد.

برای تمام outcomeهای انتخاب‌شدهٔ جمعیتی/اکولوژیک، بازهٔ تقریبی paired 95% از صفر عبور می‌کند:

- active population؛
- births؛
- deaths؛
- historical genotypes؛
- blocked divisions؛
- mean local neighbors؛
- mean nearest-neighbor distance.

در نتیجه این campaign اثر جهت‌دار و robust جمعیتی یا اکولوژیک ناشی از اجرای حرکت به‌تنهایی را نشان نمی‌دهد.

## تفسیر علمی پذیرفته‌شده

دامنهٔ نتیجه باید محدود بماند:

1. مرحلهٔ سه می‌تواند دستورهای حرکتی ارثی را با semantics پرداخت اتمیک `v0.3` اجرا کند.
2. حرکت واقعی commit‌شده از نظر انرژی حسابداری می‌شود و شکست پرداخت بعدی، اثر حرکتی commit‌شده برجای نمی‌گذارد.
3. اجرای حرکت به‌تنهایی در این campaign اثر جهت‌دار robust بر outcomeهای جمعیتی/اکولوژیک انتخاب‌شده نشان نمی‌دهد.
4. این نتایج navigation، adaptation، resource seeking، fitness advantage، intelligence، cooperation، predation یا open-ended evolution را اثبات نمی‌کنند.

این نتیجه گیت کنترل‌شدهٔ بعدی را باز می‌کند: آزمایش `sensing + movement` می‌تواند بررسی کند آیا اتصال اطلاعات محیطی به locomotion، outcomeهای فضایی یا منابع را تغییر می‌دهد یا نه. آن آزمایش باید semantics اتمیک `v0.3` را حفظ کند و نباید resource seeking را به‌صورت ازپیش‌برنامه‌ریزی‌شده وارد موجودات کند.

## آرشیو شواهد

شواهد machine-readable در مسیر زیر قرار دارند:

`results/phase-three/movement-actuation-atomic/full/`

فایل‌های اصلی عبارت‌اند از:

- `campaign-verification.json`؛
- `paired-analysis.json`؛
- `merge-readiness.json`؛
- `validation.json`؛
- `campaign.json`؛
- `runs.csv`؛
- `summary.json`؛
- `SHA256SUMS.txt`.

پس از عبور موفق campaign، conservation، reproducibility، atomic-payment و گیت تفسیر outcomeهای جمعیتی، وضعیت این evidence record برابر `READY_FOR_MERGE_REVIEW` ثبت شده است.
