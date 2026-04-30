from flask import Flask
import os
import requests

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


@app.route('/')
def home():
    return "Server is working 👍"


@app.route('/models')
def models():
    if not GEMINI_API_KEY:
        return "No API key ❌"

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
    res = requests.get(url)

    return res.text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
