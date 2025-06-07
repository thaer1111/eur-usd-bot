import requests
import threading
from flask import Flask, request
import time

app = Flask(__name__)

# החלף בטוקן ובמספר שלך
BOT_TOKEN = '7665383679:AAGa263syK8FdyOiSXHLsUtKEKzFajbZJlM'
CHAT_ID = 'הכנס_כאן_את_מספר_הצ׳אט_שלך'

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': text})

@app.route('/')
def home():
    return 'Bot is running!'

@app.route('/check', methods=['GET'])
def check_eur_usd():
    response = requests.get('https://api.exchangerate.host/latest?base=EUR&symbols=USD')
    if response.status_code == 200:
        data = response.json()
        rate = data['rates']['USD']
        send_telegram_message(f"💱 שער EUR/USD: {rate}")
        return f"EUR/USD rate: {rate}"
    else:
        return "Failed to fetch exchange rate", 500

def heartbeat():
    while True:
        send_telegram_message("✅ הבוט עדיין חי ועובד!")
        time.sleep(3600)  # כל שעה

# הפעלת heartbeat כ-thread נפרד
threading.Thread(target=heartbeat, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
