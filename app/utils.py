import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TELEGRAM_TOKEN or not CHAT_ID:
    raise ValueError("TELEGRAM_TOKEN and CHAT_ID must be set!")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload)
        print(f"Telegram API response: {response.status_code}, {response.text}")
        
        # Add detailed error logging
        if response.status_code != 200:
            error_msg = f"❌ Telegram error {response.status_code}: {response.text}"
            print(error_msg)
        else:
            print("✅ Message sent to Telegram successfully")
            
    except Exception as e:
        print(f"🔥 Failed to send Telegram message: {str(e)}")

# Check for tickets
def check_tickets():
    urls = {
        "04.07.2025": [
            "https://bilet.railways.kz/sale/default/route/search?route_search_form%5BdepartureStation%5D=2700770&route_search_form%5BarrivalStation%5D=2708001&route_search_form%5BforwardDepartureDate%5D=04-07-2025",
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
