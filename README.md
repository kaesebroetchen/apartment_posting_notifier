Apartment Listing Notifier

This is a Python bot that monitors a webpage of a real estate company [DHU Hamburg's apartment listings](https://dhu.hamburg/wohnen/wohnungsangebote/) and notifies you via **Telegram** and **Email** when a new listing is published.

## 🔔 Features

- Scrapes the DHU listings page
- Detects new postings using file hashes
- Sends notifications:
  - 📬 Email alerts
  - 💬 Telegram messages
- Automatically runs every 15 minutes (via Render.com)
