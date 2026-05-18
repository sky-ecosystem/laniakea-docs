# Laniakea Phase 1: Pragmatic Delivery

**Status:** Draft
**Last Updated:** 2026-03-01

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Sentinels and Beacons](#sentinels-and-beacons)
3. [Diamond PAU Deployment](#1-diamond-pau-deployment)
4. [Synome-MVP](#2-synome-mvp)
5. [Verify Beacon](#3-verify-beacon)
6. [Relay Beacon](#4-relay-beacon)
7. [Core Halos and Legacy Cleanup](#5-core-halos-and-legacy-cleanup)
8. [Configurator Unit](#6-configurator-unit)
9. [NFAT Smart Contracts](#7-nfat-smart-contracts)
10. [NFAT Beacon](#8-nfat-beacon)
11. [Council Beacon](#9-council-beacon)
12. [Term Halo Legal](#10-term-halo-legal)
13. [SOFR Hedging](#11-sofr-hedging)
14. [Substages](#substages)

---

## Executive Summary

Phase 1 is pragmatically focused on delivering a minimal viable infrastructure for automated capital deployment. **Phase 1 continues using the existing manual settlement process**; formalized monthly settlement with lpla-checker begins in Phase 2, and daily settlement is the Phase 3 target.

Seven deliverables in sequence order:

1. **Diamond PAU Deployment** — Upgrade to Diamond PAU architecture (EIP-2535)
2. **Synome-MVP** — Operational database for halo books, halo units, Core Halo entries, attestations, and risk framework
3. **MVP Beacons** — Five low-power beacons for monitoring, execution, attestation, and governance (Prime performance reporting begins in Phase 3 with daily settlement)
4. **Core Halos and Legacy Cleanup** — Standardize legacy assets as Core Halos, wind down the rest
5. **Configurator Unit** — Simplest form enabling spell-less operations
6. **NFAT Smart Contracts** — Facility and Redeemer contracts for Term Halos
7. **Term Halo Legal** — Legal infrastructure enabling autonomous NFAT operations

**Bootstrap note:** Starting in Phase 1, Sky governance manually allocates liability duration matching (top-down). Sealed-bid OSRC and Duration auctions begin later once Prime-side `stl-base` is deployed.

**Settlement note:** Phase 1 does not formalize or automate settlement. The existing manual settlement process continues. lpla-verify monitors positions and calculates CRRs but does not track settlement progress — that capability arrives with lpla-checker in Phase 2.

---

## Sentinels and Beacons

To reduce overload of the term "sentinel," Phase 1 introduces a broader taxonomy: **beacons**.

### Beacon Taxonomy

Beacons are autonomous operational components. They vary along two axes (see `synomics/macrosynomics/beacon-framework.md` for the canonical definitions):

| Axis | Low | High |
|------|-----|------|
| **Power** | Minimal compute, narrow I/O, executes policies from elsewhere | Substantial compute, continuous I/O, local intelligence and adaptation |
| **Authority** | Independent action, peer-to-peer interaction between teleonomes | Acts on behalf of a Synomic Agent (Prime, Halo, Generator, Guardian) |

**Sentinels** are a subset of beacons — specifically, high-power beacons with high authority that will eventually manage Prime and Halo operations autonomously.

### Phase 1: Low-Power Beacons

Phase 1 deploys **low-power beacons** (programs, not AI) to enable Core Halo and NFAT operations at smaller scale:

| Beacon              | Type                      | Purpose                                                      |
| ------------------- | ------------------------- | ------------------------------------------------------------ |
| **lpla-verify**     | Low Power, Low Authority  | Monitor positions, calculate CRRs, generate alerts           |
| **lpha-relay**      | Low Power, High Authority | Execute PAU transactions with rate limits                    |
| **lpha-nfat**       | Low Power, High Authority | Manage NFAT Facility lifecycle (books, units, deployment, redemption) |
| **lpha-attest**     | Low Power, High Authority | Independent attestor; posts risk attestations gating book transitions |
| **lpha-council**    | Low Power, High Authority | Core Council toolkit for risk framework and Core Halo configuration |

These MVP beacons provide the operational foundation. lpla-verify is extended into the full lpla-checker in Phase 2 (adding settlement tracking). Prime performance summaries (`lpha-report`) are introduced in Phase 3 as part of the daily settlement process.

### Beacon Categories

**Read-only (LPLA):**
- lpla-verify — observes positions, calculates CRRs, generates alerts (no settlement tracking — that arrives with lpla-checker in Phase 2)

**Execution (LPHA):**
- lpha-relay — executes PAU transactions
- lpha-nfat — manages NFAT Facility lifecycle (creates/updates books and units in Synome, executes on-chain operations)

**Attestation (LPHA):**
- lpha-attest — operated by an independent Attestor company; posts risk attestations to Synome that gate book transitions (pre-deployment, at-rest, periodic re-attestation)

**Governance tooling (LPHA):**
- lpha-council — Core Council interface for publishing risk framework and Core Halo entries to Synome

---

## 1. Diamond PAU Deployment

Phase 1 deploys the **Diamond PAU** architecture (EIP-2535 diamond proxy pattern) replacing the legacy PAU pattern. Diamond PAUs provide modular, upgradeable functionality without full contract redeployment.

### Diamond PAU Architecture

| Component | Purpose |
|-----------|---------|
| **Diamond Proxy** | Single entry point; delegates to facets based on function selector |
| **Action Facets** | Modular contract pieces implementing specific actions |
| **DiamondCut Facet** | Adds/removes/replaces facets via governance |
| **DiamondLoupe Facet** | Introspection — lists available facets and functions |
| **RateLimits** | Linear replenishment with configurable max and slope (unchanged) |

### Benefits Over Legacy PAU

| Aspect | Legacy PAU | Diamond PAU |
|--------|------------|-------------|
| **Adding actions** | Requires full controller redeployment | Add new facet only |
| **Upgrading logic** | Replace entire controller | Replace single facet |
| **Contract size** | Limited by 24KB contract limit | Unlimited (split across facets) |
| **Factory deployment** | Manual per-Prime | Standardized factory for all Primes |

### Phase 1 Action Facets

**Core Facets:**
- `NfatDepositFacet` — Deposit into NFAT Facility queues
- `NfatWithdrawFacet` — Withdraw from queues before deal execution
- `CoreHaloFacet` — Deploy into Core Halo positions

**Migration Facets:**
- `LegacyMigrationFacet` — Wind down legacy positions during transition

### Migration Path

Each Prime migrates from legacy PAU to Diamond PAU:
1. Deploy Diamond PAU with initial facet set
2. Migrate positions from legacy ALMProxy to new Diamond
3. Grant cBEAMs to GovOps for new Diamond
4. Wind down legacy PAU once migration complete

---

## 2. Synome-MVP

Synome-MVP is the shared operational database for Halo operations. It tracks halo books (asset side), halo units (liability side), Core Halo entries (legacy collateral), risk framework configuration, and attestations from an independent attestor.

**Phase 1 mental model:** Synome-MVP is the shared database; beacons are the app layer.

See [`synome-mvp-reqs.md`](./phase1/synome-mvp-reqs.md) for the full Phase 1 requirements (data model, end-to-end flows, and explicit non-goals).

### What Synome-MVP Stores

- **Risk framework** — CRR equations and data model, published by Core Council via `lpha-council`
- **Halo books** — Asset-side containers tracking what a Halo holds; created/updated by `lpha-nfat`, with transitions gated by attestations from `lpha-attest`
- **Halo units** — Liability-side claims mapping 1:1 to on-chain NFATs; created by `lpha-nfat` when sweeping deposits
- **Attestations** — Independent risk attestations from `lpha-attest` that gate book lifecycle transitions (pre-deployment, at-rest, periodic)
- **Core Halo entries** — Static entries for legacy collateral (e.g., Morpho, SparkLend, JAAA, BUIDL); registered by `lpha-council`, read by `lpla-verify` which fetches live data externally

### Data Flows

| Beacon | Reads from Synome | Writes to Synome |
|--------|-------------------|------------------|
| **lpha-council** | — | Risk framework, Core Halo entries |
| **lpha-nfat** | Attestations (to gate transitions) | Books (create, update, state transitions), Units (create, update) |
| **lpha-attest** | Book state (to know when to attest) | Attestations |
| **lpla-verify** | Risk framework, books, units, attestations, Core Halo entries | Nothing (read-only; fetches live data for Core Halos via RPC/APIs) |

---

## 3. Verify Beacon

The Verify Beacon (lpla-verify) is the Phase 1 monitoring system for position verification and risk alerting.

**Purpose:** Monitor positions, calculate CRRs, and generate alerts (read-only reporting)

| Responsibility | Description |
|----------------|-------------|
| **Position Verification** | Verify on-chain positions match expected state |
| **CRR Calculation** | Calculate Capital Ratio Requirements using risk params from Synome-MVP |
| **Alert Generation** | Flag positions approaching risk thresholds |

**Inputs:** On-chain position data, price feeds, risk parameters from Synome-MVP

**Outputs:** CRR calculations, verification results, alerts

> **Note:** lpla-verify is LPLA (Low Power, Low Authority) because it only reads and reports — no execution authority. Settlement tracking is added when lpla-verify is extended into the full lpla-checker in Phase 2.

---

## 4. Relay Beacon

The Relay Beacon (lpha-relay) is the execution system that deploys assets via PAU into NFATs and legacy assets (Core Halos).

**Purpose:** Execute PAU transactions with rate limits and relay role

| Responsibility | Description |
|----------------|-------------|
| **Rate-Limited Execution** | Submit transactions within governance-approved rate limits |
| **Relay Role** | Act as authorized executor for PAU operations |
| **NFAT Deployment** | Deploy capital into NFAT Facilities |
| **Legacy Deployment** | Deploy capital into Core Halo legacy assets |
| **Queue Processing** | Process pending operations in priority order |
| **Failure Handling** | Retry failed transactions, escalate persistent failures |

**Inputs:** Execution requests from governance/operations, rate limit parameters from Configurator

**Outputs:** Executed transactions, execution logs

---

## 5. Core Halos and Legacy Cleanup

Before deploying Configurator, current Prime exposures must be reduced and simplified. Legacy assets either become **Core Halos** or are wound down.

### Why Cleanup Matters

Each additional exposure creates complexity:

| Impact Area | Complexity Cost |
|-------------|-----------------|
| **Configurator** | More allocation targets = more cBEAM surface area to manage |
| **MVP Beacons** | More exposures = more data to scrape, process, and monitor |
| **Risk Framework** | More positions = more CRR calculations, more edge cases |
| **Operations** | More integrations = more failure modes to handle manually |

### Core Halos

**Core Halos** are legacy or static collateral positions retained under Core Council maintenance. Unlike Term Halos (which have the full book lifecycle with attestor-gated transitions), Core Halos are registered once in Synome-MVP and their state doesn't change — `lpla-verify` fetches live data itself.

| Aspect | Description |
|--------|-------------|
| **What they are** | Existing Prime allocations worth keeping (e.g., Morpho vaults, SparkLend, JAAA, BlackRock BUIDL) |
| **How they work** | Registered as static entries in Synome-MVP by `lpha-council`, with a risk model and data model reference |
| **Risk monitoring** | `lpla-verify` reads the Core Halo entry to know what to fetch (on-chain via RPC for DeFi positions, financial APIs for assets like JAAA/BUIDL), then applies the risk model to compute CRR |
| **Integration** | `lpha-relay` deploys into Core Halos using the same relay infrastructure as NFATs |

**Initial scope:** Core Halos cover all assets that aren't Term Halos. These assets can later transition into standard Halos controlled by their respective Primes as the infrastructure matures.

```
Legacy Asset Decision Tree:

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

### Cleanup Targets

- **Promote to Core Halo**: Valuable legacy assets standardized as Halo Units
- **Wind down**: Experimental, low-value, or redundant allocations
- **Consolidate**: Redundant exposures merged into fewer, larger positions
- **Document**: Each Core Halo's data requirements for MVP beacons

### Acceptance Criteria

Primes enter Phase 1 with:
- **Core Halos** — Legacy assets wrapped as standardized Halo Units
- **No orphan exposures** — Everything either becomes a Core Halo or is wound down
- **Consistent interfaces** — All remaining positions accessible via standard PAU actions

---

## 6. Configurator Unit

The Configurator enables GovOps teams to manage Prime operations without requiring Sky Spells for routine changes.

### How It Works

The Configurator uses a **two-tier access model**:

```
┌─────────────────────────────────────────────────────┐
│  aBEAMs (Core Council)                              │
│  • Add inits (pre-approved configs) via timelock    │
│  • Grant cBEAMs to GovOps teams                     │
│  • Remove permissions instantly (emergency)         │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  Configurator Unit                                  │
│  (BEAMTimeLock → BEAMState → Configurator)         │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  cBEAMs (GovOps Teams)                              │
│  • Set rate limits using approved inits             │
│  • Increase rate limits (max 25% per 18h via SORL) │
│  • Decrease rate limits (always instant)            │
│  • Set relayer/freezer addresses                    │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  PAU (Controller + ALMProxy + RateLimits)           │
└─────────────────────────────────────────────────────┘
```

**Key concepts:**

| Term | Meaning |
|------|---------|
| **aBEAM** | Admin BEAM — Core Council role that manages inits and grants cBEAMs (via 14-day timelock) |
| **cBEAM** | Configurator BEAM — operational role held by GovOps for specific PAUs |
| **Init** | Pre-approved rate limit or controller action that GovOps can activate |
| **Accordant** | A GovOps is "accordant" to a PAU when they hold its cBEAM |
| **SORL** | Second-Order Rate Limit — constrains how fast rate limits can increase (25% per 18h; see `smart-contracts/configurator-unit.md` for canonical parameters) |

**Typical flow:**

1. Core Council creates inits for a new allocation target (14-day timelock)
2. Core Council grants cBEAM to GovOps for that PAU (14-day timelock)
3. GovOps activates rate limits using the approved inits
4. GovOps increases limits gradually via SORL (25% every 18 hours)
5. GovOps can decrease limits instantly at any time

**Safety properties:**

- Additions require 14-day timelock (time to detect problems)
- Removals are instant (emergency response)
- Rate limit increases are gradual (SORL bounds damage from compromise)
- Decreases are always allowed (can always reduce exposure)

---

## 7. NFAT Smart Contracts

Two contracts enable Term Halos:

### NFAT Facility

The Facility manages the complete NFAT lifecycle:

| Function | Description |
|----------|-------------|
| **Queue** | Holds Prime capital awaiting deal execution |
| **Claim** | lpha-nfat claims capital from queue when deal is struck |
| **Mint** | Issues ERC-721 NFAT representing the claim |
| **Deploy** | Transfers funds to RWA endpoint via PAU |

### NFAT Redeemer

The Redeemer processes NFAT redemptions:

| Function | Description |
|----------|-------------|
| **Receive** | Accepts returned funds from RWA endpoint |
| **Notify** | Signals NFAT holder that redemption is available |
| **Redeem** | NFAT holder presents token, receives funds, NFAT burns |

### Integration

- Facility and Redeemer connect via shared PAU
- lpha-nfat holds pBEAM for Facility operations
- All state changes logged to Synome

---

## 8. NFAT Beacon

The NFAT Beacon (lpha-nfat) manages the NFAT Facility lifecycle — from queue sweeping to RWA offboarding.

**Purpose:** Operate NFAT Facilities end-to-end

| Responsibility | Description |
|----------------|-------------|
| **Book Management** | Create halo books in Synome-MVP, update through lifecycle (filling → offboarding → deploying → at rest → unwinding → closed) |
| **Queue Sweeping + Unit Creation** | Sweep assets from NFAT Facility queue, mint on-chain NFATs, create corresponding halo unit entries in Synome-MVP |
| **Attestation-Gated Deployment** | Read attestations from lpha-attest in Synome-MVP, trigger book state transitions (deploying, at rest) |
| **RWA Offboarding** | Offboard funds to RWA endpoints, update book assets |
| **Redemption** | Process returned funds, update book and unit state through unwinding and closure |

**Inputs:** Attestations from Synome-MVP (from lpha-attest), Facility queue state, RWA endpoint status

**Outputs:** On-chain NFATs, book and unit records in Synome-MVP, deployment/redemption transactions

---

## 9. Council Beacon

The Council Beacon (lpha-council) is the Core Council toolkit for managing Synome configuration.

**Purpose:** Enable Core Council to configure the risk framework and register Core Halo entries in Synome-MVP

| Responsibility | Description |
|----------------|-------------|
| **Risk Framework** | Publish CRR equations and the data model that books and units must conform to |
| **Core Halo Entries** | Register legacy/static collateral positions with risk model and data model references |
| **Configuration Management** | Maintain Synome operational parameters |

**Inputs:** Core Council decisions on risk framework and Core Halo configuration

**Outputs:** Risk framework and Core Halo entries in Synome-MVP

> **Note:** lpha-council is governance tooling, not an autonomous beacon. It provides the interface through which Core Council configures the operational Synome.

---

## 10. Term Halo Legal

The legal infrastructure for Term Halos must be established before NFAT Facilities can operate. This framework enables lpha-nfat to execute deals autonomously within governance-approved bounds.

### Design Principles (Inspired by Portfolio Halos)

| Principle | Application to Term Halos |
|-----------|----------------------------------|
| **Default Ownership to Sky** | Fortification Conserver can assume control of NFAT Facility assets if legal intervention is needed |
| **Standardized Structures** | Buybox templates enable rapid deal execution without per-deal legal negotiation |
| **Pre-signed Integration** | Primes and counterparties pre-sign agreements covering the full buybox parameter range |

### The Buybox Model

Each NFAT Facility defines a **buybox** — the acceptable parameter ranges for deals:

| Parameter | Example Range |
|-----------|---------------|
| **Duration** | 6-24 months |
| **Size** | 5M-100M per NFAT |
| **APY** | 8-15% |
| **Counterparties** | Approved Primes only |
| **Asset Types** | Senior secured loans, investment-grade bonds |

Deals within the buybox can be executed by lpha-nfat without additional governance approval. Deals outside the buybox require governance intervention.

### Legal Isolation

Each NFAT represents a claim on a distinct **Halo Unit** — legally and operationally isolated:

- If one NFAT's underlying deal fails, other NFATs in the facility are protected
- Each Halo Unit functions as a serialized LLC equivalent
- Recourse is limited to the specific Unit's assets

### Governance Artifacts

| Artifact | Contents |
|----------|----------|
| **Halo Artifact** | Overall governance, buybox definitions, recourse mechanisms, migration procedures |
| **Unit Artifact** | Per-NFAT operational parameters, legal recourse documentation, deal terms |

### Deliverables

1. **Buybox Template** — Reusable legal framework defining acceptable deal parameters
2. **Pre-signed Agreements** — Standard agreements Primes sign to participate in NFAT Facilities
3. **Recourse Mechanisms** — Procedures for Fortification Conserver intervention
4. **Artifact Templates** — Governance documentation for Halo and Unit Artifacts

---

## 11. SOFR Hedging

Primes deploying into NFATs with duration must manage interest rate risk. When using the ALDM (Asset-Liability Duration Matching) system for duration matching, Primes have two options:

| Option | Description |
|--------|-------------|
| **Fully Hedged** | Maintain a hedged interest rate position that provides variable yield based on SOFR movements |
| **SOFR Plus Terms** | Structure NFAT positions with SOFR plus spread pricing (floating rate) |

### Why This Matters

Fixed-rate NFATs with duration create interest rate exposure. If SOFR rises, the Prime holds a below-market position. The duration matching system assumes either:

1. The Prime has hedged this risk externally (swaps, futures), receiving variable SOFR exposure that offsets fixed NFAT duration, OR
2. The NFAT itself is priced as SOFR + spread, so yield floats with the benchmark

### Validation

lpla-verify validates that Primes deploying into duration NFATs have declared either:
- Hedge positions covering the interest rate exposure
- SOFR plus terms on the underlying NFAT

Primes without valid hedging or floating-rate terms cannot deploy into duration NFATs via the ALDM system.

---

## Substages

Phase 1 is delivered in seven sequential substages:

| Substage | Name | Key Outcome |
|----------|------|-------------|
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

| Task                                 | Description                                          |
| ------------------------------------ | ---------------------------------------------------- |
| **Deploy Diamond PAU factory**       | Standardized factory for Diamond PAU deployment      |
| **Deploy first-cohort Diamond PAUs** | Diamond PAUs for Primes joining initial NFAT rollout |
| **Migrate from legacy PAUs**         | Migrate positions and wind down legacy controllers   |

---

### Phase 1.2: Operational Infrastructure

**Objective:** Deploy infrastructure enabling Prime deployment into Core Halos

| Task                      | Description                                                |
| ------------------------- | ---------------------------------------------------------- |
| **Deploy Synome-MVP**     | Operational database for risk parameters and position data |
| **Deploy Verify Beacon**  | lpla-verify for CRR calculations and position monitoring   |
| **Deploy Relay Beacon**   | lpha-relay for rate-limited PAU operations                 |

These components enable Primes to deploy into Core Halos with proper monitoring and execution infrastructure, even before Configurator removes the spell requirement. Settlement tracking is added in Phase 2 with the full lpla-checker.

---

### Phase 1.3: Legacy Cleanup & Core Halos

**Objective:** Complete legacy cleanup and standardize retained assets

| Task | Description |
|------|-------------|
| **Wind down remaining legacy** | Close out exposures not becoming Core Halos |
| **Register Core Halos** | Register retained legacy assets as Core Halo entries in Synome-MVP (via lpha-council) with risk model and data model references |
| **Verify data sources** | Confirm lpla-verify can fetch live data for each Core Halo (on-chain RPC or financial APIs) |

---

### Phase 1.4: Configurator Deployment

**Objective:** Enable spell-less Prime operations

| Task                                 | Description                                              |
| ------------------------------------ | -------------------------------------------------------- |
| **Deploy Configurator Unit**         | BEAMTimeLock → BEAMState → Configurator stack            |
| **Register Core Halos**              | Add Core Halo allocation targets to Configurator         |
| **Grant cBEAMs**                     | Provision GovOps teams for their respective PAUs         |
| **Prime deployment into Core Halos** | All Primes can now deploy into Core Halos without spells |

---

### Phase 1.5: First Term Halo

**Objective:** Deploy and validate first Term Halo

| Task                            | Description                                                       |
| ------------------------------- | ----------------------------------------------------------------- |
| **Deploy NFAT Smart Contracts** | Facility and Redeemer contracts                                   |
| **Deploy NFAT Beacon**          | lpha-nfat for NFAT lifecycle management                           |
| **Deploy Halo1**                | First Term Halo with legal buybox                          |
| **Onboard to Configurator**     | Create Halo1 inits, grant cBEAMs                                  |
| **Prime deployment**            | All Primes can deploy into Halo1 via spell-less Configurator flow |
| **Validate end-to-end**         | Confirm NFAT issuance, deployment, and redemption flow            |

---

### Phase 1.6: Term Halo Cohort

**Objective:** Complete initial Term Halo rollout

Deploy remaining first-cohort Term Halos:

| Halo | Description |
|------|-------------|
| **Halo2** | Term Halo partner  |
| **Halo3** | Term Halo partner |
| **Halo4** | Term Halo partner |
| **Halo5** | Term Halo partner |
| **Halo6** | Term Halo partner |

Each Term Halo follows the same pattern:
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

### End State

At completion of Phase 1.6:
- All first-cohort Primes operate without spells via Configurator
- Core Halos registered in Synome-MVP with lpla-verify fetching live data
- Six Term Halos (Halo1-Halo6) accepting NFAT deployments with full book lifecycle
- All five beacons operational (lpla-verify, lpha-relay, lpha-nfat, lpha-attest, lpha-council)
- Synome-MVP tracking books, units, attestations, Core Halo entries, and risk framework
