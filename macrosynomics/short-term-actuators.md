---
concepts:
  references:
    - beacon-framework
    - five-layer-architecture
    - dreamer-actuator-split
    - rsi
    - probabilistic-mesh
    - cancer-logic
    - atlas-synome-separation
---

# Short-Term Actuator Work: Teleonome-less Beacons

Phase 1 beacon deployments and how they evolve toward full teleonome-based actuators.

---

## Purpose

The full Synome vision involves autonomous teleonomes with directives, [RSI](../core-concepts/rsi.md), and [dreamer/actuator](../core-concepts/dreamer-actuator-split.md) embodiments. Building this all at once is impractical.

Instead: start with **teleonome-less beacons** — deterministic programs that provide operational infrastructure without autonomous agency. Then evolve toward full teleonomes.

**Principle:** Deploy working infrastructure now, designed to accept increasing autonomy over time.

---

## What Are Teleonome-less Beacons?

Beacons are autonomous operational components classified by **authority tier** plus **I/O role** under it (see [`beacon-framework.md`](beacon-framework.md) for the canonical framing):

| Tier | What it is |
|------|------------|
| **High authority** | Operates a Synomic Agent — auth-scoped to specific verbs/targets, certified by a synomic agent. |
| **Low authority** | No Synomic Agent operation. Either passive observation (input) OR direct teleonome-to-teleonome interaction (action). |

Underneath authority, beacons divide by **work shape**:
- **Input** — push data atoms into book spaces (endoscraper / oracle / attestor)
- **Action** — emit chain transactions based on synart state (relayer / executor / sentinel formation)

Phase 1 beacons are **deterministic programs, not AI**. They follow rules, don't learn, don't have directives. They're "teleonome-less" because there's no autonomous entity with its own mission. The deterministic nature is what makes them teleonome-less; it has nothing to do with how much local compute they run.

**Sentinel formations** (high-authority action beacons with continuous real-time strategy loops) come in later phases (Phase 9-10 in the current roadmap). Full teleonomes come later.

---

## Phase 1 Beacons

### Phase 1 Beacon Set

| Beacon | Authority | Role | Reads | Writes | Executes |
|--------|-----------|------|-------|--------|----------|
| **lpla-verify** | Low | Input (verification) | positions, prices, risk params | — | — |
| **lpha-relay** | High | Action (executor) | execution requests, rate limits | — | PAU transactions |
| **lpha-nfat** | High | Action (executor + record-writer) | deal params, queue state | NFAT records | NFAT lifecycle |
| **lpha-council** | High | Action (governance writer) | — | risk equations, report formats, disclosures | — |

Legacy `lp*` prefixes are retained as stable operational identifiers (see [`beacon-framework.md` §11 Glossary](beacon-framework.md#12-glossary)). They no longer encode the retired power axis.

In the new framework, position verification, settlement processing, and CRR calculation move into **synart-resolved in-space computation** that synserv runs (see [`beacon-framework.md` §4](beacon-framework.md#4-io-role-under-authority)). Phase 2's settlement-tracking role survives but as synserv-run code reading the same scraped state, not as a separate beacon class. Phase 3 introduces `lpha-report` to write daily Prime performance summaries as settlement artifacts.

### Grouped by Function

**Verification (low-authority input):**
- lpla-verify — observes, calculates, alerts (no write authority)

**Reporters (high-authority action):**
- lpha-nfat — writes NFAT records to Synome (also executes)
- lpha-report — writes daily Prime performance summaries as settlement artifacts (Phase 3+)

**Executors (high-authority action):**
- lpha-relay — executes PAU transactions with rate limits
- lpha-nfat — executes NFAT lifecycle operations

**Governance writers (high-authority action):**
- lpha-council — Core Council interface for updating Synome

### Data Flow

```
                        GOVERNANCE
                            │
                            ▼
                     ┌──────────────┐
                     │ lpha-council │
                     │              │
                     │ • Risk eqns  │
                     │ • Formats    │
                     │ • Disclosures│
                     └──────┬───────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       SYNOME-MVP                             │
│                                                              │
│  • Risk parameters (from lpha-council)                       │
│  • Report formats (from lpha-council)                        │
│  • Disclosures (from lpha-council)                           │
│  • NFAT records (from lpha-nfat)                             │
│  • Artifacts (addresses, metadata)                           │
│  • Position data (optional)                                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
       ┌───────────────────┼───────────────────┐
       ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│lpla-verify  │     │ lpha-relay  │     │  lpha-nfat  │
│             │     │             │     │             │
│ Reads:      │     │ Reads:      │     │ Reads:      │
│ • positions │     │ • requests  │     │ • deal params│
│ • prices    │     │ • limits    │     │ • queue     │
│ • risk params│    │             │     │             │
│             │     │ Executes:   │     │ Writes:     │
│ Outputs:    │     │ • PAU txns  │     │ • NFAT recs │
│ • CRR calcs │     │             │     │             │
│ • alerts    │     │             │     │ Executes:   │
│             │     │             │     │ • lifecycle │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## Synome-MVP Content Inventory

The Synome-MVP spans both governance data and operational data. Different source documents emphasize different facets; this section provides the unified inventory.

**Governance data** (emphasis in [whitepaper Part 7](../../whitepaper/sky-whitepaper.md)):

| Content | Source | Description |
|---------|--------|-------------|
| Agent artifacts | Governance (lpha-council) | Agent type definitions, encoded rules, directives |
| Governance process rules | Governance (lpha-council) | Escalation procedures, approval thresholds |
| Penalty/compliance parameters | Governance (lpha-council) | Encumbrance ratio targets, violation consequences |
| Atlas-derived constraints | Governance (lpha-council) | Constitutional principles encoded as machine-readable rules |

**Operational data** (emphasis in this document):

| Content | Source | Description |
|---------|--------|-------------|
| Risk parameters | lpha-council | Risk equations, CRR formulas, correlation framework parameters |
| Report formats | lpha-council | Standardized formats for Prime performance and risk reporting |
| Disclosures | lpha-council | Required disclosure templates and schedules |
| NFAT records | lpha-nfat | Individual deal records (terms, status, lifecycle events) |
| Position data | External feeds / beacons | Current holdings, prices, valuations per Prime |

Both categories coexist in the Synome-MVP as a single operational database. The governance data provides the rules and constraints; the operational data provides the state that beacons read and write. In the full Synome architecture, governance data crystallizes into the deontic skeleton (synart layer), while operational data evolves into the probabilistic mesh.

---

## Mapping to Full Synome Architecture

| Phase 1 Concept | Full Architecture | Notes |
|-----------------|-------------------|-------|
| Synome-MVP | Synart (operational subset) | Risk params, artifacts, NFAT records, disclosures (position data optional) |
| Deterministic beacons | Actuator embodiments | But without teleonome layer, no learning |
| lpha-council updates | Governance crystallization | Human-in-loop, signed statements |
| Rate limits, constraints | Hard constraints (axioms) | Enforced by smart contracts |
| lpla-verify alerts | Low-authority input/verification beacon pattern | Read-only, reporting |
| lpha-* execution | High-authority action beacon pattern | Operates a Synomic Agent under scoped auth |

### What's Simplified

- **No teleonome layer** — Beacons don't have directives or missions
- **No learning** — Deterministic programs, no RSI
- **No dreamer/actuator split** — All beacons are "actuators" (operate on real state)
- **Human governance** — Core Council provides all configuration, no autonomous decision-making
- **No [probabilistic mesh](../core-concepts/probabilistic-mesh.md)** — Synome-MVP is operational database, not probabilistic KB

### What's Preserved

- **Beacon taxonomy** — Two-tier authority + I/O role framework applies
- **Authority hierarchy** — Synome > beacon operations
- **Rate limits** — Universal constraint pattern
- **Audit trail** — All writes to Synome are logged
- **Separation of concerns** — Reading, reporting, executing are distinct roles

---

## Evolution Pathway

### Roadmap Phase 1: Teleonome-less Beacons (Current)

```
GOVERNANCE (Core Council, GovOps)
            │
            ▼
     ┌─────────────┐
     │ SYNOME-MVP  │ ◄── Operational database
     └──────┬──────┘
            │
    ┌───────┼───────┐
    ▼       ▼       ▼
 low-auth  high-auth  high-auth
 verify    relay     nfat ...
```

- All beacons are deterministic programs
- Human governance provides all configuration
- No learning, no adaptation
- Settlement remains manual in Phase 1 (legacy process)

> **Roadmap note:** Phases 2–8 add daily settlement, srUSDS/LCTS, governed (pre-auction) allocations, and the factory stack — but operations remain beacon-driven and governance-directed until sentinel formations are live.

### Roadmap Phases 9–10: Sentinel Introduction

```
GOVERNANCE
    │
    ▼
SYNOME-MVP ◄── Now includes learned patterns
    │
    ├── Deterministic beacons (unchanged)
    │
    └── Sentinel formations (new)
        • Baseline / Stream / Warden / Principal
        • High-authority action beacons with continuous real-time loops
```

- Sentinels run continuous real-time strategy loops
- Can learn from outcomes within constraints
- Daily settlement cycle (already live from Phase 3)
- Still no teleonome layer — sentinels are "proto-teleonomes"

### Beyond Roadmap: Teleonome Emergence

```
SYNART (governance layer)
    │
    ├── Teleonome 1 (Prime operations)
    │   ├── Directive
    │   ├── Telart (mission-specific patterns)
    │   └── Embodiments
    │       ├── Actuators (real execution)
    │       └── Dreamers (simulation)
    │
    ├── Teleonome 2 (Halo operations)
    │   └── ...
    │
    └── Shared beacons (low-authority utilities)
```

- Teleonomes have directives and missions
- Telart layer emerges (teleonome-specific knowledge)
- Dreamer/actuator split for RSI
- Beacons become embodiments of teleonomes

### Beyond Roadmap: Full Synome

```
SYNART
    │
    ├── Multiple Teleonomes
    │   ├── Directives (human-readable)
    │   ├── Teleonomic Axioms (machine constraints)
    │   ├── Telart (mission-specific, ossified patterns)
    │   └── Embodiments
    │       ├── Actuators (execute in reality)
    │       ├── Dreamers (evolve strategies)
    │       └── Embart (embodiment-specific patterns)
    │
    └── Full probabilistic mesh
        • Evidence flows back
        • Patterns ossify over time
        • RSI at all levels
```

---

## Invariants Across All Phases

These must hold regardless of current phase:

### 1. Authority Hierarchy

Synome/Synart always trumps beacon/embodiment decisions. Beacons operate within constraints, not around them.

### 2. Rate Limits as Universal Pattern

All execution authority is rate-limited. Increases are gradual (SORL: 25% per 18h). Decreases are instant. This pattern scales from Phase 1 beacons to Phase 4 teleonomes.

### 3. Audit Trail

All writes to Synome are logged with source and timestamp. This enables rollback and accountability.

### 4. Separation of Read/Write/Execute

Different beacons have different authorities:
- Low-authority input/verification: read-only (observation, calculation)
- High-authority action: write and/or execute (within constraints)

This separation prevents any single beacon from having unconstrained authority.

### 5. Human Governance as Backstop

Even in Phase 4, governance (Atlas, Core Council, token holders) can override teleonome decisions. Autonomy operates within governance-defined bounds.

### 6. Security = Preventing Self-Corruption

The threat model is [internal drift, not external attackers](../core-concepts/cancer-logic.md). Rate limits, audit trails, and governance oversight prevent beacons (and later teleonomes) from corrupting the system through overeager updates.

---

## Design Principles for Phase 1

These ensure Phase 1 beacons can evolve toward full teleonomes:

### 1. Beacons Should Be Stateless Where Possible

State lives in Synome-MVP. Beacons read state, perform operations, write results. This makes beacons replaceable and upgradeable.

### 2. Interfaces Should Be Stable

The interface between beacons and Synome-MVP should be designed for extension:
- New beacons can be added without changing existing ones
- New data types can be added to Synome-MVP
- Report formats (defined by lpha-council) provide flexibility

### 3. Constraints Should Be Explicit

Rate limits, buyboxes, and other constraints are data in Synome-MVP, not hardcoded in beacons. This allows constraints to evolve without beacon redeployment.

### 4. Logging Should Be Comprehensive

Every decision, every write, every execution should be logged. This provides:
- Audit trail for governance
- Training data for future sentinels
- Evidence for future RSI

### 5. Failure Modes Should Be Safe

When beacons fail:
- Fail closed (don't execute if uncertain)
- Alert for human intervention
- Preserve state for recovery

---

## What Phase 1 Teaches Us

Phase 1 is not just "getting things done" — it's learning about operational realities:

| Learning | How It Informs Later Phases |
|----------|----------------------------|
| Which data flows are needed | Shapes Synome schema |
| What constraints actually work | Informs axiom design |
| Where human intervention is needed | Identifies automation opportunities |
| What failure modes occur | Shapes sentinel training |
| How fast can operations run | Informs settlement cycle decisions |

This operational experience becomes the foundation for sentinel and teleonome design.
