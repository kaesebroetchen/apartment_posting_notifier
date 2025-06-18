
import requests
from bs4 import BeautifulSoup
import hashlib
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import difflib

load_dotenv()

CHECK_URL = "https://dhu.hamburg/wohnen/wohnungsangebote/"
STORAGE_FILE = "last_seen.txt"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))


def get_page_hash_and_text():
    response = requests.get(CHECK_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Target main content area, fallback to full text
    listings_section = soup.find("main")
    if listings_section:
        content_string = listings_section.get_text(separator="\n", strip=True)
    else:
        content_string = soup.get_text()

    content_hash = hashlib.md5(content_string.encode()).hexdigest()
    return content_hash, content_string


def load_last_hash_and_text():
    if not os.path.exists(STORAGE_FILE):
        return None, ""
    with open(STORAGE_FILE, 'r') as f:
        lines = f.readlines()
        return lines[0].strip(), ''.join(lines[1:])


def save_new_hash_and_text(hash_value, content):
    with open(STORAGE_FILE, 'w') as f:
        f.write(hash_value + "\n")
        f.write(content)


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

        recipients = [email.strip() for email in EMAIL_RECEIVER.split(",")]
        msg["To"] = ", ".join(recipients)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Email error:", str(e))


def compare_changes(old_text, new_text):
    diff = difflib.unified_diff(
        old_text.splitlines(), new_text.splitlines(),
        lineterm="", n=5
    )
    return "\n".join(diff)


def notify_user(changes):
    message = f"🏠 <b>New or updated apartment listings detected!</b>\n\n<pre>{changes}</pre>"
    print("🔔 Change detected! Notifying user...")
    send_telegram_message(message)
    send_email("New DHU Apartment Listings 🏢", changes)


def main():
    current_hash, current_text = get_page_hash_and_text()
    last_hash, last_text = load_last_hash_and_text()

    if current_hash != last_hash:
        changes = compare_changes(last_text, current_text)
        notify_user(changes)
        save_new_hash_and_text(current_hash, current_text)
    else:
        print("✅ No new updates.")


if __name__ == "__main__":
    main()
