"""Risk Profiler Agent - determines investment risk profile."""

from langchain_groq import ChatGroq
from app.config import settings


llm = ChatGroq(model=settings.groq_model, temperature=0)

VALID_RISK_PROFILES = {"low", "moderate", "high"}


def risk_profiler_agent(state):
    """
    Determine the risk profile.

    If an explicit valid risk profile is already present in the state,
    preserve it. Otherwise, determine it from the user's investment inputs.
    """

    existing_risk = (
        state.get("risk_profile") or ""
    ).strip().lower()

    # Explicit risk requested by the user through chat.
    if existing_risk in VALID_RISK_PROFILES:
        risk = existing_risk

        return {
            "risk_profile": risk,
            "recommendations": state.get("recommendations", []),
            "history": state["history"] + [{
                "agent": "risk_profiler",
                "output": risk,
                "source": "explicit_user_request"
            }]
        }

    # Existing /invest behavior.
    prompt = f"""
    Determine the risk profile (low, moderate, high).

    Goal: {state['user_goal']}
    Investment amount: ₹{state['investment_amount']}
    Duration: {state['duration_years']} years

    Return only one word: low, moderate, or high.
    """

    response = llm.invoke(prompt)

    risk = response.content.strip().lower()

    # Safety normalization.
    if risk not in VALID_RISK_PROFILES:
        risk = "moderate"

    return {
        "risk_profile": risk,
        "recommendations": state.get("recommendations", []),
        "history": state["history"] + [{
            "agent": "risk_profiler",
            "output": risk,
            "source": "calculated"
        }]
    }