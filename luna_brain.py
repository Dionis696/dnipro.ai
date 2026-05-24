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

# 🧠 НОВЕ
known_users = {}
chat_users = []
last_auto_action = 0


def learn_party(msg):
    global learned_party

    text = msg.strip()

    if len(text) < 8:
        return

    if len(text) > 400:
        return

    party_words = [
        "dj","діджей","music","party","pump","bravo",
        "wooo","yaaa","🔥","🎧","♪","❤","✯","🎤","donate","донат"
    ]

    if not (
        any(sym in text for sym in ["★","☆","🎧","🔥","♪","❤","✯","🎤"])
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
    return (
        active_session_user == user and
        time.time() < session_until
    )


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
            "клуб трохи затих 😌",
            "музика ще жива 🎧",
            "хтось ще не спить? 👀"
        ])

    return None


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
# 😂 REACTIONS (АНТИ-СПАМ)
# =========================

last_react_time = {}

def reaction_reply(user, msg):
    global last_react_time

    text = msg.lower()

    # ⛔ анти-спам 30 сек на юзера
    if user in last_react_time:
        if time.time() - last_react_time[user] < 30:
            return None

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
        "до зустрічі": ["ще побачимось 😏"],
        "тихої та спокійної ночі": ["взаємно 😌"],
    }

    for key in reactions:
        if key in text:
            last_react_time[user] = time.time()
            return random.choice(reactions[key])

    return None


# =========================
# 📚 LOAD LANGUAGE BOOK
# =========================

def load_book(lang):
    filename = f"luna_book_{lang}.txt"

    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [x.strip() for x in f if x.strip()]
    except:
        return []


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
        if ru > ua and ru > 0:
            return "ru"
        if en > 5:
            return "en"

        return "ua"

    def reply(self, user, msg):

        global session_lang
        global chat_counter
        global party_trigger_count
        global last_party_time
        global known_users, chat_users, last_auto_action

        msg_l = msg.lower()

        # 🧠 запам’ятовуємо юзерів
        known_users[user] = known_users.get(user, 0) + 1
        if user not in chat_users:
            chat_users.append(user)
            if len(chat_users) > 30:
                chat_users.pop(0)

        # 🔴 STOP
        if re.search(r"\bstop\b", msg_l) or "луна стоп" in msg_l:
            trigger_stop()
            return "окей… мовчу 😌"

        if not can_talk():
            return ""

        session_tick()

        # 🟢 авто-життя (без луна)
        chat_counter += 1

        if chat_counter >= 20:
            chat_counter = 0

            if time.time() - last_auto_action > 120:
                last_auto_action = time.time()

                if chat_users:
                    target = random.choice(chat_users)

                    if known_users.get(target, 0) < 3:
                        return f"Луна 😏 привіт {target}, ти тут вперше?"

                    actions = [
                        f"Луна 😏 {target}, ти сьогодні у вайбі чи ще розганяєшся?",
                        f"Луна 👀 {target}, ти чув цей трек чи я одна кайфую?",
                        f"Луна 🎧 {target}, щось ти тихий сьогодні",
                        f"Луна 😏 {target}, ти з нами чи десь літаєш?"
                    ]

                    return random.choice(actions)

        # 🔥 КРИЧАЛКИ
        is_party = (
            len(msg) > 40 and
            any(sym in msg for sym in ["🎧","🔥","♪","★","☆","🎤"])
        )

        if is_party:
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
        if not in_session(user):
            react = reaction_reply(user, msg)
            if react:
                return react
            return ""

        update_activity()

        learn_from_chat(user, msg)

        react = reaction_reply(user, msg)
        if react:
            return react

        lang = session_lang
        book = load_book(lang)

        pool = []

        if book:
            pool.append(random.choice(book))

        memory = get_random_memory()
        if memory and "]" in memory:
            memory = memory.split("]",1)[1].strip()
            pool.append(memory)

        if not pool:
            return "клуб живе 🎧"

        response = pick_response(pool, [], msg)

        if not response:
            response = random.choice(pool)

        if random.random() < 0.5:
            response = f"Луна 😏 {user}, {response}"

        return response


# =========================
# 🚀 INSTANCE
# =========================

luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)
