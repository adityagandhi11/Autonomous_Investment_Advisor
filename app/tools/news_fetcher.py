"""News fetching tools for market sentiment analysis."""

import httpx
import os


def fetch_market_news(query: str = "india stock market") -> dict:
    """
    Fetch market news from NewsAPI.
    Useful for sentiment analysis in portfolio decisions.
    """
    key = os.getenv("NEWS_API_KEY")

    if not key or key == "your_newsapi_key_here":
        return {"articles": [], "warning": "NEWS_API_KEY not configured"}

    url = (
        "https://newsapi.org/v2/everything"
        f"?q={query}&language=en&pageSize=5&apiKey={key}"
    )

    try:
        response = httpx.get(url, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
