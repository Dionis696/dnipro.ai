import random
import re

# =========================
# 🧠 MEMORY
# =========================
user_memory = {}

def remember(user, message):
    if user not in user_memory:
        user_memory[user] = []
    user_memory[user].append(message)
    user_memory[user] = user_memory[user][-5:]


# =========================
# 🌍 LANGUAGE DETECTION
# =========================
def detect_language(text):
    text = text.lower()

    ua = len(re.findall(r"[а-щьюяєіїґ]", text))
    ru = len(re.findall(r"[а-яё]", text))
    en = len(re.findall(r"[a-z]", text))

    if en > ua and en > ru:
        return "EN"
    if ru > ua and ru > en:
        return "RU"
    return "UA"


# =========================
# 🎭 LUNA PERSONALITY BANK
# =========================

UA = {
    "greet": ["привіт 😏", "йо 💃", "хей 🔥", "о, ти тут 😉"],
    "music": ["цей бас зараз би зайшов 🔥", "музика вже в повітрі 🎧", "давай качати 💃"],
    "react": ["цікаво 👀", "мм… відчуваю тебе 😏", "ще щось скажеш? 🔥"],
    "default": ["я тут 😌", "слухаю тебе 💃", "вайб ловлю 🔥"]
}

EN = {
    "greet": ["hey 😏", "yo 💃", "hi 🔥"],
    "music": ["we need bass 🔥", "music is alive 🎧", "let's vibe 💃"],
    "react": ["interesting 👀", "I feel that 😏", "go on 🔥"],
    "default": ["I'm here 😌", "listening 💃", "vibing 🔥"]
}

RU = {
    "greet": ["привет 😏", "йо 💃", "хей 🔥"],
    "music": ["нужен бас 🔥", "музыка жива 🎧", "давай кач 💃"],
    "react": ["интересно 👀", "чувствую вайб 😏", "продолжай 🔥"],
    "default": ["я тут 😌", "слушаю 💃", "ловлю вайб 🔥"]
}


# =========================
# 🧠 CORE ENGINE
# =========================
def pick(lang, key):
    if lang == "EN":
        return random.choice(EN[key])
    if lang == "RU":
        return random.choice(RU[key])
    return random.choice(UA[key])


def process_luna_message(user, message):
    if not message:
        return "..."

    remember(user, message)

    msg = message.lower()
    lang = detect_language(msg)

    # ===== GREET =====
    if any(x in msg for x in ["привіт", "hi", "hello", "привет"]):
        return pick(lang, "greet")

    # ===== MUSIC =====
    if any(x in msg for x in ["муз", "music", "dj", "трек"]):
        return pick(lang, "music")

    # ===== QUESTION =====
    if "?" in msg:
        return pick(lang, "react")

    # ===== DEFAULT =====
    return pick(lang, "default")
