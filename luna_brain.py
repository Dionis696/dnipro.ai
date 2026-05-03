import random
import time

users = {}

# 📚 книга
book_lines = []

try:
    with open("luna_book.txt", "r", encoding="utf-8") as f:
        book_lines = [line.strip() for line in f if line.strip()]
except:
    book_lines = []


def get_book_line():
    if not book_lines:
        return None
    return random.choice(book_lines)


def get_user(user):
    if user not in users:
        users[user] = {"last_reply": 0}
    return users[user]


# 🌍 мова
def detect_lang(text):
    t = text.lower()

    if any(w in t for w in ["hello", "what", "how", "do you", "write"]):
        return "en"
    if any(w in t for w in ["привет", "что", "как", "расскажи"]):
        return "ru"
    return "ua"


# 🎯 тип
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


# 🎭 фрази
ua = [
    "ну ти даєш 😄",
    "є щось в цьому 😏",
    "звучить цікаво 😉",
    "ага, вже краще 😎",
    "давай трохи драйву 💃",
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
    "було якось — світло вирубилось, а всі танцювали далі 🔥",
    "один раз в клубі бармен почав танцювати швидше за гостей 😄",
]

ru_story = [
    "вчера один тип раскачал зал так, что даже охрана улыбалась 😄",
]

en_story = [
    "yesterday one guy turned the whole dancefloor crazy 😄",
]


ua_greet = ["Привіт 🙂", "Йо 😎", "О, ти з’явився 😏"]
ru_greet = ["Привет 🙂", "Йо 😎"]
en_greet = ["Hey 🙂", "Yo 😎"]


def pick(arr):
    return random.choice(arr)


def get_fallback_response(user, message):
    data = get_user(user)

    # анти-спам
    if time.time() - data["last_reply"] < 2:
        return None

    data["last_reply"] = time.time()

    name = user.split(" ")[0]

    lang = detect_lang(message)
    intent = analyze(message)

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

    if intent == "greet":
        text = pick(greet_pool)

    elif intent == "story":
        text = pick(story_pool)

    elif intent == "how":
        text = {
            "ua": "та норм, ловлю вайб 😏",
            "ru": "да нормально, ловлю вайб 😏",
            "en": "I'm good, just vibing 😏"
        }[lang]

    elif intent == "question":
        text = {
            "ua": "шо саме? 😉",
            "ru": "что именно? 😉",
            "en": "what exactly? 😉"
        }[lang]

    else:
        text = pick(base_pool)

    # 📚 додаємо книгу інколи
    if random.random() < 0.25:
        book = get_book_line()
        if book:
            text += "\n" + book

    return f"{name}, {text}"
