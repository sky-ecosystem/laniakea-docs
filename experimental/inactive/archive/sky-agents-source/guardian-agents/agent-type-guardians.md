# Guardians: Privileged Operation Agents

Guardians are Synomic Agents that perform privileged operations — entities that post collateral and execute critical functions with accountability. Guardians consolidate the former Facilitator (interpretation), Aligned Delegate (governance participation), and Executor (operations) roles into a single collateral-backed role.

---

## What Guardians Are

Guardians are operational Synomic Agents:

- **Privileged operations** — Can perform actions others cannot
- **Collateral backing** — Post escrow to guarantee performance
- **Slashing risk** — Face penalties for failures
- **Interpretation authority** — Core Guardians interpret Atlas and create binding precedents
- **Governance participation** — Core Guardians receive delegated SKY voting power

Guardians are the stewards of the system — they interpret its constitution, execute its operations, and guard its integrity.

---

## How Guardians Work

The Guardian model:

```
Guardian
    │
    ├── Posts collateral/escrow
    │
    ├── Receives authority to perform operations
    │
    ├── Interprets Atlas (Core Guardians)
    │
    ├── Executes privileged functions
    │
    └── Faces slashing if failures occur
```

**The accountability loop:**
1. Guardian posts collateral (skin in the game)
2. System grants execution authority
3. Guardian performs operations (and interpretation, if Core)
4. If failure: collateral slashed
5. If success: Guardian earns fees/rewards

---

## Guardian Types

Different Guardian roles in Sky:

| Guardian Type | Function | Risk |
|---------------|----------|------|
| **Core Guardians** | Interpret Atlas, oversee Operational Guardians, governance participation | Slashing for misinterpretation or misalignment |
| **Operational Guardians** | Perform routine privileged ops | Slashing for failures |

---

## Guardians vs Other Agents

**Guardians vs Primes:**
- Primes allocate capital; Guardians perform operations
- Primes are strategic; Guardians are operational
- Primes are permanent; Guardians are role-based

**Guardians vs Halos:**
- Halos wrap value; Guardians perform actions
- Halos can be passive; Guardians are active
- Halos proliferate; Guardians are specific roles

**Guardians vs Generators:**
- Generators create credit; Guardians execute operations
- Generators are foundational; Guardians are functional
- Generators are singular; Guardians are multiple per type

---

## Collateral and Slashing

The Guardian accountability model:

**Collateral:**
- Posted before receiving authority
- Proportional to operation risk
- Locked for duration of role
- Released on successful completion or role exit

**Slashing conditions:**
- Incorrect execution
- Failure to execute
- Delayed execution beyond tolerance
- Malicious behavior
- Bad faith interpretation (Core Guardians)

**Slashing severity:**
- Minor failures: partial slash
- Major failures: significant slash
- Malicious behavior: full slash + exclusion

---

## Guardian Lifecycle

**Registration:**
- Post required collateral
- Register for Guardian role
- Receive authority envelope
- Begin operations

**Operation:**
- Perform privileged functions
- Interpret Atlas and create precedents (Core Guardians)
- Maintain collateral levels
- Report and attest as required
- Earn execution fees

**Exit:**
- Complete pending operations
- Wait for challenge period
- Reclaim collateral (if no slashing)
- Deregister from role

---

## Guardians as Synomic Agents

Like all Synomic Agents, Guardians are woven into the Synome:

- **Public accountability** — Actions visible and auditable
- **Constrained authority** — Can only do what role permits
- **Collateral-backed** — Skin in the game ensures alignment
- **Part of the system** — Not external contractors, Synomic entities

Guardians demonstrate that trusted execution can exist in a trustless system — through collateral, slashing, and Synomic integration.

---

## Recovery Agent as Crisis Successor

When a Guardian collapses or is implicated in misconduct, the Core Council activates a **Recovery Agent** — a rank 1 crisis wrapper that takes over the affected agent tree (the Guardian's accordant Primes, their Halos, and all downstream positions). The Recovery Agent manages resolution: Guardian replacement, orderly wind-down, agent restructuring, or loss absorption.

The Guardian's collateral (ORC) is designed to cover the costs of this transition period. See [`../recovery-agents/agent-type-recovery.md`](../recovery-agents/agent-type-recovery.md) for the full Recovery Agent specification.

---

## Summary

1. Guardians perform privileged operations with collateral backing
2. They post escrow and face slashing for failures
3. Core Guardians interpret Atlas and participate in governance; Operational Guardians focus on execution
4. Accountability through skin in the game
5. Distinct from Primes (strategic), Halos (products), Generators (foundational)
6. Woven into the Synome with public accountability
7. Recovery Agents serve as crisis successors when Guardians collapse
