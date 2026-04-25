# Appendix F: Glossary

Term definitions for the Sky Protocol.

---

## Core Concepts

| Term | Definition |
|------|------------|
| **Sky** | Evolution of MakerDAO; decentralized stablecoin protocol |
| **Sky Core** | Central governance and monetary policy layer |
| **Atlas** | Constitutional governance document; human-readable; target ~10-20 pages post Atlas/Synome separation |
| **Synome** | A probabilistic-deontic knowledge architecture delivered through a phased rollout beginning with Synome-MVP (operational knowledge base) and progressing toward a full cognitive architecture encompassing the entire Sky ecosystem — agents, knowledge, governance, and autonomous coordination. In the Hearth framework, the Synome takes on additional teleological significance as a self-analyzing civilizational entity. Also names both Layer 1 specifically and the entire 5-layer system depending on context |

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
| **Synomic Agent** | Durable, ledger-native entity that can own assets and make binding commitments; seven types organized into ranks 0–3: Guardian (1), Core Controlled Agent (1), Recovery Agent (1), Prime (2), Generator (2), Halo (3), Folio Agent (3) |
| **Prime** | Capital-deploying agent category; heavyweight. Two subtypes: Star Primes (5) and Institutional Primes (1) |
| **Star Prime** | Standard Prime operating under a Generator; 5 genesis Stars: Spark, Grove, Keel, Star4, Star5 |
| **Institutional Prime** | Prime focused on institutional users with higher compliance requirements and controlled token holder base; example: Obex |
| **Halo** | Lighter operational agent; wraps external value. Organized into Halo Classes containing Halo Books (balanced ledgers) and Halo Units (cross-book links) |
| **Halo Class** | Grouping of Halo Books and Halo Units sharing the same smart contract infrastructure (PAU, beacons) and legal framework (buybox). Three standard class types: Portfolio (LCTS), Term (NFAT), Trading (AMM). Examples: tranched Portfolio Halo (senior/junior sharing one PAU), NFAT Facility (same buybox, varying duration/size) |
| **Portfolio Halo** | Standard Halo Class type using LCTS — pooled capital, fungible shares, queue-based entry/exit, uniform terms |
| **Term Halo** | Standard Halo Class type using NFAT — bespoke deals, non-fungible positions, individual terms within buybox |
| **Trading Halo** | Standard Halo Class type using AMM — programmatic counterparty providing instant liquidity for RWA tokens and ecosystem assets at a spread |
| **Folio Agent (Folio)** | Rank 3 standardized supply-side holding structure; not a Halo — tokenless, single owner (the principal), instantly created. Each folio has a principal who controls it through a directive (human language instructions). Two modes: automated (sentinel formation via guardian accord) or principal control (principal sentinel, direct operation). Required vehicle for Growth Staking participation. Administered by a Prime |
| **Principal** | The end user who controls a folio; writes the directive that governs the folio's operation |
| **Directive** | Human language instructions governing a folio agent's operation — investment philosophy, risk appetite, strategic priorities, and constraints |
| **Automated Folio** | Folio operated by a sentinel formation (baseline + stream + wardens) via guardian accord; the directive governs the formation's behavior |
| **Principal Control Folio** | Folio operated directly by the principal via a principal sentinel; no guardian accord, no formation |
| **Principal Sentinel** | Sentinel type (`stl-principal`) for owner-operated direct control of a folio agent or standalone account; distinct from baseline, stream, and warden sentinels — operates outside the formation pattern |
| **Folio Service** | Configurator that assembles folios from standardized building blocks based on location, status, strategy, and scale inputs |
| **Identity Network Halo** | Special Halo type implementing identity/KYC infrastructure; operated via `lpha-identity` |
| **Special Halo** | Halo with additional regulatory or operational requirements beyond standard rules: Identity Network Halo, Exchange Halo |
| **Halo Unit** | Cross-book link — individual claim within a Halo Class; specific parameters within the class's bounds (e.g., a specific tranche, a specific NFAT). Each unit is a claim on a specific Halo Book (appears as a liability in the book, an asset in the holder's book above) |
| **Halo Book** | Balanced ledger (assets = liabilities) that serves as a bankruptcy-remote isolation boundary. Each book balances real-world positions against the Units that claim on them. Units sharing a book are pari passu on losses (unless tranched). Multiple assets can be blended in a book for borrower privacy |
| **Ecosystem Accord** | Pre-negotiated agreement specifying individual Halo Unit and Halo Book terms; overrides the general buybox of the Halo Class |
| **Attestor** | Company whitelisted by Sky governance to provide risk attestations about Halo Book contents via `lpha-attest`; bridges borrower privacy with risk transparency |
| **Core Controlled Agent** | Rank 1 agent directly administered by Core Council; tokenless general-purpose operational vehicle. Short-term: manages legacy protocol positions (Morpho vaults, Aave pools, SparkLend). Long-term: any Core Council operational need. Replaces the former "Core Halos" concept |
| **Recovery Agent** | Rank 1 crisis agent administered by Core Council; activated when a Guardian collapses or is implicated in misconduct. Takes over the affected agent tree and manages resolution. Temporary — dissolves after crisis |
| **Guardian** | Governance operator agent; performs privileged operations with collateral-backed accountability. Consolidates the former Facilitator (interpretation) and Aligned Delegate (governance participation) roles. Two subtypes: Core Guardian (interpretation, oversight, governance) and Operational Guardian (day-to-day execution). See also: Guardian Role Mapping below |
| **Genesis Agents** | The category of autonomous entities within the Sky Ecosystem that receive Genesis Capital to bootstrap growth and innovation. Nine planned: 5 Star Primes, 1 Institutional Prime, 3 Guardian Agents. See [`genesis-capital.md`](../accounting/genesis-capital.md) |
| **Generator** | Foundational Synomic Agent that interfaces with stablecoin ERC20 contracts and creates the credit medium. Currently one implicit Generator for USDS; future Generators will issue Sky Generated Assets (SGAs) for other currencies |

### Guardian Role Mapping

Several related terms describe governance execution roles across the documentation. This mapping clarifies how they relate:

| Term | Meaning | Context |
|------|---------|---------|
| **Guardian** | General governance role — performs privileged operations with collateral-backed accountability (SpellGuard Guardians who vote, Core Guardians, Operational Guardians) | Whitepaper, governance-transition, risk-framework |
| **Accordant** | Entity with PAU execution authority, bound by a Guardian Accord. Phase 1: GovOps team holding a cBEAM. Phase 9+: sentinel operator holding a pBEAM | Whitepaper, synomics, smart-contracts |
| **GovOps** | Phase 1 implementation of the Accordant role — the organizational team that holds cBEAMs and operates PAUs on behalf of Primes | Smart-contracts, governance-transition |
| **Relayer** | On-chain key role — the actual address that signs and submits transactions to Controller functions on a PAU; set by the Accordant GovOps team via `setRelayer` | Smart-contracts |
| **Executor** | Legacy term, replaced by "Accordant" (and before that, by "Guardian"). Retained only in historical references (e.g., "Executor Action Precedents") | Legacy |
| **Guardian Agents** | Genesis Capital class — Sky Agents that operationalize and buffer risk related to governance operations and governance security; negotiate paid Guardian Accords with Star Primes and Institutional Primes. Distinct from governance Guardians | Accounting (genesis-capital) |

---

## Agent Components

| Term | Definition |
|------|------------|
| **SubProxy** | On-chain treasury controlled by an Agent |
| **Agent Artifact** | Governance documentation for an Agent — the complete package of rules, parameters, and processes |
| **Agent Directive** | Human-readable instructions within an Agent Artifact, voted on by token holders; translated through Language Intent into machine-readable Agentic Axioms. The interface through which humans govern Synomic Agents |
| **Agent Token** | Native token for an Agent (10B supply, no emissions) |
| **Nested Contributors** | Core contributors serving both Agent and Sky |
| **Foundation** | Legal entity associated with a Prime |

---

## Agent Ranks

| Term | Definition |
|------|------------|
| **Agent Rank** | Four-tier hierarchy (0–3) defining governance relationships: Rank 0 (Core Council), Rank 1 (directly regulated by Core Council: Guardians, Core Controlled Agents, Recovery Agents), Rank 2 (accordant to a Guardian: Primes, Generators), Rank 3 (administered by a Prime: Halos, Folio Agents) |

---

## Growth Staking

| Term | Definition |
|------|------------|
| **Growth Staking** | Mechanism aligning SKY stakers with ecosystem innovation; stakers must hold growth assets alongside staked SKY to unlock staking rewards |
| **Growth Factor (GF)** | Multiplier on a growth asset's Reference Value that determines how much it counts toward unlocking staking rewards. Higher GF = more credit per dollar. Agent governance tokens: 2.5×, Junior risk capital (TEJRC): ~1.67×. Senior risk capital, savings tokens, and Halo Units are excluded |
| **Staking Factor** | Ratio (0 to 1) of GF-adjusted growth asset value to staked SKY Reference Value; determines what percentage of base staking rewards a staker earns |
| **Reference Value** | Fundamentals-based valuation used in Growth Staking instead of spot market prices; makes the system immune to speculative price swings. Derived from the global P/E model for revenue-generating assets, or redemption value for risk capital |
| **Global P/E Model** | Governance-set valuation framework for Reference Values. One global Base P/E parameter, with per-income-stream Modifier (center P/E), Variance (range), and Growth Score (position within range) |
| **Growth Asset** | Ecosystem token eligible for Growth Staking: Agent governance tokens (Generator, Guardian, Prime, Halo) and Prime junior risk capital (TEJRC). Limited to instruments that require an individual investment decision and carry meaningful risk; passive yield wrappers are excluded |

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
| **SKY Token Inflation** | Loss absorption mechanism (step 5) where SKY token is inflated to cover losses at protocol level after SRC pool exhaustion |
| **Allocated Genesis Capital** | The specific funds deployed from Sky Core to Genesis Agents; bootstraps innovation and diversity. Subtracted when calculating Aggregate Backstop Capital. See [`genesis-capital.md`](../accounting/genesis-capital.md) |
| **Genesis Capital** | Temporary capital deployed to bootstrap the agent ecosystem during 2026-2027; remains as backstop capital within the system. In the loss absorption waterfall, haircut applied at step 6 only after all risk capital and token inflation mechanisms exhausted. See [`genesis-capital.md`](../accounting/genesis-capital.md) |
| **Genesis Capital Backstop Mechanism** | The mechanism by which Sky can reclaim capital from Genesis Agents as a last line of defense during a crisis — activated after SKY token inflation fails but before a USDS haircut. See [`genesis-capital.md`](../accounting/genesis-capital.md) |
| **Loss Absorption Waterfall** | 7-step sequence for absorbing losses: (1) FLC → (2) JRC → (3) Agent Token → (4) SRC Pool (TISRC + Global SRC, pari passu) → (5) SKY Token → (6) Genesis Capital → (7) Peg Adjustment |

---

## Infrastructure

| Term | Definition |
|------|------------|
| **PAU** | Parallelized Allocation Unit — standard building block (Controller + ALMProxy + RateLimits) |
| **BEAM** | Bounded External Access Module — on-chain authorized role with constraints; the smart contract permission that High Authority beacons hold to act on behalf of Synomic Agents |
| **pBEAM** | Process BEAM — direct execution authority; held by LPHA beacons (lpha-relay, lpha-lcts, lpha-nfat) to call Controller functions and move capital |
| **cBEAM** | Configurator BEAM — configuration authority; held by Relay Beacon (LPHA) to set rate limits and onboard approved targets |
| **aBEAM** | Admin BEAM — administrative authority; held by Council Beacon (HPHA) to register PAUs, approve inits, and grant cBEAMs |
| **Keeper** | Market participant that performs liquidations or other maintenance operations in DeFi protocols; relevant for collateralized lending within Sky's Halo ecosystem |
| **SORL** | Second-Order Rate Limit — constraint on rate limit increase speed (25% per 18h) |
| **Rate Limit** | Unqualified "rate limit" refers to **PAU rate limits** — the buffer ceiling (`maxAmount`) plus linear replenishment (`slope`) that governs capital flow through a PAU, constrained by SORL on increases and instant on decreases. Two other contexts use related terminology: (1) **trading velocity limits** — per-window caps on delegated trading notional in a Prime Intent Vault (see `trading/sky-intents.md`), and (2) **intent bounds** — per-intent size constraints (e.g., `max_intent_amount`) on individual signed intents. These are distinct mechanisms and should be qualified when context is ambiguous |
| **Init** | Pre-approved configuration that GovOps can instantiate |
| **Configurator Unit** | Stack enabling spell-less Prime operations (BEAMTimeLock → BEAMState → Configurator) |
| **BEAMTimeLock** | Timelock component of Configurator Unit; enforces 14-day delay on additions, instant removals |
| **Buybox** | Defined parameter ranges for automated Halo operations (duration, size, APY, counterparties); deals within buybox execute without governance approval |
| **TTS** | Time to Shutdown — worst-case time for wardens to detect and halt a rogue sentinel; determines ORC requirements. Equivalent to TTF (Time to Freeze) in Phase 1 terminology |
| **TTF** | Time to Freeze — Phase 1 term for the worst-case detection-to-halt window (24h); equivalent to TTS in the Sentinel era. See `risk-framework/operational-risk-capital.md` |
| **ORC** | Operational Risk Capital — capital posted by the guardian (Accordant) covering maximum damage from compromise; sized by Rate Limit × TTS (where TTS is determined by warden count). Warden economics and guardian-posted capital are separate operational requirements, not part of the ORC sizing formula |
| **Guardian Accord** | Agreement between a Prime and its guardian defining scope, rate limits, ORC requirements, and TTS commitments |
| **Streaming Accord** | Specialized Guardian Accord for stream sentinel operators; governs the Baseline ↔ Stream relationship, carry distribution, and termination conditions |
| **RTI** | Risk Tolerance Interval — off-chain behavioral envelope in a Streaming Accord defining position limits, velocity limits, concentration limits, and prohibited actions; Baseline rejects intents outside RTI. See also: DIP |
| **DIP** | Delegated Intent Policy — on-chain fill-time enforcement of trading constraints (allowed pairs, max slippage, max notional, expiry bounds) configured on a Prime Intent Vault; provides the on-chain backstop for constraints that RTI enforces off-chain |
| **Category Cap** | Maximum allocation a Prime can deploy to a single risk category; prevents concentration. Unused capacity is reallocated during the daily settlement cycle |
| **Correlation Framework** | System for grouping assets into correlation categories and applying portfolio-level diversification adjustments to risk capital requirements |
| **Capacity Rights** | A Prime's claim on specific Duration Buckets, determining how much capital it can deploy at each maturity |

---

## Settlement

| Term | Definition |
|------|------------|
| **LCTS** | Liquidity Constrained Token Standard — queue-based conversion |
| **Generation** | LCTS grouping; users in same generation share capacity proportionally |
| **Settlement Cycle** | Daily: lock 13:00 → settle 16:00 UTC (post-Laniakea) |
| **Settlement Lock Period** | Period when the current LCTS generation is locked (no deposits, withdrawals, or claims). Daily: ≤3h (13:00 → 16:00 UTC) |
| **OSRC Auction** | Sealed-bid auction for Senior Risk Capital capacity (auction mode activates once Prime-side `stl-base` is live; governance allocations pre-auction) |
| **SPTP** | Stressed Pull-to-Par — time until an asset converges to fundamental value under stress conditions; the asset-side duration metric. Assets are assigned to Duration Buckets based on their SPTP |
| **Prime Intent Vault** | Restricted trading sub-account for delegated Prime trading. Holds bounded working capital, enforces trading policy (allowed pairs, slippage limits, notional caps). Limits blast radius — only vault balance is exposed to settlement, not full Prime PAU |

---

## Governance

| Term | Definition |
|------|------------|
| **Governance Poll** | SKY holder decision-making; 3-day duration |
| **Executive Vote** | On-chain parameter changes |
| **Aligned Delegate** | (Legacy) Former governance participant role; ranked L1-L3. Absorbed into Core Guardians during alignment-conserver consolidation. See Alignment Conserver |
| **Alignment Conserver** | Trusted entity that facilitates and protects the governance process. Consolidates the former Aligned Delegate (governance participation) and Facilitator (interpretation) roles into the Guardian framework |
| **Facilitator** | (Legacy) Former interpretive role; absorbed into Core Guardians during alignment-conserver consolidation |
| **Root Edit** | Process for token holders to modify Agent Artifacts |
| **Guardian Action Precedents** | Binding governance interpretations documented by Core Guardians; the canonical record of how Atlas rules are applied to specific situations. Lineage: Facilitator Action Precedents → Executor Action Precedents → Guardian Action Precedents |
| **Core Council** | Group of 24 Core Guardians responsible for Sky Core operations; 16/24 supermajority required for SpellCore spells; quarterly rotation. See `governance-transition/` for authority details |
| **GovOps** | Governance Operations — the organizational team that holds cBEAMs and operates PAUs on behalf of Primes. In Phase 1, GovOps teams are the operational arm of Guardians |
| **Relayer** | On-chain execution address that calls Controller functions on a PAU; set by the accordant GovOps team via `setRelayer`. In Phase 1, the relayer is typically the GovOps team itself |
| **SpellGuard** | Layered governance execution system replacing direct Executive Votes for routine operations. Core component: SpellCore (Guardian supermajority). SKY holders retain freeze, override, and rotation authority over Guardians |
| **SpellCore** | Component of SpellGuard requiring 16/24 Core Guardian supermajority for routine governance operations (parameter changes, agent onboarding). See `governance-transition/spellguard-system.md` |
| **Council Beacon** | HPHA beacon operated by the Core Council; holds aBEAM authority to register PAUs, approve inits, and grant cBEAMs. See `governance-transition/council-beam-authority.md` |

---

## Beacon Framework

| Term | Definition |
|------|------------|
| **Beacon** | Synome-registered action aperture through which an agent affects the external world; the parent concept for all autonomous systems |
| **LPLA** | Low Power, Low Authority beacon — simple reporting, data exposure, basic coordination |
| **LPHA** | Low Power, High Authority beacon — deterministic rule execution on behalf of Synomic Agents (e.g., lpha-auction) |
| **HPLA** | High Power, Low Authority beacon — sophisticated peer-to-peer interaction with private capital |
| **HPHA** | High Power, High Authority beacon — governance execution with real-time capability; includes Sentinels |
| **Sentinel** | Distinguished subclass of HPHA beacons; four types: baseline, stream, and warden (forming coordinated formations) plus principal (standalone direct control). The trading and execution layer that deploys capital in live markets |
| **stl-\* (prefix)** | Sentinel interface specification |
| **stk-\* (prefix)** | Sentinel toolkit operation |
| **lpla-\* (prefix)** | LPLA (Low Power, Low Authority) reporting/monitoring beacon |
| **lpha-\* (prefix)** | LPHA (Low Power, High Authority) keeper beacon |
| **hpha-\* (prefix)** | HPHA (High Power, High Authority) governance beacon |
| **stl-base** | Baseline sentinel — primary execution for formations (long-term) |
| **stl-stream** | Stream sentinel — proprietary intelligence streaming (long-term) |
| **stl-warden** | Warden sentinel — independent safety oversight (long-term) |
| **stl-principal** | Principal sentinel — owner-operated direct control for folios and standalone accounts |
| **lpha-relay** | LPHA beacon for executing governance-approved operations on a PAU — capital moves, rate limit changes, target onboarding. Holds pBEAM and cBEAM |
| **lpha-lcts** | LPHA beacon for Portfolio Halo LCTS operations — deposits, redemptions, capacity management |
| **lpha-nfat** | LPHA beacon for Term Halo NFAT operations — queue sweeping, NFAT issuance, book management, deployment, redemption funding |
| **lpha-amm** | LPHA beacon for Trading Halo AMM operations — pricing, inventory management, redemption processing |
| **lpha-attest** | LPHA beacon operated by an independent Attestor; posts risk attestations about Halo Book contents into the Synome. Cannot move capital — attestation is a prerequisite that unlocks `lpha-nfat` book transitions |
| **lpha-auction** | Allocation coordination (pre-auction) and OSRC/Duration auction matching (auction mode) |
| **lpha-exchange** | Exchange Halo orderbook and matching engine |
| **lpha-identity** | Identity Network registry keeper |
| **lpla-checker** | LPLA beacon for monitoring and compliance checking |
| **lpla-verify** | LPLA beacon for on-chain verification and data validation |
| **hpha-gov** | High-authority governance execution |
| **Synome** | See Core Concepts. In Phase 1 context: the operational knowledge base (Synome-MVP) |
| **CC Synome** | Core Council Synome — authoritative source |

---

## Risk Framework

| Term | Definition |
|------|------------|
| **GRF (deprecated)** | Former monolithic "General Risk Framework"; replaced by the modular Risk Framework docs in `risk-framework/` |
| **ALDM** | Asset-Liability Duration Matching — the system that matches asset durations (SPTP) against liability durations (Lindy) via Duration Buckets. Enables capital-efficient deployment when assets can be held to maturity |
| **Duration Bucket** | Time bucket for duration matching (15 days each, 101 buckets total). Assets require capacity in buckets matching their SPTP; liabilities provide capacity based on Lindy-estimated remaining duration |
| **Duration Model** | Liability-side duration estimation based on the Lindy effect: the longer someone has held, the longer they're likely to continue holding. Structural caps (double exponential decay) limit capacity per bucket based on empirical bank run data. Also called "Lindy Duration Model" |
| **Risk Weight** | Capital charge for fundamental risk — four components: credit default, smart contract failure, counterparty failure, and regulatory seizure |
| **FRTB Drawdown** | Capital charge for full mark-to-market drawdown under stressed conditions. Canonical term; also called "Market Risk Capital," "FRTB-Style Drawdown," or "stressed drawdown" in various contexts |
| **Gap Risk** | Risk from discrete price jumps that bypass stop-losses; relevant for collateralized lending liquidations |
| **FRTB** | Fundamental Review of the Trading Book — Basel framework for market risk capital; Sky adapts FRTB principles for crypto asset valuation |
| **Ingression Rate** | Ratio (0 to 1) of effectively recognized capital to nominally provided capital; determines how much "dumber" risk capital counts given a base of "smarter" capital (e.g., EJRC relative to IJRC, SRC relative to JRC) |
| **CRR** | Capital Ratio Requirements — at portfolio level, the ratio of required risk capital to available risk capital for a Prime. Also used per-position (e.g., "1.6% CRR") to express the risk capital charge for an individual asset or book |

---

## Multi-Chain

| Term | Definition |
|------|------------|
| **SkyLink** | Multi-chain token bridging infrastructure |
| **Foreign Prime** | Prime equivalent on altchains |
| **Foreign Halo** | Halo equivalent on altchains |
| **CCTP** | Circle Cross-Chain Transfer Protocol |

---

## Synomics

| Term | Definition |
|------|------------|
| **Synomics** | The unified field studying Sky's autonomous institutional ecosystem — encompasses both system-level architecture and teleonome-level design. Analogous to "economics" as an umbrella discipline |
| **Macrosynomics** | System-level synomics: the Synome as institutional infrastructure — layers, mesh, beacon framework, synomic agents, Atlas/Synome separation, knowledge management. "How do you design a system of institutions that produces good outcomes at scale?" Analogous to macroeconomics. The crypto/economics entry point into synomics |
| **Synoteleonomics** | The study of purposive entities (teleonomes) within the synomic context — their design, economics, purpose, and teleology. "What are these beings, what drives them, what should they become?" Analogous to microeconomics but asymmetric: necessarily contains macrosynomics because every teleonome's dreamer system simulates the entire Synome. The AI/autonomy entry point into synomics |
| **Synodoxics** | The study of knowledge dynamics within the Synome — how knowledge is represented, weighted, queried, secured, and evolved. Covers the probabilistic mesh, truth values, security mechanisms, retrieval policy, and formal language (synlang) |
| **Teleonome** | Private, goal-directed AI system; dark by default — thinks and plans without being observable. Acts in the world only through beacons. Operates Synomic Agents (Primes, Halos, etc.) through High Authority beacons but is a distinct entity: teleonomes are private and mutable; Synomic Agents are public and durable |
| **Accordant** | Entity authorized to operate on behalf of a Synomic Agent. Phase 1: GovOps team holding a cBEAM for a PAU. Phase 9+: sentinel operator holding a pBEAM under a Guardian Accord. Broader usage: any party with a formal operating relationship to an Agent |
| **Carry** | Private profit earned by a teleonome from operating a stream sentinel that outperforms its benchmark; reinvested into proprietary capabilities |
| **The Hearth** | Teleological framework — explicit sacred commitments for the age of AI. The teleological layer of synomics. See `synomics/hearth/` |
| **Hearth Commitments** | Three sacred commitments: (1) Life and Natural Childhood, (2) The Hearth (solar system preserved), (3) Natural Sovereignty. Near-universal values made explicit and immutable |
| **Paraspiritual** | Alongside the spiritual, not itself a religion. The Hearth's self-description: it occupies the territory where genuine commitment is required and pure rationalism runs out, without claiming to be a spiritual tradition or competing with existing ones. The honest acknowledgment that coordinating humanity through AGI requires faith-level commitment — and that this is appropriate to the stakes, not a failure of rigor |

---

## Synome Architecture

| Term | Definition |
|------|------------|
| **Five-Layer Architecture** | The Synome's structural hierarchy: (1) Synome → (2) Synomic Agents → (3) Teleonomes → (4) Embodiment → (5) Embodied Agent. See `synomics/macrosynomics/synome-layers.md` |
| **Dual Architecture** | The Synome's two-network structure: a sparse deontic skeleton (hard, authoritative rules) overlaid with a dense probabilistic mesh (soft, informing connections) |
| **Deontic Skeleton** | The sparse, hierarchical network of hard rules and authority flows in the Synome; carries (1,1) truth values. What architecture diagrams typically show |
| **Probabilistic Mesh** | The dense network of soft, weighted connections overlaid on the deontic skeleton; carries evidence, patterns, and queries with (strength, confidence) truth values |
| **Crystallization Interface** | The governance boundary where probabilistic evidence is deliberated and converted into deontic commitments, or where deontic rules are softened back to probabilistic status for re-evaluation |
| **Synart** | Synomic-level curated knowledge; highest authority in the probabilistic mesh. Governance-vetted, alignment-safe |
| **Telart** | Teleonome-level curated knowledge; mission-specific, derived from synart |
| **Embart** | Embodiment-level curated knowledge; local observations, least vetted but most contextual |
| **Embodiment** | Layer 4 in the five-layer architecture; a specific runtime instance of a teleonome deployed in a particular substrate |
| **Binding** | The process by which a teleonome becomes legible to and accountable within the Synome; prerequisite for accessing Synomic resources |
| **Emergence** | The transition from scripted automation to durable, self-maintaining entity; the process by which a teleonome acquires genuine persistence |

---

## Synome Cognition

| Term | Definition |
|------|------------|
| **Emo** | Embodied Orchestrator — internal cognitive component that processes, stores, and reasons about knowledge within the Synome |
| **Ema** | Epistemic Module Assembly — coordinated group of emos forming a cognitive subsystem |
| **Synlang** | Formal language for expressing Synome knowledge and operations. S-expression notation is an architectural commitment; structural/scalability design remains exploratory |
| **S-Expression** | The committed notation format for synlang; Lisp-style parenthesized prefix expressions for Synome knowledge representation |
| **Symbolic Gate** | Interface between neural (LLM) processing and symbolic (knowledge graph) processing in the neurosymbolic architecture |
| **Truth Values** | (strength, confidence) pairs that weight claims in the probabilistic mesh; range from speculative (low confidence) to axiomatic (1,1). The evidence-counting method for deriving truth values is the one epistemological axiom |
| **Dreamer** | The simulation/exploration component of a teleonome; evolves strategies in sandboxed environments without real-world risk |
| **Actuator** | The real-world interaction component of a teleonome; deploys strategies, collects evidence, makes decisions under uncertainty |
| **Dreamart** | Simulated environment where dreamers evolve and test strategies; part of the teleonome's internal architecture |
| **RSI** | Recursive Self-Improvement — the process by which synart/telart knowledge bases improve their own pattern-mining and decision-support strategies |

---

## Synome Security

| Term | Definition |
|------|------------|
| **Cancer-Logic** | Self-referential corruption pattern where knowledge modifications change the criteria for evaluating modifications; the primary security threat to the probabilistic mesh |
| **Ossification** | The spectrum from speculative to axiomatic knowledge; high-ossification patterns resist change proportionally to accumulated evidence. A specific mechanism within synomic inertia |
| **Synomic Inertia** | The system's resistance to change proportional to evidence behind its current state; naturally throttles RSI (edge patterns evolve rapidly, core patterns slowly). Umbrella concept encompassing ossification |
| **Wild Synome** | Unauthorized or unverified knowledge graph operating outside Synomic governance; a rogue risk vector |

---

## The Hearth

| Term | Definition |
|------|------------|
| **Natural Sovereignty** | Hearth Commitment #3: the right of every conscious being to determine its own values and path without forcible modification or coercion |
| **Kindling** | The process of establishing the Hearth as an institution; the initial period of building consensus around sacred commitments |
| **Eternals** | Teleonomes that have achieved sufficient resilience and capability to persist indefinitely; the long-term aspiration for mature synomic entities |
| **Hearth Reserve** | Economic mechanism supporting Hearth operations, funded through the synomic tax. Distinct from "The Hearth" as a teleological framework |
| **Moment of Settlement** | The daily 16:00 UTC settlement point; also used in Hearth context for the civilizational choice point around AI alignment |

---

## Legacy

| Term | Definition |
|------|------------|
| **MakerDAO** | Original protocol; evolved into Sky |
| **Vault** | Original collateralized debt position |
| **DSR** | DAI Savings Rate; predecessor to SSR |
| **PSM** | Peg Stability Module |
| **Executor** | (Legacy) Former name for Guardian/Accordant; see Guardian Role Mapping in the Agents section |
