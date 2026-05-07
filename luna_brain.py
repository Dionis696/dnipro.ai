import random
import re
import time

from luna_memory import learn_from_chat, get_random_memory, get_user_style

# =========================
# 📚 BOOK
# =========================

book_lines = []

def load_book():
    global book_lines
    try:
        with open("luna_book_big.txt", "r", encoding="utf-8") as f:
            book_lines = [x.strip() for x in f if x.strip()]
    except:
        book_lines = []

load_book()

# =========================
# 🎧 DJ LIST
# =========================

dj_list = [
    "DJ дядя Жора",
    "DJ Tomas",
    "DJ Demnius"
]

# =========================
# 🧠 STATE
# =========================

last_reply_time = 0
COOLDOWN = 4

luna_state = {
    "mode": "normal",   # normal / peak / idle
    "last_activity": time.time()
}

# =========================
# 🚫 FILTER
# =========================

def should_ignore(msg):
    if len(msg) > 200:
        return True
    return False


def detect_lang(msg):
    if re.search(r"[a-zA-Z]", msg):
        return "EN"
    if re.search(r"[а-яА-Я]", msg):
        return "UA"
    return "UA"


# =========================
# 🔥 PEAK DETECTOR
# =========================

def is_peak(msg):
    triggers = ["DJ", "Club", "☆", "★", "ıllı", "▓", "✪"]
    return any(t in msg for t in triggers)


def update_mode(msg):
    if is_peak(msg):
        luna_state["mode"] = "peak"
    else:
        if time.time() - luna_state["last_activity"] > 600:
            luna_state["mode"] = "idle"
        else:
            luna_state["mode"] = "normal"


# =========================
# 💬 RESPONSE
# =========================

def pick_line():
    if not book_lines:
        return "..."

    return random.choice(book_lines)


def maybe_add_dj(text):
    if random.random() < 0.3:
        text += " " + random.choice(dj_list)
    return text


# =========================
# 💤 IDLE MODE
# =========================

idle_lines = [
    "в клубі трохи тихо сьогодні",
    "де всі пропали?",
    "DJ мовчить сьогодні",
    "давайте трохи руху",
    "цей вечір спокійний"
]


def idle_reply():
    return random.choice(idle_lines)


# =========================
# 🧠 MAIN ENGINE
# =========================

def process_luna_message(user, msg):
    global last_reply_time

    now = time.time()

    # cooldown
    if now - last_reply_time < COOLDOWN:
        return ""

    if should_ignore(msg):
        return ""

    # memory learning
    learn_from_chat(user, msg)

    update_mode(msg)
    luna_state["last_activity"] = now

    lang = detect_lang(msg)

    # ❌ якщо не звернулись — мовчить (важливо як ти хотів)
    if "luna" not in msg.lower() and "луна" not in msg.lower():
        if luna_state["mode"] == "idle" and random.random() < 0.2:
            last_reply_time = now
            return idle_reply()
        return ""

    # 🔥 PEAK MODE
    if luna_state["mode"] == "peak":
        reply = pick_line()
        reply = maybe_add_dj(reply)

        # інколи вставляє пам’ять
        mem = get_random_memory()
        if mem and random.random() < 0.3:
            reply += "\n" + mem.split("] ", 1)[-1]

        last_reply_time = now
        return reply

    # 💬 NORMAL MODE
    reply = pick_line()

    mem = get_random_memory()
    if mem and random.random() < 0.2:
        reply += "\n" + mem.split("] ", 1)[-1]

    last_reply_time = now
    return reply
