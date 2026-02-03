# Atlas/Synome Separation

**Status:** Draft
**Pillar:** 8
**Last Updated:** 2026-01-27

---

## The Problem

The Atlas was originally envisioned as the complete, immutable knowledge base of all Sky data, algorithms, and intelligence. The Endgame State would lock this comprehensive documentation forever.

But this vision contains a fundamental contradiction:

1. **Comprehensive documentation** must cover every operational detail, algorithm, configuration, and edge case
2. **Machine-readable structure** is required for autonomous systems (Sentinels) to consume and act on this data
3. **Human readability** is required for democratic legitimacy—stakeholders must understand what they're governing

These requirements conflict. The current Atlas (~364,000 words across 7 scope documents) attempts to be both, resulting in:
- Dense, legalistic language mixing human explanations with machine-precise specifications
- Agent Artifacts (A.6) alone comprising 26,838 lines of Instance Configuration Documents, rate limits, and operational parameters
- Neither fully readable by humans nor fully parseable by machines

---

## The Solution: Two Layers

Split into two complementary components that serve different audiences:

### Atlas (Human Layer)

A constitutional document that exists as a single root node within the Synome.

**What Stays in Atlas:**
- Spirit of the Atlas / Universal Alignment principles (A.0)
- Governance structure and decision processes (A.1)
- Sky Primitive definitions and lifecycle rules (A.2)
- Risk Capital Framework principles—JRC/SRC seniority, encumbrance ratio target (A.3)
- Token architecture and reward mechanisms (A.4)
- Geographic access controls and compliance philosophy (A.5)
- Agent type definitions and transformation rules (A.6 introduction)

**Characteristics:**
- Short enough to be readable by any stakeholder (~10-20 pages target)
- Written in plain language (not legalese, not code)
- Describes WHAT must be true, not HOW it's implemented
- Verification assertions that the Synome must satisfy

### Synome (Machine Layer)

A graph database containing ALL operational data, structured for machine consumption.

**What Moves to Synome:**

| Current Atlas Location | Synome Destination | Notes |
|------------------------|-------------------|-------|
| Agent Artifacts (A.6.1-A.6.6) | Agent Nodes | Complete specs for all 6 Primes (5 Stars + 1 Institutional) |
| Instance Configuration Documents | Instance Nodes | Contract addresses, rate limits, parameters |
| Active Data Documents (A.1) | State Nodes | Modifiable outside governance cycles |
| Budget Documents | Budget Nodes | Rates, allocations, disbursement rules |
| Precedents & Action Tenets | Precedent Nodes | Historical decisions and interpretations |
| BEAM Parameters (A.4) | Config Nodes | min/max/step/tau for each controlled parameter |
| Settlement Calculations | Algorithm Nodes | P&L formulas, waterfall logic, penalty calculations |
| Rate Limits per Instance | RateLimit Nodes | maxAmount, slope, current capacity |

**Current Examples from Atlas:**

From A.6 (Agent Scope):
```
Prime SubProxy Addresses:
  Spark: 0x3300f198988e4C9C63F75dF86De36421f06af8c4
  Grove: 0x1369f7b2b38c76B6478c0f0E66D94923421891Ba
  Keel:  0x355CD90Ecb1b409Fdf8b64c4473C3B858dA2c310
  Obex:  0x8be042581f581E3620e29F213EA8b94afA1C8071

Core Operator Relayer Multisig: 0x8Cc0Cb0cfB6B7e548cfd395B833c05C346534795 (2/5)

SLL Rate Limit Types (per chain):
  LIMIT_USDS_MINT, LIMIT_USDS_BURN, LIMIT_USDS_TO_USDC,
  LIMIT_USDC_TO_CCTP, LIMIT_USDC_TO_DOMAIN

SLL Deployed Chains: Ethereum, Base, Arbitrum, Unichain, Optimism, Avalanche
```
→ All moves to Synome as structured Agent Artifact nodes.

From A.4 (Protocol Scope):
```
stUSDS BEAM Controls:
| str | stUSDS rate | 200bp | 5000bp | 500bp | 16h |
| duty | SKY borrow rate | 210bp | 5000bp | 500bp | 16h |
```
→ Moves to Synome as BEAM Config node with typed fields.

From A.3 (Stability Scope):
```
Encumbrance Breach Severities:
  Low:  100% ≤ ER < 103%
  High: ER ≥ 103%

Penalty Schedule (Low Severity):
  0-30 min:  500% APY on shortfall
  30-60 min: 1,000% APY on shortfall
  60+ min:   1,500% APY on shortfall

Penalty Schedule (High Severity):
  0-15 min:  1,500% APY on shortfall
  15-30 min: 2,000% APY on shortfall
  30-60 min: 2,500% APY on shortfall
  60+ min:   3,000% APY on shortfall

Risk Capital Ratios:
  EPI (External Per Internal) = 1.00
  First Loss Capital = 10% of Total JRC (Prime's IJRC only)
  ESRC Earnings Fee = 5%
```
→ All move to Synome as Config/Algorithm nodes.

From A.2 (Support Scope):
```
Monthly Settlement Cycle Timeline:
  End of month:     Core GovOps creates MSC Post
  +7 days:          Initial Calculation (OEA) + Independent Calculation (CCRA)
  +12 days:         Final Calculation (resolve disputes)
  Next Executive:   Include payments in Sky Core Executive Vote

Calculation Tolerance: 1% deviation = Agreed, >1% = Disputed

Treasury Waterfall (% of Net Revenue):
  Step 1: Security & Stability Maintenance (10%)
    - Core Executor Budget: up to 5%
    - Core Executor Reward: up to 3%
    - Aligned Delegates: up to 1%
    - Governance Accessibility: 1%
  Step 2: High Activity Staking Rewards (5%)
  Step 3: Stability Capital Retention (variable)
    - SCR = (1 - (SCB/TS)/TSCB) × RF
    - Target SCB = 0.75% + (TS × 1.4e-14), max 5%
    - RF = 25% + (TS × 1.6e-13), max 75%
  Step 4: Smart Burn (80%) + Standard Activity Staking (20%)

Ecosystem Upkeep:
  Distribution Requirement: 0.25% of token supply annually
  Market Cap Fee: 0.30% of market cap annually
```
→ All move to Synome as Settlement Algorithm and Config nodes.

---

## Document Type Mapping

The existing Atlas hierarchy already hints at the split:

| Current Type | Destination | Rationale |
|--------------|-------------|-----------|
| **Immutable Documents** (Scopes, Articles, Sections) | Atlas | Constitutional principles |
| **Primary Documents** | Atlas | Core rules that operationalize the Spirit |
| **Supporting Documents** | Bridge | Some stay (explanatory), some move (data) |
| **Active Data Documents** | Synome | Modifiable state = machine territory |
| **Budget Documents** | Synome | Rates and allocations = machine territory |
| **Instance Configuration Documents** | Synome | Per-deployment parameters = machine territory |
| **Precedents** | Synome | Historical decisions for pattern recognition |
| **Accessory Documents** | Atlas | Translations, archives (for humans) |

---

## The Relationship

```
┌─────────────────────────────────────────────────────────────────────┐
│                            SYNOME                                    │
│  (Graph database - all operational data)                             │
│                                                                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                         ATLAS                                  │  │
│  │  (Root node - human-readable constitution)                     │  │
│  │                                                                │  │
│  │  A.0 Spirit of the Atlas                                       │  │
│  │  A.1 Governance (who decides, how)                             │  │
│  │  A.2 Primitives (what building blocks exist)                   │  │
│  │  A.3 Risk Framework (seniority, encumbrance principles)        │  │
│  │  A.4 Protocol (tokens, rewards, BEAM pattern)                  │  │
│  │  A.5 Accessibility (compliance philosophy)                     │  │
│  │  A.6 Agent Types (what Primes and Executors are)              │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                              │                                       │
│           ┌──────────────────┼──────────────────┐                   │
│           ▼                  ▼                  ▼                   │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐            │
│  │ Spark Agent  │   │ Grove Agent  │   │ Keel Agent   │  ...       │
│  │   Artifact   │   │   Artifact   │   │   Artifact   │            │
│  ├──────────────┤   ├──────────────┤   ├──────────────┤            │
│  │ SubProxy     │   │ SubProxy     │   │ SubProxy     │            │
│  │ Rate Limits  │   │ Rate Limits  │   │ Rate Limits  │            │
│  │ Instances[]  │   │ Instances[]  │   │ Instances[]  │            │
│  │ ICDs[]       │   │ ICDs[]       │   │ ICDs[]       │            │
│  └──────────────┘   └──────────────┘   └──────────────┘            │
│           │                  │                  │                   │
│           ▼                  ▼                  ▼                   │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    Instance Nodes                             │  │
│  │  Morpho USDS, Aave USDC, Curve USDS-USDC, Treasury Bills...  │  │
│  │  Each with: addresses, rate limits, operational procedures   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    Config Nodes                               │  │
│  │  BEAM parameters, Penalty schedules, Settlement formulas      │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                   Transaction Logs                            │  │
│  │  All Sentinel actions, settlements, state changes, precedents │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

The Atlas is embedded IN the Synome, not separate from it. It's the human-interpretable entry point to a machine-readable system.

---

## Synomic Agents: Autonomous Entities Tethered to the Synome

The Synome structure enables a crucial property: **Synomic Agents can be fully autonomous**.

### What Makes This Possible

A Synomic Agent (Prime, Halo, Generator) exists entirely within the Synome:

| Property | Implication |
|----------|-------------|
| Identity is Synome-native | SubProxy address, token — cannot exist outside |
| Assets are Synome-controlled | TRC, credit lines governed by Synome rules |
| Actions are Synome-bounded | Rate limits, encumbrance ratios enforced by code |
| Accountability is structural | Penalties accrue automatically, conservatorship triggers automatically |

Because the agent cannot escape its constraints, it can operate without human oversight for individual decisions. No one can lobby, bribe, or override it — the rules hold unconditionally.

### Why Autonomy Matters

**1. Protecting Humans from Each Other**

Without autonomous Synomic Agents, rules hold only until someone powerful enough lobbies to break them. With autonomous agents:
- Encumbrance penalties apply regardless of who wants an exception
- Settlement happens regardless of who benefits or loses
- Rate limits hold regardless of market pressure

The agent isn't protecting humans because it's benevolent — it's protecting them because it literally cannot deviate.

**2. Enabling Cooperation Without Trust**

Multiple parties (opaque to each other, potentially competing) can coordinate through Synomic Agents:

```
Party A ──┐
          ├───► Synomic Agent ◄───► Synome constraints
Party B ──┘     (neutral arbiter)
```

- A cannot read B's strategy
- B cannot read A's strategy
- Both can verify the Synomic Agent follows rules
- Both can trust outcomes without trusting each other

This enables: sealed-bid auctions, multi-party settlement, cross-jurisdictional capital flows.

### Agent Types

**Primes** — Specialized, heavyweight Synomic Agents. Two subtypes: Star Primes (5: Spark, Grove, Keel, Star4, Star5) and Institutional Primes (1: Obex). Require transformation primitives, foundations, nested contributors.

**Halos** — General-purpose Synomic Agents. Can wrap any value and give it agency. Organized into **Halo Classes** (shared SC + legal infra) containing **Halo Units** (individual products). Examples: tranched Passthrough Halo (senior/junior sharing one PAU), NFAT Facility (same buybox, varying duration/size). Halos are the fractal layer — they proliferate.

**Executors** — Perform privileged operations with collateral backing. Post escrow, face slashing for failures.

### Escalation to Human Reasonableness

The Synome provides what traditional smart contracts lack: **a path to human judgment for edge cases**.

Regular smart contracts are "code is law" — no appeal, no reasonableness check. If the code produces an absurd outcome, too bad. Synomic Agents are different:

```
99% of cases              1% edge cases
─────────────────         ─────────────────
Automated                 Escalates to governance
Cheap (gas only)          Expensive (time, attention, voting)
Code resolves             Humans resolve
No human involvement      Sky ensures reasonable outcome
```

**Example: Escrow Synomic Agent**

A dispute arises that the code can't resolve cleanly. Instead of defaulting to an arbitrary outcome:
1. Agent flags the dispute
2. Escalates through governance layers
3. If necessary, reaches Sky Core governance
4. Humans apply reasonableness — "what would a sensible person conclude?"
5. Resolution flows back down

The escalation is expensive by design. This creates incentive to:
- Write better code that handles more cases automatically
- Resolve disputes at the lowest possible level
- Only escalate genuinely hard cases

But the path exists. Any edge case can ultimately reach human judgment.

**This is what makes Synomic Agents "smart contracts with a backstop":**
- The code handles the predictable
- The Synome guarantees alignment with human values when the unpredictable happens
- No outcome is ever truly "code said so, deal with it"

### The Trust Equation

Traditional smart contracts: `Trust = Code (no recourse)`

Synomic systems: `Trust = Code × Synome Constraints × Human Escalation Path`

The second is stronger because it combines automation efficiency with human reasonableness. The agent handles 99% cheaply; the Synome guarantees the 1% gets a sensible outcome.

---

## Mini-Atlases: The Fractal Pattern

Every level of the Synome with human stakeholders should have a human-readable summary.

### Prime Mini-Atlases

Each Prime Agent creates their own "mini-Atlas" to explain their Agent Artifact:

**Audience:** Prime token holders, users of Prime services

**Contents (derived from Agent Artifact):**
- What the Prime does (strategic overview from A.6 introduction sections)
- Key parameters explained in plain language
- Risk disclosures without full Risk Framework formulas
- Governance processes for the Prime (Root Edit Primitive configuration)
- How to participate (staking, using services)

**Root Edit Governance (Standard across Primes):**
- **Who can propose:** 1% token holders (Nested Contributors exempt)
- **Review period:** 7-day Operational Facilitator alignment review
- **Voting period:** 3-day Snapshot poll
- **Quorum:** 10% of token supply
- **Approval threshold:** >50%
- **"Publicly Held" gate:** Root Edit not operational until 2,000+ holders own 10%+ of genesis supply

**Current Prime Agents needing Mini-Atlases:**

*Star Primes:*

| Prime | Focus | SubProxy |
|-------|-------|----------|
| Spark | DeFi: SLL (6 chains), SparkLend, Spark Savings | `0x3300...af8c4` |
| Grove | Institutional: CLOs, RWA allocations | `0x1369...891Ba` |
| Keel | Solana ecosystem, USDS adoption | `0x355C...2c310` |
| Star4 | TBD | TBD |
| Star5 | TBD | TBD |

*Institutional Primes:*

| Prime | Focus | SubProxy |
|-------|-------|----------|
| Obex | Agent incubator (Prime + Halo development) | `0x8be0...c8071` |

### Halo Mini-Atlases

For Halos with external participants (like Passthrough Halos with institutional investors):

**Audience:** Institutional investors, regulatory bodies

**Contents:**
- Investment strategy and expected returns
- Risk factors in compliance-suitable language
- Legal structure and regulatory status
- Reporting cadence and metrics

### The Pattern

```
Sky Atlas               → Describes Sky Core (A.0-A.5 + A.6 intro)
  ├─ Spark Mini-Atlas        → Describes Spark Agent Artifact node
  │    ├─ SLL docs           → Describes SLL Instance nodes
  │    ├─ SparkLend docs     → Describes SparkLend Instance nodes
  │    └─ Halo A docs        → Describes Halo A node
  │         └─ Halo Class 1  → Shared PAU + sentinel + legal
  │              ├─ Unit 1   → Senior tranche
  │              └─ Unit 2   → Junior tranche
  ├─ Grove Mini-Atlas        → Describes Grove Agent Artifact node
  │    └─ Halo B docs        → Describes Halo B node (NFAT Facility)
  │         └─ Halo Class 1  → Shared buybox + lpha-nfat
  │              ├─ NFAT 1   → 6mo term, 10M
  │              └─ NFAT 2   → 12mo term, 25M
  └─ ...
```

Every node with human stakeholders gets a human summary. The Synome can grow arbitrarily complex; the human layer stays manageable.

---

## Verification Model

The Atlas/Synome split enables a clear verification model:

### Human Verification (Atlas)

Humans verify that the Atlas:
- Reflects their values and intentions
- Contains sensible, non-contradictory principles
- Adequately protects their interests
- Is understandable without technical expertise

This happens through:
- Governance Polls and Executive Votes (A.1)
- Aligned Delegate review
- Public debate on Sky Forum

### Machine Verification (Synome → Atlas)

Machines verify that the Synome:
- Conforms to Atlas constraints
- Maintains internal consistency
- Produces valid state transitions
- Satisfies formal invariants

This happens through:
- Sentinel constraint checking before actions
- Monthly/Weekly Settlement Cycle validation (A.2, A.3)
- Independent Calculation vs Initial Calculation comparison
  - ≤1% deviation = **Agreed Amount** (auto-approved)
  - >1% deviation = **Disputed Amount** (requires Core GovOps resolution)
  - Prime can post Dispute Notice within 5 days of calculation posting

### The Bridge: Atlas Assertions → Synome Constraints

| Atlas Statement | Synome Constraint |
|-----------------|-------------------|
| "Encumbrance ratio target ≤90%" | `∀ prime: prime.RRC / prime.TRC ≤ 0.90` |
| "JRC absorbs losses before SRC" | `loss_order = [tip_jrc, remaining_jrc, src, backstop]` |
| "Rate changes limited by BEAM tau" | `∀ param: time_since_last_change(param) ≥ param.tau` |
| "srUSDS queues process at Monthly Settlement" | `∀ queue: process_on(queue) = MSC_date` |
| "Penalty escalates with duration" | `penalty_rate = f(shortfall_duration)` per schedule |

The Atlas describes intent; the Synome encodes implementation.

---

## Synome Structure for Laniakea

### How Sentinels Use Synome

Sentinels operate on Synome data, not Atlas text:

| Beacon | Synome Data Consumed | Synome Data Written |
|--------|---------------------|---------------------|
| stl-base | Prime pBEAM permissions, rate limits | Bid submissions, capacity requests |
| lpha-lcts | LCTS config, queue state, Halo parameters | Settlement transactions, exchange rates, status updates |
| lpha-auction | Bid submissions, capacity pools | Clearing prices, allocations |
| lpla-checker | All above (read-only) | Verification attestations |

### BEAM Hierarchy in Synome

```
pBEAM Node (Prime-level)
├── Controlled Parameters[]
│   ├── OSRC_capacity: {min, max, step, tau, current_value}
│   ├── Interest_rate: {min, max, step, tau, current_value}
│   └── ...
├── Authorized Operators[]
│   ├── stl-base (automated)
│   └── Prime Multisig (manual)
└── Last Update Timestamps{}

cBEAM Node (Core-level guardrails)
├── Global Limits{}
│   ├── max_total_allocation
│   ├── max_single_prime_exposure
│   └── ...
└── Override Permissions
    └── Core Council multisig

aBEAM Node (Emergency controls)
├── Freeze Permissions[]
├── Recovery Procedures[]
└── Emergency Contact Info[]
```

### Transaction Log Structure

All Sentinel actions create Synome transaction log entries:

```
Transaction {
  id: bytes32
  timestamp: uint256
  sentinel: address
  action_type: enum
  target_node: bytes32
  parameters: bytes
  result: enum
  verification_hash: bytes32
}
```

This enables:
- Audit trail for all autonomous actions
- Pattern recognition for anomaly detection
- Precedent lookup for similar situations
- Continuous improvement via post-hoc analysis

---

## Migration Path

### Phase 1: Extraction

Extract machine data from current Atlas into structured format:
- Parse A.6 Agent Artifacts → Agent nodes
- Parse Instance Configuration Documents → Instance nodes
- Parse BEAM tables (A.4) → Config nodes
- Parse penalty schedules (A.3) → Algorithm nodes
- Parse Active Data references → State node templates

### Phase 2: Distillation

Condense Atlas to constitutional core:
- Keep principles, remove parameters
- Keep definitions, remove instances
- Keep rules, remove implementation details
- Target: ~10-20 page document

### Phase 3: Verification Mapping

Create formal links between Atlas assertions and Synome constraints:
- Each Atlas rule → one or more Synome invariants
- Invariants checked by Sentinels continuously
- Violations trigger alerts/actions per cBEAM/aBEAM

### Phase 4: Sentinel Integration

Build Sentinel interfaces to Synome:
- Read APIs for configuration retrieval
- Write APIs for transaction logging
- Query APIs for state inspection
- Subscription APIs for real-time updates

---

## Open Questions

1. **Synome implementation** — What graph database or data structure? On-chain (expensive), off-chain (trust), or hybrid (anchored)?

2. **Atlas constraint language** — How to express assertions in a way that's both human-readable AND machine-checkable? Natural language + formal spec?

3. **Mini-Atlas governance** — Are mini-Atlases required or optional? What minimum contents? Who verifies accuracy?

4. **Migration governance** — How to govern the transition from current Atlas to Atlas/Synome split? Phased rollout?

5. **Versioning** — How to version Synome nodes? How to handle backwards compatibility when constraints change?

6. **Access control** — Who can read/write which Synome nodes? How does this map to current role structure (Facilitators, GovOps, Executors)?

---

## Summary

The Atlas/Synome separation resolves the fundamental tension between comprehensive machine-readable documentation and human-readable governance:

| Aspect | Atlas | Synome |
|--------|-------|--------|
| **Audience** | Humans | Machines (Sentinels) |
| **Size** | Compact (~10-20 pages) | Unlimited |
| **Language** | Natural language | Structured/typed data |
| **Content** | Principles, rules, definitions | Parameters, state, transactions |
| **Modification** | Governance votes | Via Atlas-conforming operations |
| **Verification** | Human review | Automated checking |
| **Examples** | Spirit of Atlas, JRC/SRC seniority | Spark SubProxy address, LIMIT_USDS_MINT |

The Atlas becomes the human-interpretable window into an arbitrarily complex machine-readable system. Every stakeholder can understand their rights and the system's principles without needing to parse operational specifications.

**Key Insight:** Agent Artifacts are already structured for machines (addresses, rate limits, ICDs). The Atlas/Synome split formalizes what's implicit: A.0-A.5 + A.6 intro are the Atlas; A.6.1-A.6.5 details are the Synome.

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| `synome-layers.md` | The 5-layer architecture and artifact hierarchy (synart, telart, embart) |
| `syno-teleonomic-paradigm.md` | External interaction model — how Synomic Agents operate through beacons |
| `beacon-framework.md` | How beacons derive authority envelopes from governance |
| `probabilistic-mesh.md` | The soft knowledge layer that informs governance decisions |
| `short-term-actuators.md` | Phase 1 beacon implementation — teleonome-less beacons interacting with Synome-MVP |
