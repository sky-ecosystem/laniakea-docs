# The Probabilistic Mesh

**Status:** Speculative / architectural concept
**Last Updated:** 2026-02-03

This document describes the probabilistic mesh — the dense network of soft, informing connections that permeates the entire Synome architecture, overlaid on the sparse deontic skeleton.

---

## Two Networks, One System

The Synome is a **probabilistic-deontic architecture** with two fundamentally different types of connections:

| | Deontic Skeleton | Probabilistic Mesh |
|---|---|---|
| **Nature** | Hard, deterministic, authoritative | Soft, weighted, informing |
| **Density** | Sparse (what we draw in diagrams) | Dense (permeates everything) |
| **Structure** | Hierarchical (layers, containment) | Non-hierarchical (everything can inform everything) |
| **Flow** | Top-down authority | Multi-directional evidence |
| **Change** | Requires governance to update | Constantly flowing, learning |
| **Purpose** | Load-bearing, must be followed | Decision support, pattern discovery |

The deontic skeleton is what we draw in architecture diagrams — the hard connections between layers.

The probabilistic mesh is too dense to draw — it's essentially "everything can potentially inform everything else" within access constraints.

---

## Authority Within the Mesh

Even within the probabilistic mesh, there's a hierarchy of authority:

```
synart ────────────── Highest authority (governance-vetted, alignment-safe)
    │
    ▼
telart ────────────── Mission-specific (derived from synart)
    │
    ▼
embart ────────────── Local observations (least vetted, most contextual)
```

> **Terminology note:** "synart/telart/embart" refer to the curated probabilistic knowledge at each level — structured, queryable, with (strength, confidence) values. This is distinct from "Local Data" (raw logs/observations) and "ephemeral context" (runtime scratchpad). See `synome-layers.md` for definitions.

**When an embodiment makes a decision, it can reference:**

1. **Local probabilities (embart)** — Fast, contextual, but least authoritative
2. **Teleonome probabilities (telart)** — Mission-aligned, more vetted
3. **Synomic probabilities (synart)** — Highest authority, most alignment-safe

**Why higher-level probabilities have more authority:**
- More thoroughly vetted by governance
- Derived from Atlas chain (alignment guarantee)
- Using them reduces risk of penalties
- More likely to be correct long-term
- Better for avoiding drift

**The incentive structure:**
Embodiments are naturally incentivized to "look up" to higher-authority knowledge sources when making decisions. Using only local reasoning is riskier — it might drift from alignment and trigger penalties.

---

## What Flows Through the Mesh

The probabilistic mesh carries:

### Evidence
- Observations from the World flowing back to Libraries
- Outcomes of decisions feeding back as data
- Sensor data, metrics, measurements

### Patterns
- Regularities discovered in evidence
- Correlations, causal models, predictive patterns
- (strength, confidence) weighted by evidence

### Queries
- Embodiments querying knowledge bases
- Pattern-matching requests
- Similarity searches

### Meta-information
- What queries were useful
- Which patterns led to good outcomes
- Strategy effectiveness data

---

## The Crystallization Interface

Governance sits at the interface between probabilistic and deontic:

```
┌─────────────────────────────────────────────────────────────┐
│                    PROBABILISTIC MESH                        │
│                                                             │
│   Evidence, patterns, queries, meta-information             │
│   Flowing constantly, multi-directional                     │
│   (strength, confidence) weighted                           │
│                                                             │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │      GOVERNANCE       │
              │                       │
              │  - Deliberates        │
              │  - Weighs evidence    │
              │  - Makes decisions    │
              │  - Sets rules         │
              │                       │
              └───────────┬───────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    DEONTIC SKELETON                          │
│                                                             │
│   Axioms, Directives, instantiation, control                │
│   Hard, authoritative, (1,1) truth value                    │
│   Must be followed                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Governance consumes** probabilistic evidence, patterns, recommendations.
**Governance produces** deontic commitments, rules, decisions.

Once crystallized, decisions are clean and deterministic — the system couldn't function otherwise.

---

## RSI: Recursive Self-Improvement

The synart and telart knowledge bases don't just store knowledge — they actively improve at **meta-level** tasks.

### The Levels

```
Level 0: Raw knowledge
         (patterns, probabilities, evidence)
              │
              ▼
Level 1: Using knowledge
         (making decisions, executing tasks)
              │
              ▼
Level 2: Strategies for pattern-mining
         (how to effectively query and use knowledge)
              │
              ▼
Level 3: Meta-strategies (RSI)
         (getting better at finding better strategies)
              │
              └──────── recursive ────────┘
```

### What RSI Improves

The synart and telart recursively improve at:

- **Pattern discovery** — Finding useful regularities in accumulated evidence
- **Query optimization** — Developing better search and retrieval strategies
- **Relevance prediction** — Anticipating what knowledge embodiments will need
- **Strategy evaluation** — Assessing which approaches lead to good outcomes
- **Meta-learning** — Learning how to learn more effectively

### The RSI Loop

```
Embodiment uses synart/telart
        │
        ▼
Discovers patterns, makes decisions
        │
        ▼
Outcomes feed back as evidence
        │
        ▼
Library analyzes what worked
        │
        ▼
Pattern-mining strategies improve
        │
        ▼
Better strategies → better patterns → better decisions
        │
        └──────────── recursive ────────────┘
```

### RSI Across Layers

| Layer | RSI Focus |
|-------|-----------|
| **synart** | Improving strategies that benefit all aligned entities |
| **telart** | Improving strategies specific to this teleonome's mission |
| **embart** | Local optimizations (may propose improvements to telart) |

Improvements discovered at lower layers can be proposed upward:
- embart discovers useful pattern → proposes to telart
- telart validates and incorporates → may propose to synart
- synart governance reviews → if general, becomes canonical

---

## Implications for Design

### 1. The Mesh is Implicit, Not Drawn

Architecture diagrams show the deontic skeleton. The probabilistic mesh is assumed — any node can potentially query any knowledge base it has access to.

### 2. Access Controls Matter

Not everything should connect to everything. The mesh operates within constraints:
- Embodiments access their embart, telart, synart (not other teleonomes' telarts)
- Queries flow up the authority hierarchy (embart → telart → synart)
- Evidence flows down and up (World → all layers that should know)

### 3. Caching and Locality

High-authority synart queries may be expensive. Systems will naturally:
- Cache frequently-used synart patterns locally
- Prefer local (embart) knowledge when sufficient
- "Look up" to synart for important/uncertain decisions

### 4. The Mesh Enables Alignment

By making synart knowledge highest-authority, embodiments are incentivized to align with it. The mesh isn't just information flow — it's an alignment mechanism.

### 5. RSI is Continuous

The system is always improving its ability to improve. This isn't a feature to add later — it's core to how the knowledge bases function.

---

## Connection to Dreaming

Dreamarts (Layer 3) are where the RSI loop can run safely:

- Spawn experimental embodiments
- Try new strategies in simulation
- Evaluate outcomes without real-world risk
- Successful experiments improve telart
- Potentially propose improvements to synart

Dreaming is how the system explores the strategy space safely before committing to deontic changes.

---

## Summary

| Concept | Description |
|---------|-------------|
| **Probabilistic mesh** | Dense network of soft, informing connections overlaid on deontic skeleton |
| **Authority hierarchy** | synart > telart > embart for probabilistic knowledge |
| **Crystallization** | Governance converts probabilistic evidence into deontic rules |
| **RSI** | Knowledge bases recursively improve their pattern-mining strategies |
| **Meta-learning** | Getting better at getting better at finding useful patterns |
| **Alignment incentive** | Higher-authority knowledge = safer = embodiments naturally look up |

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| `synome-layers.md` | The 5-layer architecture and artifact hierarchy (synart, telart, embart) |
| `retrieval-policy.md` | Invariants for querying the probabilistic mesh |
| `security-and-resources.md` | The update problem — how ossification prevents self-corruption |
| `dreamer-perspective.md` | How dreamers use the mesh for exploration and RSI |
| `actuator-perspective.md` | How actuators use the mesh for decision-making |
| `short-term-experiments.md` | Phase 1 dreamer implementation pathway |
