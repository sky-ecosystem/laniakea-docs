# Laniakea Phase 2: Monthly Settlement

**Status:** Draft
**Last Updated:** 2026-02-12

---

## Executive Summary

Phase 2 formalizes the monthly settlement cycle that Phase 1 ran manually. The headline deliverable is **lpla-checker**: the full checker beacon that extends lpla-verify's monitoring capabilities with settlement tracking, completeness verification, and penalty detection.

Phase 1 deployed infrastructure and ran settlement through existing manual processes. Phase 2 makes that settlement cycle auditable, beacon-monitored, and penalty-enforced — establishing the operational discipline that Phase 3 will accelerate to a daily cadence.

**Important constraint:** Phase 2 has **no Prime-side sentinels** and **no auctions**. Allocation remains governance-directed. The goal is reliable, verifiable monthly settlement with beacon-assisted oversight.

---

## Scope

### Objective

Formalize monthly settlement by:
- Deploying lpla-checker with full settlement tracking (building on lpla-verify)
- Establishing consistent settlement artifacts in Synome
- Introducing prepayment discipline and late-payment penalty mechanics
- Proving the settlement → verification → enforcement loop at monthly cadence

### In Scope (Phase 2 Deliverables)

1. **lpla-checker beacon**
   - All lpla-verify capabilities (position verification, CRR calculation, alert generation)
   - **Settlement cycle tracking** — monitors progress through monthly settlement windows
   - **Settlement completeness verification** — confirms all obligations are met before settlement closes
   - **Late payment detection** — flags Primes that miss prepayment deadlines
   - **Penalty calculation** — computes penalties for late/incomplete settlement obligations

2. **Monthly settlement formalization**
   - Define canonical monthly settlement timeline (settlement window, processing period, moment of settlement)
   - Establish which subsystems must coordinate around the settlement window
   - Operational runbooks for GovOps execution during settlement periods

3. **Prepayment and penalty mechanics**
   - Prime → Generator interest prepayment obligations
   - Late-payment penalty calculation and Synome logging
   - Penalty forgiveness process for early incidents (explicit governance statements)

4. **Synome schema updates**
   - Monthly epoch identifiers
   - Settlement outputs and verification results
   - Prepayment receipts and penalty events
   - lpla-checker attestations

### Explicit Non-Goals (Deferred)

- Daily settlement cadence (Phase 3)
- LCTS and srUSDS (Phase 4)
- Any sealed-bid auctions (Phase 9, once `stl-base` is live)
- Sentinel formations (Phases 9–10)

---

## lpla-checker: Full Checker Beacon

lpla-checker extends lpla-verify with settlement-aware capabilities:

| Capability | From lpla-verify | New in lpla-checker |
|-----------|:-:|:-:|
| **Position verification** | Yes | |
| **CRR calculation** | Yes | |
| **Alert generation** | Yes | |
| **Settlement cycle tracking** | | Yes |
| **Completeness verification** | | Yes |
| **Late payment detection** | | Yes |
| **Penalty calculation** | | Yes |

**Type:** LPLA (Low Power, Low Authority) — reads and reports only, no execution authority.

**Inputs:** On-chain position data, price feeds, risk parameters from Synome-MVP, settlement timeline parameters

**Outputs:** CRR calculations, settlement status, verification results, alerts, penalty calculations, settlement attestations to Synome

---

## Monthly Settlement Timeline

The monthly settlement cycle establishes the operational pattern that Phase 3 will compress to daily:

| Period | Description |
|--------|-------------|
| **Active Period** | Normal operations: deposits, withdrawals, data collection, parameter staging |
| **Settlement Window** | Processing: calculation finalization, prepayments, verification |
| **Moment of Settlement** | New parameters take effect; penalties accrue if obligations incomplete |

> **Note:** Exact monthly timing (which day, which hours) is an operational decision. The key deliverable is the discipline and tooling, not the specific calendar date. Phase 3 compresses this to the canonical daily timeline (Active 16:00→13:00, Lock 13:00→16:00, Settlement at 16:00 UTC).

---

## Temporary Measures

### 1) GovOps-Run Settlement Coordination (Interim for `stl-base`)

**Problem:** The end-state calls for `stl-base` to compute interest due, submit prepayments, and participate in auctions. That does not exist yet.

**Temporary measure:** GovOps teams coordinate monthly settlement:
- Compute interest owed using published formulas/parameters
- Submit prepayment transactions through bounded execution surfaces (Prime multisig / lpha-relay)
- lpla-checker verifies completeness and flags discrepancies

**Design requirement:** All calculations must be deterministic and reproducible from on-chain + Synome inputs, using the same schemas that daily settlement (Phase 3) and eventually `stl-base` (Phase 9) will use.

### 2) Penalty Forgiveness Process (Interim Governance)

**Problem:** Early monthly settlement will have operational failures. A strict penalty regime can create cascading issues.

**Temporary measure:**
- Penalties are calculated and logged in Synome, but Core Council retains an explicit "forgiveness" process for early incidents
- Forgiveness must be recorded as a signed governance statement that references the original penalty event and provides rationale

This avoids "silent exception handling" while allowing early operations to proceed.

### 3) Manual Settlement Window Enforcement

**Problem:** Without system-level lock enforcement, actors can mutate state during the settlement window.

**Temporary measure:** Operational policies during the settlement window:
- No governance parameter changes except emergency removals
- No onboarding of new targets
- Only settlement-critical transactions are submitted
- lpla-checker flags any unexpected state mutations during the window

This is replaced by system-level locking in Phase 3 (daily settlement) and later by sentinel-operated discipline.

---

## Acceptance Criteria (Exit to Phase 3)

Phase 2 is considered complete when:
- lpla-checker is operational with full settlement tracking capabilities
- Monthly settlement has run for several cycles without missed settlements (or with explicit, documented skips)
- Prime interest prepayment workflows complete reliably before the Moment of Settlement
- lpla-checker produces settlement verification outputs and flags late/missing obligations
- Settlement artifacts are written to Synome with consistent epoch identifiers
- Penalty calculations are logged correctly (even if forgiveness is applied)

---

## Links (Relevant Specs)

- Roadmap overview: [roadmap-overview.md](./roadmap-overview.md)
- Phase 1 (infrastructure + lpla-verify): [phase-1-overview.md](./phase1/phase-1-overview.md)
- Phase 3 (daily settlement): [phase-3-daily-settlement.md](./phase-3-daily-settlement.md)
- Daily settlement spec (target cadence): [daily-settlement-cycle.md](../accounting/daily-settlement-cycle.md)
- Beacon taxonomy: [beacon-framework.md](../synomics/macrosynomics/beacon-framework.md)
- Execution surfaces: [diamond-pau.md](../smart-contracts/diamond-pau.md), [configurator-unit.md](../smart-contracts/configurator-unit.md)
