import os
import time
import threading
import requests
from flask import Flask
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.error import TelegramError

# Flask uygulaması başlatma
app = Flask(__name__)

# Telegram bot bilgilerinizi burada ayarlayın
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'
bot = Bot(token=TELEGRAM_TOKEN)

# Stok kontrolü yapan fonksiyon
def check_stock():
    url = "YOUR_PRODUCT_URL"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    while True:
        try:
            # Sayfayı al
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Sayfa içeriğinde fotoğraf var mı kontrol et
                image_element = soup.find('img')  # Burada img etiketini kontrol ediyoruz
                if image_element:
                    message = "Stokta araç var!"
                    bot.send_message(chat_id=CHAT_ID, text=message)
                    print("Stokta araç var, Telegram'a bildirim gönderildi.")
                else:
                    print("Stokta araç yok.")
            else:
                print("Sayfaya erişim sağlanamadı, tekrar deneniyor...")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")
        
        # 10 saniyede bir kontrol et
        time.sleep(10)

# Flask başlatma ve kontrol fonksiyonunu thread ile çalıştırma
if __name__ == '__main__':
    # Telegram kontrolünü ayrı bir thread'de çalıştırma
    threading.Thread(target=check_stock, daemon=True).start()

    # Flask uygulamasını başlatma
    port = int(os.environ.get('PORT', 8080))  # Render veya başka bir platform için port ayarları
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
