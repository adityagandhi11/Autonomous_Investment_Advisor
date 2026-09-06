"""Portfolio service for managing portfolio operations."""

from typing import Dict, List, Any


class PortfolioService:
    """Service to manage portfolio persistence and retrieval."""

    def __init__(self, db):
        self.db = db

    async def save(self, portfolio: dict) -> bool:
        """Save portfolio to database."""
        return True

    async def get_by_id(self, portfolio_id: str) -> Dict[str, Any]:
        """Retrieve portfolio by ID."""
        return {}

    def calculate_allocation(self, portfolio: Dict[str, float]) -> Dict[str, float]:
        """Calculate percentage allocation for each asset."""
        total = sum(portfolio.values())
        if total == 0:
            return {}
        return {asset: round((value / total) * 100, 2) for asset, value in portfolio.items()}

    def validate_diversification(self, portfolio: Dict[str, float], min_assets: int = 3, max_single_weight: float = 0.6) -> tuple:
        """
        Validate portfolio diversification.
        Returns: (is_valid, issues_list)
        """
        issues = []

        if len(portfolio) < min_assets:
            issues.append(f"Portfolio has {len(portfolio)} assets, minimum {min_assets} required")

        total = sum(portfolio.values())
        for asset, value in portfolio.items():
            weight = value / total if total > 0 else 0
            if weight > max_single_weight:
                issues.append(f"{asset} allocation {weight:.1%} exceeds maximum {max_single_weight:.1%}")

        return len(issues) == 0, issues
