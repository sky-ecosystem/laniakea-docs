"""End-of-period and annualized snapshot calculations."""

from dataclasses import dataclass
from decimal import Decimal

from .agents import AgentDefinition


@dataclass
class EndPeriodSnapshot:
    """End-of-period snapshot values.

    Uses full agent values (no launch weighting) for all launched agents.
    """
    end_farmable_tokens: Decimal
    end_unrewarded_usds_farm: Decimal
    end_usds_supply: Decimal


def calculate_end_snapshot(
    agents: list[AgentDefinition],
    period_configs: dict[str, int],  # name -> launch_month
    spark_market_cap: Decimal,
    end_base_usds: Decimal,
    farm_emission_rate: Decimal,
    farm_yield: Decimal,
) -> EndPeriodSnapshot:
    """
    Calculate end-of-period snapshot.

    All launched agents (launch_month > 0) contribute full value (no weighting).
    """
    from .agents import calculate_agent_value

    end_farmable = Decimal("0")

    for agent in agents:
        launch_month = period_configs.get(agent.name, 0)
        if launch_month > 0 and agent.agent_type == "FARM":
            value = calculate_agent_value(agent, spark_market_cap)
            end_farmable += value

    end_unrewarded_usds_farm = (end_farmable * farm_emission_rate) / farm_yield
    end_usds_supply = end_base_usds + end_unrewarded_usds_farm

    return EndPeriodSnapshot(
        end_farmable_tokens=end_farmable,
        end_unrewarded_usds_farm=end_unrewarded_usds_farm,
        end_usds_supply=end_usds_supply,
    )
