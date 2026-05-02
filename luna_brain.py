import random
import time

# памʼять користувачів
users = {}

def get_user(user):
    if user not in users:
        users[user] = {
            "count": 0,
            "mood": 0,
            "favorite": False,
            "last_reply": 0
        }
    return users[user]


def update_user(user, message):
    data = get_user(user)

    data["count"] += 1

    msg = message.lower()

    if any(w in msg for w in ["круто", "love", "клас"]):
        data["mood"] += 1

    if any(w in msg for w in ["погано", "фігня"]):
        data["mood"] -= 1

    if data["count"] > 10 and data["mood"] > 1:
        data["favorite"] = True


# фрази
ua = [
    "мм цікаво 🙂",
    "ну ти даєш 😄",
    "є щось в цьому 😏",
    "давай трохи драйву 💃",
]

ua_flirt = [
    "ти сьогодні цікавий 😏",
    "мені подобається як ти пишеш 😉",
]

ua_greet = [
    "Привіт 🙂",
    "Йо 😎",
]

memory = [
    "я тебе пам’ятаю 😉",
    "ти тут не вперше 😏",
]


def get_fallback_response(user, message):
    data = get_user(user)

    # антиспам
    if time.time() - data["last_reply"] < 4:
        return None

    data["last_reply"] = time.time()

    update_user(user, message)

    name = user.split(" ")[0]

    if "привіт" in message.lower():
        base = random.choice(ua_greet)
    elif data["mood"] > 1:
        base = random.choice(ua_flirt)
    else:
        base = random.choice(ua)

    text = f"{name}, {base}"

    if data["favorite"]:
        text += "\nти мені подобаєшся 😏"

    if random.random() < 0.2:
        text += "\n" + random.choice(memory)

    return text
