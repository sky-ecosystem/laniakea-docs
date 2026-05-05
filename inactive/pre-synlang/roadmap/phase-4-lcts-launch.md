# Laniakea Phase 4: LCTS Launch

**Status:** Draft
**Last Updated:** 2026-02-12

---

## Executive Summary

Phase 4 launches the **Liquidity Constrained Token Standard (LCTS)** as the core mechanism for capacity-constrained conversions and pooled products. The headline deliverables are:
- `srUSDS` as the first Generator-level LCTS product
- The first LCTS-based **Portfolio Halo** (e.g., an MMF unit) using the same queue primitives

Phase 4 runs in **pre-auction mode**: Sky Core sets the srUSDS rate directly, with Core Council managing day-to-day according to Atlas instructions. Sealed-bid auctions do not begin until Prime-side `stl-base` exists (Phase 9).

---

## Scope

### Objective

Prove the daily lock/settle loop with real queue-based products:
- Users can subscribe/redeem via LCTS queues
- Settlement updates exchange rates at 16:00 UTC
- Capacity management is deterministic and auditable

### In Scope (Phase 4 Deliverables)

1. **LCTS core contracts**
   - `SubscribeQueue` and `RedeemQueue`
   - Generation lifecycle (DORMANT → ACTIVE → LOCKED → FINALIZED/DORMANT)
   - Pro-rata settlement within a generation

2. **`srUSDS`**
   - `sUSDS → srUSDS` subscribe queue
   - `srUSDS → sUSDS` redeem queue
   - Daily exchange-rate updates at settlement

3. **Holding System**
   - Contract system that holds `sUSDS` backing `srUSDS`
   - Receives funding flows from Prime PAUs (subject to rate limits)

4. **`lpha-lcts` beacon**
   - Executes LCTS lock/settle operations
   - Enforces deterministic capacity processing and accounting

5. **First Portfolio Halo (MMF example)**
   - LCTS-based Halo Class + first Unit
   - Manual deployment + onboarding via spells (factories start Phase 5)

### Explicit Non-Goals (Deferred)

- Automated Halo deployment (Phase 5)
- Any auctions (Phase 9)
- Sentinel-operated Prime allocation (Phases 9–10)

---

## LCTS in the Daily Settlement Cycle

LCTS is designed to “snap” to the daily cadence:
- **13:00–16:00 UTC (Processing/Lock):** queues lock; settlement computations run
- **16:00 UTC:** the exchange rate updates and claims become available for the settled generation

Canonical settlement timing is specified in:
- `accounting/daily-settlement-cycle.md`
- `smart-contracts/lcts.md`

---

## srUSDS Rate Management (Pre-Auction)

When srUSDS goes live, Sky Core will initially decide what rate it receives, manually targeting a governance-set rate. Core Council manages day-to-day rate decisions according to instructions from Atlas.

This governance-directed approach remains in place until Prime-side `stl-base` is deployed (Phase 9), at which point sealed-bid OSRC auctions replace manual rate-setting. The key design constraint: downstream consumers (`lpha-lcts`, lpla-checker, Prime reporting) should not need to change when the rate-setting mechanism switches from manual to auction-based.

### Pre-Auction Operational Details

- Core Council sets srUSDS origination capacity and rate inputs, published as signed Synome statements
- `lpha-lcts` consumes published capacity inputs and settles LCTS generations deterministically
- Settlement logs are emitted for lpla-checker verification
- If a rate/capacity input is missing at lock time, the system uses a defined fallback (e.g., previous epoch's parameters or net-flow-only settlement), explicitly logged

---

## First Portfolio Halo (MMF Example)

Phase 4 also proves the LCTS + Halo pattern in a real RWA deployment path:
- A **Halo Class** defines shared contracts, beacon integration, and legal framework
- A **Halo Unit** is the actual product (e.g., MMF senior tranche)

### Temporary Measures (Pre-Factory)

Because Halo factories do not exist until Phase 5:
- Halo Classes and Units are deployed manually (spells / governance transactions)
- Contract addresses are registered manually in Synome/Artifacts
- Rate limits and pBEAM permissions are configured manually via governance + cBEAM procedures

The Phase 4 deliverable is not "deployment convenience"; it is proving the **queue + settlement + reporting** loop with a production-shaped Halo unit.

---

## Acceptance Criteria (Exit to Phase 5: Halo Factory)

Phase 4 is considered complete when:
- `srUSDS` subscribe/redeem queues operate reliably on the daily cadence
- `lpha-lcts` lock/settle runs consistently within the Processing Window
- Holding System funding and accounting are correct and auditable
- The first Portfolio Halo Unit can accept deposits/redemptions using the same primitives
- Governance can operate pre-auction capacity inputs safely and reproducibly

---

## Links (Relevant Specs)

- Roadmap overview: [roadmap-overview.md](./roadmap-overview.md)
- Daily settlement cycle: [daily-settlement-cycle.md](../accounting/daily-settlement-cycle.md)
- LCTS contract specification: [lcts.md](../smart-contracts/lcts.md)
- Portfolio Halo business + structure: [portfolio-halo.md](../sky-agents/halo-agents/portfolio-halo.md)
- Beacon taxonomy and LPHA role: [beacon-framework.md](../synomics/macrosynomics/beacon-framework.md)
