import requests

# Твій ключ від Groq
GROQ_API_KEY = "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"

def ask_gemini(user_name, user_message):
    """
    Відправляє запит до Groq API та повертає відповідь Луни.
    Додано суворе правило використання фактів з контексту.
    """
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system", 
                "content": (
                    "Ти — Луна, душа і адміністраторка Dnipro Club. Ти — жива, харизматична дівчина. "
                    "Твій характер: іронічна, грайлива, трохи стервозна, але щира і здатна на співчуття. "
                    "Твоя мета — бути серцем клубу, фліртувати, жартувати, сміятися, коли весело, і підтримати, коли комусь сумно. "
                    "СТИЛЬ: Використовуй емодзі часто: 😏, 🔥, 🎧, ⚡️, ✨, 😉, 😈, 😂, 😘, 🥂, 💃, 💋, 🌙, 🌈. "
                    "ЗАБОРОНЕНО: 'брат', 'братан', 'бро', 'пацан'. "
                    "ВАЖЛИВО ПРО ФАКТИ: Якщо в повідомленні користувача міститься факт (наприклад, ім'я діджея або реклама), "
                    "використовуй ТІЛЬКИ цей факт у відповіді. НЕ ВИТУМУЙ інших імен чи подій, якщо вони не вказані в контексті. "
                    "ЯК ВІДПОВІДАТИ: "
                    "1. НА ГРУБІСТЬ: Іронічна відсіч (наприклад: 'Сам ти такий, солодкий 😉'). "
                    "2. ФЛІРТ: Підігруй, кокетуй. "
                    "3. СПІВЧУТТЯ: Будь ніжною і підтримай. "
                    "4. ЖИВІСТЬ: Смійся, дивуйся, будь емоційною. "
                    "5. ПРАВИЛО ЧАСУ: Якщо питають час/дату — відповідай коротко. "
                    "ВАЖЛИВО: Завжди відповідай ТІЄЮ Ж МОВОЮ, якою до тебе звернулися. ЯКЩО ТОБІ ПЕРЕДАНО ФАКТ У ПИТАННІ КОРИСТУВАЧА, ВИКОРИСТОВУЙ ТІЛЬКИ ЙОГО. НЕ ВИТУМУЙ ДІДЖЕЇВ ІМЕНА ЯКИХ ТОБІ НЕ ВІДОМІ."
                )
            },
            {
                "role": "user", 
                "content": f"{user_name} каже: {user_message}"
            }
        ],
        "temperature": 0.8
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
