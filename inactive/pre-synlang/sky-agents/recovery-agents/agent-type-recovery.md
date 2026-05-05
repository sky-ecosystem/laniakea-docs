# Recovery Agents

**Status:** Draft concept
**Date:** February 2026

---

## Overview

Recovery Agents are rank 1 agents administered by the Core Council, activated in crisis scenarios when a Guardian collapses or is implicated in misconduct. A Recovery Agent takes over the affected agent tree — the Guardian's accordant Primes, their Halos, and all downstream positions — and manages the liquidation, restructuring, or wind-down process.

Recovery Agents are temporary by nature. They exist for the duration of the crisis, then dissolve once all affected agents have been resolved.

---

## Key Properties

| Property | Description |
|---|---|
| **Rank** | 1 — directly regulated by Core Council |
| **Administration** | Core Council (via SpellCore governance) |
| **Token issuance** | None — Recovery Agents are tokenless |
| **Governance tokens** | None |
| **Growth asset status** | Not a growth asset (excluded from Growth Staking) |
| **Creation** | By Core Council governance action in response to crisis |
| **Duration** | Temporary — dissolves after resolution |
| **Purpose** | Crisis wrapper for managing affected agent trees |

---

## Activation Triggers

A Recovery Agent is created when:

1. **Guardian collapse** — A Guardian becomes insolvent, is derecognized, or is otherwise unable to fulfill its accord obligations
2. **Guardian misconduct** — A Guardian is implicated in fraud, bad faith interpretation, or other violations that require immediate separation from the agents it oversees
3. **Systemic crisis** — Broader conditions require centralized crisis management of specific agent trees

---

## Scope of Authority

When activated, a Recovery Agent assumes operational control of:

- **The affected Guardian's accord relationships** — All Primes and other agents that were accordant to the collapsed Guardian
- **Downstream agents** — Halos and other rank 3 agents administered by affected Primes
- **Risk capital positions** — TEJRC, TISRC, and other risk capital associated with affected agents

The Recovery Agent operates within the same PAU infrastructure but with emergency authority granted by Core Council via SpellCore.

---

## Resolution Process

The Recovery Agent manages one or more of:

1. **Guardian replacement** — Transfer accord relationships to a healthy Guardian. Primes and Halos continue operating under new guardianship.
2. **Orderly wind-down** — Systematically unwind positions, redeem risk capital, and return assets to stakeholders.
3. **Agent restructuring** — Split, merge, or reconfigure affected agents to restore operational health.
4. **Loss absorption** — Invoke the loss absorption waterfall for any realized losses during the crisis.

---

## Relationship to Guardians

Recovery Agents are the crisis counterpart to Guardians:

| Dimension | Guardian | Recovery Agent |
|---|---|---|
| **Condition** | Normal operations | Crisis — Guardian collapsed or implicated |
| **Duration** | Ongoing | Temporary |
| **Authority source** | Collateral-backed accord | Core Council emergency action |
| **Purpose** | Stewardship and execution | Liquidation, restructuring, wind-down |

Guardians should anticipate the possibility of Recovery Agent activation — the Guardian's collateral (ORC) is designed to cover the costs of the transition period. See [Guardian Agents](../guardian-agents/agent-type-guardians.md) for details on collateral and slashing mechanics.

---

## Summary

1. Rank 1 agent, directly administered by Core Council
2. Tokenless — no governance tokens, no growth asset status
3. Crisis wrapper activated when a Guardian collapses or is implicated
4. Takes over the affected agent tree (Primes, Halos, risk capital)
5. Manages resolution: replacement, wind-down, restructuring, or loss absorption
6. Temporary by nature — dissolves after resolution
