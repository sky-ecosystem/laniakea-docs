# Halo Architecture: Class, Book, Unit

**Status:** Draft
**Last Updated:** 2026-02-28

---

## Overview

Halos organize capital into three layers: **Class**, **Book**, and **Unit**. Each layer serves a distinct purpose: Classes share infrastructure, Books balance assets against liabilities, and Units connect one agent's book to another's.

```
Halo Class (shared smart contract infra + default terms)
    |
    +-- Halo Book (balanced ledger)
    |     Assets:      Loan X + Loan Y
    |     Liabilities: Unit 1, Unit 2
    |
    +-- Halo Book (balanced ledger)
          Assets:      Loan Z
          Liabilities: Unit 3
```

---

## The Book Pattern

A Book is a **balanced ledger**: assets on one side, liabilities on the other. Every agent in the Laniakea capital stack maintains books, and they chain together through Units — a Unit is simultaneously an asset in the book above and a liability in the book below.

```
Generator
  Book:
    Liabilities: USDS in circulation
    Assets:      Prime Units
                    │
                    ▼  Unit = connecting tissue
Prime
  Book:
    Liabilities: Units held by Generator
    Assets:      Halo Units
                    │
                    ▼  Unit = connecting tissue
Halo
  Book:
    Liabilities: Units held by Primes
    Assets:      Real-world loans, bonds, positions
```

This recursive structure means the entire capital stack, from USDS holders down to individual loans, is connected through a uniform pattern of books linked by units. Each layer can be reasoned about independently (does this book balance? are its assets sound?) while the unit links ensure the whole system stays coherent.

> **Phase 1 scope:** Only Halo books are implemented. The book pattern at Prime and Generator level is the target architecture but is not yet built.

---

## Halo Class

A Halo Class is the **unit of smart contract infrastructure and default terms**. It defines the product family — what kinds of deals can happen, through what contracts, under what rules.

### What a Class Provides

| Component | Purpose |
|---|---|
| **PAU** | Single Controller + ALMProxy + RateLimits shared by all Units in the Class |
| **LPHA Beacon(s)** | `lpha-lcts` for Portfolio Classes; `lpha-nfat` + `lpha-attest` for Term Classes |
| **Legal Buybox** | Acceptable parameter ranges — duration, size, APY, asset types, counterparty requirements |
| **Queue Contract** | Where capital enters (Primes deposit here) |
| **Redeem Contract** | Where capital exits (Halo deposits returned funds here) |
| **Factory Template** | All Units deployed from the same pre-audited template |

### What a Class Defines

The Class sets the **default terms and constraints** that all Units and Books within it must respect:

- **Parameter ranges** (the buybox): what durations, sizes, yields, and asset types are acceptable
- **Counterparty requirements**: which Primes can participate, what qualifications are needed
- **Recourse mechanisms**: what happens on default, what the Fortification Conserver can do
- **Operational rules**: how beacons operate, what rate limits apply, what reporting is required

Anything within the buybox can be executed autonomously by the LPHA beacon. Anything outside requires governance intervention.

### One Class, Many Books

A single Class can support multiple Books and many Units — all sharing the same contracts and legal framework but offering different risk/return profiles. This is what makes Halos scalable: the expensive infrastructure (smart contracts, legal setup, audits, governance approval) is built once per Class, then reused across every Book and Unit.

---

## Halo Book

A Halo Book is a **balanced ledger** — a bankruptcy-remote boundary where the asset side holds real-world positions and the liability side records the Units that claim on those assets.

### Core Properties

| Property | Description |
|---|---|
| **Balanced** | A book's assets must equal its liabilities. The asset side holds the actual positions; the liability side records the Units that have claims on them. |
| **Bankruptcy-remote** | Each book is its own isolation boundary. If assets in one book fail, other books are unaffected. |
| **Pari passu within** | All Units in the same book share losses equally. (Tranching per book is a future extension, not yet supported.) |
| **Fully isolated across** | Units in different books have zero exposure to each other. |
| **Blended for privacy** | Multiple assets can be blended in a single book, preventing outsiders from inferring individual deal terms. |
| **Whole assets** | Each asset sits entirely in one book — assets are not split across books. |
| **Recursive** | A book's assets can include Units from other books, enabling structured layering. |

> **Phase 1 constraint:** Each Halo book holds a single asset (or multiple assets that must all be in the same state). Multi-asset books with independent asset states are a future extension.

### Book Lifecycle

Books progress through defined phases, each with different transparency and capital requirements:

```
Created --> Filling --> Deploying --> At Rest --> Unwinding --> Closed
```

| Phase | What's Happening | Synome Visibility | CRR Impact |
|---|---|---|---|
| **Created** | Empty book exists | Full | None |
| **Filling** | NFATs swept in; book holds USDS earning agent rate | Full transparency | Low |
| **Deploying** | Capital offboarded to real-world assets | Obfuscated (Schrodinger's risk) | **High** |
| **At Rest** | Fully deployed; attestor has confirmed risk characteristics | Attested risk profile (not individual borrower details) | Medium |
| **Unwinding** | Assets returning; Halo funds Redeem Contract | Transitional | -- |
| **Closed** | All Units redeemed; book wound down | Archived | -- |

The high CRR during the deploying phase creates an economic incentive to minimize the obfuscated period — Halos want to get through deployment quickly and reach the lower at-rest CRR. This balances borrower privacy against capital efficiency without mandating specific behavior.

### Two-Beacon Deployment Gate

Neither beacon can trigger deployment alone:

1. **lpha-attest** (independent Attestor) posts a risk attestation into the Synome
2. Only then can **lpha-nfat** transition the book from filling to deploying

This separation ensures independent validation before capital leaves the on-chain boundary.

### Why Books Exist

Without books, the isolation boundary would be either the Class (too broad — one bad deal contaminates everything) or the Unit (impractical — every individual NFAT would need its own legal entity and bank account). Books sit in between: they group related assets for privacy and operational efficiency while maintaining meaningful bankruptcy remoteness between groups.

The double-entry framing also makes the system auditable by construction — at any point, you can verify that a book's assets match its liabilities, and trace the full chain from USDS issuance down to individual positions through the unit links.

---

## Halo Unit

A Halo Unit is the **connecting tissue between books**. Within a Halo book, it appears as a liability — what the Halo owes to the holder. In the Prime's book above, the same Unit appears as an asset — what the Prime owns.

Every NFAT maps to a Unit. The Unit maps to a liability in the Halo book. The book holds assets equivalent to its liabilities.

### Two Token Standards

| | Portfolio (LCTS) | Term (NFAT) |
|---|---|---|
| **What the Unit is** | Shares in a pooled position | An individual ERC-721 token representing a bespoke deal |
| **Fungibility** | Fungible within the pool | Non-fungible — each NFAT has unique terms |
| **Terms** | Same for all participants | Bespoke per deal (within buybox) |
| **Transferability** | Non-transferable (internal accounting) | Transferable (optionally whitelist-restricted) |
| **What varies per Unit** | Seniority, yield, capacity, queue config | Duration, size, APY, counterparty, specific conditions |

### What a Unit Represents

A Unit is a **claim on a book**, not a claim on a specific asset. The holder's exposure is to the blended contents of the book, not to any individual loan or position within it. This is the privacy mechanism: even if you hold a Unit, you know your own terms (APY, duration, size) but cannot determine the individual terms of the underlying assets — only the blended risk characteristics as attested by the Attestor.

### Unit-to-Book Mapping

The mapping between Units and Books is flexible:

| Pattern | Description | Use Case |
|---|---|---|
| **1 Unit : 1 Book** | Single deal, single container | Simple bilateral arrangement |
| **Many Units : 1 Book** | Multiple NFATs backed by the same blended collateral | Privacy protection — individual terms can't be inferred from NFAT data |
| **Recursive** | A Book holds Units from other Books as assets | Structured products, tranching across books |

In the simplest case (1:1:1 — one Unit, one Book, one asset), the effect is identical to per-deal isolation. The book structure adds flexibility without removing the simple case.

---

## How the Layers Interact

### Capital Flow

```
Prime deposits sUSDS
        |
        v
  Queue Contract  (Class-level)
        |
        | lpha-nfat claims from queue
        v
  Halo Book  (asset side receives capital; liability side records the Unit)
        |
        | NFAT minted
        v
  Halo Unit  (appears as liability in Halo book, asset in Prime book)
```

At redemption, the flow reverses: assets return to the book, the Halo funds the Redeem Contract (Class-level), and the Unit holder burns their NFAT to claim.

### What Each Layer Controls

| Decision | Layer |
|---|---|
| What contracts are used? | **Class** |
| What parameter ranges are acceptable? | **Class** (buybox) |
| What rate limits apply? | **Class** (PAU) |
| Which beacon operates? | **Class** |
| Where is the bankruptcy-remote boundary? | **Book** |
| Who bears losses if assets fail? | **Book** (pari passu across Units in the same book) |
| What blended risk profile do assets have? | **Book** (via attestor) |
| What specific terms does the investor have? | **Unit** |
| Who holds the claim? | **Unit** |
| What can be transferred or traded? | **Unit** |

### Boundaries Summary

```
CLASS boundary = infrastructure sharing
                 (same contracts, same beacon, same legal framework)

BOOK boundary  = risk isolation + balance
                 (bankruptcy remoteness, loss containment, privacy,
                  assets = liabilities)

UNIT boundary  = individual claim + cross-book link
                 (specific terms, specific holder, transferable position,
                  asset in one book ↔ liability in another)
```

---

## Examples

### Example 1: Portfolio Halo — Tranched CLO

```
Halo Class: CLO Tranched
  (PAU + lpha-lcts + legal buybox for CLO assets)
  |
  +-- Book alpha
  |     Assets:      Pool of CLO tranches
  |     Liabilities: Senior Unit (lower yield, first claim)
  |                  Junior Unit (higher yield, absorbs losses first)
  |
  +-- Book beta
        Assets:      Different CLO pool
        Liabilities: Single Unit
```

Senior and Junior Units in Book alpha share fate on the book's assets (with waterfall priority defined by tranche terms). If Book beta's assets default, Book alpha is unaffected.

### Example 2: Term Halo — Blended Lending Facility

```
Halo Class: Senior Secured Facility
  (PAU + lpha-nfat + lpha-attest + buybox: 6-24mo, 8-15% APY)
  |
  +-- Book alpha
  |     Assets:      Loan A + Loan B (blended)
  |     Liabilities: NFAT #1 (25M, 6mo, 10% APY → Spark)
  |                  NFAT #2 (50M, 12mo, 11% APY → Grove)
  |
  +-- Book beta
        Assets:      Loan C + Loan D (blended)
        Liabilities: NFAT #3 (30M, 18mo, 12% APY → Spark)
                     NFAT #4 (15M, 9mo, 9% APY → Keel)
```

NFAT holders #1 and #2 share fate in Book alpha (pari passu). NFAT holders #3 and #4 share fate in Book beta. The two books are fully isolated. None of the four NFAT holders can infer the individual terms of Loans A-D — only the blended risk characteristics attested by the Attestor.

### Example 3: Simple 1:1:1

```
Halo Class: Bilateral Facility
  |
  +-- Book gamma
        Assets:      Single bond position
        Liabilities: NFAT #5 (100M, 12mo → Grove)
```

One Unit, one Book, one asset. The book structure adds no overhead in this case — it degenerates to straightforward per-deal isolation.

---

## Legal Mapping

| Halo Concept | BVI SPC Equivalent | Delaware Equivalent |
|---|---|---|
| **Halo Class** | The SPC entity itself | The Series LLC parent |
| **Halo Book** | Segregated portfolio (statutory ring-fencing under BVI BCA s.146) | Individual series (untested in bankruptcy) |
| **Halo Unit** | Share/interest within a portfolio | Membership interest in a series |

BVI SPCs provide materially stronger book-level isolation than Delaware Series LLCs — the BVI statutory segregation has been court-tested, while Delaware series isolation has not.

At scale (100+ concurrent Units), a hybrid approach applies: statutory isolation (separate portfolio) for high-value books, contractual isolation (grouped portfolio with limited recourse clauses) for smaller ones.

---

## Related Documents

| Document | Relationship |
|---|---|
| `agent-type-halos.md` | Halos as a Synomic Agent type; spectrum from minimal to complex |
| `portfolio-halo.md` | Portfolio Halo business overview (LCTS-based Classes) |
| `term-halo.md` | Term Halo business overview (NFAT-based Classes) |
| `../smart-contracts/lcts.md` | LCTS token standard — queue mechanics for Portfolio Units |
| `../smart-contracts/nfats.md` | NFAT token standard — bespoke deal mechanics for Term Units |
