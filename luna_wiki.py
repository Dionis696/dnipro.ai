import requests
import re

# =========================
# 🧠 WIKI TRIGGERS
# =========================

WIKI_TRIGGERS = [

"що таке","що це","що означає","що значить","в чому суть",
"як це працює","поясни","поясни мені","розкажи","розкажи про",
"дай інфу","дай інформацію","хочу знати","що воно таке","шо це",

"хто такий","хто така","хто це","ким є","біографія",
"чим відомий","чим відома","що зробив","що зробила",

"де це","де знаходиться","що за місто","що за країна",
"столиця","населення","яка країна","яке місто",

"інформація про","факти про","цікаві факти",
"більше про","що відомо про","з чого складається",
"як виникло","історія","походження",

"як працює","принцип роботи","механізм",
"структура","система","алгоритм",

"what is","who is","tell me about","explain",
"define","meaning of","facts about","history of",

"вікі","wiki","wikipedia","знайди","погугли"
]


# =========================
# 🔎 SHOULD USE WIKI
# =========================

def should_use_wiki(msg):

    msg = msg.lower()

    if any(t in msg for t in WIKI_TRIGGERS):
        return True

    if "?" in msg and 8 < len(msg) < 80:
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

    return text.strip()


# =========================
# 🌐 GET WIKI
# =========================

def get_wiki_answer(query):

    q = clean_query(query)

    if not q:
        q = query.lower()

    q = q.replace(" ", "_")

    url = "https://uk.wikipedia.org/api/rest_v1/page/summary/" + q

    try:
        r = requests.get(url, timeout=5)

        # fallback
        if r.status_code != 200:

            q2 = query.lower().replace(" ", "_")
            url2 = "https://uk.wikipedia.org/api/rest_v1/page/summary/" + q2

            r = requests.get(url2, timeout=5)

            if r.status_code != 200:
                return None

        data = r.json()
        text = data.get("extract")

        if not text:
            return None

        if len(text) > 300:
            text = text[:300].rsplit(".", 1)[0] + "..."

        return text

    except:
        return None
