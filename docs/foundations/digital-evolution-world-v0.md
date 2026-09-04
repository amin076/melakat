# Digital Evolution World

## سند بنیادی پروژه برای مطالعهٔ تکامل آزاد نرم‌افزار در یک جهان دیجیتال محدود

**نسخه:** Concept & Research Foundation v0.1
**زبان پیاده‌سازی اولیه:** Python
**وضعیت:** Research / Experimental
**هدف اولیه:** طراحی یک جهان محاسباتی ساده، محدود و همگن که در آن برنامه‌های بسیار ابتدایی بتوانند تکثیر شوند، با تغییرات کوچک وراثتی نسل ایجاد کنند، برای منابع محدود رقابت کنند و بدون هدف تکاملی از پیش تعیین‌شده تحت انتخاب طبیعی دیجیتال قرار گیرند.

---

# 1. ایدهٔ اصلی

این پروژه تلاش برای شبیه‌سازی زیست‌شناسی زمین نیست.

قرار نیست با Python یک باکتری، سلول، انسان، اکوسیستم یا سیارهٔ زمین را شبیه‌سازی کنیم.

موضوع اصلی پروژه این است:

**آیا می‌توان برای نرم‌افزار یک «طبیعت» ساخت؟**

طبیعتی که در آن برنامه‌های بسیار ساده بتوانند:

- وجود داشته باشند؛
- برای ادامهٔ فعالیت به منابع نیاز داشته باشند؛
- انرژی مصرف کنند؛
- خود را تکثیر کنند؛
- هنگام تکثیر مقدار کمی تغییر کنند؛
- ویژگی‌های خود را به نسل بعد منتقل کنند؛
- برای فضای محدود و انرژی محدود رقابت کنند؛
- بمیرند؛
- و در طول تعداد بسیار زیادی نسل تحت selection قرار گیرند.

اما مهم‌ترین شرط پروژه این است:

> **ما نباید مشخص کنیم evolution باید به چه چیزی برسد.**

هدف موجودات نباید intelligence باشد.

هدف نباید Machine Learning باشد.

هدف نباید neural network باشد.

هدف نباید افزایش complexity باشد.

هدف نباید ساخت برنامهٔ بزرگ‌تر باشد.

هدف نباید cooperation، aggression، parasitism یا multicellularity باشد.

حتی اگر پس از میلیون‌ها نسل موجودات از ancestor اولیه ساده‌تر شوند، این نتیجه باید پذیرفته شود.

سؤال آزمایش این است:

**چه اتفاقی می‌افتد؟**

نه:

**چگونه آنها را مجبور کنیم به چیزی که می‌خواهیم تبدیل شوند؟**

---

# 2. فرضیهٔ بنیادی

آزمایش از یک یا تعداد اندکی **Minimal Digital Replicator** آغاز می‌شود.

به صورت مفهومی:

```text
Minimal Digital Program
        +
Finite Digital Environment
        +
Continuous Energy Input
        +
Energy Consumption
        +
Finite Space
        +
Imperfect Replication
        +
Heritable Variation
        +
Competition
        +
Death
        ↓
        ?

```

علامت سؤال مهم‌ترین بخش پروژه است.

نباید از قبل با:

```text
AI
Complex Software
Super-Agent
Neural Network

```

جایگزین شود.

اگر نتیجه فقط مجموعه‌ای از replicatorهای کوچک باشد، آن هم نتیجهٔ معتبر آزمایش است.

---

# 3. چرا برای طراحی جهان دیجیتال، زیست‌شناسی را مطالعه می‌کنیم؟

ما قصد شبیه‌سازی زیست‌شناسی نداریم.

اما زمین تنها نمونه‌ای است که می‌دانیم در آن یک فرایند evolutionary بسیار طولانی توانسته از سیستم‌های بسیار ساده به تنوع عظیمی از ساختارها و رفتارها برسد.

بنابراین از طبیعت به‌عنوان **راهنمای طراحی قوانین** استفاده می‌کنیم، نه به‌عنوان چیزی که باید کپی شود.

روش کار باید چنین باشد:

```text
Natural principle
       ↓
Why is it important?
       ↓
Abstract principle
       ↓
Possible digital analogue
       ↓
Is the analogue necessary?
       ↓
Implement the minimum version

```

مثلاً نباید بگوییم:

> زمین خورشید دارد، پس simulation ما هم باید خورشید سه‌بعدی داشته باشد.

بلکه می‌پرسیم:

> نقش بنیادی خورشید چیست؟

یکی از پاسخ‌ها:

**ورود پیوستهٔ free energy به یک سیستم باز.**

پس digital analogue ممکن است فقط این باشد:

```text
Environment receives X energy units / tick

```

بدون هیچ خورشید گرافیکی.

---

# 4. اصل مهم: Functional Analogy، نه Visual Analogy

ما به شباهت ظاهری نیاز نداریم.

نیازی نیست:

- کوه بسازیم؛
- آب بسازیم؛
- خورشید render کنیم؛
- سلول را گرد بکشیم؛
- DNA گرافیکی بسازیم.

آنچه اهمیت دارد **نقش عملکردی** پدیده‌های طبیعی است.

بنابراین:

**Sun → external energy flux**

نه تصویر خورشید.

**ATP → spendable internal energy**

نه مولکول ATP.

**DNA → heritable executable information**

نه رشتهٔ A/C/G/T.

**Cell membrane → protected computational boundary**

نه غشای چربی.

**Metabolism → resource-to-usable-energy transformation**

نه glycolysis شیمیایی.

این distinction باید در تمام پروژه حفظ شود.

---

# 5. درس اول از شیمی و زیست‌شناسی: حیات سیستم بسته نیست

زمین مادهٔ تقریباً محدودی دارد، اما انرژی دائماً وارد و خارج می‌شود.

در زیست‌شناسی، موجود زنده برای حفظ ساختار خود باید دائماً انرژی آزاد دریافت و مصرف کند.

سلول نمی‌تواند صرفاً یک بار «انرژی دریافت کند» و برای همیشه زنده بماند.

فعالیت‌های سلولی هزینه دارند.

در زیست‌شناسی مدرن ATP یکی از حامل‌های اصلی free energy قابل استفاده در سلول است. واکنش‌های انرژی‌زا می‌توانند با تولید ATP و واکنش‌های انرژی‌خواه با مصرف آن coupled شوند.

در جهان دیجیتال ما اصل انتزاعی چنین خواهد بود:

> **Computation must not be free.**

هر فعالیت محاسباتی باید هزینه داشته باشد.

---

# 6. خورشید دیجیتال

نسخهٔ اولیهٔ جهان homogeneous است.

بنابراین هیچ منطقه‌ای نور بیشتر یا کمتر دریافت نمی‌کند.

در هر simulation tick مقدار مشخصی انرژی وارد جهان می‌شود:

```text
E_world(t+1) =
E_world(t)
+ E_input
- E_consumed
- E_dissipated

```

این `E_input` معادل عملکردی ورود انرژی خورشیدی/ژئوشیمیایی است.

اما انرژی نباید مستقیماً به‌طور مساوی داخل تمام موجودات ریخته شود؛ زیرا در آن صورت competition ضعیف می‌شود.

باید یک **environmental energy pool** وجود داشته باشد و موجودات برای capture کردن سهمی از آن با محدودیت مواجه شوند.

در V0 جهان homogeneous است، بنابراین احتمال دسترسی اولیه به انرژی از نظر مکانی یکسان خواهد بود.

---

# 7. ATP دیجیتال

در طبیعت، داشتن انرژی در محیط با داشتن انرژی قابل مصرف داخل سلول یکی نیست.

این distinction بسیار ارزشمند است.

بنابراین بهتر است دو مفهوم داشته باشیم:

### Environmental Energy

انرژی موجود در محیط.

### Internal Energy

انرژی‌ای که یک Digital Organism توانسته به دست آورد و اکنون می‌تواند خرج کند.

پس:

```text
Environment Energy
        ↓ capture
Organism Internal Energy
        ↓
execution
copying
maintenance
reproduction
interaction

```

این internal energy را می‌توانیم فعلاً صرفاً `energy` بنامیم.

لازم نیست واقعاً ATP شبیه‌سازی کنیم.

---

# 8. اصل Maintenance Energy

مطالعات microbial bioenergetics نشان می‌دهند حتی سلول‌هایی که رشد نمی‌کنند برای حفظ عملکردهای اساسی خود به حداقلی از energy flux نیاز دارند.

این ایده برای جهان ما بسیار مهم است.

یک برنامه نباید بتواند برای همیشه در memory بنشیند و هیچ هزینه‌ای نپردازد.

بنابراین دو هزینه را جدا می‌کنیم:

### Activity Cost

هزینهٔ اجرای instructions.

### Maintenance Cost

هزینهٔ ادامهٔ موجودیت.

مثلاً:

```text
every tick:
    organism.energy -= maintenance_cost

```

و:

```text
for every executed instruction:
    organism.energy -= instruction_cost

```

اگر:

```text
energy <= 0

```

موجود دیگر قادر به حفظ state خود نیست و می‌میرد.

این قانون می‌تواند pressure بسیار مهمی ایجاد کند:

یک genome بزرگ یا inefficient باید واقعاً هزینهٔ بیشتری تحمل کند.

---

# 9. مرز سلول در جهان دیجیتال

یکی از بنیادی‌ترین ویژگی‌های سلول biological compartmentalization است.

Membrane باعث می‌شود:

- داخل از خارج جدا شود؛
- اطلاعات حفظ شود؛
- واکنش‌های داخلی local بمانند؛
- منابع کنترل شوند؛
- و organism یک واحد نسبتاً مستقل شود.

Digital Organism نیز به یک boundary نیاز دارد.

اما boundary نباید لزوماً absolute باشد.

هر organism باید حداقل دارای:

```text
Organism
 ├── genome
 ├── internal state
 ├── registers
 ├── instruction pointer
 ├── internal energy
 └── allocated memory

```

باشد.

در V0 موجودات احتمالاً نمی‌توانند memory یکدیگر را تغییر دهند.

اما architecture باید از ابتدا طوری طراحی شود که در experiments آینده بتوان permeability این boundary را تغییر داد.

چرا؟

چون بعداً می‌خواهیم ببینیم آیا از interactionهای ساده ممکن است:

- parasitism
- exploitation
- defence
- cooperation
- resource theft
- symbiosis

پدید آید.

---

# 10. Genome دیجیتال

Genome نباید Python source code باشد.

این تصمیم بنیادی است.

Python زبان **Simulator** است.

Digital Organism باید داخل یک Virtual Machine اختصاصی زندگی کند.

مثلاً genome:

```text
[
  READ,
  COPY,
  MOVE,
  IF,
  JUMP,
  ...
]

```

باشد.

هر instruction باید توسط VM خودمان تفسیر شود.

این کار سه دلیل دارد.

اول: امنیت.

Digital organism نباید به:

- OS
- filesystem
- network
- subprocess
- Python runtime
- external APIs

دسترسی داشته باشد.

دوم: evolvability.

یک mutation تصادفی در Python source معمولاً syntax را خراب می‌کند.

اما می‌توان instruction set را طوری طراحی کرد که mutationهای کوچک احتمال معقولی برای ایجاد برنامهٔ قابل اجرا داشته باشند.

سوم: physics.

اگر organisms Python باشند، بخش عظیمی از «قوانین طبیعت» آنها را CPython، operating system و libraries تعیین می‌کنند.

ما می‌خواهیم قوانین جهان خودمان را تعریف کنیم.

---

# 11. Instruction Set باید بسیار کوچک باشد

یکی از حساس‌ترین تصمیمات کل پروژه همین است.

اگر instructionهای خیلی قدرتمند قرار دهیم، نتیجه را از قبل وارد genome کرده‌ایم.

نباید چنین چیزهایی داشته باشیم:

```text
LEARN
ATTACK
COOPERATE
EVOLVE
OPTIMIZE
FIND_ENERGY
BUILD_AI
NEURAL_NETWORK

```

حتی `REPRODUCE` به‌عنوان یک instruction جادویی مشکوک است.

بهتر است reproduction نتیجهٔ ترکیب primitive operations باشد.

مثلاً candidate primitives:

```text
NOP
READ
WRITE
COPY
MOVE
JUMP
IF
ALLOCATE
DIVIDE

```

ولی این لیست هنوز نهایی نیست.

**اولین کار مهندسی پروژه باید طراحی و نقد دقیق Instruction Set باشد.**

هر instruction باید با این سؤال بررسی شود:

> آیا این یک قانون بنیادی جهان است یا داریم یک رفتار سطح بالا را از قبل به evolution هدیه می‌دهیم؟

---

# 12. موجود اولیه

ما فعلاً Digital Abiogenesis آزمایش نمی‌کنیم.

یعنی انتظار نداریم random bytes خودشان replication را کشف کنند.

Experiment اولیه **Digital Evolution** است.

بنابراین یک Minimal Replicator را خودمان می‌نویسیم.

وظیفهٔ آن تا حد ممکن فقط این باشد:

```text
identify/copy genome
        ↓
allocate offspring space
        ↓
copy instructions
        ↓
divide

```

نباید دارای:

- intelligence
- strategy
- attack
- defence
- communication
- learning
- optimization logic

باشد.

این موجود Digital Ancestor پروژه است.

---

# 13. تولد

Birth زمانی رخ می‌دهد که یک organism بتواند:

1. فضای لازم را به دست آورد؛
2. genome جدید بسازد؛
3. حداقل energy لازم را تأمین کند؛
4. عملیات division را کامل کند.

بنابراین reproduction باید **هزینه‌دار** باشد.

Genome دو برابر بزرگ‌تر باید به‌طور طبیعی copying بیشتری بخواهد.

این موضوع بسیار مهم است، زیرا complexity نباید رایگان باشد.

---

# 14. Mutation

Replication کامل نیست.

برای هر instruction هنگام copy احتمال بسیار کوچکی وجود دارد:

```text
P_mutation = μ

```

در V0 فقط:

### substitution mutation

خواهیم داشت.

مثلاً:

```text
Parent:
A B C D E F

Child:
A B C X E F

```

در نسخه‌های بعد می‌توان اضافه کرد:

- insertion
- deletion
- duplication
- transposition
- recombination

اما نه در اولین آزمایش.

مهم:

**Mutation نباید بداند چه تغییری مفید است.**

کاملاً blind است.

---

# 15. وراثت

اگر mutation در genome فرزند ایجاد شد، همان genome جدید باید در reproductionهای بعدی آن lineage منتقل شود.

بنابراین:

```text
P0
 ↓
P1
 ↓
P2
 ↓
P3

```

تاریخچهٔ lineage قابل بازسازی خواهد بود.

بدون heredity، evolution واقعی نداریم.

---

# 16. انرژی و انتخاب طبیعی

هیچ fitness function صریحی نمی‌نویسیم.

ممنوع:

```python
fitness = intelligence_score

```

ممنوع:

```python
fitness = complexity

```

ممنوع:

```python
fitness = genome_size

```

ممنوع:

```python
fitness = desired_behavior

```

Fitness باید **implicit** باشد.

یعنی اگر lineageای در قوانین جهان بهتر توانست باقی بماند و offspring تولید کند، population آن افزایش می‌یابد.

به زبان ساده:

```text
survive + reproduce

```

نتیجه است، نه score داده‌شده توسط ما.

---

# 17. فضای محدود

زمین ظرفیت نامحدود ندارد.

Digital World هم نباید داشته باشد.

فرض اولیه:

```text
WORLD_MEMORY = fixed

```

مثلاً:

```text
10,000 memory units

```

اگر organisms تمام memory را اشغال کنند، offspring جدید نمی‌تواند بدون آزادشدن فضا ساخته شود.

در نتیجه competition خودبه‌خود ایجاد می‌شود.

این analogue بسیار مهمی از محدودیت ماده/فضا است.

---

# 18. Matter analogue

نباید energy و memory را یکی بدانیم.

در طبیعت:

**Matter ≠ Energy**

به‌صورت مشابه در simulation:

**Memory capacity ≠ Computational energy**

Memory نقش چیزی شبیه **space/material capacity** را دارد.

Energy نقش ability-to-do-work را دارد.

این separation از ابتدا باید حفظ شود.

ممکن است organism انرژی زیادی داشته باشد ولی جایی برای offspring نداشته باشد.

یا memory آزاد باشد ولی انرژی کافی برای reproduction موجود نباشد.

این دو limitation متفاوت می‌توانند selection متفاوت ایجاد کنند.

---

# 19. مرگ

مرگ نباید صرفاً یک timer مصنوعی باشد.

در V0 بهتر است موجود عمدتاً زمانی بمیرد که دیگر نتواند هزینهٔ وجود خود را تأمین کند:

```text
internal_energy <= 0
        ↓
death

```

پس از مرگ:

```text
allocated memory → environment
remaining recyclable resources → environment

```

می‌توانیم بعداً ageing یا random failure را آزمایش کنیم، اما در baseline بهتر است lifespan ثابت نداشته باشیم.

در نتیجه اگر evolution راهی برای survival بسیار طولانی پیدا کند، اجازه می‌دهیم اتفاق بیفتد.

---

# 20. چرخهٔ منابع

یک اصل طبیعی مهم:

**ماده recycle می‌شود؛ انرژی جریان دارد.**

نسخهٔ سادهٔ دیجیتال:

```text
EXTERNAL ENERGY
       ↓
ENVIRONMENT
       ↓
ORGANISMS
       ↓
COMPUTATION
       ↓
DISSIPATION

```

ولی:

```text
MEMORY
 ↓ organism occupies
ORGANISM DIES
 ↓
MEMORY RELEASED
 ↓
available again

```

بنابراین energy و matter دو رفتار متفاوت دارند.

این distinction باید در simulation core ثبت شود.

---

# 21. چرا انرژی باید تلف شود؟

اگر تمام energy پس از هر computation دوباره 100% قابل استفاده باشد، جهان essentially perpetual خواهد شد.

در طبیعت biological work همراه dissipation است.

پس energy مصرف‌شده برای instruction execution نباید کامل به usable pool برگردد.

برای V0 ساده‌ترین مدل:

```text
spent energy → unavailable

```

و external source در tick بعد energy تازه وارد می‌کند.

بعداً می‌توان waste، recycling و secondary metabolism را اضافه کرد.

---

# 22. جهان اولیه همگن

طبق تصمیم پروژه، Experiment 0 هیچ geography ندارد.

وجود ندارد:

- mountain
- ocean
- desert
- wet region
- dry region
- temperature gradient
- day/night
- season

تمام نقاط environment از نظر قوانین یکسان‌اند.

این کار بسیار مهم است زیرا اگر اتفاق جالبی رخ دهد، بهتر می‌توانیم علت آن را بفهمیم.

پیچیدگی محیط باید **مرحله‌ای** اضافه شود.

---

# 23. ولی locality را با homogeneity اشتباه نگیریم

Homogeneous بودن الزاماً به معنی «همه با همه فوراً ارتباط دارند» نیست.

این تصمیم باید جداگانه بررسی شود.

دو مدل داریم:

### Well-mixed Soup

هر organism می‌تواند از یک pool جهانی resource دریافت کند.

### Homogeneous Spatial World

همهٔ نقاط قوانین یکسان دارند ولی interaction محلی است.

مثلاً یک ring یا grid homogeneous.

برای V0 باید هر دو را از نظر علمی بررسی کنیم.

احتمالاً ابتدا **well-mixed baseline** ساده‌تر است؛ سپس spatial homogeneous experiment را اجرا کنیم.

---

# 24. جمعیت اولیه

برای شروع population کوچک باشد.

مثلاً:

```text
10–20 organisms

```

همه از یک ancestor یکسان.

بنابراین:

```text
Genotype diversity at t=0 ≈ 1

```

هر diversity بعدی نتیجهٔ mutation و evolutionary history خواهد بود.

---

# 25. انرژی ورودی و Carrying Capacity

اگر:

```text
energy input = unlimited
memory = unlimited

```

تقریباً pressure انتخابی مهمی نداریم.

اگر:

```text
energy input = 0

```

همه می‌میرند.

بنابراین باید regimeای پیدا کنیم که population بتواند زنده بماند ولی resource-limited باشد.

مثلاً:

```text
Energy added per tick = E_in

```

اگر population افزایش یابد:

```text
energy per organism ↓

```

در نتیجه competition افزایش می‌یابد.

این می‌تواند بدون نوشتن یک `population_limit` صریح، carrying capacity ایجاد کند.

این ترجیح ماست:

**ظرفیت جمعیت باید تا حد ممکن emergent باشد، نه hard-coded.**

---

# 26. بیماری، ویروس و کنترل جمعیت

در طبیعت microbial ecology، viruses و parasites می‌توانند نقش مهمی در mortality و diversity داشته باشند. ایده‌هایی مانند **Kill-the-Winner** توضیح می‌دهند که چگونه افزایش یک lineage غالب می‌تواند آن را به target بزرگ‌تری برای viral predation تبدیل کند و امکان coexistence lineageهای دیگر را افزایش دهد.

اما:

### در V0 هیچ virus مصنوعی اضافه نمی‌کنیم.

این بسیار مهم است.

اگر از ابتدا بنویسیم:

```text
if population > threshold:
    create virus

```

داریم نتیجه را طراحی می‌کنیم.

در عوض architecture باید در آینده اجازه دهد organisms بتوانند از computation/information دیگر organisms استفاده کنند.

اگر بعداً یک mutant کوچک‌تر بتواند reproduction machinery دیگری را exploit کند:

**آن وقت parasite واقعاً evolved شده است.**

این تفاوت فلسفی پروژه است.

---

# 27. جنگ

همین اصل درباره aggression برقرار است.

نباید instruction زیر داشته باشیم:

```text
ATTACK(other)

```

در مراحل آینده می‌توان primitive interactionهایی ایجاد کرد که مثلاً اجازه دهند organism تحت هزینه و محدودیت به memory/resource همسایه دسترسی پیدا کند.

اگر evolution کشف کرد که:

```text
damaging competitor
        ↓
more resource for me
        ↓
more descendants

```

آن رفتار را می‌توان aggression دیجیتال دانست.

اما ما آن را از قبل نام‌گذاری و reward نکرده‌ایم.

---

# 28. دفاع

وقتی امکان damage وجود داشته باشد، ممکن است mutationهایی که resistance ایجاد می‌کنند مزیت پیدا کنند.

آن وقت:

```text
exploitation
    ↓
resistance
    ↓
better exploitation
    ↓
better resistance
    ↓
...

```

ممکن است evolutionary arms race ایجاد شود.

این یکی از candidate mechanisms برای ادامهٔ evolutionary innovation است، ولی نباید آن را تضمین کنیم.

---

# 29. exploitation به‌جای «برده‌داری»

برای زبان علمی پروژه بهتر است از اصطلاح:

**Persistent Exploitation**

استفاده کنیم.

ممکن است organism A به جای نابودی B، از output یا resource processing آن استفاده کند.

اگر چنین رفتاری از primitive interactions تکامل پیدا کند، ثبتش می‌کنیم.

اما هیچ `ENSLAVE` instruction وجود نخواهد داشت.

---

# 30. Cooperation

قوانینی که exploitation را ممکن می‌کنند ideally باید cooperation را هم ممکن کنند.

مثلاً ممکن است دو lineage به‌طور مستقل فعالیت‌هایی داشته باشند که محصول یکی برای دیگری مفید باشد.

اگر association آنها reproductive success هر دو را افزایش دهد، cooperation می‌تواند گسترش پیدا کند.

باز هم:

```text
COOPERATE

```

نباید instruction باشد.

---

# 31. Major Transitions

یکی از عمیق‌ترین درس‌های evolution طبیعی این است که complexity فقط با طولانی‌تر شدن genome ایجاد نشده است.

چند بار واحد selection تغییر کرده است.

به‌صورت انتزاعی:

```text
replicators
   ↓
cooperative groups
   ↓
integrated higher-level individual

```

مطالعات major evolutionary transitions نشان می‌دهند cooperation، division of labor، communication، mutual dependence و کاهش conflict داخلی از عناصر مهم تشکیل واحدهای سطح بالاتر بوده‌اند.

برای پروژه ما این یک **موضوع مشاهده** است، نه target.

اگر چند digital organism روزی به یک واحد computational وابسته به هم تبدیل شوند، آن را بررسی می‌کنیم.

اما هیچ reward برای این transition نمی‌دهیم.

---

# 32. درس مهم Tierra

Tierra نزدیک‌ترین predecessor مفهومی پروژه ماست.

در Tierra:

```text
CPU time ≈ energy
RAM ≈ material/space
machine instructions ≈ genome
self-replicating program ≈ organism
mutation ≈ genetic variation

```

و از ancestor ساده:

- parasites،
- immunity،
- counter-adaptation،
- hyper-parasites،
- ecological interactions

ظاهر شدند.

این نشان می‌دهد که interactionهای غیرمنتظره واقعاً می‌توانند از digital evolution پدید آیند.

اما Tierra همچنین نشان داد که evolution لزوماً به افزایش دائمی complexity منجر نمی‌شود.

این هشدار بنیادی پروژه ماست.

---

# 33. یک اصلاح مهم درباره Tierra

مستندات Tierra نشان می‌دهند simulator حتی پارامترهای environmental disturbance داشته است.

برای نمونه `DistProp` می‌توانست بخشی از population را در disturbance حذف کند و `DistFreq` زمان disturbance بعدی را نسبت به recovery تنظیم کند.

همچنین random ejection و چندین mutation mechanism وجود داشت.

بنابراین نباید پروژه خودمان را با ادعای سادهٔ «Tierra هیچ disturbance نداشت» توجیه کنیم.

سؤال علمی‌تر این است:

> چه نوع environmental dynamics و organism–environment interactions برای sustained innovation کافی یا ضروری‌اند؟

---

# 34. Open-Ended Evolution

این پروژه مستقیماً با مسئلهٔ **Open-Ended Evolution (OEE)** تماس دارد.

ادبیات OEE تأکید می‌کند که reproduction + mutation + selection به تنهایی تضمین نمی‌کنند novelty و complexity برای همیشه ادامه پیدا کنند.

سیستم‌ها اغلب به یک regime نسبتاً ثابت می‌رسند.

پیشنهادهای پژوهشی برای OEE شامل مواردی مانند:

- فضای بسیار بزرگ برای genotype/phenotype؛
- مسیرهای mutation که viability را حفظ کنند؛
- امکان offspring پیچیده‌تر؛
- interaction diversity؛
- coevolution؛
- niche construction؛
- تغییر سطح organization؛
- environmental dynamics

هستند.

اما پروژه ما نباید همه را در V0 وارد کند.

ما می‌خواهیم بفهمیم **کدام additions واقعاً چه اثری دارند.**

---

# 35. مهم‌ترین روش علمی پروژه: Incremental Worlds

به جای ساخت یک جهان بسیار پیچیده، مجموعه‌ای از جهان‌ها می‌سازیم.

### World 0

```text
Replication
Energy
Finite memory
Mutation
Death

```

### World 1

اضافه:

```text
locality

```

### World 2

اضافه:

```text
direct organism interaction

```

### World 3

اضافه:

```text
resource transformation

```

### World 4

اضافه:

```text
environmental fluctuations

```

### World 5

اضافه:

```text
disturbance

```

و به همین ترتیب.

هر مرحله با قبلی مقایسه می‌شود.

این به ما اجازه می‌دهد بفهمیم کدام قانون چه evolutionary consequenceای ایجاد کرده است.

---

# 36. Experiment 0 — Digital Petri Dish

اولین implementation باید عمداً کوچک باشد.

Candidate configuration:

```text
Language: Python

Initial organisms:
10–20

Initial genotypes:
1

World:
homogeneous

Memory:
finite

Energy input:
constant per tick

Energy:
finite and consumable

Genome:
tiny instruction sequence

Mutation:
small substitution probability

Reproduction:
self-copy through primitive operations

Death:
energy exhaustion

Explicit fitness:
NONE

Attack:
NONE

Cooperation:
NONE

Parasites:
NONE injected

Learning:
NONE

ML:
NONE

Neural network:
NONE

External APIs:
NONE

Network:
NONE

Filesystem:
NONE

```

---

# 37. Digital Physics v0

قوانین اولیه باید کم و واضح باشند.

### Law 1 — Finite Space

کل memory محدود است.

### Law 2 — External Energy Flux

در هر tick مقدار محدودی usable resource وارد environment می‌شود.

### Law 3 — Computation Costs Energy

هیچ instruction رایگان نیست.

### Law 4 — Existence Costs Energy

maintenance هزینه دارد.

### Law 5 — Replication Costs Resources

copying و ساخت offspring رایگان نیست.

### Law 6 — Replication Is Imperfect

احتمال mutation کوچک ولی غیرصفر است.

### Law 7 — Heredity

تغییر genome قابل انتقال به نسل بعد است.

### Law 8 — Death Releases Space

موجود مرده memory را اشغال نمی‌کند.

### Law 9 — No External Fitness

Simulator درباره خوب یا بد بودن genotype تصمیم نمی‌گیرد.

### Law 10 — Conservation Accounting

هیچ resource نباید بدون ثبت از هیچ ظاهر یا ناپدید شود، جز source/sinkهایی که صریحاً جزو physics جهان تعریف شده‌اند.

---

# 38. Conservation Ledger

از روز اول باید accounting داشته باشیم.

در هر tick:

```text
Energy added
Energy captured
Energy stored
Energy spent on execution
Energy spent on maintenance
Energy spent on reproduction
Energy dissipated

```

باید قابل محاسبه باشد.

و:

```text
Total memory
Occupied memory
Free memory

```

نیز همیشه ثبت شود.

اگر accounting برقرار نباشد، selection ممکن است بر اساس bug شکل بگیرد.

---

# 39. Bugs می‌توانند «قوانین طبیعت» شوند

این پروژه یک خطر خاص دارد.

در software معمولی bug فقط bug است.

اما در evolutionary system، organism ممکن است bug simulator را exploit کند.

مثلاً اگر یک instruction به اشتباه energy منفی مصرف کند:

```text
cost = -1

```

evolution احتمالاً آن را پیدا خواهد کرد.

بنابراین simulator باید دارای invariantهای بسیار سخت باشد.

ولی اگر organism یک loophole **واقعی در قوانین تعریف‌شده** پیدا کرد، نباید فوراً آن را bug فرض کنیم.

باید distinction داشته باشیم:

### Implementation Bug

رفتاری مخالف specification.

### Evolutionary Exploit

استفادهٔ غیرمنتظره ولی قانونی از physics.

دومی یکی از جالب‌ترین نتایج پروژه خواهد بود.

---

# 40. Reproducibility

تمام randomness باید seed داشته باشد.

هر run:

```text
run_id
random_seed
world_config
ancestor_version
instruction_set_version
simulator_commit

```

را ذخیره کند.

اگر Run 1842 رفتار عجیبی نشان داد، باید بتوانیم همان جهان را دقیقاً replay کنیم.

Tierra نیز random seed و state را برای reproducibility ثبت می‌کرد؛ این درس خوبی برای ماست.

---

# 41. Genealogy

هر organism باید identity داشته باشد.

حداقل:

```text
organism_id
parent_id
generation
birth_tick
death_tick
genome_hash
genome_length
birth_energy
death_reason
offspring_count

```

ثبت شود.

در نتیجه می‌توانیم lineage را بازسازی کنیم:

```text
Ancestor
 ├── A
 │   ├── A1
 │   └── A2
 └── B
     ├── B1
     └── B2

```

این برای فهمیدن evolution ضروری است.

---

# 42. چه چیزهایی را اندازه بگیریم؟

حداقل metrics:

### Population

```text
N(t)

```

### Genetic Diversity

تعداد genotypeهای متمایز.

### Genome Size

mean / min / max.

### Energy Efficiency

offspring per energy consumed.

### Replication Cost

energy/instructions required per successful reproduction.

### Lineage Persistence

هر lineage چند generation باقی می‌ماند؟

### Dominance

چه سهمی از population متعلق به dominant genotype است؟

### Mutation Survival

چه درصد mutationها:

- lethal
- transient
- persistent
- dominant

می‌شوند؟

### Extinction

آیا کل population از بین می‌رود؟

---

# 43. Complexity را reward نکنیم، فقط measure کنیم

می‌توان complexity metrics مختلف تعریف کرد، اما فقط observer هستند.

مثلاً:

- genome length؛
- executed instruction diversity؛
- control-flow complexity؛
- state usage؛
- dependency structure؛
- behavioral diversity.

ولی هیچ‌کدام نباید energy یا reproductive bonus ایجاد کنند.

Observer حق ندارد actor شود.

---

# 44. Observer باید از Physics جدا باشد

Architecture باید separation واضح داشته باشد:

```text
Simulation Core
     |
     +--- Physics
     |
     +--- VM
     |
     +--- Organisms
     |
     +--- Environment

Observation Layer
     |
     +--- Logger
     +--- Metrics
     +--- Genealogy
     +--- Replay
     +--- Visualization

```

Observation نباید رفتار world را تغییر دهد.

---

# 45. Python Architecture پیشنهادی

ساختار اولیه می‌تواند چنین باشد:

```text
digital-evolution-world/
│
├── src/
│   ├── world.py
│   ├── organism.py
│   ├── genome.py
│   ├── vm.py
│   ├── instructions.py
│   ├── energy.py
│   ├── mutation.py
│   ├── reproduction.py
│   └── scheduler.py
│
├── experiments/
│   ├── world_00_baseline.py
│   └── configs/
│
├── analysis/
│   ├── population.py
│   ├── diversity.py
│   ├── genealogy.py
│   └── plots.py
│
├── tests/
│
├── data/
│
├── docs/
│
└── README.md

```

این فقط starting architecture است و قبل از coding باید نقد شود.

---

# 46. Libraries

برای V0 عمداً stack کوچک باشد.

Core:

```text
Python

```

Analysis:

```text
NumPy
Pandas
Matplotlib

```

Testing:

```text
pytest

```

برای اولین نسخه به frameworkهای agentic، ML libraries یا simulation engine سنگین نیاز نداریم.

اگر بعداً performance bottleneck شد می‌توانیم بررسی کنیم:

- NumPy optimization
- Numba
- multiprocessing
- Rust/C++ core
- GPU

اما performance optimization نباید قبل از validation مدل انجام شود.

---

# 47. Scheduler

یکی از تصمیمات بسیار مهم این است که چه کسی چه زمانی instruction اجرا کند.

نباید یک organism بتواند فقط به دلیل position در Python loop advantage دائمی بگیرد.

پس scheduler باید fairness قابل تعریف داشته باشد.

Candidate baseline:

```text
randomized round-robin

```

یا:

```text
each living organism receives a bounded execution opportunity per cycle

```

اما مقدار computation واقعی باید همچنان energy cost داشته باشد.

این مسئله باید قبل از V0 دقیق طراحی شود زیرا scheduler بخشی از «فیزیک جهان» است.

---

# 48. Time

نباید biological second را شبیه‌سازی کنیم.

واحد بنیادی:

### Tick

است.

هر tick یک واحد simulation time است.

Generation نیز نباید الزاماً time unit باشد؛ چون lineageهای مختلف ممکن است reproduction rate متفاوت داشته باشند.

پس:

```text
tick ≠ generation

```

هر organism generation خودش را از parent دریافت می‌کند:

```text
child.generation = parent.generation + 1

```

---

# 49. Population Control نباید مستقیم باشد

تا حد امکان نباید بنویسیم:

```python
if population > 1000:
    kill(...)

```

زیرا این artificial population management است.

ترجیح:

```text
finite memory
+
finite energy
+
maintenance
+
reproduction cost

```

خودشان carrying capacity ایجاد کنند.

بعداً می‌توانیم disturbance را به‌عنوان experiment مستقل اضافه کنیم.

---

# 50. Catastrophes — نه در V0

Earth دارای:

- volcanic events
- impacts
- fires
- floods
- climate shifts

است.

اما هدف ما شبیه‌سازی آنها نیست.

در مراحل بعد می‌توان abstract disturbance تعریف کرد:

```text
temporary energy collapse
random local destruction
memory corruption
resource pulse
population bottleneck

```

و اثر آنها بر evolution را مقایسه کرد.

ولی V0 باید بدون catastrophe اجرا شود تا baseline داشته باشیم.

---

# 51. بیماری — نه در V0

بیماری را نیز hard-code نمی‌کنیم.

بعداً وقتی direct interaction ممکن شد، می‌توانیم ببینیم آیا یک lineage می‌تواند از machinery lineage دیگر استفاده کند.

اگر بله:

```text
parasite-like strategy

```

ممکن است خودبه‌خود ایجاد شود.

این از ساختن یک Virus class از روز اول علمی‌تر است.

---

# 52. سؤال عمیق درباره «منابع»

در طبیعت organisms فقط انرژی نمی‌خواهند.

به matter هم نیاز دارند.

برای V0:

```text
memory ≈ structural resource
energy ≈ work resource

```

کافی است.

ولی در نسخه‌های بعد شاید چند resource مستقل داشته باشیم:

```text
R1
R2
R3

```

بدون اینکه بگوییم R1=carbon یا R2=nitrogen.

اگر organisms برای functions متفاوت به resources متفاوت نیاز داشته باشند، امکان specialization و ecological niches بسیار بیشتر می‌شود.

اما این complexity باید بعداً اضافه شود.

---

# 53. سؤال بسیار مهم درباره Energy Capture

نباید از همان ابتدا موجودی بسازیم که instruction جادویی:

```text
GET_ENERGY

```

داشته باشد بدون هزینه یا محدودیت.

باید بررسی کنیم آیا energy acquisition:

1. passive باشد؛
2. نیاز به instruction داشته باشد؛
3. نیاز به pattern خاص genome داشته باشد؛
4. نیاز به structure محاسباتی داشته باشد.

این تصمیم می‌تواند مسیر evolution را کاملاً تغییر دهد.

بنابراین قبل از implementation نهایی باید چند مدل انرژی را با هم مقایسه کنیم.

---

# 54. اصل Minimal Hand of God

هر بار که می‌خواهیم یک rule اضافه کنیم باید بپرسیم:

> آیا این قانون واقعاً برای وجود جهان ضروری است یا داریم evolution را هدایت می‌کنیم؟

Simulator ناگزیر قوانینی دارد.

پس دخالت صفر انسان ممکن نیست.

اما هدف:

### Minimum necessary imposed structure

است.

ما physics را می‌سازیم.

Evolution history را نمی‌نویسیم.

---

# 55. چیزهایی که نباید در V0 وجود داشته باشند

به‌طور صریح:

**No ML**

**No neural networks**

**No LLM**

**No AI API**

**No reinforcement learning**

**No explicit fitness function**

**No intelligence reward**

**No complexity reward**

**No attack instruction**

**No cooperation instruction**

**No parasite injection**

**No species labels**

**No predefined roles**

**No predator class**

**No prey class**

**No human-directed mutation**

**No manual selection**

---

# 56. Species چیست؟

در ابتدا حتی species را هم به simulator تحمیل نمی‌کنیم.

Simulator فقط genomeها و lineages را می‌بیند.

بعداً observer می‌تواند بر اساس genetic/behavioral similarity cluster ایجاد کند.

پس:

```text
species

```

باید تا حد ممکن یک **analytical interpretation** باشد، نه object بنیادی physics.

---

# 57. Success چیست؟

موفقیت پروژه این نیست:

> AI ساخته شد.

موفقیت Experiment 0 این است که بتوانیم نشان دهیم:

1. ancestor واقعاً self-replicates؛
2. resources محدودند؛
3. replication هزینه دارد؛
4. mutations وراثتی‌اند؛
5. lineages متفاوت ایجاد می‌شوند؛
6. differential survival/reproduction رخ می‌دهد؛
7. هیچ explicit fitness function وجود ندارد؛
8. نتایج reproducible هستند.

اگر تمام population بمیرد، آن run نیز داده است.

---

# 58. اولین سؤال علمی

Experiment 0 باید سؤال بسیار محدودی داشته باشد:

> در یک جهان دیجیتال همگن با فضای محدود و جریان ثابت انرژی، آیا جمعیتی از replicatorهای بسیار ساده با mutation کوچک می‌تواند یک evolutionary equilibrium پایدار ایجاد کند و چه ویژگی‌هایی تحت selection قرار می‌گیرند؟

ما پیش‌بینی را به عنوان نتیجه تحمیل نمی‌کنیم.

ممکن است ببینیم:

- genome shortening؛
- faster replication؛
- lower maintenance cost؛
- extinction؛
- neutral drift؛
- dominance؛
- coexistence؛
- یا رفتار دیگری.

---

# 59. Control Experiments

برای اینکه مطمئن شویم چیزی که می‌بینیم واقعاً evolution است، control لازم داریم.

### Control A

```text
mutation = 0

```

### Control B

```text
energy abundant

```

### Control C

```text
memory abundant

```

### Control D

```text
maintenance cost = 0

```

سپس با baseline مقایسه کنیم.

این کمک می‌کند بفهمیم هر pressure چه نقشی دارد.

---

# 60. Replicates

یک simulation کافی نیست.

چون mutation stochastic است.

هر configuration باید با seedهای متعدد اجرا شود.

مثلاً:

```text
30 independent runs

```

اگر یک رفتار فقط در 1/30 run رخ داد، با رفتاری که در 29/30 رخ داده فرق دارد.

این پروژه باید از ابتدا experimental science باشد، نه صرفاً یک demo زیبا.

---

# 61. Phase 0 — قبل از کدنویسی

در چت جدید نباید فوراً شروع به نوشتن simulator کنیم.

اول باید چهار specification بسازیم:

### Specification A

**Digital–Natural Analogy Matrix**

### Specification B

**Digital Physics v0**

### Specification C

**Instruction Set v0**

### Specification D

**Experiment 0 Protocol**

تا وقتی این چهار مورد منطقی نشده‌اند، implementation شروع نشود.

---

# 62. Digital–Natural Analogy Matrix اولیه

| Natural WorldFundamental FunctionCandidate Digital Analogue |                                   |                                |
| ----------------------------------------------------------- | --------------------------------- | ------------------------------ |
| Sun/geochemical energy                                      | external free-energy source       | energy influx                  |
| ATP-like usable energy                                      | stored spendable energy           | internal energy                |
| Matter                                                      | structural resource               | finite memory                  |
| Cell membrane                                               | compartment/boundary              | organism-owned memory/state    |
| DNA/RNA                                                     | heritable information             | genome instructions            |
| Metabolism                                                  | resource → usable work            | VM resource processing         |
| Cellular machinery                                          | executes encoded functions        | VM execution state             |
| Reproduction                                                | new individual                    | genome copying + division      |
| Mutation                                                    | heritable variation               | instruction mutation           |
| Death                                                       | loss of organized individual      | deallocation                   |
| Decomposition                                               | resource recycling                | memory/resource release        |
| Competition                                                 | shared limited resources          | energy/memory competition      |
| Environment                                                 | external constraints              | digital physics                |
| Time                                                        | process ordering                  | simulation ticks               |
| Population                                                  | interacting individuals           | active organisms               |
| Natural selection                                           | differential reproduction         | emergent lineage frequencies   |
| Parasite                                                    | exploits host machinery           | future emergent exploit        |
| Disease                                                     | damaging biological interaction   | future interaction dynamics    |
| Ecosystem                                                   | interacting populations/resources | digital ecology                |
| Catastrophe                                                 | exogenous disturbance             | later perturbation experiments |

این جدول **فرضیه است، نه حقیقت**.

هر ردیف باید قبل از implementation نقد شود.

---

# 63. چیزهایی که نباید بیش از حد مشابه کنیم

مثلاً:

**DNA دارای چهار base است.**

این دلیل نمی‌شود genome دیجیتال چهار opcode داشته باشد.

**زمین سه‌بعدی است.**

این دلیل نمی‌شود Digital World سه‌بعدی باشد.

**ATP شیمی خاصی دارد.**

این دلیل نمی‌شود chemistry ATP را simulate کنیم.

**باکتری membrane lipid دارد.**

این دلیل نمی‌شود lipid simulation بنویسیم.

ما باید underlying principle را استخراج کنیم.

---

# 64. سؤال فلسفی/علمی اصلی پروژه

این پروژه در نهایت درباره یک سؤال بسیار ساده ولی عمیق است:

> **اگر برنامه‌های کامپیوتری به جای آنکه نسل به نسل توسط انسان طراحی شوند، بتوانند در یک جهان محاسباتی محدود خودشان تکثیر، تغییر و برای ادامهٔ وجود رقابت کنند، چه نوع نرم‌افزاری در طول evolutionary time پدید خواهد آمد؟**

ما نمی‌دانیم.

و دقیقاً **ندانستن پاسخ** دلیل انجام آزمایش است.

---

# 65. فرضیه‌ای که نباید تبدیل به پیش‌فرض شود

ممکن است امیدوار باشیم:

```text
simple replicator
        ↓
complex replicator
        ↓
cooperation
        ↓
specialization
        ↓
higher-level software organism
        ↓
complex information processing
        ↓
?

```

اما simulator نباید این مسیر را بداند.

ممکن است واقعیت دیجیتال چنین باشد:

```text
simple replicator
        ↓
better simple replicator
        ↓
even smaller replicator
        ↓
stable equilibrium

```

اگر چنین شود، باید بفهمیم **چرا**.

بعد می‌توانیم یک environmental law را تغییر دهیم و آزمایش جدید انجام دهیم.

---

# 66. رویکرد پژوهشی پروژه

چرخهٔ توسعه باید چنین باشد:

```text
Research
   ↓
Hypothesis
   ↓
Minimal World Rule
   ↓
Implementation
   ↓
Validation
   ↓
Multiple Runs
   ↓
Measurement
   ↓
Unexpected Result
   ↓
Analysis
   ↓
Next Hypothesis

```

نه:

```text
Build features
↓
Build more features
↓
Build AI

```

این پروژه باید آزمایشگاه باشد.

---

# 67. اصل نهایی طراحی

هر بار که نتیجه جالبی ظاهر شد، قبل از اضافه‌کردن feature جدید باید بپرسیم:

> آیا این رفتار واقعاً توسط evolution کشف شد، یا ما ناخواسته آن را داخل قوانین جهان نوشته بودیم؟

این شاید مهم‌ترین سؤال کل پروژه باشد.

---

# 68. نقطهٔ شروع چت جدید

در شروع پروژه جدید، **اول کد ننویس.**

ابتدا این سند را به‌عنوان Research Charter در نظر بگیر.

سپس با من این کار را انجام بده:

> **Phase 0A: Digital–Natural Analogy Audit**
>
> تمام analogyهای این سند را یکی‌یکی نقد کن. برای هر کدام بررسی کن:
>
> 1. نقش واقعی آن پدیده در زیست‌شناسی چیست؟
> 2. آیا برای Digital Evolution ضروری است؟
> 3. آیا analogue پیشنهادی ما درست است؟
> 4. آیا analogue ساده‌تری وجود دارد؟
> 5. آیا با اضافه‌کردنش نتیجه را bias می‌کنیم؟
> 6. اگر حذفش کنیم چه اتفاقی ممکن است بیفتد؟
>
> هنوز implementation را شروع نکن.
>
> پس از آن:
>
> **Phase 0B — Digital Physics v0**
>
> **Phase 0C — Minimal Instruction Set**
>
> **Phase 0D — Energy & Resource Model**
>
> **Phase 0E — Reproduction & Mutation Model**
>
> **Phase 0F — Experimental Protocol**
>
> و فقط پس از تصویب این مراحل:
>
> **Phase 1 — Python Prototype**

---

# 69. اصل مرکزی پروژه در یک جمله

## ما نمی‌خواهیم یک موجود دیجیتال پیچیده طراحی کنیم؛ می‌خواهیم یک جهان دیجیتال به‌اندازهٔ کافی ساده و منصفانه طراحی کنیم که بتوانیم ببینیم evolution خودش چه نرم‌افزارهایی قادر است اختراع کند.

و بنابراین خروجی مورد انتظار پروژه از ابتدا فقط این است:

```text
Minimal Digital Replicator

        ↓

Finite space
Continuous energy flux
Resource competition
Costly computation
Costly maintenance
Costly reproduction
Imperfect copying
Heritable variation
Death
Selection

        ↓

?????????????????

```

**علامت سؤال نباید حذف شود.**