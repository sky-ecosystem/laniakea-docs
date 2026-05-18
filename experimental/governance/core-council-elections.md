# Core Council Elections

How the 24-seat Core Council is composed, rotated, and held accountable. The Core Council is the body of Guardians whose collective vote shapes SpellCore (see [`spellguard.md`](spellguard.md)) and the Council Beacon (see [`../smart-contracts/configurator-unit.md`](../smart-contracts/configurator-unit.md) for the on-chain authority cascade).

---

## Council Size and Hat Threshold

| Property | Value |
|---|---|
| Council size | 24 Guardians |
| Hat threshold | 16 of 24 (2/3 supermajority) |
| Voting tokens | Core Council Guardian tokens (not SKY) |

A SpellCore spell gains the hat and executes when 16 of the 24 Guardians each have their majority vote pointing to that spell. The hat mechanic mirrors the legacy SKY-driven Executive Vote with Guardian tokens substituted for SKY.

---

## Self-Modification

The Core Council uses SpellCore to modify its own membership — adding, removing, or replacing Guardians via regular spells subject to the 16/24 threshold. Self-modification is bounded by SKY-holder freeze/override (see [`voting-mechanics.md`](voting-mechanics.md)) and by quarterly rotation (below).

---

## Quarterly Rotation

| Property | Value |
|---|---|
| Cadence | Every quarter |
| Seats rotated | 6 of 24 (full cycle every 4 quarters) |
| Mechanism | Direct SKY-holder polls (not SpellCore spells) |
| Implementation | Core Council enacts the poll result in the next regular SpellCore spell |

Rotation is anchored to SKY holders rather than the sitting Council. This prevents the Council from indefinitely entrenching itself: even with the 16/24 hat, the Council cannot block a quarterly seat poll, only execute it.

---

## Passthrough Voting

Prime, Generator, Halo, and Folio token holders whose entities hold SKY must pass their token votes through to the SKY poll. This creates a chain:

```
Entity token holder → Entity's SKY position → Quarterly poll vote
```

The passthrough mechanism ensures that beneficial ownership of SKY at the entity level translates into voting power at the protocol level. Without it, entities holding large SKY balances could either abstain (depriving holders of representation) or vote unilaterally (depriving holders of agency).

---

## Incentive Enforcement

Failure to vote in quarterly polls means **no growth staking rewards** for the failing token holder. Participation is economically enforced rather than legally required: a holder who skips a poll is not penalized directly but does forfeit the yield that participating holders receive.

This compounds: persistent non-voters fall behind on rewards, which selects against passive holding and toward active participation.

---

## Related

- [`spellguard.md`](spellguard.md) — How a hatted Council spell propagates as SpellCore → Prime SpellGuard → Halo SpellGuard
- [`voting-mechanics.md`](voting-mechanics.md) — SKY-holder freeze/override on SpellCore; ratification thresholds at each level
- [`../macrosynomics/synomic-entities.md`](../macrosynomics/synomic-entities.md) — Guardian as a Synomic Entity rank
- [`../synomic-entities/guardian.md`](../synomic-entities/guardian.md) — Ozone (the single operational Guardian)
