import random
import time

# =========================
# 🧠 MEMORY
# =========================

active_dialogs = {}
DIALOG_TIMEOUT = 180  # 3 хв

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
        "dj": ["DJ щось готує 😏", "відчуваю що буде рух", "він щось задумав"],
        "confusion": ["хмм… не зовсім ясно", "цікаво сформульовано", "є щось дивне в цьому"],
        "doubt": ["ти сумніваєшся? 😏", "чому так думаєш?", "не все так просто"],
        "followup": ["розкажи більше", "і що далі?", "цікаво, продовжуй"],
        "default": ["ніч жива", "цікавий момент", "атмосфера цікава"]
    },
    "RU": {
        "greeting": ["привет 🙂", "рада тебя видеть", "хей 😉"],
        "how": ["всё нормально 🙂", "ловлю вайб", "всё ок 😉"],
        "silence": ["тишина сегодня 😏", "в клубе тихо", "странный вайб"],
        "dj": ["DJ что-то готовит 😏", "чувствую движ", "он что-то задумал"],
        "confusion": ["хмм… не совсем ясно", "интересно сказано", "что-то странное"],
        "doubt": ["сомневаешься? 😏", "почему так думаешь?", "не всё так просто"],
        "followup": ["расскажи больше", "и что дальше?", "интересно, продолжай"],
        "default": ["ночь живая", "интересная атмосфера", "странный вечер"]
    },
    "EN": {
        "greeting": ["hey 🙂", "nice to see you", "hello 😉"],
        "how": ["I'm good 🙂", "just vibing", "all good 😉"],
        "silence": ["too quiet here 😏", "club feels calm", "strange vibe"],
        "dj": ["DJ is preparing something 😏", "I feel something big coming", "he is planning something"],
        "confusion": ["hmm… not sure", "interesting phrasing", "something feels off"],
        "doubt": ["you doubt it? 😏", "why do you think that?", "not that simple"],
        "followup": ["tell me more", "and then?", "interesting, go on"],
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
# 🧠 INTENT
# =========================

def detect_intent(msg):
    msg = msg.lower()

    if "dj" in msg or "муз" in msg:
        return "dj"

    if "тиша" in msg or "quiet" in msg:
        return "silence"

    if "як" in msg or "how" in msg or "как" in msg:
        return "how"

    if "прив" in msg or "hello" in msg:
        return "greeting"

    if "ти впевн" in msg or "sure" in msg:
        return "doubt"

    if "що" in msg or "what" in msg:
        return "confusion"

    return "default"

# =========================
# 🧠 SAFE PICK
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
# 🎯 MAIN
# =========================

def process_luna_message(user, msg):

    now = time.time()

    if not msg:
        return ""

    msg_low = msg.lower()

    lang = detect_lang(msg_low)
    intent = detect_intent(msg_low)

    dialog = active_dialogs.get(user)

    # =========================
    # ⏳ TIMEOUT DIALOG
    # =========================

    if dialog:
        if now - dialog["time"] > DIALOG_TIMEOUT:
            active_dialogs.pop(user)
            dialog = None

    # =========================
    # 🔥 START / CONTINUE DIALOG
    # =========================

    if "luna" in msg_low or "луна" in msg_low or dialog:

        # новий діалог
        if not dialog:
            active_dialogs[user] = {
                "time": now,
                "lang": lang,
                "topic": intent,
                "last_q": msg_low
            }
            dialog = active_dialogs[user]

        # 🔒 LANGUAGE LOCK
        lang = dialog["lang"]

        # 🧠 update context
        last_q = dialog.get("last_q", "")

        # якщо це follow-up (коротке питання)
        is_followup = len(msg_low.split()) <= 4

        dialog["time"] = now
        dialog["topic"] = intent

        # зберігаємо питання
        if "?" in msg_low:
            dialog["last_q"] = msg_low

        # =========================
        # 🎯 FOLLOW-UP LOGIC
        # =========================

        if is_followup and dialog.get("last_q"):
            return safe_pick(lang, "followup")

        # =========================
        # 🎯 NORMAL RESPONSE
        # =========================

        return safe_pick(lang, intent)

    # =========================
    # 🤫 RANDOM
    # =========================

    if random.random() < 0.02:
        return safe_pick(lang, "default")

    return ""
