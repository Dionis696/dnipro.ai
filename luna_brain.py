import random
import time

# =========================
# 🧠 MEMORY STATE
# =========================

active_dialogs = {}
DIALOG_TIMEOUT = 180

recent_replies = []
MAX_RECENT = 10

user_topic = {}

# =========================
# 💬 RESPONSES
# =========================

responses = {
    "UA": {
        "dj": [
            "DJ ще не назвав сет, але буде сильний 😏",
            "він готує новий мікс зараз",
            "скоро старт музики 🔥"
        ],
        "music": [
            "сьогодні більше танцювального настрою 😏",
            "музика буде змінюватись по ходу ночі",
            "є нові треки в сеті"
        ],
        "dance": [
            "давай рух 🔥",
            "клуб вже готовий до танців",
            "це момент для енергії 😏"
        ],
        "silence": [
            "зараз спокійно, але це тимчасово",
            "тиша перед рухом 😏",
            "клуб чекає старту"
        ],
        "chat": [
            "я тут 🙂",
            "слухаю тебе",
            "кажи далі"
        ],
        "answer_dj": [
            "ще не оголошували назву сету 😏",
            "поки тримають інтригу",
            "це буде щось нове"
        ],
        "answer_general": [
            "розкажи трохи більше",
            "цікаво, продовжуй",
            "я тебе слухаю"
        ]
    },

    "RU": {
        "dj": [
            "DJ ещё не объявил сет 😏",
            "он готовит микс",
            "скоро старт музыки 🔥"
        ],
        "music": [
            "сегодня танцевальный настрой",
            "музыка будет меняться",
            "есть новые треки"
        ],
        "dance": [
            "давай движение 🔥",
            "клуб готов к танцам",
            "энергия растёт 😏"
        ],
        "silence": [
            "сейчас спокойно, но не надолго",
            "тишина перед движением 😏",
            "клуб ждёт старт"
        ],
        "chat": [
            "я тут 🙂",
            "слушаю тебя",
            "говори"
        ],
        "answer_dj": [
            "название сета пока не сказали 😏",
            "держат интригу",
            "будет что-то новое"
        ],
        "answer_general": [
            "расскажи подробнее",
            "интересно, продолжай",
            "я слушаю"
        ]
    },

    "EN": {
        "dj": [
            "DJ hasn’t announced the set yet 😏",
            "he is preparing a mix",
            "music will start soon 🔥"
        ],
        "music": [
            "tonight is more dance oriented",
            "music will evolve",
            "new tracks are included"
        ],
        "dance": [
            "let’s move 🔥",
            "club is ready",
            "energy is rising 😏"
        ],
        "silence": [
            "quiet now, but not for long",
            "calm before the wave 😏",
            "waiting for the start"
        ],
        "chat": [
            "I'm here 🙂",
            "listening",
            "go on"
        ],
        "answer_dj": [
            "they haven’t revealed the set name yet 😏",
            "they keep it secret",
            "something new is coming"
        ],
        "answer_general": [
            "tell me more",
            "interesting, continue",
            "I'm listening"
        ]
    }
}

# =========================
# 🌍 LANGUAGE
# =========================

def detect_lang(msg):
    msg = msg.lower()

    if any(x in msg for x in ["hello", "how", "what", "why"]):
        return "EN"

    if any(x in msg for x in ["привет", "как", "что", "почему"]):
        return "RU"

    return "UA"

# =========================
# 🔥 TOPIC DETECTION
# =========================

def detect_topic(msg):
    msg = msg.lower()

    # IMPORTANT: QUESTION FIRST RULE
    if "?" in msg:
        if "dj" in msg or "сет" in msg or "муз" in msg:
            return "answer_dj"
        return "answer_general"

    if any(x in msg for x in ["dj", "сет"]):
        return "dj"

    if any(x in msg for x in ["муз", "music", "треки"]):
        return "music"

    if any(x in msg for x in ["танц", "dance", "рух"]):
        return "dance"

    if any(x in msg for x in ["тихо", "тишина", "нема"]):
        return "silence"

    return "chat"

# =========================
# 🧠 ANTI REPEAT
# =========================

def safe_pick(lang, topic):

    global recent_replies

    pool = responses[lang].get(topic, responses[lang]["chat"])

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
    topic = detect_topic(msg_low)

    # save topic per user
    user_topic[user] = topic

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
                "topic": topic
            }
            dialog = active_dialogs[user]

        lang = dialog["lang"]
        dialog["time"] = now

        # TOPIC LOCK (важливо)
        locked_topic = dialog.get("topic", topic)

        reply = safe_pick(lang, locked_topic)

        return reply

    # =========================
    # 🤫 IDLE MODE
    # =========================

    if random.random() < 0.02:
        return safe_pick(lang, "chat")

    return ""
