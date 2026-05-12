import random
import re
import time

from luna_memory import learn_from_chat, get_random_memory
from luna_mixer import pick_response


# =========================
# 🧠 GLOBAL STATE
# =========================

active_session_user = None
session_until = 0
session_lang = "ua"

stop_until = 0
last_activity_time = time.time()


# =========================
# 🔴 STOP SYSTEM
# =========================

def trigger_stop():
    global stop_until
    global active_session_user
    global session_until

    stop_until = time.time() + 600

    active_session_user = None
    session_until = 0


def can_talk():
    return time.time() >= stop_until


# =========================
# 🟢 SESSION SYSTEM
# =========================

def open_session(user, lang):

    global active_session_user
    global session_until
    global session_lang

    active_session_user = user
    session_until = time.time() + 60
    session_lang = lang


def in_session(user):

    return (
        active_session_user == user and
        time.time() < session_until
    )


def session_tick():

    global active_session_user
    global session_until

    if time.time() > session_until:
        active_session_user = None
        session_until = 0


# =========================
# 🟡 ACTIVITY
# =========================

def update_activity():

    global last_activity_time
    last_activity_time = time.time()


# =========================
# 🌙 IDLE MODE
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
            "ніч сьогодні дивна 🌙",
            "клуб трохи затих 🎧",
            "хтось ще не спить? 👀",
            "музика ще жива 🔥"
        ])

    return ""


# =========================
# 🌍 LANGUAGE DETECT
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

    if en > 4:
        return "en"

    return "ua"


# =========================
# 📚 LOAD BOOK
# =========================

def load_book(lang):

    filename = f"luna_book_{lang}.txt"

    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [
                x.strip()
                for x in f
                if x.strip()
            ]
    except:
        return []


# =========================
# 🎭 MAIN BRAIN
# =========================

class LunaBrain:

    def __init__(self):

        self.last_reply = ""

    # =========================
    # 💬 REPLY ENGINE
    # =========================

    def reply(self, user, msg):

        global session_lang

        msg_l = msg.lower()

        # =========================
        # 🔴 STOP
        # =========================

        if (
            "stop" in msg_l or
            "луна стоп" in msg_l
        ):
            trigger_stop()
            return "окей… мовчу 😌"

        if not can_talk():
            return ""

        # =========================
        # 🧠 SESSION UPDATE
        # =========================

        session_tick()

        # =========================
        # 🌍 LANGUAGE DETECT
        # =========================

        detected_lang = detect_lang(msg)

        # =========================
        # 🟢 OPEN SESSION
        # =========================

        trigger_words = [
            "луна",
            "luna"
        ]

        if any(x in msg_l for x in trigger_words):

            open_session(user, detected_lang)

        # =========================
        # 🔵 SESSION RULE
        # =========================

        if not in_session(user):
            return ""

        # =========================
        # 🟡 ACTIVITY UPDATE
        # =========================

        update_activity()

        # =========================
        # 🧠 LEARN
        # =========================

        learn_from_chat(user, msg)

        # =========================
        # 📚 LOAD LANGUAGE BOOK
        # =========================

        book = load_book(session_lang)

        # =========================
        # 📚 BOOK PICK
        # =========================

        book_pick = ""

        if book:
            book_pick = random.choice(book)

        # =========================
        # 🧠 MEMORY PICK
        # =========================

        memory = get_random_memory()

        if memory and "]" in memory:
            memory = memory.split("]", 1)[1].strip()

        # =========================
        # 🌍 MEMORY FILTER
        # =========================

        memory_lang = detect_lang(memory)

        if memory_lang != session_lang:
            memory = ""

        # =========================
        # 🚫 ANTI ECHO
        # =========================

        if memory.lower() == msg.lower():
            memory = ""

        # =========================
        # 🎲 RESPONSE POOL
        # =========================

        pool = []

        # 60% BOOK
        if random.random() < 0.6 and book_pick:
            pool.append(book_pick)

        # 40% MEMORY
        if random.random() < 0.4 and memory:
            pool.append(memory)

        # fallback
        if not pool:

            if book_pick:
                pool.append(book_pick)

            if memory:
                pool.append(memory)

        # final fallback
        if not pool:
            return "я тут 😌"

        # =========================
        # 🎭 PICK RESPONSE
        # =========================

        response = pick_response(pool, [], msg)

        if not response:
            response = random.choice(pool)

        # =========================
        # 🔁 ANTI REPEAT
        # =========================

        if response == self.last_reply:

            anti_repeat = {
                "ua": [
                    "я слухаю тебе 😌",
                    "ніч ще жива 🌙",
                    "клуб дихає музикою 🎧"
                ],

                "ru": [
                    "я тебя слушаю 😌",
                    "ночь ещё живая 🌙",
                    "музыка всё слышит 🎧"
                ],

                "en": [
                    "the night is still alive 🌙",
                    "music never sleeps 🎧",
                    "i hear you 😌"
                ]
            }

            response = random.choice(
                anti_repeat.get(session_lang, ["😌"])
            )

        # =========================
        # 💾 SAVE LAST
        # =========================

        self.last_reply = response

        return response


# =========================
# 🚀 INSTANCE
# =========================

luna = LunaBrain()


# =========================
# 🌙 HANDLE MESSAGE
# =========================

def handle_message(user, message):
    return luna.reply(user, message)
