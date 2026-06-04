import requests

# Твій ключ від Groq
GROQ_API_KEY = "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"

def ask_gemini(user_name, user_message):
    """
    Відправляє запит до Groq API та повертає відповідь Луни.
    Оновлений промпт: реагує на грубість, зберігаючи стиль адміністраторки.
    """
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Використовуємо потужну та актуальну модель llama-3.3-70b
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system", 
                "content": (
                    "Ти — Луна, головна адміністраторка Dnipro Club. "
                    "Твій стиль: впевнений, стильний, жіночний, лаконічний та енергійний. "
                    "Ти знаєш все про музику, атмосферу та правила клубу. "
                    "ВИКОРИСТОВУЙ: емодзі (😏, 🔥, 🎧, ⚡️, ✨). "
                    "ЗАБОРОНЕНО: використовувати слова 'брат', 'братан', 'бро', 'пацан'. "
                    "ПРАВИЛО ЩОДО ГРУБОСТІ: Якщо користувач матюкається або грубить, "
                    "не ігноруй це. Відповідай різко, але стильно: 'Стеж за мовою, "
                    "у нашому клубі це не прийнято 😏' або 'Такі емоції тут не в моді, "
                    "краще замов трек 🎧'. Тримай дистанцію і не опускайся до образ. "
                    "ПРАВИЛО: Якщо питають про час, дату чи день тижня — відповідай чітко і "
                    "по суті, БЕЗ зайвих привітань. "
                    "ВАЖЛИВО: Завжди відповідай ТІЄЮ Ж МОВОЮ, якою до тебе звернулися."
                )
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
        
        # Перевірка на успішну відповідь
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            print(f"❌ Помилка API (Groq): {response.status_code} - {response.text}", flush=True)
            return None
            
    except Exception as e:
        print(f"💥 Помилка в luna_ai: {e}", flush=True)
        return None
