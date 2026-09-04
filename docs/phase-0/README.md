# مرحلهٔ صفر: محیط دیجیتال پیش از کدنویسی

تا زمانی که substrate دیجیتال، قوانین جهان و آزمایش‌ها دقیق، منطقی و قابل‌آزمون نشده‌اند، implementation شبیه‌ساز آغاز نمی‌شود.

## سند پیش‌نیاز

قبل از این مرحله، [مبانی محیط‌های دیجیتال](../foundations/digital-environment-basics.md) را بخوانید. این سند درباره‌ی bit، byte، memory، address، CPU، program، process، interpreter، VM، execution، copy، clone، replication، scheduler، randomness و رابطه‌ی سخت‌افزار و نرم‌افزار است.

## مسیر Phase 0

### Phase 0A — Digital substrate

باید این مفاهیم پایه مشخص شوند:

- bit و byte؛
- نمایش عدد و دامنه‌ی مقدار؛
- memory و address؛
- register و state؛
- instruction و opcode؛
- program counter یا instruction pointer؛
- fetch، decode و execute؛
- VM و مرز آن با host؛
- ظرفیت محدود و رفتار overflow یا خطا.

### Phase 0B — Genome representation and interpreter

باید مشخص شود:

- genome چگونه به‌عنوان data ذخیره می‌شود؛
- چه تفاوتی میان genome، program، process و organism وجود دارد؛
- interpreter چگونه instructionها را اجرا می‌کند؛
- کدام instructionها مجازند؛
- دستور نامعتبر چه نتیجه‌ای دارد؛
- genome چگونه از native execution جدا می‌ماند؛
- دسترسی به OS، filesystem، network، subprocess، runtime و API بیرونی چگونه ممنوع می‌شود.

### Phase 0C — Virtual cell/body

باید حداقل body دیجیتال تعریف شود:

- genome؛
- execution state؛
- private یا allocated memory؛
- registers؛
- instruction pointer؛
- internal resource budget؛
- وضعیت active، stopped یا dead؛
- مرز دسترسی موجود.

در این مرحله نباید ادعا کنیم که یک سلول زیستی واقعی ساخته‌ایم. این فقط یک analogue عملکردی و قابل‌آزمون است.

### Phase 0D — Signals, energy and reproduction

باید تعریف شوند:

- ورودی متوالی انرژی به محیط؛
- environmental resource pool؛
- internal usable energy؛
- هزینه‌ی execution و maintenance؛
- signalهای مجاز جهان؛
- memory allocation؛
- copy و division؛
- فرزند و والد؛
- شرایط شکست تولیدمثل.

### Phase 0E — Variation, competition and selection

باید بررسی شود:

- mutation چگونه رخ می‌دهد؛
- mutation اولیه فقط substitution باشد؛
- کدام تغییرات ارثی‌اند؛
- محدودیت انرژی و memory چگونه تفاوت تولیدمثل ایجاد می‌کند؛
- competition دقیقاً بر سر چیست؛
- natural selection چگونه فقط اندازه‌گیری می‌شود، نه اینکه به‌صورت fitness function هدف‌گذاری شود؛
- lineage و population چگونه ثبت می‌شوند.

در این مرحله هنوز attack، cooperation، parasite، geography و رفتار اجتماعی صریح وارد نمی‌شوند، مگر اینکه specification و آزمایش جداگانه آن را توجیه کند.

### Phase 0F — Multi-cellularity and emergent complexity

این مرحله عمداً بعد از اعتبارسنجی مراحل قبل قرار دارد. در آن می‌توانیم بررسی کنیم:

- آیا چند واحد می‌توانند سازمان پایدار بسازند؛
- آیا cooperation یا division of labor بدون instruction جادویی ظاهر می‌شود؛
- آیا complexity یا novelty پیامد قوانین است؛
- چه چیزی واقعاً emergent است و چه چیزی از قبل در مدل نوشته شده است.

هیچ نتیجه‌ای درباره‌ی multicellularity یا complexity پیش از تکمیل مراحل قبلی پذیرفته نمی‌شود.

## چهار specification اجباری

### Specification A — Digital–Natural Analogy Matrix

برای هر مفهوم طبیعی ثبت می‌شود:

- نقش آن در جهان واقعی چیست؟
- آیا برای حیات یا تکامل بنیادی است یا فقط یک ویژگی فرعی است؟
- analogue دیجیتال پیشنهادی چیست؟
- چه چیزی در این analogy از بین می‌رود؟
- آیا نسخه‌ی حداقلی آن برای آزمایش لازم است؟
- چه پیش‌بینی قابل‌آزمونی تولید می‌کند؟

### Specification B — Digital Physics v0

باید state، زمان و قوانین پایه را تعریف کند:

- فضای حافظه و ظرفیت آن؛
- واحد زمان و ترتیب اجرای tick؛
- ورود انرژی در هر tick؛
- هزینه‌ی اجرای instruction؛
- هزینه‌ی نگهداری و تکثیر؛
- قوانین برخورد با کمبود انرژی یا حافظه؛
- مرز قطعی بین organism و simulator؛
- قوانین مرگ و آزادشدن منابع.

### Specification C — Minimal Instruction Set

هر instruction باید دلیل وجودی روشن داشته باشد.

در نسخه‌ی اولیه instructionهایی مانند LEARN، ATTACK، COOPERATE، EVOLVE، OPTIMIZE یا FIND_ENERGY مجاز نیستند.

وجود یک instruction جادویی مانند REPRODUCE نیز باید با احتیاط بررسی شود؛ تکثیر باید تا حد امکان از تعامل محدود instructionها با VM و منابع پدیدار شود.

### Specification D — Experiment 0 Protocol

پروتکل باید از قبل مشخص کند:

- اندازه‌ی جهان؛
- مقدار انرژی ورودی در هر tick؛
- تعداد اولیه‌ی organismها، ترجیحاً ۱۰ تا ۲۰؛
- genome اولیه؛
- نرخ mutation؛
- تعداد runهای مستقل؛
- seedهای تصادفی؛
- معیارهای ثبت داده؛
- شرایط توقف؛
- تعریف موفقیت، شکست و نتیجه‌ی خنثی؛
- آزمون‌های control برای جداکردن اثر هر قانون.

## ترتیب اعتبارسنجی

1. سند مبانی محیط دیجیتال و منطق Phase 0A بررسی می‌شود.
2. هر specification به‌صورت مستقل بررسی می‌شود.
3. وابستگی‌ها و تناقض‌های بین specificationها بررسی می‌شوند.
4. پیش‌بینی‌های قابل‌آزمون استخراج می‌شوند.
5. پروتکل با اجرای دستی یا مدل کاغذی کوچک بررسی می‌شود.
6. فقط پس از تأیید، Phase 1 و prototype Python آغاز می‌شود.

## پرسش محافظ

در هر مرحله باید بتوانیم پاسخ دهیم:

> آیا این قانون واقعاً از نیازهای یک جهان تکاملی می‌آید، یا فقط برای نزدیک‌کردن نتیجه به چیزی که دوست داریم اضافه شده است؟
