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
# 🟢 SESSION CONTROL
# =========================

def open_session(user):
    global active_session_user, session_until

    active_session_user = user
    session_until = time.time() + 120  # 2 хв


def in_session(user):
    global active_session_user, session_until

    return active_session_user == user and time.time() < session_until


def update_activity():
    global last_activity_time
    last_activity_time = time.time()


# =========================
# 🔴 STOP SYSTEM
# =========================

def trigger_stop():
    global stop_until
    stop_until = time.time() + 600  # 10 хв


def can_talk():
    return time.time() >= stop_until


# =========================
# 🟡 IDLE MODE (10 min)
# =========================

def check_idle():
    global last_activity_time

    if time.time() - last_activity_time > 600:
        update_activity()
        return random.choice([
            "клуб трохи затих… 😌",
            "музика грає тихіше 🎧",
            "ніч дивиться на танцпол 🌙",
            "хтось ще тут? 👀",
            "атмосфера зависла між треками"
        ])

    return None


# =========================
# 🌍 LANGUAGE (no spam EN)
# =========================

def detect_lang(text):
    text = text.lower()

    ua = len(re.findall(r"[іїєґ]", text))
    ru = len(re.findall(r"[ыэъё]", text))
    en = len(re.findall(r"[a-z]", text))

    if ua > 0:
        return "ua"
    if ru > ua and ru > 0:
        return "ru"
    if en > 5:
        return "en"

    return "ua"


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

        global stop_until, last_activity_time

        msg_l = msg.lower()

        # 🔴 STOP
        if "stop" in msg_l or "луна стоп" in msg_l:
            trigger_stop()
            return "окей… мовчу 😌"

        if not can_talk():
            return ""

        # 🟢 SESSION OPEN
        trigger_words = ["луна", "luna", "hey luna", "эй луна"]

        if any(w in msg_l for w in trigger_words):
            open_session(user)

        # 🔵 session rule
        if not in_session(user):

            # трохи “життя” без спаму
            if random.random() < 0.05:
                return random.choice([
                    "я тут… 👀",
                    "клуб слухає 🎧",
                    "ти мене покликав? 😌"
                ])

            return ""

        update_activity()

        # 🧠 learn
        learn_from_chat(user, msg)

        # 📚 memory
        memory_raw = get_random_memory()
        memory = ""

        if memory_raw and "]" in memory_raw:
            memory = memory_raw.split("]", 1)[1].strip()

        # 📚 book
        book_pick = random.choice(self.book) if self.book else ""

        # =========================
        # MIX
        # =========================

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

        # 🚫 anti repeat
        if response == self.last_reply:
            response = random.choice([
                "ти ще тут? 👀",
                "ніч трохи затихла…",
                "клуб дихає музикою 🎧",
                "я слухаю тебе 😌"
            ])

        self.last_reply = response

        # 🌍 language safety
        if detect_lang(msg) == "ua":
            if any(x in response.lower() for x in ["the ", "you ", "this "]):
                response = random.choice([
                    "цікава атмосфера 😌",
                    "я тебе чую 👀",
                    "клуб живе 🔥"
                ])

        return response


# =========================
# 🚀 INSTANCE
# =========================

luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)
