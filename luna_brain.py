import random
import re
import time

from luna_memory import learn_from_chat, get_random_memory
from luna_mixer import pick_response
from luna_time import get_time_message


# 🔥 LIVE CONTROL
last_live_time = 0

LIVE_COOLDOWN_MIN = 180
LIVE_COOLDOWN_MAX = 360

next_live_delay = random.randint(
    LIVE_COOLDOWN_MIN,
    LIVE_COOLDOWN_MAX
)

chat_activity = 0


# 🔥 PARTY LINES
party_lines = [
    "🎧 IN THE MIX 🔥",
    "Dnipro Club на зв’язку 😎",
    "музику гучніше 🎧🔥",
    "танцпол горить 💃",
    "всім гарного настрою 😏",
    "бас качає сьогодні 🔥",
    "ніч тільки починається 😎",
    "DJ тримає хвилю 🎧",
    "танцюємо далі 💃",
    "клуб живе музикою 😏"
]


# 🔥 AUTO LIVE
last_auto_time = 0
auto_cooldown = 60


# =========================
# 🔥 CLEAN USERNAME
# =========================

def clean_username(name):

    bad_words = ["resident", "guest", "user"]

    words = name.split()

    clean = [
        w for w in words
        if w.lower() not in bad_words
    ]

    if not clean:
        return name

    return clean[0]


# =========================
# 🔥 LIVE PHRASE
# =========================

def build_live_phrase():

    mode = random.random()

    # 1️⃣ MEMORY
    if mode < 0.4:

        memory = get_random_memory()

        if memory and "]" in memory:
            memory = memory.split("]", 1)[1].strip()

        if memory and len(memory) > 5:
            return memory

    # 2️⃣ MIX
    parts = []

    for _ in range(random.randint(2, 3)):

        memory = get_random_memory()

        if not memory:
            continue

        if "]" in memory:
            memory = memory.split("]", 1)[1].strip()

        if len(memory) < 5:
            continue

        # 🚫 сміття
        if any(
            x in memory.lower()
            for x in [
                "привіт",
                "hello",
                "зайшов"
            ]
        ):
            continue

        # 🚫 дивні імена
        if re.search(r"[A-Z][a-z]+", memory):
            continue

        parts.append(memory)

    if parts:

        base = random.choice(parts)

        if len(parts) > 1:

            extra = random.choice(parts)

            if extra != base:
                phrase = f"{base}… {extra}"
            else:
                phrase = base

        else:
            phrase = base

        emoji = random.choice([
            "😏",
            "👀",
            "🔥",
            "😌"
        ])

        return f"{phrase} {emoji}"

    # 3️⃣ fallback
    return random.choice([
        "мм… 😏",
        "👀",
        "цікаво…",
        "тааак 😌",
        "дивно 😏"
    ])


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
        active_session_user == user
        and
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

        phrase = build_live_phrase()

        if phrase:
            return phrase

        return random.choice([
            "ніч сьогодні дивна 🌙",
            "клуб трохи затих 😌",
            "музика ще жива 🎧",
            "хтось ще не спить? 👀"
        ])

    return None


# =========================
# 😂 REACTIONS
# =========================

def reaction_reply(msg):

    text = msg.lower()

    reactions = {

        "привіт": [
            "привіт 😏",
            "о привіт 👀"
        ],

        "привет": [
            "привет 😏",
            "о привет 👀"
        ],

        "дура": [
            "сама ти бешкетниця 😏",
            "ой все 😎"
        ],

        "ніч": [
            "ніч тільки розігрівається 🌙"
        ],

        "музика": [
            "сьогодні музика качає 🎧"
        ],

        "dj": [
            "DJ сьогодні в ударі 🔥"
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

        global last_live_time
        global next_live_delay
        global chat_activity

        msg_l = msg.lower()

        chat_activity += 1

        # 🔴 STOP
        if (
            re.search(r"\bstop\b", msg_l)
            or
            "луна стоп" in msg_l
        ):

            trigger_stop()

            return "окей… мовчу 😌"

        # 🚫 muted
        if not can_talk():
            return ""

        session_tick()

        # 🔥 OPEN SESSION
        if "луна" in msg_l or "luna" in msg_l:

            detected_lang = self.detect_lang(msg)

            open_session(
                user,
                detected_lang
            )

        # 🕒 TIME
        time_msg = get_time_message()

        # ❗ НЕ В СЕСІЇ
        if not in_session(user):

            # 😂 reactions
            react = reaction_reply(msg)

            if react:

                if react not in self.last_responses:

                    self.last_responses.append(react)

                    if len(self.last_responses) > 8:
                        self.last_responses.pop(0)

                    return react

            # 🕒 time
            if time_msg and random.random() < 0.25:
                return time_msg

            # 🔥 PARTY RANDOM
            if (
                random.random() < 0.05
                and
                any(
                    x in msg_l
                    for x in [
                        "dj",
                        "music",
                        "party",
                        "🔥",
                        "🎧"
                    ]
                )
            ):
                return random.choice(party_lines)

            # 🔥 LIVE MODE
            now = time.time()

            if now - last_live_time > next_live_delay:

                if chat_activity > random.randint(5, 12):

                    phrase = build_live_phrase()

                    if phrase:

                        last_live_time = now

                        next_live_delay = random.randint(
                            LIVE_COOLDOWN_MIN,
                            LIVE_COOLDOWN_MAX
                        )

                        chat_activity = 0

                        return phrase

            return ""

        # ✅ В СЕСІЇ
        update_activity()

        # 💾 memory save
        learn_from_chat(user, msg)

        # 😂 reaction
        react = reaction_reply(msg)

        if react:

            if react not in self.last_responses:

                self.last_responses.append(react)

                if len(self.last_responses) > 8:
                    self.last_responses.pop(0)

                return react

        # 🔥 PARTY
        if random.random() < 0.08:
            return random.choice(party_lines)

        # 🔥 LIVE MEMORY
        if random.random() < 0.2:

            phrase = build_live_phrase()

            if phrase:
                return phrase

        # 🔥 BOOK + MEMORY MIX
        memory = get_random_memory()

        if memory and "]" in memory:
            memory = memory.split("]", 1)[1].strip()

        pool = []

        if memory:
            pool.append(memory)

        if not pool:

            fallback = [
                "ти мене перевіряєш? 😏",
                "хмм... цікаво 👀",
                "ну ти й загадковий 😄",
                "тааа... навіть не знаю шо сказати 😅",
                "ого 😏",
                "ммм... інтригує 😎"
            ]

            return random.choice(fallback)

        response = pick_response(
            pool,
            [],
            msg
        )

        if not response:
            response = random.choice(pool)

        clean_user = clean_username(user)

        response = response.replace(
            "{user}",
            clean_user
        )

        if random.random() < 0.5:
            response = f"{clean_user} 😏 {response}"

        return response


# =========================
# 🚀 START
# =========================

luna = LunaBrain()


def handle_message(user, message):

    return luna.reply(
        user,
        message
    )
