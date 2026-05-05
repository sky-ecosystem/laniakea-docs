# Artifact Hierarchy

> Knowledge artifacts layered by scope and authority: synart (shared) > telart (per-teleonome) > embart (per-embodiment).

**Also known as:** synart/telart/embart, knowledge hierarchy, artifact mapping

## Definition

The artifact hierarchy defines how curated probabilistic knowledge is scoped across the five-layer architecture. Each artifact level combines layers and determines what knowledge an entity can access and how authoritative that knowledge is.

- **synart** (Layers 1+2) — Shared across all aligned entities. Contains the Synomic Library, axioms, governance rules, Atlas, and Language Intent configuration. Highest authority. Updates slowly through governance.
- **telart** (Layers 1+2+3) — Shared across all embodiments of a single teleonome. Includes everything in synart plus the teleonome's own library, dreamarts, and mission-specific knowledge.
- **embart** (Layers 1+2+3+4) — Local to a single embodiment. Includes everything in telart plus local observations, learned patterns, and embodiment-specific state.

Authority flows downward: synart > telart > embart. When in doubt, consult higher authority.

## Key Properties

- Higher-level knowledge is more authoritative but updates more slowly
- Lower-level knowledge is more contextual but less vetted
- synart is identical across all aligned entities (public, shared)
- telart is private to a teleonome but shared across its embodiments
- embart is private to a single embodiment
- Layer 5 produces only ephemeral context (runtime scratchpad, not persisted)
- Local Data (raw logs/observations in Layer 4) is distinct from embart (curated, queryable probabilistic knowledge)

## Relationships

- **derived-from:** [five-layer-architecture](five-layer-architecture.md) — artifact boundaries follow layer boundaries
- **implements:** [truth-values](truth-values.md) — all artifact levels carry (strength, confidence) weighted knowledge
- **constrains:** [retrieval-policy](retrieval-policy.md) — authority hierarchy in retrieval follows synart > telart > embart
