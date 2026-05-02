import random
import time

users = {}

def get_user(user):
    if user not in users:
        users[user] = {
            "count": 0,
            "mood": 0,
            "favorite": False,
            "last_reply": 0,
            "last_message": ""
        }
    return users[user]


def update_user(user, message):
    data = get_user(user)

    data["count"] += 1
    data["last_message"] = message.lower()

    msg = message.lower()

    if any(w in msg for w in ["круто", "love", "клас"]):
        data["mood"] += 1

    if any(w in msg for w in ["погано", "фігня"]):
        data["mood"] -= 1

    if data["count"] > 10 and data["mood"] > 1:
        data["favorite"] = True


# 🔥 БІЛЬШЕ ФРАЗ
ua_neutral = [
    "ну ти даєш 😄",
    "є щось в цьому 😏",
    "звучить цікаво 😉",
    "ага, вже краще 😎",
]

ua_fun = [
    "давай качнемо атмосферу 💃🔥",
    "музика вже проситься голосніше 🎧",
    "я б зараз такий трек поставила… 😏",
]

ua_flirt = [
    "ти сьогодні прям заряджаєш 😏",
    "мені подобається як ти думаєш 😉",
    "обережно… я можу втягнути тебе в ніч 💋",
]

ua_greet = [
    "Привіт 🙂 рада тебе бачити",
    "Йо 😎 ти якраз в тему",
    "О, з’явився 😏",
]

ua_question = [
    "а ти як думаєш? 😉",
    "ну і що будемо робити далі? 😏",
    "розкажеш більше? 🙂",
]

memory = [
    "я тебе пам’ятаю 😉",
    "ти тут не вперше 😏",
]


# 🔥 АНАЛІЗ ПОВІДОМЛЕННЯ
def analyze(message):
    msg = message.lower()

    if "привіт" in msg:
        return "greet"

    if "як справи" in msg or "як ти" in msg:
        return "how"

    if "шо" in msg or "що" in msg:
        return "question"

    if "давай" in msg:
        return "action"

    if "ти тут" in msg:
        return "presence"

    return "normal"


def get_fallback_response(user, message):
    data = get_user(user)

    if time.time() - data["last_reply"] < 3:
        return None

    data["last_reply"] = time.time()

    update_user(user, message)

    name = user.split(" ")[0]
    intent = analyze(message)

    # 🔥 ЛОГІКА
    if intent == "greet":
        base = random.choice(ua_greet)

    elif intent == "how":
        base = random.choice([
            "та нормально, ловлю вайб 😏",
            "живу, кайфую 😉",
            "все ок, музика рятує 🎧",
        ])

    elif intent == "question":
        base = random.choice(ua_question)

    elif intent == "action":
        base = random.choice(ua_fun)

    elif intent == "presence":
        base = random.choice([
            "я тут, не зникаю 😏",
            "звісно тут 😉",
            "я ж нікуди не йду 😎",
        ])

    else:
        if data["mood"] > 1:
            base = random.choice(ua_flirt)
        else:
            base = random.choice(ua_neutral + ua_fun)

    text = f"{name}, {base}"

    # фаворит
    if data["favorite"]:
        text += "\nти мені подобаєшся 😏"

    # памʼять
    if random.random() < 0.15:
        text += "\n" + random.choice(memory)

    return text
