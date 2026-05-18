# Laniakea Implementation Roadmap

**Status:** Draft
**Last Updated:** 2026-02-12

---

## Overview

This roadmap outlines the phased implementation of Laniakea infrastructure, from Phase 0 legacy exceptions through full autonomous operation with Sentinel formations in Phase 10.

Phase 0 handles exceptional deployments (primarily Grove) that must proceed before standardized infrastructure exists. The main progression follows a deliberate sequence: establish foundational infrastructure first (Phases 1-4), then build factory systems for scalable deployment (Phases 5-8), and finally achieve full automation through Sentinel formations (Phases 9-10).

---

## Phase Summary

| Phase | Name | Core Deliverable |
|-------|------|------------------|
| **0** | Legacy & Exceptional Deployments | Grove pre-standardization deployments; acknowledged technical debt. 6 substages (0.0–0.5). |
| **1** | Pragmatic Delivery | MVP beacons (lpla-verify), Configurator, NFAT infrastructure; manual settlement continues. 7 substages (1.0–1.6). |
| **2** | Monthly Settlement | Full lpla-checker with settlement tracking; formalized monthly settlement cycle |
| **3** | Daily Settlement | Transition from monthly to daily settlement cycle |
| **4** | LCTS Launch | srUSDS and first Portfolio Halo (pre-auction); Core Council manages srUSDS rate |
| **5** | Halo Factory | Automated Halo Agent creation with LCTS/NFAT class attachment |
| **6** | Generator PAU | Single-ilk USDS Generator PAU replacing per-Prime ilks |
| **7** | Prime Factory | Automated Prime deployment |
| **8** | Generator Factory | Automated Generator deployment |
| **9** | Sentinel Base & Warden | High-power beacon foundations, Warden formation, auction activation |
| **10** | Sentinel Stream | Stream formation for continuous operations |

---

## Detailed Phase Descriptions

### Phase 0: Legacy & Exceptional Deployments

**Objective:** Deploy legacy and exceptional actions for Grove before standardized Laniakea infrastructure is ready

**Scope:** Grove (Star Prime) only. All Phase 0 deployments are acknowledged technical debt — they operate outside standardized infrastructure and will be converted to Core Halos (or evolved into proper Halo Classes) as Phase 1 matures.

**Substages:**

| Substage | Name | Description |
|----------|------|-------------|
| **0.0** | Planning & Finalization | Inventory all legacy/exception actions; accept technical debt |
| **0.1** | Custodial Crypto-Backed Lending | USDC → legal entity → offchain custodial crypto-backed lending |
| **0.2** | Crypto-Enabled Lending | USDC → legal entity → crypto-enabled lending |
| **0.3** | Tokenized RWA Trading | Early-stage tokenized RWA trading (precursor to PSM3-based Halo Class) |
| **0.4** | Blockchain Bridge | Bridge to a new blockchain |
| **0.5** | Star4 Deployment | Initial deployment only; joins standard Phase 1 track afterward |

**Runs concurrently with Phase 1.** Phase 0 does not block Phase 1 progress.

**End State:** All planned Grove exceptional deployments live. Phase 1.3 has a clear inventory of assets to wrap as Core Halos.

**Document:** [phase-0-legacy-exceptions.md](./phase-0-legacy-exceptions.md)

---

### Phase 1: Pragmatic Delivery

**Objective:** Establish minimal viable infrastructure for automated capital deployment

**Settlement:** Existing manual process continues (formalized monthly settlement begins in Phase 2)

**Substages:**

| Substage | Name | Key Outcome |
|----------|------|-------------|
| **1.0** | Planning | Stakeholder alignment, Prime cohort identification |
| **1.1** | Diamond PAU Deployment | Diamond PAUs deployed for first-cohort Primes |
| **1.2** | Operational Infrastructure | Synome-MVP, lpla-verify, lpha-relay, lpha-attest operational |
| **1.3** | Legacy Cleanup & Core Halos | Legacy assets standardized or wound down |
| **1.4** | Configurator Deployment | Spell-less Prime operations enabled |
| **1.5** | First Term Halo | Halo1 live with end-to-end NFAT flow validated |
| **1.6** | Term Halo Cohort | Halo2-Halo6 deployed and accepting NFAT deployments |

**lpla-verify:** Monitors positions, calculates CRRs, generates alerts. Does not track settlement — that capability arrives with lpla-checker in Phase 2.

**End State:** Primes can deploy into Core Halos and Term Halos without spells. Full first-cohort of Term Halos operational. Five beacons live (lpla-verify, lpha-relay, lpha-nfat, lpha-attest, lpha-council).

**Document:** [phase-1-overview.md](./phase1/phase-1-overview.md)

---

### Phase 2: Monthly Settlement

**Objective:** Formalize monthly settlement cycle with beacon-assisted oversight

**Settlement Cycle:** Monthly (formalized with lpla-checker tracking)

**Key Deliverables:**
- **lpla-checker beacon** — Extends lpla-verify with settlement tracking, completeness verification, late payment detection, and penalty calculation
- **Formalized monthly settlement** — Canonical monthly timeline with defined settlement windows
- **Prepayment and penalty mechanics** — Prime interest prepayment obligations, penalty calculation and logging
- **Synome schema updates** — Monthly epoch identifiers, settlement artifacts, penalty events

**Dependencies:** Phase 1 complete

**End State:** Monthly settlement runs reliably with lpla-checker validation. Prepayment and penalty system operational. Settlement artifacts consistently logged in Synome.

**Document:** [phase-2-monthly-settlement.md](./phase-2-monthly-settlement.md)

---

### Phase 3: Daily Settlement

**Objective:** Transition from monthly to daily settlement cycle

**Settlement Cycle:** Daily (21h Active Window + ≤3h Processing Window)

**Daily Timeline (UTC):**
| Period | Timing | Purpose |
|--------|--------|---------|
| **Active Window** | 16:00 → 13:00 | Data collection, deposits/withdrawals |
| **Processing Window (Lock)** | 13:00 → 16:00 | Calculation, verification, prepayment |
| **Moment of Settlement** | 16:00 | New parameters take effect |

**Key Deliverables:**
- **Daily settlement infrastructure** — Lock/unlock cycle synchronized across all systems
- **Interest/distribution prepayment system** — Primes prepay before 16:00 or face penalties
- **Synome schema updates** — Daily reporting, penalty tracking
- **Beacon modifications** — lpla-checker adapted for daily cadence
- **Late payment penalties** — Continuous accrual from Moment of Settlement until payment

**Dependencies:** Phase 2 complete (formalized monthly settlement established)

**End State:** All Primes and Halos operate on daily settlement cycle. Prepayment and penalty system operational at daily cadence. Allocation remains governance-directed until stl-base enables auctions.

**Document:** [phase-3-daily-settlement.md](./phase-3-daily-settlement.md)

---

### Phase 4: LCTS Launch

**Objective:** Launch LCTS (Liquidity Constrained Token Standard) with srUSDS and MMF Portfolio Halo

**LCTS Core Concept:** Queue-based system for capacity-constrained token conversions. Users subscribe assets, receive shares representing queue position, receive converted assets over time as capacity allows.

**LCTS Architecture:**
- **SubscribeQueue** + **RedeemQueue** — Independent queues with generation model
- **Generation lifecycle:** DORMANT → ACTIVE → LOCKED → (ACTIVE or FINALIZED → DORMANT)
- **Lock window:** 13:00-16:00 UTC (synchronized with daily settlement)
- **LCTS-pBEAM** — Operated by lpha-lcts beacon (LPHA, not sentinel)

**srUSDS Rate Management (Pre-Auction):** When srUSDS goes live, Sky Core will initially decide what rate it receives, manually targeting a governance-set rate. Core Council manages day-to-day rate decisions according to instructions from Atlas. This governance-directed approach remains in place until Phase 9 activates sealed-bid auctions.

**Key Deliverables:**
- **LCTS smart contracts** — SubscribeQueue, RedeemQueue with generation model
- **srUSDS token** — Senior Risk Capital token via LCTS (Generator level)
  - sUSDS → srUSDS via SubscribeQueue
  - srUSDS → sUSDS via RedeemQueue
  - Exchange rate updated at each settlement
- **Holding System** — Contract backing srUSDS with sUSDS, receives funding from Prime PAUs
- **lpha-lcts beacon** — Manages LCTS vault operations (lock, settle, capacity determination)
- **Pre-auction origination mode** — Core Council sets srUSDS rate and capacity directly (no auctions until stl-base)
- **MMF Portfolio Halo** — First LCTS-based Halo for Money Market Fund deployment
- **Target spread mechanism** — Governance-set spread above SSR protects yield rates
- **Net flow netting** — Subscribe/redeem queues cancel out first, reducing conversion needs

**LCTS Use Cases by Agent Type:**
| Agent | Token | Description |
|-------|-------|-------------|
| Generator | srUSDS | External pooled Senior Risk Capital |
| Prime | TEJRC | Tokenized External Junior Risk Capital |
| Prime | TISRC | Tokenized Isolated Senior Risk Capital |
| Halo | Unit shares | Claims on Halo Units (default for capacity-constrained products) |

**Portfolio Halo Structure:**
- **Halo Class** = shared PAU + lpha-lcts + legal framework
- Multiple **Halo Units** per class (e.g., senior/junior tranches)
- Manual deployment + onboarding via spells (factories begin in Phase 5)
- Prime allocations into Units are governance-directed/manual (Prime-side stl-base automation begins in Phase 9)

**Dependencies:** Phase 3 complete (daily settlement cycle required — LCTS lock/settle synchronized with daily cycle)

**End State:** srUSDS operational as first LCTS product. MMF Portfolio Halo accepting deposits. Infrastructure ready for additional Portfolio Halos.

**Document:** [phase-4-lcts-launch.md](./phase-4-lcts-launch.md)

---

### Phase 5: Halo Factory

**Objective:** Enable automated creation of Halo Agents with attached Halo Classes via Laniakea Factory

**Laniakea Factory Concept:**
Factory system deploys standardized PAU infrastructure from audited templates. Factory-deployed PAUs get streamlined governance approval.

**Halo Class Structure:**
A **Halo Class** = grouping of Halo Units sharing:
- **PAU** (Controller + ALMProxy + RateLimits)
- **Beacon** (lpha-lcts or lpha-nfat)
- **Legal Framework** (buybox, counterparty requirements, recourse)

**Key Deliverables:**
- **Halo Factory smart contracts** — Deploy standardized Halo PAUs
- **Halo Class templates:**
  - **LCTS-based (Portfolio Halos):** Pooled capital, fungible shares, queue-based settlement
  - **NFAT-based (Term Halos):** Bespoke deals, ERC-721 NFATs, individual queues
- **Factory → Configurator integration:**
  - Auto-register PAU contracts
  - Pre-create init rate limits for standard operations
  - Streamlined cBEAM grants for GovOps
- **Halo Unit deployment within Classes:**
  - Multiple Units per Class (e.g., senior/junior tranches)
  - Units vary: seniority, yield, capacity, specific terms
  - Shared beacon and legal infrastructure

**NFAT Facility Structure (Term Halos):**
- Each Facility is a Halo Class with its own buybox
- Individual queues per Prime (not shared generations)
- Halo claims from queues, mints ERC-721 NFAT
- Each NFAT = claim on one Halo Unit (bankruptcy remote)
- Deal terms tracked in Synome (APY, duration, maturity)

**Dependencies:** Phase 4 complete (LCTS and daily settlement established; factories begin here)

**End State:** New Halos deployed via factory with standardized PAU infrastructure. Both LCTS and NFAT Halo Classes supported. No custom contract development required.

**Document:** [phase-5-halo-factory.md](./phase-5-halo-factory.md)

---

### Phase 6: Generator PAU

**Objective:** Replace individual Prime ilks with unified USDS Generator PAU architecture

**Generator Layer Role (from Architecture):**
- Manages interface with stablecoin ERC20 contract
- Deploys capital into Prime Layer via **ERC4626 vaults**
- Has its own governance scope separate from Prime/Halo
- Issues **srUSDS** (Senior Risk Capital) via LCTS

**Key Deliverables:**
- **Generator PAU smart contracts** — Standard PAU pattern (Controller + ALMProxy + RateLimits)
- **Single MCD ilk architecture** — Replace per-Prime ilks with single Generator ilk
- **ERC4626 vault interface** — Primes deposit/withdraw from Generator vault
- **srUSDS issuance integration** — Generator manages Senior Risk Capital via LCTS
- **Generator Configurator scope** — Separate governance scope for Generator operations
- **Migration path** — Existing Prime ilks migrate to Generator PAU

**Architecture Change:**
```
Before (per-Prime ilks):          After (Generator PAU):

Prime1 ── ilk1 ── MCD             Prime1 ─┐
Prime2 ── ilk2 ── MCD       →     Prime2 ─┼─ [ERC4626] ─ Generator PAU ─ ilk ─ MCD
Prime3 ── ilk3 ── MCD             Prime3 ─┘
                                     │
                                     └── srUSDS (via LCTS)
```

**Generator → Prime Connection:**
- ERC4626 vault (deposit anytime, redeem if liquidity available)
- Rate limits on deposit/withdraw
- Each Prime controls its own vault's liquidity availability

**Dependencies:** Phase 5 complete (Halo Factory establishes factory patterns)

**End State:** Generator PAU operational with single MCD ilk. All Primes connect via ERC4626 vault. srUSDS issuance integrated.

**Document:** [phase-6-generator-pau.md](./phase-6-generator-pau.md)

---

### Phase 7: Prime Factory

**Objective:** Enable automated Prime deployment via Laniakea Factory

**Prime Layer Role (from Architecture):**
- Receives capital from Generator via ERC4626 vault
- Deploys to: Halo Layer, Core Halos (legacy DeFi), Foreign Primes (cross-chain)
- Each Prime controls its own vault's liquidity availability

**Key Deliverables:**
- **Prime Factory smart contracts** — Deploy standardized Prime PAUs
- **Automated Diamond PAU deployment** — EIP-2535 faceted architecture
  - Standard facets: ERC4626Facet, SwapFacet, NFATFacet, AdminFacet, etc.
  - New integrations = new facets, not controller upgrades
- **Automatic Generator PAU integration:**
  - ERC4626 vault connection
  - Rate limits on Generator deposits/withdrawals
- **Automatic Configurator registration:**
  - PAU registered via BEAMTimeLock (14-day delay)
  - Init rate limits pre-created for standard targets
  - cBEAM grant path for GovOps
- **Prime → Halo connection templates:**
  - LCTS-based Halo vaults
  - NFAT Facility queues
  - Core Halo interfaces (Morpho, Aave, SparkLend)
- **Risk capital integration:**
  - TEJRC (Tokenized External Junior Risk Capital) via LCTS
  - TISRC (Tokenized Isolated Senior Risk Capital) via LCTS

**Factory → Configurator Flow:**
1. Factory deploys Prime PAU (Diamond Proxy + facets + ALMProxy + RateLimits)
2. Factory registers PAU in Configurator (via BEAMTimeLock)
3. Factory pre-creates init rate limits for standard operations
4. Core Council grants cBEAM to GovOps (14-day timelock)
5. GovOps activates rate limits, sets relayer, begins operations

**Dependencies:** Phase 6 complete (Generator PAU required for Prime connection)

**End State:** New Primes deployed via factory with standardized Diamond PAU. Automatic Generator integration. Streamlined Configurator onboarding.

**Document:** [phase-7-prime-factory.md](./phase-7-prime-factory.md)

---

### Phase 8: Generator Factory

**Objective:** Enable automated Generator deployment for multi-Generator architecture

**Why Multiple Generators:**
- Different stablecoin types (USDS, others)
- Different risk capital structures
- Different governance scopes
- Isolation between Generator contexts

**Key Deliverables:**
- **Generator Factory smart contracts** — Deploy standardized Generator PAUs
- **Multi-Generator architecture:**
  - Each Generator has its own MCD ilk
  - Separate LCTS for each Generator's risk capital tokens
  - Independent governance scopes
- **Generator-to-Prime relationship management:**
  - Which Primes can connect to which Generators
  - ERC4626 vault deployment for each relationship
  - Cross-Generator restrictions (if any)
- **Factory → Configurator integration:**
  - Generator PAU registration
  - Generator-scope Configurator Unit deployment
  - Init rate limits for Generator operations
- **Risk capital token factories:**
  - srUSDS deployment per Generator
  - Holding System deployment
  - LCTS queue deployment (SubscribeQueue + RedeemQueue)

**Full Factory Stack:**
```
Generator Factory
    │
    └── Generator PAU + srUSDS + Holding System
            │
            └── Prime Factory
                    │
                    └── Prime PAU (Diamond) + TEJRC/TISRC
                            │
                            └── Halo Factory
                                    │
                                    └── Halo PAU + Halo Class (LCTS or NFAT)
```

**Dependencies:** Phase 7 complete (Prime Factory establishes middle layer patterns)

**End State:** Full factory stack operational. New Generators, Primes, and Halos deployable via standardized factories. No custom contract development at any layer.

**Document:** [phase-8-generator-factory.md](./phase-8-generator-factory.md)

---

### Phase 9: Sentinel Base & Warden

**Objective:** Deploy Baseline Sentinel (stl-base) and Warden Sentinels (stl-warden) — the execution and safety layers of sentinel formations, enabling auctions

**Sentinel Formation Architecture:**
Sentinels operate as **coordinated formations** (data plane / control plane / safety plane):

| Component | Role | Execution Authority | Operator |
|-----------|------|---------------------|----------|
| **stl-base** (Baseline) | Primary decision-making and execution | **Yes** — holds Execution Engine | Accordant GovOps |
| **stl-stream** (Stream) | Data ingestion, signal generation, intent streaming | **No** — feeds Baseline only | Ecosystem Actor |
| **stl-warden** (Warden) | Independent monitoring, risk enforcement | **Limited** — safety stops only | Independent operators |

**Key Deliverables:**
- **stl-base (Baseline Sentinel)**
  - Holds Execution Engine (pBEAMs, signs transactions)
  - Runs public Base Strategy from Prime Artifact
  - Three parallel processes: Counterfactual Simulation, Streaming Monitor, Active Management
  - Fail-safe: reverts to Base Strategy if Stream disconnects
- **Auction activation (OSRC + Duration)**
  - stl-base instances submit bids for srUSDS origination capacity and duration bucket capacity
  - lpha-auction switches from Core Council rate-setting to sealed-bid matching
  - lpha-lcts consumes auction results for srUSDS settlement capacity/yield inputs
- **stl-warden (Warden Sentinels)**
  - **Must be operated by independent parties** (not same as Baseline)
  - Multiple wardens per formation (operator diversity)
  - Continuous monitoring, invariant enforcement, anomaly detection
  - **Halt authority** — can freeze Execution Engine
  - Determines **Time to Shutdown (TTS)** — bounds maximum damage from rogue sentinel
- **TTS Economics**
  - `Maximum Damage = Rate Limit × TTS`
  - `Required Risk Capital ≥ Rate Limit × TTS`
  - Better wardens → Lower TTS → Higher rate limits / less risk capital required
- **Sentinel Toolkit** — lpla-checker (verification/settlement), stk-carry (performance attribution)
- **Synome integration** — Counterfactual simulation logging, warden attestations, formation status

**Why Separation Matters:**
- **Baseline:** All execution flows through public, auditable code
- **Wardens:** Independent safety oversight, cannot be compromised by same failure modes

**Dependencies:** Phase 8 complete (full factory stack provides scale for Sentinel operations)

**End State:** Baseline Sentinels execute Prime strategies. OSRC and duration auctions are live (stl-base bidding). Multiple independent Wardens monitor each formation. TTS-based risk capital requirements operational.

**Document:** [phase-9-sentinel-base-warden.md](./phase-9-sentinel-base-warden.md)

---

### Phase 10: Sentinel Stream

**Objective:** Deploy Stream Sentinels (stl-stream) for proprietary intelligence and alpha generation

**Stream Sentinel Role:**
The commercial engine for alpha generation — allows proprietary intelligence to influence execution without exposing strategies or holding keys.

**Key Deliverables:**
- **stl-stream (Stream Sentinel)**
  - Operated by Ecosystem Actors (DevCos, Trading Firms)
  - **Private/proprietary** — strategies not exposed
  - Data ingestion (public + proprietary sources)
  - Signal generation and model inference
  - **Intent streaming** — sends trading intent (not transactions) to Baseline
  - **No Execution Engine** — cannot move capital directly
- **Streaming Accord** — Smart contract framework governing Baseline ↔ Stream relationship
  - **Risk Tolerance Interval** — bounds on acceptable intent (position limits, velocity limits, concentration limits)
  - **Performance Fee Ratio** — share of alpha that becomes carry
  - Termination conditions, dispute resolution
- **Carry Mechanism**
  - `Carry = (Actual PnL - Simulated Baseline PnL) × Performance Fee Ratio`
  - Stream only profits when outperforming Base Strategy
  - Counterfactual simulation (stl-base Process A) provides benchmark
- **The Compounding Loop**
  ```
  Public Capital → Private Intelligence → Better Streams → More Carry → More Intelligence
  ```
  - Carry reinvested into AGI capabilities (compute, models, data)
  - Fastest known compounding loop, bounded by synomic constraints

**Formation Lifecycle:**
1. Accord Negotiation (Risk Tolerance, Performance Fee)
2. Formation Assembly (Baseline, Stream, Wardens register in Synome)
3. Activation (Stream sends intent, Baseline executes or falls back)
4. Ongoing Operation (continuous trading, periodic settlement, carry distribution)
5. Termination (expiration, breach, governance intervention)

**Safety Properties:**
- All execution flows through public Baseline code
- Wardens provide independent halt authority
- Rate limits bound maximum damage
- Beacons can be revoked by governance
- Worst-case losses collateralized by risk capital

**Dependencies:** Phase 9 complete (Baseline + Wardens must be operational before Stream can influence execution)

**End State:** Full sentinel formations operational (stl-base + stl-stream + stl-warden). Ecosystem actors operate Streams, earning carry from alpha. Teleonomes compound intelligence within safe bounds.

**Document:** [phase-10-sentinel-stream.md](./phase-10-sentinel-stream.md)

---

## Unscheduled Specifications

The following features have complete or partial specifications but are not yet assigned to roadmap phases:

| Feature | Specification | Key Dependencies |
|---------|--------------|-----------------|
| **Fixed Rates / Yield Splitter** | `smart-contracts/fixed-rates.md` | LCTS exchange rate interfaces (Phase 4+), Exchange Halos |
| **Exchange Halos** | Whitepaper Part 7 (no smart-contract spec) | Limit orderbook infrastructure |
| **Identity Networks** | Whitepaper Part 7 (no spec) | — |
| **Sky Intents** | `trading/sky-intents.md` | Sentinel formations (Phase 9+), Exchange Halos |
| **SBE BEAM** | `accounting/current-accounting.md` | Daily settlement cycle (Phase 3+) — governance-controlled execution surface for dynamic Smart Burn Engine |
| **Folio Agents** | `sky-agents/folio-agents/agent-type-folios.md` | Folio Agent deployment (stl-principal, automated folios, Growth Staking integration). Depends on: Halo Factory (Phase 5) |
| **Growth Staking** | `growth-staking/growth-staking.md` | Growth Staking mechanism linking staking rewards to growth asset holdings via folios. Depends on: Folio Agents |
| **Trading Halos / lpha-amm** | Whitepaper Part 7, `sky-agents/halo-agents/trading-halo.md` | Trading Halo type and lpha-amm beacon for automated market making. Depends on: Halo Factory (Phase 5) |
| **SpellGuard Governance Transition** | `governance-transition/spellguard-system.md` | Transition from Executive Vote to SpellGuard model (SpellCore + Guardians). See `governance-transition/` |
| **Recovery Agents** | `sky-agents/recovery-agents/agent-type-recovery.md` | Recovery Agent deployment for crisis response and system restoration. Prerequisite for full Sentinel formation autonomy (Phase 9+) |

These features will be assigned to phases as their dependencies mature and implementation priorities are established.

---

## Infrastructure Progression

```
Phase 0: Exceptions (concurrent with Phase 1)
├── Grove legacy deployments (0.1–0.4)
├── Star4 bootstrap (0.5, then joins Phase 1 track)
└── All become Core Halos in Phase 1.3 (or evolve into Halo Classes)

Phase 1-4: Foundation
├── Beacons: lpla-verify, lpha-relay, lpha-nfat, lpha-attest, lpha-council (Phase 1) → lpla-checker (Phase 2+)
├── Settlement: Manual → Formalized Monthly → Daily
├── Halos: Core Halos (wrapping Phase 0 debt) → Term Halos → Portfolio Halos (LCTS)
├── srUSDS: Core Council manages rate (pre-auction)
└── Beacons: LPLA/LPHA (low-power programs)

Phase 5-8: Factories
├── Halo Factory (LCTS + NFAT classes)
├── Generator PAU (unified ilk architecture)
├── Prime Factory
└── Generator Factory

Phase 9-10: Automation
├── Sentinel Base + Warden (execution + safety)
├── Auctions (OSRC + Duration) via stl-base
└── Stream formation (proprietary intelligence)
```

---

## Dependencies Graph

```
Phase 0 (Legacy & Exceptional Deployments)  ──── runs concurrently ────┐
                                                                        │
Phase 1 (Pragmatic Delivery)  ◄─── Phase 0 assets feed into 1.3 ──────┘
    │
    ▼
Phase 2 (Monthly Settlement)
    │
    ▼
Phase 3 (Daily Settlement)
    │
    ▼
Phase 4 (LCTS Launch)
    │
    ▼
Phase 5 (Halo Factory)
    │
    ▼
Phase 6 (Generator PAU)
    │
    ▼
Phase 7 (Prime Factory)
    │
    ▼
Phase 8 (Generator Factory)
    │
    ▼
Phase 9 (Sentinel Base & Warden)
    │
    ▼
Phase 10 (Sentinel Stream)
```

---

## Key Milestones

| Milestone | Phase | Significance |
|-----------|-------|--------------|
| Grove exceptional deployments live | 0.1–0.4 | Legacy deployments operational (acknowledged technical debt) |
| Star4 deployed | 0.5 | Star4 bootstrapped; joins standard Phase 1 track |
| Diamond PAUs deployed | 1.1 | EIP-2535 architecture live for first-cohort Primes |
| Synome-MVP + lpla-verify operational | 1.2 | Position monitoring and CRR verification live |
| Core Halos standardized | 1.3 | Legacy assets wrapped or wound down |
| First spell-less Prime deployment | 1.4 | Configurator enables operations without spells |
| First Term Halo (Halo1) live | 1.5 | End-to-end NFAT flow validated |
| Full first cohort (Halo1-Halo6) | 1.6 | Term Halo rollout complete |
| lpla-checker with settlement tracking | 2 | Formalized monthly settlement with beacon oversight |
| Daily settlement live | 3 | Settlement frequency scales |
| srUSDS launch | 4 | First LCTS product; Core Council manages rate |
| First factory-deployed Halo | 5 | Halo creation scales |
| Generator PAU live | 6 | MCD integration simplified |
| First factory-deployed Prime | 7 | Prime creation scales |
| First factory-deployed Generator | 8 | Full factory stack operational |
| First auctions live | 9 | Market-based allocation begins |
| First Sentinel formation active | 9 | Prime automation begins |
| Full autonomous operations | 10 | Human oversight for exceptions only |

---

## Document Index

| Phase | Document | Status |
|-------|----------|--------|
| 0 | [phase-0-legacy-exceptions.md](./phase-0-legacy-exceptions.md) | Draft |
| 1 | [phase1/phase-1-overview.md](./phase1/phase-1-overview.md) | Draft |
| 1 | [phase1/synome-mvp-reqs.md](./phase1/synome-mvp-reqs.md) | Draft |
| 1 | [phase1/halo-book-deep-dive.md](./phase1/halo-book-deep-dive.md) | Draft |
| 2 | [phase-2-monthly-settlement.md](./phase-2-monthly-settlement.md) | Draft |
| 3 | [phase-3-daily-settlement.md](./phase-3-daily-settlement.md) | Draft |
| 4 | [phase-4-lcts-launch.md](./phase-4-lcts-launch.md) | Draft |
| 5 | [phase-5-halo-factory.md](./phase-5-halo-factory.md) | Draft |
| 6 | [phase-6-generator-pau.md](./phase-6-generator-pau.md) | Draft |
| 7 | [phase-7-prime-factory.md](./phase-7-prime-factory.md) | Draft |
| 8 | [phase-8-generator-factory.md](./phase-8-generator-factory.md) | Draft |
| 9 | [phase-9-sentinel-base-warden.md](./phase-9-sentinel-base-warden.md) | Draft |
| 10 | [phase-10-sentinel-stream.md](./phase-10-sentinel-stream.md) | Draft |

---

## Source References

This roadmap draws from the following source documents:

### Smart Contracts
| Document | Relevance |
|----------|-----------|
| `smart-contracts/architecture-overview.md` | Four-layer architecture, PAU pattern, Laniakea Factory |
| `smart-contracts/lcts.md` | LCTS queue system, generation model, settlement integration |
| `smart-contracts/nfats.md` | NFAT Facility structure, queue mechanics, deal lifecycle |
| `smart-contracts/diamond-pau.md` | EIP-2535 faceted architecture |
| `smart-contracts/configurator-unit.md` | aBEAM/cBEAM hierarchy, SORL, timelock mechanics |
| `smart-contracts/rate-limit-attacks.md` | Rate limit attack models and mitigations |
| `smart-contracts/fixed-rates.md` | Fixed-rate yield splitting (PT/YT), LCTS exchange rate interface |

### Trading & Halos
| Document | Relevance |
|----------|-----------|
| `trading/sentinel-network.md` | Sentinel formations, TTS economics, Streaming Accord |
| `sky-agents/halo-agents/portfolio-halo.md` | LCTS-based Portfolio Halos, Halo Classes, lpha-lcts beacon |
| `sky-agents/halo-agents/term-halo.md` | NFAT-based Term Halos, lpha-nfat beacon, buybox model |

### Synomics
| Document | Relevance |
|----------|-----------|
| `synomics/macrosynomics/beacon-framework.md` | Beacon taxonomy (LPLA/LPHA/HPLA/HPHA), naming conventions |

### Accounting
| Document | Relevance |
|----------|-----------|
| `accounting/daily-settlement-cycle.md` | Settlement timing, auctions, tug-of-war, LCTS integration |
| `accounting/tugofwar.md` | Tug-of-war algorithm for duration capacity allocation |
| `accounting/genesis-capital.md` | Genesis Capital, Aggregate Backstop Capital, insolvency defense hierarchy |
| `accounting/risk-capital-ingression.md` | Ingression curves, quality multipliers — relevant from Phase 4 |
| `accounting/forecast-model.md` | Financial projections, TMF waterfall modeling |

### Whitepaper
| Document | Relevance |
|----------|-----------|
| `whitepaper/sky-whitepaper.md` | Architecture overview, risk framework, loss absorption waterfall |
| `whitepaper/appendix-c-treasury-management-function.md` | TMF mechanics — backstop targets, revenue allocation |

---

## Beacon Taxonomy Quick Reference

| Profile | Power | Authority | Examples | Phase |
|---------|-------|-----------|----------|-------|
| **LPLA** | Low | Low | lpla-verify (Phase 1), lpla-checker (Phase 2+), lpla-report | 1+ |
| **LPHA** | Low | High | lpha-relay, lpha-nfat, lpha-attest, lpha-council, lpha-lcts, lpha-auction | 1-4 |
| **HPLA** | High | Low | hpla-trade (private capital trading) | — |
| **HPHA** | High | High | stl-base, stl-stream, stl-warden | 9-10 |

**Sentinels** are a distinguished HPHA subclass with continuous real-time control over Synomic Agents (Primes, Halos).

---

## Glossary of Key Terms

| Term | Definition |
|------|------------|
| **PAU** | Parallelized Allocation Unit (Controller + ALMProxy + RateLimits) |
| **LCTS** | Liquidity Constrained Token Standard (queue-based token conversion) |
| **NFAT** | Non-Fungible Allocation Token (bespoke deal claim) |
| **srUSDS** | Senior Risk Capital token (Generator-level, via LCTS) |
| **OSRC** | Originated Senior Risk Capital (Core Council-originated initially; auction-allocated once stl-base is live) |
| **Tug-of-war** | Algorithm for allocating duration capacity to existing reservations |
| **Lindy** | Liability duration measurement based on USDS lot ages |
| **cBEAM** | Configurator BEAM (operational role for GovOps) |
| **aBEAM** | Admin BEAM (Core Council role, manages inits) |
| **SORL** | Second-Order Rate Limit (25%/18h constraint on increases) |
| **TTS** | Time to Shutdown (warden detection latency) |
| **Halo Class** | Grouping of Halo Units sharing PAU, beacon, and legal framework |
| **Buybox** | Acceptable parameter ranges for NFAT deals within a Facility |
