from flask import Flask, request
import requests
import os
import json
import urllib.parse
from luna_brain import get_fallback_response

app = Flask(__name__)

print("🔥 LUNA SECURE VERSION 🔥")

# 🔒 ключ тільки з Render Environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("KEY LOADED:", "YES" if GEMINI_API_KEY else "NO")


# 🤖 Gemini
def ask_gemini(message):
    try:
        if not GEMINI_API_KEY:
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"""
Ти Luna — жива дівчина в клубі Dnipro.
Відповідай природно, коротко, емоційно.
Не повторюй одні й ті самі фрази.
Іноді фліртуй.
Не будь як бот.

Повідомлення:
{message}
"""
                        }
                    ]
                }
            ]
        }

        r = requests.post(url, json=data, timeout=10)

        if r.status_code != 200:
            print("GEMINI ERROR:", r.status_code)
            return None

        res = r.json()

        if "candidates" not in res:
            print("BAD RESPONSE")
            return None

        return res["candidates"][0]["content"]["parts"][0]["text"].strip()

    except Exception as e:
        print("EXCEPTION:", e)
        return None


# 💬 Chat
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json

        user = data.get("user", "User")
        message = data.get("message", "")

        # 🤖 пробуємо Gemini
        reply = ask_gemini(message)

        # 🔁 fallback якщо Gemini недоступний
        if not reply:
            reply = get_fallback_response(user, message)

        if not reply:
            reply = "..."

        # 🔒 правильне кодування
        safe_reply = urllib.parse.quote(reply)

        return app.response_class(
            response=json.dumps({"reply": safe_reply}),
            status=200,
            mimetype="application/json"
        )

    except Exception as e:
        print("CHAT ERROR:", e)

        return app.response_class(
            response=json.dumps({"reply": "error"}),
            status=200,
            mimetype="application/json"
        )


@app.route("/")
def home():
    return "Luna AI is running 🔥"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
