import requests
import threading
from flask import Flask, request
import time

app = Flask(__name__)

BOT_TOKEN = '7665383679:AAGa263syK8FdyOiSXHLsUtKEKzFajbZJlM'
CHAT_ID = 'הכנס_כאן_את_מספר_הטלגרם_שלך'  # למשל '123456789'

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': text})

@app.route('/')
def home():
    return 'Bot is running!'

@app.route('/check', methods=['GET'])
def check_eur_usd():
    try:
        response = requests.get('https://api.exchangerate.host/latest?base=EUR&symbols=USD')
        data = response.json()
        rate = data['rates']['USD']
        send_telegram_message(f"שער EUR/USD: {rate}")
        return 'Message sent!'
    except Exception as e:
        return str(e)

# Heartbeat כל שעה
def heartbeat():
    while True:
        try:
            requests.get('https://eur-usd-bot-wb9i.onrender.com/check')
        except:
            pass
        time.sleep(3600)

# התחלת ה־heartbeat ברקע
threading.Thread(target=heartbeat, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
