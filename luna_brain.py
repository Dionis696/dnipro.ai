import random
import time

# =========================
# 🌍 ФРАЗИ
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
    "ніч сьогодні цікава"
]

how_ru = [
    "всё нормально 🙂",
    "атмосфера кайф",
    "всё ок 😉",
]

how_en = [
    "I'm good 🙂",
    "just vibing here",
    "all good 😉",
]

idle_lines = [
    "в клубі тихо сьогодні",
    "DJ щось задумав 😏",
    "дивний вайб сьогодні",
    "де всі поділись?",
    "ніч жива"
]

# =========================
# 🧠 ПАМʼЯТЬ
# =========================

recent_replies = []

MAX_RECENT = 10

last_message_time = 0
COOLDOWN = 2

# коротка памʼять діалогу
active_users = {}

DIALOG_MEMORY = 30

# =========================
# 🌍 МОВА
# =========================

def detect_lang(msg):

    msg = msg.lower()

    if any(x in msg for x in [
        "hello", "hi", "how are", "why"
    ]):
        return "EN"

    if any(x in msg for x in [
        "привет", "как дела", "почему"
    ]):
        return "RU"

    return "UA"

# =========================
# 🧠 SAFE RANDOM
# =========================

def safe_random(lines):

    global recent_replies

    available = [
        x for x in lines
        if x not in recent_replies
    ]

    if not available:
        recent_replies = []
        available = lines

    choice = random.choice(available)

    recent_replies.append(choice)

    if len(recent_replies) > MAX_RECENT:
        recent_replies.pop(0)

    return choice

# =========================
# 🎯 MAIN
# =========================

def process_luna_message(user, msg):

    global last_message_time
    global active_users

    now = time.time()

    # антиспам
    if now - last_message_time < COOLDOWN:
        return ""

    if not msg:
        return ""

    msg_low = msg.lower()

    lang = detect_lang(msg_low)

    # =========================
    # 🎯 ТРИГЕР
    # =========================

    direct_trigger = (
        "luna" in msg_low or
        "луна" in msg_low
    )

    # якщо був діалог
    remembered = False

    if user in active_users:
        if now - active_users[user] < DIALOG_MEMORY:
            remembered = True

    # =========================
    # 👋 ПРИВІТ
    # =========================

    if (
        "прив" in msg_low or
        "hello" in msg_low or
        "hi" in msg_low
    ) and (direct_trigger or remembered):

        active_users[user] = now
        last_message_time = now

        if lang == "RU":
            return safe_random(hello_ru)

        if lang == "EN":
            return safe_random(hello_en)

        return safe_random(hello_ua)

    # =========================
    # ❓ ЯК СПРАВИ
    # =========================

    if (
        "як" in msg_low or
        "как" in msg_low or
        "how" in msg_low
    ) and (direct_trigger or remembered):

        active_users[user] = now
        last_message_time = now

        if lang == "RU":
            return safe_random(how_ru)

        if lang == "EN":
            return safe_random(how_en)

        return safe_random(how_ua)

    # =========================
    # 🌙 ПРОСТО ЗГАДАЛИ LUNA
    # =========================

    if direct_trigger:

        active_users[user] = now
        last_message_time = now

        return safe_random(idle_lines)

    # =========================
    # 🎲 РІДКІ РЕАКЦІЇ
    # =========================

    if random.random() < 0.03:

        last_message_time = now

        return safe_random(idle_lines)

    return ""
