import requests
from flask import Flask, request

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
    response = requests.get('https://api.exchangerate.host/latest?base=EUR&symbols=USD')
    rate = response.json()['rates']['USD']
    if abs(rate - check_eur_usd.last_rate) > 0.005:
        send_telegram_message(f"📉 EUR/USD תזוזה חדה! שער נוכחי: {rate}")
    check_eur_usd.last_rate = rate
    return {'rate': rate}

check_eur_usd.last_rate = 1.08  # ערך התחלתי

if __name__ == '__main__':
    send_telegram_message("✅ הבוט עלה ועובד!")
    threading.Thread(target=heartbeat, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
