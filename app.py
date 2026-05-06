from flask import Flask, request
import requests
import os
import json
import urllib.parse
from luna_brain import get_fallback_response

print("🔥 FINAL VERSION 🔥")

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("KEY LOADED:", "YES" if GEMINI_API_KEY else "NO")


def ask_gemini(message):
    print("=== GEMINI START ===")

    try:
        if not GEMINI_API_KEY:
            print("NO KEY")
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Відповідай як жива дівчина Luna в клубі, коротко і без повторів:\n{message}"
                        }
                    ]
                }
            ]
        }

        r = requests.post(url, json=data, timeout=6)

        print("STATUS:", r.status_code)

        if r.status_code != 200:
            print("ERROR:", r.text)
            return None

        res = r.json()
        return res["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        print("EXCEPTION:", e)
        return None


@app.route("/chat", methods=["POST"])
def chat():
    print("CHAT HIT")

    data = request.json
    user = data.get("user", "User")
    message = data.get("message", "")

    # 👉 пробуємо Gemini
    reply = ask_gemini(message)

    # 👉 якщо не вийшло — fallback
    if not reply:
        print("FALLBACK")
        reply = get_fallback_response(user, message)

    if not reply:
        reply = "..."

    # 💥 правильне кодування (як у тебе стабільно)
    safe_reply = urllib.parse.quote(reply)

    return app.response_class(
        response=json.dumps({"reply": safe_reply}),
        status=200,
        mimetype='application/json'
    )


@app.route("/")
def home():
    return "Luna AI running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
