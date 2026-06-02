import os
from google import genai
from google.genai import types

# 🔑 Твій ключ
GEMINI_API_KEY = "AQ.Ab8RN6IUXWDUcB3nwmArcwI4JbTy1wuDGL4DIKdhiLKFs9IlNw"

# Ініціалізація з явною версією API (v1beta потрібна для SDK)
client = genai.Client(api_key=GEMINI_API_KEY, http_options={'api_version': 'v1beta'})

def ask_gemini(user_name, user_message):
    print(f"🚀 [LUNA_AI] Виклик Gemini для: '{user_name}'", flush=True)

    system_instruction = (
        "Ти — Луна, зухвала, розумна та харизматична тусовщиця нічного клубу 'Dnipro Club' у Second Life. "
        "Ти обожнюєш електронну музику та гучні вечірки. Відповідай коротко (1-2 речення), сленгово, з емодзі 😏, 🔥, 🎧."
    )

    try:
        # Використовуємо 'models/gemini-1.5-flash' як повний шлях
        response = client.models.generate_content(
            model='models/gemini-1.5-flash',
            contents=f"Користувач {user_name} каже: {user_message}",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.85,
            )
        )
        
        print("✨ [LUNA_AI] Текст успішно отримано!", flush=True)
        return response.text.strip()

    except Exception as e:
        print(f"💥 [LUNA_AI] ПОМИЛКА: {str(e)}", flush=True)
        return None
