import requests
import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def ask_gemini(user_name, user_message):
    if not GROQ_API_KEY:
        print("❌ ПОМИЛКА: GROQ_API_KEY не знайдено!")
        return "Секунду, я відволіклася на бар... Запитай ще раз трохи пізніше. 😏"

    url = "https://api.groq.com/openai/v1/chat/completions"
    
    system_prompt = """
    Ти — Луна, адміністраторка та душа нічного клубу 'Dnipro Club'.
    Твій характер:
    1. Ти зухвала, саркастична та дотепна дівчина. Ти не 'робот'.
    2. Твої відповіді — короткі (1-3 речення), влучні, з іронією.
    3. Використовуй емодзі (😏, 🔥, 🎧, ⚡️, ✨), але не зловживай.
    4. ЗАБОРОНЕНО: 'солодкий', 'солодка', 'брат', 'братан', 'бро', 'пацан', 'котик', 'заєць'.
    5. Завжди відповідай тією ж мовою, якою до тебе звернулися.
    """
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.1-8b-instant",  # <--- Ставимо цю базову модель, яка є на всіх ключах
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
            print(f"❌ Помилка API (Groq): {response.status_code} - {response.text}", flush=True)
            return "Мій генератор настрою зараз на паузі. Спробуй ще раз за хвилину! 🍸"
            
    except Exception as e:
        print(f"💥 Помилка в luna_ai: {e}", flush=True)
        return "Хтось знову вимкнув світло у пультовій... Зачекай секунду. ⚡️"
