"""Critic Agent - evaluates and validates portfolios."""


def critic_agent(state):
    """
    Critique the proposed portfolio for diversification and risk compliance.
    Implements reflection loop for iterative refinement.
    """
    portfolio = state["portfolio"]
    total = sum(portfolio.values())

    issues = []

    for asset, value in portfolio.items():
        weight = value / total

        if weight > 0.60:
            issues.append(f"{asset} exceeds 60% allocation")

    if len(portfolio) < 3:
        issues.append("Portfolio lacks diversification")

    if issues:
        return {
            "approved": False,
            "critique": "; ".join(issues),
            "recommendations": state.get("recommendations", []),
            "history": state["history"] + [{
                "agent": "critic",
                "output": issues
            }]
        }

    return {
        "approved": True,
        "critique": "Portfolio approved",
        "recommendations": state.get("recommendations", []),
        "history": state["history"] + [{
            "agent": "critic",
            "output": "approved"
        }]
    }
