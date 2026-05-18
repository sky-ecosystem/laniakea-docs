"""srUSDS Cost extension.

Fixed expense to attract senior risk capital.
Constant annual cost throughout the model period.
"""

from decimal import Decimal
from typing import Any, Dict

from ..loaders.models import parse_decimal
from .base import Extension, ExtensionResults


class SrUSDSCostExtension(Extension):
    """srUSDS cost - fixed cost for senior risk capital."""

    name = "srusds_cost"

    def calculate(
        self,
        month: int,
        inputs: Dict[str, Any],
        rates: Any,
    ) -> ExtensionResults:
        if not self.enabled:
            return ExtensionResults()

        annual_cost = parse_decimal(self.config.get("annual_cost", 5_000_000))
        monthly_cost = annual_cost / Decimal("12")

        return ExtensionResults(
            cost_adjustment=monthly_cost,
            breakdown={
                "srusds_annual_cost": annual_cost,
                "srusds_monthly_cost": monthly_cost,
            },
        )
