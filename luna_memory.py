import time
import re
import random
import os

# =========================
# 📦 FILE PATH
# =========================

MEM_FILE = "luna_memory.txt"

# =========================
# 🔥 AUTO CREATE FILE (ВАЖЛИВО)
# =========================

def init_memory_file():
    if not os.path.exists(MEM_FILE):
        with open(MEM_FILE, "w", encoding="utf-8") as f:
            f.write("")
        print("✅ luna_memory.txt created")

init_memory_file()

# =========================
# 📦 MEMORY STORAGE
# =========================

user_memory = {}
phrase_memory = []

# =========================
# 💾 LOAD MEMORY
# =========================

def load_memory():
    global phrase_memory
    try:
        with open(MEM_FILE, "r", encoding="utf-8") as f:
            phrase_memory = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print("LOAD ERROR:", e)
        phrase_memory = []

load_memory()

# =========================
# 🚫 FILTER
# =========================

def is_good_phrase(text):
    text = text.strip()

    if len(text) < 10:
        return False

    if len(text) > 150:
        return False

    if re.fullmatch(r"[a-zA-Zа-яА-ЯёЁ\s]+", text) and len(text.split()) < 3:
        return False

    bad_ratio = len(re.findall(r"[^\w\sа-яА-ЯёЁ]", text)) / max(len(text), 1)
    if bad_ratio > 0.35:
        return False

    return True

# =========================
# 💾 SAVE MEMORY
# =========================

def save_phrase(user, text):
    if not is_good_phrase(text):
        return

    entry = f"[{user}] {text}"

    if entry in phrase_memory:
        return

    phrase_memory.append(entry)

    if len(phrase_memory) > 2000:
        phrase_memory.pop(0)

    with open(MEM_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

# =========================
# 🧠 USER MEMORY
# =========================

def remember_user(user):
    if user not in user_memory:
        user_memory[user] = {
            "count": 0,
            "last_seen": time.time()
        }

    user_memory[user]["count"] += 1
    user_memory[user]["last_seen"] = time.time()

# =========================
# 📥 MAIN HOOK
# =========================

def learn_from_chat(user, message):
    remember_user(user)
    save_phrase(user, message)

# =========================
# 🎯 RANDOM MEMORY
# =========================

def get_random_memory():
    if not phrase_memory:
        return ""
    return random.choice(phrase_memory)

# =========================
# 🎭 USER STYLE
# =========================

def get_user_style(user):
    if user not in user_memory:
        return "new"

    count = user_memory[user]["count"]

    if count > 50:
        return "regular"
    elif count > 10:
        return "known"
    else:
        return "new"
