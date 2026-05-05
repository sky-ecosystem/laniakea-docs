"""Token Farming extension.

Stars distribute tokens to USDS/sUSDS holders, creating supply boost.
- Distribution rate: 17.5% per year of original holdings (for first 2 years)
- Supply boost = distribution_value / farm_yield
"""

from decimal import Decimal
from typing import Any, Dict

from ..loaders.models import parse_decimal
from .base import Extension, ExtensionResults


MONTHLY_FACTOR = Decimal("1") / Decimal("12")


class TokenFarmingExtension(Extension):
    """Token farming - supply boost from star token distribution."""

    name = "token_farming"

    def calculate(
        self,
        month: int,
        inputs: Dict[str, Any],
        rates: Any,
    ) -> ExtensionResults:
        if not self.enabled:
            return ExtensionResults()

        distribution_rate = parse_decimal(self.config.get("distribution_rate", "0.175"))
        farm_yield_spread = parse_decimal(self.config.get("farm_yield_spread", "0.0010"))
        duration_months = int(self.config.get("duration_months", 24))
        stars_config = self.config.get("stars", {})

        # Farm yield = savings_rate + spread
        farm_yield = rates.savings_rate + farm_yield_spread

        if farm_yield <= 0:
            return ExtensionResults()

        total_distribution_value = Decimal("0")
        star_breakdown = {}

        # Get Spark market cap first (other stars are relative to it)
        spark_config = stars_config.get("spark", {})
        spark_market_cap = parse_decimal(
            inputs.get("spark_market_cap", spark_config.get("market_cap", 0))
        )

        for star_name, star_config in stars_config.items():
            launch_month = int(star_config.get("launch_month", 1))
            months_active = month - launch_month

            # Check if star is active and within distribution period
            if months_active < 0 or months_active >= duration_months:
                continue

            # Get market cap - Spark uses absolute, others use percentage of Spark
            if star_name == "spark":
                market_cap = spark_market_cap
            else:
                market_cap_pct = parse_decimal(star_config.get("market_cap_pct", "0"))
                market_cap = spark_market_cap * market_cap_pct
            ownership = parse_decimal(star_config.get("ownership", "0.65"))

            # Value of Sky's holdings
            holdings_value = market_cap * ownership

            # Annual distribution (17.5% of original holdings)
            annual_distribution = holdings_value * distribution_rate
            monthly_distribution = annual_distribution * MONTHLY_FACTOR

            total_distribution_value += monthly_distribution
            star_breakdown[f"{star_name}_distribution"] = monthly_distribution

        # Supply boost: users attracted by farming yield
        # distribution_value / (farm_yield / 12) = distribution_value * 12 / farm_yield
        if total_distribution_value > 0:
            supply_boost = total_distribution_value / (farm_yield * MONTHLY_FACTOR)
        else:
            supply_boost = Decimal("0")

        breakdown = {
            "farm_yield": farm_yield,
            "total_distribution_value": total_distribution_value,
            "farming_supply_boost": supply_boost,
        }
        breakdown.update(star_breakdown)

        return ExtensionResults(
            supply_boost=supply_boost,
            breakdown=breakdown,
        )
