"""USDT Liquidity Subsidy extension.

Foregone PSM income on a portion of USDS for USDT liquidity.
USDT earns a fraction of SSR (default 50%) instead of PSM rate.
"""

from decimal import Decimal
from typing import Any, Dict

from ..loaders.models import parse_decimal
from .base import Extension, ExtensionResults


MONTHLY_FACTOR = Decimal("1") / Decimal("12")


class USDTSubsidyExtension(Extension):
    """USDT liquidity subsidy - reduced rate vs PSM."""

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

        # Rate factor: what fraction of SSR does USDT earn (default 50%)
        rate_factor = parse_decimal(self.config.get("rate_factor", "0.50"))

        if amount <= 0:
            return ExtensionResults()

        # PSM rate that we would otherwise earn
        sofr = parse_decimal(inputs.get("sofr", "0"))
        psm_rate = sofr + psm_spread

        # USDT earns rate_factor * SSR instead of PSM rate
        savings_rate = rates.savings_rate
        usdt_rate = savings_rate * rate_factor

        # Cost = difference between what we'd earn at PSM rate vs what we earn at USDT rate
        foregone_income = amount * (psm_rate - usdt_rate) * MONTHLY_FACTOR

        return ExtensionResults(
            cost_adjustment=foregone_income if foregone_income > 0 else Decimal("0"),
            gross_revenue_adjustment=-foregone_income if foregone_income < 0 else Decimal("0"),
            breakdown={
                "usdt_subsidy_amount": amount,
                "usdt_rate": usdt_rate,
                "usdt_foregone_income": foregone_income,
            },
        )
