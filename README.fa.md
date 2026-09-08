# ملاکت

[English](README.md)

«ملاکت» یک شبیه‌سازی پژوهش‌محور برای بررسی این پرسش است که آیا موجودات دیجیتال ساده و داده‌محور می‌توانند در یک جهان محاسباتی محدود، دینامیک‌های تکاملی و اکولوژیک ایجاد کنند یا نه.

موجودات درون یک `Virtual Machine` محدود اجرا می‌شوند. انرژی و حافظهٔ محدود مصرف می‌کنند، ژنوم خود را کپی می‌کنند، `mutation` کور و وراثتی دارند، تولیدمثل می‌کنند و ممکن است بمیرند. مراحل بعدی فضا، منابع محلی، ناهمگنی محیط، sensing اسکالر منبع و حرکت محدود را اضافه کردند، بدون آنکه `fitness function`، کنترل‌گر `Machine Learning` یا رفتار اجتماعی از پیش نوشته‌شده به موجودات تحمیل شود.

## وضعیت فعلی

**مرحلهٔ صفر، مرحلهٔ یک و مرحلهٔ دو کامل شده‌اند. مرحلهٔ دو رسماً به‌عنوان baseline مرجع منجمد شده است. زنجیرهٔ mechanism/evidence مرحلهٔ سه برای ناهمگنی محیط، sensing و movement کامل شده و evidence gate مرحلهٔ چهار برای sensing در حضور movement نیز کامل شده است.**

نسخه‌های منجمد مرحلهٔ دو:

- قرارداد جهان: `phase-two-spatial-0.7`
- موتور: `phase-two-vm-0.7`
- قرارداد اندازه‌گیری: `phase-two-measurement-0.1`
- قالب artifact: `melakat-run-artifact-0.2`

نسخه‌های فعلی evidence اجرایی مرحلهٔ سه که در gate تکمیل‌شدهٔ مرحلهٔ چهار استفاده شدند:

- قرارداد جهان: `phase-three-environment-0.1`
- موتور: `phase-three-vm-0.3`
- اندازه‌گیری: `phase-three-measurement-0.3`

خط پایهٔ همگن مرحلهٔ یک همچنان کنترل دائمی منجمد است. implementation/evidence پذیرفته‌شدهٔ مرحلهٔ دو نیز مرجع منجمد فضا و منابع محلی باقی می‌ماند. evidenceهای مرحلهٔ سه و چهار این baselineها را گسترش می‌دهند، بدون آنکه آنها را بی‌صدا بازنویسی کنند.

### قابلیت‌های اصلی فعلی

- `Virtual Machine` محدود و داده‌محور با self-copy و division ابتدایی؛
- `mutation` کور و وراثتی، genealogy، lineage و genotype tracking؛
- انرژی محدود، حافظهٔ ساختاری محدود و هزینه‌های execution، maintenance و reproduction؛
- اجرای deterministic بر پایهٔ seed و ledgerهای conservation؛
- فضای انتزاعی پیوستهٔ دوبعدی؛
- مرزهای `reflective` و `toroidal`؛
- تولد محلی فرزند و اندازه‌گیری‌های فضایی؛
- grid محافظه‌کار منابع انرژی محلی با capture از cell فعلی؛
- ناهمگنی محیطی deterministic از نوع `center_patch` با ثابت‌ماندن کل ورودی resource؛
- instructionهای داده‌محور `SENSE_RESOURCE`، `MOVE_X` و `MOVE_Y`؛
- امکان تکامل stepهای غیرصفر حرکت؛
- حرکت محدود با پرداخت اتمیک انرژی؛
- eventها و measurementهای فضا، resource و movement؛
- رابط دسکتاپ پژوهشی schema-driven با لایه‌های organism/boundary/resource؛
- بازرس organism انتخاب‌شده و metricهای زمانی فضایی؛
- مقایسهٔ نتایج ذخیره‌شده و export نسخه‌گذاری‌شده؛
- experiment specificationهای خودکار چند-condition و چند-seed؛
- deterministic replay، provenance، validation، archiveهای CSV/JSON و manifestهای SHA-256؛
- paired evidence analysis برای seedهای matched.

## دروازه‌های شواهد پذیرفته‌شده

### مرحلهٔ یک

کارزار پذیرفته‌شدهٔ مرحلهٔ یک شامل ۹۹۰ اجراست: ۳۰ `seed` در شش وضعیت control و ۲۷ حالت sensitivity تک‌عاملی، با `2000 tick` برای هر اجرا. تمام بررسی‌های configuration، checksum، تعداد tick، انرژی و حافظه پاس شدند. بیشترین خطای مطلق تراز انرژی `2.5e-08` در برابر tolerance برابر `1e-07` بود.

### مرحلهٔ دو

کارزار پذیرفته‌شدهٔ مرحلهٔ دو شامل **۳۶۰ اجرا** است: ۳۰ `seed` در ۱۲ وضعیت فضایی/محیطی matched و `2000 tick` برای هر اجرا.

اعتبارسنجی نهایی:

- شکست validation: `0`؛
- بیشترین خطای مطلق تراز انرژی: `1.02e-08`؛
- بیشترین خطای مطلق تراز منبع محلی: `4.2e-09`؛
- tolerance هر دو ledger: `1e-07`؛
- deterministic repeat: PASS؛
- source commit پذیرفته‌شده: `ad5e21159baf0d6bd79a028799b9318ba144fed7`؛
- evidence workflow run: `33969619473`.

در بسیاری از آزمایش‌های پیش‌فرض resource محلی extinction رخ داد، چون انرژی می‌تواند در cellهای بدون organism باقی بماند و مرحلهٔ دو عمداً diffusion ندارد. وضعیت resource فراوان می‌تواند جمعیت را نگه دارد ولی turnover بالاتری ایجاد می‌کند. اینها outcome مدل هستند، نه شکست invariant.

رکورد رسمی freeze در [خط پایهٔ منجمد مرحلهٔ دو](docs/phase-2/phase-two-frozen-baseline.fa.md) ثبت شده است.

### مرحلهٔ سه

مرحلهٔ سه ابتدا ناهمگنی allocation منابع را اضافه کرد و سپس sensing و movement را پیش از ترکیب‌شدن، جداگانه causal-isolate کرد.

یافته‌های پذیرفته‌شدهٔ اصلی:

- مقایسهٔ `uniform` و `center_patch` با ثابت نگه‌داشتن کل resource input، در مدل فعلی persistence/turnover جمعیت و concentration فضایی را تغییر داد؛
- sensing-only بدون movement با موفقیت جدا شد، اما intervalهای انتخاب‌شده advantage جهت‌دار پایداری را نشان ندادند؛
- movement-only جدا شد و بعد representation تکاملی برای step غیرصفر حرکت اضافه شد؛
- یک full campaign یک bug در movement accounting پیدا کرد؛ آن campaign به‌عنوان evidence نهایی رد شد و atomic movement payment پیاده‌سازی شد؛
- campaign اتمیک ۳۰-seed بعدی locomotion واقعی، پرداخت‌شده و reproducible را نشان داد، بدون ادعای navigation یا adaptation.

### مرحلهٔ چهار

پرسش ثبت‌شدهٔ مرحلهٔ چهار:

> آیا اجرای sensing اسکالر منبع محلی، در حالی که locomotion در دسترس است، اجرای movement تکامل‌یافته و outcomeهای فضایی/منبعی را تغییر می‌دهد؟

Full campaign شامل:

۳۰ `seed` matched × ۲ condition × `2000 tick` = ۶۰ اجرای اصلی بود.

در هر دو condition، availability وراثتی sensing/movement، اجرای movement، `movement_step_rate=0.5`، atomic movement payment و environment نوع `center_patch` یکسان بودند. تنها تفاوت causal موردنظر `world.resource_sensing_enabled` بود.

سلامت و exposure:

- اجراهای کامل: `60/60`؛
- شکست validation: `0`؛
- deterministic replay: PASS؛
- sensing operation در control: `0`؛
- sensing operation در treatment: `508`؛
- runهای treatment دارای sensing: `15/30`؛
- runهای treatment دارای هم‌زمانی sensing + movement غیرصفر: `7/30`؛
- run دارای realized movement کم‌پرداخت‌شده: `0`؛
- بیشترین خطای مطلق energy balance: `4.8e-09`؛
- بیشترین خطای مطلق local-resource balance: `6.3e-09`.

هیچ endpoint ثبت‌شدهٔ اجرای movement interval paired تقریبی ۹۵٪ نداشت که صفر را کنار بگذارد. اما سه endpoint ثبت‌شدهٔ spatial/resource صفر را کنار گذاشتند: در treatment میانگین همسایهٔ محلی کمتر، فاصلهٔ نزدیک‌ترین همسایه بیشتر و resource باقی‌مانده در محیط بیشتر بود. یک endpoint ثانویهٔ `active_population` نیز در treatment کمتر بود.

بنابراین تفسیر پذیرفته‌شده محدود است: sensing اسکالر محلی downstream ecological/spatial state را در این مدل به‌صورت causal تغییر داد و نتیجه با `resource-conditioned dynamics` سازگار است، اما campaign تفاوت حل‌شده‌ای در خود locomotor execution نشان نداد. چون `SENSE_RESOURCE` هیچ direction یا gradientی نمی‌دهد، این evidence برای directional navigation یا resource seeking نیست.

برای جزئیات، [گزارش تکمیل مرحلهٔ چهار](docs/phase-4/phase-four-completion-report.fa.md) را ببینید.

## مرزهای پژوهشی

ملاکت همچنان عمداً این موارد را شامل نمی‌شود:

- یادگیری ماشین و شبکهٔ عصبی؛
- هدف هوشمندی؛
- تابع صریح `fitness`؛
- انتخاب دستی organismهای موفق؛
- رفتار حمله یا همکاری نوشته‌شده توسط host؛
- نقش‌های mating، parasite، disease یا کلاس‌های از پیش تعریف‌شدهٔ predator/prey؛
- reward برای complexity؛
- منطق جهت‌دار resource seeking؛
- diffusion منابع یا تولید منابع توسط organism در مدل پذیرفته‌شدهٔ فعلی؛
- دسترسی organismها به filesystem، network، `subprocess`، host runtime یا `API` خارجی.

فرایند Python فقط simulator میزبان است. organismها کد Python اجرا نمی‌کنند.

Evidence فعلی navigation، adaptation، fitness advantage، intelligence، cooperation، predation، multicellularity یا open-ended evolution را اثبات نمی‌کند.

## مستندات

- [فهرست مستندات فارسی](docs/README.fa.md)
- [Documentation index](docs/README.md)
- [گزارش شواهد مرحلهٔ یک](docs/doc-farsi/phase-one-evidence-report.md)
- [گزارش تکمیل و شواهد مرحلهٔ دو](docs/phase-2/phase-two-completion-report.fa.md)
- [خط پایهٔ منجمد مرحلهٔ دو](docs/phase-2/phase-two-frozen-baseline.fa.md)
- [نقشهٔ راه مرحلهٔ سه](docs/phase-3/phase-three-roadmap.fa.md)
- [گیت از پیش ثبت‌شدهٔ مرحلهٔ چهار](docs/phase-4/phase-four-sensing-movement-gate.fa.md)
- [گزارش preflight مرحلهٔ چهار](docs/phase-4/phase-four-sensing-movement-preflight-report.fa.md)
- [گزارش تکمیل مرحلهٔ چهار](docs/phase-4/phase-four-completion-report.fa.md)
- [آرشیو شواهد مرحلهٔ یک](results/phase-one/evidence-gate/README.fa.md)
- `results/phase-two/evidence-gate/` — آرشیو پذیرفته‌شدهٔ مرحلهٔ دو
- `results/phase-four/resource-sensing-with-movement/full/` — آرشیو پذیرفته‌شدهٔ full evidence مرحلهٔ چهار

## ساختار مخزن

- `desktop/src/melakat_desktop/phase_zero_engine.py` — موتور مرجع منجمد جهان همگن؛
- `desktop/src/melakat_desktop/phase_two_engine.py` — موتور منجمد فضایی/محیطی مرحلهٔ دو؛
- `desktop/src/melakat_desktop/phase_two_vm.py` — گسترش داده‌محور VM برای sensing و movement؛
- `desktop/src/melakat_desktop/phase_three_contract.py` — قرارداد ناهمگنی محیطی مرحلهٔ سه؛
- `desktop/src/melakat_desktop/phase_three_engine.py` — مسیر موتور فعلی مرحلهٔ سه، شامل semanticsهای scoped sensing/movement/atomic؛
- `desktop/src/melakat_desktop/phase_three_experiment_support.py` — parameterهای scoped مرحلهٔ سه و compatibility routing؛
- `desktop/src/melakat_desktop/resources.py` — میدان محافظه‌کار منابع و weighted allocation؛
- `desktop/src/melakat_desktop/spatial.py` — topology، placement و spatial measurementها؛
- `desktop/src/melakat_desktop/world_contract.py` — قرارداد منجمد مرحلهٔ دو؛
- `desktop/src/melakat_desktop/experiment_runner.py` — سیستم experiment خودکار نسخه‌گذاری‌شده؛
- `desktop/src/melakat_desktop/ui.py` — رابط پژوهشی دسکتاپ؛
- `results/phase-one/evidence-gate/` — شواهد پذیرفته‌شدهٔ مرحلهٔ یک؛
- `results/phase-two/evidence-gate/` — شواهد پذیرفته‌شدهٔ مرحلهٔ دو؛
- `results/phase-four/resource-sensing-with-movement/` — smoke، preflight و full evidence مرحلهٔ چهار.

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

کارزارهای علمی headless با command نسخه‌گذاری‌شدهٔ `melakat-experiment` اجرا می‌شوند و جدا از runهای interactive دسکتاپ بایگانی می‌شوند.
