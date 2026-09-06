"""Portfolio Builder Agent - constructs data-informed portfolios."""

import json
import re

from langchain_groq import ChatGroq

from app.config import settings
from app.services.rag_service import retrieve_investment_guidance
from app.services.investment_guidance_service import get_investment_guidance


llm = ChatGroq(model=settings.groq_model, temperature=0)


def _fallback_allocation(risk: str) -> dict[str, float]:
    """Return a valid baseline when the model cannot produce usable JSON."""
    allocations = {
        "low": {
            "NIFTYBEES.NS": 0.50,
            "GOLDBEES.NS": 0.30,
            "HDFCBANK.NS": 0.20,
        },
        "high": {
            "NIFTYBEES.NS": 0.35,
            "JUNIORBEES.NS": 0.30,
            "INFY.NS": 0.20,
            "HDFCBANK.NS": 0.15,
        },
        "moderate": {
            "NIFTYBEES.NS": 0.45,
            "JUNIORBEES.NS": 0.20,
            "GOLDBEES.NS": 0.20,
            "HDFCBANK.NS": 0.15,
        },
    }
    return allocations.get(risk, allocations["moderate"])


def _extract_json(content: str) -> dict:
    """Accept plain or markdown-wrapped JSON from the model."""
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if not match:
        raise ValueError("Model response did not contain a JSON object")
    return json.loads(match.group(0))


def _model_allocation(state) -> tuple[dict[str, float], str]:
    research_data = state.get("research_data", {})
    market_data = research_data.get("assets", research_data)
    news_data = research_data.get("news", {}) if isinstance(research_data, dict) else {}
    indicators = research_data.get("indicators", {}) if isinstance(research_data, dict) else {}
    allowed_assets = set(market_data)
    if not allowed_assets:
        raise ValueError("No market data is available for model analysis")

    guidance = retrieve_investment_guidance(
        f"{state['risk_profile']} risk portfolio for {state['duration_years']} years"
    )
    news = [
        {"title": article.get("title"), "description": article.get("description")}
        for article in news_data.get("articles", [])[:5]
        if isinstance(article, dict)
    ] if isinstance(news_data, dict) else []

    prompt = f"""
You are a portfolio construction model. Use the supplied market snapshot as evidence,
but do not invent prices or metrics. Build a diversified Indian investment portfolio.

Investor goal: {state['user_goal']}
Investment amount: {state['investment_amount']}
Horizon: {state['duration_years']} years
Risk profile: {state['risk_profile']}
Market snapshot: {json.dumps(market_data, default=str)}
Recent news: {json.dumps(news, default=str)}
Calculated indicators: {json.dumps(indicators, default=str)}
Retrieved investment guidance: {json.dumps(guidance, default=str)}

Return ONLY valid JSON in this shape:
{{
  "allocations": {{"TICKER": weight_as_decimal}},
  "rationale": "brief evidence-based explanation"
}}

Rules:
- Use only tickers present in the market snapshot.
- Use at least 3 tickers when at least 3 are available.
- Every weight must be greater than 0 and no weight may exceed 0.60.
- Weights must sum to exactly 1.0.
- Consider the risk profile, horizon, diversification, prices, returns, volatility, and calculated indicators.
- Use retrieved guidance and news as context, but do not treat either as guaranteed facts or predictions.
"""
    response = llm.invoke(prompt)
    payload = _extract_json(response.content)
    raw_allocations = payload.get("allocations")
    if not isinstance(raw_allocations, dict):
        raise ValueError("Model response did not contain allocations")

    allocations = {asset: float(weight) for asset, weight in raw_allocations.items()}
    if not allocations or not set(allocations).issubset(allowed_assets):
        raise ValueError("Model selected an asset outside the market snapshot")
    if len(allocations) < min(3, len(allowed_assets)):
        raise ValueError("Model portfolio is not diversified")
    if any(weight <= 0 or weight > 0.60 for weight in allocations.values()):
        raise ValueError("Model allocation violates weight limits")
    if abs(sum(allocations.values()) - 1.0) > 0.001:
        raise ValueError("Model allocations do not sum to 1.0")

    return allocations, str(payload.get("rationale", "Model allocation based on market data"))


def portfolio_builder_agent(state):
    """Build a portfolio using the market snapshot, with a safe fallback."""
    risk = state["risk_profile"]
    amount = state["investment_amount"]
    try:
        allocation, rationale = _model_allocation(state)
        source = "model"
    except Exception as error:
        allocation = _fallback_allocation(risk)
        rationale = f"Model analysis unavailable; used baseline allocation: {error}"
        source = "fallback"

    portfolio = {
        asset: round(amount * weight, 2)
        for asset, weight in allocation.items()
    }
    
    # Enrich recommendations with detailed investment guidance
    recommendations = []
    for asset, weight in allocation.items():
        investment_details = get_investment_guidance(asset)
        recommendations.append({
            "symbol": asset,
            "weight": weight,
            "amount": portfolio[asset],
            "details": investment_details
        })

    return {
        "portfolio": portfolio,
        "recommendations": recommendations,
        "history": state["history"] + [{
            "agent": "portfolio_builder",
            "output": {
                "source": source,
                "allocations": allocation,
                "rationale": rationale,
                "market_data_used": bool(state.get("research_data")),
                "rag_guidance_used": source == "model",
            }
        }]
    }
