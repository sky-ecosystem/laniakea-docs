# noemar-synlang — Runtime + Language Technical Reference

The canonical home for the **Noemar runtime + synlang** technical specifics. Everything else in the repo assumes familiarity with what's here; this is where readers go to find out what Noemar is, how the runtime works, what synlang looks like in practice, and how the substrate is organized.

Analogous to a `smart-contracts/` directory in a financial protocol — distinct from conceptual docs, answers **"how is this actually implemented."**

For the broader concept map (what synomics is *about*), see [`../synomics-overview.md`](../synomics-overview.md). For the abstract runtime architecture this directory implements, see [`../synodoxics/noemar-substrate.md`](../synodoxics/noemar-substrate.md).

---

## Reading order

For a new reader of this directory:

1. **[`synlang.md`](synlang.md)** — The language. S-expressions grounded in the synomic library; what got resolved (homoiconicity, compositionality, library-grounded symbols); what's still being designed (surface conventions, schema, versioning).
2. **[`topology.md`](topology.md)** — Canonical structural reference. Entart tree, six-layer synome root, four meta-patterns, naming convention, two-step rule and loop shapes, thirteen Phase 1 commitments.
3. **[`runtime.md`](runtime.md)** — Access control kernel + runtime architecture. Auth domains, three-level interaction model (root / cert / auth), gate primitive, in-synlang heartbeat, identity-driven boot summary, call-out primitive summary, sixteen migration principles.
4. **[`boot-model.md`](boot-model.md)** — Identity-driven boot. The synart-as-program insight, Boot CLI, spec/instance collapse, shadow execution, hot-swap modes, failure modes, the grounded fast-path.
5. **[`synlang-patterns.md`](synlang-patterns.md)** — Synlang code library. Platonic kernel, cross-book duality, four-constructor MeTTa surface with proper types, sentinel decision rule with risk-adjusted return, **the call-out primitive (canonical synlang form)**, **Sentinel formation patterns (Baseline / Stream / Warden as beacons-with-call-outs)**.
6. **[`scaling.md`](scaling.md)** — Operational concerns when this becomes a networked system. Synserv as single sequencer, replication and staleness, partial sync, hot-spotting, partitions, telart spread, call-out propagation, telseed onboarding load, testing strategy.
7. **[`listener-loops.md`](listener-loops.md)** — In-space calculation pattern (sketch). Endoscrapers / oracles / attestors push data atoms into book spaces; synserv keeps each book's derived state real-time consistent. Implementation mechanism deferred to Phase 1.
8. **[`beacons.md`](beacons.md)** — Phase 1 beacon implementation sketches (input vs action, per-protocol details deferred). Conceptual core has been absorbed into [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md); this file remains as Phase-1-implementation reference until Phase 1 lands real classes.
9. **[`telseed-bootstrap-example.md`](telseed-bootstrap-example.md)** — Worked Noemar boot example. Trace of one teleonome's first 24 hours from spawn to stable multi-emb operation.

### Phase 2 content

Risk-framework rewrite landed; canonical conceptual treatment now lives in [`../risk-framework/`](../risk-framework/README.md). Two synlang-flavored docs remain in this directory:

- **`risk-framework.md`** — Synlang-flavored complement (atom shapes, equations, four-tier resolution as code, five worked examples). Conceptual material defers to `../risk-framework/`.
- **`settlement-cycle-example.md`** — Worked end-to-end settlement cycle synlang example. Demonstrates the synlang machinery (entart subtree, scatter-gather, settlement closure) using the new content-based CRR framing.

### Working notes (archived)

Session handoff and design-discussion notes that fed the risk-framework rewrite have been archived to [`../inactive/archive/`](../inactive/archive/) as of 2026-05-05:

- `notes1.md` (session handoff)
- `rewrite-plan-final.md` (Phase 0-6 plan of record)
- `risk-framework-redesign-2026-05-03.md` (substrate for the rewrite)
- `synome-extra-info.md` (refinements + §10 rewrite plan)

---

## File map

| File | Role |
|---|---|
| [`synlang.md`](synlang.md) | Language reference — s-expressions grounded in the synomic library |
| [`topology.md`](topology.md) | Canonical structural reference (synome root + entart tree + naming + meta-patterns + Phase 1 commitments) |
| [`runtime.md`](runtime.md) | Auth domains, runtime architecture, gate primitive, migration principles, identity-driven boot summary, call-out summary |
| [`boot-model.md`](boot-model.md) | Identity-driven boot — how `noemar boot` resolves to a running loop; synart-as-program; shadow execution |
| [`synlang-patterns.md`](synlang-patterns.md) | Synlang code library — Platonic kernel, four-constructor surface, call-out primitive, Sentinel formation patterns |
| [`scaling.md`](scaling.md) | Operational concerns — synserv as single sequencer, replication, partial sync, hot-spotting, partitions, testing |
| [`listener-loops.md`](listener-loops.md) | In-space calculation pattern (sketch) |
| [`beacons.md`](beacons.md) | Phase 1 beacon implementation sketches (per-protocol details deferred); conceptual core lives in `../macrosynomics/beacon-framework.md` |
| [`telseed-bootstrap-example.md`](telseed-bootstrap-example.md) | Worked telseed bootstrap trace |
| `risk-framework.md` | Phase 2 risk model — pending rewrite into `../risk-framework/` |
| `settlement-cycle-example.md` | Phase 2 worked example — pending rewrite |

---

## Conceptual content that lives elsewhere

If you came here looking for one of these, they've moved:

| Topic | New canonical home |
|---|---|
| Concept map / synomics overview | [`../synomics-overview.md`](../synomics-overview.md) (formerly `syn-overview.md`) |
| Artifact tiers (synart / telart / embart) + telseeds + bootstrap arc + atomspace runtimes + resilience model | [`../synodoxics/noemar-substrate.md`](../synodoxics/noemar-substrate.md) (absorbed `syn-tel-emb.md` §§1-7, 9, 10) |
| Recipe marketplace | [`../synoteleonomics/recipe-marketplace.md`](../synoteleonomics/recipe-marketplace.md) (formerly `syn-tel-emb.md` §8) |
| Beacon framework (two-tier authority + I/O role) | [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) (absorbed `beacons.md` + `listener-loops.md` conceptual core) |
| Topology / population / probmesh meta-architectural layering | [`../macrosynomics/topology-layers.md`](../macrosynomics/topology-layers.md) (formerly `topology-population-probmesh.md`) |
| GovOps demo pattern catalog | [`../inactive/archive/govops-synlang-patterns.md`](../inactive/archive/govops-synlang-patterns.md) (archived as historical) |

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

- **Permission rule template:** `(if (auth $beacon $verb $target) True False)`.
- **Space naming:** `core-<kind>` and `entity-<type>-<id>-<sub-kind>` per `topology.md` §9.
- **Phase 1 commitments:** thirteen total, canonical list in `topology.md` §19.
- **Beacons and operators are external.** Only synomic agents own entarts.
- **Auth atoms** live in the entart owning the verb's target.
- **Settlement is two-phase:** per-Prime (parallel) → global aggregation (`&core-settlement`).
- **Cadence-agnostic** — Phase 1 is monthly, Phase 2+ daily; the architectural shape doesn't depend on the period.
- **Six synome-root layers:** constitutional, framework, registry, aggregation, executable, library — per `topology.md` §6.
- **Four meta-patterns:** frameworks propagate, registries identify, aggregations collect, specifications execute — per `topology.md` §7.
- **Three artifact tiers:** synart (commons), telart (proprietary alpha), embart (hardware-local) — each a *tree of Spaces*. Full treatment in `../synodoxics/noemar-substrate.md`.
- **Recipe marketplace canonical home:** `../synoteleonomics/recipe-marketplace.md`. Other docs reference, don't duplicate.
- **Five levels of self-reference canonical home:** `../synomics-overview.md` §10.5. Other docs reference.
- **Identity-driven boot canonical home:** `boot-model.md`. `runtime.md` §10 documents the synserv-specific concrete shape; §11.5 references the abstract model.
- **Loops and gates live in synart** as content. Universal templates in synome root; entity-specific configurations in entarts (two-step loop pattern per `topology.md` §17).
- **Telgate code lives in `&core-telgate`** (synart, universal); per-tel instance state lives in that tel's telart.
- **Telseeds are minimal bootstrap configs**, not packaged knowledge corpora; full treatment in `../synodoxics/noemar-substrate.md`.
- **Call-out primitive** is the only sanctioned mechanism for synart-resolved code to consult local cognition; canonical synlang form in `synlang-patterns.md` §5.
- **Beacon framework is two-tier authority + I/O role under it.** Calculation lives in synart-resolved in-space computation that synserv runs (per `listener-loops.md`); beacons are pure I/O. Canonical home: `../macrosynomics/beacon-framework.md`.

If a doc contradicts one of these, that's a doc bug, not a model bug.
