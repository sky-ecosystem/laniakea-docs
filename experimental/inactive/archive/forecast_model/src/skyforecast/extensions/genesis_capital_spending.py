"""Genesis Capital Spending extension.

Tracks outflows from backstop capital that don't count as expenses.
Linear trajectory from start_month to end_month reaching total_outflow.
"""

from decimal import Decimal
from typing import Any, Dict

from ..loaders.models import parse_decimal
from .base import Extension, ExtensionResults


class GenesisCapitalSpendingExtension(Extension):
    """Genesis capital spending - backstop outflows (not expenses)."""

    name = "genesis_capital_spending"

    def calculate(
        self,
        month: int,
        inputs: Dict[str, Any],
        rates: Any,
    ) -> ExtensionResults:
        if not self.enabled:
            return ExtensionResults()

        start_month = int(self.config.get("start_month", 2))
        end_month = int(self.config.get("end_month", 12))
        total_outflow = parse_decimal(self.config.get("total_outflow", 0))

        # No outflow before start_month
        if month < start_month:
            return ExtensionResults(
                breakdown={"monthly_outflow": Decimal("0"), "cumulative_outflow": Decimal("0")}
            )

        # Calculate monthly outflow for linear trajectory
        # From start_month to end_month inclusive
        num_months = end_month - start_month + 1
        monthly_outflow = total_outflow / Decimal(str(num_months))

        # Cap at end_month (no more outflows after)
        if month > end_month:
            return ExtensionResults(
                breakdown={"monthly_outflow": Decimal("0"), "cumulative_outflow": total_outflow}
            )

        # Calculate cumulative outflow up to and including this month
        months_elapsed = month - start_month + 1
        cumulative_outflow = monthly_outflow * Decimal(str(months_elapsed))

        return ExtensionResults(
            backstop_outflow=monthly_outflow,
            breakdown={
                "monthly_outflow": monthly_outflow,
                "cumulative_outflow": cumulative_outflow,
            },
        )
