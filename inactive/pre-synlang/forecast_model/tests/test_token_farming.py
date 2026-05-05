"""Tests for token farming and genesis prime extension calculations."""

import pytest
from decimal import Decimal
from dataclasses import dataclass

from skyforecast.extensions.token_farming import TokenFarmingExtension
from skyforecast.extensions.genesis_prime import GenesisPrimeExtension
from skyforecast.loaders.models import parse_decimal


@dataclass
class MockRates:
    """Mock rates object for testing."""
    savings_rate: Decimal = Decimal("0.04")  # 4%


class TestTokenFarmingCalculations:
    """Test the token farming supply boost calculations."""

    def test_spark_only_supply_boost(self):
        """Test supply boost from Spark alone."""
        config = {
            "enabled": True,
            "distribution_rate": "0.175",  # 17.5%
            "farm_yield_spread": "0.0010",  # 10bps
            "duration_months": 24,
            "stars": {
                "spark": {
                    "market_cap": 250_000_000,  # 250M
                    "ownership": "0.65",
                    "launch_month": 1,
                }
            }
        }

        ext = TokenFarmingExtension(config)
        rates = MockRates()

        result = ext.calculate(month=1, inputs={}, rates=rates)

        # Manual calculation:
        # holdings_value = 250M * 0.65 = 162.5M
        # annual_distribution = 162.5M * 0.175 = 28.4375M
        # monthly_distribution = 28.4375M / 12 = 2.3698M
        # farm_yield = 0.04 + 0.001 = 0.041
        # supply_boost = 2.3698M / (0.041 / 12) = 2.3698M * 12 / 0.041 = 693.3M

        expected_monthly_dist = Decimal("250000000") * Decimal("0.65") * Decimal("0.175") / Decimal("12")
        farm_yield = Decimal("0.041")
        expected_boost = expected_monthly_dist * Decimal("12") / farm_yield

        print(f"\nSpark only (250M MC):")
        print(f"  Monthly distribution: ${float(expected_monthly_dist):,.0f}")
        print(f"  Farm yield: {float(farm_yield)*100:.2f}%")
        print(f"  Supply boost: ${float(result.supply_boost):,.0f}")
        print(f"  Expected boost: ${float(expected_boost):,.0f}")

        assert abs(result.supply_boost - expected_boost) < Decimal("1"), f"Expected {expected_boost}, got {result.supply_boost}"

    def test_all_stars_q4_supply_boost(self):
        """Test supply boost with all stars active in Q4."""
        config = {
            "enabled": True,
            "distribution_rate": "0.175",
            "farm_yield_spread": "0.0010",
            "duration_months": 24,
            "stars": {
                "spark": {
                    "market_cap": 430_000_000,  # Q4: 430M
                    "ownership": "0.65",
                    "launch_month": 1,
                },
                "grove": {
                    "market_cap_pct": "0.60",  # 60% of Spark
                    "ownership": "0.70",
                    "launch_month": 4,
                },
                "keel": {
                    "market_cap_pct": "0.25",
                    "ownership": "0.70",
                    "launch_month": 6,
                },
                "star4": {
                    "market_cap_pct": "0.25",
                    "ownership": "0.32",
                    "launch_month": 7,
                },
                "star5": {
                    "market_cap_pct": "0.25",
                    "ownership": "0.80",
                    "launch_month": 10,
                },
            }
        }

        ext = TokenFarmingExtension(config)
        rates = MockRates()

        # Test month 12 (all stars active)
        result = ext.calculate(month=12, inputs={}, rates=rates)

        spark_mc = Decimal("430000000")
        farm_yield = Decimal("0.041")

        # Calculate expected per-star
        stars = [
            ("spark", spark_mc, Decimal("0.65")),
            ("grove", spark_mc * Decimal("0.60"), Decimal("0.70")),
            ("keel", spark_mc * Decimal("0.25"), Decimal("0.70")),
            ("star4", spark_mc * Decimal("0.25"), Decimal("0.32")),
            ("star5", spark_mc * Decimal("0.25"), Decimal("0.80")),
        ]

        print(f"\nAll stars active (Month 12, Spark MC = 430M):")
        total_monthly_dist = Decimal("0")
        for name, mc, ownership in stars:
            holdings = mc * ownership
            monthly_dist = holdings * Decimal("0.175") / Decimal("12")
            boost = monthly_dist * Decimal("12") / farm_yield
            total_monthly_dist += monthly_dist
            print(f"  {name}: MC=${float(mc):,.0f}, holdings=${float(holdings):,.0f}, dist=${float(monthly_dist):,.0f}/mo, boost=${float(boost):,.0f}")

        expected_boost = total_monthly_dist * Decimal("12") / farm_yield
        print(f"  TOTAL monthly distribution: ${float(total_monthly_dist):,.0f}")
        print(f"  TOTAL supply boost: ${float(result.supply_boost):,.0f}")
        print(f"  Expected boost: ${float(expected_boost):,.0f}")

        # The supply boost is HUGE - nearly 3B!
        assert result.supply_boost > Decimal("2_000_000_000"), "Supply boost should be over 2B"

    def test_supply_boost_vs_base_usds(self):
        """Compare supply boost to base USDS to show relative impact."""
        config = {
            "enabled": True,
            "distribution_rate": "0.175",
            "farm_yield_spread": "0.0010",
            "duration_months": 24,
            "stars": {
                "spark": {
                    "market_cap": 430_000_000,
                    "ownership": "0.65",
                    "launch_month": 1,
                },
                "grove": {
                    "market_cap_pct": "0.60",
                    "ownership": "0.70",
                    "launch_month": 4,
                },
                "keel": {
                    "market_cap_pct": "0.25",
                    "ownership": "0.70",
                    "launch_month": 6,
                },
                "star4": {
                    "market_cap_pct": "0.25",
                    "ownership": "0.32",
                    "launch_month": 7,
                },
                "star5": {
                    "market_cap_pct": "0.25",
                    "ownership": "0.80",
                    "launch_month": 10,
                },
            }
        }

        ext = TokenFarmingExtension(config)
        rates = MockRates()

        # Base USDS at end of year
        base_usds = Decimal("16_000_000_000")  # 16B

        result = ext.calculate(month=12, inputs={}, rates=rates)

        boost_pct = result.supply_boost / base_usds * Decimal("100")

        print(f"\nSupply boost impact:")
        print(f"  Base USDS: ${float(base_usds):,.0f}")
        print(f"  Supply boost: ${float(result.supply_boost):,.0f}")
        print(f"  Boost as % of base: {float(boost_pct):.1f}%")

        # This shows the issue - boost is 15-20% of base supply!

    def test_lower_ownership_reduces_boost(self):
        """Test that reducing ownership significantly reduces boost."""
        # Original ownership
        config_high = {
            "enabled": True,
            "distribution_rate": "0.175",
            "farm_yield_spread": "0.0010",
            "duration_months": 24,
            "stars": {
                "spark": {"market_cap": 250_000_000, "ownership": "0.65", "launch_month": 1},
                "grove": {"market_cap_pct": "0.60", "ownership": "0.70", "launch_month": 4},
            }
        }

        # Lower ownership
        config_low = {
            "enabled": True,
            "distribution_rate": "0.175",
            "farm_yield_spread": "0.0010",
            "duration_months": 24,
            "stars": {
                "spark": {"market_cap": 250_000_000, "ownership": "0.30", "launch_month": 1},
                "grove": {"market_cap_pct": "0.60", "ownership": "0.30", "launch_month": 4},
            }
        }

        ext_high = TokenFarmingExtension(config_high)
        ext_low = TokenFarmingExtension(config_low)
        rates = MockRates()

        result_high = ext_high.calculate(month=6, inputs={}, rates=rates)
        result_low = ext_low.calculate(month=6, inputs={}, rates=rates)

        print(f"\nOwnership impact:")
        print(f"  High ownership (65%/70%): ${float(result_high.supply_boost):,.0f}")
        print(f"  Low ownership (30%/30%): ${float(result_low.supply_boost):,.0f}")
        print(f"  Ratio: {float(result_high.supply_boost / result_low.supply_boost):.2f}x")


class TestSupplyBoostFormula:
    """Test the supply boost formula itself."""

    def test_formula_interpretation(self):
        """The supply boost formula: dist_value / (yield/12) = dist_value * 12 / yield

        This represents: how much capital is needed to absorb all farming rewards
        at the given yield rate.

        Example: If monthly rewards = $5M and annual yield = 4%
        Monthly yield = 4%/12 = 0.33%
        Capital needed = $5M / 0.33% = $1.5B

        This means: to earn $5M at 0.33% monthly, you need $1.5B deposited.
        """
        monthly_distribution = Decimal("5_000_000")  # $5M
        annual_yield = Decimal("0.04")  # 4%

        supply_boost = monthly_distribution / (annual_yield / Decimal("12"))

        print(f"\nFormula interpretation:")
        print(f"  Monthly distribution: ${float(monthly_distribution):,.0f}")
        print(f"  Annual yield: {float(annual_yield)*100:.1f}%")
        print(f"  Monthly yield: {float(annual_yield/12)*100:.3f}%")
        print(f"  Supply boost (capital needed): ${float(supply_boost):,.0f}")

        # Verify: capital * monthly_yield = monthly_distribution
        verify = supply_boost * (annual_yield / Decimal("12"))
        print(f"  Verify: ${float(supply_boost):,.0f} * {float(annual_yield/12)*100:.3f}% = ${float(verify):,.0f}")

        assert abs(verify - monthly_distribution) < Decimal("1")


class TestGenesisPrimeExtension:
    """Test the genesis prime token sales calculations."""

    def test_obex_not_active_before_launch(self):
        """Obex should not generate revenue before M11."""
        config = {
            "enabled": True,
            "sell_rate": "0.175",
            "primes": {
                "obex": {
                    "market_cap_pct": "0.60",
                    "ownership": "0.70",
                    "launch_month": 11,
                }
            }
        }

        ext = GenesisPrimeExtension(config)
        rates = MockRates()

        # Month 10 - not yet launched
        result = ext.calculate(month=10, inputs={"spark_market_cap": 430_000_000}, rates=rates)
        assert result.gross_revenue_adjustment == Decimal("0")
        print(f"\nMonth 10 (before launch): ${float(result.gross_revenue_adjustment):,.0f}")

    def test_obex_active_after_launch(self):
        """Obex should generate token sales revenue after M11."""
        config = {
            "enabled": True,
            "sell_rate": "0.175",
            "primes": {
                "obex": {
                    "market_cap_pct": "0.60",
                    "ownership": "0.70",
                    "launch_month": 11,
                }
            }
        }

        ext = GenesisPrimeExtension(config)
        rates = MockRates()

        # Month 11 - just launched
        spark_mc = Decimal("430000000")  # Q4 Spark MC
        result = ext.calculate(month=11, inputs={"spark_market_cap": spark_mc}, rates=rates)

        # Manual calc:
        # obex MC = 430M * 0.60 = 258M
        # holdings = 258M * 0.70 = 180.6M
        # annual sales = 180.6M * 0.175 = 31.605M
        # monthly sales = 31.605M / 12 = 2.634M
        expected = spark_mc * Decimal("0.60") * Decimal("0.70") * Decimal("0.175") / Decimal("12")

        print(f"\nMonth 11 (Obex launched):")
        print(f"  Spark MC: ${float(spark_mc):,.0f}")
        print(f"  Obex MC (60%): ${float(spark_mc * Decimal('0.60')):,.0f}")
        print(f"  Holdings (70%): ${float(spark_mc * Decimal('0.60') * Decimal('0.70')):,.0f}")
        print(f"  Monthly token sales: ${float(result.gross_revenue_adjustment):,.0f}")
        print(f"  Expected: ${float(expected):,.0f}")

        assert abs(result.gross_revenue_adjustment - expected) < Decimal("1")

    def test_genesis_prime_vs_token_farming_difference(self):
        """Genesis Prime adds to gross revenue (token sales), not supply boost."""
        # Token farming config (similar to genesis prime for comparison)
        farming_config = {
            "enabled": True,
            "distribution_rate": "0.175",
            "farm_yield_spread": "0.0010",
            "duration_months": 24,
            "stars": {
                "spark": {
                    "market_cap": 430_000_000,
                    "ownership": "0.70",
                    "launch_month": 1,
                }
            }
        }

        # Genesis prime config
        prime_config = {
            "enabled": True,
            "sell_rate": "0.175",
            "primes": {
                "test": {
                    "market_cap_pct": "1.0",  # 100% of Spark for easy comparison
                    "ownership": "0.70",
                    "launch_month": 1,
                }
            }
        }

        farming_ext = TokenFarmingExtension(farming_config)
        prime_ext = GenesisPrimeExtension(prime_config)
        rates = MockRates()

        farming_result = farming_ext.calculate(month=6, inputs={}, rates=rates)
        prime_result = prime_ext.calculate(month=6, inputs={"spark_market_cap": 430_000_000}, rates=rates)

        print(f"\nToken Farming vs Genesis Prime (same holdings):")
        print(f"  Token Farming: supply_boost=${float(farming_result.supply_boost):,.0f}, gross_adj=${float(farming_result.gross_revenue_adjustment):,.0f}")
        print(f"  Genesis Prime: supply_boost=${float(prime_result.supply_boost):,.0f}, gross_adj=${float(prime_result.gross_revenue_adjustment):,.0f}")

        # Token farming creates supply boost, not gross revenue adjustment
        assert farming_result.supply_boost > 0
        assert farming_result.gross_revenue_adjustment == 0

        # Genesis prime creates gross revenue adjustment, not supply boost
        assert prime_result.supply_boost == 0
        assert prime_result.gross_revenue_adjustment > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
