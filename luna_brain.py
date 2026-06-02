import random
import re
import time

from luna_memory import learn_from_chat, get_random_memory, get_related_memory
from luna_time import get_time_message
from luna_wiki import get_wiki_answer, should_use_wiki


# =========================
# 🔥 GLOBAL
# =========================

last_live_time = 0
next_live_delay = random.randint(180, 360)
chat_activity = 0

last_time_message = 0
TIME_COOLDOWN = 1800

last_wiki_time = 0
WIKI_COOLDOWN = 20

active_session_user = None
session_until = 0

stop_until = 0
last_activity_time = time.time()


# =========================
# 🎧 PARTY
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
# 👤 USER
# =========================

def clean_username(name):
    bad_words = ["resident", "guest", "user"]
    words = name.split()
    clean = [w for w in words if w.lower() not in bad_words]
    return clean[0] if clean else name


# =========================
# 🟢 SESSION
# =========================

def open_session(user):
    global active_session_user, session_until
    active_session_user = user
    session_until = time.time() + 120


def in_session(user):
    return active_session_user == user and time.time() < session_until


def session_tick():
    global active_session_user, session_until
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
# 😂 REACTIONS
# =========================

def reaction_reply(msg):

    text = msg.lower()

    reactions = {
        "привіт": ["привіт 😏", "о привіт 👀"],
        "привет": ["привет 😏", "о привет 👀"],
        "ніч": ["ніч тільки розігрівається 🌙"],
        "музика": ["сьогодні музика качає 🎧"],
        "dj": ["DJ сьогодні в ударі 🔥"]
    }

    for key in reactions:
        if key in text:
            return random.choice(reactions[key])

    return None


# =========================
# 🔥 LIVE PHRASE
# =========================

def build_live_phrase():

    parts = []

    for _ in range(3):

        memory = get_random_memory()

        if not memory:
            continue

        if len(memory) < 5 or len(memory) > 120:
            continue

        parts.append(memory)

    if parts:
        return f"{random.choice(parts)} {random.choice(['😏','👀','🔥'])}"

    return random.choice(["мм… 😏", "цікаво 👀"])


# =========================
# 🧠 BRAIN
# =========================

class LunaBrain:

    def __init__(self):
        self.last_responses = []
        self.user_topics = {}

    def remember_response(self, text):
        if not text:
            return
        self.last_responses.append(text)
        if len(self.last_responses) > 10:
            self.last_responses.pop(0)

    def reply(self, user, msg):

        global last_live_time, next_live_delay, chat_activity
        global last_time_message, last_wiki_time

        msg_l = msg.lower().strip()
        now = time.time()

        # 🔥 user memory
        if user not in self.user_topics:
            self.user_topics[user] = []

        self.user_topics[user].append(msg)

        if len(self.user_topics[user]) > 10:
            self.user_topics[user].pop(0)

        chat_activity += 1

        is_direct = ("луна" in msg_l or "luna" in msg_l)

        # learn
        bad_parts = ["joined", "left", "http", ".com", "teleport"]

        if (
            len(msg) > 4
            and len(msg) < 180
            and not any(x in msg_l for x in bad_parts)
        ):
            learn_from_chat(user, msg)

        session_tick()

        # STOP
        if msg_l in ["stop", "луна стоп"]:
            trigger_stop()
            update_activity()
            return "окей… мовчу 😌"

        if not can_talk():
            return ""

        # не лізти
        if not is_direct and not in_session(user):
            if random.random() < 0.9:
                return ""

        if is_direct:
            open_session(user)

        # =========================
        # 💬 SIMPLE DIALOG
        # =========================

        if is_direct:

            if any(x in msg_l for x in ["як поживаєш","як справи","як ти"]):
                return random.choice([
                    "у мене все добре 😏",
                    "та потроху живу 🎧",
                    "слухаю музику і чат 👀",
                    "ніч проходить цікаво 😌"
                ])

            if "шо нового" in msg_l or "що нового" in msg_l:
                return random.choice([
                    "та нічого особливого 😏",
                    "спостерігаю за вами 👀",
                    "слухаю чат і запам’ятовую 😌"
                ])

            if "хто сьогодні діджеє" in msg_l:
                return random.choice([
                    "сьогодні музика точно качає 🎧",
                    "схоже діджей у хорошому настрої 😏"
                ])

            if "який зараз час" in msg_l:
                tm = time.localtime()
                return f"Зараз {tm.tm_hour:02d}:{tm.tm_min:02d} 😏"

        # =========================
        # 🌍 WIKI (ПІДСИЛЕНИЙ)
        # =========================

        if (
            should_use_wiki(msg)
            or "що таке" in msg_l
            or "шо таке" in msg_l
            or "хто такий" in msg_l
        ):

            if now - last_wiki_time > WIKI_COOLDOWN:

                wiki = get_wiki_answer(msg)

                if wiki:

                    last_wiki_time = now

                    final = f"{clean_username(user)} 😏 {wiki}"

                    update_activity()
                    self.remember_response(final)
                    return final

        # ❗ якщо питання — не нести дічь
        if "?" in msg and not should_use_wiki(msg):
            if not is_direct:
                return ""

        # =========================
        # 🧠 MEMORY
        # =========================

        memory = get_related_memory(msg)

        if memory and memory.lower() in msg_l:
            memory = None

        if not memory:
            memory = get_random_memory()

        if memory:

            if not is_direct and not in_session(user):
                if random.random() < 0.85:
                    return ""

            response = random.choice([
                memory,
                f"ммм 😏 {memory}",
                f"цікаво… {memory}",
                f"👀 {memory}"
            ])

        else:

            if not is_direct:
                return ""

            response = random.choice([
                "я думаю над цим 😏",
                "цікаве питання 👀",
                "хмм… дай секунду 😌",
                "ти змусив мене задуматись 😏"
            ])

        final = f"{clean_username(user)} 😏 {response}"

        if final in self.last_responses:
            final += f" {random.choice(['😏','👀','🔥'])}"

        update_activity()
        self.remember_response(final)

        return final


# =========================
# 🚀 START
# =========================

luna = LunaBrain()

def handle_message(user, message):
    return luna.reply(user, message)
