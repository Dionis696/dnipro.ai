from flask import Flask, request, jsonify
import requests
import time
import random
import re

from luna_brain import (
    should_ignore,
    detect_language,
    should_use_ai,
    get_fallback_response,
    get_atmosphere_message,
    update_user_memory
)

app = Flask(__name__)

GEMINI_API_KEY = "ТУТ_ТВОЙ_API_KEY"

last_request_time = 0
COOLDOWN = 6  # секунд між AI запитами

# ===== GEMINI =====
def ask_gemini(user_text, lang):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    prompt = f"""
You are Luna, a girl in a nightclub chat (Club DNIPRO).
Reply like a real human, short and natural (1-2 sentences max).
Be slightly playful and casual.

Language: {lang}

User: {user_text}
"""

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        r = requests.post(url, json=data)
        result = r.json()

        return result["candidates"][0]["content"]["parts"][0]["text"]

    except:
        return None


# ===== CHAT =====
@app.route('/chat', methods=['POST'])
def chat():
    global last_request_time

    data = request.json
    user = data.get("user", "user")
    message = data.get("message", "")

    # ❌ ігнор сміття
    if should_ignore(message):
        return jsonify({"reply": ""})

    # 🧠 пам’ять
    update_user_memory(user, message)

    # 🌍 мова
    lang = detect_language(message)

    # 🤖 чи викликати AI
    use_ai = should_use_ai(message)

    now = time.time()

    # ===== GEMINI =====
    if use_ai and (now - last_request_time > COOLDOWN):
        ai_reply = ask_gemini(message, lang)

        if ai_reply:
            last_request_time = now
            return jsonify({"reply": ai_reply})

    # ===== FALLBACK =====
    reply = get_fallback_response(user, message, lang)

    # 🎧 іноді атмосфера
    if random.random() < 0.08:
        reply += "\n" + get_atmosphere_message()

    return jsonify({"reply": reply})


# ===== RUN =====
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
