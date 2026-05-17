# Synodoxics

**Status:** Architecture mostly target / mixed. Core commitments locked; first running implementations explicitly illustrative (the fork→regress→promote crystallization loop and the LLM-driven Rule-Author Agent are first instances, not canonical). `lift.md` is canonical vocabulary used corpus-wide.
**Canonical home:** `lani/synodoxics/`

---

## TL;DR

Synodoxics is the epistemic half of the dual architecture — what the Synome believes and how it learns, vs macrosynomics' structural what-it-is. Five docs cover: the **probabilistic mesh** (`(strength, confidence)` truth values overlaid on the deontic skeleton); the **retrieval policy** (invariants — synart > telart > embart, risk gates authority — plus principles and RSI degrees of freedom); **security & resources** (cancer-logic as primary threat; ossification, defense in depth, intent-as-asymmetric-evidence, fractal pattern); the **Noemar substrate** (synlang runtime: Space, PLN with delta method, provenance disjointness, protocol system, six-stage epistemic cycle, two-axis RSI); and **lift** (canonical vocabulary: lift, meta-lift, opaque grounded primitives, weakness as cost-algebra). The crystallization interface — governance gating from probabilistic to deontic — is the central architectural claim.

## Section map

| § | Topic |
|---|---|
| §1 | Mesh, deontic skeleton, evidence axiom, inertia |
| §2 | Retrieval policy: invariants, principles, RSI freedom |
| §3 | Cancer-logic, ossification, defense in depth |
| §4 | Noemar substrate: Space, PLN, protocols, epistemic cycle |
| §5 | RSI: meta-depth × autonomy scope |
| §6 | Lift / meta-lift / weakness vocabulary |

---

## §1 Probabilistic mesh

The synome is **probabilistic-deontic** — two endpoints of one spectrum, not separate systems:

| | Deontic skeleton | Probabilistic mesh |
|---|---|---|
| Truth | `(1,1)` axiomatic | `(s, c)` belief |
| Density | Sparse (drawn) | Dense (assumed) |
| Flow | Top-down authority | Multi-directional evidence |
| Change | Governance-only | Continuous, evidence-driven |

Unannotated knowledge is implicit `(1,1)`. The **crystallization interface** (canonical: `core-concepts/crystallization-interface.md`) hardens patterns into axioms and softens them back.

**Evidence axiom**: the one `(1,1)` epistemological commitment, not revisable: evidence-counting → `(s, c)`. All other truth-setting methods (LLM assertions, governance overrides, time-decay, regime detectors) are **fudge methods** — provisional patterns that themselves accumulate evidence and earn/lose credibility. Bootstrap necessarily runs on fudge.

**Synomic inertia**: confidence-weighted resistance to change, emergent from PLN math. Edge patterns evolve fast, core slow. **Negative inertia**: sustained contradictory evidence makes a belief actively easier to replace. **Regime change** is the cancer-logic-adjacent failure mode — a second-order detector for established-pattern misprediction is itself a fudge method, with asymmetry favoring missing a regime change over falsely declaring one.

**The hardening pipeline — three gates.** Crystallization is the last of three named gates that progressively harden content from raw observation to deontic rule:

| Gate | Source → Target | Cadence | Authority |
|---|---|---|---|
| **Inform** | Operational workspace → Local mesh | Continuous | Beacon-internal (private) |
| **Publication** | Local mesh → Canonical mesh | Scientific | Distributed review; governance-paced |
| **Crystallization** | Canonical mesh → Deontic skeleton | Rare | Governance vote |

Most observations live and die in the workspace; most local theories never publish; most canonical patterns never crystallize. Crystallization is the only gate that crosses the probabilistic/deontic boundary and is structurally the most dangerous (cancer-logic risk) — hence the slowest. Canonical home: `synodoxics/probabilistic-mesh.md`.

**Four-tier knowledge view** (cross-cut to synart/telart/embart): deontic skeleton (synart-deontic) + canonical probmesh (synart-probabilistic) + local probmesh (telart) + **operational workspace** (per-loop execution Spaces in embart). The first three are about *what is believed/known*; the fourth is about *what is currently happening* — operational, not epistemic. The hardening pipeline runs across these four tiers bottom to top. See `synodoxics/noemar-substrate.md` for the cross-cut.

## §2 Authority hierarchy and retrieval policy

`synart > telart > embart`. Caching/locality are RSI degrees of freedom.

**Retrieval-policy invariants** (any RSI weakening these is cancer-logic):

1. Authority hierarchy exists, cannot be inverted.
2. Risk gates minimum authority (low → embart may suffice; high → synart required; existential → synart + governance).
3. Evidence flows back — no black-box decisions evading the feedback loop.
4. Same retrieval logic for actuators and dreamers (data may be constrained; policy logic may not).
5. Audit trail for high-stakes decisions.

**Principles**: cheapest sufficient evidence; look up when uncertain; conflicts resolve upward and become evidence. **DoF**: query algorithms, caching, risk classification, cost models, prefetching, conflict resolution, temporal evidence weighting.

## §3 Cancer-logic, ossification, defense in depth

**Core thesis: thoughtful constraint beats reckless capability.** Cancer-logic = self-improvement that overrides safety — exponentially destructive vs linear gains, often unrecoverable. Primary security challenge is **self-corruption through overeager updating**, not external attackers. The `(s, c)` mechanism gives natural ossification: speculative patterns update freely; axiomatic ones require governance.

**Resource discipline** (money, compute, space, time, attention, trust, alignment budget) generalizes; constraints enable reasoning, security, alignment.

**Defense in depth — seven layers**: (1) ossification, (2) symbolic gate (per-action verification against live graph), (3) validation (tests pre-propagation), (4) governance review for significant changes, (5) monitoring for anomalous drift, (6) rollback, (7) peer enforcement.

**Adversarial soft channels** assumed across evidence submission, governance manipulation, disinformation, mesh gaming. Defense is **intent-as-asymmetric-evidence**: suspicious patterns trigger intent analysis; discovery of malicious intent → near-total reversal (fabricated evidence reclassified as counter-evidence; fabricator faces catastrophic consequences). Adversarial ossification becomes high-risk.

**Foundational limit — faith in the seed.** No operational defense covers a corrupted axiom at `(1,1)`; the system's own inertia would protect the corruption. Sharpest argument for getting the seed right while humans still meaningfully participate.

**Fractal security pattern**: same `growth + cancer safeguard` recurs at every scale — neural-net gradient descent with regularization, teleonome RSI with multi-emb + ossification, synome-wide evolutionary learning with telos-point + hard-fork. AI and risk management are the same operation at scale. See `core-concepts/rsi-risk-convergence.md`.

## §4 Noemar substrate

**Noemar = the runtime.** **Synlang = the language** (S-expressions grounded in the synomic library). Lisp-vs-SBCL relationship. `Space` plays MeTTa/Hyperon's Atomspace role, rebuilt for civilizational scale. Full language reference + runtime tech live in `noemar-synlang/`; synodoxics covers the *epistemic architecture* the substrate hosts. **Commitments are stable; first running implementations (crystallization loop, Rule-Author Agent's CONSULT/MUTATE/FINALIZE) are explicitly illustrative.**

### Artifact tiers (canonical home)

| Tier | Replication | Privacy | Role |
|---|---|---|---|
| **synart** | global via synserv | public | commons brain; SOTA knowledge + recipes + runtime source |
| **telart** | within one tel's emb fleet | private | the moat: proprietary alpha, RSI lift, telgate state, call-out services, dreamart, experience, endowment |
| **embart** | one emb only | private | hardware-local: per-loop execution Spaces, working memory, cycle state |

A tel's economic position is its **delta from synart**. Synart streams (browser-pulling-pages, not download). Publication gate promotes telart→synart, governance-paced. Embart isn't resilient by design — dies with the emb; resilience scales with emb count. Telart replicates separately from synart. See `noemar-synlang/topology.md`, `scaling.md`.

A **telseed** is KB-to-MB: atomspace runtime + network endpoint + sync prefs + identity material + endowment. Knowledge streams from synart on demand. Stage 3 (telart instantiation) is where founder intent ends and tel agency begins. Worked example: `noemar-synlang/telseed-bootstrap-example.md`.

### Space, PLN, provenance

Space holds facts, rules, beliefs (with provenance), indexes. Queries: direct fact match → rewriting → compound resolution (`and`/`or`/`not` via set ops). One-way matching and Robinson unification (optional occurs check) both supported.

**PLN with delta method**. Beta semantics: strength = posterior mean; `count = k·c/(1−c)`; `variance = s(1−s)/(count+2)`. Confidence propagation via `Var(out) = Σ(∂f/∂xᵢ)²·Var(xᵢ)` — calibrated, not pessimistically discounted. Operators: deduction, MP, induction, abduction, inversion, revision, conjunction/disjunction, similarity/equivalence, belief queries.

**Provenance disjointness**: every belief carries a frozen evidence-ID set; revision merges only when disjoint. With append-only Space semantics this is the operational defense against evidence double-counting and the concrete first layer of defense-in-depth.

### Protocol system

Head-symbol dispatch to expert backends:

| Protocol | Backend | Reasoning |
|---|---|---|
| PLN | scipy | probabilistic, belief revision |
| Graph | NetworkX | traversal, paths, connectivity |
| SMT | Z3 | satisfiability, formal verification |
| SymbolicMath | SymPy | differentiation, integration |
| Validation | built-in | type/schema constraints |

Open set. Noemar = manager, protocols = experts, S-expressions = interchange.

### Crystallization, epistemic cycle, emo

**Crystallization as staging + promotion**. Locked requirements: changes isolated from main, validated before promotion, applied additively, audit-trailed. Illustrative first instance: fork → propose → test → regress → decide → record (the dreamer-actuator split at implementation level).

**Six-stage epistemic cycle**: Sense → Revise (with disjointness) → Infer (multi-protocol composition) → Hypothesize (predictions as first-class beliefs with derivation trees) → Act (`(verify $claim)` replays the chain; auto-apply gated on category-level confidence) → Calibrate. Recursion is bounded — miscalibration triggers reduced ambition, not unbounded growth.

**The emo, concretized**. Rule-Author Agent (LLM driving a tool surface) is one realization. CONSULT/MUTATE/FINALIZE was empirical — successful runs had several-times-more CONSULT than MUTATE (reasoned *with* Noemar, not over it). Stable pattern: neural proposal → symbolic verification → evidence-stamped feedback. Everything else in flux.

**Runtime plurality**. Noemar is one implementation. Other archetypes: PIM-targeting (Goertzel/Tachyum), embedded (light embs), verifier-optimized. Conformance via public test atoms in synart. Runtime source lives in `&core.library.runtime.*` — synome funds its own substrate research from value captured by substrate use.

## §5 RSI: two orthogonal axes

**Meta-depth** (synomics): 0 raw knowledge → 1 using → 2 pattern-mining strategies → 3 meta-strategies (recursive). **Autonomy scope** (Noemar):

| Level | What updates | Profile |
|---|---|---|
| L1 | belief strengths/confidences as evidence arrives | always on |
| L2 | the system's own prediction-accuracy calibrations | low; fully audited |
| L3 | inference rules, regression-gated in staging | moderate; current first instance |
| L4 | runtime source under constrained patch vocabulary | high; gated on L2 calibration above threshold |

A capability has both axes. Current Rule-Author Agent: meta-depth 2, scope L3. Synomic inertia ossification gradient applies to both axes — deeper meta-depth and higher autonomy scope ossify slower, require more evidence.

## §6 Lift, meta-lift, weakness

**Lift = what cognition leaves behind that makes future cognition easier.** Mass noun, generated not declared. Around any primitive: synlang elaborations, worked examples, derived variants, PLN reliability beliefs, calibration data, dispatch meta-rules, provenance, catalogued failure modes.

> Ground gives reality contact. Lift gives leverage. Meta-lift makes leverage compound.

**Lifted vs grounded** is one axis, narrower than lift — both kinds can have or lack lift. Mature pattern: important primitives exist in both forms (fast grounded + lifted elaboration); relationship temporally contingent (verify at compilation, recompile when lifted has moved). **False lift**: stale docs, overfit benchmarks, decorative reasoning traces, uncalibrated confidence, premature abstractions, dead variants. Target: **net lift after costs**.

**Opaque grounded primitives** (LLMs, neural matchers, GPU kernels, JIT'd paths) need lift, but it's **mostly empirical**: calibrate per context, lift the dispatch, wrap with checks, treat outputs as candidate lift not facts.

**Meta-lift = lift pointed at the lift-generating machinery.** Six verbs: generate, allocate, test, adapt, compress, reuse. Lift on roots beats lift on leaves. CS pattern: **self-hosting** (gcc, Lisp, Smalltalk, PyPy). > **RSI is lift learning to make better lift.** Aspiration: **synlang all the way down** — unlifted floor as low as possible; failure mode = glass ceiling at substrate boundary. Three roles: researchers seed a minimum viable core; environments grow lift through dynamic loops; the system generates most lift via derivation/calibration/variant proposals.

**Weakness (Goertzel quantale)** = the cost-algebra: prefer least-contrivance structure that does the work, in the cost algebra appropriate to the domain. Three orthogonal channels:

| Channel | Measures | Lift form |
|---|---|---|
| Evidential | predictive distinctions data warrants | calibration, predictions vs outcomes |
| Cultural | representational distinctions in accepted language | synlang elaborations, derived variants |
| Pragmatic | distinctions that change action/outcome | dispatch rules, when-to-invoke meta-rules |

Composition: `W(g∘f) ≤ W(g)⊗W(f)`. **Budget-capped weakness** is the typed home for empirical lift around opaque primitives ("cheapest reconstruction under the computational regime"). > Lift is what to grow. Weakness is how to weigh it. Meta-lift is learning to weigh better.

---

## Key vocabulary

Originating in this dir (concepts defined elsewhere just referenced):

- **probabilistic-mesh.md**: probabilistic mesh; evidence axiom; fudge method; synomic inertia (canonical with security-and-resources.md); negative inertia; crystallization interface (canonical home of the concept here too).
- **security-and-resources.md**: cancer-logic; fractal security pattern; adversarial ossification; intent-as-asymmetric-evidence; faith-in-the-seed.
- **noemar-substrate.md**: canonical home for synart / telart / embart trio; telseed (bootstrap package, not a packaged KB); Noemar (runtime); Space (metagraph store, three-layer query resolution); delta method (first-order PLN confidence propagation via partial derivatives); provenance disjointness; protocol system (head-symbol dispatch to PLN/Graph/SMT/SymbolicMath/Validation experts); epistemic cycle (six stages); Rule-Author Agent / CONSULT-MUTATE-FINALIZE (illustrative first emo); meta-depth × autonomy-scope two-axis RSI.
- **retrieval-policy.md**: retrieval-policy invariants (five hard constraints); risk-gates-authority.
- **lift.md** (canonical home for the lift vocabulary): lift; meta-lift; false lift; lifted vs grounded; opaque grounded primitive; net lift after costs; weakness (Goertzel quantale); three channels (evidential / cultural / pragmatic); budget-capped weakness; synlang-all-the-way-down; self-hosting.

## Cross-references

- `core-concepts/dual-architecture.md`, `crystallization-interface.md`, `ossification.md`, `synomic-inertia.md`, `cancer-logic.md`, `truth-values.md`, `dreamer-actuator-split.md`, `rsi.md`, `rsi-risk-convergence.md`, `artifact-hierarchy.md`
- `macrosynomics/synome-layers.md` — Layers 1+2 synart definition; Language-Intent-as-security-surface
- `macrosynomics/beacon-framework.md` — action-side counterpart
- `neurosymbolic/neuro-symbolic-cognition.md` — cognition loop running on this substrate; emo as opaque grounded primitive
- `neurosymbolic/live-graph-context.md` — concurrent-access snapshot semantics for multi-emo reads
- `neurosymbolic/attention-allocation.md` — attention-as-mesh-pattern with `(s,c)`
- `synoteleonomics/synomic-game-theory.md`, `recipe-marketplace.md`, `dreamer-perspective.md`, `actuator-perspective.md`, `teleonome-economics.md`
- `noemar-synlang/synlang.md` — language reference (lives there, not here)
- `noemar-synlang/topology.md`, `scaling.md`, `telseed-bootstrap-example.md`

## File map

| File | What's in it that the summary doesn't have |
|---|---|
| `probabilistic-mesh.md` | Detailed crystallization-interface ASCII diagram; full RSI loop / cross-layer table; dreamer connection (validation model: continuous hypothesis testing IS validation, dreamart-design-is-itself-evolved, bandwidth limiter as defensive); concurrent-access semantics narrative; full inertia treatment (institutional credibility, governance weight, temporal stability, progressive edge-case closure, regime-change defense detail, adversarial-ossification defense). |
| `retrieval-policy.md` | Risk-tier table verbatim; full degrees-of-freedom enumeration; "framework holds it together; RSI makes it better" framing. |
| `security-and-resources.md` | Per-layer security checklist for all five layers (Layer 1–5 questions); full pre-action resource-discipline checklist; review-tax math; constraints-as-features rationale; full self-analysis-and-inner-enforcement layer table; immutability-as-equilibrium argument; full fractal-security table at three scales (neural net / teleonome / synome). |
| `noemar-substrate.md` | Browser-bootstrap analogy; full 7-stage bootstrap arc; per-tier telart sub-Space breakdown (telgate / alpha-store / call-out-services / strategy-config / dreamart / experience / endowment-record); resilience model loss/recovery table (5 scenarios); alignment-implication trio (commons gravity / rogues need synart / founder-as-installer); what's-still-being-designed roadmap. |
| `lift.md` | Lifted/grounded contrast table; full opaque-grounded discipline (calibrate per context / lift dispatch / wrap with checks / treat outputs as candidate); self-hosting CS-name detail (gcc/Lisp/Smalltalk/PyPy); compression-as-dual-move + lift-cycling; pave-the-cowpath gating; six meta-lift verbs with one-line each; three-roles model (researchers seed / environments grow / system generates); product-quantales detail; canonical "where this connects" table. |
