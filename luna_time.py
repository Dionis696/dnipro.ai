import random
import time
from datetime import datetime
import pytz

# 🇺🇦 timezone Київ
KYIV_TZ = pytz.timezone("Europe/Kyiv")

# ⏱ анти-спам
last_time_talk = 0  

# 🔥 інтервал (60–80 хв)
MIN_DELAY = 3600
MAX_DELAY = 4800

next_trigger = time.time() + random.randint(MIN_DELAY, MAX_DELAY)


# =========================
# 🧠 ОТРИМАТИ ЧАС
# =========================

def get_now():

    now = datetime.now(KYIV_TZ)

    hour = now.hour
    minute = now.minute

    weekday = now.weekday()

    return hour, minute, weekday


# =========================
# 📅 ДЕНЬ ТИЖНЯ
# =========================

def get_day_name(weekday):

    days = [
        "понеділок",
        "вівторок",
        "середа",
        "четвер",
        "п’ятниця",
        "субота",
        "неділя"
    ]

    return days[weekday]


# =========================
# 🌙 ПЕРІОД ДНЯ
# =========================

def get_period(hour):

    if 5 <= hour <= 10:
        return "morning"
    elif 11 <= hour <= 17:
        return "day"
    elif 18 <= hour <= 22:
        return "evening"
    else:
        return "night"


# =========================
# 🎭 ГЕНЕРАЦІЯ ФРАЗИ
# =========================

def build_time_phrase():

    hour, minute, weekday = get_now()

    day_name = get_day_name(weekday)
    period = get_period(hour)

    time_str = f"{hour:02d}:{minute:02d}"

    if period == "morning":
        variants = [
            f"☀️ {time_str}… ви взагалі спите? 😄",
            f"{day_name} ранок… а тут вже рух 😏",
            f"{time_str}… новий день, новий вайб 👀"
        ]

    elif period == "day":
        variants = [
            f"{time_str}… день іде, а атмосфера росте 😏",
            f"{day_name} день… але тут свій світ 😎",
            f"☀️ {time_str}… ще не вечір, але вже цікаво 👀"
        ]

    elif period == "evening":
        variants = [
            f"{time_str}… ідеальний час щоб почати 😏",
            f"{day_name} вечір… ви ж відчуваєте це 🔥",
            f"🌆 {time_str}… танцпол чекає 💃"
        ]

    else:
        variants = [
            f"🌙 {time_str}… ніч тільки почалась 😏",
            f"{time_str}… і ти ще тут… мені це подобається 👀",
            f"{day_name} ніч… тут стає цікавіше 🔥"
        ]

    return random.choice(variants)


# =========================
# ⏱ ЧИ ЧАС ГОВОРИТИ
# =========================

def should_talk_time():

    global next_trigger

    now = time.time()

    if now >= next_trigger:
        next_trigger = now + random.randint(MIN_DELAY, MAX_DELAY)
        return True

    return False


# =========================
# 🚀 ГОЛОВНА ФУНКЦІЯ (твоя)
# =========================

def get_time_message():

    if should_talk_time():
        return build_time_phrase()

    return None


# =========================
# ✅ ДОДАНО ДЛЯ LUNA_BRAIN
# =========================

def get_time_data():

    hour, minute, weekday = get_now()

    return {
        "hour": hour,
        "minute": minute,
        "time": f"{hour:02d}:{minute:02d}",
        "day": get_day_name(weekday)
    }


# =========================
# 🔥 LIVE РЕЖИМ (САМА ПИШЕ)
# =========================

def live_loop(send_func):

    while True:

        delay = random.randint(MIN_DELAY, MAX_DELAY)
        time.sleep(delay)

        msg = build_time_phrase()

        if msg:
            send_func(msg)


def start_live_mode(send_func):
    import threading

    t = threading.Thread(target=live_loop, args=(send_func,))
    t.daemon = True
    t.start()
