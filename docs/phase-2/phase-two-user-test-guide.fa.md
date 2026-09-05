# راهنمای تست کاربر برای مرحلهٔ دو

[English](phase-two-user-test-guide.md) | [نقشهٔ راه مرحلهٔ دو](../doc-farsi/phase-two-roadmap.md)

این راهنما مسیر پذیرش دستی نسخهٔ کامل مرحلهٔ دو در «ملاکت» است.

## ۱. به‌روزرسانی مخزن

از ریشهٔ مخزن ملاکت:

~~~powershell
git checkout main
git pull
~~~

## ۲. ساخت یا نوسازی محیط Python

در صورت امکان از `CPython 3.12` استفاده کنید.

~~~powershell
cd desktop
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
~~~

## ۳. اجرای آزمون‌های خودکار

~~~powershell
python -m unittest discover -s tests -v
~~~

پیش از تست دستی شبیه‌سازی، مجموعهٔ آزمون‌ها باید بدون شکست تمام شود.

## ۴. اجرای آزمایشگاه دسکتاپ

با فعال‌بودن محیط مجازی، از ریشهٔ مخزن:

~~~powershell
cd ..
python -m melakat_desktop.main
~~~

## ۵. کنترل سازگاری با مرحلهٔ یک

ابتدا کنترل همگن دائمی را اجرا کنید:

- `Engine backend`: `phase-two-vm`
- `Enable spatial rules`: خاموش
- `Enable local resource field`: خاموش
- `Enable evolved sensing/movement`: خاموش
- `Seed`: `1`
- `Maximum ticks`: `2000`

این مسیر کنترل دائمی و سازگار با مرحلهٔ یک است. ممکن است متادیتای مرحلهٔ دو در خروجی وجود داشته باشد، اما حالت علمی باید با خط پایهٔ پذیرفته‌شده هم‌ارز بماند.

## ۶. تست فضا و توپولوژی

این تنظیمات را استفاده کنید:

- `Engine backend`: `phase-two-vm`
- `Enable spatial rules`: روشن
- `Boundary model`: `reflective`
- `Offspring dispersion radius`: `1.0`
- `Enable local resource field`: خاموش
- `Enable evolved sensing/movement`: خاموش
- `Seed`: `1`

ابتدا یک اجرای کوتاه مثلاً ۲۰۰ تا ۵۰۰ `tick` انجام دهید. موقعیت موجودات، فاصلهٔ والد-فرزند، همسایه‌های محلی، اشغال فضایی و تماس با مرز را بررسی کنید.

سپس همان آزمایش را با مرز `toroidal` تکرار کنید. در جهان `toroidal`، فاصلهٔ همسایگی بر اساس کوتاه‌ترین مسیرِ پیچیده‌شده در مرز محاسبه می‌شود.

## ۷. تست منبع محلی

این موارد را روشن کنید:

- `Enable spatial rules`: روشن
- `Enable local resource field`: روشن
- `Resource grid columns`: `10`
- `Resource grid rows`: `7`
- `Local capture limit`: `1.0`

برای این آزمایش مستقل، حرکت و sensing تکاملی را خاموش نگه دارید. لایهٔ منبع باید در رابط دیده شود، هیچ سلول منبعی نباید منفی شود، و `local_resource_balance_error` باید در تلورانس مستندشدهٔ `1e-7` باقی بماند.

## ۸. تست sensing و حرکت

سپس این موارد را روشن کنید:

- `Enable evolved sensing/movement`: روشن
- `Maximum movement per instruction`: `1.0`
- `Movement energy cost per unit`: `0.1`

در این حالت الفبای mutation مرحلهٔ دو می‌تواند شامل `SENSE_RESOURCE`، `MOVE_X` و `MOVE_Y` باشد. حرکت با مدل مرزی انتخاب‌شده محدود می‌شود و هزینهٔ واقعی حرکت در ledger انرژی ثبت می‌شود.

نکتهٔ مهم: فعال‌کردن این opcodeها هیچ هوش، همکاری یا رفتار هدف‌داری را از قبل تعریف نمی‌کند. ممکن است موجودات در روند mutation ژنوم‌هایی بسازند که از این دستورها استفاده کنند یا نکنند.

## ۹. بررسی رابط پژوهشی

در اجرای مرحلهٔ دو بررسی کنید که بتوانید این موارد را ببینید یا کنترل کنید:

- نمایش/عدم نمایش لایهٔ موجودات، مرز و منابع؛
- انتخاب نمودارهای زمانی متریک‌های فضایی؛
- موقعیت، منبع محلی و اطلاعات همسایگی موجود انتخاب‌شده؛
- فیلتر رویدادهای حرکت، مرز، منبع، تولد و مرگ؛
- تنظیمات دقیق اجرا و نسخهٔ world contract در artifact ذخیره‌شده.

## ۱۰. بازتولید گیت شواهد مرحلهٔ دو

کارزار پذیرفته‌شدهٔ مرحلهٔ دو شامل ۳۰ `seed`، دوازده وضعیت و `2000 tick` برای هر اجراست؛ در مجموع ۳۶۰ اجرا.

با محیط فعال‌شده:

~~~powershell
melakat-phase-two-evidence --runs 30 --ticks 2000 --seed-start 1 --output-dir results/phase-two/evidence-gate
~~~

برای یک تست سریع پیش از کارزار کامل:

~~~powershell
melakat-phase-two-evidence --runs 2 --ticks 200 --seed-start 1 --output-dir results/phase-two/manual-smoke
~~~

خروجی اجرای دستی نباید بدون بررسی و پذیرش آگاهانه جایگزین آرشیو شواهد پذیرفته‌شده شود.

## مرز علمی مرحلهٔ دو

مرحلهٔ دو فضا، توپولوژی، منبع انرژی محلی، primitiveهای مشاهده و حرکت، مقایسه‌های کنترل‌شده، متریک‌های فضایی و رابط پژوهشی را اضافه می‌کند. این مرحله شامل یادگیری ماشین، هدف `fitness`، حمله، همکاری، نقش‌های جفت‌گیری، انگل یا رفتار اجتماعی نوشته‌شده توسط host نیست.
