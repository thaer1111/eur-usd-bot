import requests
import threading
from flask import Flask, request
import time

app = Flask(__name__)

BOT_TOKEN = '7665383679:AAGa263syK8FdyOiSXHLsUtKEKzFajbZJlM'
CHAT_ID = '1589414763'  # ID שלך

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

@app.route('/')
def home():
    return '✅ Bot is running!'

@app.route('/check', methods=['GET'])
def check_eur_usd():
    try:
        response = requests.get("https://api.exchangerate.host/latest?base=EUR&symbols=USD")
        data = response.json()
        rate = data['rates']['USD']
        send_telegram_message(f"שער EUR/USD הנוכחי: {rate}")
        return 'Message sent!'
    except Exception as e:
        send_telegram_message(f"שגיאה בבדיקה: {e}")
        return str(e)

def heartbeat():
    while True:
        send_telegram_message("✅ הבוט פעיל ובודק שערים...")
        time.sleep(3600)  # כל שעה

if __name__ == '__main__':
    threading.Thread(target=heartbeat, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
