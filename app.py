from flask import Flask, request, Response
import json

from luna_brain import luna, check_idle
from luna_time import start_live_mode  # 🔥 ДОДАНО

app = Flask(__name__)

# 🔥 ФУНКЦІЯ ВІДПРАВКИ В ЧАТ (ДОДАНО)
def send_message_to_chat(msg):
    print("Luna LIVE:", msg)


@app.route("/")
def home():
    return "Luna ONLINE"

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json or {}

    user = data.get("user", "unknown")
    message = data.get("message", "")

    try:

        reply = luna.reply(user, message)

        # 🌙 IDLE MODE
        if not reply:
            reply = check_idle()

        if not reply:
            reply = ""

    except Exception as e:

        print("Luna ERROR:", e)
        reply = ""

    return Response(
        json.dumps({"reply": reply}, ensure_ascii=False),
        content_type="application/json; charset=utf-8"
    )

if __name__ == "__main__":
    print("🔥 Luna ONLINE")

    # 🔥 ЗАПУСК LIVE РЕЖИМУ (ДОДАНО)
    start_live_mode(send_message_to_chat)

    app.run(host="0.0.0.0", port=10000)
