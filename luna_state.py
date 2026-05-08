import time

# =========================
# 🧠 STATE ENGINE
# =========================

active_session_user = None
session_until = 0

stop_until = 0
last_activity_time = time.time()


# =========================
# 🟢 SESSION CONTROL
# =========================

def open_session(user):
    global active_session_user, session_until

    active_session_user = user
    session_until = time.time() + 120  # 2 хв

def in_session(user):
    global active_session_user, session_until

    return (
        active_session_user == user and
        time.time() < session_until
    )

def close_session():
    global active_session_user, session_until

    active_session_user = None
    session_until = 0


# =========================
# 🔴 STOP SYSTEM
# =========================

def trigger_stop():
    global stop_until
    stop_until = time.time() + 600  # 10 хв


def can_talk():
    return time.time() >= stop_until


def is_stopped():
    return time.time() < stop_until


# =========================
# 🟡 ACTIVITY TRACKING
# =========================

def update_activity():
    global last_activity_time
    last_activity_time = time.time()


def check_idle():
    global last_activity_time

    if time.time() - last_activity_time > 600:
        update_activity()
        return True

    return False
