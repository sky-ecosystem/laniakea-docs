# Laniakea Phase 1: Pragmatic Delivery — Overview

**Status:** Draft
**Last Updated:** 2026-02-24

---

## Executive Summary

Phase 1 delivers minimal viable infrastructure for automated capital deployment. **Phase 1 continues using the existing manual settlement process**; formalized monthly settlement with lpla-checker begins in Phase 2, and daily settlement is the Phase 3 target.

**Bootstrap note:** Starting in Phase 1, Sky governance manually allocates liability duration matching (top-down). Sealed-bid OSRC and Duration auctions begin later once Prime-side `stl-base` is deployed.

---

## Deliverables

Seven deliverables in sequence order:

### 1. Diamond PAU Deployment

Upgrade all first-cohort Primes from legacy PAU to **Diamond PAU** architecture (EIP-2535 diamond proxy). Modular facets replace monolithic controllers — adding or upgrading actions no longer requires full redeployment.

Phase 1 facets: `NfatDepositFacet`, `NfatWithdrawFacet`, `CoreHaloFacet`, `LegacyMigrationFacet`.

Each Prime migrates: deploy Diamond PAU → migrate positions → grant cBEAMs → wind down legacy.

*Canonical spec:* [`../../smart-contracts/diamond-pau.md`](../../smart-contracts/diamond-pau.md)

### 2. Synome-MVP

Shared operational database for Halo operations. Tracks halo books (balanced ledgers), halo units (cross-book links), Core Halo entries, risk framework configuration, and attestations from an independent attestor.

**Phase 1 mental model:** Synome-MVP is the shared database; beacons are the app layer.

*Deep-dive:* [`synome-mvp-reqs.md`](synome-mvp-reqs.md) — data model, end-to-end flows, acceptance tests, non-goals

### 3. MVP Beacons

Five low-power beacons (programs, not AI) for monitoring, execution, attestation, and governance:

| Beacon | Type | Purpose |
|---|---|---|
| **lpla-verify** | LPLA | Monitor positions, calculate CRRs, generate alerts |
| **lpha-relay** | LPHA | Execute PAU transactions with rate limits |
| **lpha-nfat** | LPHA | Manage NFAT Facility lifecycle (books, units, deployment, redemption) |
| **lpha-attest** | LPHA | Independent attestor; posts risk attestations gating book transitions |
| **lpha-council** | LPHA | Core Council toolkit for risk framework and Core Halo configuration |

lpla-verify is extended into the full lpla-checker in Phase 2 (adding settlement tracking). Prime performance summaries (`lpha-report`) are introduced in Phase 3.

*Deep-dive:* [`beacons.md`](beacons.md) — responsibilities, inputs/outputs, Synome access patterns, beacon categories

### 4. Core Halos and Legacy Cleanup

Before deploying Configurator, current Prime exposures must be reduced and simplified. Legacy assets either become **Core Halos** (static entries in Synome-MVP, live data fetched by lpla-verify) or are wound down.

*Deep-dive:* [`core-halos-and-cleanup.md`](core-halos-and-cleanup.md) — Core Halo model, decision tree, cleanup targets, acceptance criteria

### 5. Configurator Unit

Enables GovOps teams to manage Prime operations without requiring Sky Spells. Two-tier access model: Core Council creates pre-approved configurations (inits) via 14-day timelock; GovOps activates rate limits within those bounds. SORL constrains rate limit increases to 25% per 18h.

*Canonical spec:* [`../../smart-contracts/configurator-unit.md`](../../smart-contracts/configurator-unit.md)

### 6. NFAT Smart Contracts

Two contracts enable Term Halos: the **NFAT Facility** (queue, claim, mint, deploy) and the **Redeem Contract** (receive, notify, redeem). Connected via shared PAU; lpha-nfat holds pBEAM for Facility operations.

*Canonical spec:* [`../../smart-contracts/nfats.md`](../../smart-contracts/nfats.md)
*Book implementation:* [`halo-book-deep-dive.md`](halo-book-deep-dive.md) — lifecycle, Synome schema, offboarding pipeline

### 7. Term Halo Legal + SOFR Hedging

Legal infrastructure enabling lpha-nfat to execute deals autonomously within governance-approved bounds. Buybox model defines acceptable parameter ranges; deals within the buybox need no additional governance approval. Includes SOFR hedging requirements for Primes deploying into duration NFATs.

*Deep-dive:* [`term-halo-legal.md`](term-halo-legal.md) — buybox model, legal isolation, governance artifacts, SOFR hedging, deliverables

---

## Substages

Phase 1 is delivered in seven sequential substages:

| Substage | Name | Key Outcome |
|---|---|---|
| **1.0** | Planning | Stakeholder alignment, Prime cohort identification |
| **1.1** | Diamond PAU Deployment | Diamond PAUs deployed for first-cohort Primes |
| **1.2** | Operational Infrastructure | Synome-MVP, lpla-verify, lpha-relay operational |
| **1.3** | Legacy Cleanup & Core Halos | Legacy assets standardized or wound down |
| **1.4** | Configurator Deployment | Spell-less Prime operations enabled |
| **1.5** | First Term Halo | Halo1 live with end-to-end NFAT flow validated |
| **1.6** | Term Halo Cohort | Halo2-Halo6 deployed and accepting NFAT deployments |

---

### Phase 1.0: Planning

**Objective:** Establish target timeline for full Phase 1 delivery

- Align all stakeholders on scope and dependencies
- Identify first cohort of Primes participating in initial NFAT deployments
- Confirm Term Halo partners and onboarding order

---

### Phase 1.1: Diamond PAU Deployment

**Objective:** Deploy Diamond PAU architecture for first-cohort Primes

| Task | Description |
|---|---|
| **Deploy Diamond PAU factory** | Standardized factory for Diamond PAU deployment |
| **Deploy first-cohort Diamond PAUs** | Diamond PAUs for Primes joining initial NFAT rollout |
| **Migrate from legacy PAUs** | Migrate positions and wind down legacy controllers |

---

### Phase 1.2: Operational Infrastructure

**Objective:** Deploy infrastructure enabling Prime deployment into Core Halos

| Task | Description |
|---|---|
| **Deploy Synome-MVP** | Operational database for risk parameters and position data |
| **Deploy Verify Beacon** | lpla-verify for CRR calculations and position monitoring |
| **Deploy Relay Beacon** | lpha-relay for rate-limited PAU operations |

These components enable Primes to deploy into Core Halos with proper monitoring and execution infrastructure, even before Configurator removes the spell requirement. Settlement tracking is added in Phase 2 with the full lpla-checker.

---

### Phase 1.3: Legacy Cleanup & Core Halos

**Objective:** Complete legacy cleanup and standardize retained assets

| Task | Description |
|---|---|
| **Wind down remaining legacy** | Close out exposures not becoming Core Halos |
| **Register Core Halos** | Register retained legacy assets as Core Halo entries in Synome-MVP (via lpha-council) with risk model and data model references |
| **Verify data sources** | Confirm lpla-verify can fetch live data for each Core Halo (on-chain RPC or financial APIs) |

---

### Phase 1.4: Configurator Deployment

**Objective:** Enable spell-less Prime operations

| Task | Description |
|---|---|
| **Deploy Configurator Unit** | BEAMTimeLock → BEAMState → Configurator stack |
| **Register Core Halos** | Add Core Halo allocation targets to Configurator |
| **Grant cBEAMs** | Provision GovOps teams for their respective PAUs |
| **Prime deployment into Core Halos** | All Primes can now deploy into Core Halos without spells |

---

### Phase 1.5: First Term Halo

**Objective:** Deploy and validate first Term Halo

| Task | Description |
|---|---|
| **Deploy NFAT Smart Contracts** | Facility and Redeemer contracts |
| **Deploy NFAT Beacon** | lpha-nfat for NFAT lifecycle management |
| **Deploy Halo1** | First Term Halo with legal buybox |
| **Onboard to Configurator** | Create Halo1 inits, grant cBEAMs |
| **Prime deployment** | All Primes can deploy into Halo1 via spell-less Configurator flow |
| **Validate end-to-end** | Confirm NFAT issuance, deployment, and redemption flow |

---

### Phase 1.6: Term Halo Cohort

**Objective:** Complete initial Term Halo rollout

Deploy remaining first-cohort Term Halos (Halo2-Halo6). Each follows the same pattern:
1. Deploy legal buybox
2. Onboard to Configurator (inits + cBEAMs)
3. Primes deploy immediately — no spell required

```
Execution Timeline:

1.0           1.1            1.2            1.3            1.4            1.5            1.6
Planning  →   Diamond    →   Operational →  Legacy      →  Configurator → Halo1       →  Full Cohort
              PAU Deploy     Infra          Cleanup        Deployment     (First Halo)   Deployment
                                            + Core Halos
    │             │              │              │              │              │              │
    ▼             ▼              ▼              ▼              ▼              ▼              ▼
┌────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│Timeline│  │Diamond   │  │Synome-MVP│  │Core Halos│  │Spell-less│  │NFAT      │  │Halo2     │
│agreed  │  │PAUs      │  │Verify    │  │ready     │  │operations│  │contracts │  │Halo3     │
│        │  │deployed  │  │Relay     │  │          │  │enabled   │  │Halo1 live│  │Halo4     │
│        │  │          │  │beacons   │  │          │  │          │  │          │  │Halo5     │
│        │  │          │  │          │  │          │  │          │  │          │  │Halo6     │
└────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
```

---

## End State

At completion of Phase 1.6:
- All first-cohort Primes operate without spells via Configurator
- Core Halos registered in Synome-MVP with lpla-verify fetching live data
- Six Term Halos (Halo1-Halo6) accepting NFAT deployments with full book lifecycle
- All five beacons operational (lpla-verify, lpha-relay, lpha-nfat, lpha-attest, lpha-council)
- Synome-MVP tracking books, units, attestations, Core Halo entries, and risk framework

---

## Document Index

| Document | Description |
|---|---|
| **This file** | Phase 1 overview — deliverables, substages, end state |
| [`synome-mvp-reqs.md`](synome-mvp-reqs.md) | Synome-MVP data model, end-to-end flows, acceptance tests |
| [`halo-book-deep-dive.md`](halo-book-deep-dive.md) | Halo Book implementation — lifecycle, Synome schema, offboarding, creation policy |
| [`beacons.md`](beacons.md) | All 5 Phase 1 beacons — responsibilities, I/O, Synome access |
| [`core-halos-and-cleanup.md`](core-halos-and-cleanup.md) | Core Halo model, legacy decision tree, cleanup targets |
| [`term-halo-legal.md`](term-halo-legal.md) | Buybox model, legal isolation, governance artifacts, SOFR hedging |

**Canonical smart contract specs** (not duplicated here):
- [`../../smart-contracts/diamond-pau.md`](../../smart-contracts/diamond-pau.md) — Diamond PAU architecture
- [`../../smart-contracts/configurator-unit.md`](../../smart-contracts/configurator-unit.md) — Configurator Unit
- [`../../smart-contracts/nfats.md`](../../smart-contracts/nfats.md) — NFAT Facility and Redeem Contract

---

## Related

- [Roadmap overview](../roadmap-overview.md)
- [Phase 0 — Legacy Exceptions](../phase-0-legacy-exceptions.md) (runs concurrently)
- [Phase 2 — Monthly Settlement](../phase-2-monthly-settlement.md) (next phase)
- [Beacon taxonomy](../../synomics/macrosynomics/beacon-framework.md) — canonical LPLA/LPHA/HPLA/HPHA definitions
