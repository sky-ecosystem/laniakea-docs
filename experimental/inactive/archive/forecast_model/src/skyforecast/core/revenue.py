"""Revenue calculations."""

from dataclasses import dataclass
from decimal import Decimal


# Monthly factor: 1/12 of annual rate
MONTHLY_FACTOR = Decimal("1") / Decimal("12")


@dataclass
class RevenueInputs:
    """Inputs for revenue calculation."""
    usds_supply: Decimal
    susds_supply: Decimal
    gross_revenue_rate: Decimal
    savings_rate: Decimal
    sellable_tokens: Decimal
    sell_token_rate: Decimal
    subsidized_borrow: Decimal  # monthly cost (negative)
    srusds_cost: Decimal        # monthly cost (negative)
    # Distribution reward tier ratios
    tier2_ratio: Decimal  # 10 bps
    tier3_ratio: Decimal  # 20 bps
    tier4_ratio: Decimal  # 50 bps


@dataclass
class RevenueCalculations:
    """Derived revenue values."""
    token_sales_income: Decimal
    gross_revenue: Decimal
    savings_expense: Decimal
    distribution_rewards: Decimal
    net_revenue: Decimal


# Distribution reward rates (annual)
DR_TIER2_RATE = Decimal("0.0010")  # 10 bps
DR_TIER3_RATE = Decimal("0.0020")  # 20 bps
DR_TIER4_RATE = Decimal("0.0050")  # 50 bps


def calculate_revenue(inputs: RevenueInputs) -> RevenueCalculations:
    """Monthly revenue calculation."""
    token_sales_income = inputs.sellable_tokens * inputs.sell_token_rate * MONTHLY_FACTOR

    gross_revenue = (
        inputs.usds_supply * inputs.gross_revenue_rate * MONTHLY_FACTOR
        + token_sales_income
    )

    savings_expense = inputs.susds_supply * inputs.savings_rate * MONTHLY_FACTOR

    # Distribution rewards by tier (cost to protocol)
    tier2_supply = inputs.susds_supply * inputs.tier2_ratio
    tier3_supply = inputs.susds_supply * inputs.tier3_ratio
    tier4_supply = inputs.susds_supply * inputs.tier4_ratio

    distribution_rewards = (
        tier2_supply * DR_TIER2_RATE +
        tier3_supply * DR_TIER3_RATE +
        tier4_supply * DR_TIER4_RATE
    ) * MONTHLY_FACTOR

    net_revenue = (
        gross_revenue
        - savings_expense
        - distribution_rewards
        + inputs.subsidized_borrow
        + inputs.srusds_cost
    )

    return RevenueCalculations(
        token_sales_income=token_sales_income,
        gross_revenue=gross_revenue,
        savings_expense=savings_expense,
        distribution_rewards=distribution_rewards,
        net_revenue=net_revenue,
    )
