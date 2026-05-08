import random

def pick_response(book, memory, msg):

    # cleanup
    book = [x for x in book if x and x.strip()]
    memory = [x for x in memory if x and x.strip()]

    # priority to book
    choices = []

    # 📚 book має більшу вагу
    for b in book:
        choices.extend([b, b])

    # 🧠 memory меншу
    for m in memory:
        choices.append(m)

    if not choices:
        return ""

    response = random.choice(choices)

    # 🚫 no raw user mirror
    if response.strip().lower() == msg.strip().lower():
        return ""

    return response
