import time
import random
import re

from luna_memory import learn_from_chat, get_random_memory
from luna_mixer import pick_response


# =========================
# 🧠 CONTEXT + ACTIVITY
# =========================

context_buffer = []
last_activity_time = time.time()

def update_context(user, msg):
    global context_buffer, last_activity_time

    context_buffer.append(f"{user}: {msg}")
    last_activity_time = time.time()

    if len(context_buffer) > 10:
        context_buffer.pop(0)


# =========================
# 🔴 STOP SYSTEM
# =========================

stop_until = 0

def check_stop(msg):
    global stop_until
    text = msg.lower()

    if "stop" in text or "луна стоп" in text:
        stop_until = time.time() + 600
        return True

    return False


def can_talk():
    return time.time() >= stop_until


# =========================
# 🌍 LANGUAGE
# =========================

def detect_language(text):
    text = text.lower()

    ua = len(re.findall(r"[іїєґ]", text))
    ru = len(re.findall(r"[ыэъё]", text))
    en = len(re.findall(r"[a-z]", text))

    if ua > ru and ua > 0:
        return "ua"
    if ru > ua and ru > 0:
        return "ru"
    if en > 3:
        return "en"

    return "ua"


# =========================
# 🟡 IDLE MODE (10 MIN)
# =========================

def check_idle():
    global last_activity_time

    if time.time() - last_activity_time > 600:
        last_activity_time = time.time()

        return random.choice([
            "клуб трохи затих… 😌",
            "музика ще грає, але всі мовчать 🎧",
            "ніч дивиться на танцпол 🌙",
            "хтось ще тут? 👀",
            "атмосфера зависла між треками…"
        ])

    return None


# =========================
# 🎭 MAIN BRAIN
# =========================

class LunaBrain:

    def __init__(self):
        self.book = []
        self.last_reply = ""

        try:
            with open("luna_book.txt", "r", encoding="utf-8") as f:
                self.book = [x.strip() for x in f if x.strip()]
        except:
            self.book = []

    # =========================
    # 💬 REPLY ENGINE
    # =========================

    def reply(self, user, msg):

        global last_activity_time

        # 🔴 STOP CHECK
        if not can_talk():
            return ""

        if check_stop(msg):
            return "окей… мовчу 😌"

        # 🟢 SESSION / ATTENTION RULE
        if "луна" not in msg.lower() and "luna" not in msg.lower():
            return ""  # ігнорує якщо не звернулись

        # 🧠 UPDATE
        update_context(user, msg)
        learn_from_chat(user, msg)

        # =========================
        # 📚 BOOK + MEMORY
        # =========================

        book_pick = random.choice(self.book) if self.book else ""

        memory_raw = get_random_memory()
        memory = ""

        if memory_raw and "]" in memory_raw:
            memory = memory_raw.split("]", 1)[1].strip()

        # =========================
        # MIX PRIORITY
        # =========================

        candidates = []

        if memory:
            candidates.append(memory)

        if book_pick:
            candidates.append(book_pick)

        response = pick_response(candidates, [], msg)

        if not response:
            response = random.choice(candidates) if candidates else "я тут 😌"

        # =========================
        # MEMORY BOOST (ЖИВІСТЬ)
        # =========================

        if memory and random.random() < 0.35:
            response = memory

        # =========================
        # ANTI REPEAT
        # =========================

        if response == self.last_reply:
            response = random.choice([
                "ти ще тут? 👀",
                "ніч трохи затихла…",
                "клуб дихає музикою 🎧",
                "цікава пауза 😌"
            ])

        self.last_reply = response
        return response


# =========================
# 🚀 INSTANCE
# =========================

luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)
