        # запит до Gemini
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Ти веселий DJ клубу Дніпро. Відповідай коротко, з гумором. Запит: {msg}"
                        }
                    ]
                }
            ]
        }

        res = requests.post(url, json=payload)

        if res.status_code == 200:
            result = res.json()
            try:
                reply = result["candidates"][0]["content"]["parts"][0]["text"]
                return reply
            except:
                return "Gemini щось намутив 😅"
        else:
            return f"Gemini error: {res.text}"
