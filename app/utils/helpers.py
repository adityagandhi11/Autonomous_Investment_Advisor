"""Utility helper functions."""

from pprint import pformat
from typing import Any


def pretty_print(obj: Any) -> str:
    """Pretty print any object for debugging."""
    return pformat(obj)


def calculate_portfolio_variance(portfolio: dict) -> dict:
    """Calculate weight variance of portfolio assets."""
    if not portfolio:
        return {}

    total = sum(portfolio.values())
    weights = {asset: (value / total * 100) for asset, value in portfolio.items()}
    return weights


def format_currency(amount: float, currency: str = "₹") -> str:
    """Format amount as currency string."""
    return f"{currency}{amount:,.2f}"
