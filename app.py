from flask import Flask, request
import requests
import os
import json
from luna_brain import get_fallback_response

app = Flask(__name__)

# 🔑 ключ (ЗАЛИШАЄМО)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("KEY LOADED:", "YES" if GEMINI_API_KEY else "NO")


def ask_gemini(message):
    try:
        # якщо нема ключа — не ліземо
        if not GEMINI_API_KEY:
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"""
Ти — Luna, жива дівчина в клубі DNIPRO.

Стиль:
- природна, жива
- трохи флірт 😏
- не як бот
- коротко або середньо

Правила:
- не кажи що ти AI
- відповідай як у чаті
- іноді грайливо або з настроєм

Мова:
- відповідай мовою повідомлення

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

        # 🔇 ігнор сміття / коротких
        if not message or len(message.strip()) < 2:
            return app.response_class(
                response=json.dumps({"reply": ""}, ensure_ascii=False),
                status=200,
                mimetype='application/json'
            )

        # 🔥 Gemini
        reply = ask_gemini(message)

        # 🔥 fallback якщо треба
        if not reply:
            reply = get_fallback_response(user, message)

        if not reply:
            reply = "..."

        # 💥 ВАЖЛИВО — ФІКС Unicode
        return app.response_class(
            response=json.dumps({"reply": reply}, ensure_ascii=False),
            status=200,
            mimetype='application/json'
        )

    except:
        return app.response_class(
            response=json.dumps({"reply": "error"}, ensure_ascii=False),
            status=200,
            mimetype='application/json'
        )


@app.route("/")
def home():
    return "Luna AI is running 🔥"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
