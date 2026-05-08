import os
import random

# =========================
# 📁 FILE PATH (FIXED)
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEM_FILE = os.path.join(BASE_DIR, "luna_memory.txt")

# =========================
# 📦 INIT FILE
# =========================

if not os.path.exists(MEM_FILE):
    with open(MEM_FILE, "w", encoding="utf-8") as f:
        f.write("")

# =========================
# 🧠 MEMORY STORAGE
# =========================

phrase_memory = []

# =========================
# 📥 LOAD MEMORY
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
# 🚫 VALIDATION FILTER
# =========================

def is_valid(text):
    if not text:
        return False
    if len(text.strip()) < 3:
        return False
    if len(text) > 250:
        return False
    return True

# =========================
# 💾 SAVE MEMORY (FIXED)
# =========================

def save_phrase(user, text):

    if not is_valid(text):
        return

    entry = f"[{user}] {text}"

    # ❌ no duplicates
    if entry in phrase_memory:
        return

    phrase_memory.append(entry)

    # limit memory size
    if len(phrase_memory) > 2000:
        phrase_memory.pop(0)

    # 💾 write to file (FORCED)
    try:
        with open(MEM_FILE, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
            f.flush()
            os.fsync(f.fileno())
    except Exception as e:
        print("MEMORY WRITE ERROR:", e)

# =========================
# 🧠 LEARN FROM CHAT
# =========================

def learn_from_chat(user, message):

    # 🚨 DO NOT LEARN FROM LUNA ITSELF
    if user.lower() == "luna":
        return

    save_phrase(user, message)

# =========================
# 🎲 GET RANDOM MEMORY
# =========================

def get_random_memory():
    if not phrase_memory:
        return ""
    return random.choice(phrase_memory)

# =========================
# 📊 DEBUG HELP (optional)
# =========================

def memory_size():
    return len(phrase_memory)
