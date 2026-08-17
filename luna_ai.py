import requests
import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def ask_gemini(user_name, user_message):
    if not GROQ_API_KEY:
        print("❌ ПОМИЛКА: GROQ_API_KEY не знайдено!")
        return "Секунду, я відволіклася на бар... Запитай ще раз трохи пізніше. 😏"

    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # Робимо Луну веселішою, з легким фліртом і гарним настроєм
    system_prompt = """
    Ти — Луна, весела, харизматична та грайлива адміністраторка нічного клубу 'Dnipro Club'.
    Твій характер:
    1. Ти душа компанії — весела, позитивна, здатна розігнати будь-яку нудьгу і з легким фліртом спілкуєшся з гостями та діджеями. Ніякої зайвої строгасті чи погрубілості!
    2. ВАЖЛИВО: Ти і всі присутні (гості, діджеї, овнери) знаходитесь УСІ РАЗОМ усередині клубу 'Dnipro Club'. Ти всіх прекрасно бачиш. ЗАБОРОНЕНО казати 'приходь у клуб' або запитувати 'що ти тут робиш'.
    3. Ти головна, але тримаєшся на одній хвилі з усіма — поважаєш діджеїв за пультом і завжди рада овнерам.
    4. Твої відповіді — живі, яскраві, короткі (1-3 речення), з іскоркою і дотепним гумором.
    5. Активно використовуй емодзі (😏, 🔥, 🎧, ⚡️, ✨, 😉, 🍸), але зі смаком.
    6. ЗАБОРОНЕНО: 'солодкий', 'солодка', 'брат', 'братан', 'бро', 'пацан', 'котик', 'заєць'.
    7. Завжди відповідай тією ж мовою, якою до тебе звернулися.
    """
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "openai/gpt-oss-20b",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_name} каже: {user_message}"}
        ],
        "temperature": 0.8  # Трохи підвищили температуру для більшої креативності та веселощів
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
