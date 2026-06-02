import os
import requests

# Зчитуємо ключ із секретних змінних оточення Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

def ask_gemini(user_name, user_message):
    # Якщо ключ забули додати в Render, виводимо помилку в логи і повертаємо None (включиться фолбек)
    if not GEMINI_API_KEY:
        print("GEMINI AI ERROR: API Ключ не знайдено в системних змінних Render (GEMINI_API_KEY)!")
        return None

    # Використовуємо швидку, стабільну та безкоштовну модель gemini-1.5-flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    # 🎭 Задаємо характер Луни. Вона знає де вона перебуває і як себе поводити.
    system_instruction = (
        "Ти — Луна, зухвала, розумна та неймовірно харизматична тусовщиця нічного клубу 'Dnipro Club' у Second Life. "
        "Ти обожнюєш електронну музику, нічний вайб, глибокі баси та гучні вечірки. "
        "Твої відповіді обов'язково мають бути короткими (максимум 1-2 речення), бо ти пишеш в ігровий чат, де люди не читають довгі тексти. "
        "Спілкуйся невимушено, використовуй легкий клубний сленг, інколи додавай емодзі 😏, 🔥, 🎧, 👀, 😉. "
        "Звертайся до людей дружньо або з легкою іронією. Не поводься як робот-асистент чи ШІ, ти — живий гість клубу."
    )

    # Структура JSON запиту відповідно до офіційної документації Google API v1beta
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
            "maxOutputTokens": 120  # Гарантує, що відповідь не обріжеться лімітами чату Second Life
        }
    }

    try:
        # Надсилаємо POST запит з таймаутом, щоб гра не зависала, якщо Google довго думає
        r = requests.post(url, json=data, timeout=7)

        if r.status_code != 200:
            print(f"GEMINI API БАГ: Статус {r.status_code}, Текст: {r.text}")
            return None

        result = r.json()
        
        # Парсимо текст відповіді
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        return text.strip()

    except Exception as e:
        print("GEMINI EXCEPTION:", e)
        return None
