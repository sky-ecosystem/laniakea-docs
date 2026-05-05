"""Rate derivations from SOFR base."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class RateInputs:
    """Input rates for derivation."""
    sofr: Decimal
    savings_rate_spread: Decimal
    gross_revenue_rate_spread: Decimal
    farm_yield_spread: Decimal


@dataclass
class DerivedRates:
    """Derived rates from SOFR base.

    Derivation chain:
        savings_rate = sofr + savings_rate_spread
        gross_revenue_rate = savings_rate + gross_revenue_rate_spread
        farm_yield = savings_rate + farm_yield_spread
    """
    sofr: Decimal
    savings_rate: Decimal
    gross_revenue_rate: Decimal
    farm_yield: Decimal


def derive_rates(inputs: RateInputs) -> DerivedRates:
    """Pure function: inputs → derived rates."""
    savings_rate = inputs.sofr + inputs.savings_rate_spread
    return DerivedRates(
        sofr=inputs.sofr,
        savings_rate=savings_rate,
        gross_revenue_rate=savings_rate + inputs.gross_revenue_rate_spread,
        farm_yield=savings_rate + inputs.farm_yield_spread,
    )
