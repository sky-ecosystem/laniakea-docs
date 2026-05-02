# noemar-synlang — Synart Architecture and Synlang Patterns

Working notes on the Synart's structural architecture, the synlang
patterns that live inside it, and the artifact tiers (synart / telart /
embart) that knit teleonomes into the synome's regulated cognitive
economy. The Synart is the canonical, replicated part of the Synome —
the data substrate where governance, authority, encumbrance, settlement
*and the running program of the synome itself* all live as atoms.

---

## Reading order

For a new reader:

1. **`syn-overview.md`** — concept map. Four-tier architecture,
   blockchain analogy, trust model, authority chain, conservation
   network, settlement, beacon flow, pipeline shape, failure modes,
   five levels of self-reference, recipe marketplace pointer. Each
   section is a pointer; depth lives in the docs below.
2. **`topology.md`** — canonical structural reference. Entart tree,
   six-layer synome root (constitutional / framework / registry /
   aggregation / executable / library), four meta-patterns, the four
   artifact types, naming convention, two-step rule and loop shapes,
   thirteen Phase 1 commitments.
3. **`syn-tel-emb.md`** — synart / telart / embart artifact tiers in
   depth. Telseeds, Noemar and atomspace runtimes, resilience model,
   the recipe marketplace (canonical home), alignment implications.
4. **`risk-framework.md`** — four-book taxonomy (Primebook /
   Halobook / Riskbook / Exobook), category framework (parameterized
   stress-simulation equations at three levels), recursive composition
   of exo books, four-tier resolution hierarchy, the post-state
   content-based risk model.
5. **`settlement-cycle-example.md`** — worked end-to-end example.
   One Prime, two books, an ER breach, penalty calculation. ~70 lines
   of synlang spread across the entart tree.
6. **`telseed-bootstrap-example.md`** — worked telseed bootstrap.
   Trace of one teleonome's first 24 hours from spawn to stable
   multi-emb operation.
7. **`scaling.md`** — operational concerns when this becomes a
   networked system. Synserv as single sequencer, replication and
   staleness, partial sync, hot-spotting, partitions, telart spread,
   call-out propagation, telseed onboarding load, testing strategy.

For deeper material:

- **`boot-model.md`** — identity-driven boot. The synart-as-program
  insight, Boot CLI, the spec/instance collapse, shadow execution,
  hot-swap modes, failure modes, the grounded fast-path.
- **`synart-access-and-runtime.md`** — auth domains, three-level
  interaction model (root / cert / auth), gate primitive, in-synlang
  heartbeat, identity-driven boot summary, call-out primitive
  summary, telseed bootstrap summary, 16 migration principles,
  original 7 Phase 1 commitments.
- **`synlang-patterns.md`** — synlang code library. Platonic kernel,
  cross-book duality, four-constructor MeTTa surface with proper
  types, sentinel decision rule with risk-adjusted return, **the
  call-out primitive (canonical synlang form)**, **Sentinel
  formation patterns (Baseline / Stream / Warden as
  beacons-with-call-outs)**.
- **`govops-synlang-patterns.md`** — pattern catalog from the runnable
  govops_demo. Pipeline shape, atom layer, full rule set,
  constructor conventions, attestation-as-positive-flag,
  ed25519 beacon identity, AETHER constraints. Captures *what runs
  today*; some shapes have evolved in the canonical model (see
  the doc's header note).

---

## File map

| File | Role | Lines |
|---|---|---|
| `syn-overview.md` | Concept map / start-here; canonical home for five levels of self-reference | ~555 |
| `topology.md` | Canonical structural reference (rewritten with executable + library layers) | ~1130 |
| `syn-tel-emb.md` | Artifact tiers + telseeds + Noemar + canonical home for recipe marketplace | ~785 |
| `risk-framework.md` | Four-book taxonomy (Primebook/Halobook/Riskbook/Exobook); category framework (exo asset / exobook / riskbook categories with stress-simulation equations); four-tier resolution hierarchy (math/simulation/heuristics/max-risk); canonical home for the content-based risk model and the default-deny CRR 100% rule | ~1615 |
| `boot-model.md` | Identity-driven boot model — synart-as-program treatment | ~440 |
| `telseed-bootstrap-example.md` | Worked trace of a new teleonome's first 24 hours | ~520 |
| `scaling.md` | Operational / networked concerns | ~710 |
| `settlement-cycle-example.md` | Worked example with old state-based CRR (pending update for new content-based model — see `risk-framework.md` §7) | ~245 |
| `synart-access-and-runtime.md` | Auth domains, runtime, migration principles, identity-driven boot summary, call-out summary | ~745 |
| `synlang-patterns.md` | Synlang code library + call-out primitive + Sentinel formation patterns | ~635 |
| `govops-synlang-patterns.md` | Pattern catalog from runnable demo (historical) | ~440 |

---

## Vocabulary cheat sheet

| Term | Meaning |
|---|---|
| **synart** | The canonical, replicated part of the synome (whole tree of entarts + universal `&core-*` Spaces); open-source SOTA |
| **synent** | A *synomic entity* — Guardian, Prime, Halo. Owns an entart. |
| **entart** | A synent's subtree of synart, rooted at one root Space |
| **telart** | A teleonome's private state tree — telgate, alpha store, call-out services, dreamart, experience archive. Replicated within own emb fleet. |
| **embart** | An embodiment's local workspace tree — per-loop execution Spaces + working memory. Never replicated. |
| **synserv** | The synome server — the canonical instance, run by Core GovOps |
| **telseed** | Minimal package (atomspace runtime + connection info + sync prefs + identity + endowment) that bootstraps a new teleonome |
| **Noemar** | One implementation of the synlang atomspace runtime contract; multiple impls expected |
| **atomspace runtime** | Any conforming implementation of the synlang/atomspace contract; source lives in `&core-library-runtime-*` |
| **call-out** | Synlang primitive `(call-out $service (inputs …) (output-shape …))` — the synart→telart bridge for consulting local cognition |
| **recipe** | A loop bundled with economics + auth + slashing — the regulated marketplace's products |
| **alpha / edge** | A teleonome's proprietary delta beyond synart's open-source SOTA; the moat |
| **emb fleet** | The set of embodiments owned by one teleonome; telart replicates within this set |
| **endoscraper** | Loop class that scrapes internal protocol smart contract state on certain public chains; verifies beacon claims |
| **`&core-*`** | Universal Spaces (synome root); see `topology.md` §6 |
| **`&core-syngate`** | Synserv's gate (synart, universal) |
| **`&core-telgate`** | Universal telgate spec (synart, universal) — every tel runs an instance with state in own telart |
| **`&core-loop-*`** | Universal loop templates (synart, executable layer) |
| **`&core-library-*`** | Library content — runtime source, telseeds, knowledge corpora, published alpha |
| **`&entity-<type>-<id>-<sub-kind>`** | Per-entart Spaces; see `topology.md` §9 |

---

## Cross-doc invariants

Things that should be true across all docs in this directory:

- **Permission rule template:** `(if (auth $beacon $verb $target) True False)`
  (the longer preamble in `govops-synlang-patterns.md` is documented
  there as historical demo state).
- **Space naming:** `core-<kind>` and `entity-<type>-<id>-<sub-kind>` per `topology.md` §9.
- **Phase 1 commitments:** thirteen total, canonical list in `topology.md` §19.
- **Beacons and operators are external.** Only synomic agents own entarts.
- **Auth atoms** live in the entart owning the verb's target.
- **Settlement is two-phase:** per-Prime (parallel) → global aggregation (`&core-settlement`).
- **Cadence-agnostic** — Phase 1 is monthly, Phase 2+ daily; the architectural shape doesn't depend on the period.
- **Six synome-root layers:** constitutional, framework, registry, aggregation, executable, library — per `topology.md` §6.
- **Four meta-patterns:** frameworks propagate, registries identify, aggregations collect, specifications execute — per `topology.md` §7.
- **Three artifact tiers:** synart (commons), telart (proprietary alpha), embart (hardware-local) — each a *tree of Spaces*, not a single Space. Full treatment in `syn-tel-emb.md`.
- **Recipe marketplace canonical home:** `syn-tel-emb.md` §8. Other docs reference, don't duplicate.
- **Five levels of self-reference canonical home:** `syn-overview.md` §10.5. Other docs reference.
- **Identity-driven boot canonical home:** `boot-model.md`. `synart-access-and-runtime.md` §10 documents the synserv-specific concrete shape; §11.5 references the abstract model.
- **Loops and gates live in synart** as content. Universal templates in synome root; entity-specific configurations in entarts (two-step loop pattern per `topology.md` §17).
- **Telgate code lives in `&core-telgate`** (synart, universal); per-tel instance state lives in that tel's telart.
- **Telseeds are minimal bootstrap configs**, not packaged knowledge corpora; full treatment in `syn-tel-emb.md` §4.
- **Call-out primitive** is the only sanctioned mechanism for synart-resolved code to consult local cognition; canonical synlang form in `synlang-patterns.md` §5.
- **Risk is content-based, not state-based.** The original state-based CRR (`(crr filling 5)` etc.) is gone. Risk derives from category-equation evaluation against current exo book state and Riskbook composition, typically as stress simulations. Canonical home: `risk-framework.md`.
- **Four book types:** Primebook (Prime aggregation), Halobook (Halo aggregation), Riskbook (the unit of regulation; finality CRR computed here), Exobook (external structures, recursive). Bankruptcy remoteness lies above the Riskbook level.
- **Riskbook categories are the unit of regulation.** A Riskbook must match a registered Riskbook category or get CRR 100% (default-deny). Risk categories live at three levels (exo asset / exobook / riskbook) with riskbook categories as the load-bearing economic citizens.
- **Equations are stress simulations.** Category equations evaluate composition under a library of stress scenarios; risk weights reflect worst-case real claim to real assets in correlated crash. Four-tier resolution: math → simulation → heuristics → max-risk.

If a doc contradicts one of these, that's a doc bug, not a model bug.
