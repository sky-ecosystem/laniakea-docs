# Core Entity

A **Core Entity** is a tokenless rank-1 Synomic Entity that serves as a Core Council operational vehicle. A Core Entity operates in one of several modes; initially two are defined — **halo mode** (managing legacy protocol positions as a halo-like vehicle under direct Core Council governance) and **busted prime/halo mode** (wrapping a failed Prime or Halo until normal operations resume). Future modes may be added as new use cases emerge.

For Synomic Entity theory, see [`../macrosynomics/synomic-entities.md`](../macrosynomics/synomic-entities.md). For the rank hierarchy, see [`README.md`](README.md). For the Guardian role and how a Guardian collapse is handled, see [`guardian.md`](guardian.md).

---

## Properties

| Property | Description |
|---|---|
| **Rank** | 1 — directly regulated by Core Council |
| **Administration** | Core Council via SpellCore |
| **Token issuance** | None — tokenless |
| **Governance tokens** | None |
| **Growth-asset status** | Excluded from Growth Staking — see [`../growth-staking/growth-staking.md`](../growth-staking/growth-staking.md) |
| **Creation** | By Core Council governance action (no Guardian Accord required, since rank-1) |
| **Duration** | Indefinite (halo mode) or temporary, dissolving after resolution (busted prime/halo mode) |
| **Function** | Operational vehicle for Core Council functions — managing legacy positions or wrapping a failed Prime/Halo |
| **Dependencies** | None at rank-1; in busted prime/halo mode, takes over the wrapped entity's downstream tree |

---

## Modes

A Core Entity operates in one of several modes. Initially, two modes are defined; future modes may be added as new use cases emerge.

### halo mode

A standardized wrapper for legacy protocol positions that are not (or not yet) operated by a Prime — managed as a halo-like vehicle under direct Core Council governance:

- **Morpho vaults** — protocol positions in Morpho lending markets
- **Aave pools** — protocol positions in Aave lending markets
- **SparkLend exposures** — direct protocol lending positions predating Prime operations
- **Other pre-existing allocations** — RWA positions or DeFi deployments from before the Agent framework

This is the function previously covered by "Core Halos." The wrapper applies the same risk framework and reporting standards as other agents in the system. Governance is via Core Council artifacts, not Halo / Prime governance.

Beyond legacy assets, halo mode is also a general-purpose mechanism for any operational need the Core Council identifies — bridge-side custody, Core-Council-funded experiments, temporary asset holders for cross-Prime coordination.

Halo-mode Core Entities are indefinite in duration and sunset per-asset as positions migrate or are wound down.

**Transition paths.** Core Entities in halo mode have two natural exits:

| Path | Description |
|---|---|
| **Transfer to Prime ownership** | When a suitable Prime is identified, assets and operational infrastructure transfer to a Prime, which then manages them through standard Halos (Portfolio, Term, or Trading) |
| **Systematic wind-down** | If positions are no longer strategically aligned, the Core Entity provides an orderly framework for unwinding |

### busted prime/halo mode

A Core Entity is activated as a temporary crisis vehicle wrapping a failed Prime or Halo when:

1. **Prime collapse** — A rank-2 Prime becomes insolvent, suffers a governance failure, or is otherwise unable to continue normal operations
2. **Halo collapse** — A rank-3 Halo collapses (e.g., insolvency, governance failure, security breach)
3. **Misconduct or breach** — The wrapped entity is implicated in fraud, security compromise, or other violations requiring immediate operational takeover

When activated in this mode, the Core Entity assumes operational control of the wrapped entity's mandate and assets:

- The wrapped Prime's strategic capital relationships, or the wrapped Halo's positions
- Downstream agents under the wrapped entity (in the Prime case, its Halos and other administered agents)
- Risk capital positions — TEJRC, TISRC, srUSDS associated with the wrapped entity

The Core Entity operates within the same PAU infrastructure but with emergency authority granted by Core Council via SpellCore. It operates the wrapped entity's mandate under direct Core Council governance until normal accordancy is restored or the wrapped entity is wound down. It then manages one or more of:

| Path | Description |
|---|---|
| **Restoration** | Hand the mandate back to a healthy Prime or Halo, restoring normal accordancy |
| **Orderly wind-down** | Systematically unwind positions, redeem risk capital, return assets to stakeholders |
| **Restructuring** | Split, merge, or reconfigure the wrapped entity (and its downstream tree) to restore operational health |
| **Loss absorption** | Invoke the loss-absorption waterfall for any realized losses during the crisis |

A busted-prime/halo-mode Core Entity dissolves once the wrapped entity has been resolved.

---

## Capital and Slashing

Core Entities do not issue tokens and do not post their own collateral — they are direct extensions of Core Council authority, not collateral-backed accountable agents like Guardians. In busted prime/halo mode, the **wrapped entity's risk capital** (TEJRC / TISRC / srUSDS) and any Guardian ORC sized to cover the wrapped entity fund the costs of the transition; the Core Entity inherits authority but not collateral risk. See [`guardian.md`](guardian.md) for ORC sizing (Rate Limit × TTS) and the slashing conditions associated with collapsed agents.

For the loss waterfall (which TEJRC / TISRC / srUSDS layer absorbs first during a crisis), see [`../risk-framework/capital-formula.md`](../risk-framework/capital-formula.md).

---

## Lifecycle

| Phase | Action |
|---|---|
| **Creation** | Core Council governance action via SpellCore — no Guardian Accord required (rank-1 entities bypass the Accord) |
| **Operation** | Operates legacy positions (halo mode) or assumes the wrapped entity's tree (busted prime/halo mode) under emergency SpellCore authority |
| **Dissolution / Termination** | halo mode: indefinite, until assets transition to a Prime or wind down; busted prime/halo mode: terminates after the wrapped entity is resolved (mandate restored to a healthy agent, wound down, or restructured) |

For the SpellCore mechanism itself, see [`../governance/spellguard.md`](../governance/spellguard.md). For where Core Entity creation sits in the broader creation-paths picture, see [`creation-restructuring.md`](creation-restructuring.md).

---

## Open Questions

| Item | Status |
|---|---|
| Future modes | Open — beyond halo mode and busted prime/halo mode, what additional modes (e.g., Guardian-wrap, governance-bridge) might be added as new use cases emerge? Each Core Entity instance is single-mode by default (immutable identity, like all Synomic Entities); to change mode, create a new entity. |
| Busted-mode authority bounds | Open — what specifically can a Core Entity in busted prime/halo mode do without further SpellCore action? Default vs escalation thresholds. |
| Guardian-collapse handling | Open — the initial two modes scope to Prime and Halo wrapping; Guardian-collapse handling is not currently covered by either mode and may require a future mode addition. The post-transition design assumes Ozone is the single operational Guardian. |

---

## Relationship to Other Entity Types

| vs | Core Entity | Other |
|---|---|---|
| **Guardian** | Direct Core Council authority via SpellCore; no collateral; tokenless | Collateral-backed accord; slashable; provides accord gatekeeping for normal Prime/Halo operations |
| **Prime** | Operational vehicle; no Synomic Entity Primitives; no capital deployment | Strategic capital deployer with Synomic Entity Primitives (credit lines, ingression, origination) |
| **Halo** | Administered by Core Council; tokenless; no Class / Book / Unit structure | Administered by a Prime; may issue tokens; has Class / Book / Unit structure |

---

## Related

- [`README.md`](README.md) — Rank hierarchy and entity index
- [`guardian.md`](guardian.md) — Normal-operations Guardian role; Guardian-collapse handling sits outside the initial two modes
- [`prime.md`](prime.md) — Common destination for transitioned halo-mode Core Entity assets; also the entity type wrapped in busted prime/halo mode
- [`creation-restructuring.md`](creation-restructuring.md) — Creation paths; Core Entity creation via SpellCore (no Guardian Accord)
- [`../governance/spellguard.md`](../governance/spellguard.md) — SpellCore action that creates Core Entities
- [`../risk-framework/capital-formula.md`](../risk-framework/capital-formula.md) — Loss-absorption waterfall used in busted prime/halo mode
- [`../sentinel/sentinel-network.md`](../sentinel/sentinel-network.md) — TTS-driven ORC sizing
