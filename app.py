from flask import Flask, request, Response
from luna_brain import handle_message
import json
import traceback

app = Flask(__name__)

@app.route("/")
def home():
    return "Luna ONLINE"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json or {}

        user = data.get("user", "unknown")
        message = data.get("message", "")

        reply = handle_message(user, message)

        if not reply:
            reply = ""

        return Response(
            json.dumps({"reply": reply}, ensure_ascii=False),
            content_type="application/json"
        )

    except Exception as e:
        print("🔥 ERROR:", str(e))
        traceback.print_exc()

        return Response(
            json.dumps({"reply": ""}, ensure_ascii=False),
            content_type="application/json"
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
