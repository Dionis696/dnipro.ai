from flask import Flask, request, Response
import json
import os
from luna_brain import luna, check_idle, check_new_user

app = Flask(__name__)

@app.route("/")
def home():
    return "Luna ONLINE 😏"

@app.route("/chat", methods=["POST"])
def chat():
    # Отримуємо дані з запиту
    data = request.json or {}
    user = data.get("user", "unknown")
    message = data.get("message", "")

    # 1. СПОЧАТКУ намагаємось отримати відповідь від мозку Луни
    # Якщо мозок видає змістовну відповідь, ми її повертаємо і не йдемо далі
    try:
        reply = luna.reply(user, message)
        if reply and reply.strip() != "":
            return Response(
                json.dumps({"reply": reply}, ensure_ascii=False),
                content_type="application/json; charset=utf-8"
            )
    except Exception as e:
        print(f"Luna BRAIN ERROR: {e}")

    # 2. ЯКЩО мозок нічого не відповів, перевіряємо, чи це новий користувач
    welcome_msg = check_new_user(user)
    if welcome_msg:
        return Response(
            json.dumps({"reply": welcome_msg}, ensure_ascii=False),
            content_type="application/json; charset=utf-8"
        )

    # 3. ЯКЩО нових немає, перевіряємо, чи не час для повідомлення IDLE
    idle_reply = check_idle()
    if idle_reply:
        return Response(
            json.dumps({"reply": idle_reply}, ensure_ascii=False),
            content_type="application/json; charset=utf-8"
        )

    # 4. Якщо нічого не підійшло, просто повертаємо 204 (тиша)
    return Response("", status=204)

if __name__ == "__main__":
    print("🔥 Luna ONLINE - Система запущена та виправлена")
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
