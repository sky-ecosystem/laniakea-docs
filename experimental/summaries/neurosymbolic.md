# Neurosymbolic

**Status:** target architecture (cognition-loop spec). Phase-1 instantiation lives in Noemar's Rule-Author Agent (`synodoxics/noemar-substrate.md`); higher embodiment power levels scale up the emo, not the loop structure.
**Canonical home:** `lani/neurosymbolic/`

---

## TL;DR

How an individual teleonome thinks. The architectural commitment is **symbolic-first**: a symbolic machine using neural nets as sandboxed subroutines, not an LLM with symbolic tools. Everything — knowledge, code, neural chain-of-thought, search strategies, scheduling rules — is **synlang**. The neural component (the **emo**, embodied orchestrator) does fuzzy pattern-matching to narrow search; the symbolic system verifies, gates, and acts. The emo's context is a **live reactive view** into the probmesh (Noemar's Space), not a static text buffer; cognition IS surgical manipulation of that context via probabilistic pattern-matching function calls. Token throughput is the intelligence bottleneck, so the mesh exists as a **context-preparation engine**. Attention, query strategies, and hardware-scheduling policies are all learned patterns subject to the same evidence dynamics as everything else — the cognition loop is simultaneously an epistemic and risk-management loop (RSI-risk convergence).

## Section map

| § | Topic |
|---|---|
| 1 | Synlang as cognitive language |
| 2 | The neuro-symbolic loop (emo, gate, dual perspective) |
| 3 | Live graph context (rendered views, staleness, data model) |
| 4 | Cognition as context manipulation (10:10000 ratio, invisible-graph ops) |
| 5 | Query mechanics (contract, backends, stochastic, emo as coder) |
| 6 | Attention allocation (3 layers, evidence dynamics replace ECAN) |
| 7 | Hardware-aware cognition |
| 8 | Embodiment power levels |

## §1 Synlang as cognitive language

One language end-to-end: mesh storage, rules, neural chain-of-thought ("halluci-reasoning"), reasoning traces, action proposals — zero translation overhead. **Homoiconicity** (code = data): RSI-evolved strategies, queried knowledge, followed rules, emitted patterns are the same data structure; self-modification at every level is manipulation of one structure.

Training loop: mesh accumulates synlang patterns → NN trains on mesh → better candidates → symbolic verifies → good patterns enter mesh → recursive. The mesh IS the training corpus. **Effortless freeriding:** synart improvements propagate to every synlang-native teleonome instantly — contributing and benefiting are the same act at zero marginal cost.

## §2 The neuro-symbolic loop

Symbolic at boundaries, neural in the middle: incoming → structural checks → emo fuzzy match → emo narrows search space → symbolic verifies/refines → maybe loop → decision → symbolic gate → beacon/hardware.

**The emo** = neural component of each embodiment. Hallucinates candidates from weights; symbolic verifies before any real action. In **lift** vocabulary, the emo is *opaque grounded power* — calibrated per context, dispatched via lifted rules, wrapped with the symbolic gate; outputs are candidate lift, not facts.

Brute-force pattern matching over the mesh is intractable (subgraph isomorphism is NP-complete), so the emo is a query heuristic: hallucinate, narrow, let symbolic verify rather than search. **Dual perspective:** neural view sees the mesh as preparing optimal context for the next call; symbolic view sees the NN as shortcutting intractable pattern matching. Same loop.

**Cancer-logic defense.** NN never touches the outside world directly — sandboxed inside the symbolic loop. Synlang-native halluci-reasoning means failed bypass attempts are inspectable in the same formal language as the rules. **Halluci-reasoning properties:** formally structured (no handwaving), verifiable step-by-step against the mesh, evidence-generating (failed = negative evidence; successful = patterns), inspectable for cancer-logic.

## §3 Live graph context

Context is **not** a static text buffer. Each loaded s-expression is a **rendered view with a live binding** to its source claim: `(value, binding to graph location, version)`. Reactive data binding system on top of Noemar's Space.

**Staleness is the default and a non-issue.** Symbolic gate always verifies against the **live graph** before any real action. Staleness in reasoning context is an *efficiency* problem (wasted inference cycles), not a *safety* problem. Evidence dynamics punish attention configurations that produce many "premise stale, conclusion rejected" events.

**Between-turn reconciliation:** check bindings (cheap version comparison) → classify changes (noise / minor / major / premise-invalidation) → patch differentially for minor (deltas more informative than snapshots), rebuild for major, flag for premise-invalidation. Patch-vs-rebuild is itself learned. **Snapshot isolation within turns** — bindings update between turns, not during.

**Concrete data model (load-bearing):**
- **Claims** are canonical s-expressions; identity = hash of canonical form: `(rate-limit spark 25% 18h)`.
- **Truth values are an optional overlay**, not baked into storage: `((price-direction ETH up) TV 0.6 0.8)`. Some claims are governance facts with no TV; some are probabilistic beliefs with rich evidence histories.
- **Bindings** carry claim ID, version, current TV: `(bind claim:a7f3 (ver 91) (expr ...) (tv 0.6 0.8))`.
- The graph is a knowledge graph **first**; TVs/evidence/update rules layer on top.

**Change provenance.** Deltas between turns carry *what* + *why* + *who* (ema observation vs. dreamer revision vs. orchestrator override) — provenance shapes the emo's response.

**Multi-ema consistency.** Diversity at view level, consistency at graph level. Symbolic gate enforces consistency at the action boundary.

## §4 Cognition as context manipulation

From the inside: the emo stares at an array of s-expressions, has an objective, and **surgically manipulates that array** — load, drop, query, transform — to build the strongest possible justified case for an action. Reasoning and context management are the same activity.

**Core loop:** evaluate → emit pattern-match function calls modifying context → observe → repeat until maximally justified or no action justified → action proposal → symbolic gate.

**The 10:10000 ratio.** A compact pattern (~10 tokens) reshapes thousands of tokens:
```
(drop (domain finance) (confidence < 0.3) (age > 30d))
(load (related-to credit-spreads) (strength > 0.6) (depth 2))
```
Flat natural language degrades to brute-force token-by-token editing; structured s-expressions let the emo operate in **pattern space** (Fourier-transform metaphor — work in the frequency domain of context).

**Imprecision is fine.** Convergence across cheap turns is what matters. Iteration patterns (broad prune → targeted load → notice loss → zoom → repivot) are learned per task type.

**Operating on invisible graph structure.** The emo has graph topology baked into weights — it can issue ops referencing structure it can't see in current context. E.g., `(drop (related-to Y) (depth 1))` removes everything connected to a pivot Y the emo never loaded, because weights suggest X and Z (both wanted gone) connect to Y.

**Graph as hallucination filter.** Operations resolve against the live graph, not the emo's weights. Wrong intuitions produce visible "matched differently" feedback rather than silent corruption. Aggressive speculation is safe because the graph caps damage. RSI compounds: better weights → more accurate intuition → more aggressive invisible operations → faster convergence → better training data.

**Building justified confidence.** Strength = positive evidence; **confidence = thoroughness of the invalidation search**. High strength + low confidence = "looks good but I haven't checked." The emo deliberately loads threatening counter-evidence; either it invalidates (thesis collapses) or doesn't (the *record of where you looked* becomes evidence). Symbolic gate verifies the search was genuine.

**Training objective.** Input = objective + graph state. Task = pattern-match-op sequence converging on a maximally justified context. Reward = action success + calibration + invalidation catches + efficiency. Failed past attempts are training gold.

**Ema specialization** lives in LoRA adapters encoding domain-specific manipulation patterns — not different knowledge, different manipulation skills.

**Security:** three attack surfaces — attention manipulation, between-turn context poisoning, unconstrained pattern-matching against an adversarially mutated graph. Symbolic gate against the live graph is the primary real-time safety layer; staleness/manipulation in reasoning context are efficiency problems as long as the gate holds.

## §5 Query mechanics

Implements §4 on top of Noemar's three-layer query resolution.

**Interface contract** (uniform across backends):
```
query(input, budgets) -> candidates + evidence + cost
```

**Search backends:**

| Primitive | Use |
|---|---|
| graph-traverse | Structured edges, known topology, TV-filterable |
| vector-search | Semantically related claims structure misses |
| keyword-search | Direct literal/regex lookup |
| aggregate | Count/avg/group across results |

No backend privileged. System learns which composition orders work for which tasks.

**Combinatorial-explosion handling:**
- **Deterministic threshold pruning.** Compose TVs along path (multiply strengths, min confidence), prune below floor, top-K. Replayable.
- **Stochastic TV-weighted sampling.** Sample N edges per hop weighted by TV; temperature controls explore-vs-exploit; **seed reproduces**. Discovers low-TV surprises deterministic top-K never sees.

**Emo as coder.** General case: emo writes arbitrary s-expression programs the engine executes. Strategies are programs, not parameterized fixed functions:
```
(strategy assess-correlated-risk
  (step 1 (keyword-search ...))
  (step 2 (graph-traverse (start ?step1) (samples-per-hop 3)))
  (step 3 (vector-search (embed (context ?current-thesis))))
  (step 4 (merge ?step1 ?step2 ?step3 (dedup-by claim-id))))
```
Emo can write new, load existing, modify, compose. **Strategies are patterns in the graph** with TVs. Dreamer evolves new strategies. Engine is dumb; intelligence is in the program.

**TV-aware traversal ≠ probabilistic inference.** Engine multiplies strengths and takes min confidence for pruning/ranking only. Does NOT compute marginals (#P-hard, unnecessary). Hard probabilistic reasoning happens in the cognition loop, not storage.

## §6 Attention allocation

The mesh is vast; context is finite. Attention is **learned patterns in the mesh**, not a separate architectural mechanism.

**Three layers:**

| Layer | Role | Cadence |
|---|---|---|
| 1: Context window | Tokens loaded for this cycle. Zero-sum. | Every cycle, via §4 ops |
| 2: Navigation layer | Always-loaded compressed map: pointers + confidence + qualifiers. Teleonome's claude.md. Live-bound to graph. | Continuous values, periodic structure |
| 3: Candidate queue | Probably-promotable patterns; tested during maintenance. | Reviewed during maintenance |

**Topic-specific attention.** Importance is a relationship: `(relevance pattern-X context-Y (strength 0.8) (confidence 0.7))`. Different emas have different attention profiles via filtering through their relevance patterns; cross-ema filters emerge through evolution, not predesigned.

**Evidence dynamics replace artificial economics (vs. ECAN):**

| ECAN | Synome equivalent |
|---|---|
| Wages | Positive evidence on attention patterns leading to good outcomes |
| Rent | Confidence decay on unreinforced patterns |
| Conservation | Context is zero-sum |
| Importance spreading | Co-occurrence patterns learned like any other |
| Forgetting | Compaction of low-confidence, low-use patterns |
| Homeostatic controls | Synomic inertia |

Advantage: attention improves through the same RSI loop as everything else. ECAN parameters become evidence-grounded patterns rather than tuned constants.

**Lift framing.** Useful pointers pay rent in lift terms. Pointers wasting tokens are *false lift* — detected and pruned.

**Maintenance** (in the daydreaming queue): review performance → process candidate queue → refine qualifiers → compress → prune. Frequency, aggressiveness, compression targets learned. High-inertia patterns (axiomatic safety rules) resist forgetting regardless of recent use.

**Bootstrap.** Hand-crafted pointers + simple heuristics earn credibility through convergence with what evidence dynamics would produce.

**Prior art: ECAN** (OpenCog). Preserved insights: scarce/zero-sum, dual time-horizon, mandatory decay, learned co-activation. Diverged: ECAN architectural mechanism → Synome learned patterns.

## §7 Hardware-aware cognition

Hardware topology is **knowledge in the graph** (Tier 1 claims), and scheduling strategies are **patterns subject to evidence dynamics**:
```
(gpu node-1 (type A100) (vram 80GB) (inference-ms-per-token 12))
(cpu node-1 (cores 64) (graph-query-avg-ms 3))
```

**Pipelining.** GPU inference and CPU ops execution should not wait for each other. Goal: zero idle GPU time. While GPU generates turn N, CPU executes ops from turn N-1 and renders context for turn N+1.

**Speculative pre-execution.** Idle CPU runs predicted-next queries, graph maintenance, background searches. Free at the margin; system learns what to speculate on through evidence dynamics.

**Context efficiency.** Self-hosted GPU cost is dominated by **prefill** — longer context = more prefill = fewer turns/sec. 2000 precise tokens vs. 8000 full-document tokens = 4× more turns/sec. Surgical context assembly directly converts to convergence speed.

**Fixed-cost GPU economics inverts incentive:**

| | API (pay-per-token) | Self-hosted (fixed-cost) |
|---|---|---|
| Marginal query cost | Real $$ | Zero |
| Idle cost | Zero | Real |
| Exploration incentive | Minimize | Maximize |
| Speculative work | Expensive | Free |

Aggressive speculation, Monte Carlo sampling, broad exploration are *correct* on self-hosted because the alternative is wasted capacity. System learns this from its own performance data.

**Scheduling strategies as patterns.** Strategies (e.g., `parallel-fanout-between-turns` for CPU-rich, `sequential-steering` for GPU-rich) are s-expressions in the graph with TVs. System tries both, measures GPU utilization / turns-per-sec / decision quality. Hardware change automatically restages: TVs go stale, system re-evaluates.

**Self-optimization.** Performance metrics like `(evidence perf:441 (supports (strategy ...)) (context (gpu-util 0.94)))` are just more evidence. The system doesn't distinguish knowledge about the world from knowledge about itself.

## §8 Embodiment power levels

What scales between Light / Medium / Heavy is the emo's size and capability — the loop structure stays constant.

| Level | Emo profile | Typical role |
|---|---|---|
| Light | Small or remote emo; mostly cached symbolic rules | Policy endpoints, simple execution |
| Medium | Local emo; real-time neural reasoning | Sentinels, online learning, continuous sensing |
| Heavy | Large sophisticated emo; long reasoning chains | Deep cognition, dreaming, RSI |

"Compute" in the embodiment spec is really "how big is your emo."

## Key vocabulary

| Term | Meaning |
|---|---|
| **emo** | Embodied orchestrator — neural component of each embodiment. Sandboxed inside the symbolic loop. Opaque grounded power in lift terms. |
| **ema** | Specialist emo — domain-specific LoRA adapter (finance, defense, orchestrator). |
| **halluci-reasoning** | Neural chain-of-thought in synlang — formally structured, verifiable, evidence-generating. |
| **rendered view** | An s-expression in context with a live binding to its source claim + version. |
| **between-turn reconciliation** | Symbolic system's pass between inference turns: check bindings, classify, patch/rebuild/flag. |
| **navigation layer** | Always-loaded compressed pointer map into the mesh — the teleonome's claude.md. |
| **candidate queue** | Layer-3 backlog of probably-promotable patterns. |
| **10:10000 ratio** | A ~10-token pattern reshaping thousands of tokens of structured context. |
| **invisible-graph operations** | Pattern ops referencing graph structure not in current context, using weight-baked topological intuition. |
| **symbolic gate** | Final pre-action check verifying the proposal against the live graph. Primary real-time safety layer. |
| **strategy** | Multi-step multi-backend s-expression query program the emo writes. First-class graph pattern with a TV. |
| **stochastic TV-weighted sampling** | Hop-by-hop traversal sampling weighted by TV with a temperature parameter; reproducible via seed. |
| **speculative pre-execution** | Idle-CPU work between turns: predicted-next queries, maintenance, background searches. |
| **context efficiency** | Useful-tokens-over-total-tokens metric the cognition loop optimizes against. |

## Cross-references

- **`synodoxics/noemar-substrate.md`** — Runtime implementing this loop. Space, three-layer query resolution, evidence-stamped beliefs, the Rule-Author Agent (Phase-1 instantiation of cognition-as-manipulation).
- **`synodoxics/probabilistic-mesh.md`** — Full probmesh spec the live graph exposes.
- **`synodoxics/security-and-resources.md`** — Cancer-logic defense surface; fractal evidence pattern.
- **`synodoxics/lift.md`** — Vocabulary: opaque grounded power, false lift, lift-after-costs.
- **`synoteleonomics/teleonome-economics.md`** — Daydreaming queue (where nav-layer maintenance runs), fixed-cost GPU economics.
- **`synoteleonomics/dreamer-perspective.md`** — Dreamer's role evolving strategies, attention profiles, scheduling patterns.
- **`core-concepts/`** — `cancer-logic`, `truth-values`, `ossification`, `synomic-inertia`, `rsi`, `dreamer-actuator-split`, `rsi-risk-convergence`.
- **`macrosynomics/synome-layers.md`** — Embodiment power levels.

## File map

| File | What's in it that the summary doesn't have |
|---|---|
| `neuro-symbolic-cognition.md` | Full architectural-commitment narrative; why-one-language argument; full training-loop diagram; lift-framing blockquote on the emo as opaque grounded primitive. **Read first.** |
| `live-graph-context.md` | Full reconciliation classifier (4 response types); rebuild-vs-patch tradeoff; full change-provenance discussion shaping the emo's response; multi-ema consistency framing. |
| `cognition-as-manipulation.md` | Worked example of invisible-graph ops (X, Y, Z); full Fourier-transform metaphor; iteration-pattern catalog; three security attack surfaces with explicit defenses; full justified-confidence semantics. |
| `query-mechanics.md` | Full deterministic vs. stochastic traversal s-expression examples with parameters (`min-composed-tv`, `samples-per-hop`, `temperature`, `seed`); meta-pattern for composition orders as graph patterns; explicit "engine is dumb / TV-aware traversal ≠ probabilistic inference" delineation. |
| `attention-allocation.md` | Full ECAN-mechanism comparison; bootstrap process; forgetting-as-cascade through layers 1→2→3→archive; cross-ema attention sharing detail. |
| `hardware-aware-cognition.md` | Full pipelining diagram; concrete hardware-fact s-expression examples; full strategy s-expression examples (`parallel-fanout-between-turns`, `sequential-steering`); evidence-record format for performance metrics; explicit fractal-pattern claim. |
