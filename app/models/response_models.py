from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class InvestmentStep(BaseModel):
    step: int
    title: str
    description: Optional[str] = None
    platforms: Optional[List[Dict[str, str]]] = None
    timeline: Optional[str] = None
    charges: Optional[str] = None
    instructions: Optional[List[str]] = None
    resources: Optional[List[Dict[str, str]]] = None
    average_cost: Optional[str] = None


class InvestmentDetails(BaseModel):
    name: str
    category: str
    description: str
    risk_level: Optional[str] = None
    investment_steps: List[InvestmentStep]
    best_for: Optional[str] = None
    yearly_return: Optional[str] = None
    expense_ratio: Optional[str] = None
    dividend_yield: Optional[str] = None
    liquidity: Optional[str] = None
    taxes: Optional[str] = None
    advantages: Optional[str] = None
    market_cap: Optional[str] = None
    pe_ratio: Optional[str] = None


class Recommendation(BaseModel):
    symbol: str
    weight: float
    amount: float
    details: Optional[InvestmentDetails] = None


class PortfolioResponse(BaseModel):
    recommendations: List[Recommendation]
    expected_return: float


class InvestmentResponse(BaseModel):
    """Final response from investment advisor."""
    risk_profile: str
    portfolio: Dict[str, float]
    recommendations: Optional[List[Recommendation]] = None
    critique: str
    workflow_history: List[Dict[str, Any]]
