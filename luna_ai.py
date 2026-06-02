import requests

# Твій робочий ключ Groq
GROQ_API_KEY = "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"

def ask_gemini(user_name, user_message):
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system", 
                "content": "Ти — Луна з Dnipro Club. Твій стиль: сленговий, короткий, емоційний, завжди використовуй емодзі (😏, 🔥, 🎧, ⚡️)."
            },
            {
                "role": "user", 
                "content": f"{user_name} каже: {user_message}"
            }
        ]
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            print(f"❌ Помилка API: {response.status_code} - {response.text}")
            return "Луна зараз ставить новий трек, спробуй пізніше! 🎧"
            
    except Exception as e:
        print(f"💥 Помилка: {e}")
        return "Луна на танцполі, не чує! 🔥"
