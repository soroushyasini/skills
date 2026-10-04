<div dir="rtl" align="right" markdown="1">

# اسکیل‌های شخصی سروش یاسینی

این مخزن مجموعهٔ اسکیل‌های شخصی من برای کارهای سازمانی، توسعهٔ سامانه، تحلیل فرایند و نگارش فارسی است. هر اسکیل یک پوشهٔ مستقل دارد و فایل `SKILL.md` نقطهٔ ورود آن است.

## اسکیل‌های موجود

| اسکیل | کاربرد | فایل اصلی |
|---|---|---|
| `classify-kanboard-work` | طبقه‌بندی فعالیت‌های کاری، تشخیص مسیر تخصصی و آماده‌سازی کارت فارسی Kanboard | [مشاهدهٔ اسکیل](skills/classify-kanboard-work/SKILL.md) |
| `persian-meeting-minutes` | تبدیل یادداشت‌های جلسه به صورت‌جلسهٔ فارسی با حفظ تصمیم‌ها و جزئیات منبع | [مشاهدهٔ اسکیل](skills/persian-meeting-minutes/SKILL.md) |

## ساختار مخزن

</div>

```text
skills/
├── classify-kanboard-work/
│   ├── SKILL.md
│   └── references/
│       └── decision-audit.md
└── persian-meeting-minutes/
    ├── SKILL.md
    └── references/
        ├── output-formats.md
        └── examples.md

scripts/
└── validate_skills.py
tests/
└── test_validate_skills.py
.github/workflows/
└── validate-skills.yml
README.md
requirements-dev.txt
.gitignore
.gitattributes
```

<div dir="rtl" align="right" markdown="1">

پوشهٔ `references/` هر اسکیل فقط منابع همان اسکیل را نگه می‌دارد. در صورت نیاز واقعی، پوشه‌های `scripts/`، `assets/` یا `agents/` را داخل همان اسکیل اضافه کن؛ برای اسکیل‌های ساده ساختن پوشه‌های خالی لازم نیست.

`scripts/` در ریشه برای ابزارهای نگهداری کل مخزن است. اسکریپتی که فقط به یک اسکیل مربوط است باید داخل پوشهٔ همان اسکیل قرار بگیرد.

## استفاده

برای مطالعه، فایل اصلی اسکیل مورد نظر را باز کن. برای انتقال به ابزاری که پوشه‌های `SKILL.md` را می‌خواند، کل پوشهٔ همان اسکیل را کپی یا نصب کن تا ارجاع‌های نسبی به منابع نیز حفظ شوند. مسیر نصب را مطابق ابزار مورد استفاده انتخاب کن.

نام اسکیل همان مقدار `name` در ابتدای `SKILL.md` است. فایل‌های مرجع اسکیل مستقل نیستند و از طریق راهنمای اصلی خوانده می‌شوند.

## افزودن اسکیل جدید

۱. داخل `skills/` یک پوشه با نام کوتاه انگلیسی، حروف کوچک و خط تیره بساز.
۲. فایل `SKILL.md` را با نامی برابر نام پوشه ایجاد کن. `description` باید مشخص کند اسکیل چه کاری انجام می‌دهد و چه زمانی استفاده شود.
۳. دستورهای اصلی و قواعد تصمیم را در `SKILL.md` بنویس. جزئیات طولانی، قالب‌ها و مثال‌های وابسته به حالت اجرا را در `references/` قرار بده و زمان خواندن هر مرجع را مشخص کن.
۴. فقط منابعی را اضافه کن که واقعاً برای اجرای اسکیل لازم‌اند. لینک‌های فایل را نسبت به فایل ارجاع‌دهنده بنویس.
۵. ردیف اسکیل را به جدول بالا اضافه کن و بررسی محلی را اجرا کن.

نمونهٔ فراداده:

</div>

```yaml
---
name: example-skill
description: Explain the specific task and when this skill should be used.
metadata:
  version: "1.0.0"
  language: fa
---
```

<div dir="rtl" align="right" markdown="1">

فیلدهای `name` و `description` الزامی‌اند. اطلاعاتی مانند نسخه و زبان زیر `metadata` قرار می‌گیرند. نسخهٔ هر اسکیل فقط با تغییر خود آن اسکیل به‌روزرسانی می‌شود؛ برای مرتب‌سازی پوشه‌ها نسخهٔ تازه نساز.

## بررسی محلی و خودکار

Python 3.10 یا جدیدتر برای ابزار بررسی مخزن لازم است. این وابستگی برای نگهداری مخزن است؛ استفاده از دو اسکیل فعلی به اجرای Python نیاز ندارد.

</div>

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate_skills.py
python -m unittest discover -s tests -v
```

<div dir="rtl" align="right" markdown="1">

بررسی خودکار، وجود `SKILL.md`، فرادادهٔ YAML، تطابق نام پوشه و اسکیل و وجود مقصد لینک‌های نسبی فایل در Markdown را کنترل می‌کند. لینک‌های اینترنتی و محتوای نمونه‌های داخل بلوک کد از بررسی مسیر فایل کنار گذاشته می‌شوند. درستی معنایی دستورها و نتیجهٔ واقعی اسکیل همچنان به بازبینی و سناریوهای کاربردی نیاز دارد.

همین بررسی‌ها در [گردش‌کار GitHub Actions](.github/workflows/validate-skills.yml) روی push و pull request اجرا می‌شوند.

## مسیرهای جدید

فایل‌های قدیمی ریشه به این مسیرها منتقل شده‌اند؛ برای ارجاع‌های جدید از مسیرهای فعلی استفاده کن:

| مسیر قبلی | مسیر فعلی |
|---|---|
| `kanboard-task-classifier.md` | [skills/classify-kanboard-work/SKILL.md](skills/classify-kanboard-work/SKILL.md) |
| `persian-meeting-minutes.md` | [skills/persian-meeting-minutes/SKILL.md](skills/persian-meeting-minutes/SKILL.md) |
| `references/kanboard-task-classifier/decision-audit.md` | [مرجع داخل اسکیل Kanboard](skills/classify-kanboard-work/references/decision-audit.md) |

</div>
