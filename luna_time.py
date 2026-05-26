import random
import time
from datetime import datetime
import pytz

# 🇺🇦 timezone Київ
KYIV_TZ = pytz.timezone("Europe/Kyiv")

# 🔥 інтервал (60–80 хв)
MIN_DELAY = 3600
MAX_DELAY = 4800

# ✅ старт таймера
next_trigger = int(time.time()) + random.randint(MIN_DELAY, MAX_DELAY)


# =========================
# 🧠 ОТРИМАТИ ЧАС
# =========================

def get_now():
    now = datetime.now(KYIV_TZ)
    return now.hour, now.minute, now.weekday()


# =========================
# 📅 ДЕНЬ ТИЖНЯ
# =========================

def get_day_name(weekday):
    return [
        "понеділок",
        "вівторок",
        "середа",
        "четвер",
        "п’ятниця",
        "субота",
        "неділя"
    ][weekday]


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
# 🎭 ФРАЗА ЧАСУ
# =========================

def build_time_phrase():
    hour, minute, weekday = get_now()

    day_name = get_day_name(weekday)
    period = get_period(hour)

    time_str = f"{hour:02d}:{minute:02d}"

    if period == "morning":
        return random.choice([
            f"☀️ {time_str}… ви взагалі спите? 😄",
            f"{day_name} ранок… а тут вже рух 😏"
        ])

    if period == "day":
        return random.choice([
            f"{time_str}… день іде, а атмосфера росте 😏",
            f"{day_name} день… але тут свій світ 😎"
        ])

    if period == "evening":
        return random.choice([
            f"{time_str}… ідеальний час щоб почати 😏",
            f"{day_name} вечір… ви ж відчуваєте це 🔥"
        ])

    return random.choice([
        f"🌙 {time_str}… ніч тільки почалась 😏",
        f"{day_name} ніч… тут стає цікавіше 🔥"
    ])


# =========================
# ⏱ ЧИ ЧАС ГОВОРИТИ
# =========================

def should_talk_time():
    global next_trigger

    now = int(time.time())  # ✅ беремо один раз

    if now >= next_trigger:
        # ✅ твій фінальний фікс
        next_trigger = now + random.randint(MIN_DELAY, MAX_DELAY)
        return True

    return False


# =========================
# 🚀 ГОЛОВНА
# =========================

def get_time_message():
    if should_talk_time():
        return build_time_phrase()
    return None
