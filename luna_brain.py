import random
import time
import os

# =========================
# FILES
# =========================

BOOK_FILE = "luna_book.txt"
MEMORY_FILE = "luna_memory.txt"

# =========================
# MEMORY CACHE
# =========================

recent_replies = []
user_memory = {}

MAX_RECENT = 10

# =========================
# LOAD FILES
# =========================

def load_file(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def save_memory(line):
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

# =========================
# INTENT DETECTION
# =========================

def detect_intent(msg):
    msg = msg.lower()

    if "?" in msg:
        return "question"

    if any(x in msg for x in ["вчора", "учора", "yesterday"]):
        return "memory"

    if any(x in msg for x in ["dj", "муз", "сет"]):
        return "dj"

    return "chat"

# =========================
# RESPONSE PICKER
# =========================

def pick_response(user, msg, intent):

    global recent_replies

    book = load_file(BOOK_FILE)
    memory = load_file(MEMORY_FILE)

    pool = []

    # 70% book / 30% memory
    if random.random() < 0.7:
        pool += book
    else:
        pool += memory

    if not pool:
        return "я тут 🙂"

    available = [x for x in pool if x not in recent_replies]

    if not available:
        recent_replies = []
        available = pool

    reply = random.choice(available)

    recent_replies.append(reply)

    if len(recent_replies) > MAX_RECENT:
        recent_replies.pop(0)

    return reply

# =========================
# LEARNING SYSTEM
# =========================

def learn_from_user(user, msg):

    msg_low = msg.lower()

    # зберігаємо тільки цікаві фрази
    if len(msg_low) > 15 and "?" not in msg_low:

        save_memory(f"{user}: {msg}")

        user_memory.setdefault(user, [])
        user_memory[user].append(msg)

        if len(user_memory[user]) > 20:
            user_memory[user].pop(0)

# =========================
# MAIN ENGINE
# =========================

def process_luna_message(user, msg):

    if not msg:
        return ""

    msg_low = msg.lower()

    intent = detect_intent(msg_low)

    # =========================
    # LEARN ALWAYS
    # =========================

    learn_from_user(user, msg)

    # =========================
    # ACTIVE MODE
    # =========================

    if "luna" in msg_low or "луна" in msg_low:

        # memory recall trigger
        if intent == "memory":
            return "пам’ятаю ти щось казав про це 😏"

        if intent == "question":
            return pick_response(user, msg, "chat")

        if intent == "dj":
            return pick_response(user, msg, "dj")

        return pick_response(user, msg, "chat")

    # =========================
    # IDLE MODE
    # =========================

    if random.random() < 0.02:
        return pick_response(user, msg, "chat")

    return ""
