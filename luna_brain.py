import random
import time
import os

# =========================
# FILES
# =========================

BOOK_FILE = "luna_book.txt"
MEMORY_FILE = "luna_memory.txt"

# =========================
# DIALOG SESSION (2 MIN)
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
# LANGUAGE LOCK
# =========================

def detect_lang(msg):
    msg = msg.lower()

    if any(x in msg for x in ["hello", "what", "why", "how", "are you"]):
        return "EN"

    if any(x in msg for x in ["привет", "что", "почему"]):
        return "RU"

    return "UA"

def enforce_lang(text, lang):

    if lang == "UA":
        text = text.replace("every", "").replace("you are", "")
        text = text.replace("interesting vibe", "цікава атмосфера")
        text = text.replace("night feels alive", "ніч жива")
        text = text.replace("you", "ти")

    if lang == "RU":
        pass  # можна додати пізніше

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

    if any(x in msg for x in ["істор", "story", "розкажи", "что было"]):
        return "story"

    return "chat"

# =========================
# ANTI REPEAT
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

    # =========================
    # LEARN ALWAYS
    # =========================
    learn(user, msg)

    # =========================
    # QUESTION MODE
    # =========================
    if intent == "question":

        if "dj" in msg_low or "сет" in msg_low:
            return enforce_lang(
                pick([
                    "сьогодні лайнап ще уточнюється 😏",
                    "DJ сет буде пізніше 🔥",
                    "поки інтрига тримається"
                ]),
                lang
            )

        return enforce_lang(
            pick([
                "цікаве питання 😏",
                "я слухаю тебе",
                "розкажи більше"
            ]),
            lang
        )

    # =========================
    # EVENT MODE
    # =========================
    if intent == "event":

        pool = [
            "сьогодні буде клубний вечір 🔥",
            "DJ сет очікується 😏",
            "лайнап ще формується",
            "вечір буде активний"
        ] + book[:20]

        return enforce_lang(pick(pool), lang)

    # =========================
    # MEMORY MODE
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

        return enforce_lang(
            pick([
                "десь у клубі музика так зайшла, що всі просто танцювали до ранку 😏",
                "кажуть тут був вечір коли світло зникло, але ніхто не зупинився",
                "інколи найкращі ночі тут стаються випадково"
            ]),
            lang
        )

    # =========================
    # CHAT MODE
    # =========================

    if is_continuing:
        return enforce_lang(pick(book + memory), lang)

    if "luna" in msg_low or "луна" in msg_low:
        return enforce_lang(pick(book + memory), lang)

    # =========================
    # IDLE MODE
    # =========================
    if random.random() < 0.02:
        return enforce_lang(pick(book), lang)

    return ""
