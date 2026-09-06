"""Rebalancer Agent - performs portfolio rebalancing operations."""


def rebalancer_agent(current_portfolio: dict, target_weights: dict) -> dict:
    """
    Calculate rebalancing actions to align portfolio with target allocation.
    Can be scheduled monthly via APScheduler or cron.
    """
    total = sum(current_portfolio.values())

    target_values = {
        asset: total * weight
        for asset, weight in target_weights.items()
    }

    actions = {}

    for asset, target in target_values.items():
        current = current_portfolio.get(asset, 0)
        diff = round(target - current, 2)

        if diff != 0:
            if diff > 0:
                actions[asset] = {"action": "BUY", "amount": diff}
            else:
                actions[asset] = {"action": "SELL", "amount": abs(diff)}

    return actions


def evaluate_rebalance_trigger(current_portfolio: dict, target_weights: dict, threshold: float = 0.05) -> bool:
    """
    Check if portfolio drift exceeds threshold and rebalancing is needed.
    Threshold: percentage point drift allowed before rebalancing (default 5%).
    """
    total = sum(current_portfolio.values())

    for asset, target_weight in target_weights.items():
        current = current_portfolio.get(asset, 0)
        current_weight = current / total if total > 0 else 0
        drift = abs(current_weight - target_weight)

        if drift > threshold:
            return True

    return False
