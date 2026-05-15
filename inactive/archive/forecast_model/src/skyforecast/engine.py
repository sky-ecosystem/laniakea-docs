"""Forecast engine - monthly calculations with quarterly aggregation."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, List, Optional

from .core import (
    RateInputs,
    DerivedRates,
    derive_rates,
    AgentDefinition,
    aggregate_active_agents,
    SupplyInputs,
    SupplyCalculations,
    calculate_supply,
    RevenueInputs,
    RevenueCalculations,
    calculate_revenue,
    WaterfallInputs,
    WaterfallResults,
    calculate_waterfall,
)
from .extensions import (
    Extension,
    PSMExposureExtension,
    SubsidizedBorrowExtension,
    SrUSDSCostExtension,
    TokenFarmingExtension,
    USDTSubsidyExtension,
    GenesisPrimeExtension,
    CoreVaultsExtension,
    AgentCreationFeeExtension,
)
from .loaders import AgentConfig, ModelConstants, ResolvedScenario
from .loaders.models import parse_decimal


EXTENSION_CLASSES = {
    "psm_exposure": PSMExposureExtension,
    "subsidized_borrow": SubsidizedBorrowExtension,
    "srusds_cost": SrUSDSCostExtension,
    "token_farming": TokenFarmingExtension,
    "usdt_subsidy": USDTSubsidyExtension,
    "genesis_prime": GenesisPrimeExtension,
    "core_vaults": CoreVaultsExtension,
    "agent_creation_fee": AgentCreationFeeExtension,
}


@dataclass
class MonthResults:
    """Results for a single month."""
    month: int
    month_name: str
    rates: DerivedRates
    farmable_tokens: Decimal
    sellable_tokens: Decimal
    supply: SupplyCalculations
    revenue: RevenueCalculations
    waterfall: WaterfallResults
    extension_costs: Decimal = Decimal("0")
    extension_supply_boost: Decimal = Decimal("0")


@dataclass
class QuarterResults:
    """Aggregated results for a quarter."""
    quarter: int
    quarter_name: str
    months: List[MonthResults]
    # Aggregated values
    gross_revenue: Decimal
    net_revenue: Decimal
    security_budget: Decimal
    backstop_contribution: Decimal
    backstop_withdrawal: Decimal
    net_backstop_change: Decimal
    staking_rewards: Decimal
    net_profit: Decimal
    # End-of-quarter values
    end_usds_supply: Decimal


@dataclass
class ScenarioResults:
    """Complete results for a scenario."""
    name: str
    description: str
    monthly: List[MonthResults]
    quarterly: List[QuarterResults]
    # Annual totals
    annual_gross_revenue: Decimal
    annual_net_revenue: Decimal
    annual_staking_rewards: Decimal
    annual_net_profit: Decimal


MONTH_NAMES = [
    "", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

QUARTER_MONTHS = ["", "Jan-Mar", "Apr-Jun", "Jul-Sep", "Oct-Dec"]


def _calendar_month(model_month: int, start_month: int) -> int:
    return ((model_month - 1 + start_month - 1) % 12) + 1


def _month_display_name(model_month: int, start_month: int) -> str:
    return MONTH_NAMES[_calendar_month(model_month, start_month)]


def _quarter_label(model_quarter: int, start_month: int, start_year: int) -> str:
    first_cal_month_idx = (model_quarter - 1) * 3 + start_month - 1
    cal_quarter = (first_cal_month_idx % 12) // 3 + 1
    cal_year = start_year + first_cal_month_idx // 12
    return f"Q{cal_quarter} {cal_year}"


def agents_from_config(configs: list[AgentConfig]) -> list[AgentDefinition]:
    """Convert config models to core domain models."""
    return [
        AgentDefinition(
            name=c.name,
            agent_type=c.type,
            ownership_ratio=c.ownership_ratio,
            market_cap_ratio=c.market_cap_ratio,
        )
        for c in configs
    ]


def create_extensions(extension_configs: Dict[str, Any]) -> List[Extension]:
    """Create extension instances from config."""
    extensions = []
    for name, config in extension_configs.items():
        if name in EXTENSION_CLASSES and config.get("enabled", True):
            extensions.append(EXTENSION_CLASSES[name](config))
    return extensions


def run_month(
    month: int,
    inputs: dict[str, Any],
    agents: list[AgentDefinition],
    agent_launches: dict[str, int],
    constants: ModelConstants,
    extensions: Optional[List[Extension]] = None,
    start_month: int = 1,
) -> MonthResults:
    """Run all calculations for a single month."""

    # Parse inputs to Decimal
    def get_decimal(key: str, default: Any = 0) -> Decimal:
        val = inputs.get(key, default)
        return parse_decimal(val) if val is not None else Decimal("0")

    # 1. Rate derivations
    rates = derive_rates(RateInputs(
        sofr=get_decimal("sofr"),
        savings_rate_spread=get_decimal("savings_rate_spread"),
        gross_revenue_rate_spread=get_decimal("gross_revenue_rate_spread"),
        farm_yield_spread=get_decimal("farm_yield_spread"),
    ))

    # 2. Run extensions (first pass) - get supply boost and non-PSM adjustments
    extension_supply_boost = Decimal("0")
    extension_gross_adj = Decimal("0")
    extension_cost_adj = Decimal("0")
    psm_extension = None

    if extensions:
        for ext in extensions:
            # Skip PSM extension for now - needs total supply
            if ext.name == "psm_exposure":
                psm_extension = ext
                continue
            result = ext.calculate(month, inputs, rates)
            extension_supply_boost += result.supply_boost
            extension_gross_adj += result.gross_revenue_adjustment
            extension_cost_adj += result.cost_adjustment

    # 3. Agent valuations (binary active/inactive) - legacy, will be replaced by token_farming extension
    spark_market_cap = get_decimal("spark_market_cap")
    farmable, sellable = aggregate_active_agents(
        agents=agents,
        agent_launches=agent_launches,
        current_month=month,
        spark_market_cap=spark_market_cap,
    )

    # 4. Supply calculations (include extension supply boost)
    base_usds = get_decimal("base_usds") + extension_supply_boost
    supply = calculate_supply(SupplyInputs(
        base_usds=base_usds,
        unrewarded_usds_user=get_decimal("unrewarded_usds_user"),
        farmable_tokens=farmable,
        farm_emission_rate=constants.farm_emission_rate,
        farm_yield=rates.farm_yield,
    ))

    # 4b. Run PSM extension with total supply available
    if psm_extension:
        psm_inputs = dict(inputs)
        psm_inputs["total_usds"] = supply.avg_usds_supply
        result = psm_extension.calculate(month, psm_inputs, rates)
        extension_gross_adj += result.gross_revenue_adjustment

    # 5. Revenue calculations (uses 1/12 factor internally)
    # Note: subsidized_borrow and srusds_cost are now handled by extensions
    # Setting to 0 here, extension costs applied after
    revenue = calculate_revenue(RevenueInputs(
        usds_supply=supply.avg_usds_supply,
        susds_supply=supply.avg_susds_supply,
        gross_revenue_rate=rates.gross_revenue_rate,
        savings_rate=rates.savings_rate,
        sellable_tokens=sellable,
        sell_token_rate=get_decimal("sell_token_rate"),
        subsidized_borrow=Decimal("0"),  # Handled by extension
        srusds_cost=Decimal("0"),         # Handled by extension
        tier2_ratio=get_decimal("tier2_ratio"),
        tier3_ratio=get_decimal("tier3_ratio"),
        tier4_ratio=get_decimal("tier4_ratio"),
    ))

    # Apply extension adjustments to net revenue
    adjusted_net_revenue = (
        revenue.net_revenue
        + extension_gross_adj  # PSM drag (negative)
        - extension_cost_adj   # Subsidies and costs (positive = cost)
    )

    # Create adjusted revenue result
    adjusted_revenue = RevenueCalculations(
        token_sales_income=revenue.token_sales_income,
        gross_revenue=revenue.gross_revenue + extension_gross_adj,
        savings_expense=revenue.savings_expense,
        distribution_rewards=revenue.distribution_rewards,
        net_revenue=adjusted_net_revenue,
    )

    # 6. TMF waterfall (uses adjusted net revenue)
    waterfall = calculate_waterfall(WaterfallInputs(
        net_revenue=adjusted_net_revenue,
        security_rate=get_decimal("security_rate"),
        backstop_rate=constants.backstop_rate,
        backstop_withdrawal=get_decimal("backstop_withdrawal"),
    ))

    month_name = _month_display_name(month, start_month)

    return MonthResults(
        month=month,
        month_name=month_name,
        rates=rates,
        farmable_tokens=farmable,
        sellable_tokens=sellable,
        supply=supply,
        revenue=adjusted_revenue,
        waterfall=waterfall,
        extension_costs=extension_cost_adj,
        extension_supply_boost=extension_supply_boost,
    )


def aggregate_quarter(
    months: List[MonthResults],
    quarter: int,
    quarter_name: Optional[str] = None,
) -> QuarterResults:
    """Aggregate monthly results into a quarter."""
    return QuarterResults(
        quarter=quarter,
        quarter_name=quarter_name or f"Q{quarter}",
        months=months,
        gross_revenue=sum(m.revenue.gross_revenue for m in months),
        net_revenue=sum(m.revenue.net_revenue for m in months),
        security_budget=sum(m.waterfall.security_budget for m in months),
        backstop_contribution=sum(m.waterfall.backstop_contribution for m in months),
        backstop_withdrawal=sum(m.waterfall.backstop_withdrawal for m in months),
        net_backstop_change=sum(m.waterfall.net_backstop_change for m in months),
        staking_rewards=sum(m.waterfall.staking_rewards for m in months),
        net_profit=sum(m.waterfall.net_profit for m in months),
        end_usds_supply=months[-1].supply.avg_usds_supply if months else Decimal("0"),
    )


def run_scenario(
    scenario: ResolvedScenario,
    agents: list[AgentConfig],
    constants: ModelConstants,
    extension_configs: Optional[Dict[str, Any]] = None,
) -> ScenarioResults:
    """Run all months and aggregate to quarters."""
    agent_defs = agents_from_config(agents)

    # Create extensions
    extensions = create_extensions(extension_configs or {})

    # Reset any stateful extensions before each scenario run.
    for ext in extensions:
        if hasattr(ext, 'reset'):
            ext.reset()

    # Run each month independently.
    monthly_results = []

    for month in range(1, scenario.months + 1):
        inputs = scenario.get_month_inputs(month)

        result = run_month(
            month=month,
            inputs=inputs,
            agents=agent_defs,
            agent_launches=scenario.agent_launches,
            constants=constants,
            extensions=extensions,
            start_month=scenario.start_month,
        )
        monthly_results.append(result)

    # Aggregate to quarters
    quarters = []
    for q in range(4):
        start = q * 3
        end = start + 3
        if end <= len(monthly_results):
            quarter_months = monthly_results[start:end]
            label = _quarter_label(q + 1, scenario.start_month, scenario.start_year)
            quarters.append(aggregate_quarter(quarter_months, q + 1, label))

    # Annual totals
    annual_gross = sum(m.revenue.gross_revenue for m in monthly_results)
    annual_net = sum(m.revenue.net_revenue for m in monthly_results)
    annual_staking = sum(m.waterfall.staking_rewards for m in monthly_results)
    annual_profit = sum(m.waterfall.net_profit for m in monthly_results)

    return ScenarioResults(
        name=scenario.name,
        description=scenario.description,
        monthly=monthly_results,
        quarterly=quarters,
        annual_gross_revenue=annual_gross,
        annual_net_revenue=annual_net,
        annual_staking_rewards=annual_staking,
        annual_net_profit=annual_profit,
    )
