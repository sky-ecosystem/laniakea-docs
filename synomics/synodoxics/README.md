# Synodoxics

The study of synomic belief, knowledge dynamics, and how the Synome knows and learns. From *doxa* (belief) — synodoxics covers the probabilistic mesh, the security model that protects it, the retrieval policies that govern access to it, and the formal language research for representing it.

Where [macrosynomics](../macrosynomics/README.md) defines what the Synome IS (structure, entities, authority, governance), synodoxics defines what the Synome BELIEVES and how it learns — the epistemic and security half of the dual architecture.

**One-line gloss:** synodoxics is how you think as a shared brain, and how you individually think in a way that fully taps into the shared brain. The synodoxic mesh puts the meat on the macrosynomic skeleton, using governance gates (the [crystallization interface](../core-concepts/crystallization-interface.md)) to transition from probabilities to deontics.

**Design constraint on the axioms:** the core synodoxic commitments should be few, simple, and implementation-invariant — they must carry over regardless of language, hardware, model, embodiment, or how much of the system has been rewritten. Well-suited for constant vibe coding, self-rewrite, different hardware, different embodiments.

---

## Reading Order

### Core Epistemic Architecture

Start here for the knowledge dynamics.

1. **[`probabilistic-mesh.md`](probabilistic-mesh.md)** — The dense network of soft, informing connections overlaid on the deontic skeleton. Truth values (strength, confidence), crystallization interface, RSI levels, synomic inertia. The foundational document for synodoxics.
2. **[`retrieval-policy.md`](retrieval-policy.md)** — Invariants, principles, and degrees of freedom for querying the probabilistic mesh. Risk-gates-authority constraint.
3. **[`security-and-resources.md`](security-and-resources.md)** — Cancer-logic as the primary threat. Ossification as the solution. Resource discipline, defense in depth, the update problem, adversarial soft channels, fractal security pattern.

### Cognition

How the Synome actually thinks — the architectural commitments. For the practical mechanisms (live context, context manipulation, attention), see [`../neurosymbolic/`](../neurosymbolic/README.md).

4. **[`neuro-symbolic-cognition.md`](neuro-symbolic-cognition.md)** — Synlang as cognitive language, the symbolic-neural loop (emo), context as bottleneck. How the mesh gets used.
5. **[`noemar-substrate.md`](noemar-substrate.md)** — The synlang runtime: Space, PLN truth values, the protocol system, the epistemic cycle, the emo concretized as the Rule-Author Agent.

### Synlang

6. **[`synlang.md`](synlang.md)** — The language itself: S-expressions grounded in the synomic library. Settled questions and evolving surface conventions. (The earlier hypergraph/notation/extensions research track is resolved by Noemar's design — see `noemar-substrate.md`.)

---

## Dependency Graph

```
probabilistic-mesh
    ├──► retrieval-policy
    ├──► security-and-resources
    └──► neuro-symbolic-cognition ──► noemar-substrate
                                          │
                                          ▼
                                      ../neurosymbolic/ (practical mechanisms)

synlang ◄── noemar-substrate
(language) ◄── (runtime)
```

`noemar-substrate.md` grounds the abstract epistemic architecture in its concrete runtime. `synlang.md` describes the language; `noemar-substrate.md` describes what runs it.

---

## Relationship to Siblings

**[Macrosynomics](../macrosynomics/README.md)** defines structure: layers, agents, beacons, governance. Synodoxics defines knowledge: what the Synome believes, how it learns, how it protects itself. The two are the structural (deontic) and epistemic (probabilistic) halves of the [dual architecture](../core-concepts/dual-architecture.md).

**[Synoteleonomics](../synoteleonomics/README.md)** describes the entities that inhabit the structures macrosynomics defines and use the knowledge synodoxics governs. Teleonome memory, resilience, and economics all depend heavily on the probabilistic mesh and security model.

**[The Hearth](../hearth/README.md)** provides the purpose — the Hearth commitments that the security model ultimately protects.

Atomic concept definitions shared across all directories live in [`../core-concepts/`](../core-concepts/README.md).
