# Sky Agents

Specifications for the seven Synomic Agent types in the Sky ecosystem, organized into a formal four-tier rank hierarchy. Each agent type serves a distinct role in the capital flow and governance structure, from foundational credit creation (Generator) through capital allocation (Primes) to product-level deployment (Halos), with operational stewardship by Guardians and crisis management by Recovery Agents.

This directory also covers the lifecycle mechanics — how agents are created and restructured.

## Agent Rank Hierarchy

Agents are organized into four ranks based on their governance relationship to the Core Council:

| Rank | Agent Types | Governance Relationship |
|---|---|---|
| **0** | Core Council | Sovereign — governs all other ranks |
| **1** | Guardians, Core Controlled Agents, Recovery Agents | Directly regulated by Core Council |
| **2** | Primes, Generators | Accordant to a Guardian |
| **3** | Halos, Folio Agents | Administered by a Prime, transitively accordant to that Prime's Guardian |

```
Rank 0: Core Council
    │
    ├── Rank 1: Guardians ──────────┐
    │                               │ (Guardian Accord)
    ├── Rank 1: Core Controlled     ├── Rank 2: Primes ──────┐
    │                               │                         │ (Prime administers)
    └── Rank 1: Recovery            └── Rank 2: Generators    ├── Rank 3: Halos
                                                              │
                                                              └── Rank 3: Folio Agents
```

## Agent Type Overview

| Agent Type | Rank | Role | Tokenized | Key Property |
|---|---|---|---|---|
| **Guardian** | 1 | Performs privileged operations | Yes | Accountable — collateral-backed with slashing |
| **Core Controlled** | 1 | Core Council operational vehicle | No | Legacy asset management + general-purpose |
| **Recovery** | 1 | Crisis wrapper for collapsed guardians | No | Temporary — dissolves after resolution |
| **Prime** | 2 | Allocates capital at scale | Yes | Heavyweight — billions under management |
| **Generator** | 2 | Creates credit medium (USDS, SGAs) | Yes | Foundational — all others depend on it |
| **Halo** | 3 | Wraps value into products | Yes | Flexible — from minimal to complex |
| **Folio Agent** | 3 | Standardized supply-side holding structure | No | Entry point — instant creation, principal + directive control |

## Subdirectories

| Directory | Description |
|---|---|
| [`guardian-agents/`](guardian-agents/) | Guardian specifications — privileged operation agents with collateral backing |
| [`core-controlled-agents/`](core-controlled-agents/) | Core Controlled Agent specifications — rank 1 Core Council operational vehicles |
| [`recovery-agents/`](recovery-agents/) | Recovery Agent specifications — rank 1 crisis wrappers |
| [`prime-agents/`](prime-agents/) | Prime specifications — heavyweight capital allocators (Spark, Grove, Keel, Obex) |
| [`generator-agents/`](generator-agents/) | Generator specifications — foundational agents that create the credit medium |
| [`halo-agents/`](halo-agents/) | Halo specifications — the fractal layer (Portfolio, Term, Trading, Exchange, Identity Network) |
| [`folio-agents/`](folio-agents/) | Folio Agent specifications — standardized supply-side holding structures with principal control |
| [`agent-creation-restructuring/`](agent-creation-restructuring/) | Agent creation and restructuring mechanics (Guardian Accord, Type 1/Type 2 restructures) |

## Related

- [`smart-contracts/architecture-overview.md`](../smart-contracts/architecture-overview.md) — Four-layer capital flow architecture that agents operate within
- [`synomics/macrosynomics/synomic-agents.md`](../synomics/macrosynomics/synomic-agents.md) — Theoretical framework for Synomic Agents
- [`synomics/macrosynomics/beacon-framework.md`](../synomics/macrosynomics/beacon-framework.md) — Beacon taxonomy through which agents are operated
- [`growth-staking/growth-staking.md`](../growth-staking/growth-staking.md) — Growth Staking mechanism linking governance to innovation investment
- [`roadmap/`](../roadmap/) — Phased deployment of agent infrastructure (factories in Phases 5-8)
