import requests
import re

# =========================
# 🧠 WIKI TRIGGERS (ЗВУЖЕНІ - ТІЛЬКИ ПИТАННЯ ПРО СУТЬ)
# =========================

WIKI_TRIGGERS = [
    "що таке", "хто такий", "хто така", "що означає", "поясни що таке",
    "розкажи про", "інформація про", "факти про", "історія",
    "what is", "who is", "explain", "tell me about"
]

# Додаємо User-Agent для стабільності
HEADERS = {'User-Agent': 'LunaBot/1.0 (ClubDniproClub; contact: admin)'}

# =========================
# 🔎 SHOULD USE WIKI
# =========================

def should_use_wiki(msg):
    msg = msg.lower()
    # Wiki спрацює тільки якщо в повідомленні є чіткий запит на визначення
    return any(t in msg for t in WIKI_TRIGGERS)

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
    q = clean_query(query)
    if not q or len(q) < 3: return None # Ігноруємо надто короткі запити

    try:
        search_url = "https://uk.wikipedia.org/w/api.php"
        search_params = {"action": "query", "list": "search", "srsearch": q, "format": "json"}
        
        r = requests.get(search_url, params=search_params, headers=HEADERS, timeout=5)
        if r.status_code != 200: return None

        results = r.json().get("query", {}).get("search", [])
        if not results: return None

        title = results[0]["title"]
        summary_url = f"https://uk.wikipedia.org/api/rest_v1/page/summary/{title}"
        r2 = requests.get(summary_url, headers=HEADERS, timeout=5)

        if r2.status_code != 200: return None
        text = r2.json().get("extract")
        
        if not text: return None

        # Скорочення тексту
        if len(text) > 300:
            text = text[:300].rsplit(".", 1)[0] + "..."
        return text

    except Exception:
        return None
