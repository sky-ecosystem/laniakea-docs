# Appendix B: Sky Agent Framework Primitives

Features and capabilities available to Sky Agents. Together with Appendix A (Protocol Features), this provides complete coverage of every mechanism in Sky.

---

## Agent Types Overview

Sky Agents are created directly as their permanent type. Each agent type has specific capabilities, primitives, and governance structures. Agent types cannot be changed after creation.

### Agent Type Hierarchy

| Type | Role | Examples |
|------|------|----------|
| **Prime** | Capital-deploying agents operating at scale | 5 Stars (Spark, Grove, Keel, Star4, Star5) + 1 Institutional (Obex) |
| **Halo** | Lighter investment products under Prime umbrella | CLO tranches, yield vaults |
| **Generator** | Issue Sky Generated Assets (new currencies) | USDS Generator (current), future SGA Generators |
| **Executor** | Operate systems with collateral backing | Core Executors, Operational Executors |

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
| Control | Agent governance via Executor Accord |
| Purpose | Hold treasury assets, execute approved transactions |
| Access | Executors with appropriate BEAM authorization |

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
│   ├── Operational Primitives (Executor Accord, Root Edit, etc.)
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
| Optional | Only Halos can realistically opt out of token issuance |

Agent tokens enable decentralized governance and align stakeholder incentives. While all agent types can issue tokens, Halos may operate without one when functioning purely as investment wrappers under a Prime's umbrella.

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

### Executor Accord Primitive

Framework for executor relationships.

| Property | Value |
|----------|-------|
| Purpose | Define executor roles, responsibilities, accountability |
| Parties | Agent ↔ Executor (Operational or Core) |
| Enforcement | Collateralized insurance, derecognition |

---

### Facilitator Framework

Interpret Atlas/Artifacts on behalf of Executors.

| Property | Value |
|----------|-------|
| Role | Authoritative interpretation of governance documents |
| Discretion | Broad authority when explicit guidance absent |
| Documentation | All interpretations recorded as Facilitator Action Precedents |

**Key Principle: Spirit of the Atlas**
- All rules have underlying intent to serve human values
- Facilitators interpret Spirit when explicit guidance is absent
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
| Max Increase | 20% per cooldown period |
| Cooldown | 18 hours between increases |
| Decrease | Always instant (no constraint) |

**Purpose:**
- Prevent sudden capacity expansion attacks
- Enable emergency decreases without delay
- Give monitoring time to detect anomalies

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
| **4** | TISRC | Prime | Isolated senior risk capital for this Prime |
| **5** | Global SRC (srUSDS) | System | Shared senior risk capital pool across all Primes |
| **6** | SKY Token Inflation | System | Dilute protocol token holders |
| **7** | Genesis Capital Haircut | Nuclear | Protocol reserves |
| **8** | USDS Peg Adjustment | Nuclear | Final backstop — affects all USDS holders |

```
Loss Event
    ↓
┌─── PRIME-LEVEL (per-Prime) ─────────────────────────────────────┐
│  1. First Loss Capital (10%)        │  ← Absolute first loss    │
├─────────────────────────────────────┤                           │
│  2. IJRC + EJRC (pro-rata)          │  ← Remaining junior       │
├─────────────────────────────────────┤                           │
│  3. Agent Token Inflation           │  ← Dilute Prime token     │
├─────────────────────────────────────┤                           │
│  4. TISRC                           │  ← Prime-isolated SRC     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─── SYSTEM-LEVEL (shared across all Primes) ─────────────────────┐
│  5. Global SRC (srUSDS)             │  ← System-wide SRC        │
├─────────────────────────────────────┤                           │
│  6. SKY Token Inflation             │  ← Dilute SKY holders     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─── NUCLEAR OPTIONS (protocol reserves / peg) ───────────────────┐
│  7. Genesis Capital Haircut         │  ← Protocol reserves      │
├─────────────────────────────────────┤                           │
│  8. USDS Peg Adjustment             │  ← Final backstop         │
└─────────────────────────────────────────────────────────────────┘
```

**Prime-Level (Steps 1-4):** Losses are first absorbed by the specific Prime's capital stack. Agent Token inflation at step 3 can theoretically cover unlimited losses through dilution of Prime token holders.

**System-Level (Steps 5-6):** If Prime-level capital is exhausted, losses flow to system-wide pools. Global SRC is shared across all Primes; SKY inflation dilutes protocol token holders.

**Nuclear Options (Steps 7-8):** Genesis Capital and peg adjustment are last-resort mechanisms that should never be reached under normal conditions. These affect the entire protocol and all USDS holders.

---

### Prime Rewards & Incentives

#### Distribution Rewards

Token rewards to incentivize USDS/sUSDS adoption through tagging. Rewards are tiered based on how strongly the distribution channel builds long-term demand-side moat.

| Property | Value |
|----------|-------|
| Recipient | Stars (who then distribute at their discretion) |
| Split | No enforced split — each Star determines how to share with integrators |
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

Tagging associates a USDS/sUSDS balance with a Star for Distribution Reward purposes.

| Method | How It Works |
|--------|--------------|
| **On-chain** | Codes embedded into transactions by frontends or smart contracts |
| **Off-chain** | Verified by Executor and GovOps |

**Tag Ownership Rules:**

| Property | Value |
|----------|-------|
| Duration | 10 years from tagging |
| Retagging | Whoever tagged last owns the entire account |
| Transferability | Tags cannot be transferred or sold |

> **Note:** Tag ownership rules (last-tagger-wins) are not yet finalized and may change.

---

#### Liability Duration Rewards

Rewards for Primes that source tagged USDS demand feeding into the SPTP (Stressed Pull-to-Par) system.

| Property | Value |
|----------|-------|
| Purpose | Compensate Primes for bringing sticky USDS demand (liability duration) |
| Eligibility | Tagged USDS that sits in SPTP buckets |
| Split | 2/3 to tagging Prime, 1/3 to Sky (initial setting) |

**How It Works:**

1. USDS accounts accrue liability duration over time and are placed in SPTP buckets based on their duration profile
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

### Prime: SPTP Capacity Reservation (Planned)

Acquire duration-matching capacity via auctions.

| Property | Value |
|----------|-------|
| Purpose | Reserve SPTP bucket capacity for long-duration assets |
| Mechanism | Weekly sealed-bid auctions |
| Benefit | Lower capital requirements when assets match liability duration |

**101 SPTP Buckets:**
- Each bucket = 0.5 months (15 days)
- Bucket 0 = immediate liquidity
- Bucket 84 = 42 months (JAAA CLO AAA)
- Bucket 100 = 50+ months (structural/permanent)

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

### Halo Types

| Type | Purpose | Flexibility |
|------|---------|-------------|
| **Standard Halo** | General investment products; supports Halo Units | Can do anything |
| **Identity Network Halo** | Operates identity verification infrastructure | Specially regulated |
| **Exchange Halo** | Operates intent-based exchange infrastructure | Specially regulated |

**Standard Halos** are the most common type and can be configured for any investment strategy or operational purpose. They support multiple Halo Units within a single Halo structure.

**Identity Network Halos** and **Exchange Halos** are specialized types with additional regulatory requirements, tied to the Identity Network and Sky Intents systems respectively. See `identity-network.md` and `sky-intents.md` for details.

---

### Halo Creation

| Property | Value |
|----------|-------|
| Creator | Parent Prime only |
| Method | Factory deployment from templates |
| Result | Halo with Unit Structure, Artifact, token standard integration |

---

### Halo Class Structure

A **Halo Class** is a grouping of Halo Units that share the same smart contract infrastructure (PAU, sentinel formation) and legal framework (buybox, agreements). The Halo Class defines the operational bounds; individual Halo Units vary within those bounds.

**Hierarchy:**
```
Halo (Synomic Agent)
└── Halo Class (shared SC + legal infra)
    └── Halo Unit (specific instance)
```

**Examples:**

| Halo Type | Halo Class Example | Halo Units Within |
|-----------|-------------------|-------------------|
| **Passthrough** | Tranched CLO structure | Senior tranche, Junior tranche (same PAU, same lpha-lcts) |
| **Structuring** | NFAT Facility with buybox | Multiple NFAT deals (varying duration, size within buybox) |

**What a Halo Class shares:**
- PAU (Controller + ALMProxy + RateLimits)
- Sentinel formation (lpha-lcts or lpha-nfat)
- Legal framework (buybox constraints, counterparty agreements)
- Factory template (audited, reusable deployment)

**What Halo Units can vary:**
- Tranche seniority (for Passthrough)
- Duration, size, specific terms (for NFAT)
- Risk/return profile within class constraints

---

### Halo Unit Structure

A **Halo Unit** is a governance-level construct — not a smart contract — representing a bankruptcy-remote capital deployment within a Halo Class. Similar to a serialized LLC, each Halo Unit is legally and operationally isolated from other units within the same Halo. If one unit suffers losses, other units are protected.

A single Halo Class can contain multiple Halo Units, each with specific parameters within the class's bounds.

**Token Standards:** The choice of token standard determines how claims on a Halo Unit are represented — analogous to choosing between bonds, ETFs, or stocks to represent value:

| Standard | Model | Use Case |
|----------|-------|----------|
| **LCTS** | Pooled, fungible shares | Many users, same terms, shared capacity (ETF-like) |
| **NFATS** | Individual, non-fungible tokens | Bespoke deals, named counterparties (bond-like) |

The underlying smart contract infrastructure (PAU + Sentinel) remains consistent across a Halo Class; the token standard determines the user-facing mechanics for subscribing, redeeming, and transferring positions.

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
| Purpose | Distribute SPTP auction income to Primes |
| Recipients | Primes that have sourced sticky demand (long-duration liabilities) |
| Source | Revenue from SPTP capacity auctions |

---

## Executor Agents

Executor Agents operate systems with collateral backing. They execute day-to-day operations and provide oversight within the Sky governance framework.

### Executor Types

| Type | Role | Accountability |
|------|------|----------------|
| **Operational Executor** | Day-to-day execution | Posts collateral; subject to derecognition |
| **Core Executor** | Oversight of Operational Executors | Atlas alignment; governs Operational Executors |

---

### Operational Executor

| Property | Value |
|----------|-------|
| Function | Execute routine operations within defined bounds |
| Collateral | Posts insurance backing their operations |
| Supervision | Subject to Core Executor oversight |
| Risk | Derecognition and collateral loss for violations |

---

### Core Executor

| Property | Value |
|----------|-------|
| Function | Oversee Operational Executors; ensure Atlas alignment |
| Relationship | Governs multiple Operational Executors |
| Accountability | To Sky Governance and Facilitators |

---

*This appendix should be updated as new primitives are deployed.*
