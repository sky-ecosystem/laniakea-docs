"""Genesis Capital Phase-out extension.

Tracks genesis capital allocated to stars and phase-out over time.
Phase-out doesn't affect expenses, just reduces backstop accounting.

Phase-out logic (monthly):
- IF star has token with ≥10m daily volume
- AND aggregate_backstop_capital ≥ 50m
- THEN phase out: 1m base + 1m per 10m above 50m per eligible star
"""

from decimal import Decimal
from typing import Any, Dict, Optional

from ..loaders.models import parse_decimal
from .base import Extension, ExtensionResults


class GenesisCapitalExtension(Extension):
    """Genesis capital phase-out - backstop accounting."""

    name = "genesis_capital"

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        # Track cumulative phase-out per star
        self._cumulative_phaseout: Dict[str, Decimal] = {}
        self._initialized = False

    def _initialize_if_needed(self):
        if self._initialized:
            return
        stars_config = self.config.get("stars", {})
        for star_name in stars_config:
            self._cumulative_phaseout[star_name] = Decimal("0")
        self._initialized = True

    def calculate(
        self,
        month: int,
        inputs: Dict[str, Any],
        rates: Any,
        displayed_backstop: Optional[Decimal] = None,
    ) -> ExtensionResults:
        if not self.enabled:
            return ExtensionResults()

        self._initialize_if_needed()

        stars_config = self.config.get("stars", {})
        min_backstop = parse_decimal(self.config.get("min_backstop_threshold", 50_000_000))
        base_phaseout = parse_decimal(self.config.get("base_phaseout_per_star", 1_000_000))
        phaseout_per_10m = parse_decimal(self.config.get("phaseout_per_10m_above", 1_000_000))

        # Calculate total remaining genesis capital before this month's phase-out
        total_genesis = Decimal("0")
        for star_name, star_config in stars_config.items():
            genesis_capital = parse_decimal(star_config.get("genesis_capital", 0))
            remaining = genesis_capital - self._cumulative_phaseout.get(star_name, Decimal("0"))
            total_genesis += max(Decimal("0"), remaining)

        # Use displayed_backstop for phaseout threshold (surplus + contributions + genesis)
        # If not provided, fall back to genesis remaining only
        if displayed_backstop is None:
            displayed_backstop = total_genesis

        # Determine phase-out for this month
        month_phaseout = Decimal("0")
        star_breakdown = {}

        if displayed_backstop >= min_backstop:
            # Calculate phase-out rate based on displayed backstop
            above_min = displayed_backstop - min_backstop
            bonus_phaseout = (above_min // Decimal("10_000_000")) * phaseout_per_10m
            per_star_phaseout = base_phaseout + bonus_phaseout

            for star_name, star_config in stars_config.items():
                launch_month = int(star_config.get("token_launch", 1))
                has_volume = star_config.get("has_volume", True)
                genesis_capital = parse_decimal(star_config.get("genesis_capital", 0))

                # Check if star is eligible for phase-out
                if month < launch_month or not has_volume:
                    continue

                # Calculate remaining genesis capital for this star
                remaining = genesis_capital - self._cumulative_phaseout.get(star_name, Decimal("0"))
                if remaining <= 0:
                    continue

                # Phase out (capped at remaining)
                actual_phaseout = min(per_star_phaseout, remaining)
                self._cumulative_phaseout[star_name] = (
                    self._cumulative_phaseout.get(star_name, Decimal("0")) + actual_phaseout
                )
                month_phaseout += actual_phaseout
                star_breakdown[f"{star_name}_phaseout"] = actual_phaseout

        # Recalculate remaining genesis capital after phase-out
        total_remaining = Decimal("0")
        for star_name, star_config in stars_config.items():
            genesis_capital = parse_decimal(star_config.get("genesis_capital", 0))
            remaining = genesis_capital - self._cumulative_phaseout.get(star_name, Decimal("0"))
            total_remaining += max(Decimal("0"), remaining)
            star_breakdown[f"{star_name}_remaining"] = max(Decimal("0"), remaining)

        breakdown = {
            "genesis_capital_remaining": total_remaining,
            "month_phaseout": month_phaseout,
        }
        breakdown.update(star_breakdown)

        return ExtensionResults(
            genesis_capital_remaining=total_remaining,
            breakdown=breakdown,
        )

    def reset(self):
        """Reset cumulative state for a new scenario run."""
        self._cumulative_phaseout = {}
        self._initialized = False
