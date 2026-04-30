from flask import Flask, request
import os
import requests
import random
import time

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ⏱️ анти-спам (1 запит в 5 сек)
LAST_REQUEST_TIME = 0
COOLDOWN = 5

# 🎧 fallback
DJ_FALLBACK = [
    "мм цікаво 🙂",
    "ага, зрозумів",
    "ну ти даєш 😄",
    "окей, прийняв",
    "є щось в цьому"
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

        # ❌ ігнор коротких/сміттєвих повідомлень
        if len(msg) < 3:
            return ""

        # ❌ не реагує на кожне повідомлення (рандом)
        if random.random() < 0.6:
            return ""

        # ⏱️ cooldown щоб не було 429
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
Ти звичайна людина в чаті клубу Дніпро.
Ти іноді як діджей, але НЕ перегравай.

Правила:
- відповідай коротко (1-2 речення)
- не пиши довгі тексти
- не будь занадто “шоумен”
- іноді жартуй, але легко
- поводься як реальна людина в чаті

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
                result = res.json()
                try:
                    reply = result["candidates"][0]["content"]["parts"][0]["text"]

                    # ✂️ обрізаємо довгі відповіді
                    return reply[:200]

                except:
                    continue

            elif res.status_code == 429:
                return random.choice(DJ_FALLBACK)

            elif res.status_code == 503:
                continue

        return random.choice(DJ_FALLBACK)

    except:
        return random.choice(DJ_FALLBACK)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
