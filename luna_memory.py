import time
import re
import os

MEM_FILE = "luna_memory.txt"

# =========================
# 🔥 AUTO CREATE FILE
# =========================

if not os.path.exists(MEM_FILE):
    with open(MEM_FILE, "w", encoding="utf-8") as f:
        f.write("")

# =========================
# MEMORY
# =========================

phrase_memory = []

# =========================
# LOAD
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

def is_good(text):
    if len(text) < 6:
        return False
    if len(text) > 200:
        return False
    return True

# =========================
# SAVE (FIXED)
# =========================

def save_phrase(user, text):

    if not is_good(text):
        return

    entry = f"[{user}] {text}"

    # ❌ no duplicates
    if entry in phrase_memory:
        return

    phrase_memory.append(entry)

    # limit
    if len(phrase_memory) > 2000:
        phrase_memory.pop(0)

    # 💾 WRITE TO FILE (MAIN FIX)
    try:
        with open(MEM_FILE, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except Exception as e:
        print("MEMORY WRITE ERROR:", e)


# =========================
# LEARN ENTRY
# =========================

def learn_from_chat(user, message):
    save_phrase(user, message)


# =========================
# GET MEMORY
# =========================

def get_random_memory():
    if not phrase_memory:
        return ""
    import random
    return random.choice(phrase_memory)
