# Trading

Specifications for the Sentinel Network and Sky Intents — the execution and trading infrastructure that operates Synomic Agents' PAUs. Sentinels are distinguished HPHA beacons that execute strategies in real time; Sky Intents is the intent-based trading protocol that enables secure, MEV-resistant trading.

## Documents

| Document | Description |
|---|---|
| [sentinel-network.md](sentinel-network.md) | Sentinel formations — coordinated HPHA beacon systems (Baseline/Stream/Warden) for real-time capital deployment |
| [sky-intents.md](sky-intents.md) | Intent-based trading protocol — signed intents, centralized matching, on-chain settlement, Exchange Halo integration |

## Related

- [`../synomics/macrosynomics/beacon-framework.md`](../synomics/macrosynomics/beacon-framework.md) — Broader beacon taxonomy (Sentinels are a distinguished HPHA subclass)
- [`../sky-agents/halo-agents/exchange-halo.md`](../sky-agents/halo-agents/exchange-halo.md) — Exchange Halo that operates orderbook infrastructure for Sky Intents
- [`../sky-agents/halo-agents/trading-halo.md`](../sky-agents/halo-agents/trading-halo.md) — AMM-based Trading Halo for instant RWA settlement
- [`../smart-contracts/architecture-overview.md`](../smart-contracts/architecture-overview.md) — PAU pattern that Sentinels operate through
