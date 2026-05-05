"""Agent valuations with binary active/inactive status."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Literal, Optional


@dataclass
class AgentDefinition:
    """Static agent definition."""
    name: str
    agent_type: Literal["FARM", "SELL"]
    ownership_ratio: Decimal
    market_cap_ratio: Optional[Decimal]  # None for spark (special case)


def is_agent_active(launch_month: int, current_month: int) -> bool:
    """Agent is active if current month >= launch month."""
    if launch_month <= 0:
        return False
    return current_month >= launch_month


def calculate_agent_value(
    agent: AgentDefinition,
    spark_market_cap: Decimal,
) -> Decimal:
    """Calculate agent value from spark market cap."""
    if agent.market_cap_ratio is None:  # spark special case
        return spark_market_cap * agent.ownership_ratio
    return spark_market_cap * agent.market_cap_ratio * agent.ownership_ratio


def aggregate_active_agents(
    agents: list[AgentDefinition],
    agent_launches: dict[str, int],
    current_month: int,
    spark_market_cap: Decimal,
) -> tuple[Decimal, Decimal]:
    """
    Sum values of all active agents by type.

    Returns:
        (farmable_tokens, sellable_tokens)
    """
    farmable = Decimal("0")
    sellable = Decimal("0")

    for agent in agents:
        launch_month = agent_launches.get(agent.name, 0)
        if is_agent_active(launch_month, current_month):
            value = calculate_agent_value(agent, spark_market_cap)
            if agent.agent_type == "FARM":
                farmable += value
            else:
                sellable += value

    return farmable, sellable
