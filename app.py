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

# список моделей (він сам підбере робочу)
MODELS = [
    "gemini-1.5-pro-latest",
    "gemini-1.5-flash-latest",
    "gemini-pro"
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

        if not GEMINI_API_KEY:
            return random.choice(DJ_FALLBACK)

        # пробуємо моделі по черзі
        for model in MODELS:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"

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
                try:
                    result = res.json()
                    reply = result["candidates"][0]["content"]["parts"][0]["text"]
                    return reply
                except:
                    continue  # якщо формат дивний — пробує іншу модель

        # якщо всі моделі не спрацювали
        return random.choice(DJ_FALLBACK)

    except Exception as e:
        return f"ERROR: {str(e)}"

@app.route('/models')
def models():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
    res = requests.get(url)
    return res.text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
