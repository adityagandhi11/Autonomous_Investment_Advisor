"""Planner Agent - breaks investment request into actionable steps."""

from langchain_groq import ChatGroq
from app.config import settings


llm = ChatGroq(model=settings.groq_model, temperature=0)


def planner_agent(state):
    """
    Analyze the investment goal and break it down into steps.
    """
    prompt = f"""
    Break this investment request into actionable steps:

    Goal: {state['user_goal']}
    Amount: ₹{state['investment_amount']}
    Duration: {state['duration_years']} years
    
    Provide a structured plan.
    """

    response = llm.invoke(prompt)

    return {
        "recommendations": state.get("recommendations", []),
        "history": state.get("history", []) + [{
            "agent": "planner",
            "output": response.content
        }]
    }
