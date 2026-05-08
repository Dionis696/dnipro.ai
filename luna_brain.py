import random
import time

# =========================
# 🧠 MEMORY
# =========================

active_dialogs = {}
DIALOG_TIMEOUT = 180

recent_replies = []
MAX_RECENT = 12

# =========================
# 💬 RESPONSES
# =========================

responses = {
    "UA": {
        "greeting": ["привіт 🙂", "рада тебе бачити", "хей 😉"],
        "question": ["так, слухаю тебе", "розкажи детальніше", "я тут, кажи"],
        "confusion": ["розумію що це плутає", "давай поясню", "що саме не ясно?"],
        "accusation": ["я нікого не виганяла 😌", "ти, мабуть, щось не так зрозумів", "спокійно, все нормально"],
        "curiosity": ["цікаве питання 😏", "і що ти думаєш сам?", "давай розберемо"],
        "dj": ["DJ ще тут, все під контролем 😏", "він готує сет", "нічого не зникало"],
        "default": ["я тут 🙂", "слухаю тебе", "продовжуй"]
    },
    "RU": {
        "greeting": ["привет 🙂", "рада тебя видеть", "хей 😉"],
        "question": ["да, слушаю тебя", "расскажи подробнее", "я тут, говори"],
        "confusion": ["понимаю что это путает", "давай объясню", "что именно непонятно?"],
        "accusation": ["я никого не выгоняла 😌", "ты, возможно, неправильно понял", "всё нормально"],
        "curiosity": ["интересный вопрос 😏", "а ты как думаешь?", "давай разберём"],
        "dj": ["DJ на месте 😏", "он готовит сет", "всё под контролем"],
        "default": ["я тут 🙂", "слушаю тебя", "продолжай"]
    },
    "EN": {
        "greeting": ["hey 🙂", "nice to see you", "hello 😉"],
        "question": ["yes, I'm listening", "tell me more", "I'm here, go on"],
        "confusion": ["I get that it's confusing", "let me clarify", "what exactly is unclear?"],
        "accusation": ["I didn’t remove anyone 😌", "you might be mistaken", "everything is fine"],
        "curiosity": ["interesting question 😏", "what do you think?", "let's explore it"],
        "dj": ["DJ is still here 😏", "he is preparing a set", "nothing is wrong"],
        "default": ["I'm here 🙂", "listening", "go on"]
    }
}

# =========================
# 🌍 LANGUAGE
# =========================

def detect_lang(msg):
    msg = msg.lower()

    if any(x in msg for x in ["hello", "how are", "why", "what"]):
        return "EN"

    if any(x in msg for x in ["привет", "как", "почему", "что"]):
        return "RU"

    return "UA"

# =========================
# 🧠 INTENT + EMOTION
# =========================

def detect_emotion(msg):
    msg = msg.lower()

    # accusation / blame
    if "выгнал" in msg or "removed" in msg or "why did you" in msg:
        return "accusation"

    # confusion
    if "не понимаю" in msg or "don’t understand" in msg or "что" in msg:
        return "confusion"

    # curiosity
    if "зачем" in msg or "why" in msg or "что дальше" in msg:
        return "curiosity"

    # question
    if "?" in msg:
        return "question"

    # dj topic
    if "dj" in msg or "муз" in msg:
        return "dj"

    return "default"

# =========================
# 🧠 ANTI REPEAT
# =========================

def safe_pick(lang, emotion):

    global recent_replies

    pool = responses[lang].get(emotion, responses[lang]["default"])

    available = [x for x in pool if x not in recent_replies]

    if not available:
        recent_replies = []
        available = pool

    choice = random.choice(available)

    recent_replies.append(choice)

    if len(recent_replies) > MAX_RECENT:
        recent_replies.pop(0)

    return choice

# =========================
# 🎯 MAIN
# =========================

def process_luna_message(user, msg):

    now = time.time()

    if not msg:
        return ""

    msg_low = msg.lower()

    lang = detect_lang(msg_low)
    emotion = detect_emotion(msg_low)

    dialog = active_dialogs.get(user)

    if dialog:
        if now - dialog["time"] > DIALOG_TIMEOUT:
            active_dialogs.pop(user)
            dialog = None

    # =========================
    # 🔥 ACTIVE DIALOG
    # =========================

    if "luna" in msg_low or "луна" in msg_low or dialog:

        if not dialog:
            active_dialogs[user] = {
                "time": now,
                "lang": lang,
                "emotion": emotion
            }
            dialog = active_dialogs[user]

        lang = dialog["lang"]

        dialog["time"] = now
        dialog["emotion"] = emotion

        return safe_pick(lang, emotion)

    # =========================
    # 🤫 RANDOM REACTION
    # =========================

    if random.random() < 0.02:
        return safe_pick(lang, "default")

    return ""
