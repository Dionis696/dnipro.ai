@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        msg = data.get("message", "")

        if not msg.strip():
            return "Скажи щось 😄"

        if not GEMINI_API_KEY:
            return random.choice(DJ_FALLBACK)

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Ти веселий AI DJ клубу Дніпро. Відповідай як живий ведучий, не повторюйся, жартуй. Повідомлення: {msg}"
                        }
                    ]
                }
            ]
        }

        # 🔁 пробуємо 3 рази
        for i in range(3):
            res = requests.post(url, json=payload)

            if res.status_code == 200:
                result = res.json()
                try:
                    return result["candidates"][0]["content"]["parts"][0]["text"]
                except:
                    continue

            elif res.status_code == 503:
                continue  # пробує ще раз

            else:
                return f"Gemini error: {res.text}"

        # якщо не вийшло після 3 спроб
        return random.choice(DJ_FALLBACK)

    except Exception as e:
        return f"ERROR: {str(e)}"
