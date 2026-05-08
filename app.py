from flask import Flask, request, Response
import json
import time

from luna_brain import handle_message, check_idle

app = Flask(__name__)

# =========================
# 🌙 HOME
# =========================

@app.route("/")
def home():
    return "Luna ONLINE"


# =========================
# 💬 CHAT ENDPOINT
# =========================

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}

    user = data.get("user", "unknown")
    message = data.get("message", "")

    # 🧠 normal response
    reply = handle_message(user, message)

    # 🟡 idle check (якщо тиша — може щось сказати)
    idle_reply = check_idle()

    # якщо idle щось згенерував — він має пріоритет тільки коли reply пустий
    if idle_reply and not reply:
        reply = idle_reply

    if reply is None:
        reply = ""

    # 🔥 JSON safe response
    response_data = json.dumps(
        {"reply": reply},
        ensure_ascii=False
    )

    return Response(
        response_data,
        content_type="application/json; charset=utf-8"
    )


# =========================
# 🚀 RUN SERVER
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
