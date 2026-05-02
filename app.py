import requests
import time
import json
from flask import Flask, request, Response
from luna_brain import get_fallback_response

app = Flask(__name__)

GEMINI_API_KEY = "ТУТ_ТВІЙ_API_KEY"
MODEL = "models/gemini-2.5-flash"

last_api_call = 0


def ask_gemini(message):
    global last_api_call

    # антиспам
    if time.time() - last_api_call < 2:
        return None

    last_api_call = time.time()

    # стиль Luna (щоб не писала "я мовна модель")
    message = "Ти дівчина Luna, відповідаєш коротко, живо, як людина, інколи з фліртом. Не кажи що ти AI.\n" + message

    url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {"parts": [{"text": message}]}
        ]
    }

    try:
        r = requests.post(url, json=payload, timeout=10)

        if r.status_code != 200:
            print("Gemini error:", r.text)
            return None

        data = r.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]

        # фільтр кривих відповідей
        if not text or len(text.strip()) < 2:
            return None

        return text.strip()

    except Exception as e:
        print("Gemini exception:", e)
        return None


def make_json(reply_text):
    return Response(
        json.dumps({"reply": reply_text}, ensure_ascii=False),
        content_type="application/json; charset=utf-8"
    )


@app.route('/')
def home():
    return "Luna + Gemini OK 🔥"


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json

    user = data.get("user", "User")
    message = data.get("message", "")

    # ігнор мусорних символів
    if not any(c.isalnum() for c in message):
        return make_json("")

    # ===== GEMINI =====
    ai_reply = ask_gemini(message)

    if ai_reply:
        return make_json(ai_reply)

    # ===== FALLBACK =====
    fallback = get_fallback_response(user, message)

    if fallback:
        return make_json(fallback)

    return make_json("")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
