import random
import re

# ===== MEMORY =====
users = {}

def update_user_memory(user, message):
    if user not in users:
        users[user] = {"count": 0}
    users[user]["count"] += 1


# ===== IGNORE =====
def should_ignore(text):
    if len(text) > 150:
        return True

    bad = re.findall(r"[^\w\sа-яА-ЯёЁa-zA-Z]", text)
    if len(bad) > len(text) * 0.5:
        return True

    return False


# ===== LANGUAGE FIX (СТАБІЛЬНИЙ) =====
def detect_language(text):
    text = text.lower()

    ua = len(re.findall(r"[а-щьюяєіїґ]", text))
    ru = len(re.findall(r"[а-яё]", text))
    en = len(re.findall(r"[a-z]", text))

    if ua >= ru and ua > 0:
        return "UA"
    if ru > ua:
        return "RU"
    if en > 0:
        return "EN"

    return "UA"


# ===== AI TRIGGER (СТАБІЛЬНИЙ) =====
def should_use_ai(text):
    t = text.lower()

    if "luna" in t or "луна" in t:
        return True

    # короткі фрази → AI (щоб не було тупих fallback)
    if len(t) < 20:
        return True

    return False


# =========================
# 🎭 UA
# =========================

greetings_ua = [
    "Привіт 🙂 я тут 💃",
    "Йо 😏 як настрій?",
    "Хей 🔥 заходь у ритм",
]

how_ua = [
    "Норм 😏 музика качає 🔥",
    "Все ок 💃 ти як?",
]

music_ua = [
    "давай баси 🔥😏",
    "цей танцпол чекає 💃",
]

flirt_ua = [
    "ти цікавий 😏",
    "ловиш мій вайб 💃🔥",
]

neutral_ua = [
    "ага 😏",
    "зрозуміла 💃",
    "мм 🙂",
]


# =========================
# EN
# =========================

greetings_en = ["hey 😏", "yo 💃"]
how_en = ["good 🔥", "all vibe 😏"]
music_en = ["bass time 🔥", "let’s dance 💃"]
neutral_en = ["yeah 😏", "hmm 🙂"]


# =========================
# RU
# =========================

neutral_ru = ["ну да 😏", "поняла 💃", "ок 🙂"]


# ===== BOOK =====
book_lines = []

def load_book():
    global book_lines
    try:
        with open("luna_book.txt", "r", encoding="utf-8") as f:
            book_lines = [l.strip() for l in f if l.strip()]
    except:
        book_lines = []

load_book()


# ===== RESPONSE =====
def get_fallback_response(user, message, lang):
    msg = message.lower()

    if lang == "EN":
        base = random.choice(greetings_en)

    elif lang == "RU":
        base = random.choice(neutral_ru)

    else:
        if "привіт" in msg:
            base = random.choice(greetings_ua)
        elif "як" in msg:
            base = random.choice(how_ua)
        elif "муз" in msg:
            base = random.choice(music_ua)
        else:
            base = random.choice(neutral_ua)

        if random.random() < 0.35:
            base += "\n" + random.choice(flirt_ua)

    if book_lines and random.random() < 0.4:
        base += "\n" + random.choice(book_lines)

    return base


# ===== ATMOSPHERE =====
def get_atmosphere_message():
    if not book_lines:
        return ""
    return random.choice(book_lines)
