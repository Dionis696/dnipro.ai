import requests
import json

GROQ_API_KEY = "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"

def ask_gemini(user_name, user_message):
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Структура повідомлень має бути чіткою
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system", 
                "content": "Ти — Луна з Dnipro Club. Відповідай сленгом, коротко, емоційно, з емодзі (😏, 🔥, 🎧)."
            },
            {
                "role": "user", 
                "content": f"{user_name} каже: {user_message}"
            }
        ],
        "temperature": 0.7
    }
    
    try:
        # Важливо: використовуємо json=payload, це автоматично ставить потрібні заголовки
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            # Виведемо текст помилки, щоб зрозуміти, що саме не подобається Groq
            print(f"❌ Помилка API (400): {response.text}", flush=True)
            return None
            
    except Exception as e:
        print(f"💥 Помилка в коді: {e}", flush=True)
        return None
