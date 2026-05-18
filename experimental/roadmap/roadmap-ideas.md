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

Arbitrary expression introduced via syngate by Core Council. Lands in a spell space (e.g., `&core.spells`) with a maturation deadline (24-48h). During maturation: visible to subscribers, cancellable by Core Council. After maturation: executable by the council beacon if not cancelled.

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

1. **Substrate** — atomspace + runtime + naming convention (`core.<kind>` / `entity.<type>.<id>.<sub-kind>`)
2. **Trust boundary** — gate primitive (sig verify, nonce, rate limit) + auth check predicate `(can $beacon $verb $target)`
3. **Identity layer** — beacon registry (`&core.registry.beacon`) + entart index
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

Phase 1 implementation: deep copy is enough at this scale (~72 Spaces, modest atom count). Copy-on-write becomes valuable later.

---

## The lift principle

Phase 1 is not just "the simplest thing that works." It's an exercise in building **production-quality lift** — synlang that exists once and doesn't get rewritten. The test:

> If we'd build it in Python now and rewrite it in synlang later, build it in synlang now.

The Phase 1 deliverables are bounded — only what's needed for the phase to perform — but within that scope, the synlang is the long-term shape. CRR equations, risk-form match, sub-book routing, ER, equity invariants, health factors, loop bodies — all production synlang evaluated by Noemar from day 1. Python remains for **grounded primitives** the runtime calls into (ed25519 verification, atom storage, network I/O, basic numeric ops); these don't get replaced by synlang later because they can't be.

"Lift" at this stage just means high-quality synlang. Probmesh, dense comments, formal proofs are not yet load-bearing. The bar is: the synlang you write now is the synlang the system runs on indefinitely.

### Code vs data — the discriminator that prevents over-rabbit-holing

- **Code → synlang.** Every rule, equation, derivation, loop body, predicate. Lifty.
- **Data → atoms** (sudo-set or derived). Stress scenario parameters, asset stress profiles, capital allocations, governance numbers. Sudo-setting *numbers* in Phase 1 isn't duct tape — it's policy. The equations consuming them are synlang.

A function whose body we don't yet know how to write isn't duct tape either, **as long as the signature is real synlang**. Declare the inputs, declare the output, leave the body deferred. The matured P1 `custodial-crypto` direction is no longer opaque: it is a stress-envelope waterfall consuming `chain-read`, market-memory atoms, and attestation gates, returning per-risk-type CRR components. Exact scenario constants remain data atoms, not code.

### The insyn/exsyn pattern — phasing capabilities into synome

The synome is built in phases. At any phase, some capabilities are **insyn** (synome-native, real synlang on real atoms) and some are **exsyn** (outside the synome, fed in by trusted oracle providers). For aggregations that span both, split the quantity:

```
quantity = insyn-component + exsyn-component
            (computed in-synlang)   (oracle-fed gap-filler)
```

> **Naming note.** Distinct from `endo`/`exo` in synlang substrate vocabulary (endoasset/exoasset, endobook/exobook), which is about graph membership. **Insyn/exsyn** is about **epistemic provenance** — did we derive this from synome-native data, or did we accept a signed claim from an external provider? Different distinction, different scope, different name.

Phase 1 uses this for TRRC: `insynTRRC` from the 3 P1 halos in real synlang, `exsynTRRC` for legacy halos written into each Prime's primebook by a govops-operated **patch-beacon** (one `patch-{prime}` instance per Prime, sudoed inline at genesis; data lives directly in `&entity.prime.{id}.primebook`, no oracle-entity hop). ER = (insynTRRC + exsynTRRC) / TRC is computed in real synlang against real values; only the exsyn number is provider-attested. As more halos migrate into the synlang-native stack, the exsyn number shrinks and the patch-beacon retires. **The synlang code doesn't change at the migration boundary.**

This is the canonical mechanism for **phased synome buildout**. Anywhere a system-wide quantity needs values from infrastructure that isn't yet synlang-native:

- Concentration exposure per category (insyn positions + exsyn legacy oracle)
- Total USDS backing
- Cross-Prime aggregations in Genbook
- Telart→synart migration of published patterns
- Cross-chain aggregations (native-chain insyn + foreign-chain exsyn)
- Any other partial-migration aggregation

Each exsyn-bridging instance — patch-beacon in Phase 1, or any future scaffold of this nature — is **transitional by design**: it deprecates as insyn coverage grows. Both endpoints (full-insyn mature state, mostly-exsyn Phase 1) are valid configurations of the **same synlang**. The phase progression is: insyn coverage grows, exsyn shrinks toward zero per domain, synlang code is unchanged throughout.

When it fits:
- The quantity is associative (sum, max, etc.) over independent contributors
- You can identify which contributors are insyn vs exsyn cleanly
- A trustable provider exists (governance-curated, slashable) for the exsyn side
- The migration trajectory is one-way (exsyn shrinks, never grows arbitrarily)

When it doesn't fit:
- Cross-contributor interactions (e.g. correlation matrices — can't split cleanly)
- The exsyn provider has the same trust deficit as the missing infrastructure (you've moved the problem, not solved it)
- Migration trajectory isn't well-defined (exsyn could grow without bound → not transitional)

For doesn't-fit cases, black-box deferral (define the function signature, leave the body opaque) is the lifty alternative.

### Black-box deferrals — honest scaffolds, not duct tape

When you don't know enough about a domain to model its internals well, define the function signature in synlang and leave the body opaque. This was the right earlier discipline for the P1 risk-form conversation: lock the `custodial-crypto` signature and do not invent a fake scalar. The current live P1 design has since matured past opacity: the body is a stress-envelope exobook waterfall over `chain-read`, market-memory reducer outputs, and attestation gates. The black-box pattern remains the right tool for future risk classes whose internals are not yet understood.

The discipline: **define the smallest synlang surface** that lets the layer above proceed. Defer everything else to its respective phase boundary.

### Temporary-equation bodies — real-but-provisional computation

Some P1 bodies are not opaque; they are known temporary equations. They are real synlang, run in production, and produce real atoms, but their body is expected to be swapped when the mature mechanism lands. This differs from black-box deferral:

- black-box deferral: signature is real, body is opaque;
- temporary-equation body: signature and body are real, but the body is intentionally provisional.

The P1 SDR auction is the canonical case. Synserv triggers it during the daily processing window. It reads effective SDR bucket capacities from `&entity.generator.usge.structural-demand`, Sky Prime token-share facts, and per-Prime IJRC, then writes ownership-weighted pro-rata `sdr-allocation` atoms. A later phase replaces the body with real Prime-strategy-driven SDR auction matching. The trigger, read path, atom shape, and structbook consumption site stay fixed.

**Temporary-equation containment:** all temporary logic must live inside the body that will later be swapped. Long-term systems it consumes stay clean. For P1, `&core.treasury` stores raw Sky token-share facts; `&entity.generator.usge.structural-demand` stores the lot-age surface, Lindy SDR output, policy overlay, and effective SDR bucket capacities; the ownership-weight split lives entirely in `&entity.generator.usge.sdr-auction`.

### Phase-invariant consumption sites — additive-only transitions

The lift principle's third move, alongside insyn/exsyn and black-box deferral. When a Phase 1 capability will later gain a more elaborate backing — a canonical source where there was none, a propagation mechanism, a real auction where there was a sudo-set table — **fix the consumption site in Phase 1 and let the provenance migrate behind it.**

The worked case is the risk form. In Phase 1 there is no canonical `&core.framework.risk.forms` Space and no propagation; each halo's risk class Space (`&entity.halo.{id}.custodial-crypto`) holds its own copy of the risk form, sudoed at genesis. The halo factory imports the risk form into each dynamic consumer (riskbook) at creation. synserv reads it purely local. Later, a canonical `&core.framework.risk.forms` source plus a propagation mechanism are added — refreshing the *same* per-halo risk class Spaces that Phase 1 already sudo-populates. The factory is unchanged; synserv's read path is unchanged. The transition is purely **additive**: a new source Space + a new propagation loop, nothing relocated, renamed, or rewired.

The same shape recurs for **loop bodies** (per-entity loop Spaces hold their bodies in P1; canonical templates ship later, propagating into the same per-entity Spaces — entarts can also keep local extensions alongside the propagated body) and for **SDR allocations** (`&entity.generator.usge.sdr-auction` holds synserv-written pro-rata SDR allocations in P1; the real Prime-strategy-driven SDR auction later writes the same atom shape into the same Space).

**The invariant:** whoever consumes the thing must read it from the exact same local location in Phase 1 and later. The only thing allowed to change across the transition is the *provenance* of how it got there — sudo-authored → propagated-from-canonical. The read side never sees the difference. Same shape as insyn/exsyn ("the synlang code doesn't change at the migration boundary") — here it is the *read path* that doesn't change.

**The debt traps it rules out:**

- Don't cross-space-reference a central Space in Phase 1 with a plan to "make it local later." That later fix *is* the tech debt. Phase 1 must already be local-read — the thing materialized at its consumption site from day 1, even with no canonical source yet behind it.
- The propagation *target* must already exist and be populated in Phase 1 topology. Phase 1 sudo-populates it; the later mechanism populates it; the Space itself never appears or moves.
- The constructor / wiring that imports into dynamic consumers must already be the Phase 1 behavior — so it is literally unchanged at the transition.

**Distinguish the instances from the spec.** Saying a capability "only lives in tests" in Phase 1 is shorthand for *the normative spec* having no Space yet — the binding that says "these copies must be equal and must mean X." The *instances* (the actual equation atoms) do live in real Spaces from day 1; they have to, or the read path cannot be phase-invariant. Tests carry the normative spec until a canonical Space does; their *role* then shifts from binding to conformance-check. That role shift is expected evolution, not debt — debt only ever shows up in topology or read-path.

### DSC — the synomic settlement cadence

The synome only knows the daily synomic settlement cycle (DSC). Legacy monthly settlement is an out-of-band operational shadow, not a set of atoms. As a capability becomes visible to the synome it enters DSC; there is no MSC-inside-synome intermediate state.

P1 uses DSC for structural-demand processing:

- cut: 13:00 UTC;
- processing window: 13:00-16:00 UTC;
- processing tasks: treasury refresh, lot-age surface refresh, Lindy SDR, SDR policy overlay, temporary SDR auction;
- settle / epoch advance: 16:00 UTC;
- advancement: synserv derives state from wall clock and writes `&core.settlement`, not a sudo loop.

Later settlement closure, TMF, DR/SDRR, and real auctions add more processing tasks to the same cadence.

### Market memory — reducer outputs, not raw history atoms

Market-data beacons should be understood as market-memory beacons. Raw source tapes live in archive nodes. Versioned reducer formulas run over those tapes in two modes:

- replay mode: historical archive range -> backfilled reducer outputs;
- live-tail mode: new events -> updated reducer outputs.

The same reducer runs in both modes. If fundamental understanding changes, governance approves a new reducer version, archive nodes replay history with the new formula, and once caught up the same reducer continues live. The synome stores reducer outputs and checkpoints, not the full raw tape.

Risk scenarios should minimize arbitrary parameters by referencing reducer outputs wherever possible. Any remaining semantic bridge ("war means this bundle of rate-spike, liquidity-drought, and crypto-risk-off reducer references") must be explicit.

### Don't rabbit-hole — what to skip

Lifty doesn't mean fanatical. The boundary:

- ✅ Build the production CRR equation in synlang now (it'll exist forever; build once)
- ✅ Build the insyn/exsyn split now (the pattern itself is the lift)
- ✅ Build the heartbeat loop body in real synlang now
- ✅ Build constructors (`create-halobook`, etc.) as real synlang now
- ❌ Don't model the full stress scenario library when v1 only needs one risk form
- ❌ Don't build event-driven derivation when heartbeat sweep suffices
- ❌ Don't build full multi-Generator architecture when v1 has one Generator
- ❌ Don't activate concentration excess penalty when v1 has no caps
- ❌ Don't hardcode full causal macro models when scenario atoms can reference market-memory reducer outputs

The test for any deferred component: *would building it now exercise architecture we'll otherwise miss, or would it be speculative scaffolding for a phase that hasn't arrived?* If speculative, defer. If load-bearing for the phase's deliverable, build it lifty.

---

## Phase doc template (for Phases 2-10)

Each future phase doc, in order: (1) framing — what changes operationally vs sudo-only; (2) Spaces added at the phase boundary; (3) Spaces modified (new I/O edges or content); (4) new constructors / verbs; (5) new beacon classes + I/O matrix; (6) test additions to `&core.test-suite`; (7) genesis-equivalent sudo sequence for the phase boundary; (8) what carries forward unchanged (important — most substrate doesn't change at most phase boundaries); (9) deferred internals; (10) running totals.

For the Phase 1 instantiation of this template and the canonical scope/carve-out lists, see [`phase-1-spaces.md`](phase-1-spaces.md) and [`v1-principles.md`](v1-principles.md).

---

## Open questions carried forward

Things noted during the Phase 1 work that don't have settled answers:

- **Crypto stress scenario calibration** — deferred to governance discussion when CRR values become real
- **Shadow-test execution mechanism** — same synserv flipping pointer vs separate synserv instance pointed at shadow (Phase 1 doesn't need to settle this; pre-launch testing only needs one)
- **Whether `&core.spells` should exist in Phase 1** as empty/unused infrastructure that exospells will populate later — currently deferred (no spells in Phase 1)
- **Opaque-RWA risk class attestation schema** — legacy HVB-style classes (no on-chain visibility) need a richer numeric schema beyond the custodial-crypto boolean reframe; deferred, not a P1 risk class
- **Later-phase Space-name judgment calls** — names chosen during the 2026-05-13 naming sweep but not used in P1: `&core.framework.risk.crash-oracle` (could be `&core.framework.crash-oracle` if not strictly risk), `&core.framework.prime-token-metrics` (could be registry data), and `&core.registry.cross-prime-flows` (compound id pattern is consistent but not yet reserved vocabulary)

---

## What might come next

Reasonable next steps:

1. **`phase-0-substrate.md`** — foundational substrate (genesis sudo, gate, identity, authority bootstrap, sudo + audit + failover); the irreducible base every phase rests on. Recommended first.
2. **`phase-2-spaces.md`** — adds formal settlement closure tasks to the daily synomic settlement cycle (in-space settlement verification, prepayment / penalty event records), plus Phase 2 test additions.
3. **Continue through Phases 3-10** in order, each as a topology delta.

(Pre-synlang ↔ synlang vocabulary mapping is in [`../roadstart/README.md`](../roadstart/README.md).)
