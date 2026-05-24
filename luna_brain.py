import random
import re
import time

from luna_memory import learn_from_chat, get_random_memory, get_memory_with_user
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

party_trigger_count = 0
last_party_time = 0


# 🔥 CLEAN NAME (FIX Resident)
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
    return active_session_user == user and time.time() < session_until


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
            "зате весела 😌",
            "ой все 😎"
        ],

        "ніч": [
            "ніч тільки розігрівається 🌙",
            "вночі тут інший світ 😌"
        ],

        "ааа": [
            "не кричи 😄",
            "шо сталося 😏",
            "ти мене лякаєш 😂"
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
            return [x.strip() for x in f if x.strip()]

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

        # 🔥 PARTY
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

        if not in_session(user):

            react = reaction_reply(msg)

            if react:
                return react

            return ""

        update_activity()

        learn_party(msg)
        chat_counter += 1

        learn_from_chat(user, msg)

        react = reaction_reply(msg)

        if react:

            if react in self.last_responses:
                react = None

            else:

                self.last_responses.append(react)

                if len(self.last_responses) > 8:
                    self.last_responses.pop(0)

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

            # 🔥 ЗГАДКА ГРАВЦЯ
            if random.random() < 0.25:

                mem_user, mem_text = get_memory_with_user()

                if mem_user and mem_text:

                    clean_mem_user = clean_username(mem_user)

                    if clean_mem_user.lower() != clean_username(user).lower():

                        variants = [
                            f"{clean_mem_user} 😏 ти ж казав що {mem_text} — ще так?",
                            f"{clean_mem_user} 👀 ти серйозно це писав: {mem_text}?",
                            f"{clean_mem_user} 😏 пам’ятаю ти казав: {mem_text}",
                            f"{clean_mem_user} 😌 а ти досі так думаєш: {mem_text}?",
                            f"{clean_mem_user} 🔥 ти це тоді зарядив: {mem_text}"
                        ]

                        return random.choice(variants)

        pool = []

        if book_pick:
            pool.append(book_pick)

        if memory:
            pool.append(memory)

        if not pool:

            fallback = [
                "ти мене перевіряєш? 😏",
                "хмм... цікаво 👀",
                "ну ти й загадковий 😄",
                "тааа... навіть не знаю шо сказати 😅",
                "я ще думаю над цим 🤔",
                "ого 😏",
                "ммм... інтригує 😎",
                "ну і ситуація 😂",
                "ти сьогодні в ударі 😄",
                "ахах, оце ти видав 😆"
            ]

            return random.choice(fallback)

        response = pick_response(pool, [], msg)

        if not response:
            response = random.choice(pool)

        # 🔥 підстановка ніку
        clean_user = clean_username(user)

        response = response.replace("{user}", clean_user)

        if random.random() < 0.6:
            response = f"{clean_user} 😏 {response}"

        return response


luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)
