# Melakat

## شبیه‌سازی یک جهان زیستی-دیجیتال محدود

Melakat یک پروژهٔ پژوهشی برای بررسی امکان شکل‌گیری فرایندهای شبیه به حیات و تکامل در یک جهان محاسباتی محدود است.

پروژه از برنامه‌های بسیار ساده شروع می‌شود؛ برنامه‌هایی که درون یک VM/sandbox اختصاصی زندگی می‌کنند، منابع محدود مصرف می‌کنند، تکثیر می‌شوند، تغییرات وراثتی پیدا می‌کنند، برای منابع مشترک رقابت می‌کنند و ممکن است بمیرند.

سؤال اصلی این نیست که چگونه یک AI یا نرم‌افزار پیچیده بسازیم. سؤال این است:

> اگر فقط قوانین ساده، منابع محدود، انرژی ورودی، تکثیر ناقص و مرگ را تعریف کنیم، چه الگوهایی خودبه‌خود پدیدار می‌شوند؟

## اصل مرکزی

ما زیست‌شناسی زمین را از نظر ظاهری کپی نمی‌کنیم. از نقش عملکردی پدیده‌های طبیعی برای طراحی حداقل قوانین دیجیتال استفاده می‌کنیم.

برای نمونه:

- Sun → جریان انرژی آزاد به جهان
- Metabolism → تبدیل منابع محیط به انرژی قابل‌مصرف
- DNA → اطلاعات اجراییِ وراثتی
- Cell boundary → مرز محاسباتی محافظت‌شده
- Time → گام‌های شبیه‌سازی
- Natural selection → تغییر فراوانی دودمان‌ها بر اثر تفاوت در بقا و تکثیر

هر analogy باید جداگانه بررسی و توجیه شود؛ هیچ تشبیهی فقط به‌دلیل شباهت ظاهری پذیرفته نمی‌شود.

## مبانی محیط دیجیتال

پیش از مطالعه‌ی organism، باید خودِ محیط محاسباتی را بشناسیم:

- bit، byte و نمایش عدد؛
- memory، address و state؛
- CPU، register، ALU و program counter؛
- program، process، compiler و interpreter؛
- fetch، decode و execute؛
- copy، clone، snapshot و replication؛
- محدودیت سخت‌افزار و محدودیت نرم‌افزار؛
- VM، scheduler، randomness و sandbox.

سند پایه:

- [Digital Environment Basics](docs/foundations/digital-environment-basics.md)

## محدودیت‌های الزام‌آور

- جهان باید یک VM/sandbox مصنوعی و غیرقابل‌خروج باشد.
- Python فقط شبیه‌ساز جهان است؛ genomeها نباید کد Python یا فرایندهای واقعی سیستم‌عامل باشند.
- organismها نباید به filesystem، network، subprocess، runtime پایتون یا API خارجی دسترسی داشته باشند.
- هدف‌گذاری برای AI، ML، هوش، یادگیری، RL، افزایش complexity یا ساخت برنامهٔ بزرگ‌تر ممنوع است.
- در نسخهٔ اولیه fitness function صریح، گونه‌گذاری دستی، انتخاب دستی، حمله، همکاری، انگل و جغرافیا وجود ندارد.
- آزمایش اولیه کوچک، همگن و مبتنی بر ورود متوالی انرژی است.
- mutation اولیه فقط از نوع substitution خواهد بود، مگر اینکه پژوهش و پروتکل بعدی خلاف آن را توجیه کند.
- قبل از تکمیل مشخصات علمی، کدنویسی شبیه‌ساز آغاز نمی‌شود.

## ترتیب کار

1. Phase 0A — Digital substrate and Digital–Natural Analogy Audit
2. Phase 0B — Genome representation and interpreter
3. Phase 0C — Virtual cell/body
4. Phase 0D — Signals, energy and reproduction
5. Phase 0E — Variation, competition and selection
6. Phase 0F — Experiment 0 Protocol
7. Phase 1 — Python prototype، فقط پس از اعتبارسنجی مراحل قبل

## حلقهٔ پژوهش

Research → Hypothesis → Minimal World Rule → Implementation → Validation → Multiple Runs → Measurement → Unexpected Result → Analysis → Next Hypothesis

نتیجهٔ مطلوب از قبل تعیین نشده است. حتی ساده‌ترشدن organismها، انقراض کامل، پایداری یک replicator کوچک یا شکست در پیدایش تکثیر، همگی نتایج معتبر آزمایش هستند.

## وضعیت فعلی

این repository در مرحلهٔ Research / Pre-Implementation قرار دارد.

اسناد اصلی:

- [Digital Environment Basics](docs/foundations/digital-environment-basics.md)
- [Digital Evolution World v0](docs/foundations/digital-evolution-world-v0.md)
- [Phase 0](docs/phase-0/README.md)
- [Research README](docs/research/README.md)
- [Research Report](docs/research/report-source.md)
- [Evidence Matrix](docs/research/evidence-matrix.md)

## ساختار repository

- docs/foundations/ — مبانی محیط دیجیتال و سند مادر پروژه
- docs/phase-0/ — مشخصات پیش از کدنویسی
- docs/research/ — منابع، مقایسهٔ پروژه‌ها و evidence matrix
- src/ — شبیه‌ساز آینده، پس از تأیید مشخصات
- tests/ — آزمون‌های تعیین‌کنندهٔ قوانین جهان

## English summary

Melakat is a research-first project exploring whether a constrained computational world can support open-ended digital evolution from minimal digital replicators.

The first world will be homogeneous, finite, energy-limited, and isolated inside a dedicated virtual machine. No machine learning, intelligence objective, explicit fitness function, or predefined complexity target will be introduced.
