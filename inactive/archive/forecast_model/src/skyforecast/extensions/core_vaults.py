"""Core Vaults extension.

Core vaults provide a fixed higher yield than the base gross revenue rate.
This replaces a portion of normal base rate debt with higher-yielding debt.
"""

from decimal import Decimal
from typing import Any, Dict

from ..loaders.models import parse_decimal
from .base import Extension, ExtensionResults


MONTHLY_FACTOR = Decimal("1") / Decimal("12")


class CoreVaultsExtension(Extension):
    """Core vaults - fixed higher yield debt."""

    name = "core_vaults"

    def calculate(
        self,
        month: int,
        inputs: Dict[str, Any],
        rates: Any,
    ) -> ExtensionResults:
        if not self.enabled:
            return ExtensionResults()

        # Get core vault parameters (can be overridden in inputs)
        debt = parse_decimal(inputs.get("core_vault_debt", self.config.get("debt", 0)))
        vault_rate = parse_decimal(inputs.get("core_vault_rate", self.config.get("rate", "0.08")))

        if debt <= 0:
            return ExtensionResults()

        # Core vaults earn vault_rate instead of gross_revenue_rate
        # The benefit is the difference between vault_rate and gross_revenue_rate
        rate_difference = vault_rate - rates.gross_revenue_rate
        monthly_benefit = debt * rate_difference * MONTHLY_FACTOR

        return ExtensionResults(
            gross_revenue_adjustment=monthly_benefit,  # positive = additional revenue
            breakdown={
                "core_vault_debt": debt,
                "core_vault_rate": vault_rate,
                "rate_benefit": rate_difference,
                "monthly_benefit": monthly_benefit,
            },
        )
