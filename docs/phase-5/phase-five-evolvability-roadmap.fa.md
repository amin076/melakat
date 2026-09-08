# مرحلهٔ پنج — افزایش Evolvability ژنوم بدون پاداش برای Complexity

## وضعیت

**این سند فقط قرارداد علمی و طراحی است. هنوز هیچ کد موتور برای Phase 5 مجاز نشده است.**

Phase 4 بسته شده است. Phase 5 یک پرسش علّی تازه را آغاز می‌کند: آیا طول ژنوم می‌تواند خودش به یک متغیر وراثتی و قابل‌تکامل تبدیل شود، بدون اینکه host برای ژنوم بلندتر پاداش بگذارد، fitness score تعریف کند یا هدفی برای «پیچیدگی بیشتر» تعیین کند؟

اولین implementation مرحلهٔ پنج باید یک backend مستقل و opt-in باشد. موتورهای منجمد Phase Zero تا Phase Four، experimentها و evidenceهای پذیرفته‌شده باید بدون تغییر reproducible باقی بمانند.

## پرسش علمی

> آیا می‌توان bottleneck فعلی fixed-length genome در ملاکت را حذف کرد، به‌طوری‌که structural mutationهای کور بتوانند genomeهای کوتاه‌تر و بلندترِ self-replicating ایجاد کنند و سرنوشت آنها فقط توسط محدودیت‌های موجود جهان محاسباتی تعیین شود؟

نتیجهٔ مثبت Phase 5 فقط می‌تواند **heritable variable genome length** و **structural evolvability** را نشان دهد. این به‌تنهایی افزایش complexity، adaptation، intelligence، open-ended evolution یا شباهت زیستی را اثبات نمی‌کند.

## چرا نمی‌توانیم همین حالا فقط insertion/deletion را به VM فعلی اضافه کنیم؟

نمایش فعلی genome دو قفل مصنوعی برای تغییر طول دارد.

1. حلقهٔ replication در ancestor طول genome را به‌صورت ثابت `SET R0, 8` داخل خودش نوشته است. اگر طول فرزند تغییر کند، copy loop هنوز همان count قدیمی را اجرا می‌کند.
2. flow control از absolute jump address استفاده می‌کند. insertion یا deletion می‌تواند جای دستورها را جابه‌جا کند اما operand پرش‌ها همان عدد قبلی بماند؛ در نتیجه حتی flow control نامرتبط نیز می‌شکند.

یک محدودیت سوم این brittleness را شدیدتر می‌کند: substitution معمولی opcode را عوض می‌کند ولی operandهای instruction را نگه می‌دارد. بنابراین یک genome تغییرطول‌یافته عملاً نمی‌تواند به‌سادگی count کپی یا jump targetهای خراب‌شده را repair کند.

پس اگر روی representation فعلی indel را روشن کنیم، عمدتاً داریم **شکنندگی representation** را آزمایش می‌کنیم، نه evolvability را.

این درس با سامانه‌های کلاسیک Digital Evolution نیز سازگار است. Tierra عمداً از template-based indirect addressing استفاده کرد و Avida نیز از template/head-based addressing بهره می‌گیرد تا insertion/deletion به‌طور خودکار همهٔ آدرس‌های absolute را خراب نکنند. Avida و Aevol هر دو mutationهای تغییرطول‌دهنده دارند، اما در representationهایی که از ابتدا برای تغییر اندازهٔ genome مناسب‌تر طراحی شده‌اند.

## اصول طراحی Phase 5

1. **هیچ complexity reward وجود ندارد.** هیچ termی نباید طول genome، تعداد instruction، novelty، diversity یا یک task انسانی را reward کند.
2. **هیچ strategy از سوی host نوشته نمی‌شود.** host فقط affordanceهای سطح substrate برای replication و addressing فراهم می‌کند.
3. **هزینه‌های موجود واقعی باقی می‌مانند.** genome بلندتر memory بیشتری می‌گیرد و برای copy/execution به کار بیشتری نیاز دارد. صرفاً به دلیل بلندبودن genome، penalty مصنوعی اضافه نمی‌کنیم.
4. **Genome length برابر complexity نیست.** طول فقط یک state variable ساختاری است.
5. **هر بار یک causal mechanism جدید.** اول representation robust می‌شود، بعد structural mutation؛ single-instruction event قبل از rearrangement بزرگ.
6. **Backendهای منجمد دست‌نخورده می‌مانند.** رفتار Phase 5 فقط در یک VM/engine جدید قرار می‌گیرد.
7. **Determinism و accounting همچنان بنیادی‌اند.** structural mutation باید reproducible و audit-able باشد و energy/memory accounting را نشکند.
8. **هیچ promotion post-hoc نداریم.** calibration فقط برای exposure مجاز است، نه برای انتخاب rateای که genome بزرگ‌تر یا outcome دلخواه تولید کند.

## تصمیم ۱ — قبل از structural mutation، یک replication substrate مقاوم به تغییر طول می‌سازیم

Phase 5 باید یک replication/addressing layer کوچک و مستقل اضافه کند و semantics دستورهای منجمد `COPY`، `JUMP` و `DIVIDE` در موتورهای قدیمی را تغییر ندهد.

### 1A. Sequential copy head

یک primitive مخصوص Phase 5 با نام موقت `COPY_NEXT` اضافه شود.

Semantics مفهومی:

- هر organism در شروع lifecycle replication یک read position در ابتدای genome خودش دارد؛
- `COPY_NEXT` دقیقاً یک instruction از genome فعلی را به daughter buffer کپی می‌کند و read position را یک خانه جلو می‌برد؛
- پس از کپی آخرین instruction، VM یک completion state در اختیار control flow عادی می‌گذارد؛
- این instruction به‌صورت خودکار divide نمی‌کند و تصمیم نمی‌گیرد reproduction مفید است یا نه؛
- `DIVIDE` همچنان باید صریحاً توسط genome اجرا شود و فقط در صورت کامل‌بودن daughter proposal موفق شود.

در Phase 5، daughter buffer باید dynamic باشد، نه اینکه از ابتدا با طول ثابت parent پر شود. این کار نیاز مصنوعی به اینکه genome طول خودش را به‌صورت یک literal هشت‌بیتی بداند از بین می‌برد.

ترجیح طراحی این است که completion از طریق یک state سادهٔ قابل‌مشاهده توسط VM منتقل شود؛ نه اینکه دستور سطح‌بالایی مثل `COPY_ALL` داشته باشیم. genome هنوز باید loop و `DIVIDE` را خودش اجرا کند.

### 1B. Template-based indirect flow control

Absolute jumpها برای backward compatibility باقی می‌مانند، اما ancestor جدید Phase 5 نباید replication loop خودش را با absolute address بسازد.

دو no-op خنثی با نام موقت `NOP_A` و `NOP_B` و حداقل jumpهای template-search لازم برای loop و exit branch اضافه شوند.

Template یک sequence کوتاه از `NOP_A/NOP_B` است. jump template بعد از خودش را می‌خواند و در genome همان organism به دنبال complement آن می‌گردد. اجرای مستقیم NOPها هیچ state effect ندارد.

به این ترتیب insertion/deletion خارج از template دیگر فقط به خاطر shift شدن indexها flow control را نابود نمی‌کند.

رفتار دقیق template search در صورت failure، بیشترین طول template، direction search و circular یا non-circular بودن باید قبل از اولین mutation experiment در contract Phase 5 freeze شود.

### چرا فقط `GENOME_LENGTH` اضافه نکنیم؟

یک self-length instruction فقط hard-coded copy count را حل می‌کند؛ مشکل absolute jumpها باقی می‌ماند. علاوه بر آن، registerهای فعلی 8-bit هستند و این روش به‌طور ناخواسته سقف 255 instruction ایجاد می‌کند مگر اینکه سخت‌افزار را هم تغییر دهیم. Sequential copy head + indirect addressing هر دو bottleneck اصلی را بدون تعریف یک genome size مطلوب حل می‌کنند.

## تصمیم ۲ — اولین expansion operator: single-instruction tandem duplication

Phase 5 با arbitrary random insertion شروع نمی‌شود.

Instruction در ملاکت فقط opcode نیست؛ operandهای `a` و `b` هم دارد. پس random insertion مجبورمان می‌کند یک distribution دست‌ساز برای opcode و operandها تعریف کنیم. این distribution می‌تواند خودش viability را به‌شدت تعیین کند و تبدیل به یک bias پنهان شود.

بنابراین اولین operator افزایش طول یک **single-instruction tandem duplication** کور است:

1. یک instruction index به‌صورت uniform انتخاب می‌شود؛
2. همان instruction کامل با operandهای خودش copy می‌شود؛
3. duplicate بلافاصله بعد از source قرار می‌گیرد.

طول دقیقاً `+1` می‌شود، بدون اینکه host payload تازه‌ای اختراع کند. substitution کور موجود همچنان می‌تواند بعداً یکی از نسخه‌های تکرارشده را تغییر دهد.

این فقط یک affordance ساختاری است و هیچ ادعایی دربارهٔ مفیدبودن duplication ندارد.

## تصمیم ۳ — اولین contraction operator: single-instruction deletion

اولین operator کاهش طول:

1. یک instruction index را uniform انتخاب می‌کند؛
2. همان یک instruction را حذف می‌کند؛
3. فقط transition به genome کاملاً خالی به‌عنوان state نامعتبر substrate رد می‌شود.

هیچ replication instruction، template، sensing، movement یا region «ضروری» توسط host محافظت نمی‌شود. حذف یک instruction حیاتی کاملاً مجاز است و ممکن است mutant را نابارور یا مرده کند.

## تصمیم ۴ — در نخستین gate حداکثر یک structural event برای هر daughter proposal

مدل اولیهٔ Phase 5 به‌صورت per-division تعریف می‌شود:

- `mutation.structural_event_rate`: احتمال اینکه برای یک daughter یک structural event رخ دهد؛
- `mutation.structural_duplication_probability`: در صورت رخداد event، احتمال duplication؛ در غیر این صورت deletion.

در gate اولیه بیش از یک structural event برای یک child مجاز نیست. این کار causal interpretation را ساده نگه می‌دارد.

Conditionهای جداشده می‌توانند total event rate یکسان داشته باشند:

- structural OFF؛
- duplication-only؛
- deletion-only؛
- balanced duplication/deletion.

Per-site rate، multiple event، large indel و segment rearrangement به مرحلهٔ بعد موکول می‌شوند.

## تصمیم ۵ — RNG مستقل و deterministic برای structural mutation

Structural event drawها باید از یک RNG stream مشتق‌شده و versioned مستقل از random streamهای تاریخی mutation/spatial استفاده کنند.

دلیل: صرفاً روشن‌کردن یک operator جدید نباید فقط به خاطر مصرف random number اضافی، sequence تمام random eventهای قدیمی را تغییر دهد. پس از اولین structural mutation و divergence genomeها، مسیرها طبیعتاً می‌توانند از هم جدا شوند.

روش derivation و version این RNG باید در provenance ثبت شود.

## ترتیب mutation

Contract اولیهٔ Phase 5:

1. self-copy موفق، daughter proposal عادی را می‌سازد؛
2. substitution channel موجود طبق semantics ثبت‌شده اعمال می‌شود؛
3. حداکثر یک structural event اعمال می‌شود؛
4. genome حاصل به pending daughter proposal پایدار تبدیل می‌شود؛
5. eligibility مربوط به memory و energy بر اساس همین genome نهایی محاسبه می‌شود؛
6. اگر reproduction block شود، همان pending genome باید دوباره امتحان شود و mutation مجدد roll نشود.

این rule تاریخی را حفظ می‌کند که blocked division جهش‌ها را مرتباً دوباره قرعه‌کشی نمی‌کند.

## هزینه‌های طبیعی — بدون fitness term برای genome size

Phase 5 نباید هیچ size-dependent fitness score اضافه کند.

خود substrate فعلی هزینه‌های واقعی دارد:

- live-memory allocation برابر `working memory + genome length` است؛
- genome بلندتر سهم بیشتری از finite world memory می‌گیرد؛
- self-copy ترتیبی به `COPY_NEXT` بیشتری نیاز دارد؛
- execution برای هر instruction energy cost دارد؛
- replication بلندتر می‌تواند tick و energy بیشتری مصرف کند؛
- genome کوتاه‌تر ممکن است سریع‌تر/ارزان‌تر باشد اما functionality ضروری را از دست بدهد.

همین trade-offها برای selection کافی‌اند؛ لازم نیست host بگوید بزرگ‌تر یا کوچک‌تر «بهتر» است.

## برنامهٔ evidence مرحلهٔ پنج

### Gate 5A — Representation robustness

Structural mutation خاموش می‌ماند.

باید نشان دهیم:

- ancestor جدید چند generation self-replicate می‌کند؛
- genomeهای viable با طول‌های متفاوت با همان replication logic تکثیر می‌شوند؛
- افزودن/حذف یک instruction خنثی خارج از template حیاتی صرفاً به علت shift شدن address باعث failure نمی‌شود؛
- copied instruction count دقیقاً برابر طول genome فعلی است؛
- `DIVIDE` روی copy ناقص commit نمی‌شود؛
- deterministic replay پاس می‌شود؛
- تمام testها و checksumهای منجمد Phase Zero تا Phase Four تغییر نمی‌کنند.

فقط بعد از پاس 5A، structural mutation implementation مجاز است.

### Gate 5B — Structural mutation mechanics

Deterministic unit test و smoke campaign برای single-instruction duplication/deletion.

باید ثابت شود:

- duplication طول را دقیقاً `+1` می‌کند؛
- deletion طول را دقیقاً `-1` می‌کند، جز genome خالی که رد می‌شود؛
- mutation position روی indexهای موجود bias دست‌ساز ندارد؛
- parent/child genome hash و length ثبت می‌شوند؛
- blocked pending daughter ثابت می‌ماند؛
- child memory allocation از طول mutated genome استفاده می‌کند؛
- conservation و atomic accounting regression ندارند؛
- structural event metricها هم در JSON و هم CSV export می‌شوند.

برای پاس این gate هیچ persistence یا complexity outcome مثبتی لازم نیست.

### Gate 5C — Exposure calibration

چند structural event rate کوچک از قبل مشخص می‌شوند.

Calibration فقط مجاز است **کمترین** rateای را انتخاب کند که exposure کافی از structural event ایجاد می‌کند و integrity/reproducibility را پاس می‌کند. rate نباید بر اساس genome expansion، population بیشتر، lineage طولانی‌تر یا outcome مطلوب انتخاب شود.

Rate انتخاب‌شده و duration full campaign قبل از interpretation freeze می‌شوند.

### Gate 5D — Full variable-genome campaign

اولین campaign استنباطی با matched seed و substrate منجمد Phase 5 اجرا می‌شود.

Primary structural endpointها:

- structural eventهای attempted/committed به تفکیک type؛
- parent-to-child genome-length delta؛
- mean / median / minimum / maximum genome length؛
- genome-length variance؛
- تعداد distinct genome lengths؛
- birthهایی با non-ancestral length؛
- offspringهای structural-mutant که خودشان دست‌کم یک بار reproduction می‌کنند؛
- persistence duration / generation depth برای lineageهای non-ancestral-length.

Primary cost/accounting endpointها:

- genome memory occupied؛
- replication copy operations؛
- execution energy during replication؛
- reproduction latency در صورت قابل‌اندازه‌گیری‌بودن؛
- memory-blocked divisions؛
- total live memory و free memory.

Population/genotype/ecological metricها secondary باقی می‌مانند.

برای endpointهای paired باید uncertainty interval گزارش شود. صرفاً non-zero بودن mean genome-length difference به معنی complexity یا حتی evolvability بیشتر نیست.

## مرزهای interpretation

### در صورت evidence مستقیم، این جملات مجازند

- «ملاکت genome با طول متغیر و وراثتی را پشتیبانی می‌کند.»
- «structural mutation کور descendants کوتاه‌تر و بلندتر ایجاد کرد.»
- «برخی structural variantها تحت constraints فعلی جهان باقی ماندند و reproduction کردند.» — فقط اگر واقعاً اندازه‌گیری شود.

### Phase 5 به‌تنهایی اجازهٔ این ادعاها را نمی‌دهد

- «complexity افزایش یافت»؛
- «genome بزرگ‌تر پیشرفته‌تر است»؛
- «adaptation افزایش یافت»؛
- «intelligence پدیدار شد»؛
- «open-ended evolution به دست آمد»؛
- «gene duplication عملکرد زیستی جدید ساخت».

Genome length فقط فضای جست‌وجو را بازتر می‌کند؛ خودش complexity metric نیست.

## Mechanismهای به‌تعویق‌افتاده

### Arbitrary random insertion

فعلاً عقب می‌افتد تا rule صریح و auditشده‌ای برای ساخت operandهای instruction تازه داشته باشیم. نباید operand sampling دست host به bias تکاملی پنهان تبدیل شود.

### Segment duplication/deletion

پس از پاس single-instruction gate. Segment event چند instruction هم‌بسته را یک‌جا تغییر می‌دهد و می‌تواند jump بزرگی در memory ایجاد کند؛ بنابراین causal gate مستقل می‌خواهد.

### Inversion، translocation، recombination، crossover

خارج از scope اولین Phase 5.

### General operand mutation

برای evolvability آینده احتمالاً مهم است، اما از first structural-length intervention جدا نگه داشته می‌شود. movement-step operand mutation تاریخی Phase 3 همچنان mechanism مستقل خودش است.

## Measurementهای لازم قبل از استفادهٔ علمی

Contract اندازه‌گیری Phase 5 حداقل باید شامل این‌ها باشد:

- `genome_length_mean`
- `genome_length_median`
- `genome_length_minimum`
- `genome_length_maximum`
- `genome_length_variance`
- `distinct_genome_lengths`
- `structural_mutation_operations`
- `instruction_duplication_operations`
- `instruction_deletion_operations`
- `structural_mutation_rejected_operations`
- `variable_length_births`
- `variable_length_reproducing_offspring`
- `replication_copy_operations`
- `genome_memory_used`

Event record باید در صورت ارتباط parent length، child length، mutation type، source/deletion index، generation، parent/child ID و genotype hashها را نگه دارد.

## مرز مهندسی

Phase 5 باید backend/contract نسخه‌گذاری‌شدهٔ تازه داشته باشد و نباید بی‌صدا این موارد را بازتعریف کند:

- Phase Zero `VirtualMachine`؛
- mutation semantics منجمد Phase One؛
- Phase Two VM؛
- atomic movement پذیرفته‌شدهٔ Phase Three؛
- evidence sensing/movement پذیرفته‌شدهٔ Phase Four.

اولین implementation PR بعد از این design contract فقط باید VM/representation robustness مربوط به Gate 5A را بسازد. Structural mutation باید در PR بعدی و پس از پاس Gate 5A وارد شود.

## precedentهای طراحی بیرونی

- Thomas S. Ray / Tierra: برای کاهش brittleness تحت mutation از template-based addressing در machine code تکاملی استفاده کرد.
- Ofria & Wilke / Avida: template/head-based addressing باعث می‌شود insertion/deletion صرفاً به علت جابه‌جایی absolute memory position همهٔ flow control را خراب نکند؛ Avida point/insert/delete mutation دارد.
- Gupta et al. (2016): genome size در Digital Evolution خودش یک evolutionary outcome است که از mutation regime و selection شکل می‌گیرد؛ بزرگ‌تر بودن genome را نمی‌توان مستقیم معادل complexity دانست.
- Aevol: substitution، small indel، duplication، deletion و rearrangementهای دیگر را به‌عنوان تغییر sequence بدون beneficial effect از پیش تعیین‌شده مدل می‌کند.

منابع:

- https://people.scs.carleton.ca/~soma/biosec/readings/tierra.pdf
- https://cse.msu.edu/~ofria/pubs/2004OfriaEtAl.pdf
- https://github.com/devosoft/avida/blob/master/avida-core/support/config/avida.cfg
- https://pmc.ncbi.nlm.nih.gov/articles/PMC4867773/
- https://www.aevol.fr/model-description/detailed/

## تعریف Done برای Phase 5

Phase 5 فقط وقتی کامل است که:

1. representation مقاوم به تغییر طول برای self-replication ساخته و evidences آن ثبت شود؛
2. single-instruction duplication/deletion مستقل، audit-able و controllable باشند؛
3. genomeهای variable-length در full matched-seed campaign تولید و inherited شوند؛
4. memory، execution، reproduction و conservation accounting معتبر بمانند؛
5. deterministic replay پاس شود؛
6. artifacts کامل و paired analysis آرشیو شوند؛
7. conclusion علمی صریحاً genome-length evolvability را از complexity جدا کند.

تا قبل از پاس این gateها، ملاکت نباید ادعا کند که خودِ genome complexity در حال تکامل است.
