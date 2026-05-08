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

stop_until = 0
last_activity_time = time.time()

# 🧠 CLUB MEMORY
club_owners = []
club_djs = []

# 🎭 moods
MOODS = [
    "playful",
    "calm",
    "wild",
    "sarcastic",
    "night"
]


# =========================
# 🔴 STOP SYSTEM
# =========================

def trigger_stop():
    global stop_until
    stop_until = time.time() + 600


def can_talk():
    return time.time() >= stop_until


# =========================
# 🟢 SESSION
# =========================

def open_session(user):
    global active_session_user, session_until

    active_session_user = user
    session_until = time.time() + 90


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
# 🎭 MOOD ENGINE
# =========================

def random_mood():
    return random.choice(MOODS)


# =========================
# 🎧 DJ / OWNER MEMORY
# =========================

def remember_people(msg):

    global club_owners, club_djs

    text = msg.lower()

    # owner
    if "овнер" in text or "owner" in text:

        words = msg.split()

        if len(words) >= 2:
            name = words[-1]

            if name not in club_owners:
                club_owners.append(name)

    # dj
    if "діджей" in text or "dj" in text:

        words = msg.split()

        if len(words) >= 2:
            name = words[-1]

            if name not in club_djs:
                club_djs.append(name)


# =========================
# 😂 REACTION ENGINE
# =========================

def reaction_reply(msg):

    text = msg.lower()

    reactions = {

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
            "сміх — це вже хороший знак 😏"
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
# 🎭 MAIN BRAIN
# =========================

class LunaBrain:

    def __init__(self):

        self.book = []
        self.last_responses = []

        try:
            with open("luna_book.txt", "r", encoding="utf-8") as f:
                self.book = [
                    x.strip()
                    for x in f
                    if x.strip()
                ]

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
    # 💬 REPLY ENGINE
    # =========================

    def reply(self, user, msg):

        msg_l = msg.lower()

        # 🔴 stop
        if "stop" in msg_l or "луна стоп" in msg_l:
            trigger_stop()
            return "окей… мовчу 😌"

        if not can_talk():
            return ""

        session_tick()

        # 🟢 open session
        if "луна" in msg_l or "luna" in msg_l:
            open_session(user)

        # 🧠 remember people
        remember_people(msg)

        # 🔵 session logic
        if not in_session(user):

            if random.random() < 0.02:
                return random.choice([
                    "я тут 👀",
                    "ніч ще жива 🌙",
                    "клуб слухає 🎧"
                ])

            return ""

        update_activity()

        # 🧠 learn
        learn_from_chat(user, msg)

        # 🎭 mood
        mood = random_mood()

        # 😂 direct reaction
        react = reaction_reply(msg)

        if react:
            return react

        # 📚 memory
        memory = ""

        if random.random() < 0.45:
            memory_raw = get_random_memory()

            if memory_raw and "]" in memory_raw:
                memory = memory_raw.split("]", 1)[1].strip()

        # 📚 book
        book_pick = ""

        if self.book:
            book_pick = random.choice(self.book)

        pool = []

        if memory:
            pool.append(memory)

        if book_pick:
            pool.append(book_pick)

        # 👑 owners
        if "овнер" in msg_l or "owner" in msg_l:

            if club_owners:
                return f"я знаю хто тут головний 😏 {random.choice(club_owners)}"

        # 🎧 djs
        if "діджей" in msg_l or "dj" in msg_l:

            if club_djs:
                return f"сьогодні вайб робить {random.choice(club_djs)} 🔥"

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
        response = ""

        if filtered_pool:
            response = pick_response(filtered_pool, [], msg)

        if not response and filtered_pool:
            response = random.choice(filtered_pool)

        # 🎭 mood inject
        if mood == "playful":
            if random.random() < 0.3:
                response += " 😏"

        elif mood == "wild":
            if random.random() < 0.3:
                response += " 🔥"

        elif mood == "night":
            if random.random() < 0.3:
                response += " 🌙"

        # 🔁 anti-repeat
        if response in self.last_responses:

            response = random.choice([
                "ти сьогодні цікавий 😏",
                "я за тобою спостерігаю 👀",
                "вайб сьогодні дивний 🌙",
                "клуб не спить 🎧"
            ])

        self.last_responses.append(response)

        if len(self.last_responses) > 8:
            self.last_responses.pop(0)

        if not response:
            response = random.choice([
                "я слухаю 😌",
                "цікаво говориш 👀",
                "атмосфера змінюється 🔥"
            ])

        return response


# =========================
# 🚀 INSTANCE
# =========================

luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)
