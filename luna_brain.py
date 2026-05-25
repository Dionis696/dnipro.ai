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


# 🕒 TIME COOLDOWN (🔥 ФІКС)
last_time_talk = 0
TIME_COOLDOWN = 600  # 10 хв


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

        if any(char.isdigit() for char in memory):
            continue

        if len(memory.split()) < 2:
            continue

        parts.append(memory)

    if parts:
        base = random.choice(parts)

        if len(parts) > 1:
            extra = random.choice(parts)
            phrase = f"{base}… {extra}" if extra != base else base
        else:
            phrase = base

        return f"{phrase} {random.choice(['😏','👀','🔥','😌'])}"

    return random.choice([
        "мм… 😏",
        "👀",
        "цікаво…",
        "тааак 😌"
    ])


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
        return build_live_phrase()

    return None


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
        global last_time_talk

        msg_l = msg.lower()
        chat_activity += 1

        learn_from_chat(user, msg)

        if re.search(r"\bstop\b", msg_l) or "луна стоп" in msg_l:
            trigger_stop()
            return "окей… мовчу 😌"

        if not can_talk():
            return ""

        session_tick()

        if "луна" in msg_l or "luna" in msg_l:
            open_session(user, self.detect_lang(msg))

        now = time.time()
        time_msg = get_time_message()

        # 🔥 TIME (всюди працює нормально)
        if (
            time_msg
            and now - last_time_talk > TIME_COOLDOWN
            and random.random() < 0.35
            and time_msg not in self.last_responses
        ):
            last_time_talk = now
            self.last_responses.append(time_msg)
            return time_msg

        # ❗ НЕ В СЕСІЇ
        if not in_session(user):

            react = reaction_reply(msg)
            if react and react not in self.last_responses:
                self.last_responses.append(react)
                return react

            if random.random() < 0.05:
                return random.choice(party_lines)

            if now - last_live_time > next_live_delay:
                if chat_activity > random.randint(4, 10):

                    phrase = build_live_phrase()

                    if phrase and phrase not in self.last_responses:
                        self.last_responses.append(phrase)

                        last_live_time = now
                        next_live_delay = random.randint(LIVE_COOLDOWN_MIN, LIVE_COOLDOWN_MAX)
                        chat_activity = 0

                        return phrase

            idle_msg = check_idle()
            if idle_msg:
                return idle_msg

            return ""

        # ✅ В СЕСІЇ
        update_activity()

        react = reaction_reply(msg)
        if react and react not in self.last_responses:
            self.last_responses.append(react)
            return react

        if random.random() < 0.08:
            party = random.choice(party_lines)
            if party not in self.last_responses:
                self.last_responses.append(party)
                return party

        if random.random() < 0.3:
            phrase = build_live_phrase()
            if phrase and phrase not in self.last_responses:
                self.last_responses.append(phrase)
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
            return ""

        self.last_responses.append(response)

        if len(self.last_responses) > 10:
            self.last_responses.pop(0)

        return response


luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)
