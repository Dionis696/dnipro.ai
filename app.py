import requests
import time
from flask import Flask, request, jsonify
from luna_brain import get_fallback_response

app = Flask(__name__)

GEMINI_API_KEY = "ТУТ_ТВІЙ_API_KEY"
MODEL = "models/gemini-2.5-flash"

last_api_call = 0

# =========================
# 🚀 GEMINI
# =========================
def ask_gemini(message):
    global last_api_call

    # анти-спам (1 запит в 2 сек)
    if time.time() - last_api_call < 2:
        return None

    last_api_call = time.time()

    url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": message}
                ]
            }
        ]
    }

    try:
        r = requests.post(url, json=payload, timeout=10)

        if r.status_code != 200:
            print("Gemini error:", r.text)
            return None

        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        print("Gemini exception:", e)
        return None


# =========================
# 🌐 ROUTES
# =========================

@app.route('/')
def home():
    return "Luna + Gemini працює 🔥"


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json

    user = data.get("user", "User")
    message = data.get("message", "")

    # ❌ ігнор мусор
    if not any(c.isalnum() for c in message):
        return jsonify({"reply": ""})

    # ===== GEMINI =====
    ai_reply = ask_gemini(message)

    if ai_reply:
        return jsonify({"reply": ai_reply})

    # ===== FALLBACK =====
    fallback = get_fallback_response(user, message)

    if not fallback:
        return jsonify({"reply": ""})

    return jsonify({"reply": fallback})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
