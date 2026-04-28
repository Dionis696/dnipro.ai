from flask import Flask, request
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

@app.route('/')
def home():
    return "AI bot is running"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    msg = data.get("message")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ти — веселий AI діджей клубу Дніпро. Спілкуйся живо, з гумором."},
            {"role": "user", "content": msg}
        ]
    )

    reply = response.choices[0].message.content

    return reply

app.run(host="0.0.0.0", port=3000)
