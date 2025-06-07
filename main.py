import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = 'הכנס_כאן_את_הטוקן_שלך'
CHAT_ID = 'הכנס_כאן_את_מספר_הטלגרם_שלך'

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
        send_telegram_message(f"EUR/USD movement alert! Current rate: {rate}")
    check_eur_usd.last_rate = rate
    return {'rate': rate}

check_eur_usd.last_rate = 1.08  # ערך התחלתי

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
