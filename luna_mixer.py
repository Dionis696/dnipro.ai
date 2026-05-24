import random

# 🧠 cache останніх відповідей
last_responses = []

MAX_CACHE = 15


def pick_response(book, memory, msg):

    global last_responses

    # cleanup
    book = [x.strip() for x in book if x and x.strip()]
    memory = [x.strip() for x in memory if x and x.strip()]

    msg = msg.strip().lower()

    choices = []

    # 📚 BOOK PRIORITY (живі фрази)
    for b in book:

        low = b.lower()

        # 🚫 no mirror
        if low == msg:
            continue

        # 🚫 anti repeat
        if low in last_responses:
            continue

        score = 3  # 🔥 підсилюємо книгу

        if any(word in low for word in msg.split()):
            score += 3

        for _ in range(score):
            choices.append(b)

    # 🧠 MEMORY (трохи рідше)
    for m in memory:

        low = m.lower()

        if low == msg:
            continue

        if low in last_responses:
            continue

        score = 2

        if any(word in low for word in msg.split()):
            score += 2

        for _ in range(score):
            choices.append(m)

    # ❌ якщо нічого нема → беремо з BOOK напряму
    if not choices:

        fallback = []

        fallback.extend(book)
        fallback.extend(memory)

        if not fallback:
            return "щось ти мене загнав 😏"

        response = random.choice(fallback)

    else:
        # 🎲 smart random
        response = random.choice(choices)

    # 💾 cache
    last_responses.append(response.lower())

    if len(last_responses) > MAX_CACHE:
        last_responses.pop(0)

    return response
