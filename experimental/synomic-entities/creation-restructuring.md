# Agent Creation and Restructuring

How new Synomic Entities come into existence, and how existing ones reorganize. Both flows route through the **Guardian Accord** — the operational gatekeeping mechanism that brings new agents into the ecosystem.

For the rank hierarchy and the per-type spec each new agent slots into, see the [`README`](lani/synomic-entities/README.md). For Synomic Entity theory (why agents have inalienable claims, why integration eliminates the adversarial frame), see [`../macrosynomics/synomic-entities.md`](../macrosynomics/synomic-entities.md).

---

## Guardian Accord

Before any rank 2 or rank 3 agent is created, the creator obtains a **Guardian Accord** — an agreement with a Guardian (Ozone, see [`guardian.md`](guardian.md)) to facilitate the creation.

| Step | Action |
|---|---|
| 1 — Request | Creator (existing agent or external user) approaches a Guardian |
| 2 — Accord | Guardian evaluates and, if accepted, enters the accord |
| 3 — Execution | Guardian triggers the on-chain creation action |

The accord requirement applies to both creation and restructuring (Type 1 and Type 2). Guardians are operational gatekeepers; rank 1 agents created by Core Council (Core Entity, in either halo mode or busted prime/halo mode) bypass this and are created directly via SpellCore.

### Auto-Accord for Folios

Folio creation uses a lightweight **auto-accord** — a programmatic accord rather than bilateral negotiation. This preserves instant folio creation while keeping the formal Guardian-Accord requirement.

---

## Creation Paths

### By External User

| Target | Flow |
|---|---|
| **Folio** | Auto-accord → instant creation, no fee |
| **Standard Halo** | Guardian Accord → Halo created → admin ownership to user (un-tokenized; user can issue tokens later) |
| **Prime** | Guardian Accord → Prime created → admin ownership to user → **waiting period** (Synomic Entity Primitives locked) → user issues tokens (95% to user, 5% to protocol as creation fee — see [`../accounting/entity-fees.md`](../accounting/entity-fees.md) for the canonical fee spec covering Entity Creation Fee, Entity Upkeep Fee 50 bps/yr, Cross-Entity Upkeep Rebate) → Synomic Entity Primitives accessible |

**Synomic Entity Primitives** — protocol-level capabilities exclusive to Primes: receiving capital from Sky Protocol, participating in ingression, originating risk capital, accessing settlement infrastructure. Locked until the Prime issues tokens. The waiting period creates a deliberate gate between admin-controlled setup and full protocol participation.

### By Existing Agent

Mechanically identical to **Type 1 Restructure** below. The creating agent transfers assets into the new agent and receives ownership or tokens.

### By Core Council (rank 1)

| Target | Flow |
|---|---|
| **Core Entity** (halo mode) | SpellCore action → no Guardian Accord required → indefinite lifetime |
| **Core Entity** (busted prime/halo mode) | SpellCore crisis action → no Guardian Accord required → temporary lifetime, dissolves after resolution |
| **Guardian** | Governance + collateral posting (see [`guardian.md`](guardian.md)) |
| **Generator** | Governance (foundational; rare creation events) |

---

## Type 1 Restructure

**Shape:** Agent A creates Agent B, transfers selected assets into B, and receives ownership or tokens.

| Mechanic | Behavior |
|---|---|
| If B is a Halo | Agent A receives admin ownership (un-tokenized) |
| If B is a Prime | Agent A receives admin ownership; Prime starts in waiting period; Synomic Entity Primitives locked until tokens issued; on token issuance, Agent A receives 95%, protocol takes 5% creation fee |

**Available to:** All agents, including Folios.

### Use cases

- Folio holder formalizes their growth asset portfolio into a Standard Halo
- Folio holder with a strong thesis seeds a new Prime; receives 95% of Prime tokens (growth assets at GF 2.5× per growth-staking spec)
- Existing Prime spins off a specialized strategy into a Halo subsidiary
- Halo creates a new Halo to isolate an asset class or geography

### Example — Folio seeds a Prime

```
Before:
  Folio
    ├── Staked SKY: $100k
    └── Assets: $500k (mixed portfolio)

Type 1 Restructure → creates "Alpha" Prime

Immediately after:
  Folio
    ├── Staked SKY: $100k
    └── Admin control of Alpha Prime

  Alpha Prime (new, admin-controlled, no tokens yet)
    └── Assets: $500k
    └── Synomic Entity Primitives: LOCKED

After token issuance:
  Folio
    ├── Staked SKY: $100k
    └── Growth Assets: 95% of Alpha Prime tokens

  Alpha Prime (tokenized, Synomic Entity Primitives active)
    └── Assets: $500k
```

---

## Type 2 Restructure

**Shape:** Agent A spins off its infrastructure (operational system + parts of its synomic artifact) into a new Halo that A controls, and optionally upgrades its own agent type (Halo → Prime).

| Mechanic | Behavior |
|---|---|
| Step 1 | Agent A creates Halo B |
| Step 2 | Agent A transfers operational infrastructure into B |
| Step 3 | Agent A receives admin ownership of B |
| Step 4 (optional) | Agent A upgrades from Halo to Prime |

Agent A retains its identity and token. The infrastructure moves. Token holders go along — a BETA-token holder ends up holding a Prime BETA token instead of a Halo BETA token.

**Available to:** All agents *except* Folios.

### Use cases

- Successful Standard Halo upgrades to Prime status — spins off existing ops as a subsidiary Halo (admin-controlled), then upgrades itself
- Halo that has grown complex separates its infrastructure into a subsidiary for cleaner governance without upgrading

### Example — Halo upgrades to Prime

```
Before:
  "Beta" Halo (tokenized)
    ├── Token: BETA
    ├── Infrastructure: lending protocol + oracle system
    └── Assets: $200M deployed

Type 2 Restructure → spins off infra, upgrades to Prime

After:
  "Beta" Prime (same token: BETA)
    ├── Token: BETA (unchanged, now a Prime token)
    └── Admin control of:
        └── "Beta Operations" Halo (new, un-tokenized)
            ├── Infrastructure: lending protocol + oracle system
            └── Assets: $200M deployed
```

---

## Constraints and Open Questions

| Item | Status |
|---|---|
| 5% creation fee | Applies when a Prime issues tokens (Type 1 or external creation). Does not apply to Halos. |
| Synomic artifact transfer in Type 2 | Operational artifacts transfer to the new Halo; identity/governance artifacts stay with the original agent |
| Governance approval for Halo→Prime upgrade | Open — permissionless or governance-gated? |
| Reversibility of Type 2 | Open — can a Prime downgrade back to a Halo and reabsorb its subsidiary? |
| Guardian selection mechanism | Open — registry vs bilateral negotiation? |
| Guardian obligations under accord | Open — ongoing operational support or just creation trigger? |

---

## Related

- [`README.md`](lani/synomic-entities/README.md) — Rank hierarchy and entity index
- [`guardian.md`](guardian.md) — Ozone, the operational counterpart of Guardian Accords
- [`prime.md`](prime.md) — Synomic Entity Primitives and the Prime waiting period
- [`folio.md`](folio.md) — Folio auto-accord; entry point for new participants
- [`../growth-staking/growth-staking.md`](../growth-staking/growth-staking.md) — Growth-staking interaction with Type 1 Restructure
