"""Core calculation modules."""

from .rates import RateInputs, DerivedRates, derive_rates
from .agents import (
    AgentDefinition,
    is_agent_active,
    calculate_agent_value,
    aggregate_active_agents,
)
from .supply import SupplyInputs, SupplyCalculations, calculate_supply
from .revenue import RevenueInputs, RevenueCalculations, calculate_revenue, MONTHLY_FACTOR
from .waterfall import WaterfallInputs, WaterfallResults, calculate_waterfall

__all__ = [
    "RateInputs", "DerivedRates", "derive_rates",
    "AgentDefinition", "is_agent_active", "calculate_agent_value", "aggregate_active_agents",
    "SupplyInputs", "SupplyCalculations", "calculate_supply",
    "RevenueInputs", "RevenueCalculations", "calculate_revenue", "MONTHLY_FACTOR",
    "WaterfallInputs", "WaterfallResults", "calculate_waterfall",
]
