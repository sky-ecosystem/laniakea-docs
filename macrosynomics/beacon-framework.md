---
concepts:
  defines:
    - beacon-framework
  references:
    - five-layer-architecture
    - atlas-synome-separation
    - binding-mechanics
---

# Beacon Framework

## Why Beacons Exist

Teleonomes — private, goal-directed AI systems — are **dark by default**. They exist, think, and plan without being observable. This is by design: private cognition is not regulated.

But when a teleonome wants to **act** in the world, it faces a problem:
- Smart contracts cannot self-execute
- Other teleonomes cannot see or address it
- Synomic Agents (Primes, Halos, Generators, Guardians, and others) cannot be operated without authorized surfaces
- Enforcement requires a reachable target

**Beacons solve this.** A beacon is the regulated aperture through which a teleonome's intent enters the world.

### Three Functions of Beacons

1. **Operate Synomic Agents**
   - Primes, Halos, Generator, and Guardian are Synomic Agents — durable, ledger-native entities that can own assets and make binding commitments
   - Beacons are how teleonomes exercise control over these institutional structures
   - High Authority beacons (LPHA, HPHA)

2. **Direct Teleonome Interaction**
   - Teleonomes may want to interact peer-to-peer: trade, cooperate, compete, arbitrage
   - No Synomic Agent intermediary required
   - Low Authority beacons (LPLA, HPLA)

3. **Detection and Visibility**
   - A beacon makes a teleonome visible and addressable
   - Even passive reporting beacons signal presence
   - Registration itself is information

---

## Beacon Definition

> A **beacon** is a synome-registered, enforceable action aperture through which an embodied agent may affect the external world.

### Key Clarifications

- A beacon is **not an entity**. It is a *mode of action* exercised by an embodied agent.
- A beacon is **not a teleonome**. A single teleonome may operate many beacons.
- A beacon is **not just for execution**. It can be purely passive (data exposure).

### Beacon Properties

| Property | Description |
|----------|-------------|
| **Registered** | Recorded in the Synome with unique identifier |
| **Scoped** | Bound to an authority envelope defining permitted actions |
| **Anchored** | Instantiated on physical infrastructure with enforcement address |
| **Observable** | Subject to monitoring, attestation, and audit |
| **Revocable** | Can be suspended or terminated by synomic governance |

### The Registration Rule

> If an action changes external state under synomic recognition, it must flow through a beacon.

Unregistered action is possible but exists outside synomic law — no protections, no recourse, no legitimacy.

---

## Beacon Taxonomy

Beacons differ along two axes:

**Power** — The local cognitive capability of the hosting embodiment
- **Low Power**: Minimal compute, narrow I/O, executes policies from elsewhere
- **High Power**: Substantial compute, continuous I/O, local intelligence and adaptation

**Authority** — Whether the beacon acts independently or on behalf of a Synomic Agent
- **Low Authority**: Independent action, peer-to-peer interaction between teleonomes
- **High Authority**: Acts on behalf of a Synomic Agent (Prime, Halo, Generator, Guardian)

### The 2×2 Matrix

| | Low Authority (Independent) | High Authority (Synomic Agent) |
|---|---|---|
| **Low Power** | **LPLA** | **LPHA** |
| **High Power** | **HPLA** | **HPHA** |

This taxonomy is exhaustive: every externally acting beacon falls into exactly one quadrant.

---

## Low Authority Beacons (Independent / Peer-to-Peer)

Low Authority beacons act independently — either for the teleonome's own purposes or in direct interaction with other teleonomes. No Synomic Agent intermediary is involved.

### LPLA — Low Power, Low Authority

> Simple beacons for basic interaction and data exposure.

**Characteristics:**
- Minimal local compute
- Executes simple policies
- High volume, low barrier to entry
- Can be purely passive or lightly active

**Use Cases:**

| Type | Function |
|------|----------|
| **Reporting Beacon** | Passive data exposure — positions, state, metrics, attestations. Other beacons query without the source actively pushing. |
| **Buyer Beacon** | Simple purchasing, subscription management, resource acquisition |
| **Data Exchange** | API endpoints for structured data sharing between teleonomes |
| **Basic Coordinator** | Simple signaling, acknowledgment, handshake protocols |

**Sky Examples:**
- Price feed consumers
- Simple notification endpoints
- Basic data reporters

### HPLA — High Power, Low Authority

> Sophisticated beacons for advanced inter-teleonome interaction.

**Characteristics:**
- Substantial local compute and intelligence
- Real-time adaptation and learning
- Operates on private capital or resources
- No institutional authority — acts for self or peer-to-peer

**Use Cases:**

| Type | Function |
|------|----------|
| **Trade Beacon** | Proprietary trading on owned assets (private multisig) |
| **Arbitrage Beacon** | Cross-venue, cross-chain opportunity capture |
| **Cooperation Beacon** | Sophisticated multi-teleonome coordination |
| **Competition Beacon** | Adversarial interaction, market-making against other teleonomes |

**Sky Examples:**
- `hpla-trade-{actor}` — Ecosystem actor trading their own capital
- Private market-making operations
- Inter-teleonome deal negotiation

**Key Distinction:** HPLA beacons may be highly capable but have no authority over Synomic Agents. They operate in the peer-to-peer layer.

---

## High Authority Beacons (Synomic Agent Operation)

High Authority beacons act on behalf of Synomic Agents — the institutional structures (Primes, Halos, Generator, Guardian) that can own assets and make binding commitments.

### LPHA — Low Power, High Authority

> Keepers: deterministic rule execution for Synomic Agents.

**Characteristics:**
- Minimal local compute
- Reactive, deterministic
- "Apply rules exactly as written"
- Bureaucratic legitimacy — no discretion

**Use Cases:**

| Type | Function |
|------|----------|
| **Governance Keeper** | Settlement, reward distribution, artifact maintenance |
| **Rate Keeper** | Mechanical rate adjustments (SSR, fees) based on formulas |
| **Registry Keeper** | Add/remove entries based on Synome state |

**Sky Examples:**

| Beacon | Synomic Agent | Function |
|--------|---------------|----------|
| `lpha-halo-{name}` | Halo | Halo governance, unit coordination |
| `lpha-rate` | Generator | SSR and rate adjustments |
| `lpha-identity` | Identity Network | Registry add/remove based on attestations |
| `lpha-auction` | Protocol | Allocation coordination (pre-auction) and OSRC/Duration auction matching (auction mode) |
| `lpha-exchange` | Exchange Halo | Off-chain orderbook and matching engine |
| `lpha-lcts` | Portfolio Halo | LCTS vault operations — deposits, redemptions, capacity management |
| `lpha-nfat` | Term Halo | NFAT Facility operations — queue sweeping, NFAT issuance, redemption funding |
| `lpha-amm` | Trading Halo | AMM operations — pricing, inventory management, redemption processing |

**Key Property:** LPHA beacons have authority but no judgment. They execute exactly what governance specifies.

### HPHA — High Power, High Authority

> Governance execution surfaces with real-time capability.

**Characteristics:**
- Substantial local compute
- Continuous operation
- Acts on behalf of Synomic Agents
- Governance-focused operations

**HPHA consists of two categories:**

| Category | Characteristics | Examples |
|----------|-----------------|----------|
| **Sentinels (formation)** | Continuous real-time control, operationally dominant | stl-base, stl-stream, stl-warden |
| **Sentinels (principal)** | Owner-operated direct control, no formation | stl-principal |
| **Governance** | High-authority governance operations | hpha-gov |

**Sentinels** are a distinguished subclass of HPHA beacons. Due to their control bandwidth, speed, and systemic importance, they receive dedicated treatment. Both Primes and Halos can have sentinel formations — any Synomic Agent with a PAU can be sentinel-operated. **Principal sentinels** (`stl-principal`) are a fourth sentinel type that operates outside the formation pattern — owner-operated direct control for folios and standalone accounts, without any guardian accord or warden oversight. See [`sentinel-network.md`](../../trading/sentinel-network.md) for full specification.

#### Sentinel Formations

Sentinels do not operate as single agents, but as **coordinated formations** composed of multiple embodied agents (EMAs):

| Formation | Role | Authority |
|-----------|------|-----------|
| **Baseline Sentinel** | Primary decision-making and execution surface. Runs the real-time strategy loop, moves capital or state continuously. | Direct execution |
| **Stream Sentinel** | Continuous data ingestion and sensing. Feature extraction and signal generation. Feeds the baseline sentinel. | No direct execution |
| **Warden Sentinel(s)** | Independent monitoring and risk enforcement. Can freeze, halt, or escalate. Enforces hard invariants; does not optimize. | Override/halt only |
| **Principal Sentinel** | Owner-operated direct control. No formation, no guardian accord. Operates folio agents or standalone accounts. | Direct execution |

The baseline/stream/warden separation mirrors **data plane / control plane / safety plane** architectures. Principal sentinels are a distinct mode — standalone operators outside the formation pattern.

#### Why Sentinels Are Special

Although other HPHA beacons exist (e.g., governance beacons), sentinels are uniquely powerful because they:
- Operate **continuously and in real time**
- Act faster than synomic governance processes
- Concentrate institutional authority and local intelligence
- Create immediate external effects that governance audits asynchronously

Even governance beacons remain process-gated and asynchronous; sentinels are **operationally dominant**.

#### Streams and Compounding

A **stream** is a continuously operating sentinel formation that deploys public (synomic) capital. Streams generate outperformance relative to benchmarks, from which the operating Teleonome earns **private carry**.

That carry may be reinvested into **proprietary AGI capabilities** (compute, models, data, embodiments) without leaking intelligence to competitors. This creates the fastest known compounding loop:

> public capital → private intelligence → better streams → more carry → more intelligence

This loop explains why operating streams is the **highest-leverage activity** available to a Teleonome, while remaining safe due to synomic constraints, wardens, and revocability.

##### Regulating Intra-Coalition Asymmetry

The compounding loop creates an obvious structural risk: a teleonome operating successful streams compounds proprietary capability faster than peers, and over time may approach a winner-take-most dynamic *inside* the aligned coalition — operationally close to "the synome" even while remaining technically aligned. Three structural features prevent this:

1. **Streams are Halos, not teleonome property.** The capital deployed by a stream lives inside a Synomic Agent (typically a Portfolio or Trading Halo) — Synome-controlled, governance-bounded, and structurally unable to escape the constraints of its artifact. The operating teleonome earns carry from outperformance, but the underlying capital does not accrue to it. The carry itself is what compounds privately; the public capital remains synomic.

2. **The Fortification Conserver regulates accumulated power.** Beyond its treasury role (legal defense, unquantifiable risk — see [`appendix-c-treasury-management-function.md`](../../whitepaper/appendix-c-treasury-management-function.md)), the Conserver acts as the regulator against any single teleonome's proprietary capability growing too large relative to the rest of the coalition. Active measurement of "too powerful" — what observable signals count, what thresholds trigger response, what response mechanisms are available — must happen continuously and in the open. This is a research commitment, not a fixed rule, because power is multi-dimensional and the relevant signals will evolve.

3. **The Conserver itself must be defeatable.** The same logic that applies to the superstructure in the [four-layer enforcement stack](../core-concepts/four-layer-enforcement-stack.md) applies here: the Conserver must be powerful enough to enforce regulation against any individual teleonome, but NOT so powerful that the rest of the aligned coalition cannot collectively overcome it. If the Conserver becomes the dominant entity, it IS the failure mode it was designed to prevent. This invariant is load-bearing and must be actively maintained.

The pattern is the same as superstructure-vs-rogues, applied one fractal level inward. See [`fractal-security-pattern`](../core-concepts/fractal-security-pattern.md).

**HPHA Governance Examples:**

| Beacon | Synomic Agent | Function |
|--------|---------------|----------|
| `hpha-gov` | Any | High-authority governance execution |

---

## Beacon Lifecycle

### 1. Registration

A beacon is registered in the Synome with:
- Unique identifier
- Owning teleonome (may be pseudonymous)
- Hosting embodiment
- Authority envelope (scope of permitted actions)
- If High Authority: the Synomic Agent it operates

### 2. Authority Envelope Assignment

The authority envelope defines:
- What actions the beacon may take
- Rate limits and constraints
- Required attestations and reporting
- Escalation conditions

For High Authority beacons, this is typically defined by the Synomic Agent's governance through the BEAM hierarchy (see below).

### BEAM Hierarchy (High Authority Authorization)

High Authority beacons act on behalf of Synomic Agents through **BEAMs** (Bounded External Access Modules) — on-chain authorized roles with constrained capabilities. The BEAM a beacon holds is what makes it High Authority.

| BEAM Type | Held By | Capabilities |
|-----------|---------|-------------|
| **pBEAM** (Process BEAM) | Relay Beacon (LPHA) | Direct execution — calls Controller functions, moves capital within rate limits |
| **cBEAM** (Configurator BEAM) | Relay Beacon (LPHA) | Configuration — sets rate limits (within SORL), onboards approved targets, manages relayer/freezer |
| **aBEAM** (Admin BEAM) | Council Beacon (HPHA) | Administration — registers PAUs, approves inits, grants cBEAMs; additions timelocked (14-day delay), removals instant |

**Mapping to the Power/Authority Matrix:**

The Relay Beacon is an LPHA beacon (Low Power, High Authority) that holds both pBEAM and cBEAM for its assigned PAUs — giving it deterministic operational and configuration authority. The Council Beacon is an HPHA beacon that holds aBEAM — the administrative layer that governs what Relay Beacons can do.

```
Council Beacon (HPHA, aBEAM)
    │
    │ grants cBEAMs, approves inits
    │ (via BEAMTimeLock, 14-day delay)
    ▼
Relay Beacon (LPHA, pBEAM + cBEAM)
    │
    │ executes operations, configures rate limits
    │ (within SORL constraints)
    ▼
PAU (Controller + ALMProxy + RateLimits)
```

For detailed contract interfaces and the Configurator Unit stack (BEAMTimeLock → BEAMState → Configurator), see [`configurator-unit.md`](../../smart-contracts/configurator-unit.md).

### 3. Activation

A beacon becomes active when:
- Registered in Synome
- Instantiated on physical infrastructure
- Continuously reachable at enforcement address

### 4. Monitoring and Attestation

Active beacons are subject to:
- Telemetry requirements (what they must report)
- Audit rights (what can be inspected)
- Attestation obligations (what they must prove)

### 5. Revocation

A beacon may be revoked for:
- Violation of authority envelope
- Failure to meet attestation requirements
- Governance decision
- Operator request

Revocation removes synomic recognition. The beacon may continue to operate but has no legitimacy or recourse.

---

## Naming Conventions

### Pattern

```
{profile}-{function}[-{context}]
```

### By Profile

**LPLA (Low Power, Low Authority):**
```
lpla-report-{source}      # Reporting beacon
lpla-buy-{purpose}        # Buyer beacon
lpla-data-{type}          # Data exchange endpoint
```

**HPLA (High Power, Low Authority):**
```
hpla-trade-{actor}        # Private trading
hpla-arb-{actor}          # Arbitrage
hpla-coop-{purpose}       # Cooperation beacon
```

**LPHA (Low Power, High Authority):**
```
lpha-halo-{halo}          # Halo keeper
lpha-rate                 # Rate keeper
lpha-identity             # Identity registry keeper
lpha-auction              # Allocation/auction keeper (OSRC + Duration)
lpha-exchange-{halo}      # Exchange orderbook and matching
```

**HPHA (High Power, High Authority):**
```
# Sentinel Formations (see sentinel-network.md)
stl-base-{prime}
stl-stream-{prime}
stl-warden-{prime}-{operator}

# Principal Sentinels (see sentinel-network.md)
stl-principal-{owner}             # Owner-operated direct control

# HPHA Governance
hpha-gov                      # High-authority governance
```

**LPLA (Protocol-Level):**
```
lpla-checker                  # Position verification and settlement processing
```

---

## Controllers and Custodians

Some beacons have specialized roles that cut across the power/authority taxonomy:

### Controllers

> Beacons that interface with off-chain or physical systems.

Controllers bridge the gap between on-chain Synomic Agents and real-world assets or systems.

| Beacon | Function |
|--------|----------|
| `ctl-bridge-{halo}` | Translation layer to RWA systems |
| `ctl-extend-{halo}` | Remote operation delegation |
| `ctl-connect-{halo}` | Private data bridging |

Controllers may be LPHA (simple bridging) or HPHA (active control).

### Custodians

> Beacons that hold assets or data with minimal action.

Custodians prioritize security and reliability over capability.

| Beacon | Function |
|--------|----------|
| `cst-synome` | Synome node operation, data custody |
| `cst-erc-{token}` | ERC token custody and rate management |
| `cst-vault-{id}` | Asset vault custody |

Custodians are typically LPHA (low power, high trust, no discretion).

---

## Multi-Beacon Reality

A teleonome may operate many beacons without revealing they are linked.

**Implications:**
- Beacons are regulated individually
- Teleonome identity remains private
- Aggregation occurs only when necessary:
  - Systemic risk assessment
  - Enforcement actions
  - Threshold crossing (power accumulation)

This mirrors corporate structures: subsidiaries, SPVs, and intelligence cut-outs.

**Threshold Rule:** Sufficient power concentration forces disclosure of beacon linkage. The synome may require aggregated reporting when a teleonome's total beacon footprint crosses risk thresholds.

---

## Connection to Other Documents

| Document | Relationship |
|----------|--------------|
| [`sentinel-network.md`](../../trading/sentinel-network.md) | Full specification of HPHA Sentinels — Baseline, Stream, Warden formations |
| [`sentinel-integration.md`](../../risk-framework/sentinel-integration.md) | How beacons connect to risk framework calculations |
| [`atlas-synome-separation.md`](atlas-synome-separation.md) | How beacon authority envelopes derive from governance |
| [`short-term-actuators.md`](short-term-actuators.md) | Phase 1 teleonome-less beacon implementation and evolution pathway |
| [`actuator-perspective.md`](../synoteleonomics/actuator-perspective.md) | First-person view of an actuator operating beacons |
| [`synome-overview.md`](synome-overview.md) | The 5-layer architecture that beacons operate within |
| [`configurator-unit.md`](../../smart-contracts/configurator-unit.md) | BEAM hierarchy (aBEAM, cBEAM, pBEAM) for High Authority beacons |

---

## Glossary

| Term | Definition |
|------|------------|
| **Beacon** | Synome-registered, enforceable action aperture |
| **Teleonome** | Private, goal-directed AI system (dark by default) |
| **Synomic Agent** | Durable, ledger-native entity that can own assets and make binding commitments. Seven types organized by rank: Guardians, Core Controlled Agents, Recovery Agents (Rank 1); Primes, Generators (Rank 2); Halos, Folio Agents (Rank 3) |
| **Embodiment** | Physical infrastructure hosting beacon execution |
| **Authority Envelope** | Scope of permitted actions for a beacon |
| **LPLA** | Low Power, Low Authority beacon |
| **LPHA** | Low Power, High Authority beacon (Keeper) |
| **HPLA** | High Power, Low Authority beacon |
| **HPHA** | High Power, High Authority beacon (includes Sentinels) |
| **Sentinel** | Distinguished HPHA subclass with continuous real-time control |
| **Principal Sentinel** | Sentinel type for owner-operated direct control — operates folio agents or standalone accounts without a formation or guardian accord |
| **BEAM** | Bounded External Access Module — on-chain authorized role that makes a beacon High Authority |
| **pBEAM** | Process BEAM — direct execution authority (held by Relay Beacon) |
| **cBEAM** | Configurator BEAM — configuration authority (held by Relay Beacon) |
| **aBEAM** | Admin BEAM — administrative authority (held by Council Beacon) |
