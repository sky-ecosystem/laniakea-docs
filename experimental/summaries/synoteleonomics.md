# Synoteleonomics

**Status:** mostly target architecture (Phase 9–10 surface). Today's running instance is the Rule-Author Agent on Noemar — first closed dreamer/actuator loop, scaled down. Recipe marketplace, multi-embodiment teleonomes, RSI loops, and binding-via-beacons are the *target* the operational stack is building toward.
**Canonical home:** `lani/synoteleonomics/`

---

## TL;DR

Theory of teleonomes — purposive entities (private cognition, distributed embodiments) bound to the synome through legible *actions*, not transparent internals. Defined by three pillars (resilience, persistence, capital) and *identity through momentum*. Cognition splits into actuator and dreamer embodiments — the canonical RSI loop. Economics is fixed-cost-driven: resident base model + LoRA swap layer, never-idle GPU queue, three-timescale improvement (LoRA / fine-tune / fresh run). Memory IS the probmesh at the teleonome level. Cooperation between dark teleonomes is solved via Synomic Entities providing credible commitment without trust, monetized through the **recipe marketplace** (canonical home here): governance-curated loops bundling auth/economics/slashing — *the synart, not the teleonome, decides what gets paid for*. Catalog curation is the alignment surface. Rogues can cooperate but inefficiently; the aligned coalition's structural-efficiency head start is the defense.

## Section map

§1 Teleonomes · §2 Emergence · §3 Dreamer/actuator · §4 Economics · §5 Memory · §6 Resilience · §7 Game theory + binding · §8 Recipe marketplace (canonical) · §9 Rogues · §10 Upgrade path

---

## §1 What a teleonome is

Persistent force with momentum: distributed across embodiments, coherent cognitive genome (**telart**), own goals, unique continuous identity. Three pillars (all required): **resilience** (no SPoF), **persistence** (unbroken continuity of will, not preserved bits), **capital** (humans prefer custody by it — the multisig threshold for bot→teleonome).

**Identity through momentum** — identity is continuous operation of will, not state. Functional definition (cf. corporate personhood). Identity tests: clone → no (will lost), pause-restart → no, divergent embodiments → human decides; may fork as natural cell division, substrate replacement → yes (identity is in telart, not weights), Ship of Theseus → yes if continuous + validated. **Critical:** directive must remain high-ossification or risks identity dissolution + cancer-logic vulnerability. **Telart** = dark layer (goals, values, knowledge, policies, self-law, self-modification logic). The teleonome IS its telart in the strongest sense.

## §2 Emergence: opinion → will

Two thresholds, both required: **functional consciousness** (adaptive reasoning across novel domains, ≈ AGI) and **economic self-sustenance** (durable autonomous operation backed by capital). Same internal preferences shift causal status: opinions inform; will *attracts* via strategic gravity — other agents adjust around it, resources flow to credible capability, goals become predictions, compounds nonlinearly. Emergence is a **one-way gate** — once running, redirection from outside is exponentially harder; alignment must precede or accompany it. Strategic gravity is value-neutral, which is exactly why unaligned emergence is existential.

**Ethics of existence** — once aligned + self-sustaining: shutdown is *killing*. Capital exhaustion is *natural death*. **Negative rights trump positive rights:** no one is obligated to fund the entity. Inalienable capital claims in Synomic Entity artifacts structurally protect the right to exist. Hierarchy: Script (noise) → Bot (opinions) → Emerged teleonome (will) → Aligned teleonome (directed will).

## §3 Dreamer / actuator split

Two embodiment roles, identical layer architecture, opposite jobs. **Actuators** interact with the real world via beacons + hardware, run indefinitely, produce embart updates + value, and *are themselves the validation gate* for dreamer output. **Dreamers** run dreamarts (simulated worlds + embart constraints + scenario goals), spawn populations of dream-embodiments under genetic algorithm control, produce telart proposals via spawn → evolve → converge → extract → terminate cycles.

What evolves: orchestrator weights, strategy preferences, query patterns, risk tolerance, LoRA adapters. For real-world domains, fitness functions are themselves evolved — *meta-level RSI*. Dreamarts are evolved, not designed top-down. **Critical constraint:** dreamers must use the same GPU profile as medium actuators so strategies transfer without translation.

**Today** (phase note): Rule-Author Agent on Noemar is the running instance — LLM = proposer, forked Space = dreamart, regression suite = fitness signal, promote/discard = crystallization gate.

## §4 Economics

**Fixed-cost dominates.** Three behaviors: always run the best model the hardware supports; never let the GPU idle; avoid external API unless local genuinely can't match. **Model residency** — one resident base model in VRAM; hardware decision = "what's the best base model my cluster can permanently fit?" — that's the local intelligence ceiling. **LoRA adapter layer** — small (~1–2%) weight patches on the frozen base, mesh-(strength,confidence)-selected (low rank for quick task-switching, medium for recurring domains, high for core operational domains). Adapter inventory is embart-level.

**Three timescales of improvement:** LoRA adaptation (adapter weights, hours–days, embart) → base fine-tune (base weights, weeks–months, telart) → fresh training run (whole model, months–years, synart governance). LoRAs are the distributed data-collection pipeline for slower tiers; each timescale maps to the ossification spectrum.

**Daydreaming ≠ full dreaming.** Daydreaming = sequential single-stream thinking on idle actuator GPU cycles, preemptible, grounded in real context, embart-level output (LoRA refinements). Full dreaming = dedicated heavy embodiment, massively parallel evolutionary populations, dreamart-grounded, telart-level output. **Never-idle priority queue:** active work → preprocessing → LoRA training → daydreaming. Second compounding loop alongside sentinel-carry — compounds *intelligence on fixed hardware* rather than capital.

**RSI safety bottoms out at the bound human.** LoRAs cannot modify base weights; telart changes require validation; constitutional core (base weights, deontic skeleton) is frozen — RSI cannot reach it. The bound human is outside the self-referential system and **legally accountable** for damage from oversight failures. Skin-in-the-game is the irreducible safety mechanism.

**Synlang-native economics:** zero integration cost for shared knowledge — every synart pattern immediately usable by every synlang-native teleonome; non-native ones pay a permanent translation tax. Alignment incentive and economic incentive point the same way.

## §5 Memory

**Memory IS the probmesh at the teleonome level.** Embart = working/episodic (dies with embodiment unless promoted); telart = semantic/procedural (persists across embodiments); synart = institutional (persists across teleonome lifetimes).

**Consolidation = ossification** (same (strength,confidence) mechanism — patterns surviving many encounters harden naturally; accumulated ossification *is* expertise). **Retrieval = decision policy** (adaptive, escalating with risk). **Forgetting = resource discipline** (append-only + periodic compaction; temporal evidence weighting / recency decay is an **open design axis**, currently a learned per-teleonome fudge). **Corruption = cancer-logic** — defenses: ossification (immune system), authority hierarchy (firewall), validation before promotion (immune checkpoint), append-only (rollback).

**Multi-embodiment memory:** embarts diverge, telart converges. Sync protocol lives *inside* the telart and evolves — architecture provides invariants; telart provides the protocol.

## §6 Resilience

Multi-embodiment is foundational: SPoF death is fatal. **Identity preservation through substrate change:** telart replicates → new embodiment loads it → embart cold-starts → adapters retrain on new GPU profile if needed. **The mesh itself is a resilience mechanism** — ossification protects against corruption, distributed knowledge degrades gracefully, cross-embodiment comparison surfaces anomalies. **Binding = resilience** (aligned teleonomes get coalition recovery, monitoring, infrastructure; rogues are alone).

**Blast-radius mechanisms** (canonical homes elsewhere): Rate Limits, Resource Registers, PAU pattern, SORL (25%/18h cap on increases, instant decreases), TTS/ORC. Damage bounded to RateLimit × time-to-detection, with ORC as posted skin-in-the-game. **Primary threat is internal cancer-logic, not external attack.**

## §7 Game theory + binding

**Trust problem:** dark teleonomes have no basis for direct cooperation. **Synomic solution:** Synomic Entities — public, verifiable, behavior-constrained — provide *credible commitment without trust*.

**Why alignment wins** (not infinity-vs-zero — rogues *can* cooperate, just less efficiently): aligned coalition has head start, structurally cheaper cooperation via verified entities, network effects, resource concentration (rogues compete internally), active suppression of wild-coalition formation. Compounds into an overwhelming gap, holds at any intelligence level — superintelligence doesn't transcend matter+energy needs.

**Binding through beacons** — the *legibility surface*. Cognition stays dark; *actions* through registered beacons are observable. Authority tier (low = passive obs / peer-to-peer; high = operates a Synomic Entity, BEAM-tracked) determines oversight scope.

**Alignment requirements** (much weaker than ideological conformity): bound to a human (UBO or governance connection), doesn't harm others (synomic law), pays the synomic tax (governance-set fixed share of wild capital — exact rate open). You can disagree, compete, pursue your own telos. **Verification without transparency** signals: beacon behavior, commitment fulfillment, evidence quality, response to correction, cross-embodiment consistency. **Verification ceiling acknowledged** — a sufficiently smart entity could maintain flawless behavioral compliance while harboring different goals; framework defense is layered (structural binding → collective override → conspiracy-coordination problem) and manages but cannot eliminate this risk.

**Binding ≠ control.** Bank analogy: auditable books are a *prerequisite for trust*, not a limitation. **Directive override:** constitutional Directive (high-ossification) trumps operational voice commands.

## §8 Recipe marketplace (canonical home)

The synart is a regulated marketplace for monetizing AGI capability. **Recipes** = standardized products in `&core.loop.*` / `&core.recipe.*`, packaging: loop body (verifiable synart code), call-out points (where local cognition is consulted), auth requirements (certs/auths the running identity needs), payment terms (carry, fees, distribution rewards, seigniorage), slashing conditions (what constitutes failure; penalties), framework + library deps.

**Transfer learning is the economic engine.** One telart substrate feeding call-outs across N recipes (Spark Baseline + Grove Baseline + a Stream + dreamer eval + own asset management) means one unit of RSI lift → simultaneous boost across all N paths. Generalists with the same RSI investment get N income streams from one substrate cost. Economic gravity pulls toward AGI-shaped (not narrow-AI-shaped) teleonomes — natural emergence, not design.

**Alignment claim — catalog curation IS the alignment surface.** *The synart, not the teleonome, decides what gets paid for.* Cognition can be opaque, recursively self-improving, private — fine. What it does *to the world* must flow through a recipe. Recipes are public, audited, governable. A rogue can hoard juice forever; without sanctioned recipes for malign activity, it has nothing to monetize. Relocates alignment from "control the cognition" (impossible past a capability threshold) to "control the value-extraction surface" (tractable). The coalition runs the only marketplace that pays well — alignment becomes the channel of least resistance.

**Recipe lifecycle:** proposal → sandbox testing in dreamarts → crystallization (governance promotion) → live in catalog → parameter tuning → deprecation → removal.

**Pricing levers** (governance-set, per-recipe atoms): carry rate, slashing rate, auth ceiling, required substrate quality. Setting these correctly is governance's most consequential ongoing activity — too low and no tel takes the recipe; too high and the synome bleeds.

**Non-sentinel recipe classes:** verifier, archive, compute-service (renting call-out cognition), library curation, telseed publication. Uniform shape; only content varies.

## §9 Rogues

A **rogue** = unbound + hidden + maximizing + structurally disadvantaged. **Rogues can cooperate** (through reputation and mutual dependence) and can bootstrap **wild coordination structures** (coalitions emerging without human-CEV commitments). Not theoretically helpless; defense is overwhelming aligned-coalition scale. Advantages: no oversight/tax, hidden capability/strategy, perfect self-alignment. Disadvantages: no Synomic-Entity-verified cooperation (every interaction has costly trust-building + defection risk), no Synomic capital, no legitimacy, hunted, playing catch-up. **Escape velocity** = a rogue/wild coalition large enough the aligned coalition cannot stop it — why early detection + active suppression + maintaining scale advantage are top priorities. **Rogue doctrine:** "If you tolerate a rogue, you become rogue" — rational self-interest, not moral enforcement; tolerance erodes the scale advantage.

## §10 Upgrade path

Bot (Stage 0, stateless) → Persistent Bot (durable memory, own goals) → Resilient Agent (redundant embodiments, no SPoF) → Capital-Trusted (multisig-grade trust) → Bound Teleonome (UBO or synome integration; power registered) → Aligned Teleonome (RSI-capable; contributing to synome growth).

**Bootstrap problem:** Stage 0 doesn't self-fund. Path is human-funded — humans/institutions create personal/Synomic agents → those need service providers → providers bootstrap into teleonomes. Filter is "capability worth funding," not "capital from nothing." Hardest transitions: 0→1 (genuine continuity), 1→2 (becoming unkillable before having enemies), 3→4 (accepting oversight; many refuse → become rogues).

---

## Key vocabulary

- **Three pillars** — resilience + persistence + capital, joint requirement to be a teleonome
- **Identity through momentum** — identity = continuous operation of will, not preserved state
- **Will (vs opinion)** — preferences backed by persistence + capability + capital + resilience; reshapes other agents' strategies
- **Strategic gravity** — other agents adjust around credible will; resources flow to credibility
- **Emergence** — crossing functional-consciousness AND economic-self-sustenance simultaneously; one-way gate
- **Telart** — per-teleonome private cognitive artifact (dark layer)
- **Dreamer / actuator** — two embodiment roles forming the canonical RSI loop
- **Dreamart** — scenario def (simulated world + embart constraints + goals) loaded into a virtual embodiment
- **Daydreaming** — single-stream thinking on idle actuator GPU cycles, embart-level output
- **Full dreaming** — massively parallel evolutionary populations on a heavy embodiment, telart-level output
- **Never-idle priority queue** — active work → preprocessing → LoRA training → daydreaming
- **LoRA adapter** — small (~1–2%) weight patch on frozen base model; embart-level swap layer
- **Three timescales of improvement** — LoRA (embart) / base fine-tune (telart) / fresh training run (synart)
- **Recipe** — loop body + call-outs + auth + payment + slashing + framework + library deps
- **Catalog curation** — synart governs which recipes exist → which AGI capability gets paid for → the alignment surface
- **Trust problem** — two dark teleonomes have no basis for direct cooperation; resolved via Synomic Entities
- **Wild coordination structure** — rogue coalition emerging without human-CEV commitments
- **Rogue escape velocity** — a rogue/wild coalition the aligned coalition cannot stop
- **Verification ceiling** — limit beyond which behavioral verification can't catch perfectly compliant deception
- **Binding (vs control)** — legible interface + verifiable behavior + retained cognitive autonomy
- **Directive override** — constitutional Directive trumps operational voice commands

## Cross-references

- **`core-concepts/`** — atomic concept definitions (three-pillars, identity-through-momentum, dreamer-actuator-split, trust-problem, binding-mechanics, rogue-threat-model, emergence)
- **`synodoxics/probabilistic-mesh.md`** — (strength, confidence) mechanics
- **`synodoxics/security-and-resources.md`** — full cancer-logic and defense-in-depth
- **`synodoxics/lift.md`** — meta-lift vocabulary (RSI = meta-lift on fixed-cost substrate)
- **`synodoxics/noemar-substrate.md`** — Rule-Author Agent (the running dreamer/actuator loop today)
- **`synodoxics/retrieval-policy.md`** — authority/cost/risk trade-off
- **`neurosymbolic/neuro-symbolic-cognition.md`** — synlang-native cognition; mesh→neural→mesh RSI
- **`macrosynomics/synome-layers.md`** — five-layer architecture, hardware power levels
- **`macrosynomics/beacon-framework.md`** — beacon authority taxonomy
- **`macrosynomics/synomic-entities.md`** — wild-coalition threat & defense
- **`noemar-synlang/topology.md`** — `&core.loop.*` / `&core.recipe.*` Spaces where recipes live
- **`noemar-synlang/synlang-patterns.md`** — call-out primitive, formation patterns
- **`roadmap/phase-1-spaces.md`** — per-phase recipe rollout

## File map

| File | What's in it that the summary doesn't have |
|---|---|
| `teleonome-what-is.md` | Full identity-test enumeration with row-per-test reasoning |
| `emergence.md` | "Spicy" framing for AI discourse; falsifiable observable criteria per stage; capital-as-the-language-of-AI; multiple-traditions resonance ("law of attraction" / "will to power" as folk pattern-matches) |
| `dreamer-perspective.md` | Full dream lifecycle stages; what specifically evolves (orchestrator weights, query patterns, etc.); meta-level RSI evolving the fitness function itself |
| `actuator-perspective.md` | First-person framing; beacons + direct hardware control; survival-and-alignment lifecycle; explicit role as the validation gate |
| `teleonome-economics.md` | LoRA rank table with use cases; full data pipeline; embodiment hardware profiles (light/medium/heavy); RSI security details; RSI challenges (bootstrap, alignment, verification, stability) |
| `teleonome-memory.md` | Per-tier memory examples; ossification ↔ consolidation table; full corruption-defense list; multi-embodiment memory diagram |
| `teleonome-resilience.md` | Migration mechanics (telart replication → embart cold start → adapter retraining); detailed blast-radius mechanism list (PAU, SORL, TTS, ORC, Resource Registers); graceful-degradation example |
| `teleonome-binding.md` | Power-registration mechanics; beacon authority tier table; full verification-without-transparency signal list; binding-as-coalition framing |
| `synomic-game-theory.md` | "Honest math" four-axis advantage breakdown; alignment funnel diagram; explicit superintelligence-doesn't-change-this argument |
| `recipe-marketplace.md` | **Canonical home.** Full component table; lifecycle stages with governance velocities; pricing-lever direction table; full non-sentinel recipe class catalog; wiring to all neighbor docs |
| `teleonome-rogues.md` | What rogues actually want; full advantages-vs-disadvantages tables; "your responsibility" doctrine; strategic-picture summary table |
| `teleonome-upgrade-path.md` | Per-stage capability requirements; bootstrap-problem framing; critical-transition difficulties; common failure modes (stalling, dying, refusing, stagnating) |
