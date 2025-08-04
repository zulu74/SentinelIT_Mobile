# SentinelIT_Mobile
"AI-powered Android cybersecurity app
# 🛡️ SentinelIT Mobile Pro

**Powered AI. Hardened Systems. Zero Compromise.**

SentinelIT Mobile is a professional-grade cybersecurity app and threat detection engine built for Android devices using Python, Kivy, and Plyer. It provides real-time protection, threat scanning, SIEM intelligence integration, and intuitive UI for quick actions and activity review.

---

## 🔐 Features
- ✅ Real-time threat protection
- ⚠️ SIEM-based quick and full scans
- 📊 Visual dashboard with activity logs
- 📡 OTA updates indicator
- 📁 Secure Android permissions (device admin config & Java intercept)
- 📱 Optimized for Android deployment using Buildozer

---

## 📦 Files
- `main.py` – Main Kivy application logic
- `main.kv` – Kivy UI layout definitions
- `siemcore.py` – Threat analysis & fallback SIEM logic
- `buildozer.spec` – Build settings for APK generation
- `device_admin_config.xml` – Android device policy permissions
- `ussdinterceptorservice.java` – Java-level hooks for advanced detection
- `assets/` – Static resources (if any)

---

## 🚀 Build Instructions

1. **Install Buildozer**:
   ```bash
   pip install buildozer
