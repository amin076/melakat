# سامانهٔ آزمایش خودکار ملاکت — نسخهٔ ۱

رابط دسکتاپ ملاکت برای مشاهده، inspect کردن و بازتولید یک اجرای مشخص مناسب است؛ اما نباید ابزار اصلی برای صدها یا هزاران اجرای علمی باشد. `Automated Experiment System v1` یک runner بدون GUI و بازتولیدپذیر برای آزمایش‌های چندشرطی و چند-`seed` فراهم می‌کند.

## هدف‌ها

این سامانه می‌تواند:

- آزمایش را با specification نسخه‌گذاری‌شدهٔ JSON یا YAML تعریف کند؛
- conditionهای تطبیقی را بدون باز کردن GUI اجرا کند؛
- مجموعهٔ صریح `seed`ها یا یک بازهٔ پیوسته را اجرا کند؛
- sweep تک‌پارامتری یا چندپارامتری را گسترش دهد؛
- invariantهای انرژی، منبع محلی و فضا را برای هر run بررسی کند؛
- یک جفت condition/seed را دقیقاً دوباره اجرا کند تا determinism بررسی شود؛
- آمار conditionها را تجمیع کند؛
- artifactهای CSV/JSON همراه provenance و checksumهای SHA-256 بسازد؛
- campaign کوچک را در CI و campaign پژوهشی بزرگ‌تر را با GitHub Actions اجرا کند.

این runner هیچ قانون شبیه‌سازی را تغییر نمی‌دهد و فقط موتورهای موجود را orchestrate می‌کند.

## CLI

پس از نصب package دسکتاپ، specification را بررسی کنید:

```powershell
cd desktop
python -m pip install -e .
cd ..
melakat-experiment validate experiments/phase-two/local-resource-energy-sweep.json
```

سپس campaign را اجرا کنید:

```powershell
melakat-experiment run experiments/phase-two/local-resource-energy-sweep.json `
  --output-dir results/automated-experiments/local-resource-energy
```

برای smoke test در CI می‌توان بدون دست‌کاری specification تعداد seed و tick را موقتاً کم کرد:

```powershell
melakat-experiment run experiments/phase-two/local-resource-energy-sweep.json `
  --seed-count 3 `
  --ticks 300 `
  --output-dir results/automated-experiments/smoke
```

گزینهٔ `--seed-start` نیز در دسترس است.

## specification آزمایش

قالب فعلی:

```text
melakat-experiment-spec-0.1
```

هر specification شامل این بخش‌هاست:

- `name` و `description` اختیاری؛
- `base_config` برای override کردن پارامترهای ملاکت؛
- `seeds` به‌صورت لیست صریح یا `{start, count}`؛
- `conditions` اختیاری برای وضعیت‌های تطبیقی نام‌گذاری‌شده؛
- `sweeps` اختیاری برای ساخت conditionهای حاصل از parameter grid؛
- `reproducibility` اختیاری برای تعیین condition و seed تکرارشونده.

نام پارامتر ناشناخته رد می‌شود تا typo یا config اشتباه به‌صورت خاموش وارد پژوهش نشود.

JSON بدون dependency اضافی کار می‌کند. برای YAML از `PyYAML` استفاده می‌شود که در dependencyهای عادی package دسکتاپ قرار دارد.

## خروجی campaign

هر campaign کامل این فایل‌ها را می‌سازد:

- `campaign.json` — plan نهایی، runهای فشرده، summary و validation؛
- `runs.csv` — یک ردیف برای هر run؛
- `summary.json` — آمار هر condition و delta نسبت به condition اول؛
- `comparison.csv` — جدول تجمیعی conditionها؛
- `validation.json` — نتایج invariantها و reproducibility؛
- `provenance.json` — نسخهٔ Python، platform، hash specification و metadata گیت‌هاب در صورت وجود؛
- `SHA256SUMS.txt` — checksum تمام خروجی‌های اصلی.

اگر invariant بشکند، run خطای اجرایی بدهد، run مورد انتظار گم شود یا deterministic repeat یکسان نباشد، فرمان با status غیرصفر پایان می‌یابد.

## GitHub Actions

workflow جدید `.github/workflows/melakat-experiments.yml` دو حالت دارد:

1. **PR/main smoke** — سه seed و ۳۰۰ tick برای sweep انرژی مرحلهٔ دو؛
2. **Manual research campaign** — با `workflow_dispatch` مسیر specification، تعداد seed و تعداد tick دریافت می‌شود. حالت پیش‌فرض ۳۰ seed و ۲۰۰۰ tick است.

خروجی‌ها به‌عنوان artifact workflow نگهداری می‌شوند و به‌طور خودکار روی `main` commit نمی‌شوند.

## نخستین campaign ثبت‌شده

`experiments/phase-two/local-resource-energy-sweep.json` همان آزمایش منابع محلی است که از تست دستی ما به وجود آمد:

- spatial rules: روشن؛
- local resources: روشن؛
- evolved sensing/movement: خاموش؛
- resource grid: `10 × 7`؛
- world: `96 × 70`؛
- offspring dispersion radius: `1.4`؛
- energy input per tick: `10.4`، `20.0` و `40.0`؛
- seedهای `1..30`؛
- `2000 tick`.

در نتیجه campaign کامل ۹۰ run دارد. هدف آن اندازه‌گیری اثر نرخ تجدید انرژی محلی بر بقا و turnover است، بدون آنکه movement به‌عنوان confound وارد شود.

## نقش Keynu

این runner عمداً مرز علمی پایدار برای اتصال آیندهٔ Keynu است. `MelakatDriver` بهتر است CLI را صدا بزند و artifactهای آن را بخواند، نه اینکه با mouse روی GUI کلیک کند. به این ترتیب repository ملاکت، specificationهای آزمایش و artifactهای نتیجه، source of truth علمی باقی می‌مانند.
