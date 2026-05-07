import time
import re
import random

MEM_FILE = "luna_memory.txt"

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
    except:
        phrase_memory = []

load_memory()

# =========================
# 🚫 FILTER (важливо)
# =========================

def is_good_phrase(text):
    text = text.strip()

    if len(text) < 10:
        return False

    if len(text) > 150:
        return False

    # занадто прості фрази
    if re.fullmatch(r"[a-zA-Zа-яА-ЯёЁ\s]+", text) and len(text.split()) < 3:
        return False

    # сміттєві символи
    bad_ratio = len(re.findall(r"[^\w\sа-яА-ЯёЁ]", text)) / max(len(text), 1)
    if bad_ratio > 0.35:
        return False

    return True


# =========================
# 💾 SAVE TO FILE
# =========================

def save_phrase(user, text):
    if not is_good_phrase(text):
        return

    entry = f"[{user}] {text}"

    # не дублюємо
    if entry in phrase_memory:
        return

    phrase_memory.append(entry)

    # обмеження пам’яті (щоб не зламати сервер)
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
# 📥 MAIN INPUT HOOK
# =========================

def learn_from_chat(user, message):
    remember_user(user)

    # зберігаємо тільки “живі” фрази
    save_phrase(user, message)


# =========================
# 🎯 GET LEARNED PHRASE
# =========================

def get_random_memory():
    if not phrase_memory:
        return ""

    # беремо випадкову фразу
    return random.choice(phrase_memory)


# =========================
# 🎭 GET USER STYLE (простий аналіз)
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
