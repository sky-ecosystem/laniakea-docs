# Current Accounting (Pre-Laniakea)

**Status:** Draft
**Last Updated:** 2026-02-12

---

## Overview

This document describes how Sky's accounting currently works — the monthly settlement cycle, three major legacy exceptions, and recent accounting changes that affect how the numbers look.

The current system is transitional. It will be replaced by the daily settlement cycle (`daily-settlement-cycle.md`) as Laniakea phases roll out, but understanding the current state is necessary for interpreting financial data during the transition.

---

## Monthly Settlement Cycle

Sky currently operates on a **monthly settlement cycle**. Settlement is a **manual process** — slow and operationally cumbersome — typically executed toward the **end of the following month**. For example, January's settlement is processed in late February.

This manual cadence means that fund transfers (including Security & Maintenance Budget payments from the Surplus Buffer to the Core Council Buffer) only happen at settlement time. Expenses therefore appear in lumps at settlement, not spread across the period they cover.

At each Monthly Settlement:

1. **Net Revenue Calculation** — Total protocol revenue minus costs for the period
2. **TMF Waterfall** — Net revenue distributed per the Treasury Management Function (see `appendix-c-treasury-management-function.md`):
   - Security & Maintenance Budget (currently 21% Genesis Phase rate)
   - Aggregate Backstop Capital contribution (25% minimum retention until $125M target)
   - Fortification Conserver
   - Smart Burn Engine
   - Staking Rewards (remainder)
3. **Senior Risk Capital Origination** — srUSDS clearing price and OSRC capacity
4. **srUSDS Conversions** — Queued subscribe/redeem requests processed
5. **Smart Burn** — Burn rate calculated and executed
6. **GovOps Functions** — Payments, compliance, penalty processing

For the detailed calculation of what each Prime owes at settlement, see `prime-settlement-methodology.md`.

### November/December 2025 Settlement Anomaly

The November 2025 settlement was skipped over the Christmas period. It was instead processed together with the December 2025 settlement at the end of January 2026 — two months of activity compressed into a single processing window.

**Why this matters:** Settlement is when fund transfers happen. Two months of Security & Maintenance payments, backstop contributions, and other TMF waterfall transfers all executed at once, making late January 2026 look like a period of unusually high spending.

**Compounding factors:** This double settlement coincided with the Core Council Buffer reclassification (see below), which also took effect at the end of January 2026. The combination of a double settlement and a one-time accounting reclassification in the same window created an apparent expense spike that was significantly larger than either event alone.

**Dashboard distortion:** Dashboards like info.sky.money display expenses as the last 3 months annualized. A one-time lump of expenses concentrated in a single month gets annualized at roughly 4× its actual value, making the expense figure appear far higher than the real run-rate. This annualization effect will wash out over the following months as the 3-month window moves past the anomaly.

When reviewing Q4 2025 / Q1 2026 financial data, these timing effects should be kept in mind.

---

## Three Legacy Exceptions

The current accounting has three major categories of assets that don't yet fit cleanly into the Laniakea capital flow architecture (Generator → Prime → Halo). Each is handled differently and has its own accounting quirks.

### 1. Legacy Core Vaults

**What they are:** The original MakerDAO CDP vaults — ETH-A, ETH-B, ETH-C, WBTC-A, WSTETH-A, and others. These are overcollateralized lending positions where users deposit crypto collateral and borrow USDS (originally DAI).

**Current treatment:** These are being standardized as **Core Controlled Agents** under Core Council governance. In Laniakea terms, they sit at the Halo layer but predate the Prime/Halo architecture.

**Accounting implications:**
- Revenue from stability fees flows directly to the protocol, not through a Prime
- Collateral ratios and liquidation parameters are managed by governance, not by Prime-level risk management
- These positions will eventually be migrated to proper Prime → Halo flows or wound down

### 2. PSM (Peg Stability Module)

**What it is:** The LitePSM provides 1:1 USDC ↔ USDS conversion, maintaining the USDS peg. It holds USDC as a reserve asset.

**Current treatment:** Sky Core manages the LitePSM directly. Multi-chain PSM3 instances exist on Base, Arbitrum, Unichain, and Optimism.

**Accounting implications:**
- USDC held in the PSM earns no yield (opportunity cost)
- PSM USDC counts as Resting ASC (Actively Stabilizing Collateral) — see `../risk-framework/asc.md`
- The PSM is being transitioned to Grove's operational ownership, at which point Grove pays the Base Rate on PSM assets and manages it as an ASC asset under ALM rules
- Until transition completes, PSM assets sit outside the normal Prime capital flow and are accounted for separately

### 3. Legacy RWA (HVB and Others)

**What they are:** Real-world asset positions established under MakerDAO governance — including Huntingdon Valley Bank (HVB) and other legacy RWA arrangements. These are direct lending or investment relationships with traditional financial counterparties.

**Current treatment:** These predate the Halo framework. They don't have standardized LCTS interfaces, Halo Unit tokens, or beacon-operated settlement.

**Accounting implications:**
- Revenue recognition depends on the specific deal structure (interest payments, maturity schedules)
- These positions lack the standardized risk framework treatment (no SPTP classification, no duration matching, no gap risk model)
- Wind-down or migration to Portfolio/Term Halos is expected but timelines vary by counterparty
- Until migrated, they are accounted for on their own terms — each with different reporting cadences and settlement mechanics

---

## Core Council Buffer Reclassification

### Previous Treatment

The Core Council Buffer previously counted as protocol capital — internal reserves of the system. Because it was included in the Aggregate Backstop Capital calculation, the Security and Maintenance Budget payouts funded from it **did not appear as expenses** in protocol accounting — the money moved within what was considered the protocol's own capital base.

Under this treatment, expenses were only recognized when the Core Council Buffer *disbursed* funds (e.g., paid a vendor or team). The transfer from the Surplus Buffer to the Core Council Buffer was an internal capital movement, not an expense.

### Current Treatment

The Core Council Buffer **no longer counts toward Aggregate Backstop Capital**. It is now classified as operational capital — external to the system's reserves. The formula is now:

```
Aggregate Backstop Capital = Total Genesis Capital - Allocated Genesis Capital
```

**Expense recognition change:** Under the updated methodology, Surplus Buffer transfers to the Core Council Buffer (and the Aligned Delegates Buffer) are recognized as expenses **at the point of transfer from the Surplus Buffer**, rather than when the respective wallets disburse the funds. This means the entire transfer amount appears as an expense immediately, even though the actual spending happens gradually over subsequent months.

### Visible Effects

This reclassification has three visible effects:

1. **One-time stock reclassification** — The entire existing Core Council Buffer balance was reclassified from internal reserves to operational capital in a single accounting event (end of January 2026). This appeared as a large one-time expense as those assets stopped being counted as system capital.
2. **Ongoing expense recognition change** — Future S&M payments now show up as expenses at the point of Surplus Buffer transfer, making current spending look higher relative to prior periods (where the same payments were invisible as internal capital movements).
3. **Lower reported Aggregate Backstop Capital** — Removing the Core Council Buffer from the calculation reduces the headline safety margin figure.

**None of these represents an actual change in economic reality** — the same money is flowing to the same places. The accounting now more accurately reflects that the Core Council Buffer is operational spending capacity, not a solvency backstop.

### Dashboard Amplification

Dashboards that display expenses as "last 3 months annualized" (such as info.sky.money) amplify one-time events. The reclassification of the entire CCB stock, combined with the double November/December settlement, occurred in a single month — and the annualized display multiplied this lump by roughly 4×. This effect is temporary and will normalize as the 3-month window moves past the anomaly.

---

## Smart Burn Engine (Current Configuration)

The Smart Burn Engine (SBE) is the protocol's SKY buyback mechanism, funded by TMF Step 4 (and currently Step 5 as well).

### Current Behavior: Fixed Buyback Amount

The SBE is currently operating in a **special temporary configuration** where it buys a **fixed amount of SKY regardless of market conditions**, currently approximately **$300,000 per day**. In this temporary configuration, Steps 4 and 5 of the TMF waterfall are unified in execution — all funds from both steps are used to buy SKY from the open market. The canonical TMF defines these as separate steps (Step 4: Smart Burn Engine, Step 5: Staking Rewards — see `../whitepaper/appendix-c-treasury-management-function.md`); the current unification is an operational simplification that will be unwound when the SBE BEAM system is deployed.

The accumulated SKY purchased through this process is **distributed to SKY stakers** as yield.

### Staking Rewards Feedback Mechanism

SKY staking rewards are adjusted periodically via governance spells, designed to track the USD value of SKY being bought back through the SBE. This creates a **counter-cyclical feedback loop**:

- **SKY price rises** → $300k/day buys fewer SKY → staking rewards (in SKY terms) decrease
- **SKY price falls** → $300k/day buys more SKY → staking rewards (in SKY terms) increase

The staking reward rate is adjusted slowly (gradual increases or decreases) to follow the buyback output, not pegged exactly to it. This smooths volatility while keeping staking yields roughly aligned with what the protocol is actually buying.

**Growth path:** As protocol profits increase over time, the daily buyback rate will also increase, which pulls staking rewards up with it.

### Long-Run SBE (Not Yet Active)

The planned long-run SBE uses a dynamic burn rate formula that adjusts buying based on market conditions:

```
Burn Rate = (1 - MC / TMC) × 50%
```

Where MC is current market capitalization and TMC is a target market cap derived from growth rate and annual profits. This formula buys more when the token is undervalued and retains capital when overvalued.

### Why the Long-Run SBE Isn't Active Yet

Switching to the dynamic formula requires a **SBE BEAM system** — a governance-controlled execution surface with proper rate limits and parameter management. This BEAM system can only be created after the transition to the daily settlement cycle (Phase 3), because:

- The SBE BEAM needs to operate within the daily settlement cadence for parameter updates and execution windows
- Proper rate limits and governance controls must be in place before allowing dynamic market-responsive behavior
- The current fixed-amount approach is safe and simple enough to operate without BEAM infrastructure

Until then, the fixed buyback configuration continues.

---

## Income & Expense Categories

Understanding Sky's P&L requires distinguishing between **cost of capital** (payments to attract and retain USDS supply) and **operational expenses** (payments to run the protocol). Cost of capital is the largest expense category by far, but it is the mechanism that makes the system work — not overhead.

### Income Categories

| Category | Examples | Notes |
|----------|----------|-------|
| **CDPs (Core Vaults)** | ETH-A, ETH-B, ETH-C, WBTC-A, WSTETH-A, LSEV2-SKY-A | Legacy overcollateralized lending; stability fee income |
| **D3Ms** | DIRECT-SPARK-DAI, DIRECT-SPARK-MORPHO | Direct Deposit Modules; being wound down (legacy) |
| **Primes** | ALLOCATOR-SPARK-A, ALLOCATOR-BLOOM-A (Grove), ALLOCATOR-OBEX-A, ALLOCATOR-NOVA-A (Keel) | New Laniakea capital allocation; growing as Primes scale |
| **Rewards Income** | SKY-SPK | Income from rewards tokens; recognized when distributed |
| **Legacy RWA** | RWA015-A, RWA007-A, RWA009-A | Bespoke real-world asset deals; winding down or migrating |
| **Stablecoins** | LITE-PSM-USDC-A | PSM fee income from USDC ↔ USDS conversions |

### Expense Categories

| Category | Examples | Nature |
|----------|----------|--------|
| **Operations** | Spells, Vest, Core Council Buffer, Accessibility Rewards | **Operational expense** — cost of running governance and teams |
| **Rewards** | USDS-SKY farming rewards | **Growth expense** — incentives to attract ecosystem participation |
| **Savings** | DSR, SSR/sUSDS, Integration Boost | **Cost of capital** — yield paid to USDS holders to attract/retain supply |
| **Staking** | SKY-SKY, stUSDS | **Value distribution** — SKY yield from buyback proceeds |

### Cost of Capital vs Operational Expenses

In FY 2025, Savings (DSR + SSR + Integration Boost) was approximately $194M out of $285M total expenses — roughly 68% of all spending. This is the cost of maintaining the savings rate that attracts USDS deposits. It scales with USDS supply and the savings rate spread, not with headcount or operational complexity.

Operational expenses (Spells, Vest, Core Council Buffer, etc.) were approximately $67M — the actual cost of running the protocol. These have been declining as legacy overhead winds down (Spells dropped from ~$16M/quarter in Q1 2025 to ~$0.3M/quarter by Q4 2025).

This distinction matters when evaluating protocol efficiency: the savings rate is a competitive market cost, while operational expenses are the controllable overhead.

---

## Transition to Laniakea Accounting

The current monthly settlement and legacy exceptions will be replaced over time:

| Current State | Target State | Phase |
|--------------|-------------|-------|
| Monthly settlement | Daily settlement cycle | Phase 3 |
| Legacy core vaults | Core Controlled Agents under Prime management | Phase 1 |
| PSM managed by Sky Core | Grove-operated ASC asset | Phase 1–3 |
| Legacy RWA (bespoke deals) | Term Halos (Phase 1.5+) / Portfolio Halos (Phase 4+) | Phase 1.5–4+ |
| SBE fixed buyback | Dynamic burn rate via SBE BEAM | Phase 2+ |
| Manual revenue accounting | Automated beacon-operated settlement | Phase 9+ |

Until these transitions complete, the current accounting described here remains the operational reality.

---

## Connections

- Prime settlement calculation (5-step methodology): `prime-settlement-methodology.md`
- Genesis Capital and Aggregate Backstop Capital: `genesis-capital.md`
- TMF waterfall specification: `../whitepaper/appendix-c-treasury-management-function.md`
- ASC / PSM transition: `../risk-framework/asc.md`
- Core Controlled Agents: `../roadmap/phase1/phase-1-overview.md`
- Future daily settlement: `daily-settlement-cycle.md`
