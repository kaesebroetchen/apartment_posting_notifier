
# 🏘️ Apartment Monitoring Bots

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 🔍 Overview

This project monitors apartment listings from:

- 🏠 [DHU Hamburg](https://dhu.hamburg/wohnen/wohnungsangebote/)
- 🏢 [SAGA Hamburg](https://www.saga.hamburg/immobiliensuche?Kategorie=APARTMENT)

and sends **Telegram** + **Email** notifications when changes are detected.

---

## 🧠 What's Inside

| Script            | Description                      | Frequency | Deployment |
|-------------------|----------------------------------|-----------|-------------|
| `dhu_notifier.py` | Monitors DHU listings            | Every 15 min | Render Cron |
| `saga_notifier.py`| Monitors SAGA listings           | Every 15 min | Render Cron |

Environment variables are managed through `.env` or set directly in Render.

---

## ✉️ Notifications

When a new listing appears:

- You'll get a **Telegram alert**.
- You'll receive a **formatted email** with full listing details.

---

## ⚙️ Deployment (Render)

1. Fork or clone this repository.
2. Click the button below:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

3. Render will detect the `render.yaml` and set up:
   - One job for `dhu_notifier.py`
   - One job for `saga_notifier.py`

---

## 🔐 Environment Variables Required

These must be set in Render or your local `.env` file:

```
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
EMAIL_SENDER=
EMAIL_PASSWORD=
EMAIL_RECEIVER=
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

---

## 📁 Project Structure

```
.
├── dhu_notifier.py
├── saga_notifier.py
├── render.yaml
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🪪 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
