---
concepts:
  references:
    - probabilistic-mesh
    - truth-values
    - rsi
    - dreamer-actuator-split
    - ossification
---

# Cognition as Context Manipulation

From the inside, cognition looks like this: the emo stares at a large array of s-expressions — its rendered view of the [live graph](live-graph-context.md), concretely Noemar's Space. It has an objective. Its entire cognitive activity is **surgically manipulating that array** — loading, dropping, querying, transforming s-expressions — to build the strongest possible justified case for an action. Reasoning and context management are the same activity.

The first running instance of this loop is the **Rule-Author Agent** described in [`../synodoxics/noemar-substrate.md`](../synodoxics/noemar-substrate.md): an LLM-driven emo that proposes synlang rules, stages them in a forked Space, runs regression queries, and decides whether to promote. The CONSULT/MUTATE/FINALIZE call pattern is this loop's operational form today; what scales up at higher embodiment power levels is the size and capability of the proposing component, not the loop structure.

---

## The Core Loop

The emo doesn't reason in natural language and then act on the graph. The thinking IS the graph manipulation:

1. Start with current context (rendered s-expressions)
2. Evaluate: does this context justify an action toward the objective?
3. If not: emit function calls that modify the context — load new patterns, drop irrelevant ones, query specific graph regions, zoom in on promising evidence
4. Observe the result — the context changed, maybe not exactly as expected
5. Repeat until context maximally justifies an action, or until the evidence shows no action is justified
6. Emit the action proposal → symbolic gate verifies against the live graph → action proceeds or gets bounced

Each turn, the emo emits a small number of pattern-matching function calls. Each call is compact (tens of tokens). Each call potentially reshapes thousands of tokens of context. The skill is efficiency — how few operations to converge on maximally justified confidence.

---

## Probabilistic Pattern-Matching Function Calls

The emo manipulates context through **function calls that pattern-match against the s-expression graph.** This is where the leverage comes from.

### The 10:10000 Ratio

Because context is structured s-expressions, a compact pattern can match and modify a vast region:

```
(drop (domain finance) (confidence < 0.3) (age > 30d))
```

~10 tokens. Matches and removes potentially thousands of tokens of stale low-confidence finance patterns from context. With flat natural language, you'd have to enumerate what to remove token by token. With structured s-expressions, a pattern carves out a region.

```
(load (related-to credit-spreads) (strength > 0.6) (depth 2))
```

Pulls in a subgraph of strong credit-spread-related patterns with two levels of connections. A few tokens of pattern → thousands of tokens of relevant context loaded.

The deterministic examples above are the simplified picture. The full query mechanics — stochastic traversal, multiple search backends, NN-authored strategy programs — are in [`query-mechanics.md`](query-mechanics.md). What follows here is the principle; that document makes it concrete.

### The Fourier Transformation Metaphor

The emo operates in **pattern space** rather than token space. Like a fourier transformation: decompose the context into structural patterns, identify which signals matter for the decision, amplify the relevant ones, filter the noise. Each operation transforms the context at the structural level. The s-expression structure is what makes this possible — it provides the "frequency domain" for context manipulation.

### Imprecision Is Fine

Pattern matching is probabilistic. Each turn:
- The pattern might **over-match** — accidentally dropping something useful
- The pattern might **under-match** — missing patterns you wanted to catch
- The match might hit **differently than expected** — the graph structure wasn't quite what the emo's weights predicted

None of this is a problem. The emo iterates:

1. **Broad prune** — clear out the noise (might lose some signal)
2. **Targeted load** — pull in what you need (might get some noise)
3. **Notice a loss** — recover something specific that was accidentally dropped
4. **Zoom in** — narrow to the most promising evidence region
5. **Discover wrong area** — zoom back out, repivot to a different part of the graph

Each turn is cheap. Convergence across turns is what matters. The emo learns which pattern operations tend to converge fastest for which kinds of tasks.

---

## Operating on Invisible Graph Structure

The emo has the graph structure baked into its weights from training on the mesh. It "knows" topology it can't currently see in context. This enables a critical capability: **issuing pattern operations that reference invisible graph structure.**

### Example

X and Z are in context. Y is not. The emo wants to remove both X and Z but doesn't know an efficient pattern that directly matches both. However, its weights suggest X and Z are both connected to Y in the mesh. So it emits:

```
(drop (related-to Y) (depth 1))
```

If the X-Y and Z-Y connections exist in the graph, this operation catches both X and Z — plus potentially other Y-related patterns the emo didn't even know about but are also irrelevant. The emo inferred Y as a useful pivot from its weights, operating on graph structure it can't see.

### The Graph as Hallucination Filter

The operation resolves against the **live graph**, not against the emo's weights. If the emo hallucinates a connection that doesn't exist:

- The operation doesn't match what the emo expected
- X might stay in context (the X-Y connection doesn't exist in the graph)
- Nothing bad happens — the emo sees the unexpected result and adjusts

The probabilistic logic graph constrains the emo's speculative operations. The emo can be aggressively speculative because:

- **When weights are right** (common for well-established graph structure): massive leverage — invisible operations carve out or load exactly the right stuff
- **When weights are wrong** (graph changed, or emo oversimplified): the graph limits the damage — the operation matches differently than expected, the emo sees the result, iterates

This is the neural-symbolic duality at its most concrete:
- **Neural perspective:** "I'm using my intuition about graph structure to issue efficient operations"
- **Symbolic perspective:** "The neural net is producing approximate queries that I resolve precisely against the actual graph"

### Why Training Compounds

The better the emo's weights model the actual graph, the more efficiently it can operate through invisible references. This creates a compounding RSI loop:

Better training → more accurate graph intuition → more aggressive invisible operations → faster context convergence → better decisions → better training data → better weights

The emo is literally getting better at navigating a graph it can't fully see.

---

## Building Justified Confidence

The emo's objective is not just "find evidence for action X." It's "build the strongest possible **justified** case for action X" — and justification requires both positive evidence and exhaustive invalidation search.

### The Confidence Structure

**Strength** — how much positive evidence supports the thesis. Visible in context as loaded evidence patterns.

**Confidence** — how thoroughly the invalidation search has been conducted. Visible in context as the record of where the emo looked for counter-evidence and what it found (or didn't find).

High strength + low confidence = "looks good but I haven't checked." The emo knows it needs to load counter-patterns — patterns that could invalidate the thesis — and verify they don't. Part of the context manipulation is deliberately loading the most threatening counter-evidence, checking it, and either:

- **Finding real invalidation** → thesis collapses, adjust, start building a different case
- **Not finding invalidation** → confidence increases, and the *record of where you looked* becomes part of the evidence

The emo's modified context literally contains the evidence chain and the invalidation search record. The symbolic gate can verify: was the search genuine? Did it cover the relevant threat patterns?

---

## The Training Objective

This gives a concrete, measurable training objective for synlang-native emos:

**Input:** An objective and a graph state (or a rendered view of one).

**Task:** Produce a sequence of probabilistic pattern-matching operations that converge on a maximally justified context for the best available action.

**Reward signal:**
- Did the action succeed?
- Was the confidence well-calibrated? (The system was confident and right, or uncertain and right to be uncertain)
- Did the invalidation search catch real problems when they existed?
- How efficiently did the emo converge? (Fewer operations for the same quality = better)

**Training data:** Every past decision — every evidence chain, every invalidation search, every success and failure — sits in the mesh as s-expressions. Directly consumable as training data in the same format as the reasoning.

Failed attempts are training gold: "here's what the context manipulation should have been given what we now know." The training loop from [`neuro-symbolic-cognition.md`](neuro-symbolic-cognition.md) is literal — train the emo to be better at manipulating its own context toward justified action.

---

## Why S-Expressions Are Load-Bearing

The s-expression commitment is not a notation preference. It's what makes the 10:10000 ratio possible:

- **Structural matching** — patterns can match by structure (domain, depth, type, relationships), not just content
- **Hierarchical zoom** — s-expressions nest, so you can match at any depth of granularity
- **Uniform format** — operations, data, evidence, reasoning traces, navigation pointers — all the same structure, all manipulable by the same patterns
- **Homoiconicity** — the patterns that manipulate context are themselves s-expressions in the mesh, subject to the same evidence dynamics

With flat natural language, context manipulation degrades to brute-force token-by-token editing. With structured s-expressions, the emo operates in pattern space — orders of magnitude more efficient.

---

## Ema Specialization Through Manipulation Style

Different emas develop different context manipulation skills even on the same base model:

- A **finance ema** has learned which patterns to load for financial decisions, where to look for invalidation in market data, how to build evidence cases for trades
- A **defense ema** has learned different manipulation patterns optimized for threat assessment, anomaly detection, security verification
- The **orchestrator** has learned broad context manipulation — efficient at assembling high-level situational awareness, dispatching to specialist emas

The specialization lives in LoRA adapters that encode "how to manipulate context for this domain." Not different knowledge — different manipulation skills. The [dreamer's](../core-concepts/dreamer-actuator-split.md) job: evolve better manipulation strategies per domain through evolutionary populations evaluated on decision quality.

---

## Security Considerations

The cognitive loop has three attack surfaces that require defense-in-depth (see [`security-and-resources.md`](../synodoxics/security-and-resources.md)):

**Attention manipulation.** An adversary that can influence which patterns get loaded into context can bias reasoning without touching the underlying graph. The defense is that attention patterns are themselves mesh patterns subject to evidence dynamics — artificially promoted patterns that don't lead to good outcomes lose confidence. The [navigation layer maintenance](attention-allocation.md#navigation-layer-maintenance) cycle provides periodic review.

**Context poisoning via live graph.** Between turns, malicious graph updates could shift the emo's premises. The defense is [between-turn reconciliation](live-graph-context.md#between-turn-reconciliation) — the symbolic system classifies changes and flags premise invalidation — combined with the symbolic gate verifying against the live graph before any real action proceeds.

**Unconstrained pattern-matching.** The emo references invisible graph structure through its weights. An adversary that can manipulate graph topology could create misleading pivot points. The defense is that operations resolve against the live graph, not the emo's weights — the graph constrains speculative operations. Wrong guesses produce unexpected results that the emo observes and adjusts to, rather than silently propagating errors.

In all three cases, the **symbolic gate** is the primary real-time safety layer within the cognition loop: every action proposal is verified against the live graph state before execution. Staleness and manipulation in the reasoning context are efficiency problems, not safety problems, as long as the gate holds.
