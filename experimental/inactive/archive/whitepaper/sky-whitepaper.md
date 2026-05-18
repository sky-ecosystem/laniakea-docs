# Sky Ecosystem Whitepaper

**Version:** 2.0 (Draft)
**Date:** December 2025

---

## Part 1: What is Sky Ecosystem

Sky Ecosystem powers USDS, a large decentralized yield-generating stablecoin. Sky Ecosystem is community-governed through the SKY token, with no single entity unilaterally controlling the Sky Protocol infrastructure.

### Scale and Performance

As of December 2025 (approximate snapshot; subject to change):

| Metric | Value |
|--------|-------|
| USDS Supply | ~$9.9 billion |
| Annualized Protocol Revenue | ~$435 million |
| Annualized Protocol Profits | ~$168 million |
| SKY Buybacks (2025 YTD) | ~$92 million |

Sky Ecosystem's USDS supply grew significantly in 2025 (often cited at ~86%), outpacing overall stablecoin market growth in the same period (often cited at ~50%). This growth occurred while Sky Ecosystem remained among the highest-earning protocols in decentralized finance.

The broader opportunity: over $300 billion in stablecoins currently sit idle without earning yield — capital that naturally seeks returns.

### How Sky Ecosystem Generates Revenue

Sky Ecosystem generates revenue through the spread between what it earns on deployed capital (the "base rate") and what it pays to sUSDS holders (the "savings rate"). The difference constitutes net protocol revenue.

Revenue is generated through Sky Protocol from a diversified set of sources:

- **Collateralized lending** — Users deposit crypto assets as collateral to borrow USDS
- **Digital asset-backed lending** — Lending against high-quality crypto collateral (BTC, ETH)
- **U.S. Treasuries** — Low-risk yield from tokenized government securities
- **Private credit** — CLO allocations and other credit strategies
- **Delta-neutral strategies** — Market-neutral yield generation

This diversification can reduce reliance on any single market regime, and has historically helped dampen sensitivity to crypto price cycles relative to single-source protocols.

### Decentralization

Sky Ecosystem operates as a decentralized, community-driven system. The Sky Protocol consists of smart contracts deployed on Ethereum and other blockchains, governed by SKY token holders through on-chain voting.

Key decentralization properties:

- No single entity controls Sky Protocol
- All protocol parameters are set through decentralized governance
- Smart contracts execute automatically according to their programmed logic
- The protocol continues operating regardless of any single participant

USDS is a decentralized yield-generating stablecoin focused on capital formation — distinct from payment stablecoins regulated under frameworks like the GENIUS Act.

---

## Part 2: History and Track Record

Sky Ecosystem evolved from MakerDAO, which launched in 2017 and created DAI — the first decentralized stablecoin to achieve significant scale. Over eight years, the protocol has demonstrated continuous operation through multiple market cycles, including the 2018 bear market, the March 2020 crash (ETH dropped over 50% in 24 hours), and the 2022 crypto winter.

### Key Milestones

| Year | Milestone |
|------|-----------|
| 2017 | MakerDAO launches single-collateral DAI |
| 2019 | Multi-Collateral DAI enables diverse collateral types |
| 2020 | DAI Savings Rate introduced; protocol survives March crash |
| 2021 | Real-world asset integration begins |
| 2023 | Endgame initiative announced; Agent framework conceived |
| 2024 | Rebrand to Sky Ecosystem; USDS and SKY tokens launch |
| 2025 | Four Synomic Agents deployed; SKY buyback mechanism activated |

The 2024-2025 transition from MakerDAO to Sky Ecosystem included a complete rebrand and technical migration. DAI remains operational and is convertible 1:1 with USDS. MKR is convertible to SKY at a ratio of 1:24,000.

Sky Ecosystem's eight-year track record of uninterrupted operation provides a foundation of technical credibility that newer protocols cannot match.

---

## Part 3: Token System

Sky Ecosystem's token system consists of three primary tokens, each serving a distinct function within the protocol.

### USDS: The Stablecoin

USDS is Sky Ecosystem's primary stablecoin, maintaining a 1:1 peg to the US dollar. USDS is minted when users deposit collateral into Sky Protocol and can be redeemed by repaying the borrowed amount.

| Property | Description |
|----------|-------------|
| Peg | 1:1 USD |
| Supply | $9.86 billion |
| Backing | Overcollateralized by crypto assets, Treasuries, and credit positions |
| Availability | Ethereum mainnet + multiple L2s and L1s via SkyLink |

USDS is freely transferable, composable with other DeFi protocols, and convertible 1:1 with DAI. Unlike payment stablecoins, USDS is designed for capital formation and yield generation rather than transaction settlement.

### sUSDS: The Savings Token

sUSDS (Savings USDS) is an ERC-4626 vault token representing a deposit in the Sky Savings system. Holders of sUSDS automatically earn the Sky Savings Rate without any active management.

| Property | Description |
|----------|-------------|
| Standard | ERC-4626 vault |
| Yield mechanism | Exchange rate increases continuously at Sky Savings Rate |
| Lock-up | None — freely redeemable at any time |
| Multi-chain | Earns yield on all supported chains via SkyLink |

When users deposit USDS into the savings contract, they receive sUSDS tokens. The exchange rate between sUSDS and USDS increases over time as yield accrues. To withdraw, users simply redeem sUSDS for the increased amount of USDS.

### SKY: The Governance Token

Sky Protocol is community-governed through use of the SKY token. Holders who stake SKY actively participate in securing and directing the protocol.

The system is designed so that staked SKY provides three core functions:

**1. Governance Participation**

The ability to contribute to decentralized governance of all protocol parameters, risk controls, capital allocation, and the multi-billion-dollar treasury. SKY holders vote on executive proposals that modify protocol parameters, modify the risk frameworks, and change Alignment Conservers — trusted entities that facilitate and protect the governance process, ensuring decisions serve the long-term health of the ecosystem.

**2. Programmatic Profit Allocation**

Under current protocol parameters, as determined through decentralized governance, approximately 75-100% of protocol profits are allocated to stakers of the SKY token through programmatic, open-market buybacks that are redistributed as additional yield to staked SKY.

The SKY buyback and staking rewards mechanism uses protocol profits to repurchase SKY tokens on the open market. Since launching in February 2025, this mechanism has repurchased over $92.2 million in SKY — representing over 6.3% of the total 23.46 billion token supply.

**3. Collateral Utility**

The ability to use governance-participating (staked) SKY as collateral for borrowing USDS while continuing to earn staking rewards, effectively lowering borrowing costs without sacrificing governance participation or yield.

### Supply Dynamics

SKY has a fixed maximum supply with deflationary mechanisms:

| Property                  | Value                                          |
| ------------------------- | ---------------------------------------------- |
| Total Supply Cap          | 23.46 billion SKY                              |
| Emissions                 | Permanently disabled                           |
| Buyback Rate (Annualized) | ~$102 million                                  |
| Unclaimed MKR Burn        | 1% quarterly burn of SKY backing unclaimed MKR |

Approximately 14% of the original MKR supply remains unclaimed after migration. Through quarterly redemption-and-burn, all SKY tokens backing unclaimed MKR will be burned over approximately 24 years.

### Growth Staking

Growth Staking links staking rewards to holding growth assets — governance tokens of Synomic Agents such as Primes and Halos — through a folio structure. Stakers who hold a portfolio of growth assets alongside their staked SKY receive enhanced staking rewards, with the reward multiplier determined by the composition and value of growth assets in the folio. This creates a natural demand loop for agent tokens while incentivizing long-term ecosystem alignment. See `sky-agents/folio-agents/agent-type-folios.md` and `growth-staking/growth-staking.md` for the full mechanism.

---

## Part 4: How the Protocol Works

Sky Protocol is the decentralized infrastructure powering Sky Ecosystem — a set of smart contracts and on-chain mechanisms that manage stablecoin issuance, collateral, capital deployment, and profit allocation.

### Revenue Generation

Sky Protocol generates revenue from capital deployed through the Agent network. The protocol earns the "base rate" on deployed capital while paying the "savings rate" to sUSDS holders. Net protocol revenue equals:

```
Net Revenue = (Base Rate × Deployed Capital) - (Savings Rate × sUSDS Deposits)
```

Revenue sources are managed by Synomic Agents (see Part 5), each specializing in different asset classes and strategies. This diversification enables Sky Ecosystem to maintain yield across varying market conditions.

### Treasury Management Function (TMF)

The Sky TMF is a sequential waterfall that distributes all protocol net revenue through five steps. Each step calculates its allocation based on what remains after the previous step.

| Step                              | Allocation                              | Purpose                                        |
| --------------------------------- | --------------------------------------- | ---------------------------------------------- |
| **1. Security & Maintenance**     | 21% (Genesis) / 4-10% (Post-Genesis)    | Core teams, security, risk management          |
| **2. Aggregate Backstop Capital** | Variable (target: 1.5% of total USDS supply) | Solvency buffer for bad debt protection        |
| **3. Fortification Conserver**    | 20% × Net Revenue Ratio                 | Legal defense, resilience, unquantifiable risk |
| **4. Smart Burn Engine**          | 20% × Net Revenue Ratio                 | SKY buybacks                                   |
| **5. Staking Rewards**            | 100% of remainder                       | Distributed to SKY stakers                     |

**Net Revenue Ratio:** A hyperbolic function that scales allocations based on total protocol net revenue. At low revenue, most surplus flows to staking rewards. As revenue grows, more flows to burn and fortification. The formula approaches 1.0 as revenue approaches the cap threshold.

**Aggregate Backstop Capital:** Fills dynamically based on how far the buffer is from its target. When empty, up to 50% of available funds flow to the buffer (at maximum Net Revenue Ratio; the effective rate scales with the Net Revenue Ratio). When full, the step is skipped entirely.

**Fortification Conserver:** An Alignment Conserver responsible for legal defense and resilience. Allocation grows with net revenue because larger scale requires greater legal infrastructure.

### The Smart Burn Engine

The Smart Burn Engine executes SKY buybacks using protocol surplus allocated by the TMF. Key properties:

- **Programmatic execution** — Operates automatically based on protocol parameters
- **Scaling allocation** — Receives larger share as protocol revenue grows
- **Transparent** — All transactions visible on-chain

Purchased SKY is distributed to stakers as additional yield, though allocation parameters are subject to change through decentralized governance.

### Peg Stability

USDS maintains its dollar peg through multiple layers:

| Mechanism | Function |
|-----------|----------|
| **LitePSM (current)** | 1:1 USDC ↔ USDS conversion backstop |
| **ALM liquidity (ASC/DAB, evolving)** | Prime-held liquidity requirements for buy-side (ASC) and sell-side (DAB) support near the peg |
| **Overcollateralization** | All USDS backed by >100% collateral value |
| **Liquidation system** | Underwater positions automatically liquidated |
| **Oracle system** | Price feeds from decentralized oracle networks |

Today, LitePSM (Lite Peg Stability Module) provides a simple onchain conversion backstop that enables arbitrage to keep USDS tightly anchored.

Over time, Sky's Asset Liability Management framework shifts more of peg liquidity into the Prime layer through requirements like Actively Stabilizing Collateral (ASC) and the Demand Absorption Buffer (DAB). This approach is more efficient than a centralized module: Primes can hold yield-generating assets that convert to liquidity when needed, earning returns in normal times while still providing peg support. It also places liquidity where users actually are — including on L2s and other chains — and can earn spreads on conversions rather than leaving capital idle. This turns peg defense into a system-wide obligation that can be dynamically managed rather than relying primarily on a single legacy module.

---

## Part 5: The Agent Network

Synomic Agents are operationally autonomous systems within Sky Ecosystem that plug into the decentralized Sky Protocol primitives. (Operational autonomy means each agent's own synomic artifacts — its constitution, directives, and encoded rules — shape the teleonome activity that drives it; the agent's institutional purpose is executed according to its own governance surface, not external direction.) These Agents compete to deliver the highest risk-adjusted returns while efficiently sharing the economies of scale of the entire ecosystem.

### Agent Structure

The Agent network operates as a capital allocation layer between Sky Protocol and end investments:

```
Sky Protocol → Synomic Agents (Primes) → Investment Products (Halos) → End Assets
```

**Primes** are the primary capital deployers — governance-approved operators that receive capital from Sky Protocol and deploy it into various strategies. Each Prime operates with its own treasury, governance token, and specialized focus.

**Halos** are investment product wrappers created by Primes. Each Halo wraps a specific strategy or asset class, providing standardized interfaces for capital deployment and risk management. Halos are organized into **Halo Classes** (shared smart contract and legal infrastructure) containing **Halo Units** (individual products with specific parameters).

There are three primary Halo Class types for standard Halos:

| Type | Token Standard | Use Case |
|------|----------------|----------|
| **Portfolio Halo** | LCTS (pooled, fungible) | Standardized products with uniform terms — all participants share the same conditions |
| **Term Halo** | NFAT (individual, non-fungible) | Bespoke deals with negotiated terms — each position can have different duration, size, and yield |
| **Trading Halo** | AMM (programmatic counterparty) | Instant liquidity for RWA tokens and ecosystem assets via automated market making |

**Portfolio Halos** use the Liquidity Constrained Token Standard (LCTS) for queue-based entry and exit. Participants deposit to a queue, and at daily settlement (16:00 UTC), deposits convert to Halo Unit shares at the current exchange rate. The queue locks during the processing window (13:00 → 16:00 UTC) to ensure deterministic calculations and fair proportional allocation. If conversion capacity is constrained, the generation may span multiple settlement cycles — see `smart-contracts/lcts.md`.

**Term Halos** use Non-Fungible Allocation Tokens (NFATs) to represent individual deals. Each NFAT is a distinct position with its own terms negotiated within a defined "buybox" (acceptable parameter ranges). NFATs are transferable and can be used as collateral, enabling secondary markets for structured positions. NFATs can also be wrapped in fungible ERC-20 tokens for broader secondary market access. Entry uses a share-based queue: depositors receive queue shares proportional to their contribution, and conversion to NFAT positions occurs when the Halo selectively claims from the queue (no lock period or batch settlement — see `smart-contracts/nfats.md`). For example, a Term Halo might issue 6-month, 12-month, and 18-month NFATs with different yields, all within the same legal framework.

**Trading Halos** operate AMM smart contracts using predeposited USDS to provide instant liquidity for assets already onboarded onto the Configurator. Users can sell RWA tokens for instant USDS at a spread; the Trading Halo redeems the underlying with the issuer over the normal settlement cycle. See `sky-agents/halo-agents/trading-halo.md`.

In addition to standard Halos, **Special Halos** have additional regulatory or operational requirements:

| Type | Purpose |
|------|---------|
| **Identity Network Halo** | Operates identity verification infrastructure (KYC registries) |
| **Exchange Halo** | Operates intent-based exchange infrastructure (orderbooks, matching engines) |

**Folio Agents** are distinct from Halos — they are rank 3 standardized supply-side holding structures. Each folio has a **principal** (the end user) who controls the folio through a **directive** (human language instructions). The key structural difference from Halos: a Halo wraps around a legal entity (Halo is the outer shell), while a folio is controlled BY the principal through legal entities (the principal's legal structure is the governance surface). Folios can be operated in two modes: **automated** (sentinel formation via guardian accord, same protection as Primes) or **principal control** (principal sentinel, direct operation by the owner). Folio Agents are tokenless, single-owner, and instantly created (via automatic Guardian Accord). Folios are also the required vehicle for Growth Staking participation, holding both staked SKY and growth assets within their PAU (see Part 3). See `sky-agents/folio-agents/agent-type-folios.md`.

This structure separates risk-taking from monetary policy: Sky Core sets parameters and constraints, while Primes compete to deploy capital efficiently within those bounds. Primes bear the business risk — providing their own capital as first-loss protection on the assets they deploy — freeing core governance from day-to-day investment decisions.

### Current Synomic Agents

Sky has 5 Star Prime slots defined (Spark, Grove, Keel, Star4, Star5), with 3 currently operational, plus 1 Institutional Prime (Obex). Star4 and Star5 are reserved for future expansion.

**Star Primes (3 operational):**

| Agent | Focus | Products |
|-------|-------|----------|
| **Spark** | DeFi lending | SparkLend, Spark Liquidity Layer (6 chains), Spark Savings |
| **Grove** | Private credit | CLO allocations, RWA strategies |
| **Keel** | Ecosystem expansion | Solana deployment, USDS adoption initiatives |

**Institutional Primes:**

| Agent | Focus | Products |
|-------|-------|----------|
| **Obex** | Incubation | New Prime and Halo development |

Each Agent is competitively incentivized to maximize risk-adjusted returns and drive USDS issuance.

### Core Controlled Agents

In addition to Primes creating new Halos, Sky maintains **Core Controlled Agents** — rank 1 agents directly administered by the Core Council. In the short term, Core Controlled Agents manage legacy protocol positions (Morpho vaults, Aave pools, SparkLend exposures, etc.) that were previously described as "Core Halos." In the long term, they serve as general-purpose Core Council operational vehicles.

Core Controlled Agents are tokenless and governed via artifacts maintained by Core Council. This provides a path for legacy assets to either:
- Transition to Prime ownership when a suitable Prime is identified
- Wind down systematically if no longer strategically aligned

See `sky-agents/core-controlled-agents/agent-type-core-controlled.md`.

### Recovery Agents

**Recovery Agents** are rank 1 crisis agents administered by the Core Council. They are activated when a Guardian collapses or is implicated in misconduct — taking over the affected agent tree (Primes, Halos, risk capital) and managing liquidation, restructuring, or wind-down. Recovery Agents are temporary and dissolve after resolution. See `sky-agents/recovery-agents/agent-type-recovery.md`.

### Agent Rank Hierarchy

Agents are organized into four ranks:

| Rank | Agent Types | Governance Relationship |
|------|-------------|------------------------|
| **0** | Core Council | Sovereign |
| **1** | Guardians, Core Controlled Agents, Recovery Agents | Directly regulated by Core Council |
| **2** | Primes, Generators | Accordant to a Guardian |
| **3** | Halos, Folio Agents | Administered by a Prime |

See `sky-agents/README.md` for the complete hierarchy and agent type specifications.

### How Agents Compete

Synomic Agents compete for capital allocation based on performance. The Agent with the best risk-adjusted returns receives more capital, creating market pressure for optimization. This competitive dynamic benefits Sky Ecosystem through:

- **Higher yields** — Agents optimize strategies to attract capital
- **Risk specialization** — Each Agent focuses on their area of expertise
- **Innovation** — New strategies and products emerge from competition
- **Efficiency** — Shared infrastructure reduces costs across all Agents

### Adding New Agents

New Synomic Agents are added through decentralized governance. The approval process includes evaluation of the Agent's strategy, team, risk framework, and operational infrastructure. Once approved, new Agents can immediately access capital from Sky Protocol within their governance-approved limits.

For the complete list of Agent Framework primitives and technical specifications, see Appendix B.

---

## Part 6: Risk Management

Sky Ecosystem employs risk management methods adapted from traditional finance, using frameworks informed by banking regulation while designed for decentralized operation. The core principle: capital requirements reflect the maximum loss that could actually be forced to realize, not mark-to-market volatility. By measuring liability duration (how long USDS holders tend to stay), Sky can effectively and securely hold longer-duration assets while maintaining appropriate buffers.

### Two-Tier Capital Structure

Risk capital in Sky Ecosystem is organized into two tiers with distinct risk/reward profiles:

| Tier | Name | Absorbs Losses | Compensation |
|------|------|----------------|--------------|
| **Junior** | JRC (Junior Risk Capital) | First | Higher yield |
| **Senior** | SRC (Senior Risk Capital) | Second | Lower yield, lower risk |

Junior Risk Capital providers take first-loss position in exchange for higher returns. Senior Risk Capital providers are protected by the JRC buffer and accept lower returns for reduced risk.

This structure operates at the Prime level: each Prime provides its own Junior Risk Capital from its treasury, taking first-loss position on the assets it deploys. Primes can also raise additional JRC from external parties and originate Senior Risk Capital from a global pool. This makes Primes directly accountable for their investment decisions — they lose their own capital first if things go wrong.

The capital structure has two distinct user-facing surfaces. On the **demand side**, sUSDS gives passive holders a single token that earns the savings rate with no deployment decisions. On the **supply side**, folios give active participants a governed PAU for direct capital deployment within the Laniakea stack — each folio operates under the same rate-limit and risk-capital infrastructure as Primes and Halos, but is controlled by (or on behalf of) a single principal. Together, sUSDS and folios complete the user layer: one abstracts away all allocation complexity, the other exposes it for sophisticated participants who want direct agency over their capital.

### Loss Absorption Waterfall

If losses occur, they are absorbed in a defined sequence across three tiers:

```
PRIME-LEVEL (per-Prime):
  1. First Loss Capital (10% of total JRC, from IJRC) ← Prime's own capital first
  2. Remaining JRC (IJRC + EJRC pro-rata)              ← All junior capital
  3. Agent Token Inflation                             ← Dilute Prime token holders

SYSTEM-LEVEL (shared):
  4. SRC Pool (TISRC + Global SRC, pari passu)         ← All senior risk capital
  5. SKY Token Inflation                               ← Dilute protocol token holders

NUCLEAR OPTIONS (protocol-level):
  6. Genesis Capital Haircut                           ← Protocol reserves
  7. USDS Peg Adjustment                               ← Final backstop
```

The First Loss Capital requirement ensures Primes have direct skin in the game — they absorb the first 10% of total JRC losses from their own capital before external junior capital shares in subsequent losses. Agent Token inflation can cover losses "to infinity" before touching senior capital. If Prime-level mechanisms are exhausted, the insolvent Prime's TISRC merges into the Global SRC pool and losses are shared pari passu across all SRC holders (Sky charges a fee on TISRC yield for this protection). Genesis Capital and peg adjustment are nuclear options that should never be reached under normal conditions.

### Encumbrance Monitoring

Sky Ecosystem continuously monitors the ratio of required risk capital to total risk capital available:

```
Encumbrance Ratio = Required Risk Capital / Total Risk Capital
```

The target encumbrance ratio is ≤90%, providing a 10% buffer above minimum requirements. Agents exceeding this threshold face restrictions until they restore compliance; the specific penalty schedule will be defined in a future governance proposal.

### Duration Matching

Sky tracks USDS lot ages to estimate how long holders will actually stay, using the Lindy Duration Model: the longer someone has held, the longer they're likely to continue holding. This liability duration data determines capacity in Duration Buckets, which are matched against asset durations measured by Stressed Pull-to-Par (SPTP) — the time until an asset converges to its fundamental value under stress conditions. This Asset-Liability Duration Matching (ALDM) system enables capital-efficient deployment of long-duration assets.

The risk framework matches asset characteristics to liability profiles: assets with longer time-to-liquidity require backing from longer-duration liabilities. When an asset's duration matches available liability capacity, it only needs capital for fundamental risk (credit default, smart contract failure, counterparty failure, and regulatory seizure). Unmatched assets must hold additional capital covering potential mark-to-market losses from credit spread widening — temporary price drops that recover as spreads normalize.

Laniakea extends this framework with explicit rate hedging requirements: since duration matching protects against mean-reverting credit spread movements but not permanent interest rate shifts, all fixed-rate exposure must be hedged or carry additional capital (see `risk-framework/matching.md` for the full rate risk vs credit spread risk analysis and rate hedging requirements).

### Concentration Limits

Beyond per-position capital requirements, Sky enforces **category caps** — governance-defined concentration limits for correlated risk types (e.g., "CLOs," "real estate," "US-based assets"). Any exposure exceeding a category cap is subject to 100% CRR (fully capitalized, no leverage). This prevents the system from concentrating into a single correlated risk type even when sufficient risk capital exists. Category caps are calibrated using scenario stress analysis and updated through governance.

### Operational Risk Capital

In addition to market and credit risk capital, Sky requires Operational Risk Capital (ORC) — an independent, additive capital charge sized by the formula Rate Limit × TTS (Time to Shutdown, determined by warden count). Warden economics and guardian-posted capital are separate operational requirements that complement the ORC formula but are not part of the sizing calculation itself. ORC ensures that capital adequacy reflects not just asset risk but the operational infrastructure required to manage it. See `risk-framework/operational-risk-capital.md`.

### Risk Capital Ingression

Not all external risk capital counts at face value. The ingression system determines how much "effective" capital a Prime can recognize based on capital quality — measured by whether the capital provider is synomic (framework-encoded, auditable), how long the capital is committed, and the Prime's existing capital composition.

Each capital layer has an ingression curve: external JRC is discounted relative to the Prime's own internal JRC, and SRC is discounted relative to the Prime's effective JRC base. A Prime token market cap constraint further limits total leverage, ensuring capital credibility is tied to genuine market validation of the Prime. This creates natural incentives: Primes that build their own capital base first, attract higher-quality capital providers, and maintain healthy token metrics can deploy more capital per unit of risk.

The ingression rate is a measure of leverage capacity — how much external capital effectively counts for capital adequacy purposes. The loss absorption waterfall, by contrast, uses nominal capital: if a Prime has $100M of nominal EJRC, the full $100M absorbs losses regardless of its ingression-adjusted effective value.

### Independent Assessment

Sky Ecosystem’s risk framework design is intended to be independently analyzable and auditable by third parties. Risk parameters are continuously monitored and adjusted through decentralized governance based on market conditions and portfolio composition.

---

## Part 7: Protocol Upgrades

Sky Ecosystem is implementing the Laniakea upgrade, a significant expansion of protocol capabilities enabling automated settlement at scale, unified risk management, and rapid deployment of new investment products.

### Implementation Phases

Laniakea is deployed incrementally:

| Stage | Phases | Core Deliverable | Settlement |
|-------|--------|------------------|------------|
| **Foundation** | 0–4 | Beacons, Synome-MVP, Term Halos, daily settlement, LCTS launch (srUSDS) | Monthly → Daily |
| **Factories** | 5–8 | Halo Factory, Generator PAU, Prime Factory, Generator Factory | Daily |
| **Automation** | 9–10 | Sentinel Base + Warden, auction activation, Stream formation | Daily |

The Foundation stage establishes core infrastructure using low-power beacons (deterministic programs), progressing from manual monthly settlement through formalized monthly (Phase 2) to daily settlement (Phase 3) and LCTS launch (Phase 4). The Factories stage builds automated deployment systems for all agent types. The Automation stage introduces high-power Sentinels (AI-capable formations) with sealed-bid auction-based allocation.

### Beacon Infrastructure

Laniakea introduces a beacon framework for autonomous operations. Beacons are classified by two axes:

| | Low Authority | High Authority |
|---|---|---|
| **Low Power** | LPLA (reporting) | LPHA (rule execution) |
| **High Power** | HPLA (trading) | HPHA (Sentinels) |

Phase 1 deploys LPLA and LPHA beacons — deterministic programs that execute predefined rules. Later phases introduce HPHA Sentinels — AI-capable formations with Baseline (execution), Stream (intelligence), and Warden (safety) components. A fourth sentinel type, the **principal sentinel** (`stl-principal`), provides owner-operated direct control of folio agents and standalone accounts outside the formation pattern (see Folio Agents in Part 5).

Sentinel operators are compensated through **carry** — private profit earned from outperformance above the required base returns. Stream Sentinels generate alpha by deploying proprietary intelligence through the public Baseline; carry equals the difference between actual returns and what the base strategy would have produced, multiplied by the negotiated performance fee ratio. This carry model is what makes sentinel operation economically viable and creates competition for operational quality — operators invest in better intelligence infrastructure because superior performance compounds into greater carry.

### Diamond PAU

The current Legacy PAU architecture (Controller + ALMProxy + RateLimits) will be replaced by the Diamond PAU pattern, which uses EIP-2535 diamond proxy architecture for modular, upgradeable functionality. PAU permissions are governed by the Configurator Unit (BEAMTimeLock, BEAMState, Configurator) — see `smart-contracts/configurator-unit.md`. Diamond PAUs enable:

- Modular action facets that can be added without full redeployment
- Foundation for standardized factory deployment (Phases 5–8)
- Unified interface across all agent types

In Phase 6, the Generator PAU replaces the multiple per-Prime MCD ilks with a single Generator ilk, using ERC-4626 vault relationships between the Generator and each Prime. This simplifies the USDS minting interface and depends on the Diamond PAU and factory patterns from Phases 5–6.

### Daily Settlement Cycle

Full Laniakea introduces a daily settlement cycle replacing the monthly cadence:

| Period | Timing | Function |
|--------|--------|----------|
| Active Window | 16:00 → 13:00 | Data collection, allocation submission (bids once `stl-base` is live) |
| Processing (Lock) | 13:00 → 16:00 | Calculations, verification |
| Settlement | 16:00 | All changes take effect |

Daily settlement enables faster capital reallocation, more responsive risk management, and tighter feedback loops between Agent performance and capital allocation. In early phases, allocations are governance-directed (pre-auction); once Prime-side `stl-base` is deployed, each cycle can include sealed-bid auctions where Primes compete for senior risk capital capacity and duration-matching reservations.

### Automated Operations

The upgrade introduces automated operational infrastructure:

- **Automated risk capital verification** — Continuous monitoring without manual intervention
- **Programmatic settlement** — Calculations and distributions execute automatically
- **Rate-limited capital flows** — All movements bounded by governance-set limits

This automation reduces operational overhead while maintaining governance control over parameters and limits.

### Five-Layer Synome Architecture

The Synome's long-term design is a five-layer containment hierarchy that progresses from data storage through autonomous execution. Layer 1 (Synome) holds the Atlas, canonical knowledge, and governance axioms. Layer 2 (Synomic Agents) contains the institutional entities — Primes, Halos, Generators, and Guardians — operated through Agent Directives. Layer 3 (Teleonomes) introduces private, goal-directed AI systems that operate Synomic Agents through regulated beacon apertures. Layer 4 (Embodiment) encompasses the physical infrastructure — compute, storage, network, and cryptographic keys. Layer 5 (Embodied Agent) represents fully running agents with real-time execution capabilities. Each layer contains the layers below it; intelligence lives privately at Layers 3-5 and enters the world only through regulated apertures registered at Layer 2. See Appendix A for the full five-layer specification.

### SpellGuard System

Post-transition, spell governance moves from direct SKY token Executive Votes to a layered SpellGuard model:

| Layer | Mechanism | Token Hat | Safety Valve |
|-------|-----------|-----------|-------------|
| **SpellCore** | Core Council Guardian vote (16/24 hat) | Guardian tokens | SKY holders: graduated freeze → override (Council dismissal) |
| **Prime SpellGuard** | Core spell payload + Prime token vote | Prime tokens | Prime token holders: freeze / cancel |
| **Halo SpellGuard** | Prime spell payload + Halo token vote | Halo tokens | Halo token holders: freeze / cancel |

Each level requires **dual-key authorization** — both a top-down payload from the layer above and a bottom-up token hat from the level's own token holders. SKY holders retain ultimate sovereignty: a full quorum override dismisses the Core Council and reverts to direct SKY holder control. See `governance-transition/spellguard-system.md` for full details.

### Expanded Agent Capabilities

Laniakea provides new capabilities for Synomic Agents:

| Capability | Description |
|------------|-------------|
| Factory-deployed products (Phase 5+) | Standardized Halo creation with reduced setup time |
| Unified risk framework | Consistent capital requirements across all asset types |
| Auction-based allocation | Market-driven distribution of scarce resources |
| Enhanced monitoring | Real-time visibility into Agent operations |

These capabilities allow Sky Ecosystem to onboard new asset classes and strategies more rapidly while maintaining consistent risk standards.

### Trading Infrastructure

Laniakea introduces Sky Intents, an intent-based trading system for Sky Ecosystem assets:

| Component | Function |
|-----------|----------|
| **Sky Intents** | Users express trading intent; matching occurs off-chain; settlement on-chain |
| **Exchange Halos** | Special Halos operating orderbooks and matching engines for specific markets |
| **Trading Halos** | Standard Halos providing instant AMM-based liquidity for RWA tokens and ecosystem assets |
| **LPHA Beacons** | Low Power, High Authority beacons executing deterministic rules (`lpha-exchange` for orderbooks, `lpha-amm` for AMMs) |

Sky Intents separates intent expression from execution: users submit what they want to trade, and Exchange Halos handle price discovery and matching. Settlement occurs on-chain with atomic execution — either the entire trade succeeds or it reverts.

Exchange Halos can support different market types: spot trading, Halo Unit shares, risk capital tokens, and restricted assets requiring identity verification. Each Exchange Halo operates within governance-approved parameters defining supported pairs, fee structures, and access requirements.

Trading Halos complement Exchange Halos by providing always-on AMM-based liquidity. Where Exchange Halos enable price discovery through orderbooks, Trading Halos provide baseline instant liquidity at a spread — particularly valuable for RWAs with known NAVs and predictable redemption values. See `sky-agents/halo-agents/trading-halo.md`.

#### Risk Isolation

Trading operations use two key safety mechanisms. **Settlement Latency** measures the delay between trade execution and final settlement — during this window, the Prime bears counterparty and market risk, which feeds into operational risk capital sizing. **Prime Intent Vaults** isolate trading capital from a Prime's main treasury: USDS committed to trading flows sits in a dedicated vault, limiting blast radius if a trading operation fails.

### Identity Network

For regulated products and institutional participants, Sky Ecosystem supports Identity Networks — specialized Halos that maintain on-chain registries of verified addresses.

| Property | Description |
|----------|-------------|
| **Function** | KYC/identity verification with on-chain attestation |
| **Registry** | Simple on-chain list of verified addresses |
| **Verification** | Legal entity performs KYC; documents stored off-chain |
| **Token Restriction** | Issuers configure which Identity Networks their tokens accept |

When a Halo Unit or Prime token issuer wants to restrict holders, they configure accepted Identity Networks. Only addresses with valid attestations can receive the token — restrictions are enforced at the token level, so any exchange or protocol using these tokens automatically inherits the restrictions.

Multiple Identity Networks can operate simultaneously, specializing in different jurisdictions (US, EU, APAC) or investor types (accredited, institutional, qualified purchaser). Competition between networks creates pressure for reasonable pricing and efficient verification.

### Multi-Chain Infrastructure

Sky Ecosystem operates across multiple chains through SkyLink, the native bridging infrastructure:

- Ethereum mainnet (primary)
- Major L2 networks (Arbitrum, Optimism, Base)
- Alternative L1s (Solana via Keel)

SkyLink enables USDS and sUSDS to maintain full functionality — including savings rate accrual — on all supported chains.

---

## Part 8: Governance

> **Note:** This section describes Sky's current governance mechanism. The SpellGuard system (Part 7) introduces a post-transition model where the Core Council handles routine operations through SpellCore, replacing direct Executive Votes for most parameter changes. SKY token holders retain ultimate authority over constitutional changes, freeze/override power, and quarterly Council rotation.

Sky Ecosystem is governed through decentralized on-chain voting by SKY token holders. This governance system controls all protocol parameters, risk settings, capital allocation, and treasury management.

### Voting Mechanism

SKY holders participate in governance through two types of votes:

| Vote Type | Purpose | Duration |
|-----------|---------|----------|
| **Governance Polls** | Signal preferences, gather consensus | 3 days |
| **Executive Votes** | Implement on-chain parameter changes | Variable |

Executive votes modify the actual protocol parameters. When an executive vote passes, the changes are queued for implementation after a security delay.

### What Governance Controls

Decentralized governance has authority over:

- **Risk parameters** — Collateral ratios, debt ceilings, liquidation thresholds
- **Rate settings** — Base rates, savings rates, fee structures
- **Agent approval** — Adding new Synomic Agents, setting allocation limits
- **Treasury management** — Reserve allocation, buyback parameters
- **Protocol upgrades** — Smart contract modifications, new features

### The Atlas

The Atlas is Sky Ecosystem's governance constitution — a document defining the principles, structures, and rules that govern how decisions are made. The Atlas establishes:

- Core principles that cannot be violated
- Agent type definitions and requirements
- Governance process rules
- Escalation procedures for edge cases

The Atlas can be modified through governance, but changes require elevated thresholds reflecting the document's constitutional nature. In its mature form, governance functions as a crystallization interface — the process through which accumulated evidence and operational experience are converted into binding rules. The Synome uses synlang — a formal S-expression notation — for machine-readable encoding of governance rules and agent directives. See `synomics/synodoxics/` for the epistemological framework and `synomics/synoteleonomics/` for teleonome design theory.

### The Hearth

The Hearth is the teleological framework that grounds Sky Ecosystem's long-term mission. It defines three immutable commitments: the **Commitment to Life and Natural Childhood** (all natural life on Earth survives and flourishes), the **Commitment to the Hearth** (the solar system is preserved indefinitely as a protected habitat), and the **Commitment to Natural Sovereignty** (naturals own everything inside the Hearth; human labour remains the dominant mode of daily life). These commitments provide the stable, non-negotiable foundation upon which all governance, coordination, and autonomous agent design ultimately rest. For the full teleological framework, see `synomics/hearth/`.

### Operational Model

Sky Ecosystem's governance operates on an escalation model:

- **99% automated** — Smart contracts execute predefined logic without intervention
- **1% human judgment** — Edge cases escalate through governance for resolution

This model provides efficiency for routine operations while preserving human oversight for exceptional circumstances. The goal is minimal governance intervention in day-to-day operations, with clear escalation paths when needed.

### Emergency Response

Sky Ecosystem maintains emergency response capabilities for critical situations:

- Geographically distributed emergency response team
- Freeze capabilities for compromised components
- Recovery procedures for various failure modes

Emergency powers are constrained by governance-set parameters and subject to post-incident review.

---

## Appendices

- [Appendix A: Protocol Features](appendix-a-protocol-features.md) — Exhaustive list of Sky Protocol mechanisms
- [Appendix B: Synomic Agent Framework Primitives](appendix-b-sky-agent-framework-primitives.md) — Complete Agent Framework capabilities
- [Appendix C: Treasury Management Function](appendix-c-treasury-management-function.md) — Complete TMF waterfall specification
- [Appendix D: Tokens](appendix-d-tokens.md) — All tokens in Sky Ecosystem
- [Appendix E: Design Rationale](appendix-e-design-rationale.md) — Q&A explaining critical design decisions
- [Appendix F: Glossary](appendix-f-glossary.md) — Term definitions
- [Appendix G: Infrastructure](appendix-g-infrastructure.md) — Deployed contracts, bridges, and legacy systems

## Detailed Specifications

For implementation details beyond this whitepaper:

**Smart Contracts:**
- `smart-contracts/architecture-overview.md` — Four-layer architecture (Generator → Prime → Halo → Foreign)
- `smart-contracts/lcts.md` — LCTS (Liquidity Constrained Token Standard) specification
- `smart-contracts/nfats.md` — NFAT (Non-Fungible Allocation Token) specification
- `smart-contracts/diamond-pau.md` — Diamond PAU (EIP-2535) architecture
- `smart-contracts/rate-limit-attacks.md` — IRL/SORL optimization model and attack surface analysis
- `smart-contracts/fixed-rates.md` — Fixed-rate yield splitting (PT/YT) via Yield Splitter

**Beacon Framework & Automation:**
- `synomics/macrosynomics/beacon-framework.md` — Complete beacon taxonomy (LPLA, LPHA, HPLA, HPHA)
- `trading/sentinel-network.md` — Sentinel formations (stl-base, stl-stream, stl-warden)

**Risk Framework:**
- `risk-framework/capital-formula.md` — Risk capital calculations
- `risk-framework/duration-model.md` — Duration Buckets and liability duration (Duration Model)
- `risk-framework/asset-classification.md` — Asset type classifications
- `risk-framework/matching.md` — Asset-liability duration matching (ALDM) and rate hedging
- `risk-framework/asc.md` — Actively Stabilizing Collateral requirements
- `risk-framework/correlation-framework.md` — Correlation-based capital adjustments
- `risk-framework/operational-risk-capital.md` — Operational Risk Capital (ORC)
- `risk-framework/collateralized-lending-risk.md` — Collateralized lending risk parameters
- `risk-framework/market-risk-frtb.md` — FRTB-style market risk capital
- `risk-framework/risk-monitoring.md` — Risk monitoring and reporting

**Agent Types:**
- `sky-agents/` — Agent type specifications (Primes, Halos, Guardians, Generators)

**Halos & Trading:**
- `sky-agents/halo-agents/portfolio-halo.md` — LCTS-based Portfolio Halos
- `sky-agents/halo-agents/term-halo.md` — NFAT-based Term Halos
- `sky-agents/halo-agents/trading-halo.md` — AMM-based Trading Halos
- `trading/sky-intents.md` — Intent-based trading system and Exchange Halos

**Governance Transition:**
- `governance-transition/spellguard-system.md` — SpellGuard layered governance model
- `governance-transition/guardian-rename.md` — Guardian role consolidation

**Cognitive Architecture:**
- `synomics/neurosymbolic/` — Attention allocation, live graph context, cognitive manipulation loops

**Teleology:**
- `synomics/hearth/` — Hearth commitments, stellar husbandry, human-AI integration, sacred reserve design

**Implementation:**
- `roadmap/phase1/phase-1-overview.md` — Phase 1 implementation roadmap

---

*This document describes Sky Ecosystem as of January 2026. Protocol parameters and capabilities are subject to change through decentralized governance. This whitepaper is for informational purposes only and does not constitute investment advice or an offer to sell securities.*
