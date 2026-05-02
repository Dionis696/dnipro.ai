import random
import re
import time
import requests

# ===== ПАМ'ЯТЬ =====
users = {}

def update_user_memory(user, message):
    if user not in users:
        users[user] = {"count": 0}
    users[user]["count"] += 1


# ===== ІГНОР =====
def should_ignore(text):
    if len(text) > 120:
        return True

    bad = re.findall(r"[^\w\sа-яА-ЯёЁa-zA-Z]", text)
    if len(bad) > len(text) * 0.4:
        return True

    return False


# ===== МОВА =====
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


# ===== AI TRIGGER =====
def should_use_ai(text):
    text = text.lower()
    if "luna" in text or "луна" in text:
        return True
    if "?" in text:
        return True
    return False


# =====================
# 🤖 GEMINI
# =====================
GEMINI_API_KEY = "ТУТ_ТВІЙ_API_KEY"

def ask_gemini(user_text, lang):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    prompt = f"""
You are Luna 💃 DJ in Club DNIPRO 🎧
Reply in {lang}
1-2 sentences, club vibe, emojis allowed 😏🔥💃
User: {user_text}
"""

    try:
        r = requests.post(url, json={
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }, timeout=10)

        data = r.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except:
        return None


# =====================
# 🎭 FALLBACK (ТВОЇ КАТЕГОРІЇ НЕ ТРОГАЮ)
# =====================

greetings_ua = [
    "Привіт 🙂",
    "Йо 😏",
]

how_ua = [
    "норм 🔥",
    "все ок 💃",
]

neutral_ua = [
    "ага 😏",
    "мм 🙂",
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


def get_fallback_response(user, message, lang):
    msg = message.lower()

    if "привіт" in msg:
        base = random.choice(greetings_ua)
    elif "як" in msg:
        base = random.choice(how_ua)
    else:
        base = random.choice(neutral_ua)

    if book_lines and random.random() < 0.3:
        base += "\n" + random.choice(book_lines)

    return base


# ===== ATMOSPHERE =====
def get_atmosphere_message():
    if not book_lines:
        return ""
    return random.choice(book_lines)
