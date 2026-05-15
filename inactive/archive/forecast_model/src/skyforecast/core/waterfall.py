"""TMF waterfall calculations."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class WaterfallInputs:
    """Inputs for TMF waterfall calculation."""
    net_revenue: Decimal
    security_rate: Decimal
    backstop_rate: Decimal
    backstop_withdrawal: Decimal = Decimal("0")  # one-time withdrawal (positive number)


@dataclass
class WaterfallResults:
    """TMF waterfall results."""
    security_budget: Decimal
    after_security: Decimal
    backstop_contribution: Decimal
    backstop_withdrawal: Decimal
    net_backstop_change: Decimal
    staking_rewards: Decimal
    net_profit: Decimal


def calculate_waterfall(inputs: WaterfallInputs) -> WaterfallResults:
    """Monthly TMF waterfall."""
    security_budget = inputs.net_revenue * inputs.security_rate
    after_security = inputs.net_revenue - security_budget

    backstop_contribution = after_security * inputs.backstop_rate
    net_backstop_change = backstop_contribution - inputs.backstop_withdrawal

    staking_rewards = after_security * (Decimal("1") - inputs.backstop_rate)
    net_profit = backstop_contribution + staking_rewards

    return WaterfallResults(
        security_budget=security_budget,
        after_security=after_security,
        backstop_contribution=backstop_contribution,
        backstop_withdrawal=inputs.backstop_withdrawal,
        net_backstop_change=net_backstop_change,
        staking_rewards=staking_rewards,
        net_profit=net_profit,
    )
