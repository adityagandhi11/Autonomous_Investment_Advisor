"""Advanced Risk Analytics Service - comprehensive portfolio risk analysis."""

import yfinance as yf
import numpy as np
import statistics
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta


class RiskAnalyticsEngine:
    """Advanced risk analytics for portfolios and assets."""
    
    # Risk-free rate (approximate annual rate for Indian government securities)
    RISK_FREE_RATE = 0.06  # 6% annual
    
    # Market return (approximate annual return of Nifty 50)
    MARKET_RETURN = 0.12  # 12% annual
    
    @staticmethod
    def calculate_volatility(returns: List[float], periods_per_year: int = 252) -> float:
        """
        Calculate annualized volatility (standard deviation).
        
        Args:
            returns: List of daily returns as decimals
            periods_per_year: Trading days per year (default: 252)
        
        Returns:
            Annualized volatility as percentage
        """
        if len(returns) < 2:
            return 0.0
        
        daily_volatility = statistics.stdev(returns)
        annualized = daily_volatility * (periods_per_year ** 0.5)
        return round(annualized * 100, 2)
    
    @staticmethod
    def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = None) -> float:
        """
        Calculate Sharpe Ratio (return per unit of risk).
        
        Higher is better. Negative means underperforming risk-free rate.
        """
        if risk_free_rate is None:
            risk_free_rate = RiskAnalyticsEngine.RISK_FREE_RATE
        
        if len(returns) < 2:
            return 0.0
        
        avg_return = statistics.mean(returns)
        volatility = statistics.stdev(returns)
        
        if volatility == 0:
            return 0.0
        
        # Annualize
        periods_per_year = 252
        sharpe = (avg_return * periods_per_year - risk_free_rate) / (volatility * (periods_per_year ** 0.5))
        return round(sharpe, 2)
    
    @staticmethod
    def calculate_sortino_ratio(returns: List[float], target_return: float = 0.0) -> float:
        """
        Calculate Sortino Ratio (focuses on downside risk).
        Better than Sharpe for portfolios with asymmetric returns.
        """
        if len(returns) < 2:
            return 0.0
        
        avg_return = statistics.mean(returns)
        
        # Downside deviation (only negative returns)
        downside_returns = [r for r in returns if r < target_return]
        
        if not downside_returns:
            return 0.0
        
        downside_deviation = statistics.stdev(downside_returns)
        
        if downside_deviation == 0:
            return 0.0
        
        periods_per_year = 252
        sortino = (avg_return * periods_per_year - RiskAnalyticsEngine.RISK_FREE_RATE) / (downside_deviation * (periods_per_year ** 0.5))
        return round(sortino, 2)
    
    @staticmethod
    def calculate_beta(asset_returns: List[float], market_returns: List[float]) -> float:
        """
        Calculate Beta (volatility vs market).
        
        Beta > 1: More volatile than market
        Beta = 1: Same as market
        Beta < 1: Less volatile than market
        """
        if len(asset_returns) < 2 or len(market_returns) < 2:
            return 1.0
        
        # Ensure same length
        min_len = min(len(asset_returns), len(market_returns))
        asset_returns = asset_returns[-min_len:]
        market_returns = market_returns[-min_len:]
        
        asset_array = np.array(asset_returns)
        market_array = np.array(market_returns)
        
        # Covariance
        covariance = np.cov(asset_array, market_array)[0, 1]
        
        # Market variance
        market_variance = np.var(market_array)
        
        if market_variance == 0:
            return 1.0
        
        beta = covariance / market_variance
        return round(beta, 2)
    
    @staticmethod
    def calculate_alpha(asset_return_pct: float, beta: float, market_return_pct: float = None, risk_free_rate: float = None) -> float:
        """
        Calculate Alpha (excess return above expected).
        
        CAPM: Expected Return = Risk-Free Rate + Beta * (Market Return - Risk-Free Rate)
        Alpha = Actual Return - Expected Return
        """
        if market_return_pct is None:
            market_return_pct = RiskAnalyticsEngine.MARKET_RETURN * 100
        if risk_free_rate is None:
            risk_free_rate = RiskAnalyticsEngine.RISK_FREE_RATE * 100
        
        expected_return = risk_free_rate + beta * (market_return_pct - risk_free_rate)
        alpha = asset_return_pct - expected_return
        return round(alpha, 2)
    
    @staticmethod
    def calculate_maximum_drawdown(price_history: List[float]) -> float:
        """
        Calculate Maximum Drawdown (largest decline from peak to trough).
        
        Returns:
            Drawdown as percentage (e.g., -25.5 for 25.5% decline)
        """
        if len(price_history) < 2:
            return 0.0
        
        peak = price_history[0]
        max_drawdown = 0.0
        
        for price in price_history:
            if price > peak:
                peak = price
            drawdown = (price - peak) / peak
            if drawdown < max_drawdown:
                max_drawdown = drawdown
        
        return round(max_drawdown * 100, 2)
    
    @staticmethod
    def calculate_value_at_risk(returns: List[float], confidence_level: float = 0.95) -> float:
        """
        Calculate Value at Risk (VaR) - maximum expected loss at confidence level.
        
        Args:
            returns: List of returns as decimals
            confidence_level: Confidence level (0.95 = 95%, 0.99 = 99%)
        
        Returns:
            VaR as percentage (negative value represents potential loss)
        """
        if len(returns) < 2:
            return 0.0
        
        sorted_returns = sorted(returns)
        index = int(len(sorted_returns) * (1 - confidence_level))
        var = sorted_returns[index] if index < len(sorted_returns) else sorted_returns[0]
        
        return round(var * 100, 2)
    
    @staticmethod
    def calculate_portfolio_metrics(portfolio: Dict[str, float], prices: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculate comprehensive portfolio metrics.
        
        Args:
            portfolio: {ticker: amount_invested}
            prices: {ticker: current_price}
        
        Returns:
            Dictionary with portfolio metrics
        """
        total_value = sum(portfolio.values())
        
        if total_value == 0:
            return {"error": "Portfolio value is zero"}
        
        # Calculate weights
        weights = {ticker: amount / total_value for ticker, amount in portfolio.items()}
        
        # Get market data for each asset
        all_returns = []
        volatilities = []
        
        for ticker in portfolio.keys():
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1mo")
                
                if not hist.empty:
                    daily_returns = hist["Close"].pct_change().dropna().tolist()
                    all_returns.append(daily_returns)
                    
                    if len(daily_returns) > 1:
                        volatility = statistics.stdev(daily_returns) * (252 ** 0.5)
                        volatilities.append(volatility * weights.get(ticker, 0))
            except:
                pass
        
        # Portfolio volatility (simplified - doesn't account for correlation)
        portfolio_volatility = sum(volatilities) if volatilities else 0.0
        
        return {
            "total_value": round(total_value, 2),
            "weights": {k: round(v * 100, 2) for k, v in weights.items()},
            "portfolio_volatility_pct": round(portfolio_volatility * 100, 2),
            "number_of_assets": len(portfolio),
            "largest_position": round(max(weights.values()) * 100, 2) if weights else 0,
            "concentration_risk": "High" if max(weights.values()) > 0.4 else "Moderate" if max(weights.values()) > 0.25 else "Low"
        }
    
    @staticmethod
    def calculate_correlation_matrix(tickers: List[str], period: str = "1mo") -> Dict[str, Dict[str, float]]:
        """
        Calculate correlation matrix between assets.
        
        Returns:
            Dictionary with correlation coefficients
        """
        data_dict = {}
        
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period=period)
                if not hist.empty:
                    data_dict[ticker] = hist["Close"].pct_change().dropna().tolist()
            except:
                pass
        
        if len(data_dict) < 2:
            return {"error": "Not enough data"}
        
        correlation_matrix = {}
        tickers_list = list(data_dict.keys())
        
        for i, ticker1 in enumerate(tickers_list):
            correlation_matrix[ticker1] = {}
            for j, ticker2 in enumerate(tickers_list):
                if i == j:
                    correlation_matrix[ticker1][ticker2] = 1.0
                elif ticker2 in correlation_matrix and ticker1 in correlation_matrix[ticker2]:
                    correlation_matrix[ticker1][ticker2] = correlation_matrix[ticker2][ticker1]
                else:
                    returns1 = np.array(data_dict[ticker1])
                    returns2 = np.array(data_dict[ticker2])
                    
                    if len(returns1) > 1 and len(returns2) > 1:
                        correlation = np.corrcoef(returns1, returns2)[0, 1]
                        correlation_matrix[ticker1][ticker2] = round(float(correlation), 2)
                    else:
                        correlation_matrix[ticker1][ticker2] = 0.0
        
        return correlation_matrix
    
    @staticmethod
    def calculate_stress_test(portfolio: Dict[str, float], scenario: str = "market_down_10") -> Dict[str, Any]:
        """
        Simulate portfolio performance under stress scenarios.
        
        Scenarios:
        - market_down_10: 10% market decline
        - market_down_20: 20% market decline
        - market_crash: 35% market crash
        - interest_rate_up: 2% interest rate increase
        """
        total_value = sum(portfolio.values())
        
        scenarios = {
            "market_down_10": {"beta_multiplier": 1.0, "market_change": -0.10},
            "market_down_20": {"beta_multiplier": 1.0, "market_change": -0.20},
            "market_crash": {"beta_multiplier": 1.2, "market_change": -0.35},
            "interest_rate_up": {"bond_impact": -0.02, "stock_impact": -0.05},
        }
        
        if scenario not in scenarios:
            scenario = "market_down_10"
        
        scenario_params = scenarios[scenario]
        estimated_loss = 0.0
        
        # Simplified calculation
        for ticker, amount in portfolio.items():
            if "beta_multiplier" in scenario_params:
                # Assume average beta of 1.0
                estimated_change = scenario_params["market_change"] * scenario_params["beta_multiplier"]
            else:
                estimated_change = scenario_params.get("stock_impact", 0)
            
            estimated_loss += amount * estimated_change
        
        new_value = total_value + estimated_loss
        loss_pct = (estimated_loss / total_value * 100) if total_value > 0 else 0
        
        return {
            "scenario": scenario,
            "current_value": round(total_value, 2),
            "estimated_value": round(new_value, 2),
            "estimated_loss": round(estimated_loss, 2),
            "loss_percentage": round(loss_pct, 2),
            "description": f"Portfolio could drop to ₹{new_value:,.0f} ({loss_pct:.1f}% loss)"
        }


# Public API functions
def get_asset_risk_metrics(ticker: str, period: str = "3mo") -> Dict[str, Any]:
    """Get comprehensive risk metrics for an asset."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        
        if hist.empty:
            return {"error": "No data available"}
        
        daily_returns = hist["Close"].pct_change().dropna().tolist()
        prices = hist["Close"].tolist()
        
        return {
            "ticker": ticker,
            "volatility_pct": RiskAnalyticsEngine.calculate_volatility(daily_returns),
            "sharpe_ratio": RiskAnalyticsEngine.calculate_sharpe_ratio(daily_returns),
            "sortino_ratio": RiskAnalyticsEngine.calculate_sortino_ratio(daily_returns),
            "maximum_drawdown_pct": RiskAnalyticsEngine.calculate_maximum_drawdown(prices),
            "var_95_pct": RiskAnalyticsEngine.calculate_value_at_risk(daily_returns, 0.95),
            "var_99_pct": RiskAnalyticsEngine.calculate_value_at_risk(daily_returns, 0.99),
            "period": period,
            "observations": len(daily_returns)
        }
    except Exception as e:
        return {"error": str(e), "ticker": ticker}


def get_portfolio_risk_dashboard(portfolio: Dict[str, float]) -> Dict[str, Any]:
    """Get complete risk analytics dashboard for portfolio."""
    engine = RiskAnalyticsEngine()
    
    metrics = engine.calculate_portfolio_metrics(portfolio, {})
    
    return {
        "portfolio_summary": metrics,
        "risk_assessment": {
            "concentration_risk": metrics.get("concentration_risk", "Unknown"),
            "largest_position_weight": metrics.get("largest_position", 0),
            "portfolio_volatility": metrics.get("portfolio_volatility_pct", 0)
        },
        "stress_test": engine.calculate_stress_test(portfolio, "market_down_10"),
        "generated_at": datetime.now().isoformat()
    }
