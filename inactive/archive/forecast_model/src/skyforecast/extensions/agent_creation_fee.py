"""Agent Creation Fee extension.

When non-star/non-prime agents are created, Sky receives 5% of tokens.
These are sold at 1% of market cap per year (20% of holdings per year).

Agent types:
- Small: 50M market cap
- Large: 150M market cap
"""

from decimal import Decimal
from typing import Any, Dict

from ..loaders.models import parse_decimal
from .base import Extension, ExtensionResults


MONTHLY_FACTOR = Decimal("1") / Decimal("12")
DEFAULT_OWNERSHIP = Decimal("0.05")  # 5% of tokens
DEFAULT_SELL_RATE = Decimal("0.01")  # 1% of market cap per year

AGENT_TYPES = {
    "small": Decimal("50000000"),   # 50M
    "large": Decimal("150000000"),  # 150M
}


class AgentCreationFeeExtension(Extension):
    """Agent Creation Fee - token sales from agent creation rewards."""

    name = "agent_creation_fee"

    def calculate(
        self,
        month: int,
        inputs: Dict[str, Any],
        rates: Any,
    ) -> ExtensionResults:
        if not self.enabled:
            return ExtensionResults()

        sell_rate = parse_decimal(
            self.config.get("sell_rate_annual", DEFAULT_SELL_RATE)
        )
        agents_config = self.config.get("agents", {})

        total_token_sales = Decimal("0")
        agent_breakdown = {}

        for agent_name, agent_config in agents_config.items():
            launch_month = int(agent_config.get("launch_month", 1))

            # Check if agent is active (launched)
            if month < launch_month:
                continue

            # Get market cap from type or explicit value
            agent_type = agent_config.get("type")
            if agent_type and agent_type in AGENT_TYPES:
                market_cap = AGENT_TYPES[agent_type]
            else:
                market_cap = parse_decimal(agent_config.get("market_cap", 0))

            # Sky's ownership (default 5%)
            ownership = parse_decimal(
                agent_config.get("ownership", DEFAULT_OWNERSHIP)
            )

            # Value of Sky's holdings
            holdings_value = market_cap * ownership

            # Annual token sales (sell_rate of market cap = sell_rate/ownership of holdings)
            # e.g., 1% of 50M = 500K/year, which is 20% of 2.5M holdings
            annual_sales = market_cap * sell_rate
            monthly_sales = annual_sales * MONTHLY_FACTOR

            total_token_sales += monthly_sales
            agent_breakdown[f"{agent_name}_token_sales"] = monthly_sales

        breakdown = {
            "total_agent_fee_sales": total_token_sales,
        }
        breakdown.update(agent_breakdown)

        # Token sales add to gross revenue
        return ExtensionResults(
            gross_revenue_adjustment=total_token_sales,
            breakdown=breakdown,
        )
