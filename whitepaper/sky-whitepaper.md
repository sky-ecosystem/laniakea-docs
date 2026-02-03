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
| 2025 | Four Sky Agents deployed; SKY buyback mechanism activated |

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

---

## Part 4: How the Protocol Works

Sky Protocol is the decentralized infrastructure powering Sky Ecosystem — a set of smart contracts and on-chain mechanisms that manage stablecoin issuance, collateral, capital deployment, and profit allocation.

### Revenue Generation

Sky Protocol generates revenue from capital deployed through the Agent network. The protocol earns the "base rate" on deployed capital while paying the "savings rate" to sUSDS holders. Net protocol revenue equals:

```
Net Revenue = (Base Rate × Deployed Capital) - (Savings Rate × sUSDS Deposits)
```

Revenue sources are managed by Sky Agents (see Part 5), each specializing in different asset classes and strategies. This diversification enables Sky Ecosystem to maintain yield across varying market conditions.

### Treasury Management Function (TMF)

The Sky TMF is a sequential waterfall that distributes all protocol net revenue through five steps. Each step calculates its allocation based on what remains after the previous step.

| Step                              | Allocation                              | Purpose                                        |
| --------------------------------- | --------------------------------------- | ---------------------------------------------- |
| **1. Security & Maintenance**     | 21% (Genesis) / 4-10% (Post-Genesis)    | Core teams, security, risk management          |
| **2. Aggregate Backstop Capital** | Variable (target: 1.5% of total supply) | Solvency buffer for bad debt protection        |
| **3. Fortification Conserver**    | 20% × Net Revenue Ratio                 | Legal defense, resilience, unquantifiable risk |
| **4. Smart Burn Engine**          | 20% × Net Revenue Ratio                 | SKY buybacks                                   |
| **5. Staking Rewards**            | 100% of remainder                       | Distributed to SKY stakers                     |

**Net Revenue Ratio:** A hyperbolic function that scales allocations based on total protocol net revenue. At low revenue, most surplus flows to staking rewards. As revenue grows, more flows to burn and fortification. The formula approaches 1.0 as revenue approaches the cap threshold.

**Aggregate Backstop Capital:** Fills dynamically based on how far the buffer is from its target. When empty, up to 50% of available funds flow to the buffer. When full, the step is skipped entirely.

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

Sky Agents are autonomous and independent systems within Sky Ecosystem that plug into the decentralized Sky Protocol primitives. These Agents compete to deliver the highest risk-adjusted returns while efficiently sharing the economies of scale of the entire ecosystem.

### Agent Structure

The Agent network operates as a capital allocation layer between Sky Protocol and end investments:

```
Sky Protocol → Sky Agents (Primes) → Investment Products (Halos) → End Assets
```

**Primes** are the primary capital deployers — governance-approved operators that receive capital from Sky Protocol and deploy it into various strategies. Each Prime operates with its own treasury, governance token, and specialized focus.

**Halos** are investment product wrappers created by Primes. Each Halo wraps a specific strategy or asset class, providing standardized interfaces for capital deployment and risk management. Halos are organized into **Halo Classes** (shared smart contract and legal infrastructure) containing **Halo Units** (individual products with specific parameters).

There are two primary Halo types:

| Type | Token Standard | Use Case |
|------|----------------|----------|
| **Passthrough Halo** | LCTS (pooled, fungible) | Standardized products with uniform terms — all participants share the same conditions |
| **Structuring Halo** | NFAT (individual, non-fungible) | Bespoke deals with negotiated terms — each position can have different duration, size, and yield |

**Passthrough Halos** use the Liquidity Constrained Token Standard (LCTS) for queue-based entry and exit. Participants deposit to a queue, and at weekly settlement, deposits convert to Halo Unit shares at the current exchange rate. This model works well for open-ended funds where all participants receive identical treatment.

**Structuring Halos** use Non-Fungible Allocation Tokens (NFATs) to represent individual deals. Each NFAT is a distinct position with its own terms negotiated within a defined "buybox" (acceptable parameter ranges). NFATs are transferable and can be used as collateral, enabling secondary markets for structured positions. For example, a Structuring Halo might issue 6-month, 12-month, and 18-month NFATs with different yields, all within the same legal framework.

This structure separates risk-taking from monetary policy: Sky Core sets parameters and constraints, while Primes compete to deploy capital efficiently within those bounds. Primes bear the business risk — providing their own capital as first-loss protection on the assets they deploy — freeing core governance from day-to-day investment decisions.

### Current Sky Agents

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

### Core Halos

In addition to Primes creating new Halos, Sky maintains **Core Halos** — legacy assets standardized as Halo Units under Core Council governance. Core Halos allow existing protocol positions (such as legacy vault exposures or pre-existing RWA allocations) to be wrapped with the same risk framework and reporting standards as Prime-created Halos.

Core Halos are governed via Halo Unit Artifacts maintained by Core Council, not by individual Primes. This provides a path for legacy assets to either:
- Transition to Prime ownership when a suitable Prime is identified
- Wind down systematically if no longer strategically aligned

Initially, Core Halos cover all protocol assets that aren't yet operated by Primes through Structuring Halos.

### How Agents Compete

Sky Agents compete for capital allocation based on performance. The Agent with the best risk-adjusted returns receives more capital, creating market pressure for optimization. This competitive dynamic benefits Sky Ecosystem through:

- **Higher yields** — Agents optimize strategies to attract capital
- **Risk specialization** — Each Agent focuses on their area of expertise
- **Innovation** — New strategies and products emerge from competition
- **Efficiency** — Shared infrastructure reduces costs across all Agents

### Adding New Agents

New Sky Agents are added through decentralized governance. The approval process includes evaluation of the Agent's strategy, team, risk framework, and operational infrastructure. Once approved, new Agents can immediately access capital from Sky Protocol within their governance-approved limits.

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

### Loss Absorption Waterfall

If losses occur, they are absorbed in a defined sequence across three tiers:

```
PRIME-LEVEL (per-Prime):
  1. First Loss Capital (10% of IJRC)     ← Prime's own capital first
  2. Remaining JRC (IJRC + EJRC pro-rata) ← All junior capital
  3. Agent Token Inflation                ← Dilute Prime token holders
  4. TISRC (Prime-isolated SRC)           ← Senior capital scoped to this Prime

SYSTEM-LEVEL (shared):
  5. Global SRC (srUSDS)                  ← Senior capital across all Primes
  6. SKY Token Inflation                  ← Dilute protocol token holders

NUCLEAR OPTIONS (protocol-level):
  7. Genesis Capital Haircut              ← Protocol reserves
  8. USDS Peg Adjustment                  ← Final backstop
```

The First Loss Capital requirement ensures Primes have direct skin in the game — they absorb the initial 10% of any losses from their own capital before external junior capital shares in subsequent losses. Agent Token inflation can cover losses "to infinity" before touching senior capital. If Prime-level mechanisms are exhausted, system-level capital (Global SRC, then SKY inflation) absorbs remaining losses. Genesis Capital and peg adjustment are nuclear options that should never be reached under normal conditions.

### Encumbrance Monitoring

Sky Ecosystem continuously monitors the ratio of required risk capital to total risk capital available:

```
Encumbrance Ratio = Required Risk Capital / Total Risk Capital
```

The target encumbrance ratio is ≤90%, providing a 10% buffer above minimum requirements. Agents exceeding this threshold face escalating penalties until they restore compliance.

### Duration Matching

Sky tracks USDS lot ages to estimate how long holders will actually stay, using the Lindy Duration Model: the longer someone has held, the longer they're likely to continue holding. This liability duration data determines capacity in Duration Buckets, which are matched against asset durations measured by Stressed Pull-to-Par (SPTP) — the time until an asset converges to its fundamental value under stress conditions. This Asset-Liability Duration Matching (ALDM) system enables capital-efficient deployment of long-duration assets.

The risk framework matches asset characteristics to liability profiles: assets with longer time-to-liquidity require backing from longer-duration liabilities. When an asset's duration matches available liability capacity, it only needs capital for fundamental risk (credit default, smart contract failure). Unmatched assets must hold additional capital covering potential mark-to-market losses from credit spread widening — temporary price drops that recover as spreads normalize.

Laniakea extends this framework with explicit rate hedging requirements: since duration matching protects against mean-reverting credit spread movements but not permanent interest rate shifts, all fixed-rate exposure must be hedged or carry additional capital.

### Independent Assessment

Sky Ecosystem’s risk framework design is intended to be independently analyzable and auditable by third parties. Risk parameters are continuously monitored and adjusted through decentralized governance based on market conditions and portfolio composition.

---

## Part 7: Protocol Upgrades

Sky Ecosystem is implementing the Laniakea upgrade, a significant expansion of protocol capabilities enabling automated settlement at scale, unified risk management, and rapid deployment of new investment products.

### Implementation Phases

Laniakea is deployed incrementally:

| Phase | Focus | Settlement |
|-------|-------|------------|
| **Phase 1** | Core infrastructure — beacons, Synome-MVP, first Structuring Halos | Monthly |
| **Phase 2+** | Full automation — weekly settlement, auction systems, Sentinel formations | Weekly |

Phase 1 establishes the foundational infrastructure using low-power beacons (deterministic programs) while maintaining monthly settlement. Later phases introduce high-power Sentinels (AI-capable formations) and weekly settlement cycles.

### Beacon Infrastructure

Laniakea introduces a beacon framework for autonomous operations. Beacons are classified by two axes:

| | Low Authority | High Authority |
|---|---|---|
| **Low Power** | LPLA (reporting) | LPHA (rule execution) |
| **High Power** | HPLA (trading) | HPHA (Sentinels) |

Phase 1 deploys LPLA and LPHA beacons — deterministic programs that execute predefined rules. Later phases introduce HPHA Sentinels — AI-capable formations with Baseline (execution), Stream (intelligence), and Warden (safety) components.

### Diamond PAU

The current Legacy PAU architecture (Controller + ALMProxy + RateLimits) will be replaced by the Diamond PAU pattern, which uses EIP-2535 diamond proxy architecture for modular, upgradeable functionality. Diamond PAUs enable:

- Modular action facets that can be added without full redeployment
- Standardized factory deployment for new Halos
- Unified interface across all agent types

### Weekly Settlement Cycle

Full Laniakea introduces a weekly settlement cycle replacing the monthly cadence:

| Period | Timing | Function |
|--------|--------|----------|
| Measurement | Tuesday → Tuesday | Data collection, position tracking |
| Processing | Tuesday noon → Wednesday noon | Calculations, verification |
| Settlement | Wednesday noon | All changes take effect |

Weekly settlement enables faster capital reallocation, more responsive risk management, and tighter feedback loops between Agent performance and capital allocation. Each cycle includes sealed-bid auctions where Primes compete for senior risk capital capacity and duration-matching reservations.

### Automated Operations

The upgrade introduces automated operational infrastructure:

- **Automated risk capital verification** — Continuous monitoring without manual intervention
- **Programmatic settlement** — Calculations and distributions execute automatically
- **Rate-limited capital flows** — All movements bounded by governance-set limits

This automation reduces operational overhead while maintaining governance control over parameters and limits.

### Expanded Agent Capabilities

Laniakea provides new capabilities for Sky Agents:

| Capability | Description |
|------------|-------------|
| Factory-deployed products | Standardized Halo creation with reduced setup time |
| Unified risk framework | Consistent capital requirements across all asset types |
| Auction-based allocation | Market-driven distribution of scarce resources |
| Enhanced monitoring | Real-time visibility into Agent operations |

These capabilities allow Sky Ecosystem to onboard new asset classes and strategies more rapidly while maintaining consistent risk standards.

### Trading Infrastructure

Laniakea introduces Sky Intents, an intent-based trading system for Sky Ecosystem assets:

| Component | Function |
|-----------|----------|
| **Sky Intents** | Users express trading intent; matching occurs off-chain; settlement on-chain |
| **Exchange Halos** | Specialized Halos operating orderbooks and matching engines for specific markets |
| **LPHA Beacons** | Low Power, High Authority beacons executing deterministic matching rules |

Sky Intents separates intent expression from execution: users submit what they want to trade, and Exchange Halos handle price discovery and matching. Settlement occurs on-chain with atomic execution — either the entire trade succeeds or it reverts.

Exchange Halos can support different market types: spot trading, Halo Unit shares, risk capital tokens, and restricted assets requiring identity verification. Each Exchange Halo operates within governance-approved parameters defining supported pairs, fee structures, and access requirements.

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
- **Agent approval** — Adding new Sky Agents, setting allocation limits
- **Treasury management** — Reserve allocation, buyback parameters
- **Protocol upgrades** — Smart contract modifications, new features

### The Atlas

The Atlas is Sky Ecosystem's governance constitution — a document defining the principles, structures, and rules that govern how decisions are made. The Atlas establishes:

- Core principles that cannot be violated
- Agent type definitions and requirements
- Governance process rules
- Escalation procedures for edge cases

The Atlas can be modified through governance, but changes require elevated thresholds reflecting the document's constitutional nature.

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
- [Appendix B: Sky Agent Framework Primitives](appendix-b-sky-agent-framework-primitives.md) — Complete Agent Framework capabilities
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

**Beacon Framework & Automation:**
- `synomics/beacon-framework.md` — Complete beacon taxonomy (LPLA, LPHA, HPLA, HPHA)
- `legal-and-trading/sentinel-network.md` — Sentinel formations (stl-base, stl-stream, stl-warden)

**Risk Framework:**
- `risk-framework/capital-formula.md` — Risk capital calculations
- `risk-framework/duration-model.md` — Duration Buckets and liability duration (Lindy Duration Model)
- `risk-framework/asset-classification.md` — Asset type classifications

**Halos:**
- `legal-and-trading/passthrough-halo.md` — LCTS-based Passthrough Halos
- `legal-and-trading/structuring-halo.md` — NFAT-based Structuring Halos

**Implementation:**
- `phase1/laniakea-phase-1.md` — Phase 1 implementation roadmap

---

*This document describes Sky Ecosystem as of January 2026. Protocol parameters and capabilities are subject to change through decentralized governance. This whitepaper is for informational purposes only and does not constitute investment advice or an offer to sell securities.*
