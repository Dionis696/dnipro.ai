from flask import Flask, request, Response
import json

from luna_brain import luna

app = Flask(__name__)


@app.route("/")
def home():
    return "Luna ONLINE"


@app.route("/chat", methods=["POST"])
def chat():

    data = request.json or {}

    user = data.get("user", "unknown")
    message = data.get("message", "")

    reply = luna.reply(user, message)

    response_data = json.dumps(
        {"reply": reply},
        ensure_ascii=False
    )

    return Response(
        response_data,
        content_type="application/json; charset=utf-8"
    )


if __name__ == "__main__":
    print("🔥 Luna ONLINE")
    app.run(host="0.0.0.0", port=10000)
