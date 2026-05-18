# Oracle Entity

**Status:** Stub spec — type designation. Two instantiations operational at Phase 1 (Crypto Majors Oracle, Book Attestation Oracle).

The Oracle Entity is a domain-specific data provider — a synomic entity that owns its data, certs its own beacons, and is independently revocable. It replaces the older universal `&core.oracle` Space pattern with first-class entity status. For Synomic Entity theory, see [`../macrosynomics/synomic-entities.md`](../macrosynomics/synomic-entities.md).

---

## Properties

| Property | Description |
|---|---|
| **Rank** | 2 (accordant to a Guardian) |
| **Scope** | Domain-specific — one Oracle Entity per data domain |
| **Function** | Provide trusted data atoms to the synome; cert own beacons; bear slashing for misbehavior |
| **Dependencies** | Accordant to Ozone (the operational Guardian) |
| **Governance** | Tokenless — Core Council operational vehicle, no governance token |

---

## Phase 1 Instantiations

| Entity | Domain | Data |
|---|---|---|
| **Crypto Majors Oracle** | Market data | Per-asset price / liquidity / funding-rate ticks for BTC, ETH, stETH, USDC; pushed by market-data beacons from external venues |
| **Book Attestation Oracle** | Off-synome state attestation | Cert chain for class-accordant attest-data beacons (per-riskbook attestation accord; one attestation per riskbook covers all its exobooks). Attestation atoms themselves land in the target riskbook Spaces, not at the entity root — the entity owns the cert chain that makes those attestations recognizable. |

The split: market data is objective and oracle-pushable from public venues. Attestation is signed claims about exobook state the synome can't directly verify (custody balances, exobook structural integrity). Different trust models, different beacon classes, different entities.

**Out of scope here:** legacy-halo exsyn-TRRC claims. These are not oracle-entity data. They are written per-Prime by govops-operated **patch-beacons** sudoed directly into each `&entity.prime.{id}.primebook` at genesis. Patch-beacons are unregulated scaffolds (no framework, no loop template) intended to sunset as insyn coverage grows. See [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) and [`../roadmap/phase-1-spaces.md`](../roadmap/phase-1-spaces.md).

See [`../roadmap/phase-1-spaces.md`](../roadmap/phase-1-spaces.md) §"Per Oracle Entity" for the topology under each instance.

---

## Beacon Classes

| Class | Loop template | Data target | Purpose |
|---|---|---|---|
| `market-data-beacon` | `&core.loop.market-data` | Oracle entity entart root (`&entity.oracle.{domain}.root`) | Push market-data atoms (price, liquidity, funding) |
| `attest-data-beacon` | `&core.loop.attest-data` | Specific exobook Spaces the oracle is accordant to | Walk an exobook, verify assets at custodian, sign attestation atom into the target exobook |

Beacons are admin'd by their owning Oracle Entity (cert chain + per-entity config in registry).

The legacy `oracle-exsyn` class has been retired: per-Prime exsyn-TRRC scaffolding is now handled by govops-operated **patch-beacons** (no oracle-entity ownership, no regulated framework, designed to sunset). See [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md).

---

## Operational Verbs

| Verb | Caller | Effect |
|---|---|---|
| `market-data-write-tick` | `market-data-{provider}` (market-data-beacon) | Push price / liquidity / funding tick atoms to oracle entity entart root |
| `post-riskbook-attestation` | `attest-data-{class-id}` (attest-data-beacon) | Write the riskbook attestation atom into the target riskbook (closes the riskbook + all its exobooks for rollup) |

---

## Trust Model

Oracle entities bear slashing risk for misbehavior:
- Stale or missing market-data ticks
- Incorrect riskbook attestation
- Collusion with attested entities

Misbehavior propagates: bad data → wrong CRR → wrong rollup → wrong ER. The framework defaults to default-deny (no fresh accordant attestation → exobook excluded from rollup), which limits attack surface but doesn't eliminate it.

Note: legacy-halo exsyn-TRRC misbehavior is *not* an oracle-entity slashing surface — those claims are written by patch-beacons under direct govops authority, with discipline borne by govops, not oracle-entity slashing.

Independent revocability: a misbehaving Oracle Entity can be retired without affecting other oracle data. Revocation flows through Core Council governance.

---

## Lifecycle

Created via Guardian Accord under SpellCore + creation fee, like other rank-2 entities. Tokenless — no governance token issuance. See [`creation-restructuring.md`](creation-restructuring.md).

---

## Open Questions

- **Fee model.** Does Entity Creation Fee (5%) and Entity Upkeep Fee (50 bps/yr) apply to tokenless Oracle Entities? Or a different structure (e.g., usage-based fees from data consumers)?
- **Slashing parameters.** Concrete slashing magnitudes per misbehavior class.
- **Decentralization model.** Are oracle providers under one Oracle Entity required to be diverse (e.g., multi-source price aggregation), or is single-provider acceptable with slashing pressure as the discipline?
- **Cross-entity data dependencies.** Can one Oracle Entity's beacons read another's data (e.g., attest-data-beacons referencing Crypto Majors price feed for liquidation-trigger inputs in their attestation logic)? Distinct from the retired exsyn-TRRC question, which is now resolved by the patch-beacon split.
- **Future oracle entity types.** Beyond Crypto Majors + Book Attestation — off-chain interest rates, cross-chain state, equities prices, regulated-market data, others?

---

## Relationship to Other Entity Types

| Comparison | Oracle Entity | Other |
|---|---|---|
| vs **Generator** | Provides data; tokenless; multiple per domain | Provides credit; tokenless; singular |
| vs **Prime** | Tokenless data provider | Tokenized capital allocator |
| vs **Core Entity** | Domain-specific data provider; permanent | Crisis wrapper or legacy management; specialized |

---

## Related

- [`../macrosynomics/synomic-entities.md`](../macrosynomics/synomic-entities.md) — Synomic Entity theory
- [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) — Beacon taxonomy (market-data-beacon / attest-data-beacon are input classes admin'd by Oracle Entities; patch-beacons are govops-sudoed scaffolds with no oracle-entity ownership)
- [`../roadmap/phase-1-spaces.md`](../roadmap/phase-1-spaces.md) — Phase 1 Oracle Entity instances and topology
- [`creation-restructuring.md`](creation-restructuring.md) — Entity creation mechanism
- [`../accounting/entity-fees.md`](../accounting/entity-fees.md) — Fee model
