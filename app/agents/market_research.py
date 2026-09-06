"""Market Research Agent - analyzes market data and trends."""

from app.tools.market_tools import fetch_market_snapshot
from app.tools.news_fetcher import fetch_market_news
from app.tools.calculators import (
    calculate_expected_return,
    calculate_risk,
    calculate_sharpe_ratio,
)


def market_research_agent(state):
    """
    Fetch and analyze market data for investment decision-making.
    """
    market_data = fetch_market_snapshot()
    news = fetch_market_news()
    positions = [
        {
            "value": data.get("price", 0) or 0,
            "volatility": (data.get("annualized_volatility_pct") or 0) / 100,
            "expected_return": (data.get("monthly_return_pct") or 0) / 100,
        }
        for data in market_data.values()
        if isinstance(data, dict) and data.get("price") is not None
    ]
    monthly_returns = [
        (data.get("monthly_return_pct") or 0) / 100
        for data in market_data.values()
        if isinstance(data, dict) and data.get("monthly_return_pct") is not None
    ]
    indicators = {
        "average_risk": calculate_risk(positions),
        "weighted_monthly_return_pct": calculate_expected_return(positions),
        "monthly_sharpe_ratio": calculate_sharpe_ratio(monthly_returns, risk_free_rate=0),
    }

    return {
        "research_data": {
            "assets": market_data,
            "news": news,
            "indicators": indicators,
        },
        "recommendations": state.get("recommendations", []),
        "history": state["history"] + [{
            "agent": "market_research",
            "output": {
                "assets": market_data,
                "news_articles": len(news.get("articles", [])) if isinstance(news, dict) else 0,
            }
        }]
    }
