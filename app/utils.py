import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TELEGRAM_TOKEN or not CHAT_ID:
    raise ValueError("TELEGRAM_TOKEN and CHAT_ID must be set!")

# Send a message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

# Check for tickets
def check_tickets():
    urls = {
        "30.12.2024": [
            "https://bilet.railways.kz/sale/default/route/search?route_search_form%5BdepartureStation%5D=2700000&route_search_form%5BarrivalStation%5D=2700770&route_search_form%5BforwardDepartureDate%5D=30-12-2024",
        ],
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    for date, url_list in urls.items():
        for url in url_list:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                if "No tickets" not in soup.text:
                    message = f"🎟️ Tickets found for {date}! Check: {url}"
                    send_telegram_message(message)
            except Exception as e:
                print(f"Error checking {url}: {e}")
