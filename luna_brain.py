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
# 🟢 SESSION (2 min)
# =========================

def open_session(user):
    global active_session_user, session_until

    active_session_user = user
    session_until = time.time() + 120  # 2 хв


def in_session(user):
    global active_session_user, session_until

    return active_session_user == user and time.time() < session_until


def session_timeout():
    global active_session_user, session_until

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

        # 🧠 session timeout reset
        session_timeout()

        # 🎧 CLUB TRIGGER
        if "dnipro" in msg_l or "club" in msg_l:
            return random.choice([
                "☆ Club DNIPRO живе в ритмі 🎧",
                "DJ тримає атмосферу 🔥",
                "ніч у клубі дихає музикою 🌙",
                "танцпол не зупиняється 💃"
            ])

        # 🟢 OPEN SESSION
        if msg_l.strip() in ["луна", "luna", "hey luna", "эй луна"]:
            open_session(user)

        # 🔵 session rule
        if not in_session(user):
            if random.random() < 0.02:
                return random.choice([
                    "я тут… 👀",
                    "ти мене покликав? 😌"
                ])
            return ""

        update_activity()

        # 🧠 LEARN
        learn_from_chat(user, msg)

        # 📚 MEMORY
        memory_raw = get_random_memory()
        memory = ""

        if memory_raw and "]" in memory_raw:
            parts = memory_raw.split("]", 1)
            if len(parts) > 1:
                memory = parts[1].strip()

        # 📚 BOOK
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
                "ніч трохи затихла…",
                "клуб дихає музикою 🎧",
                "я слухаю тебе 😌"
            ])

        self.last_reply = response

        return response


# =========================
# 🚀 INSTANCE
# =========================

luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)
