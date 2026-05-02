import random
import re

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


# ===== МОВА (FIXED, але м’яко) =====
def detect_language(text):
    text = text.lower()

    ua_chars = len(re.findall(r"[а-щьюяєіїґ]", text))
    ru_chars = len(re.findall(r"[а-яё]", text))
    en_chars = len(re.findall(r"[a-z]", text))

    # даємо пріоритет кирилиці
    if ua_chars > 0 and ua_chars >= ru_chars:
        return "UA"
    if ru_chars > ua_chars and ru_chars > 0:
        return "RU"
    if en_chars > 0 and ua_chars == 0:
        return "EN"

    return "UA"


# ===== AI TRIGGER (НЕ ЛАМАТИ ЛОГІКУ) =====
def should_use_ai(text):
    text = text.lower()

    if "luna" in text or "луна" in text:
        return True

    # тільки якщо реально питання
    if "?" in text:
        return True

    return False


# =========================
# 🎭 ТВОЇ КАТЕГОРІЇ (ЗБЕРЕЖЕНО 100%)
# =========================

greetings_ua = [
    "Привіт 🙂 рада тебе бачити",
    "Йо, привіт 😎 як настрій?",
    "Привіт, заходь не стій 😉",
    "О, новенький? вітаю в клубі 😏",
    "Хей, привіт 💃 давно не бачилися",
]

how_ua = [
    "Та нормально, ловлю вайб 😏 а ти як?",
    "Все ок, музика качає 🔥",
    "Все ок, трохи музики і настрій топ 🔥",
    "Живу, кайфую 😉",
    "Та як завжди — музика і настрій 😎",
]

music_ua = [
    "щось з басом зараз би зайшло 😏",
    "давай качнемо танцпол 💃",
    "мм щось з 2000-х зараз би зайшло 😏",
    "може щось танцювальне включимо? 💃",
    "я б зараз щось з басом поставила 🔥",
    "цей трек норм, але можна ще качнути 😉",
]

flirt_ua = [
    "ти сьогодні підозріло цікавий 😏",
    "мені подобається як ти пишеш 😉",
    "обережно… я можу спокусити на танець 💋",
    "не дивись так… я ж теж людина 😄",
]

neutral_ua = [
    "ага, зрозуміла 😉",
    "мм цікаво 🙂",
    "ну ти даєш 😄",
    "є щось в цьому 😏",
]


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


# ===== ВІДПОВІДЬ =====
def get_fallback_response(user, message, lang):
    msg = message.lower()

    if lang == "EN":
        if "hi" in msg:
            base = random.choice(greetings_en)
        elif "how" in msg:
            base = random.choice(how_en)
        elif "music" in msg:
            base = random.choice(music_en)
        else:
            base = random.choice(neutral_en)

        if random.random() < 0.3:
            base += "\n" + random.choice(flirt_en)

    elif lang == "RU":
        base = random.choice(neutral_ru)

    else:
        if "привіт" in msg:
            base = random.choice(greetings_ua)
        elif "як" in msg:
            base = random.choice(how_ua)
        elif "муз" in msg or "трек" in msg:
            base = random.choice(music_ua)
        else:
            base = random.choice(neutral_ua)

        if random.random() < 0.3:
            base += "\n" + random.choice(flirt_ua)

    # 🎧 атмосфера (твоя книга НЕ втрачена)
    if book_lines and random.random() < 0.4:
        base += "\n" + random.choice(book_lines)

    return base


# ===== АТМОСФЕРА =====
def get_atmosphere_message():
    if not book_lines:
        return ""
    return random.choice(book_lines)
