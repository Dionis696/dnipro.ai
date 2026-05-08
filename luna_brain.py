import random
import re
import time

from luna_memory import learn_from_chat, get_random_memory
from luna_mixer import pick_response

from luna_state import (
    open_session,
    in_session,
    trigger_stop,
    can_talk,
    update_activity
)

# =========================
# 🧠 LUNA BRAIN (STATE ENGINE v1)
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
    # 🌍 LANGUAGE LOCK (no random EN spam)
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
    # 💬 MAIN REPLY ENGINE
    # =========================

    def reply(self, user, msg):

        msg_l = msg.lower()

        # 🔴 STOP MODE
        if "stop" in msg_l or "луна стоп" in msg_l:
            trigger_stop()
            return "окей… я замовкаю 😌"

        if not can_talk():
            return ""

        # 🟢 OPEN SESSION (якщо звернулись)
        if "луна" in msg_l or "luna" in msg_l:
            open_session(user)

        # 🔵 якщо немає сесії — мовчить
        if not in_session(user):
            return ""

        # 🧠 activity update
        update_activity()

        # 🧠 learn memory
        learn_from_chat(user, msg)

        # 🌍 language
        lang = self.detect_lang(msg)

        # 📚 memory
        memory_raw = get_random_memory()
        memory = ""

        if memory_raw and "]" in memory_raw:
            memory = memory_raw.split("]", 1)[1].strip()

        # 📚 book
        book_pick = random.choice(self.book) if self.book else ""

        # =========================
        # 🎯 MIX CORE
        # =========================

        options = []

        if memory:
            options.append(memory)

        if book_pick:
            options.append(book_pick)

        if not options:
            return "я тут 😌"

        response = pick_response(options, [], msg)

        if not response:
            response = random.choice(options)

        # =========================
        # 🚫 anti repeat
        # =========================

        if response == self.last_reply:
            response = random.choice([
                "ти ще тут? 👀",
                "ніч трохи затихла…",
                "клуб дихає музикою 🎧",
                "я слухаю тебе 😌"
            ])

        self.last_reply = response

        # =========================
        # 🌍 language safety (no random EN spam)
        # =========================

        if lang == "ua" and any(x in response.lower() for x in ["the ", "this ", "you "]):
            response = random.choice([
                "цікава атмосфера 😌",
                "я тебе чую 👀",
                "клуб живе своїм ритмом 🔥"
            ])

        return response


# =========================
# 🚀 INSTANCE
# =========================

luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)
