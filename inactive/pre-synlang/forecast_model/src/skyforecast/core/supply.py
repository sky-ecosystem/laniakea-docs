"""USDS/sUSDS supply calculations."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class SupplyInputs:
    """Inputs for supply calculation."""
    base_usds: Decimal
    unrewarded_usds_user: Decimal
    farmable_tokens: Decimal
    farm_emission_rate: Decimal
    farm_yield: Decimal


@dataclass
class SupplyCalculations:
    """Derived supply values.

    Derivation chain:
        unrewarded_usds_farm = (farmable_tokens × emission_rate) / farm_yield
        avg_usds_supply = base_usds + unrewarded_usds_farm
        avg_unrewarded_usds = unrewarded_usds_user + unrewarded_usds_farm
        avg_susds_supply = avg_usds_supply - avg_unrewarded_usds
    """
    unrewarded_usds_farm: Decimal
    avg_usds_supply: Decimal
    avg_unrewarded_usds: Decimal
    avg_susds_supply: Decimal


def calculate_supply(inputs: SupplyInputs) -> SupplyCalculations:
    """Pure function: inputs → supply calculations."""
    unrewarded_usds_farm = (
        inputs.farmable_tokens * inputs.farm_emission_rate
    ) / inputs.farm_yield

    avg_usds_supply = inputs.base_usds + unrewarded_usds_farm
    avg_unrewarded_usds = inputs.unrewarded_usds_user + unrewarded_usds_farm
    avg_susds_supply = avg_usds_supply - avg_unrewarded_usds

    return SupplyCalculations(
        unrewarded_usds_farm=unrewarded_usds_farm,
        avg_usds_supply=avg_usds_supply,
        avg_unrewarded_usds=avg_unrewarded_usds,
        avg_susds_supply=avg_susds_supply,
    )
