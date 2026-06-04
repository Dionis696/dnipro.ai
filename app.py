from flask import Flask, request, Response
import json
import os
from luna_brain import luna, check_idle

app = Flask(__name__)

@app.route("/")
def home():
    return "Luna ONLINE 😏"

@app.route("/chat", methods=["POST"])
def chat():
    # Отримуємо дані з запиту
    data = request.get_json(silent=True) or {}
    user = data.get("user", "unknown")
    message = data.get("message", "")

    # 1. СПОЧАТКУ намагаємось отримати відповідь від мозку Луни
    # Луна тепер відповідає на все, включаючи грубість, завдяки оновленому промпту
    try:
        reply = luna.reply(user, message)
        if reply and isinstance(reply, str) and reply.strip() != "":
            return Response(
                json.dumps({"reply": reply}, ensure_ascii=False),
                content_type="application/json; charset=utf-8"
            )
    except Exception as e:
        print(f"Luna BRAIN ERROR: {e}")

    # 2. Якщо мозок мовчить — перевіряємо IDLE (для підтримки активності)
    try:
        idle_reply = check_idle()
        if idle_reply and isinstance(idle_reply, str):
            return Response(
                json.dumps({"reply": idle_reply}, ensure_ascii=False),
                content_type="application/json; charset=utf-8"
            )
    except Exception as e:
        print(f"Idle Check ERROR: {e}")

    # 3. Якщо нічого не підійшло — тиша (204 No Content)
    return Response("", status=204)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🔥 Luna ONLINE - Система запущена на порті {port}")
    app.run(
        host="0.0.0.0",
        port=port
    )
