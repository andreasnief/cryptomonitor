import feedparser
import requests
from datetime import datetime
import json
import os

# Telegram Einstellungen
TELEGRAM_ENABLED = True
TELEGRAM_BOT_TOKEN = "8358391123:AAGJdjcg4vmLQeiylz81KqdqULXYpkXHSmo"      # Platzhalter
TELEGRAM_CHAT_ID = "8285970985"         # Platzhalter

# RSS-Feeds
RSS_FEEDS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://www.newsbtc.com/feed/"
]

# Verzeichnisse
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
SEEN_FILE = os.path.join(BASE_DIR, "seen.json")

log_file = os.path.join(LOG_DIR, f"crypto_monitor_{datetime.now().strftime('%Y-%m-%d')}.log")

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

# Vorherige Einträge laden
if os.path.exists(SEEN_FILE):
    with open(SEEN_FILE, "r", encoding="utf-8") as f:
        seen = set(json.load(f))
else:
    seen = set()

new_items = []

# RSS Feeds auslesen
for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        if entry.id not in seen:
            seen.add(entry.id)
            new_items.append(entry)

# Neue Einträge verarbeiten
for item in new_items:
    message = f"{item.title}\n{item.link}"
    log(f"Neuer Eintrag: {item.title}")

    if TELEGRAM_ENABLED:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
            requests.post(url, data=data)
            log("Telegram gesendet")
        except Exception as e:
            log(f"Telegram Fehler: {e}")

# Gespeicherte Einträge aktualisieren
with open(SEEN_FILE, "w", encoding="utf-8") as f:
    json.dump(list(seen), f, ensure_ascii=False)
