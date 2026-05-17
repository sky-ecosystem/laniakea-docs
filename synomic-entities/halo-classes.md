# Halo Architecture: Class, Book, Unit

Halos are general-purpose Synomic Entities that proliferate to meet demand. They organize capital into three layers: **Class**, **Book**, and **Unit**. Classes share infrastructure, Books balance assets against liabilities, and Units connect one agent's book to another's.

For Halo theory (autonomous lifeforms, the minimal-to-complex spectrum, structural integration), see [`../macrosynomics/synomic-entities.md`](../macrosynomics/synomic-entities.md). For per-Class operational specs, see [`halo-portfolio.md`](halo-portfolio.md), [`halo-term.md`](halo-term.md), [`halo-trading.md`](halo-trading.md), and [`halo-identity-network.md`](halo-identity-network.md).

---

## The Layered Picture

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

A **Class** is the unit of smart-contract deployment and legal framework. A **Book** is the bankruptcy-remote balanced-ledger boundary. A **Unit** is the connecting tissue — a liability in the Halo's book and an asset in the holder's book above.

---

## The Book Pattern

A Book is a balanced ledger: assets on one side, liabilities on the other. Every agent in the Laniakea capital stack maintains books, chained through Units — a Unit is simultaneously an asset in the book above and a liability in the book below.

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

The structure is recursive — at any layer you can verify that assets equal liabilities and trace the chain from USDS issuance down to individual positions. For the risk-framework formalization (riskbook → halobook → primebook), see [`../risk-framework/book-primitive.md`](../risk-framework/book-primitive.md), [`../risk-framework/riskbook-layer.md`](../risk-framework/riskbook-layer.md), [`../risk-framework/halobook-layer.md`](../risk-framework/halobook-layer.md), and [`../risk-framework/primebook-composition.md`](../risk-framework/primebook-composition.md).

---

## Halo Class

A Halo Class is the unit of smart contract infrastructure and default terms. It defines the product family — what kinds of deals can happen, through what contracts, under what rules.

### What a Class provides

| Component | Purpose |
|---|---|
| **PAU** | Single Controller + ALMProxy + RateLimits shared by all Units in the Class |
| **High-authority beacons** | `lcts-{halo}` (relay) for Portfolio Classes; `nfat-{halo}` (relay) + `attest-data-{class}` (attest-data-beacon, Oracle-Entity-owned) for Term Classes; `amm-{halo}` (relay) for Trading; `identity-{network}` (relay) for Identity Network |
| **Legal Buybox** | Acceptable parameter ranges — term / maturity, size, APY, asset types, counterparty requirements |
| **Queue Contract** | Where capital enters (Primes deposit here) |
| **Redeem Contract** | Where capital exits (Halo deposits returned funds here) |
| **Factory Template** | All Units deployed from the same pre-audited template |

### What a Class defines

The Class sets the default terms and constraints all Units and Books within it must respect:

- **Parameter ranges** (the buybox): terms / maturities, sizes, yields, asset types
- **Counterparty requirements**: which Primes can participate, qualifications needed
- **Recourse mechanisms**: default behavior, Fortification Conserver authority
- **Operational rules**: beacon operation, rate limits, reporting

Anything within the buybox can be executed autonomously by the Class's beacon(s). Anything outside requires governance intervention.

### One Class, many Books

A single Class can support multiple Books and many Units, all sharing contracts and legal framework but offering different risk/return profiles. This is what makes Halos scalable: expensive infrastructure (smart contracts, legal setup, audits, governance approval) is built once per Class, then reused.

---

## Halo Book

A Halo Book is a balanced ledger — a bankruptcy-remote boundary where the asset side holds real-world positions and the liability side records the Units that claim on those assets.

| Property | Description |
|---|---|
| **Balanced** | Assets equal liabilities; the asset side holds the positions, the liability side records the Units |
| **Bankruptcy-remote** | Each book is its own isolation boundary. If one book's assets fail, others are unaffected |
| **Pari passu within** | Units in the same book share losses equally (tranching per book is a future extension) |
| **Fully isolated across** | Units in different books have zero exposure to each other |
| **Blended for privacy** | Multiple assets blended in a book prevent inference of individual deal terms |
| **Whole assets** | Each asset sits entirely in one book |
| **Recursive** | A book's assets can include Units from other books (structured layering) |

### Book lifecycle

Books progress through defined phases with different transparency and capital requirements:

```
Created --> Filling --> Deploying --> At Rest --> Unwinding --> Closed
```

| Phase | What's Happening | Synome Visibility | CRR Impact |
|---|---|---|---|
| **Created** | Empty book exists | Full | None |
| **Filling** | NFATs swept in; book holds USDS earning agent rate | Full transparency | Low |
| **Deploying** | Capital offboarded to RWAs | Obfuscated (Schrödinger's risk) | High |
| **At Rest** | Fully deployed; attestor confirmed risk characteristics | Attested risk profile (no individual borrower details) | Medium |
| **Unwinding** | Assets returning; Halo funds Redeem Contract | Transitional | — |
| **Closed** | All Units redeemed; book wound down | Archived | — |

The high CRR during Deploying creates economic incentive to minimize the obfuscated period. See [`halo-term.md`](halo-term.md) for the two-beacon deployment gate (`attest-data-{class}` + `nfat-{halo}`).

---

## Halo Unit

A Halo Unit is the connecting tissue between books. Within a Halo book, it appears as a liability — what the Halo owes to the holder. In the Prime's book above, the same Unit appears as an asset.

### Two main token standards

| | Portfolio (LCTS) | Term (NFAT) |
|---|---|---|
| **Unit shape** | Shares in a pooled position | ERC-721 token representing a bespoke deal |
| **Fungibility** | Fungible within the pool | Non-fungible — each NFAT has unique terms |
| **Terms** | Same for all participants | Bespoke per deal (within buybox) |
| **Transferability** | Non-transferable (internal accounting) | Transferable (optionally whitelist-restricted) |
| **What varies per Unit** | Seniority, yield, capacity, queue config | Term / maturity, size, APY, counterparty, conditions |

Trading Halo Units use AMM pool shares (LCTS-shaped); Identity Network Halos do not issue capital-deployment Units in the standard sense (they are Special Halo types).

### Unit-to-Book mapping

| Pattern | Description | Use Case |
|---|---|---|
| **1 Unit : 1 Book** | Single deal, single container | Simple bilateral arrangement |
| **Many Units : 1 Book** | Multiple Units backed by the same blended collateral | Privacy protection — individual terms can't be inferred from Unit data |
| **Recursive** | A Book holds Units from other Books as assets | Structured products, tranching across books |

In the simplest case (1:1:1 — one Unit, one Book, one asset), the effect is identical to per-deal isolation. The book structure adds flexibility without removing the simple case.

---

## How the Layers Interact

### Capital flow (Term/NFAT example)

```
Prime deposits sUSDS
        |
        v
  Queue Contract  (Class-level)
        |
        | nfat-{halo} claims from queue
        v
  Halo Book  (asset side receives capital; liability side records the Unit)
        |
        | NFAT minted
        v
  Halo Unit  (liability in Halo book, asset in Prime book)
```

At redemption, the flow reverses: assets return to the book, the Halo funds the Redeem Contract (Class-level), and the Unit holder burns their NFAT to claim.

### What each layer controls

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

---

## Examples

### Tranched Portfolio Halo

```
Halo Class: CLO Tranched
  (PAU + lcts-{halo} + legal buybox for CLO assets)
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

Senior and Junior Units in Book alpha share fate (with waterfall priority defined by tranche terms). If Book beta's assets default, Book alpha is unaffected.

### Term Halo with privacy blending

```
Halo Class: Senior Secured Facility
  (PAU + nfat-{halo} + attest-data-{class} + buybox: 6-24mo, 8-15% APY)
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

NFAT holders #1 and #2 share fate in Book alpha; #3 and #4 share fate in Book beta; the two books are fully isolated. None of the four NFAT holders can infer the individual terms of Loans A-D — only blended risk characteristics attested by the Attestor.

### Simple 1:1:1

```
Halo Class: Bilateral Facility
  |
  +-- Book gamma
        Assets:      Single bond position
        Liabilities: NFAT #5 (100M, 12mo → Grove)
```

One Unit, one Book, one asset. The book structure adds no overhead — it degenerates to straightforward per-deal isolation.

---

## Legal Mapping

| Halo Concept | BVI SPC Equivalent | Delaware Equivalent |
|---|---|---|
| **Halo Class** | The SPC entity itself | The Series LLC parent |
| **Halo Book** | Segregated portfolio (statutory ring-fencing under BVI BCA s.146) | Individual series (untested in bankruptcy) |
| **Halo Unit** | Share/interest within a portfolio | Membership interest in a series |

BVI SPCs provide materially stronger book-level isolation than Delaware Series LLCs — BVI statutory segregation has been court-tested; Delaware series isolation has not. At scale (100+ concurrent Units), a hybrid approach applies: statutory isolation (separate portfolio) for high-value books, contractual isolation (grouped portfolio with limited recourse clauses) for smaller ones.

---

## Halo Spectrum

Halos span the full Synomic Entity range — from minimal (no token, just existing) to complex (governed, tranched institutional products). The Class types in this directory cover the operational architectures:

- **Standard** Classes — Portfolio, Term, Trading
- **Special** Classes — Identity Network (additional regulatory / operational requirements)

For minimal Halos (autonomous lifeforms with no token, no owner), see [`../macrosynomics/synomic-entities.md`](../macrosynomics/synomic-entities.md).

---

## Reference Value

For Growth Staking purposes, a Halo's governance token is valued at `(Capital Reserves + Annual Earnings × Actual P/E) / Tokens Outstanding`. Capital reserves are valued at par; earnings run through the global P/E model. Early-stage Halos with no earnings history can still earn the Agent token GF (2.5×) provided their synomic artifacts demonstrate genuine deployment of capital. **Halo Units are excluded** as growth assets — they're passive yield wrappers. See [`../growth-staking/growth-staking.md`](../growth-staking/growth-staking.md) §4.6 for the full treatment.

---

## Related

- [`README.md`](lani/synomic-entities/README.md) — Rank hierarchy and entity index
- [`halo-portfolio.md`](halo-portfolio.md) — Portfolio Halo (LCTS-based)
- [`halo-term.md`](halo-term.md) — Term Halo (NFAT-based + book lifecycle)
- [`halo-trading.md`](halo-trading.md) — Trading Halo (AMM-based)
- [`halo-identity-network.md`](halo-identity-network.md) — Identity Network Halo (KYC registry)
- [`prime.md`](prime.md) — Primes administering Halos
- [`../smart-contracts/lcts.md`](../smart-contracts/lcts.md) — LCTS standard
- [`../smart-contracts/nfats.md`](../smart-contracts/nfats.md) — NFAT standard
- [`../risk-framework/halobook-layer.md`](../risk-framework/halobook-layer.md) — Halobook in the risk framework
