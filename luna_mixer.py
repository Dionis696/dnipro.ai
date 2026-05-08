import random

def pick_response(book, memory, msg):

    book = book or []
    memory = memory or []

    b = random.choice(book) if book else ""
    m = random.choice(memory) if memory else ""

    # 🔥 PRIORITY LOGIC
    if "?" in msg:
        return m if m else b

    # 🔥 MIX MODE
    if random.random() > 0.5:
        return b
    else:
        return m
