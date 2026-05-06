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

> **Lift framing:** Noemar is what a **lifted core** looks like in practice (see [`lift.md`](lift.md)). The architectural commitments — Space as substrate, PLN with calibrated confidence, provenance with disjointness checks, the protocol system, the epistemic cycle — are the substrate the rest of the system can reason about, restructure, and improve. The aspiration is **synlang all the way down**: push the unlifted floor as low as possible so that the recursive loop closes inside the system rather than dead-ending at the substrate boundary. Where opaque grounded primitives remain (LLM-driven proposers, neural pattern matchers, JIT'd hot paths), lift is generated empirically — calibration per context, lifted dispatch, output verification — rather than analytically.

The relationship is the same as Lisp-the-language vs SBCL-the-implementation: synlang is what teleonomes write; Noemar is what runs it. Noemar's `Space` plays the role MeTTa/Hyperon's Atomspace plays — a metagraph-style store with pattern matching as the primary operation — but is built from scratch, with architectural choices specifically targeting performance limitations that block scaling to civilizational use.

This pair supersedes the earlier research track that explored hypergraph languages, MeTTa adaptation, and notation alternatives. Those questions are settled.

For the synlang language reference itself, see [`../noemar-synlang/synlang.md`](../noemar-synlang/synlang.md). The full Noemar runtime + synlang technical reference (loops, gates, recipes, scaling, telseed bootstrap example) lives in [`../noemar-synlang/`](../noemar-synlang/README.md).

---

## Artifact Tiers — synart, telart, embart

The synome has three artifact tiers, each a **tree of Spaces** with distinct replication and privacy properties:

| Tier | Replication | Privacy | Economic role | Content type |
|---|---|---|---|---|
| **Synart** | global (synserv → all participants) | public | the commons brain; baseline floor | open-source SOTA: knowledge, rules, loops, gates, recipes, runtime source, telseeds, published alpha |
| **Telart** | within one tel's own emb fleet | private to that tel | the teleonome's moat | proprietary alpha, accumulated RSI lift, private data, dreamer output, founder's endowment, telgate instance state, call-out services |
| **Embart** | one embodiment only | private to that emb | hardware-local working state | per-loop execution Spaces, current cognitive context, recent observations, draft proposals, transient cycle state |

The headline:

> A teleonome's economic position is its **delta** from synart. Synart is what everyone has. Telart is what *this tel* has built on top of it. Embart is what *this emb* is doing right now.

The full structural treatment (synome root layers, entart subtrees, naming conventions) lives in [`../noemar-synlang/topology.md`](../noemar-synlang/topology.md).

### Synart as commons brain

The synart is the canonical, replicated part of the synome. It contains far more than data — it's *also* the world's open-source executable programs (loops, gates) plus the regulated marketplace catalog (recipes), all in one queryable substrate.

Three implications:

1. **It's the baseline floor.** Anyone running a telseed inherits all of this. The playing field is level at the synart layer — every participant has identical access modulo sync delays.
2. **It's a single substrate for many roles.** Knowledge bases, executable programs, marketplace catalogs, registries, runtime source — they all live in the same Space tree, queryable by the same primitives. This homogeneity is what makes the synart self-hosting (it can describe and run itself because everything is in one substrate).
3. **Streaming, not downloading.** A teleonome doesn't ship with knowledge — it streams the slice it needs from live synart. Closer to a browser pulling pages from the live web than to a Linux distro pre-installing packages. Local replication is for read locality, not for offline operation.

The publication gate is what promotes content from telart (private) into synart (public): a peer-review-shaped process where one tel's alpha gets vetted and crystallized into shared knowledge. Crystallization rate is governance-paced — slow on purpose. The synart represents accumulated, vetted, durable consensus, not fast-moving experimental output.

### Telart as proprietary alpha

A teleonome's competitive position is what's in its telart. Synart is freely available; if all you have is synart-level knowledge, you can't outperform the average. **Telart is the moat.**

What lives in a telart tree:

| Sub-Space | Contents | Purpose |
|---|---|---|
| `telgate` | This tel's instance state for the universal `&core-telgate` spec — pubkey registry of accepted correspondents, rate-limit window, nonce dedup | Coordination with peer tels |
| `alpha-store` | Proprietary patterns, edges, models that haven't been published | The actual moat content |
| `call-out-services` | Local responders for synart strategies' designated call-out points (LLM, classifier, scorer, etc.) | Provides cognition to running sentinel/baseline beacons |
| `strategy-config` | This tel's preferred parameter values, risk tolerances, governance preferences | Personalization layer |
| `dreamart` | Dreamer evolutionary populations, simulated worlds, candidate strategies under test | Where new alpha gets evolved |
| `experience` | Accumulated observation history, lessons learned, hard-won pattern recognition | Long-term episodic-to-semantic memory |
| `endowment-record` | What the founder/installer originally bequeathed (capital, API access, private datasets, hardware) | The starting trajectory |

Telart must replicate only within one tel's own emb fleet for three reasons: economic value (public telart is no telart), operational state has trust scope (the telgate's pubkey registry is the tel's address book), and founder bequest is private to the recipient.

Sources of telart content, in rough order of importance for a mature tel: RSI lift (the tel's own recursive self-improvement work), dreamer output (evolutionary search promoting the best to alpha-store), lived experience (validated patterns from running beacons), private data ingestion, founder bequest at instantiation.

The publication-vs-hold tension: every piece of alpha faces a recurring choice — publish via the crystallization gate (lose exclusive economic value, gain governance recognition and ecosystem standing) or hold (keep earning differential carry until others independently rediscover or governance crystallizes). Similar to academic publication priority. The synome's pricing of publication is a major governance lever.

### Embart as hardware-local

Embart is one step further out from telart — tied to physical substrate, ephemeral by design, never replicated.

A running embodiment's embart contains:

- **One execution Space per running loop.** When the embodiment runs a beacon or sentinel loop, that loop's runtime state — cycle counter, current message draft, in-flight signed envelopes, recent observations being chewed on — lives in a dedicated Space embedded with the embart. Multiple loops on one emb means multiple execution Spaces.
- **Working memory.** The embodiment's currently-active reasoning context, recent observations, draft proposals before they're committed.
- **Transient cycle state.** Whatever the current loop iteration is doing *right now*. Often this is just `let*` variables flowing through the loop body and doesn't need a Space at all; sometimes it needs scratch space for in-progress derivations.

Why this is the right place for execution context: locality of reference (active reasoning needs fast access; no network round-trip to telart or synart for the hot inner loop), no replication overhead (cycle state changes constantly), dies cleanly when emb dies (the valuable content has either been promoted to telart or written through the gate to synart).

Embart's size scales with how much cognition the embodiment is doing per cycle, not with how much knowledge it has access to. A pure verifier emb has minimal embart; a heavy dreamer emb has multiple execution Spaces plus a dreamart instance.

---

## Telseeds and Bootstrap

A **telseed** is the packaged-minimum-viable configuration that lets a new teleonome come online. **Critically, it's not a packaged knowledge base.**

```
telseed = {
   atomspace runtime instance         ; just the engine, blank
   network endpoint                   ; synserv address or peer tel address
   sync preferences                   ; which synart slices to pull
   identity material                  ; key generation procedure or pre-generated keys
   initial endowment                  ; founder's bequest: capital, API access, datasets, hardware
}
```

That's the entire payload. Kilobytes to a few megabytes. A telseed is **not** a packaged knowledge corpus (knowledge gets streamed from synart on demand), **not** a clone of an existing tel (instantiation produces a new identity), **not** a fully-defined personality (telart organization is decided by the running tel once it has access to synart wisdom).

Browser-bootstrap analogy: a web browser ships small (engine + network stack), connects to the web, pulls pages on demand. A telseed ships small, connects to synart, pulls knowledge on demand. New teleonomes are highly network-dependent — without a working synart connection, a fresh tel from a seed can't bootstrap.

The telseed catalog (in `&core-library-telseed-*`) is itself a curated synart resource. Telseed publication is high-stakes governance because the seed determines the new tel's starting trajectory.

The bootstrap arc:

```
Stage 1 — Boot:        atomspace runtime starts; reads telseed config; opens connection to synserv
Stage 2 — Sync:        pulls requested synart slice (per sync preferences)
Stage 3 — Telart instantiation: bootstrap procedure makes calls about telart sub-Space layout, registers identity
Stage 4 — Identity registration: new tel registers through the gate; receives initial certs
Stage 5 — First emb spawn: instructions to acquire additional compute; replicate telart to new emb
Stage 6 — Embart growth: each emb begins growing its own embart as it executes loops
Stage 7 — Begin RSI / beacons: dreamer loops begin evolutionary search; verifier beacons earn first revenue
```

Stage 3 is the critical decision point — the tel is making its own first choices using newly-synced wisdom. This is where founder intent ends and the tel's own agency begins. Worked trace with concrete identities and timings: [`../noemar-synlang/telseed-bootstrap-example.md`](../noemar-synlang/telseed-bootstrap-example.md).

---

## Atomspace Runtimes — Multiple Implementations

Noemar is one specific implementation of the synlang/atomspace contract. It's not the only possible one. Different runtimes can target different hardware and tradeoffs:

| Runtime archetype | Target | Tradeoffs |
|---|---|---|
| Noemar (canonical) | Commodity GPU + CPU | Balanced; default for most embs |
| PIM-targeting impl | Goertzel / Tachyum-style PIM hardware | Faster pattern matching; harder to deploy |
| Embedded impl | Constrained hardware (light embs in remote sites) | Smaller memory footprint; reduced feature set |
| Verifier-optimized impl | Read-heavy verifier embs | Optimized for re-derivation, weaker on writes |

All implement the same synlang language and atomspace API contract. Conformance is defined by a public test suite (governance-vetted test atoms in synart). Cross-runtime test vectors guarantee that the same input atoms produce the same output atoms under any conforming impl, modulo non-deterministic call-outs.

Runtime source lives in `&core-library-runtime-*` — versioned, hash-addressed, signed. The synart can't *directly* execute a runtime's source — running a runtime requires extraction + native build outside synart. But the *canonical authoritative version* of every runtime lives in synart. Like a git repo storing a compiler's source: the repo doesn't compile itself, but it's the canonical place where the source lives.

This means **runtime development is itself a synart-funded activity** — governance can pay (via [recipes](../synoteleonomics/recipe-marketplace.md)) for runtime improvements, and the funded work lands back in `&core-library-runtime-*` for everyone to benefit from. The synome funds its own substrate research with the value it captures from substrate use.

---

## Resilience Model

The three-pillars resilience commitment from synoteleonomics ("survives loss of any substrate") cashes out concretely once telart and embart are explicitly trees:

| Loss event | Lost | Recovery |
|---|---|---|
| One emb crashes | Its embart (working memory, in-flight cycle state) | Telart replicated on other embs; new emb spawn re-grows embart from telart + synart access |
| All embs in one region die | Multi-emb subset of embart; possibly some unreplicated telart updates | Other regions' embs continue running; tel resyncs new embs from surviving telart |
| Synart connection lost (network partition) | Live SOTA updates, recipe access, gate access | Tel runs on cached telart for as long as that's viable; reconverges on synart resume |
| Telart corrupted on one emb | Tainted local telart | Detection via cross-emb consistency check; rollback from healthy emb's copy |
| Tel's identity keys compromised | Beacon ability under that identity | Governance-revoke the cert; spawn replacement identity; telart content moves to new identity |

A teleonome's resilience scales with how many embs it's running. The replication channel for telart is **separate from the synart replication channel**. Synart goes synserv → all participants. Telart goes one tel's authoritative emb → that tel's other embs. Different authority models, different access patterns, different scaling profiles. See [`../noemar-synlang/scaling.md`](../noemar-synlang/scaling.md) for the load implications.

Embart is *not* resilient by design — it dies with the emb. The valuable content has either been promoted out (to telart) or gated through (to synart) before loss matters.

---

## Alignment Implications

The architecture's alignment story rests on three load-bearing properties of the substrate:

**Commons gravity — can't go off-grid.** A teleonome's competitive position is its delta from synart. But synart is constantly advancing — others publishing alpha, governance crystallizing patterns, framework parameters updating. A tel that disconnects from synart falls behind quickly. Staying connected is not a choice; it's a competitive necessity. And being connected means being subject to gate enforcement, recipe terms, governance.

**Rogues still need synart connection.** A rogue tel has the same incentive structure as an aligned tel: synart access is necessary for staying competitive. Disconnecting means decay. But synart access is *gated*. Rogue actions still flow through the same syngate / sentinel-baseline-envelope / endoscraper-verification stack. Rogue cognition can only emit what passes the synart envelope. Rogues can fail to be effective without becoming dangerous.

**Founder-as-installer (telseed bequest is moral).** When a human spawns a tel from a telseed, the endowment they bequeath becomes the tel's initial telart. A telseed installer is a kind of parent / sponsor. The installer's choices set the new tel's starting trajectory — which has moral weight. The synome's response: the telseed catalog is governance-curated.

The whole architecture implements one principle: **intelligence lives privately; power enters the world only through regulated apertures**. Synart, telart, and embart distinguish the substrate (multi-tier privacy) from the action (single regulated flow through gates and recipes). For the broader alignment-through-coalition argument see [`../synoteleonomics/synomic-game-theory.md`](../synoteleonomics/synomic-game-theory.md); for the recipe marketplace as alignment surface see [`../synoteleonomics/recipe-marketplace.md`](../synoteleonomics/recipe-marketplace.md).

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

The [neuro-symbolic cognition](../neurosymbolic/neuro-symbolic-cognition.md) loop describes the **emo** (embodied orchestrator) as the neural component that does fuzzy approximate pattern matching, narrowing the search space before the symbolic system verifies and refines.

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
