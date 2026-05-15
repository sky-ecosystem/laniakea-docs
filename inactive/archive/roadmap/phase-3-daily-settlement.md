# Laniakea Phase 3: Daily Settlement

**Status:** Draft  
**Last Updated:** 2026-02-12

---

## Executive Summary

Phase 3 transitions Laniakea operations from a **formalized monthly** cadence (Phase 2) to the **daily settlement cycle** that all later phases assume. Phase 1 ran manual settlement; Phase 2 formalized monthly settlement; Phase 3 now standardizes the time windows, data posting, verification, prepayment, and penalty mechanics needed to safely run higher-frequency daily operations.

**Core idea:** A single daily “Moment of Settlement” (16:00 UTC) where new parameters take effect, with a short lock window (13:00–16:00 UTC) for settlement-critical processing.

**Important constraint:** In Phase 3 there are **no Prime-side sentinels** and **no auctions**. Operational computations and submissions are performed by GovOps teams and deterministic LPHA beacons where available.

---

## Scope

### Objective

Establish a reliable daily cycle that:
- Produces consistent, timestamped settlement artifacts in Synome
- Coordinates lock/settle actions across systems that need them
- Enforces prepayment discipline and late-payment penalties
- Enables Phase 4 LCTS lock/settle behavior without redesigning timing later

### In Scope (Phase 3 Deliverables)

1. **Daily schedule and locking discipline**
   - Adopt the canonical schedule: Active Window → Processing Window (Lock) → Moment of Settlement
   - Define which subsystems must be “lock aware” (i.e., do not mutate critical state during the Processing Window)

2. **Prepayment and penalties**
   - Prime → Generator interest prepayment
   - Generator → Prime distributions (as applicable)
   - Late-payment penalty calculation and logging

3. **Synome schema + operational logging**
   - Daily epoch identifiers
   - Settlement outputs, prepayment receipts, and penalty events

4. **Beacon and ops cadence upgrades**
   - lpla-checker: daily cadence tracking + verification reports
   - lpha-report: daily Prime performance summaries written as a settlement artifact
   - Operational runbooks for GovOps execution during the lock window

### Explicit Non-Goals (Deferred)

- LCTS and srUSDS (Phase 4)
- Any sealed-bid auctions (OSRC, Duration) (Phase 9, once `stl-base` is live)
- Sentinel formations (`stl-base`, `stl-stream`, `stl-warden`) (Phases 9–10)
- Factory deployment of Halos/Primes/Generator (Phases 5–8)

---

## The Daily Timeline (Canonical)

All times are **UTC**.

| Period | Timing | Purpose |
|--------|--------|---------|
| **Active Window** | 16:00 → 13:00 | Data collection; normal deposits/withdrawals; parameter staging |
| **Processing Window (Lock)** | 13:00 → 16:00 | Calculation finalization; prepayments; verification; lock/settle actions |
| **Moment of Settlement** | 16:00 | New parameters take effect; penalties start accruing if obligations incomplete |

This is specified in detail in `accounting/daily-settlement-cycle.md`. Phase 3's goal is to make the cadence *real* operationally, even before later components (auctions, sentinels) exist.

---

## System Behavior in Phase 3

### What "Lock" Means in Phase 3

In Phase 3, "lock" is primarily an **operational and beacon-level discipline**:
- Beacons that perform settlement-sensitive actions should not execute those actions during the Processing Window unless explicitly part of the settlement procedure.
- Operators avoid governance changes, large migrations, or novel integrations during the Processing Window.

Some systems (notably LCTS in Phase 4) will later have explicit on-chain lock/settle methods; Phase 3 establishes the *timing contract* first so later phases can plug into it.

### Prepayments (Without `stl-base`)

The daily settlement specification assumes `stl-base` eventually performs computations and submits transactions. In Phase 3:
- **GovOps automation** (deterministic scripts and checklists) performs calculations
- **Prime multisigs and/or LPHA executors** submit required transactions within rate limits
- lpla-checker verifies postings and completeness

### Auctions (Not Yet)

Even though the daily settlement cycle includes "submission windows" conceptually, Phase 3 does **not** include:
- bid intake
- matching engines
- clearing prices

Allocation remains governance-directed/manual. Phase 3 focuses on *time synchronization and operational reliability*.

---

## Temporary Measures (Before the Final Automation)

Phase 3 is intentionally heavy on temporary/bootstrapping measures. These should be treated as part of the deliverable: they are what make the daily cadence safe before the end-state systems exist.

### 1) GovOps-Run Settlement Operator (Interim for `stl-base`)

**Problem:** The end-state calls for Prime-side `stl-base` to compute interest due, submit prepayment, and participate in auctions. That does not exist yet.

**Temporary measure:** A GovOps-run settlement operator performs the `stl-base` responsibilities that are purely mechanical:
- Computes interest owed using published formulas/parameters
- Produces signed settlement statements for Synome posting
- Coordinates transaction submission through bounded execution surfaces (Prime multisig / LPHA executor)

**Design requirements (so it can be replaced cleanly in Phase 9):**
- All calculations must be deterministic and reproducible from on-chain + Synome inputs
- All outputs must use the same epoch identifiers and schemas that `stl-base` will later use
- Any discretionary decisions must be explicitly marked as “governance-directed” (not “system-derived”)

### 2) Manual / Policy-Based Enforcement of the Processing Window

**Problem:** Without full on-chain lock enforcement everywhere, actors can mutate state at any time.

**Temporary measure:** Operational policies during 13:00–16:00 UTC:
- No governance parameter changes except emergency removals
- No onboarding of new targets (Core Halo additions, new NFAT facilities, etc.)
- No large discretionary reallocations
- Only settlement-critical transactions are submitted (interest, distributions, required attestations)

This is replaced over time by:
- system-level lock/settle in LCTS (Phase 4)
- auction-based allocation once `stl-base` is live (Phase 9)
- sentinel-operated, automated discipline (Phases 9–10)

### 3) Penalty Calculation and Forgiveness Process (Interim Governance)

**Problem:** Early rollout will have operational failures. A strict penalty regime can create cascading issues.

**Temporary measure:**
- Penalties are calculated and logged in Synome, but Core Council retains an explicit “forgiveness” process for early incidents.
- Forgiveness must be recorded as a signed governance statement that references the original penalty event and provides rationale.

This avoids “silent exception handling” while allowing early operations to proceed.

---

## Acceptance Criteria (Exit to Phase 4)

Phase 3 is considered complete when:
- A full daily cadence has run for a sustained period without missed settlements (or with explicit, documented skips)
- Prime interest prepayment and (if applicable) distribution workflows complete reliably before 16:00 UTC
- lpla-checker produces daily verification outputs and flags late/missing obligations
- Settlement artifacts are written to Synome with consistent epoch identifiers and timestamps
- Operators can execute the Processing Window runbook without relying on ad hoc decisions

---

## Dependencies

- Phase 2 complete (formalized monthly settlement established)

---

## Links (Relevant Specs)

- Roadmap overview: [roadmap-overview.md](./roadmap-overview.md)
- Phase 1: [phase-1-overview.md](./phase1/phase-1-overview.md)
- Phase 2: [phase-2-monthly-settlement.md](./phase-2-monthly-settlement.md)
- Daily settlement spec: [daily-settlement-cycle.md](../accounting/daily-settlement-cycle.md)
- Beacon taxonomy (for lock-aware roles): [beacon-framework.md](../synomics/macrosynomics/beacon-framework.md)
- Teleonome-less beacon pathway: [short-term-actuators.md](../synomics/macrosynomics/short-term-actuators.md)
- Execution surfaces: [diamond-pau.md](../smart-contracts/diamond-pau.md), [configurator-unit.md](../smart-contracts/configurator-unit.md)
