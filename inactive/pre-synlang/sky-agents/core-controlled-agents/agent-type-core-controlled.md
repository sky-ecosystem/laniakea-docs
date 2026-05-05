# Core Controlled Agents

**Status:** Draft concept
**Date:** February 2026

---

## Overview

Core Controlled Agents are rank 1 agents directly administered by the Core Council. They serve as general-purpose operational vehicles for the Core Council — managing assets and executing functions that don't fall under any Guardian, Prime, or Halo.

In the short term, Core Controlled Agents cover the functions previously handled by "Core Halos" — legacy protocol positions (Morpho vaults, Aave pools, SparkLend exposures, etc.) that need standardized management under Core Council governance. In the long term, Core Controlled Agents are a general-purpose mechanism for any operational need the Core Council identifies.

---

## Key Properties

| Property | Description |
|---|---|
| **Rank** | 1 — directly regulated by Core Council |
| **Administration** | Core Council (via SpellCore governance) |
| **Token issuance** | None — Core Controlled Agents are tokenless |
| **Governance tokens** | None |
| **Growth asset status** | Not a growth asset (excluded from Growth Staking) |
| **Creation** | By Core Council governance action |
| **Purpose** | Operational vehicle for Core Council functions |

---

## Legacy Asset Management

Core Controlled Agents provide a standardized wrapper for legacy protocol positions that are not yet operated by Primes:

- **Morpho vaults** — Protocol positions in Morpho lending markets
- **Aave pools** — Protocol positions in Aave lending markets
- **SparkLend exposures** — Direct protocol lending positions predating Prime operations
- **Other pre-existing allocations** — RWA positions or DeFi deployments from before the Agent framework

These positions are governed via artifacts maintained by Core Council. The Core Controlled Agent wraps them with the same risk framework and reporting standards as other agents in the system.

---

## Transition Paths

Core Controlled Agents managing legacy assets have two natural transition paths:

1. **Transfer to Prime ownership** — When a suitable Prime is identified, the assets and operational infrastructure can be transferred to a Prime, which then manages them through standard Halos (Portfolio, Term, or Trading).

2. **Systematic wind-down** — If the positions are no longer strategically aligned, the Core Controlled Agent provides an orderly framework for unwinding them.

---

## Relationship to Other Agent Types

Core Controlled Agents are distinct from all other agent types:

| Comparison | Core Controlled Agent | Other Type |
|---|---|---|
| vs. **Halo** | Administered by Core Council; tokenless; no Units or Books | Administered by a Prime; may issue tokens; has Class/Book/Unit structure |
| vs. **Prime** | Operational vehicle; no capital deployment primitives | Strategic capital deployer with Sky Agent Primitives |
| vs. **Recovery Agent** | Ongoing operations under normal conditions | Crisis wrapper activated when a guardian collapses |

---

## Summary

1. Rank 1 agent, directly administered by Core Council
2. Tokenless — no governance tokens, no growth asset status
3. Short-term: manages legacy protocol positions (replacing "Core Halos")
4. Long-term: general-purpose Core Council operational vehicle
5. Assets can transition to Prime ownership or wind down systematically
