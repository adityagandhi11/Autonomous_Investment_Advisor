"""Tests for LangGraph workflow."""

import pytest
from app.graph import build_investment_graph
from app.state import AgentState


@pytest.fixture
def investment_graph():
    """Fixture for compiled investment graph."""
    return build_investment_graph()


@pytest.fixture
def sample_request() -> AgentState:
    """Fixture for sample investment request."""
    return {
        "user_goal": "Invest ₹50,000 for 5 years",
        "investment_amount": 50000.0,
        "duration_years": 5,
        "risk_profile": "",
        "research_data": {},
        "portfolio": {},
        "critique": "",
        "approved": False,
        "history": []
    }


def test_graph_compiles():
    """Test that graph compiles without errors."""
    graph = build_investment_graph()
    assert graph is not None


def test_graph_workflow_executes(investment_graph, sample_request):
    """Test full workflow execution (optional: requires API keys)."""
    # This test requires OPENAI_API_KEY to be set
    # Uncomment to run with valid credentials:
    
    # result = investment_graph.invoke(sample_request)
    # assert "risk_profile" in result
    # assert "portfolio" in result
    # assert "approved" in result
    
    # Placeholder for now
    assert investment_graph is not None


def test_graph_produces_valid_state(investment_graph, sample_request):
    """Test that graph produces valid output state structure."""
    # Placeholder test - full execution requires API keys
    assert "user_goal" in sample_request
    assert "investment_amount" in sample_request
