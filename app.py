from flask import Flask, request, Response
from luna_brain import process_luna_message
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "Luna ONLINE"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}

    user = data.get("user", "unknown")
    message = data.get("message", "")

    reply = process_luna_message(user, message)

    if reply is None:
        reply = ""

    # 🔥 ГОЛОВНИЙ ФІКС
    response_data = json.dumps(
        {"reply": reply},
        ensure_ascii=False
    )

    return Response(
        response_data,
        content_type="application/json; charset=utf-8"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
