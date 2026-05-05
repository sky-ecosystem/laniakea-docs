# Halo Book Deep Dive — Phase 1 Implementation Specification

**Status:** Draft
**Last Updated:** 2026-03-01
**Audience:** Engineering teams building lpha-nfat, Synome-MVP, and lpla-verify

---

## Purpose

This document specifies how Halo Books work in Phase 1 at the level of detail needed to build them. It answers: what records exist, who writes them, what triggers each state transition, and what the Synome data looks like at each step.

Books are the balanced-ledger isolation boundaries within Halos — each book balances assets against liabilities to back Halo Units (NFATs). They exist **only in the Synome** — there is no on-chain book contract. The on-chain NFAT is linked to its book via the Synome's halo unit record.

---

## Core Concepts

### Identity and Linkage

```
ON-CHAIN                              SYNOME-MVP
─────────                             ──────────
NFAT (ERC-721)                        Halo Unit record
  tokenId: 42          ◄── same ID ──►  unitId: 42
  facility: 0xABC...                    bookId: "book-7"
  principal: 25M                        dealTerms: { ... }
  depositor: 0xPrime...                 state: ACTIVE

                                      Halo Book record
                                        bookId: "book-7"
                                        haloClass: "facility-A"
                                        state: FILLING
                                        assets: [ ... ]
                                        linkedUnits: [42, 43, 44]
                                        attestations: [ ... ]
```

**Key linkage rule:** When lpha-nfat mints an NFAT on-chain (assigning it a `tokenId`), it simultaneously creates a halo unit record in the Synome using the same ID, and maps that unit to a book. The NFAT's `tokenId` is the join key between on-chain and off-chain state.

A book has no on-chain representation. It is a Synome record that groups halo units and balances the assets backing them against their corresponding liabilities.

### Phase 1 Simplification

In Phase 1, **book state is uniform** — the entire book is in one lifecycle phase at a time. A book cannot be partially filling and partially deploying.

Long-term, books may have mixed internal states (e.g., a portion in USDC, a portion deployed, a portion obfuscated). Phase 1 does not need to support this.

### Concurrent Books

A Halo Class (NFAT Facility) can have **multiple books in different states simultaneously**. For example:

- Book A: AT REST (deployed 3 months ago, earning yield)
- Book B: DEPLOYING (capital offboarded last week)
- Book C: FILLING (gathering deposits for next deployment round)

lpha-nfat manages all books within its Halo Class and must track each independently.

### Attestation Principle

**Attestation is required before any state change that makes assets not visible on-chain.** This includes:

1. **Sending assets off-chain** (within OFFBOARDING, before external transfer) — assets leaving the on-chain boundary to a bank account
2. **Entering obfuscated deployment** (OFFBOARDING → DEPLOYING) — assets entering the black-box phase with no Synome updates
3. **Entering at-rest** (DEPLOYING → AT REST) — assets remaining off-chain with attested risk characteristics

The pre-deployment attestation (posted during OFFBOARDING) gates both #1 and #2. The at-rest attestation gates #3. Any state where assets are on-chain and transparent (CREATED, FILLING, UNWINDING, CLOSED) does not require attestation to enter.

---

## Book Lifecycle — Phase 1

```
CREATED ──► FILLING ──► OFFBOARDING ──► DEPLOYING ──► AT REST ──► UNWINDING ──► CLOSED
```

Each transition is detailed below with: trigger, who acts, what changes in Synome, and what CRR treatment applies.

---

### State: CREATED

**What it is:** An empty book exists in the Synome. No assets, no units linked.

**Who creates it:** lpha-nfat

**When:** lpha-nfat decides a new book is needed based on upcoming deal pipeline and deposit demand (see [Book Creation Policy](#book-creation-policy)).

**Synome record at this point:**

```json
{
  "bookId": "book-7",
  "haloClass": "facility-A",
  "state": "CREATED",
  "assets": [],
  "linkedUnits": [],
  "attestations": [],
  "timestamps": {
    "created": "2026-03-15T10:00:00Z"
  }
}
```

**CRR:** None — empty book has no capital.

---

### State: FILLING

**What it is:** NFATs are being swept into the book. Capital enters as USDS (earning agent rate). Multiple NFATs can be added over time as deposits come in.

**Trigger:** lpha-nfat sweeps the first deposit from a Prime's facility queue into this book.

**What happens (per sweep):**

1. lpha-nfat claims USDS from a Prime's facility queue (on-chain: NFAT minted, USDS moves to Facility ALMProxy)
2. lpha-nfat writes to Synome (single transaction, two records):
   - **Create halo unit** — `unitId` matching the on-chain NFAT `tokenId`, linked to this book, with deal terms (APY, maturity, payment schedule = `bullet`)
   - **Update book** — add unit to `linkedUnits`, update `assets` to reflect increased USDS balance

This can repeat — more NFATs swept into the same book over days or weeks as deposit demand accumulates.

**Synome record during filling:**

```json
{
  "bookId": "book-7",
  "haloClass": "facility-A",
  "state": "FILLING",
  "assets": [
    {
      "type": "USDS",
      "amount": 75000000,
      "location": "facility-ALMProxy"
    }
  ],
  "linkedUnits": [42, 43, 44],
  "attestations": [],
  "timestamps": {
    "created": "2026-03-15T10:00:00Z",
    "fillingStarted": "2026-03-15T10:05:00Z"
  }
}
```

**CRR:** Low — the book holds USDS, a known and transparent asset.

**Key point:** During filling, the book's asset list is simply a USDS balance. Full transparency. Anyone reading the Synome can see exactly how much capital is staged and where it sits.

---

### State: OFFBOARDING

**What it is:** Capital is being converted from USDS → USDC and moved off-chain to the Halo's bank account. This is a multi-step process with several Synome updates as the asset composition changes.

**Trigger:** lpha-nfat decides the book is fully filled and ready for deployment. No attestation is required to begin offboarding — lpha-nfat can freely transition to OFFBOARDING and convert assets on-chain. The attestation gate comes later, before capital leaves the on-chain boundary.

**Offboarding sub-steps:**

Each sub-step is a distinct lpha-nfat action that updates the book's asset list in the Synome.

**Step 1 — Convert USDS → USDC (no attestation required):**

lpha-nfat uses its relay pBEAM on the Halo's PAU to convert USDS to USDC on-chain. This is a permissionless on-chain operation — no attestation gate needed because assets remain on-chain and fully transparent.

Synome update:
```json
{
  "assets": [
    {
      "type": "USDC",
      "amount": 75000000,
      "location": "facility-ALMProxy"
    }
  ]
}
```

**Attestation gate — before external transfer:**

Before USDC can be sent to an external account, lpha-attest must post a **pre-deployment attestation** confirming the legal structure and bank account are in good shape:

```json
{
  "attestationId": "att-101",
  "type": "PRE_DEPLOYMENT",
  "bookId": "book-7",
  "content": {
    "legalStructureVerified": true,
    "bankAccountVerified": true,
    "expectedRiskParameters": { ... },
    "maximumDeploymentDuration": "90d"
  },
  "timestamp": "2026-04-01T09:00:00Z"
}
```

Only after this attestation exists in the Synome can lpha-nfat proceed to send USDC externally. This ensures independent validation before capital leaves the on-chain boundary.

**Step 2 — Send USDC to external account (requires attestation):**

lpha-nfat initiates the off-ramp transfer (USDC → Halo bank account). Updates Synome to reflect funds are in transit.

Synome update:
```json
{
  "assets": [
    {
      "type": "USDC",
      "amount": 75000000,
      "location": "in-transit",
      "destination": "halo-bank-account-ref",
      "initiatedAt": "2026-04-01T10:30:00Z"
    }
  ]
}
```

**Step 3 — Confirm receipt:**

Once the Halo's bank confirms receipt of USD, lpha-nfat updates the Synome.

Synome update:
```json
{
  "assets": [
    {
      "type": "USD",
      "amount": 75000000,
      "location": "halo-bank-account",
      "confirmedAt": "2026-04-02T14:00:00Z"
    }
  ]
}
```

**CRR:** Transitional — the CRR during offboarding should reflect that assets are moving from transparent (USDS) to less transparent (bank account). The risk framework will define the exact treatment; implementers should track the current sub-step so lpla-verify can apply the correct rate.

**Key point:** Offboarding is where the asset list on the book gets interesting. It's not a single atomic operation — it's a sequence of real-world steps, each reflected as a Synome update to the book's assets. The book's asset list is the source of truth for "where is the money right now."

---

### State: DEPLOYING

**What it is:** Capital has been offboarded to the Halo's bank account and is now being deployed into real-world deals (loans, bonds, etc.). This is the **obfuscated phase** — the Synome does not receive granular updates about which specific borrowers receive funds, when, or on what terms.

**Trigger:** lpha-nfat transitions the book after offboarding is complete (all funds confirmed received in bank account).

**What the Synome knows during deployment:**

```json
{
  "bookId": "book-7",
  "state": "DEPLOYING",
  "assets": [
    {
      "type": "USD",
      "amount": 75000000,
      "location": "deploying",
      "note": "Funds being deployed into deals per pre-deployment attestation att-101"
    }
  ],
  "attestations": ["att-101"]
}
```

**What the Synome does NOT know:** Individual borrower identities, specific loan terms, deployment timing per deal. This is intentional — blending multiple deployments preserves borrower privacy and prevents observers from inferring terms from NFAT data.

**CRR:** **High** — "Schrodinger's risk." The assets could be anywhere from still sitting as cash to fully deployed into risky positions. The elevated CRR creates an economic incentive to minimize time in this state.

**No writes during deploying:** Neither lpha-nfat nor lpha-attest updates the book during the deploying phase. The book record is intentionally static. This is the obfuscation mechanism.

---

### State: AT REST

**What it is:** All capital has been deployed and the attestor has confirmed the risk characteristics of the deployed assets. The book now has attested aggregate risk data — not individual deal details, but blended risk characteristics.

**Trigger — attestation gate:**

lpha-attest posts an **at-rest attestation** confirming the deployed assets' characteristics:

```json
{
  "attestationId": "att-102",
  "type": "AT_REST",
  "bookId": "book-7",
  "content": {
    "confirmedRiskParameters": { ... },
    "legalClaimsVerified": true,
    "deploymentComplete": true
  },
  "timestamp": "2026-04-15T09:00:00Z"
}
```

Then lpha-nfat transitions the book and writes the attested aggregate risk data:

```json
{
  "bookId": "book-7",
  "state": "AT_REST",
  "assets": [
    {
      "type": "aggregate-deployed",
      "amount": 75000000,
      "riskData": {
        "schemaVersion": "1.0",
        "attestationRef": "att-102",
        "_comment": "Exact fields TBD — developed with Phase 1 halo cohort"
      }
    }
  ],
  "attestations": ["att-101", "att-102"]
}
```

**CRR:** Medium — lower than deploying because the attestor has confirmed characteristics, but still reflects the inherent risk of deployed real-world assets.

**Periodic re-attestation:** While at rest, lpha-attest posts periodic attestations (e.g., quarterly) confirming the book remains nominal. lpha-nfat updates the book record to reflect the fresh attestation. If re-attestation is missed, CRR increases until a new attestation is posted.

```json
{
  "attestationId": "att-103",
  "type": "PERIODIC",
  "bookId": "book-7",
  "content": {
    "statusNominal": true,
    "riskDataUpdate": { ... }
  },
  "timestamp": "2026-07-15T09:00:00Z"
}
```

---

### State: UNWINDING

**What it is:** Underlying assets are maturing or being liquidated. Funds flow back: borrower → Halo bank account → USDC → USDS → Facility Redeem Contract.

**Trigger:** lpha-nfat initiates unwinding when the first assets in the book begin returning.

**Unwinding sub-steps (mirrors offboarding in reverse):**

**Step 1 — Funds return to bank account:**
```json
{
  "assets": [
    {
      "type": "USD",
      "amount": 76500000,
      "location": "halo-bank-account",
      "note": "Principal + yield returned from deployment"
    }
  ]
}
```

**Step 2 — Convert to USDC and on-ramp:**
```json
{
  "assets": [
    {
      "type": "USDC",
      "amount": 76500000,
      "location": "facility-ALMProxy"
    }
  ]
}
```

**Step 3 — Convert USDC → USDS, fund Redeem Contract:**
```json
{
  "assets": [
    {
      "type": "USDS",
      "amount": 76500000,
      "location": "redeem-contract"
    }
  ]
}
```

lpha-nfat simultaneously updates each linked halo unit's state to REPAYMENT_AVAILABLE.

**CRR:** Transitional — decreasing as assets convert back to transparent on-chain form.

---

### State: CLOSED

**What it is:** All linked halo units have been redeemed (NFATs burned). The book is fully wound down.

**Trigger:** lpha-nfat transitions to CLOSED when the last linked unit is redeemed.

**Synome record:**

```json
{
  "bookId": "book-7",
  "state": "CLOSED",
  "assets": [],
  "linkedUnits": [42, 43, 44],
  "timestamps": {
    "created": "2026-03-15T10:00:00Z",
    "fillingStarted": "2026-03-15T10:05:00Z",
    "offboardingStarted": "2026-04-01T10:00:00Z",
    "deployingStarted": "2026-04-02T15:00:00Z",
    "atRestStarted": "2026-04-15T09:30:00Z",
    "unwindingStarted": "2026-10-01T09:00:00Z",
    "closed": "2026-10-05T11:00:00Z"
  }
}
```

The book record is retained as an archive — full history preserved for audit.

---

## Book Creation Policy

lpha-nfat decides when to create new books and which deposits to group together. This is a **business decision** driven by:

### Decision Factors

| Factor | Description |
|---|---|
| **Deal pipeline** | Upcoming borrower demand and deal opportunities inform how much capital a book should target |
| **Deposit demand** | Current queue balances across Primes — how much capital is available to sweep |
| **Diversity target** | Books should contain enough deposits to back a diversity of underlying assets, enabling borrower term obfuscation |
| **Privacy threshold** | A book with only one NFAT and one underlying asset provides no obfuscation — lpha-nfat should target multiple units per book where possible |
| **Timing** | Deposits may arrive over days or weeks; lpha-nfat holds a book in FILLING until it reaches a target size |

### Phase 1 Expectations

In Phase 1, lpha-nfat is a **low-power, rule-based beacon** — it does not make complex AI-driven decisions. The book creation logic will be straightforward:

- Halo operations team configures target book sizes and diversity parameters
- lpha-nfat follows these configured rules to bucket deposits
- Edge cases (e.g., a single large deposit that fills an entire book) are handled by the rules, not by judgment

The goal is to balance two competing needs:
1. **Don't wait forever** — Primes want their capital deployed, not sitting in a filling book
2. **Don't deploy too thin** — A book with a single asset provides no privacy benefit

### Example

```
Deal pipeline: 3 senior secured loans expected, 25M each = 75M needed
Queue state: Spark has 30M queued, Grove has 50M queued, Keel has 20M queued

lpha-nfat creates book-7 and sweeps:
  - 30M from Spark → NFAT #42
  - 25M from Grove → NFAT #43
  - 20M from Keel  → NFAT #44
  Total: 75M in book-7

Remaining 25M from Grove stays in queue for next book.
```

---

## Loss Distribution

If a book enters unwinding with **less value than expected** (partial default), proceeds are distributed **pro rata by principal** across all linked units.

### Example

```
Book-7 holds 3 units:
  NFAT #42: 30M principal
  NFAT #43: 25M principal
  NFAT #44: 20M principal
  Total: 75M principal

Book returns only 60M (80% recovery):
  NFAT #42 receives: 60M × (30/75) = 24M
  NFAT #43 receives: 60M × (25/75) = 20M
  NFAT #44 receives: 60M × (20/75) = 16M
```

Each unit bears losses in proportion to its share of the book's total principal. This is the pari passu guarantee: units sharing a book share fate equally.

**Phase 1 note:** Phase 1 uses bullet loans. The partial-default scenario is handled through legal recourse (Fortification Conserver intervention, Halo Artifact default procedures) rather than automated smart contract distribution. However, the Synome should track the pro-rata entitlements so that any resolution process has clear data to work from.

---

## Aggregate Risk Data — Phase 1 Approach

The exact fields for aggregate risk data on at-rest books are **not yet defined**. They will be developed in partnership with the Phase 1 halo cohort, because the risk parameters depend on the actual asset types being deployed.

### What Implementers Should Build

**Flexible schema:** Store aggregate risk data as versioned JSON, not as fixed database columns.

```json
{
  "schemaVersion": "1.0",
  "attestationRef": "att-102",
  "data": {
    // Fields TBD — whatever the risk framework and attestor agree on
    // Examples of what MIGHT go here (not prescriptive):
    // "weightedAverageDuration": "9.2m",
    // "creditQualityDistribution": { "investmentGrade": 0.85, "subInvestmentGrade": 0.15 },
    // "concentrationMetrics": { ... }
  }
}
```

**Validation approach:** Synome-MVP should validate that:
- `schemaVersion` is present and recognized
- `attestationRef` points to a valid attestation
- `data` is valid JSON conforming to the schema version's structure

Synome-MVP should **not** validate the semantic content of the risk data (e.g., "is this CRR reasonable?"). That's lpla-verify's job.

**lpla-verify contract:** lpla-verify reads the risk framework (published by lpha-council) to know what fields to expect, then reads the book's aggregate risk data to compute CRR. If the schema version doesn't match what the risk framework expects, lpla-verify should flag an alert.

---

## Synome-MVP Schema — Book Record

The canonical book record in Synome-MVP:

| Field | Type | Description |
|---|---|---|
| `bookId` | string | Unique identifier |
| `haloClass` | string | Parent Halo Class (NFAT Facility) identifier |
| `state` | enum | CREATED, FILLING, OFFBOARDING, DEPLOYING, AT_REST, UNWINDING, CLOSED |
| `assets` | array[Asset] | Current asset composition (see below) |
| `linkedUnits` | array[unitId] | NFAT token IDs of all halo units mapped to this book |
| `attestations` | array[attestationId] | References to attestations on this book |
| `timestamps` | object | Timestamp for each state transition |
| `metadata` | object | Versioned flexible JSON — aggregate risk data, operational notes |

### Asset Record

Each entry in the `assets` array:

| Field | Type | Description |
|---|---|---|
| `type` | string | Asset denomination: USDS, USDC, USD, aggregate-deployed |
| `amount` | number | Value in the asset's native denomination |
| `location` | string | Where the asset sits: facility-ALMProxy, in-transit, halo-bank-account, deploying, redeem-contract |
| `destination` | string? | For in-transit assets: where they're going |
| `initiatedAt` | timestamp? | For in-transit assets: when the transfer started |
| `confirmedAt` | timestamp? | For bank-confirmed assets: when receipt was confirmed |
| `riskData` | object? | For aggregate-deployed assets: versioned risk data from attestor |

**Design intent:** The asset list is a journal of "what does this book hold right now." It changes as capital moves through the offboarding and unwinding pipelines. During DEPLOYING, it's a single entry saying "this much capital is being deployed." During OFFBOARDING, it tracks the real-world movement step by step.

---

## Write Access Matrix

| Operation | Who Writes | Preconditions |
|---|---|---|
| Create book | lpha-nfat | — |
| Add unit to book (sweep) | lpha-nfat | Book is in FILLING state |
| Update book assets (offboarding sub-steps) | lpha-nfat | Book is in OFFBOARDING state |
| Transition FILLING → OFFBOARDING | lpha-nfat | — (no attestation required) |
| Convert USDS → USDC (offboarding step 1) | lpha-nfat | Book is in OFFBOARDING state |
| Post pre-deployment attestation | lpha-attest | Book is in OFFBOARDING state, USDC conversion complete |
| Send USDC externally (offboarding step 2) | lpha-nfat | Pre-deployment attestation exists from lpha-attest |
| Transition OFFBOARDING → DEPLOYING | lpha-nfat | Pre-deployment attestation exists; all funds confirmed received in bank account |
| Post at-rest attestation | lpha-attest | Book is in DEPLOYING state |
| Transition DEPLOYING → AT REST | lpha-nfat | At-rest attestation exists from lpha-attest |
| Write aggregate risk data to book | lpha-nfat | At-rest attestation provides the data |
| Post periodic attestation | lpha-attest | Book is in AT_REST state |
| Update book with periodic attestation | lpha-nfat | New periodic attestation exists |
| Transition AT REST → UNWINDING | lpha-nfat | Assets returning |
| Update book assets (unwinding sub-steps) | lpha-nfat | Book is in UNWINDING state |
| Transition UNWINDING → CLOSED | lpha-nfat | All linked units redeemed |

**Read access:** lpla-verify reads everything. lpha-attest reads book state to know when attestation is needed.

---

## End-to-End Example — Phase 1 Happy Path

This traces a single book through the entire lifecycle.

### Day 0: Book Created

lpha-nfat sees 75M in deposit demand across Primes and a pipeline of 3 senior secured deals. Creates book-7.

### Days 1-5: Filling

- Day 1: Sweep 30M from Spark → NFAT #42 created, book-7 assets: 30M USDS
- Day 2: Sweep 25M from Grove → NFAT #43 created, book-7 assets: 55M USDS
- Day 4: Sweep 20M from Keel → NFAT #44 created, book-7 assets: 75M USDS

### Day 6: Offboarding Begins

lpha-nfat transitions book-7 to OFFBOARDING (no attestation needed for this transition).

- Step 1: Convert 75M USDS → 75M USDC (on-chain via PAU relay). Synome: assets = 75M USDC at facility-ALMProxy.

### Day 6: Pre-deployment Attestation

lpha-attest posts attestation att-101: legal structure verified, bank account verified, expected risk parameters for the planned deployments, maximum deployment duration 90 days.

Now lpha-nfat can send USDC externally:

- Step 2: Send 75M USDC to Halo bank account. Synome: assets = 75M USDC in-transit.
- Step 3 (Day 7): Bank confirms receipt. Synome: assets = 75M USD in halo-bank-account.

### Day 7: Deploying

lpha-nfat transitions book-7 to DEPLOYING. From this point, no Synome updates on the book. Assets are being deployed into deals — the black box.

CRR is elevated. lpla-verify reports the book as "deploying — high CRR."

### Day 21: At Rest

Attestor completes diligence on deployed assets. lpha-attest posts attestation att-102: confirmed risk parameters, legal claims verified, deployment complete.

lpha-nfat transitions book-7 to AT_REST and writes aggregate risk data from the attestation.

CRR drops to medium level. lpla-verify reads the attested risk data and computes CRR accordingly.

### Day 90 (Quarterly): Periodic Re-attestation

lpha-attest posts attestation att-103: status nominal, no material changes. lpha-nfat updates the book.

If this attestation were missed, lpla-verify would flag the book and CRR would increase until re-attestation occurs.

### Day 180: Unwinding Begins

Underlying loans mature. Funds return to Halo bank account (75M principal + 3.75M yield = 78.75M).

- Step 1: 78.75M USD confirmed in bank account. Synome updated.
- Step 2: On-ramp 78.75M USDC. Synome: assets = 78.75M USDC at facility-ALMProxy.
- Step 3: Convert USDC → USDS, fund Redeem Contract. Synome: assets = 78.75M USDS at redeem-contract.

lpha-nfat updates each halo unit to REPAYMENT_AVAILABLE:
- NFAT #42 (30M principal): 31.5M available (pro rata share of yield)
- NFAT #43 (25M principal): 26.25M available
- NFAT #44 (20M principal): 21.0M available

### Days 181-185: Closure

- Spark burns NFAT #42, receives 31.5M USDS.
- Grove burns NFAT #43, receives 26.25M USDS.
- Keel burns NFAT #44, receives 21.0M USDS.

lpha-nfat transitions book-7 to CLOSED. Record archived.

---

## State Transition Diagram — Summary

```
                      lpha-nfat
                          │
                          ▼
                    ┌──────────┐
                    │ CREATED  │
                    └────┬─────┘
                         │ lpha-nfat sweeps first deposit
                         ▼
                    ┌──────────┐
              ┌────▶│ FILLING  │◄──── additional sweeps
              │     └────┬─────┘
              │          │
              │          │ lpha-nfat transitions (no attestation needed)
              │          ▼
              │     ┌──────────────┐
              │     │ OFFBOARDING  │  Step 1: USDS → USDC (no gate)
              │     │              │  GATE: pre-deployment attestation from lpha-attest
              │     │              │  Step 2: Send USDC externally (requires attestation)
              │     │              │  Step 3: Confirm bank receipt
              │     └──────┬───────┘
              │            │ All funds confirmed in bank account
              │            │ lpha-nfat transitions
              │            ▼
              │     ┌──────────────┐
              │     │  DEPLOYING   │  No Synome updates (intentional obfuscation)
              │     │  (black box) │  High CRR
              │     └──────┬───────┘
              │            │
              │            │ REQUIRES: at-rest attestation from lpha-attest
              │            │ THEN: lpha-nfat transitions + writes risk data
              │            ▼
              │     ┌──────────────┐
              │     │   AT REST    │  Periodic re-attestation from lpha-attest
              │     │  (deployed)  │  Medium CRR
              │     └──────┬───────┘
              │            │ Assets mature / return
              │            │ lpha-nfat transitions
              │            ▼
              │     ┌──────────────┐
              │     │  UNWINDING   │  Multiple Synome updates as assets return:
              │     │              │  bank account → USDC → USDS → redeem contract
              │     └──────┬───────┘
              │            │ All units redeemed (NFATs burned)
              │            │ lpha-nfat transitions
              │            ▼
              │     ┌──────────────┐
              │     │   CLOSED     │  Archived
              │     └──────────────┘
              │
              │
  [Error / abort paths not shown — see below]
```

---

## Error and Edge Cases

### Offboarding Failure

If the USDC transfer fails or bank receipt is not confirmed within a timeout:

- lpha-nfat should flag the issue in the book's metadata
- lpla-verify should generate an alert
- The book remains in OFFBOARDING until resolved
- Worst case: funds can be converted back to USDS and the book reverted to FILLING (operational decision, not automated)

### Missed Re-attestation

If lpha-attest does not post a periodic attestation by the expected date:

- lpla-verify escalates CRR for the book
- lpha-nfat does NOT automatically change book state — the book remains AT_REST
- The CRR penalty creates economic pressure for the attestor to re-attest

### Partial Return (Default Scenario)

If the book returns less value than the total principal:

- lpha-nfat computes pro-rata entitlements based on principal
- lpha-nfat writes the actual return amounts to each halo unit
- Legal recourse procedures (per Halo Artifact) determine recovery process
- The book can remain in UNWINDING until recovery is resolved

### Book with Single Unit

A book with only one NFAT provides no privacy obfuscation. This is acceptable in Phase 1 (especially for the first deals), but lpha-nfat should prefer multi-unit books where deposit demand allows.

---

## Open Questions (Phase 1)

| # | Question | Status |
|---|---|---|
| 1 | What are the exact fields in the aggregate risk data schema? | Blocked on Phase 1 halo cohort engagement |
| 2 | What is the periodic re-attestation cadence for Phase 1 asset types? | TBD — likely quarterly |
| 3 | What are the specific CRR multipliers for each book state? | Owned by risk framework — `risk-framework/capital-formula.md` |
| 4 | How does the yield distribution work — does the book track yield accrual, or is it just the return amount at maturity? | For Phase 1 bullet loans, yield is bundled with principal at maturity. Yield tracking is Phase 2+. |
| 5 | What timeout triggers an offboarding failure alert? | TBD — operational parameter configured per Halo Class |

---

## Related Documents

| Document | Relationship |
|---|---|
| [`synome-mvp-reqs.md`](synome-mvp-reqs.md) | Synome-MVP data model and end-to-end flows |
| [`phase-1-overview.md`](phase-1-overview.md) | Phase 1 overview and substages |
| [`../../sky-agents/halo-agents/halo-class-book-unit.md`](../../sky-agents/halo-agents/halo-class-book-unit.md) | Architectural overview of Class/Book/Unit |
| [`../../sky-agents/halo-agents/term-halo.md`](../../sky-agents/halo-agents/term-halo.md) | Term Halo business overview |
| [`../../smart-contracts/nfats.md`](../../smart-contracts/nfats.md) | NFAT smart contract specification |
| [`../../synomics/macrosynomics/beacon-framework.md`](../../synomics/macrosynomics/beacon-framework.md) | Beacon taxonomy (lpha-nfat and lpha-attest are LPHA) |
