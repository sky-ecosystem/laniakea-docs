# Phases Directory — Ideas, Conventions, and Context

**Status:** Working notes / context doc.
**Purpose:** Captures vocabulary, conventions, design decisions, and open questions that informed `phase-1-spaces.md` and that should carry forward as later phase docs get written. Not a spec; meant to be read by anyone (including future-me) picking up the roadmap rewrite.

---

## What this directory is for

Phase docs written in **space-perspective** — each phase as a topology delta on the previous one. Phase 1 (`phase-1-spaces.md`) is the first; the same shape should apply to Phases 2-10.

The discipline: each phase doc answers four questions, in this order:

1. **What Spaces exist after this phase** — fixed-at-genesis-of-this-phase Spaces, plus any factory-created classes
2. **What each Space holds** — one paragraph per Space, content type + update cadence + operational vs fixed
3. **What I/O happens** between beacons, gate, and Spaces during this phase's normal operation
4. **What changes vs what's sudo-only** — within-phase operational changes vs phase-boundary sudo events

Topology + I/O are the rigid layer that the doc commits. Internal mechanics (calculation algorithms, beacon implementation choices, schema specifics) stay deferrable. The discipline of writing in this shape is what enforces the topology-first rigor that the architecture wants.

---

## Vocabulary

### sudo

Local superpowers of doom. Runtime-level direct write to atomspace, bypasses gate. Used for:

- Genesis bootstrap (the only path that can place initial atoms before anything has authority)
- Phase boundary events (every move from one phase to the next is a sequence of sudo writes)
- Mature-state escape hatch (rare, true emergencies — but largely obviated by failover; see below)

Integrity properties: off-space audit log + operator diversity (backup synserv operators with independent state). The audit is *external to and independent of* the audited substrate — same pattern as DB transaction logs vs the DB.

### exospell

Arbitrary expression introduced via syngate by Core Council. Lands in a spell space (e.g., `&core-spells`) with a maturation deadline (24-48h). During maturation: visible to subscribers, cancellable by Core Council. After maturation: executable by the council beacon if not cancelled.

Content is whatever Core Council signed; no formal binding to upstream reasoning. Like the legacy MakerDAO "spell" pattern but generalized to any atomspace mutation.

Not in Phase 1. Comes online when topology change frequency picks up and you want timelocked + subscriber-visible governance writes.

### endospell

Same execution machinery as exospell, but the spell content is cryptographically bound to a synodoxics derivation. The gate verifies that the proposed diff matches the deterministic output of a referenced PLN inference run. The probmesh argument has to have ossified to a sufficient confidence threshold before becoming a candidate endospell. Core Council ratifies; the substrate verifies the binding.

Mature-state mechanism. Requires probmesh + synodoxics infrastructure to exist.

### Failover (the resilience model)

Backup synserv operators run the same loop with independent state. If the canonical synserv is compromised or breaks, Core Council out-of-band signs a new `(canonical-synserv-runner X)` declaration; subscribers reconnect to the new synserv. This cleanly handles "broken synserv" without needing an in-system emergency mechanism.

Per `boot-model.md` §5: "Failover is an atom write." This is what obviates the need for "emergency sudo" as a distinct architectural concept.

---

## The three-mechanism sudo staircase

Each step adds a constraint on the previous one:

| Mechanism | What it adds | When it appears |
|---|---|---|
| **sudo** | (none — direct write) | Always — genesis bootstrap, then rare emergency / phase boundaries |
| **exospell** | Gating + timelock + visibility + cancellability | When topology change frequency increases (mid phases) |
| **endospell** | + Cryptographic binding to deterministic synodoxics output | Mature state |

Sudo never goes away — it's the bootstrap and emergency mechanism. But its usage profile shrinks from "the only mechanism we have" (Phase 0-1) to "the escape hatch when nothing else can do it" (mature state).

---

## Foundational substrate (pre-Phase / Phase 0 conceptually)

What's irreducibly required regardless of phase. This is what genesis sudo establishes before any phase machinery lands:

1. **Substrate** — atomspace + runtime + naming convention (`core-<kind>` / `entity-<type>-<id>-<sub-kind>`)
2. **Trust boundary** — gate primitive (sig verify, nonce, rate limit) + auth check predicate `(can $beacon $verb $target)`
3. **Identity layer** — beacon registry (`&core-registry-beacon`) + entart index
4. **Authority bootstrap** — genesis seed + the five construction verbs (create-guardian, set-root, cert-beacon, auth-beacon, revoke) + open verb dispatch via whitelist
5. **Networking + replication** — gate-in (signed beacon submissions) + gate-out (hash-chained diffs to subscribers)
6. **Sudo capability + off-space audit + operator diversity** — the meta-mechanism that lets the substrate be bootstrapped and modified at all

The genesis seed itself is a sudo write — placed pre-bootstrap, before any synomic mechanism exists. After it lands, ordinary operations through the gate become possible.

If we ever write a Phase 0 doc, this is its content: the irreducible substrate every phase rests on.

---

## Frame mechanism

A frame is a complete instance of synome state — every Space, every atom. The runtime can hold multiple frames simultaneously and operate against a chosen one (the "active frame").

Operations: `fork(source, new-id)`, `switch(frame-id)`, `discard(frame-id)`, `diff(a, b)`.

Lives below the synomic surface — a runtime addition, not a synart concept. From inside synart you can't tell which frame you're in.

Phase 1 use case: clone-and-test isolation. Genesis bootstraps canonical → fork to shadow → run tests against shadow → discard shadow → canonical verified by structural identity.

Future use cases the same mechanism supports:
- Sudo event safety (apply to shadow first, observe, then promote)
- Forecasting (replay scenarios in shadow without affecting reality)
- What-if queries (synodoxics arguments exercised in shadow before becoming endospells)
- Major migrations / repartitioning (double-mesh trick)

Phase 1 implementation: deep copy is enough at this scale (~53 Spaces, thousands of atoms). Copy-on-write becomes valuable later.

---

## Why Phase 1 ended up at the exact scope it did

The conversation iterated:

1. Started with the full architecture from `topology.md` — too much for Phase 1
2. Narrowed to absolute minimum (gate + halos + book factory) — too little; doesn't include the operational shape that makes Phase 1 actually do anything
3. Expanded to include Primes + Generator's structural demand subtree + scrapers + oracle + per-halo attestors — landed on 53 fixed Spaces

The discriminating principle: include everything that's part of Phase 1's *operational semantics* (Phase 1 is the first phase the system is actually running with real beacons doing real work). Defer everything else to its respective later phase.

What's in Phase 1:
- 53 fixed Spaces (universal core + Guardian + Generator + 6 Primes + 3 Halos with aggregation hierarchy)
- 1 constructor (the book factory `create-book`)
- ~23 beacon identities
- Synart-native test suite + runtime frame mechanism for clone-and-test isolation
- One risk category, shared across the 3 halos

What's deferred:
- Aggregation logic in halobook / riskbook / primebook / structbook / genbook (Phase 1 has the Spaces but derives values at read time)
- Settlement formalization (Phase 2-3)
- LCTS / srUSDS (Phase 4)
- Factories for new entities (Phases 5-8)
- Sentinel formations (Phases 9-10)

---

## Phase doc template (for Phases 2-10)

Each future phase doc should have, in this order:

1. **Framing** — what changes operationally vs sudo-only in this phase
2. **Spaces added** — new Spaces sudo-allocated at the phase boundary
3. **Spaces modified** — existing Spaces with new I/O edges or new content types
4. **New constructors / verbs** — anything that allocates Spaces or that's added to the verb whitelist
5. **New beacon classes** — new identity classes registered, with their I/O matrix
6. **Test additions** — new test atoms appended to `&core-test-suite`
7. **Genesis-equivalent sudo sequence** for this phase boundary — exact sequence of sudo writes that constitutes "moving to this phase"
8. **What carries forward unchanged** — explicit list of Spaces / verbs / archetypes from prior phase that don't change here
9. **Deferred internals** — what's intentionally not specified yet
10. **Totals** — running total of fixed Spaces, beacons, constructors, etc.

The "what carries forward unchanged" section is important — it makes the phase boundary's scope visible. Most of the substrate doesn't change at most phase boundaries; the doc should make that explicit.

---

## Key design takeaways from the Phase 1 work

A few principles that emerged:

- **"Any sudo event is a phase boundary by definition."** This is what makes phase boundaries crisp — modifying fixed Spaces necessarily means leaving the phase. If you're tempted to sudo during a phase, that's the signal you're starting a new phase.
- **The factory is the only operational construction.** In Phase 1, only the book factory exists. Everything else is fixed at genesis. This is what bounds the operational write surface and makes "what changes during a phase" tractable.
- **Aggregation Spaces are structural placeholders in early phases.** Halobooks, riskbooks, primebooks, structbooks, genbook — they exist as Spaces in Phase 1 but their actual content is mostly derived at read time by lpla-verify. They become populated with operational atoms only when later phases (settlement, auctions) need persistent aggregate state.
- **Placeholder topology proves substrate scales.** Three Primes (keel/skybase/launch6) without halos in Phase 1 is intentional — it shows the substrate handles 6 Primes' worth of entart even when only 3 are operationally active.
- **Test halo deleted in favor of shadow frame.** The clone-and-test pattern is cleaner than dedicated test entities + cleanup verbs. The shadow frame mechanism is the single payoff that handles testing, sudo safety, forecasting, etc.
- **Frames live below synomic surface.** Don't add `&core-frames` Space. The frame mechanism is a runtime feature; from inside synart you can't tell what frame you're in.

---

## Open questions carried forward

Things noted during the Phase 1 work that don't have settled answers:

- **Exact attestation atom shape** — deferred to halo cohort engagement during implementation
- **Crypto stress scenario calibration** — deferred to governance discussion when CRR values become real
- **Shadow-test execution mechanism** — same synserv flipping pointer vs separate synserv instance pointed at shadow (Phase 1 doesn't need to settle this; pre-launch testing only needs one)
- **Pre-synlang → synlang vocabulary mapping** — whether to inline mapping tables in each phase doc or maintain a single shared mapping. Lean: one shared mapping at `phases/README.md`.
- **Whether `&core-spells` should exist in Phase 1** as empty/unused infrastructure that exospells will populate later — currently deferred (no spells in Phase 1)
- **Generator's place in authority chain** — this came up earlier and was resolved to "USGE direct child of Ozone, peer of Primes" in `topology.md`. Phase 1 follows this.

---

## Pre-synlang ↔ synlang vocabulary mapping (partial)

A few translations between the legacy roadmap (`inactive/pre-synlang/roadmap/`) and the synlang-native phase docs:

| Pre-synlang term | Synlang-native equivalent |
|---|---|
| Synome-MVP | Universal Spaces (`&core-*`) + per-entity entart subtrees |
| Halo Books (in Synome-MVP) | Factory-created `&entity-halo-<id>-book-<book-id>` Spaces |
| Halo Units | Atoms inside book Spaces (one unit atom per NFAT) |
| Risk Framework (Synome-MVP entity) | `&core-framework-risk` content |
| Attestations (Synome-MVP entity) | Atoms inside book Spaces (gated by lpha-attest auth) |
| Core Halo entries | Atoms in (a future) `&core-registry-corehalo` — Phase 1 collapses these into the existing 3 halos so no separate registry needed |
| LPLA / LPHA / HPLA / HPHA codes | Two-tier authority + I/O role under it (per `macrosynomics/beacon-framework.md`); legacy codes survive as operational identifier prefixes |
| `lpla-checker` (legacy beacon class) | Synserv-run in-space calculation (per `noemar-synlang/listener-loops.md`) — no longer a separate beacon |

Worth maintaining a more complete version as later phase docs reference back to roadmap content.

---

## Files in this directory (so far)

| File | What it is |
|---|---|
| `phase-1-spaces.md` | Phase 1 in space-perspective — the canonical Phase 1 spec |
| `phases-ideas.md` | This file — context, vocabulary, conventions, design notes |

---

## What might come next

Reasonable next steps from where we are:

1. **`phase-0-substrate.md`** — write up the foundational substrate (genesis sudo, gate, identity, authority bootstrap, sudo + audit + failover). This is what every phase rests on.
2. **`phase-2-spaces.md`** — Phase 2 adds formalized monthly settlement; what Spaces does that introduce (settlement-tracking atoms, lpla-checker beacon, prepayment / penalty event records)? Plus the test additions for Phase 2.
3. **Continue through Phases 3-10** in order, each as a topology delta.
4. **`phases/README.md`** — a directory index + conventions reference + complete vocabulary mapping table.

Recommend starting with Phase 0 doc since it's the substrate every other phase references.
