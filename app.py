from flask import Flask, request, Response
import json
from luna_brain import process_luna_message

app = Flask(__name__)

@app.route("/")
def home():
    return "Luna is alive 💃"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}

    user = data.get("user", "user")
    message = data.get("message", "")

    reply = process_luna_message(user, message)

    return Response(
        json.dumps({"reply": reply}, ensure_ascii=False),
        mimetype="application/json; charset=utf-8"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
