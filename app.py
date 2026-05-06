from flask import Flask, request
import requests
import os
import json
import urllib.parse
from luna_brain import get_fallback_response

print("🔥 THIS IS NEW VERSION 🔥")

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("KEY LOADED:", "YES" if GEMINI_API_KEY else "NO")


# 🔥 GEMINI
def ask_gemini(message):
    print("=== GEMINI START ===")
    try:
        if not GEMINI_API_KEY:
            print("NO GEMINI KEY")
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

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

        r = requests.post(url, json=data, timeout=5)

        print("STATUS:", r.status_code)

        if r.status_code != 200:
            print("GEMINI ERROR:", r.text)
            return None

        res = r.json()
        text = res["candidates"][0]["content"]["parts"][0]["text"]

        print("GEMINI OK")
        return text

    except Exception as e:
        print("GEMINI EXCEPTION:", e)
        return None


# 🔥 CHAT
@app.route("/chat", methods=["POST"])
def chat():
    try:
        print("CHAT FUNCTION WORKING")

        data = request.json
        user = data.get("user", "User")
        message = data.get("message", "")

        # 👉 СПОЧАТКУ GEMINI
        reply = ask_gemini(message)

        # 👉 ЯКЩО НЕ ВІДПОВІВ — FALLBACK
        if reply:
            print("USING GEMINI")
        else:
            print("FALLBACK MODE")
            reply = get_fallback_response(user, message)

        if not reply:
            reply = "..."

        # 💥 СТАБІЛЬНИЙ ФІКС КОДУВАННЯ (твій варіант)
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
