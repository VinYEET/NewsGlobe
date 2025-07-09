# backend/app/services/geo_utils.py
import httpx

USER_AGENT = "YourAppName/1.0 (your.email@example.com)"

def get_country_code(lat: float, lon: float) -> str:
    """
    Reverse-geocode via OSM Nominatim to get ISO country code.
    Returns lowercase two-letter code (e.g. 'us'), or '' on failure.
    """
    try:
        resp = httpx.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={
                "format": "json",
                "lat": lat,
                "lon": lon,
                "zoom": 5,               # country-level
                "addressdetails": 1
            },
            headers={"User-Agent": USER_AGENT},
            timeout=5.0
        )
        resp.raise_for_status()
        data = resp.json()
        addr = data.get("address", {})
        code = addr.get("country_code", "")
        return code.lower()
    except Exception:
        return ""
