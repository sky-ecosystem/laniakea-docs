# Actively Stabilizing Collateral (ASC)

**Last Updated:** 2026-01-27

ASC is the Asset Liability Management (ALM) requirement that each Prime must satisfy to keep USDS near $1 during downward peg pressure. Complementary to ASC, each Prime must also maintain a Demand Absorption Buffer (DAB) to provide sell-side liquidity during upward peg pressure.

This document is the Risk Framework’s operational view of ASC/DAB (definitions, qualification rules, enforcement, and how it replaces legacy PSM-centric liquidity over time).

## Definitions

### Prime Primebook Assets

A Prime’s **Primebook Assets** are the total capital it has deployed from Sky through the Allocation System Primitive, excluding any portion held in USDS.

### ASC (Actively Stabilizing Collateral)

Primes must maintain at least **5%** of their Primebook Assets in **Actively Stabilizing Collateral**.

ASC is the sum of:
- **Resting ASC** (immediate buy support near the peg)
- **Latent ASC** (convertible into resting ASC quickly)

### Resting ASC (immediate buy support)

Resting ASC must provide buy support at a price of at least **0.999 USD per USDS** (10 bps downside spread). To avoid “paper liquidity”: resting ASC must correspond to a **directly and atomically executable** bid/quote (onchain DEX position, live CEX orderbook order/quote) — or to a verifiable arrangement (including offchain market-making) that guarantees buy support within the allowed spread.

**Current calculation inputs (implementation snapshot):** USDC in LitePSM; USDC in PSM3 on Base/Arbitrum/Unichain/Optimism; cash stablecoins in Curve paired with USDS; USDC in GUNI pools (0.01%, 0.05%); cash stablecoins in Uniswap paired with USDS.

### Latent ASC (convertible within 15 minutes)

Latent ASC = cash stablecoins that don't qualify as resting but can be converted into resting ASC. To qualify: (1) verifiable onchain or through reputable APIs/oracles; (2) convertible into resting ASC within **15 minutes** under normal market conditions; (3) convert via a fully automated process that triggers when ASC falls below specified levels. **Cap:** ≤ **25%** of total ASC.

**Current calculation inputs (implementation snapshot):** cash stablecoins in Curve/Uniswap not paired with USDS; cash stablecoins in SparkLend, Aave, Morpho; cash stablecoins held in a Prime ALM Proxy.

## Demand Absorption Buffer (DAB)

Every Prime must maintain a **DAB equal to 25% of its required ASC**.

DAB is intended to stabilize USDS during periods of excess supply by providing **sell-side** liquidity. In current implementation language, DAB is “a subset of ASC” consisting of **USDS that is for sale for at most 1.001 USD per USDS**.

Qualifying forms may include:
- USDS or DAI in PSMs
- Autonomous systems that generate USDS dynamically through allocation as needed

## Peg Defense Events

### Trigger

A Peg Defense Event occurs when the average USDS price on LayerZero-connected DEXes falls below **0.999 USD per USDS**.

### Prime obligations

During a Peg Defense Event, each Prime must immediately begin buying USDS at a rate of at least:

`6.25% of its ASC requirement every 6 hours`

Peg defense can be performed through a combination of:
1. Selling other collateral for USDS, and/or
2. Using USDS (or newly generated USDS) as collateral to borrow other assets (e.g., USDC/USDT on Aave) and buy USDS.

## Enforcement and near-term posture

In the near term:
- Failures to maintain minimum ASC have **no explicit penalty**, but must be detected and reported (including into the settlement-cycle independent calculation).
- DAB and peg-defense penalty schedules are explicitly “to be specified” in future iterations.

Separately from penalties, ASC can be supported with **incentives**: eligible ASC can earn an incentive tied to the spread between Base Rate and Treasury Bill Rate (paid as part of the settlement cycle).

## ASC renting (ALM rental)

Each Prime has an ASC (and DAB/peg-defense) obligation proportional to the portion of the Sky Primebook Assets it deploys. To satisfy these obligations efficiently, Primes can trade ALM responsibilities with each other via **Asset Liability Management Rental**:

- **Renting out (being rented from):** you receive payment and take over another Prime’s ASC obligation (you hold “extra” ASC for them).
- **Renting in (renting from others):** you pay to have another Prime take over your ASC obligation (they hold ASC on your behalf).

When ALM obligations are rented, the associated obligations for **ASC, DAB, and Peg Defense Events are transferred together**.

## Transition away from the PSM

ASC is designed to become the primary liquidity-management layer, replacing Sky Core's legacy ALM mechanisms over time.

**Transitional state** (legacy still active): Sky Core manages and controls the PSM while ASC infrastructure is deployed. Control of the LitePSM is being transitioned to Grove; post-transition, Grove manages the LitePSM as an ASC asset under ALM rules.

### PSM as an ASC asset (Grove operations)

In the transition period the PSM functions as a large, simple ASC reservoir and backstop:
- Grove assumes operational/accounting ownership (Sky retains oversight until full ASC implementation).
- Grove pays the **Base Rate** on PSM assets; can use PSM to meet ASC requirements if no better alternatives exist.
- USDC in the PSM is uniquely capital-efficient for peg liquidity (no capital requirement vs alternative deployments).
- Grove can reduce/empty the PSM if better ASC options exist (Uniswap/Curve positions); usage can increase if ASC obligations rise materially.
- Protocol can support "ASC point" economics where other actors rent/offer ASC capacity (aligns with ALM renting).

**Target state** (Laniakea intent): ASC becomes the comprehensive ALM layer across Primes; the legacy PSM becomes an implementation detail of Grove's liquidity operations (potentially a Grove-owned Halo/Unit), not the protocol's primary peg mechanism.

## Where this fits in the Risk Framework

- **Parallel track to portfolio risk capital.** ASC/DAB constrain liquidity posture and peg-defense readiness; they are complementary to risk-capital requirements (CRR/RRC), not folded into them.
- **ASC-eligible holdings route to `ascbook`** — the Primebook sub-book whose product *is* immediate liquidity. Sub-book taxonomy in [`../roadstart/risk-framework.md`](../roadstart/risk-framework.md) "Sub-book taxonomy + coverage matrix". Eligibility prerequisites: deep peg-defense liquidity, < 15min convertibility.
- **Concentration and portfolio-risk controls** are a separate track from ASC — see [`../roadstart/risk-framework.md`](../roadstart/risk-framework.md) "Concentration framework". ASC determines "how fast can we buy" during peg defense, not how much capital buffers credit/market losses.

Derived from the Sky Atlas Stability Scope (ALM / ASC / DAB sections).
