import time
import random
import re

from luna_memory import learn_from_chat, get_random_memory
from luna_mixer import pick_response


# =========================
# 🧠 CONTEXT MEMORY (2–3 MIN)
# =========================

context_buffer = []
last_activity_time = time.time()

def update_context(user, msg):
    global context_buffer, last_activity_time

    context_buffer.append(f"{user}: {msg}")
    last_activity_time = time.time()

    # keep only last ~10 messages
    if len(context_buffer) > 10:
        context_buffer.pop(0)


# =========================
# 🔴 STOP MODE
# =========================

stop_until = 0

def check_stop(msg):
    global stop_until

    text = msg.lower()

    if "stop" in text or "луна стоп" in text:
        stop_until = time.time() + 600  # 10 min
        return True

    return False


def is_stopped():
    return time.time() < stop_until


# =========================
# 🌍 LANGUAGE DETECT
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
# 🧠 IDLE MODE
# =========================

def idle_message():
    return random.choice([
        "клуб сьогодні трохи тихий 😌",
        "музика ще звучить навіть у тиші 🎧",
        "тиша теж має свій ритм…",
        "ніч спостерігає за нами 🌙",
        "цікава атмосфера сьогодні…"
    ])


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
    # 💬 RESPONSE ENGINE
    # =========================

    def reply(self, user, msg):

        global last_activity_time

        # 🔴 STOP CHECK
        if check_stop(msg):
            return "окей… мовчу 😌"

        if is_stopped():
            return ""  # full mute

        # 🧠 CONTEXT UPDATE
        update_context(user, msg)

        # 🧠 LEARN
        learn_from_chat(user, msg)

        lang = detect_language(msg)

        # 📚 BOOK PICK
        book_pick = random.choice(self.book) if self.book else ""

        # 🧠 MEMORY PICK
        memory = get_random_memory()

        # clean memory
        if "]" in memory:
            memory = memory.split("]", 1)[1].strip()

        # 🚫 anti echo
        if memory.lower() == msg.lower():
            memory = ""

        # =========================
        # MIX RESPONSE
        # =========================

        response = pick_response([book_pick], [memory], msg)

        if not response:
            response = book_pick

        if not response:
            response = "я тут 😌"

        # 🚫 repeat protection
        if response == self.last_reply:
            response = random.choice([
                "цікава атмосфера 😌",
                "ніч сьогодні жива",
                "ти в настрої говорити? 💃",
                "клуб дихає музикою 🎧"
            ])

        self.last_reply = response
        return response


# =========================
# 🟡 IDLE CHECK (CALL THIS OUTSIDE)
# =========================

def check_idle():
    global last_activity_time

    if time.time() - last_activity_time > 120:  # 2 min idle
        last_activity_time = time.time()
        return idle_message()

    return None


# =========================
# 🚀 INSTANCE
# =========================

luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)
