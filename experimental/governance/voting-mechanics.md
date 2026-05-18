# Voting Mechanics

The graduated freeze, cancel, and override responses available to SKY holders, Core Council Guardians, and per-entity token holders. These are the practical voting surfaces; for the dual-key spell flow that they wrap, see [`spellguard.md`](spellguard.md).

---

## SKY Holder Freeze and Override

SKY holders do not trigger spells under the post-transition model — that role passes to the Core Council Guardians. SKY holders retain ultimate sovereignty through a graduated response mechanism on SpellCore.

| SKY Opposition Level | Effect |
|---|---|
| Tiny minority voting against | Freeze for a few hours |
| Larger minority voting against | Freeze for a few days |
| Full quorum | **Override** — entire Core Council dismissed |

### Override Consequences

When SKY holders pass an override at full quorum:

- All 24 Core Council Guardians are dismissed
- Governance reverts to direct SKY-holder control
- SKY holders can either:
  - Pass spells directly (the original MakerDAO model), or
  - Select a new Core Council

The override is the constitutional fail-safe. It is not designed for routine use; the asymmetry between the freeze threshold (a tiny minority) and the override threshold (a full quorum) means that disagreement freezes the system, but only broad consensus dismisses the Council.

---

## Per-Level Freeze and Cancel

At Prime and Halo levels, the response is freeze-then-cancel rather than freeze-then-override.

| Mechanism | Where | Effect |
|---|---|---|
| **Freeze / Override** | SpellCore only | Graduated freeze → Council dismissal at full quorum |
| **Freeze / Cancel** | Prime and Halo SpellGuards | Graduated freeze → spell fully cancelled (no entity dismissal) |

The distinction is constitutional: at the Core level, override results in the Core Council being dismissed and governance reverting to SKY holders. At Prime and Halo levels, there is no "override" — the spell is simply cancelled. No governance body is dismissed because none of these levels has constitutional authority over its parent.

---

## BEAM-Level Freeze

Authority over BEAMs (the on-chain access cascade — see [`../smart-contracts/configurator-unit.md`](../smart-contracts/configurator-unit.md)) sits adjacent to spell governance. BEAMs can be frozen or cancelled by two independent paths:

### Individual Council Guardian Freeze

| Property | Value |
|---|---|
| Who | Any single Core Council Guardian |
| Scope | All BEAMs (aBEAM, cBEAM, pBEAM) |
| Effect | Immediate freeze/cancel of the targeted BEAM |
| Purpose | Emergency response — halt compromised or rogue operations instantly |

### SKY Holder Freeze

| Property | Value |
|---|---|
| Who | SKY token holders |
| Scope | All BEAMs |
| Mechanism | Same graduated response as SpellCore freeze |

### Anti-Paralysis: Mutual Freeze Among Guardians

Individual freeze creates a paralysis risk: a rogue Guardian could freeze everything. The anti-paralysis mechanism addresses this.

| Property | Value |
|---|---|
| Mechanism | Council Guardians can freeze/cancel each other's freeze authority |
| Quorum | 16 of 24 (same as SpellCore hat) |
| Effect | Removes the targeted Guardian's freeze/cancel ability |

The threshold to halt (any single Guardian) is deliberately much lower than the threshold to act (16/24) or to remove a blocker (16/24). This asymmetry favors safety: it is always easier to stop the system than to advance it or to remove someone trying to stop it.

```
Rogue Guardian freezes all BEAMs
        │
        ▼
Remaining Guardians coordinate
        │
        ▼
16/24 vote to revoke rogue Guardian's freeze authority
        │
        ▼
BEAMs unfrozen, operations resume
```

---

## Ratification Thresholds Summary

| Action | Threshold | Time |
|---|---|---|
| SpellCore spell hatted | 16/24 Guardians | Per spell |
| SKY freeze on SpellCore | Tiny minority → larger minority | Hours → days |
| SKY override of SpellCore | Full quorum | Constitutional emergency |
| Prime SpellGuard hatted | Prime token majority + core payload | Per spell |
| Halo SpellGuard hatted | Halo token majority + prime payload | Per spell |
| Per-level freeze | Token-holder minority | Hours → days |
| Per-level cancel | Larger minority | Days |
| BEAM freeze (individual) | Single Guardian | Instant |
| BEAM freeze (SKY) | SKY graduated response | Hours → days |
| Revoke rogue Guardian freeze | 16/24 Guardians | Per vote |
| Quarterly Council rotation | SKY-holder poll | Quarterly |

---

## Related

- [`spellguard.md`](spellguard.md) — SpellCore and SpellGuard mechanics; the dual-key flow these vote levers wrap
- [`core-council-elections.md`](core-council-elections.md) — Quarterly rotation, passthrough voting, incentive enforcement
- [`../smart-contracts/configurator-unit.md`](../smart-contracts/configurator-unit.md) — BEAM cascade beneath the Council Beacon
