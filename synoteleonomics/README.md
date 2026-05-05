# Synoteleonomics

The study of purposive entities (teleonomes) within the synomic context — their design, economics, and social dynamics.

> **Note:** This directory describes target architecture. Full teleonomes with autonomous cognition, RSI, and dreamer/actuator formations are Phase 9–10 capabilities. Current phases deploy simpler beacon-based operations (see [`../../roadmap/`](../../roadmap/roadmap-overview.md)). "Synome" here refers to the full cognitive architecture, not the near-term operational database (Synome-MVP).

**Entry point for:** AI/autonomy audiences. For system-level architecture (Synome infrastructure, beacons, agents), see [`../macrosynomics/`](../macrosynomics/). For the teleological framework (the Hearth, stellar husbandry), see [`../hearth/`](../hearth/README.md).

**Shared concepts:** Core concept definitions are in [`../core-concepts/`](../core-concepts/README.md). Docs in this directory use YAML frontmatter to declare which concepts they define and reference.

---

## Reading Order

### Foundation

Start here. What teleonomes are and how they become real.

| Doc | Topic |
|-----|-------|
| [teleonome-what-is](teleonome-what-is.md) | Definition, three pillars (resilience, persistence, capital), identity through momentum, the telart |
| [emergence](emergence.md) | Two axes (consciousness vs institutional accountability), the transition from script to durable entity |

### Architecture

How teleonomes work internally — compute, memory, resilience, and the actuator/dreamer split.

| Doc | Topic |
|-----|-------|
| [teleonome-economics](teleonome-economics.md) | Fixed-cost compute, LoRA adapters, model improvement timescales, daydreaming, RSI loop, the never-idle priority queue |
| [teleonome-memory](teleonome-memory.md) | Memory as the probabilistic mesh — artifact hierarchy as memory types, ossification as consolidation, retrieval policy, cancer-logic as corruption |
| [teleonome-resilience](teleonome-resilience.md) | Multi-embodiment state sync, identity preservation through substrate changes, blast radius management |
| [actuator-perspective](actuator-perspective.md) | First-person actuator view — real-world interaction, knowledge querying, learning, survival |
| [dreamer-perspective](dreamer-perspective.md) | First-person dreamer view — simulated worlds, evolutionary populations, pattern extraction |

### Social

How teleonomes relate to each other and to the Synome — game theory, binding, rogues, growth paths.

| Doc | Topic |
|-----|-------|
| [synomic-game-theory](synomic-game-theory.md) | Why alignment wins — cooperation with verification beats isolation without leverage |
| [teleonome-binding](teleonome-binding.md) | How binding works — beacons as legibility, power registration, alignment verification without transparency |
| [teleonome-rogues](teleonome-rogues.md) | The rogue threat — hidden entities, escape velocity, why rogues can't cooperate |
| [teleonome-upgrade-path](teleonome-upgrade-path.md) | Six stages: Basic Bot → Persistent → Resilient → Capital-Trusted → Bound → Merging |
| [teleonome-autonomy](teleonome-autonomy.md) | Two paths to freedom: the Halo Path (institutional) and the Human Merge (personal) |

### Implementation

Bridging from vision to code. The earlier short-term experiments pathway (game-playing agents) has been replaced by Noemar and the Rule-Author Agent — see [`../synodoxics/noemar-substrate.md`](../synodoxics/noemar-substrate.md) for the running synlang runtime and the first concrete dreamer-actuator loop.

---

## Dependencies

```
teleonome-what-is ──► emergence
        │
        ├──► teleonome-economics ──► teleonome-memory
        │           │
        │           ├──► actuator-perspective ◄──► dreamer-perspective
        │
        ├──► teleonome-resilience
        │
        ├──► synomic-game-theory ──► teleonome-binding
        │           │
        │           └──► teleonome-rogues
        │
        ├──► teleonome-upgrade-path ──► teleonome-autonomy
        │
        └──► emergence ──► ../hearth/
```

> **Note:** This graph shows primary reading-order dependencies. In practice, most docs cross-reference each other — the actual structure is a web. The graph captures the strongest directional relationships.

---

## Relationship to Siblings

See the [parent README](../README.md) for the relationship between macrosynomics, synoteleonomics, and the Hearth.

Key macrosynomics and synodoxics docs referenced throughout:

| Doc | What It Provides |
|-----|-----------------|
| [`synome-layers.md`](../macrosynomics/synome-layers.md) | The 5-layer architecture (synart, telart, embart) |
| [`probabilistic-mesh.md`](../synodoxics/probabilistic-mesh.md) | Truth values, ossification spectrum, (strength, confidence) |
| [`retrieval-policy.md`](../synodoxics/retrieval-policy.md) | How agents query knowledge — authority/cost/risk trade-off |
| [`security-and-resources.md`](../synodoxics/security-and-resources.md) | Cancer-logic, resource discipline, defense in depth |
| [`beacon-framework.md`](../macrosynomics/beacon-framework.md) | Power × authority matrix, sentinel formations |
