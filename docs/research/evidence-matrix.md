# ماتریس شواهد و پیامدهای طراحی

آخرین به‌روزرسانی: 2026-09-04

این فایل خلاصه‌ی قابل‌ممیزیِ ادعاهای مهم گزارش پژوهش است. «درجه» کیفیت منبع و نزدیکی آن به ادعا را نشان می‌دهد، نه میزان جذابیت نتیجه.

| شناسه | ادعای قابل‌بررسی | منبع اصلی | درجه | پیامد برای Melakat | آزمون یا محدودیت |
|---|---|---|---|---|---|
| E01 | یک تعریف کاری رایج از حیات، سامانه‌ی شیمیایی خودپایدار با توان تکامل داروینی است | [NASA: What Is Life?](https://science.nasa.gov/exoplanets/what-is-life/) | A/B | خودتکثیری، وراثت و تغییر جمعیتی باید از هم جدا ثبت شوند | این تعریف مخصوصاً برای حیات زمینی است و تعریف فلسفی نهایی نیست |
| E02 | سامانه‌های زنده بازند و برای نگهداری و کار با محیط انرژی مبادله می‌کنند | [OpenStax: Energy and Metabolism](https://openstax.org/books/concepts-biology-2e/pages/4-1-energy-and-metabolism) | A/B | منبع ورودی، موجودی و هزینه باید در مدل جدا باشند | واحد انرژی دیجیتال، اندازه‌گیری انرژی فیزیکی نیست |
| E03 | وراثت، تنوع ارثی و تولیدمثل نابرابر برای تغییر تکاملی ضروری‌اند | [OpenStax: Understanding Evolution](https://openstax.org/books/biology-2e/pages/18-1-understanding-evolution) | A/B | mutation باید ارثی و reproduction باید دارای پیامد متفاوت باشد | drift می‌تواند بدون selection هم فراوانی‌ها را تغییر دهد |
| E04 | تکامل در سطح جمعیت به‌صورت تغییر فراوانی تبار یا allele دیده می‌شود | [OpenStax: Population Genetics](https://openstax.org/books/biology-2e/pages/19-2-population-genetics) | A/B | معیار اصلی، population و lineage است، نه یک فرد یا یک اجرای منفرد | جمعیت کوچک به drift حساس است |
| E05 | یک protocell ساده به محفظه و اطلاعات قابل‌تکثیر نیاز دارد | [Schrum, Zhu & Szostak](https://pmc.ncbi.nlm.nih.gov/articles/PMC2926753/) | A | genome را نباید با organism یکی گرفت؛ memory boundary مهم است | analog دیجیتال هنوز غشا و شیمی ندارد |
| E06 | Cellular automata بر حالت‌های گسسته و قانون به‌روزرسانی محلی تکیه دارند | [SEP: Cellular Automata](https://plato.stanford.edu/entries/cellular-automata/) | B | state، tick و transition rule باید صریح باشند | Melakat الزاماً cellular automaton نیست |
| E07 | Digital physics ادعایی فلسفی و مورد مناقشه درباره‌ی بنیادی‌بودن محاسبه است | [SEP: Digital Physics](https://plato.stanford.edu/entries/digital-physics/) | B | از آن فقط برای الهام مفهومی استفاده کنیم | این منبع اعتبار تجربی برای قوانین Melakat نمی‌دهد |
| E08 | Tierra جداسازی ارگانیسم دیجیتال از ماشین واقعی و استفاده از VM را نشان داد | [Ray: Tierra](https://faculty.cc.gatech.edu/~turk/bio_sim/articles/tierra_thomas_ray.pdf) | A/B | ژنوم فقط در VM محدود اجرا شود؛ OS و network ممنوع | زبان، scheduler و تخصیص حافظه نتیجه را تعیین می‌کنند |
| E09 | در Tierra، CPU time و memory بخشی از اقتصاد محیط بودند و تعاملات جدید پدیدار شدند | [Ray: Tierra](https://faculty.cc.gatech.edu/~turk/bio_sim/articles/tierra_thomas_ray.pdf) | A/B | محدودیت منابع می‌تواند selection ضمنی بسازد | نتایج Tierra را نباید بدون بازتولید به Melakat تعمیم داد |
| E10 | Avida کپی دستوربه‌دستور، mutation و genotype–phenotype map را برای مطالعه‌ی دقیق فراهم می‌کند | [Fortuna et al.](https://doi.org/10.1371/journal.pcbi.1005414) | A | replication، execution و phenotype باید جدا لاگ شوند | task و merit در Avida با هدف بدون reward ما متفاوت‌اند |
| E11 | برخی نتایج Computational Life ادعا می‌کنند self-replicatorها بدون explicit fitness landscape می‌توانند ظاهر شوند | [Google Research](https://research.google/pubs/computational-life-how-well-formed-self-replicating-programs-emerge-from-simple-interaction/) و [arXiv](https://arxiv.org/abs/2406.19108) | C | emergence را جدا از evolution seeded آزمایش کنیم | پیش‌چاپ است و نتیجه به زبان و شرایط برخورد حساس است |
| E12 | امکان منطقی یک replicator با احتمال ظهور عملی آن یکی نیست | [Computational Life](https://arxiv.org/abs/2406.19108) | C | «قابل‌اجرا» و «قابل‌ظهور» دو معیار جدا باشند | باید با seedهای مستقل و تعداد اجرای کافی اندازه‌گیری شود |
| E13 | Stringmol و Squirm3 نشان می‌دهند اطلاعات می‌تواند با machinery، chemistry و compartment درهم‌تنیده باشد | [Stringmol](https://stringmol.york.ac.uk/) و [Squirm3](https://github.com/timhutton/squirm3) | A/C | فازهای آینده می‌توانند از genome-only به artificial chemistry بروند | برای V0 فضای حالت و پیچیدگی زیاد است |
| E14 | Aevol و MABE2 اهمیت نسخه‌بندی، تبار، data logging و modular experiment را نشان می‌دهند | [Aevol](https://www.aevol.fr/) و [MABE2](https://github.com/mercere99/MABE2) | A/C | reproducibility باید از اولین prototype طراحی شود | امکانات غنی آن‌ها نباید به قوانین V0 اضافه شوند |
| E15 | self-replication دقیق با self-reproduction دارای variation و heredity یکسان نیست | [MIT Press: Self-Reproduction and Evolution in Cellular Automata](https://direct.mit.edu/artl) و [Frontiers review](https://www.frontiersin.org/journals/ecology-and-evolution/articles/10.3389/fevo.2021.739047/full) | B | آزمایش کپی بدون mutation باید control باشد، نه evidence تکامل | تعریف واژه‌ها در مقالات مختلف همیشه یکسان نیست |
| E16 | هزینه‌ی thermodynamic واقعیِ پاک‌کردن اطلاعات، مربوط به سخت‌افزار فیزیکی است | [Nature Reviews Physics: Landauer’s principle](https://www.nature.com/articles/s42254-021-00400-8) | A/B | energy cost در VM باید به‌عنوان قرارداد انتزاعی مستند شود | از این اصل نمی‌توان cost دلخواهِ هر instruction را استخراج کرد |
| E17 | open-ended evolution به معنی رشد خودکار پیچیدگی نیست | [Open-Ended Evolution review](https://www.frontiersin.org/journals/ecology-and-evolution/articles/10.3389/fevo.2021.630189/full) | B | complexity و novelty معیارهای مشاهده‌اند، نه reward اولیه | باید metric را طوری نسازیم که نتیجه را از قبل تعیین کند |

## درجه‌بندی منابع

- A: مقاله‌ی داوری‌شده، منبع دانشگاهی معتبر یا مستندات رسمی قابل‌اعتماد.
- B: مرور علمی یا مدخل دانشگاهی که چند نتیجه را جمع‌بندی می‌کند.
- C: پیش‌چاپ، مخزن کد یا بازتولید آموزشی؛ برای ساخت فرضیه و آزمایش اولیه مفید است، اما ادعای نهایی نیست.

## نتیجه‌ی موقت

برای Phase 0، شواهد از این تصمیم‌ها پشتیبانی می‌کنند:

1. VM محدود و sandbox‌شده.
2. genome به‌عنوان داده و organism به‌عنوان genome به‌علاوه‌ی state و resource budget.
3. وراثت و mutation جدا از phenotype و outcome.
4. محدودیت واقعیِ حافظه یا انرژی، بدون explicit fitness function.
5. seeded evolution و emergence در دو آزمایش مجزا.
6. اجرای چند seed، ثبت lineage و ذخیره‌ی نتایج ناموفق.
7. energy به‌عنوان واحد انتزاعی مدل، با توضیح روشن درباره‌ی تفاوت آن با فیزیک واقعی.
