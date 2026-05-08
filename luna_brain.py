import random
import os

BOOK_FILE = "luna_book.txt"
MEMORY_FILE = "luna_memory.txt"

# =========================
# LOAD FILES
# =========================

def load_file(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# =========================
# CLEAN OUTPUT GUARD
# =========================

def clean(text):
    bad = ["Resident", "undefined", "None", "null"]
    for b in bad:
        text = text.replace(b, "")
    return text.strip()

# =========================
# PRIORITY ENGINE (ГОЛОВНЕ)
# =========================

def detect_intent(msg):
    msg = msg.lower()

    # 1. QUESTION FIRST
    if "?" in msg:
        return "question"

    # 2. EVENT / DJ INFO
    if any(x in msg for x in ["сьогодні", "сегодня", "tonight", "що буде", "what", "лайн", "lineup", "dj", "сет"]):
        return "event"

    # 3. MEMORY TRIGGER
    if any(x in msg for x in ["вчора", "учора", "remember", "пам"]):
        return "memory"

    # 4. CHAT
    return "chat"

# =========================
# SAFE PICK (NO REPETITION)
# =========================

recent = []

def pick(pool):
    global recent

    if not pool:
        return "я тут 🙂"

    options = [x for x in pool if x not in recent]

    if not options:
        recent.clear()
        options = pool

    choice = random.choice(options)

    recent.append(choice)

    if len(recent) > 10:
        recent.pop(0)

    return clean(choice)

# =========================
# MAIN BRAIN
# =========================

def process_luna_message(user, msg):

    if not msg:
        return ""

    msg_low = msg.lower()

    book = load_file(BOOK_FILE)
    memory = load_file(MEMORY_FILE)

    intent = detect_intent(msg_low)

    # =========================
    # 1. QUESTION MODE (TOP PRIORITY)
    # =========================
    if intent == "question":

        if "dj" in msg_low or "сет" in msg_low:
            return pick([
                "сьогодні ще уточнюють лайнап 😏",
                "буде DJ сет пізніше 🔥",
                "поки інтрига тримається"
            ])

        return pick([
            "цікаве питання 😏",
            "розкажи трохи більше",
            "я слухаю тебе"
        ])

    # =========================
    # 2. EVENT MODE (CLUB INFO)
    # =========================
    if intent == "event":

        pool = [
            "сьогодні буде клубний вечір 🔥",
            "DJ сет очікується сьогодні 😏",
            "лайнап ще формується",
            "вечір буде активний"
        ]

        # додаємо трохи book
        pool += book[:20]

        return pick(pool)

    # =========================
    # 3. MEMORY MODE
    # =========================
    if intent == "memory":

        if memory:
            return pick([
                "пам’ятаю що ти про це згадував 😏",
                "ти вже казав щось подібне",
                "є відчуття знайомої історії"
            ])

        return "я це запам’ятаю 🙂"

    # =========================
    # 4. NORMAL CHAT MODE
    # =========================
    if "luna" in msg_low or "луна" in msg_low:

        pool = book + memory

        return pick(pool)

    # =========================
    # 5. IDLE MODE
    # =========================
    if random.random() < 0.02:
        return pick(book)

    return ""
    
