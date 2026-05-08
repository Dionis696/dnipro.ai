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

    stop_until = time.time() + 600
    active_session_user = None
    session_until = 0


def can_talk():
    return time.time() >= stop_until


# =========================
# 🟢 SESSION
# =========================

def open_session(user):
    global active_session_user, session_until

    active_session_user = user
    session_until = time.time() + 60


def in_session(user):
    global active_session_user, session_until

    return active_session_user == user and time.time() < session_until


def session_tick():
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
# 🌙 IDLE (10 MIN)
# =========================

def check_idle():
    global last_activity_time

    if time.time() - last_activity_time > 600:
        update_activity()

        memory = get_random_memory()

        if memory and "]" in memory:
            memory = memory.split("]", 1)[1].strip()

        if memory and 5 < len(memory) < 120:
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
        self.last_responses = []  # 🔥 анти-залипання

        try:
            with open("luna_book.txt", "r", encoding="utf-8") as f:
                self.book = [x.strip() for x in f if x.strip()]
        except:
            self.book = []

    # =========================
    # 🌍 LANGUAGE
    # =========================

    def detect_lang(self, text):
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
    # 💬 REPLY
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

        session_tick()

        # 🟢 SESSION
        if "луна" in msg_l or "luna" in msg_l:
            open_session(user)

        # 🔵 LIVE RULE
        if not in_session(user):
            if random.random() < 0.03:
                return random.choice([
                    "я тут… 👀",
                    "ти мене шукаєш? 😌",
                    "клуб слухає 🎧"
                ])
            return ""

        update_activity()

        # 🧠 learning
        learn_from_chat(user, msg)

        # 📚 memory
        memory_raw = get_random_memory()
        memory = ""

        if memory_raw and "]" in memory_raw:
            memory = memory_raw.split("]", 1)[1].strip()

        if memory and (len(memory) < 5 or len(memory) > 120):
            memory = ""

        # 📚 book
        book_pick = random.choice(self.book) if self.book else ""

        pool = []

        if memory:
            pool.append(memory)

        if book_pick:
            pool.append(book_pick)

        if not pool:
            return "я тут 😌"

        # 🌍 language
        lang = self.detect_lang(msg)

        filtered_pool = []

        for p in pool:
            p_low = p.lower()

            if lang == "ua" and re.search(r"[а-яіїєґ]", p_low):
                filtered_pool.append(p)
            elif lang == "ru" and re.search(r"[а-яё]", p_low):
                filtered_pool.append(p)
            elif lang == "en" and re.search(r"[a-z]", p_low):
                filtered_pool.append(p)

        if not filtered_pool:
            filtered_pool = pool

        # 🎲 response
        response = pick_response(filtered_pool, [], msg)

        if not response:
            response = random.choice(pool)

        # 🌍 UA safety
        if lang == "ua" and any(x in response.lower() for x in ["the ", "you ", "this "]):
            response = "я тебе чую 👀"

        # 🔥 ANTI LOOP (ПОВНОЦІННИЙ)
        if response in self.last_responses:
            response = random.choice([
                "ти ще тут? 👀",
                "ніч дихає музикою 🎧",
                "я слухаю тебе 😌",
                "клуб живе 🔥"
            ])

        # save history
        self.last_responses.append(response)

        if len(self.last_responses) > 5:
            self.last_responses.pop(0)

        self.last_reply = response

        return response


# =========================
# 🚀 INSTANCE
# =========================

luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)
