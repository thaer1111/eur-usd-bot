import requests
from flask import Flask, request
import threading
import time

app = Flask(__name__)

BOT_TOKEN = '7665383679:AAGa263syK8FdyOiSXHLsUtKEKzFajbZJlM'
CHAT_ID = 7665383679:AAGa263syK8FdyOiSXHLsUtKEKzFajbZJlM

# שליחת הודעה לטלגרם
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': text})

# דף בדיקה
@app.route('/')
def home():
    return 'Bot is running!'

# בדיקה ידנית אם השער זז
@app.route('/check', methods=['GET'])
def check_eur_usd():
    response = requests.get('https://api.exchangerate.host/latest?base=EUR&symbols=USD')
    data = response.json()
    rate = data['rates']['USD']
    send_telegram_message(f"EUR/USD: {rate}")
    return f"EUR/USD: {rate}"

# שליחת heartbeat כל שעה
def heartbeat():
    while True:
        try:
            send_telegram_message("✅ הבוט עלה ועובד!")
            time.sleep(3600)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(3600)

# התחלת הבוט
if __name__ == '__main__':
    threading.Thread(target=heartbeat, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
