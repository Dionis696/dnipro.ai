import random
import time
from datetime import datetime
import pytz

# Імпортуємо ваш міксер для вибору фраз із файлів
from luna_mixer import pick_response 
from luna_memory import learn_from_chat, get_random_memory, get_related_memory, save_fact, get_fact, clear_old_facts
from luna_wiki import get_wiki_answer, should_use_wiki
from luna_ai import ask_gemini

# =========================
# 🔥 GLOBAL
# =========================
last_wiki_time = 0
WIKI_COOLDOWN = 60 
# Використовуємо словник для зберігання сесій кожного користувача окремо
active_sessions = {} 
last_activity_time = time.time()

def clean_username(name):
    bad_words = ["resident", "guest", "user"]
    words = name.split()
    clean = [w for w in words if w.lower() not in bad_words]
    return clean[0] if clean else name

def open_session(user):
    global active_sessions
    # Сесія на 180 секунд (3 хвилини) для конкретного користувача
    active_sessions[user] = time.time() + 180 

def in_session(user):
    # Перевіряємо, чи є користувач у списку та чи не вийшов час
    if user in active_sessions:
        if time.time() < active_sessions[user]:
            return True
        else:
            del active_sessions[user]
    return False

def session_tick():
    global active_sessions
    now = time.time()
    # Автоматичне видалення прострочених сесій
    expired = [u for u, t in active_sessions.items() if now > t]
    for u in expired:
        del active_sessions[u]

def update_activity():
    global last_activity_time
    last_activity_time = time.time()

# =========================
# 🧠 BRAIN
# =========================

class LunaBrain:
    def __init__(self):
        self.last_responses = []
        self.user_topics = {}
        try:
            with open("luna_book_ua.txt", "r", encoding="utf-8") as f: self.book = f.readlines()
            with open("luna_memory.txt", "r", encoding="utf-8") as f: self.memory = f.readlines()
        except:
            self.book = ["Привіт! 😏"]
            self.memory = ["Я тут. 🔥"]

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

        # 🧠 1. ЧАС
        if any(q in msg_l for q in ["котра година", "який час", "скільки часу", "яка зараз година", "який зараз час"]):
            kyiv_time = datetime.now(pytz.timezone("Europe/Kyiv")).strftime("%H:%M")
            return f"{clean_name} 😏 Зараз рівно {kyiv_time}. Готова запалювати? 🔥"

        # 🧠 2. ФАКТИ ТА КОМАНДИ
        if is_direct:
            if any(cmd in msg_l for cmd in ["запам'ятай", "запиши"]):
                if "діджей" in msg_l:
                    fact = msg.split("діджей")[-1].strip(" ,.:-")
                    return f"{clean_name} 😏 {save_fact('діджей', fact)}"
                if "рекламу" in msg_l:
                    fact = msg.split("рекламу")[-1].strip(" ,.:-")
                    return f"{clean_name} 😏 {save_fact('реклама', fact)}"
            
            if any(q in msg_l for q in ["хто діджей", "який діджей", "діджей сьогодні"]):
                fact = get_fact("діджей")
                return f"{clean_name} 😏 Сьогодні за пультом {fact} 🔥" if fact else f"{clean_name} 😏 Я ще не знаю, хто сьогодні діджей 🎧"
            
            if any(q in msg_l for q in ["дай рекламу", "покажи рекламу", "яка реклама"]):
                fact = get_fact("реклама")
                return f"{clean_name} 😏 Ось актуальне: {fact} ✨" if fact else f"{clean_name} 😏 Поки що немає свіжої реклами ✨"

        # Навчання
        if user not in self.user_topics: self.user_topics[user] = []
        self.user_topics[user].append(msg)
        if len(self.user_topics[user]) > 10: self.user_topics[user].pop(0)

        if 4 < len(msg) < 180:
            learn_from_chat(user, msg)

        # Оновлення сесій
        session_tick()
        if is_direct: 
            open_session(user)

        # 🌍 WIKI
        if should_use_wiki(msg):
            if now - last_wiki_time > WIKI_COOLDOWN:
                wiki = get_wiki_answer(msg)
                if wiki:
                    last_wiki_time = now
                    update_activity()
                    return f"{clean_name} 😏 {wiki}"

        # 🤖 GROQ API (AI відповіді)
        # Відповідає, якщо звертаються до неї АБО якщо це триває діалог конкретного юзера
        if is_direct or in_session(user):
            update_activity() 
            # Якщо він у сесії, оновлюємо її час (продовжуємо на 3 хв)
            if user in active_sessions:
                open_session(user)
            
            dj_fact = get_fact("діджей")
            context = f"Пам'ятай, що сьогодні діджей: {dj_fact}. " if dj_fact else ""
            
            response = ask_gemini(clean_name, f"{context} Користувач питає: {msg}")
            
            if response:
                self.remember_response(response)
                return f"{clean_name} 😏 {response}"
            else:
                fallback = pick_response(self.book, self.memory, msg)
                return f"{clean_name} 😏 {fallback.strip()}"

        return ""

luna = LunaBrain()

def handle_message(user, message):
    return luna.reply(user, message)
