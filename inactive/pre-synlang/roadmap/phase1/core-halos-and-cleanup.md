# Core Halos and Legacy Cleanup — Phase 1

**Status:** Draft
**Last Updated:** 2026-02-24

---

## Overview

Before deploying the Configurator (Phase 1.4), current Prime exposures must be reduced and simplified. Legacy assets either become **Core Halos** or are wound down.

This is a prerequisite workstream — every asset must have a clear disposition before Primes can operate via Configurator without spells.

---

## Why Cleanup Matters

Each additional exposure creates complexity across every Phase 1 system:

| Impact Area | Complexity Cost |
|---|---|
| **Configurator** | More allocation targets = more cBEAM surface area to manage |
| **MVP Beacons** | More exposures = more data to scrape, process, and monitor |
| **Risk Framework** | More positions = more CRR calculations, more edge cases |
| **Operations** | More integrations = more failure modes to handle manually |

Fewer, standardized positions → simpler infrastructure → faster Phase 1 delivery.

---

## Core Halos

**Core Halos** are legacy or static collateral positions retained under Core Council maintenance. Unlike Term Halos (which have the full book lifecycle with attestor-gated transitions), Core Halos are registered once in Synome-MVP and their state doesn't change — `lpla-verify` fetches live data itself.

| Aspect | Description |
|---|---|
| **What they are** | Existing Prime allocations worth keeping (e.g., Morpho vaults, SparkLend, JAAA, BlackRock BUIDL) |
| **How they work** | Registered as static entries in Synome-MVP by `lpha-council`, with a risk model and data model reference |
| **Risk monitoring** | `lpla-verify` reads the Core Halo entry to know what to fetch (on-chain via RPC for DeFi positions, financial APIs for assets like JAAA/BUIDL), then applies the risk model to compute CRR |
| **Integration** | `lpha-relay` deploys into Core Halos using the same relay infrastructure as NFATs |

**Initial scope:** Core Halos cover all assets that aren't Term Halos. These assets can later transition into standard Halos controlled by their respective Primes as the infrastructure matures.

### Core Halos vs Term Halos

| | Term Halo (Books + Units) | Core Halo |
|---|---|---|
| **Lifecycle** | Full state machine (created → ... → closed) | Static entry, state doesn't change |
| **Risk data source** | Attestor provides aggregate risk data | Council sets a fixed risk model + data model; lpla-verify scrapes live data itself |
| **Data updates** | lpha-nfat + lpha-attest beacons update Synome | No regular Synome updates — lpla-verify pulls fresh data at read time |
| **Beacons involved** | lpha-nfat, lpha-attest, lpla-verify | lpha-council (setup), lpla-verify (reads) |

### Core Halo Data in Synome-MVP

Each Core Halo entry stores:

| Field | Description |
|---|---|
| Entry identifier | Unique ID for this Core Halo |
| Parent Prime | Which Prime holds this position |
| Collateral type and description | What the position is (e.g., "Morpho USDC vault", "JAAA CLO tranche") |
| On-chain address(es) | Where applicable — contract addresses for DeFi positions |
| Risk model reference | Which risk framework equations apply to this position |
| Data model reference | What data lpla-verify should collect — on-chain via RPC, or off-chain via financial APIs |
| Static parameters | Any fixed values set by Council (e.g., haircuts, classification) |

### How lpla-verify Uses Core Halos

For each Core Halo entry, lpla-verify:
1. Reads the **data model reference** to know *what* to fetch and *where* to fetch it from
2. Fetches live data: on-chain RPC for DeFi positions, financial APIs for assets like JAAA or BUIDL
3. Reads the **risk model reference** to know which CRR equations to apply
4. Computes CRR using the live data and the risk model

Synome-MVP stores the configuration; lpla-verify fetches live data externally.

---

## Legacy Asset Decision Tree

```
┌─────────────────────────────────────────┐
│         LEGACY PRIME EXPOSURE           │
└──────────────────┬──────────────────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │  Worth retaining?   │
        └──────────┬──────────┘
                   │
         ┌─────────┴─────────┐
         │                   │
         ▼                   ▼
   ┌───────────┐       ┌───────────┐
   │    YES    │       │    NO     │
   └─────┬─────┘       └─────┬─────┘
         │                   │
         ▼                   ▼
   ┌───────────┐       ┌───────────┐
   │ Wrap as   │       │ Wind down │
   │ Core Halo │       │ position  │
   └───────────┘       └───────────┘
```

---

## Cleanup Targets

- **Promote to Core Halo**: Valuable legacy assets standardized as Halo entries in Synome-MVP
- **Wind down**: Experimental, low-value, or redundant allocations
- **Consolidate**: Redundant exposures merged into fewer, larger positions
- **Document**: Each Core Halo's data requirements for MVP beacons (what to fetch, from where, how often)

---

## Acceptance Criteria

Primes enter Phase 1.4 (Configurator Deployment) with:
- **Core Halos registered** — All retained legacy assets wrapped as Core Halo entries in Synome-MVP with risk model and data model references
- **No orphan exposures** — Everything either becomes a Core Halo or is wound down
- **Consistent interfaces** — All remaining positions accessible via standard PAU actions
- **Verified data sources** — lpla-verify can successfully fetch live data for each Core Halo (confirmed via test runs)

---

## Substage Mapping

| Substage | Core Halos Work |
|---|---|
| **1.2** | Synome-MVP and lpla-verify deployed — infrastructure ready to register Core Halos |
| **1.3** | Legacy cleanup complete — all assets either Core Halos or wound down |
| **1.4** | Core Halos registered in Configurator — Primes can deploy via spell-less flow |

---

## Related Documents

| Document | Relationship |
|---|---|
| [`phase-1-overview.md`](phase-1-overview.md) | Phase 1 substages (1.3 is the cleanup substage) |
| [`synome-mvp-reqs.md`](synome-mvp-reqs.md) | Core Halo entry data model in Synome-MVP |
| [`beacons.md`](beacons.md) | lpha-council (registers entries), lpla-verify (reads entries + fetches live data) |
| [`../../smart-contracts/configurator-unit.md`](../../smart-contracts/configurator-unit.md) | Configurator integration for Core Halo allocation targets |
