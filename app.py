from flask import Flask, request, jsonify
import random

from luna_brain import (
    should_ignore,
    detect_language,
    should_use_ai,
    get_fallback_response,
    get_atmosphere_message,
    update_user_memory,
    ask_gemini
)

app = Flask(__name__)

# 🔥 ФІКС UTF (ОСНОВНА ПРОБЛЕМА ТВОЯ)
app.config["JSON_AS_ASCII"] = False


# =====================
# 🧼 SAFE CLEAN (ДУЖЕ ВАЖЛИВО)
# =====================
def safe(text):
    if not text:
        return "..."

    return str(text) \
        .replace("\\u", "u") \
        .replace("u0430", "а") \
        .replace("u043d", "н") \
        .replace("u0438", "и")


# =====================
# 💬 CHAT
# =====================
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json or {}

    user = data.get("user", "user")
    message = data.get("message", "")

    if should_ignore(message):
        return jsonify({"reply": "..."})

    update_user_memory(user, message)

    lang = detect_language(message)
    use_ai = should_use_ai(message)

    reply = None

    # 🤖 AI
    if use_ai:
        reply = ask_gemini(message, lang)

    # 🎭 FALLBACK
    if not reply:
        reply = get_fallback_response(user, message, lang)

    # 🎧 ATMOSPHERE
    if random.random() < 0.1:
        reply += "\n" + get_atmosphere_message()

    return jsonify({"reply": safe(reply)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
