"""Genesis Prime extension.

Prime tokens are sold (not farmed) at a fixed rate per year.
- Obex: 60% of Spark market cap
- Sell rate: 17.5% per year (25% * 0.7)
"""

from decimal import Decimal
from typing import Any, Dict

from ..loaders.models import parse_decimal
from .base import Extension, ExtensionResults


MONTHLY_FACTOR = Decimal("1") / Decimal("12")


class GenesisPrimeExtension(Extension):
    """Genesis Prime - token sales from prime protocols."""

    name = "genesis_prime"

    def calculate(
        self,
        month: int,
        inputs: Dict[str, Any],
        rates: Any,
    ) -> ExtensionResults:
        if not self.enabled:
            return ExtensionResults()

        sell_rate = parse_decimal(self.config.get("sell_rate", "0.175"))  # 17.5%
        primes_config = self.config.get("primes", {})

        # Get Spark market cap (primes are relative to it)
        spark_market_cap = parse_decimal(inputs.get("spark_market_cap", 0))

        total_token_sales = Decimal("0")
        prime_breakdown = {}

        for prime_name, prime_config in primes_config.items():
            launch_month = int(prime_config.get("launch_month", 1))
            months_active = month - launch_month

            # Check if prime is active
            if months_active < 0:
                continue

            # Get market cap as percentage of Spark
            market_cap_pct = parse_decimal(prime_config.get("market_cap_pct", "0"))
            market_cap = spark_market_cap * market_cap_pct
            ownership = parse_decimal(prime_config.get("ownership", "0.70"))

            # Value of Sky's holdings
            holdings_value = market_cap * ownership

            # Annual token sales (17.5% of holdings per year)
            annual_sales = holdings_value * sell_rate
            monthly_sales = annual_sales * MONTHLY_FACTOR

            total_token_sales += monthly_sales
            prime_breakdown[f"{prime_name}_token_sales"] = monthly_sales

        breakdown = {
            "total_prime_token_sales": total_token_sales,
        }
        breakdown.update(prime_breakdown)

        # Token sales add to gross revenue
        return ExtensionResults(
            gross_revenue_adjustment=total_token_sales,
            breakdown=breakdown,
        )
