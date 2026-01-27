# Appendix F: Glossary

Term definitions for the Sky Protocol.

---

## Core Concepts

| Term | Definition |
|------|------------|
| **Sky** | Evolution of MakerDAO; decentralized stablecoin protocol |
| **Sky Core** | Central governance and monetary policy layer |
| **Atlas** | Constitutional governance document; human-readable; ~10-20 pages |
| **Synome** | Machine-readable operational database; contains all parameters and configurations |

---

## Tokens

| Term | Definition |
|------|------------|
| **USDS** | Sky stablecoin; 1:1 with USD |
| **sUSDS** | Savings token; earns Sky Savings Rate |
| **SKY** | Governance token; staking rewards + buyback/burn |
| **stUSDS** | Segregated risk capital for SKY-backed borrowing |
| **DAI** | Legacy stablecoin; 1:1 convertible with USDS |
| **MKR** | Legacy governance token; 1:24000 convertible with SKY |

---

## Rates

| Term | Definition |
|------|------------|
| **SSR** | Sky Savings Rate — base yield for sUSDS holders |
| **Base Rate** | Protocol-wide stability fee |
| **Sky Borrow Rate** | Rate for borrowing USDS against SKY |
| **stUSDS Rate** | Yield for stUSDS holders (higher than SSR) |

---

## Stability

| Term | Definition |
|------|------------|
| **ALM** | Asset Liability Management — liquidity and portfolio rules that support the USDS peg |
| **ASC** | Actively Stabilizing Collateral — highly liquid non‑USDS assets used to buy USDS during downward peg pressure |
| **DAB** | Demand Absorption Buffer — highly liquid USDS (or USDS-equivalent) positions used to sell USDS during upward peg pressure |
| **LitePSM** | Lite Peg Stability Module — 1:1 USDC ↔ USDS conversion backstop used for peg stability |

---

## Treasury

| Term | Definition |
|------|------------|
| **TMF** | Treasury Management Function — the waterfall that allocates protocol net revenue to security/operations, buffers, burn, and staking rewards |
| **Smart Burn Engine** | Automated mechanism that executes SKY buybacks (and related actions) using TMF-allocated surplus |
| **Aggregate Backstop Capital** | Protocol solvency buffer for bad debt protection (targeted as a percentage of USDS liabilities) |
| **Fortification Conserver** | Treasury allocation for legal defense and unquantifiable risk management (often implemented via a designated foundation/entity) |
| **Net Revenue Ratio** | Scaling factor used in TMF allocations that increases with protocol net revenue (higher revenue increases allocations to certain steps like burn/fortification) |

---

## Agents

| Term | Definition |
|------|------------|
| **Agent** | Autonomous entity operating within Sky's framework |
| **Synomic Agent** | Durable, ledger-native entity that can own assets and make binding commitments; four types: Prime, Halo, Generator, Executor |
| **Prime** | Capital-deploying agent category; heavyweight. Two subtypes: Star Primes (5) and Institutional Primes (1) |
| **Star Prime** | Standard Prime operating under a Generator; 5 genesis Stars: Spark, Grove, Keel, Star4, Star5 |
| **Institutional Prime** | Prime serving institutional clients with higher compliance requirements; example: Obex |
| **Halo** | Lighter operational agent; wraps external value. Organized into Halo Classes containing Halo Units |
| **Halo Class** | Grouping of Halo Units sharing the same smart contract infrastructure (PAU, sentinel) and legal framework (buybox). Examples: tranched Passthrough Halo (senior/junior sharing one PAU), NFAT Facility (same buybox, varying duration/size) |
| **Halo Unit** | Individual instance within a Halo Class; specific parameters within the class's bounds (e.g., a specific tranche, a specific NFAT deal) |
| **Core Halos** | Legacy assets (Morpho vaults, Aave pools, SparkLend, etc.) standardized as Halo Units under Core Council governance. Primes deploy to Core Halos via CoreHaloFacet. Core Halos can transition to Prime ownership or wind down systematically |
| **Executor** | Governance operator agent; performs privileged operations |
| **Generator** | Layer interfacing with stablecoin ERC20 contract |
| **Generator Agent** | Agent that issues Sky Generated Assets (SGAs); future growth vector |

---

## Agent Components

| Term | Definition |
|------|------------|
| **SubProxy** | On-chain treasury controlled by an Agent |
| **Agent Artifact** | Governance documentation for an Agent |
| **Agent Token** | Native token for an Agent (10B supply, no emissions) |
| **Nested Contributors** | Core contributors serving both Agent and Sky |
| **Foundation** | Legal entity associated with a Prime |

---

## Risk Capital

| Term | Definition |
|------|------------|
| **JRC** | Junior Risk Capital — first to absorb losses |
| **SRC** | Senior Risk Capital — absorbs after JRC depleted |
| **IJRC** | Internal JRC — Prime's own capital |
| **EJRC** | External JRC — from other parties |
| **TEJRC** | Tokenized External JRC |
| **TISRC** | Tokenized Isolated SRC (per-Prime) |
| **srUSDS** | Senior Risk USDS — global senior risk capital |
| **Encumbrance Ratio** | Required Risk Capital / Total Risk Capital |
| **First Loss Capital (FLC)** | The first 10% of JRC losses, absorbed solely by Prime's own capital (IJRC) before external JRC shares losses |
| **Agent Token Inflation** | Loss absorption mechanism (step 3) where Prime token is inflated to cover losses after JRC exhaustion; can theoretically cover unlimited losses |
| **SKY Token Inflation** | Loss absorption mechanism (step 6) where SKY token is inflated to cover losses at protocol level after Global SRC exhaustion |
| **Genesis Capital** | Protocol reserves; loss absorption step 7 — haircut applied only after all risk capital and token inflation mechanisms exhausted |
| **Loss Absorption Waterfall** | 8-step sequence for absorbing losses: (1) FLC → (2) JRC → (3) Agent Token → (4) TISRC → (5) Global SRC → (6) SKY Token → (7) Genesis Capital → (8) Peg Adjustment |

---

## Infrastructure

| Term | Definition |
|------|------------|
| **PAU** | Parallelized Allocation Unit — standard building block (Controller + ALMProxy + RateLimits) |
| **BEAM** | Bounded External Access Module — authorized role with constraints |
| **pBEAM** | Process BEAM — directly impacts contracts |
| **cBEAM** | Configurator BEAM — modifies pBEAM guardrails |
| **aBEAM** | Admin BEAM — grants cBEAMs, creates inits |
| **Keeper** | LPHA (Low Power, High Authority) beacon for deterministic rule execution; applies rules exactly as written without judgment |
| **SORL** | Second-Order Rate Limit — constraint on rate limit increase speed |
| **Init** | Pre-approved configuration that GovOps can instantiate |
| **Configurator Unit** | Stack enabling spell-less Prime operations (BEAMTimeLock → BEAMState → Configurator) |
| **BEAMTimeLock** | Timelock component of Configurator Unit; enforces 14-day delay on additions, instant removals |
| **Buybox** | Defined parameter ranges for automated Halo operations (duration, size, APY, counterparties); deals within buybox execute without governance approval |
| **TTS** | Time to Shutdown — maximum time for a Sentinel to safely unwind positions during emergency |
| **Streaming Accord** | Agreement between Prime and Sentinel defining operational parameters, risk limits, and accountability |

---

## Settlement

| Term | Definition |
|------|------------|
| **LCTS** | Liquidity Constrained Token Standard — queue-based conversion |
| **Generation** | LCTS grouping; users in same generation share capacity proportionally |
| **Settlement Cycle** | Weekly: Tue lock → Wed settle (post-Laniakea) |
| **Settlement Lock Period** | Period when queue entries cannot be withdrawn. Weekly mode: 24h (Tue 12:00 → Wed 12:00 UTC). Weekday mode: 3h (12:00 → 15:00 UTC) |
| **OSRC Auction** | Sealed-bid auction for Senior Risk Capital capacity |
| **SPTP** | Stressed Pull-to-Par — time until asset converges to fundamental value under stress. Used for duration matching: assets are assigned to buckets based on SPTP, matched against liability duration capacity. Formula uses double exponential decay calibrated to empirical bank run data |
| **Prime Intent Vault** | Restricted trading sub-account for delegated Prime trading. Holds bounded working capital, enforces trading policy (allowed pairs, slippage limits, notional caps). Limits blast radius — only vault balance is exposed to settlement, not full Prime PAU |

---

## Governance

| Term | Definition |
|------|------------|
| **Governance Poll** | SKY holder decision-making; 3-day duration |
| **Executive Vote** | On-chain parameter changes |
| **Aligned Delegate** | Recognized governance participant; ranked L1-L3 |
| **Facilitator** | Interprets Atlas on behalf of Executors |
| **Root Edit** | Process for token holders to modify Agent Artifacts |
| **Core Council** | Group of Executors responsible for Sky Core operations |

---

## Beacon Framework

| Term | Definition |
|------|------------|
| **Beacon** | Synome-registered action aperture through which an agent affects the external world; the parent concept for all autonomous systems |
| **LPLA** | Low Power, Low Authority beacon — simple reporting, data exposure, basic coordination |
| **LPHA** | Low Power, High Authority beacon — deterministic rule execution on behalf of Synomic Agents (e.g., lpha-auction) |
| **HPLA** | High Power, Low Authority beacon — sophisticated peer-to-peer interaction with private capital |
| **HPHA** | High Power, High Authority beacon — governance execution with real-time capability; includes Sentinels |
| **Sentinel** | Distinguished subclass of HPHA beacons forming coordinated Baseline/Stream/Warden formations; specifically the trading and execution layer that deploys capital in live markets |
| **stl-* (prefix)** | Sentinel interface specification |
| **stk-* (prefix)** | Sentinel toolkit operation |
| **lpla-* (prefix)** | LPLA (Low Power, Low Authority) reporting/monitoring beacon |
| **lpha-* (prefix)** | LPHA (Low Power, High Authority) keeper beacon |
| **hpha-* (prefix)** | HPHA (High Power, High Authority) governance beacon |
| **stl-base** | Baseline sentinel — primary execution for formations (long-term) |
| **stl-stream** | Stream sentinel — proprietary intelligence streaming (long-term) |
| **stl-warden** | Warden sentinel — independent safety oversight (long-term) |
| **lpha-lcts** | LPHA beacon for Passthrough Halo LCTS operations — deposits, redemptions, capacity management |
| **lpha-nfat** | LPHA beacon for Structuring Halo NFAT operations — queue sweeping, NFAT issuance, redemption funding |
| **lpha-auction** | OSRC auction matching and capacity allocation |
| **lpha-exchange** | Exchange Halo orderbook and matching engine |
| **lpha-identity** | Identity Network registry keeper |
| **hpha-gov** | High-authority governance execution |
| **Synome** | Decentralized database for operational data |
| **CC Synome** | Core Council Synome — authoritative source |

---

## Risk Framework

| Term | Definition |
|------|------------|
| **GRF (deprecated)** | Former monolithic "General Risk Framework"; replaced by the modular Risk Framework docs in `risk-framework/` |
| **SPTP Bucket** | Time bucket for liability matching (0.5 months each) |
| **Lindy-Based Demand** | Liability duration estimation based on current age |
| **Risk Weight** | Capital for fundamental risk (credit, smart contract) |
| **FRTB Drawdown** | Capital for full mark-to-market drawdown |
| **Gap Risk** | Risk from discrete price jumps that bypass stop-losses; relevant for collateralized lending liquidations |
| **FRTB** | Fundamental Review of the Trading Book — Basel framework for market risk capital; Sky adapts FRTB principles for crypto asset valuation |
| **Ingression Rate** | Speed at which new risk capital can be deployed; constrained by SORL and governance limits |

---

## Multi-Chain

| Term | Definition |
|------|------------|
| **SkyLink** | Multi-chain token bridging infrastructure |
| **Foreign Prime** | Prime equivalent on altchains |
| **Foreign Halo** | Halo equivalent on altchains |
| **CCTP** | Circle Cross-Chain Transfer Protocol |

---

## Legacy

| Term | Definition |
|------|------------|
| **MakerDAO** | Original protocol; evolved into Sky |
| **Vault** | Original collateralized debt position |
| **DSR** | DAI Savings Rate; predecessor to SSR |
| **PSM** | Peg Stability Module |
