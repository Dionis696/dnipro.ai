import requests
import re

# =========================
# 🧠 WIKI TRIGGERS (РОЗШИРЕНІ)
# =========================

WIKI_TRIGGERS = [
    # 🇺🇦 ПИТАННЯ
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

    # 🇬🇧 ENG
    "what is","who is","tell me about","explain",
    "define","meaning of","facts about","history of",

    # 🔎 ПРЯМІ
    "вікі","wiki","wikipedia","знайди","погугли",

    # 🔥 ДОДАТКОВІ (ЩОБ ЛОВИЛО ВСЕ)
    "шо за","шо це таке","шо означає",
    "розкажи детальніше","дай більше інформації",
    "шо воно","шо за штука",
    "як воно працює","як це влаштовано",

    "хто він","хто вона","шо це взагалі",
    "це що","це хто",

    "more about","info about","details about",
    "explain this","tell me more"
]


# =========================
# 🔎 SHOULD USE WIKI
# =========================

def should_use_wiki(msg):
    msg = msg.lower()
    if any(t in msg for t in WIKI_TRIGGERS):
        return True
    if "?" in msg and len(msg) > 5:
        return True
    return False


# =========================
# 🧼 CLEAN QUERY
# =========================

def clean_query(text):
    text = text.lower()
    for t in WIKI_TRIGGERS:
        text = text.replace(t, "")
    text = re.sub(r"[^a-zа-яіїєґ0-9 ]", "", text)
    return text.strip()


# =========================
# 🌍 GET WIKI (SEARCH + SUMMARY)
# =========================

def get_wiki_answer(query):
    print("WIKI QUERY:", query)
    q = clean_query(query)
    if not q:
        q = query.lower()

    try:
        # 🔍 1. SEARCH
        search_url = "https://uk.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": q,
            "format": "json"
        }

        r = requests.get(search_url, params=search_params, timeout=5)
        
        # Перевірка статусу відповіді, щоб уникнути помилок парсингу
        if r.status_code != 200:
            print("WIKI SEARCH ERROR: status", r.status_code)
            return None

        data = r.json()
        results = data.get("query", {}).get("search", [])

        if not results:
            print("WIKI: нічого не знайдено")
            return None

        title = results[0]["title"]
        print("WIKI TITLE:", title)

        # 📄 2. SUMMARY
        summary_url = f"https://uk.wikipedia.org/api/rest_v1/page/summary/{title}"
        r2 = requests.get(summary_url, timeout=5)

        # Перевірка статусу відповіді[cite: 3]
        if r2.status_code != 200:
            print("WIKI SUMMARY ERROR: status", r2.status_code)
            return None

        data2 = r2.json()
        text = data2.get("extract")

        if not text:
            return None

        # ✂️ скорочення
        if len(text) > 400:
            text = text[:400].rsplit(".", 1)[0] + "..."

        return text

    except Exception as e:
        print("WIKI ERROR:", e)
        return None
