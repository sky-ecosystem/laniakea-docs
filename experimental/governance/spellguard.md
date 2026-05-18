# SpellGuards

Spells in Laniakea flow through a layered system: **SpellCore** at the top (Core Council), **Prime SpellGuards** at the Prime level, **Halo SpellGuards** at the Halo level. Each layer has its own freeze and cancel capabilities. Each layer below SpellCore requires **dual-key authorization** — a top-down payload from the layer above, plus a bottom-up token hat from that layer's own holders.

---

## Layer Diagram

```
SpellCore (Core Council Guardian vote, 16/24 hat)
    │  SKY holders: freeze / override  (see voting-mechanics.md)
    │
    ▼ core spell payload
    │
Prime SpellGuard  (Prime token vote hat + core spell payload)
    │  Prime token holders: freeze / cancel
    │  (can only trigger Halo spells)
    │
    ▼ prime spell payload
    │
Halo SpellGuard  (Halo token vote hat + prime spell payload)
       Halo token holders: freeze / cancel
       (arbitrary execution)
```

---

## SpellCore

The top-level spell mechanism. Replaces the legacy model where SKY tokens directly voted on Executive Spells through the pause proxy.

### Hat Mechanic

| Property | Value |
|---|---|
| Voting tokens | Core Council Guardian tokens (not SKY) |
| Council size | 24 |
| Hat threshold | 16 of 24 (2/3 supermajority) |

A core spell gains the hat and executes when 16 of the 24 Guardians have their majority vote pointing to it. See [`core-council-elections.md`](core-council-elections.md) for how the Council itself is elected and rotated.

### What SpellCore Controls

| Function | Mechanism |
|---|---|
| Set Council Beacon | Council Beacon roots all on-chain authority. See [`../smart-contracts/configurator-unit.md`](../smart-contracts/configurator-unit.md) for the aBEAM/cBEAM/pBEAM cascade beneath it. |
| Override BEAM ownership | Can revoke or reassign any aBEAM, cBEAM, or pBEAM in emergencies |
| Set Synome write rights | All Synome write access flows from Council-Beacon-derived authority |
| Trigger Prime SpellGuards | Provides the core spell payload that Prime SpellGuards require |
| Modify Council composition | Subject to quarterly rotation by SKY holders |
| Force override spells | Bypass Prime/Halo token hats (emergency, by convention) |

The SpellCore-side surface is intentionally narrow: it is the constitutional aperture between the human/governance layer and the machine layer. Operational mechanics (rate limit changes, init approvals, relayer assignments) happen further down the cascade and require specific BEAM grants — not SpellCore spells.

---

## SpellGuards (Prime and Halo Level)

SpellGuards function like the legacy StarGuard subspell-parking pattern, with added freeze/cancel capability and a dual-key authorization requirement.

### Dual-Key Authorization

No level can act unilaterally. Each SpellGuard requires both:

1. **Top-down payload** — Authorization from the layer above (core spell payload for Prime, prime spell payload for Halo)
2. **Bottom-up token hat** — The level's own token holders must vote the spell into the hat position

| SpellGuard | Payload Required | Hat Required |
|---|---|---|
| Prime SpellGuard | Core spell payload pointing to this Prime spell | Prime token holder majority |
| Halo SpellGuard | Prime spell payload pointing to this Halo spell | Halo token holder majority |

### Prime SpellGuard

| Property | Value |
|---|---|
| Authorization | Core spell payload + Prime token hat |
| Scope | Can only trigger Halo spells (cannot modify Prime state — locked by Laniakea factory) |
| Freeze/cancel | Minority of Prime token holders can freeze, escalating to full cancellation |

### Halo SpellGuard

| Property | Value |
|---|---|
| Authorization | Prime spell payload + Halo token hat |
| Scope | Arbitrary execution within the Halo's bounded surface |
| Freeze/cancel | Minority of Halo token holders can freeze, escalating to full cancellation |

---

## Force Override

The Core Council can force spells on Primes (and by extension Halos) without the Prime/Halo token hat, bypassing dual-key.

| Property | Value |
|---|---|
| Authority | Core Council via SpellCore |
| Scope | Push spells to any Prime or Halo without their token holder approval |
| Convention | Emergency use only — not exercised in normal operations |
| Backstop | SKY holders retain freeze/override on SpellCore itself (see [`voting-mechanics.md`](voting-mechanics.md)) |

The power exists because the Council may need to act when Prime/Halo token holders cannot coordinate in time, or where a Prime/Halo is acting against system interests. The SKY-holder backstop is what keeps it bounded.

---

## Relationship to Legacy

| Aspect | Legacy | Post-Transition |
|---|---|---|
| Core spell trigger | SKY token Executive Vote | Core Council Guardian vote (16/24 hat) |
| SKY holder role | Direct spell triggering | Freeze/override + quarterly rotation polls |
| Prime spell trigger | Spell from Sky Core | SpellGuard: core payload + Prime token hat |
| Halo spell trigger | Spell from Prime | SpellGuard: prime payload + Halo token hat |
| Minority protection | None | Freeze/cancel at every level |
| Emergency power | Governance pause (GSM) | Force override + Council mutual freeze/cancel |
| SubSpell parking | StarGuard | SpellGuards (same concept, extended) |

---

## Related

- [`core-council-elections.md`](core-council-elections.md) — How the 24-seat Council is composed and rotated
- [`voting-mechanics.md`](voting-mechanics.md) — SKY-holder freeze/override; per-level ratification thresholds
- [`../smart-contracts/configurator-unit.md`](../smart-contracts/configurator-unit.md) — On-chain BEAM cascade beneath the Council Beacon
- [`../noemar-synlang/runtime.md`](../noemar-synlang/runtime.md) §3-§7 — Synlang-side cert and auth chain
