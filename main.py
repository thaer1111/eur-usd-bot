import requests
import threading
import time
from flask import Flask, request

app = Flask(__name__)

# טוקן וצ'אט ID מהטלגרם
BOT_TOKEN = '7665383679:AAGa263syK8FdyOiSXHLsUtKEKzFajbZJlM'
CHAT_ID = '1589414763'

# שליחת הודעה לטלגרם
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

# בדיקת שער יורו/דולר
def check_eur_usd():
    try:
        response = requests.get('https://api.exchangerate.host/latest?base=EUR&symbols=USD')
        data = response.json()
        rate = data['rates']['USD']
        send_telegram_message(f"שער EUR/USD כרגע: {rate}")
        return 'Message sent!'
    except Exception as e:
        send_telegram_message(f"שגיאה בבדיקה: {e}")
        return str(e)

# בדיקת חיים – שליחת heartbeat כל שעה
def heartbeat():
    while True:
        send_telegram_message("✅ הבוט פעיל ובודק שערים...")
        time.sleep(3600)  # כל שעה

@app.route('/')
def home():
    return 'Bot is running!'

@app.route('/check', methods=['GET'])
def check_route():
    return check_eur_usd()

# הפעלת בדיקת heartbeat ברקע
threading.Thread(target=heartbeat, daemon=True).start()

# הפעלת השרת
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
