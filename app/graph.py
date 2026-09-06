"""LangGraph workflow for autonomous investment advisor."""

from langgraph.graph import StateGraph, END

from app.state import AgentState
from app.agents.planner import planner_agent
from app.agents.risk_profiler import risk_profiler_agent
from app.agents.market_research import market_research_agent
from app.agents.portfolio_builder import portfolio_builder_agent
from app.agents.critic import critic_agent


def build_investment_graph():
    """
    Construct the LangGraph workflow.
    Flow: Planner → Risk Profiler → Market Research → Portfolio Builder → Critic
    Critic implements conditional routing for approval/revision loop.
    """
    graph = StateGraph(AgentState)

    # Add all agent nodes
    graph.add_node("planner", planner_agent)
    graph.add_node("risk_profiler", risk_profiler_agent)
    graph.add_node("market_research", market_research_agent)
    graph.add_node("portfolio_builder", portfolio_builder_agent)
    graph.add_node("critic", critic_agent)

    # Set entry point
    graph.set_entry_point("planner")

    # Define linear edges
    graph.add_edge("planner", "risk_profiler")
    graph.add_edge("risk_profiler", "market_research")
    graph.add_edge("market_research", "portfolio_builder")
    graph.add_edge("portfolio_builder", "critic")

    # Conditional routing: critic can approve or send back to portfolio_builder
    def review_router(state):
        """Route based on portfolio approval."""
        return "approve" if state["approved"] else "revise"

    graph.add_conditional_edges(
        "critic",
        review_router,
        {
            "approve": END,
            "revise": "portfolio_builder"
        }
    )

    return graph.compile()


# Compile the graph at module load
investment_graph = build_investment_graph()
