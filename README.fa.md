# ملاکت

[English](README.md)

«ملاکت» یک شبیه‌ساز پژوهش‌محور برای تکامل دیجیتال است. organismهای ساده و داده‌محور داخل یک `Virtual Machine` محدود اجرا می‌شوند، انرژی و حافظهٔ محدود مصرف می‌کنند، genome وراثتی خود را کپی می‌کنند، mutation دارند، تولیدمثل می‌کنند و می‌میرند. مراحل بعدی فضا، منابع محلی، ناهمگنی محیط، sensing اسکالر منبع، movement محدود و اکنون **طول متغیر و وراثتی genome** را اضافه کرده‌اند—بدون `fitness function` صریح، کنترل‌گر `Machine Learning`، انتخاب دستی یا رفتار اجتماعی از پیش نوشته‌شده.

## وضعیت فعلی

**Phase Zero تا Phase Five کامل شده‌اند.** baselineهای پذیرفته‌شدهٔ قدیمی منجمد و reproducible باقی مانده‌اند و مراحل بعدی با contractهای مستقل و versioned آنها را گسترش داده‌اند، نه اینکه بی‌صدا بازنویسی‌شان کنند.

مهم‌ترین milestoneها:

- **Phase Zero** — VM محدود، self-copy/division واقعی، energy/memory محدود، تولد و مرگ.
- **Phase One** — instrumentation جهان همگن و evidence campaign شامل ۹۹۰ run.
- **Phase Two** — فضای 2D، resource محلی، substrate sensing/movement و evidence پذیرفته‌شدهٔ ۳۶۰-run؛ Phase Two رسماً frozen است.
- **Phase Three** — ناهمگنی کنترل‌شدهٔ resource، causal isolation sensing/movement، step غیرصفر تکامل‌پذیر حرکت و atomic movement payment.
- **Phase Four** — causal gate شامل ۶۰ run matched برای sensing در حضور movement. sensing downstream ecological/spatial state را تغییر داد، اما effect حل‌شده‌ای روی خود locomotor execution یا directional navigation نشان نداد.
- **Phase Five** — replication مقاوم به تغییر طول همراه با tandem duplication/deletion کور. full campaign شامل ۶۰ run نشان داد **طول متغیر genome وراثتی است**: organismهای variable-length متولد شدند و تعدادی از آنها خودشان بعداً reproduction انجام دادند.

## نسخه‌های فعلی Phase Five

- world contract: `phase-five-evolvability-0.1`
- structural engine: `phase-five-vm-0.2`
- structural measurement: `phase-five-measurement-0.2`
- structural RNG: `phase-five-structural-rng-0.1`

substrate replication مرحلهٔ پنج از self-copy ترتیبی `COPY_NEXT` و flow control مبتنی بر template (`NOP_A`، `NOP_B`، `JUMP_TEMPLATE`، `JUMP_TEMPLATE_IF_ZERO`) استفاده می‌کند؛ بنابراین replication loop دیگر طول genome یا آدرس مطلق loop را hard-code نمی‌کند.

## Evidence پذیرفته‌شدهٔ Phase Five

### Gate 5C — exposure calibration

نرخ‌های candidate برابر `0.01`، `0.025`، `0.05` و `0.10` بودند. طبق قانون pre-registered، **کمترین** نرخی انتخاب شد که exposure کافی بدهد؛ outcome مطلوب تکاملی یا زیستی حق دخالت در انتخاب نداشت.

- `0.01`: ۱۱ event committed — FAIL
- `0.025`: ۲۶ event، exposure در ۷/۸ run، ۱۲ duplication و ۱۴ deletion — **انتخاب شد**
- `0.05`: ۵۰ event — PASS اما عمداً انتخاب نشد
- `0.10`: ۸۳ event — PASS اما عمداً انتخاب نشد

### Gate 5D — full variable-genome campaign

- ۳۰ `seed` matched × ۲ condition × ۲۰۰۰ tick = **۶۰ run اصلی**
- نرخ structural event در control: `0.0`
- نرخ structural event در treatment: `0.025`
- احتمال balanced duplication/deletion: `0.5`
- run کامل: `60/60`
- validation failure: `0`
- deterministic replay: PASS
- بیشترین خطای مطلق energy balance: `4.36e-08` با tolerance برابر `1e-07`
- structural event در control: `0`
- structural event در treatment: `97`
- duplication در treatment: `42`
- deletion در treatment: `55`
- runهای treatment دارای structural event: `29/30`
- variable-length birth: `61`
- organismهای variable-length که بعداً خودشان reproduction کردند: `12`
- runهای treatment با variable-length organism فعال در پایان: `14/30`

طول ancestor برابر `14` است. genomeهای فعال control همگی طول `14` داشتند؛ در treatment طول‌های `13`، `14` و `15` مشاهده شد. میانگین طول تقریباً همان `14` باقی ماند؛ یعنی intervention dimension وراثتی طول را باز کرد، نه اینکه genome را مجبور به رشد یک‌طرفه کند.

جزئیات در [گزارش تکمیل Phase Five](docs/phase-5/phase-five-completion-report.fa.md) و [نقشهٔ راه Phase Five](docs/phase-5/phase-five-evolvability-roadmap.fa.md) آمده است.

## مرزهای علمی

ملاکت عمداً genome size یا complexity را reward نمی‌کند. genome بلندتر به‌طور طبیعی structural memory بیشتری مصرف می‌کند و copying/execution بیشتری می‌خواهد؛ genome کوتاه‌تر ممکن است instruction مفید یا ضروری را از دست بدهد. host هیچ critical instructionی را محافظت نمی‌کند و organism موفق را دستی انتخاب نمی‌کند.

Evidence فعلی **این موارد را ثابت نمی‌کند**:

- افزایش functional complexity؛
- بهتر بودن genome بزرگ‌تر؛
- adaptation یا fitness advantage؛
- intelligence؛
- directional navigation یا resource seeking؛
- cooperation، predation، communication یا multicellularity؛
- open-ended evolution.

**Variable genome length یک complexity metric نیست.** هر ادعای آینده دربارهٔ complexity باید measurement مستقل functional/algorithmic/behavioral داشته باشد.

## قابلیت‌های اصلی

- `Virtual Machine` محدود و داده‌محور؛
- self-copy و division واقعی؛
- blind hereditary opcode mutation؛
- single-instruction tandem duplication/deletion کور در Phase Five؛
- genomeهای variable-length و وراثتی؛
- genealogy، lineage و genotype tracking؛
- energy و structural memory محدود؛
- هزینهٔ صریح execution، maintenance و reproduction؛
- runهای deterministic بر پایهٔ seed و conservation ledger؛
- فضای 2D پیوسته با مرزهای `reflective` / `toroidal`؛
- منابع محافظه‌کار cell-local؛
- ناهمگنی deterministic نوع `center_patch`؛
- instructionهای `SENSE_RESOURCE`، `MOVE_X` و `MOVE_Y`؛
- step غیرصفر تکامل‌پذیر movement و atomic movement payment؛
- experiment specهای versioned، exportهای JSON/CSV، provenance و SHA-256 manifest؛
- matched-seed paired evidence analysis.

## مستندات و Evidence

- [فهرست مستندات فارسی](docs/README.fa.md)
- [Documentation index](docs/README.md)
- [خط پایهٔ منجمد Phase Two](docs/phase-2/phase-two-frozen-baseline.fa.md)
- [گزارش تکمیل Phase Four](docs/phase-4/phase-four-completion-report.fa.md)
- [نقشهٔ راه Evolvability در Phase Five](docs/phase-5/phase-five-evolvability-roadmap.fa.md)
- [گزارش تکمیل Phase Five](docs/phase-5/phase-five-completion-report.fa.md)
- `results/phase-one/evidence-gate/` — evidence پذیرفته‌شدهٔ Phase One
- `results/phase-two/evidence-gate/` — evidence پذیرفته‌شدهٔ Phase Two
- `results/phase-four/resource-sensing-with-movement/full/` — evidence پذیرفته‌شدهٔ Phase Four
- `results/phase-five/structural-event-rate-calibration/` — calibration مرحلهٔ پنج
- `results/phase-five/variable-genome-full/` — full evidence مرحلهٔ پنج

## نقشهٔ repository

- `desktop/src/melakat_desktop/phase_zero_engine.py` — موتور مرجع همگن منجمد
- `desktop/src/melakat_desktop/phase_two_engine.py` — موتور منجمد فضایی/resource محلی
- `desktop/src/melakat_desktop/phase_three_engine.py` — مسیر evidence محیط/sensing/movement
- `desktop/src/melakat_desktop/phase_five_vm.py` — VM مقاوم به تغییر طول genome
- `desktop/src/melakat_desktop/phase_five_engine.py` — موتور variable-genome مرحلهٔ پنج
- `desktop/src/melakat_desktop/phase_five_experiment_support.py` — routing/metrics آزمایش‌های Phase Five
- `desktop/src/melakat_desktop/experiment_runner.py` — سیستم عمومی experiment reproducible
- `desktop/src/melakat_desktop/ui.py` — رابط پژوهشی desktop

## اجرای محلی

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
