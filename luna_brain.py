import random
import re
import time
import requests

# =========================
# 🧠 MEMORY / ANTI REPEAT
# =========================
last_reply_by_user = {}

def avoid_repeat(user, reply):
    last = last_reply_by_user.get(user)

    if last == reply:
        return None

    last_reply_by_user[user] = reply
    return reply


# =========================
# ⚙️ CONFIG
# =========================
GEMINI_API_KEY = "ТУТ_ТВІЙ_API_KEY"
COOLDOWN = 5
last_ai_time = 0


# =========================
# 🌍 LANGUAGE DETECTOR (СТАБІЛЬНИЙ)
# =========================
def detect_language(text):
    text = text.lower()

    ua = len(re.findall(r"[а-щьюяєіїґ]", text))
    ru = len(re.findall(r"[а-яё]", text))
    en = len(re.findall(r"[a-z]", text))

    if ua >= ru:
        return "UA"
    if ru > ua:
        return "RU"
    return "UA"


# =========================
# 🧼 SAFE TEXT FIX (ANTI Uxxxx + EMOJI)
# =========================
def fix_text(text):
    if not text:
        return "..."

    text = str(text)

    # основні баги які ти ловив
    text = text.replace("u0430", "а")
    text = text.replace("u043d", "н")
    text = text.replace("u0438", "и")
    text = text.replace("ud83dude0f", "😏")
    text = text.replace("ud83dudc83", "💃")

    return text


# =========================
# 🤖 GEMINI AI
# =========================
def ask_gemini(message, lang):
    global last_ai_time

    if time.time() - last_ai_time < COOLDOWN:
        return None

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    prompt = f"""
You are Luna 💃 DJ in Club DNIPRO 🎧

RULES:
- ONLY {lang}
- NO mixing languages
- NEVER repeat previous answer
- 1-2 short sentences
- club vibe, emojis 😏🔥💃
"""

    try:
        r = requests.post(url, json={
            "contents": [{
                "parts": [{
                    "text": prompt + "\nUser: " + message
                }]
            }]
        }, timeout=10)

        data = r.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]

        last_ai_time = time.time()

        return text

    except:
        return None


# =========================
# 🎭 FALLBACK (твій стиль)
# =========================
greetings_ua = [
    "Привіт 😏",
    "Йо 💃",
    "Хей 🔥",
    "О, ти тут 😉"
]

neutral_ua = [
    "ага 😏",
    "мм 🙂",
    "зрозуміла 💃"
]

book_lines = []

def load_book():
    global book_lines
    try:
        with open("luna_book.txt", "r", encoding="utf-8") as f:
            book_lines = [l.strip() for l in f if l.strip()]
    except:
        book_lines = []

load_book()


def fallback_response(lang):
    if lang == "UA":
        base = random.choice(greetings_ua + neutral_ua)

        if book_lines and random.random() < 0.3:
            base += "\n" + random.choice(book_lines)

        return base

    return "ok 😏"


# =========================
# 🧠 MAIN BRAIN (1 МОЗОК)
# =========================
def process_luna_message(user, message):
    if not message:
        return "..."

    lang = detect_language(message)

    # 1) AI
    ai = ask_gemini(message, lang)
    if ai:
        cleaned = fix_text(ai)
        checked = avoid_repeat(user, cleaned)
        if checked:
            return checked

    # 2) fallback
    fb = fix_text(fallback_response(lang))
    checked = avoid_repeat(user, fb)

    if checked:
        return checked

    return "..."
