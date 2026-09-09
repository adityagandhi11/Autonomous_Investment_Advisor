"""FastAPI application for Autonomous Investment Advisor."""

from dotenv import load_dotenv

# Load environment variables from .env file FIRST, before any imports
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.graph import investment_graph
from app.models.request_models import InvestmentRequest
from app.models.response_models import InvestmentResponse
from app.services.mongodb_service import save_portfolio, get_portfolio_history
from app.services.market_data_cache_service import (
    get_real_time_price,
    get_market_data_with_cache,
    get_all_market_data_cached,
    clear_market_cache,
    get_cache_stats
)
from app.services.risk_analytics_service import (
    get_asset_risk_metrics,
    get_portfolio_risk_dashboard,
    RiskAnalyticsEngine
)

from app.auth_routes import router as auth_router
from app.investor_routes import router as investor_router

app = FastAPI(
    title="Autonomous Investment Advisor",
    description="Production-grade agentic AI for personalized investment recommendations",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(investor_router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Autonomous Investment Advisor API is running"}


@app.post("/invest", response_model=InvestmentResponse)
async def invest(request: InvestmentRequest):
    """
    Main endpoint for investment recommendation.
    
    Accepts:
    - user_goal: Investment objective (string)
    - investment_amount: Capital in rupees (float)
    - duration_years: Investment horizon (int)
    
    Returns:
    - risk_profile: Determined risk category (low/moderate/high)
    - portfolio: Asset allocation with amounts
    - critique: Validation notes
    - workflow_history: Decision trace from all agents
    """
    try:
        # Initialize agent state
        initial_state = {
            "user_goal": request.user_goal,
            "investment_amount": request.investment_amount,
            "duration_years": request.duration_years,
            "risk_profile": "",
            "research_data": {},
            "portfolio": {},
            "recommendations": [],
            "critique": "",
            "approved": False,
            "history": []
        }

        # Execute the workflow
        result = investment_graph.invoke(initial_state)

        # Persist to MongoDB
        save_portfolio({
            "goal": request.user_goal,
            "amount": request.investment_amount,
            "duration": request.duration_years,
            "risk_profile": result["risk_profile"],
            "portfolio": result["portfolio"],
            "critique": result["critique"]
        })

        return InvestmentResponse(
            risk_profile=result["risk_profile"],
            portfolio=result["portfolio"],
            recommendations=result.get("recommendations"),
            critique=result["critique"],
            workflow_history=result["history"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow error: {str(e)}")


@app.get("/portfolio-history")
async def portfolio_history(limit: int = 10):
    """
    Retrieve past portfolio recommendations from MongoDB.
    """
    history = get_portfolio_history(limit)
    # Convert ObjectId to string for JSON serialization
    for item in history:
        item["_id"] = str(item.get("_id", ""))
    return {"portfolios": history}


@app.post("/rebalance")
async def rebalance(current_portfolio: dict, target_weights: dict):
    """
    Endpoint for portfolio rebalancing.
    Calculates actions needed to align with target allocation.
    """
    from app.agents.rebalancer import rebalancer_agent
    
    try:
        actions = rebalancer_agent(current_portfolio, target_weights)
        return {"rebalancing_actions": actions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Rebalancing error: {str(e)}")


@app.get("/health")
async def health_check():
    """Extended health check with dependency status."""
    return {
        "status": "healthy",
        "service": "Autonomous Investment Advisor",
        "version": "1.0.0"
    }


# ============================================================================
# MARKET DATA ENDPOINTS - Real-time prices with caching
# ============================================================================

@app.get("/market/price/{ticker}")
async def get_price(ticker: str):
    """
    Get real-time price for a ticker with caching.
    Cache TTL: 5 minutes
    
    Example: /market/price/NIFTYBEES.NS
    """
    return get_real_time_price(ticker)


@app.get("/market/data/{ticker}")
async def get_market_data(ticker: str, period: str = "1mo"):
    """
    Get market data (OHLCV, returns, volatility) for a ticker.
    
    Periods: 1d, 5d, 1mo, 3mo, 6mo, 1y
    Includes: price, returns, volatility, 52-week range
    """
    return get_market_data_with_cache(ticker, period)


@app.post("/market/data-multiple")
async def get_multiple_market_data(tickers: list, period: str = "1mo"):
    """
    Get market data for multiple tickers at once.
    
    Example payload:
    {
        "tickers": ["NIFTYBEES.NS", "HDFCBANK.NS", "TCS.NS"],
        "period": "1mo"
    }
    """
    return get_all_market_data_cached(tickers, period)


@app.get("/market/cache-stats")
async def cache_statistics():
    """Get current market data cache statistics."""
    return get_cache_stats()


@app.post("/market/cache-clear")
async def clear_cache():
    """Clear all cached market data (admin endpoint)."""
    clear_market_cache()
    return {"message": "Cache cleared successfully"}


# ============================================================================
# RISK ANALYTICS ENDPOINTS - Advanced portfolio analytics
# ============================================================================

@app.get("/analytics/asset-risk/{ticker}")
async def asset_risk_metrics(ticker: str, period: str = "3mo"):
    """
    Get comprehensive risk metrics for an asset.
    
    Returns:
    - Volatility (annualized standard deviation)
    - Sharpe Ratio (return per unit of risk)
    - Sortino Ratio (downside risk focus)
    - Maximum Drawdown
    - Value at Risk (VaR at 95% and 99% confidence)
    
    Example: /analytics/asset-risk/NIFTYBEES.NS?period=3mo
    """
    return get_asset_risk_metrics(ticker, period)


@app.post("/analytics/portfolio-risk")
async def portfolio_risk_analytics(portfolio: dict):
    """
    Get complete risk analytics dashboard for a portfolio.
    
    Example payload:
    {
        "NIFTYBEES.NS": 25000,
        "HDFCBANK.NS": 15000,
        "TCS.NS": 10000
    }
    
    Returns:
    - Portfolio summary (value, weights, volatility, concentration)
    - Risk assessment
    - Stress test results (market down 10%)
    """
    return get_portfolio_risk_dashboard(portfolio)


@app.post("/analytics/sharpe-ratio")
async def calculate_sharpe_ratio(returns: list):
    """
    Calculate Sharpe Ratio for a list of daily returns.
    
    Higher is better. Negative means underperforming risk-free rate.
    """
    engine = RiskAnalyticsEngine()
    sharpe = engine.calculate_sharpe_ratio(returns)
    return {
        "sharpe_ratio": sharpe,
        "interpretation": "Excellent return per unit of risk" if sharpe > 1 else "Good risk-adjusted returns" if sharpe > 0.5 else "Moderate risk-adjusted returns" if sharpe > 0 else "Underperforming risk-free rate"
    }


@app.post("/analytics/volatility")
async def calculate_volatility(returns: list):
    """Calculate annualized volatility (standard deviation) from daily returns."""
    engine = RiskAnalyticsEngine()
    volatility = engine.calculate_volatility(returns)
    return {"volatility_pct": volatility}


@app.post("/analytics/correlation-matrix")
async def correlation_matrix(tickers: list, period: str = "1mo"):
    """
    Calculate correlation matrix between multiple assets.
    
    Example payload:
    {
        "tickers": ["NIFTYBEES.NS", "GOLDBEES.NS", "HDFCBANK.NS"],
        "period": "1mo"
    }
    
    Correlation closer to 1: assets move together
    Correlation closer to -1: assets move opposite
    Correlation = 0: no relationship
    """
    engine = RiskAnalyticsEngine()
    return engine.calculate_correlation_matrix(tickers, period)


@app.post("/analytics/stress-test")
async def stress_test_portfolio(portfolio: dict, scenario: str = "market_down_10"):
    """
    Simulate portfolio performance under stress scenarios.
    
    Scenarios:
    - market_down_10: 10% market decline
    - market_down_20: 20% market decline
    - market_crash: 35% market crash
    - interest_rate_up: 2% interest rate increase
    
    Example payload:
    {
        "portfolio": {"NIFTYBEES.NS": 25000, "GOLDBEES.NS": 15000},
        "scenario": "market_down_10"
    }
    """
    engine = RiskAnalyticsEngine()
    return engine.calculate_stress_test(portfolio, scenario)


@app.post("/analytics/maximum-drawdown")
async def max_drawdown(price_history: list):
    """
    Calculate Maximum Drawdown (largest decline from peak to trough).
    
    Returns negative percentage for decline.
    """
    engine = RiskAnalyticsEngine()
    drawdown = engine.calculate_maximum_drawdown(price_history)
    return {
        "maximum_drawdown_pct": drawdown,
        "interpretation": f"Portfolio could lose up to {abs(drawdown):.1f}% from peak"
    }


@app.post("/analytics/value-at-risk")
async def value_at_risk(returns: list, confidence_level: float = 0.95):
    """
    Calculate Value at Risk (VaR) - maximum expected loss at confidence level.
    
    Confidence levels:
    - 0.95: 95% confidence (5% chance of worse loss)
    - 0.99: 99% confidence (1% chance of worse loss)
    """
    engine = RiskAnalyticsEngine()
    var = engine.calculate_value_at_risk(returns, confidence_level)
    return {
        "var_pct": var,
        "confidence_level": confidence_level * 100,
        "interpretation": f"There is a {(1-confidence_level)*100:.0f}% chance of losing more than {abs(var):.2f}%"
    }


@app.post("/analytics/portfolio-metrics")
async def portfolio_metrics(portfolio: dict):
    """
    Calculate comprehensive portfolio metrics.
    
    Returns:
    - Total portfolio value
    - Asset weights
    - Portfolio volatility
    - Concentration risk assessment
    - Largest position weight
    """
    engine = RiskAnalyticsEngine()
    return engine.calculate_portfolio_metrics(portfolio, {})

