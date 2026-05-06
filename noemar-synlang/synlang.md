---
concepts:
  references:
    - probabilistic-mesh
    - truth-values
    - noemar-substrate
---

# Synlang

Synlang is the formal language the Synome uses for knowledge representation, reasoning, and cognition. The earlier research track explored hypergraph alternatives, notation options, and probabilistic extensions; those questions are resolved.

For the runtime that executes synlang — pattern matching, query resolution, belief propagation, multi-modal reasoning — see [`noemar-substrate.md`](../synodoxics/noemar-substrate.md). This doc covers the language itself.

---

## What Synlang Is

S-expressions grounded in the synomic library. The same format Lisp pioneered, with the synomic library providing the symbol vocabulary that makes expressions meaningful.

```
(= (croaks Fritz) True)
(= (frog $x) (and (croaks $x) (eats_flies $x)))
(allocation Generator (to Spark 40) (to Grove 30) (to Keel 30))
```

Three commitments are load-bearing:

- **Homoiconicity** — code = data = knowledge = reasoning traces. Self-modification operates on one data structure at every level.
- **Compositionality** — n-ary structures nest naturally without reification. A multi-party allocation is one expression, not a triple-store workaround.
- **Synomic-library grounding** — symbols draw their meaning from the shared synomic library, not from per-document declarations.

Together these enable the [neuro-symbolic cognition](../neurosymbolic/neuro-symbolic-cognition.md) loop: neural nets train synlang-native (synlang in, synlang out, halluci-reasoning in synlang), eliminating translation overhead at every boundary.

---

## What Got Resolved

The earlier research track explored questions that Noemar's design has now settled:

| Question | Resolution |
|---|---|
| Hypergraph language vs alternatives | S-expressions with n-ary heads as natural hyperedges |
| Notation (Prolog-style, RDF, property graphs, JSON-LD, custom) | S-expressions |
| Probabilistic logic (ProbLog, Bayesian nets, MLNs, neural-symbolic) | PLN truth values with the delta method |
| Pattern matching at scale | Inverted-index dispatch + one-way matching + Robinson unification; stochastic TV-weighted traversal for graph-style queries |

See [`noemar-substrate.md`](../synodoxics/noemar-substrate.md) for what the runtime does with these decisions, and [`neuro-symbolic-cognition.md`](../neurosymbolic/neuro-symbolic-cognition.md) for why synlang-native cognition is load-bearing.

---

## What's Still Being Designed

At the language level, several conventions are still evolving with usage:

- **Surface conventions for common patterns** — rule shorthand, belief annotation, query DSLs. Bracket notation is fixed; idiomatic synlang is being shaped by writing it.
- **Schema and type systems** — gradual typing seems likely; specifics depend on what the synomic library actually needs to enforce.
- **Versioning** — how synlang itself evolves, how older expressions stay valid as the language grows.
- **Macro and surface-syntax compilation** — whether higher-level forms compile down to canonical s-expressions, and how strictly canonical form is enforced for storage vs human authoring.

These are open in the way language-design questions are open after a language ships — refined through use, not blocking the runtime.
