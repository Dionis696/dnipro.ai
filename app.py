from flask import Flask, request, Response
import json
import os

from luna_brain import luna

app = Flask(__name__)


@app.route("/")
def home():
    return "Luna ONLINE 😏"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}

    user = data.get("user", "unknown")
    message = data.get("message", "")

    reply = ""

    try:
        # 🧠 Передаємо запит у головний мозок Луни
        reply = luna.reply(user, message)

        # ❗ Захист від None
        if not reply:
            reply = ""

    except Exception as e:
        print("Luna ERROR:", e)
        reply = ""

    # =========================
    # 🛑 ОПТИМІЗАЦІЯ ПІНГУ
    # =========================
    if reply == "":
        return Response("", status=204)

    # =========================
    # 💬 НОРМАЛЬНА ВІДПОВІДЬ
    # =========================
    return Response(
        json.dumps({"reply": reply}, ensure_ascii=False),
        content_type="application/json; charset=utf-8"
    )


if __name__ == "__main__":
    print("🔥 Luna ONLINE")

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
