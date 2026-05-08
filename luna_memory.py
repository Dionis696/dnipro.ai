import os
import random

# =========================
# 📁 FILE PATH
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEM_FILE = os.path.join(BASE_DIR, "luna_memory.txt")

# =========================
# 📦 CREATE FILE IF NOT EXISTS
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
            phrase_memory = [
                line.strip()
                for line in f
                if line.strip()
            ]
    except:
        phrase_memory = []

load_memory()

# =========================
# 🚫 VALIDATION
# =========================

def is_valid(text):

    if not text:
        return False

    text = text.strip()

    if len(text) < 3:
        return False

    if len(text) > 250:
        return False

    return True

# =========================
# 💾 SAVE PHRASE
# =========================

def save_phrase(user, text):

    if not is_valid(text):
        return

    # 🚫 Luna НЕ вчиться сама на собі
    if user.lower() == "luna":
        return

    # 🚫 не зберігати системні штуки
    if text.startswith("["):
        return

    entry = f"[{user}] {text}"

    # 🚫 no duplicates
    if entry in phrase_memory:
        return

    phrase_memory.append(entry)

    # 🚫 limit
    if len(phrase_memory) > 2000:
        phrase_memory.pop(0)

    # 💾 SAVE TO FILE
    try:
        with open(MEM_FILE, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
            f.flush()
            os.fsync(f.fileno())

    except Exception as e:
        print("MEMORY ERROR:", e)

# =========================
# 🧠 LEARN FROM CHAT
# =========================

def learn_from_chat(user, message):

    save_phrase(user, message)

# =========================
# 🎲 GET RANDOM MEMORY
# =========================

def get_random_memory():

    if not phrase_memory:
        return ""

    # 🚫 беремо тільки людські фрази
    clean = []

    for x in phrase_memory:

        # remove [USER]
        if "]" in x:
            text = x.split("]", 1)[1].strip()
        else:
            text = x.strip()

        if text:
            clean.append(text)

    if not clean:
        return ""

    return random.choice(clean)

# =========================
# 📊 DEBUG
# =========================

def memory_size():
    return len(phrase_memory)
