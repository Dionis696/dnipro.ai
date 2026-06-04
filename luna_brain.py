import random
import time

from luna_memory import learn_from_chat, get_random_memory, get_related_memory, save_fact, get_fact, clear_old_facts
from luna_wiki import get_wiki_answer, should_use_wiki
from luna_ai import ask_gemini
from luna_time import build_time_phrase

# =========================
# 🔥 GLOBAL
# =========================
last_wiki_time = 0
WIKI_COOLDOWN = 60 
active_session_user = None
session_until = 0
last_activity_time = time.time()

def clean_username(name):
    bad_words = ["resident", "guest", "user"]
    words = name.split()
    clean = [w for w in words if w.lower() not in bad_words]
    return clean[0] if clean else name

def open_session(user):
    global active_session_user, session_until
    active_session_user = user
    session_until = time.time() + 3600

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

        clear_old_facts()

        if not msg_l or msg_l == "ping" or user == "system":
            update_activity()
            return ""

        is_direct = ("луна" in msg_l or "luna" in msg_l)

        # 🧠 ЛОГІКА КОМАНД
        if is_direct:
            # 1. ЗАПИС ФАКТІВ
            if any(cmd in msg_l for cmd in ["запам'ятай", "запиши"]):
                if "діджей" in msg_l:
                    fact = msg.split("діджей")[-1].strip(" ,.:-")
                    return f"{clean_name} 😏 {save_fact('діджей', fact)}"
                if "рекламу" in msg_l:
                    fact = msg.split("рекламу")[-1].strip(" ,.:-")
                    return f"{clean_name} 😏 {save_fact('реклама', fact)}"
            
            # 2. ЧИТАННЯ ФАКТІВ
            if any(q in msg_l for q in ["хто діджей", "який діджей", "діджей сьогодні"]):
                fact = get_fact("діджей")
                return f"{clean_name} 😏 За моїми даними, сьогодні за пультом {fact} 🔥" if fact else f"{clean_name} 😏 Я ще не знаю, хто сьогодні діджей 🎧"
            
            if any(q in msg_l for q in ["дай рекламу", "покажи рекламу", "яка реклама"]):
                fact = get_fact("реклама")
                return f"{clean_name} 😏 Ось актуальне: {fact} ✨" if fact else f"{clean_name} 😏 Поки що немає свіжої реклами ✨"
            
            # 3. ЧАС (НОВА КОМАНДА)
            if any(q in msg_l for q in ["котра година", "який час", "скільки часу", "яка зараз година"]):
                return f"{clean_name} 😏 {build_time_phrase()}"

        # Навчання (загальне)
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
                    return f"{clean_name} 😏 {wiki}"

        # 🤖 GROQ API
        if is_direct or in_session(user):
            dj_fact = get_fact("діджей")
            context = f"Пам'ятай, що сьогодні діджей: {dj_fact}. " if dj_fact else ""
            
            response = ask_gemini(clean_name, f"{context} Користувач питає: {msg}")
            
            if response:
                update_activity()
                self.remember_response(response)
                return f"{clean_name} 😏 {response}"

        return ""

luna = LunaBrain()

def handle_message(user, message):
    return luna.reply(user, message)
