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
# 💬 POOLS
# =========================

responses = {
    "UA": {
        "greeting": ["привіт 🙂", "рада тебе бачити", "хей 😉"],
        "how": ["та нормально 🙂", "ловлю вайб", "все ок 😉"],
        "silence": ["тиша якась сьогодні 😏", "в клубі затихло", "дивний вайб"],
        "dj": ["DJ щось задумав 😏", "зараз буде рух", "відчуваю двіж"],
        "confusion": ["щось не так відчувається", "дивний момент", "хмм… цікаво"],
        "doubt": ["ти сумніваєшся? 😏", "чому так думаєш?", "не все так просто"],
        "default": ["ніч жива", "атмосфера цікава", "цікавий вечір"]
    },
    "RU": {
        "greeting": ["привет 🙂", "рада тебя видеть", "хей 😉"],
        "how": ["всё нормально 🙂", "ловлю вайб", "всё ок 😉"],
        "silence": ["тишина сегодня 😏", "в клубе тихо", "странный вайб"],
        "dj": ["DJ что-то задумал 😏", "сейчас будет движ", "чувствую разрыв"],
        "confusion": ["что-то странно", "интересный момент", "хмм…"],
        "doubt": ["сомневаешься? 😏", "почему так думаешь?", "не всё так просто"],
        "default": ["ночь живая", "интересная атмосфера", "странный вечер"]
    },
    "EN": {
        "greeting": ["hey 🙂", "nice to see you", "hello 😉"],
        "how": ["I'm good 🙂", "just vibing", "all good 😉"],
        "silence": ["too quiet here 😏", "club feels calm", "strange vibe"],
        "dj": ["DJ planning something 😏", "big drop coming", "feeling the vibe"],
        "confusion": ["something feels off", "interesting moment", "hmm…"],
        "doubt": ["you doubt it? 😏", "why do you think that?", "not that simple"],
        "default": ["night feels alive", "interesting vibe", "odd night"]
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
# 🎯 INTENT (НОВЕ!)
# =========================

def detect_intent(msg):
    msg = msg.lower()

    if "dj" in msg or "муз" in msg:
        return "dj"

    if "тиша" in msg or "quiet" in msg:
        return "silence"

    if "як справ" in msg or "how are" in msg:
        return "how"

    if "прив" in msg or "hello" in msg:
        return "greeting"

    if "ти впевн" in msg or "are you sure" in msg:
        return "doubt"

    if "що" in msg or "what" in msg:
        return "confusion"

    return "default"

# =========================
# 🧠 ANTI LOOP
# =========================

def safe_pick(lang, intent):

    global recent_replies

    pool = responses[lang].get(intent, responses[lang]["default"])

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
# 🧠 MAIN
# =========================

def process_luna_message(user, msg):

    now = time.time()

    if not msg:
        return ""

    msg_low = msg.lower()

    lang = detect_lang(msg_low)
    intent = detect_intent(msg_low)

    dialog = active_dialogs.get(user)

    if dialog:
        if now - dialog["time"] > DIALOG_TIMEOUT:
            active_dialogs.pop(user)
            dialog = None

    # =========================
    # 🔥 START / CONTINUE DIALOG
    # =========================

    if "luna" in msg_low or "луна" in msg_low or dialog:

        if not dialog:
            active_dialogs[user] = {
                "time": now,
                "lang": lang,
                "intent": intent
            }
            dialog = active_dialogs[user]

        # update only time + intent (LANG LOCK!)
        dialog["time"] = now
        dialog["intent"] = intent

        lang = dialog["lang"]

        return safe_pick(lang, intent)

    # =========================
    # 🤫 RANDOM REACTION
    # =========================

    if random.random() < 0.02:
        return safe_pick(lang, "default")

    return ""
