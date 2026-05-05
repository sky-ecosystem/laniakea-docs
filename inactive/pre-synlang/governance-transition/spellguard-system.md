# SpellGuard System

Post-transition spell governance replacing the current SKY-token-driven Executive Vote model. Spells flow through a layered system — SpellCore at the top, SpellGuards at Prime and Halo levels — with freeze/cancel/override capabilities at every layer.

---

## Overview

```
SpellCore (Core Council Guardian vote, 16/24 hat)
    │  SKY holders: freeze / override
    │
    ▼ core spell payload
    │
Prime SpellGuard (Prime token vote hat + core spell payload)
    │  Prime token holders: freeze / cancel
    │  (can only trigger Halo spells)
    │
    ▼ prime spell payload
    │
Halo SpellGuard (Halo token vote hat + prime spell payload)
       Halo token holders: freeze / cancel
       (arbitrary execution)
```

**Key principles:**
- **Dual-key authorization** — Each level requires both top-down payload from the layer above AND bottom-up token hat from the layer's own token holders
- **Asymmetric safety** — Any minority can freeze; only majorities can act
- **Core Council force override** — Core Council can bypass Prime/Halo token hats in emergencies (by convention, not used in normal operation)
- **SKY holder supremacy** — SKY holders can dismiss the entire Core Council via override

---

## SpellCore

The top-level spell mechanism. Replaces the current model where SKY tokens directly vote on Executive Spells through the pause proxy.

### Hat Mechanic

| Property | Value |
|----------|-------|
| Voting tokens | Core Council Guardian tokens (not SKY) |
| Council size | 24 Core Council Guardians |
| Hat threshold | 16 of 24 (2/3rds supermajority) |
| Mechanism | A spell gains the hat when 16 of 24 Guardians support it |

A core spell gains the hat and executes when 16 of the 24 Core Council Guardians each have their majority vote pointing to that spell. This is the same "hat" concept from the current system but with Guardian tokens replacing SKY.

### SKY Holder Freeze/Override

SKY holders do not trigger spells but retain ultimate sovereignty through a graduated response mechanism:

| SKY Opposition Level | Effect |
|---------------------|--------|
| Tiny minority voting against | Freeze for a few hours |
| Larger minority voting against | Freeze for a few days |
| Full quorum | **Override** — entire Core Council dismissed |

**Override consequences:**
- All 24 Core Council Guardians are dismissed
- Governance reverts to direct SKY holder control
- SKY holders can either:
  - Pass spells directly (the original MakerDAO model)
  - Select a new Core Council

### What SpellCore Controls

| Function | Mechanism |
|----------|-----------|
| Set Council Beacons | Controls aBEAMs (admin BEAMs); see [council-beam-authority.md](council-beam-authority.md) |
| Override all BEAM ownership | Can override any form of BEAM ownership across the system |
| Set Synome write rights | All Synome write access flows from the Council Beacon |
| Trigger Prime SpellGuards | Provides core spell payload for Prime spells |
| Modify Council composition | Core Council uses SpellCore to modify its own membership |
| Force override spells | Can bypass Prime/Halo token hats (emergency, by convention) |

---

## Core Council Composition

### Self-Modification

The Core Council uses SpellCore to modify its own membership — adding, removing, or replacing members via regular spells (subject to the 16/24 hat threshold).

### Quarterly Rotation

| Property | Value |
|----------|-------|
| Cadence | Every quarter |
| Seats rotated | 6 of 24 (full cycle in 4 quarters) |
| Mechanism | Direct SKY holder polls (not spells) |
| Implementation | Core Council implements the poll result in the next regular SpellCore spell |

**Passthrough voting:** Prime, Generator, and Halo token holders whose agents hold SKY must vote in quarterly polls, passing their token votes through to the SKY poll. This creates a chain:

```
Agent token holder → Agent's SKY position → Quarterly poll vote
```

**Incentive enforcement:** Failure to vote in quarterly polls means no growth staking rewards. Participation is economically enforced, not optional.

---

## SpellGuards (Prime and Halo Level)

SpellGuards operate at the Prime and Halo levels. They function like the current StarGuard system where a subspell is "parked," but with added freeze/cancel capability and a dual-key authorization requirement.

### Dual-Key Authorization

No level can act unilaterally. Each SpellGuard requires both:

1. **Top-down payload** — Authorization from the layer above (core spell payload for Prime, prime spell payload for Halo)
2. **Bottom-up token hat** — The level's own token holders must vote the spell into the hat position

| SpellGuard | Payload Required | Hat Required |
|------------|-----------------|--------------|
| Prime SpellGuard | Core spell payload pointing to this Prime spell | Prime token holder majority |
| Halo SpellGuard | Prime spell payload pointing to this Halo spell | Halo token holder majority |

### Prime SpellGuard

| Property | Value |
|----------|-------|
| Authorization | Core spell payload + Prime token hat |
| Scope | Can only trigger Halo spells (cannot modify Prime state — locked by Laniakea factory) |
| Freeze/cancel | Minority of Prime token holders can freeze, escalating to full cancellation |

### Halo SpellGuard

| Property | Value |
|----------|-------|
| Authorization | Prime spell payload + Halo token hat |
| Scope | Arbitrary execution (Halos retain full flexibility) |
| Freeze/cancel | Minority of Halo token holders can freeze, escalating to full cancellation |

### Freeze/Cancel vs Freeze/Override

| Mechanism | Where | Effect |
|-----------|-------|--------|
| **Freeze/Override** | SpellCore only | Graduated freeze → Council dismissal at full quorum |
| **Freeze/Cancel** | Prime and Halo SpellGuards | Graduated freeze → spell fully cancelled (no entity dismissal) |

The distinction: at the Core level, override results in the Core Council being dismissed and governance reverting to SKY holders. At Prime and Halo levels, there is no "override" — the spell simply gets cancelled. No governance body is dismissed.

---

## Core Council Force Override

The Core Council has the power to force spells on Primes (and by extension Halos) without the Prime/Halo token hat. This bypasses the dual-key requirement.

| Property | Value |
|----------|-------|
| Authority | Core Council via SpellCore |
| Scope | Can push spells to any Prime or Halo without their token holder approval |
| Convention | Emergency use only — not exercised in normal operations |
| Backstop | SKY holders retain freeze/override on SpellCore itself |

This power exists because the Core Council may need to act in emergencies where Prime or Halo token holders cannot coordinate in time, or where a Prime/Halo is acting against system interests.

---

## Relationship to Current System

| Aspect | Current | Post-Transition |
|--------|---------|-----------------|
| Core spell trigger | SKY token Executive Vote | Core Council Guardian vote (16/24 hat) |
| SKY holder role | Direct spell triggering | Freeze/override + quarterly rotation polls |
| Prime spell trigger | Spell from Sky Core | SpellGuard: core payload + Prime token hat |
| Halo spell trigger | Spell from Prime | SpellGuard: prime payload + Halo token hat |
| Minority protection | None | Freeze/cancel at every level |
| Emergency power | Governance pause (GSM) | Force override spells + CC mutual freeze/cancel |
| SubSpell parking | StarGuard | SpellGuards (same concept, extended) |

---

## Related Documents

- [council-beam-authority.md](council-beam-authority.md) — How SpellCore sets Council Beacons and controls the BEAM hierarchy
- [target-model.md](target-model.md) — The consolidated Guardian role that populates the Core Council
- [transition-plan.md](transition-plan.md) — Phased transition to this system
- [Configurator Unit](../smart-contracts/configurator-unit.md) — Current BEAM hierarchy and operational mechanics
