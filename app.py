from flask import Flask, request, jsonify
from luna_brain import process_luna_message

app = Flask(__name__)

@app.route("/")
def home():
    return "Luna AI ONLINE"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json or {}

        user = data.get("user", "unknown")
        message = data.get("message", "")

        reply = process_luna_message(user, message)

        # 🔥 ВАЖЛИВО: LSL НЕ ПОВИНЕН БАЧИТИ ПУСТОГО ВІДПОВІДІ
        if reply is None or reply.strip() == "":
            reply = "..."

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        # 🔥 ніколи не падаємо
        return jsonify({
            "reply": "..."
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
