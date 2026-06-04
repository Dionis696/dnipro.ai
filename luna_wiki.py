import requests
import re

# =========================
# 🧠 WIKI TRIGGERS (ЗВУЖЕНІ)
# =========================
WIKI_TRIGGERS = [
    "що таке", "хто такий", "хто така", "що означає", "поясни що таке",
    "розкажи про", "інформація про", "факти про", "історія",
    "what is", "who is", "explain", "tell me about"
]

HEADERS = {'User-Agent': 'LunaBot/1.0 (ClubDniproClub; contact: admin)'}

# =========================
# 🔎 SHOULD USE WIKI
# =========================

def should_use_wiki(msg):
    msg = msg.lower().strip()
    # Спрацьовує, якщо повідомлення ПОЧИНАЄТЬСЯ з одного з тригерів
    # Це значно зменшує кількість помилкових спрацювань
    return any(msg.startswith(t) for t in WIKI_TRIGGERS)

# =========================
# 🧼 CLEAN QUERY
# =========================

def clean_query(text):
    text = text.lower()
    for t in WIKI_TRIGGERS:
        text = text.replace(t, "")
    # Очищуємо від зайвих символів, залишаючи тільки букви, цифри та пробіли
    text = re.sub(r"[^a-zа-яіїєґ0-9 ]", "", text)
    return text.strip()

# =========================
# 🌍 GET WIKI
# =========================

def get_wiki_answer(query):
    q = clean_query(query)
    if not q or len(q) < 3: 
        return None

    try:
        # 1. Пошук заголовка
        search_url = "https://uk.wikipedia.org/w/api.php"
        search_params = {"action": "query", "list": "search", "srsearch": q, "format": "json"}
        r = requests.get(search_url, params=search_params, headers=HEADERS, timeout=5)
        
        if r.status_code != 200: return None
        results = r.json().get("query", {}).get("search", [])
        if not results: return None

        # 2. Отримання короткого опису (summary)
        title = results[0]["title"]
        summary_url = f"https://uk.wikipedia.org/api/rest_v1/page/summary/{title}"
        r2 = requests.get(summary_url, headers=HEADERS, timeout=5)

        if r2.status_code != 200: return None
        text = r2.json().get("extract")
        
        if not text: return None

        # ✂️ Скорочення для чату (до 300 символів)
        if len(text) > 300:
            text = text[:300].rsplit(".", 1)[0] + "..."
        return text

    except Exception as e:
        print(f"WIKI ERROR: {e}")
        return None
