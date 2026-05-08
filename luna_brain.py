import random
import re

from luna_memory import learn_from_chat, get_random_memory
from luna_mixer import pick_response


# =========================
# 📥 LOAD BOOK
# =========================

def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [x.strip() for x in f if x.strip()]
    except:
        return []


# =========================
# 🌍 LANGUAGE DETECT
# =========================

def detect_language(text):

    text = text.lower()

    # українська
    ua = len(re.findall(r"[іїєґ]", text))

    # російська
    ru = len(re.findall(r"[ыэъё]", text))

    # англійська
    en = len(re.findall(r"[a-z]", text))

    if ua > ru and ua > 0:
        return "ua"

    if ru > ua and ru > 0:
        return "ru"

    if en > 3:
        return "en"

    # fallback
    if re.search(r"[а-яА-Я]", text):
        return "ua"

    return "en"


# =========================
# 🔒 LANGUAGE FILTER
# =========================

def match_language(text, lang):

    t = detect_language(text)

    return t == lang


# =========================
# 🧠 LUNA BRAIN
# =========================

class LunaBrain:

    def __init__(self):

        self.book = load_file("luna_book.txt")

        self.last_reply = ""

    # =========================
    # 💬 MAIN REPLY
    # =========================

    def reply(self, user, msg):

        if not msg:
            return "..."

        # 🧠 LEARN USER
        learn_from_chat(user, msg)

        # 🌍 detect language
        lang = detect_language(msg)

        # 📚 FILTER BOOK BY LANGUAGE
        filtered_book = [
            x for x in self.book
            if match_language(x, lang)
        ]

        if not filtered_book:
            filtered_book = self.book

        # 🎲 pick book phrase
        book_pick = random.choice(filtered_book) if filtered_book else ""

        # 🧠 MEMORY
        memory = get_random_memory()

        # 🔥 CLEAN MEMORY
        if "]" in memory:
            memory = memory.split("]", 1)[1].strip()

        # 🚫 NO EMPTY MEMORY
        if not memory:
            memory = ""

        # 🚫 NO ECHO MEMORY
        if memory.strip().lower() == msg.strip().lower():
            memory = ""

        # 🌍 MEMORY LANGUAGE FILTER
        if memory and not match_language(memory, lang):
            memory = ""

        # 🎭 MIX
        response = pick_response(
            [book_pick],
            [memory],
            msg
        )

        # 🚫 EMPTY
        if not response:
            response = book_pick

        # 🚫 STILL EMPTY
        if not response:
            response = "я тут 😌"

        # 🚫 HARD ECHO BLOCK
        if response.strip().lower() == msg.strip().lower():
            response = random.choice(filtered_book) if filtered_book else "я тебе слухаю"

        # 🚫 REPEAT BLOCK
        if response == self.last_reply:
            variants = [
                "цікава атмосфера 😌",
                "сьогодні дивний вайб",
                "ти в настрої говорити 🙂",
                "музика сьогодні жива 🎧",
                "клуб не спить 😏"
            ]

            # 🌍 language lock
            if lang == "ru":
                variants = [
                    "интересный вечер 😌",
                    "клуб сегодня живой 🎧",
                    "необычная атмосфера",
                    "ты сегодня активный 🙂"
                ]

            elif lang == "en":
                variants = [
                    "interesting vibe tonight",
                    "the club feels alive",
                    "music changes everything",
                    "strange atmosphere tonight"
                ]

            response = random.choice(variants)

        # 💾 SAVE LAST
        self.last_reply = response

        return response


# =========================
# 🚀 INSTANCE
# =========================

luna = LunaBrain()


# =========================
# 📡 EXTERNAL CALL
# =========================

def handle_message(user, message):
    return luna.reply(user, message)
