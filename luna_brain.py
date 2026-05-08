import time
import random
import re

from luna_memory import learn_from_chat, get_random_memory
from luna_mixer import pick_response


# =========================
# 🧠 CONTEXT MEMORY
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
# 🔴 STOP MODE
# =========================

stop_until = 0

def check_stop(msg):
    global stop_until

    text = msg.lower()

    if "stop" in text or "луна стоп" in text:
        stop_until = time.time() + 600  # 10 min mute
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
# 🟡 IDLE MODE (CLEAN 10 MIN)
# =========================

def check_idle():
    global last_activity_time

    if time.time() - last_activity_time > 600:  # 10 min silence
        last_activity_time = time.time()

        return random.choice([
            "клуб трохи затих… 😌",
            "музика ще грає, але розмови зникли 🎧",
            "тиша сьогодні особлива…",
            "ніч дивиться на танцпол 🌙",
            "хтось ще тут? 👀"
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
    # 💬 RESPONSE ENGINE
    # =========================

    def reply(self, user, msg):

        global last_activity_time

        # 🔴 STOP CHECK
        if check_stop(msg):
            return "окей… мовчу 😌"

        if is_stopped():
            return ""

        # 🧠 CONTEXT
        update_context(user, msg)

        # 🧠 LEARN
        learn_from_chat(user, msg)

        # 📚 BOOK
        book_pick = random.choice(self.book) if self.book else ""

        # 🧠 MEMORY
        memory = get_random_memory()

        if "]" in memory:
            memory = memory.split("]", 1)[1].strip()

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
# 🚀 INSTANCE
# =========================

luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)


# =========================
# 🟡 EXTERNAL IDLE CALL
# =========================

def get_idle_message():
    return check_idle()
