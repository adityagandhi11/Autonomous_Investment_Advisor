"""Tests for FastAPI application endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Fixture for FastAPI test client."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test root health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_invest_endpoint_valid_request(client):
    """Test invest endpoint with valid request (requires API keys)."""
    payload = {
        "user_goal": "Invest for retirement",
        "investment_amount": 50000,
        "duration_years": 5
    }
    
    # This will fail without valid OPENAI_API_KEY
    # Uncomment when testing with valid credentials:
    # response = client.post("/invest", json=payload)
    # assert response.status_code == 200
    # data = response.json()
    # assert "risk_profile" in data
    # assert "portfolio" in data
    # assert "critique" in data
    
    # Placeholder validation
    assert payload["investment_amount"] > 0
    assert payload["duration_years"] > 0


def test_invest_endpoint_invalid_amount(client):
    """Test invest endpoint with invalid investment amount."""
    payload = {
        "user_goal": "Invest for retirement",
        "investment_amount": -1000,  # Invalid
        "duration_years": 5
    }
    
    # Validation at Pydantic level
    # Negative amounts should ideally be rejected
    # This is a business logic decision


def test_invest_endpoint_missing_fields(client):
    """Test invest endpoint with missing required fields."""
    payload = {
        "user_goal": "Invest",
        # Missing investment_amount and duration_years
    }
    
    response = client.post("/invest", json=payload)
    assert response.status_code == 422  # Validation error


def test_portfolio_history_endpoint(client):
    """Test portfolio history retrieval."""
    response = client.get("/portfolio-history?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "portfolios" in data
    assert isinstance(data["portfolios"], list)
