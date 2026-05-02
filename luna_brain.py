import random
import time

# =========================
# 🧠 ПАМʼЯТЬ
# =========================

users = {}

def get_user(user):
    if user not in users:
        users[user] = {
            "count": 0,
            "mood": 0,
            "gender": "unknown",
            "favorite": False,
            "last_seen": 0,
            "last_reply": 0
        }
    return users[user]


def update_user(user, message):
    data = get_user(user)

    data["count"] += 1
    data["last_seen"] = time.time()

    msg = message.lower()

    if any(w in msg for w in ["люблю", "love", "клас", "круто"]):
        data["mood"] += 1

    if any(w in msg for w in ["фігня", "погано", "бісить"]):
        data["mood"] -= 1

    if "я дівчина" in msg or "i am a girl" in msg:
        data["gender"] = "female"

    if "я хлопець" in msg or "i am a guy" in msg:
        data["gender"] = "male"

    if data["count"] > 15 and data["mood"] > 2:
        data["favorite"] = True


# =========================
# 🎭 ФРАЗИ
# =========================

ua_greet = [
    "Привіт 🙂 рада тебе бачити",
    "Йо 😎 ти як завжди вчасно",
    "О, з’явився 😏",
    "Ну привіт 😉",
]

ua_neutral = [
    "мм цікаво 🙂",
    "ну ти даєш 😄",
    "є щось в цьому 😏",
    "ха, звучить непогано 😎",
]

ua_flirt = [
    "ти сьогодні підозріло цікавий 😏",
    "мені подобається як ти пишеш 😉",
    "обережно… я можу затягнути тебе в танець 💋",
]

ua_cold = [
    "мм… ну ок 🙂",
    "не переконав 😉",
    "я ще думаю 😏",
]

ua_music = [
    "давай качнемо танцпол 💃",
    "цей трек вже розкачує 🔥",
    "музика вже качає 🎧",
]

greetings_en = [
    "hey 🙂 nice to see you",
    "yo 😎 you came at the right time",
]

neutral_en = [
    "hmm interesting 🙂",
    "not bad 😎",
]

flirt_en = [
    "you're kinda interesting 😏",
    "I like your vibe 😉",
]

cold_en = [
    "hmm… alright 🙂",
]

music_en = [
    "we need more bass 🔥",
]

memory_phrases = [
    "я тебе пам’ятаю 😉",
    "ти тут не вперше 😏",
]


# =========================
# 🎯 РЕАКЦІЇ
# =========================

reactions = {
    "dance": [
        "ну все, пішли танцювати 💃",
        "я вже на танцполі 😏",
    ],
    "kiss": [
        "обережно зі мною 💋",
        "мм… цікаво 😉",
    ],
    "sad": [
        "не сумуй 🙂",
        "давай піднімемо настрій 🔥",
    ]
}

def check_reactions(message):
    msg = message.lower()

    if any(w in msg for w in ["танц", "dance"]):
        return random.choice(reactions["dance"])

    if any(w in msg for w in ["поціл", "kiss"]):
        return random.choice(reactions["kiss"])

    if any(w in msg for w in ["сум", "sad"]):
        return random.choice(reactions["sad"])

    return None


# =========================
# 🌍 МОВА
# =========================

def detect_language(message):
    msg = message.lower()

    if any(c in msg for c in "qwertyuiopasdfghjklzxcvbnm"):
        return "EN"

    return "UA"


# =========================
# 💬 ВІДПОВІДЬ
# =========================

def get_fallback_response(user, message):
    data = get_user(user)

    if time.time() - data["last_reply"] < 5:
        return None

    data["last_reply"] = time.time()

    update_user(user, message)

    lang = detect_language(message)
    name = user.split(" ")[0]

    reaction = check_reactions(message)
    if reaction:
        return f"{name}, {reaction}"

    if lang == "EN":
        if data["mood"] > 1:
            base = random.choice(flirt_en)
        elif data["mood"] < -1:
            base = random.choice(cold_en)
        else:
            base = random.choice(neutral_en + music_en)
    else:
        if "привіт" in message.lower():
            base = random.choice(ua_greet)
        elif data["mood"] > 1:
            base = random.choice(ua_flirt)
        elif data["mood"] < -1:
            base = random.choice(ua_cold)
        else:
            base = random.choice(ua_neutral + ua_music)

    base = f"{name}, {base}"

    if data["favorite"]:
        base += "\n" + random.choice([
            "ти мій фаворит 😏",
            "з тобою цікавіше 💋",
        ])

    if random.random() < 0.2:
        base += "\n" + random.choice(memory_phrases)

    return base
