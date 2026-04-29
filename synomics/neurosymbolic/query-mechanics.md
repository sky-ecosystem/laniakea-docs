---
concepts:
  references:
    - probabilistic-mesh
    - truth-values
    - rsi
    - dreamer-actuator-split
---

# Query Mechanics

How the emo actually searches the graph. [`cognition-as-manipulation.md`](cognition-as-manipulation.md) describes the principle: compact pattern-matching function calls that reshape vast regions of context. This document makes it concrete — what kinds of queries exist, how they handle the combinatorial explosion of graph traversal, and how the emo learns to write its own search strategies.

The runtime sits underneath. Noemar's three-layer query resolution (direct fact matching via inverted index → rewriting → compound resolution via set operations) is the mechanism the strategies described here compose into. See [`../synodoxics/noemar-substrate.md`](../synodoxics/noemar-substrate.md) for the substrate; this doc describes what the emo writes on top of it.

---

## The Interface Contract

All query operations — regardless of implementation — satisfy the same contract:

```
query(input, budgets) -> candidates + evidence + cost
```

- **candidates** — the items/structures found
- **evidence** — why they were returned (trace, provenance, scores)
- **cost** — what the query spent (ops, time, tokens)

This contract is the invariant. Everything behind it can vary, compete, and evolve.

---

## Search Backends

Multiple search primitives, each returning the same shape. The emo composes them freely:

| Primitive | What it does | Good for |
|-----------|-------------|----------|
| **graph-traverse** | Follow edges from a starting node, optionally filtering by type, TV, depth | Structured relationships, known topology |
| **vector-search** | Find semantically similar claims by embedding distance | Catching related claims that aren't structurally connected |
| **keyword-search** | Fast literal or regex matching on claim content | Quick, targeted lookups when you know what you're looking for |
| **aggregate** | Count, average, group across a result set | Summaries, statistical queries |

No backend is privileged. Graph traversal is the natural fit for structured mesh navigation, but vector search catches things the graph structure misses, and keyword search is sometimes the right tool for a direct lookup. The system learns which backends work for which tasks.

---

## The Combinatorial Explosion

Naive graph traversal blows up. Query "what's related to X," follow all edges, at each hop the fan-out multiplies. After 3 hops on a moderately connected graph, you're looking at thousands of paths. The graph is larger than context — you can't return everything.

Two approaches, both useful:

### Deterministic: Threshold Pruning

At each hop, compose TVs along the path (simplest: multiply strengths, min confidence). Prune branches where the composed TV drops below a floor. Return top K by composed TV.

```
(graph-traverse (start ETH) (depth 3)
  (min-composed-tv 0.3) (limit 50) (compose strength-product))
```

Predictable, replayable, no randomness. Good when you know roughly what you're looking for.

### Stochastic: TV-Weighted Sampling

At each hop, don't follow all edges — **sample** a few, weighted by TV. High-TV edges are more likely to be followed, but low-TV edges aren't impossible. Each run through the same query returns different results.

```
(graph-traverse (start ETH) (depth 3)
  (samples-per-hop 3)
  (temperature 0.7)
  (tv-weight strength)
  (seed 8812))
```

This is Monte Carlo-style exploration of the graph. Each sample is a different random walk weighted by TV. Run it 5 times and you get 5 different views. Across samples, you converge on the important stuff while occasionally discovering surprises in low-TV regions.

**Why stochastic matters:** deterministic top-K always returns the same results. You never stumble into a low-TV path that leads somewhere important. Stochastic sampling naturally explores — the temperature parameter controls how aggressively. High temperature = more random (explore). Low temperature = nearly deterministic (exploit).

**Replayability:** the seed makes stochastic queries reproducible. Same seed, same graph state → same results.

---

## The Emo as Coder

The parameterized queries above are special cases. The general case: **the emo writes arbitrary s-expression programs that the engine executes.**

A traversal strategy is not a fixed function with parameters — it's a program:

```
(strategy assess-correlated-risk
  (start ?asset)
  (step 1 (keyword-search (concat ?asset " risk") (recency 7d) (limit 20)))
  (step 2 (graph-traverse (start ?step1) (edges correlation)
           (samples-per-hop 3) (temperature 0.5)))
  (step 3 (vector-search (embed (context ?current-thesis)) (top-k 10)))
  (step 4 (merge ?step1 ?step2 ?step3 (dedup-by claim-id)))
  (return ?merged))
```

The emo can:

- **Write new strategies** from scratch
- **Load existing strategies** from the graph and execute them
- **Modify existing strategies** — tweak parameters, add steps, swap backends
- **Compose strategies** — pipe the output of one into the input of another

### Strategies Are Patterns in the Graph

This is the homoiconicity principle made concrete. A traversal strategy is an s-expression. It lives in the graph like any other claim. It has a TV based on how well it's worked:

```
((strategy assess-correlated-risk ...) TV 0.78 0.65)
```

Good strategies accumulate positive evidence and get reused. Bad strategies lose confidence and decay. The dreamer evolves new strategies in simulation. Different emas develop preferences for different strategies — specialization through strategy selection, not just through weights.

The system doesn't just learn what to believe — it learns how to search, and stores its search methods as first-class knowledge.

### What the Emo Controls

The emo's query programs can specify anything the engine supports:

- Which backends to use and in what order
- Sampling parameters (temperature, samples-per-hop, weight function)
- Composition of results across backends (merge, intersect, subtract)
- Stopping conditions (budget limits, confidence thresholds, convergence tests)
- Branching logic (if step 2 returns nothing, try step 2b instead)

The engine is a dumb executor. The intelligence is in the program the emo writes.

---

## Backend Composition

Real search often requires multiple backends in sequence:

1. **Keyword search** to find entry points — "where in the graph is credit spread data?"
2. **Graph traversal** from those entry points — follow structural edges to related risk metrics, counterparties, historical patterns
3. **Vector search** to catch semantically related claims the structure missed — "what else in the graph is similar to what I've found?"

Each step feeds into the next. The composition is part of the strategy program. Which compositions work for which tasks is itself a learned pattern:

```
;; A meta-pattern: "for risk assessment, this composition order works well"
((composition-order risk-assessment
    (keyword-search -> graph-traverse -> vector-search))
  TV 0.72 0.58)
```

---

## TV-Aware Traversal (Not Probabilistic Inference)

The query engine composes TVs during traversal — multiplying strengths, taking min confidence along a path. This is simple arithmetic for pruning and ranking, not full probabilistic inference.

The engine does NOT compute "what is the marginal probability of X given all possible worlds?" That's #P-hard and unnecessary. The engine returns individual claims with their TVs and the composed TV of the path that found them. The **emo** reasons about what the TVs mean in combination. The hard probabilistic reasoning happens in the cognition loop, not in the storage layer.

The query engine is a TV-aware graph traverser with sampling. It is not a probabilistic database.
