import requests
import time
import telegram
from datetime import datetime

# פרטי הבוט
TOKEN = '7665383679:AAGa263syK8FdyOiSXHLsUtKEKzFajbZJlM'
CHAT_ID = 'your_chat_id_here'  # שים את ה־chat_id שלך כאן
bot = telegram.Bot(token=TOKEN)

# הגדרת רגישות – שינוי של לפחות 0.005 (50 פיפס)
THRESHOLD = 0.005

# משתנה לשמירת השער האחרון
last_rate = None

def get_current_rate():
    url = "https://api.exchangerate.host/latest?base=EUR&symbols=USD"
    response = requests.get(url)
    data = response.json()
    return float(data["rates"]["USD"])

def send_alert(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

def heartbeat():
    bot.send_message(chat_id=CHAT_ID, text="💓 הבוט פעיל ובודק שערים...")

# הפעלה ראשונית עם heartbeat
heartbeat()

while True:
    try:
        current_rate = get_current_rate()
        now = datetime.now().strftime('%H:%M:%S')

        if last_rate:
            diff = abs(current_rate - last_rate)
            if diff >= THRESHOLD:
                direction = "📈 עלייה" if current_rate > last_rate else "📉 ירידה"
                message = f"{direction} חדה בזוג EUR/USD\nשער חדש: {current_rate:.5f} ({now})"
                send_alert(message)

        last_rate = current_rate

        # heartbeat כל שעה
        if datetime.now().minute == 0 and datetime.now().second < 5:
            heartbeat()

        time.sleep(60)  # בדיקה כל דקה

    except Exception as e:
        print(f"שגיאה: {e}")
        time.sleep(60)
