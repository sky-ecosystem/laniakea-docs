"""Extensions module - modular temporary mechanisms."""

from .base import Extension, ExtensionResults
from .psm_exposure import PSMExposureExtension
from .subsidized_borrow import SubsidizedBorrowExtension
from .srusds_cost import SrUSDSCostExtension
from .token_farming import TokenFarmingExtension
from .genesis_capital import GenesisCapitalExtension
from .genesis_capital_spending import GenesisCapitalSpendingExtension
from .usdt_subsidy import USDTSubsidyExtension
from .genesis_prime import GenesisPrimeExtension
from .core_vaults import CoreVaultsExtension
from .agent_creation_fee import AgentCreationFeeExtension

__all__ = [
    "Extension",
    "ExtensionResults",
    "PSMExposureExtension",
    "SubsidizedBorrowExtension",
    "SrUSDSCostExtension",
    "TokenFarmingExtension",
    "GenesisCapitalExtension",
    "GenesisCapitalSpendingExtension",
    "USDTSubsidyExtension",
    "GenesisPrimeExtension",
    "CoreVaultsExtension",
    "AgentCreationFeeExtension",
]
