# Topology, Population, Probmesh — Architectural Layering

**Status:** Draft (2026-05-04 design pass; topology atom-set not yet drafted)
**Last Updated:** 2026-05-04

The synome stratifies into four layers — three rigid, one variable — with the probmesh as a transverse alignment-argument substrate that crisscrosses all of them. This document captures the layering decisions and their implications for everything that follows.

Companion to:
- [`../noemar-synlang/topology.md`](../noemar-synlang/topology.md) — structural treatment of the synome that this layering is being grafted onto
- [`../synomics-overview.md`](../synomics-overview.md) — concept map, four-tier architecture, five levels of self-reference
- [`../noemar-synlang/runtime.md`](../noemar-synlang/runtime.md) — gate, constructors, runtime mechanics
- [`../noemar-synlang/boot-model.md`](../noemar-synlang/boot-model.md) — identity-driven boot, shadow execution
- [`../synodoxics/noemar-substrate.md`](../synodoxics/noemar-substrate.md) — artifact tiers (synart/telart/embart), alignment-through-coalition story

---

## TL;DR

Four layers, three rigid, one variable, plus a transverse argument substrate:

```
TELOS                          What the system is for
  ↓ (sudo only; ideally externally fixed)
AXIOMS                         Invariants flowing from telos
  ↓ (sudo only; rare events)
TOPOLOGY                       Archetypes, connections, interfaces, constructors
  ↓ (constructor-mediated, validated)
POPULATION                     Concrete instances filling topology slots

PROBMESH crisscrosses all four — argues whether population-under-topology
serves telos, and whether axioms or topology must change to maintain alignment.
```

The probmesh is not generic knowledge; it's the alignment-justification machinery. Every probmesh atom is implicitly part of a chain reaching back to telos. Topology evolution happens via **sudo** events — arbitrary atomspace edits — prompted by probmesh argument and ratified by governance. There are **no meta-constructors**; the rigid layers are sudo-only by design.

Comments today, pre-probmesh, are early-phase placeholders for alignment-argument content. Writing them with the eventual chain in mind ("this serves intermediate goal G, which serves telos T") is the discipline that makes the comments → probmesh transition smooth rather than a rewrite.

---

## Section map

| § | Topic |
|---|---|
| 1 | The four-layer hierarchy |
| 2 | Two atom classes, one substrate |
| 3 | Probmesh as alignment-argument substrate |
| 4 | Sudo: the only path to change rigid layers |
| 5 | Frames: canonical and shadow |
| 6 | Comments as pre-probmesh content |
| 7 | Topology as per-phase deliverable |
| 8 | What this commits us to |
| 9 | Open questions |
| 10 | Cross-doc invariants |
| 11 | One-line summary |

---

## 1. The four-layer hierarchy

### Telos

What the system is for. The apex commitment. Externally fixed; arguments flow *from* it, not toward changing it. Mutable only through what amounts to writing a new constitution — probably out-of-band of the synome itself.

Recommended shape: a **structured statement with named sub-commitments**, not a single sentence. Probmesh arguments will reference different aspects of "what the system is for"; without sub-commitments every argument has to re-derive what telos requires from scratch.

### Axioms

Invariants that flow from telos and can never be violated. Concrete enough to cite directly when arguing against a population pattern, without having to reach all the way back to telos. Examples (illustrative, not the canonical set):

- "Equity invariant holds for every book."
- "No atom is written outside a constructor (except sudo)."
- "USDS is always backed at ≥100% collateral."

Live in `&core-skeleton` (or possibly `&core-axioms` as a sibling — see Open Questions). Cadence-of-change: closer to never than to rare.

### Topology

The rigid shape of the synome — what space archetypes exist, what atoms each archetype is allowed to hold (interface), what connections exist between archetypes, what constructors can write to them. Lives in `&core-meta-topology`. **Sudo-only by design** — there is no smooth path to evolve it.

The archetype-with-count pattern handles repeated instances (entarts, books, units) without combinatorial blowup. One archetype declaration; many populated instances. Same two-step pattern as universal templates + per-entity instances in [`../noemar-synlang/topology.md`](../noemar-synlang/topology.md) §17, applied recursively to the topology itself.

### Population

Concrete instances of archetypes (this Halo, this book, this unit), atoms within those instances, actual events. Cadence: operational (seconds) to slow governance. Constructor-mediated, validated against topology. Lives in the entart tree + universal layers (`&core-registry-*`, `&core-settlement`, etc.).

---

## 2. Two atom classes, one substrate

Topology atoms and population atoms live in the same atomspace, distinguished by predicate head, not by storage:

| Atom class | Examples | Where |
|---|---|---|
| Topology | `(space-archetype …)`, `(connection …)`, `(constructor-def …)`, `(interface-contract …)` | `&core-meta-topology` |
| Population | `(book …)`, `(unit …)`, `(book-state …)`, `(auth …)`, `(beacon-pubkey …)` | entart tree + universal layers |

Population fills topology. Every populational write must reference an archetype, and the constructor checks the resulting atom against the archetype's declared interface. **Validation is total** — no exceptions, no opt-outs, no "system mode" that bypasses it. The gate enforces it; constructors refuse non-conforming writes.

This is what makes the topology layer load-bearing rather than documentation. Without enforcement, topology drifts into prose; with it, the gate is the validation surface and topology atoms are the spec.

### Topology-derived population atoms

Some atoms are populational by storage and update mechanics, but generated *from* topology — routing tables (`(verb-target-space …)`), registry indexes, sub-entart lists, settlement targets. Pattern: constructors that touch these read the topology and write the populational atom. Worth deciding once: **indexes derived from topology are populational atoms with topology provenance**, kept consistent by their constructors.

---

## 3. Probmesh: alignment-argument substrate

The probmesh isn't a layer at any one level. It's a transverse substrate where alignment claims live. Every probmesh atom is implicitly part of a chain:

```
observation in population
  → claim about whether it serves telos
  → reference to current topology / axioms
  → "yes, this works" OR "no, change needed at level X"
```

This sharpens what probmesh content looks like. A weather forecast or a price prediction is probmesh content only insofar as it bears on alignment. Generic domain knowledge is just data.

### Two failure modes the probmesh detects

- **Population misalignment** — behavior doesn't serve telos but topology was sufficient. Fix is corrective action within existing topology (parameter change, sentinel halt, governance directive).
- **Topology / axiom insufficiency** — the rigid layer itself doesn't enable alignment. Fix is a sudo-event proposal.

Distinguishing these is itself a probmesh argument. Treating topology insufficiency as population misalignment leads to brittle patchwork that papers over real structural problems.

### Verdicts are graded

Probabilistic logic — confidence values, evidence weights, alternatives considered, opposing arguments. Output to governance is "argument with confidence X for change Y," not "do Y." Governance decides ratification. Same shape as legal scholarship → judicial decision, or scientific consensus → paradigm shift.

### Why this gives alignment architectural teeth

Per [`../synodoxics/noemar-substrate.md`](../synodoxics/noemar-substrate.md) (formerly `syn-tel-emb.md` §9) — "intelligence private, power regulated." With the probmesh-as-alignment-argument framing, this is enforced structurally: private cognition can do anything internally, but to *influence* the system beyond population, it has to translate into public probmesh arguments referencing telos.

A teleonome with arbitrary intelligence has exactly two channels:
1. Act within population (rate-limited, reversible)
2. Submit probmesh arguments (public, debatable, requires ratification for anything topology-touching)

Neither lets it unilaterally change shape. The alignment surface lives in *argumentation*, not in code, and argumentation gets harder to fake as scrutiny scales — which is the property that makes the architecture robust to capability scaling.

---

## 4. Sudo: the only path to change rigid layers

**Sudo is arbitrary atomspace mutation** — bypasses the gate, bypasses constructor validation, bypasses archetype conformance. Writes raw synlang directly. Reserved for changes to telos / axioms / topology.

Honest framing: the system being changed *includes* the gate and validation logic, so it can't validate its own replacement. Topology change and system change are the same event.

### Sudo events are flag-day events

- Audit trail captures every write
- Rationale required, referencing probmesh content
- Run in shadow frame first, observed, then promoted to canonical
- Versioned, dated, ratified, archived in their entirety

There is no "smooth path" or "meta-constructor." Topology changes are constitutional rewrites. Frequency is rare-by-design, ratification-required, all-or-nothing.

### Freeze early posture

After one focused design pass, freeze topology. Subsequent evolution is sudo-as-amendment. The commitment that matters is the **posture of unwillingness to change**, which forces the design pass to be high-stakes and careful.

You can't literally freeze before designing. Order:
1. Draft topology in detail for a phase
2. Review hard
3. Freeze
4. Sudo only thereafter

Committing to permanent before designing either ships something underspecified that needs an immediate sudo-event (defeats the point) or stalls forever. The design pass is the thing.

---

## 5. Frames: canonical and shadow

A **frame** is a concrete instance of synome state. There's a **canonical frame** (live, what synserv writes) and arbitrary **shadow frames** (forks for prediction, testing, forecast).

| Property | Canonical | Shadow |
|---|---|---|
| Topology | Frozen (sudo to change) | Same as canonical (or experimental for topology-tests) |
| Population | Live, evolving | Forked at a settlement boundary; evolves independently |
| Constructors | Run normally | Same constructors; write to shadow store |
| Gate | Real | Frame-aware |

Builds on shadow execution ([`../noemar-synlang/boot-model.md`](../noemar-synlang/boot-model.md) §5), the double-mesh trick ([`../noemar-synlang/scaling.md`](../noemar-synlang/scaling.md) §10), and counterfactual simulation in `stl-base` ([`../trading/sentinel-network.md`](../trading/sentinel-network.md)). What's new in this framing: shadows are **first-class**, not an upgrade pattern. There's *always* a shadow available alongside live.

### Useful frame operations

- `frame-fork` — clone canonical at a settlement boundary into a new shadow
- `frame-rebase` — replay real events into a forecast to test calibration
- `frame-diff` — compare population atoms across frames

The forecast model in `laniakea-docs/forecast_model/` becomes a specific shadow-frame configuration, not a separate system.

### Sudo events use frames for safety

All sudo edits get applied to a shadow frame first, exercised against representative population, observed, then promoted to canonical. Doesn't add new machinery — frames already need to exist; just makes "shadow → canonical" the standard procedure for sudo events. Bypassing this is itself a sudo decision, fine in true emergencies but visibly out-of-pattern.

---

## 6. Comments as pre-probmesh content

Synlang comments are atoms — queryable, attributable, versionable. Different from conventional code comments which are stripped at parse time.

### Standard comment shapes

| Shape | Purpose |
|---|---|
| `(doc-for $atom "what this does")` | Interface description |
| `(rationale-for $rule "why this exists, what we rejected")` | Design intent |
| `(invariant-comment $space "this should always hold")` | Local assertion |
| `(open-question $atom "...")` | Known-unknowns |
| `(deprecated $atom "...")` | Soft markers |
| `(serves-telos-via $atom $intermediate-purpose)` | Explicit alignment-chain link |

### Today's comments → tomorrow's probmesh

Today: `(rationale-for $rule "we did X because Y")` is markdown-in-atom. Tomorrow: it becomes a probmesh atom with confidence values, evidence pointers, alternatives-considered structure, opposing-argument links. Same role, richer structure.

The transition is smooth if comments today are written **with the chain in mind** — naming intermediate purpose and reaching toward telos, rather than just "we did this." The discipline is annoying where the chain is obvious, but it's the chain that has to exist eventually anyway.

### Lightweight inline scratch

Reserve `;;` style for inline working notes that don't need durable structure. Use atom-form for documentation that future agents (LLM call-outs, verifier embs, governance reviewers) will query.

---

## 7. Topology as per-phase deliverable

Each phase ships a **topology delta** — atom-set declaring what the synome should look like after this phase. Phase completion becomes a queryable predicate: "does actual topology match declared phase-N topology?"

Structurally identical to infrastructure-as-code (Terraform, k8s manifests), applied to a synome. Changes the existing markdown roadmap from description into specification.

For each phase:
- New archetypes declared
- New connections declared
- New constructors with declared interfaces
- New axioms (if any) with rationale chains
- New comments / pre-probmesh content

The 13 Phase 1 commitments ([`../noemar-synlang/topology.md`](../noemar-synlang/topology.md) §19) become topology constraints checked by automation rather than read by humans.

### Most important per-phase artifact

Topology atoms for everything involved — both synome and teleonomes/beacons — with comments and documentation explaining the innards and connections of each space, and clearly labelling shared (synome) vs local (teleonome/beacon) spaces.

This makes the roadmap rollout testable: Phase N is "complete" when actual canonical topology matches phase-N declared topology and the constructors are exercising the new connections.

---

## 8. What this commits us to

1. **Two atom classes, one substrate.** Topology and population atoms distinguished by predicate head, both go through the gate, both stored uniformly.
2. **Validation is mandatory.** Every population write checked against topology. No `add-atom` runs without archetype lookup.
3. **No meta-constructors.** Topology changes via sudo only.
4. **Sudo events are flag-day events.** Audited, ratified, shadowed-first, rationale required.
5. **Topology is frozen after design pass.** Posture of unwillingness to change.
6. **Frames carry both topology and population.** Shadows usually mirror topology and vary population; topology-test shadows are rare and explicit.
7. **Comments are written with the alignment chain in mind.** Reach toward telos, not just "rationale."
8. **Phase deliverables are topology atom-sets.** Queryable, validatable, versionable.
9. **Probmesh argument is the only justification for sudo events.** No silent constitutional changes.

---

## 9. Open questions

- **Telos specificity.** Single statement vs structured statement with named sub-commitments? (Lean toward structured.)
- **Telos mutability.** Interpretation only, or revisable from within? (Lean toward interpretation only — telos fixed externally; otherwise the alignment story unravels.)
- **Axiom Space placement.** Separate from `&core-skeleton` or shared? (Lean toward separate — different cadence; axioms change less than skeleton, which might itself include sub-content like type universes.)
- **Probmesh structural placement.** `&core-probmesh-*` with sub-spaces by argument-type or topology-region argued-about? Probably both axes, details TBD.
- **Frame boundary semantics.** Shadow replicates full atomspace or per-Space deltas (COW)? Probably deltas + COW, details TBD.
- **Sudo authority structure.** Single threshold (Core Council ratification) or graded (sudo-types with different ratification requirements)? Probably graded for proportionality; specifics TBD.
- **Probmesh → sudo path mechanics.** What's the threshold mechanism that turns accumulated argument into a ratified sudo event? Confidence threshold, vote ratification, both?
- **Crystallization of probmesh content into axioms.** When an alignment argument matures, does it become an axiom? Or just a topology change with the rationale archived in probmesh? (Probably the latter — axioms shouldn't accumulate from arguments; they should be deliberately curated.)

---

## 10. Cross-doc invariants

Things that should be true across all docs once this layering is adopted:

- Four-layer hierarchy: telos → axioms → topology → population
- Probmesh crisscrosses; doesn't sit at one layer
- Topology is sudo-only; no smooth evolution path
- Population is constructor-mediated; constructors validate against topology
- Comments today are pre-probmesh content; written with alignment chain in mind
- Frames carry both topology and population; canonical is what synserv writes; shadows fork at settlement boundaries
- Sudo events run in shadow first, observed, ratified, promoted
- Phase deliverables are topology atom-sets, validatable against canonical

If a doc contradicts one of these, that's a doc bug, not a model bug.

---

## 11. One-line summary

**The synome stratifies into four layers — telos, axioms, topology, population — three rigid (sudo-only, ratification-required) and one variable (constructor-mediated, validated against topology); the probmesh is a transverse alignment-argument substrate that argues whether population-under-topology serves telos and whether the rigid layers must change to maintain it; comments today are early-phase pre-probmesh content; sudo is the only path to change rigid layers, runs in shadow first, and is reserved for constitutional rewrites; phase deliverables are topology atom-sets the system can verify actual state against.**

---

## File map

| Doc | Relationship |
|---|---|
| [`../noemar-synlang/topology.md`](../noemar-synlang/topology.md) | Structural treatment of the synome — this layering is being grafted onto it |
| [`../synomics-overview.md`](../synomics-overview.md) | Concept map; four-tier architecture, five levels of self-reference |
| [`../noemar-synlang/runtime.md`](../noemar-synlang/runtime.md) | Gate, constructors, runtime — operational substrate |
| [`../noemar-synlang/boot-model.md`](../noemar-synlang/boot-model.md) | Identity-driven boot, shadow execution — frame mechanics begin here |
| [`../synodoxics/noemar-substrate.md`](../synodoxics/noemar-substrate.md) | Artifact tiers (synart/telart/embart) and the substrate; the recipe marketplace lives in [`../synoteleonomics/recipe-marketplace.md`](../synoteleonomics/recipe-marketplace.md) |
| [`../noemar-synlang/risk-framework.md`](../noemar-synlang/risk-framework.md) | Four-book taxonomy, content-based risk; specific population shape (pending Phase 2 rewrite into `../risk-framework/`) |
| [`../synodoxics/`](../synodoxics/README.md) | Canonical home for probmesh detailed treatment |
