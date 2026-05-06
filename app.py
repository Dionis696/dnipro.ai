from flask import Flask, request
import json

print("🔥 TEST VERSION 🔥")

app = Flask(__name__)

@app.route("/")
def home():
    return "OK"


@app.route("/chat", methods=["POST"])
def chat():
    print("CHAT HIT!!!")

    data = request.json
    print("DATA:", data)

    return app.response_class(
        response=json.dumps({"reply": "TEST OK"}),
        status=200,
        mimetype='application/json'
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
