from flask import Flask, request, Response
import json

from luna_brain import luna  # 🔥 беремо новий brain instance

app = Flask(__name__)

# =========================
# 🌐 HOME
# =========================

@app.route("/")
def home():
    return "Luna ONLINE"

# =========================
# 💬 CHAT (FIXED)
# =========================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json or {}

    user = data.get("user", "unknown")
    message = data.get("message", "")

    # 🔥 ВАЖЛИВО: використовуємо новий brain правильно
    reply = luna.reply(user, message)

    if not reply:
        reply = ""

    response_data = json.dumps(
        {"reply": reply},
        ensure_ascii=False
    )

    return Response(
        response_data,
        content_type="application/json; charset=utf-8"
    )

# =========================
# 🚀 RUN
# =========================

if __name__ == "__main__":
    print("🔥 Luna ONLINE")
    app.run(host="0.0.0.0", port=10000)
