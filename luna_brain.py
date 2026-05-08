import random

from luna_memory import learn_from_chat, get_random_memory
from luna_mixer import pick_response


def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [x.strip() for x in f if x.strip()]
    except:
        return []


class LunaBrain:

    def __init__(self):
        self.book = load_file("luna_book.txt")

    def reply(self, user, msg):

        if not msg:
            return "..."

        # 🧠 LEARN ALWAYS
        learn_from_chat(user, msg)

        memory = get_random_memory()

        book_pick = random.choice(self.book) if self.book else ""

        response = pick_response(
            [book_pick],
            [memory],
            msg
        )

        # 🔥 ANTI ECHO FIX (КРИТИЧНО)
        if response.strip() == msg.strip():
            response = random.choice(self.book) if self.book else "я тут 😌"

        # fallback
        if not response:
            response = "я тут 😌"

        return response


luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)
