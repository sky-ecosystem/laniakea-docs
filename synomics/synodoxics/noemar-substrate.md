---
concepts:
  defines:
    - noemar-substrate
    - epistemic-cycle
  references:
    - probabilistic-mesh
    - truth-values
    - crystallization-interface
    - dreamer-actuator-split
    - cancer-logic
    - rsi
    - artifact-hierarchy
    - retrieval-policy
---

# Noemar: The Synlang Runtime

Grounds the synomics epistemic architecture in its concrete implementation. Where other synodoxics docs describe what the Synome knows and how it learns abstractly, this doc names the runtime and maps the abstractions onto it.

> **Stable vs evolving:** The architectural commitments below — Space as the substrate, PLN truth values with the delta method, provenance with disjointness checks, the protocol system, the epistemic cycle, and the two-axis RSI model — are settled. The specific *implementations* described (the fork → regress → promote crystallization loop, the LLM-driven Rule-Author Agent with its CONSULT/MUTATE/FINALIZE call pattern) are first running instances, not fixed architecture. The dev teams are actively exploring alternative mechanisms; treat the implementation specifics as illustrative of how the architecture *can* be realized rather than as a canonical design.

---

## Synlang and Noemar

**Synlang** is the language: S-expressions grounded in the synomic library. Code, data, knowledge, queries, and reasoning traces all live in one homoiconic format.

**Noemar** is the runtime: the engine that stores synlang expressions, matches patterns over them, propagates beliefs, and dispatches multi-modal reasoning.

> **Lift framing:** Noemar is what a **lifted core** looks like in practice (see [`../lift.md`](../lift.md)). The architectural commitments — Space as substrate, PLN with calibrated confidence, provenance with disjointness checks, the protocol system, the epistemic cycle — are the substrate the rest of the system can reason about, restructure, and improve. The aspiration is **synlang all the way down**: push the unlifted floor as low as possible so that the recursive loop closes inside the system rather than dead-ending at the substrate boundary. Where opaque grounded primitives remain (LLM-driven proposers, neural pattern matchers, JIT'd hot paths), lift is generated empirically — calibration per context, lifted dispatch, output verification — rather than analytically.

The relationship is the same as Lisp-the-language vs SBCL-the-implementation: synlang is what teleonomes write; Noemar is what runs it. Noemar's `Space` plays the role MeTTa/Hyperon's Atomspace plays — a metagraph-style store with pattern matching as the primary operation — but is built from scratch, with architectural choices specifically targeting performance limitations that block scaling to civilizational use.

This pair supersedes the earlier research track that explored hypergraph languages, MeTTa adaptation, and notation alternatives. Those questions are settled.

---

## The Space as the Mesh

The [probabilistic mesh](probabilistic-mesh.md) is, concretely, the **Space** — Noemar's central knowledge store and query engine. Where the mesh chapter describes the abstract dynamics (truth values, crystallization, RSI), the Space provides the concrete substrate: an inverted index for fast candidate retrieval, a memoized term rewriter, and a compound body resolver for set-theoretic query operations.

A Space contains:

- **Facts** — ground synlang expressions: `(= (croaks Fritz) True)`
- **Rules** — rewrite patterns with variables: `(= (frog $x) (and (croaks $x) (eats_flies $x)))`
- **Beliefs** — PLN truth values attached to expressions, with provenance
- **Indexes** — head-symbol, arity, and argument-position lookups for fast retrieval

Queries decompose into three layers, applied in order:

1. **Direct fact matching** — index lookup against the inverted index
2. **Rewriting** — apply rules to reduce the query toward normal form, with memoization
3. **Compound resolution** — `and`/`or`/`not` decompose into sub-queries combined via set operations (intersection, union, complement against the fact store)

The mesh's abstract claim that "everything can inform everything else within access constraints" is operationalized as: any synlang expression may be a query target, and the Space's three-layer resolution finds it through whatever combination of fact lookup, rule application, and compound decomposition is needed. The "subgraph isomorphism is NP-complete" caveat that the prior research track flagged turns out not to bind in practice — the inverted index plus head-symbol dispatch reduces most queries to small candidate sets that pattern matching resolves cheaply.

---

## Truth Values: PLN with the Delta Method

The (strength, confidence) framework described in [`probabilistic-mesh.md`](probabilistic-mesh.md) is implemented as **PLN truth values** with Beta distribution semantics:

- **Strength** = the probability estimate (mean of the Beta posterior)
- **Confidence** = how certain we are about that estimate (maps to pseudo-count via `count = k * c / (1 - c)`)
- **Variance** = `s * (1 - s) / (count + 2)` — naturally decreases as evidence accumulates

This implementation makes one significant departure from canonical PLN: Noemar uses the **delta method** for confidence propagation through inference rules — first-order uncertainty propagation via partial derivatives, not heuristic confidence multipliers:

```
Var(output) = Sum_i (df/dx_i)^2 * Var(x_i)
```

The output's uncertainty is shaped by the formula's *sensitivity* to each input. High-strength premises with low sensitivity contribute minimal uncertainty — unlike heuristic multipliers, which penalize all inputs equally regardless of how much the output actually depends on them. The result is calibrated confidence rather than pessimistically discounted confidence.

Consequence for synomics: the [evidence axiom](probabilistic-mesh.md#the-evidence-axiom) commitment — that evidence-counting is the foundational epistemological method — is preserved. The delta method is a more faithful implementation of that commitment than canonical PLN's heuristics.

The PLN protocol covers the operator surface synomics needs: deduction, modus ponens, induction, abduction, inversion (Bayes), revision (independent-evidence merging), conjunction, disjunction, and similarity/equivalence operators, plus belief queries (truth-value, confidence, credible-interval, posterior-sample). Additional operators are added as inference patterns prove load-bearing.

---

## Provenance and the Cancer-Logic Defense

The [cancer-logic](../core-concepts/cancer-logic.md) threat model — self-corruption through overeager updates and evidence double-counting — has a concrete structural defense in Noemar.

Every belief carries **provenance**: a frozen set of evidence IDs identifying which observations contributed to it. Combining beliefs via `revision` (PLN's evidence-merging operator) checks for shared provenance and either:

- Merges cleanly when evidence sources are disjoint
- Refuses to count overlapping evidence twice when provenance overlaps

This is the operational form of "evidence flows back" and "no double-counting." It's not policy — it's a check at the operator level, written into the revision rule.

Combined with append-only Space semantics (rules and facts are added, never silently mutated), this gives the [defense in depth](security-and-resources.md#defense-in-depth) pattern its concrete first layer:

| Defense layer | Noemar mechanism |
|---|---|
| Ossification | High-confidence beliefs require proportionally more contrary evidence — emergent from the PLN math, not imposed |
| Validation before promotion | Forked-Space staging + regression suite |
| Evidence integrity | Provenance disjointness checks at revision |
| Audit trail | Every belief's derivation is replayable from its provenance leaves |
| Rollback | Append-only enables reversion to any prior state |

---

## Pattern Matching: One-Way and Bidirectional

Synlang queries match against the Space via two complementary mechanisms.

**One-way matching** is directional: pattern variables bind against ground expressions. Used when retrieving facts and applying rules — the rule's pattern is the query, the Space's facts are the targets. Wildcards (`$_`) match without binding.

**Robinson unification** is symmetric: both sides may contain variables, and the result is the most general unifier (MGU). Used when composing rules, threading bindings through compound queries, and resolving constraints across multiple beliefs. Optional occurs check prevents infinite-type cycles.

Both mechanisms compose. A compound query like `(and (parent $x $y) (parent $y $z))` is resolved by intersecting binding sets from each conjunct, threading variables consistently across the conjunction.

---

## The Crystallization Interface as Staging + Promotion

The [crystallization interface](../core-concepts/crystallization-interface.md) — where governance converts probabilistic evidence into deontic commitments — needs *some* concrete mechanism for staging proposed changes, validating them, and either incorporating or rejecting them. The architectural requirements are: changes are proposed in isolation from main state, are validated against acceptance criteria before promotion, are applied additively (not as silent mutations), and leave an audit trail.

> **Implementation note:** The first running instance of this — fork → propose → test → regress → decide → record, with a forked Space as staging and a regression suite as the gate — is one realization of these requirements, not the canonical mechanism. The dev teams are exploring alternative staging and validation strategies (different acceptance criteria, different proposal sources, different rollback semantics). The pattern below illustrates how the architecture *can* be realized; expect the specifics to evolve.

The first running mechanism:

1. **Fork** — clone the main Space into an isolated staging Space. Full copy of facts, rules, and beliefs. Fresh caches. Changes in staging never touch main.
2. **Propose** — add candidate rules or facts to staging.
3. **Test** — run targeted queries to verify intended behavior.
4. **Regress** — run the full regression suite against both Spaces, diff the results.
5. **Decide** — promote (apply additively to main), discard, or retry.
6. **Record** — emit an event fact: `(promoted ...)` or `(abandoned ...)` so the decision becomes part of the audit trail.

In any realization, the staging-and-promotion pattern is the [dreamer-actuator split](../core-concepts/dreamer-actuator-split.md) at the implementation level: dreamart-as-isolated-state, evolutionary-loop-as-proposal-plus-validation, promotion-as-deontic-commitment. The current first instance uses an LLM agent as the proposer; the larger architecture replaces this with synomic dreamer formations as embodiment power scales.

---

## The Protocol System: Multi-Modal Reasoning

Noemar routes specialized reasoning through pluggable **protocols**, each registering head symbols and dispatching to a specialized expert backend:

| Protocol | Backend | Reasoning kind |
|---|---|---|
| PLN | scipy | Probabilistic inference, belief revision, uncertainty propagation |
| Graph | NetworkX | Traversal, paths, connectivity, subgraph operations |
| SMT | Z3 | Satisfiability, constraint solving, formal verification |
| SymbolicMath | SymPy | Differentiation, integration, simplification |
| Validation | built-in | Type and schema constraints |

Architecturally: Noemar is the manager, each protocol is an expert. A single query chain can compose protocols — a PLN inference feeds a graph traversal feeds an SMT check, all in one synlang expression with provenance tracked through.

This concretizes the abstract claim that the Synome supports cross-modal reasoning. It's not metaphysics — it's head-symbol dispatch with structured inter-protocol bridges.

The protocol set is open. Future protocols may include theorem-proving backends, specialized graph databases, time-series solvers, or domain-specific reasoners. The commitment is to the architecture (manager + experts, head-symbol dispatch, S-expression interchange), not to the current expert list.

---

## The Epistemic Cycle

The closed loop by which an embodiment senses the world, updates beliefs, predicts outcomes, acts, and calibrates its own reliability is six-stage:

1. **Sense** — evidence sources emit beliefs with stable evidence stamps. External sources, none generated by the embodiment itself.
2. **Revise** — new evidence merges with existing beliefs via PLN revision. Disjointness checks prevent double-counting. Confidence grows monotonically with independent evidence.
3. **Infer** — multi-protocol rules compose beliefs into higher-order verdicts.
4. **Hypothesize** — emit predictions as first-class beliefs, each accompanied by a derivation tree carrying the full proof.
5. **Act** — before applying anything, replay the derivation chain via `(verify $claim)`. If verification fails, the action is dropped and an audit fact is recorded. Auto-apply is gated on category-level confidence thresholds.
6. **Calibrate** — compare prediction to outcome. Revise the calibration belief for that category. The next cycle's predictions inherit the updated reliability estimate.

The recursion is not metaphorical: calibration beliefs about the embodiment's own reliability become load-bearing inputs to its own future inference. The system reasons about the quality of its own reasoning, in synlang, using the same PLN operators it uses for everything else. Each cycle's evidence makes the next cycle's predictions either more accurate (when the system is well-calibrated) or less ambitious (when miscalibration is detected) — bounded, convergent self-improvement, not unbounded recursive growth.

For the security analysis of why this is bounded rather than unbounded, see [`security-and-resources.md`](security-and-resources.md).

---

## The Emo, Concretized

The [neuro-symbolic cognition](neuro-symbolic-cognition.md) loop describes the **emo** (embodied orchestrator) as the neural component that does fuzzy approximate pattern matching, narrowing the search space before the symbolic system verifies and refines.

> **Implementation note:** The first running instance — the **Rule-Author Agent**, an LLM driving a tool surface around Noemar — is one concretization of the emo, not the architectural commitment. The dev teams are actively exploring alternatives: different proposing components (smaller specialized models, dreamer formations, hybrid architectures), different tool surfaces, different control loops. What's stable is the pattern: a neural proposer narrowing search, symbolic verification gating action, evidence-stamped results feeding back into the mesh. What's evolving is everything else.

The first running instance — the Rule-Author Agent — uses an LLM driving a tool surface to propose synlang rules, stage them, run regression queries, and decide whether to promote. The agent's interaction pattern with Noemar decomposes into three call kinds:

- **CONSULT** — the agent queries Noemar for reasoning input: what gaps exist, how confident are existing beliefs, did this change fix or break the regression suite
- **MUTATE** — the agent edits staging: fork, add rule, draft
- **FINALIZE** — the agent closes the loop: promote or abandon

Empirically, successful runs in this instance had several times more CONSULT calls than MUTATE calls. The agent reasoned *with* Noemar, not just over it. Whether the CONSULT/MUTATE/FINALIZE decomposition generalizes to other emo realizations is an open question; the underlying pattern (neural proposal, symbolic verification, evidence-stamped result) is what scales.

---

## RSI: Two Orthogonal Axes

[Recursive self-improvement](../core-concepts/rsi.md) has two distinct dimensions, neither subsumed by the other.

**Meta-depth** (synomics axis) — how recursively meta the improvement is:

| Level | Focus |
|---|---|
| 0 | Raw knowledge (patterns, probabilities, evidence) |
| 1 | Using knowledge (decisions, executing tasks) |
| 2 | Strategies for pattern-mining (better querying) |
| 3 | Meta-strategies (better strategies for finding strategies) — recursive |

**Autonomy scope** (Noemar axis) — what gets updated, with what gating:

| Level | What updates | Safety profile |
|---|---|---|
| L1 | Belief strengths and confidences as evidence arrives | Zero risk — always on |
| L2 | The system's own prediction-accuracy calibrations | Low — fully audited |
| L3 | Inference rules, regression-gated in staging | Moderate — implemented today |
| L4 | The runtime's own source under a constrained patch vocabulary | High — gated on L2 calibration above a fixed threshold |

These measure different things. A capability has both a meta-depth and an autonomy scope. The Rule-Author Agent operates at meta-depth Level 2 (improving pattern-mining strategies) and autonomy scope L3 (rule discovery with regression gating). A future dreamer formation evolving its own evaluative criteria operates at meta-depth Level 3 with autonomy scope L3 — same scope, deeper recursion. A pure belief-calibration ingest operates at meta-depth Level 0 with autonomy scope L1.

The synomic inertia spectrum applies to both axes: deeper meta-depth and higher autonomy scope both ossify more slowly and require more evidence to advance.

---

## What's Still Being Designed

The architectural commitment is locked. Specifics in flux:

- **Authority hierarchy in Space terms** — how synart/telart/embart map onto Space scoping. Options under consideration: tagged authority on each fact, separate Spaces per artifact level with sync rules, or hybrid. The retrieval-policy invariants (synart > telart > embart, risk gates authority) constrain the design but don't determine it.
- **Cross-embodiment Space synchronization** — how separate embodiments share synart while maintaining private telart and embart. Append-only foundations make this tractable; the protocol is open.
- **The full protocol set** — current protocols cover much of what the Synome needs. New protocols will be added as use cases mature.
- **Evidence-stamp design at scale** — frozen sets work today. Evidence sources may grow numerous enough to require structured stamp schemas with hierarchical scoping.
- **Synlang surface conventions** — the language is settled (S-expressions). Surface conventions for common patterns (rule shorthand, belief annotation, query DSLs) are evolving with usage.
