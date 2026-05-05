"""Subsidized Borrow extension.

Spark and Grove get $1B each at subsidized rate for 2 years.
Rate starts at SOFR and moves 1/24th toward gross_revenue_rate each month.
"""

from decimal import Decimal
from typing import Any, Dict

from ..loaders.models import parse_decimal
from .base import Extension, ExtensionResults


MONTHLY_FACTOR = Decimal("1") / Decimal("12")


class SubsidizedBorrowExtension(Extension):
    """Subsidized borrow - decaying subsidy for Primes."""

    name = "subsidized_borrow"

    def calculate(
        self,
        month: int,
        inputs: Dict[str, Any],
        rates: Any,
    ) -> ExtensionResults:
        if not self.enabled:
            return ExtensionResults()

        total_amount = parse_decimal(self.config.get("total_amount", 2_000_000_000))
        start_month = int(self.config.get("start_month", 1))
        duration_months = int(self.config.get("duration_months", 24))

        # Check if subsidy is active
        months_elapsed = month - start_month
        if months_elapsed < 0 or months_elapsed >= duration_months:
            return ExtensionResults()

        # Calculate decay factor (0 at start, 1 at end)
        decay_factor = Decimal(months_elapsed) / Decimal(duration_months)

        # Subsidized rate moves from SOFR toward gross_revenue_rate
        sofr = parse_decimal(inputs.get("sofr", "0"))
        spread = rates.gross_revenue_rate - sofr
        subsidized_rate = sofr + decay_factor * spread

        # Cost is reimbursement: difference between base rate and subsidized rate
        rate_difference = rates.gross_revenue_rate - subsidized_rate
        monthly_cost = total_amount * rate_difference * MONTHLY_FACTOR

        return ExtensionResults(
            cost_adjustment=monthly_cost,
            breakdown={
                "subsidy_amount": total_amount,
                "subsidized_rate": subsidized_rate,
                "decay_factor": decay_factor,
                "subsidy_cost": monthly_cost,
            },
        )
