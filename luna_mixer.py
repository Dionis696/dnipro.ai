import random

def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [x.strip() for x in f if x.strip()]
    except:
        return []


def pick_response(book, memory, msg):

    # 1. book = стиль
    b = random.choice(book) if book else ""

    # 2. memory = досвід
    m = random.choice(memory) if memory else ""

    # 3. логіка змішування
    if "?" in msg:
        return m if m else b

    if len(msg) > 30:
        return b

    # мікс
    if random.random() > 0.5:
        return b
    else:
        return m
