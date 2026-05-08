import random
import time
import os

# =========================
# FILES
# =========================

BOOK_FILE = "luna_book.txt"
MEMORY_FILE = "luna_memory.txt"

# =========================
# SESSION SYSTEM (2 MIN CHAT)
# =========================

active_sessions = {}
DIALOG_TIMEOUT = 120  # 2 хвилини

def update_session(user):
    now = time.time()

    if user not in active_sessions:
        active_sessions[user] = now
        return False

    if now - active_sessions[user] > DIALOG_TIMEOUT:
        active_sessions[user] = now
        return False

    active_sessions[user] = now
    return True

# =========================
# LOAD FILES
# =========================

def load_file(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def save_memory(text):
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

# =========================
# INTENT DETECTION
# =========================

def detect_intent(msg):
    msg = msg.lower()

    if "?" in msg:
        return "question"

    if any(x in msg for x in ["сьогодні", "сегодня", "tonight", "dj", "сет", "лайн", "lineup"]):
        return "event"

    if any(x in msg for x in ["вчора", "пам", "remember"]):
        return "memory"

    return "chat"

# =========================
# ANTI REPEAT
# =========================

recent = []

def pick(pool):
    global recent

    if not pool:
        return "я тут 🙂"

    options = [x for x in pool if x not in recent]

    if not options:
        recent.clear()
        options = pool

    choice = random.choice(options)

    recent.append(choice)

    if len(recent) > 10:
        recent.pop(0)

    return choice

# =========================
# LEARNING SYSTEM
# =========================

def learn(user, msg):
    msg_low = msg.lower()

    if len(msg_low) > 12 and "?" not in msg_low:
        save_memory(f"{user}: {msg}")

# =========================
# MAIN BRAIN
# =========================

def process_luna_message(user, msg):

    if not msg:
        return ""

    msg_low = msg.lower()

    book = load_file(BOOK_FILE)
    memory = load_file(MEMORY_FILE)

    intent = detect_intent(msg_low)
    is_continuing = update_session(user)

    # =========================
    # LEARN ALWAYS
    # =========================
    learn(user, msg)

    # =========================
    # QUESTION MODE (TOP)
    # =========================
    if intent == "question":

        if "dj" in msg_low or "сет" in msg_low:
            return pick([
                "сьогодні лайнап ще уточнюється 😏",
                "DJ сет буде пізніше 🔥",
                "поки інтрига тримається"
            ])

        return pick([
            "цікаве питання 😏",
            "я слухаю тебе",
            "розкажи більше"
        ])

    # =========================
    # EVENT MODE
    # =========================
    if intent == "event":

        pool = [
            "сьогодні буде клубний вечір 🔥",
            "DJ сет очікується 😏",
            "лайнап ще формується",
            "вечір буде активний"
        ] + book[:20]

        return pick(pool)

    # =========================
    # MEMORY MODE
    # =========================
    if intent == "memory":

        return pick([
            "ти вже про це згадував 😏",
            "пам’ятаю цю тему",
            "знайома історія"
        ])

    # =========================
    # CHAT MODE
    # =========================

    # 🔥 IMPORTANT: CONTINUING DIALOG
    if is_continuing:

        # НЕ скидаємо стиль, НЕ "я тут"
        pool = book + memory
        return pick(pool)

    # =========================
    # NEW DIALOG
    # =========================

    if "luna" in msg_low or "луна" in msg_low:
        pool = book + memory
        return pick(pool)

    # =========================
    # IDLE MODE
    # =========================

    if random.random() < 0.02:
        return pick(book)

    return ""
