import random
import time

from luna_memory import learn_from_chat, get_random_memory, get_related_memory
from luna_wiki import get_wiki_answer, should_use_wiki
from luna_ai import ask_gemini
from luna_time import get_time_message

# =========================
# 🔥 GLOBAL
# =========================

last_wiki_time = 0
WIKI_COOLDOWN = 5

active_session_user = None
session_until = 0

last_activity_time = time.time()

seen_users = set()

def check_new_user(user):
    clean_name = clean_username(user)
    if clean_name not in seen_users:
        seen_users.add(clean_name)
        return random.choice([
            f"О, привіт, {clean_name}! Рада бачити в Dnipro Club 😏🔥",
            f"Хто це до нас завітав? Привіт, {clean_name}! 👋🎧",
            f"Привіт, {clean_name}! Розташовуйся, сьогодні буде спекотно 🔥😎",
            f"Оу, нове обличчя! Вітаю, {clean_name}! 😏✨"
        ])
    return None

def clean_username(name):
    bad_words = ["resident", "guest", "user"]
    words = name.split()
    clean = [w for w in words if w.lower() not in bad_words]
    return clean[0] if clean else name

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

def update_activity():
    global last_activity_time
    last_activity_time = time.time()

def check_idle():
    global last_activity_time
    if time.time() - last_activity_time > 600:
        update_activity()
        return random.choice([
            "хтось ще не спить? 👀",
            "ніч сьогодні жива 😏",
            "бас ще качає 🎧",
            "Dnipro Club не спить 🔥"
        ])
    return None

# =========================
# 🧠 BRAIN
# =========================

class LunaBrain:
    def __init__(self):
        self.last_responses = []
        self.user_topics = {}

    def remember_response(self, text):
        if not text: return
        self.last_responses.append(text)
        if len(self.last_responses) > 10: self.last_responses.pop(0)

    def reply(self, user, msg):
        global last_wiki_time
        msg_l = msg.lower().strip()
        now = time.time()
        clean_name = clean_username(user)

        if not msg_l or msg_l == "ping" or user == "system":
            update_activity()
            return ""

        time_msg = get_time_message()
        if time_msg:
            return f"{clean_name} 😏 {time_msg}"

        is_direct = ("луна" in msg_l or "luna" in msg_l)

        if user not in self.user_topics: self.user_topics[user] = []
        self.user_topics[user].append(msg)
        if len(self.user_topics[user]) > 10: self.user_topics[user].pop(0)

        if 4 < len(msg) < 180:
            learn_from_chat(user, msg)

        session_tick()
        if is_direct: open_session(user)

        # 🌍 WIKI
        if should_use_wiki(msg):
            if now - last_wiki_time > WIKI_COOLDOWN:
                wiki = get_wiki_answer(msg)
                if wiki:
                    last_wiki_time = now
                    update_activity()
                    # Викидаємо нік з вікі-відповіді, щоб не дублювати
                    final = f"{clean_name} 😏 {wiki}"
                    self.remember_response(final)
                    return final

        if not is_direct and not in_session(user):
            return ""

        # 🤖 GROQ API
        response = ask_gemini(clean_name, msg)

        if not response:
            memory = get_related_memory(msg) or get_random_memory()
            response = memory or "щось сьогодні зв'язок плаває 😏"

        # 🧹 АНТИ-ПОВТОР (ігноруємо нік при перевірці повтору)
        if msg_l in response.lower() or response.lower() in msg_l:
            response = get_random_memory() or "таке буває, розкажи щось ще 😏"

        # ФІНАЛЬНА ЗБІРКА (Нік додається лише тут)
        final = f"{clean_name} 😏 {response}"
        update_activity()
        self.remember_response(final)

        return final

luna = LunaBrain()

def handle_message(user, message):
    return luna.reply(user, message)
