# Short-Term Actuator Work: Teleonome-less Beacons

**Status:** Implementation pathway
**Last Updated:** 2026-02-03

This document describes Phase 1 beacon deployments and how they evolve toward full teleonome-based actuators.

---

## Purpose

The full Synome vision involves autonomous teleonomes with directives, RSI, and dreamer/actuator embodiments. Building this all at once is impractical.

Instead: start with **teleonome-less beacons** — deterministic programs that provide operational infrastructure without autonomous agency. Then evolve toward full teleonomes.

**Principle:** Deploy working infrastructure now, designed to accept increasing autonomy over time.

---

## What Are Teleonome-less Beacons?

Beacons are autonomous operational components. They vary along two axes:

| Axis | Low | High |
|------|-----|------|
| **Power** | Programs (deterministic, rule-based) | AI (adaptive, learning) |
| **Authority** | Controls independent entities | Synome or smart contract capabilities |

**Phase 1 beacons are all Low-Power** — deterministic programs, not AI. They follow rules, don't learn, don't have directives. They're "teleonome-less" because there's no autonomous entity with its own mission.

**Sentinels** (high-power, AI beacons) come in Phase 2+. Full teleonomes come later.

---

## Phase 1 Beacons

### The Six Beacons

| Beacon | Type | Reads | Writes | Executes |
|--------|------|-------|--------|----------|
| **lpla-checker** | LPLA | positions, prices, risk params | — | — |
| **lpha-relay** | LPHA | execution requests, rate limits | — | PAU transactions |
| **lpha-nfat** | LPHA | deal params, queue state | NFAT records | NFAT lifecycle |
| **lpha-report** | LPHA | Prime positions, CRRs | 24h summaries | — |
| **lpha-collateral** | LPHA | Core Halo / legacy RWA state | collateral data | — |
| **lpha-council** | LPHA | — | risk equations, report formats | — |

> **Note:** lpha-collateral is speculative and may not be needed.

### Grouped by Function

**Read-only (LPLA):**
- lpla-checker — observes, calculates, alerts (no write authority)

**Reporters (LPHA):**
- lpha-report — writes Prime performance summaries to Synome
- lpha-collateral — writes Core Halo / legacy data to Synome
- lpha-nfat — writes NFAT records to Synome (also executes)

**Executors (LPHA):**
- lpha-relay — executes PAU transactions with rate limits
- lpha-nfat — executes NFAT lifecycle operations

**Governance tooling (LPHA):**
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
                     └──────┬───────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       SYNOME-MVP                             │
│                                                              │
│  • Risk parameters (from lpha-council)                       │
│  • Report formats (from lpha-council)                        │
│  • Prime reports (from lpha-report)                          │
│  • Collateral data (from lpha-collateral)                    │
│  • NFAT records (from lpha-nfat)                             │
│  • Position data                                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
       ┌───────────────────┼───────────────────┐
       ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│lpla-checker │     │ lpha-relay  │     │  lpha-nfat  │
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
       │
       ▼
┌─────────────┐     ┌─────────────────┐
│lpha-report  │     │lpha-collateral  │
│             │     │  (speculative)  │
│ Reads:      │     │                 │
│ • positions │     │ Reads:          │
│ • CRRs      │     │ • Core Halos    │
│             │     │ • legacy RWA    │
│ Writes:     │     │                 │
│ • 24h report│     │ Writes:         │
│             │     │ • collateral    │
└─────────────┘     └─────────────────┘
```

---

## Mapping to Full Synome Architecture

| Phase 1 Concept | Full Architecture | Notes |
|-----------------|-------------------|-------|
| Synome-MVP | Synart (operational subset) | Risk params, NFAT records, position data |
| Low-power beacons | Actuator embodiments | But without teleonome layer, no learning |
| lpha-council updates | Governance crystallization | Human-in-loop, signed statements |
| Rate limits, constraints | Hard constraints (axioms) | Enforced by smart contracts |
| lpla-checker alerts | LPLA beacon pattern | Read-only, reporting |
| lpha-* execution | LPHA beacon pattern | High authority, constrained execution |

### What's Simplified

- **No teleonome layer** — Beacons don't have directives or missions
- **No learning** — Deterministic programs, no RSI
- **No dreamer/actuator split** — All beacons are "actuators" (operate on real state)
- **Human governance** — Core Council provides all configuration, no autonomous decision-making
- **No probabilistic mesh** — Synome-MVP is operational database, not probabilistic KB

### What's Preserved

- **Beacon taxonomy** — LPLA/LPHA/HPLA/HPHA framework applies
- **Authority hierarchy** — Synome > beacon operations
- **Rate limits** — Universal constraint pattern
- **Audit trail** — All writes to Synome are logged
- **Separation of concerns** — Reading, reporting, executing are distinct roles

---

## Evolution Pathway

### Phase 1: Teleonome-less Beacons (Current)

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
 LPLA     LPHA    LPHA
checker   relay   nfat ...
```

- All beacons are Low-Power (deterministic programs)
- Human governance provides all configuration
- No learning, no adaptation
- Monthly settlement cycle

### Phase 2: Sentinel Introduction

```
GOVERNANCE
    │
    ▼
SYNOME-MVP ◄── Now includes learned patterns
    │
    ├── Low-Power beacons (unchanged)
    │
    └── High-Power Sentinels (new)
        • HPLA: Trading, adaptive execution
        • HPHA: Governance-level autonomy
```

- Sentinels are High-Power (AI, adaptive)
- Can learn from outcomes within constraints
- Weekly settlement cycle
- Still no teleonome layer — sentinels are "proto-teleonomes"

### Phase 3: Teleonome Emergence

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
    └── Shared beacons (LPLA utilities)
```

- Teleonomes have directives and missions
- Telart layer emerges (teleonome-specific knowledge)
- Dreamer/actuator split for RSI
- Beacons become embodiments of teleonomes

### Phase 4: Full Synome

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

All execution authority is rate-limited. Increases are gradual (SORL: 20% per 18h). Decreases are instant. This pattern scales from Phase 1 beacons to Phase 4 teleonomes.

### 3. Audit Trail

All writes to Synome are logged with source and timestamp. This enables rollback and accountability.

### 4. Separation of Read/Write/Execute

Different beacons have different authorities:
- LPLA: Read-only (observation, calculation)
- LPHA: Write and/or execute (within constraints)

This separation prevents any single beacon from having unconstrained authority.

### 5. Human Governance as Backstop

Even in Phase 4, governance (Atlas, Core Council, token holders) can override teleonome decisions. Autonomy operates within governance-defined bounds.

### 6. Security = Preventing Self-Corruption

The threat model is internal drift, not external attackers. Rate limits, audit trails, and governance oversight prevent beacons (and later teleonomes) from corrupting the system through overeager updates.

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

---

## Summary

| Aspect | Phase 1 | Evolves Toward |
|--------|---------|----------------|
| Beacons | 6 low-power (deterministic) | High-power sentinels, then teleonome embodiments |
| Intelligence | None (rule-based) | AI (adaptive), then RSI |
| Learning | None | Sentinels learn, teleonomes have full RSI |
| Synome | MVP (operational database) | Full synart + telart + embart |
| Governance | Human-in-loop (Core Council) | Increasing autonomy within bounds |
| Settlement | Monthly | Weekly, then continuous |

**The goal:** Build working infrastructure that accepts increasing autonomy without rearchitecting.

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| `beacon-framework.md` | Full beacon taxonomy (LPLA/LPHA/HPLA/HPHA) |
| `synome-layers.md` | The 5-layer architecture these beacons evolve toward |
| `actuator-perspective.md` | Full actuator embodiment — the evolution target |
| `security-and-resources.md` | Security principles (rate limits, audit trails, governance) |
| `atlas-synome-separation.md` | How Synome-MVP relates to full Atlas/Synome model |
| `short-term-experiments.md` | Parallel dreamer pathway (game-playing agents) |
| `../phase1/laniakea-phase-1.md` | Full Phase 1 implementation spec |
