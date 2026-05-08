import random
import time

# =========================
# 🧠 MEMORY
# =========================

active_dialogs = {}
DIALOG_TIMEOUT = 180  # 3 хв

# =========================
# 💬 RESPONSES
# =========================

greetings = {
    "UA": ["привіт 🙂", "рада тебе бачити", "хей 😉"],
    "RU": ["привет 🙂", "рада тебя видеть", "хей 😉"],
    "EN": ["hey 🙂", "nice to see you", "hello 😉"]
}

how_are_you = {
    "UA": ["та нормально 🙂", "ловлю вайб", "все ок 😉"],
    "RU": ["всё нормально 🙂", "ловлю вайб", "всё ок 😉"],
    "EN": ["I'm good 🙂", "just vibing", "all good 😉"]
}

silence = {
    "UA": ["тиша якась сьогодні 😏", "в клубі затихло", "дивний вайб"],
    "RU": ["тишина сегодня 😏", "в клубе тихо", "странный вайб"],
    "EN": ["too quiet here 😏", "club feels calm", "strange vibe"]
}

dj_topic = {
    "UA": ["DJ щось задумав 😏", "зараз буде рух", "відчуваю двіж"],
    "RU": ["DJ что-то задумал 😏", "сейчас будет движ", "чувствую разрыв"],
    "EN": ["DJ planning something 😏", "big drop coming", "feeling the vibe"]
}

idle_lines = {
    "UA": ["ніч жива", "атмосфера цікава", "дивний вечір"],
    "RU": ["ночь живая", "интересная атмосфера", "странный вечер"],
    "EN": ["night feels alive", "interesting vibe", "odd night"]
}

# =========================
# 🌍 LANGUAGE DETECTION
# =========================

def detect_lang(msg):
    msg = msg.lower()

    if any(x in msg for x in ["hello", "how are", "why", "what"]):
        return "EN"

    if any(x in msg for x in ["привет", "как", "почему", "что"]):
        return "RU"

    return "UA"

# =========================
# 🧠 TOPIC
# =========================

def detect_topic(msg):
    msg = msg.lower()

    if "dj" in msg or "муз" in msg:
        return "dj"

    if "тиша" in msg or "quiet" in msg:
        return "silence"

    if "як" in msg or "как" in msg or "how" in msg:
        return "how"

    if "прив" in msg or "hello" in msg:
        return "greeting"

    return "default"

# =========================
# 🎯 MAIN
# =========================

def process_luna_message(user, msg):

    now = time.time()

    if not msg:
        return ""

    msg_low = msg.lower()

    topic = detect_topic(msg_low)
    detected_lang = detect_lang(msg_low)

    # =========================
    # 🧠 ACTIVE DIALOG
    # =========================

    dialog = active_dialogs.get(user)

    if dialog:
        if now - dialog["time"] > DIALOG_TIMEOUT:
            active_dialogs.pop(user)
            dialog = None

    # =========================
    # 🔥 START OR CONTINUE DIALOG
    # =========================

    if "luna" in msg_low or "луна" in msg_low or dialog:

        # якщо новий діалог → фіксуємо мову
        if not dialog:
            active_dialogs[user] = {
                "time": now,
                "lang": detected_lang,
                "topic": topic
            }
            dialog = active_dialogs[user]

        # якщо вже є → НЕ міняємо мову (LANG LOCK)
        lang = dialog["lang"]

        dialog["time"] = now
        dialog["topic"] = topic

        # =========================
        # 🎯 RESPONSES BY TOPIC
        # =========================

        if topic == "dj":
            return random.choice(dj_topic[lang])

        if topic == "silence":
            return random.choice(silence[lang])

        if topic == "greeting":
            return random.choice(greetings[lang])

        if topic == "how":
            return random.choice(how_are_you[lang])

        return random.choice(idle_lines[lang])

    # =========================
    # 🤫 RANDOM REACTION
    # =========================

    if random.random() < 0.02:
        return random.choice(idle_lines["UA"])

    return ""
