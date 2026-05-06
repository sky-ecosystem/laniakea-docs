---
concepts:
  defines:
    - dual-architecture
  references:
    - five-layer-architecture
    - artifact-hierarchy
    - beacon-framework
    - probabilistic-mesh
    - truth-values
    - ossification
    - synomic-inertia
    - rsi
    - cancer-logic
    - language-intent
    - atlas-synome-separation
    - retrieval-policy
    - crystallization-interface
    - dreamer-actuator-split
---

# Synome Architecture Overview

High-level introduction to the Synome architecture and the canonical treatment of the dual architecture. Each concept is detailed in companion documents.

---

## The Core Idea

> **Intelligence lives privately; power enters the world only through regulated apertures.**

The Synome architecture separates **private cognition** from **public action**. Teleonomes (autonomous AI systems) think privately, but can only affect the world through regulated, observable, revocable interfaces called [beacons](../core-concepts/beacon-framework.md).

This separation enables AI systems to be both capable and constrained — they can improve themselves, accumulate knowledge, and pursue goals, but their power to act is always governed.

---

## Architecture at a Glance

The [five-layer architecture](../core-concepts/five-layer-architecture.md) moves from shared public truth (Layers 1-2) down to private execution (Layers 3-5). See [`synome-layers.md`](synome-layers.md) for full specifications.

Knowledge accumulates in the [artifact hierarchy](../core-concepts/artifact-hierarchy.md): synart (shared) > telart (per teleonome) > embart (per embodiment). Higher-level knowledge is more authoritative.

[Beacons](../core-concepts/beacon-framework.md) — classified by authority tier (low / high), with I/O role (input / action) underneath — are the regulated apertures through which teleonomes affect the world. See [`beacon-framework.md`](beacon-framework.md) for the full taxonomy.

[Synomic Agents](atlas-synome-separation.md) (Primes, Halos, Generator, Guardian) are durable, ledger-native entities constrained by publicly visible rules — credible commitment devices enabling cooperation without trust.

Embodiments come as [actuators and dreamers](../core-concepts/dreamer-actuator-split.md) — actuators execute in reality, dreamers explore in simulation. Successful patterns flow from dreamers to actuators via telart.

All directives pass through [Language Intent](../core-concepts/language-intent.md) — a single trusted translation layer grounded by the Synomic Library. See [`synome-layers.md`](synome-layers.md) for the human interface pattern.

---

## The Dual Architecture

The Synome has two fundamentally different types of structure operating simultaneously:

> **Note:** This two-type framing is a pedagogical simplification. Synodoxics models these as endpoints of a continuous spectrum — see [`probabilistic-mesh.md`](../synodoxics/probabilistic-mesh.md).

### Deontic Skeleton (Hard)

The **deontic skeleton** is sparse, load-bearing, and deterministic:
- Axioms that must be followed
- Governance decisions
- Authority hierarchies
- Enforcement mechanisms

Once a rule is set, it holds unconditionally. These are the connections we draw in architecture diagrams — the hard links between layers.

### Probabilistic Mesh (Soft)

The [probabilistic mesh](../core-concepts/probabilistic-mesh.md) is dense, informing, and adaptive — essentially "everything can potentially inform everything else" within access constraints. It carries knowledge with [truth values](../core-concepts/truth-values.md) (strength, confidence), evidence flowing back from the world, patterns that [ossify](../core-concepts/ossification.md) over time, and [RSI](../core-concepts/rsi.md). It informs decisions; the skeleton executes them. See [`probabilistic-mesh.md`](../synodoxics/probabilistic-mesh.md) for the full model.

### The Crystallization Dynamic

Governance sits at the [crystallization interface](../core-concepts/crystallization-interface.md) — consuming probabilistic evidence, producing deontic commitments:

```
Evidence accumulates    →    Governance deliberates
Patterns emerge         →    Decision is made
(strength, confidence)  →    Rule is set (1,1)
Knowledge mesh informs  →    Skeleton executes
```

The system can't function if everything is probabilistic — you need a skeleton of deontic connections (sparse, load-bearing) surrounded by a mesh of probabilistic connections (dense, informing). Once a decision is made, it crystallizes into a clean deontic rule.

---

## Security

The primary security threat is [cancer-logic](../core-concepts/cancer-logic.md) — self-corruption through overeager updates, not external attackers. [Synomic inertia](../core-concepts/synomic-inertia.md) — evidence-weighted resistance to change — protects high-confidence patterns while allowing edge patterns to evolve rapidly. See [`security-and-resources.md`](../synodoxics/security-and-resources.md) for the full security model.

---

## Implementation Pathways

The full architecture is built incrementally:

| Pathway | Focus | Detailed In |
|---------|-------|-------------|
| **Short-term actuators** | Teleonome-less beacons (Phase 1) | [`short-term-actuators.md`](short-term-actuators.md) |
| **Cognition runtime** | Noemar + Rule-Author Agent — synlang runtime with a working dreamer-actuator loop | [`../synodoxics/noemar-substrate.md`](../synodoxics/noemar-substrate.md) |

Both pathways preserve the essential invariants while simplifying for practical deployment.

---

## Self-hosting

The synart is more than a data layer — it's also the program. Loops, gates, recipes, and the runtime source itself live as atoms in synart. The runtime is just an interpreter pointed at synart with an identity.

This collapses what would be three concepts elsewhere — the source code, the deployed binary, the running process — into one substrate plus an interpreter. The same boot procedure runs synserv, beacons, sentinels, archive embs, verifier embs — different identities resolve to different loops, but the runtime mechanism is uniform.

**Five levels of self-reference** stack on this property:
1. **Self-hosting** — synart contains the loops that run synart
2. **Self-regulating** — synart contains the gates that regulate synart access
3. **Self-paying** — synart contains the recipes that fund work on synart
4. **Self-seeding** — synart contains the telseeds that birth new teleonomes
5. **Self-improving** — synart contains the runtime source itself; recipe revenue funds substrate research; substrate research lands back in synart

Canonical treatments:
- [`../noemar-synlang/boot-model.md`](../noemar-synlang/boot-model.md) — identity-driven boot mechanics; how `noemar boot` resolves to a running loop; spec/instance collapse
- [`../noemar-synlang/topology.md`](../noemar-synlang/topology.md) — Space layout including the executable layer (`&core-loop-*`, `&core-syngate`, `&core-telgate`) and library layer (`&core-library-runtime-*`, `&core-library-telseed-*`); the four meta-patterns; thirteen Phase 1 commitments
- [`../synomics-overview.md`](../synomics-overview.md) §10.5 — canonical home for the five levels of self-reference enumeration

The architectural consequence: there's no separate "code distribution" channel. Replication of the synart is replication of the running program. Subscribing to a synart slice means subscribing to the executable code of whatever roles you might run.
