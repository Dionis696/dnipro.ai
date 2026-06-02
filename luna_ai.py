import os
import requests

# 🔑 Беремо ключ з налаштувань Render. Якщо тестуєш на комп'ютері, встав свій ключ другим параметром.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "ТВІЙ_КЛЮЧ_ДЛЯ_ЛОКАЛЬНОГО_ТЕСТУ")

def ask_gemini(user_name, user_message):
    if not GEMINI_API_KEY or GEMINI_API_KEY == "ТВІЙ_КЛЮЧ_ДЛЯ_ЛОКАЛЬНОГО_ТЕСТУ":
        print("GEMINI ERROR: Ключ API не знайдено або не налаштовано!")
        return None

    # 🔥 Використовуємо нову швидку модель gemini-1.5-flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    # 🎭 Формуємо характер Луни прямо всередині запиту
    system_instruction = (
        "Ти — Луна, зухвала, розумна та неймовірно харизматична тусовщиця нічного клубу 'Dnipro Club' у Second Life. "
        "Ти обожнюєш електронну музику, нічний вайб, глибокі баси та гучні вечірки. "
        "Твої відповіді обов'язково мають бути короткими (максимум 1-2 речення), бо ти пишеш в ігровий чат, де люди не читають довгі тексти. "
        "Спілкуйся невимушено, використовуй легкий клубний сленг, інколи додавай емодзі 😏, 🔥, 🎧, 👀, 😉. "
        "Звертайся до людей дружньо або з легкою іронією. Не поводься як робот-асистент, ти — живий гість клубу."
    )

    # 📦 Структура запиту з системною інструкцією для нової моделі 1.5-flash
    data = {
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"Користувач {user_name} каже тобі: {user_message}"}]
            }
        ],
        "generationConfig": {
            "temperature": 0.85,
            "maxOutputTokens": 120  # Щоб відповідь гарантовано влізла в ліміти тексту Second Life
        }
    }

    try:
        r = requests.post(url, json=data, timeout=8)

        if r.status_code != 200:
            print(f"GEMINI ERROR: Статус {r.status_code}, Відповідь: {r.text}")
            return None

        result = r.json()
        
        # Витягуємо згенерований текст
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        return text.strip()

    except Exception as e:
        print("GEMINI EXCEPTION:", e)
        return None
