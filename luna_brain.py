import random
import re
import time

from luna_memory import learn_from_chat, get_random_memory
from luna_mixer import pick_response
from luna_time import get_time_message
from luna_wiki import get_wiki_answer, should_use_wiki


# =========================
# 🔥 LIVE CONTROL
# =========================

last_live_time = 0

LIVE_COOLDOWN_MIN = 180
LIVE_COOLDOWN_MAX = 360

next_live_delay = random.randint(
    LIVE_COOLDOWN_MIN,
    LIVE_COOLDOWN_MAX
)

chat_activity = 0


# =========================
# 🕒 TIME CONTROL
# =========================

last_time_message = 0
TIME_COOLDOWN = 1800


# =========================
# 🌍 WIKI CONTROL
# =========================

last_wiki_time = 0
WIKI_COOLDOWN = 15


# =========================
# 🧠 SESSION
# =========================

active_session_user = None
session_until = 0

stop_until = 0

last_activity_time = time.time()


# =========================
# 🔥 PARTY LINES
# =========================

party_lines = [

    "🎧 IN THE MIX 🔥",
    "Dnipro Club на зв’язку 😎",
    "музику гучніше 🎧🔥",
    "танцпол горить 💃",
    "бас качає сьогодні 🔥",
    "ніч тільки починається 😎",
    "DJ тримає хвилю 🎧",
    "танцюємо далі 💃",
    "клуб живе музикою 😏"
]


# =========================
# 👤 CLEAN USER
# =========================

def clean_username(name):

    bad_words = ["resident", "guest", "user"]

    words = name.split()

    clean = [
        w for w in words
        if w.lower() not in bad_words
    ]

    return clean[0] if clean else name


# =========================
# 🟢 SESSION
# =========================

def open_session(user):

    global active_session_user
    global session_until

    active_session_user = user
    session_until = time.time() + 120


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
# 🔴 STOP
# =========================

def trigger_stop():

    global stop_until

    stop_until = time.time() + 600


def can_talk():

    return time.time() >= stop_until


# =========================
# 🟡 ACTIVITY
# =========================

def update_activity():

    global last_activity_time

    last_activity_time = time.time()


# =========================
# 🌙 IDLE
# =========================

def check_idle():

    global last_activity_time

    if time.time() - last_activity_time > 600:

        update_activity()

        return random.choice([

            "хтось ще не спить? 👀",
            "ніч сьогодні дивна 😏",
            "музика ще жива 🎧",
            "Dnipro Club не спить 🔥"
        ])

    return None


# =========================
# 🔥 LIVE PHRASE
# =========================

def build_live_phrase():

    parts = []

    for _ in range(random.randint(2, 3)):

        memory = get_random_memory()

        if not memory:
            continue

        if "]" in memory:
            memory = memory.split("]", 1)[1].strip()

        if len(memory) < 5:
            continue

        if len(memory) > 120:
            continue

        if any(char.isdigit() for char in memory):
            continue

        if len(memory.split()) < 2:
            continue

        parts.append(memory)

    if parts:

        base = random.choice(parts)

        extra_choices = [
            x for x in parts
            if x != base
        ]

        if extra_choices:

            extra = random.choice(extra_choices)

            phrase = f"{base}… {extra}"

        else:
            phrase = base

        return f"{phrase} {random.choice(['😏','👀','🔥','😌'])}"

    return random.choice([

        "мм… 😏",
        "цікаво 👀",
        "тааак 😌"
    ])


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


    def remember_response(self, text):

        if not text:
            return

        self.last_responses.append(text)

        if len(self.last_responses) > 10:
            self.last_responses.pop(0)


    def reply(self, user, msg):

        global last_live_time
        global next_live_delay
        global chat_activity

        global last_time_message
        global last_wiki_time

        msg_l = msg.lower()

        chat_activity += 1

        learn_from_chat(user, msg)

        session_tick()

        # =========================
        # 🔴 STOP
        # =========================

        if msg_l.strip() in ["stop", "луна стоп"]:

            trigger_stop()

            return "окей… мовчу 😌"

        if not can_talk():
            return ""

        # =========================
        # 🟢 SESSION START
        # =========================

        if "луна" in msg_l or "luna" in msg_l:

            open_session(user)

        # =========================
        # 🌍 WIKI MODE
        # =========================

        if (
            should_use_wiki(msg)
            and len(msg.split()) >= 2
        ):

            now = time.time()

            if now - last_wiki_time > WIKI_COOLDOWN:

                wiki = get_wiki_answer(msg)

                if wiki:

                    last_wiki_time = now

                    clean_user = clean_username(user)

                    intro = random.choice([

                        "я десь таке читала 😏",
                        "ммм… цікава тема 👀",
                        "зараз поясню 😌",
                        "о це я знаю 🔥"
                    ])

                    final = f"{clean_user} 😏 {intro} {wiki}"

                    if final in self.last_responses:
                        final += " 👀"

                    update_activity()

                    self.remember_response(final)

                    return final

        # =========================
        # 😂 REACTION
        # =========================

        react = reaction_reply(msg)

        if react:

            if react not in self.last_responses:

                update_activity()

                self.remember_response(react)

                return react

        # =========================
        # 🔥 LIVE
        # =========================

        now = time.time()

        if now - last_live_time > next_live_delay:

            if chat_activity >= 3:

                if random.random() < 0.45:

                    phrase = random.choice(party_lines)

                else:

                    phrase = build_live_phrase()

                if phrase in self.last_responses:
                    phrase += f" {random.choice(['😏','🔥'])}"

                update_activity()

                self.remember_response(phrase)

                last_live_time = now

                next_live_delay = random.randint(
                    LIVE_COOLDOWN_MIN,
                    LIVE_COOLDOWN_MAX
                )

                chat_activity = 0

                return phrase

        # =========================
        # 🕒 TIME
        # =========================

        time_msg = get_time_message()

        if time_msg:

            now = time.time()

            if now - last_time_message > TIME_COOLDOWN:

                last_time_message = now

                if time_msg in self.last_responses:
                    time_msg += f" {random.choice(['😏','👀'])}"

                update_activity()

                self.remember_response(time_msg)

                return time_msg

        # =========================
        # 🌙 SESSION MODE
        # =========================

        if in_session(user):

            if random.random() < 0.35:

                phrase = build_live_phrase()

                if phrase not in self.last_responses:

                    update_activity()

                    self.remember_response(phrase)

                    return phrase

        # =========================
        # 🧠 MEMORY
        # =========================

        memory = get_random_memory()

        if memory:

            if "]" in memory:
                memory = memory.split("]", 1)[1].strip()

            response = memory

        else:

            response = random.choice([

                "ти мене перевіряєш? 😏",
                "хмм... цікаво 👀",
                "ну ти й загадковий 😄",
                "ого 😏"
            ])

        clean_user = clean_username(user)

        final = f"{clean_user} 😏 {response}"

        if final in self.last_responses:

            final = random.choice([

                f"{clean_user} 😏 цікаво...",
                f"{clean_user} 👀 ти сьогодні активний",
                f"{clean_user} 🔥 ого"
            ])

        update_activity()

        self.remember_response(final)

        return final


# 🚀 START

luna = LunaBrain()


def handle_message(user, message):

    return luna.reply(user, message)
