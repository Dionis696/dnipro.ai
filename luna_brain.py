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
        "info": [
            "сьогодні DJ готує новий сет 😏",
            "в клубі зараз спокійно, але це ненадовго",
            "є нові треки в ротації"
        ],
        "smalltalk": [
            "все нормально 🙂",
            "ловлю атмосферу",
            "ніч цікава сьогодні"
        ],
        "confusion": [
            "що саме тебе збило з пантелику?",
            "давай уточнимо",
            "поясни трохи детальніше"
        ],
        "complaint": [
            "я не зациклилась 🙂 просто ти не даєш нових даних",
            "я тут, просто чекаю конкретне питання",
            "спокійно, все працює нормально"
        ],
        "repetition": [
            "ти про одне і те ж питаєш 🙂",
            "ми вже трохи про це говорили",
            "давай щось нове"
        ],
        "default": [
            "ніч жива",
            "атмосфера цікава",
            "дивний вечір сьогодні"
        ]
    },
    "RU": {
        "info": [
            "сегодня DJ готовит новый сет 😏",
            "в клубе спокойно, но не надолго",
            "есть новые треки"
        ],
        "smalltalk": [
            "всё нормально 🙂",
            "ловлю атмосферу",
            "интересная ночь"
        ],
        "confusion": [
            "что именно непонятно?",
            "давай уточним",
            "объясни подробнее"
        ],
        "complaint": [
            "я не зациклилась 🙂 просто нет новых вопросов",
            "я тут, жду конкретику",
            "всё работает нормально"
        ],
        "repetition": [
            "ты повторяешься 🙂",
            "мы уже это обсуждали",
            "давай дальше"
        ],
        "default": [
            "ночь живая",
            "интересная атмосфера",
            "странный вечер"
        ]
    },
    "EN": {
        "info": [
            "DJ is preparing a new set 😏",
            "club is calm but not for long",
            "new tracks are coming"
        ],
        "smalltalk": [
            "I'm good 🙂",
            "just vibing",
            "interesting night"
        ],
        "confusion": [
            "what exactly is unclear?",
            "let's clarify",
            "tell me more"
        ],
        "complaint": [
            "I'm not stuck 🙂 you just repeat questions",
            "I'm here, waiting for real input",
            "everything is fine"
        ],
        "repetition": [
            "you're repeating yourself 🙂",
            "we already covered that",
            "let's move on"
        ],
        "default": [
            "night feels alive",
            "interesting vibe",
            "odd night"
        ]
    }
}

# =========================
# 🌍 LANGUAGE
# =========================

def detect_lang(msg):
    msg = msg.lower()

    if any(x in msg for x in ["hello", "how are", "what", "why"]):
        return "EN"

    if any(x in msg for x in ["привет", "как", "что", "почему"]):
        return "RU"

    return "UA"

# =========================
# 🧠 MESSAGE TYPE (КЛЮЧОВЕ НОВЕ)
# =========================

def detect_type(msg):
    msg = msg.lower()

    # complaint
    if "зацик" in msg or "stuck" in msg or "repeating" in msg:
        return "complaint"

    # repetition
    if "again" in msg or "знову" in msg:
        return "repetition"

    # confusion
    if "не понимаю" in msg or "что происходит" in msg:
        return "confusion"

    # info request
    if "что нового" in msg or "what's new" in msg or "новости" in msg:
        return "info"

    # smalltalk
    if "как дела" in msg or "how are" in msg:
        return "smalltalk"

    return "default"

# =========================
# 🧠 ANTI LOOP
# =========================

def safe_pick(lang, ttype):

    global recent_replies

    pool = responses[lang].get(ttype, responses[lang]["default"])

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
    ttype = detect_type(msg_low)

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
                "type": ttype
            }
            dialog = active_dialogs[user]

        lang = dialog["lang"]

        dialog["time"] = now
        dialog["type"] = ttype

        return safe_pick(lang, ttype)

    # =========================
    # 🤫 RANDOM
    # =========================

    if random.random() < 0.02:
        return safe_pick(lang, "default")

    return ""
