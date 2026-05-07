from flask import Flask, request, jsonify
import random
import time
import re

app = Flask(__name__)

# =========================
# 📚 БАЗА
# =========================

book = []

def load_book():
    global book
    try:
        with open("luna_book_big.txt", "r", encoding="utf-8") as f:
            book = [x.strip() for x in f if x.strip()]
    except:
        book = ["я тут 🙂"]

load_book()

# =========================
# 🧠 STATE
# =========================

last_time = 0
COOLDOWN = 3

mode = "normal"
last_activity = time.time()

# =========================
# 🎧 PEAK DETECT
# =========================

def is_peak(msg):
    triggers = ["DJ", "Club", "☆", "★", "ıllı", "▓", "✪"]
    return any(t in msg for t in triggers)

# =========================
# 💬 PICK
# =========================

def pick():
    if not book:
        return "я тут 🙂"
    return random.choice(book)

# =========================
# 💤 IDLE
# =========================

idle_phrases = [
    "в клубі тихо сьогодні",
    "де всі поділись?",
    "DJ мовчить…",
    "давайте трохи руху",
    "тиша дивна сьогодні"
]

def idle():
    return random.choice(idle_phrases)

# =========================
# 🧠 MAIN LOGIC
# =========================

def process(user, msg):
    global last_time, mode, last_activity

    now = time.time()

    # cooldown
    if now - last_time < COOLDOWN:
        return ""

    if not msg:
        return ""

    msg_low = msg.lower()
    last_activity = now

    # mode
    if is_peak(msg):
        mode = "peak"
    else:
        if now - last_activity > 600:
            mode = "idle"
        else:
            mode = "normal"

    # =========================
    # 🎯 1. якщо звернулись
    # =========================

    if "luna" in msg_low or "луна" in msg_low:
        last_time = now
        return pick()

    # =========================
    # 🔥 2. peak mode (інколи реагує)
    # =========================

    if mode == "peak" and random.random() < 0.25:
        last_time = now
        return pick()

    # =========================
    # 💤 3. idle mode
    # =========================

    if mode == "idle" and random.random() < 0.15:
        last_time = now
        return idle()

    return ""

# =========================
# 🌐 API
# =========================

@app.route("/")
def home():
    return "Luna AI ONLINE"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json or {}

        user = data.get("user", "unknown")
        message = data.get("message", "")

        reply = process(user, message)

        # ❗ ВАЖЛИВО: НЕ ДАЄМО ПУСТОГО ПОВІДОМЛЕННЯ В LSL
        if not reply:
            reply = ""

        return jsonify({"reply": reply})

    except:
        return jsonify({"reply": ""})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
