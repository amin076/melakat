# مشخصات نهایی Phase 0 — Melakat

نسخه: Phase 0 Final Specification v0.1
وضعیت: نهایی برای طراحی و بررسی؛ اجرای simulator هنوز ممنوع است.

## هدف

ساختن یک جهان محاسباتی کوچک، همگن، محدود و قابل‌بازتولید برای آزمودن self-replication، heredity، mutation و differential reproduction، بدون explicit fitness function یا هدف پیچیدگی.

## قوانین الزام‌آور

- Python فقط host simulator است.
- genome فقط data است و فقط توسط VM محدود تفسیر می‌شود.
- native execution، Python exec/eval، import، filesystem، network، subprocess، runtime و API بیرونی ممنوع است.
- حافظه، انرژی، زمان اجرا و ظرفیت جمعیت محدودند.
- جهان اولیه کوچک و همگن است؛ جمعیت اولیه حدود 10 تا 20 organism است.
- انرژی به‌صورت متوالی از منبع خارجی وارد محیط می‌شود.
- محاسبه، نگهداری و reproduction هزینه دارند.
- mutation اولیه فقط substitution است.
- AI، ML، learning، intelligence، RL، complexity reward، manual selection، attack، cooperation، parasite و geography در V0 ممنوع‌اند.
- نتیجه از قبل تعیین نمی‌شود؛ انقراض، replicator ساده یا divergence هم نتیجه‌ی معتبر است.

## ساختار Phase 0

### 0A — Digital substrate

تعریف bit، byte، number، memory، address، register، state، instruction، opcode، program counter، VM، trap و execution budget.

### 0B — Genome and interpreter

تعریف genome به‌عنوان data، instruction set کمینه، semantics دقیق، خطاها، پرش‌ها و جداسازی کامل از host.

### 0C — Virtual cell/body

هر organism شامل genome، execution state، registers، instruction pointer، allocated memory، internal energy، status و lineage identity است.

### 0D — Signals, energy and reproduction

تعریف environmental resource pool، internal energy، هزینه‌ی instruction، maintenance، memory allocation، copy، division، parent و child.

### 0E — Variation, competition and selection

mutation ارثی، lineage، population، محدودیت منابع و تفاوت آماری در تولیدمثل اندازه‌گیری می‌شوند؛ fitness هرگز به‌عنوان هدف نوشته نمی‌شود.

### 0F — Emergent organization

فقط پس از موفقیت 0A تا 0E، سازمان چندواحدی، همکاری، تقسیم کار یا complexity بررسی می‌شود. هیچ‌کدام در V0 وجود ندارند.

## چهار specification اصلی

- Specification A: Digital–Natural Analogy Matrix
- Specification B: Digital Physics v0
- Specification C: Minimal Instruction Set
- Specification D: Experiment 0 Protocol

این چهار سند باید پیش از Phase 1 منطقی و سازگار باشند.

## قواعد replication

کپی genome، ساخت child memory، mutation، ساخت child state و ثبت lineage باید مراحل جدا باشند. parent و child نباید reference حافظه‌ی پنهان مشترک داشته باشند. replication ناموفق نباید child ناقصِ ثبت‌نشده ایجاد کند.

## Experiment 0

برای هر configuration حداقل 30 run مستقل با seed ثبت‌شده انجام می‌شود. کنترل‌ها:

- mutation = 0
- energy abundant
- memory abundant
- maintenance cost = 0
- reproduction cost = 0

معیارهای ثبت: births، deaths، active population، lineage frequencies، genome length، instruction counts، energy balance، viable offspring، mutation robustness، time to first replication و extinction.

## معیار عبور به Phase 1

Phase 1 فقط وقتی مجاز است که:

1. semantics تمام instructionها نوشته و دستی بررسی شده باشد.
2. رفتار memory bounds، overflow، trap و execution budget مشخص باشد.
3. replication و استقلال parent/child آزمون طراحی داشته باشند.
4. اجرای یک seed ثابت بازتولید شود.
5. کنترل‌های Experiment 0 تعریف شده باشند.
6. هیچ مسیر دسترسی organism به host وجود نداشته باشد.
7. تفاوت میان observed result و interpretation در گزارش ثبت شود.

## اصل نهایی

هر قانون باید به یک نیاز روشن در digital world مربوط باشد، قابل‌آزمون باشد و نتیجه‌ی مطلوب را از قبل تحمیل نکند.
