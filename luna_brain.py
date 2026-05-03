import random
import time

users = {}

def get_user(user):
    if user not in users:
        users[user] = {
            "last_reply": 0
        }
    return users[user]


# 🌍 визначення мови
def detect_lang(text):
    t = text.lower()

    if any(w in t for w in ["hello", "what", "how", "do you", "write"]):
        return "en"
    if any(w in t for w in ["привет", "что", "как", "расскажи"]):
        return "ru"
    return "ua"


# 🎯 тип повідомлення
def analyze(text):
    t = text.lower()

    if "прив" in t or "hello" in t:
        return "greet"

    if "як" in t or "how" in t:
        return "how"

    if "істор" in t or "story" in t or "расскаж" in t:
        return "story"

    if "шо" in t or "what" in t:
        return "question"

    return "normal"


# 🎭 ФРАЗИ

ua = [
    "ну ти даєш 😄",
    "є щось в цьому 😏",
    "звучить цікаво 😉",
    "ага, вже краще 😎",
]

ru = [
    "ну ты даешь 😄",
    "есть в этом что-то 😏",
    "звучит интересно 😉",
]

en = [
    "hmm interesting 😏",
    "sounds good 😉",
    "you got my attention 😎",
]


ua_story = [
    "пам’ятаю вчора в клубі один тип так розкачав зал, що навіть бармен почав танцювати 😄",
    "було якось — світло вирубилось, а народ не зупинився… співали і танцювали в темряві 🔥",
]

ru_story = [
    "вчера в клубе один чувак так зажёг, что даже охрана начала качать 😄",
]

en_story = [
    "yesterday one guy turned the whole dancefloor crazy… even the DJ lost control 😄",
]


ua_greet = ["Привіт 🙂", "Йо 😎", "О, ти з’явився 😏"]
ru_greet = ["Привет 🙂", "Йо 😎"]
en_greet = ["Hey 🙂", "Yo 😎"]


def pick(arr):
    return random.choice(arr)


def get_fallback_response(user, message):
    data = get_user(user)

    if time.time() - data["last_reply"] < 2:
        return None

    data["last_reply"] = time.time()

    name = user.split(" ")[0]

    lang = detect_lang(message)
    intent = analyze(message)

    # 🔥 логіка по мові
    if lang == "ua":
        base_pool = ua
        greet_pool = ua_greet
        story_pool = ua_story

    elif lang == "ru":
        base_pool = ru
        greet_pool = ru_greet
        story_pool = ru_story

    else:
        base_pool = en
        greet_pool = en_greet
        story_pool = en_story

    # 🎯 відповіді
    if intent == "greet":
        text = pick(greet_pool)

    elif intent == "story":
        text = pick(story_pool)

    elif intent == "how":
        if lang == "en":
            text = "I'm good, just catching the vibe 😏"
        elif lang == "ru":
            text = "да нормально, ловлю вайб 😏"
        else:
            text = "та норм, ловлю вайб 😏"

    elif intent == "question":
        if lang == "en":
            text = "what exactly do you mean? 😉"
        elif lang == "ru":
            text = "что именно? 😉"
        else:
            text = "шо саме? 😉"

    else:
        text = pick(base_pool)

    return f"{name}, {text}"
