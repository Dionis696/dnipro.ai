from flask import Flask, request
import json

app = Flask(__name__)

print("🔥 TEST VERSION STARTED 🔥")


@app.route("/chat", methods=["POST"])
def chat():
    print("🚨 CHAT FUNCTION 100% WORKING 🚨")

    data = request.json
    print("DATA:", data)

    return app.response_class(
        response=json.dumps({"reply": "OK"}),
        status=200,
        mimetype='application/json'
    )


@app.route("/")
def home():
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
