import requests
import threading
from flask import Flask, request
import time

app = Flask(__name__)

BOT_TOKEN = '7665383679:AAGa263syK8FdyOiSXHLsUtKEKzFajbZJlM'
CHAT_ID = '1589414763'
API_KEY = '4IiAdjuN2O9An7o90e4G3ePANmVqQrc7'

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

@app.route('/')
def home():
    return 'Bot is running!'

@app.route('/check', methods=['GET'])
def check_eur_usd():
    try:
        response = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}&symbols=USD,EUR')
        data = response.json()
        if 'rates' not in data:
            send_telegram_message(f"שגיאה בבדיקת שערים: {data}")
            return 'שגיאה בבדיקה: rates'
        rate = data['rates']['USD']
        send_telegram_message(f"שער EUR/USD: {rate}")
        return 'Message sent!'
    except Exception as e:
        send_telegram_message(f"שגיאה בבדיקה: {e}")
        return str(e)

def heartbeat():
    while True:
        send_telegram_message("✅ הבוט פעיל ובודק שערים...")
        time.sleep(300)

if __name__ == '__main__':
    threading.Thread(target=heartbeat, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
