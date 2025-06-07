import requests
import threading
from flask import Flask, request
import time

app = Flask(__name__)

BOT_TOKEN = '7665383679:AAGa263syK8FdyOiSXHLsUtKEKzFajbZJlM'
CHAT_ID = '1589414763'
API_KEY = '4IiAdjuN2O9An7o90e4G3ePANmVqQrc7'

last_rate = None  # שמירת השער האחרון

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': text})

@app.route('/')
def home():
    return 'Bot is running!'

@app.route('/check', methods=['GET'])
def check_eur_usd():
    global last_rate
    try:
        response = requests.get(
            f"http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}&base=EUR&symbols=USD"
        )
        data = response.json()

        rate = float(data['rates']['USD'])
        send_telegram_message(f"שער EUR/USD: {rate}")

        # בדיקת תנועה חדה
        if last_rate is not None and abs(rate - last_rate) >= 0.005:
            change = rate - last_rate
            direction = "⬆️ עלייה חדה" if change > 0 else "⬇️ ירידה חדה"
            send_telegram_message(f"🚨 {direction} בזיהוי! שינוי של {change:.5f} בשער EUR/USD")

        last_rate = rate
        return 'Message sent!'

    except Exception as e:
        send_telegram_message(f"שגיאה בבדיקת שערים: {e}")
        return 'Error'

def heartbeat():
    while True:
        send_telegram_message("✅ הבוט פעיל ובודק שערים...")
        time.sleep(1800)  # כל חצי שעה

# התחלת ה-heartbeat
threading.Thread(target=heartbeat, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
