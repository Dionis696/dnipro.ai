from flask import Flask, request, jsonify
from luna_brain import process_luna_message

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json or {}

    user = data.get("user", "user")
    message = data.get("message", "")

    reply = process_luna_message(user, message)

    return jsonify({"reply": reply})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
