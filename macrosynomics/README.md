# Macrosynomics

System-level architecture for the Synome — the deontic skeleton: layers, entities, governance, authority, and action. Macrosynomics defines what the Synome IS and how power flows through it.

For the epistemic and security side (knowledge dynamics, the probabilistic mesh, retrieval policy, formal language research), see [`../synodoxics/`](../synodoxics/README.md). For the study of individual teleonomes, see [`../synoteleonomics/`](../synoteleonomics/README.md). For the teleological framework, see [`../hearth/`](../hearth/README.md).

---

## Reading Order

### Core Architecture

Start here for the structural foundation.

1. **[`synome-overview.md`](synome-overview.md)** — Entry point. Core idea, five layers, dual architecture, knowledge hierarchy. Read this first.
2. **[`synome-layers.md`](synome-layers.md)** — Full 5-layer specification. Components, relationships, artifact hierarchy (synart/telart/embart), structural invariants, permanent design choices. The architectural bedrock.
3. **[`atlas-synome-separation.md`](atlas-synome-separation.md)** — How the human-readable Atlas relates to the machine-readable Synome. Concrete examples from Sky (contract addresses, BEAM parameters, penalty schedules). Synomic Agent autonomy, escalation to human reasonableness, Mini-Atlas fractal pattern, verification model.

### Agents and Action

How entities exist and act within the architecture.

4. **[`synomic-agents.md`](synomic-agents.md)** — Synomic Agents as ledger-native entities. The spectrum from minimal Halos to mega capital allocators. Power through integration, joint-stock properties, autonomous lifeforms.
5. **[`beacon-framework.md`](beacon-framework.md)** — Beacon taxonomy (two-tier authority + I/O role under it). Sentinel formations as a high-authority action subclass, BEAM hierarchy (pBEAM/cBEAM/aBEAM), in-space calculation, lifecycle, naming conventions.

### Implementation

Connecting architecture to deployment.

6. **[`short-term-actuators.md`](short-term-actuators.md)** — Phase 1 teleonome-less beacons. Beacon set + Synome-MVP + evolution pathway toward full teleonome-based operation.

### Meta-Architectural Layering

Higher-level frame for thinking about how the synome stratifies and evolves.

7. **[`topology-layers.md`](topology-layers.md)** — Telos / axioms / topology / population stratification, plus the probmesh as transverse alignment-argument substrate. Sudo as the only path to change rigid layers; frames (canonical and shadow); comments as pre-probmesh content; phase deliverables as topology atom-sets.

---

## Dependency Graph

```
synome-overview
    │
    ▼
synome-layers
    │
    ├──► atlas-synome-separation
    │         │
    │         ▼
    ├──► synomic-agents
    │
    ├──► beacon-framework
    │
    ├──► short-term-actuators
    │         │
    │    (Phase 1 → full architecture)
    │
    └──► topology-layers
              │
         (meta-architecture: telos / axioms / topology / population)
```

---

## Relationship to Siblings

**[Synodoxics](../synodoxics/README.md)** defines the epistemic and security side — the probabilistic mesh, truth values, retrieval policy, cancer-logic, fractal security, and the synlang research track. Together, macrosynomics (structure) and synodoxics (knowledge) form the two halves of the [dual architecture](../core-concepts/dual-architecture.md).

**[Synoteleonomics](../synoteleonomics/README.md)** describes the entities that inhabit the structures defined here.

**[The Hearth](../hearth/README.md)** holds the system's telos point and high-level commitments.

Atomic concept definitions shared across all directories live in [`../core-concepts/`](../core-concepts/README.md). Narrative documents link to concept files for cross-references rather than re-explaining shared concepts.
