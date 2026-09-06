from typing import TypedDict, Dict, Any, List


class AgentState(TypedDict):
    """Shared state for all agents in the LangGraph workflow."""
    user_goal: str
    investment_amount: float
    duration_years: int
    risk_profile: str
    research_data: Dict[str, Any]
    portfolio: Dict[str, float]
    recommendations: List[Dict[str, Any]]
    critique: str
    approved: bool
    history: List[Dict[str, Any]]
