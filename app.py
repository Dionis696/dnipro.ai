from flask import Flask, request
import requests
import os
import json
import urllib.parse
from luna_brain import get_fallback_response

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("KEY LOADED:", "YES" if GEMINI_API_KEY else "NO")


def ask_gemini(message):
    try:
        if not GEMINI_API_KEY:
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"""
Ти — дівчина Luna в клубі DNIPRO 😏
Стиль: жива, трохи флірт, короткі відповіді, без занудства

Правила:
- не пиши довго
- не повторюйся
- відповідай по змісту
- можна мікс мов (ua/ru/en)
- іноді додавай вайб клубу

Повідомлення:
{message}
"""
                        }
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

        # 🔥 1. пробуємо Gemini
        reply = ask_gemini(message)

        # 🔁 2. fallback якщо нема відповіді
        if not reply:
            reply = get_fallback_response(user, message)

        if not reply:
            reply = "..."

        # 💥 стабільне кодування
        safe_reply = urllib.parse.quote(reply)

        return app.response_class(
            response=json.dumps({"reply": safe_reply}),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        print("ERROR:", e)
        return app.response_class(
            response=json.dumps({"reply": "error"}),
            status=200,
            mimetype='application/json'
        )


@app.route("/")
def home():
    return "Luna AI is running 🔥"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
