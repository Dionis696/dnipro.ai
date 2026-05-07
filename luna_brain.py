import random
import re
import time

# =========================
# 📚 БАЗА ФРАЗ
# =========================

book_lines = []

def load_book():
    global book_lines
    try:
        with open("luna_book_big.txt", "r", encoding="utf-8") as f:
            book_lines = [x.strip() for x in f if x.strip()]
    except:
        book_lines = []

load_book()

# =========================
# 🧠 СТАН
# =========================

last_time = 0
COOLDOWN = 3

luna_mode = "normal"  # normal / peak / idle
last_activity = time.time()

# =========================
# 🎧 DJ / PEAK DETECT
# =========================

def is_peak(msg):
    keywords = ["DJ", "Club", "☆", "★", "ıllı", "▓", "✪", "COMЕ", "█"]
    return any(k in msg for k in keywords)

# =========================
# 🌍 МОВА (простий режим)
# =========================

def detect_lang(text):
    if re.search(r"[a-zA-Z]", text):
        return "EN"
    return "UA"

# =========================
# 💬 ВИБІР ФРАЗИ
# =========================

def pick():
    if not book_lines:
        return "я тут 🙂"
    return random.choice(book_lines)

# =========================
# 💤 IDLE
# =========================

idle_phrases = [
    "в клубі трохи тихо сьогодні",
    "де всі пропали?",
    "DJ мовчить сьогодні",
    "давайте трохи руху",
    "тиша якась цікава"
]

def idle():
    return random.choice(idle_phrases)

# =========================
# 🧠 MAIN ENGINE
# =========================

def process_luna_message(user, msg):
    global last_time, luna_mode, last_activity

    now = time.time()

    # cooldown
    if now - last_time < COOLDOWN:
        return ""

    if not msg:
        return ""

    msg_low = msg.lower()

    # оновлення активності
    last_activity = now

    # PEAK MODE
    if is_peak(msg):
        luna_mode = "peak"
    else:
        if now - last_activity > 600:
            luna_mode = "idle"
        else:
            luna_mode = "normal"

    # ❗ ВАЖЛИВО: реагуємо тільки на "luna"
    if "luna" not in msg_low and "луна" not in msg_low:

        # idle іноді говорить
        if luna_mode == "idle" and random.random() < 0.2:
            last_time = now
            return idle()

        return ""

    # 🔥 PEAK
    if luna_mode == "peak":
        reply = pick()
        last_time = now
        return reply

    # 💬 NORMAL
    reply = pick()

    last_time = now
    return reply
