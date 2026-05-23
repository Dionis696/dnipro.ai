import random

# 🧠 cache останніх відповідей
last_responses = []

MAX_CACHE = 10


def pick_response(book, memory, msg):

    global last_responses

    # cleanup
    book = [x.strip() for x in book if x and x.strip()]
    memory = [x.strip() for x in memory if x and x.strip()]

    msg = msg.strip().lower()

    choices = []

    # 📚 BOOK PRIORITY
    for b in book:

        low = b.lower()

        # 🚫 no mirror
        if low == msg:
            continue

        # 🚫 anti repeat
        if low in last_responses:
            continue

        # ⭐ keyword boost
        score = 2

        if any(word in low for word in msg.split()):
            score += 3

        for i in range(score):
            choices.append(b)

    # 🧠 MEMORY
    for m in memory:

        low = m.lower()

        if low == msg:
            continue

        if low in last_responses:
            continue

        score = 1

        if any(word in low for word in msg.split()):
            score += 2

        for i in range(score):
            choices.append(m)

    # ❌ nothing found
    if not choices:
        return "Хмм... навіть не знаю що сказати 😄"

    # 🎲 random smart pick
    response = random.choice(choices)

    # 💾 save cache
    last_responses.append(response.lower())

    # limit cache
    if len(last_responses) > MAX_CACHE:
        last_responses.pop(0)

    return response
