from flask import Flask, request, jsonify
import requests
import time
import random

from luna_brain import (
    should_ignore,
    detect_language,
    should_use_ai,
    get_fallback_response,
    get_atmosphere_message,
    update_user_memory
)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

GEMINI_API_KEY = "ТУТ_ТВОЙ_API_KEY"

last_request_time = 0
COOLDOWN = 6


# ===== 🔥 FIX UTF-8 (ГОЛОВНЕ РІШЕННЯ) =====
def fix_text(text):
    if not text:
        return text
    try:
        # repair broken unicode like u00d0u00a5
        return text.encode("raw_unicode_escape").decode("utf-8", errors="ignore")
    except:
        return text


# ===== GEMINI =====
def ask_gemini(user_text, lang):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    prompt = f"""
You are Luna 💃 DJ girl in Club DNIPRO 🎧
Reply short (1-2 sentences), natural, playful.
Add emojis sometimes 😏🔥💃🎶

Language: {lang}
User: {user_text}
"""

    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        r = requests.post(url, json=data, timeout=15)
        result = r.json()

        text = result["candidates"][0]["content"]["parts"][0]["text"]
        return fix_text(text)

    except:
        return None


# ===== CHAT =====
@app.route('/chat', methods=['POST'])
def chat():
    global last_request_time

    data = request.json
    user = data.get("user", "user")
    message = data.get("message", "")

    if should_ignore(message):
        return jsonify({"reply": ""})

    update_user_memory(user, message)

    lang = detect_language(message)
    use_ai = should_use_ai(message)

    now = time.time()

    # ===== GEMINI =====
    if use_ai and (now - last_request_time > COOLDOWN):
        ai_reply = ask_gemini(message, lang)

        if ai_reply:
            last_request_time = now
            return jsonify({"reply": ai_reply})

    # ===== FALLBACK =====
    reply = fix_text(get_fallback_response(user, message, lang))

    # ===== ATMOSPHERE =====
    if random.random() < 0.10:
        reply += "\n" + fix_text(get_atmosphere_message())

    return jsonify({"reply": reply})


# ===== RUN =====
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
