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
    "hi there 😉 don't just stand, join in",
]

how_en = [
    "I'm good 😏 just vibing, you?",
    "all good, music hits 🔥",
]

music_en = [
    "we need something with bass 😏",
    "let’s make the floor move 💃",
]

flirt_en = [
    "you're kinda interesting today 😏",
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

    # ===== ВИБІР БАЗИ =====
    if lang == "EN":
        if "hi" in msg:
            base = random.choice(greetings_en)
        elif "how" in msg:
            base = random.choice(how_en)
        elif "music" in msg or "track" in msg:
            base = random.choice(music_en)
        else:
            base = random.choice(neutral_en)

        if random.random() < 0.3:
            base += "\n" + random.choice(flirt_en)

    elif lang == "RU":
        base = random.choice(neutral_ru)

    else:  # UA
        if "привіт" in msg:
            base = random.choice(greetings_ua)
        elif "як" in msg:
            base = random.choice(how_ua)
        elif "трек" in msg or "муз" in msg:
            base = random.choice(music_ua)
        else:
            base = random.choice(neutral_ua)

        if random.random() < 0.3:
            base += "\n" + random.choice(flirt_ua)

    # ===== КНИГА (мікс) =====
    if book_lines and random.random() < 0.4:
        lines = random.randint(1, 2)
        base += "\n" + "\n".join(random.sample(book_lines, min(lines, len(book_lines))))

    return base


# ===== АТМОСФЕРА =====
def get_atmosphere_message():
    if not book_lines:
        return ""

    return "\n".join(random.sample(book_lines, random.randint(1, 2)))
