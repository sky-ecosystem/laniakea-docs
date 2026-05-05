# Exchange Halo

**Status:** Stub — specifications live in `trading/sky-intents.md`

---

## Overview

An **Exchange Halo** is a Special Halo that operates intent-based exchange infrastructure — orderbooks and matching engines for specific markets. Exchange Halos are part of the Sky Intents trading system.

| Property | Value |
|----------|-------|
| **Regulatory treatment** | Special (additional regulatory requirements) |
| **LPHA Beacon** | `lpha-exchange` — executes deterministic matching rules |
| **Mechanism** | Off-chain orderbook with on-chain atomic settlement |
| **Markets** | Spot trading, Halo Unit shares, risk capital tokens, restricted assets |

---

## Relationship to Trading Halos

Exchange Halos and Trading Halos serve complementary liquidity needs:

| | Exchange Halo | Trading Halo |
|---|---|---|
| **Mechanism** | Orderbook-based matching | AMM-based programmatic counterparty |
| **Liquidity** | Depends on counterparties posting orders | Always-on, oracle-referenced |
| **Price discovery** | Market-determined via matching | Oracle + spread |
| **Best for** | Price discovery, volatile assets | Predictable assets with known NAV (t-bills, money markets) |
| **Settlement** | Batch via `lpha-exchange` | Atomic on-chain swap |
| **Regulatory treatment** | Special | Standard |

Exchange Halos enable price discovery; Trading Halos provide baseline instant liquidity. Users may check both venues before executing.

---

## Specifications

Full Exchange Halo specifications are part of the Sky Intents system:

| Document | Content |
|----------|---------|
| `trading/sky-intents.md` | Intent-based trading protocol, fair matching, permissioned trading |
| `trading/sentinel-network.md` | `lpha-exchange` beacon context |

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| `trading-halo.md` | Complementary standard Halo providing AMM-based liquidity |
| `portfolio-halo.md` | Portfolio Halo (LCTS-based standard Halo) |
| `term-halo.md` | Term Halo (NFAT-based standard Halo) |
| `identity-network.md` | Identity Networks enable permissioned trading on Exchange Halos |
