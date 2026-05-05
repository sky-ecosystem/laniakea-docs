# Phase 1 Beacons

**Status:** Draft
**Last Updated:** 2026-03-01

---

## Overview

Phase 1 deploys **five low-power beacons** — deterministic programs, not AI — to enable Core Halo and NFAT operations. All are either LPLA (read-only) or LPHA (rule-based execution). Sentinels (high-power, adaptive) arrive in Phases 9-10.

See [`../../synomics/macrosynomics/beacon-framework.md`](../../synomics/macrosynomics/beacon-framework.md) for the canonical beacon taxonomy.

### Beacon Summary

| Beacon | Type | Category | Purpose |
|---|---|---|---|
| **lpla-verify** | LPLA | Read-only | Monitor positions, calculate CRRs, generate alerts |
| **lpha-relay** | LPHA | Execution | Execute PAU transactions with rate limits |
| **lpha-nfat** | LPHA | Execution | Manage NFAT Facility lifecycle (books, units, deployment, redemption) |
| **lpha-attest** | LPHA | Attestation | Independent attestor; posts risk attestations gating book transitions |
| **lpha-council** | LPHA | Governance tooling | Core Council toolkit for risk framework and Core Halo configuration |

### Synome-MVP Access Matrix

| Beacon | Reads from Synome | Writes to Synome |
|---|---|---|
| **lpha-council** | — | Risk framework, Core Halo entries |
| **lpha-nfat** | Attestations (to gate transitions) | Books (create, update, state transitions), Units (create, update) |
| **lpha-attest** | Book state (to know when to attest) | Attestations |
| **lpla-verify** | Risk framework, books, units, attestations, Core Halo entries | Nothing (read-only) |
| **lpha-relay** | — | — |

---

## lpla-verify — Position Verification and Risk Alerting

**Type:** LPLA (Low Power, Low Authority) — read-only, no execution authority

**Operator:** Core Council GovOps

### Responsibilities

| Responsibility | Description |
|---|---|
| **Position Verification** | Verify on-chain positions match expected state |
| **CRR Calculation** | Calculate Capital Ratio Requirements using risk params from Synome-MVP |
| **Alert Generation** | Flag positions approaching risk thresholds |
| **Core Halo Monitoring** | For each Core Halo entry, fetch live data from external sources (on-chain RPC for DeFi positions, financial APIs for assets like JAAA/BUIDL) and compute CRR |
| **Book State Monitoring** | Read book records from Synome-MVP, apply CRR multipliers based on book lifecycle phase |
| **Re-attestation Tracking** | Flag books where periodic re-attestation is overdue; escalate CRR |

### Inputs

- On-chain position data (via RPC)
- Price feeds (oracles)
- Risk framework from Synome-MVP (CRR equations, data model)
- Book records from Synome-MVP (state, aggregate risk data, attestation timestamps)
- Core Halo entries from Synome-MVP (risk model reference, data model reference)
- External financial data (APIs for assets like JAAA, BUIDL)

### Outputs

- CRR calculations per Prime, per book, per Core Halo
- Position verification results (match/mismatch)
- Alerts (threshold breaches, overdue re-attestations, position anomalies)

### Phase 1 Scope vs Later

| Phase 1 | Phase 2+ |
|---|---|
| CRR calculation and position monitoring | **+ Settlement tracking** (lpla-checker) |
| Alert generation | **+ Settlement completeness verification** |
| Core Halo live data fetching | **+ Late payment detection and penalty calculation** |
| Book state monitoring | **+ Prime performance summaries** (Phase 3, lpha-report) |

---

## lpha-relay — Rate-Limited Execution

**Type:** LPHA (Low Power, High Authority) — rule-based execution on behalf of Halos/Primes

**Operator:** Halo GovOps (accordant to the PAU)

### Responsibilities

| Responsibility | Description |
|---|---|
| **Rate-Limited Execution** | Submit transactions within governance-approved rate limits |
| **Relay Role** | Act as authorized executor for PAU operations |
| **NFAT Deployment** | Deploy capital into NFAT Facilities |
| **Core Halo Deployment** | Deploy capital into Core Halo legacy assets |
| **Queue Processing** | Process pending operations in priority order |
| **Failure Handling** | Retry failed transactions, escalate persistent failures |

### Inputs

- Execution requests from governance/operations
- Rate limit parameters from Configurator
- PAU state (current rate limit headroom)

### Outputs

- Executed transactions (on-chain)
- Execution logs

### Key Constraint

lpha-relay **does not read or write Synome-MVP**. It operates purely on-chain via PAU infrastructure. Synome awareness is handled by lpha-nfat (which coordinates with lpha-relay for NFAT-related deployments).

---

## lpha-nfat — NFAT Facility Lifecycle

**Type:** LPHA (Low Power, High Authority) — rule-based execution on behalf of a Term Halo

**Operator:** Halo GovOps (accordant to the NFAT Facility PAU)

### Responsibilities

| Responsibility | Description |
|---|---|
| **Book Management** | Create halo books in Synome-MVP, update through lifecycle (created → filling → offboarding → deploying → at rest → unwinding → closed) |
| **Queue Sweeping + Unit Creation** | Sweep assets from NFAT Facility queue, mint on-chain NFATs, create corresponding halo unit entries in Synome-MVP |
| **Book Creation Policy** | Decide when to create new books vs. add NFATs to existing filling books, based on deal pipeline and deposit demand |
| **Attestation-Gated Transitions** | Read attestations from lpha-attest in Synome-MVP; only transition books when required attestation exists |
| **RWA Offboarding** | Convert USDS → USDC via PAU relay, send to external account, update book assets at each step |
| **Redemption** | Process returned funds (bank account → USDC → USDS → Redeem Contract), update book and unit state through unwinding and closure |

### Inputs

- Attestations from Synome-MVP (from lpha-attest)
- Facility queue state (on-chain)
- RWA endpoint status (external — bank confirmations)
- Configured book creation parameters (target size, diversity requirements)

### Outputs

- On-chain NFATs (ERC-721 minted to Primes)
- Book and unit records in Synome-MVP
- Deployment/redemption transactions (on-chain via PAU)

### On-chain Permissions

| Action | Required Permission |
|---|---|
| Claim from Queue | pBEAM on Queue Contract |
| Mint NFAT | pBEAM on NFAT Contract |
| Deploy via PAU | pBEAM on Controller (relay role) |
| Move to Redeem Contract | pBEAM on Redeem Contract |

### Detailed Book Operations

See [`halo-book-deep-dive.md`](halo-book-deep-dive.md) for the full book lifecycle, Synome schema, offboarding sub-steps, and creation policy.

---

## lpha-attest — Independent Attestor

**Type:** LPHA (Low Power, High Authority) — deterministic, rule-based

**Operator:** Independent Attestor company (whitelisted by Sky governance)

### Responsibilities

| Responsibility | Description |
|---|---|
| **Pre-deployment Attestation** | Before a book enters deploying: attest expected aggregate risk parameters, confirm legal documentation, set maximum deployment duration |
| **At-rest Attestation** | When deployment is complete: confirm aggregate risk parameters, verify legal claims are in place |
| **Periodic Re-attestation** | Per schedule (e.g., quarterly): re-attest that book status is nominal, update risk data if needed |

### Key Constraints

| Property | Description |
|---|---|
| **Can** | Write attestations into Synome-MVP |
| **Cannot** | Move capital, mint NFATs, change book status directly |
| **Accountability** | Subject to its own GovOps supply chain of checks and audits |
| **Independence** | Must be operated by a party independent from the Halo operator |

### Attestation Types

| Type | When | Content |
|---|---|---|
| **Pre-deployment** | During OFFBOARDING, after USDC conversion but before external transfer | Legal structure verified, bank account verified, expected aggregate risk parameters, maximum deployment duration |
| **At-rest** | When deployment is complete | Confirmed aggregate risk parameters, legal claims verified |
| **Periodic** | Per schedule (e.g., quarterly) | Re-attestation that book status is nominal, any risk data updates |

### Two-Beacon Deployment Gate

Neither lpha-attest nor lpha-nfat can send capital off-chain alone. lpha-nfat can freely begin offboarding and convert USDS → USDC on-chain, but requires attestation before sending USDC externally:

```
HALO                              SYNOME                          ATTESTOR
(lpha-nfat)                                                     (lpha-attest)
    │                                │                               │
    │  1. Book → OFFBOARDING       │                               │
    │  ─────────────────────────────▶│                               │
    │                                │                               │
    │  2. Convert USDS → USDC        │                               │
    │     (on-chain, no gate)        │                               │
    │  ─────────────────────────────▶│                               │
    │                                │                               │
    │                                │  3. Upload pre-deployment     │
    │                                │     attestation (legal +      │
    │                                │     bank account verified)    │
    │                                │  ◀────────────────────────────│
    │                                │                               │
    │  4. Attestation present ✓      │                               │
    │  ◀─────────────────────────────│                               │
    │                                │                               │
    │  5. Send USDC externally       │                               │
    │  ─────────────────────────────▶│                               │
```

This separation ensures independent validation before capital leaves the on-chain boundary. The attestor confirms that legal structure and destination bank account are sound before any USDC moves off-chain.

---

## lpha-council — Core Council Toolkit

**Type:** LPHA (Low Power, High Authority) — governance tooling, not an autonomous beacon

**Operator:** Core Council GovOps

### Responsibilities

| Responsibility | Description |
|---|---|
| **Risk Framework** | Publish CRR equations and the data model that books and units must conform to |
| **Core Halo Entries** | Register legacy/static collateral positions with risk model and data model references |
| **Configuration Management** | Maintain Synome operational parameters |

### Inputs

- Core Council decisions on risk framework and Core Halo configuration

### Outputs

- Risk framework records in Synome-MVP
- Core Halo entries in Synome-MVP

### Key Distinction

lpha-council is **governance tooling**, not an autonomous beacon. It provides the interface through which Core Council configures the operational Synome. It does not make autonomous decisions or act without explicit human direction.

---

## Phase 1 Evolution Path

| Phase 1 Beacon | Evolves Into | Phase |
|---|---|---|
| lpla-verify | **lpla-checker** (adds settlement tracking, penalty calculation) | Phase 2 |
| lpha-relay | Remains; eventually supplemented by stl-base execution | Phase 9 |
| lpha-nfat | Remains; factories automate Halo deployment around it | Phase 5 |
| lpha-attest | Remains; may gain richer attestation schemas over time | — |
| lpha-council | Remains; expanded to manage Portfolio Halo configs | Phase 4 |
| *(new)* | **lpha-report** — Prime performance summaries | Phase 3 |
| *(new)* | **lpha-lcts** — LCTS vault operations for Portfolio Halos | Phase 4 |

---

## Related Documents

| Document | Relationship |
|---|---|
| [`phase-1-overview.md`](phase-1-overview.md) | Phase 1 deliverables and substages |
| [`synome-mvp-reqs.md`](synome-mvp-reqs.md) | Synome-MVP data model and beacon access patterns |
| [`halo-book-deep-dive.md`](halo-book-deep-dive.md) | Book lifecycle detail for lpha-nfat and lpha-attest |
| [`../../synomics/macrosynomics/beacon-framework.md`](../../synomics/macrosynomics/beacon-framework.md) | Canonical beacon taxonomy (LPLA/LPHA/HPLA/HPHA) |
