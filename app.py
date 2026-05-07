from flask import Flask, request
import requests
import os
import json
import urllib.parse

app = Flask(__name__)

print("🔥 GEMINI DEBUG VERSION 🔥")

# 🔒 API KEY тільки з Render Environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("KEY LOADED:", "YES" if GEMINI_API_KEY else "NO")


# 🤖 GEMINI
def ask_gemini(message):

    print("=== GEMINI START ===")
    print("USER MESSAGE:", message)

    try:

        if not GEMINI_API_KEY:
            print("❌ NO API KEY")
            return "ERROR: NO API KEY"

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"""
Ти Luna — жива дівчина в клубі Dnipro.
Відповідай коротко, живо і природно.

Повідомлення:
{message}
"""
                        }
                    ]
                }
            ]
        }

        print("📤 SENDING TO GEMINI...")

        r = requests.post(url, json=data, timeout=15)

        print("📥 STATUS:", r.status_code)
        print("📥 RESPONSE:", r.text)

        if r.status_code != 200:
            return f"GEMINI ERROR {r.status_code}"

        res = r.json()

        if "candidates" not in res:
            return "NO CANDIDATES IN RESPONSE"

        reply = res["candidates"][0]["content"]["parts"][0]["text"].strip()

        print("✅ GEMINI REPLY:", reply)

        return reply

    except Exception as e:

        print("💥 EXCEPTION:", str(e))

        return f"EXCEPTION: {str(e)}"


# 💬 CHAT
@app.route("/chat", methods=["POST"])
def chat():

    print("🚨 CHAT FUNCTION WORKING 🚨")

    try:

        data = request.json

        user = data.get("user", "User")
        message = data.get("message", "")

        print("USER:", user)
        print("MESSAGE:", message)

        # 🤖 ТІЛЬКИ GEMINI
        reply = ask_gemini(message)

        if not reply:
            reply = "EMPTY RESPONSE"

        # 🔒 UTF FIX
        safe_reply = urllib.parse.quote(reply)

        return app.response_class(
            response=json.dumps({"reply": safe_reply}),
            status=200,
            mimetype="application/json"
        )

    except Exception as e:

        print("💥 CHAT ERROR:", str(e))

        safe_reply = urllib.parse.quote(str(e))

        return app.response_class(
            response=json.dumps({"reply": safe_reply}),
            status=200,
            mimetype="application/json"
        )


@app.route("/")
def home():
    return "Luna Debug Server Running 🔥"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
