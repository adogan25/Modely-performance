import requests
from bs4 import BeautifulSoup
import time
import telegram
import os

TESLA_URL = 'https://www.tesla.com/tr_TR/inventory/new/my?arrangeby=plh&zip=34025&range=0'
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

TERIMLER = [
    "model y all-wheel drive",
    "long range all-wheel drive performance",
    "long range d",
    "long range rear-wheel drive",
    "long range arkadan",
    "long range all-wheel drive",
    "long range arkadan çekiş",
    "performance dört çeker",
    "performance d"
]

def send_telegram_message(message):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def check_for_keywords():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(TESLA_URL, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Tüm <div class="tds-text_color--10"> öğelerini ara
            all_divs = soup.find_all('div', class_='tds-text_color--10')
            for div in all_divs:
                text = div.get_text(strip=True).lower()
                for keyword in TERIMLER:
                    if keyword.lower() in text:
                        print(f"✓ Bulundu: {keyword}")
                        send_telegram_message(f"🚗 Stokta bulundu: {keyword}")
                        return True
    except Exception as e:
        print(f"Hata oluştu: {e}")
    return False

def background_worker():
    while True:
        print("Stok kontrol ediliyor...")
        check_for_keywords()
        time.sleep(10)

background_worker()
if __name__ == '__main__':
    threading.Thread(target=background_worker).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
