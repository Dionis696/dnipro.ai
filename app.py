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


# 🔥 GEMINI
def ask_gemini(message):
    print("=== GEMINI START ===")

    try:
        if not GEMINI_API_KEY:
            print("NO KEY")
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Відповідай як жива дівчина Luna в клубі, коротко, природно, без повторів:\n{message}"
                        }
                    ]
                }
            ]
        }

        r = requests.post(url, json=data, timeout=10)

        print("STATUS:", r.status_code)
        print("RAW:", r.text)

        if r.status_code != 200:
            return None

        res = r.json()

        if "candidates" not in res:
            print("NO CANDIDATES")
            return None

        text = res["candidates"][0]["content"]["parts"][0]["text"]

        print("GEMINI OK")
        return text

    except Exception as e:
        print("EXCEPTION:", e)
        return None


# 🔥 CHAT
@app.route("/chat", methods=["POST"])
def chat():
    print("CHAT HIT")

    try:
        data = request.json
        print("DATA:", data)

        user = data.get("user", "User")
        message = data.get("message", "")

        # 👉 пробуємо Gemini
        reply = ask_gemini(message)

        # 👉 fallback якщо нема відповіді
        if not reply:
            print("FALLBACK MODE")
            reply = get_fallback_response(user, message)
        else:
            print("USING GEMINI")

        if not reply:
            reply = "..."

        # 💥 правильне кодування
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
    return "Luna AI running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
