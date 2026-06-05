import requests
import os

# Беремо ключ із налаштувань сервера (Environment Variables)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def ask_gemini(user_name, user_message):
    if not GROQ_API_KEY:
        print("❌ ПОМИЛКА: GROQ_API_KEY не знайдено в оточенні!")
        return None

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
