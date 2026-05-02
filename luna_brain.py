import random
import re
import time

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
    if re.search(r"[a-zA-Z]", text):
        return "EN"
    if re.search(r"[а-яА-ЯёЁ]", text):
        if "ы" in text or "э" in text:
            return "RU"
        return "UA"
    return "UA"


# ===== КОЛИ AI =====
def should_use_ai(text):
    text = text.lower()
    if "luna" in text or "луна" in text:
        return True
    if "?" in text:
        return True
    return False


# =========================
# 🎭 КАТЕГОРІЇ
# =========================

# 🇺🇦
greetings_ua = [
    "Привіт 🙂 рада тебе бачити",
    "Йо, привіт 😎 як настрій?",
    "Привіт, заходь не стій 😉",
]

how_ua = [
    "Та нормально, ловлю вайб 😏 а ти як?",
    "Все ок, музика качає 🔥",
]

music_ua = [
    "щось з басом зараз би зайшло 😏",
    "давай качнемо танцпол 💃",
]

flirt_ua = [
    "ти сьогодні підозріло цікавий 😏",
    "мені подобається як ти пишеш 😉",
]

neutral_ua = [
    "ага, зрозуміла 😉",
    "мм цікаво 🙂",
]

# 🇬🇧
greetings_en = [
    "hey 🙂 nice to see you",
    "yo 😎 what's your vibe?",
    "hi 😉 join the vibe",
]

how_en = [
    "I'm good 😏 just vibing",
    "all good, music hits 🔥",
]

music_en = [
    "we need more bass 😏",
    "let’s make it louder 💃",
]

flirt_en = [
    "you're interesting today 😏",
    "careful… I might pull you to dance 💋",
]

neutral_en = [
    "yeah 😉 got you",
    "hmm interesting 🙂",
]

# 🇷🇺
neutral_ru = [
    "ну да 😏",
    "поняла 😉",
    "интересно 🙂",
]


# ===== КНИГА =====
book_lines = []

def load_book():
    global book_lines
    try:
        with open("luna_book.txt", "r", encoding="utf-8") as f:
            book_lines = [line.strip() for line in f if line.strip()]
    except:
        book_lines = []

load_book()


# ===== ВИБІР =====
def get_fallback_response(user, message, lang):
    msg = message.lower()

    # базова відповідь
    if lang == "EN":
        if "hi" in msg:
            base = random.choice(greetings_en)
        elif "how" in msg:
            base = random.choice(how_en)
        elif "music" in msg:
            base = random.choice(music_en)
        else:
            base = random.choice(neutral_en)

        # трохи флірту (рідко)
        if random.random() < 0.15:
            base += "\n" + random.choice(flirt_en)

    elif lang == "RU":
        base = random.choice(neutral_ru)

    else:
        if "привіт" in msg:
            base = random.choice(greetings_ua)
        elif "як" in msg:
            base = random.choice(how_ua)
        elif "трек" in msg or "муз" in msg:
            base = random.choice(music_ua)
        else:
            base = random.choice(neutral_ua)

        if random.random() < 0.15:
            base += "\n" + random.choice(flirt_ua)

    # 📖 книга (ДУЖЕ ОБЕРЕЖНО)
    if book_lines and random.random() < 0.2:
        base += "\n" + random.choice(book_lines)

    return base


# ===== АТМОСФЕРА =====
def get_atmosphere_message():
    if not book_lines:
        return ""
    return random.choice(book_lines)
