import requests
import threading
import time
from flask import Flask
from datetime import datetime

# הגדרות
BOT_TOKEN = '7665383679:AAGa263syK8FdyOiSXHLsUtKEKzFajbZJlM'
CHAT_ID = '1589414763'
THRESHOLD = 0.005  # שינוי חד בשער

app = Flask(__name__)
last_rate = None
daily_rates = []

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
        daily_rates.append(rate)

        if last_rate is not None and abs(rate - last_rate) >= THRESHOLD:
            change = rate - last_rate
            direction = "⬆️ עלייה חדה" if change > 0 else "⬇️ ירידה חדה"
            send_telegram_message(
                f"🚨 {direction} בזיהוי!\nשינוי של {change:.5f} בשער EUR/USD\nשער נוכחי: {rate:.5f} ({now})"
            )
        last_rate = rate
    except Exception as e:
        send_telegram_message(f"שגיאה בבדיקת שערים: {e}")

def send_daily_trend():
    while True:
        time.sleep(3600 * 24)  # כל 24 שעות
        if len(daily_rates) > 1:
            trend = daily_rates[-1] - daily_rates[0]
            message = (
                f"📊 סיכום יומי של שער EUR/USD:\n"
                f"השער התחיל ב: {daily_rates[0]:.5f}\n"
                f"השער סיים ב: {daily_rates[-1]:.5f}\n"
                f"{'⬆️ יותר עליות' if trend > 0 else '⬇️ יותר ירידות' if trend < 0 else '➖ יציב'}"
            )
            send_telegram_message(message)
        daily_rates.clear()

def loop_check():
    while True:
        check_eur_usd()
        time.sleep(3600)  # כל שעה

def heartbeat():
    while True:
        send_telegram_message("💓 הבוט פעיל ובודק שערים כל שעה.")
        time.sleep(3600)

@app.route('/')
def home():
    return '✅ הבוט רץ!'

# הפעלת תהליכים ברקע
threading.Thread(target=loop_check, daemon=True).start()
threading.Thread(target=heartbeat, daemon=True).start()
threading.Thread(target=send_daily_trend, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
