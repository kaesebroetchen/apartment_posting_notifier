import requests
from bs4 import BeautifulSoup
import hashlib
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# URL and storage
CHECK_URL = "https://dhu.hamburg/wohnen/wohnungsangebote/"
STORAGE_FILE = "last_seen.txt"

# Load credentials
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))


def get_page_hash():
    response = requests.get(CHECK_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_links = [a['href'] for a in soup.find_all('a', href=True) if ".pdf" in a['href']]
    pdf_links = sorted(set(pdf_links))
    content_string = ''.join(pdf_links)
    return hashlib.md5(content_string.encode()).hexdigest(), pdf_links


def load_last_hash():
    if not os.path.exists(STORAGE_FILE):
        return None
    with open(STORAGE_FILE, 'r') as f:
        return f.read().strip()


def save_new_hash(hash_value):
    with open(STORAGE_FILE, 'w') as f:
        f.write(hash_value)


def send_telegram_message(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        }
        requests.post(url, data=payload)
        print("✅ Telegram notification sent.")
    except Exception as e:
        print("❌ Telegram error:", str(e))


def send_email(subject, body):
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Email error:", str(e))


def notify_user(new_links):
    message = "🏠 <b>New DHU apartment listings posted!</b>\n\n" + "\n".join(new_links)
    print("🔔 Change detected! Notifying user...")
    send_telegram_message(message)
    send_email("New DHU Apartment Listings 🏢", message)


def main():
    current_hash, current_links = get_page_hash()
    last_hash = load_last_hash()

    if current_hash != last_hash:
        notify_user(current_links)
        save_new_hash(current_hash)
    else:
        print("✅ No new updates.")


if __name__ == "__main__":
    main()