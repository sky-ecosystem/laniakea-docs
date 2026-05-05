# Books and Units

**Status:** Draft
**Last Updated:** 2026-03-01

---

## Overview

A **book** is a balanced ledger — assets on one side, liabilities on the other, always equal. A **unit** is the connecting tissue between books: it appears as an asset in one book and a liability in another.

Together, books and units form the recursive accounting structure that links the entire Laniakea capital stack — from USDS issuance down to individual real-world positions.

---

## What Is a Book?

A book is the fundamental accounting primitive in Laniakea. Every agent that holds or allocates capital maintains one or more books, and each book satisfies a single invariant:

```
Assets = Liabilities
```

The asset side holds what the agent owns — real-world loans, bond positions, units from other agents' books, or protocol tokens. The liability side records what the agent owes — units issued to holders above, or obligations to the protocol.

Books provide three properties simultaneously:

| Property | Description |
|---|---|
| **Balance** | Assets always equal liabilities. Any imbalance is immediately visible. |
| **Isolation** | Each book is bankruptcy-remote. Losses in one book cannot contaminate another. |
| **Auditability** | The double-entry structure means every position can be traced and verified at any point. |

---

## What Is a Unit?

A unit is a **cross-book link**. It represents the same economic position in two places:

- In the **issuing agent's book** — the unit is a **liability** (what the agent owes)
- In the **holding agent's book** — the unit is an **asset** (what the agent owns)

This duality is what chains the capital stack together. When a Prime holds a Halo unit, it appears as an asset on the Prime's books and a liability on the Halo's books. When the Generator holds a Prime unit, the same pattern repeats one level up.

```
Generator Book
  Assets:      Prime Unit A, Prime Unit B
  Liabilities: USDS in circulation
                    │
                    ▼  (Unit A is an asset above, a liability below)
Prime Book
  Assets:      Halo Unit X, Halo Unit Y
  Liabilities: Unit A (held by Generator), Unit B (held by Generator)
                    │
                    ▼  (Unit X is an asset above, a liability below)
Halo Book
  Assets:      Loan 1, Loan 2
  Liabilities: Unit X (held by Prime), Unit Y (held by Prime)
```

At every level, each book balances independently. The unit links ensure the full chain from USDS to underlying assets stays coherent.

---

## Two Token Standards for Units

Units are represented on-chain using one of two token standards, depending on the Halo Class:

| Standard | Model | When Used |
|---|---|---|
| **LCTS** | Fungible shares in a pooled position | Portfolio Halos — many investors, same terms |
| **NFAT** | Non-fungible ERC-721 token with bespoke terms | Term Halos — individual deals, unique parameters |

The accounting treatment is identical in both cases: the unit is an asset above and a liability below. The token standard determines how claims are subdivided and transferred, not how the book balances.

---

## Books in the Capital Stack

The book pattern applies recursively across the capital stack. Each layer maintains books, and units connect them:

| Layer | Book Assets | Book Liabilities | Units Issued To |
|---|---|---|---|
| **Generator** | Prime units | USDS in circulation | (USDS holders) |
| **Prime** | Halo units | Units held by Generator | Generator |
| **Halo** | Real-world positions (loans, bonds, AMM positions) | Units held by Primes | Primes |

### Why This Matters for Accounting

1. **Verification** — at any point, sum all books at a given level. The total liabilities should match the total assets of the level above. If they don't, something is wrong.

2. **Settlement as book updates** — settlement is the process of updating book states. Prime settlement (`prime-settlement-methodology.md`) computes what a Prime owes and adjusts its book accordingly. Daily settlement (`daily-settlement-cycle.md`) updates all books in the system at the moment of settlement.

3. **Capital ingression creates units** — when external risk capital enters a Prime (`risk-capital-ingression.md`), it creates units that appear as liabilities on the Prime's book and assets on the capital provider's book. The ingression rate determines how much of those units count toward capital adequacy.

4. **Audit trail** — the chain of books linked by units creates a complete trace from USDS issuance to real-world assets. Every USDS in circulation can be traced down through Generator → Prime → Halo books to the assets that back it.

---

## Phase 1 Scope

In Phase 1, only **Halo books** are fully implemented — see `../sky-agents/halo-agents/halo-class-book-unit.md` for the complete specification of Halo Classes, Books, and Units.

The book pattern at Prime and Generator level is the **target architecture**. Currently, Prime accounting is handled through the five-step settlement methodology (`prime-settlement-methodology.md`) without formal book structures. As the system matures through later phases, explicit book primitives will be introduced at each level.

---

## Related Documents

| Document | Relationship |
|---|---|
| `../sky-agents/halo-agents/halo-class-book-unit.md` | Halo-level Class/Book/Unit specification (Phase 1 implementation) |
| `prime-settlement-methodology.md` | How Prime settlement updates Prime-level accounting |
| `daily-settlement-cycle.md` | Daily cycle that triggers book-state updates system-wide |
| `risk-capital-ingression.md` | How ingression creates units (cross-book liabilities) |
| `../risk-framework/README.md` | Capital requirements that books must satisfy |
