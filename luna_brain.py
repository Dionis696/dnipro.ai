import random
import re
import time

from luna_memory import learn_from_chat, get_random_memory
from luna_mixer import pick_response
from luna_time import get_time_message
from luna_wiki import get_wiki_answer, should_use_wiki


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


def clean_username(name):
    bad_words = ["resident", "guest", "user"]
    words = name.split()
    clean = [w for w in words if w.lower() not in bad_words]
    return clean[0] if clean else name


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

        if len(parts) > 1:
            extra_choices = [x for x in parts if x != base]

            if extra_choices:
                extra = random.choice(extra_choices)
                phrase = f"{base}… {extra}"
            else:
                phrase = base
        else:
            phrase = base

        return f"{phrase} {random.choice(['😏','👀','🔥','😌'])}"

    return random.choice([
        "мм… 😏",
        "👀",
        "цікаво…",
        "тааак 😌"
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
# 🔴 STOP
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
# 🌙 IDLE
# =========================

def check_idle():
    global last_activity_time

    if time.time() - last_activity_time > 600:
        update_activity()
        return build_live_phrase()

    return None


# =========================
# 😂 REACTIONS
# =========================

def reaction_reply(msg):

    text = msg.lower()

    reactions = {
        "привіт": ["привіт 😏", "о привіт 👀"],
        "привет": ["привет 😏", "о привет 👀"],
        "дура": ["сама ти бешкетниця 😏", "ой все 😎"],
        "ніч": ["ніч тільки розігрівається 🌙"],
        "музика": ["сьогодні музика качає 🎧"],
        "dj": ["DJ сьогодні в ударі 🔥"]
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

        if "..." in text and ":" in text:
            return

        self.last_responses.append(text)

        if len(self.last_responses) > 10:
            self.last_responses.pop(0)

    def detect_lang(self, text):
        text = text.lower()

        ua = len(re.findall(r"[іїєґ]", text))
        ru = len(re.findall(r"[ыэъё]", text))
        en = len(re.findall(r"[a-z]", text))

        if ua > 0:
            return "ua"
        if ru > ua and ru > 0:
            return "ru"
        if en > 2:
            return "en"

        return "ua"

    def reply(self, user, msg):

        global last_live_time
        global next_live_delay
        global chat_activity

        msg_l = msg.lower()
        chat_activity += 1

        learn_from_chat(user, msg)

        # 🔴 STOP
        if msg_l.strip() in ["stop", "луна стоп"]:
            trigger_stop()
            return "окей… мовчу 😌"

        if not can_talk():
            return ""

        session_tick()

        if "луна" in msg_l or "luna" in msg_l:
            open_session(user, self.detect_lang(msg))

        now = time.time()

        # 🔥🔥🔥 WIKI (БЕЗ БЛОКІВ І РАНДОМУ)
        if should_use_wiki(msg):

            wiki = get_wiki_answer(msg)

            if wiki:
                final = f"{clean_username(user)} 😏 {wiki}"
                self.remember_response(final)
                return final

        # 🔥 TIME
        time_msg = get_time_message()
        if time_msg and time_msg not in self.last_responses:
            self.remember_response(time_msg)
            return time_msg

        # ❗ НЕ В СЕСІЇ
        if not in_session(user):

            react = reaction_reply(msg)
            if react and react not in self.last_responses:
                self.remember_response(react)
                return react

            if random.random() < 0.05:
                available = [x for x in party_lines if x not in self.last_responses]
                if available:
                    party = random.choice(available)
                    self.remember_response(party)
                    return party

            if now - last_live_time > next_live_delay:
                if chat_activity > random.randint(4, 10):

                    phrase = build_live_phrase()

                    if phrase and phrase not in self.last_responses:
                        self.remember_response(phrase)

                        last_live_time = now
                        next_live_delay = random.randint(LIVE_COOLDOWN_MIN, LIVE_COOLDOWN_MAX)
                        chat_activity = 0

                        return phrase

            idle_msg = check_idle()
            if idle_msg and idle_msg not in self.last_responses:
                self.remember_response(idle_msg)
                return idle_msg

            return ""

        # ✅ В СЕСІЇ
        update_activity()

        react = reaction_reply(msg)
        if react and react not in self.last_responses:
            self.remember_response(react)
            return react

        if random.random() < 0.08:
            available = [x for x in party_lines if x not in self.last_responses]
            if available:
                party = random.choice(available)
                self.remember_response(party)
                return party

        if random.random() < 0.3:
            phrase = build_live_phrase()
            if phrase and phrase not in self.last_responses:
                self.remember_response(phrase)
                return phrase

        memory = get_random_memory()

        if memory and "]" in memory:
            memory = memory.split("]", 1)[1].strip()

        pool = [memory] if memory else []

        if not pool:
            response = random.choice([
                "ти мене перевіряєш? 😏",
                "хмм... цікаво 👀",
                "ну ти й загадковий 😄",
                "ого 😏",
                "ммм... інтригує 😎"
            ])
        else:
            response = pick_response(pool, [], msg) or random.choice(pool)

        clean_user = clean_username(user)

        response = response.replace("{user}", clean_user)

        if clean_user.lower() not in response.lower():
            response = f"{clean_user} 😏 {response}"

        if response in self.last_responses:

            fallback = random.choice([
                "цікаво 😏",
                "ммм 👀",
                "ти сьогодні активний 😄",
                "ого 🔥"
            ])

            final = f"{clean_user} 😏 {fallback}"
            self.remember_response(final)
            return final

        self.remember_response(response)

        return response


# 🚀 START
luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)
