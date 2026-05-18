# Council Beacon and BEAM Authority

How the Core Council controls all operational authority in the post-transition system through the Council Beacon, aBEAMs, and Synome write rights.

---

## Overview

The Council Beacon is the root of all operational authority. It is an HPHA (High Power, High Authority) beacon operated by the Core Council. Through SpellCore spells, the Council Beacon sets aBEAMs, which in turn control all other BEAM types. The Council Beacon also governs all Synome write rights.

```
SpellCore (16/24 Core Council Guardian hat)
    │
    ▼
Council Beacon (HPHA)
    │
    ├── Sets aBEAMs (admin BEAMs)
    │       │
    │       ├── aBEAMs grant cBEAMs (configurator BEAMs)
    │       │       │
    │       │       └── cBEAMs set pBEAMs (process BEAMs)
    │       │               │
    │       │               └── pBEAMs execute on PAUs
    │       │
    │       └── aBEAMs register PAUs, approve inits
    │
    ├── Sets all Synome write rights
    │
    └── Can override all BEAM ownership
```

---

## Council Beacon

| Property | Value |
|----------|-------|
| Beacon type | HPHA (High Power, High Authority) |
| Operator | Core Council (24 Guardians) |
| Set by | SpellCore spells |
| Authority | Root of all BEAM and Synome write authority |

The Council Beacon is the single point from which all downstream authority flows. It is set and modified exclusively through SpellCore spells (requiring the 16/24 Guardian hat). This means modifying the Council Beacon requires the same governance process as any other core spell.

---

## BEAM Hierarchy

BEAMs (Bounded External Access Modules) are on-chain authorized roles. The Council Beacon controls the top of the hierarchy; authority cascades downward.

### Authority Cascade

| Level | BEAM Type | Set By | Capabilities |
|-------|-----------|--------|-------------|
| **1** | Council Beacon | SpellCore | Sets aBEAMs, overrides all BEAM ownership, sets Synome write rights |
| **2** | aBEAM (Admin) | Council Beacon | Registers PAUs, approves inits, grants cBEAMs; additions timelocked (14 days), removals instant |
| **3** | cBEAM (Configurator) | aBEAM | Sets rate limits (within SORL), executes approved controller actions, manages relayer/freezer |
| **4** | pBEAM (Process) | cBEAM | Direct execution on PAUs — calls Controller functions, moves capital within rate limits |

### How Authority Flows

1. **SpellCore** sets the **Council Beacon** via core spells
2. **Council Beacon** grants **aBEAMs** to administrative entities (currently Core Council members via the Configurator Unit)
3. **aBEAM** holders grant **cBEAMs** to GovOps teams, making them accordant to specific PAUs (via BEAMTimeLock, 14-day delay)
4. **cBEAM** holders (accordant GovOps) set **pBEAMs** by configuring relayers and operational parameters for their PAUs
5. **pBEAM** holders execute operations on PAUs within rate limits

### BEAM Override

SpellCore can override all forms of BEAM ownership at any level. This means the Core Council can:
- Revoke any aBEAM, cBEAM, or pBEAM
- Reassign BEAM ownership
- Bypass the normal cascade in emergencies

This override power is subject to the same 16/24 hat threshold and SKY holder freeze/override as any other SpellCore spell.

---

## Synome Write Rights

The Council Beacon is the root authority for all Synome write access. No entity can write to the Synome without authority that traces back to the Council Beacon.

| Write Right | Granted By | Used For |
|-------------|-----------|----------|
| Agent Artifact updates | Council Beacon → aBEAM | Modifying governance documentation for Primes, Halos, Generators, Guardians |
| Parameter updates | Council Beacon → aBEAM → cBEAM | Rate limits, init configurations, operational parameters |
| Role registry | Council Beacon | Guardian registration, role assignment |
| Precedent creation | Council Beacon → Core Guardians | Guardian Action Precedents (governance interpretations) |
| Beacon registration | Council Beacon → aBEAM | Registering new beacons in the Synome |
| Transaction logs | Council Beacon → cBEAM → pBEAM | Operational transaction records |

**Implication:** If the Council Beacon is frozen or the Core Council is dismissed via SKY override, Synome write access halts until governance is restored (either through direct SKY holder control or a new Core Council).

---

## Freeze/Cancel on BEAMs

### Individual CC Guardian Freeze/Cancel

Any single Core Council Guardian can freeze or cancel **any BEAM** across the entire system. This is a powerful emergency brake — one person can shut down all operational authority.

| Property | Value |
|----------|-------|
| Who | Any single CC Guardian |
| Scope | All BEAMs (aBEAM, cBEAM, pBEAM) |
| Effect | Immediate freeze/cancel of the targeted BEAM |
| Purpose | Emergency response — halt compromised or rogue operations instantly |

### SKY Holder Freeze/Cancel

SKY token holders also have freeze/cancel authority on all BEAMs, providing a second independent emergency brake outside the Core Council.

| Property | Value |
|----------|-------|
| Who | SKY token holders |
| Scope | All BEAMs |
| Mechanism | Same graduated response as SpellCore freeze (minority freeze → escalation) |

### Anti-Paralysis: Mutual Freeze/Cancel Among CC Guardians

The individual freeze/cancel power creates a paralysis risk: a rogue Guardian could freeze everything and hold the system hostage. The anti-paralysis mechanism addresses this.

| Property | Value |
|----------|-------|
| Mechanism | CC Guardians can freeze/cancel each other |
| Quorum | 2/3rds of the Core Council (16 of 24) |
| Effect | Removes the targeted Guardian's freeze/cancel ability |

**Attack and response scenario:**

```
1. Rogue Guardian freezes all BEAMs (paralysis attack)
              │
              ▼
2. Remaining CC Guardians coordinate
              │
              ▼
3. 16/24 vote to remove rogue Guardian
              │
              ▼
4. Rogue Guardian's freeze/cancel authority revoked
              │
              ▼
5. BEAMs unfrozen, operations resume
```

**Design rationale:** The threshold to halt (any single Guardian) is deliberately much lower than the threshold to act (16/24 for spells) or to remove a blocker (16/24 to kick). This asymmetry favors safety — it is always easier to stop the system than to do damage.

---

## Relationship to Current System

| Aspect | Current | Post-Transition |
|--------|---------|-----------------|
| aBEAM holder | Core Council (via Configurator Unit) | Council Beacon (set by SpellCore) |
| aBEAM scope | PAU registration, init approval, cBEAM grants | Same + Synome write rights + BEAM override |
| cBEAM granting | aBEAM via BEAMTimeLock (14-day delay) | Same mechanism, unchanged |
| BEAM override | Not formalized | SpellCore can override all BEAM ownership |
| Freeze authority | BEAMTimeLock pause (aBEAM holders) | Individual CC Guardian + SKY holders on all BEAMs |
| Anti-paralysis | Not formalized | 2/3rds CC mutual freeze/cancel |
| Synome write root | Governance spells | Council Beacon |

---

## Related Documents

- [spellguard-system.md](spellguard-system.md) — SpellCore and SpellGuard mechanics
- [Beacon Framework](../synomics/macrosynomics/beacon-framework.md) — Beacon taxonomy and BEAM hierarchy
- [Configurator Unit](../smart-contracts/configurator-unit.md) — Current aBEAM/cBEAM mechanics and contract interfaces
- [target-model.md](target-model.md) — Consolidated Guardian role that populates the Core Council
