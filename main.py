import requests
import threading
import time
from flask import Flask, request
from datetime import datetime

# הגדרות
BOT_TOKEN = '7665383679:AAGa263syK8FdyOiSXHLsUtKEKzFajbZJlM'
CHAT_ID = '1589414763'
THRESHOLD = 0.005

app = Flask(__name__)
last_rate = None

def send_telegram_message(text, chat_id=CHAT_ID):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={'chat_id': chat_id, 'text': text})
    except Exception as e:
        print(f"שגיאה בשליחה לטלגרם: {e}")

def check_eur_usd():
    global last_rate
    try:
        response = requests.get("https://api.exchangerate.host/latest?base=EUR&symbols=USD")
        data = response.json()

        if "rates" not in data or "USD" not in data["rates"]:
            send_telegram_message("⚠️ שגיאה בבדיקת שערים: תגובה לא תקינה מהשרת")
            return

        rate = float(data["rates"]["USD"])
        now = datetime.now().strftime('%H:%M:%S')

        if last_rate is not None and abs(rate - last_rate) >= THRESHOLD:
            change = rate - last_rate
            direction = "⬆️ עלייה חדה" if change > 0 else "⬇️ ירידה חדה"
            send_telegram_message(
                f"🚨 {direction} בזיהוי!\nשינוי של {change:.5f} בשער EUR/USD\nשער נוכחי: {rate:.5f} ({now})"
            )
        last_rate = rate
    except Exception as e:
        send_telegram_message(f"שגיאה בבדיקת שערים: {e}")

def loop_check():
    while True:
        check_eur_usd()
        time.sleep(3600)

def heartbeat():
    while True:
        send_telegram_message("💓 הבוט פעיל ובודק שערים כל שעה.")
        time.sleep(3600)

@app.route('/')
def home():
    return '✅ הבוט רץ!'

@app.route('/webhook', methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        send_telegram_message("הבוט מחובר, אך לא מוגדרת תקשורת עם ChatGPT.", chat_id)
    return 'ok'

# הפעלת תהליכים במקביל
threading.Thread(target=loop_check, daemon=True).start()
threading.Thread(target=heartbeat, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
