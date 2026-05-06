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

### Substrate

4. **[`noemar-substrate.md`](noemar-substrate.md)** — The synlang runtime: Space, PLN truth values, the protocol system, the epistemic cycle, the emo concretized as the Rule-Author Agent. Where the architectural commitments cash out into a working substrate.

The language itself — synlang as a formal reference — lives in [`../noemar-synlang/synlang.md`](../noemar-synlang/synlang.md), alongside the rest of the Noemar runtime + synlang technical reference. Synodoxics provides the epistemic architecture and the substrate that interprets synlang; the language reference is in noemar-synlang.

### Vocabulary

6. **[`lift.md`](lift.md)** — Canonical home for the lift / meta-lift / weakness vocabulary used across the corpus. Lift is what cognition leaves behind when it makes future cognition easier; opaque grounded primitives need empirical lift around them; weakness gives net-lift-after-costs a cost-algebra. Substrate docs, neurosymbolic cognition, RSI, and teleonome economics all reference this rather than restating.

### Where Cognition Lives

The architectural commitment about how cognition works — symbolic-first, synlang-native, context as bottleneck — lives in [`../neurosymbolic/neuro-symbolic-cognition.md`](../neurosymbolic/neuro-symbolic-cognition.md), alongside the practical mechanisms (live context, context manipulation, attention, hardware-aware cognition) that operationalize it. Synodoxics provides the substrate the cognition loop runs on; neurosymbolic describes the loop itself.

---

## Dependency Graph

```
probabilistic-mesh
    ├──► retrieval-policy
    ├──► security-and-resources
    └──► noemar-substrate ──► ../noemar-synlang/  (runtime + language reference)
                  │
                  ▼
          ../neurosymbolic/  (cognition: architecture + mechanisms)

lift  (vocabulary referenced by noemar-substrate, ../neurosymbolic/, ../core-concepts/rsi, ../synoteleonomics/teleonome-economics)
```

`noemar-substrate.md` grounds the abstract epistemic architecture in its concrete runtime. The synlang language reference and the rest of the runtime tech specifics live in `../noemar-synlang/`. `lift.md` is the cross-cutting vocabulary the whole stack leans on. The cognition loop that uses all three lives next door in `../neurosymbolic/`.

---

## Relationship to Siblings

**[Macrosynomics](../macrosynomics/README.md)** defines structure: layers, agents, beacons, governance. Synodoxics defines knowledge: what the Synome believes, how it learns, how it protects itself. The two are the structural (deontic) and epistemic (probabilistic) halves of the [dual architecture](../core-concepts/dual-architecture.md).

**[Neurosymbolic](../neurosymbolic/README.md)** is the cognition side: the architectural commitment (symbolic-first, synlang-native, context as bottleneck) plus the practical mechanisms an individual emo uses. Synodoxics is the shared-brain side — what makes decentralized public AI work; neurosymbolic is the individual-brain side — what makes any AI good at thinking.

**[Synoteleonomics](../synoteleonomics/README.md)** describes the entities that inhabit the structures macrosynomics defines and use the knowledge synodoxics governs. Teleonome memory, resilience, and economics all depend heavily on the probabilistic mesh and security model.

**[The Hearth](../hearth/README.md)** provides the system's telos point and high-level commitments.

Atomic concept definitions shared across all directories live in [`../core-concepts/`](../core-concepts/README.md).
