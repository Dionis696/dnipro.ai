import os
import random
import re

# =========================
# 📁 FILE PATH
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEM_FILE = os.path.join(BASE_DIR, "luna_memory.txt")

if not os.path.exists(MEM_FILE):
    with open(MEM_FILE, "w", encoding="utf-8") as f:
        f.write("")


# =========================
# 🚫 BAD WORDS
# =========================

BAD_PARTS = [
    "joined","left","teleport","http","https",".com",".ru",".exe",
    "wearing","attachment","secondlife://","marketplace",
    "object","rezzed","gesture","group notice"
]


# =========================
# 🧼 CLEAN TEXT
# =========================

def clean_text(text):

    text = text.strip()

    text = re.sub(r"^[A-Za-z0-9_]+[\s,:-]+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================
# ✅ VALIDATION
# =========================

def is_valid(text):

    if not text:
        return False

    text = clean_text(text)

    if len(text) < 5 or len(text) > 180:
        return False

    text_l = text.lower()

    # ❌ НЕ ВЧИМО ПИТАННЯ
    if "?" in text:
        return False

    if any(x in text_l for x in BAD_PARTS):
        return False

    if text.count("😂") > 5:
        return False

    if text.count("🔥") > 5:
        return False

    bad_ratio = len([
        c for c in text
        if not c.isalnum() and c not in " .,!?'-🙂😏👀🔥😄😌🌙🎧💃"
    ]) / max(len(text), 1)

    if bad_ratio > 0.35:
        return False

    if re.search(r"\b[A-Z0-9_]{4,}\b", text):
        return False

    return True


# =========================
# 📥 LOAD
# =========================

def load_all():
    try:
        with open(MEM_FILE, "r", encoding="utf-8") as f:
            return [x.strip() for x in f if x.strip()]
    except:
        return []


# =========================
# 💾 SAVE MEMORY
# =========================

def save_phrase(user, text):

    if "luna" in user.lower():
        return

    if not is_valid(text):
        return

    text = clean_text(text)

    existing = load_all()

    for line in existing:
        if "]" not in line:
            continue

        old = line.split("]", 1)[1].strip().lower()

        if old == text.lower():
            return

    entry = f"[{user}] {text}"

    try:
        with open(MEM_FILE, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except:
        pass


def learn_from_chat(user, message):
    save_phrase(user, message)


# =========================
# 🎯 RELATED MEMORY
# =========================

def get_related_memory(msg):

    lines = load_all()

    if not lines:
        return None

    msg_l = msg.lower()

    ignore_words = ["клуб", "ніч", "музика", "dj", "луна"]

    words = re.findall(r"\w+", msg_l)
    words = [
        w for w in words
        if len(w) >= 4 and w not in ignore_words
    ]

    if not words:
        return None

    scored = []

    for line in lines:

        if "]" not in line:
            continue

        text = line.split("]", 1)[1].strip()
        text = clean_text(text)

        if not is_valid(text):
            continue

        text_l = text.lower()

        score = 0

        for w in words:
            if f" {w} " in f" {text_l} ":
                score += 1

        if score >= 2:
            scored.append((score, text))

    if not scored:
        return None

    scored.sort(key=lambda x: x[0], reverse=True)

    return random.choice(scored[:3])[1]


# =========================
# 🎲 RANDOM MEMORY
# =========================

last_memories = []

def get_random_memory():

    global last_memories

    lines = load_all()

    clean_pool = []

    for line in lines:

        if "]" not in line:
            continue

        text = line.split("]", 1)[1].strip()
        text = clean_text(text)

        if not is_valid(text):
            continue

        if text.lower() in ["ok","ага","привіт","hello","hi","lol"]:
            continue

        clean_pool.append(text)

    if not clean_pool:
        return None

    pool = [x for x in clean_pool if x not in last_memories]

    if not pool:
        pool = clean_pool

    result = random.choice(pool)

    last_memories.append(result)

    if len(last_memories) > 20:
        last_memories.pop(0)

    return result
