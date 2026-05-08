import random

from luna_memory import learn_from_chat, get_random_memory
from luna_mixer import pick_response


# =========================
# 📦 LOAD BOOK
# =========================

def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [x.strip() for x in f if x.strip()]
    except:
        return []


# =========================
# 🧠 LUNA BRAIN
# =========================

class LunaBrain:

    def __init__(self):
        self.book = load_file("luna_book.txt")

    # =========================
    # 🔥 MAIN ENGINE
    # =========================

    def reply(self, user, msg):

        if not msg:
            return "..."

        # 1. навчаємось
        learn_from_chat(user, msg)

        # 2. memory
        memory = get_random_memory()

        # 3. book (характер)
        book_pick = random.choice(self.book) if self.book else ""

        # 4. system intents (анти-зациклення)
        msg_low = msg.lower()

        if "?" in msg_low:
            context_type = "question"
        elif any(x in msg_low for x in ["dj", "музика", "сет", "клуб"]):
            context_type = "club"
        else:
            context_type = "chat"

        # 5. mixer decision
        response = pick_response(
            [book_pick],
            [memory],
            msg
        )

        # 6. fallback FIX (більше немає "я тут 🙂 spam")
        if not response or response.strip() == "":
            if context_type == "question":
                return "цікаве питання 😏"
            elif context_type == "club":
                return "клубна атмосфера змінюється 🔥"
            else:
                return "слухаю тебе"

        return response


# =========================
# 🔥 INSTANCE
# =========================

luna = LunaBrain()


def handle_message(user, message):
    return luna.reply(user, message)
