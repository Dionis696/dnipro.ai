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

# 🔥 НОВЕ
party_trigger_count = 0
last_party_time = 0


def learn_party(msg):

    global learned_party

    text = msg.strip()

    if len(text) < 40:
        return

    if len(text) > 400:
        return

    if not any(sym in text for sym in ["★", "☆", "🎧", "🔥", "♪", "❤", "✯", "🎤"]):
        return

    if text in learned_party:
        return

    learned_party.append(text)

    if len(learned_party) > 20:
        learned_party.pop(0)
# 🔥 ====== КІНЕЦЬ ДОДАНО ======


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
last_greet_time = 0

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
# 🟢 SESSION
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
            "клуб трохи затих 😌",
            "музика ще жива 🎧",
            "хтось ще не спить? 👀"
        ])

    return None


# =========================
# 👑 OWNER / DJ MEMORY
# =========================

def remember_people(msg):

    global club_owners
    global club_djs

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

        # 🔥 ДОДАНО
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
        # 🔥 КІНЕЦЬ ДОДАНО

        "дура": [
            "сама ти бешкетниця 😏",
            "зате весела 😌",
            "ой все 😎"
        ],

        "йди": [
            "сама дорогу знайду 😏",
            "я ще тут 👀",
            "клуб без мене сумуватиме 😌"
        ],

        "хаха": [
            "бачиш, я піднімаю настрій 😎",
            "сміх — це хороший знак 😏"
        ],

        "очі": [
            "вже в окулярах 😎",
            "не всі таємниці треба бачити 👀"
        ],

        "музика": [
            "музика тут керує настроєм 🎧",
            "цей ритм затягує 🔥"
        ],

        "діджей": [
            "діджей сьогодні в ударі 🔥",
            "музика зараз небезпечна 😏"
        ],

        "ніч": [
            "ніч тільки розігрівається 🌙",
            "вночі тут інший світ 😌"
        ]
    }

    for key in reactions:

        if key in text:
            return random.choice(reactions[key])

    return None


# =========================
# 📚 LOAD LANGUAGE BOOK
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

        msg_l = msg.lower()

        if re.search(r"\bstop\b", msg_l) or "луна стоп" in msg_l:

            trigger_stop()

            return "окей… мовчу 😌"

        if not can_talk():
            return ""

        session_tick()

        if "луна" in msg_l or "luna" in msg_l:

            detected_lang = self.detect_lang(msg)

            open_session(user, detected_lang)

        remember_people(msg)

        # 🔥 ====== НОВА ЛОГІКА КРИЧАЛОК ======

        is_party = (
            len(msg) > 40 and
            any(sym in msg for sym in ["🎧", "🔥", "♪", "★", "☆", "🎤"])
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

        # 🔥 ====== КІНЕЦЬ ======

        # 🔥 ДОДАНО (реакція без луна)
        if not in_session(user):

    react = reaction_reply(msg)

    if react:

        global last_greet_time

        # анти-спам привітів
        if any(x in msg_l for x in ["привіт", "привет", "hallo", "лабас"]):

            if time.time() - last_greet_time < 5:
                return ""

            last_greet_time = time.time()

        return react

    return ""

        update_activity()

        learn_party(msg)

        chat_counter += 1

        if chat_counter > 6:
            chat_counter = 0
            if random.random() < 0.25:
                if learned_party and random.random() < 0.5:
                    return random.choice(learned_party)
                return random.choice(party_lines)

        learn_from_chat(user, msg)

        react = reaction_reply(msg)

        if react:
            return react

        lang = session_lang

        book = load_book(lang)

        response_source = "book"

        if random.random() > 0.6:
            response_source = "memory"

        book_pick = ""
        memory = ""

        if response_source == "book":

            if book:
                book_pick = random.choice(book)

        else:

            memory_raw = get_random_memory()

            if memory_raw and "]" in memory_raw:

                memory = memory_raw.split("]", 1)[1].strip()

        if memory:

            memory_lang = self.detect_lang(memory)

            if memory_lang != lang:
                memory = ""

        if memory.lower() == msg.lower():
            memory = ""

        if "овнер" in msg_l or "owner" in msg_l:

            if club_owners:

                return f"я знаю хто тут головний 😏 {random.choice(club_owners)}"

        if "діджей" in msg_l or "dj" in msg_l:

            if club_djs:

                return f"сьогодні вайб робить {random.choice(club_djs)} 🔥"

        pool = []

        if book_pick:
            pool.append(book_pick)

        if memory:
            pool.append(memory)

        if not pool:

            fallback = {

                "ua": [
                    "я слухаю 😌",
                    "ніч сьогодні цікава 🌙",
                    "клуб живе музикою 🎧"
                ],

                "ru": [
                    "я слушаю 😌",
                    "ночь сегодня интересная 🌙",
                    "клуб живёт музыкой 🎧"
                ],

                "en": [
                    "i hear you 😌",
                    "the vibe is alive 🌙",
                    "music never sleeps 🎧"
                ]
            }

            return random.choice(
                fallback.get(lang, ["😌"])
            )

        response = pick_response(pool, [], msg)

        if not response:
            response = random.choice(pool)

        if lang == "ua":

            if any(x in response.lower() for x in [
                "the ",
                "you ",
                "this "
            ]):

                response = random.choice([
                    "я тебе чую 👀",
                    "клуб живе 😌",
                    "ніч сьогодні цікава 🌙"
                ])

        attempts = 0
        while response in self.last_responses and attempts < 5:
            if book:
                response = random.choice(book)
            attempts += 1

        self.last_responses.append(response)

        if len(self.last_responses) > 8:
            self.last_responses.pop(0)

        if random.random() < 0.6:
            response = f"{user} 😏 {response}"

        return response


luna = LunaBrain()


def handle_message(user, message):

    return luna.reply(user, message)
