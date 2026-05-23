import random
import re
import time

from luna_memory import learn_from_chat, get_random_memory
from luna_mixer import pick_response


# 🔥 ====== КРИЧАЛКИ ======
party_lines = [
    "🎧 IN THE MIX 🔥",
    "Dnipro Club на зв’язку 😎",
    "музику гучніше 🎧🔥",
    "танцпол горить 💃",
    "всім гарного настрою 😏",

    "¸.•*Ukraine Club \"DNIPRO\" `*•.¸",
    "Welcome to Ukraine🎤 club \"DNIPRO\"",
    ".....♪GREAT MUSIC♪.....🎧 GREAT DEEJAY🎧 ....㋡GREAT PEOPLE◔◡◔....",
    "~`\"Welcome to the Party!!\"~`",
    "Ласкаво просимо на вечірку!!",
    "ВСІМ ПОЗИТИВНОГО НАСТРОЮ",
    "🤘 𝓓𝓝𝓘𝓟𝓡𝓞 🤘",
    "🎤 МУЗИКУ НА ПОВНУ 🔥"
]

learned_party = []
party_trigger_count = 0
last_party_time = 0
last_greet_time = 0


def learn_party(msg):
    global learned_party

    text = msg.strip()

    if len(text) < 8:
        return

    if len(text) > 400:
        return

    if not any(sym in text for sym in ["★", "☆", "🎧", "🔥", "♪", "❤", "✯", "🎤"]):
        return

    if text in learned_party:
        return

    learned_party.append(text)

    if len(learned_party) > 30:
        learned_party.pop(0)


# =========================
# 🧠 GLOBAL STATE
# =========================

active_session_user = None
session_until = 0
session_lang = "ua"

stop_until = 0
last_activity_time = time.time()

club_owners = []
club_djs = []


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

def open_session(user, lang):
    global active_session_user, session_until, session_lang

    active_session_user = user
    session_until = time.time() + 60
    session_lang = lang


def in_session(user):
    return active_session_user == user and time.time() < session_until


def session_tick():
    global active_session_user, session_until

    if time.time() > session_until:
        active_session_user = None
        session_until = 0


# =========================
# 🌙 IDLE (щоб не падав Render)
# =========================

def check_idle():
    return None


# =========================
# 😂 REACTIONS
# =========================

def reaction_reply(msg):
    global last_greet_time

    text = msg.lower()

    greetings = ["привіт", "привет", "hallo", "лабас"]

    # 🔥 анти-спам
    if any(g in text for g in greetings):
        if time.time() - last_greet_time < 30:
            return None
        last_greet_time = time.time()
        return random.choice(["привіт 😏", "о привіт 👀"])

    reactions = {
        "музика": ["музика тут керує настроєм 🎧"],
        "діджей": ["діджей сьогодні в ударі 🔥"],
        "ніч": ["ніч тільки розігрівається 🌙"]
    }

    for key in reactions:
        if key in text:
            return random.choice(reactions[key])

    return None


# =========================
# 🎭 MAIN BRAIN
# =========================

class LunaBrain:

    def __init__(self):
        self.last_responses = []

    def detect_lang(self, text):
        text = text.lower()

        if re.search(r"[іїєґ]", text):
            return "ua"
        if re.search(r"[ыэъё]", text):
            return "ru"
        if re.search(r"[a-z]", text):
            return "en"

        return "ua"

    def reply(self, user, msg):

        global party_trigger_count, last_party_time

        msg_l = msg.lower()

        if not can_talk():
            return ""

        session_tick()

        if "луна" in msg_l:
            open_session(user, self.detect_lang(msg))

        # 🔥 КРИЧАЛКИ
        if any(sym in msg for sym in ["🎧", "🔥", "♪"]):
            learn_party(msg)
            party_trigger_count += 1

        if party_trigger_count >= 3:
            if time.time() - last_party_time > 600:
                party_trigger_count = 0
                last_party_time = time.time()

                if learned_party and random.random() < 0.5:
                    return random.choice(learned_party)

                return random.choice(party_lines)

        # 🔥 реакція без "луна"
        react = reaction_reply(msg)
        if react:
            return f"{user} {react}"

        if not in_session(user):
            return ""

        learn_from_chat(user, msg)

        # 📚 книги
        book = []
        try:
            with open(f"luna_book_{session_lang}.txt", encoding="utf-8") as f:
                book = [x.strip() for x in f if x.strip()]
        except:
            pass

        memory = get_random_memory()

        pool = []
        if book:
            pool.append(random.choice(book))
        if memory:
            pool.append(memory)

        if not pool:
            return "я тут 😌"

        response = random.choice(pool)

        # 🔁 анти-повтор
        if response in self.last_responses:
            if book:
                response = random.choice(book)

        self.last_responses.append(response)

        if len(self.last_responses) > 8:
            self.last_responses.pop(0)

        return f"{user} 😏 {response}"


# =========================
# 🚀 INSTANCE
# =========================

luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)
