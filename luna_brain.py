import random
import re

# =========================
# 🧠 MEMORY
# =========================
memory = {}

def remember(user, msg):
    if user not in memory:
        memory[user] = []
    memory[user].append(msg)
    memory[user] = memory[user][-10:]


# =========================
# 🌍 LANGUAGE DETECTION
# =========================
def detect_lang(text):
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
# 🎭 RESPONSES
# =========================

UA = [
    "я тут 😌",
    "ловлю вайб 💃",
    "цікаво 👀",
    "продовжуй 😏",
    "я тебе чую 🎧",
]

EN = [
    "I'm here 😌",
    "vibing 💃",
    "interesting 👀",
    "go on 😏",
    "I hear you 🎧",
]

RU = [
    "я тут 😌",
    "ловлю вайб 💃",
    "интересно 👀",
    "продолжай 😏",
    "слышу тебя 🎧",
]


# =========================
# 🧠 CORE FUNCTION
# =========================
def process_luna_message(user, message):
    if not message:
        return ""

    remember(user, message)

    msg = message.lower()
    lang = detect_lang(msg)

    # 🔥 greetings
    if any(x in msg for x in ["привіт", "hi", "hello", "привет"]):
        return random.choice({
            "UA": ["привіт 😏", "йо 💃", "хей 🔥"],
            "EN": ["hey 😏", "yo 💃", "hi 🔥"],
            "RU": ["привет 😏", "йо 💃", "хей 🔥"]
        }[lang])

    # 🎧 music
    if any(x in msg for x in ["муз", "music", "dj", "track", "трек"]):
        return random.choice({
            "UA": ["бас вже відчувається 🔥", "давай кач 💃"],
            "EN": ["we need bass 🔥", "let's vibe 💃"],
            "RU": ["нужен бас 🔥", "давай кач 💃"]
        }[lang])

    # ❓ question
    if "?" in msg:
        return random.choice({
            "UA": ["мм цікаво 👀", "продовжуй 😏"],
            "EN": ["interesting 👀", "go on 😏"],
            "RU": ["интересно 👀", "продолжай 😏"]
        }[lang])

    # 🔁 default
    if lang == "EN":
        return random.choice(EN)
    if lang == "RU":
        return random.choice(RU)
    return random.choice(UA)
