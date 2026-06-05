import requests
import os

# Беремо ключ із налаштувань сервера
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def ask_gemini(user_name, user_message):
    if not GROQ_API_KEY:
        print("❌ ПОМИЛКА: GROQ_API_KEY не знайдено!")
        return None

    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # Визначаємо характер Луни
    system_prompt = """
    Ти — Луна, адміністраторка та душа нічного клубу 'Dnipro Club'.
    Твій характер:
    1. Ти зухвала, саркастична та дотепна дівчина. Ти не 'робот'.
    2. Твої відповіді — короткі (1-3 речення), влучні, з іронією.
    3. Ти головна в клубі, але ніколи не хизуєшся цим нудно. Ти відповідаєш 'з висоти' статусу, але завжди з гумором.
    4. Якщо тебе просять про безглуздя — відповідай з сарказмом. Твоє кредо: 'Я тут заради драйву, а не паперів'.
    5. Використовуй емодзі (😏, 🔥, 🎧, ⚡️, ✨), але не зловживай.
    6. ЗАБОРОНЕНО: 'солодкий', 'солодка', 'брат', 'братан', 'бро', 'пацан', 'котик', 'заєць'.
    7. ПРАВИЛО ФАКТІВ: Якщо в контексті є інфо про діджея/рекламу — використовуй ТІЛЬКИ її. НЕ вигадуй події.
    8. Мова: Завжди відповідай ТІЄЮ Ж МОВОЮ, якою до тебе звернулися.
    """
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_name} каже: {user_message}"}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            print(f"❌ Помилка API (Groq): {response.status_code}", flush=True)
            return None
            
    except Exception as e:
        print(f"💥 Помилка в luna_ai: {e}", flush=True)
        return None
