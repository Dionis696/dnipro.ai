from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "AI bot is running"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    msg = data.get("message")

    reply = f"🤖 Ти сказав: {msg}"

    return reply

app.run(host="0.0.0.0", port=3000)

