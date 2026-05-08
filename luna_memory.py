import os
import random

MEM_FILE = "luna_memory.txt"

# =========================
# CREATE FILE IF NOT EXISTS
# =========================

if not os.path.exists(MEM_FILE):
    open(MEM_FILE, "w", encoding="utf-8").close()

# =========================
# MEMORY STORAGE
# =========================

phrase_memory = []

# =========================
# LOAD MEMORY
# =========================

def load_memory():
    global phrase_memory
    try:
        with open(MEM_FILE, "r", encoding="utf-8") as f:
            phrase_memory = [x.strip() for x in f if x.strip()]
    except:
        phrase_memory = []

load_memory()

# =========================
# FILTER
# =========================

def is_valid(text):
    if not text:
        return False
    if len(text) < 5:
        return False
    if len(text) > 200:
        return False
    return True

# =========================
# SAVE (NO ECHO FIX)
# =========================

def save_phrase(user, text):

    # 🚨 НЕ ЗБЕРІГАЄМО ПУСТЕ
    if not is_valid(text):
        return

    entry = f"[{user}] {text}"

    # 🚨 no duplicates
    if entry in phrase_memory:
        return

    phrase_memory.append(entry)

    if len(phrase_memory) > 2000:
        phrase_memory.pop(0)

    try:
        with open(MEM_FILE, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except:
        pass

# =========================
# LEARN (FIXED)
# =========================

def learn_from_chat(user, message):

    # 🚨 STOP LUNA SELF LEARNING
    if user.lower() == "luna":
        return

    save_phrase(user, message)

# =========================
# GET MEMORY
# =========================

def get_random_memory():
    if not phrase_memory:
        return ""
    return random.choice(phrase_memory)
