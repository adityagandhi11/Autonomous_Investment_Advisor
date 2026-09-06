"""Tests for investment advisor agents."""

import pytest
from app.state import AgentState
from app.agents.planner import planner_agent
from app.agents.risk_profiler import risk_profiler_agent
from app.agents.portfolio_builder import portfolio_builder_agent
from app.agents.critic import critic_agent


@pytest.fixture
def sample_state() -> AgentState:
    """Fixture for base agent state."""
    return {
        "user_goal": "Invest for long-term wealth",
        "investment_amount": 50000.0,
        "duration_years": 5,
        "risk_profile": "",
        "research_data": {},
        "portfolio": {},
        "critique": "",
        "approved": False,
        "history": []
    }


def test_planner_agent(sample_state):
    """Test planner agent generates plan."""
    result = planner_agent(sample_state)
    assert "history" in result
    assert len(result["history"]) > 0
    assert result["history"][0]["agent"] == "planner"


def test_risk_profiler_agent(sample_state):
    """Test risk profiler determines risk category."""
    result = risk_profiler_agent(sample_state)
    assert "risk_profile" in result
    assert result["risk_profile"] in ["low", "moderate", "high"]
    assert "history" in result


def test_portfolio_builder_agent(sample_state):
    """Test portfolio builder creates allocation."""
    sample_state["risk_profile"] = "moderate"
    result = portfolio_builder_agent(sample_state)
    
    assert "portfolio" in result
    portfolio = result["portfolio"]
    
    # Check portfolio is not empty
    assert len(portfolio) > 0
    
    # Check all values are positive
    assert all(v > 0 for v in portfolio.values())
    
    # Check total matches investment amount
    total = sum(portfolio.values())
    assert abs(total - sample_state["investment_amount"]) < 0.01


def test_portfolio_builder_risk_levels(sample_state):
    """Test portfolio builder creates different allocations for different risk levels."""
    for risk_level in ["low", "moderate", "high"]:
        sample_state["risk_profile"] = risk_level
        result = portfolio_builder_agent(sample_state)
        portfolio = result["portfolio"]
        assert sum(portfolio.values()) > 0


def test_critic_agent_approves_good_portfolio(sample_state):
    """Test critic approves well-diversified portfolio."""
    sample_state["portfolio"] = {
        "NIFTYBEES.NS": 25000.0,
        "GOLDBEES.NS": 15000.0,
        "HDFCBANK.NS": 10000.0
    }
    
    result = critic_agent(sample_state)
    assert result["approved"] is True
    assert result["critique"] == "Portfolio approved"


def test_critic_agent_rejects_concentrated_portfolio(sample_state):
    """Test critic rejects overly concentrated portfolio."""
    sample_state["portfolio"] = {
        "NIFTYBEES.NS": 45000.0,
        "GOLDBEES.NS": 5000.0
    }
    
    result = critic_agent(sample_state)
    assert result["approved"] is False
    assert "exceeds 60%" in result["critique"]


def test_critic_agent_rejects_poor_diversification(sample_state):
    """Test critic rejects poorly diversified portfolio."""
    sample_state["portfolio"] = {
        "NIFTYBEES.NS": 50000.0
    }
    
    result = critic_agent(sample_state)
    assert result["approved"] is False
    assert "diversification" in result["critique"].lower()
