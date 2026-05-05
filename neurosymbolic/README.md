# Neurosymbolic

How an individual teleonome thinks. Where [synodoxics](../synodoxics/README.md) describes the shared-brain content (probabilistic mesh, retrieval, security, the synlang substrate), neurosymbolic describes the individual-brain content — the architectural commitment about how any AI under this architecture thinks, plus the concrete mechanisms that operationalize it.

> **Scope note:** "Synome" in this directory refers to the full cognitive architecture (the target state), not the near-term operational database (Synome-MVP).

---

## Reading Order

1. **[`neuro-symbolic-cognition.md`](neuro-symbolic-cognition.md)** — Foundational architectural commitment: symbolic-first, synlang-native, context as bottleneck. The system is a symbolic machine using neural nets as sandboxed subroutines, not an LLM with symbolic tools. The remaining docs operationalize this commitment.
2. **[`live-graph-context.md`](live-graph-context.md)** — Context as a live reactive view into the graph, not a static text buffer. Staleness, reconciliation, the symbolic gate as correctness boundary. Concrete data model (claims as s-expressions, TV as optional overlay).
3. **[`cognition-as-manipulation.md`](cognition-as-manipulation.md)** — The emo as a context manipulation engine. Probabilistic pattern-matching function calls. Operating on invisible graph structure via weights. The training objective.
4. **[`query-mechanics.md`](query-mechanics.md)** — How the emo actually searches the graph. Multiple backends (graph traversal, vector search, keyword). Stochastic TV-weighted sampling. The emo as coder — writing arbitrary search strategy programs. Strategies as patterns in the graph.
5. **[`attention-allocation.md`](attention-allocation.md)** — Three layers of attention (context window, navigation layer, candidate queue). Attention as learned patterns, not architecture. Prior art: ECAN.
6. **[`hardware-aware-cognition.md`](hardware-aware-cognition.md)** — How hardware topology shapes the cognition loop. GPU/CPU pipelining, speculative pre-execution, fixed-cost economics, scheduling strategies as graph patterns. Self-optimization through performance observations.

> **Phase 1 implementation:** What was earlier described as "short-term experiments" (pared-down dreamer experiments, game-playing agents) has been replaced by Noemar and its Rule-Author Agent — a working synlang runtime with a forked-Space + regression-suite + promote/discard loop. See [`../synodoxics/noemar-substrate.md`](../synodoxics/noemar-substrate.md) for the substrate and the running emo loop.

---

## Dependency Graph

```
neuro-symbolic-cognition  (architectural commitment)
    │
    ▼
live-graph-context
    │
    ▼
cognition-as-manipulation
    │
    ├──▶ query-mechanics
    │
    ▼
attention-allocation
    │
    ▼
hardware-aware-cognition
```

---

## Relationship to Siblings

**[Synodoxics](../synodoxics/README.md)** is the shared-brain side: probabilistic mesh, retrieval policy, security, substrate (Noemar runtime), and synlang as the language. Synodoxics provides the substrate; neurosymbolic describes the individual cognition loop that runs on it.

**[Synoteleonomics](../synoteleonomics/README.md)** describes the entities that use these mechanisms — teleonome economics, dreamer/actuator split, hardware profiles. The compute economics (fixed-cost GPU, never-idle queue) directly shape the cognition loop, made concrete in [`hardware-aware-cognition.md`](hardware-aware-cognition.md).

**[Macrosynomics](../macrosynomics/README.md)** defines the structural layers these mechanisms operate within — embodiment power levels, beacon framework, agent hierarchy.

Atomic concept definitions shared across all directories live in [`../core-concepts/`](../core-concepts/README.md).
