# Asset Type Treatment

**Last Updated:** 2026-01-27

## Asset Type Treatment

### Liquid TradFi (STRB — e.g., JAAA, Money Market ETFs)

| Component | Treatment |
|-----------|-----------|
| Fundamental risk | Credit risk weight of underlying securities |
| Drawdown risk | FRTB-style drawdown (see `market-risk-frtb.md`) |
| Stressed pull-to-par | Normal pull-to-par × stress modifier (e.g., ~3.5 years for JAAA) |
| Matching | Can be duration-matched to liability tiers ≥ stressed pull-to-par |
| **Capital if matched** | Risk weight only |
| **Capital if unmatched** | Full FRTB drawdown |

### Overcollateralized Crypto Lending (e.g., Sparklend)

| Component | Treatment |
|-----------|-----------|
| Fundamental risk | Smart contract risk, oracle risk |
| Drawdown risk | Gap risk — bad debt from flash crash (see `collateralized-lending-risk.md`) |
| Pull-to-par | **None** (perpetual positions, no maturity) |
| Matching | **Cannot be duration-matched** (no pull-to-par) |
| **Capital** | Must cover gap risk at relevant confidence level |

### Overcollateralized TradFi Lending (e.g., Lending Against Tokenized Treasuries)

| Component | Treatment |
|-----------|-----------|
| Fundamental risk | Credit risk of collateral, counterparty risk |
| Drawdown risk | Gap risk (lower volatility than crypto; see `collateralized-lending-risk.md`) |
| Pull-to-par | Depends on loan structure — if loans mature, there's a duration |
| Matching | Potentially matchable if loan book has defined duration |
| **Capital** | Hybrid — gap risk for unmatched portion, risk weight for matched portion |

---
