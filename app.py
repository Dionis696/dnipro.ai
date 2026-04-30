from flask import Flask, request
import os
import requests
import random
import time

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ⏱️ анти-спам
LAST_REQUEST_TIME = 0
COOLDOWN = 2  # секунди

# fallback (людські відповіді)
DJ_FALLBACK = [
    "та може й варто змінити трек",
    "не знаю, але щось дивне 😄",
    "а ти як думаєш?",
    "може просто глюк",
    "ну щось тут не те"
]


@app.route('/')
def home():
    return "AI bot is running"


@app.route('/chat', methods=['POST'])
def chat():
    global LAST_REQUEST_TIME

    try:
        data = request.json
        msg = data.get("message", "").strip().lower()

        # ❌ ігнор дуже коротких
        if len(msg) < 3:
            return ""

        # 🎲 не відповідає на кожне повідомлення
        if random.random() < 0.3:
            return ""

        # ⏱️ cooldown
        now = time.time()
        if now - LAST_REQUEST_TIME < COOLDOWN:
            return ""

        LAST_REQUEST_TIME = now

        if not GEMINI_API_KEY:
            return random.choice(DJ_FALLBACK)

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"""
Ти звичайна людина в чаті клубу.
Говориш просто і по темі.

Правила:
- 1-3 речення
- не пиши довго
- не будь клоуном
- іноді легкий жарт

Повідомлення: {msg}
"""
                        }
                    ]
                }
            ]
        }

        # 🔁 пробуємо 2 рази
        for _ in range(2):
            res = requests.post(url, json=payload)

            if res.status_code == 200:
                try:
                    result = res.json()
                    reply = result["candidates"][0]["content"]["parts"][0]["text"]
                    return reply[:300]
                except:
                    continue

            elif res.status_code in [429, 503]:
                time.sleep(1)
                continue

        # якщо не вийшло — або мовчимо, або fallback
        if random.random() < 0.5:
            return ""
        else:
            return random.choice(DJ_FALLBACK)

    except:
        return ""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
