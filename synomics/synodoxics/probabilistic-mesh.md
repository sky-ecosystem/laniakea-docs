---
concepts:
  defines:
    - probabilistic-mesh
    - truth-values
    - ossification
    - synomic-inertia
    - rsi
    - crystallization-interface
  references:
    - dual-architecture
    - artifact-hierarchy
    - five-layer-architecture
    - dreamer-actuator-split
    - cancer-logic
---

# The Probabilistic Mesh

The dense network of soft, informing connections that permeates the entire Synome architecture, overlaid on the sparse deontic skeleton.

---

## Two Networks, One System

The Synome is a **[probabilistic-deontic architecture](../core-concepts/dual-architecture.md)** with two fundamentally different types of connections:

| | Deontic Skeleton | Probabilistic Mesh |
|---|---|---|
| **Nature** | Hard, deterministic, authoritative | Soft, weighted, informing |
| **Density** | Sparse (what we draw in diagrams) | Dense (permeates everything) |
| **Structure** | Hierarchical (layers, containment) | Non-hierarchical (everything can inform everything) |
| **Flow** | Top-down authority | Multi-directional evidence |
| **Change** | Requires governance to update | Constantly flowing, learning |
| **Purpose** | Load-bearing, must be followed | Decision support, pattern discovery |

The deontic skeleton is what we draw in architecture diagrams — the hard connections between layers. The probabilistic mesh is too dense to draw — it's essentially "everything can potentially inform everything else" within access constraints.

The table describes the endpoints of a spectrum, not two separate systems. Unannotated knowledge in the Synome carries an implicit (1,1) truth value — axiomatic, deontic. The skeleton IS the mesh: a plain knowledge graph with no truth value annotations is a valid Synome where everything is axiomatic. You soften parts of it by adding explicit truth values. The mesh grows outward from the skeleton as uncertainty gets expressed. Governance gates (the crystallization interface) work in both directions — hardening probabilistic patterns into (1,1) axioms, and softening axioms back to probabilistic status when governance decides they need re-evaluation.

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

> **Terminology note:** A synart is the full Layers 1+2 artifact — it contains both deontic (hard rules, axioms, governance) and probabilistic (knowledge, patterns, evidence) content. See [`synome-layers.md`](../macrosynomics/synome-layers.md) for the authoritative definition. The probabilistic mesh provides the L2 (probabilistic) component of synarts; the terms "synart/telart/embart" as used in this hierarchy refer to the curated probabilistic knowledge at each level — structured, queryable, with (strength, confidence) values. This is distinct from "Local Data" (raw logs/observations) and "ephemeral context" (runtime scratchpad).

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

## The Evidence Axiom

The evidence-counting method — observe outcomes, update positive and negative weights, derive (strength, confidence) — is itself a synomic axiom at (1,1). It is the one epistemological commitment not subject to revision. All other methods of arriving at truth values earn their legitimacy through this process.

Evidence dynamics govern not just knowledge truth values but also [attention allocation](../neurosymbolic/attention-allocation.md#evidence-dynamics-replace-artificial-economics). Attention patterns — which parts of the graph to load into context — are themselves mesh patterns with (strength, confidence). Patterns whose recommendations lead to good outcomes accumulate positive evidence; patterns that waste context tokens decay through non-reinforcement. This unifies knowledge management and attention management under a single epistemological mechanism.

### Fudge Methods

Other methods of setting truth values are permitted — LLM assertions, governance overrides, arbitrary injection. But they earn trust through the evidence method. If a fudge method's outputs consistently converge with what evidence-counting would eventually produce, that convergence pattern itself accumulates positive evidence, and the fudge method earns credibility. If its assertions keep getting contradicted, it loses credibility. Fudge methods are themselves patterns in the mesh, carrying their own truth values.

At bootstrap this matters: there is no evidence yet, so you must fudge. LLMs seed beliefs, humans inject priors. Those seeded values are explicitly provisional. The evidence process then validates or invalidates them.

Temporal evidence weighting — how to handle the relevance of old observations as the world changes — is itself a fudge method. Time-decay formulas, regime-sensitivity heuristics, and surprise detectors are not axiomatic. They earn trust by producing patterns that predict well, and lose trust when they don't. The evidence-counting axiom tells you HOW to ground knowledge; everything about WHICH evidence to weight how much is learned.

---

## Synomic Inertia

The truth value mechanism creates a natural property: **synomic inertia** — the system's resistance to change proportional to the evidence behind its current state. Patterns with high confidence require proportionally more counter-evidence to shift. This makes high-inertia patterns stable and trustworthy, while low-inertia patterns at the edges remain fluid and experimentable.

Inertia naturally throttles RSI: edge patterns evolve rapidly, core patterns evolve slowly. This gradient is not imposed by policy — it emerges from the evidence dynamics.

For the full treatment — including ossification levels, negative inertia, institutional credibility implications, and temporal stability across cosmic timescales — see [`security-and-resources.md`](security-and-resources.md#synomic-inertia).

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

### 6. Concurrent Access

Multiple emas read from the shared mesh concurrently. The mesh is the single source of truth; ema views are approximate, per-ema snapshots. Within a single inference turn, an ema reasons over a consistent snapshot (no mutations). Between turns, the symbolic system reconciles each ema's view with the live graph — classifying changes, patching or rebuilding context as needed. See [`live-graph-context.md`](../neurosymbolic/live-graph-context.md) for the concrete data model: snapshot isolation, between-turn reconciliation, and multi-ema consistency semantics.

---

## Connection to Dreaming

Dreamarts (Layer 3) are where the RSI loop can run safely:

- Spawn experimental embodiments
- Try new strategies in simulation
- Evaluate outcomes without real-world risk
- Successful experiments improve telart
- Potentially propose improvements to synart

Dreaming is how the system explores the strategy space safely before committing to deontic changes.

Dreamer workload splits into two categories. **Task-specific:** evolving strategies for particular problems the teleonome faces. **Generalizable infrastructure:** improving the epistemic machinery itself — evidence weighting methods, regime-change detectors, context assembly strategies, retrieval optimizations. The second category is often more valuable because it benefits everything the teleonome does, and successful generalizable discoveries are natural candidates for proposal upward to synart.

### The Validation Model

How is dreamer output validated? The answer is already implicit in the architecture:

**Continuous hypothesis testing IS the validation.** Dreamers produce hypotheses (strategies, patterns, models). Actuators test them in reality. Failures feed back as evidence, improving both the dreamart and future dreamer output. There is no separate validation step — the dreamer-actuator loop is itself a continuous validation engine.

**Not all output needs experimental validation.** Mathematical proofs, pattern discoveries in existing actuator data, and analytical insights can be verified against what's already known. A dreamer that finds a provable relationship in existing evidence has produced something valuable without needing a new experiment.

**Dreamart design is itself evolved.** The perturbations, scenarios, and noise that dreamarts inject into dreamer environments are not designed top-down — they are evolved through evolutionary logic. Try things, see what produces strategies that actually work when actuators deploy them in reality, iterate. Neural nets and high-probability patterns seed the exploration; evolutionary selection keeps what works.

**The bandwidth limiter is primarily defensive.** Dreamers and actuators exchange information at high bandwidth. The primary constraint on this exchange is defensive: dreamer infrastructure is extremely valuable (heavy embodiments, proprietary strategies, evolved dreamarts) and must be protected from exposure. The broader dreamer-actuator exchange is architecturally mediated through the telart layer, but the bandwidth limiter itself protects the dreamer's operational security.

For first-person perspectives, see [`../synoteleonomics/dreamer-perspective.md`](../synoteleonomics/dreamer-perspective.md) and [`../synoteleonomics/actuator-perspective.md`](../synoteleonomics/actuator-perspective.md).
