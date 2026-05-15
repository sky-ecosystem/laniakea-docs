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

Phase 1 implementation: deep copy is enough at this scale (~64 Spaces, modest atom count). Copy-on-write becomes valuable later.

---

## The lift principle

Phase 1 is not just "the simplest thing that works." It's an exercise in building **production-quality lift** — synlang that exists once and doesn't get rewritten. The test:

> If we'd build it in Python now and rewrite it in synlang later, build it in synlang now.

The Phase 1 deliverables are bounded — only what's needed for the phase to perform — but within that scope, the synlang is the long-term shape. CRR equations, risk-form match, sub-book routing, ER, equity invariants, health factors, loop bodies — all production synlang evaluated by Noemar from day 1. Python remains for **grounded primitives** the runtime calls into (ed25519 verification, atom storage, network I/O, basic numeric ops); these don't get replaced by synlang later because they can't be.

"Lift" at this stage just means high-quality synlang. Probmesh, dense comments, formal proofs are not yet load-bearing. The bar is: the synlang you write now is the synlang the system runs on indefinitely.

### Code vs data — the discriminator that prevents over-rabbit-holing

- **Code → synlang.** Every rule, equation, derivation, loop body, predicate. Lifty.
- **Data → atoms** (sudo-set or derived). Stress scenario parameters, asset stress profiles, capital allocations, governance numbers. Sudo-setting *numbers* in Phase 1 isn't duct tape — it's policy. The equations consuming them are synlang.

A function whose body we don't yet know how to write isn't duct tape either, **as long as the signature is real synlang**. Declare the inputs, declare the output, leave the body deferred. The custodial-crypto risk form (the equation inside each per-halo risk class) is exactly this in v1: real synlang signature consuming `chain-read` + market-data ticks + the boolean attestation gate, returning per-risk-type CRR components; opaque body; no rewrite required when the body matures.

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

When you don't know enough about a domain to model its internals well, define the function signature in synlang and leave the body opaque. The risk framework in v1 collapses to a single risk class (`custodial-crypto`) per halo, each carrying a risk form that consumes `chain-read` + market-data + the boolean attestation gate and returns per-risk-type CRR components; the body is unknown territory; the signature is permanent. When the body matures, fill in the synlang — same signature, same callers, no rewrite. Modeling internals prematurely (stress scenario library, asset stress profile derivation, volatility calibration) would lock in a model that may not survive contact with reality.

The discipline: **define the smallest synlang surface** that lets the layer above proceed. Defer everything else to its respective phase boundary.

### Phase-invariant consumption sites — additive-only transitions

The lift principle's third move, alongside insyn/exsyn and black-box deferral. When a Phase 1 capability will later gain a more elaborate backing — a canonical source where there was none, a propagation mechanism, a real auction where there was a sudo-set table — **fix the consumption site in Phase 1 and let the provenance migrate behind it.**

The worked case is the risk form. In Phase 1 there is no canonical `&core.framework.risk.forms` Space and no propagation; each halo's risk class Space (`&entity.halo.{id}.custodial-crypto`) holds its own copy of the risk form, sudoed at genesis. The halo factory imports the risk form into each dynamic consumer (riskbook) at creation. synserv reads it purely local. Later, a canonical `&core.framework.risk.forms` source plus a propagation mechanism are added — refreshing the *same* per-halo risk class Spaces that Phase 1 already sudo-populates. The factory is unchanged; synserv's read path is unchanged. The transition is purely **additive**: a new source Space + a new propagation loop, nothing relocated, renamed, or rewired.

The same shape recurs for **loop bodies** (per-entity loop Spaces hold their bodies in P1; canonical templates ship later, propagating into the same per-entity Spaces — entarts can also keep local extensions alongside the propagated body) and for **structural-demand allocations** (the auction Space holds sudo-set allocations in P1; the real Prime-strategy-driven auction later writes the same atom shape into the same Space).

**The invariant:** whoever consumes the thing must read it from the exact same local location in Phase 1 and later. The only thing allowed to change across the transition is the *provenance* of how it got there — sudo-authored → propagated-from-canonical. The read side never sees the difference. Same shape as insyn/exsyn ("the synlang code doesn't change at the migration boundary") — here it is the *read path* that doesn't change.

**The debt traps it rules out:**

- Don't cross-space-reference a central Space in Phase 1 with a plan to "make it local later." That later fix *is* the tech debt. Phase 1 must already be local-read — the thing materialized at its consumption site from day 1, even with no canonical source yet behind it.
- The propagation *target* must already exist and be populated in Phase 1 topology. Phase 1 sudo-populates it; the later mechanism populates it; the Space itself never appears or moves.
- The constructor / wiring that imports into dynamic consumers must already be the Phase 1 behavior — so it is literally unchanged at the transition.

**Distinguish the instances from the spec.** Saying a capability "only lives in tests" in Phase 1 is shorthand for *the normative spec* having no Space yet — the binding that says "these copies must be equal and must mean X." The *instances* (the actual equation atoms) do live in real Spaces from day 1; they have to, or the read path cannot be phase-invariant. Tests carry the normative spec until a canonical Space does; their *role* then shifts from binding to conformance-check. That role shift is expected evolution, not debt — debt only ever shows up in topology or read-path.

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
- ❌ Don't build asset history derivation when stress profiles are sudo-set

The test for any deferred component: *would building it now exercise architecture we'll otherwise miss, or would it be speculative scaffolding for a phase that hasn't arrived?* If speculative, defer. If load-bearing for the phase's deliverable, build it lifty.

---

## Why Phase 1 ended up at the exact scope it did

The conversation iterated through several scopes; v3 (2026-05-15 topology redesign, building on v2 of 2026-05-06) settled on:

1. **Real-time ER per Prime as the single deliverable.** Settlement and penalty action remain manual; the synome publishes ER, governance consumes externally.
2. **All synlang from day 1**, per the lift principle above. No Python placeholders.
3. **Risk framework via per-halo risk class** — one risk class (`custodial-crypto`) per halo, each carrying a risk form (real synlang signature, body deferred); no canonical `&core.framework.*` Space in P1.
4. **Insyn/exsyn split for system-wide quantities** — TRRC = insynTRRC + exsynTRRC; TRC fully insyn (synome-tracked).
5. **Seven Primes all active**, deploying into 3 P1 Halos. No placeholder Primes.
6. **Halo class + risk class split per halo** — halo class (`nfat-term`) carries halobook policy + permitted risk classes; risk class (`custodial-crypto`) carries risk form + attestor as sub-Space. Per-halo materialization per the phase-invariant consumption-site principle.
7. **Root holds registry + constructors only.** Operational logic lives in dedicated sub-Spaces. Universal pattern across every entart type.
8. **Cert / auth fold into `&core.registry.beacon`.** No standing Guardian root Space in P1; the beacon registry is the authority root.

What's in Phase 1 (v3):
- **64 fixed Spaces** (4 universal Core + 4 Generator + 3 Oracle + 7 Primes × 5 + 3 Halos × 6)
- 3 constructors (`create-halobook`, `create-riskbook`, `create-exobook`); constructor-made depth grows per deal flow
- ~23 beacon identities, all running real synlang loops in Noemar
- Per-halo halo class + risk class copies (`nfat-term` × `custodial-crypto` in each of the 3 halos); tests bind the per-halo copies until canonical propagation ships later
- Per-entart `protocol-registry` sub-Spaces (each Prime, Halo, and the Generator owns its own chain-contract refs locally)
- Synart-native test suite + runtime frame mechanism for clone-and-test isolation
- Real-time ER per Prime emitted continuously via synlang heartbeat
- Authority chain rooted in `&core.registry.beacon` (no standing Guardian Space; Guardian's cert content sudoed into the beacon registry at genesis)

What's deferred:
- Stress scenario library, asset stress profile derivation, asset history (risk framework treated as black box; no `&core.framework.*` Space in P1)
- Concentration excess penalty (no caps active)
- Other Primebook sub-books (only `structbook` active)
- Settlement closure / penalty calculation (Phase 2)
- LCTS / srUSDS (Phase 4)
- Factories for new entities (Phases 5-8)
- Sentinel formations (Phases 9-10)
- Cross-Prime concentration in Genbook (Genbook itself deferred)
- Multi-Generator architecture
- Event-driven derivation (heartbeat sweep is enough)
- Endoscraper-driven verification — endoscraper is a grounded runtime primitive `(chain-read $contract $slot)`; per-protocol metadata lives in per-entart `protocol-registry` sub-Spaces (each Prime, Halo, and the Generator carries its own contract refs locally), not a single `&core.protocol`
- `&core.escalation` (status atoms in books are enough)
- Canonical loop-template propagation (per-entity loop Spaces hold their bodies in P1; templates arrive additively in a later phase)
- Canonical risk-form source + propagation (per-halo copies in P1; canonical source ships additively later)

---

## Phase doc template (for Phases 2-10)

Each future phase doc should have, in this order:

1. **Framing** — what changes operationally vs sudo-only in this phase
2. **Spaces added** — new Spaces sudo-allocated at the phase boundary
3. **Spaces modified** — existing Spaces with new I/O edges or new content types
4. **New constructors / verbs** — anything that allocates Spaces or that's added to the verb whitelist
5. **New beacon classes** — new identity classes registered, with their I/O matrix
6. **Test additions** — new test atoms appended to `&core.test-suite`
7. **Genesis-equivalent sudo sequence** for this phase boundary — exact sequence of sudo writes that constitutes "moving to this phase"
8. **What carries forward unchanged** — explicit list of Spaces / verbs / archetypes from prior phase that don't change here
9. **Deferred internals** — what's intentionally not specified yet
10. **Totals** — running total of fixed Spaces, beacons, constructors, etc.

The "what carries forward unchanged" section is important — it makes the phase boundary's scope visible. Most of the substrate doesn't change at most phase boundaries; the doc should make that explicit.

---

## Key design takeaways from the Phase 1 work

A few principles that emerged:

- **The lift principle is the bar.** Synlang-first, production-quality, no Python placeholders that get rewritten. Test: code → synlang, data → atoms. Grounded primitives (ed25519, atom storage, network, math) stay native; everything else is synlang.
- **Insyn/exsyn split is the generalizable phased-buildout device.** Quantity = insyn (real synlang on what's in synome) + exsyn (oracle gap-filler for what's not yet). As phases progress, insyn coverage grows, exsyn shrinks toward zero. The synlang code doesn't change at the migration boundary. Distinct from endo/exo in synlang substrate vocabulary — different scope, different distinction.
- **Black-box deferrals are honest scaffolds.** Define synlang function signatures; leave bodies opaque when domain understanding is thin. The risk form inside each per-halo risk class is the v1 example — production signature, deferred internals, no rewrite when matured.
- **Phase-invariant consumption sites make transitions additive.** Fix where a thing is read from in Phase 1; let its provenance migrate behind it (sudo-authored → propagated-from-canonical). Materialize at the consumption site from day 1 — never cross-space-reference-then-fix-later. Same family as insyn/exsyn and black-box deferral.
- **Don't rabbit-hole.** Lifty doesn't mean fanatical. Build what's load-bearing for the phase's deliverable; defer speculative scaffolding to its phase boundary.
- **"Any sudo event is a phase boundary by definition."** Modifying fixed Spaces necessarily means leaving the phase. If you're tempted to sudo during a phase, that's the signal you're starting a new phase.
- **Real beacons run synlang loops.** Not Python placeholders. Two-step pattern (universal templates + per-entity configs). Phase 1 is when Noemar steps up to production load.
- **Authority is fully sudo at genesis.** No Core GovOps role in Phase 1; cert + auth content sudoed into `&core.registry.beacon` (no standing Guardian root Space — the beacon registry is the authority root). Simplifies the authority chain dramatically.
- **Attestation closes the rollup.** One per exobook, signed by class-accordant attestor (the attestor loop lives as a sub-Space of the risk class, making class-accordance structural). Without a fresh accordant `(underwriting pass)`, the exobook doesn't roll up — the riskbook's risk form excludes it (default-deny). Integrity discipline that prevents stale legal/credit facts from poisoning the rollup.
- **All 7 Primes active.** No placeholder Primes. Each deploys into the 3 P1 Halos (spark-term, grove-term, maple-term). Real ER for everyone from day 1.
- **Halobooks/riskbooks/exobooks are constructor-made**, not sudo. Deals come in bursts; the substrate accommodates them via 3 factory verbs.
- **Test halo deleted in favor of shadow frame.** The clone-and-test pattern is cleaner than dedicated test entities + cleanup verbs.
- **Frames live below synomic surface.** Don't add `&core.frames` Space. The frame mechanism is a runtime feature; from inside synart you can't tell what frame you're in.

---

## Open questions carried forward

Things noted during the Phase 1 work that don't have settled answers:

- **Exact attestation atom shape** — RESOLVED 2026-05-14 for custodial-crypto: see [`attestor-atom-schema.md`](attestor-atom-schema.md). The boolean reframe (legal/credit/custodian underwriter, no quantitative oracle role) holds for any custodial-crypto-shaped class. Opaque-RWA classes (legacy HVB-style) still need a richer numeric schema — deferred, not a P1 risk class.
- **Crypto stress scenario calibration** — deferred to governance discussion when CRR values become real
- **Shadow-test execution mechanism** — same synserv flipping pointer vs separate synserv instance pointed at shadow (Phase 1 doesn't need to settle this; pre-launch testing only needs one)
- **Pre-synlang → synlang vocabulary mapping** — whether to inline mapping tables in each phase doc or maintain a single shared mapping. Lean: one shared mapping at `roadmap/README.md`.
- **Whether `&core.spells` should exist in Phase 1** as empty/unused infrastructure that exospells will populate later — currently deferred (no spells in Phase 1)
- **Generator's place in authority chain** — this came up earlier and was resolved to "USGE direct child of Ozone, peer of Primes" in `topology.md`. Phase 1 follows this.

---

## Pre-synlang ↔ synlang vocabulary mapping (partial)

A few translations between the legacy roadmap (`inactive/pre-synlang/roadmap/`) and the synlang-native phase docs:

| Pre-synlang term | Synlang-native equivalent |
|---|---|
| Synome-MVP | Universal Spaces (`&core.*`) + per-entity entart subtrees |
| Halo Books (in Synome-MVP) | Factory-created `&entity.halo.<id>.halobook.<hbk-id>` Spaces |
| Halo Units | Atoms inside book Spaces (one unit atom per NFAT) |
| Risk Framework (Synome-MVP entity) | `&core.framework.risk` content |
| Attestations (Synome-MVP entity) | Atoms inside book Spaces (gated by class-accordant attest-data auth) |
| Core Halo entries | Atoms in (a future) `&core.registry.corehalo` — Phase 1 collapses these into the existing 3 halos so no separate registry needed |
| LPLA / LPHA / HPLA / HPHA codes | Two-tier authority + I/O role under it (per `macrosynomics/beacon-framework.md`); legacy `hpla-` prefix survives only on legacy peer-to-peer trade beacon identifiers |
| `lpla-checker` (legacy beacon class) | Synserv-run in-space calculation (per `noemar-synlang/listener-loops.md`) — no longer a separate beacon |

Worth maintaining a more complete version as later phase docs reference back to roadmap content.

---

## What might come next

Reasonable next steps from where we are:

1. **`phase-0-substrate.md`** — write up the foundational substrate (genesis sudo, gate, identity, authority bootstrap, sudo + audit + failover). This is what every phase rests on.
2. **`phase-2-spaces.md`** — Phase 2 adds formalized monthly settlement; what Spaces does that introduce (settlement-tracking atoms, in-space settlement verification, prepayment / penalty event records)? Plus the test additions for Phase 2.
3. **Continue through Phases 3-10** in order, each as a topology delta.
4. **`roadmap/README.md`** — a directory index + conventions reference + complete vocabulary mapping table.

Recommend starting with Phase 0 doc since it's the substrate every other phase references.
