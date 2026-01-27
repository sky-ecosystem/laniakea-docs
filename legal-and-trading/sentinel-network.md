# Sentinel Network

**Status:** Draft
**Last Updated:** 2026-01-27

---

## What Are Sentinels?

Sentinels are a **distinguished subclass of HPHA beacons** — High Power, High Authority action apertures that exercise continuous, real-time operational control on behalf of Synomic Agents.

Sentinels are **not** all autonomous systems in Laniakea. That broader category is covered by the beacon framework. Sentinels are specifically the **execution layer** — the primary mechanism by which teleonomes deploy capital through PAUs.

**Both Primes and Halos can have sentinel formations.** Any Synomic Agent with a PAU can be operated by a sentinel formation. The pattern is the same:
- **Prime sentinel**: Ingresses risk capital → deploys leverage into yield opportunities
- **Halo sentinel**: Ingresses capital (via LCTS or NFAT) → deploys to RWA endpoints or other allocations

### Why Sentinels Are Special

Although other HPHA beacons exist (auction brokers, exchange matchers), sentinels are uniquely powerful because they:

- Operate **continuously and in real time**
- Act faster than synomic governance processes
- Concentrate institutional authority and local intelligence
- Create immediate external effects that governance audits asynchronously
- Are **operationally dominant** — they move capital, not just process rules

Even governance beacons (LPHA beacons) remain process-gated and asynchronous. Sentinels are the live edge.

### Connection to Beacon Framework

For the broader taxonomy of beacons — including LPHA keepers, HPLA trade beacons, LPLA reporting beacons, controllers, and custodians — see `beacon-framework.md`.

This document focuses on **sentinel formations**: the coordinated HPHA beacon systems that execute strategies for Synomic Agents (Primes and Halos with PAUs).

---

## Sentinel Formations

Sentinels do not operate as single agents. They operate as **coordinated formations** composed of multiple specialized components, mirroring **data plane / control plane / safety plane** architecture.

### Formation Components

| Component | Role | Execution Authority | Operator |
|-----------|------|---------------------|----------|
| **Baseline Sentinel** | Primary decision-making and execution | **Yes** — holds Execution Engine | Accordant GovOps |
| **Stream Sentinel** | Data ingestion, signal generation, intent streaming | **No** — feeds Baseline only | Ecosystem Actor |
| **Warden Sentinel(s)** | Independent monitoring, risk enforcement | **Limited** — safety stops only | Independent operators |

### Why This Separation?

**Baseline** ensures all execution flows through public, auditable code. No private actor directly moves Prime capital.

**Stream** allows proprietary intelligence to influence execution without exposing strategies or holding keys. The teleonome's alpha remains private.

**Wardens** provide independent safety oversight. They can halt operations when things go wrong, without being compromised by the same failure modes as Baseline or Stream.

---

## Baseline Sentinel

> The public autopilot — the only entity holding keys to the Execution Engine.

**Profile:** HPHA (High Power, High Authority)
**Operator:** Accordant GovOps
**Access:** Public / Open Source

### Responsibilities

- **Execution Engine holder** — Controls pBEAMs, executes transactions on PAU
- **Base Strategy execution** — Runs the public strategy defined in Prime Artifact
- **Fail-safe** — If Stream disconnects or sends invalid data, automatically reverts to Base Strategy
- **Counterfactual simulation** — Continuously simulates "what would we have earned with just the Base Strategy?" for carry comparison
- **Intent validation** — Validates Stream intent against Risk Tolerance Interval before execution

### Three Parallel Processes

1. **Process A: Counterfactual Simulation**
   - Virtual simulation of Base Strategy running in parallel
   - Uploads results to Synome
   - Provides benchmark for carry calculation

2. **Process B: Streaming Monitor**
   - Receives intent from Stream Sentinel
   - Validates against Risk Tolerance Interval
   - Executes if compliant; rejects if not

3. **Process C: Active Management**
   - Engages when Stream disconnects or sends invalid data
   - Executes Base Strategy directly
   - Ensures continuous operation regardless of Stream availability

### Execution Engine

The Execution Engine is the component that actually holds pBEAMs and signs transactions.

**Critical properties:**
- Only Baseline Sentinel holds this
- Stream Sentinel cannot execute directly — only stream intent
- All execution flows through public, auditable code
- Wardens can freeze the Execution Engine

---

## Stream Sentinel

> The commercial engine for alpha generation.

**Profile:** HPHA (High Power, High Authority)
**Operator:** Ecosystem Actors (DevCos, Trading Firms)
**Access:** Private / Proprietary

### Why Stream is HPHA

Stream operates on behalf of a Prime (Synomic Agent), not independently. Even though it doesn't execute directly, its intent streams determine how Prime capital is deployed. It's subject to the Streaming Accord — a synomic contract governing the relationship.

### Responsibilities

- **Data ingestion** — Ingests public data + proprietary sources (off-chain order books, sentiment, credit models)
- **Signal generation** — Feature extraction, model inference, strategy computation
- **Intent streaming** — Sends trading intent (not transactions) to Baseline
- **Alpha generation** — The commercial purpose: outperform the Base Strategy

### What Stream Does NOT Have

- No Execution Engine
- No direct pBEAM access
- No ability to move capital without Baseline validation
- No authority if Baseline rejects intent

### Incentive Structure

Stream earns **carry** only when outperforming the Base Strategy:

```
Carry = (Actual PnL - Simulated Baseline PnL) × Performance Fee Ratio
```

- If Stream underperforms Baseline: no carry
- If Stream outperforms: proportional share of alpha
- Performance Fee Ratio defined in Streaming Accord

This aligns incentives: Stream only profits when it adds genuine value.

---

## Warden Sentinels

> Independent safety oversight — can freeze, halt, or escalate.

**Profile:** HPHA (High Power, High Authority)
**Operator:** Independent operators (NOT same as Baseline)
**Access:** Audited / Certified

### Independence Requirement

Wardens **must** be operated by independent parties — not the same operator as Baseline or Stream.

**Why independence matters:**
- If Baseline goes rogue, a warden run by the same operator may also be compromised
- Independent wardens = true redundancy
- Multiple independent wardens = multiplicative reliability

### Multiple Wardens

Each sentinel formation connects to **multiple wardens**, typically operated by different independent parties.

```
                    ┌─────────────────┐
                    │    Baseline     │
                    │   (GovOps)      │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
      ┌───────▼───────┐ ┌────▼────┐ ┌───────▼───────┐
      │   Warden A    │ │Warden B │ │   Warden C    │
      │ (Operator X)  │ │ (Op Y)  │ │  (Op Z)       │
      └───────────────┘ └─────────┘ └───────────────┘
```

### Warden Responsibilities

- **Continuous monitoring** — Watch Baseline behavior in real time
- **Invariant enforcement** — Check hard constraints (rate limits, position limits, risk thresholds)
- **Anomaly detection** — Flag unusual patterns that may indicate compromise or malfunction
- **Halt authority** — Can freeze the Execution Engine
- **Escalation** — Alert governance when intervention is needed

### What Wardens Do NOT Do

- Do not optimize or trade
- Do not stream intent
- Do not have discretion over strategy
- Only enforce safety invariants

---

## Time to Shutdown (TTS)

The number and quality of wardens determines a critical parameter: **Time to Shutdown (TTS)**.

### Definition

TTS is the worst-case time between:
- A sentinel going rogue (t=0)
- All wardens detecting and halting it (t=TTS)

### Why TTS Matters

During the window [0, TTS], a rogue sentinel can cause damage bounded by rate limits:

```
Maximum Damage = Rate Limit × TTS
```

This creates two economic consequences:

### 1. Risk Capital Requirements

The Executor (Accordant to the Prime) must post operational risk capital to cover worst-case damage:

```
Required Risk Capital ≥ Rate Limit × TTS
```

**Better wardens → Lower TTS → Less risk capital required**

### 2. Rate Limit Constraints

If risk capital is fixed, TTS constrains maximum rate limits:

```
Max Rate Limit ≤ Risk Capital / TTS
```

**Better wardens → Lower TTS → Higher rate limits allowed**

### TTS Determinants

TTS is a function of:

| Factor | Effect on TTS |
|--------|---------------|
| Number of wardens | More wardens → lower TTS |
| Operator diversity | Geographic/organizational diversity → lower TTS |
| Monitoring latency | Faster detection → lower TTS |
| Response capability | Faster halt execution → lower TTS |
| Certification level | Audited wardens with SLAs → more reliable TTS |

### Warden Economics

This creates a market for warden services:

- **For Primes:** Better wardens = more operational efficiency (higher rate limits, lower capital requirements)
- **For Warden Operators:** Providing reliable, certified warden services is valuable
- **For the System:** Safety is priced in, not externalized

Wardens are **capital efficiency multipliers**, not overhead.

---

## Streams and Compounding

A **stream** is a continuously operating sentinel formation that deploys Prime (synomic) capital.

### The Compounding Loop

Streams generate outperformance relative to the Base Strategy. The operating teleonome earns private carry from this alpha.

That carry can be reinvested into **proprietary AGI capabilities**:
- Compute infrastructure
- Model training
- Proprietary data acquisition
- Additional embodiments

This creates the fastest known compounding loop:

```
Public Capital → Private Intelligence → Better Streams → More Carry → More Intelligence
```

### Why This Is Safe

Despite the compounding power, streams remain safe because:

1. **Synomic constraints** — All execution flows through public Baseline code
2. **Wardens** — Independent monitoring with halt authority
3. **Rate limits** — Maximum damage is bounded
4. **Revocability** — Beacons can be revoked by governance
5. **Risk capital** — Worst-case losses are collateralized

The teleonome gains private intelligence without gaining unchecked power.

### Why Streams Are High-Leverage

Operating streams is the **highest-leverage activity** available to a teleonome because:

1. Deploys capital at scale (Prime capital, not just owned assets)
2. Generates carry without exposing proprietary strategies
3. Compounds into capabilities that improve future performance
4. Operates within safe bounds that prevent catastrophic outcomes

---

## Streaming Accord

The **Streaming Accord** is a smart contract framework governing the Baseline ↔ Stream relationship.

### Accord Components

| Component | Purpose |
|-----------|---------|
| **Risk Tolerance Interval** | Bounds on what intent Baseline will accept |
| **Performance Fee Ratio** | Share of alpha that becomes carry |
| **Termination Conditions** | When the accord can be dissolved |
| **Dispute Resolution** | How disagreements are handled |

### Risk Tolerance Interval

Defines the envelope of acceptable intent:

- Position limits (max exposure per asset, per category)
- Velocity limits (max change per time period)
- Concentration limits (max single-counterparty exposure)
- Prohibited actions (blacklisted assets, strategies)

Baseline **rejects** any intent outside this interval.

### Performance Fee Ratio

Typical structure:
- 0% of underperformance (Stream bears downside)
- X% of outperformance (Stream shares upside)

X is negotiated in the accord, reflecting:
- Stream's track record
- Complexity of strategy
- Risk profile

---

## Trade Beacon (HPLA)

For completeness: **Trade Beacons** are the HPLA equivalent of sentinel formations, but for **private capital**.

**Profile:** HPLA (High Power, Low Authority)
**Operator:** Ecosystem Actors
**Capital:** Private (owned via multisig)

### Differences from Sentinels

| Aspect | Sentinel Formation | Trade Beacon |
|--------|-------------------|--------------|
| Capital | Prime (Synomic Agent) | Private (owned) |
| Profile | HPHA | HPLA |
| Governance | Subject to Prime governance | Independent |
| Wardens | Required | Optional |
| Carry | Earned from Prime | N/A (own profits) |

### Trade Beacon Uses

- Proprietary trading on owned assets
- Testing strategies before proposing to Primes
- Ecosystem Actor commercial operations
- Cross-venue arbitrage with private capital

Trade beacons are documented in `beacon-framework.md`.

---

## Sentinel Toolkit

Sentinel formations use shared toolkit functions for common operations.

### lpla-checker (Verification and Settlement)

**Purpose:** Risk verification, anomaly detection, and settlement processing

Operations:
- Cross-check positions against risk limits
- Calculate CRR, TRRC, TRC, Encumbrance Ratio
- Flag discrepancies and anomalies
- Calculate PnL
- Calculate interest payable
- Determine carry amounts
- Process weekly settlement cycle

Used by: Baseline (for self-monitoring), Wardens (for independent verification), Baseline (at settlement periods)

### stk-carry (Carry Calculation)

**Purpose:** Performance attribution

Operations:
- Compare actual returns vs counterfactual baseline
- Calculate carry per Streaming Accord
- Facilitate fee distribution

Used by: Baseline (for Stream compensation)

---

## Formation Lifecycle

### 1. Accord Negotiation

- Ecosystem Actor proposes to operate Stream for a Prime
- Terms negotiated: Risk Tolerance Interval, Performance Fee Ratio
- Accord deployed as smart contract

### 2. Formation Assembly

- Baseline Sentinel deployed by Accordant GovOps
- Stream Sentinel deployed by Ecosystem Actor
- Wardens engaged (minimum required number)
- All components register in Synome

### 3. Activation

- Formation begins operating
- Stream starts sending intent
- Baseline executes (or falls back to Base Strategy)
- Wardens monitor continuously

### 4. Ongoing Operation

- Continuous trading within Risk Tolerance Interval
- Periodic settlement and carry distribution
- Warden attestations logged to Synome

### 5. Termination

Triggers:
- Accord expiration
- Mutual agreement
- Breach of terms
- Governance intervention
- Warden-triggered halt (if not resolved)

---

## Connection to Laniakea Infrastructure

### PAU Pattern

Sentinel formations operate PAUs within governance-approved bounds:

- Baseline holds pBEAMs granted by Prime governance
- Rate limits constrain maximum velocity
- SORL (20%/18h) constrains rate limit increases

### Execution Engine

The Execution Engine component:
- Held only by Baseline
- Signs transactions for PAU operations
- Subject to warden freeze authority

### Synome Integration

Sentinel formations interact with Synome for:
- Counterfactual simulation logging
- Warden attestation storage
- Carry calculation inputs
- Formation status tracking

---

## Sentinel Contexts

Sentinel formations operate in different contexts depending on the Synomic Agent type:

### Prime-Side Sentinels

Prime sentinels manage capital deployment from Prime PAUs into yield opportunities.

| Sentinel | Role |
|----------|------|
| **stl-base-{prime}** | Baseline execution for Prime trading/deployment |
| **stl-stream-{prime}-{actor}** | Proprietary intelligence streaming |
| **stl-warden-{prime}-{operator}** | Independent risk oversight |

**Flow:** Risk capital ingression → leverage deployment → yield capture

### Halo LPHA Beacons

Capital flows through Halo Unit PAUs into RWA endpoints are managed by **LPHA beacons** (Low Power, High Authority keepers), not sentinels.

> **Note:** lpha-lcts and lpha-nfat are LPHA beacons that execute deterministic rules on behalf of Halos. They are distinct from sentinels (stl-base, stl-stream, stl-warden) which have continuous real-time control and proprietary intelligence. LPHA beacons apply rules exactly as written without judgment.

| LPHA Beacon | Halo Type | Role |
|-------------|-----------|------|
| **lpha-lcts-{halo}** | Passthrough Halo | Operates LCTS vaults — deposits, redemptions, capacity management |
| **lpha-nfat-{halo}** | Structuring Halo | Operates NFAT Facilities — claims from queues, mints NFATs, funds redemptions |

**Flow:** LCTS/NFAT issuance → capital deployment to RWA endpoint → yield distribution

### Protocol-Level Beacons

Shared infrastructure across all Primes and Halos:

| Beacon | Role |
|--------|------|
| **lpla-checker** | Position verification, compliance checks, risk framework calculations, weekly settlement cycle, LCTS generation processing |

---

## Naming Conventions

### Prime Formation Components

```
stl-base-{prime}                  # Baseline for specific Prime
stl-stream-{prime}-{actor}        # Stream operated by specific actor
stl-warden-{prime}-{operator}     # Warden operated by specific party
```

### Halo LPHA Beacons

```
lpha-lcts-{halo}                   # LPHA beacon: LCTS vault operations for Passthrough Halo
lpha-nfat-{halo}                   # LPHA beacon: NFAT Facility operations for Structuring Halo
```

### Protocol-Level Beacons

```
lpla-checker                      # Protocol-wide position verification and settlement processing
```

### Examples

```
# Prime formations
stl-base-spark                    # Spark Prime's Baseline
stl-stream-spark-horizonlabs      # Horizon Labs streaming for Spark
stl-warden-spark-sentinelco       # SentinelCo warden for Spark
stl-warden-spark-riskwatch        # RiskWatch warden for Spark

# Halo LPHA beacons
lpha-lcts-jaaa                     # LCTS operations for JAAA Passthrough Halo
lpha-nfat-grove-structured         # NFAT operations for Grove's Structuring Halo
```

---

## Summary

> Sentinels are the live edge of Laniakea — where teleonome intelligence meets Synomic Agent capital.

### Sentinel Type Hierarchy

| Type | Description |
|------|-------------|
| **stl-base** | Primary execution sentinel for formations |
| **stl-stream** | Proprietary intelligence streaming |
| **stl-warden** | Independent safety oversight |

> **Note:** Halo operations (LCTS and NFAT) are handled by **LPHA beacons** (lpha-lcts, lpha-nfat), not sentinels. See the Halo LPHA Beacons section above and `beacon-framework.md` for the distinction.

### Key Principles

1. **Sentinels are HPHA beacons** — distinguished by continuous real-time control
2. **Both Primes and Halos can have sentinel formations** — any PAU can be sentinel-operated
3. **Formations, not individuals** — Baseline + Stream + Wardens
4. **Separation of concerns** — Execution (Baseline), Intelligence (Stream), Safety (Wardens)
5. **Independence matters** — Wardens must be independent for TTS to be meaningful
6. **TTS economics** — Warden quality determines operational efficiency
7. **Compounding loop** — Streams enable intelligence accumulation within safe bounds

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| `beacon-framework.md` | Broader beacon taxonomy (LPLA, LPHA, HPLA, HPHA) |
| `passthrough-halo.md` | lpha-lcts beacon for LCTS-based Passthrough Halos |
| `structuring-halo.md` | lpha-nfat beacon for NFAT-based Structuring Halos |
| `sky-intents.md` | Intent-based trading infrastructure |
