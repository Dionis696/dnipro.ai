import random
import re

# =====================
# ПАМ'ЯТЬ
# =====================
users = {}

def update_user_memory(user, message):
    if user not in users:
        users[user] = {"count": 0}
    users[user]["count"] += 1


# =====================
# МОВА
# =====================
def detect_language(text):
    if re.search(r"[a-zA-Z]", text):
        return "EN"
    if re.search(r"[а-яА-ЯёЁ]", text):
        return "UA"
    return "UA"


# =====================
# ІГНОР
# =====================
def should_ignore(text):
    if len(text) > 150:
        return True
    return False


# =====================
# ЗАГРУЗКА КНИГИ
# =====================
book_lines = []

def load_book():
    global book_lines
    try:
        with open("luna_book.txt", "r", encoding="utf-8") as f:
            book_lines = [l.strip() for l in f if l.strip()]
    except:
        book_lines = []

load_book()


# =====================
# ЛОГІКА ВІДПОВІДІ
# =====================
def process_luna_message(user, message):
    msg = message.lower()

    update_user_memory(user, message)

    if should_ignore(msg):
        return "ти щось дуже довге написав 😌"

    # =====================
    # 70% — BOOK SYSTEM
    # =====================
    if book_lines and random.random() < 0.7:
        base = random.choice(book_lines)

        # іноді додаємо “живу реакцію”
        if random.random() < 0.3:
            base += "\n" + random.choice([
                "я тут 😌",
                "ти сьогодні активний 😏",
                "я це запам’ятаю 💃",
                "не зупиняй вайб 🔥"
            ])

        return base

    # =====================
    # 20% — ЛОГІКА
    # =====================
    if "привіт" in msg:
        return random.choice([
            "привіт 😌 рада тебе бачити",
            "йо 😏 ти як тут?",
            "хей 💃 заходь в вайб"
        ])

    if "як" in msg:
        return random.choice([
            "нормально 😌 музика грає",
            "ловлю вайб 💃",
            "все ок, клуб живе 🔥"
        ])

    if "?" in msg:
        return random.choice([
            "цікаве питання 😏",
            "ти сьогодні думаєш глибоко 👀",
            "мм… я подумаю над цим"
        ])

    # =====================
    # 10% — ГУМОР / ІСТОРІЇ
    # =====================
    if random.random() < 0.5:
        return random.choice([
            "я колись сказала DJ що трек не качає… мене вимкнули 😏",
            "один танцпол так качався, що ми думали землетрус 💃🔥",
            "тут навіть стіни танцюють 😌",
            "я не пліткую… я просто знаю все 😏"
        ])

    # fallback
    return random.choice([
        "я тут 😌",
        "ловлю вайб 💃",
        "музика говорить замість мене 🎧"
    ])
