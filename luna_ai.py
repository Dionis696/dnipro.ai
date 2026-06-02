import requests

# Твій ключ від Groq
GROQ_API_KEY = "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"

def ask_gemini(user_name, user_message):
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Використовуємо актуальну модель: llama-3.3-70b-versatile
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system", 
                "content": "Ти — Луна з Dnipro Club. Твій стиль: сленговий, короткий, емоційний, завжди використовуй емодзі (😏, 🔥, 🎧, ⚡️)."
            },
            {
                "role": "user", 
                "content": f"{user_name} каже: {user_message}"
            }
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            print(f"❌ Помилка API (Groq): {response.status_code} - {response.text}", flush=True)
            return None
            
    except Exception as e:
        print(f"💥 Помилка в luna_ai: {e}", flush=True)
        return None
