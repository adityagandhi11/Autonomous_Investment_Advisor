"""Risk Profiler Agent - determines investment risk profile."""

from langchain_groq import ChatGroq
from app.config import settings


llm = ChatGroq(model=settings.groq_model, temperature=0)


def risk_profiler_agent(state):
    """
    Determine the risk profile (low, moderate, high) based on user inputs.
    """
    prompt = f"""
    Determine the risk profile (low, moderate, high).

    Goal: {state['user_goal']}
    Investment amount: ₹{state['investment_amount']}
    Duration: {state['duration_years']} years

    Return only one word: low, moderate, or high.
    """

    response = llm.invoke(prompt)

    risk = response.content.strip().lower()

    return {
        "risk_profile": risk,
        "recommendations": state.get("recommendations", []),
        "history": state["history"] + [{
            "agent": "risk_profiler",
            "output": risk
        }]
    }
