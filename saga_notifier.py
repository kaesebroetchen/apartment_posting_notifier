
import requests
from bs4 import BeautifulSoup
import hashlib
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SAGA_URL = "https://www.saga.hamburg/immobiliensuche?Kategorie=APARTMENT"
STORAGE_FILE = "last_seen_saga.txt"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))


def get_saga_content():
    res = requests.get(SAGA_URL)
    soup = BeautifulSoup(res.text, "html.parser")
    cards = soup.find_all("div", class_="result-card")
    listings = []
    for card in cards:
        title = card.find("h2")
        info = card.find_all("p")
        link_tag = card.find("a", href=True)
        block = f"{title.get_text(strip=True) if title else 'No title'}\n"
        block += "\n".join(p.get_text(strip=True) for p in info)
        if link_tag:
            block += f"\nLink: https://www.saga.hamburg{link_tag['href']}"
        listings.append(block)
    return "\n\n".join(listings)


def get_hash_and_text():
    content = get_saga_content()
    hash_val = hashlib.md5(content.encode()).hexdigest()
    return hash_val, content


def load_last():
    if not os.path.exists(STORAGE_FILE):
        return None, ""
    with open(STORAGE_FILE, 'r') as f:
        lines = f.readlines()
        return lines[0].strip(), "".join(lines[1:])


def save(hash_val, content):
    with open(STORAGE_FILE, 'w') as f:
        f.write(hash_val + "\n" + content)


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    requests.post(url, data=data)


def send_email(subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)


def main():
    current_hash, current_text = get_hash_and_text()
    last_hash, last_text = load_last()

    if current_hash != last_hash:
        send_telegram("🏘️ Neue SAGA Wohnungsangebote entdeckt!")
        send_email("SAGA Hamburg Update", current_text)
        save(current_hash, current_text)
    else:
        print("✅ No updates from SAGA")


if __name__ == "__main__":
    main()
