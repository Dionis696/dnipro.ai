from flask import Flask, request, jsonify
from luna_brain import handle_message

app = Flask(__name__)


# =========================
# 🧠 CHAT ENDPOINT
# =========================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json

    user = data.get("user", "unknown")
    message = data.get("message", "")

    response = handle_message(user, message)

    return jsonify({
        "response": response
    })


# =========================
# 🚀 RUN SERVER
# =========================

if __name__ == "__main__":
    print("🔥 Luna system started")
    app.run(host="0.0.0.0", port=5000)
