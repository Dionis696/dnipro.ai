import time
import re
import random
import os

MEM_FILE = "luna_memory.txt"

# =========================
# 🧠 INIT (без створення файлу на сервері GitHub)
# =========================

def init_memory():
    # тільки перевіряємо, не створюємо магічно
    if not os.path.exists(MEM_FILE):
        print("⚠️ luna_memory.txt not found in repo")

init_memory()

# =========================
# STORAGE
# =========================

user_memory = {}
phrase_memory = []

# =========================
# LOAD MEMORY
# =========================

def load_memory():
    global phrase_memory

    try:
        with open(MEM_FILE, "r", encoding="utf-8") as f:
            phrase_memory = [line.strip() for line in f if line.strip()]
    except:
        phrase_memory = []

load_memory()

# =========================
# FILTER
# =========================

def is_good_phrase(text):
    if len(text) < 10:
        return False

    if len(text) > 150:
        return False

    bad_ratio = len(re.findall(r"[^\w\sа-яА-ЯёЁ]", text)) / max(len(text), 1)
    if bad_ratio > 0.35:
        return False

    return True

# =========================
# SAVE
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

    # ⚠️ важливо для GitHub/hosting
    try:
        with open(MEM_FILE, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except:
        print("⚠️ Cannot write to file (read-only environment?)")

# =========================
# LEARN
# =========================

def learn_from_chat(user, message):
    user_memory[user] = user_memory.get(user, {"count": 0})
    user_memory[user]["count"] += 1

    save_phrase(user, message)

# =========================
# MEMORY OUTPUT
# =========================

def get_random_memory():
    if not phrase_memory:
        return ""
    return random.choice(phrase_memory)
