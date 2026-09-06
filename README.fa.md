# ملاکت

[English](README.md)

«ملاکت» یک شبیه‌سازی پژوهش‌محور برای بررسی این پرسش است که آیا موجودات دیجیتال بسیار ساده و داده‌محور می‌توانند در یک جهان محاسباتی محدود، دینامیک‌های تکاملی و محیطی ایجاد کنند یا نه.

موجودات درون یک ماشین مجازی محدود اجرا می‌شوند، انرژی و حافظهٔ محدود مصرف می‌کنند، ژنوم خود را کپی می‌کنند، `mutation` کور و وراثتی دارند، تولیدمثل می‌کنند و ممکن است بمیرند. مرحلهٔ دو فضا، منابع محلی، sensing و حرکت محدود را اضافه کرد، بدون آنکه تابع `fitness` یا رفتار اجتماعی از پیش نوشته‌شده به موجودات تحمیل شود. مرحلهٔ سه اکنون از همان مرجع منجمد شروع شده و در نخستین مداخله فقط نحوهٔ توزیع فضایی همان مقدار کل منابع را تغییر می‌دهد.

## وضعیت فعلی

**مرحلهٔ صفر، مرحلهٔ یک و مرحلهٔ دو کامل شده‌اند. مرحلهٔ دو رسماً به‌عنوان baseline مرجع منجمد شده و مرحلهٔ سه آغاز شده است.**

نسخه‌های منجمد مرحلهٔ دو:

- قرارداد جهان: `phase-two-spatial-0.7`
- موتور: `phase-two-vm-0.7`
- قرارداد اندازه‌گیری: `phase-two-measurement-0.1`
- قالب artifact: `melakat-run-artifact-0.2`

نسخه‌های آغازین مرحلهٔ سه:

- قرارداد جهان: `phase-three-environment-0.1`
- موتور: `phase-three-vm-0.1`
- قرارداد اندازه‌گیری: `phase-three-measurement-0.1`

خط پایهٔ همگن مرحلهٔ یک همچنان کنترل دائمی و منجمد است. implementation و evidence پذیرفته‌شدهٔ مرحلهٔ دو نیز اکنون مرجع منجمد دوم برای پژوهش‌های فضایی/محیطی بعدی است.

### قابلیت‌های مرحلهٔ دو

- فضای انتزاعی پیوستهٔ دوبعدی؛
- مرزهای صریح `reflective` و `toroidal`؛
- تولد محلی فرزند و اندازه‌گیری‌های فضایی؛
- شبکهٔ محافظه‌کار منابع انرژی محلی با تجدید یکنواخت و دریافت انرژی از سلول فعلی؛
- دستورهای داده‌محور `SENSE_RESOURCE`، `MOVE_X` و `MOVE_Y`؛
- حرکت محدود با هزینهٔ انرژی صریح؛
- حسابداری رویدادها، انرژی، منابع و حرکت؛
- کنترل‌های schema-driven در رابط دسکتاپ و لایه‌های موجود/مرز/منبع؛
- مشاهدهٔ اطلاعات محلی موجود انتخاب‌شده و نمودارهای زمانی فضایی؛
- مقایسهٔ نتایج ذخیره‌شده و export نسخه‌گذاری‌شده؛
- ماتریس آزمایش چند-`seed` کنترل‌شده؛
- آزمون تکرار قطعی و اندازه‌گیری performance.

### محدودهٔ فعلی مرحلهٔ سه v0.1

در حال حاضر فقط یک intervention causal جدید اضافه شده است: ناهمگنی منابع به شکل `center_patch`.

کنترل matched حالت `uniform` است. در هر دو حالت مقدار کل منبع اولیهٔ محیط و مقدار کل `world.energy_input_per_tick` یکسان می‌ماند و فقط allocation نسبی منابع روی grid موجود تغییر می‌کند. هندسهٔ patch deterministic است و جریان تصادفی تازه‌ای وارد مدل نمی‌کند.

measurementهای غیرcausal جدید شامل `coefficient of variation` میدان منبع و بیشترین مقدار منبع در یک سلول هستند. مرحلهٔ سه v0.1 هنوز resource diffusion، حرکت برنامه‌ریزی‌شده به سمت منابع، predation، cooperation، فصل، disaster، fitness function یا انتخاب host را اضافه نمی‌کند.

این‌ها قوانین و اندازه‌گیری‌های مدل دیجیتال هستند و ادعای بازسازی حیات زیستی، هوش، adaptation، cooperation، competition یا niche formation نیستند.

## دروازه‌های شواهد پذیرفته‌شده

### مرحلهٔ یک

کارزار پذیرفته‌شدهٔ مرحلهٔ یک شامل ۹۹۰ اجراست: ۳۰ `seed` در شش وضعیت کنترل و ۲۷ حالت حساسیت تک‌عاملی، با `2000 tick` برای هر اجرا. تمام بررسی‌های پیکربندی، checksum، تعداد tick، انرژی و حافظه پاس شدند. بیشترین خطای مطلق تراز انرژی `2.5e-08` در برابر تلورانس `1e-07` بود.

### مرحلهٔ دو

کارزار پذیرفته‌شدهٔ مرحلهٔ دو شامل **۳۶۰ اجرا** است: ۳۰ `seed` در ۱۲ وضعیت تطبیقی فضایی/محیطی و `2000 tick` برای هر اجرا.

اعتبارسنجی نهایی مرحلهٔ دو:

- شکست validation: `0`؛
- بیشترین خطای مطلق تراز انرژی: `1.02e-08`؛
- بیشترین خطای مطلق تراز منبع محلی: `4.2e-09`؛
- تلورانس هر دو ledger: `1e-07`؛
- تکرار قطعی: PASS؛
- commit منبع پذیرفته‌شده: `ad5e21159baf0d6bd79a028799b9318ba144fed7`؛
- اجرای workflow شواهد: `33969619473`.

در بسیاری از آزمایش‌های پیش‌فرض منبع محلی extinction رخ داد، زیرا انرژی می‌تواند در سلول‌های بدون موجود باقی بماند و مرحلهٔ دو عمداً diffusion ندارد. در وضعیت منبع فراوان، جمعیت می‌تواند پایدار بماند اما گردش تولد/مرگ بسیار بیشتر می‌شود. این‌ها خروجی‌های مدل هستند، نه شکست invariant.

رکورد رسمی freeze در [خط پایهٔ منجمد مرحلهٔ دو](docs/phase-2/phase-two-frozen-baseline.fa.md) ثبت شده است. آزمایش‌های اکتشافی بعدی جایگزین این gate نمی‌شوند.

## مرزهای پژوهشی

ملاکت همچنان عمداً این موارد را شامل نمی‌شود:

- یادگیری ماشین و شبکهٔ عصبی؛
- هدف هوشمندی؛
- تابع صریح `fitness`؛
- انتخاب دستی موجودات موفق؛
- رفتار حمله یا همکاری نوشته‌شده توسط host؛
- نقش‌های جفت‌گیری، انگل یا بیماری؛
- پاداش برای پیچیدگی؛
- diffusion منابع یا تولید منابع توسط موجود در مدل فعلی مرحلهٔ سه v0.1؛
- دسترسی موجودات به فایل‌سیستم، شبکه، `subprocess`، runtime میزبان یا `API` بیرونی.

فرایند Python فقط شبیه‌ساز میزبان است. موجودات کد Python اجرا نمی‌کنند.

## مستندات

- [فهرست مستندات فارسی](docs/README.fa.md)
- [Documentation index](docs/README.md)
- [گزارش شواهد مرحلهٔ یک](docs/doc-farsi/phase-one-evidence-report.md)
- [گزارش تکمیل و شواهد مرحلهٔ دو](docs/phase-2/phase-two-completion-report.fa.md)
- [خط پایهٔ منجمد مرحلهٔ دو](docs/phase-2/phase-two-frozen-baseline.fa.md)
- [نقشهٔ راه مرحلهٔ سه](docs/phase-3/phase-three-roadmap.fa.md)
- [آرشیو شواهد مرحلهٔ یک](results/phase-one/evidence-gate/README.fa.md)
- `results/phase-two/evidence-gate/` — آرشیو پذیرفته‌شدهٔ campaign، validation، performance، provenance و checksumهای مرحلهٔ دو

## ساختار مخزن

- `desktop/src/melakat_desktop/phase_zero_engine.py` — موتور مرجع منجمد جهان همگن؛
- `desktop/src/melakat_desktop/phase_two_engine.py` — موتور منجمد فضایی/محیطی مرحلهٔ دو؛
- `desktop/src/melakat_desktop/phase_two_vm.py` — گسترش داده‌محور VM برای sensing و حرکت؛
- `desktop/src/melakat_desktop/phase_three_contract.py` — قرارداد ناهمگنی محیطی مرحلهٔ سه؛
- `desktop/src/melakat_desktop/phase_three_engine.py` — موتور مرحلهٔ سه v0.1 با حفظ قوانین مرحلهٔ دو و اضافه‌کردن ناهمگنی تخصیص منابع؛
- `desktop/src/melakat_desktop/resources.py` — میدان محافظه‌کار منابع محلی با allocation یکنواخت مرحلهٔ دو و primitiveهای weighted مرحلهٔ سه؛
- `desktop/src/melakat_desktop/spatial.py` — توپولوژی، جای‌گذاری و متریک‌های فضایی؛
- `desktop/src/melakat_desktop/world_contract.py` — قرارداد منجمد مرحلهٔ دو؛
- `desktop/src/melakat_desktop/phase_two_experiment.py` — ماتریس شواهد و performance probe مرحلهٔ دو؛
- `desktop/src/melakat_desktop/ui.py` — رابط پژوهشی دسکتاپ؛
- `results/phase-one/evidence-gate/` — شواهد پذیرفته‌شدهٔ مرحلهٔ یک؛
- `results/phase-two/evidence-gate/` — شواهد پذیرفته‌شدهٔ مرحلهٔ دو.

## اجرای برنامهٔ دسکتاپ

Python 3.12 نسخهٔ مرجع CI است.

~~~powershell
git checkout main
git pull
cd desktop
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
python -m unittest discover -s tests -v
cd ..
python -m melakat_desktop.main
~~~

انتخاب backend در دسکتاپ اکنون `phase-three-vm` را می‌شناسد، اما اولین intervention ناهمگن ابتدا به‌صورت headless و در testها اعتبارسنجی می‌شود؛ سپس کنترل‌های اختصاصی مرحلهٔ سه و runner عمومی آزمایش‌ها گسترش داده خواهند شد. این ترتیب کمک می‌کند اولین تغییر علمی کوچک بماند و defaultهای منجمد مرحلهٔ دو دست‌نخورده حفظ شوند.

برای قرارداد علمی فعلی و gate بعدی، [نقشهٔ راه مرحلهٔ سه](docs/phase-3/phase-three-roadmap.fa.md) را ببینید.
