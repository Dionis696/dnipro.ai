import random
import re
import time

from luna_memory import learn_from_chat, get_random_memory, get_memory_with_user
from luna_mixer import pick_response
from luna_time import get_time_data
from luna_time import get_time_message


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
    "🤘 𝓓𝓝𝓘𝓟𝓞 🤘",
    "🎤 МУЗИКУ НА ПОВНУ 🔥"
]

auto_lines = [
    "{user} 😏 ти щось задумав сьогодні",
    "{user} 👀 я тебе бачу… не ховайся",
    "{user} 💃 не стій — танцпол чекає",
    "{user} 😏 ти мовчиш… але я ж відчуваю",
    "{user} 🔥 сьогодні ти явно в вайбі",
    "{user} 😎 з тобою стає цікавіше",
    "{user} 😏 не роби вигляд що ти випадково тут",
    "{user} 👀 я за тобою спостерігаю",
    "{user} 💋 ти сьогодні підозріло тихий",
    "{user} 😏 скажи щось… я ж чекаю"
]

time_lines = [
    "а ви в курсі що зараз {day} 👀 і вже {time}… ніч тільки починається 😏",
    "зараз {time} 😏 саме час для двіжу",
    "сьогодні {day} 😎 і атмосфера вже інша",
    "ммм… {time} 👀 і тут стає цікавіше",
    "на годиннику {time} 🔥 саме те шо треба для туси"
]

chat_counter = 0
learned_party = []

party_trigger_count = 0
last_party_time = 0

last_auto_time = 0
auto_cooldown = 40

last_time_event = 0


def clean_username(name):
    bad_words = ["resident", "guest", "user"]
    words = name.split()
    clean = [w for w in words if w.lower() not in bad_words]

    if not clean:
        return name

    return clean[0]


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


active_session_user = None
session_until = 0
session_lang = "ua"

stop_until = 0
last_activity_time = time.time()

club_owners = []
club_djs = []


def trigger_stop():
    global stop_until
    global active_session_user
    global session_until

    stop_until = time.time() + 600
    active_session_user = None
    session_until = 0


def can_talk():
    return time.time() >= stop_until


def open_session(user, lang):
    global active_session_user
    global session_until
    global session_lang

    active_session_user = user
    session_until = time.time() + 60
    session_lang = lang


def in_session(user):
    return active_session_user == user and time.time() < session_until


def session_tick():
    global active_session_user
    global session_until

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
        "дура": ["сама ти бешкетниця 😏", "зате весела 😌", "ой все 😎"],
        "ніч": ["ніч тільки розігрівається 🌙", "вночі тут інший світ 😌"],
        "ааа": ["не кричи 😄", "шо сталося 😏", "ти мене лякаєш 😂"]
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

        global session_lang
        global last_auto_time

        msg_l = msg.lower()

        if re.search(r"\bstop\b", msg_l) or "луна стоп" in msg_l:
            trigger_stop()
            return "окей… мовчу 😌"

        if not can_talk():
            return ""

        session_tick()

        # ✅ TIME ТІЛЬКИ ЯК ФОНОВИЙ (НЕ ЛОМАЄ ЛОГІКУ)
        time_msg = get_time_message()

        if not in_session(user):

            react = reaction_reply(msg)
            if react:
                return react

            if time_msg:
                return time_msg

            if time.time() - last_auto_time > auto_cooldown:
                if random.random() < 0.07:
                    last_auto_time = time.time()
                    clean_user = clean_username(user)
                    return random.choice(auto_lines).replace("{user}", clean_user)

            return ""

        update_activity()

        react = reaction_reply(msg)
        if react:
            return react

        return ""
        

luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)
