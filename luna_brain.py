import random
import time
import os
import re

# =========================
# FILES
# =========================

BOOK_FILE = "luna_book.txt"
MEMORY_FILE = "luna_memory.txt"

# =========================
# DIALOG SYSTEM (2 MIN)
# =========================

active_sessions = {}
DIALOG_TIMEOUT = 120

def update_session(user):
    now = time.time()

    if user not in active_sessions:
        active_sessions[user] = now
        return False

    if now - active_sessions[user] > DIALOG_TIMEOUT:
        active_sessions[user] = now
        return False

    active_sessions[user] = now
    return True

# =========================
# LOAD FILES
# =========================

def load_file(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def save_memory(text):
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

# =========================
# LANGUAGE CONTROL (HARD FIX)
# =========================

def detect_lang(msg):
    msg = msg.lower()

    if any(x in msg for x in ["привет", "что", "почему"]):
        return "RU"

    if any(x in msg for x in ["hello", "what", "why", "you", "i see"]):
        return "EN"

    return "UA"


def strip_english(text):
    # жорстке вирізання англійських патернів
    bad_patterns = [
        r"i\s+see.*",
        r"you\s+in.*",
        r"the\s+crowd.*",
        r"rhythm.*",
        r"moment.*",
        r"this\s+place.*",
        r"drop.*",
        r"controls.*",
        r"rules.*"
    ]

    for p in bad_patterns:
        if re.search(p, text.lower()):
            return "цікава атмосфера 😏"

    return text


def enforce_lang(text, lang):

    text = strip_english(text)

    if lang == "UA":
        text = text.replace("interesting vibe", "цікава атмосфера")
        text = text.replace("night feels alive", "ніч жива")
        text = text.replace("you", "ти")

    return text

# =========================
# INTENT DETECTION
# =========================

def detect_intent(msg):
    msg = msg.lower()

    if "?" in msg:
        return "question"

    if any(x in msg for x in ["dj", "сет", "сьогодні", "lineup", "що буде"]):
        return "event"

    if any(x in msg for x in ["вчора", "пам", "remember"]):
        return "memory"

    if any(x in msg for x in ["істор", "story", "розкажи"]):
        return "story"

    return "chat"

# =========================
# ANTI LOOP
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

    return choice

# =========================
# MEMORY LEARN
# =========================

def learn(user, msg):
    if len(msg) > 12 and "?" not in msg:
        save_memory(f"{user}: {msg}")

# =========================
# SAFE STORY MODE
# =========================

def safe_story():
    return random.choice([
        "десь у клубі був вечір коли музика повністю взяла контроль 😏",
        "інколи тут люди просто танцюють і не говорять нічого",
        "ніч тут може змінити настрій за одну пісню"
    ])

# =========================
# MAIN BRAIN
# =========================

def process_luna_message(user, msg):

    if not msg:
        return ""

    msg_low = msg.lower()

    book = load_file(BOOK_FILE)
    memory = load_file(MEMORY_FILE)

    lang = detect_lang(msg_low)
    intent = detect_intent(msg_low)
    is_continuing = update_session(user)

    learn(user, msg)

    # =========================
    # QUESTION
    # =========================
    if intent == "question":

        if "dj" in msg_low or "сет" in msg_low:
            response = pick([
                "лайнап ще уточнюється 😏",
                "DJ сет буде трохи пізніше 🔥",
                "інтрига тримається"
            ])
            return enforce_lang(response, lang)

        response = pick([
            "цікаве питання 😏",
            "я слухаю тебе",
            "розкажи більше"
        ])
        return enforce_lang(response, lang)

    # =========================
    # EVENT
    # =========================
    if intent == "event":

        pool = [
            "сьогодні клубний вечір 🔥",
            "DJ сет очікується 😏",
            "лайнап ще формується",
            "вечір буде активний"
        ] + book[:20]

        return enforce_lang(pick(pool), lang)

    # =========================
    # MEMORY
    # =========================
    if intent == "memory":

        return enforce_lang(
            pick([
                "ти вже це згадував 😏",
                "пам’ятаю цю тему",
                "знайома історія"
            ]),
            lang
        )

    # =========================
    # STORY MODE
    # =========================
    if intent == "story":
        return enforce_lang(safe_story(), lang)

    # =========================
    # CHAT MODE
    # =========================
    pool = book + memory

    if is_continuing:
        response = pick(pool)
    else:
        response = pick(pool)

    response = strip_english(response)
    return enforce_lang(response, lang)
