import random

# 🔹 Категорії відповідей

greetings = [
    "Привіт 🙂 рада тебе бачити",
    "Йо, привіт 😎 як настрій?",
    "Привіт, заходь не стій 😉",
]

how_are_you = [
    "Та нормально, ловлю вайб 😏 а ти як?",
    "Все ок, трохи музики і настрій топ 🔥",
    "Живу, кайфую 😉",
]

music = [
    "мм щось з 2000-х зараз би зайшло 😏",
    "може щось танцювальне включимо? 💃",
    "я б зараз щось з басом поставила 🔥",
]

flirt = [
    "ти сьогодні підозріло цікавий 😏",
    "обережно… я можу спокусити на танець 💋",
    "мені подобається як ти пишеш 😉",
]

fallback = [
    "ага, зрозуміла 🙂",
    "мм цікаво 😏",
    "ну ти даєш 😄",
    "є щось в цьому 😉",
]

stories = [
    "пам’ятаю якось у клубі всі казали 'на 5 хв зайшли'… і пропали до ранку 😄",
    "був вечір, коли музика так качала що навіть бармен танцював 😂",
]

dance = [
    "ну що, хто на танцпол? 💃🔥",
    "пішли танцювати, не сиди 😏",
]


# 🔹 Визначення категорії
def detect_category(msg):
    msg = msg.lower()

    if "привіт" in msg:
        return "greetings"
    if "як справ" in msg:
        return "how"
    if "трек" in msg or "муз" in msg:
        return "music"

    return "fallback"


# 🔹 Визначення мови
def detect_lang(msg):
    msg = msg.lower()

    if any(word in msg for word in ["how", "hello", "hi"]):
        return "en"
    if any(word in msg for word in ["как", "привет"]):
        return "ru"

    return "ua"


# 🔹 Генерація відповіді
def get_reply(msg):
    cat = detect_category(msg)

    if cat == "greetings":
        base = greetings
    elif cat == "how":
        base = how_are_you
    elif cat == "music":
        base = music
    else:
        base = fallback

    reply = random.choice(base)

    # 😏 іноді додаємо флірт
    if random.random() < 0.2:
        reply += " " + random.choice(flirt)

    return reply


# 🔹 Іноді історія
def maybe_story():
    if random.random() < 0.1:
        return random.choice(stories)
    return None


# 🔹 Іноді танці
def maybe_dance():
    if random.random() < 0.15:
        return random.choice(dance)
    return None
