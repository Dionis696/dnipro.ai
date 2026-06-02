from google import genai
from google.genai import types

# Твій "AQ..." токен
TOKEN = "AQ.Ab8RN6J1e83tncvgZfHMVcXkeZ93DFq1Dt4YS3f1TLGdDrdfEQ"

def ask_gemini(user_name, user_message):
    print(f"🚀 [LUNA_AI] Спроба виклику через Bearer-токен для: '{user_name}'", flush=True)
    
    # Використовуємо токен як авторизацію
    client = genai.Client(
        http_options={'headers': {'Authorization': f'Bearer {TOKEN}'}}
    )

    system_instruction = "Ти — Луна з Dnipro Club. Відповідай коротко (1-2 речення), сленгово, з емодзі."

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
        print(f"💥 ПОМИЛКА авторизації: {e}", flush=True)
        return None
