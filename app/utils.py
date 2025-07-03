import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Configuration loader (prevents early loading issues)
def get_telegram_config():
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    if not token or not chat_id:
        raise ValueError("TELEGRAM_TOKEN and CHAT_ID must be set!")
    return token, chat_id

def send_telegram_message(message):
    try:
        token, chat_id = get_telegram_config()
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        response = requests.post(url, json=payload, timeout=10)
        
        # Enhanced logging
        if response.status_code == 200:
            print("✅ Telegram message sent successfully")
            return True
        else:
            error = f"❌ Telegram error {response.status_code}: {response.text}"
            print(error)
            return False
    except Exception as e:
        print(f"🔥 Telegram send failed: {str(e)}")
        return False

def check_tickets():
    urls = {
        "04.07.2025": [
            "https://bilet.railways.kz/sale/default/route/search?route_search_form%5BdepartureStation%5D=2700770&route_search_form%5BarrivalStation%5D=2708001&route_search_form%5BforwardDepartureDate%5D=04-07-2025",
        ],
    }
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    for date, url_list in urls.items():
        for url in url_list:
            try:
                response = requests.get(url, headers=headers, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # More reliable ticket detection:
                no_tickets_div = soup.find('div', class_='no-train')
                if no_tickets_div:
                    print(f"No tickets for {date}")
                else:
                    message = f"🎟️ TICKETS AVAILABLE for {date}!\n{url}"
                    send_telegram_message(message)
            except Exception as e:
                error_msg = f"Error checking {url}: {str(e)[:100]}"
                print(error_msg)
                send_telegram_message(f"⚠️ TICKET CHECK ERROR: {error_msg}")