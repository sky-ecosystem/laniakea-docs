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

## 1. Why Beacons Exist

Teleonomes — private, goal-directed AI systems — are **dark by default**. They exist, think, and plan without being observable. This is by design: private cognition is not regulated.

But when a teleonome wants to **act** in the world, it faces a problem:
- Smart contracts cannot self-execute
- Other teleonomes cannot see or address it
- Synomic Agents (Primes, Halos, Generators, Guardians) cannot be operated without authorized surfaces
- Enforcement requires a reachable target

**Beacons solve this.** A beacon is the regulated aperture through which a teleonome's intent enters the world.

### Three Functions of Beacons

1. **Operate Synomic Agents.** Primes, Halos, Generator, and Guardian are durable, ledger-native entities that can own assets and make binding commitments. High-authority beacons are how teleonomes exercise control over these institutional structures.
2. **Direct Teleonome Interaction.** Teleonomes may want to interact peer-to-peer: trade, cooperate, compete, arbitrage. No Synomic Agent intermediary required. Low-authority beacons.
3. **Detection and Visibility.** A beacon makes a teleonome visible and addressable. Even passive reporting beacons signal presence. Registration itself is information.

---

## 2. Beacon Definition

> A **beacon** is a synome-registered, enforceable action aperture through which an embodied agent may affect the external world.

### Key Clarifications

- A beacon is **not an entity**. It is a *mode of action* exercised by an embodied agent.
- A beacon is **not a teleonome**. A single teleonome may operate many beacons.
- A beacon is **not a calculator**. Calculation lives in synart-resolved in-space computation; beacons are pure I/O (see §4).

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

## 3. Authority Tier — The Load-Bearing Axis

Beacons are classified primarily by **authority**:

| Tier | What it is |
|---|---|
| **High authority** | Certified by a synomic agent; auth-scoped to specific verbs/targets; operates a Synomic Agent (Prime / Halo / Generator / Guardian). |
| **Low authority** | No Synomic Agent operation. Either passive observation OR direct teleonome-to-teleonome interaction. |

This is the only axis the framework treats as load-bearing. The roles, names, and concrete classes underneath authority are working cuts, not constitutional commitments.

### Why power-as-axis retired

The earlier framework classified beacons along two axes — power (local cognitive capability) and authority. Power was load-bearing because beacons did real cognitive work: a sentinel that ran its own decision loop needed substantial local compute. With cognition migrated into synart-resolved in-space computation, beacons no longer carry decision logic. They witness, sign, and submit; calculation happens elsewhere. Embodiment power levels still matter for hardware-aware cognition (see [`../neurosymbolic/hardware-aware-cognition.md`](../neurosymbolic/hardware-aware-cognition.md)) but no longer classify beacons.

---

## 4. I/O Role Under Authority

Underneath authority, beacons split by **work shape**: input vs action. This is non-prescriptive — a working cut, not load-bearing. Concrete classes are first-cut sketches.

### Input beacons — push data into book spaces

| Class | Reads from | Writes |
|---|---|---|
| **Endoscraper** | On-chain protocol state (deterministic, public) | Chain events, contract state deltas, redemption flows |
| **Oracle** | Off-chain market data (price feeds, indices, FX rates) | Price atoms, index updates |
| **Attestor** | Off-chain claims (custody balances, contract terms, compliance facts) | Signed attestation atoms |

Trust models differ:
- Endoscrapers are deterministic (chain reads); verifiable by re-scraping
- Oracles are pushed data with provider trust; verifiable by oracle redundancy / dispute mechanisms
- Attestors are signed off-chain claims with attestor liability; verified at slashing time, not at write time

### Action beacons — emit chain txs based on synart state

| Class | Acts on | Authority |
|---|---|---|
| **Relayer** | Submits governance-initiated or user-initiated txs to chain | Narrow, per-target |
| **Executor** | Executes strategies derived in synart (settlement, rebalance, etc.) | Scoped to specific verbs and targets |
| **Sentinel formation** | Baseline / Stream / Warden patterns operating Primes or Halos (see §6) | Broader; with formation-internal checks |

Action beacons read synart state to decide what to do; they don't calculate it themselves.

### In-space calculation — where calculation lives now

For each book (Riskbook, Halobook, Primebook, Genbook, Generator's structural-demand space), synserv runs whatever calculation is needed to keep its derived state (equity, CRR, matching status, breach flags, encumbrance ratio, etc.) consistent with current input atoms, in real time. The calculation logic is synart-resolved code; synserv executes it.

```
endoscraper write ────┐
                      │
oracle write ─────────┼──→ atom lands in book space
                      │
attestor write ───────┘
                          │
                          ▼
                    synserv re-derives the book's derived state
                    from current input atoms
                          │
                          ▼
                    derived atoms updated in the book space;
                    replicated to subscribers
```

Three consequences:

1. **Full verifiability.** Wardens can re-derive everything because the calculation is synart code, not opaque off-loop compute.
2. **Beacons become pure I/O.** Input beacons push data; action beacons emit chain txs based on synart state. No calculation in either.
3. **No lag.** Derived state always reflects current input atoms.

The implementation mechanism (event-driven, heartbeat poll, hybrid) is deferred to Phase 1. The invariant that holds regardless: **derived state in any book is a deterministic function of its current input atoms, and synserv is responsible for keeping it current.**

---

## 5. Low Authority Beacons

Low Authority beacons act independently — either for the teleonome's own purposes or in direct interaction with other teleonomes. No Synomic Agent intermediary is involved.

### Reporting / Observation Beacons (Input)

> Passive data exposure — positions, state, metrics, attestations.

Endoscraper-shaped or attestor-shaped beacons emitting facts into the synart for general consumption. Other beacons query without the source actively pushing.

**Sky examples:** price feed consumers, simple notification endpoints, basic data reporters.

### Buyer / Subscriber Beacons (Input/Action)

> Simple purchasing, subscription management, resource acquisition.

Low operational authority; bounded by rate limits.

### Peer-to-Peer Trade Beacons (Action)

> Sophisticated trading on owned assets (private multisig).

The teleonome's own capital, deployed on its own behalf, without operating any Synomic Agent. Substantial local capability is permitted; the absence of Synomic Agent operation is what makes this low authority.

**Sky examples:** `hpla-trade-{actor}` (legacy name, retained — see Glossary §11) — ecosystem actor trading their own capital.

### Arbitrage / Cooperation Beacons (Action)

> Cross-venue, cross-chain opportunity capture; sophisticated multi-teleonome coordination.

Inter-teleonome deal negotiation, peer-to-peer market-making, adversarial market-making against other teleonomes.

**Key distinction:** these may be highly capable but have no authority over Synomic Agents. They operate in the peer-to-peer layer.

---

## 6. High Authority Beacons

High Authority beacons act on behalf of Synomic Agents — the institutional structures (Primes, Halos, Generator, Guardian) that can own assets and make binding commitments.

### Deterministic Keepers (Action)

> Apply rules exactly as written.

Reactive, deterministic, no discretion — bureaucratic legitimacy.

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

These names retain their `lp*` prefix as legacy operational identifiers (see Glossary §11). The prefix no longer encodes a power axis; what makes them high-authority is the BEAM hierarchy (§7) plus auth-scoped operation of a Synomic Agent.

### Sentinel Formations (Action)

A distinguished high-authority action subclass. Sentinels do not operate as single agents, but as **coordinated formations** composed of multiple embodied agents (EMAs):

| Formation | Role | Authority |
|-----------|------|-----------|
| **Baseline Sentinel** | Primary decision-making and execution surface. Runs the real-time strategy loop, moves capital or state continuously. | Direct execution |
| **Stream Sentinel** | Continuous data ingestion and sensing. Feature extraction and signal generation. Feeds the baseline sentinel. | No direct execution |
| **Warden Sentinel(s)** | Independent monitoring and risk enforcement. Can freeze, halt, or escalate. Enforces hard invariants; does not optimize. | Override/halt only |
| **Principal Sentinel** | Owner-operated direct control. No formation, no guardian accord. Operates folio agents or standalone accounts. | Direct execution |

The baseline/stream/warden separation mirrors **data plane / control plane / safety plane** architectures. Principal sentinels are a distinct mode — standalone operators outside the formation pattern.

#### Why Sentinels Are Special

Although other high-authority beacons exist (e.g., governance beacons), sentinels are uniquely powerful because they:
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

3. **The Conserver itself must be defeatable.** The Conserver must be powerful enough to enforce regulation against any individual teleonome, but NOT so powerful that the rest of the aligned coalition cannot collectively overcome it. If the Conserver becomes the dominant entity, it IS the failure mode it was designed to prevent. This invariant is load-bearing and must be actively maintained.

See [`fractal-security-pattern`](../core-concepts/fractal-security-pattern.md) for the general pattern.

### Governance Beacons (Action)

| Beacon | Synomic Agent | Function |
|--------|---------------|----------|
| `hpha-gov` | Any | High-authority governance execution (legacy name, retained — see Glossary §11) |

---

## 7. BEAM Hierarchy (Chain-Side, Orthogonal)

High Authority beacons act on behalf of Synomic Agents through **BEAMs** (Bounded External Access Modules) — on-chain authorized roles with constrained capabilities. The BEAM a beacon holds is what makes it high-authority *in the smart-contract sense*. BEAMs are orthogonal to the input/action role taxonomy in §4.

| BEAM Type | Held By | Capabilities |
|-----------|---------|-------------|
| **pBEAM** (Process BEAM) | Relay Beacon (deterministic keeper) | Direct execution — calls Controller functions, moves capital within rate limits |
| **cBEAM** (Configurator BEAM) | Relay Beacon (deterministic keeper) | Configuration — sets rate limits (within SORL), onboards approved targets, manages relayer/freezer |
| **aBEAM** (Admin BEAM) | Council Beacon (governance) | Administration — registers PAUs, approves inits, grants cBEAMs; additions timelocked (14-day delay), removals instant |

```
Council Beacon (high-authority, aBEAM)
    │
    │ grants cBEAMs, approves inits
    │ (via BEAMTimeLock, 14-day delay)
    ▼
Relay Beacon (high-authority deterministic keeper, pBEAM + cBEAM)
    │
    │ executes operations, configures rate limits
    │ (within SORL constraints)
    ▼
PAU (Controller + ALMProxy + RateLimits)
```

For detailed contract interfaces and the Configurator Unit stack (BEAMTimeLock → BEAMState → Configurator), see [`configurator-unit.md`](../../smart-contracts/configurator-unit.md).

---

## 8. Beacon Lifecycle

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

For High Authority beacons, this is typically defined by the Synomic Agent's governance through the BEAM hierarchy (§7).

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

## 9. Naming Conventions

### Pattern

```
{legacy-prefix}-{function}[-{context}]
```

The legacy `lpla` / `lpha` / `hpla` / `hpha` prefixes survive as operational identifiers in deployed beacon names. They do not encode the retired power axis. They serve as stable handles for ops/governance reference. New beacon classes need not adopt these prefixes.

### By Authority Tier and Role

**Low-authority input/observation:**
```
lpla-report-{source}      # Reporting beacon
lpla-data-{type}          # Data exchange endpoint
endoscraper-{protocol}    # Per-protocol chain scraper
oracle-{provider}         # Off-chain feed
attestor-{halo-class}     # Off-chain claim attestor
```

**Low-authority action (peer-to-peer):**
```
hpla-trade-{actor}        # Private trading
hpla-arb-{actor}          # Arbitrage
hpla-coop-{purpose}       # Cooperation beacon
```

**High-authority action (deterministic keeper):**
```
lpha-halo-{halo}          # Halo keeper
lpha-rate                 # Rate keeper
lpha-identity             # Identity registry keeper
lpha-auction              # Allocation/auction keeper (OSRC + Duration)
lpha-exchange-{halo}      # Exchange orderbook and matching
lpha-lcts                 # LCTS vault keeper
lpha-nfat                 # NFAT facility keeper
lpha-amm                  # AMM keeper
```

**High-authority action (sentinel formations):**
```
stl-base-{prime}
stl-stream-{prime}
stl-warden-{prime}-{operator}
stl-principal-{owner}     # Owner-operated direct control
```

**High-authority action (governance):**
```
hpha-gov                  # High-authority governance
```

### Verification (Synserv-Run, Not a Beacon Class)

Position verification, settlement processing, and CRR calculation are not beacon roles in the new framework. They run as synart-resolved code inside synserv (per §4 in-space calculation). The legacy `lpla-checker` identifier no longer names a beacon class. Any document referencing it should be read as "synserv verification" against the same scraped inputs.

---

## 10. Controllers and Custodians

Some beacons have specialized roles that cut across the authority/role taxonomy:

### Controllers

> Beacons that interface with off-chain or physical systems.

Controllers bridge the gap between on-chain Synomic Agents and real-world assets or systems.

| Beacon | Function |
|--------|----------|
| `ctl-bridge-{halo}` | Translation layer to RWA systems |
| `ctl-extend-{halo}` | Remote operation delegation |
| `ctl-connect-{halo}` | Private data bridging |

Controllers are typically high-authority action beacons (deterministic bridging or active control).

### Custodians

> Beacons that hold assets or data with minimal action.

Custodians prioritize security and reliability over capability.

| Beacon | Function |
|--------|----------|
| `cst-synome` | Synome node operation, data custody |
| `cst-erc-{token}` | ERC token custody and rate management |
| `cst-vault-{id}` | Asset vault custody |

Custodians are typically high-authority deterministic keepers — high trust, no discretion.

---

## 11. Multi-Beacon Reality

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
| [`sentinel-network.md`](../../trading/sentinel-network.md) | Full specification of high-authority Sentinels — Baseline, Stream, Warden, Principal |
| [`sentinel-integration.md`](../../risk-framework/sentinel-integration.md) | How beacons connect to risk framework calculations |
| [`atlas-synome-separation.md`](atlas-synome-separation.md) | How beacon authority envelopes derive from governance |
| [`short-term-actuators.md`](short-term-actuators.md) | Phase 1 teleonome-less beacon implementation and evolution pathway |
| [`actuator-perspective.md`](../synoteleonomics/actuator-perspective.md) | First-person view of an actuator operating beacons |
| [`synome-overview.md`](synome-overview.md) | The 5-layer architecture that beacons operate within |
| [`configurator-unit.md`](../../smart-contracts/configurator-unit.md) | BEAM hierarchy (aBEAM, cBEAM, pBEAM) for High Authority beacons |
| [`../../noemar-synlang/listener-loops.md`](../../noemar-synlang/listener-loops.md) | In-space calculation pattern (sketch; implementation deferred) |
| [`../../noemar-synlang/beacons.md`](../../noemar-synlang/beacons.md) | Phase 1 beacon implementation sketches and per-protocol details |

---

## 12. Glossary

### Active framework terms

| Term | Definition |
|------|------------|
| **Beacon** | Synome-registered, enforceable action aperture |
| **Teleonome** | Private, goal-directed AI system (dark by default) |
| **Synomic Agent** | Durable, ledger-native entity that can own assets and make binding commitments. Seven types organized by rank: Guardians, Core Controlled Agents, Recovery Agents (Rank 1); Primes, Generators (Rank 2); Halos, Folio Agents (Rank 3) |
| **Embodiment** | Physical infrastructure hosting beacon execution |
| **Authority Envelope** | Scope of permitted actions for a beacon |
| **High Authority** | Beacon that operates a Synomic Agent (auth-scoped to specific verbs/targets) |
| **Low Authority** | Beacon that does not operate a Synomic Agent (passive observation OR peer-to-peer interaction) |
| **Input Beacon** | Beacon whose work shape is pushing data atoms into book spaces (endoscraper / oracle / attestor) |
| **Action Beacon** | Beacon whose work shape is emitting chain transactions based on synart state (relayer / executor / sentinel formation) |
| **Sentinel** | Distinguished high-authority action subclass with continuous real-time control |
| **Principal Sentinel** | Sentinel type for owner-operated direct control — operates folio agents or standalone accounts without a formation or guardian accord |
| **In-space calculation** | Synart-resolved code, run by synserv, that derives book state (equity, CRR, ER, etc.) from current input atoms in real time |
| **BEAM** | Bounded External Access Module — on-chain authorized role that makes a beacon high-authority in the smart-contract sense |
| **pBEAM** | Process BEAM — direct execution authority (held by Relay Beacon) |
| **cBEAM** | Configurator BEAM — configuration authority (held by Relay Beacon) |
| **aBEAM** | Admin BEAM — administrative authority (held by Council Beacon) |

### Historical naming

The earlier framework classified beacons along two axes — power and authority — yielding four quadrants. Power-as-axis retired when cognition migrated into synart-resolved in-space computation. The four-letter codes survive only as legacy operational prefixes on deployed beacon names; they do not classify the beacons in the current framework.

| Legacy code | Authority tier | I/O role | Status |
|---|---|---|---|
| **LPLA** | Low | Input (passive observation) | Retired as primary classification. Surviving prefix on legacy reporting/scraper names. |
| **LPHA** | High | Action (deterministic keeper) | Retired as primary classification. Surviving prefix on legacy keeper names (`lpha-nfat`, `lpha-lcts`, `lpha-rate`, etc.). |
| **HPLA** | Low | Action (peer-to-peer) | Retired as primary classification. Surviving prefix on legacy peer-to-peer trade beacon names (`hpla-trade-*`). |
| **HPHA** | High | Action (sentinel formation or governance) | Retired as primary classification. Sentinel formations are now described as a "high-authority action subclass." Surviving prefix on `hpha-gov`. |
| **lpla-checker** | — | — | Disappears as a beacon class. The verification role survives but runs as synart-resolved code inside synserv (in-space calculation, §4), not as a separate beacon. |

### Old → new mapping

| Old beacon name / class | New role | Notes |
|---|---|---|
| `lpla-checker` | **Disappears** | Calculation moves to synart-resolved in-space code; see §4 |
| `lpla-verify` | **Verifier emb** (not a beacon class) | Re-derivation via shadow execution |
| `lpha-relay` | **High-authority action beacon (relayer)** | Already pure I/O |
| `lpha-nfat` | **High-authority action beacon (executor)** | Submits NFAT txs based on synart state |
| `lpha-lcts` | **High-authority action beacon (executor)** | LCTS vault operations |
| `lpha-council` | **High-authority action beacon (executor)** | Council ops |
| `lpha-halo` | **Endoscraper or attestor** depending on data source | Reporting role; on-chain → endoscraper, off-chain → attestor |
| `endoscraper-<protocol>` | **Low-authority input beacon** | Already in the new shape |
| `stl-base` / `stl-stream` / `stl-warden` / `stl-principal` | **Sentinel formation (high-authority action)** | Naming and formation pattern unchanged |
| `hpha-gov` | **High-authority action beacon (governance)** | Naming retained |

### Open questions (deferred to Phase 1)

1. **Concrete class implementations** — per-protocol endoscrapers, oracle providers (Chronicle, Chainlink, etc.), attestor templates and slashing terms.
2. **Oracle vs attestor boundary** — they differ in trust model (push vs pull, who signs, what the slashing surface looks like). Some data sources blur the line; need clear per-class definitions.
3. **Action-beacon authority scope** — Phase 1 has narrow, manually-authed beacons; later phases give Sentinel formations broader scope. The auth grant/revocation mechanics are settled; the per-class scope policies aren't.
4. **In-space calculation mechanism** — event-driven, heartbeat poll, or hybrid. Resolved by Phase 1 implementation.
5. **Verifier embs vs verifier beacons** — verifier embs shadow-execute loops; whether a separate verifier beacon class is also needed, or whether shadow execution covers it entirely.
