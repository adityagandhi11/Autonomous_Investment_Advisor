"""Financial calculators for portfolio analysis."""

from typing import List, Dict


def calculate_risk(positions: List[Dict[str, float]]) -> float:
    """
    Simple risk calculation based on position volatility.
    In production, use real volatility data from market prices.
    """
    if not positions:
        return 0.0

    # Placeholder: average volatility
    total_risk = sum(p.get("volatility", 0.1) for p in positions)
    return round(total_risk / len(positions), 4)


def calculate_expected_return(positions: List[Dict[str, float]]) -> float:
    """
    Calculate expected return from weighted positions.
    Weights expected returns from each position.
    """
    if not positions:
        return 0.0

    total_value = sum(p.get("value", 0) for p in positions)
    if total_value == 0:
        return 0.0

    weighted_return = 0.0
    for position in positions:
        weight = position.get("value", 0) / total_value
        return_rate = position.get("expected_return", 0.1)
        weighted_return += weight * return_rate

    return round(weighted_return * 100, 2)  # Return as percentage


def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.05) -> float:
    """
    Calculate Sharpe ratio for portfolio performance evaluation.
    Sharpe = (Portfolio Return - Risk Free Rate) / Standard Deviation
    """
    if not returns or len(returns) < 2:
        return 0.0

    import statistics
    mean_return = statistics.mean(returns)
    std_dev = statistics.stdev(returns)

    if std_dev == 0:
        return 0.0

    sharpe = (mean_return - risk_free_rate) / std_dev
    return round(sharpe, 4)
