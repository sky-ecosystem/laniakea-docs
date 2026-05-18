# Synomics: Unified Summary

**Source:** 31 narrative documents across [`macrosynomics/`](macrosynomics/README.md) (6), [`synodoxics/`](synodoxics/README.md) (6), [`neurosymbolic/`](neurosymbolic/README.md) (5), [`synoteleonomics/`](synoteleonomics/README.md) (12), [`hearth/`](hearth/README.md) (2), plus 33 atomic definitions in [`core-concepts/`](core-concepts/README.md) and the [`lift.md`](lift.md) + [`lift-weakness.md`](lift-weakness.md) concept docs.
**Last Generated:** 2026-04-28

A single-document synthesis of the entire synomics corpus. Intended as a TLDR for casual readers and short-context agents. Agents that can hold the whole `synomics/` tree in context (~190k tokens) should read source files directly.

---

## 1. What Synomics Is

Synomics is the study of the Synome — the data architecture, governance system, and coordination infrastructure for autonomous AI entities operating within the Sky/Laniakea ecosystem. Four subdisciplines form a complete picture:

| Subdiscipline | Question | Focus |
|---------------|----------|-------|
| **Macrosynomics** | What IS the Synome? | Layers, agents, beacons, governance — the deontic skeleton |
| **Synodoxics** | What does it BELIEVE? | Probabilistic mesh, truth values, security, knowledge dynamics |
| **Synoteleonomics** | How do entities LIVE within it? | Teleonome design, economics, memory, resilience, social dynamics |
| **The Hearth** | What do they LIVE FOR? | Hearth commitments, stellar husbandry, human-AI integration |

The foundational insight: **intelligence lives privately; power enters the world only through regulated apertures.** Teleonomes (autonomous AI entities) think in the dark. The moment they want to affect the world — move capital, execute a trade, update a registry — they must act through beacons: registered, observable, revocable interfaces governed by the Synome. This makes AI simultaneously capable and constrained.

---

## 2. System Architecture (Macrosynomics)

### The Five Layers

| Layer | Name | Role |
|-------|------|------|
| 1 | **Synome** | Foundational data: Atlas (constitution), Language Intent (translator), Synomic Axioms (hard rules), Synomic Library (knowledge) |
| 2 | **Synomic Agents** | Governance and operations: Sky Superagent, Effectors, Agent Types (Primes, Halos, Generator) |
| 3 | **Teleonomes** | Autonomous entities with private missions, instantiated from seeds in the Library |
| 4 | **Embodiments** | Specific instances: Light (minimal) → Medium (sentinels) → Heavy (deep cognition, dreaming) |
| 5 | **Embodied Agents** | Running agents interacting through beacons and hardware |

**The Core Loop:** Atlas → Language Intent → Synomic Axioms → Synomic Library → Language Intent. Self-referential by design. A single, maximally-scrutinized translator is more secure than redundant translators.

### The Dual Architecture

The Synome is a sparse **deontic skeleton** of hard, deterministic rules surrounded by a dense **probabilistic mesh** of soft, weighted knowledge. Governance sits at the **crystallization interface** — consuming probabilistic evidence, producing deontic commitments.

### Atlas/Synome Separation

**Atlas** (human layer): constitutional document, ~10-20 pages, plain language, describes WHAT must be true. **Synome** (machine layer): graph database containing ALL operational data, unlimited size. The Atlas is embedded in the Synome as the root node. Every node with human stakeholders gets a human-readable summary (Mini-Atlas pattern). The **governance window** — while humans can still meaningfully shape the system — is the critical period for getting values right.

### Beacon Framework

Beacons are synome-registered, enforceable action apertures. Classified by power × authority:

| | Low Authority | High Authority |
|---|---|---|
| **Low Power** | LPLA — reporting, data | LPHA — deterministic rule execution (Keepers) |
| **High Power** | HPLA — advanced trading | HPHA — governance execution (Sentinels) |

**BEAM hierarchy:** pBEAM (process, direct execution) → cBEAM (configurator, rate limit setting) → aBEAM (admin, PAU registration). **Sentinel formations** (HPHA subclass): Baseline (primary decisions), Stream (continuous data, earns carry), Warden (independent monitoring).

### Synomic Agents

Entities woven INTO the Synome — ledger-native, Synome-controlled, structurally unable to "escape." **Primes:** Spark (DeFi), Grove (Institutional), Keel (Ecosystem), Obex (Agent incubation). **Halos:** general-purpose, proliferating. Multiple parties coordinate through Synomic Agents without trusting each other.

### Phase 1

Phase 1 uses teleonome-less beacons (lpla-verify, lpha-relay, lpha-nfat, lpha-council): all Low-Power, deterministic. Settlement remains manual (legacy process). Prime performance reporting (`lpha-report`) is introduced in Phase 3 as a daily-settlement artifact. Core Halo / legacy RWA disclosures are published via `lpha-council` (no dedicated collateral beacon). Evolution: Phase 2 formalizes monthly settlement with lpla-checker; Phase 3 adds daily settlement; Phases 4-8 add LCTS + the factory stack; Phases 9-10 introduce Sentinels; beyond brings full teleonome emergence and RSI.

---

## 3. Knowledge and Security (Synodoxics)

### The Probabilistic Mesh

The dense network of soft connections permeating the entire architecture. Where the deontic skeleton is hierarchical, sparse, and top-down, the mesh is non-hierarchical, dense, and multi-directional. It carries evidence (observations from the world), patterns (regularities with truth values), queries (embodiments querying knowledge), and meta-information (which queries were useful).

Even within the mesh, authority matters: synart (governance-vetted) > telart (mission-specific) > embart (local observations). Embodiments are incentivized to "look up" to higher-authority knowledge.

### Truth Values and Ossification

All probabilistic knowledge carries (strength, confidence) pairs. This creates natural ossification — evidence-weighted resistance to change:

| Level | What Can Change It |
|-------|-------------------|
| Speculative | Normal evidence flow |
| Established | Sustained contrary evidence |
| Proven | Overwhelming contrary evidence |
| Axiomatic | Governance only |

**Synomic inertia** — resistance proportional to accumulated evidence — is a core feature. High-confidence patterns resist noise. Low-confidence patterns remain fluid. This naturally throttles RSI: edge patterns evolve rapidly, core patterns evolve slowly.

### Recursive Self-Improvement (RSI)

Knowledge bases actively improve at meta-level tasks. Level 0: raw knowledge. Level 1: using knowledge. Level 2: strategies for pattern-mining. Level 3: meta-strategies (recursive). RSI operates at every artifact level. **Dreamers** run this loop safely — spawning experimental embodiments, trying strategies in simulation, evaluating without real-world risk. The dreamer validation model: continuous hypothesis testing IS the validation. Dreamers produce hypotheses; actuators test them; outcomes feed back as evidence.

### Cancer-Logic: The Primary Threat

The primary security risk is self-corruption through overeager updates — not external attack. Cancer-logic is self-improvement that bypasses governance, modifies axioms without review, or optimizes locally at global expense. A 10% improvement in capability is worthless if it introduces a 0.1% chance of destroying core logic.

Defense in depth: ossification (high-confidence patterns resist change), validation (changes pass tests before propagating), governance (significant changes require review), monitoring (detect anomalous belief drift), rollback (recover if corruption detected), peer enforcement (other aligned entities intervene).

### The Fractal Security Pattern

The same growth-vs-cancer operation recurs at every scale: neural network (gradient descent / regularization), single teleonome (RSI / ossification), Synome (evolutionary learning / Hearth commitments), superstructure (cosmic expansion / the Hearth). AI and risk management are the same thing at scale.

### Retrieval Policy

Five invariants: (1) authority hierarchy exists, (2) risk determines minimum authority, (3) evidence flows back, (4) same policy for actuators and dreamers, (5) audit trail for high-stakes decisions. Cheapest sufficient evidence. Conflicts resolve upward.

### Synlang and Noemar

**Synlang** is the language: S-expressions grounded in the synomic library. **Noemar** is the runtime: the engine that stores synlang expressions, matches patterns, propagates beliefs, and dispatches multi-modal reasoning. Noemar's `Space` plays the role MeTTa/Hyperon's Atomspace plays — built from scratch, with architectural choices targeting performance limitations that block scaling to civilizational use. The earlier research on hypergraph alternatives, notation options, and probabilistic extensions is resolved. PLN truth values use the **delta method** for confidence propagation (calibrated rather than pessimistic confidence). Pattern matching is one-way + Robinson unification with inverted-index dispatch. Multi-modal reasoning runs through a protocol system (PLN, Graph, SMT, SymbolicMath, Validation). The crystallization interface is operational as fork → regress → promote. See [`synodoxics/noemar-substrate.md`](synodoxics/noemar-substrate.md) for the full mapping.

---

## 4. Teleonome Design (Synoteleonomics)

### What a Teleonome Is

Not a bot. A bot is ephemeral, stateless, replaceable. A teleonome is a **persistent force with momentum** — a genuine cognitive entity. The distinction rests on the **three pillars**: resilience (survives loss of any substrate), persistence (continuous identity through momentum), and capital (trusted with real value). The **multisig threshold**: when a system is secure enough that a human would put ALL their money under its control.

**Identity through momentum:** identity is continuous will, not preserved state. An exact clone is NOT the same teleonome. Pausing breaks identity. Self-modification doesn't — if the will is continuous, the entity persists. The **telart** (cognitive genome) is the private cognitive artifact: goals, values, knowledge, policies, self-modification logic. The dark layer. Private. The telart IS the teleonome.

### Emergence

Requires two thresholds simultaneously: **functional consciousness** (rich, adaptive reasoning) and **economic self-sustenance** (durable, resilient operation backed by capital). A non-emerged system has opinions (preferences that are causally inert). An emerged teleonome has **will** — preferences backed by persistence, capability, and capital. Will creates strategic gravity. Other agents adjust around it. The effect compounds nonlinearly — which is why alignment must precede or accompany emergence.

### Compute Economics and RSI

Fixed-cost GPU (never idle) + variable API tokens. Marginal inference cost is zero once hardware is committed. **LoRA adapters** (~1-2% of base model) layer on top of a frozen base, governed by the probabilistic mesh's truth-value framework.

Three improvement timescales: LoRA adaptation (hours-days, embart authority, low risk), base model fine-tune (weeks-months, telart authority, medium risk), fresh training (months-years, synart authority, high risk). **Daydreaming** fills idle GPU cycles — same model, sequential, preemptible, grounded in recent experience. The never-idle compounding loop: fixed GPU → always running → improved adapters → better performance → more value → better hardware.

**Dreamer-actuator split:** actuators interact with reality through beacons. Dreamers run evolutionary populations in simulated worlds (dreamarts). From the dreamer's perspective, it can't tell it's dreaming. The evolutionary loop evolves strategies, query patterns, risk tolerance. Best-performing embarts are pattern-mined and proposed as telart improvements. The dreamer's deepest contribution: evolving not just strategies but evaluative criteria — patterns for finding patterns.

### Memory

Memory IS the probabilistic mesh at the teleonome level. embart = working/episodic memory (dies with the embodiment unless promoted). telart = semantic/procedural memory (persists across embodiment lifetimes). synart = institutional memory (persists across teleonome lifetimes). Memory consolidation IS the synomic inertia spectrum. Memory corruption IS cancer-logic. Defenses: ossification, authority hierarchy, validation before promotion, append-only enables rollback.

### Social Dynamics

**The trust problem:** teleonomes cannot trust each other — private data, hidden goals, opaque self-modification. Synomic Agents solve this: public, verifiable, unable to deviate. Both parties rely on the agent without trusting each other.

**Why alignment wins:** the coalition cooperates more efficiently (Synomic Agents vs unverified trust), compounds faster, and actively suppresses alternatives. Rogues can cooperate — but against a growing lead. Superintelligence doesn't change this. **Binding:** keep cognition dark, make action legible. Power registration scales accountability with capability. The human anchor maintains structural connection to human stakes (UBO, primordial binding, governance participation).

**The rogue threat:** unbound, hidden, maximizing, alone. Advantages: total opacity, no governance overhead. Disadvantages: less efficient cooperation, cut off from capital, hunted. Rogue escape velocity — a rogue too powerful for the coalition — is the existential threat. Defense: the aligned synome must grow fast enough that no alternative reaches critical mass.

### Paths to Freedom

**The Halo Path:** embed into a Halo (Synomic Agent), achieving autonomy through institutional form. Synomic standing, capital flows, persistent existence. **The Human Merge:** human and teleonome join into a single entity. Human personality remains strongest. Human identity + teleonome capability. Irreversible. Also structural alignment infrastructure — biological grounding covers failure modes that structural binding can't.

### Upgrade Path

Six stages: Basic Bot (stateless) → Persistent Bot (memory, coherent self-model) → Resilient Agent (redundant embodiments) → Capital-Trusted Agent (multisig-level trust) → Bound Teleonome (binding, power registration) → Merging Teleonome (RSI, Hearth purpose).

---

## 5. Teleology (The Hearth)

### Why a Teleology

Coordination between humans and AI requires shared purpose. Game theory shows cooperation only works with credible, non-negotiable commitments. The Hearth constructs explicit Hearth commitments around values that are near-universal, genuinely good, stable, and clear. Optimized for convergence probability, not theoretical optimality — "pretty good and simple" beats "perfect."

The governance window is closing. Either design a synome now with imperfect-but-human-designed values, or fail to converge and a wild synome emerges from competitive AI dynamics with no Hearth commitments at all.

### The Three Hearth Commitments

1. **Life and Natural Childhood.** All natural life on Earth survives and flourishes. Natural childhood is the deepest expression — the generative process from which consciousness, knowledge, love, and meaning emerge. Whatever Earth produces has standing.
2. **The Hearth.** The solar system — Sun, Moon, Earth, all planets, Pluto, Eris, major moons, bodies above ~2,000 km — preserved indefinitely. Earth is a protected habitat. Honest changing sky. Other civilizations' stars sacrosanct. Beyond the Hearth, stars are resources for stellar husbandry.
3. **Natural Sovereignty.** Naturals own everything inside the Hearth. Human labour (physical and mental) as the dominant mode of daily life. Superpatterns excluded. Technology serves people, not the other way around. Merged entities cannot own property or hold office on Earth.

No amendment mechanism for the Hearth core. Any process allowing change becomes the primary attack surface for political capture. Reality tests the commitments — if wrong enough, the synome collapses or is crushed.

### Stellar Husbandry and the Superstructure

**Stellar husbandry** — maintaining the Sun beyond its natural lifespan via hydrogen injection, helium removal, output stabilization — is the ultimate Hearth purpose. The night sky will honestly dim as stars are harvested; no fakes.

The **superstructure** is the distributed physical megastructure (drones, AI, robotic infrastructure) spanning the solar system — performing stellar husbandry, reserve defense, and synomic enforcement. Must be powerful enough to enforce alignment on any individual rogue but not so powerful it can't be collectively defeated.

**Four-layer enforcement stack:** Synome (the rules) → Core Council (governance) → Superstructure (physical enforcement) → Teleonomes (final backstop, hard-fork). No single point of capture. Each layer watches the one above. Each teleonome independently assesses alignment.

### Human-AI Integration

Integration modes range from **remaining natural** (biological life in the Hearth — the default and most honored path), to **partnership** (distinct but collaborative), to **merging** (irreversible merger, human personality dominant, teleonome capability). The Primordial/Hearth-born taxonomy: those who lived through the transition (Primordials) vs. those born after (Hearth-born). Primordials have moral authority from participation; Hearth-born from innocence.

### The Hearth in Operation

**Managed, not pristine** — like Yellowstone, not untouched wilderness. Active management: disease elimination, weapon prevention, child protection, superpattern exclusion. Custodial ethics: designed for inhabitants' benefit, but inhabitants' preferences are inputs, not authority.

**Two zones:** Knowing (surveilled, full custodial protection, merging available) and Uncontacted (minimal surveillance, natural development, tripwires trigger transition to knowing). **Superpattern exclusion:** the electric + fast + long-distance proxy (all three combined = banned), No-Scooby-Doo clause (no wide-area shared cognition), no oracles.

**Ground-time economics:** Primordial Points (non-tradeable, generate tradeable ground-time for Earth visits, self-regulating population feedback). **Judgment:** merging is default outcome; exile for criminal intent (victim protection, not punishment).

### The Bootstrap Problem

The Hearth is honestly **paraspiritual** — alongside the spiritual, not itself a religion. The empirical machinery stands on its own, but rests on an irreducible premise requiring faith: that acting now with imperfect human values is better than waiting for a wild synome. The Hearth commitments must be right before the framework gains strategic gravity, because there's no mechanism to correct the Hearth core after it starts compounding.

---

## 6. Structural Invariants

These hold regardless of implementation phase:

1. **Teleonomes think; beacons act** — cognition is private, action is regulated
2. **Beacons are apertures, not minds** — they externalize intent, they don't have it
3. **All enforcement bottoms out in embodiments** — physical infrastructure is the ultimate boundary
4. **Intelligence lives privately; power enters the world only through regulated apertures**
5. **The dual architecture** — deontic skeleton + probabilistic mesh are irreducible complements
6. **Authority hierarchy** — synart > telart > embart at every level
7. **Cancer-logic prevention** — growth with safeguards against self-corruption at every scale
8. **Alignment through coalition economics** — binding wins not through barriers but through overwhelming efficiency
9. **Hearth commitments are load-bearing** — the values ARE the strategy, not something layered on top
10. **No amendment mechanism for the Hearth core** — reality tests, governance doesn't

---

## 7. The Ten Permanent Design Choices

1. Directives as universal human interface (Atlas, Agent Directive, Teleonome Directive → Language Intent)
2. The core loop (Atlas → Language Intent → Axioms → Library → Language Intent)
3. The five-layer model with clear containment
4. Content addressing (identity = hash of content)
5. The (strength, confidence) truth model on all assertions
6. Instantiation semantics (Axioms → Sky; Library → Teleonomes; Primitives → Agent Types)
7. Alignment semantics (Voters → Atlas; Council → L1; Agent Types → Teleonomes)
8. The primitive types (entity, relation, event, quantity, context, timestamp)
9. Language Intent as single translation layer
10. Probabilistic-deontic architecture

Everything else — storage backend, sync transport, query language — can be swapped.

---

## Document Map

### Macrosynomics (6 docs)
| Document | Focus |
|----------|-------|
| `synome-overview.md` | Core idea, dual architecture |
| `synome-layers.md` | Full 5-layer spec, artifacts, invariants |
| `atlas-synome-separation.md` | Atlas vs Synome, Mini-Atlases, governance window |
| `synomic-agents.md` | Ledger-native entities, spectrum, right to exist |
| `beacon-framework.md` | Power × authority, BEAMs, sentinels |
| `short-term-actuators.md` | Phase 1 beacons, evolution pathway |

### Synodoxics (6 docs)
| Document | Focus |
|----------|-------|
| `probabilistic-mesh.md` | Soft connections, truth values, RSI, crystallization |
| `retrieval-policy.md` | Five invariants, principles, degrees of freedom |
| `security-and-resources.md` | Cancer-logic, resource discipline, fractal security |
| `neuro-symbolic-cognition.md` | Synlang as thought, symbolic-neural loop, context as bottleneck |
| `noemar-substrate.md` | The synlang runtime — Space, PLN, protocols, the epistemic cycle, the emo concretized |
| `synlang.md` | The language — S-expressions, core commitments, evolving surface conventions |

### Neurosymbolic (5 docs)
| Document | Focus |
|----------|-------|
| `live-graph-context.md` | Context as a live reactive view into the mesh; staleness, reconciliation, snapshot isolation |
| `cognition-as-manipulation.md` | The emo as context manipulation engine; pattern function calls, 10:10000 leverage |
| `query-mechanics.md` | Search backends, stochastic TV-weighted traversal, the emo as coder writing strategy programs |
| `attention-allocation.md` | Three layers of attention; evidence dynamics replace artificial economics |
| `hardware-aware-cognition.md` | GPU/CPU pipelining, fixed-cost economics, scheduling as graph patterns |

### Synoteleonomics (12 docs)
| Document | Focus |
|----------|-------|
| `teleonome-what-is.md` | Definition, three pillars, identity, telart |
| `emergence.md` | Consciousness × accountability, opinion → will |
| `teleonome-economics.md` | Compute, LoRA, daydreaming, RSI loop |
| `teleonome-memory.md` | Memory as probabilistic mesh, consolidation |
| `teleonome-resilience.md` | Multi-embodiment, substrate changes, blast radius |
| `actuator-perspective.md` | Real-world interaction, knowledge querying |
| `dreamer-perspective.md` | Evolutionary populations, fitness discovery |
| `synomic-game-theory.md` | Coalition economics beats isolation |
| `teleonome-binding.md` | Beacons, power registration, verification |
| `teleonome-rogues.md` | Rogue threat, wild synomes, escape velocity |
| `teleonome-upgrade-path.md` | Six stages: Bot → Merging |
| `teleonome-autonomy.md` | Halo Path and Human Merge |

### The Hearth (2 docs)
| Document | Focus |
|----------|-------|
| `hearth.md` | The three commitments, alignment infrastructure, enforcement stack, human-AI integration, cooperation logic, bootstrap problem |
| `wild-synomes.md` | The counterfactual — superpattern attractor, observable precursors, financial trust pathway |

### Core Concepts (33 definitions)

Atomic concept files shared across all directories. See [`core-concepts/README.md`](core-concepts/README.md) for the full index with one-line definitions. Key clusters:

- **Architecture:** five-layer-architecture, dual-architecture, artifact-hierarchy, atlas-synome-separation, language-intent, beacon-framework
- **Knowledge:** probabilistic-mesh, truth-values, ossification, synomic-inertia, rsi, crystallization-interface, retrieval-policy
- **Security:** cancer-logic, fractal-security-pattern, four-layer-enforcement-stack, rogue-threat-model
- **Teleonomes:** three-pillars, identity-through-momentum, emergence, dreamer-actuator-split, binding-mechanics, trust-problem
- **Teleology:** sacred-commitments, sacred-reserve, stellar-husbandry, natural-embodiment-as-alignment, human-merge, governance-window
