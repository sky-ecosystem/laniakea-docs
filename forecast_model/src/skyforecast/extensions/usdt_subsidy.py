"""USDT Liquidity Subsidy extension.

Foregone PSM income on a portion of USDS for USDT liquidity.
Builds on PSM exposure - nullifies PSM income on specified amount.
"""

from decimal import Decimal
from typing import Any, Dict

from ..loaders.models import parse_decimal
from .base import Extension, ExtensionResults


MONTHLY_FACTOR = Decimal("1") / Decimal("12")


class USDTSubsidyExtension(Extension):
    """USDT liquidity subsidy - foregone PSM income."""

    name = "usdt_subsidy"

    def calculate(
        self,
        month: int,
        inputs: Dict[str, Any],
        rates: Any,
    ) -> ExtensionResults:
        if not self.enabled:
            return ExtensionResults()

        # Get amount (can be overridden in inputs)
        amount = parse_decimal(
            inputs.get("usdt_subsidy_amount", self.config.get("amount", 150_000_000))
        )
        psm_spread = parse_decimal(self.config.get("psm_spread", "-0.0030"))

        if amount <= 0:
            return ExtensionResults()

        # PSM rate that we're foregoing
        sofr = parse_decimal(inputs.get("sofr", "0"))
        psm_rate = sofr + psm_spread

        # Cost = foregone income (we earn 0 instead of psm_rate on this amount)
        # If psm_rate is positive, this is a cost
        # If psm_rate is negative (unlikely), this would be a benefit
        foregone_income = amount * psm_rate * MONTHLY_FACTOR

        return ExtensionResults(
            cost_adjustment=foregone_income if foregone_income > 0 else Decimal("0"),
            gross_revenue_adjustment=-foregone_income if foregone_income < 0 else Decimal("0"),
            breakdown={
                "usdt_subsidy_amount": amount,
                "usdt_foregone_income": foregone_income,
            },
        )
