import requests
import random
import re

# =========================
# 🧠 WIKI TRIGGERS (60+)
# =========================

WIKI_TRIGGERS = [

"що таке","що це","що означає","що значить","в чому суть",
"як це працює","поясни","поясни мені","розкажи","розкажи про",
"дай інфу","дай інформацію","хочу знати","що воно таке","шо це",

"хто такий","хто така","хто це","ким є","біографія",
"чим відомий","чим відома","що зробив","що зробила",
"про людину","інфа про людину",

"де це","де знаходиться","що за місто","що за країна",
"столиця","населення","яка країна","яке місто",
"про місто","про країну",

"інформація про","факти про","цікаві факти","детальніше",
"більше про","що відомо про","з чого складається",
"як виникло","історія","походження",
"для чого потрібно","навіщо це","яка роль",

"як працює","принцип роботи","механізм",
"структура","система","алгоритм","що всередині",

"що за трек","що за музика","хто співає",
"хто автор","про що пісня","жанр","що означає трек",

"what is","who is","tell me about","explain",
"information about","define","meaning of",
"facts about","history of","who created","what does mean",

"вікі","wiki","wikipedia","знайди","погугли",
"перевір","почитай","що це взагалі",
"розбери","аналіз","розкажи детальніше"
]


# =========================
# 🧠 SMART TRIGGER
# =========================

def is_smart_wiki_trigger(msg):

    msg = msg.lower()

    if any(x in msg for x in [
        "привіт","хай","hi","лол","ахах","😂","ок","ага"
    ]):
        return False

    if len(msg) > 25:
        return True

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
        q = query.lower()

    # 🔥 головний фікс
    q = q.replace(" ", "_")

    url = "https://uk.wikipedia.org/api/rest_v1/page/summary/" + q

    try:
        r = requests.get(url, timeout=5)

        # 🔁 fallback (якщо не знайшло)
        if r.status_code != 200:

            # пробуємо без чистки
            q2 = query.lower().replace(" ", "_")
            url2 = "https://uk.wikipedia.org/api/rest_v1/page/summary/" + q2

            r = requests.get(url2, timeout=5)

            if r.status_code != 200:
                return None

        data = r.json()

        text = data.get("extract")

        if not text:
            return None

        # ✂️ обрізка
        if len(text) > 300:
            text = text[:300].rsplit(".", 1)[0] + "..."

        return text

    except:
        return None
