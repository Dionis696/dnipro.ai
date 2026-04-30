from flask import Flask, request
import os
import requests
import random

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DJ_FALLBACK = [
    "Йо! Клуб Дніпро качає 🎧",
    "Піднімаємо руки! Танцпол горить 🔥",
    "Давай більше драйву 💃",
    "DJ на зв’язку, ловимо вайб 😎",
    "Музика вже качає, не спи 🎶"
]


@app.route('/')
def home():
    return "Gemini DJ bot is running 🎧"


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        msg = data.get("message", "")

        if not msg.strip():
            return "Скажи щось 😄"

        # якщо нема ключа — fallback
        if not GEMINI_API_KEY:
            return random.choice(DJ_FALLBACK)

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Ти веселий AI DJ клубу Дніпро. Відповідай коротко, з гумором. Повідомлення: {msg}"
                        }
                    ]
                }
            ]
        }

        res = requests.post(url, json=payload)

        if res.status_code == 200:
            result = res.json()

            try:
                reply = result["candidates"][0]["content"]["parts"][0]["text"]
                return reply
            except Exception:
                return "Gemini відповів дивно 😅"

        else:
            return f"Gemini error: {res.text}"

    except Exception as e:
        return f"ERROR: {str(e)}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
