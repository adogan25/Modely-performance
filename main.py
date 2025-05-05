import requests
from bs4 import BeautifulSoup
import threading
import time
from flask import Flask
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TESLA_URL = 'https://www.tesla.com/tr_TR/inventory/new/my?arrangeby=plh&zip=34025&range=0'

def check_for_performance_awd():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(TESLA_URL, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().lower()
            if "performance dual motor" in text or \
               "long range" in text or \
               "Performance D" in text or \
               "Long Range All-Wheel Drive Performance" in text or \
               "Long Range D" in text or \
               "Long Range Rear-Wheel Drive" in text or \
               "Long Range All-Wheel Drive" in text or \
               "Performance D" in text or \
               "Model Y All-Wheel Drive" in text or \
               "performance dual motor" in text:
                return True
    except Exception as e:
        print(f"Hata oluştu: {e}")
    return False

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram bildirimi gönderilemedi: {e}")

def background_worker():
    print("Tesla 'Performance Dört Çeker' kontrolü başlatıldı...")
    while True:
        print("Kontrol ediliyor...")
        if check_for_performance_awd():
            send_telegram_message("🚗 Tesla Model Y 'Performance Dört Çeker' stokta! Kontrol et: " + TESLA_URL)
        time.sleep(10)

@app.route('/')
def index():
    return "Tesla Performance AWD checker is running."

if __name__ == '__main__':
    threading.Thread(target=background_worker).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
