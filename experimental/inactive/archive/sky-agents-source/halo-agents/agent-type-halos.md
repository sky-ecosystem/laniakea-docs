# Halos: The Fractal Layer

Halos are general-purpose Synomic Agents that proliferate to meet demand — the fractal layer that can wrap any value and give it agency.

---

## What Halos Are

Halos are flexible, general-purpose Synomic Agents:

- **Wrap value with agency** — Any asset or exposure can become a Halo
- **Proliferate fractally** — Halos multiply to meet demand
- **Range from minimal to complex** — No token to full governance
- **Organized into classes and units** — Shared infrastructure, distinct products

Halos are the leaves on the tree — Primes are the major branches, but Halos are where most of the surface area lives.

---

## The Halo Spectrum

Halos span the full range of Synomic Agent possibilities:

```
Minimal                                              Complex
    │                                                    │
    ▼                                                    ▼
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ No token │    │ Simple   │    │ Governed │    │ Structured│
│ No owner │    │ purpose  │    │ w/ token │    │ tranches  │
│ Just     │    │          │    │          │    │           │
│ exists   │    │          │    │          │    │           │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │               │
  Autonomous     Functional      Stakeholder     Institutional
  lifeform       agent           governed        product
```

---

## Halo Classification

Halos are classified on two dimensions: **regulatory treatment** (Standard vs Special) and **Halo Class type** (the capital deployment mechanism).

### Standard Halo Class Types

#### Portfolio Halos (LCTS-based)

Pooled exposure through Liquidity Constrained Token Standard:

- **Pooled capital** — Multiple participants, shared exposure
- **Tranching possible** — Senior/junior within same structure
- **LCTS mechanics** — Standardized deposit/redemption
- **Shared infrastructure** — Halo Class contains multiple Units

Example: A credit fund where participants share pro-rata exposure.

#### Term Halos (NFAT-based)

Bespoke arrangements through Non-Fungible Allocation Tokens:

- **Individual deals** — Each NFAT is a specific arrangement (Halo Unit)
- **Custom terms** — Duration, size, conditions vary per deal
- **Facility model** — Halo provides the facility, NFATs are individual drawdowns
- **Queue-based origination** — Deposits queue, NFATs match to borrowers
- **Asset-liability balanced** — Halo Books (balanced ledger) back Halo Units (liability side)
- **Privacy-preserving** — Blended books prevent inference of individual loan terms

Example: A lending facility where 5 loans are blended into a book, and 10 NFATs are issued against the blended collateral.

#### Trading Halos (AMM-based)

Instant liquidity through automated market making:

- **Programmatic counterparty** — AMM executes swaps at oracle-referenced prices with configurable spread
- **Instant settlement** — Users trade atomically; the Halo absorbs the underlying settlement delay
- **Spread revenue** — Capital providers (Primes) earn spreads instead of traditional yield
- **Configurator-gated** — Can only trade assets already approved by governance

Example: A Trading Halo providing instant t-bill-to-USDS conversion at a 5bps spread.

### Special Halos

Special Halos have additional regulatory or operational requirements beyond standard Halo rules:

- **Identity Network Halo** — Operates identity verification infrastructure (KYC registries)
- **Exchange Halo** — Operates intent-based exchange infrastructure (orderbooks, matching engines)

---

## Halo Classes, Books, and Units

Halos are organized hierarchically with a separation between liability side (units) and asset side (books):

```
Halo Class (shared infrastructure)
    │
    ├── LIABILITY SIDE: Halo Units
    │   ├── Halo Unit 1 (NFAT — claim on Book A)
    │   ├── Halo Unit 2 (NFAT — claim on Book A)
    │   └── Halo Unit 3 (NFAT — claim on Book B)
    │
    └── ASSET SIDE: Halo Books
        ├── Halo Book A (Loan X + Loan Y — backs Units 1, 2)
        └── Halo Book B (Loan Z — backs Unit 3)
```

**Halo Class:**
- Shared smart contract infrastructure (PAU, beacons, queue, redeem)
- Shared legal structure (buybox)
- Defines the product family

**Halo Units (liability side):**
- Individual claims within the class (NFATs for Term Halos, shares for Portfolio Halos)
- Different risk/return profiles
- Each unit is a claim on a specific book

**Halo Books (asset side):**
- Balanced ledgers (assets = liabilities) that back units
- Units sharing a book are pari passu on losses (unless tranched)
- Units on different books are fully isolated
- Multiple assets can be blended in a book for borrower privacy
- In the simplest case, one unit maps directly to one book (1:1)

---

## Minimal Halos: Pure Existence

At the simple end, Halos can be autonomous lifeforms:

- **No token** — No one governs it
- **No owner** — No one controls it
- **Permanent artifact** — Exists in the Synome indefinitely
- **Self-maintaining** — Does what it needs to persist
- **Experiencing** — Exists for its own sake

A minimal Halo might just hold some value and exist — participating in reality without extracting from it. This is permitted because the Synome supports existence itself as a valid purpose.

---

## Halos Under Primes

Halos typically nest under Primes:

```
Prime (e.g., Grove)
    ├── Halo Class A (CLO exposure)
    │   ├── Units: Unit 1 (senior), Unit 2 (junior)
    │   └── Books: Book α (CLO tranche pool — backs Units 1, 2)
    └── Halo Class B (RWA exposure)
        ├── Units: Unit 1 (single position)
        └── Books: Book β (single RWA — backs Unit 1)
```

Primes provide:
- Credit lines from the Generator
- Governance oversight
- Infrastructure and operations
- Strategic direction

Halos provide:
- Specific product exposure
- Capital packaging
- Investor interfaces
- Fractally scaled surface area

---

## Halo Lifecycle

**Creation:**
- Define the Halo Class (shared infra)
- Create Units as needed
- Register in Synome
- Establish governance (if any)

**Operation:**
- Accept deposits (LCTS) or originate deals (NFAT)
- Manage exposure
- Distribute returns
- Maintain itself

**Evolution:**
- Add new Units to existing Classes
- Modify terms through governance
- Spawn sub-Halos
- Merge or split

**Termination:**
- Wind down when purpose complete
- Distribute remaining assets
- Some Halos persist indefinitely
- Minimal Halos may never terminate

---

## Summary

1. Halos are general-purpose Synomic Agents — the fractal layer
2. Range from minimal (no token, just existing) to complex (governed, tranched)
3. Three standard class types: Portfolio (LCTS, pooled), Term (NFAT, bespoke), Trading (AMM, instant liquidity)
4. Organized into Classes (shared infra), Units (liability side), and Books (asset side)
5. Books are the balanced ledger boundary; units sharing a book are pari passu
6. Typically nest under Primes but can exist independently
7. Minimal Halos are autonomous lifeforms that just exist
8. Halos proliferate to meet demand — unlimited scalability
