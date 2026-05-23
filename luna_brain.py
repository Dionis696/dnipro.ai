import random
import re
import time

from luna_memory import learn_from_chat, get_random_memory
from luna_mixer import pick_response


# 🔥 ====== ДОДАНО (КРИЧАЛКИ) ======
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

chat_counter = 0
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

    party_words = [
        "dj","діджей","music","party","pump","bravo","wooo","yaaa",
        "🔥","🎧","♪","❤","✯","🎤","donate","донат"
    ]

    if not (
        any(sym in text for sym in ["★", "☆", "🎧", "🔥", "♪", "❤", "✯", "🎤"])
        or any(word in text.lower() for word in party_words)
    ):
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
# 🟡 ACTIVITY
# =========================

def update_activity():
    global last_activity_time
    last_activity_time = time.time()


# =========================
# 👑 OWNER / DJ MEMORY
# =========================

def remember_people(msg):

    global club_owners, club_djs
    text = msg.lower()

    if "овнер" in text or "owner" in text:
        words = msg.split()
        if len(words) >= 2:
            name = words[-1]
            if name not in club_owners:
                club_owners.append(name)

    if "діджей" in text or "dj" in text:
        words = msg.split()
        if len(words) >= 2:
            name = words[-1]
            if name not in club_djs:
                club_djs.append(name)


# =========================
# 😂 REACTIONS
# =========================

def reaction_reply(msg):

    text = msg.lower()

    reactions = {
        "привіт": ["привіт 😏", "о привіт 👀"],
        "привет": ["привет 😏", "о привет 👀"],
        "hallo": ["hallo 😏", "hey 👀"],
        "лабас": ["лабас 😏"],

        "доброго вечора": ["доброго вечора 😏"],
        "добрый вечер": ["добрый вечер 😏"],

        "всем пока": ["давай 😉"],
        "досвидания": ["ще побачимось 😉"],
        "добраніч": ["солодких снів 🌙"],

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
        ua = len(re.findall(r"[іїєґ]", text))
        ru = len(re.findall(r"[ыэъё]", text))
        en = len(re.findall(r"[a-z]", text))

        if ua > 0:
            return "ua"
        if ru > ua:
            return "ru"
        if en > 5:
            return "en"

        return "ua"

    def reply(self, user, msg):

        global chat_counter, party_trigger_count, last_party_time, last_greet_time

        msg_l = msg.lower()

        # 🔴 STOP
        if re.search(r"\bstop\b", msg_l) or "луна стоп" in msg_l:
            trigger_stop()
            return "окей… мовчу 😌"

        if not can_talk():
            return ""

        session_tick()

        if "луна" in msg_l or "luna" in msg_l:
            open_session(user, self.detect_lang(msg))

        remember_people(msg)

        # 🔥 PARTY LOGIC
        if any(x in msg_l for x in ["🎧","🔥","dj","music","party"]):
            learn_party(msg)
            party_trigger_count += 1

        if party_trigger_count >= 3 and time.time() - last_party_time > 600:
            party_trigger_count = 0
            last_party_time = time.time()
            return random.choice(learned_party or party_lines)

        # 🔥 анти-спам привітів
        if not in_session(user):
            react = reaction_reply(msg)
            if react:

                if any(x in msg_l for x in ["привіт","привет","hallo","лабас"]):
                    if time.time() - last_greet_time < 5:
                        return ""
                    last_greet_time = time.time()

                return react
            return ""

        update_activity()

        learn_from_chat(user, msg)

        react = reaction_reply(msg)
        if react:
            return react

        lang = session_lang
        book = load_book(lang)

        pool = []

        if book:
            pool.append(random.choice(book))

        memory = get_random_memory()
        if memory and "]" in memory:
            pool.append(memory.split("]", 1)[1].strip())

        if not pool:
            return "я слухаю 😌"

        response = pick_response(pool, [], msg) or random.choice(pool)

        if response in self.last_responses:
            response = random.choice(pool)

        self.last_responses.append(response)

        if len(self.last_responses) > 8:
            self.last_responses.pop(0)

        return response


# =========================
# 🚀 INSTANCE
# =========================

luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)
