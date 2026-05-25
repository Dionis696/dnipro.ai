import random
import re
import time

from luna_memory import learn_from_chat, get_random_memory
from luna_mixer import pick_response
from luna_time import get_time_data
from luna_time import get_time_message


# 🔥 LIVE CONTROL
last_live_time = 0
LIVE_COOLDOWN_MIN = 180   # 3 хв
LIVE_COOLDOWN_MAX = 360   # 6 хв
next_live_delay = random.randint(LIVE_COOLDOWN_MIN, LIVE_COOLDOWN_MAX)

chat_activity = 0


party_lines = [
    "🎧 IN THE MIX 🔥",
    "Dnipro Club на зв’язку 😎",
    "музику гучніше 🎧🔥",
    "танцпол горить 💃",
    "всім гарного настрою 😏"
]


last_auto_time = 0
auto_cooldown = 60


def clean_username(name):
    bad_words = ["resident", "guest", "user"]
    words = name.split()
    clean = [w for w in words if w.lower() not in bad_words]

    if not clean:
        return name

    return clean[0]


# 🔥 LIVE ФРАЗА (МІКС MEMORY + BOOK)
def build_live_phrase():

    parts = []

    # беремо 2-3 шматки
    for _ in range(random.randint(2, 3)):
        memory = get_random_memory()

        if not memory:
            continue

        if "]" in memory:
            memory = memory.split("]", 1)[1].strip()

        # ❌ фільтр сміття
        if len(memory) < 5:
            continue

        if any(x in memory.lower() for x in ["привіт", "hello", "зайшов"]):
            continue

        if re.search(r"[A-Z][a-z]+", memory):  # імена типу Asfarula
            continue

        parts.append(memory)

    if not parts:
        return None

    base = random.choice(parts)

    if len(parts) > 1:
        extra = random.choice(parts)
        if extra != base:
            phrase = f"{base}… {extra}"
        else:
            phrase = base
    else:
        phrase = base

    # емоція
    emoji = random.choice(["😏", "👀", "🔥", "😌"])

    return f"{phrase} {emoji}"


active_session_user = None
session_until = 0
session_lang = "ua"

stop_until = 0
last_activity_time = time.time()


def trigger_stop():
    global stop_until, active_session_user, session_until
    stop_until = time.time() + 600
    active_session_user = None
    session_until = 0


def can_talk():
    return time.time() >= stop_until


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


def update_activity():
    global last_activity_time
    last_activity_time = time.time()


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


def reaction_reply(msg):
    text = msg.lower()

    reactions = {
        "привіт": ["привіт 😏", "о привіт 👀"],
        "привет": ["привет 😏", "о привет 👀"],
        "дура": ["сама ти бешкетниця 😏", "ой все 😎"],
        "ніч": ["ніч тільки розігрівається 🌙"],
    }

    for key in reactions:
        if key in text:
            return random.choice(reactions[key])

    return None


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

        global last_auto_time
        global last_live_time
        global next_live_delay
        global chat_activity

        msg_l = msg.lower()

        chat_activity += 1

        # 🔇 стоп
        if re.search(r"\bstop\b", msg_l) or "луна стоп" in msg_l:
            trigger_stop()
            return "окей… мовчу 😌"

        if not can_talk():
            return ""

        session_tick()

        # 🕒 час
        time_msg = get_time_message()

        # ❗ НЕ В СЕСІЇ
        if not in_session(user):

            # реакція
            react = reaction_reply(msg)
            if react:
                return react

            # час
            if time_msg:
                return time_msg

            # 🔥 LIVE режим (головне)
            now = time.time()

            if now - last_live_time > next_live_delay:

                if chat_activity > random.randint(5, 12):

                    phrase = build_live_phrase()

                    if phrase:
                        last_live_time = now
                        next_live_delay = random.randint(LIVE_COOLDOWN_MIN, LIVE_COOLDOWN_MAX)
                        chat_activity = 0
                        return phrase

            return ""

        # ✅ В СЕСІЇ
        update_activity()

        react = reaction_reply(msg)
        if react:
            return react

        # памʼять (інколи)
        if random.random() < 0.2:
            phrase = build_live_phrase()
            if phrase:
                return phrase

        return ""


luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)
