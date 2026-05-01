from flask import Flask, request
import requests
import os
import time
import random

import luna_brain

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

last_reply_time = 0


# 🔹 Gemini функція
def ask_gemini(msg):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Ти дівчина Luna, спілкуєшся як жива людина, коротко, іноді флірт 😏. Відповідь 1-2 речення.\n\n{msg}"
                    }
                ]
            }
        ]
    }

    try:
        r = requests.post(url, json=data, timeout=5)
        res = r.json()

        return res["candidates"][0]["content"]["parts"][0]["text"]

    except:
        return None


@app.route('/')
def home():
    return "Luna AI працює 💃"


@app.route('/chat', methods=['POST'])
def chat():
    global last_reply_time

    data = request.json
    msg = data.get("message", "")

    now = time.time()

    # ⛔ анти-спам
    if now - last_reply_time < 2:
        return ""

    last_reply_time = now

    msg_lower = msg.lower()

    # 🔥 чи звернулись до Luna
    is_called = "luna" in msg_lower or "луна" in msg_lower

    # 🎲 шанс відповіді
    if not is_called:
        if random.random() > 0.2:
            return ""

    # 🧠 пробуємо Gemini
    reply = ask_gemini(msg)

    # ❌ якщо Gemini впав
    if not reply:
        reply = luna_brain.get_reply(msg)

    # 🎭 іноді додаємо історію
    extra = luna_brain.maybe_story()
    if extra:
        reply += "\n" + extra

    # 💃 іноді танці
    extra2 = luna_brain.maybe_dance()
    if extra2:
        reply += "\n" + extra2

    return reply


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
