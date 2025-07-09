# backend/app/services/fetch_news.py
import os
import httpx
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# NewsAPI supports only these country codes:
SUPPORTED_COUNTRIES = {
    'ae','ar','at','au','be','bg','br','ca','ch','cn','co','cu','cz','de','eg','fr',
    'gb','gr','hk','hu','id','ie','il','in','it','jp','kr','lt','lv','ma','mx','my',
    'ng','nl','no','nz','ph','pl','pt','ro','rs','ru','sa','se','sg','si','sk','th',
    'tr','tw','ua','us','ve','za'
}

def fetch_by_country(country_code: str) -> list[dict]:
    """
    Fetches top headlines for a country, with fallback to global headlines.
    Returns list of { title, url, source }.
    """
    if not NEWS_API_KEY:
        return []

    # 1) Normalize and validate country code
    code = (country_code or "").lower()
    if code not in SUPPORTED_COUNTRIES:
        code = "us"  # fallback default

    # 2) Try top-headlines
    headlines = _call_top_headlines(code)
    if headlines:
        return headlines

    # 3) Fallback to global everything query
    return _call_everything_top()

def _call_top_headlines(code: str) -> list[dict]:
    url = "https://newsapi.org/v2/top-headlines"
    params = {"country": code, "apiKey": NEWS_API_KEY, "pageSize": 10}
    try:
        r = httpx.get(url, params=params, timeout=5.0)
        r.raise_for_status()
        data = r.json()
        if data.get("status") != "ok":
            return []
        return [
            {
                "title": a.get("title","No title"),
                "url": a.get("url","#"),
                "source": a.get("source",{}).get("name","Unknown")
            }
            for a in data.get("articles",[])
        ]
    except Exception:
        return []

def _call_everything_top() -> list[dict]:
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "news",                # keyword fallback
        "language": "en",
        "sortBy": "popularity",
        "pageSize": 10,
        "apiKey": NEWS_API_KEY
    }
    try:
        r = httpx.get(url, params=params, timeout=5.0)
        r.raise_for_status()
        data = r.json()
        if data.get("status") != "ok":
            return []
        return [
            {
                "title": a.get("title","No title"),
                "url": a.get("url","#"),
                "source": a.get("source",{}).get("name","Unknown")
            }
            for a in data.get("articles",[])
        ]
    except Exception:
        return []
