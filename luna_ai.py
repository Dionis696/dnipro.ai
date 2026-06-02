import os
from google import genai
from google.genai import types

# Клієнт автоматично шукає ключ у змінній середовища GOOGLE_API_KEY
client = genai.Client()

def ask_gemini(user_name, user_message):
    print(f"🚀 [LUNA_AI] Виклик Gemini для: '{user_name}'", flush=True)

    system_instruction = (
        "Ти — Луна, зухвала та харизматична тусовщиця 'Dnipro Club'. "
        "Відповідай коротко (1-2 речення), сленгово, з емодзі 😏, 🔥, 🎧."
    )

    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=f"Користувач {user_name} каже: {user_message}",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.85,
            )
        )
        return response.text.strip()
    except Exception as e:
        print(f"💥 [LUNA_AI] ПОМИЛКА: {str(e)}", flush=True)
        return None
