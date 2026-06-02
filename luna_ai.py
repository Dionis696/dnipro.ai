import os
import requests

# 🔑 Твій секретний ключ від Google Gemini (залишай у лапках):
GEMINI_API_KEY = "AQ.Ab8RN6I2meJRGR0sriJtOJsFjplTxeg9mB-g4CV_OMpSMyaLQQ"  # <-- ОБОВ'ЯЗКОВО переконайся, що тут твій ПОВНИЙ ключ

def ask_gemini(user_name, user_message):
    # 🎯 ДІАГНОСТИКА 1: Перевірка самого виклику функції
    print(f"🚀 [LUNA_AI] Функція ask_gemini УСПІШНО ВИКЛИКАНА для користувача: '{user_name}'", flush=True)
    print(f"💬 [LUNA_AI] Вхідний текст: '{user_message}'", flush=True)

    # 🎯 ДІАГНОСТИКА 2: Перевірка ключа всередині коду
    if not GEMINI_API_KEY or "ВСТАВ_СЮДИ" in GEMINI_API_KEY:
        print("❌ [LUNA_AI] ПОМИЛКА: Ключ порожній або не замінений у коді luna_ai.py!", flush=True)
        return None
    else:
        masked_key = f"{GEMINI_API_KEY[:4]}...{GEMINI_API_KEY[-4:]}" if len(GEMINI_API_KEY) > 8 else "ЗАКОРОТКИЙ_КЛЮЧ"
        print(f"🔑 [LUNA_AI] Ключ зчитано прямо з коду файлу: {masked_key}", flush=True)

    # Базовий стабільний URL Google API v1
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    # 🎭 Характер Луни (зашиваємо як Context безпосередньо в запит, щоб обійти баги Google JSON)
    context_prompt = (
        "CONTEXT: Ти — Луна, зухвала, розумна та харизматична тусовщиця нічного клубу 'Dnipro Club' у Second Life. "
        "Ти обожнюєш електронну музику, нічний вайб, глибокі баси та гучні вечірки. "
        "Твої відповіді обов'язково мають бути короткими (максимум 1-2 речення), бо ти пишеш в ігровий чат. "
        "Спілкуйся невимушено, використовуй легкий клубний сленг, додавай емодзі 😏, 🔥, 🎧, 👀, 😉. "
        "Звертайся до людей дружньо або з легкою іронією. Ти живий гість клубу, а не ШІ.\n\n"
        f"Користувач {user_name} каже тобі: {user_message}\n"
        "Твоя коротка відповідь від імені Луни:"
    )

    # 🛠️ НАДНАДІЙНИЙ JSON: Тільки стандартне поле contents, яке працює всюди
    data = {
        "contents": [
            {
                "parts": [{"text": context_prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.9,
            "maxOutputTokens": 120
        }
    }

    try:
        print("📡 [LUNA_AI] Надсилаю супер-надійний POST-запит до Google Gemini API...", flush=True)
        
        # Надсилаємо POST запит з таймаутом 7 секунд
        r = requests.post(url, json=data, timeout=7)

        # 🎯 ДІАГНОСТИКА 3: Перевірка відповіді сервера Google
        print(f"📊 [LUNA_AI] Google повернув HTTP Статус: {r.status_code}", flush=True)

        if r.status_code != 200:
            print(f"❌ [LUNA_AI] ГЕМІНІ ВІДХИЛИВ ЗАПИТ! Код: {r.status_code} | Текст помилки: {r.text}", flush=True)
            return None

        result = r.json()
        
        # Парсимо текст відповіді
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        
        print(f"✨ [LUNA_AI] Текст від Gemini успішно отримано!", flush=True)
        return text.strip()

    except Exception as e:
        print(f"💥 [LUNA_AI] КРИТИЧНА ПОМИЛКА під час запиту до Gemini: {str(e)}", flush=True)
        return None
