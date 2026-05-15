# Guardian (Ozone)

Guardians are Synomic Entities that perform privileged operations under collateral-backed accountability. They consolidate the legacy Facilitator (interpretation), Aligned Delegate (governance participation), and Executor (operations) roles into a single role. **Ozone** is the single operational Guardian under post-transition governance — there is no longer a "multiple Guardians" arrangement. The legacy `Accordant` term is retained specifically for GovOps holding cBEAMs (see [`../smart-contracts/configurator-unit.md`](../smart-contracts/configurator-unit.md)).

For Synomic Entity theory, see [`../macrosynomics/synomic-entities.md`](../macrosynomics/synomic-entities.md). For the chain-side BEAM cascade beneath the Guardian's authority, see [`../smart-contracts/configurator-unit.md`](../smart-contracts/configurator-unit.md). For the practical voting mechanics of the Council Guardians who shape SpellCore, see [`../governance/spellguard.md`](../governance/spellguard.md) and [`../governance/voting-mechanics.md`](../governance/voting-mechanics.md).

---

## Role

Guardians are operational Synomic Entities:

- **Privileged operations** — Can perform actions others cannot
- **Collateral backing** — Post escrow to guarantee performance
- **Slashing risk** — Face penalties for failures
- **Interpretation authority** — Core Guardians interpret Atlas and create binding precedents
- **Governance participation** — Core Guardians receive delegated SKY voting power and populate the 24-seat Core Council

---

## Two Guardian Tiers

| Tier | Function | Risk |
|---|---|---|
| **Core Guardians** | Interpret Atlas, populate the Core Council, oversee Operational Guardians, governance participation | Slashing for misinterpretation, misalignment, bad-faith interpretation |
| **Operational Guardians (Ozone)** | Perform routine privileged ops on behalf of Primes / Halos | Slashing for execution failures |

Core Guardians shape the constitution and governance. Operational Guardians (Ozone) execute on the operational rails.

---

## Accountability Loop

```
1. Guardian posts collateral (skin in the game)
2. System grants execution authority
3. Guardian performs operations (and interpretation, if Core)
4. If failure: collateral slashed
5. If success: Guardian earns fees / rewards
```

### Collateral

| Property | Description |
|---|---|
| Posted | Before receiving authority |
| Sized | Proportional to operation risk; Operational Guardians' ORC sized as Rate Limit × TTS (see [`../sentinel/sentinel-network.md`](../sentinel/sentinel-network.md) for TTS economics) |
| Locked | For the duration of the role |
| Released | On successful completion or role exit, after challenge period |

### Slashing conditions

| Condition | Severity |
|---|---|
| Incorrect execution | Partial slash |
| Failure to execute | Partial slash |
| Delayed execution beyond tolerance | Partial slash |
| Bad-faith interpretation (Core Guardians) | Variable; potentially severe |
| Malicious behavior | Full slash + exclusion |

---

## Authority Cascade

Guardians sit at the top of the on-chain authority cascade:

```
SpellCore (Core Council Guardian vote, 16/24 hat)
    │
    ▼
Council Beacon (HPHA — operated by Core Council)
    │
    ▼ aBEAMs
Operational Guardian (Ozone)
    │
    ▼ cBEAMs
Accordant GovOps
    │
    ▼ pBEAMs
PAU operation (sentinels, executors, attestors)
```

The cascade is shared across the system — see [`../smart-contracts/configurator-unit.md`](../smart-contracts/configurator-unit.md) for the chain-side mechanics, [`../governance/spellguard.md`](../governance/spellguard.md) for the SpellCore surface above it, and [`../noemar-synlang/runtime.md`](../noemar-synlang/runtime.md) §3-§7 for the synlang-side cert/auth chain.

---

## Lifecycle

| Phase | Action |
|---|---|
| **Registration** | Post required collateral; register for Guardian role; receive authority envelope |
| **Operation** | Perform privileged functions; (Core only) interpret Atlas and create precedents; maintain collateral; report and attest as required; earn execution fees |
| **Exit** | Complete pending operations; wait for challenge period; reclaim collateral (if no slashing); deregister |

---

## Crisis Successor

When an Operational Guardian (Ozone) collapses or is implicated in misconduct, the Core Council needs to take over the affected agent tree (the Guardian's accordant Primes, their Halos, downstream positions). The Guardian's ORC is sized to cover the costs of the transition period. The initial two Core Entity modes (halo mode and busted prime/halo mode) scope to wrapping legacy positions and failed Primes/Halos respectively; Guardian-collapse handling is currently outside these scoped modes and is expected to be addressed by a future Core Entity mode addition (e.g., a Guardian-wrap mode) or an alternative Core Council protocol. See [`core-entity.md`](core-entity.md) for the current mode framing.

---

## Reference Value

For Growth Staking purposes, a Guardian is valued at `(Accord Fee Income × Actual P/E + SKY Holdings Book Value) / Tokens Outstanding`. Accord fees from Primes and other accordant agents run through the global P/E model; SKY holdings enter at SKY Reference Value (book value, no P/E multiplier). sUSDS used as operational collateral feeds the P/E component as part of accord fee income but is not double-counted as book value. See [`../growth-staking/growth-staking.md`](../growth-staking/growth-staking.md) §4.4 for the full treatment and §2 for the Guardian governance token's GF (2.5×).

---

## Comparisons

| vs | Guardian | Other |
|---|---|---|
| **Prime** | Operational; performs ops | Strategic; allocates capital |
| **Halo** | Performs actions; active | Wraps value; can be passive |
| **Generator** | Functional; multiple | Foundational; singular |

---

## Related

- [`README.md`](laniakea-docs/synomic-entities/README.md) — Rank hierarchy and entity index
- [`core-entity.md`](core-entity.md) — Core Council operational vehicle; Guardian-collapse handling is outside the initial two modes (halo mode, busted prime/halo mode)
- [`prime.md`](prime.md), [`halo-classes.md`](halo-classes.md) — Entities that are accordant to a Guardian
- [`../governance/core-council-elections.md`](../governance/core-council-elections.md) — How the 24 Council Guardians are elected
- [`../governance/spellguard.md`](../governance/spellguard.md) — SpellCore mechanics and the dual-key flow
- [`../governance/voting-mechanics.md`](../governance/voting-mechanics.md) — SKY-holder freeze/override; per-level ratification thresholds
- [`../smart-contracts/configurator-unit.md`](../smart-contracts/configurator-unit.md) — aBEAM/cBEAM/pBEAM cascade beneath the Council Beacon
- [`../noemar-synlang/runtime.md`](../noemar-synlang/runtime.md) §3-§7 — Synlang-side cert/auth chain
- [`../sentinel/sentinel-network.md`](../sentinel/sentinel-network.md) — TTS-driven ORC sizing
