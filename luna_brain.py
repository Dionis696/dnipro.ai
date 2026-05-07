import random
import time
import re

book_lines = []

def load_book():
    global book_lines
    try:
        with open("luna_book_big.txt", "r", encoding="utf-8") as f:
            book_lines = [x.strip() for x in f if x.strip()]
    except:
        book_lines = ["я тут 🙂"]

load_book()

last_time = 0
COOLDOWN = 3

mode = "normal"
last_activity = time.time()


def is_peak(msg):
    triggers = ["DJ", "Club", "☆", "★", "ıllı", "▓", "✪"]
    return any(t in msg for t in triggers)


def pick():
    if not book_lines:
        return "я тут 🙂"
    return random.choice(book_lines)


def idle():
    return random.choice([
        "в клубі тихо…",
        "де всі?",
        "DJ сьогодні мовчить",
        "дивний спокій",
        "давайте рух"
    ])


def process_luna_message(user, msg):
    global last_time, mode, last_activity

    now = time.time()

    # ❗ cooldown
    if now - last_time < COOLDOWN:
        return ""

    if not msg:
        return ""

    msg_low = msg.lower()
    last_activity = now

    # режим
    if is_peak(msg):
        mode = "peak"
    elif now - last_activity > 600:
        mode = "idle"
    else:
        mode = "normal"

    # 🎯 пряме звернення
    if "luna" in msg_low or "луна" in msg_low:
        last_time = now
        return pick()

    # 🔥 peak інколи
    if mode == "peak" and random.random() < 0.25:
        last_time = now
        return pick()

    # 💤 idle інколи
    if mode == "idle" and random.random() < 0.15:
        last_time = now
        return idle()

    return ""
