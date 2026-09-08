# گزارش تکمیل مرحلهٔ پنج — Evolvability ژنوم

## وضعیت

**مرحلهٔ پنج از نظر evidence ثبت‌شده کامل شده است و فقط merge نهایی repository/CI باقی مانده است.**

پرسش محدود و مشخص مرحلهٔ پنج این بود:

> آیا ملاکت می‌تواند سقف مصنوعی طول ثابت ژنوم را حذف کند و تغییر طول ژنوم را به‌صورت کور، وراثتی و قابل‌تکامل ممکن کند، بدون آنکه ژنوم بزرگ‌تر را reward کند یا complexity را از پیش تعریف کند؟

Evidence نهایی برای مدل فعلی پاسخ **بله** می‌دهد. این نتیجه به‌هیچ‌وجه به‌تنهایی افزایش complexity، adaptation، intelligence یا open-ended evolution را اثبات نمی‌کند.

## چرا مرحلهٔ پنج لازم بود؟

پیش از Phase 5، `mutation` می‌توانست `opcode`ها را جایگزین کند، اما طول genome عملاً ثابت بود. self-replicator اولیه طول خودش را در copy loop کد کرده بود و از آدرس‌های مطلق برای `JUMP` استفاده می‌کرد. در چنین representationی، اضافه‌کردن مستقیم `insertion/deletion` بیشتر باعث شکستن مصنوعی برنامه بر اثر جابه‌جایی indexها می‌شد تا اینکه فضای evolvability واقعی را باز کند.

به همین دلیل Phase 5 ابتدا خود substrate را برای تغییر طول مقاوم کرد و سپس structural mutation را فعال کرد. موتورهای منجمد Phase Zero تا Phase Four دست‌نخورده باقی ماندند.

## Gate 5A — replication مقاوم به تغییر طول

PR #31 یک backend مستقل Phase Five اضافه کرد که شامل این primitiveهاست:

- `COPY_NEXT`: در هر اجرا یک instruction را از genome فعلی خود organism به‌صورت sequential کپی می‌کند؛
- daughter replication buffer پویا؛
- علامت‌های template خنثی `NOP_A` و `NOP_B`؛
- `JUMP_TEMPLATE` و `JUMP_TEMPLATE_IF_ZERO` برای flow control نسبی/template-based؛
- اجازهٔ `DIVIDE` فقط پس از کامل‌شدن self-copy؛
- ancestor جدیدی که نه طول genome خود را hard-code می‌کند و نه target مطلق replication loop را.

نسخه‌های Gate 5A:

- world contract: `phase-five-evolvability-0.1`
- engine: `phase-five-vm-0.1`
- measurement: `phase-five-measurement-0.1`

`VM` مرحلهٔ پنج مستقل از مسیرهای منجمد قبلی است.

## Gate 5B — مکانیک structural mutation کور

PR #32 کانال structural mutation را به‌صورت opt-in اضافه کرد. اگر این کانال تنظیم نشود، semantics گیت 5A حفظ می‌شود.

دو operator اولیه عمداً بسیار ساده هستند:

- **single-instruction tandem duplication**: یک instruction موجود را همراه همان operandهای فعلی خودش کپی می‌کند و طول دقیقاً `+1` می‌شود؛
- **single-instruction deletion**: یک instruction موجود را حذف می‌کند و اگر genome بیش از یک instruction داشته باشد طول دقیقاً `-1` می‌شود.

هیچ instructionی از طرف host «ضروری» یا محافظت‌شده اعلام نشده است. اگر حذف یا duplication زیان‌آور باشد، selection طبیعی داخل مدل باید نتیجه را تعیین کند.

برای هر daughter proposal حداکثر یک structural event مجاز است. ترتیب mutation چنین است:

1. organism self-copy را کامل می‌کند؛
2. blind opcode substitution اعمال می‌شود؛
3. حداکثر یک structural event با random stream مستقل و deterministic اعمال می‌شود؛
4. genome پیشنهادی فرزند ثابت می‌ماند تا بررسی‌های عادی energy/memory برای reproduction حل شوند.

نسخهٔ structural RNG:

`phase-five-structural-rng-0.1`

نسخه‌های evidence مکانیک structural:

- engine: `phase-five-vm-0.2`
- measurement: `phase-five-measurement-0.2`

## هزینه‌های طبیعی؛ بدون reward برای complexity

Phase 5 هیچ `fitness term` تازه‌ای برای اندازهٔ genome اضافه نکرد.

اندازهٔ genome از قبل به هزینه‌های واقعی substrate وصل است:

- structural memory allocation شامل طول genome است؛
- هر instruction اضافی باید در replication واقعاً کپی شود؛
- VM execution هزینهٔ انرژی دارد؛
- world memory محدود می‌تواند reproduction را block کند.

پس genome بلندتر فقط به‌دلیل بلندتر بودن reward نمی‌شود و genome کوتاه‌تر نیز صرفاً به‌دلیل کوچک‌تر بودن پاداش نمی‌گیرد.

`genome length` فقط یک measurement ساختاری است، نه `complexity score`.

## Gate 5C — calibration فقط بر اساس exposure

Spec:

`experiments/phase-five/structural-event-rate-calibration.json`

شرایط:

- ۸ `seed` matched؛
- ۱۰۰۰ `tick` برای هر run؛
- جهان همگن و non-spatial؛
- substitution rate برابر `0.01`؛
- احتمال conditional برابر `0.5` برای duplication و `0.5` برای deletion؛
- نرخ‌های candidate: `0.01`، `0.025`، `0.05` و `0.10`.

قانون انتخاب پیش از دیدن نتایج ثبت شد: **کمترین** candidate باید همهٔ این شروط را پاس کند:

- حداقل ۱۶ structural event committed در مجموع؛
- exposure در حداقل ۶ run از ۸ run؛
- حداقل ۴ duplication؛
- حداقل ۴ deletion؛
- validation و deterministic replay پاس شوند.

استفاده از افزایش طول genome، population، reproduction، survival، lineage persistence یا هر outcome مطلوب دیگری برای انتخاب rate ممنوع بود.

### نتیجهٔ calibration

| نرخ structural event | eventهای committed | runهای exposed | duplication | deletion | Gate |
| ---: | ---: | ---: | ---: | ---: | --- |
| `0.01` | 11 | 6/8 | 6 | 5 | FAIL |
| `0.025` | 26 | 7/8 | 12 | 14 | **PASS — انتخاب شد** |
| `0.05` | 50 | 8/8 | 23 | 27 | PASS |
| `0.10` | 83 | 8/8 | 37 | 46 | PASS |

بنابراین پیش از اجرای full campaign، نرخ **`0.025`** freeze شد.

Calibration validation پاس شد و deterministic replay کاملاً identical بود.

## Gate 5D — full matched-seed variable-genome campaign

Spec منجمد:

`experiments/phase-five/variable-genome-full.json`

طراحی:

- ۳۰ `seed` matched؛
- دو condition؛
- ۲۰۰۰ `tick` برای هر run؛
- در مجموع ۶۰ اجرای اصلی؛
- representation، substitution mutation، energy، memory، execution و reproduction در هر دو condition یکسان؛
- duplication/deletion probability برابر `0.5`؛
- تنها تفاوت causal موردنظر، structural event rate بود.

Conditionها:

- `structural-off`: نرخ `0.0`
- `structural-balanced-on`: نرخ calibration‌شدهٔ `0.025`

## سلامت evidence

Full gate پاس شد:

- runهای کامل: **60/60**؛
- validation failure: **0**؛
- deterministic replay: **PASS / identical**؛
- structural event committed در control: **0**؛
- structural event committed در treatment: **97**؛
- runهای treatment دارای structural event: **29/30**؛
- duplication در treatment: **42**؛
- deletion در treatment: **55**؛
- بیشترین خطای مطلق energy balance: **`4.36e-08`**، کمتر از tolerance پذیرفته‌شدهٔ `1e-07`.

## نتیجهٔ اصلی Evolvability

گیت مهم heredity پاس شد:

- تولدهای variable-length در treatment: **61**؛
- organismهای variable-length که خودشان بعداً reproduction انجام دادند: **12**؛
- runهای treatment که در پایان دست‌کم یک organism فعال با طول متفاوت داشتند: **14/30**؛
- structural event در control: **0**.

بنابراین structural mutation فقط daughterهای گذرا و خراب تولید نکرد. تعدادی از variantهای طولی متولد شدند، به‌اندازهٔ کافی executable و زنده ماندند که خودشان تولیدمثل کنند، و این اتفاق تحت همان محدودیت‌های معمول energy/memory رخ داد.

پس Phase 5 شواهد مستقیم برای **heritable variable genome length** و مکانیزم structural evolvability موردنظر فراهم کرده است.

## نتایج طول genome

طول ancestor برابر `14` instruction است.

در پایان runهای control:

- minimum فعال: `14`؛
- maximum فعال: `14`؛
- تعداد طول‌های فعال متمایز همیشه `1`؛
- variance طول فعال: `0`.

در treatment:

- active minimum تا `13` رسید؛
- active maximum تا `15` رسید؛
- در یک run حداکثر `3` طول فعال متمایز دیده شد؛
- میانگین تعداد طول‌های فعال متمایز `1.5667` در برابر `1.0` control بود؛
- میانگین خودِ طول genome تقریباً ثابت ماند: `13.9981` در برابر `14.0`.

paired interval تقریبی ۹۵٪ برای این measurementها صفر را کنار گذاشت:

- `distinct_genome_lengths`: delta `+0.5667`، interval `[0.3237, 0.8096]`؛
- `genome_length_maximum`: delta `+0.3000`، interval `[0.1332, 0.4668]`؛
- `genome_length_minimum`: delta `-0.2667`، interval `[-0.4276, -0.1057]`؛
- `genome_length_variance`: delta `+0.01629`، interval `[0.00790, 0.02468]`؛
- `variable_length_births`: delta `+2.0333` در هر run، interval `[1.4504, 2.6163]`؛
- `variable_length_reproducing_offspring`: delta `+0.4000`، interval `[0.1088, 0.6912]`؛
- `variable_length_active_population`: delta `+0.9000`، interval `[0.4363, 1.3637]`.

نکتهٔ مهم این است که میانگین طول genome افزایش جهت‌دار پیدا نکرد. یعنی intervention یک dimension وراثتی جدید برای طول باز کرد، نه اینکه سیستم را مجبور به رشد genome کند.

## هزینه‌ها و outcomeهای ثانویه

`replication_copy_operations` تنها cost endpoint ثبت‌شده‌ای بود که paired interval آن صفر را کنار گذاشت:

- control mean: `1431.33`؛
- treatment mean: `1451.63`؛
- delta: `+20.30`؛
- interval تقریبی ۹۵٪: `[8.91, 31.69]`.

این با این واقعیت سازگار است که structural variants workload واقعی copying را تغییر می‌دهند؛ این «مزیت» نیست.

چند outcome ثانویهٔ diversity/turnover نیز در treatment بیشتر بودند:

- active genotype: `1.8667 -> 2.5333`؛
- active lineage: `1.8 -> 2.4`؛
- historical genotype: `6.5 -> 8.3333`؛
- births: `46.8 -> 47.9333`؛
- deaths: `4.8 -> 5.9333`؛
- faults: `3.9667 -> 5.0`.

`active_population` نهایی در هر دو condition برابر `54` بود، چون جهان تنظیم‌شده در این مقیاس به محدودیت memory رسید. این outcomeهای ثانویه evidence برای fitness advantage یا complexity بیشتر نیستند.

## Phase 5 دقیقاً چه چیزی را ثابت می‌کند؟

در محدودهٔ مدل و campaign فعلی:

1. self-replication دیگر طول genome را hard-code نمی‌کند و replication loop به absolute address وابسته نیست؛
2. duplication و deletion کور روی یک random stream مستقل و deterministic انجام می‌شوند؛
3. genome کوتاه‌تر و بلندتر reproducibly ایجاد می‌شود؛
4. طول variable از طریق reproduction به نسل بعد منتقل می‌شود؛
5. بعضی organismهای variable-length خودشان قادر به reproduction هستند؛
6. structural diversity تحت هزینه‌های واقعی memory/copy/execution شکل می‌گیرد؛
7. evidence کامل، matched-seed، versioned و reproducible آرشیو شده است.

## چه چیزی را ثابت نمی‌کند؟

Phase 5 هنوز evidence برای این موارد نیست:

- افزایش functional complexity؛
- بهتر بودن genome بلندتر؛
- adaptation؛
- fitness advantage؛
- intelligence؛
- open-ended innovation؛
- open-ended evolution؛
- multicellularity؛
- cooperation، predation یا communication.

اصل مهم:

> **Variable genome length ≠ increasing complexity.**

هر ادعای آینده دربارهٔ complexity باید measurement مستقل functional/algorithmic/behavioral داشته باشد که genome size را به‌صورت ساختاری reward نکند.

## آرشیو evidence

Calibration:

`results/phase-five/structural-event-rate-calibration/`

Full evidence:

`results/phase-five/variable-genome-full/`

Full archive شامل این فایل‌هاست:

- `campaign.json`
- `runs.csv`
- `summary.json`
- `comparison.csv`
- `validation.json`
- `provenance.json`
- `paired-analysis.json`
- `campaign-verification.json`
- `merge-readiness.json`
- `SHA256SUMS.txt`

Workflow همچنین یک GitHub Actions artifact مستقل برای evidence تولید کرد.

## تصمیم نهایی

Merge-readiness پاس شد، چون:

- همهٔ ۶۰ run کامل شدند؛
- validation و deterministic replay پاس شدند؛
- energy accounting در tolerance باقی ماند؛
- control هیچ structural event نداشت؛
- treatment هم duplication و هم deletion واقعی داشت؛
- variable-length birth رخ داد؛
- و organismهای variable-length خودشان reproduction انجام دادند.

**بنابراین Phase 5 برای پرسش ثبت‌شدهٔ genome evolvability از نظر علمی کامل است.**
