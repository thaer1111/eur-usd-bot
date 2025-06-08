import requests
import threading
import time
from flask import Flask, request
from datetime import datetime
import openai

# הגדרות
BOT_TOKEN = '7665383679:AAGa263syK8FdyOiSXHLsUtKEKzFajbZJlM'
CHAT_ID = '1589414763'
OPENAI_API_KEY = 'your_openai_key_here'  # שים כאן את המפתח שלך מ-OpenAI

app = Flask(__name__)
last_rate = None
THRESHOLD = 0.005

openai.api_key = OPENAI_API_KEY

def send_telegram_message(text, chat_id=CHAT_ID):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': chat_id, 'text': text})

def check_eur_usd():
    global last_rate
    try:
        response = requests.get("https://api.exchangerate.host/latest?base=EUR&symbols=USD")
        data = response.json()
        rate = float(data['rates']['USD'])

        now = datetime.now().strftime('%H:%M:%S')
        print(f"[{now}] EUR/USD: {rate}")

        if last_rate is not None and abs(rate - last_rate) >= THRESHOLD:
            change = rate - last_rate
            direction = "⬆️ עלייה חדה" if change > 0 else "⬇️ ירידה חדה"
            send_telegram_message(f"🚨 {direction} בזיהוי!\nשינוי של {change:.5f} בשער EUR/USD\nשער חדש: {rate:.5f}")
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

def ask_chatgpt(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"שגיאה בתקשורת עם ChatGPT: {e}"

@app.route('/')
def home():
    return '✅ הבוט רץ!'

@app.route(f"/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"]
        answer = ask_chatgpt(user_text)
        send_telegram_message(answer, chat_id)
    return 'ok'

threading.Thread(target=loop_check, daemon=True).start()
threading.Thread(target=heartbeat, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
