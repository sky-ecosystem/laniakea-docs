# RSI

> Recursive self-improvement — the system getting better at getting better. Two orthogonal axes: meta-depth (how recursive) and autonomy scope (how trusted to apply changes without supervision).

**Also known as:** recursive self-improvement, meta-learning, self-improvement

> **In lift vocabulary:** RSI is **lift learning to make better lift** — the recursive loop where the system grows reusable agency around the parts of itself that generate, allocate, test, adapt, compress, and reuse reusable agency. See [`../lift.md`](../lift.md) for the full vocabulary (ground, lift, false lift, meta-lift, opaque grounded primitives, lift the lifters).

## Definition

RSI is the process by which the Synome's knowledge bases actively improve at meta-level tasks — not just storing knowledge, but getting better at finding, using, and improving knowledge.

The recursive loop: embodiments use knowledge, discover patterns, outcomes feed back as evidence, the library analyzes what worked, pattern-mining strategies improve, better strategies yield better patterns. This loop runs at every artifact level: synart improves strategies that benefit all aligned entities, telart improves mission-specific strategies, embart proposes local optimizations upward.

## Two Orthogonal Axes

A given RSI capability has both a meta-depth and an autonomy scope. They measure different things; neither subsumes the other.

### Meta-Depth — how recursive

- **Level 0: Raw knowledge** — patterns, probabilities, evidence
- **Level 1: Using knowledge** — making decisions, executing tasks
- **Level 2: Strategies for pattern-mining** — how to effectively query and use knowledge
- **Level 3: Meta-strategies (RSI proper)** — getting better at finding better strategies (recursive)

### Autonomy Scope — what changes, with what gating

- **L1: Belief calibration** — strengths and confidences as evidence arrives. Zero risk; always on.
- **L2: Prediction calibration** — the system's own accuracy at predicting improvement deltas. Low risk; fully audited.
- **L3: Rule discovery** — new inference rules, regression-tested in staging. Moderate risk; implemented today via the Rule-Author Agent (see [`noemar-substrate.md`](../synodoxics/noemar-substrate.md)).
- **L4: Source rewriting** — the runtime's own source under a constrained patch vocabulary. High risk; gated on demonstrated L2 calibration above a fixed threshold.

A capability sits at one cell in the cross-product. The Rule-Author Agent operates at meta-depth Level 2 (improving pattern-mining strategies) and autonomy scope L3 (rule discovery with regression gating). A future dreamer formation evolving its own evaluative criteria operates at meta-depth Level 3 with autonomy scope L3 — same scope, deeper recursion. A pure belief-calibration ingest sits at meta-depth Level 0 with autonomy scope L1.

The synomic inertia spectrum applies to both axes: deeper meta-depth and higher autonomy scope both ossify more slowly and require more evidence to advance.

## Key Properties

- RSI is continuous — not a feature to add later, but core to how knowledge bases function
- Improvements discovered at lower layers can be proposed upward (embart → telart → synart)
- Constrained by ossification: RSI operates freely on speculative patterns, cannot touch axiomatic patterns
- The speed gradient (experiment freely at edges, change core slowly) is not imposed by policy — it emerges from evidence dynamics
- Dreaming (dreamarts in Layer 3) is where RSI runs safely: experimental embodiments try new strategies in simulation before real-world deployment
- RSI improves: pattern discovery, query optimization, relevance prediction, strategy evaluation, meta-learning

## Relationships

- **enabled-by:** [probabilistic-mesh](probabilistic-mesh.md) — the mesh is where RSI operates
- **constrained-by:** [ossification](ossification.md) — proven and axiomatic patterns resist RSI-driven changes
- **constrained-by:** [synomic-inertia](synomic-inertia.md) — inertia naturally throttles RSI speed
- **threatened-by:** [cancer-logic](cancer-logic.md) — RSI that bypasses governance to move faster is cancer-logic
- **implements:** [dreamer-actuator-split](dreamer-actuator-split.md) — dreamers explore strategy space safely; actuators test in reality
- **converges-with:** [rsi-risk-convergence](rsi-risk-convergence.md) — RSI and risk management are the same operation
