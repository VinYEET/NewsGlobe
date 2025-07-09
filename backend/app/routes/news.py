from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List

# stub imports — we’ll implement these next
from app.services import geo_utils, fetch_news

router = APIRouter()

class Article(BaseModel):
    title: str
    url:   str
    source:str

class NewsWithCountry(BaseModel):
    country: str
    articles: List[Article]
@router.get("",  response_model=NewsWithCountry)  # handles GET /news
@router.get("/", response_model=NewsWithCountry)  # handles GET /news/
async def get_news(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    # 1) map lat/lon → country code
    country = geo_utils.get_country_code(lat, lon)
    if not country:
        raise HTTPException(404, f"Could not resolve country at {lat},{lon}")

    # 2) fetch top headlines for that country
    raw = fetch_news.fetch_by_country(country)

    # 3) map to our Article model
    articles = [
        Article(title=a["title"], url=a["url"], source=a["source"])
        for a in raw
    ]
    # return the country code along with the articles
    return NewsWithCountry(country=country, articles=articles)