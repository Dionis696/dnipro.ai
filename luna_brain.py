import random
import time

# =========================
# 🧠 MEMORY
# =========================

active_dialogs = {}
DIALOG_TIMEOUT = 180

recent_replies = []
MAX_RECENT = 10

last_scene_reply = {}

# =========================
# 💬 RESPONSES BY ENERGY
# =========================

responses = {
    "UA": {
        "low": [
            "тиша сьогодні в клубі",
            "спокійний вечір",
            "атмосфера розслаблена"
        ],
        "normal": [
            "ніч жива 🙂",
            "цікава атмосфера",
            "щось відчувається в повітрі"
        ],
        "high": [
            "давай рух 😏 музика вже грає",
            "клуб прокидається 🔥",
            "це вже вечір для танців"
        ],
        "dj": [
            "DJ зараз готує сильний сет 😏",
            "буде різкий підйом музики",
            "він тестить нові треки"
        ],
        "repetition_block": [
            "ми це вже трохи обговорювали 🙂",
            "давай щось нове",
            "ти повторюєшся трохи"
        ]
    },
    "RU": {
        "low": [
            "тихо сегодня в клубе",
            "спокойный вечер",
            "расслабленная атмосфера"
        ],
        "normal": [
            "ночь живая 🙂",
            "интересная атмосфера",
            "что-то в воздухе"
        ],
        "high": [
            "давай движение 😏 музыка уже играет",
            "клуб оживает 🔥",
            "это вечер для танцев"
        ],
        "dj": [
            "DJ готовит сильный сет 😏",
            "будет подъем музыки",
            "он тестирует новые треки"
        ],
        "repetition_block": [
            "мы это уже обсуждали 🙂",
            "давай новое",
            "ты повторяешься"
        ]
    },
    "EN": {
        "low": [
            "quiet night in the club",
            "calm atmosphere",
            "relaxed vibe"
        ],
        "normal": [
            "night feels alive 🙂",
            "interesting vibe",
            "something in the air"
        ],
        "high": [
            "let’s move 😏 music is up",
            "club is waking up 🔥",
            "this is dance time"
        ],
        "dj": [
            "DJ is preparing a strong set 😏",
            "music is about to rise",
            "he is testing new tracks"
        ],
        "repetition_block": [
            "we already covered that 🙂",
            "let’s go further",
            "you’re repeating a bit"
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
# 🔥 SCENE DETECTION
# =========================

def detect_scene(msg):
    msg = msg.lower()

    # HIGH ENERGY
    if any(x in msg for x in ["танц", "dance", "рух", "party", "давай"]):
        return "high"

    # DJ MODE
    if "dj" in msg or "муз" in msg or "сет" in msg:
        return "dj"

    # LOW
    if any(x in msg for x in ["тихо", "нема", "тишина"]):
        return "low"

    return "normal"

# =========================
# 🧠 ANTI REPEAT SCENE
# =========================

def anti_repeat(user, msg_type, reply):

    key = f"{user}:{msg_type}"

    last = last_scene_reply.get(key)

    if last == reply:
        return random.choice(responses["UA"]["repetition_block"])

    last_scene_reply[key] = reply

    return reply

# =========================
# 🎯 MAIN
# =========================

def process_luna_message(user, msg):

    now = time.time()

    if not msg:
        return ""

    msg_low = msg.lower()

    lang = detect_lang(msg_low)
    scene = detect_scene(msg_low)

    dialog = active_dialogs.get(user)

    if dialog:
        if now - dialog["time"] > DIALOG_TIMEOUT:
            active_dialogs.pop(user)
            dialog = None

    # =========================
    # 🔥 ACTIVE MODE
    # =========================

    if "luna" in msg_low or "луна" in msg_low or dialog:

        if not dialog:
            active_dialogs[user] = {
                "time": now,
                "lang": lang,
                "scene": scene
            }
            dialog = active_dialogs[user]

        lang = dialog["lang"]

        dialog["time"] = now
        dialog["scene"] = scene

        pool = responses[lang][scene]

        reply = random.choice(pool)

        return anti_repeat(user, scene, reply)

    # =========================
    # 🤫 IDLE REACTION
    # =========================

    if random.random() < 0.02:
        return random.choice(responses[lang]["normal"])

    return ""
