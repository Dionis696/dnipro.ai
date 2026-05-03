from flask import Flask, request, jsonify
import requests
import os
import json
from luna_brain import get_fallback_response

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("KEY LOADED:", "YES" if GEMINI_API_KEY else "NO")

def ask_gemini(message):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        data = {
            "contents": [
                {
                    "parts": [
                        {"text": f"Відповідай як жива дівчина Luna, коротко, природно:\n{message}"}
                    ]
                }
            ]
        }

        r = requests.post(url, json=data, timeout=5)

        if r.status_code != 200:
            return None

        res = r.json()

        return res["candidates"][0]["content"]["parts"][0]["text"]

    except:
        return None


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user = data.get("user", "User")
        message = data.get("message", "")

        # 🔥 пробуємо Gemini
        reply = ask_gemini(message)

        # 🔥 fallback якщо Gemini впав
        if not reply:
            reply = get_fallback_response(user, message)

        if not reply:
            reply = "..."

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": "error"})


@app.route("/")
def home():
    return "Luna AI is running 🔥"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
