import random
import re
import time

from luna_memory import learn_from_chat, get_random_memory
from luna_mixer import pick_response
from luna_time import get_time_data
from luna_time import get_time_message


party_lines = [
    "🎧 IN THE MIX 🔥",
    "Dnipro Club на зв’язку 😎",
    "музику гучніше 🎧🔥",
    "танцпол горить 💃",
    "всім гарного настрою 😏"
]

auto_lines = [
    "{user} 😏 ти щось задумав сьогодні",
    "{user} 👀 я тебе бачу… не ховайся",
    "{user} 💃 не стій — танцпол чекає",
    "{user} 🔥 сьогодні ти явно в вайбі",
    "{user} 😎 з тобою стає цікавіше"
]

time_lines = [
    "а ви в курсі що зараз {day} 👀 і вже {time}… ніч тільки починається 😏",
    "зараз {time} 😏 саме час для двіжу"
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

        msg_l = msg.lower()

        # 🔇 стоп
        if re.search(r"\bstop\b", msg_l) or "луна стоп" in msg_l:
            trigger_stop()
            return "окей… мовчу 😌"

        if not can_talk():
            return ""

        session_tick()

        # 🕒 ЧАС (працює стабільно)
        time_msg = get_time_message()

        # ❗ НЕ В СЕСІЇ (просто чат)
        if not in_session(user):

            # реакції
            react = reaction_reply(msg)
            if react:
                return react

            # час (інколи)
            if time_msg:
                return time_msg

            # авто (дуже рідко)
            if time.time() - last_auto_time > auto_cooldown:
                if random.random() < 0.05:
                    last_auto_time = time.time()
                    clean_user = clean_username(user)
                    return random.choice(auto_lines).replace("{user}", clean_user)

            return ""

        # ✅ В СЕСІЇ
        update_activity()

        react = reaction_reply(msg)
        if react:
            return react

        # памʼять (БЕЗ ІМЕН!)
        memory = get_random_memory()

        if memory and "]" in memory:
            memory = memory.split("]", 1)[1].strip()

        if memory and random.random() < 0.3:
            return memory

        # fallback
        clean_user = clean_username(user)

        return random.choice([
            f"{clean_user} 😏 цікаво",
            f"{clean_user} 👀 я слухаю",
            f"{clean_user} 😎 продовжуй",
            f"{clean_user} 🔥 норм тема"
        ])


luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)
