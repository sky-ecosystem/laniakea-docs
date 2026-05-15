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
- Synomic Entities (Primes, Halos, Generators, Guardians, Oracle Entities, etc.) cannot be operated without authorized surfaces
- Enforcement requires a reachable target

**Beacons solve this.** A beacon is the regulated aperture through which a teleonome's intent enters the world.

### Three Functions of Beacons

1. **Operate Synomic Entities.** Synomic Entities are durable, ledger-native entities that can own assets and make binding commitments. High-authority beacons are how teleonomes exercise control over these institutional structures.
2. **Direct Teleonome Interaction.** Teleonomes may want to interact peer-to-peer: trade, cooperate, compete, arbitrage. No Synomic Entity intermediary required. Low-authority beacons.
3. **Detection and Visibility.** A beacon makes a teleonome visible and addressable. Even passive reporting beacons signal presence. Registration itself is information.

---

## 2. Beacon Definition

> A **beacon** is a synome-registered, enforceable action aperture through which an embodied agent may affect the external world.

### Key Clarifications

- A beacon is **not an entity**. It is a *mode of action* exercised by an embodied agent.
- A beacon is **not a teleonome**. A single teleonome may operate many beacons.
- A beacon is **not a calculator**. Calculation lives in synart-resolved in-space computation; beacons are pure I/O (see §4).
- A beacon is **not a gate**. Gates (`&core.syngate`, `&core.telgate`, per-tel embgate implementations) are *programs* — protocol code that beacons run. Beacons are *active processes* that use the gate programs. Synserv is a beacon (it runs the syngate program). The gates themselves are libraries, not actors.

### Beacon Properties

| Property | Description |
|----------|-------------|
| **Registered** | Recorded in the Synome with unique identifier (row in `&core.registry.beacon`) |
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
| **High authority** | Certified by a synomic entity; auth-scoped to specific verbs/targets; operates a Synomic Entity (Prime / Halo / Generator / Guardian / Oracle Entity / etc.). |
| **Low authority** | No Synomic Entity operation. Either passive observation OR direct teleonome-to-teleonome interaction. |

This is the only axis the framework treats as load-bearing.

### Why power-as-axis retired

The earlier framework classified beacons along two axes — power (local cognitive capability) and authority. Power was load-bearing because beacons did real cognitive work: a sentinel that ran its own decision loop needed substantial local compute. With cognition migrated into synart-resolved in-space computation, most beacons no longer carry decision logic; they witness, sign, and submit. The exception is **sentinels** (§6) which retain call-out density into operator telart for genuinely-cognitive work — but cognition is now a class property, not a separate axis. Embodiment power levels still matter for hardware-aware cognition (see [`../neurosymbolic/hardware-aware-cognition.md`](../neurosymbolic/hardware-aware-cognition.md)) but no longer classify beacons.

---

## 4. Class Taxonomy (six classes plus synserv)

Beacons split into six classes, differentiated by I/O direction and cognitive density. **Synserv** is a special singleton outside the class taxonomy.

| Class | I/O | Cognition | Admin'd by |
|---|---|---|---|
| **market-data-beacon** | input | none | Oracle Entity |
| **attest-data-beacon** | input | none | Oracle Entity |
| **patch-beacon** | input | none | Guardian via govops (no regulated framework) |
| **relay** | action | none — pure synart-resolved I/O | Synomic Entity (Prime / Halo / Generator / etc.) |
| **sentinel** | action | call-out density into operator telart | Synomic Entity; variants: **stream**, **principal-sentinel** |
| **synserv** | special | none | Core Council (singleton; runs the canonical heartbeat) |

### Endoscraper is a grounded primitive, not a class

Reading on-chain protocol state is provided by a **runtime primitive**, `(chain-read $contract $slot)`-style. Any rule in any Space can call it to get current Ethereum mainnet state. Per-protocol metadata (contract addresses, ABIs, event signatures) lives in `&core.protocol`; the primitive consumes that metadata when called.

The grounded-primitive model collapses what was previously a beacon class plus an aggregation Space (`&core.endoscrapers`, now deleted). Verification under this model: wardens re-deriving a sentinel/relay decision call the same primitive — the "second source" is the runtime guarantee, not a separately-operated scraper.

### Input classes

| Class | Reads | Writes | Trust model |
|---|---|---|---|
| **market-data-beacon** | Off-chain market data (price feeds, indices, FX rates, funding rates) | Market-data atoms (price / liquidity / funding ticks) at the owning Oracle Entity entart root (`&entity.oracle.<id>.root`) | Oracle Entity cert chain; provider redundancy / dispute |
| **attest-data-beacon** | Off-chain claims about exobook state (custody balances, contract terms, compliance facts) | Signed attestation atoms inside the specific exobook Spaces the oracle is accordant to | Oracle Entity cert chain for class-accordant attestation; attestor liability via slashing |
| **patch-beacon** | Whatever the scaffold needs (off-space governance signal, manual feed) | Sudoed-target atoms inside whichever specific Space the patch is wired into | govops directly (Guardian → govops cert → patch instance); **no regulated framework**, no universal loop template |

Patch-beacons are the one input class without a regulated framework. They're Guardian-sudoed primitives, govops-certed, with their loop body and per-entity config sudoed inline at genesis. They exist for temporary scaffolds that bridge insyn coverage gaps (Phase 1's initial use case: per-Prime exsyn-TRRC claim writes into each `&entity.prime.<id>.primebook`). Patch-beacons are designed to **sunset** as their use cases migrate to insyn-native machinery; the class is reusable for any future hack of this nature.

Naming note: legacy classes `oracle` / `oracle-exsyn` / `attestor` are retired. Instance identifiers were renamed in tandem: `oracle-{provider}` → `market-data-{domain}-{provider}`, `attestor-{class}` → `attest-data-{class}`.

### Action classes — relay vs sentinel

| Aspect | **relay** | **sentinel** |
|---|---|---|
| Cognition | none — strategy is deterministic synart code | call-out density into operator telart |
| Verifiability | full (any warden re-runs the same synart) | bounds + envelope verifiable; cognitive output not (its provenance is) |
| P1 status | active (manually controlled by govops) | not in P1 scope; forward-looking |
| Loop location | universal template at `&core.loop.relay.<stem>` | per-entity sentinel Space in entart (no universal template) |

**Relay** absorbs everything the legacy taxonomy split across `relayer`, `executor`, `lpha-*` keepers, baseline-sentinel, and warden-sentinel. They all share the same work shape — read synart state, emit chain txs or BEAM freezes — and the same trust model. Specific relay stems describe the verb-target:

| Stem | Verb-target |
|---|---|
| `baseline-` | Run a Prime's strategy loop; sign PAU txs |
| `warden-` | Watch a baseline's output; freeze BEAM on divergence past tolerance |
| `nfat-` | NFAT facility operations (queue sweeping, mint, redemption funding) |
| `lcts-` | LCTS vault operations (lock, settle, capacity management) |
| `amm-` | AMM operations (pricing, inventory, redemption) |
| `auction-` | Allocation coordination + auction matching |
| `council-` | Council ops |
| `identity-` | Identity registry add/remove |
| `rate-` | Generator rate adjustments (SSR, etc.) |
| `govops-` | Govops-controlled deploy/withdraw/rollover at Prime/Halo level |

Class is registry metadata (`(beacon-class baseline-spark relay)`); stem is the work-role name. Multiple stems share one class.

**Sentinel** is the action class with cognitive call-out density. Two variants:

| Variant | Operator | Authority over PAU |
|---|---|---|
| **stream** | Ecosystem actor (proprietary intelligence) | None — proposes intent within bounds; relay executes |
| **principal-sentinel** | The principal (folio owner) | Direct — bundled with relay + local govops over its own folio |

Sentinels are not in Phase 1 scope. They're the forward-looking surface for when ecosystem actors with proprietary strategies and folios under principal control become real. The per-operator strategy and call-out into telart mean sentinels have **no universal synart template** — their loop body lives in the entart of the entity they operate on, and the cognitive call-out resolves to a service in the operator's telart agart.

### Synserv (special)

The canonical heartbeat and sole sequencer of synart writes. Runs `&core.loop.synserv`, evaluates synart-resolved code each tick to derive book state (equity, CRR per risk type, RRC, TRRC, ER, breach flags) from current input atoms. Singleton — only one instance is canonical at a time; failover is an atom write (see `boot-model.md` §5).

### In-space calculation — where calculation lives

For each book (Riskbook, Halobook, Primebook, Genbook, Generator's structural-demand space), synserv runs whatever calculation keeps its derived state consistent with current input atoms, in real time. The calculation logic is synart-resolved code; synserv executes it; wardens re-derive against the same code via grounded primitives.

```
market-data-beacon write ───┐
                            │
attest-data-beacon write ───┼──→ atom lands in book/oracle space
                            │
patch-beacon write ─────────┘
                                │
                                ▼
                          synserv re-derives the book's derived state
                          from current input atoms (+ chain-read primitive)
                                │
                                ▼
                          derived atoms updated in the book space;
                          replicated to subscribers
                                │
                                ▼
                          relay reads synart state; emits chain tx
```

Three consequences:

1. **Full verifiability.** Wardens re-derive everything because the calculation is synart code, not opaque off-loop compute.
2. **Beacons are pure I/O.** Input beacons push data; relays emit chain txs; sentinels propose within bounds. No calculation in any beacon.
3. **No lag.** Derived state always reflects current input atoms.

### Agent ↔ Beacon comms via convention-named embart Spaces

Beacons are pure I/O at runtime; **the cognition that drives sentinel decisions lives in agarts** (per-agent subtrees in telart for proven cognition, or embart for speculative). A Beacon Space's loop reaches that cognition via a **convention-named Space in the running emb's embart** — generalizing the synchronous call-out primitive into an asynchronous mailbox pattern.

A Beacon Space publishes an **I/O contract**:
> "If you boot me as identity X, I expect to find a Space named `<convention>` in your embart, populated with content matching `<schema>`. I will read it each tick. Missing or malformed → fall back to Base Strategy + emit audit-rejected."

The convention name is some function of class + booting identity; the schema is published. Pluggable: any tel can supply cognition to any standardized Beacon class by populating compliant content.

The synchronous `(call-out $service …)` form remains for genuinely-need-an-answer-now cases.

---

## 5. Low Authority Beacons

Low Authority beacons act independently — either for the teleonome's own purposes or in direct interaction with other teleonomes. No Synomic Entity intermediary involved.

### Reporting / Observation Beacons (Input)

Passive data exposure — positions, state, metrics, attestations. attest-data-beacon-shaped (private context) or grounded primitive consumption (any rule reads chain via `(chain-read …)`).

### Buyer / Subscriber Beacons (Input/Action)

Simple purchasing, subscription management, resource acquisition. Low operational authority; bounded by rate limits.

### Peer-to-Peer Trade Beacons (Action)

Sophisticated trading on owned assets (private multisig). The teleonome's own capital, deployed on its own behalf, without operating any Synomic Entity. Substantial local capability is permitted; the absence of Synomic Entity operation is what makes this low authority.

### Arbitrage / Cooperation Beacons (Action)

Cross-venue, cross-chain opportunity capture; sophisticated multi-teleonome coordination. May be highly capable but have no authority over Synomic Entities.

---

## 6. High Authority Beacons

High Authority beacons act on behalf of Synomic Entities (Primes, Halos, Generator, Guardian, Oracle Entities). They split into **relays** (no cognition, deterministic synart-resolved I/O) and **sentinels** (call-out density into operator telart, forward-looking).

### Relays — deterministic action surface

All high-authority deterministic action lives in the relay class. Specific stems describe the verb-target. Phase 1 has only relays at the action layer (no sentinels); each is govops-controlled — humans-in-the-loop deciding what txs to send or freeze, no AI logic.

| Stem | Synomic Entity | Verb-target |
|---|---|---|
| `baseline-{prime}` | Prime | Run Prime's strategy loop, sign PAU txs |
| `warden-{prime}-{operator}` | Prime | Watch baseline output, freeze BEAM on divergence |
| `nfat-{halo}` | Term Halo | NFAT facility operations |
| `lcts-{halo}` | Portfolio Halo | LCTS vault operations |
| `amm-{halo}` | Trading Halo | AMM operations |
| `auction-{x}` | Protocol | Allocation + auction matching |
| `council-{x}` | Council | Council ops |
| `identity-{network}` | Identity Network | Registry add/remove |
| `rate-{generator}` | Generator | SSR and rate adjustments |
| `govops-{owner}` | Any | Govops-controlled deploy/withdraw/rollover/lifecycle (P1's primary action surface) |

All relay loops are universal templates at `&core.loop.relay.<stem>`; per-entity config + binding lives in the entity's entart at `&entity.<type>.<id>.relay.<stem>` (per the two-step pattern in `../noemar-synlang/topology.md` §17).

### Sentinels — forward-looking cognitive action class

Sentinels are not in Phase 1 scope. They're the action surface for when ecosystem actors with proprietary intelligence and folios with principal control come online.

| Variant | Operator | What it does |
|---|---|---|
| **stream-sentinel** | Ecosystem actor (e.g., proprietary trading firm) | Proposes intent into a Prime's relay (via gate-out) within bounds; cognitive call-outs into operator telart; no PAU keys |
| **principal-sentinel** | Folio principal | Direct PAU control + bundled relay + local govops over its own folio; cognitive call-outs into principal's telart |

Sentinel loops live in the entart of the entity they operate on — `&entity.prime.<id>.sentinel.<actor>` for stream-sentinels, `&entity.folio.<owner>.sentinel-principal` for principal-sentinels. No universal synart template because the strategy is per-operator.

#### Stream sentinels and compounding

A **stream-sentinel** is the forward-looking surface through which an ecosystem actor deploys public (synomic) capital. Streams generate outperformance relative to a deterministic Base Strategy (executed by the underlying relay); the operating Teleonome earns **private carry**.

Carry may be reinvested into **proprietary AGI capabilities** (compute, models, data, embodiments) without leaking intelligence to competitors. The compounding loop:

> public capital → private intelligence → better streams → more carry → more intelligence

This loop is the highest-leverage activity available to a Teleonome, while remaining safe due to synomic constraints, warden-relays, and revocability.

##### Regulating Intra-Coalition Asymmetry

The compounding loop creates a structural risk: a teleonome operating successful streams compounds proprietary capability faster than peers, potentially approaching a winner-take-most dynamic inside the aligned coalition. Three structural features prevent this:

1. **Streams are Halos, not teleonome property.** The capital deployed lives inside a Synomic Entity (typically Portfolio or Trading Halo) — Synome-controlled, governance-bounded. The carry compounds privately; the public capital stays synomic.

2. **The Fortification Conserver regulates accumulated power.** Beyond its treasury role (see [`treasury-management.md`](../accounting/treasury-management.md)), the Conserver acts as regulator against any single teleonome's proprietary capability growing too large relative to the rest of the coalition. Active measurement of "too powerful" is a research commitment.

3. **The Conserver itself must be defeatable.** Powerful enough to enforce regulation against any individual teleonome, but not so powerful that the rest of the coalition cannot collectively overcome it.

See [`fractal-security-pattern`](../core-concepts/fractal-security-pattern.md) for the general pattern.

#### Why Sentinels are special (forward-looking)

When sentinels become live, they are uniquely powerful because they:
- Operate continuously and in real time
- Act faster than synomic governance processes
- Concentrate institutional authority and local intelligence
- Create immediate external effects that governance audits asynchronously

The accompanying warden-relays (deterministic, in-space-verifiable) are the safety surface against rogue sentinels.

#### Open: beacon-class conceptual treatment

The four "real" beacon classes (sentinel, relay, market-data-beacon, attest-data-beacon) each represent a kind of trust relationship that needs proper synodoxics treatment before later phases — what governance criteria admit instances, what synodoxics arguments justify the trust model, what structural constructors instantiate new instances under governance gating. Phase 1 uses sudo-inline stand-ins. Patch-beacon is explicitly excluded — no regulated framework, designed to sunset.

Tracked in `summaries/clean-todo.md`.

---

## 7. BEAM Hierarchy (Chain-Side, Orthogonal)

High Authority beacons act on behalf of Synomic Entities through **BEAMs** (Bounded External Access Modules) — on-chain authorized roles with constrained capabilities. The BEAM a beacon holds is what makes it high-authority *in the smart-contract sense*. BEAMs are orthogonal to the class taxonomy in §4.

| BEAM Type | Held By | Capabilities |
|-----------|---------|-------------|
| **pBEAM** (Process BEAM) | Relay (deterministic keeper) | Direct execution — calls Controller functions, moves capital within rate limits |
| **cBEAM** (Configurator BEAM) | Relay (deterministic keeper) | Configuration — sets rate limits (within SORL), onboards approved targets, manages relayer/freezer |
| **aBEAM** (Admin BEAM) | Council-class relay (governance) | Administration — registers PAUs, approves inits, grants cBEAMs; additions timelocked (14-day delay), removals instant |

```
Council relay (high-authority, aBEAM)
    │
    │ grants cBEAMs, approves inits
    │ (via BEAMTimeLock, 14-day delay)
    ▼
Relay (high-authority deterministic keeper, pBEAM + cBEAM)
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

A beacon is registered in `&core.registry.beacon` with:
- Unique identifier (`<stem>-<owner>[-<disambiguator>]`)
- Class metadata (`(beacon-class $beacon relay|sentinel|market-data-beacon|attest-data-beacon|patch-beacon|synserv)`)
- Pubkey
- Owning teleonome (may be pseudonymous)
- Hosting embodiment
- Authority envelope (scope of permitted actions)
- If High Authority: the Synomic Entity it operates

### 2. Authority Envelope Assignment

The authority envelope defines:
- What actions the beacon may take
- Rate limits and constraints
- Required attestations and reporting
- Escalation conditions

For High Authority beacons, this is typically defined by the Synomic Entity's governance through the BEAM hierarchy (§7).

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
<stem>-<owner>[-<disambiguator>]
```

- **Stem** describes the work role (`baseline`, `warden`, `nfat`, `lcts`, `amm`, `market-data`, `attest-data`, `patch`, `govops`, etc.)
- **Owner** is the entity id the beacon operates for (`spark`, `usge`, `crypto-majors`, etc.)
- **Disambiguator** (optional): provider, sub-strategy, operator id

Beacon identifiers use dashes only, no dots, no sigil — visually distinguishing them from Space references (`&core.<...>`, `&entity.<...>`). Stem ≠ class; class is registry metadata. Multiple stems can share one class.

### By class

**market-data-beacon (input, high authority):**
```
market-data-crypto-majors-{provider}     # e.g., market-data-crypto-majors-chainlink
```

**attest-data-beacon (input, high authority):**
```
attest-data-{halo-class}                 # per class-accordant attestor
```

**patch-beacon (input, high authority, Guardian-sudoed scaffold):**
```
patch-{target}                            # e.g., patch-{prime} for exsyn-TRRC scaffold
```

**relay (action, high authority, deterministic):**
```
baseline-{prime}                          # Prime strategy execution (P1: govops-controlled manually)
warden-{prime}-{operator}                 # Independent halt monitor
nfat-{halo}                               # NFAT facility keeper
lcts-{halo}                               # LCTS vault keeper
amm-{halo}                                # AMM keeper
auction-{x}                               # Auction/allocation keeper
council-{x}                               # Council ops
identity-{network}                        # Identity registry keeper
rate-{generator}                          # SSR / rate adjustments
govops-{owner}                            # Govops-controlled action (P1's primary surface)
```

**sentinel (action, high authority, cognitive — forward-looking):**
```
stream-{prime}-{actor}                    # Stream sentinel (ecosystem actor proposes intent)
principal-{owner}                         # Principal-sentinel (folio owner direct control)
```

**Low-authority peer-to-peer (legacy hpla- prefix retained as identifier):**
```
hpla-trade-{actor}                        # Private trading
hpla-arb-{actor}                          # Arbitrage
hpla-coop-{purpose}                       # Cooperation
```

### Synserv (special)

Singleton: `synserv-canonical`. Failover: governance writes `(canonical-synserv-runner X)`.

### Legacy prefix policy

The legacy `lpla` / `lpha` / `hpla` / `hpha` prefixes are **stripped from new identifiers**. Power-as-axis is retired; the four-letter codes encoded nothing semantically meaningful under the current taxonomy. `hpla-` prefix is retained only on legacy peer-to-peer trade beacon names (`hpla-trade-*`) as a stable handle for ops/governance reference; new beacons in those categories do not adopt the prefix.

### Retired identifiers (no longer beacon classes)

| Legacy | Status |
|---|---|
| `lpla-checker` | Retired. Verification runs as synart-resolved code inside synserv (in-space calculation, §4). |
| `lpla-verify` | Retired. Re-derivation via shadow execution (verifier emb, not a beacon class). |
| `endoscraper-{protocol}` | Retired as beacon class. Endoscraper is now a grounded runtime primitive (§4); per-protocol metadata in `&core.protocol`. |
| `oracle-{provider}` | Renamed → `market-data-{domain}-{provider}` (class `market-data-beacon`). |
| `oracle-exsyn-{class}` | Retired → `patch-{target}` (class `patch-beacon`); exsyn-TRRC writes relocated to per-primebook patch-beacons. |
| `attestor-{class}` | Renamed → `attest-data-{class}` (class `attest-data-beacon`). |
| `stl-base-{prime}` | Renamed → `baseline-{prime}` (class **relay**, not sentinel — baseline strategy is now deterministic synart code). |
| `stl-warden-{prime}-{op}` | Renamed → `warden-{prime}-{op}` (class **relay**, deterministic halt monitor). |
| `stl-stream-{prime}-{actor}` | Renamed → `stream-{prime}-{actor}` (class **sentinel**, variant stream). |
| `stl-principal-{owner}` | Renamed → `principal-{owner}` (class **sentinel**, variant principal-sentinel). |

---

## 10. Specialized Stems

Some relays have specialized roles bridging external systems or holding assets. All are class **relay**; the stem describes the work shape.

### Controllers

Beacons that interface with off-chain or physical systems — translation between Synomic Entities and real-world assets.

| Stem | Function |
|---|---|
| `ctl-bridge-{halo}` | Translation layer to RWA systems |
| `ctl-extend-{halo}` | Remote operation delegation |
| `ctl-connect-{halo}` | Private data bridging |

### Custodians

Beacons that hold assets or data with minimal action — security and reliability over capability.

| Stem | Function |
|---|---|
| `cst-synome` | Synome node operation, data custody |
| `cst-erc-{token}` | ERC token custody and rate management |
| `cst-vault-{id}` | Asset vault custody |

Custodians are typically high-trust, no-discretion relays.

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

This mirrors corporate structures: subsidiaries, SPVs, intelligence cut-outs.

**Threshold Rule:** Sufficient power concentration forces disclosure of beacon linkage. The synome may require aggregated reporting when a teleonome's total beacon footprint crosses risk thresholds.

---

## Connection to Other Documents

| Document | Relationship |
|----------|--------------|
| [`../sentinel/sentinel-network.md`](../sentinel/sentinel-network.md) | Forward-looking specification of the sentinel class (stream + principal-sentinel variants) |
| [`../risk-framework/sentinel-integration.md`](../risk-framework/sentinel-integration.md) | How beacons connect to risk framework calculations |
| [`atlas-synome-separation.md`](atlas-synome-separation.md) | How beacon authority envelopes derive from governance |
| [`../synoteleonomics/actuator-perspective.md`](../synoteleonomics/actuator-perspective.md) | First-person view of an actuator operating beacons |
| [`synome-overview.md`](synome-overview.md) | The 5-layer architecture beacons operate within |
| [`../smart-contracts/configurator-unit.md`](../smart-contracts/configurator-unit.md) | BEAM hierarchy (aBEAM, cBEAM, pBEAM) for High Authority beacons |
| [`../noemar-synlang/topology.md`](../noemar-synlang/topology.md) §9 | Naming convention canonical reference (dot-delimited Spaces, dash-only beacons) |
| [`../noemar-synlang/listener-loops.md`](../noemar-synlang/listener-loops.md) | In-space calculation pattern (sketch; implementation deferred) |
| [`../noemar-synlang/beacons.md`](../noemar-synlang/beacons.md) | Phase 1 beacon implementation sketches and per-protocol details |
| [`../summaries/clean-todo.md`](../summaries/clean-todo.md) | Open: beacon-class conceptual treatment (sentinel / relay / market-data / attest-data) |

---

## 12. Glossary

### Active framework terms

| Term | Definition |
|------|------------|
| **Beacon** | Synome-registered, enforceable action aperture |
| **Teleonome** | Private, goal-directed AI system (dark by default) |
| **Synomic Entity** | Durable, ledger-native entity. Types organized by rank: Guardians, Core Entities (Rank 1); Primes, Generators, Oracle Entities, Sequencer Entities, Pylon Entities (Rank 2); Halos, Folios (Rank 3) |
| **Embodiment** | Physical infrastructure hosting beacon execution |
| **Authority Envelope** | Scope of permitted actions for a beacon |
| **High Authority** | Beacon that operates a Synomic Entity (auth-scoped to specific verbs/targets) |
| **Low Authority** | Beacon that does not operate a Synomic Entity (passive observation OR peer-to-peer interaction) |
| **Input class** | Beacons that push data atoms into book/oracle/target Spaces: `market-data-beacon`, `attest-data-beacon`, `patch-beacon` |
| **market-data-beacon** | Input class admin'd by an Oracle Entity; pushes price/liquidity/funding-rate atoms to that entity's entart root. Replaces retired `oracle` class. |
| **attest-data-beacon** | Input class admin'd by an Oracle Entity; pushes signed attestation atoms into specific exobook Spaces it is accordant to. Replaces retired `attestor` class. |
| **patch-beacon** | Input class admin'd by govops directly via Guardian sudo; sudoed inline at genesis. No regulated framework, designed to sunset. Replaces retired `oracle-exsyn` class. |
| **relay** | Action class. Pure synart-resolved I/O; emits chain txs or freezes BEAMs based on synart state. No cognition. Absorbs former relayer + executor + Baseline + Warden + various `lpha-*` keepers. |
| **sentinel** | Action class with call-out density into operator telart. Variants: **stream** (intent proposal, no PAU keys), **principal-sentinel** (direct PAU control + bundled relay + local govops over its folio). Forward-looking; not in P1 scope. |
| **synserv** | Special singleton class. Canonical heartbeat and sole sequencer of synart writes. |
| **Endoscraper (grounded primitive)** | Not a beacon class. A runtime primitive `(chain-read $contract $slot)` accessible from any rule in any Space; returns current mainnet state. Per-protocol metadata in `&core.protocol`. |
| **Stem ≠ class** | The first segment of a beacon identifier (e.g., `baseline-`, `nfat-`) describes work role; class is registry metadata. Multiple stems share one class (all relay stems are class `relay`). |
| **In-space calculation** | Synart-resolved code, run by synserv, that derives book state (equity, per-risk-type CRRs, RRC, TRRC, ER, etc.) from current input atoms in real time |
| **BEAM** | Bounded External Access Module — on-chain authorized role that makes a beacon high-authority in the smart-contract sense |
| **pBEAM / cBEAM / aBEAM** | Process / Configurator / Admin BEAM — chain-side authorization tiers (held by relays / relays / council-class relays) |

### Historical naming

The earlier framework classified beacons along two axes — power and authority — yielding four quadrants (LPLA / LPHA / HPLA / HPHA). Power-as-axis retired when cognition migrated into synart-resolved in-space computation; the four-letter codes are stripped from new identifiers. The `hpla-` prefix survives only on legacy peer-to-peer trade beacon names as a stable handle. The current taxonomy is the six-class system in §4.

| Legacy code | Status |
|---|---|
| **LPLA** | Retired. Verification roles moved to synart-resolved in-space calculation. |
| **LPHA** | Retired. Deterministic keepers are now class `relay`. |
| **HPLA** | Retired as primary classification. Surviving prefix on legacy peer-to-peer trade beacons. |
| **HPHA** | Retired. Sentinel formations restructured into the two-class action taxonomy (relay + sentinel). |
| **lpla-checker** | Disappears. Synart-resolved calculation inside synserv. |
| **stl-base / stl-warden** | Renamed to `baseline- / warden-` (class **relay**, not sentinel — strategy is deterministic synart code post-noemar). |
| **stl-stream / stl-principal** | Renamed to `stream- / principal-` (class **sentinel**). |

### Open questions

Open: conceptual treatment of the four "real" beacon classes (sentinel, relay, market-data-beacon, attest-data-beacon) — synodoxics arguments for trust models, structural constructors for governance-gated instantiation, canonical conceptual homes. Phase 1 uses sudo-inline stand-ins; patch-beacon explicitly excluded. Tracked in `../summaries/clean-todo.md`.

Implementation-level open questions (per-class concrete impls, oracle/attestor boundary details, action-beacon auth scope, attestor atom schema) live in [`../noemar-synlang/beacons.md`](../noemar-synlang/beacons.md). In-space calculation mechanism (event-driven vs heartbeat vs hybrid) lives in [`../noemar-synlang/listener-loops.md`](../noemar-synlang/listener-loops.md).
