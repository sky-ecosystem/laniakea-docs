"""PSM Exposure extension.

Sky-held collateral earning below base rate (SOFR - spread instead of gross_revenue_rate).
PSM amount can be specified as a percentage of base USDS supply.
"""

from decimal import Decimal
from typing import Any, Dict

from ..loaders.models import parse_decimal
from .base import Extension, ExtensionResults


MONTHLY_FACTOR = Decimal("1") / Decimal("12")


class PSMExposureExtension(Extension):
    """PSM exposure - collateral earning lower rate."""

    name = "psm_exposure"

    def calculate(
        self,
        month: int,
        inputs: Dict[str, Any],
        rates: Any,
    ) -> ExtensionResults:
        if not self.enabled:
            return ExtensionResults()

        spread = parse_decimal(self.config.get("spread", "-0.0030"))  # -30bps default

        # Get PSM amount - either as percentage of total USDS or fixed amount
        # Check for percentage first (can be overridden in inputs)
        psm_pct = parse_decimal(inputs.get("psm_pct", self.config.get("pct", 0)))
        if psm_pct > 0:
            # Use total_usds if available (includes farming boost), else fall back to base_usds
            total_usds = parse_decimal(inputs.get("total_usds", inputs.get("base_usds", 0)))
            amount = total_usds * psm_pct
        else:
            # Fall back to fixed amount
            amount = parse_decimal(inputs.get("psm_amount", self.config.get("amount", 0)))

        if amount <= 0:
            return ExtensionResults()

        # PSM earns SOFR + spread (where spread is negative)
        sofr = parse_decimal(inputs.get("sofr", "0"))
        psm_rate = sofr + spread

        # The "cost" is the difference between what PSM earns and what it would earn
        # at gross_revenue_rate
        rate_difference = rates.gross_revenue_rate - psm_rate
        monthly_cost = amount * rate_difference * MONTHLY_FACTOR

        return ExtensionResults(
            gross_revenue_adjustment=-monthly_cost,  # reduces gross revenue
            breakdown={
                "psm_amount": amount,
                "psm_pct": psm_pct,
                "psm_rate": psm_rate,
                "psm_drag": monthly_cost,
            },
        )
