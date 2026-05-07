import random
import re
import time

# =========================
# 🧠 MEMORY SYSTEM
# =========================

users = {}
user_phrases = {}
last_messages = {}
last_reply_time = 0

COOLDOWN = 4
IDLE_TIME = 600  # 10 хв

luna_state = {
    "mode": "normal",  # normal / peak / admin
    "last_activity": time.time()
}

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

dj_names = [
    "DJ дядя Жора",
    "DJ Дюна",
    "DJ Demnius",
]

# =========================
# 🧠 MEMORY
# =========================

def remember_user(user):
    if user not in users:
        users[user] = {"count": 0, "last_seen": time.time()}
    users[user]["count"] += 1
    users[user]["last_seen"] = time.time()


def remember_phrase(user, msg):
    if len(msg) < 5:
        return
    if user not in user_phrases:
        user_phrases[user] = []
    if len(user_phrases[user]) < 10:
        user_phrases[user].append(msg)


# =========================
# 🚫 FILTERS
# =========================

def should_ignore(msg):
    if len(msg) > 200:
        return True
    return False


def detect_language(msg):
    if re.search(r"[a-zA-Z]", msg):
        return "EN"
    if re.search(r"[а-яА-Я]", msg):
        return "UA"
    return "UA"


# =========================
# 🔥 PEAK DETECTOR
# =========================

def is_peak(msg):
    keywords = ["DJ", "Club", "☆", "★", "ıllı", "▓"]
    return any(k in msg for k in keywords)


def update_mode(msg):
    global luna_state

    if is_peak(msg):
        luna_state["mode"] = "peak"
    else:
        if time.time() - luna_state["last_activity"] > IDLE_TIME:
            luna_state["mode"] = "idle"
        else:
            luna_state["mode"] = "normal"


# =========================
# 💬 RESPONSE PICKER
# =========================

def pick_response():
    if not book_lines:
        return "..."

    return random.choice(book_lines)


def maybe_add_dj(text):
    if random.random() < 0.3:
        return text + " " + random.choice(dj_names)
    return text


# =========================
# 💤 IDLE MODE
# =========================

idle_phrases = [
    "в клубі якось тихо сьогодні",
    "де всі пропали?",
    "DJ сьогодні мовчить",
    "давайте трохи руху",
    "тиша навіть музика чується інакше"
]


def idle_message():
    return random.choice(idle_phrases)


# =========================
# 🧠 MAIN ENGINE
# =========================

def process_luna_message(user, msg):
    global last_reply_time

    remember_user(user)
    remember_phrase(user, msg)

    update_mode(msg)
    luna_state["last_activity"] = time.time()

    now = time.time()

    # ❌ cooldown
    if now - last_reply_time < COOLDOWN:
        return ""

    # ❌ ignore spam
    if should_ignore(msg):
        return ""

    # 👇 реагує тільки якщо звернення
    if "luna" not in msg.lower() and "луна" not in msg.lower():
        # idle logic
        if luna_state["mode"] == "idle" and random.random() < 0.2:
            last_reply_time = now
            return idle_message()
        return ""

    # 🔥 peak mode
    if luna_state["mode"] == "peak":
        reply = pick_response()
        reply = maybe_add_dj(reply)
        last_reply_time = now
        return reply

    # 💬 normal mode
    reply = pick_response()

    # іноді вставляє фразу користувача
    if user in user_phrases and random.random() < 0.3:
        reply += " — " + random.choice(user_phrases[user])

    last_reply_time = now
    return reply
