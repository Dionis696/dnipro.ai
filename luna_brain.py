import random
import re
import time

from luna_memory import learn_from_chat, get_random_memory
from luna_mixer import pick_response


# =========================
# 🧠 STATE
# =========================

active_session_user = None
session_until = 0

stop_until = 0
last_activity_time = time.time()


# =========================
# 🔴 STOP SYSTEM
# =========================

def trigger_stop():
    global stop_until, active_session_user, session_until

    stop_until = time.time() + 600  # 10 хв mute
    active_session_user = None
    session_until = 0


def can_talk():
    return time.time() >= stop_until


# =========================
# 🟢 SESSION (LIVE MODE)
# =========================

def open_session(user):
    global active_session_user, session_until

    active_session_user = user
    session_until = time.time() + 60  # 🔥 60 сек активної взаємодії


def in_session(user):
    global active_session_user, session_until

    return active_session_user == user and time.time() < session_until


def session_tick():
    global active_session_user, session_until

    # авто-закриття сесії
    if active_session_user and time.time() > session_until:
        active_session_user = None
        session_until = 0


# =========================
# 🟡 ACTIVITY
# =========================

def update_activity():
    global last_activity_time
    last_activity_time = time.time()


# =========================
# 🌙 IDLE (10 min)
# =========================

def check_idle():
    global last_activity_time

    if time.time() - last_activity_time > 600:
        update_activity()

        memory = get_random_memory()

        if memory and "]" in memory:
            memory = memory.split("]", 1)[1].strip()

        if memory:
            return memory

        return random.choice([
            "клуб трохи затих… 😌",
            "ніч спостерігає за танцполом 🌙",
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
    # 💬 REPLY ENGINE
    # =========================

    def reply(self, user, msg):

        global stop_until

        msg_l = msg.lower()

        # 🔴 STOP
        if "stop" in msg_l or "луна стоп" in msg_l:
            trigger_stop()
            return "окей… мовчу 😌"

        if not can_talk():
            return ""

        # 🧠 session update
        session_tick()

        # 🟢 OPEN SESSION (будь-яке звернення)
        if "луна" in msg_l or "luna" in msg_l:
            open_session(user)

        # 🔵 LIVE MODE RULE
        if not in_session(user):

            # 🔥 Luna не зникає повністю
            if random.random() < 0.03:
                return random.choice([
                    "я тут… 👀",
                    "ти мене шукаєш? 😌",
                    "клуб слухає 🎧"
                ])

            return ""

        update_activity()

        # 🧠 learn
        learn_from_chat(user, msg)

        # 📚 memory
        memory_raw = get_random_memory()
        memory = ""

        if memory_raw and "]" in memory_raw:
            parts = memory_raw.split("]", 1)
            if len(parts) > 1:
                memory = parts[1].strip()

        # 📚 book
        book_pick = random.choice(self.book) if self.book else ""

        pool = []

        if memory:
            pool.append(memory)

        if book_pick:
            pool.append(book_pick)

        if not pool:
            return "я тут 😌"

        response = pick_response(pool, [], msg)

        if not response:
            response = random.choice(pool)

        # 🔁 anti repeat
        if response == self.last_reply:
            response = random.choice([
                "ти ще тут? 👀",
                "ніч дихає музикою 🎧",
                "я слухаю тебе 😌",
                "клуб живе 🔥"
            ])

        self.last_reply = response

        return response


# =========================
# 🚀 INSTANCE
# =========================

luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)
