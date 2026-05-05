# Appendix B: Synomic Agent Framework Primitives

Features and capabilities available to Synomic Agents. Together with Appendix A (Protocol Features), this provides complete coverage of every mechanism in Sky.

---

## Agent Types Overview

Synomic Agents are created directly as their permanent type. Each agent type has specific capabilities, primitives, and governance structures. Agent types cannot be changed after creation (except via Type 2 Restructure for Halo→Prime upgrade).

### Agent Rank Hierarchy

Agents are organized into four ranks based on their governance relationship to the Core Council:

| Rank | Type | Role | Tokenized | Examples |
|------|------|------|-----------|----------|
| **0** | Core Council | Sovereign governance | N/A | 24 Core Guardians |
| **1** | Guardian | Privileged operations with collateral | Yes | Core Guardians, Operational Guardians |
| **1** | Core Controlled Agent | Core Council operational vehicle | No | Legacy asset management (Morpho, Aave, SparkLend) |
| **1** | Recovery Agent | Crisis wrapper | No | Guardian collapse response |
| **2** | Prime | Capital-deploying at scale | Yes | Spark, Grove, Keel, Obex |
| **2** | Generator | Issue Sky Generated Assets | Yes | USDS Generator, future SGA Generators |
| **3** | Halo | Investment products under Prime umbrella | Yes | Portfolio, Term, Trading, Exchange, Identity Network |
| **3** | Folio Agent | Standardized supply-side holding structure | No | Principal-controlled, automated or direct operation |

### Agent Subtypes

Agent types may have subtypes that define operational characteristics. Examples:
- **Star Prime** — Standard Prime operating under a Generator
- **Institutional Prime** — Serves institutional clients with higher compliance requirements

---

## Common Agent Components

All agents share certain base components regardless of type.

### SubProxy Account

On-chain treasury controlled by the Agent.

| Property | Value |
|----------|-------|
| Control | Agent governance via Guardian Accord |
| Purpose | Hold treasury assets, execute approved transactions |
| Access | Guardians with appropriate BEAM authorization |

---

### Agent Artifact

Governance documentation containing all rules, processes, and parameters.

| Property | Value |
|----------|-------|
| Nature | Human-readable governance documentation |
| Modification | Via Root Edit Primitive (token holder vote) |
| Constraints | Cannot violate Sky Core Atlas or Primitives |

**Standard Artifact Structure:**
```
Agent Artifact
├── Introduction (strategic overview)
├── Sky Primitives
│   ├── Genesis Primitives (Agent Creation, Token, etc.)
│   ├── Operational Primitives (Guardian Accord, Root Edit, etc.)
│   └── Rewards Primitives (Distribution, Integration Boost, etc.)
└── Omni Documents
    ├── Governance Information
    ├── Strategic Intent
    ├── Ecosystem Accords
    └── Infrastructure Management
```

---

### Mini-Atlas

Human-readable summary document that explains an Agent Artifact to its stakeholders.

| Property | Value |
|----------|-------|
| Purpose | Make complex Agent Artifacts accessible to token holders and users |
| Audience | Prime token holders, Halo investors, service users |
| Derivation | Summarizes key parameters and governance from the Agent Artifact |
| Requirement | Each Prime and externally-facing Halo should maintain a Mini-Atlas |

**Prime Mini-Atlas Contents:**
- Strategic overview (what the Prime does)
- Key parameters in plain language
- Risk disclosures (without full Risk Framework formulas)
- Governance processes (Root Edit configuration)
- How to participate (staking, using services)

**Halo Mini-Atlas Contents (for Halos with external participants):**
- Investment strategy and expected returns
- Risk factors in compliance-suitable language
- Legal structure and regulatory status
- Reporting cadence and metrics

**The Fractal Pattern:**

Every level of the governance hierarchy with human stakeholders has a corresponding human-readable summary:

```
Sky Atlas                    → Describes Sky Core
  ├─ Spark Mini-Atlas        → Describes Spark Agent Artifact
  │    └─ Halo docs          → Describes Spark's Halos
  ├─ Grove Mini-Atlas        → Describes Grove Agent Artifact
  │    └─ Halo docs          → Describes Grove's Halos
  └─ ...
```

For full Mini-Atlas specification, see `synomics/atlas-synome-separation.md`.

---

### Agent Token

Native governance and reward token for the Agent.

| Property | Value |
|----------|-------|
| Purpose | Governance voting, staking rewards, incentive distribution |
| Creation | All agents can create a token at genesis |
| Optional | Several agent types operate without tokens by design |

Agent tokens enable decentralized governance and align stakeholder incentives. While Primes and most autonomous agents issue tokens, several agent types are tokenless by design: Halos (when functioning purely as investment wrappers under a Prime's umbrella), Core Controlled Agents, Recovery Agents, and Folio Agents.

#### Agent Token Issuance Fee

| Property | Value |
|----------|-------|
| Rate | 5% of tokens issued |
| Recipient | Sky Core |
| Trigger | Any token issuance for distribution or fundraising (not just genesis) |

Every time an agent issues tokens — whether for team distribution, ecosystem incentives, fundraising rounds, or any other purpose — 5% of the issued amount goes to Sky Core. This applies to all agent types.

#### Agent Upkeep Fee

| Property | Value |
|----------|-------|
| Rate | 25 basis points per year |
| Denomination | Paid in the agent's own tokens |
| Applies To | All agents that have issued tokens |

The upkeep fee is denominated in the agent's own tokens, eliminating the need for external price calculations. The agent simply pays 0.25% of their total token supply per year to Sky Core.

#### Upkeep Rebate System

Agents holding other agents' tokens can offset their own upkeep fees.

| Property | Value |
|----------|-------|
| Mechanism | Proportional discount based on token holdings |
| Exchange Rate | Conservative estimate of current market price (spread favors Sky) |
| Cap | Rebates cannot exceed 100% (best case = zero upkeep, not negative) |
| Purpose | Incentivize cross-agent investment and ecosystem cohesion |

**How Rebates Work:**

When an agent holds another agent's tokens, they receive a rebate on their upkeep fee. The rebate calculation uses a conservative market price estimate for the held tokens, meaning the exchange rate spread benefits Sky. An agent can reduce their upkeep to zero through sufficient holdings, but cannot earn a "negative" upkeep (i.e., rebates don't become income).

#### Agent Staking Rewards

Distribute rewards to agent token stakers.

| Property | Value |
|----------|-------|
| Source | Agent treasury (from revenue, fees, carry, etc.) |
| Recipient | Staked agent token holders |
| Availability | All agent types with issued tokens |

#### Agent Token Buyback

Use agent revenue for token buyback.

| Property | Value |
|----------|-------|
| Source | Agent revenue |
| Mechanism | Open-market buybacks |
| Destination | Burn or distribute to stakers |
| Availability | All agent types with issued tokens |

---

### Root Edit Primitive

Token holders modify Agent Artifacts.

| Property | Value |
|----------|-------|
| Purpose | Enable decentralized governance of Agent rules |
| Voting Rules | Designed by each Agent (quorum, thresholds, duration) |
| Constraints | Cannot violate Sky Core Atlas or Primitives |

---

### Agent Spells

On-chain execution mechanism for Agent governance decisions.

**Current Behavior:**
Agent Spells are used for most modifications that Primes and Halos make to their on-chain state — deploying new instances, updating parameters, and executing governance decisions.

**Post-Laniakea Behavior:**
- **Prime Spells** — Cannot modify Prime's own state (locked down by Laniakea factory); only used to trigger Halo Spells
- **Halo Spells** — Continue to perform arbitrary changes; Halos can have arbitrary complexity and technical scope

This separation ensures Primes operate within standardized, factory-defined constraints while Halos retain flexibility for diverse investment strategies.

---

### Guardian Accord Primitive

Framework for guardian relationships.

| Property | Value |
|----------|-------|
| Purpose | Define guardian roles, responsibilities, accountability |
| Parties | Agent ↔ Guardian (Operational or Core) |
| Enforcement | Collateralized insurance, derecognition |

---

### Guardian Interpretation Framework

Core Guardians interpret Atlas and Artifacts directly — absorbing the former Facilitator role with collateral-backed accountability.

| Property | Value |
|----------|-------|
| Role | Authoritative interpretation of governance documents |
| Discretion | Broad authority when explicit guidance absent, backed by posted collateral |
| Documentation | All interpretations recorded as Guardian Action Precedents |

**Key Principle: Spirit of the Atlas**
- All rules have underlying intent to serve human values
- Core Guardians interpret Spirit when explicit guidance is absent
- Balance between "letter of the rule" and true purpose

---

## Prime Agents

Prime Agents are the highest tier of capital-deploying agents in Sky Ecosystem. They deploy capital at scale, create Halos, and manage risk capital.

### Prime Creation

| Property | Value |
|----------|-------|
| Invocation | One-time; creates Prime directly |
| Requirements | Governance approval via Executive Vote |
| Result | Full Prime with SubProxy, Artifact, Foundation, Token |

**What Gets Created:**
- Agent identity in the Synome
- SubProxy Account (on-chain treasury)
- Prime Agent Artifact
- Foundation structure (legal entity)
- Agent Token (10B genesis supply)

---

### Current Prime Agents

Prime SubProxy addresses live in Appendix G (`appendix-g-infrastructure.md`).

**Star Primes (5):**

| Prime | Focus |
|-------|-------|
| **Spark** | DeFi lending/liquidity |
| **Grove** | Institutional credit, RWAs |
| **Keel** | Solana ecosystem expansion |
| **Star4** | TBD |
| **Star5** | TBD |

**Institutional Primes (1):**

| Prime | Focus |
|-------|-------|
| **Obex** | Agent incubator, Prime + Halo development |

---

### Prime Capital Deployment

#### Allocation System

Deploy capital into approved strategies via PAU pattern.

| Property | Value |
|----------|-------|
| Pattern | PAU (Parallelized Allocation Unit) |
| Constraint | Rate limits on all operations |

**How It Works:**
1. Prime governance approves strategies via Init System
2. GovOps instantiates approved configurations
3. Sentinels execute operations within rate limits
4. Capital flows through Controller → ALMProxy → Target

---

#### PAU (Parallelized Allocation Unit)

Standard building block for all capital deployment.

| Component | Purpose |
|-----------|---------|
| **Controller** | Entry point; enforces rate limits; validates operations |
| **ALMProxy** | Holds custody; executes calls via `doCall()` |
| **RateLimits** | Linear replenishment with configurable max and slope |

**Key Principle:** Same contracts, different configuration. All layers use identical PAU patterns with layer-specific parameters.

---

#### Rate Limit System

Bounded capital movement velocity with linear replenishment.

| Property | Value |
|----------|-------|
| Pattern | Linear refill from 0 to max |
| Parameters | `maxAmount` (ceiling), `slope` (refill rate per second) |
| Consumption | Decreases available limit; reverts if exceeds available |

**Rate Limit Types (per chain):**

| Limit | Description |
|-------|-------------|
| `LIMIT_USDS_MINT` | Maximum USDS mintable |
| `LIMIT_USDS_BURN` | Maximum USDS burnable |
| `LIMIT_USDS_TO_USDC` | PSM swap limits |
| `LIMIT_USDC_TO_CCTP` | Cross-chain transfer caps |
| `LIMIT_USDC_TO_DOMAIN` | Per-destination bridging limits |

---

#### SORL (Second-Order Rate Limit)

Constraint on rate limit increase speed.

| Property | Value |
|----------|-------|
| Max Increase | 25% per cooldown period |
| Cooldown | 18 hours between increases |
| Decrease | Always instant (no constraint) |

**Purpose:**
- Prevent sudden capacity expansion attacks
- Enable emergency decreases without delay
- Give monitoring time to detect anomalies

---

#### Configurator Unit

Governance layer that controls rate limits and static parameters for PAUs without modifying deployed contracts.

| Component | Purpose |
|-----------|---------|
| **BEAMTimeLock** | Enforces 14-day delay on all additions (new PAU registrations, new inits, new role grants) |
| **BEAMState** | Stores approved init configurations and accordant mappings |
| **Configurator** | Operational interface where cBEAMs set rate limits and execute approved actions |

**BEAM Authority Cascade:**

| Level | Role | Holder | Capabilities |
|-------|------|--------|-------------|
| **1** | **Council Beacon** (HPHA) | Core Council (set by SpellCore) | Root of all operational authority — sets aBEAMs, overrides all BEAM ownership, sets Synome write rights |
| **2** | **aBEAM** (Admin BEAM) | Core Council | Register PAUs, approve inits, grant cBEAMs — all via timelock. Instant removals for emergency response |
| **3** | **cBEAM** (Configurator BEAM) | GovOps teams | Set rate limits (within SORL), execute approved controller actions, manage relayer/freezer addresses |
| **4** | **pBEAM** (Process BEAM) | Relayers / operational agents | Direct execution on PAUs — calls Controller functions, moves capital within rate limits |

Post-transition, the Council Beacon is set by SpellCore spells (16/24 Core Council Guardian hat) and is the single point from which all downstream BEAM authority flows. See `governance-transition/council-beam-authority.md` for the full authority model.

A GovOps team becomes **accordant** to a PAU when Core Council grants them the cBEAM for that PAU. The accordant GovOps has unified operational control: rate limit configuration, SORL increases, relayer management, and onboarding approved allocation targets.

**Safety Asymmetry:**
- **Additions** (new PAUs, new inits, new permissions) — always timelocked (14-day delay), giving wardens time to review
- **Removals** (revoke permissions, delete inits, unregister PAUs) — always instant, enabling rapid emergency response

**Deployment Scope:**

Each Configurator Unit manages PAUs within its governance scope:

| Configurator | Manages |
|-------------|---------|
| **Generator Configurator** | All Generator PAUs (single, central instance) |
| **Mainnet Configurator** | All mainnet Prime + Halo PAUs |
| **Altchain Configurator** (per chain) | All Foreign Prime + Foreign Halo PAUs on that chain |

The Generator Configurator is separate from the Prime/Halo Configurators because Generators have a distinct governance scope (see `architecture-overview.md`). Prime and Halo PAUs on each blockchain share a single Configurator for that chain.

For detailed contract interfaces, invariants, and user stories, see `smart-contracts/configurator-unit.md`. For the post-transition Council Beacon authority model, see `governance-transition/council-beam-authority.md`.

---

### Prime Risk Capital

#### Internal JRC (IJRC)

Prime's own junior risk capital; foundation of risk capacity.

| Property | Value |
|----------|-------|
| Source | Prime's own treasury (SubProxy) |
| Position | First-loss for Prime's exposures |
| Purpose | "Skin in the game" for Prime |

**First Loss Capital (FLC):**

| Property | Value |
|----------|-------|
| Size | 10% of total JRC, sourced from Prime's own treasury (IJRC) |
| Position | Absolute first-loss — absorbs before any other capital |
| Purpose | Ensures Prime has direct skin in the game before external capital is touched |

---

#### TEJRC Tokenization

External parties provide JRC via smart contract.

| Property | Value |
|----------|-------|
| Token Type | TEJRC (Tokenized External JRC) |
| Standard | LCTS-based (queue settlement) |
| Risk | Junior position; higher yield compensates |
| Yield | Set by Prime via dynamic formula matching supply/demand |
| Queue Rates | Subscribe/redeem rates also set by Prime dynamically |

> **Note:** Yield and queue rate formulas are currently experimental and will be standardized over time.

**Flow:**
1. External party deposits capital to TEJRC queue
2. Capital converts at settlement based on available capacity
3. TEJRC tokens represent junior risk capital position
4. Earns yield; absorbs losses after First Loss Capital is depleted

---

#### TISRC Tokenization

Tokenized isolated senior risk capital per Prime.

| Property | Value |
|----------|-------|
| Token Type | TISRC (Tokenized Isolated SRC) |
| Scope | Isolated to specific Prime's exposures |
| Standard | LCTS-based (queue settlement) |
| Risk | Senior to JRC; absorbs only after JRC and agent token exhausted |
| Yield | Set by Prime via dynamic formula matching supply/demand |

> **Note:** Yield and queue rate formulas are currently experimental and will be standardized over time.

---

#### Loss Absorption Waterfall

When losses occur, capital is consumed in strict order across three tiers:

| Order | Capital Layer | Tier | Mechanism |
|-------|---------------|------|-----------|
| **1** | First Loss Capital (10% from IJRC) | Prime | First loss — absorbed entirely before moving to next layer |
| **2** | Remaining IJRC + EJRC | Prime | Split proportionally between Internal and External JRC |
| **3** | Agent Token Inflation | Prime | Dilute Prime token holders (potentially to infinity) |
| **4** | SRC Pool | System | TISRC merges into Global SRC (srUSDS); losses shared pari passu |
| **5** | SKY Token Inflation | System | Dilute protocol token holders |
| **6** | Genesis Capital Haircut | Nuclear | Protocol reserves |
| **7** | USDS Peg Adjustment | Nuclear | Final backstop — affects all USDS holders |

```
Loss Event
    ↓
┌─── PRIME-LEVEL (per-Prime) ─────────────────────────────────────┐
│  1. First Loss Capital (10%)        │  ← Absolute first loss    │
├─────────────────────────────────────┤                           │
│  2. IJRC + EJRC (pro-rata)          │  ← Remaining junior       │
├─────────────────────────────────────┤                           │
│  3. Agent Token Inflation           │  ← Dilute Prime token     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─── SYSTEM-LEVEL (shared across all Primes) ─────────────────────┐
│  4. SRC Pool (pari passu)           │  ← TISRC + Global SRC     │
├─────────────────────────────────────┤                           │
│  5. SKY Token Inflation             │  ← Dilute SKY holders     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─── NUCLEAR OPTIONS (protocol reserves / peg) ───────────────────┐
│  6. Genesis Capital Haircut         │  ← Protocol reserves      │
├─────────────────────────────────────┤                           │
│  7. USDS Peg Adjustment             │  ← Final backstop         │
└─────────────────────────────────────────────────────────────────┘
```

**Prime-Level (Steps 1-3):** Losses are first absorbed by the specific Prime's capital stack. Agent Token inflation at step 3 can theoretically cover unlimited losses through dilution of Prime token holders.

**System-Level (Steps 4-5):** If Prime-level capital is exhausted, the insolvent Prime's TISRC merges into the Global SRC pool and losses are shared pari passu across all SRC holders. Sky charges a fee on TISRC yield for this protection. SKY inflation dilutes protocol token holders.

**Nuclear Options (Steps 6-7):** Genesis Capital and peg adjustment are last-resort mechanisms that should never be reached under normal conditions. These affect the entire protocol and all USDS holders.

---

### Prime Rewards & Incentives

#### Distribution Rewards

Token rewards to incentivize USDS/sUSDS adoption through tagging. Rewards are tiered based on how strongly the distribution channel builds long-term demand-side moat.

| Property | Value |
|----------|-------|
| Recipient | Primes (who then distribute at their discretion) |
| Split | No enforced split — each Prime determines how to share with integrators |
| Eligible Assets | USDS and sUSDS (both count as adoption) |
| Minimum Balance | None |

**Distribution Reward Tiers:**

| Tier | Rate | Criteria |
|------|------|----------|
| **0** | No DR | Excluded/ineligible addresses |
| **1** | 0 bps | Untagged addresses (tracked but unpaid; can still earn Liability Duration Rewards) |
| **2** | 10 bps | Unbranded complex products (<90% sUSDS backing) |
| **3** | 20 bps | Branded USDS products OR unbranded with ≥90% sUSDS backing |
| **4** | 50 bps | Direct USDS/sUSDS holding with clear Sky branding (Boosted DR) |

**Tier 2 — Unbranded Complex Products (10 bps):**
- Product does not use "USDS" in name
- Backed by mixed collateral with <90% sUSDS
- Example: "StarUSD" containing various stablecoins as collateral

**Tier 3 — Branded or High-Backing Products (20 bps):**

Two paths qualify for Tier 3:

| Path | Requirements | Example |
|------|--------------|---------|
| **3a: Branded** | Uses "USDS" in product name AND subscribe/redeem currency is USDS | "StarUSDS" |
| **3b: High Backing** | Unbranded but ≥90% backed by sUSDS | "StarUSDT" with 90%+ sUSDS backing |

**Tier 4 — Boosted Distribution Rewards (50 bps):**
- Direct holding of USDS or sUSDS
- Clear Sky branding in the frontend
- Creates strongest demand-side moat

**Tagging Mechanism:**

Tagging associates a USDS/sUSDS balance with a Prime for Distribution Reward purposes.

| Method | How It Works |
|--------|--------------|
| **On-chain** | Codes embedded into transactions by frontends or smart contracts |
| **Off-chain** | Verified by Guardian and GovOps |

**Tag Ownership Rules:**

| Property | Value |
|----------|-------|
| Duration | 10 years from tagging |
| Retagging | Whoever tagged last owns the entire account |
| Transferability | Tags cannot be transferred or sold |

> **Note:** Tag ownership rules (last-tagger-wins) are not yet finalized and may change.

---

#### Liability Duration Rewards

Rewards for Primes that source tagged USDS demand feeding into the ALDM (Asset-Liability Duration Matching) system.

| Property | Value |
|----------|-------|
| Purpose | Compensate Primes for bringing sticky USDS demand (liability duration) |
| Eligibility | Tagged USDS that sits in Duration Buckets |
| Split | 2/3 to tagging Prime, 1/3 to Sky (initial setting) |

**How It Works:**

1. USDS accounts accrue liability duration over time and are placed in Duration Buckets based on their duration profile
2. Primes tag USDS accounts, giving them a proportional "share" of each bucket's underlying demand
3. When a Prime pays fees to reserve capacity, their reservation "tugs" on buckets to match their duration needs
4. Fees flow back to whoever tagged the USDS that actually gets tugged

**Dynamic Matching:**

Bucket contents change over time as USDS accounts accrue or lose duration. When a Prime reserves capacity:
- They may tug on nearby buckets if their target bucket lacks sufficient capacity
- Fee distribution follows the actual tugging, not the original reservation target
- This ensures rewards always flow to Primes whose tagged demand is actually being matched

**Fee Distribution:**

For each bucket that gets tugged, fees are distributed proportionally:
- If Prime A tagged 30% of a bucket's USDS, Prime A receives 30% of the fees from tugs on that bucket
- The split multiplier (initially 2/3) is then applied, with the remainder going to Sky

**Example:**
- Prime B reserves capacity targeting Bucket 42, but tugs Buckets 41-43 based on availability
- Bucket 42 contains $100M of USDS; Prime A has tagged $30M (30%)
- Of the $1M fees Prime B pays, $400K is attributed to Bucket 42
- Prime A receives: 30% × (2/3) × $400K = **$80K** from Bucket 42
- (Plus any share from Buckets 41 and 43 if Prime A tagged demand there)

Even Tier 1 (0 bps DR) tagged addresses can earn Liability Duration Rewards, allowing Primes to benefit from demand-side contributions without requiring full branding or composition requirements.

---

#### Integration Boost

Mechanism to apply SSR yield to naked USDS held in smart contracts without using sUSDS.

| Property | Value |
|----------|-------|
| Rate | Equivalent to Sky Savings Rate (SSR) |
| Applies To | Naked USDS sitting in approved smart contracts |
| Purpose | Enable USDS to earn yield in contexts where sUSDS integration isn't practical |
| Approval | Per-integration; governance-approved |

**How It Works:**

Integration Boost is essentially a manual way of having USDS earn the SSR without converting to sUSDS. This is useful for:
- Protocols that need to hold raw USDS (e.g., for liquidity or specific contract logic)
- Integrations where wrapping/unwrapping sUSDS adds friction or gas costs
- Smart contracts that cannot easily integrate ERC-4626 vaults

The yield is paid out to the smart contract holding the USDS, which can then distribute it according to its own logic.

---

#### Governance Access Reward

Rewards for Primes providing compliant governance frontends.

| Property | Value |
|----------|-------|
| Pool | 1% of Sky's yearly net revenue |
| Recipient | Primes with compliant SKY Staking and governance frontends |
| Requirements | Frontend meets Atlas and Synome specifications |
| Distribution | Split among eligible Primes based on SKY staked through each frontend |

> **Note:** Specific compliance requirements for frontends are TBD.

---

### Prime: Duration Capacity Reservation (Planned)

Acquire duration-matching capacity via governance allocations initially, then via auctions once Prime-side `stl-base` is live.

| Property | Value |
|----------|-------|
| Purpose | Reserve Duration Bucket capacity for long-duration assets |
| Mechanism | Governance allocations (pre-auction), then daily sealed-bid auctions (once `stl-base` is live) |
| Benefit | Lower capital requirements when assets match liability duration |

**101 Duration Buckets:**
- Each bucket = 15 days
- Bucket 0 = immediate liquidity
- Bucket 84 = 1,260 days (JAAA CLO AAA)
- Bucket 100 = 1,500+ days (structural/permanent)

---

### Prime: Pioneer System (Genesis Stars Only)

The Pioneer System enables Stars to gain exclusive advantages when expanding USDS to new blockchains. This primitive is only available to the 5 genesis Stars.

| Property | Value |
|----------|-------|
| Availability | Genesis Stars only (Spark, Grove, Keel, Star4, Star5) |
| Purpose | Incentivize cross-chain expansion with first-mover advantages |
| Duration | 3-year Pioneer Phase per Pioneer Chain |
| Exclusivity | One Pioneer Star per chain; Stars can have multiple Pioneer Chains |

#### Pioneer Chains and Pioneer Stars

A **Pioneer Chain** is any blockchain integrating USDS for the first time. A **Pioneer Star** is the Star designated by the chain's team/foundation to lead the USDS rollout.

**Designation Process:**
1. Written confirmation from Pioneer Chain's official team/foundation
2. Star's governance verifies intention to accept Pioneer Status
3. Core Council reviews strategic alignment with Sky Ecosystem growth
4. If approved, Pioneer Phase (3 years of exclusive benefits) begins

#### Pioneer Phase Benefits

**1. Distribution Reward Tagging**

| Property | Value |
|----------|-------|
| During Pioneer Phase | Pioneer Star auto-tags all untagged USDS/sUSDS accounts on the chain |
| At Phase End | One-time permanent tag of remaining untagged balances |
| Tag Duration | 10 years (unless retagged by another Star) |
| Boosted DR | Not available on auto-tags; only on explicitly tagged + approved |

**2. Pioneer Rewards**

| Property | Value |
|----------|-------|
| Source | SSR × Unrewarded USDS balance on Pioneer Chain |
| Timing | Paid each Monthly Settlement Cycle |
| Recipient | Pioneer Star's SubProxy (as income) |

"Unrewarded USDS" = bridged USDS not earning SSR through sUSDS, Integration Boost, or Agent holdings.

**3. Unbalanced Supply Fee Authority**

The Pioneer Star can charge fees to other Stars that allocate supply without contributing to demand.

| Property | Value |
|----------|-------|
| Fee Rate | 20 bps per year |
| Applies To | Unbalanced supply (collateral/liquidity from USDS debt not matched by demand) |
| Purpose | Protect supply/demand balance on Pioneer Chain |

**Balancing Mechanisms (to avoid fee):**

| Mechanism | Offset Ratio |
|-----------|--------------|
| **Tagging Demand** | 1:1 (e.g., $1M tagged USDS offsets $1M supply) |
| **ASC Liquidity** | 3× average daily trading volume counts as demand |

**Exemptions:** Pioneer Star or Pioneer Chain team can grant exemptions via Ecosystem Accord. Exemption terms cannot be revoked if the exempted Star made significant investments based on them.

#### De-designation

If the Pioneer Star fails to meet expectations recorded in an Ecosystem Accord, the Pioneer Chain team/foundation can:
- De-designate the Pioneer Star, or
- Transfer designation to a different Star

When de-designated, the 3-year clock pauses. A future Pioneer Star continues from where the previous one stopped.

---

## Halo Agents

Halo Agents are investment products created by Primes. They wrap specific strategies and deploy capital into real-world assets, custodians, and regulated endpoints.

### Halo Classification

Halos are classified on two dimensions: **regulatory treatment** and **Halo Class type** (which determines the capital deployment mechanism).

**By regulatory treatment:**

| Treatment | Types | Rules |
|-----------|-------|-------|
| **Standard** | Portfolio, Term, Trading | Normal Halo rules — standard governance, rate limits, and risk framework |
| **Special** | Identity Network, Exchange | Additional regulatory or operational requirements beyond standard Halo rules |

**Standard Halo Class types** (by capital deployment mechanism):

| Class Type | Token Standard | Use Case |
|------------|----------------|----------|
| **Portfolio Halo** | LCTS (pooled, fungible) | Standardized products with uniform terms — all participants share the same conditions |
| **Term Halo** | NFAT (individual, non-fungible) | Bespoke deals with negotiated terms — each position has different duration, size, and yield |
| **Trading Halo** | AMM (programmatic counterparty) | Instant liquidity for RWA tokens and ecosystem assets via automated market making |

A Halo Agent with a single Halo Class is commonly referred to by its class name (e.g., "a Portfolio Halo" or "a Trading Halo").

**Special Halos:**

| Type | Purpose |
|------|---------|
| **Identity Network Halo** | Operates identity verification infrastructure (KYC registries). See `sky-agents/halo-agents/identity-network.md` |
| **Exchange Halo** | Operates intent-based exchange infrastructure (orderbooks, matching engines). See `trading/sky-intents.md` |

---

### Halo Creation

| Property | Value |
|----------|-------|
| Creator | Parent Prime only |
| Method | Factory deployment from templates |
| Result | Halo with Unit Structure, Artifact, token standard integration |

---

### Halo Class, Book, and Unit Structure

Halos organize capital into three layers: **Class**, **Book**, and **Unit**. Each layer serves a distinct purpose — infrastructure sharing, balanced ledgers, and cross-book links.

**Hierarchy:**
```
Halo (Synomic Agent)
└── Halo Class (shared SC + legal infra)
    ├── Halo Books (balanced ledgers: assets = liabilities)
    └── Halo Units (cross-book links connecting layers)
```

**Halo Class** — shared smart contract infrastructure (PAU, LPHA beacon) and legal framework (buybox, agreements). The Class defines operational bounds.

| What a Class shares | What varies per Unit |
|---------------------|---------------------|
| PAU (Controller + ALMProxy + RateLimits) | Tranche seniority (for Portfolio) |
| LPHA beacon (lpha-lcts, lpha-nfat, or lpha-amm) | Duration, size, specific terms (for Term) |
| Legal framework (buybox constraints) | Asset pair, spread, pool depth (for Trading) |
| Factory template (audited, reusable) | Risk/return profile within class constraints |

**Halo Book** — a balanced ledger (assets = liabilities) that serves as a bankruptcy-remote isolation boundary. Each book balances real-world positions on the asset side against the Units that claim on them on the liability side. Books provide risk isolation: units sharing a book are pari passu on losses; units on different books are fully isolated. Multiple assets can be blended in a book for borrower privacy. Books progress through a lifecycle (Filling → Deploying → At Rest → Unwinding) with capital requirements varying by phase — see `sky-agents/halo-agents/halo-class-book-unit.md`.

**Halo Unit** — a cross-book link representing a claim on a specific Book. Each Unit is legally and operationally isolated from other units (similar to a serialized LLC). The token standard determines how claims are represented:

| Standard | Model | Use Case |
|----------|-------|----------|
| **LCTS** | Pooled, fungible shares | Many users, same terms, shared capacity (ETF-like) |
| **NFATS** | Individual, non-fungible tokens | Bespoke deals, named counterparties (bond-like) |

**Examples:**

| Class Type | Halo Class Example | Halo Units Within |
|-----------|-------------------|-------------------|
| **Portfolio** | Tranched CLO structure | Senior tranche, Junior tranche (same PAU, same lpha-lcts) |
| **Term** | NFAT Facility with buybox | Multiple NFAT deals (varying duration, size within buybox) |
| **Trading** | RWA instant-settlement pool | USDS/T-Bill pair, USDS/JAAA pair (same AMM, same lpha-amm) |

The underlying smart contract infrastructure (PAU + LPHA beacon) remains consistent across a Halo Class; the token standard determines the user-facing mechanics for subscribing, redeeming, and transferring positions.

---

## Generator Agents

Generator Agents issue Sky Generated Assets (SGAs) — stablecoins for currencies beyond USD. Currently, there is one implicit Generator for USDS; future Generators will issue other currencies.

> **Note:** Generator creation process and detailed specifications are TBD.

Generators have a limited set of specific primitives available to them:

### Issue Generated Asset

| Property | Value |
|----------|-------|
| Types | Sky Generated Asset (SGA) or External Generated Asset (EGA) |
| Examples | USDS (current), future: additional currency SGAs |
| Mechanism | Mint new stablecoins backed by collateral |

---

### Issue Global Senior Risk Token

| Property | Value |
|----------|-------|
| Type | srSGA (e.g., srUSDS) |
| Purpose | Global senior risk capital for the generated asset |
| Standard | LCTS-based (queue settlement) |

---

### Issue Fixed Rate Tokens

| Property | Value |
|----------|-------|
| Types | Fixed-rate sSGA, Fixed-rate srSGA |
| Purpose | Provide predictable yield versions of savings and risk tokens |
| Mechanism | Lock in rate at issuance |

---

### Set Distribution Rewards

| Property | Value |
|----------|-------|
| Purpose | Incentivize adoption of the generated asset |
| Mechanism | Configure reward rates for integrations |

---

### Set Sticky Demand Rewards

| Property | Value |
|----------|-------|
| Purpose | Distribute duration auction income to Primes (once auctions are live) |
| Recipients | Primes that have sourced sticky demand (long-duration liabilities) |
| Source | Revenue from Duration Bucket capacity auctions (once auctions are live) |

---

## Guardian Agents

Guardian Agents operate systems with collateral backing. They interpret governance documents, participate in governance, execute day-to-day operations, and provide oversight within the Sky governance framework. Guardians consolidate the former Facilitator (interpretation), Aligned Delegate (governance participation), and Executor (operations) roles into a single collateral-backed role.

### Guardian Types

| Type | Role | Accountability |
|------|------|----------------|
| **Operational Guardian** | Day-to-day execution | Posts collateral; subject to derecognition |
| **Core Guardian** | Interprets Atlas, oversees Operational Guardians, participates in governance | Atlas alignment; collateral-backed interpretation |

---

### Operational Guardian

| Property | Value |
|----------|-------|
| Function | Execute routine operations within defined bounds |
| Collateral | Posts insurance backing their operations |
| Supervision | Subject to Core Guardian oversight |
| Risk | Derecognition and collateral loss for violations |

---

### Core Guardian

| Property | Value |
|----------|-------|
| Function | Interpret Atlas, oversee Operational Guardians, participate in governance votes |
| Relationship | Governs multiple Operational Guardians; receives delegated SKY voting power |
| Accountability | To Sky Governance; collateral-backed interpretation and execution |

---

## Folio Agents

Folio Agents are rank 3 standardized supply-side holding structures in the Sky ecosystem. They are **not** Halos — the structural difference is fundamental: a Halo wraps around a legal entity, while a folio is controlled BY the principal through legal entities (the principal's legal structure is the governance surface).

Each folio has a **principal** (the end user) who controls the folio through a **directive** — human language instructions defining investment philosophy, risk appetite, and constraints. Two operating modes:

- **Automated folio** — operated by a sentinel formation (baseline + stream + wardens) via guardian accord. The directive governs the formation's behavior.
- **Principal control folio** — operated directly by the principal via a **principal sentinel** (`stl-principal`). No guardian accord, no formation. The principal deploys their own algorithms and manages positions directly.

| Property | Value |
|----------|-------|
| Rank | 3 — administered by a Prime |
| Token | None — tokenless, single owner (the principal) |
| Creation | Instant — any SKY holder |
| Purpose | Standardized holding structure: Growth Staking, capital deployment, strategy access |
| Control | Automated (sentinel formation) or Principal Control (principal sentinel) |
| Restructuring | Type 1 only (graduate to Halo or Prime) |

See `sky-agents/folio-agents/agent-type-folios.md` for the full specification.

---

## Core Controlled Agents

Core Controlled Agents are rank 1 agents directly administered by the Core Council. They serve as general-purpose operational vehicles — in the short term covering legacy protocol positions (replacing "Core Halos"), in the long term serving any Core Council operational need.

| Property | Value |
|----------|-------|
| Rank | 1 — directly regulated by Core Council |
| Token | None — tokenless |
| Creation | Core Council governance (SpellCore) |
| Purpose | Legacy asset management, general-purpose Core Council operations |
| Growth asset | No — excluded from Growth Staking |

See `sky-agents/core-controlled-agents/agent-type-core-controlled.md`.

---

## Recovery Agents

Recovery Agents are rank 1 crisis agents administered by the Core Council, activated when a Guardian collapses or is implicated in misconduct.

| Property | Value |
|----------|-------|
| Rank | 1 — directly regulated by Core Council |
| Token | None — tokenless |
| Creation | Core Council governance (SpellCore), crisis response |
| Purpose | Take over affected agent tree, manage resolution |
| Duration | Temporary — dissolves after crisis resolution |
| Growth asset | No — excluded from Growth Staking |

See `sky-agents/recovery-agents/agent-type-recovery.md`.

---

*This appendix should be updated as new primitives are deployed.*
