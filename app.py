from flask import Flask, request
import os
import requests
import random
import time

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ⏱️ анти-спам
LAST_REQUEST_TIME = 0
COOLDOWN = 2  # 2 секунди

# fallback відповіді (якщо API не відповів)
DJ_FALLBACK = [
    "та може й справді варто змінити трек",
    "не знаю, але звучить підозріло 😄",
    "а ти сам як думаєш?",
    "може просто глюк якийсь",
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

        # ❌ дуже короткі повідомлення ігноруємо
        if len(msg) < 3:
            return ""

        # 🎲 не відповідає на все підряд (30% ігнор)
        if random.random() < 0.3:
            return ""

        # ⏱️ cooldown (щоб не було 429)
        now = time.time()
        if now - LAST_REQUEST_TIME < COOLDOWN:
            return random.choice(DJ_FALLBACK)

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
Не будь клоуном і не будь занадто діджеєм.

Правила:
- коротко або середньо (1-3 речення)
- відповідай по змісту
- іноді легкий жарт
- не повторюйся
- не пиши пусті фрази типу "ага зрозумів"

Повідомлення: {msg}
"""
                        }
                    ]
                }
            ]
        }

        # 🔁 2 спроби
        for i in range(2):
            res = requests.post(url, json=payload)

            if res.status_code == 200:
                try:
                    result = res.json()
                    reply = result["candidates"][0]["content"]["parts"][0]["text"]
                    return reply[:300]  # обмеження довжини
                except:
                    continue

            elif res.status_code == 429:
                return "трохи перевантажено, давай через секунду ще раз"

            elif res.status_code == 503:
                continue

        return random.choice(DJ_FALLBACK)

    except:
        return random.choice(DJ_FALLBACK)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
