import requests
import threading
from flask import Flask, request
import time

app = Flask(__name__)

BOT_TOKEN = '7665383679:AAGa263syK8FdyOiSXHLsUtKEKzFajbZJlM'
CHAT_ID = '1589414763'

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': text})

@app.route('/')
def home():
    return 'Bot is running!'

@app.route('/check', methods=['GET'])
def check_eur_usd():
    try:
        send_telegram_message("✅ הבוט פעיל ובודק שערים...")
        response = requests.get('https://api.exchangerate.host/latest?base=EUR&symbols=USD')
        data = response.json()

        if 'rates' in data and 'USD' in data['rates']:
            rate = data['rates']['USD']
            send_telegram_message(f"שער EUR/USD: {rate}")
            return 'Message sent!'
        else:
            send_telegram_message(f"שגיאה בנתונים מהשרת: {data}")
            return str(data)
    except Exception as e:
        send_telegram_message(f"שגיאה כללית בבדיקה: {str(e)}")
        return str(e)

def heartbeat():
    while True:
        try:
            requests.get('https://eur-usd-bot-wb9i.onrender.com/')
        except:
            pass
        time.sleep(600)  # כל 10 דקות

if __name__ == '__main__':
    threading.Thread(target=heartbeat, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
response = requests.get('https://api.exchangerate.host/latest?base=EUR&symbols=USD')
