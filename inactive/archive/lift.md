# Lift

A concept doc for the Noemar team. Names the central force a self-improving reasoning system has to generate, the ground it rests on, and the recursive form — meta-lift — that makes the loop compound.

---

> **Ground gives reality contact. Lift gives leverage. Meta-lift makes leverage compound.**
>
> Lift is accumulated reusable understanding. It is produced by reasoning, testing, explaining, connecting, varying, and calibrating. A thing has lift when future humans or agents can operate on it with more freedom, safety, and leverage. Meta-lift is lift that helps produce more lift. RSI is the compounding loop where the system grows lift around its own lift-generating core.
>
> But lift is not truth. Lift is increased agency over truth-seeking under feedback. Cognitive residue that looks useful but makes future cognition worse is **false lift**; carrying it imposes a persistent cost. A lifted system improves by adapting continuously — sometimes extending, sometimes revising, sometimes compressing, sometimes backing out of a bad direction.

---

## What this is

The team needs vocabulary for something that's been implicit in the work: a reasoning system doesn't just need more intelligence in the abstract. It needs **ground** — contact with reality through execution, observation, tests, and feedback — and it needs **lift** — reusable understanding that lets future humans, agents, and the system itself reason about, modify, vary, and compose its primitives. Lift is the central concept for RSI because it is what makes a system improvable by itself. Ground is what keeps lift in contact with reality.

Two refinements matter throughout. First, not every grounded primitive is inspectable; some are opaque buttons that do powerful things (LLMs, neural matchers, JIT paths, caches). These still need lift around them — calibration, dispatch rules, observed reliability — but the lift is mostly empirical because the source isn't readable. Second, not all cognitive residue is real lift; some artifacts look like reusable understanding but fail under feedback. This is **false lift**, and carrying it imposes an ongoing cost the system has to detect, revise, or remove.

The rest of this document develops the picture across several layers: what lift is as a substance, false lift and the cost it carries, the lifted-vs-grounded duality, opaque grounded primitives as a special case, the technical grounding for "lift," where to invest, how lift gets generated, why the core deserves the most lift, and what a fully meta-lifted system looks like.

---

## What lift is

The function-first definition: **lift is what cognition leaves behind when it successfully makes future cognition easier.** That "successfully" is doing real work — cognition that didn't make future cognition easier wasn't lift, it was wasted effort. Cognition that made future cognition *harder* is false lift, and the persistent cost it carries has to be detected and revised. Lift is the *durable residue* of cognition that pays forward, raising the agency that future humans or agents have over the thing it accumulates around.

**Grammatically, lift is a mass noun.** Like "weight" or "altitude" or "context." You don't have *a* lift; you have *some* lift, *more* lift, *enough* lift. Things have lift in varying amounts. The amount accumulates over time and effort, and degrades when ignored.

The substance of lift is everything that surrounds a primitive and makes it operable beyond its bare execution:

- Synlang elaborations of what it does
- Worked examples showing how it's used
- Derived variants — alternative formulations, specializations, generalizations
- PLN beliefs about its reliability across contexts
- Probabilistic links to related concepts
- Calibration data — predictions made and outcomes observed
- Experimental records — what was tried, what worked, what didn't
- Meta-rules about when to invoke it, when not to
- Provenance trails — derivations that depended on it, derivations it produced
- Edge cases discovered, failure modes catalogued

A grounded atom by itself: low lift. The same atom surrounded by all of the above: high lift. The continuum is what matters; the boundary is fuzzy.

**Lift is generated, not declared.** It accumulates from work — reasoning, derivation, experimentation, articulation, observation. Whoever (or whatever) does that work generates lift around the core thing. Nobody can declare lift into existence; it has to be produced by acts of reasoning.

**Lift is continuous, not binary.** A primitive doesn't transition from "unlifted" to "lifted." It accumulates lift over time, in increments, with the most important primitives accumulating the most.

## The aerodynamic metaphor

A wing has lift. The lift isn't a separate object — it's a force the wing generates by interacting with airflow. More wing area, more lift. More airflow, more lift. The lift is what keeps a heavy aircraft airborne.

Same here. A grounded primitive on its own is heavy and fixed — sits where it is, can't be moved, can't be reshaped. Generate enough lift around it (synlang, derivations, links, beliefs, variants), and the system can lift it off, move it, reshape it, derive new versions, compose it elsewhere.

**Without lift, things are stuck on the ground.** With enough lift, they fly.

The metaphor isn't pushed further than it goes. Lift isn't free — generating it costs compute, attention, and the risk of producing false lift instead of the real thing. The optimization isn't *maximum* lift; it's the joint allocation across lift-generation, grounded execution, and the wrapping of opaque grounded power that lets the system do what it needs to do given its resource budget.

---

## False lift

Not all cognitive residue is lift. Some artifacts create the *appearance* of lift while reducing future agency:

- Stale documentation that once explained the system but now anchors people to obsolete behavior
- Overfit benchmarks that reward the wrong thing
- Decorative reasoning traces that sound coherent but don't improve decisions
- Uncalibrated confidence that makes weak evidence feel stronger than it is
- Premature abstractions that hide the variation the system still needs to see
- Ossified metapatterns that were useful in one regime but become dogma in another
- Cached conclusions without provenance, context, or expiry conditions
- Dead variants kept alive because nobody can tell whether they're still load-bearing

This is **false lift**: structure that looks like reusable understanding but fails under feedback. The cost shows up as anchoring, brittle abstractions, bad dispatch choices, wasted search, misplaced trust, and a system that becomes less willing to explore the right alternatives because the wrong frame has hardened around them.

The implication is critical: **lift must include its own adaptation handles.** Every important piece of lift should carry enough structure for future cognition to improve it as evidence changes:

- Provenance: where it came from, what evidence produced it
- Confidence: how strongly the system currently believes it
- Context: where it has worked and where it has not
- Dependencies: what other beliefs, rules, or metrics it relies on
- Counterexamples: where it failed or became suspicious
- Alternatives: nearby variants that might replace it
- Expiry or decay: when it should be rechecked
- Revision paths: how to adjust, replace, split, merge, or roll back if it stops paying rent

This applies at every level. The system must be able to adapt not only object-level beliefs and formulas, but also partially ossified metapatterns: the abstractions it uses to create abstractions, the heuristics it uses to allocate lift, the evaluation functions it uses to decide what counts as progress. Sometimes adaptation looks like moving forward into a refinement. Sometimes it looks like splitting a pattern into contextual variants. Sometimes it looks like returning to an older path because the newer one was false lift. The direction doesn't matter; evidence-guided improvement does.

In a probabilistic world, many things that look like deep structure are temporary regularities. The system needs enough lift to use them while they're useful, and enough meta-lift to change course when the evidence turns.

So the goal is not "more lift everywhere." The goal is **net lift after costs**: reusable understanding that survives contact with reality, stays revisable, and improves future cognition more than it constrains it.

---

## Lifted and grounded

The lifted/grounded distinction is one important contrast in the concept stack, but it's narrower than the lift concept itself. **Lift is a property anything can accumulate; lifted vs grounded is a contrast about whether a thing is abstract-and-pattern-matchable or concrete-and-specific.** Both kinds of things can have lift; both can lack it.

Things in a system tend toward two poles:

| Grounded | Lifted |
|---|---|
| Concrete instance | Has free variables |
| Anchored to specifics | Floats across many bindings |
| Opaque (callable, not inspectable) | Transparent (pattern-matchable) |
| One place in the inference graph | Probabilistically connected to many places |
| Production runtime | Reasoning surface |
| Specific binding `(parent tom bob)` | Pattern `(parent $x $y)` |
| Grounded atom (external Python) | Synlang elaboration |
| RSI cannot touch it | RSI can compose, mutate, regenerate it |
| Fast | Composable |
| Heavy, sits where it is | Airborne, can be moved |

Importantly: **grounded isn't a value judgment.** Grounded is necessary. The runtime needs to actually execute somewhere; performance comes from grounding hot paths. The failure mode isn't being grounded — it's being grounded *without lift around it*, leaving the system blind to its own machinery.

And critically: **grounded artifacts can themselves generate lift.** A test result adds lift to the rule it tests. A benchmark trace adds lift to the algorithm it benchmarks. A specific counterexample adds lift to the general claim it disproves. A provenance chain adds lift to the conclusion it justifies. A captured failure mode adds lift to the design that produced it. None of these are abstract patterns; they're concrete grounded artifacts. They produce lift around the abstract things they touch by giving those abstract things contact with reality.

So the contrast that matters most for daily work isn't *lifted vs grounded* — it's **high-lift vs inert.** A primitive surrounded by rich lift (whether the primitive itself is abstract or concrete) is operable, improvable, trustable, composable. A primitive with no lift is a black box, regardless of whether it's grounded code or an unreified abstraction.

The mnemonic for this part of the stack: **ground gives reality contact; lift gives leverage.** Mature intelligence needs both grounding (for contact with evidence, execution, and feedback) and lift (for freedom of motion over that reality). They aren't competitors; they're complementary forces. When people say "ground gives truth," the precise meaning is not that grounded artifacts are infallible; tests can be wrong, observations can be noisy, and benchmarks can overfit. The point is that ground is where reality pushes back.

The mature pattern is that important primitives exist in both forms simultaneously: a fast grounded implementation that runs in production, and a lifted elaboration the system reasons over.

---

## Opaque grounded primitives

The lifted/grounded distinction has one refinement worth making explicit: **grounded primitives vary in how inspectable they are.**

A Python function with readable source is grounded but transparent — you can read what it does, derive properties from it, propose alternatives. An LLM call is also grounded — it's external machinery you call and it returns a result — but the source isn't readable in any practical sense. The cognitive surplus is locked inside the weights. You push a button and powerful stuff happens.

Many of the most important grounded primitives in a modern reasoning system are like this:

- **LLMs** — enormous amortized prior knowledge plus on-demand pattern matching, opaque at the weight level
- **Neural pattern matchers** — a transformer proposes candidate matches over synlang structures, with a precise matcher then verifying the survivors
- **GPU / SIMD kernels** — vectorized PLN formula evaluation, parallel inverted-index lookup, batched belief revision; opaque at the instruction level, much faster
- **JIT-compiled hot paths** — once a code path is hot, the JIT produces an optimized binary you don't usually inspect
- **Caches and memoization tables** — the answer without the computation; prior work crystallized into a fast lookup
- **Probabilistic data structures** — Bloom filters, HyperLogLog, count-min sketches; approximate, opaque, fast
- **Approximate algorithms** — ANN indices, sketches, sampled integration; you accept the error bar as the cost of throughput
- **Compiled grounded atoms** — once a synlang elaboration gets compiled down to optimized Python, the resulting atom is fast and callable but no longer pattern-matchable in the same way

These are still grounded primitives — they're callable, they execute, they produce results. They're not lift. But they need lift around them just like every other important grounded thing, with one difference: **the lift you can generate around them is mostly empirical.** You can't derive properties from an LLM's weights; you can only observe how it behaves and calibrate from there.

The discipline:

1. **Calibrate per context.** *"GPT-X's auth-related rule proposals: 0.81 reliability across 47 cycles."* *"The learned matcher's precision in graph-protocol contexts: 0.94."* *"This Bloom filter's false-positive rate on this corpus: 0.003."* Reliability isn't a property of the source in the abstract; it's source-in-context, and it's measured.
2. **Lift the dispatch.** *Where* and *when* to invoke each opaque primitive is a decision the system makes constantly. That dispatch logic should be lifted — queryable, revisable, calibrated — even when the primitive itself is opaque. You can't make the LLM transparent; you can make your decision to call it transparent.
3. **Wrap with checks.** Naked invocation without verification is how systems crash. LLM proposes, regression suite checks. Neural matcher proposes, precise matcher verifies. JIT compiles, parity tests verify equivalence with the lifted spec.
4. **Treat outputs as candidate lift, not as facts.** The candidate rule the LLM proposed becomes real lift only after the substrate has tested, captured, and calibrated it. The same pattern as any grounded artifact producing lift around the abstract things it touches: a test result lifts the rule it tests, a benchmark trace lifts the algorithm it benchmarks, an LLM output lifts the belief it suggests — *after* verification.

The temptation with opaque grounded power is to leave it as a raw button because it's already useful. The discipline is the opposite: the more powerful and the more frequently invoked, the more lift the system should accumulate around it.

This is one of the clearest illustrations of how lift creates value. A powerful grounded primitive used without lift around it is low-value — you have a button that does great things but no reliable way to know *when* it's the right move, *how* to use it well, or *why* it works in some contexts and not others. Add lift — calibrations per context, dispatch rules, observed failure modes, knowledge of training and finetune behavior — and the same primitive becomes high-value. The hardware didn't change; the knowledge of when, how, and why to call it did. Without that lift, it's just a button you press and hope. **Lift is what converts raw capability into compounding leverage**, and opaque grounded power makes the principle especially visible because empirical lift is the only way in.

## The technical grounding

"Lift" isn't a metaphor borrowed from physics for color. It's already a load-bearing technical term in three adjacent disciplines, all pointing at the same shape.

**Lambda lifting** (functional programming compilation). A nested function captures variables from its enclosing scope (a closure). Lambda lifting rewrites the closure as a top-level function with the captured variables passed as explicit parameters. The function moves from *hidden inside someone else's environment* to *globally visible and callable directly*. Compilers do this because top-level functions are easier to analyze, optimize, and serialize. The shape: take something trapped inside a context, expose what it needs as inputs, and pull it up where the rest of the program can see and act on it.

**Functor lifting** (Haskell, category theory). A plain function `f :: a -> b` operates on bare values. `fmap` lifts it into a structured world: `fmap f :: Functor f => f a -> f b` now operates inside `Maybe`, `[]`, `IO`, a probability distribution, anything that's a Functor. Same operation, now living in a richer context where extra machinery composes with it. The shape: take a function from a flat world and move it into a structured world where richer operations apply.

**Lifted inference** (statistical relational learning). In probabilistic logic — Markov Logic Networks, ProbLog, PLN's neighborhood — there are two ways to do inference. *Grounded inference* enumerates every variable binding, producing the full propositional graph, then reasons. Specific. Concrete. Doesn't scale. *Lifted inference* reasons at the level of the quantified variables themselves, exploiting the symmetry across all the groundings. You compute once at the variable level and the result is implicitly true for every binding. Abstract. Symmetrical. Scales. The shape: reason at the level of structure and variables, not at the level of specific instances.

These three usages cluster: **lifted means moved into a richer context where more operations apply, generally by abstracting from concrete instances toward the structure that holds across many instances.** The concept we're naming is exactly this, in the Noemar setting.

It also dovetails with the **symbol grounding** tradition in AI, where *grounded* has always meant *anchored to specifics* — perceptual data, physical instances, concrete bindings. Noemar's existing usage of "grounded atom" (anchored to specific external code) is a natural fourth member of the family.

The point: when you say "lift" in the Noemar setting, you're not coining a new word. You're picking up a word the field already uses for the thing you mean. The team will hit the literature naturally as they go deeper.

---

## Pairing, not separation

A common misreading is to think lifted and grounded are alternatives — pick one. They're not. The mature shape is **the same primitive existing in both forms simultaneously**, with the lifted form acting as the spec the system can reason about and the grounded form acting as the production artifact that runs.

This pattern is everywhere in mature systems work, under different names:

| What it's called elsewhere | The split |
|---|---|
| Source code / compiled binary | Manipulable source vs fast artifact |
| Denotational / operational semantics | What it means vs how it executes |
| Genotype / phenotype | What evolution mutates vs what gets selected |
| Specification / implementation | The contract vs the code that satisfies it |
| Theory / praxis | Why and what it means vs that it works |
| Macro-time / runtime (Lisp) | Compile-time manipulable form vs executed code |

In every one of these, the rule is the same: **don't ship binary without source. Don't ship phenotype without genotype. Don't ship runtime without spec.** The mature artifact is the *pair*, plus a verified relationship between them.

But the relationship is **temporally contingent, not absolute.** The lifted form is under continuous revision based on evidence. The grounded gets recompiled when the lifted has moved enough to matter. They agree at the moment of compilation; they will disagree tomorrow because the lifted will have moved. The discipline isn't "keep them eternally in sync"; it's "recompile the grounded when the lifted has moved, and have tests that verify agreement at the compilation moment."

The lifted is the moving target. The grounded is its periodic crystallization.

---

## Generate lift where it's earned

Lift is resource-constrained. You don't lift everything to the same altitude.

The gating principle: **lift accumulates around things that have proven themselves load-bearing.** Throwaway code: zero lift. Iteration-stage experiments: minimal lift, just enough to keep moving. Important utility code: some lift. Load-bearing core: a lot. Constitutional / canonical concepts: as much as the resource budget allows.

The Web/UX maxim **pave the cowpath** captures the gating perfectly: walk the path first, see where it actually goes, *then* pave it. Don't pave randomly. Don't pave before the path is proven. But once it's proven, paving multiplies everyone's speed on it forever.

The "rule of three" pattern from software design says the same thing: don't abstract until the third use. The first instance is just code. The second instance is duplication you tolerate. The third instance earns the abstraction. Lift works the same way — primitives earn their lift by demonstrating that they'll be reused, depended on, built upon.

A maturity gate, in operational form: as something rises in importance — gets used more, becomes load-bearing, attracts other things sitting on top of it — it earns more lift. The team doesn't lift everything to the same altitude. It lifts each thing to the altitude its role requires.

## The core is malleable

A subtle misreading of "lift the core" is to imagine the core as authoritative — a fixed PLN, a fixed chainer, a fixed matcher, with synlang descriptions sitting beside them as documentation. That's not the picture.

A truly lifted core means **nothing in it is sacred.** PLN, the chainer, the matcher, the rewriter, the protocol dispatcher — all live beliefs the system holds about what currently works best. The lifted form isn't documentation of the privileged grounded version; it's the *spec*, and the spec is under continuous revision.

The granularity of revision is **variables and constants, not monolithic v1/v2/v3.** Inside the deduction formula, the constants — the prior pseudo-count `k`, the cap on per-step confidence change, the bound on confidence decay through long chains, the choice between Beta and Dirichlet for multi-class, the threshold below which to switch from delta-method to sampling — every one of these is itself a live belief. The system holds PLN beliefs about *which value works best in which context*. Selection happens through evidence accumulation across deployments, not through version-controlled forking.

The same applies all the way down: the matcher's wildcard semantics, the rewriter's reduction order, the chainer's priority queue ordering function, the protocol dispatcher's tie-breaking rules. Each of these is a tunable. Each gets its own pile of lift over time — calibration beliefs, A/B records, context-conditional preferences. The "current Noemar" is whatever joint configuration the lift currently recommends.

This is much more biological than mechanical. Plants seed and grow. Organisms evolve under selection pressure. The lifted core is the genome on which evolution operates.

---

## Lift is grown, not hand-written

A subtle but important point: lift isn't something the team writes by hand. The hand-writing model maxes out at the staffing curve and breaks the moment the system gets big enough that no human can keep up with it.

The actual long-run picture has three roles:

- **Researchers seed.** A minimum viable lifted core, deliberately authored, exposing the right granularity. Hand-written, deliberate, small. The genome.
- **Environments grow.** Dynamic loops — RL harnesses, real users, ingestion pipelines, calibration cycles, regression sweeps, online tournaments between variants — where the system's actions produce feedback the system can convert into lift. The selection pressure.
- **The system generates.** Most of the lift. Reasoning tokens, derivations, calibration updates, variant proposals, A/B records, beliefs about its own behavior. The growth.

When an LLM does chain-of-thought, it's trying to generate lift in real time. The prompt is grounded input. The reasoning tokens are derived structure, intermediate inferences, alternative framings — candidate lift around the input. When the trace improves the answer, exposes useful structure, or leaves reusable residue, it is real lift. When it merely sounds coherent while anchoring the model to a wrong frame, it is false lift.

Reasoning models (o1, R1, etc.) are explicitly trained to generate *more candidate lift* before answering, and to select from it better. Test-time compute scaling is fundamentally: spend more cycles producing, testing, and compressing lift before grounding to an answer. The whole shift from "ask the model" to "let the model reason first" is a shift toward generating lift before grounding to an answer.

The same pattern generalizes to Noemar: the PLN chainer generates lift (derived beliefs with provenance). The RSI agent generates lift (proposed rules, regression diffs, decisions). Calibration cycles generate lift (predictions made, outcomes observed, beliefs updated). Each loop produces lift around the parts of the system it touches.

**The researcher's two highest-leverage jobs are stewarding the seed and designing the environments.** The growth itself isn't theirs to do — it can't be, at any reasonable scale.

---

## Resource-constrained, not finite

A clean way to think about lift: it's one of several resources being optimized jointly, alongside compute, attention, storage, latency, and action-cycles. The system has to learn where to spend on lift versus where to spend on execution versus where to spend on calibration versus where to spend on action.

The optimum isn't maximum lift; it's the joint allocation that achieves the mission within the resource envelope.

A few implications:

- **Where to spend lift is itself a learned policy.** The system holds beliefs like *"adding lift to this primitive raises capability by Δ; cost is C cycles; expected payoff is Δ × usage frequency over the calibration horizon."* It allocates accordingly. Beliefs about lift-allocation are themselves updated by evidence — and they live in the same Space as everything else.
- **Calibration is the converter.** Evidence about outcomes converts into lift-allocation guidance. Without calibration, the system has no basis for choosing where to spend.
- **Lift can be wasteful.** Generating elaborate lift around a primitive that turns out not to matter is a real cost — compute spent, attention diverted from where it would have paid off. The system should learn to *not* lift things that don't earn it.
- **False lift carries ongoing cost.** The system should measure not just how much lift was produced, but whether that lift increased later capability, reduced uncertainty, improved calibration, or opened better action. If it didn't, the residue should be weakened, revised, compressed, or removed.
- **Compression is the dual move.** Sometimes the right move is to *reduce* lift on a region — recognize that twenty variants have collapsed onto one stable winner, retire the others, keep the lift around the winner. Lift cycling, not just lift accumulation.
- **Adaptation is the capability; backtracking is one necessary move.** A system that cannot retreat from a bad abstraction, a misleading benchmark, or a partially ossified metapattern is not highly lifted. It is brittle. But the point is not to move backward or forward; the point is to keep moving toward configurations that work better under evidence.

"Lift is finite" would imply a fixed budget being depleted. That's the wrong model. The right model is: **lift competes with everything else for the system's resource budget, and the optimal allocation is itself something the system learns.**

---

## Meta-lift

Now the recursive form, which is the deepest piece of the concept and the operational definition of RSI.

The compact definition:

> **Meta-lift is lift that improves the system's ability to generate, allocate, test, adapt, compress, and reuse lift.**

Each verb names a meta-skill the system can grow:

- **Generate** — producing new lift through reasoning, derivation, experimentation
- **Allocate** — choosing where to spend lift given the resource budget
- **Test** — verifying that lift actually pays off (parity, calibration, regression)
- **Adapt** — changing course as evidence changes: refining, contextualizing, weakening, replacing, or rolling back lift
- **Compress** — pruning lift around regions that have crystallized; retiring dead variants
- **Reuse** — applying accumulated lift to new contexts, transferring between domains

Each of these can itself be improved by more meta-lift, which is how the recursion compounds.

In one phrase: **apply lift to the parts of the system that generate lift.** Or even more memetically: **RSI is lift learning to make better lift.**

The asymmetry: lift on a leaf improves that leaf. Lift on a branch improves what hangs from it. Lift on the *roots* improves the trunk, the branches, the leaves, and every future leaf the tree will grow. The core is the roots. Every PLN inference, every pattern match, every rule application, every protocol dispatch flows through the core — so any lift added to the core is multiplied by *every reasoning operation that ever runs*, including all future RSI runs that produce yet more lift.

This is why "lift the periphery" plateaus and "lift the lifters" doesn't.

The CS name for this pattern is **self-hosting** (or **bootstrapping**, or **metacircular**). gcc compiles itself. The Lisp interpreter is written in Lisp. Smalltalk's compiler, debugger, and class browser are written in Smalltalk and modifiable from within. PyPy is a Python interpreter written in (R)Python that traces and optimizes its own interpretation.

The reason these systems are extraordinary isn't that they're elegant. It's that **every improvement to the system immediately benefits the next iteration of the system itself.** Improve the compiler by 5%, recompile the compiler with itself, and the next compilation runs 5% better — including the next compilation of the compiler. The loop closes; improvement compounds.

Noemar's aspiration is to be a self-hosting reasoning system. The lifted core is what makes self-hosting possible. Without it, you have a normal system that occasionally improves; with it, you have a system whose foundation generates the conditions for its own elevation.

The recursive engine, in plain language:

> Lift makes things tractable. The most tractable thing you can lift is the lift-generation machinery itself. Lifting it makes future lift higher-quality. Higher-quality lift makes the next round of lifting the lift-generators more effective. Repeat.

Or in one sentence: **more lift to make better net lift, especially on the parts that make, test, adapt, and reuse lift.**

## The lifted core

The aspiration: **synlang all the way down.** Every layer expressible in the substrate it's interpreting. Push the unlifted floor as low as possible.

You'll never reach the bottom — some grounded primitives have to exist; the runtime has to actually execute somewhere. That's fine. The aspiration is to push the unlifted floor as low as possible and lift everything above it. The lower the unlifted floor, the more of the system the system can reason about itself, the more meta-lift the recursive loop produces per cycle.

**The failure mode of an unlifted core** is a glass ceiling at the substrate boundary. The system can improve user-facing rules, domain-specific logic, application-level patterns. It cannot reach into its own pattern matcher, its own PLN chainer, its own query resolver, its own protocol dispatch, its own RSI loop. There's a hard ceiling exactly at the boundary of the unlifted core, and no amount of cleverness in the periphery breaks through it. The recursion never closes; it dead-ends at the substrate.

This is why a lot of AI self-improvement work doesn't compound. Deep nets can be fine-tuned but the foundation isn't lifted — you can shape behavior but you can't reason about how the model is reasoning. RLHF reaches the surface, never the substrate. The loop never closes because the substrate doesn't speak the same language as the improvement.

Noemar's bet is the inverse: build the foundation in a substrate that can lift itself, and the loop closes naturally as the lift accumulates inward.

---

## What this looks like in Noemar, concretely

A lifted core in Noemar would have these properties (none of them present-day pass/fail tests — more like a checklist of things to grow toward):

1. **The reasoning machinery describes itself.** The PLN chainer's logic, the pattern matcher's algorithm, the query resolver's strategy, the protocol dispatcher, the RSI loop — each has a synlang elaboration the system can query and reason over.

2. **Equivalence between lifted and grounded is enforced at compilation, not aspirational.** Tests evaluate both forms on random inputs and assert agreement at the moment of compilation. The lifted form is treated as the spec; the Python is the compiled artifact. Drift between them either triggers recompilation or fails the build.

3. **Decomposition over monoliths.** Each grounded primitive is many small atoms whose composition is expressed in synlang. The same end-result is achievable through multiple synlang stitchings, each optimized for a different context. Granularity is the leverage point.

4. **Variables and constants are exposed as first-class beliefs.** PLN's `k`, the rewriter's reduction depth, the matcher's tie-breaker — these live as named, queryable, revisable facts, not as Python constants buried in modules. Evolution operates at the right granularity.

5. **Multiple variants coexist.** Several deduction formulas (strict, fuzzy, conservative, optimistic), several matcher strategies, several reduction orders. Each annotated with PLN beliefs about per-context performance. Selection happens via evidence, not human dispatch tables.

6. **Meta-rules are present.** Rules that recognize rule shapes, propose variants, derive specializations, suggest factorings. RSI doesn't synthesize from scratch; it does structured search over a space the system already understands.

7. **Self-models are auto-derived.** Facts about how the chainer behaves, how the matcher behaves, how the loop behaves — derived from observed runs, updated continuously via revision. Not markdown docs that drift; live beliefs that don't.

8. **Provenance and derivations are inspectable artifacts.** Every conclusion carries a derivation tree that's queryable. The Phase-2 `(verify $claim)` query operates on these. This is the substrate that lets the system reason about *how* it reasons.

9. **Calibration tables exist and grow.** Per-category beliefs about predictive accuracy, maintained automatically as predictions get compared to outcomes. Without calibration, lift doesn't translate into trust, and trust is what enables autonomy.

10. **Resource-allocation beliefs are first-class.** The system holds beliefs about where lift pays off, updated by evidence. These guide future lift-generation cycles.

11. **False lift is modeled explicitly.** The system tracks stale abstractions, misleading benchmarks, dead variants, overconfident rules, and metapatterns whose payoff has decayed. It can weaken, retire, or reopen them instead of silently carrying them forward.

12. **The RSI loop is the most lifted thing in the system.** Its logic — what counts as a good iteration, when to fork, when to promote, when to abandon, when to revise course, when to roll back — is queryable and modifiable in synlang. Otherwise the loop can improve everything except itself, and you've capped the recursion.

## Repo signals to watch for

If meta-lift is the direction, here's what should appear in the codebase over time:

- **Loops are running, not just snapshot tests.** Calibration cycles, dynamic environments, real user feedback flowing back as evidence, online A/B between variants. Without loops, no growth.
- **Seed minimal; growth substantial.** A researcher can articulate the core in an afternoon. The bulk of what the system runs on is grown, not authored. Anti-signal: a sprawling hand-written corpus that isn't being amended by the system itself.
- **`.noemar` files describing internal machinery.** Files like `pln_formulas.noemar`, `chainer.noemar`, `matcher.noemar` next to their Python counterparts — and tests verifying agreement.
- **Granularity exposed at the variable/constant level.** Not just `class PLNProtocol(Protocol):` but `(pln-config k 1.0)`, `(pln-config max-confidence-step 0.1)` etc., as queryable, revisable facts.
- **Live competition between variants.** Several active formulations of the same primitive coexisting. PLN beliefs annotating per-context performance. Dispatch between them as a learned, lifted, revisable thing.
- **Calibration history actually populating.** Files like `data/calibration_history.noemar` showing real numbers moving over real cycles.
- **Resource-allocation beliefs as facts.** The system tracking where it's spending lift and what's paying off.
- **Self-improvement reports proposing core-level changes, not just leaf-level.** Today's `noemar_loop_report.md` proposes refactors of `Space.query` — leaf-level. The signal of maturing meta-lift is when reports propose changes to *the matcher's tie-breaker*, *the chainer's priority function*, *the deduction formula's prior pseudo-count*.
- **A synlang → Python compiler exists.** The bidirectional move. Once the system can ground its own lifted variants, it grows new precompiles autonomously instead of waiting for humans to write them.
- **False-lift detection visible.** Reports name artifacts that looked useful but failed under feedback: abstractions that overfit, metrics that misled, rules whose confidence was too high, metapatterns that stopped paying off.
- **Adaptation records exist.** The repo contains explicit refinements, contextualizations, retirements, weakened beliefs, reverted metapatterns, and reopened search branches with provenance explaining why the change happened.
- **Compression moves visible.** Variants that lost the tournament are retired. Lift around dead branches is reclaimed. The system isn't just accumulating; it's pruning.
- **Phase-2 `(verify $claim)` actually working.** Stored derivations, replayable, fail-closed. This is the keystone — until proofs can be persisted and replayed, the recursive loop can't safely close.

---

## Vocabulary

Phrases that are useful to have in shared use:

- **"This needs more lift."** Diagnostic. Names the gap when something is operating but unimprovable.
- **"This area has good lift now."** Positive observation. Names a region where the substrate has matured.
- **"This is false lift."** Diagnostic. Names cognitive residue that looks useful but makes future cognition worse.
- **"This is opaque grounded power."** Diagnostic. Names a fast/opaque/approximate primitive (LLM call, neural matcher, JIT path, cache, probabilistic structure) so the team treats it accordingly — needs empirical lift around it, not raw invocation.
- **"Wrap with checks."** Reminder to pair opaque-primitive outputs with verification before they flow into anything that cares about correctness.
- **"Calibrate per context."** Treat each opaque primitive as a belief about reliability per context, updated by evidence.
- **"Lift the dispatch."** Even when a grounded primitive is opaque, the decision of *when* and *where* to call it should be lifted, queryable, revisable.
- **"Net lift after costs."** The real optimization target. Not more artifacts, but more future agency after the cost of generating, maintaining, and adapting them.
- **"Adapt the metapattern."** Higher-level revision. Names the move of changing an abstraction, heuristic, or evaluation frame that has partially ossified.
- **"Reasoning is lift when it pays forward."** What lift *is*, with the false-lift guardrail included. Connects LLM reasoning, PLN inference, human deliberation, cleanup work — all forms of generating candidate lift.
- **"Ground gives reality contact, lift gives leverage, meta-lift makes leverage compound."** The canonical mnemonic.
- **"Ground for contact, lift for leverage."** Shorter version, focused on the lift/grounded duality.
- **"Lift the lifters."** The meta-move. Where to direct effort for compounding returns.
- **"RSI is lift learning to make better lift."** The clean definition of RSI as an active, evidence-driven loop.
- **"More lift to make better net lift."** The recursive engine in plain words.
- **"Lift all the way down."** The aspiration. North star.
- **"Pave the cowpath."** The gating principle. Don't lift randomly; lift what's proven.
- **"Self-hosting reasoning."** The CS-canonical framing. Engineers will get it instantly.

The maxims that matter most for daily work:

- **Generate lift where it compounds.** Core compounds; periphery doesn't.
- **Optimize net lift, not visible lift.** Explanations, traces, docs, variants, and metrics only count if they improve future cognition under feedback.
- **Granularity is leverage.** Decompose monolithic primitives early; stitched assemblies expose more optimization sites.
- **The lifted form is the active spec.** Python is the compiled artifact. When evidence moves the spec, the implementation gets recompiled.
- **Adaptation is part of lifting.** A lifted system can refine, contextualize, or unwind its own abstractions, including the metapatterns it uses to decide what counts as lift.
- **Document by lifting, not by writing markdown.** Push docstring instincts into synlang annotations the system itself can consume.
- **Self-models should be auto-derived.** Hand-written docs go stale; auto-derived facts don't.
- **The RSI loop's own machinery deserves the most lift.** Otherwise the loop can improve everything except itself.

---

## The whole arc, in one sentence

**A self-improving reasoning system needs ground (contact with reality) and lift (reusable agency over structure), with meta-lift — lift pointed at the machinery that generates, tests, adapts, compresses, and reuses lift — as the engine of recursion. Some grounded primitives are opaque buttons that do powerful things; they still need lift around them, just empirically rather than analytically. Some apparent lift fails under feedback and becomes a cost the system has to detect and revise. RSI is what happens when the system gets good enough at producing net lift around its own lift-generating core that the loop starts to compound.**

The seed is a minimal lifted core, deliberately authored, exposing the right granularity. The system runs in environments rich enough to produce evidence. Each cycle, the system spends some of its resources on generating lift around the parts where lift seems to be paying off, calibrates its own predictions about what worked, and updates its beliefs — including its beliefs about how much lift to allocate where. The grounded layer is whatever the current lift recommends, recompiled as the lifted layer evolves. Nothing about the core is sacred; everything is a live belief about what currently works best, in the contexts the system is currently encountering.

The ceiling on the whole loop is set by two things: the richness of the environments the system runs in (no signal, no growth) and how granularly the core is lifted (you can only evolve what's exposed as a tunable). Researchers steward the seed and design the environments. The growth itself isn't theirs to do.

That's the work.

---

**Ground gives reality contact. Lift gives leverage. Meta-lift makes leverage compound.**
