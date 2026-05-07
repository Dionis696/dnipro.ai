import random
import time

book = []

def load_book():
    global book
    try:
        with open("luna_book_big.txt", "r", encoding="utf-8") as f:
            book = [x.strip() for x in f if x.strip()]
    except:
        book = ["я тут 🙂"]

load_book()

last_time = 0
COOLDOWN = 2

mode = "normal"
last_activity = time.time()


def pick():
    return random.choice(book) if book else "я тут 🙂"


def idle():
    return random.choice([
        "в клубі тихо сьогодні",
        "де всі поділись?",
        "DJ мовчить…",
        "давайте рух",
        "дивна тиша"
    ])


def process_luna_message(user, msg):
    global last_time, mode, last_activity

    now = time.time()

    # ❗ анти-спам
    if now - last_time < COOLDOWN:
        return ""

    if not msg:
        return ""

    msg_low = msg.lower()
    last_activity = now

    # режим
    if now - last_activity > 600:
        mode = "idle"

    # 🔥 тригери
    trigger = (
        "luna" in msg_low or
        "луна" in msg_low or
        "привіт" in msg_low or
        "тиша" in msg_low
    )

    # 💬 реакція
    if trigger:
        last_time = now
        return pick()

    # 🔥 idle інколи говорить сама
    if mode == "idle" and random.random() < 0.15:
        last_time = now
        return idle()

    return ""
