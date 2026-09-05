# Desktop Lab Architecture

## تصمیم

Melakat فعلاً یک Desktop Research Lab مستقل است. Esbiko مسیر آینده‌ی انتشار و مشاهده‌ی عمومی خواهد بود، اما جزو هسته‌ی فعلی نیست.

## لایه‌ها

### 1. Domain and engine

مسئول قوانین جهان، VM، organism، resource accounting، mutation، reproduction و measurement است. این لایه نباید هیچ import از PySide6 داشته باشد.

### 2. Process boundary

موتور در process جدا اجرا می‌شود. رابط کاربری فقط command می‌فرستد و event قابل‌سریال‌سازی دریافت می‌کند.

Commandهای پایه:

- start
- pause
- resume
- step
- reset
- stop
- save_snapshot

Eventهای پایه:

- ready
- status
- tick
- organism_born
- organism_died
- finished
- stopped
- error

### 3. Parameter schema

هر پارامتر با ParameterSpec تعریف می‌شود:

- path
- label
- group
- type
- default
- range
- step
- description
- advanced flag

رابط کاربری form را از schema می‌سازد. بنابراین افزودن پارامتر جدید به معنی افزودن یک record است، نه ساختن widget و layout جدید در چند فایل.

برای رشد از ۵۰ به ۲۰۰ پارامتر:

- گروه‌بندی اجباری است؛
- search لازم است؛
- پارامترهای advanced از ابتدا پشتیبانی می‌شوند؛
- validation مرکزی است؛
- configuration باید قابل ذخیره و versioned باشد؛
- پارامترها نباید با global variable مدیریت شوند.

### 4. Presentation

رابط شامل پنل parameter، world view، metrics، inspector و event log است. هیچ‌کدام نباید قانون علمی را خودشان محاسبه کنند.

### 5. Persistence

در نسخه‌ی اول، snapshot و result به‌صورت فایل محلی ذخیره می‌شوند. بعداً می‌توان export به JSON، CSV، Parquet یا اتصال به Esbiko را اضافه کرد.

## اصل توسعه

افزودن feature باید معمولاً یکی از این تغییرها باشد:

- افزودن ParameterSpec؛
- افزودن command یا event؛
- افزودن rule module به engine؛
- افزودن panel مستقل؛
- افزودن metric یا exporter.

افزودن feature نباید نیازمند بازنویسی MainWindow باشد.

## قرارداد علمی

DemoEngine فعلی فقط برای اعتبارسنجی مسیر UI، process، command، event و metrics است. این موتور نتیجه‌ی علمی Melakat محسوب نمی‌شود. پس از تثبیت رابط، با VM و قوانین Experiment 0 جایگزین خواهد شد.

## مسیر آینده

1. تثبیت desktop shell و parameter schema.
2. افزودن VM مستقل بدون GUI dependency.
3. اتصال VM به process protocol.
4. افزودن genome، register و memory inspector.
5. افزودن snapshot و deterministic replay.
6. اجرای چند seed و مقایسه‌ی runs.
7. ساخت package قابل‌نصب Windows.
8. اتصال اختیاری Esbiko به resultها.
