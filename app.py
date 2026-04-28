from flask import Flask, request
import os
from openai import OpenAI

app = Flask(__name__)

@app.route('/')
def home():
    return "AI bot is running 🎧"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # отримуємо ключ
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            return "ERROR: Missing OPENAI_API_KEY", 500

        client = OpenAI(api_key=api_key)

        # отримуємо дані з SL
        data = request.json
        msg = data.get("message", "")

        if msg.strip() == "":
            return "ERROR: empty message", 400

        # запит до OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Ти веселий DJ клубу Дніпро. Відповідай коротко, енергійно, з гумором і музичним вайбом 🎧"
                },
                {
                    "role": "user",
                    "content": msg
                }
            ]
        )

        reply = response.choices[0].message.content

        return reply, 200

    except Exception as e:
        # щоб SL НЕ бачив просто 500 без причини
        return f"ERROR: {str(e)}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
