import os
import requests

# Зчитуємо ключ із секретних змінних оточення Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

def ask_gemini(user_name, user_message):
    # 🎯 ДІАГНОСТИКА 1: Перевірка самого виклику функції
    print(f"🚀 [LUNA_AI] Функція ask_gemini УСПІШНО ВИКЛИКАНА для користувача: '{user_name}'")
    print(f"💬 [LUNA_AI] Вхідний текст: '{user_message}'")

    # 🎯 ДІАГНОСТИКА 2: Перевірка наявності API-ключа в системі Render
    if not GEMINI_API_KEY:
        print("❌ [LUNA_AI] ПОМИЛКА: API-ключ НЕ знайдено в змінних оточення Render! Перевірь вкладку Environment.")
        return None
    else:
        # Показуємо перші 4 і останні 4 символи ключа для безпеки, щоб переконатися, що він не порожній
        masked_key = f"{GEMINI_API_KEY[:4]}...{GEMINI_API_KEY[-4:]}" if len(GEMINI_API_KEY) > 8 else "ЗАКОРОТКИЙ_КЛЮЧ"
        print(f"🔑 [LUNA_AI] Ключ знайдено та зчитано успішно: {masked_key}")

    # Використовуємо швидку, стабільну та безкоштовну модель gemini-1.5-flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    # 🎭 Задаємо характер Луни.
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
        print("📡 [LUNA_AI] Надсилаю POST-запит до Google Gemini API...")
        
        # Надсилаємо POST запит з таймаутом 7 секунд
        r = requests.post(url, json=data, timeout=7)

        # 🎯 ДІАГНОСТИКА 3: Перевірка відповіді сервера Google
        print(f"📊 [LUNA_AI] Google повернув HTTP Статус: {r.status_code}")

        if r.status_code != 200:
            print(f"❌ [LUNA_AI] ГЕМІНІ ВІДХИЛИВ ЗАПИТ! Код: {r.status_code} | Текст помилки: {r.text}")
            return None

        result = r.json()
        
        # Парсимо текст відповіді
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        
        print(f"✨ [LUNA_AI] Текст від Gemini успішно отримано!")
        return text.strip()

    except Exception as e:
        print("💥 [LUNA_AI] КРИТИЧНА ПОМИЛКА під час запиту до Gemini:", str(e))
        return None
