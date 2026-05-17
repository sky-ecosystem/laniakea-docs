# Generator

The Generator is the foundational Synomic Entity — the entity that creates the medium through which all other Synomic activity flows. For Synomic Entity theory, see [`../macrosynomics/synomic-entities.md`](../macrosynomics/synomic-entities.md).

---

## The USDS Generator

Sky's primary Generator. Singular at the protocol level — there is one USDS Generator, and all other agents depend on it.

| Property | Description |
|---|---|
| **Type** | Foundational Agent (rank 2) |
| **Scope** | Singular per stablecoin |
| **Function** | Credit creation; system backing |
| **Dependencies** | None — others depend on it |
| **Governance** | Protocol-level (Sky Core, via SpellCore) |

---

## Credit Flow

```
            Generator
                │
                │ (credit lines)
    ┌───────────┼───────────┐
    ▼           ▼           ▼
  Spark      Grove        Keel        ...
    │           │           │
    ▼           ▼           ▼
  Halos      Halos       Halos
```

1. Generator creates USDS against collateral / backing
2. Primes receive credit lines from the Generator
3. Primes deploy capital into their domains
4. Halos nest under Primes for specific products
5. Returns flow back up the tree

The Generator does not allocate capital like a Prime. It creates the medium *of* capital. For the on-chain layout that distinguishes the Generator's PAU from Prime/Halo PAUs, see [`../smart-contracts/architecture-overview.md`](../smart-contracts/architecture-overview.md) §"Generator Layer".

---

## Operational Beacons

The Generator interacts with srUSDS via LCTS — see [`../smart-contracts/lcts.md`](../smart-contracts/lcts.md) for the queue / generation mechanics. The Generator's LCTS operations are run by `lcts-{generator}` — a relay beacon (class `relay`). See [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) for the canonical taxonomy.

---

## Risk Capital

Risk capital tokens originated through the Generator's pBEAM:

| Token | Description |
|---|---|
| **srUSDS** | Senior Risk Capital — held by end users, issued by the Generator via LCTS; absorbs losses in exchange for yield |

Primes also originate Prime-scoped risk capital (**TEJRC**, **TISRC**) via their own pBEAMs — the Generator does not own these. See [`prime.md`](prime.md) and [`../risk-framework/capital-formula.md`](../risk-framework/capital-formula.md).

---

## Reference Value

For Growth Staking purposes, the Generator is valued at `(Generator Revenue × Actual P/E + ISRC Book Value) / Tokens Outstanding`, where Generator revenue (USDS fees, USDS spread, risk capital fees, USDS SDR income; the Generator keeps 95%, with 5% pass-through to Sky Core) runs through the global P/E model and ISRC holdings are valued at par. See [`../growth-staking/growth-staking.md`](../growth-staking/growth-staking.md) §4.3 for the full formula and §2 for the Generator governance token's GF (2.5×).

---

## Relationship to Other Agent Types

| Comparison | Generator | Other |
|---|---|---|
| vs **Prime** | Creates the medium; singular; foundational | Moves the medium; multiple; operational |
| vs **Halo** | Bedrock; doesn't proliferate | Surface area; proliferates fractally |
| vs **Guardian** | Permanent; singular; creates credit | Role-based; multiple; performs operations |

---

## Related

- [`README.md`](lani/synomic-entities/README.md) — Rank hierarchy and entity index
- [`prime.md`](prime.md) — Recipients of Generator credit lines
- [`../smart-contracts/architecture-overview.md`](../smart-contracts/architecture-overview.md) — Generator-layer PAU
- [`../smart-contracts/lcts.md`](../smart-contracts/lcts.md) — srUSDS via LCTS
- [`../risk-framework/capital-formula.md`](../risk-framework/capital-formula.md) — srUSDS in the capital stack
- [`../macrosynomics/synomic-entities.md`](../macrosynomics/synomic-entities.md) — Synomic Entity theory
