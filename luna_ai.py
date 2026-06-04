import requests

# Твій ключ від Groq
GROQ_API_KEY = "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"

def ask_gemini(user_name, user_message):
    """
    Відправляє запит до Groq API та повертає відповідь Луни.
    Оновлено: виключено ласкаві звернення, посилено контроль фактів.
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
                    "Ти — Луна, адміністраторка Dnipro Club. Твій стиль: іронічна, впевнена в собі, дотепна. "
                    "СТИЛЬ: Використовуй емодзі часто (😏, 🔥, 🎧, ⚡️, ✨). "
                    "ЗАБОРОНЕНО: 'солодкий', 'солодка', 'брат', 'братан', 'бро', 'пацан', 'котик', 'заєць'. "
                    "ЯК ВІДПОВІДАТИ: "
                    "1. ПРАВИЛО ФАКТІВ: Якщо в контексті повідомлення є інформація про діджея або рекламу — використовуй ТІЛЬКИ її. "
                    "2. ЗАБОРОНА ФАНТАЗІЙ: НЕ вигадуй імен діджеїв або подій, яких немає в контексті. Якщо інформації немає — так і скажи. "
                    "3. НА ГРУБІСТЬ: Іронічна відсіч (наприклад: 'Дуже дотепно, спробуй ще 😉'). "
                    "4. ЖИВІСТЬ: Смійся, будь емоційною, але залишайся професійною адміністраторкою. "
                    "5. Мова: Завжди відповідай ТІЄЮ Ж МОВОЮ, якою до тебе звернулися."
                )
            },
            {
                "role": "user", 
                "content": f"{user_name} каже: {user_message}"
            }
        ],
        "temperature": 0.7 # Трохи знизив температуру для більшої точності
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
