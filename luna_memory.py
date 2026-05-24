import os
import random
import time

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

    # занадто шумні повідомлення
    bad_ratio = len([c for c in text if not c.isalnum() and c not in " .,!?-"]) / max(len(text), 1)
    if bad_ratio > 0.4:
        return False

    return True


# =========================
# 💾 SAVE MEMORY
# =========================

def save_phrase(user, text):

    if not is_valid(text):
        return

    if user.lower() == "luna":
        return

    if text.startswith("["):
        return

    entry = f"[{user}] {text}"

    try:
        with open(MEM_FILE, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except:
        pass


# =========================
# 🧠 LEARN
# =========================

def learn_from_chat(user, message):
    save_phrase(user, message)


# =========================
# 🎯 SMART MEMORY PICK (АНТИ-ПОВТОРИ)
# =========================

last_memories = []

def get_random_memory():

    global last_memories

    try:
        with open(MEM_FILE, "r", encoding="utf-8") as f:
            lines = [x.strip() for x in f if x.strip()]
    except:
        return ""

    if not lines:
        return ""

    clean = []

    for x in lines:

        if "]" in x:
            text = x.split("]", 1)[1].strip()
        else:
            text = x.strip()

        if len(text) < 5:
            continue

        clean.append(text)

    if not clean:
        return ""

    # 🔥 НЕ повторюємо одне і те саме
    pool = [x for x in clean if x not in last_memories]

    if not pool:
        pool = clean

    result = random.choice(pool)

    last_memories.append(result)

    if len(last_memories) > 15:
        last_memories.pop(0)

    return result


# =========================
# 🧠 НОВЕ: MEMORY З НІКОМ (ВИПРАВЛЕНО)
# =========================

def get_memory_with_user():

    try:
        with open(MEM_FILE, "r", encoding="utf-8") as f:
            lines = [x.strip() for x in f if x.strip()]
    except:
        return None, None

    if not lines:
        return None, None

    valid = []

    for line in lines:

        if "]" in line:

            user = line.split("]", 1)[0].replace("[", "").strip()

            # 🔥 ІГНОРУЄМО [Memory]
            if user.lower() == "memory":
                continue

            text = line.split("]", 1)[1].strip()

            if len(text) < 3:
                continue

            valid.append((user, text))

    if not valid:
        return None, None

    return random.choice(valid)


# =========================
# 📊 MEMORY STATS
# =========================

def memory_size():

    try:
        with open(MEM_FILE, "r", encoding="utf-8") as f:
            return len(f.readlines())
    except:
        return 0
