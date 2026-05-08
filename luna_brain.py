import random
import time

# =========================
# MEMORY
# =========================

active_dialogs = {}
DIALOG_TIMEOUT = 180

recent_replies = []
MAX_RECENT = 10

# =========================
# RESPONSES
# =========================

responses = {
    "UA": {
        "event": [
            "сьогодні п’ятниця — буде танцювальний вечір 🔥",
            "DJ сет сьогодні буде ближче до ночі 😏",
            "в клубі планується активний вечір",
            "лайнап ще уточнюється, але буде рух"
        ],
        "dj": [
            "DJ сьогодні готує новий сет 😏",
            "буде жива музика і танцювальний настрій",
            "він вже на підготовці"
        ],
        "info_event": [
            "сьогодні буде клубний вечір з DJ сетом 🔥",
            "точний лайнап ще не фіналізували",
            "вечір буде з музикою і рухом 😏"
        ],
        "chat": [
            "я тут 🙂",
            "слухаю тебе",
            "кажи далі"
        ],
        "fallback": [
            "цікаво 😏 розкажи більше",
            "я тебе слухаю",
            "продовжуй"
        ]
    },

    "RU": {
        "event": [
            "сегодня пятница — будет танцевальный вечер 🔥",
            "DJ сет будет ближе к ночи 😏",
            "в клубе планируется активный вечер",
            "лайнап ещё уточняется"
        ],
        "dj": [
            "DJ сегодня готовит новый сет 😏",
            "будет живая музыка и танцы",
            "он уже на подготовке"
        ],
        "info_event": [
            "сегодня клубный вечер с DJ сетом 🔥",
            "точный лайнап пока не финальный",
            "вечер будет с музыкой и движением 😏"
        ],
        "chat": [
            "я тут 🙂",
            "слушаю тебя",
            "говори"
        ],
        "fallback": [
            "интересно 😏 расскажи больше",
            "я слушаю",
            "продолжай"
        ]
    },

    "EN": {
        "event": [
            "tonight is club night 🔥",
            "DJ set will be later 😏",
            "active evening planned",
            "lineup is not fully confirmed"
        ],
        "dj": [
            "DJ is preparing a new set 😏",
            "there will be live music and dance vibes",
            "he is getting ready"
        ],
        "info_event": [
            "tonight is a club night with DJ set 🔥",
            "lineup is still being confirmed",
            "music and movement incoming 😏"
        ],
        "chat": [
            "I'm here 🙂",
            "listening",
            "go on"
        ],
        "fallback": [
            "interesting 😏 tell me more",
            "I'm listening",
            "continue"
        ]
    }
}

# =========================
# LANGUAGE
# =========================

def detect_lang(msg):
    msg = msg.lower()

    if any(x in msg for x in ["hello", "how", "what", "why"]):
        return "EN"

    if any(x in msg for x in ["привет", "как", "что", "почему"]):
        return "RU"

    return "UA"

# =========================
# INTENT DETECTION (КЛЮЧОВЕ)
# =========================

def detect_intent(msg):
    msg = msg.lower()

    # EVENT / CLUB INFO (головне)
    if any(x in msg for x in [
        "сьогодні", "сегодня", "tonight",
        "що буде", "что будет", "what's happening",
        "лайн", "lineup", "dj", "сет", "муз"
    ]):
        return "event"

    # DJ specific
    if "dj" in msg or "сет" in msg:
        return "dj"

    return "chat"

# =========================
# ANTI REPEAT
# =========================

def safe_pick(lang, intent):

    global recent_replies

    pool = responses[lang].get(intent, responses[lang]["fallback"])

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
# MAIN
# =========================

def process_luna_message(user, msg):

    if not msg:
        return ""

    msg_low = msg.lower()
    lang = detect_lang(msg_low)
    intent = detect_intent(msg_low)

    # =========================
    # ACTIVE MODE
    # =========================

    if "luna" in msg_low or "луна" in msg_low:

        # EVENT PRIORITY (КРИТИЧНО)
        if intent == "event":
            return safe_pick(lang, "event")

        if intent == "dj":
            return safe_pick(lang, "dj")

        return safe_pick(lang, "chat")

    # =========================
    # IDLE MODE
    # =========================

    if random.random() < 0.02:
        return safe_pick(lang, "chat")

    return ""
