import requests
import random
import re

# =========================
# 🧠 WIKI TRIGGERS (60+)
# =========================

WIKI_TRIGGERS = [

# 📚 базові
"що таке","що це","що означає","що значить","в чому суть",
"як це працює","поясни","поясни мені","розкажи","розкажи про",
"дай інфу","дай інформацію","хочу знати","що воно таке","шо це",

# 👤 люди
"хто такий","хто така","хто це","ким є","біографія",
"чим відомий","чим відома","що зробив","що зробила",
"про людину","інфа про людину",

# 🌍 місця
"де це","де знаходиться","що за місто","що за країна",
"столиця","населення","яка країна","яке місто",
"про місто","про країну",

# 🧠 знання
"інформація про","факти про","цікаві факти","детальніше",
"більше про","що відомо про","з чого складається",
"як виникло","історія","походження",
"для чого потрібно","навіщо це","яка роль",

# 🔬 наука
"як працює","принцип роботи","механізм",
"структура","система","алгоритм","що всередині",

# 🎧 музика
"що за трек","що за музика","хто співає",
"хто автор","про що пісня","жанр","що означає трек",

# 🌐 англ
"what is","who is","tell me about","explain",
"information about","define","meaning of",
"facts about","history of","who created","what does mean",

# 🔍 непрямі
"вікі","wiki","wikipedia","знайди","погугли",
"перевір","почитай","що це взагалі",
"розбери","аналіз","розкажи детальніше"
]


# =========================
# 🧠 SMART TRIGGER
# =========================

def is_smart_wiki_trigger(msg):

    msg = msg.lower()

    # ❌ ігноруємо тупий чат
    if any(x in msg for x in [
        "привіт","хай","hi","лол","ахах","😂","ок","ага"
    ]):
        return False

    # ✅ довгий текст
    if len(msg) > 25:
        return True

    # ✅ знак питання
    if "?" in msg:
        return True

    return False


# =========================
# 🔎 ЧИ ТРЕ ВІКІ
# =========================

def should_use_wiki(msg):

    msg_l = msg.lower()

    if any(x in msg_l for x in WIKI_TRIGGERS):
        return True

    if is_smart_wiki_trigger(msg_l):
        return True

    return False


# =========================
# 🌍 CLEAN QUERY
# =========================

def clean_query(text):

    text = text.lower()

    for t in WIKI_TRIGGERS:
        text = text.replace(t, "")

    text = re.sub(r"[^a-zа-яіїєґ0-9 ]", "", text)

    text = text.strip()

    return text


# =========================
# 🌐 GET WIKI
# =========================

def get_wiki_answer(query):

    q = clean_query(query)

    if not q:
        q = query

    url = "https://uk.wikipedia.org/api/rest_v1/page/summary/" + q

    try:
        r = requests.get(url, timeout=5)

        if r.status_code != 200:
            return None

        data = r.json()

        text = data.get("extract")

        if not text:
            return None

        # ✂️ обрізаємо
        if len(text) > 300:
            text = text[:300].rsplit(".", 1)[0] + "..."

        return text

    except:
        return None
