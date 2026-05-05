# Probabilistic Mesh

> The dense network of soft, informing connections that permeates the Synome — evidence, patterns, queries, and meta-information flowing through the system.

**Also known as:** the mesh, soft connections, probabilistic layer

## Definition

The probabilistic mesh is the dense, non-hierarchical network of soft connections overlaid on the sparse deontic skeleton. It carries evidence (observations flowing back from the world), patterns (regularities discovered in evidence, weighted by strength and confidence), queries (embodiments querying knowledge bases), and meta-information (which queries were useful, which patterns led to good outcomes).

The mesh is too dense to draw in architecture diagrams — essentially "everything can potentially inform everything else" within access constraints. Despite being non-hierarchical in structure, it has an authority hierarchy: synart knowledge is more authoritative than telart, which is more authoritative than embart. Embodiments are naturally incentivized to "look up" to higher-authority knowledge, as using synart-aligned patterns reduces risk of penalties and alignment drift.

## Key Properties

- Dense, multi-directional, constantly flowing and learning
- All knowledge in the mesh carries truth values: (strength, confidence) pairs
- Authority hierarchy within the mesh: synart > telart > embart
- Embodiments that reference synart probabilities are more likely to remain aligned
- The mesh enables alignment — by making synart knowledge highest-authority, embodiments are incentivized to align with it
- Access controls matter: embodiments access their own embart/telart/synart, not other teleonomes' telarts
- Caching and locality are natural: prefer local knowledge when sufficient, look up for important decisions

## Relationships

- **component-of:** [dual-architecture](dual-architecture.md) — the mesh is one half of the probabilistic-deontic architecture
- **implements:** [truth-values](truth-values.md) — all knowledge in the mesh carries (strength, confidence) pairs
- **enables:** [rsi](rsi.md) — the mesh is where recursive self-improvement operates
- **threatened-by:** [cancer-logic](cancer-logic.md) — overeager updates can corrupt the mesh
- **defended-by:** [ossification](ossification.md) — high-confidence patterns resist noise
