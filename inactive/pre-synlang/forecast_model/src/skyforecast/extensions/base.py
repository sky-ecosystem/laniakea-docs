"""Base extension interface."""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, Optional


@dataclass
class ExtensionResults:
    """Results from all extensions for a single month."""
    # Revenue adjustments
    gross_revenue_adjustment: Decimal = Decimal("0")
    cost_adjustment: Decimal = Decimal("0")  # positive = cost, negative = income

    # Supply adjustments
    supply_boost: Decimal = Decimal("0")

    # Backstop adjustments (direct outflows, not counted as expenses)
    backstop_outflow: Decimal = Decimal("0")

    # Backstop tracking
    aggregate_backstop_capital: Optional[Decimal] = None
    genesis_capital_remaining: Optional[Decimal] = None

    # Breakdown for display
    breakdown: Dict[str, Decimal] = field(default_factory=dict)


class Extension:
    """Base class for extensions."""

    name: str = "base"

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)

    def calculate(
        self,
        month: int,
        inputs: Dict[str, Any],
        rates: Any,
    ) -> ExtensionResults:
        """Calculate extension effects for a month.

        Args:
            month: Current month number (1-indexed)
            inputs: Resolved inputs for this month
            rates: DerivedRates object with rate calculations

        Returns:
            ExtensionResults with adjustments
        """
        return ExtensionResults()
