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

    # 1. ПЕРЕВІРКА НА НОВОГО КОРИСТУВАЧА (Вітання)
    welcome_msg = check_new_user(user)
    if welcome_msg:
        return Response(
            json.dumps({"reply": welcome_msg}, ensure_ascii=False),
            content_type="application/json; charset=utf-8"
        )

    # 2. ПЕРЕВІРКА НА ІДЛ (якщо чат мовчить більше 10 хв)
    idle_reply = check_idle()
    if idle_reply:
        return Response(
            json.dumps({"reply": idle_reply}, ensure_ascii=False),
            content_type="application/json; charset=utf-8"
        )

    # 3. ОТРИМАННЯ ВІДПОВІДІ ВІД МОЗКУ ЛУНИ
    reply = ""
    try:
        reply = luna.reply(user, message)
    except Exception as e:
        print(f"Luna CRITICAL ERROR: {e}")
        reply = ""

    # 4. ОПТИМІЗАЦІЯ (Якщо немає відповіді, статус 204)
    if not reply or reply.strip() == "":
        return Response("", status=204)

    # 5. ВІДПРАВКА ВІДПОВІДІ
    return Response(
        json.dumps({"reply": reply}, ensure_ascii=False),
        content_type="application/json; charset=utf-8"
    )

if __name__ == "__main__":
    print("🔥 Luna ONLINE - Система запущена")
    # Порт для Render або локальний за замовчуванням
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
