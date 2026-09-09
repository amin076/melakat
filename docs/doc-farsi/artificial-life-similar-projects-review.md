# بررسی تطبیقی ۲۰ پروژهٔ مهم در Artificial Life و Digital Evolution

این سند برای استفادهٔ مستقیم در توسعهٔ آیندهٔ **ملاکت** نگهداری می‌شود. هدف آن فقط مرور تاریخی نیست؛ بلکه باید در طراحی Phaseهای بعدی به‌عنوان یک سند تصمیم‌ساز استفاده شود تا روشن باشد پروژه‌های پیشین چه چیزهایی را از ابتدا در substrate قرار دادند، چه چیزهایی واقعاً emerge شد، در کجا دچار stagnation شدند، چه نوع ادعاهایی معتبر بود و چه درس‌هایی برای ملاکت قابل انتقال است.

> اصل راهنما برای ملاکت: هر بار باید میان «قابلیتی که سازنده از ابتدا در جهان گذاشته» و «قابلیتی که evolution درون جهان ساخته» تفاوت صریح حفظ شود.

## جمع‌بندی کوتاه

تاریخ Artificial Life هنوز نمونه‌ای ندارد که از یک substrate بسیار ساده و نسبتاً خنثی، بدون fitness function هدف‌دار و بدون وارد کردن مستقیم machinery شناختی، به‌صورت پایدار از self-replication به open-ended complexity، multicellularity، learning و intelligence عمومی برسد. پروژه‌هایی مثل `Tierra` emergence اکولوژیک واقعی ایجاد کردند اما اغلب به stagnation رسیدند؛ `Avida` computation پیچیده را تکامل داد ولی برای برخی computationها reward محیطی تعریف شده بود؛ `Polyworld` و `Markov Brains` رفتار و cognition غنی‌تری ایجاد کردند اما neural machinery از ابتدا در substrate وجود داشت؛ `DISHTINY` multicellularity چشمگیر ساخت اما affordanceهای گروهی و همکاری تا حدی از قبل فراهم شده بودند. این شکاف همان جایی است که ملاکت می‌تواند سؤال پژوهشی خودش را دقیق‌تر تعریف کند.

## ماتریس سریع

| # | پروژه | دوره | افراد/گروه | محور اصلی |
|---|---|---|---|---|
| 1 | von Neumann Self-Reproducing Automata | دههٔ ۱۹۴۰ تا ۱۹۶۶ | John von Neumann / Arthur Burks | بنیان نظری self-reproduction |
| 2 | Biomorphs / Blind Watchmaker | ۱۹۸۶–۱۹۸۸ | Richard Dawkins | فضای ژنوتیپی و selection |
| 3 | Tierra | ۱۹۹۰–۱۹۹۱ به بعد | Thomas S. Ray | digital organisms در memory/CPU soup |
| 4 | Echo | ۱۹۹۲–۱۹۹۴ | John Holland; Terry Jones; Stephanie Forrest | emergence از agent-resource interaction |
| 5 | Polyworld | ۱۹۹۴ به بعد | Larry Yaeger | neural agents، ecology و learning |
| 6 | Evolved Virtual Creatures | ۱۹۹۴ | Karl Sims | morphology + controller evolution |
| 7 | TechnoSphere | ۱۹۹۵–۱۹۹۶ | Jane Prophet و تیم | ecosystem آنلاین cyberbeasts |
| 8 | Creatures / Norns | ۱۹۹۶–۱۹۹۹ | Steve Grand, Dave Cliff, Anil Malhotra | brain + chemistry + genome |
| 9 | Geb | ۱۹۹۸–۲۰۰۲ | Alastair Channon, Rob Damper | آزمون open-ended evolutionary activity |
| 10 | Framsticks | ۱۹۹۶ به بعد | Maciej Komosinski, Szymon Ulatowski | body + neural control + evolution |
| 11 | Avida | دههٔ ۱۹۹۰ به بعد | Ofria, Adami, Wilke, Lenski و همکاران | experimental digital evolution |
| 12 | Aevol | اوایل دههٔ ۲۰۰۰ به بعد | Carole Knibbe, Guillaume Beslon و همکاران | genome structure و mutation |
| 13 | Stringmol | دههٔ ۲۰۰۰ به بعد | Simon Hickinbotham, Susan Stepney و همکاران | artificial chemistry |
| 14 | Evo²Sim | ۲۰۱۳–۲۰۱۶ به بعد | Charles Rocabert و EvoEvo team | genome + regulation + metabolism + ecology |
| 15 | Markov Brains | دههٔ ۲۰۱۰ | Arend Hintze, Christoph Adami و همکاران | evolvable artificial brains |
| 16 | SignalGP | ۲۰۱۷–۲۰۱۸ به بعد | Alexander Lalejini, Charles Ofria | evolving event-driven programs |
| 17 | EvoEvo | ۲۰۱۳–۲۰۱۶ | European consortium / Inria | evolvability برای software |
| 18 | POET | ۲۰۱۹ | Wang, Lehman, Clune, Stanley | co-evolution of problems and solutions |
| 19 | DISHTINY | ۲۰۱۹–۲۰۲۴+ | Matthew Moreno, Charles Ofria | digital multicellularity و individuality |
| 20 | Lenia / Flow-Lenia | ۲۰۱۸–۲۰۲۵+ | Bert Chan; Plantec et al. | continuous self-organized artificial life |

---

## ۱. von Neumann Self-Reproducing Automata

`John von Neumann` در دههٔ ۱۹۴۰، پیش از شکل‌گیری رایانه‌های امروزی، این پرسش را مطرح کرد که آیا یک ماشین می‌تواند بر اساس یک توصیف رمزشده از خودش، نسخه‌ای از خود بسازد و همان توصیف را نیز به فرزند منتقل کند. طرح او در قالب `cellular automaton` و چیزی که بعدها `universal constructor` نام گرفت توسعه یافت و پس از مرگش `Arthur Burks` آن را در کتاب *Theory of Self-Reproducing Automata* در ۱۹۶۶ منتشر کرد. اهمیت این پروژه برای ملاکت در این نیست که evolution واقعی اجرا کرده باشد؛ بلکه نشان داد `self-reproduction` می‌تواند خاصیت یک نظام محاسباتی باشد، نه چیزی مختص مادهٔ زیستی.

معماری von Neumann جدایی مهمی میان «توصیف» و «ماشین اجراکننده» داشت: یک description شبیه genome و دستگاهی که هم آن را تفسیر می‌کرد و هم کپی. نتیجهٔ تاریخی این بود که self-replication از نظر نظری در یک substrate مصنوعی ممکن است. اما سیستم پیچیده و کاملاً مهندسی‌شده بود و نشان نداد چنین machinery چگونه می‌تواند از اجزای ساده‌تر evolve شود. درس برای ملاکت: جدایی `genome` از `execution machinery` بسیار مهم است، ولی خود machinery نباید آن‌قدر قدرتمند و هوشمند طراحی شود که بخش اصلی مسئله از قبل حل شده باشد.

## ۲. Biomorphs / Blind Watchmaker

`Richard Dawkins` در میانهٔ دههٔ ۱۹۸۰ برنامهٔ `Blind Watchmaker` را ساخت و ساختارهای گرافیکی ساده‌ای به نام `biomorph` تولید کرد. چند پارامتر ژنتیکی شکل موجود را کنترل می‌کردند و mutationهای کوچک خانواده‌ای از فرم‌های بسیار متفاوت می‌ساختند. کاربر از میان فرزندان نمونهٔ بعدی را انتخاب می‌کرد؛ پس selection طبیعی نبود، بلکه `interactive/artificial selection` بود. هدف اصلی Dawkins این بود که نشان دهد حتی یک genotype-to-phenotype mapping ساده می‌تواند فضای عظیمی از morphology تولید کند، بدون آن‌که سازنده شکل نهایی را خط‌به‌خط طراحی کند.

نتیجه از نظر نمایش قدرت variation جالب بود، اما biomorphها organism مستقل نبودند: غذا نمی‌خوردند، self-replication خودمختار نداشتند، برای resource رقابت نمی‌کردند و محیط survival را تعیین نمی‌کرد؛ انسان selector بود. درس ملاکت این است که `novelty` یا پیچیدگی ظاهری به‌تنهایی به معنی life یا evolution طبیعی نیست. اگر انسان یا یک fitness metric ظاهر مطلوب را انتخاب کند، ما بیشتر evolutionary design داریم تا digital ecology مستقل.

## ۳. Tierra

`Thomas S. Ray` حدود ۱۹۹۰–۱۹۹۱ `Tierra` را ساخت تا برنامه‌های self-replicating مانند organism در یک `digital soup` زندگی کنند. هر organism یک رشتهٔ executable machine code بود؛ `CPU time` نقش یک resource محاسباتی و `memory` نقش material resource را داشت. organisms برای memory و processor time رقابت می‌کردند و mutation روی code رخ می‌داد. نکتهٔ بسیار مهم این است که Ray برای رفتارهای سطح‌بالایی مثل parasite یا cooperation fitness function مستقیم تعریف نکرده بود.

نتیجهٔ اولیه بسیار مشهور شد: genomeهای کوتاه‌تر، parasiteهایی که از replication machinery دیگران استفاده می‌کردند، host–parasite arms race و برخی شکل‌های دفاع و hyper-parasitism گزارش شدند. این برای فلسفهٔ ملاکت مهم است چون `PARASITE` یا `COOPERATE` به‌صورت opcode داده نشده بود؛ interactionها از consequences همان جهان اجرایی پدید آمدند. با این حال reviewهای بعدی نشان دادند که Tierra غالباً در مجموعهٔ محدودی از ecological dynamics می‌ماند و دچار `stagnation` می‌شد. بنابراین emergence اولیهٔ شگفت‌انگیز با `open-ended evolution` یکی نیست. درس مرکزی برای ملاکت: substrate ساده واقعاً می‌تواند behavior طراحی‌نشده ایجاد کند، ولی برای ادامهٔ novelty احتمالاً richness جهان، niches و interaction dimensions اهمیت تعیین‌کننده دارند.

## ۴. Echo

`John Holland` در اوایل دههٔ ۱۹۹۰ مدل `Echo` را برای مطالعهٔ `complex adaptive systems` پیشنهاد کرد و `Terry Jones` و `Stephanie Forrest` در Santa Fe Institute آن را توسعه دادند. Echo عمداً بسیاری از جزئیات فیزیکی واقعی را حذف کرد و مجموعه‌ای از agentها، resourceها، geography، reproduction و interactionهای مختلف را در یک جهان انتزاعی قرار داد. هدف این بود که بررسی شود آیا community structure، resource flows، trade، competition، arms races و cooperation می‌توانند از interaction تعداد زیادی agent ساده پدید آیند.

Echo نسبت به Tierra از ابتدا primitiveهای سطح‌بالای بیشتری فراهم می‌کرد؛ این کار مطالعهٔ ecology را آسان‌تر می‌کرد اما یک trade-off فلسفی ایجاد می‌کرد: هرچه primitiveهایی مثل `trade`، `offense` یا `defense` را مستقیم‌تر وارد کنیم، مشخص‌کردن سهم واقعی emergence دشوارتر می‌شود. Echo به مرجع مهمی در complex adaptive systems تبدیل شد، اما به intelligence یا open-ended digital organisms عمومی نرسید. درس برای ملاکت: abstraction کاملاً قابل قبول است، اما primitiveها باید تا حد ممکن substrate-level باشند و نتیجهٔ تکاملی موردنظر را از پیش encode نکنند.

## ۵. Polyworld

`Larry Yaeger` در Apple در ۱۹۹۴ `Polyworld` را معرفی کرد؛ یک computational ecology که agentهای آن genome داشتند، انرژی مصرف می‌کردند، می‌دیدند، حرکت می‌کردند، غذا می‌خوردند، جفت‌گیری یا حمله می‌کردند و رفتارشان توسط neural network کنترل می‌شد. architecture شبکه تا حدی از genome استخراج می‌شد و synapseها `Hebbian learning` داشتند؛ یعنی evolution بین نسل‌ها و learning در طول عمر هم‌زمان وجود داشت.

Polyworld نشان داد ترکیب evolution، embodiment و learning می‌تواند رفتارهای غنی تولید کند. اما حرکت، خوردن، جفت‌گیری، حمله و داشتن neural machinery از ابتدا در substrate موجود بود. بنابراین پروژه origin of cognition را نشان نمی‌دهد؛ بیشتر نشان می‌دهد وقتی یک مغز evolvable از ابتدا فراهم است، evolution چگونه آن را شکل می‌دهد. درس برای ملاکت: learning و neural machinery ممکن است در آینده بسیار مهم شوند، اما اگر هدف مطالعهٔ منشأ cognition است نباید آن‌ها را زود و آماده وارد کرد.

## ۶. Evolved Virtual Creatures

`Karl Sims` در ۱۹۹۴ در Thinking Machines Corporation مجموعهٔ مشهور `Evolved Virtual Creatures` را ساخت. genome هم morphology سه‌بعدی و هم controller را توصیف می‌کرد؛ blocks، joints و neural circuitry با هم evolve می‌شدند. populationها در physics simulation برای taskهایی مثل swimming، walking، jumping و رقابت برای یک object انتخاب می‌شدند.

نتایج از نظر مهندسی و بصری خیره‌کننده بودند و evolution راه‌حل‌های عجیب و غیرقابل‌پیش‌بینی ساخت. اما fitness function صریح بود؛ یعنی system برای task مشخص optimize می‌شد. بنابراین این پروژه بیشتر `evolutionary optimization` است تا digital ecology بدون هدف. برای Melakat Applied الگوی مهمی است، اما Melakat Core نباید task-specific fitness را وارد کند مگر این‌که آزمایش دقیقاً دربارهٔ آن باشد.

## ۷. TechnoSphere

`TechnoSphere` در ۱۹۹۵ به رهبری هنرمند بریتانیایی `Jane Prophet` و با تیمی شامل `Julian Saunderson` برای artificial-life engine ساخته شد. کاربران از طریق وب موجودات خود را طراحی و وارد جهانی سه‌بعدی می‌کردند؛ terrain، vegetation و cyberbeastها در یک محیط مشترک وجود داشتند. اهمیت تاریخی پروژه این بود که ALife را از آزمایشگاه بسته به یک ecosystem عمومی و شبکه‌ای برد.

با این حال هدف پروژه ترکیبی از هنر، interactivity، ecology و virtual embodiment بود، نه یک برنامهٔ دقیق برای مطالعهٔ open-ended evolution. درس برای ملاکت این است که در آینده می‌توان public world و مشارکت کاربران داشت، اما visualization و user engagement نباید جای research reproducibility و measurement را بگیرد.

## ۸. Creatures / Norns

`Creatures` در اواخر ۱۹۹۶ عرضه شد و توسط `Steve Grand`، `Dave Cliff`، `Anil Malhotra` و همکاران توسعه یافت. Nornها modular recurrent neural network، Hebbian learning، artificial biochemistry، metabolism، hormones، development و variable-length genetic encoding داشتند. reproduction جنسی، mutation و gene duplication نیز وجود داشت. هدف Grand ساخت یک organism نسبتاً holistic بود، نه صرفاً یک neural agent.

نتیجه virtual creatures بسیار غنی و convincing بود، اما اکثر machineryهای بنیادی از ابتدا مهندسی شده بودند: brain architecture، chemical system، sensory inputs و object interactionها. بنابراین Creatures نشان می‌دهد می‌توان یک virtual organism پیچیده ساخت، نه این‌که پیچیدگی چگونه از substrate بسیار ساده پدید می‌آید. درس برای ملاکت این است که قابلیت‌های جذاب را نباید یکجا وارد کرد؛ هر capability باید hypothesis و evidence gate خودش را داشته باشد.

## ۹. Geb

`Alastair Channon` و `Rob Damper` در اواخر دههٔ ۱۹۹۰ `Geb` را برای بررسی `evolutionary emergence` توسعه دادند. Channon بعدها معیارهای evolutionary activity را روی سیستم اعمال کرد و گزارش کرد که Geb بر اساس آن معیارها رفتار `unbounded evolutionary activity` نشان می‌دهد. اما نکتهٔ روش‌شناختی مهم این است که خود پژوهشگران این را پایان مسئله تلقی نکردند و ضعف metricها و normalization را بررسی و اصلاح کردند.

درس برای ملاکت بسیار مهم است: حتی اگر یک metric بگوید complexity یا open-endedness زیاد شده، این claim باید جداگانه falsifiable باشد. metric ممکن است representation churn یا novelty سطحی را با innovation functional اشتباه بگیرد. بنابراین در ملاکت `novelty`، `complexity`، `adaptation` و `evolutionary activity` باید مفاهیم جداگانه بمانند.

## ۱۰. Framsticks

`Maciej Komosinski` و `Szymon Ulatowski` از ۱۹۹۶ `Framsticks` را توسعه دادند. موجودات genotype برای بدن و neural network داشتند، sensor–brain–effector loop، mutation/crossover، physics و energy balance نیز وجود داشت. پروژه هم directed evolution با fitness مشخص و هم experimentهای endogenous را پشتیبانی می‌کند.

Framsticks به یک simulator پژوهشی پایدار تبدیل شد و کاربردهای زیادی در morphology، locomotion و evolutionary algorithms پیدا کرد، اما به AGI یا open-ended intelligence نرسید. درس برای ملاکت: یک ALife platform می‌تواند حتی بدون ساخت intelligence ارزش علمی بسیار بالایی داشته باشد. همچنین اگر morphology یا sensor/effectorهای غنی اضافه شوند باید روشن باشد آن‌ها substrate هستند یا emergent capability.

## ۱۱. Avida

`Avida` در دههٔ ۱۹۹۰ از سنت Tierra رشد کرد و توسط `Charles Ofria`، `Christoph Adami`، `Claus Wilke` و بعداً پژوهشگران متعدد توسعه یافت. پلتفرم برای experimentهای کنترل‌شده با self-replicating computer programs و instrumentation دقیق ساخته شد. در مقالهٔ مشهور Nature در ۲۰۰۳، `Lenski`، `Ofria`، `Pennock` و `Adami` نشان دادند digital organisms می‌توانند تابع منطقی پیچیدهٔ `EQU` را تکامل دهند و lineage analysis نشان داد این feature بر پایهٔ stepping stoneهای قبلی ساخته شده است.

اما در بسیاری از setupهای Avida، انجام logic functionها با CPU-time reward همراه است. بنابراین محیط از قبل به یک computation خاص value می‌دهد. Avida برای ملاکت دو درس دارد: instrumentation و experimental rigor آن بسیار ارزشمند است؛ اما reward architecture باید با احتیاط وارد شود، چون اگر هدف Melakat Core مشاهدهٔ emergence غیرهدف‌دار است، task reward می‌تواند مسئله را به genetic programming نزدیک کند.

## ۱۲. Aevol

`Aevol` توسط `Carole Knibbe`، `Guillaume Beslon` و همکاران توسعه یافت و روی realism نسبی genome structure و mutation process تمرکز دارد. insertion، deletion، duplication، inversion و translocation می‌توانند architecture ژنوم را تغییر دهند. یک داستان مهم پروژه این بود که پژوهشگران ابتدا دنبال modularity بودند اما به نتیجهٔ مورد انتظار نرسیدند؛ در عوض رابطهٔ mutation rate و genome size به یک کشف مهم‌تر منجر شد.

این برای ملاکت lesson مهمی است: experiment لازم نیست hypothesis جذاب ما را تأیید کند تا موفق باشد. observation غیرمنتظره ممکن است science اصلی باشد. همچنین Phase 5 ملاکت با variable-length genome به این خانواده نزدیک شده است، ولی همان‌طور که contract ملاکت می‌گوید `genome length ≠ complexity`.

## ۱۳. Stringmol

`Stringmol` توسط `Simon Hickinbotham`، `Susan Stepney` و همکاران در University of York توسعه یافت. به‌جای organism monolithic، یک artificial chemistry از رشته‌هایی دارد که می‌توانند هم information و هم function حمل کنند. این طراحی به RNA-world نزدیک‌تر است و برای مطالعهٔ self-replication، parasitism و `semantic closure` استفاده شده است.

برای ملاکت، Stringmol پاسخ مهمی به نگرانی دربارهٔ opcodeهای آماده می‌دهد: می‌توان substrate را پایین‌تر برد تا replication از interaction اجزای مولکول‌مانند حاصل شود. مشکل این است که فضای جست‌وجو عظیم‌تر و evolution بسیار کندتر می‌شود. این احتمالاً یک branch پژوهشی آینده برای origin of replication machinery است، نه جایگزین فوری engine فعلی.

## ۱۴. Evo²Sim

`Evo²Sim` توسط `Charles Rocabert` و همکاران در چارچوب پروژهٔ `EvoEvo` توسعه یافت. organismها circular genome با promoter، enzyme-coding units و transcription factors دارند و از genome هم regulatory network و هم metabolic network ساخته می‌شود. system برای bacterial in silico experimental evolution طراحی شده است.

پژوهش‌ها emergence ecotypeهای مختلف، metabolic by-product use و regulationهایی شبیه operon را بررسی کرده‌اند. اما بسیاری از biochemical abstractions از ابتدا تعریف شده‌اند. درس برای ملاکت: ecology غنی ممکن است از resource cycles و by-products پدید آید و این نوع substrate-level interaction شاید بسیار بهتر از opcodeهای سطح‌بالایی مثل `COOPERATE` باشد.

## ۱۵. Markov Brains

`Markov Brains` خط پژوهشی `Arend Hintze`، `Christoph Adami` و همکاران است. یک evolvable network از computational gates است که sensory inputs، state و outputs را ترکیب می‌کند. evolution topology و logic داخلی شبکه را شکل می‌دهد و در experimentهای predator–prey، memory و swarming به کار رفته است.

این پروژه نشان می‌دهد evolution می‌تواند controllerهای پیچیده و رفتارهای شناختی‌مانند بسازد، اگر یک brain substrate قدرتمند از ابتدا وجود داشته باشد. اما origin of brain را توضیح نمی‌دهد. برای ملاکت، Markov Brain می‌تواند یک مقصد یا comparison مهم باشد؛ نه چیزی که در core primitive زودهنگام قرار دهیم.

## ۱۶. SignalGP

`Alexander Lalejini` و `Charles Ofria` در ۲۰۱۷–۲۰۱۸ `SignalGP` را معرفی کردند؛ یک genetic programming representation برای event-driven programs. functions و events tagهای evolvable دارند و eventها نزدیک‌ترین matching function را فعال می‌کنند. در taskهای coordination و distributed leader election، representation event-driven عملکرد مناسبی نشان داد.

SignalGP یکی از مستقیم‌ترین پل‌ها میان digital evolution و software است. اما fitness بیرونی دارد و هدفش ساخت یک biosphere خنثی نیست. درس برای ملاکت: representation خودش بخشی از physics تکامل است. اگر روزی event-driven execution اضافه شود، باید به‌عنوان تغییر بنیادی representational contract مطالعه شود، نه صرفاً feature مهندسی.

## ۱۷. EvoEvo

پروژهٔ اروپایی `EvoEvo` از ۲۰۱۳ تا ۲۰۱۶ با هماهنگی `Inria` اجرا شد. هدفش مطالعهٔ evolution of evolvability و انتقال اصول آن به information science و software بود، مخصوصاً برای problemهایی که specification آن‌ها ناشناخته، تغییرپذیر یا بسیار پیچیده است.

پروژه الگوریتم‌ها، مدل‌ها و ابزارهای متعددی ساخت ولی به یک software ecosystem خودمختار و عمومی نرسید. درس برای ملاکت: ایدهٔ استفاده از evolution برای software جدی و پژوهش‌شده است، اما بهتر است Melakat Core و Melakat Applied جدا بمانند. Core سؤال علمی را نگه می‌دارد؛ Applied بعدها mechanismهای مفید کشف‌شده را برای مسائل engineering به کار می‌برد.

## ۱۸. POET

`POET` یا `Paired Open-Ended Trailblazer` در ۲۰۱۹ توسط `Rui Wang`، `Joel Lehman`، `Jeff Clune` و `Kenneth Stanley` معرفی شد. به‌جای ثابت‌بودن task، environmentها و solutionها هم‌زمان ایجاد و evolve می‌شوند و solutionها میان environmentها transfer می‌شوند. هدف عبور از محدودیت curriculum ثابت و استفاده از stepping stoneهای غیرمنتظره بود.

POET digital organism زیستی ندارد، ولی برای مسئلهٔ stagnation مهم است. یک درس ممکن برای ملاکت این است که world باید history و dynamics خودش را داشته باشد و niches جدید بسازد. اما اگر environment generator عمداً novelty یا solvability را reward کند، دوباره جهت‌گیری طراحی‌شده وارد system می‌شود.

## ۱۹. DISHTINY

`DISHTINY` توسط `Matthew Andres Moreno` و `Charles Ofria` برای مطالعهٔ major transitions و multicellularity توسعه یافت. cells در spatial world زندگی می‌کنند، communication و resource sharing دارند و hereditary groups می‌سازند. پژوهش‌ها cooperative reproduction، developmental patternها و morphologyهای چندسلولی متفاوت را گزارش کرده‌اند.

اما خود پژوهشگران تصریح کرده‌اند multicellularity از یک substrate کاملاً impartial ظاهر نشده است: cellها از ابتدا ابزار hereditary grouping، kin recognition، communication و sharing داشتند و collaboration در برخی setupها reward می‌شد. این نکته مستقیماً با فلسفهٔ ملاکت مرتبط است. اگر ما `kin recognition` یا `attach` را بدهیم، بعداً نمی‌توانیم ادعا کنیم آن concept emerge شده است. DISHTINY برای مطالعهٔ multicellularity بسیار مهم است، ولی claim boundary باید روشن بماند.

## ۲۰. Lenia / Flow-Lenia

`Bert Wang-Chak Chan` از ۲۰۱۸ `Lenia` را توسعه داد؛ یک continuous cellular automaton که صدها pattern self-organized و متحرک تولید می‌کند. `Flow-Lenia` در ۲۰۲۳ توسط `Erwan Plantec`، `Gautier Hamon`، `Mayalen Etcheverry`، `Pierre-Yves Oudeyer`، `Clément Moulin-Frier` و `Bert Chan` mass conservation و parameter localization را اضافه کرد تا چند species با rules محلی متفاوت بتوانند در یک world coexist و interact کنند.

این خانواده برای ملاکت بسیار مهم است چون individuality در آن الزاماً object صریح engine نیست؛ organism می‌تواند یک localized pattern در field باشد. این احتمالاً یکی از عمیق‌ترین سؤال‌های آیندهٔ ملاکت است: آیا باید `Organism` همیشه یک class صریح باشد، یا می‌توان روزی substrateای ساخت که individuality خودش emerge شود؟ Flow-Lenia هنوز open-ended intelligence عمومی را نشان نداده است، اما به ما یادآوری می‌کند که definition خودِ organism نیز می‌تواند موضوع پژوهش باشد.

---

## الگوهای مشترک و سرنوشت پروژه‌ها

۱. هیچ پروژه‌ای مسیر کامل `simple replicator → multicellular organism → learning → general intelligence → open-ended digital civilization` را بدون طراحی بیرونی طی نکرده است.

۲. هرجا cognition چشمگیرتر بوده، معمولاً machinery قدرتمندی مثل neural network، Markov Brain یا event-driven GP از ابتدا وجود داشته است.

۳. هرجا computation پیچیده به‌طور روشن evolve شده، اغلب task/fitness/reward تعریف‌شده وجود داشته است.

۴. پروژه‌های خنثی‌تر مثل Tierra emergence واقعی ایجاد کرده‌اند ولی با stagnation روبه‌رو شده‌اند.

۵. richness محیط و co-evolution می‌تواند novelty را بیشتر کند، ولی خطر وارد کردن پنهان هدف یا capability را نیز بالا می‌برد.

۶. پروژه‌هایی مثل Aevol نشان می‌دهند نتیجهٔ غیرمنتظره ممکن است از hypothesis اولیه مهم‌تر باشد.

۷. پروژه‌های جدیدتر مثل DISHTINY و Flow-Lenia نشان می‌دهند major transitions، individuality و open-endedness هنوز frontier فعال پژوهش هستند.

## نتیجهٔ مستقیم برای هدف ملاکت

بهترین North Star فعلی این نیست که از ابتدا وعده بدهیم ملاکت `AGI` یا `wisdom` خواهد ساخت. هدف علمی قوی‌تر این است:

> ساخت یک جهان محاسباتی محدود، reproducible و تا حد ممکن کم‌جهت که در آن heredity، variation، resource constraints و interaction اجازه دهند بررسی کنیم چه نوع organization و computation بدون task-specific fitness و بدون hard-code کردن strategy می‌تواند پدید آید.

اگر intelligence هرگز ظاهر نشود، پروژه لزوماً شکست نخورده است؛ ممکن است دربارهٔ limits of open-ended evolution، شرایط لازم برای complexity، نقش representation و constraints و تفاوت میان novelty و adaptation نتایج علمی مهمی تولید کند. اگر در آینده mechanismهای عمومی computation، multicellularity یا learning واقعاً emerge شوند، آن‌وقت یک شاخهٔ `Melakat Applied` می‌تواند بررسی کند آیا این mechanismها برای software engineering یا autonomous computing مفیدند.

## درس‌های مستقیم برای Roadmap آیندهٔ ملاکت

- **Tierra:** core world را بدون task-specific fitness نگه داریم، ولی stagnation را به‌صورت علمی مطالعه کنیم.
- **Avida:** instrumentation، replay، controls و evidence discipline را تقویت کنیم، بدون اینکه rewardهای دلخواه را بی‌دلیل وارد کنیم.
- **Aevol:** mutation operator و genome representation را بخشی از physics جهان بدانیم، نه ابزار رسیدن به نتیجهٔ مطلوب.
- **DISHTINY:** هر affordance برای cooperation یا multicellularity باید در claim boundary ثبت شود.
- **Flow-Lenia:** در آینده حتی تعریف object-level organism را نیز به‌عنوان یک assumption قابل‌آزمایش در نظر بگیریم.
- **SignalGP/Markov Brains:** representation و cognition machinery می‌توانند بسیار قدرتمند باشند، اما ورودشان باید به‌عنوان تغییر علمی عمده ثبت شود.
- **EvoEvo:** مسیر پژوهشی و مسیر کاربرد نرم‌افزاری را از یکدیگر جدا نگه داریم.

## منابع اصلی

1. John von Neumann; Arthur W. Burks (ed.), *Theory of Self-Reproducing Automata* (1966): https://search.worldcat.org/title/1085642060
2. Richard Dawkins, *The Evolution of Evolvability* / Biomorphs: https://biomorphbuilder.com/dawkins-paper/
3. Thomas S. Ray publications, including *An Approach to the Synthesis of Life* (1991): https://tomray.me/pubs/
4. Tierra review in *Symbiosis in Digital Evolution*: https://www.frontiersin.org/journals/ecology-and-evolution/articles/10.3389/fevo.2021.739047/full
5. Forrest & Jones, *Modeling Complex Adaptive Systems With Echo*: https://www.santafe.edu/research/results/working-papers/modeling-complex-adaptive-systems-with-echo
6. Polyworld background: https://pmc.ncbi.nlm.nih.gov/articles/PMC2801533/
7. Karl Sims, *Evolved Virtual Creatures* (1994): https://karlsims.com/evolved-virtual-creatures.html
8. Jane Prophet, TechnoSphere background: https://www.jstor.org/stable/1576397
9. Grand, Cliff & Malhotra, *Creatures: Artificial Life Autonomous Software Agents for Home Entertainment* (1997): https://doi.org/10.1145/267658.267663
10. *The Creatures Global Digital Ecosystem* (1999): https://direct.mit.edu/artl/article/5/1/77/2314/The-Creatures-Global-Digital-Ecosystem
11. Alastair Channon, *Passing the ALife Test* (2001): https://keele-repository.worktribe.com/output/403344
12. Framsticks objectives and scope: https://www.framsticks.com/node/303
13. Ofria & Wilke, *Avida: A Software Platform for Research in Computational Evolutionary Biology* (2004): https://direct.mit.edu/artl/article/10/2/191/2455/Avida-A-Software-Platform-for-Research-in
14. Lenski, Ofria, Pennock & Adami, *The evolutionary origin of complex features* (Nature, 2003): https://www.nature.com/articles/nature01568
15. Aevol model overview: https://www.aevol.fr/model-description/purpose-and-overview/
16. *The Surprising Creativity of Digital Evolution* — Aevol case: https://direct.mit.edu/artl/article/26/2/274/93255/The-Surprising-Creativity-of-Digital-Evolution-A
17. Stringmol Artificial Chemistry: https://stringmol.york.ac.uk/
18. *Semantic closure demonstrated by the evolution of a universal constructor architecture in an artificial chemistry* (2017): https://pmc.ncbi.nlm.nih.gov/articles/PMC5454285/
19. Evo²Sim repository and model: https://github.com/charlesrocabert/Evo2Sim
20. Hintze et al., *Markov Brains: A Technical Introduction* (2017): https://arxiv.org/abs/1709.05601
21. *Evolution of Swarming Behavior Is Shaped by How Predators Attack* (2016): https://direct.mit.edu/artl/article/22/3/299/2845/Evolution-of-Swarming-Behavior-Is-Shaped-by-How
22. Lalejini & Ofria, *Evolving Event-driven Programs with SignalGP* (2018): https://lalejini.com/GECCO-2018-Evolving-Event-driven-Programs-with-SignalGP/
23. European Commission CORDIS — EvoEvo: https://cordis.europa.eu/project/id/610427
24. Wang, Lehman, Clune & Stanley, POET (2019): https://arxiv.org/abs/1901.01753
25. Moreno & Ofria, *Exploring Evolved Multicellular Life Histories in an Open-Ended Digital Evolution System* (2022): https://www.frontiersin.org/journals/ecology-and-evolution/articles/10.3389/fevo.2022.750837/full
26. Bert Chan, *Lenia: Biology of Artificial Life* (2019): https://www.complex-systems.com/abstracts/v28_i03_a01/
27. Plantec et al., *Flow-Lenia* (2023): https://research.google/pubs/flow-lenia-towards-open-ended-evolution-in-cellular-automata-through-mass-conservation-and-parameter-localization/

## وضعیت سند

این سند یک **مرجع پژوهشی زنده** برای Phaseهای آیندهٔ ملاکت است. هرگاه طراحی جدیدی دربارهٔ memory، morphology، communication، multicellularity، learning، cognition، environmental dynamics یا software-facing capabilities پیشنهاد شود، باید پیش از implementation با پروژه‌های مناسب این سند مقایسه و assumptionها/claim boundaries ثبت شوند.
