# 403 Bypass Defender 🛡️

**Lightweight Flask-based protection against 403 Forbidden bypass techniques**  
أداة بسيطة وقوية مكتوبة بـ Python + Flask لحماية الـ endpoints المحمية بـ 403 من معظم طرق التجاوز الشائعة (path traversal، header spoofing، method switching، encoding tricks، إلخ).

مصممة خصيصًا للدفاع ضد أدوات آلية و AI-powered 403 bypass testers.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.x+-orange?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/github/license/YourUsername/403-bypass-defender?style=for-the-badge" alt="License: MIT">
  <img src="https://img.shields.io/badge/Status-Prototype-yellow?style=for-the-badge" alt="Status">
</p>

## ✨ المميزات الرئيسية

- كشف ومنع **path manipulation** (../ // %2e %252e %2f double encoding)
- حجب **headers spoofing** الشائعة (X-Forwarded-*, X-Original-URL, Client-IP, Forwarded, ...)
- تقييد **HTTP methods** (GET/POST/HEAD/OPTIONS فقط + رد 200 وهمي لبعض الهجمات)
- تسجيل كل المحاولات المشبوهة (IP + Method + Path + Host + Reason) في ملف log
- عرض اللوج بسهولة عبر endpoint `/logs` (JSON – آخر 50 محاولة)
- تشغيل آمن افتراضيًا على localhost

## ⚠️ تحذيرات هامة جدًا

- **للأغراض التعليمية والاختبار المحلي فقط**
- **ليس** بديلاً عن WAF حقيقي (Cloudflare, ModSecurity, AWS WAF, Fastly, ...)
- **لا** تستخدمها في production بدون طبقات حماية إضافية (HTTPS + Auth + Rate Limiting)
- قد لا تقاوم هجمات متقدمة جدًا أو مخصصة

## 🚀 التثبيت والتشغيل (سريع)

1. **المتطلبات**
   ```bash
   pip install flask
   python app.py
   تشغيل ملف
   الوصول الافتراضي
الصفحة المحمية: http://127.0.0.1:5000/protected/admin
عرض اللوج: http://127.0.0.1:5000/logs


اختبار سريع (جرب دي عشان تتأكد إن الأداة شغالة)# Path traversal
curl "http://127.0.0.1:5000/protected/admin/../secret"

# Header spoofing
curl -H "X-Forwarded-For: 127.0.0.1" "http://127.0.0.1:5000/protected/admin"

# Method abuse
curl -X PUT "http://127.0.0.1:5000/protected/admin"

# Encoding tricks
curl "http://127.0.0.1:5000/protected/admin/%252e%252e/%252e%252e/etc/passwd"

→ شوف اللوج في 403_bypass_attempts.log أو عبر /
📂 
# أو python 403.py حسب اسم الملف عندك
📂 هيكل المشروع403-bypass-defender/
├── app.py                      # السكريبت الرئيسي (أو 403.py)
├── 403_bypass_attempts.log     # يتولد تلقائيًا
├── README.md
├── LICENSE
└── requirements.txt
🛠️ التخصيص السريع

غيّر ALLOWED_HOSTS لدومينك الحقيقي
أضف/احذف methods في ALLOWED_METHODS
زد عمق فك الـ encoding في is_path_suspicious()
أضف rate limiting أو IP blocking لو عايز (سهل بـ flask-limiter أو dictionary)
George Boutros – Security Analyst & Python Developer
