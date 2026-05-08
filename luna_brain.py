import random
import time

# =========================
# 📚 ФРАЗИ
# =========================

hello_ua = [
    "привіт 🙂",
    "рада тебе бачити",
    "хей 😉",
    "привіт, як настрій?",
]

hello_ru = [
    "привет 🙂",
    "рада тебя видеть",
    "хей 😉",
]

hello_en = [
    "hey 🙂",
    "nice to see you",
    "hello 😉",
]

how_ua = [
    "та нормально 🙂",
    "ловлю вайб у клубі",
    "все ок 😉",
]

how_ru = [
    "всё нормально 🙂",
    "кайфую от атмосферы",
]

how_en = [
    "I'm good 🙂",
    "just vibing here",
]

fun_lines = [
    "в клубі сьогодні дивна тиша",
    "DJ явно щось задумав 😏",
    "музика сьогодні качає",
    "де всі поділись?",
]

# =========================
# 🧠 ПАМ'ЯТЬ
# =========================

last_time = 0
COOLDOWN = 2

# =========================
# 🌍 МОВА
# =========================

def detect_lang(msg):
    msg = msg.lower()

    if any(x in msg for x in ["hello", "hi", "why"]):
        return "EN"

    if any(x in msg for x in ["привет", "как", "дела"]):
        return "RU"

    return "UA"

# =========================
# 💬 ЛОГІКА
# =========================

def process_luna_message(user, msg):
    global last_time

    now = time.time()

    if now - last_time < COOLDOWN:
        return ""

    if not msg:
        return ""

    msg_low = msg.lower()

    lang = detect_lang(msg_low)

    # =========================
    # 👋 ПРИВІТАННЯ
    # =========================

    if "прив" in msg_low or "hello" in msg_low or "hi" in msg_low:

        last_time = now

        if lang == "RU":
            return random.choice(hello_ru)

        if lang == "EN":
            return random.choice(hello_en)

        return random.choice(hello_ua)

    # =========================
    # ❓ ЯК СПРАВИ
    # =========================

    if (
        "як справ" in msg_low or
        "как дела" in msg_low or
        "how are" in msg_low
    ):

        last_time = now

        if lang == "RU":
            return random.choice(how_ru)

        if lang == "EN":
            return random.choice(how_en)

        return random.choice(how_ua)

    # =========================
    # 🌙 ЗГАДАЛИ LUNA
    # =========================

    if "luna" in msg_low or "луна" in msg_low:

        last_time = now
        return random.choice(fun_lines)

    # =========================
    # 🎲 ІНКОЛИ РЕАКЦІЯ
    # =========================

    if random.random() < 0.05:
        last_time = now
        return random.choice(fun_lines)

    return ""
