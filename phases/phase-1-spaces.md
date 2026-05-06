# Phase 1 — A Space Perspective

**Status:** Draft
**Last Updated:** 2026-05-05
**Scope:** Phase 1 expressed in terms of synart Space topology — what Spaces exist, what each holds, what flows in and out, and what's fixed vs operational.

---

## Framing

Phase 1 expressed as topology answers four questions:

1. **What Spaces exist** at the start of Phase 1 (sudo-created at genesis)
2. **What each Space holds** (one paragraph per Space — content type and update cadence)
3. **What I/O happens** between beacons, gate, and Spaces during normal Phase 1 operation
4. **What's operational vs sudo-only** — what changes during Phase 1 vs what only changes at a phase boundary

The discipline: only one constructor exists in Phase 1 (the book factory). Every other change to the substrate is a sudo event, which by definition constitutes moving to a new phase. This is what makes Phase 1 a coherent unit — its topology is bounded, and its operational write surface is small.

Vocabulary refresher:

| Term | Meaning |
|---|---|
| **sudo** | Local superpowers of doom — runtime-level direct write to atomspace, bypasses gate. The genesis bootstrap runs entirely as a sequence of sudo writes. Off-space audit log + backup synserv operators provide integrity. |
| **gate-mediated write** | Signed beacon submission through `&core-syngate`. Sig + nonce + rate limit + auth check + constructor execution. The normal operational path. |
| **factory** | A constructor verb that allocates a new Space (the book factory is the only one in Phase 1). |
| **fixed at genesis** | Sudo-written once during bootstrap; never changes during Phase 1. Modifying requires another sudo event = a phase boundary. |
| **operational** | Atoms that change during Phase 1 via gate-mediated writes from registered beacons. |

---

## Universal Spaces

Sudo-created at genesis. Sit at the synome root.

| Space | Holds | Operational? |
|---|---|---|
| `&core-root` | Top-level sub-entart registry — names of Guardian, Generator, Primes, Halos | Fixed |
| `&core-syngate` | Gate state — nonce dedup window, per-pubkey rate-limit counters, external-verb whitelist, routing table mapping verbs to target Spaces | Counters mutate per-message; whitelist + routing fixed |
| `&core-registry-beacon` | One row per beacon identity: pubkey, status, class, loop pointer. Read by gate on every message | Fixed (status atoms can flip via sudo if needed) |
| `&core-registry-entity` | Denormalized entity index mirroring the entart tree | Fixed |
| `&core-framework-risk` | Risk framework: the one risk category definition + CRR equation | Fixed in Phase 1 |
| `&core-meta-topology` | Archetypes — declares the shape of valid book Spaces, attestation atoms, unit records, etc. Used by constructor validation | Fixed |
| `&core-loop-synserv` | Synserv heartbeat loop body | Fixed |
| `&core-loop-beacon-lpla-verify` | Loop template for verify beacons | Fixed |
| `&core-loop-beacon-lpha-relay` | Loop template for relay beacons | Fixed |
| `&core-loop-beacon-lpha-nfat` | Loop template for nfat beacons | Fixed |
| `&core-loop-beacon-lpha-attest` | Loop template for attestor beacons | Fixed |
| `&core-loop-beacon-lpha-council` | Loop template for council beacon | Fixed |
| `&core-loop-beacon-endoscraper` | Loop template for endoscraper beacons | Fixed |
| `&core-loop-beacon-oracle` | Loop template for oracle beacons | Fixed |
| `&core-loop-beacon-test-runner` | Loop template for test runner | Fixed |
| `&core-endoscrapers` | Raw scraped chain events from endoscrapers — staging before forwarding to book Spaces and entart leaves | Operational (endoscrapers write continuously) |
| `&core-oracle` | Price feeds, market data — universal oracle inputs | Operational (oracle writes per cadence) |
| `&core-escalation` | Failures, alerts, verification disagreements | Operational (rare, but writable) |
| `&core-test-suite` | Test definitions — declarations of what to test, expected outcomes, optional setup/teardown | Fixed (sudo at genesis) |
| `&core-test-results` | Outcomes of test runs — pass/fail/error per test, run timestamps, captured details | Operational (test runner writes) |

**20 universal Spaces.**

Note on loop templates: Phase 1 beacons are Python programs and don't actually evaluate these loop bodies at runtime. The loop Spaces exist as canonical specifications — what each beacon class is supposed to do — so subscribers can audit, wardens can later re-derive, and the path to identity-driven boot (Phase 9-10) doesn't require new universal Spaces, just runtime changes.

---

## Guardian

Sudo-created at genesis.

| Space | Holds |
|---|---|
| `&entity-guardian-ozone-root` | Sub-entart registry of generator + primes; cert atoms for GovOps team beacons |

The Guardian is operationally inert in Phase 1 — token-holder voting happens off-chain, Core Council enacts via sudo. The entart root exists to anchor the authority chain (cert atoms identifying which beacons are rooted under Ozone) and to provide a sub-entart registry that subscribers can walk to discover the live entity tree.

---

## Generator

Sudo-created at genesis. Phase 1 has one Generator (USGE → USDS → USD frame).

| Space | Holds |
|---|---|
| `&entity-generator-usge-root` | Identity, sub-space registry |
| `&entity-generator-usge-genbook` | Aggregation of Primebook units. Phase 1: just refs to which Primes serve this Generator |
| `&entity-generator-usge-structural-demand` | Top of structural demand subtree |
| `&entity-generator-usge-structural-demand-scrapers` | Scraped USDS / sUSDS / DAI holder data + lot ages. Phase 1: minimal — capacity is manually set, scraper output is mostly informational |
| `&entity-generator-usge-structural-demand-auction` | Per-Prime per-bucket capacity allocations. Phase 1 = "fake auction" — sudo-set equal split among Primes that operate halos, refreshable by Core Council |

**5 Spaces.**

Why structural demand has its own subtree even when "auction" is fake: the substrate the eventual real auction will use is the same. The interface between `lpha-auction` (Phase 9 sentinel-driven) and the consuming systems (Primebooks reading their bucket allocations) lands in the same Space layout. Phase 1 just populates it via sudo instead of via bid-matching.

---

## Primes

Sudo-created at genesis. Six Primes — spark, grove, obex, keel, skybase, launch6 — each with the same internal structure.

Per Prime:

| Space | Holds |
|---|---|
| `&entity-prime-<id>-root` | Auth atoms (which beacons can do what within this Prime's scope), sub-entart registry of halos administered by this Prime |
| `&entity-prime-<id>-primebook` | Holdings of Halobook units (refs to halo halobooks under this prime); aggregation cursor |
| `&entity-prime-<id>-primebook-structbook` | The structbook sub-book — matched-portion records for positions matched against structural demand |

**3 Spaces × 6 Primes = 18 Spaces.**

In Phase 1, only spark / grove / obex have halos under them. The other three (keel, skybase, launch6) have empty primebooks + structbooks. They exist as **placeholder topology** — proving the substrate scales to more entities and giving subscribers a clean view of the full Prime cohort. Adding a halo under one of them later is a sudo event (= phase boundary).

The structbook in Phase 1 holds simple records: which halo book is matched against which structural-demand bucket allocation. lpla-verify reads these to compute matched vs unmatched portions when calculating CRR. No optimization happens — matching is mechanical given fixed allocations.

---

## Halos

Sudo-created at genesis. Three Halos — spark-halo, grove-halo, maple-halo — each with the same internal structure.

Per Halo:

| Space | Holds |
|---|---|
| `&entity-halo-<id>-root` | Auth atoms (create-book, transition-book, post-attestation per beacon), sub-space registry of books under this halo, attestor cert |
| `&entity-halo-<id>-halobook` | Aggregate exposure record. In Phase 1, halobook state is mostly derived from books at read time, but the Space exists for structural completeness |
| `&entity-halo-<id>-riskbook` | Risk-categorized aggregation. Each Halo's riskbook matches the single risk category in `&core-framework-risk`. Holds book registry under this riskbook |

**3 Spaces × 3 Halos = 9 Spaces.**

Halo-to-Prime mapping (for sub-entart placement):

- `spark-halo` → under `&entity-prime-spark-root`
- `grove-halo` → under `&entity-prime-grove-root`
- `maple-halo` → under `&entity-prime-obex-root` (institutional credit fits under Obex)

The same class is shared across all three Halos. The class itself is not its own Space — it's expressed as archetype atoms in `&core-meta-topology` plus the shared category definition in `&core-framework-risk`. Halos point to the same class via reference; they don't each get a separate class object.

No dedicated test halo is needed because tests run against a shadow frame (see Frame Mechanism + Test System below), not against canonical halos.

---

## Factory-created Spaces (the only operational construction)

```
&entity-halo-<halo-id>-book-<book-id>
```

Created by `lpha-nfat-<halo>` via the `create-book` verb when a new deal flows in. Each book Space holds:

- Book lifecycle state (`created` → `filling` → `offboarding` → `deploying` → `at-rest` → `unwinding` → `closed`)
- Asset summary (current composition: USDS amount during filling, USDC during offboarding, attested aggregate during deploying/at-rest, etc.)
- Linked unit (NFAT) atoms — one per swept deposit, with token ID + principal + deal terms + depositor Prime
- Attestation atoms — pre-deployment, at-rest, periodic re-attestations referenced by the book
- Timestamps for each state transition

Books are the only unbounded class. Their count grows during Phase 1 operation and is bounded only by deal flow.

---

## The book factory (the only constructor)

```
verb:    (create-book $halo-id $book-id $caller $nonce)

caller:  lpha-nfat-<halo> (the beacon registered to operate that halo's NFAT facility)

gate verifies:
    1. Sig from $caller (pubkey from &core-registry-beacon)
    2. Nonce not seen (check + write &core-syngate)
    3. Rate limit headroom (check + write &core-syngate)
    4. Verb is whitelisted: (external-verb create-book ...) atom in &core-syngate
    5. $halo-id ∈ {spark-halo, grove-halo, maple-halo} (routing table in &core-syngate)
    6. Auth: (auth $caller create-book $halo-id) atom exists in &entity-halo-$halo-id-root
    7. $book-id is content-addressed (hash of $caller + $nonce + $halo-id)

constructor effect:
    1. Allocate &entity-halo-$halo-id-book-$book-id
    2. Initialize per &core-meta-topology book archetype
    3. Write initial atoms: (book-state $book-id created), timestamps
    4. Register in halo riskbook: (sub-space &entity-halo-$halo-id-riskbook ...)
    5. Register in halo root: (book-id-list ...) for fast lookup
```

The other operational verbs (`transition-book`, `update-book-assets`, `post-attestation`, `record-unit`) write atoms **into existing book Spaces**. They don't allocate new Spaces. They follow the same gate path with their own auth atoms in the halo root.

---

## Beacon roster (sudo-registered at genesis)

| Identity | Class | Per | Count | What it does |
|---|---|---|---|---|
| `lpla-verify-<halo>` | LPLA | Halo | 3 | Reads books, attestations, oracle, framework. Computes CRRs, generates alerts. Writes nothing in synart. |
| `lpha-relay-<halo>` | LPHA | Halo PAU | 3 | Executes on-chain PAU transactions for the halo. No synart writes. |
| `lpha-nfat-<halo>` | LPHA | Halo | 3 | Calls `create-book`, `transition-book`, `update-book-assets`, `record-unit`. Manages book lifecycle. |
| `lpha-attest-<halo>` | LPHA | Halo (independent operator) | 3 | Calls `post-attestation`. Independent attestor — must be operated by party other than halo operator. |
| `lpha-council` | LPHA | Universal | 1 | Core Council interface. In Phase 1, only writes via sudo (no operational verb yet). |
| `endoscraper-halos` | Input | Universal | 1 | Scrapes halo PAU chain state. Writes to `&core-endoscrapers`. |
| `endoscraper-structural-demand` | Input | Generator | 1 | Scrapes USDS / sUSDS / DAI holder lot ages. Writes to `&entity-generator-usge-structural-demand-scrapers`. |
| `oracle-prices` | Input | Universal | 1 | Pushes price feeds. Writes to `&core-oracle`. |
| `prime-govops-<id>` | High-authority | Prime | 6 | Signs Prime PAU operations on-chain. No synart writes in Phase 1 (Prime deposits are observed by endoscraper). |
| `test-runner` | Admin/test | Universal | 1 | Walks `&core-test-suite`, exercises each test by signing as the relevant beacon (operator-level test credentials), writes outcomes to `&core-test-results`. |

**~23 beacon identities** registered in `&core-registry-beacon` at genesis. Pubkeys, status atoms, class atoms, loop-pointer atoms all sudo-written.

---

## Operational write surface

Per beacon, what synart Spaces it touches during normal Phase 1 operation:

| Beacon | Reads | Writes |
|---|---|---|
| `endoscraper-halos` | (chain RPC, off-space) | `&core-endoscrapers` |
| `endoscraper-structural-demand` | (chain RPC, off-space) | `&entity-generator-usge-structural-demand-scrapers` |
| `oracle-prices` | (external feeds, off-space) | `&core-oracle` |
| `lpha-nfat-<halo>` | `&core-endoscrapers`, halo root, attestations in books | books (allocate via `create-book`; update atoms inside) + halo root sub-space registry |
| `lpha-attest-<halo>` | book state | attestation atoms inside book Spaces |
| `lpha-relay-<halo>` | (none in synart) | (executes on-chain only) |
| `lpla-verify-<halo>` | `&core-framework-risk`, books, attestations, `&core-oracle`, `&core-endoscrapers`, halo + riskbook + halobook + primebook + structbook structure | (read-only; alerts go off-space) |
| `lpha-council` | (none) | sudo-only writes (framework, capacity allocations) |
| `prime-govops-<id>` | (none in synart) | (executes on-chain only) |

The pattern: input beacons (endoscrapers, oracle) write into universal staging Spaces; lpha-nfat is the only beacon that allocates new Spaces (via the book factory); lpha-attest writes attestation atoms into existing book Spaces; lpla-verify is purely read-only and computes derived state at query time. Aggregation Spaces (halobook, riskbook, primebook, structbook, genbook) hold structural placeholders but are mostly read-through to the books beneath them in Phase 1.

---

## Frame Mechanism

A **frame** is a complete instance of synome state — every Space, every atom, every auth grant. The frame mechanism is the runtime's ability to hold *multiple frames simultaneously* and operate against a chosen one. Frames are how Phase 1 supports clone-and-test isolation, and the same mechanism generalizes to several future use cases.

### What a frame is

| | |
|---|---|
| **Frame ID** | A name (`canonical`, `shadow-test-001`, etc.) |
| **State** | The atomspace contents — every Space and atom |
| **Provenance** | Where it came from (forked from canonical at timestamp T) |
| **Status** | Active / archived / discarded |

Closest analogies: git branches, database snapshots, Unix process fork. The atomspace runtime holds N frames; reads/writes against frame A don't affect frame B.

### Operations

```
fork(source-frame, new-frame-id)  → creates new-frame-id with state == source-frame
switch(frame-id)                   → synserv now reads/writes against frame-id
discard(frame-id)                  → frame's state is deleted
diff(frame-a, frame-b)             → atoms that differ between frames (useful for test inspection)
```

### Synserv's frame pointer

Synserv has one active frame at a time. Whatever frame the pointer references is what gate-mediated submissions read/write against:

```
synserv-config:
  active-frame: canonical            ← production
                shadow-test-001      ← during testing
                canonical            ← back to production after test discard
```

When the active frame changes, every read goes to the new frame. In-flight submissions complete against whichever frame they started on.

### Phase 1 implementation

Phase 1's atomspace is small (~53 fixed Spaces, thousands of atoms). The simplest implementation is **deep copy** — `fork(canonical, shadow-X)` allocates equivalent Spaces in the shadow store and copies all atoms across. Costs a few seconds at Phase 1 scale; memory is 2× atomspace size while shadow is alive. `discard()` is just freeing storage.

For larger states later, this becomes copy-on-write. That's an optimization, not a different mechanism.

### What changes for synserv

Minimal:
- **Storage layer** — knows how to hold multiple frames, fork, discard
- **Synserv config** — has a frame pointer, swappable
- **Replication-out** — only replicates the canonical frame to subscribers (shadows are local to the runtime)

Gate verification, constructor execution, and beacon dispatch don't change. They all just operate against `synserv-config.active-frame` instead of an implicit "the atomspace."

### Why it isn't a synomic concept

Frames live entirely below the synomic surface. From inside synart — looking at atoms, querying Spaces, evaluating rules — you can't tell which frame you're in. The frame is a property of the runtime layer that holds the atoms, not of the atoms themselves. No `&core-frames` Space; no synart atoms describing frames. This is why frames are a "runtime addition" rather than a "synart addition."

### Use cases beyond Phase 1 testing

The same mechanism, once built, supports:

- **Sudo event safety** — apply a sudo edit to a shadow first, exercise representative population, observe whether anything broke, then promote to canonical (`topology-layers.md` §4)
- **Forecasting** — fork canonical, replay synthetic scenarios, observe outcomes without affecting reality
- **What-if queries** — synodoxics arguments can be exercised in shadow before becoming endospells (mature state)
- **Major migrations / repartitioning** — the "double-mesh trick" (`scaling.md` §10): stand up a parallel grid as a shadow, replay events, validate, atomically switch canonical

The Phase 1 cost (basic fork/discard support in the atomspace runtime) buys all of these long-term.

---

## Test System

A synart-native acceptance suite. Tests live as atoms in `&core-test-suite`; outcomes accumulate in `&core-test-results`. The whole suite is sudo-written at genesis as part of the bootstrap. **Tests run against a shadow frame, not canonical**, using the Frame Mechanism above.

### Why in synart

Three properties fall out of putting tests in synart rather than in an off-space test harness:

- **Auditable** — anyone with read access to synart can see what was tested, what the expected outcomes were, and what the actual outcomes have been across runs. The test definitions are part of the system's record.
- **Versionable** — when a sudo event modifies the substrate (a phase boundary), the tests that should still pass can be re-run, and the suite itself can be sudo-extended with new tests for the new substrate.
- **Replayable** — the test runner is itself a beacon doing gate-mediated work; running the suite is a recordable sequence of synart events, not an ad-hoc external script.

### Test atom shape

```
(test test-001
  (description "lpha-nfat-spark can create a book")
  (category verb-create-book)
  (precondition <synart query>)        ; optional — must hold before action
  (action <verb invocation>)            ; the thing to exercise
  (expected
    <list of synart predicates that should hold after action>)
  (cleanup <verb invocation list>))     ; optional — restore state
```

The runner reads these, signs as the test's `caller` beacon (using operator-level test credentials it holds), submits the action through the gate, then queries synart to check the expected predicates.

### Test categories (Phase 1 suite)

| Category | What it verifies |
|---|---|
| **Topology** | All 50 fixed Spaces exist; sub-entart registries point to correct child Spaces; entity index in `&core-registry-entity` matches the actual tree |
| **Auth atoms** | Each operational verb has correctly-placed auth atoms in the right entart roots; auth atom count matches expected count per halo |
| **Beacon registry** | All ~23 identities present, status=active, class atom set, loop pointer set |
| **Risk framework** | The one risk category exists; CRR equation atoms are present and well-formed |
| **Archetypes** | Book archetype, attestation archetype, unit archetype all present in `&core-meta-topology` |
| **Verb whitelist** | All operational verbs in `&core-syngate`'s `external-verb` list; routing table entries point to expected target Spaces |
| **create-book happy path** | Authorized lpha-nfat creates a book → Space allocated, registered in halo riskbook, initial state atoms correct |
| **create-book auth failure** | Unauthorized caller's submission rejected at gate; nothing allocated |
| **create-book duplicate** | Same content-addressed book-id rejected as duplicate (idempotency) |
| **Book lifecycle** | End-to-end happy path: create → fill → offboard (with attestation) → deploy → at-rest → unwind → close. Verifies attestation gating actually blocks transitions when missing. |
| **Read paths** | lpla-verify can compute CRR for a populated book; subscriber walking from `&core-root` can discover all books under a halo |
| **Gate-level** | Bad sig rejected; replay (same nonce) rejected; rate-limit headroom enforced; unknown verb rejected; unknown identity rejected |
| **Escalation** | Verification disagreements land in `&core-escalation`; failed transactions logged correctly |

### When the suite runs

| When | Purpose |
|---|---|
| **Genesis-completion verification** | After the genesis sudo sequence, the runner exercises the full suite. If anything fails, deployment is broken — fix and re-bootstrap. This is the primary use case. |
| **Post-sudo regression** | After any sudo event during Phase 1 (which is by definition a phase boundary), re-run the parts of the suite that should still pass. New tests get added for new substrate. |
| **Periodic health probe** | Optional — a subset of read-only tests can run on a cadence to confirm the substrate stays coherent under load. |

### The genesis → test → production flow

```
1. GENESIS
   ─ Sudo writes against canonical frame
   ─ All 53 Spaces allocated, beacons registered, framework written, archetypes set
   ─ Test definitions written into &core-test-suite (in canonical)

2. SHADOW FORK
   ─ Runtime: fork(canonical, shadow-test-001)
   ─ shadow-test-001 is bit-identical to canonical at this moment

3. SYNSERV SWITCHES TO SHADOW
   ─ switch(shadow-test-001)
   ─ Real input beacons (oracles, scrapers) are NOT yet running
     (production hasn't started)

4. TEST RUNNER EXECUTES
   ─ Walks &core-test-suite (in shadow)
   ─ Exercises each test:
       a. Signs as the relevant beacon (operator-level test credentials)
       b. Submits action through gate (gate operating against shadow)
       c. Queries shadow to verify expected predicates hold
   ─ Writes results to &core-test-results (in shadow)
   ─ Tests that mutate state — create books, post attestations, etc. — all
     happen in shadow
   ─ Real verbs are exercised; no test-only verbs needed

5. INSPECT RESULTS
   ─ Operator reads shadow's &core-test-results
   ─ Optionally: diff(canonical, shadow) to see exactly what tests changed
   ─ All pass → canonical is verified by structural identity (the shadow
     was bit-identical, and tests verified the substrate behaves correctly)
   ─ Any fail → canonical has the same bug; investigate, fix, re-bootstrap

6. SHADOW DISCARD
   ─ discard(shadow-test-001)
   ─ switch(canonical)

7. PRODUCTION START
   ─ Real input beacons start (oracles, scrapers feeding canonical)
   ─ Operational beacons begin processing real flow
   ─ Books grow under halos as deals come in
```

The correctness property: **if shadow was bit-identical to canonical and tests passed against shadow, then by structural identity canonical is verified.** The runtime's `fork` operation is the load-bearing assertion — produces an exact copy. As long as that holds, transitive verification works.

### Why no test halo, no cleanup verbs

Earlier drafts of this doc considered a dedicated test halo and / or cleanup verbs to handle test pollution. Both go away with shadow frames:

- No test halo — tests run on shadow, not canonical, so canonical halos stay clean
- No cleanup verbs — shadow is discarded wholesale; no per-artifact teardown needed
- No production verb-set contamination — tests exercise the same verbs production will use
- No audit pollution in canonical — test events live in shadow's audit, discarded with shadow
- No nonce / rate-limit consumption against canonical beacons — shadow has its own counters

### Genesis sequence addition

After step 8 (write all auth atoms in entart roots), add:

- **8a.** Sudo-write all test definitions into `&core-test-suite` (in canonical)
- **8b.** Initialize `&core-test-results` empty (in canonical; will be populated in the shadow only)
- **8c.** Configure operator-level test credentials so the runner can sign as any beacon during tests (runtime config, not synart content)

After the synart genesis sequence completes, the runtime forks canonical → shadow, switches to shadow, runs the test suite, inspects results, and discards the shadow. Production starts only after tests pass against the (now-discarded) shadow.

---

## Genesis sudo sequence

Bootstrap is a sequence of sudo writes that establishes the entire fixed substrate:

1. Allocate the 20 universal Spaces
2. Allocate the 33 per-entity Spaces (1 Guardian + 5 Generator + 18 Prime + 9 Halo)
3. Write the risk framework atoms into `&core-framework-risk` (one category, CRR equation)
4. Write archetype atoms into `&core-meta-topology` (book archetype, attestation archetype, unit archetype)
5. Write external-verb whitelist atoms into `&core-syngate` (`create-book`, `transition-book`, `update-book-assets`, `post-attestation`, `record-unit`, plus input-beacon write verbs)
6. Write routing table atoms into `&core-syngate` (verb → target Space mappings)
7. Register all ~23 beacon identities in `&core-registry-beacon` with pubkeys, classes, statuses, loop pointers
8. Write all auth atoms into entart roots (per-halo: who can do what)
9. Write initial structural-demand capacity allocations into `&entity-generator-usge-structural-demand-auction` (manual fake-auction split)
10. Write the entity index into `&core-registry-entity` (denormalized mirror)

After step 10, sudo stops. From here on, all writes are gate-mediated. Books grow in number; everything else is fixed until the next sudo event.

---

## What constitutes a phase boundary

By construction, **any sudo event in Phase 1 is a phase boundary** — modifying a fixed Space crosses out of Phase 1 because the fixed-topology guarantee no longer holds. Examples of changes that would constitute moving to a new phase:

- Adding a new Prime (sudo-allocate new entart subtree)
- Adding a new Halo or moving an existing one to a different Prime
- Changing the risk framework or adding a new risk category
- Adding new beacon classes (new loop template, new identity registrations)
- Activating new verbs (adding `transition-halobook` for live aggregation, etc.)
- Moving from manual fake-auction to real auctions (changes the I/O contract on `&entity-generator-usge-structural-demand-auction`)
- Activating Phase 2 (formalized monthly settlement) — adds settlement-tracking verbs and Spaces

Each later phase is, in this view, a topology delta — a precisely-specified set of sudo writes that extends what Phase 1 established. The substrate that books rest on never gets rewritten; new substrate gets added alongside.

---

## Totals

| Category | Count |
|---|---|
| Universal Spaces | 20 |
| Guardian Spaces | 1 |
| Generator Spaces | 5 |
| Prime Spaces (3 per Prime × 6) | 18 |
| Halo Spaces (3 per Halo × 3) | 9 |
| **Fixed Spaces at genesis** | **53** |
| Books (factory-created, unbounded) | N |
| Beacon identities (sudo-registered) | ~23 |
| Constructors (verbs that allocate Spaces) | 1 (`create-book`) |
| Operational verbs (write into existing Spaces) | ~5 + test-suite execution |
| Test atoms (sudo-written at genesis) | tens to hundreds |

---

## File map

| Doc | Relationship |
|---|---|
| `../noemar-synlang/topology.md` | Canonical topology reference — six-layer synome root, entart pattern, naming convention, Phase 1 commitments. This doc is the Phase 1 instantiation of those patterns. |
| `../macrosynomics/topology-layers.md` | Telos / axioms / topology / population layering and sudo discipline. Phase 1 freezes topology after genesis; sudo events are phase boundaries. |
| `../macrosynomics/beacon-framework.md` | Two-tier authority + I/O role under it. The 22 beacon identities are instances of these classes. |
| `../noemar-synlang/runtime.md` | Auth model, gate primitive, construction verb pattern. Phase 1 uses one constructor (`create-book`); the rest is genesis sudo + gate-mediated atom writes. |
| `../risk-framework/` | The risk framework that lands in `&core-framework-risk`. Phase 1 uses one risk category; the rest of the framework is the eventual catalog. |
| `../inactive/pre-synlang/roadmap/phase1/` | Pre-synlang Phase 1 specs — the same scope expressed in the older Synome-MVP vocabulary. The mapping: Synome-MVP ↔ universal Spaces + per-entity entarts; halo books ↔ factory-created book Spaces; risk framework ↔ `&core-framework-risk`; attestations ↔ atoms inside book Spaces. |

---

## One-line summary

**Phase 1 is 53 fixed Spaces sudo-allocated at genesis (universal core + Guardian + Generator + 6 Primes + 3 Halos with their books-aggregation hierarchy) plus one constructor (the book factory), ~23 beacon identities, a synart-native test suite, and a runtime-level frame mechanism that lets the suite run against a forked shadow and verify the substrate before production starts; the only thing that grows operationally is the count of book Spaces under each halo's riskbook, with everything else changing only via sudo events that constitute phase boundaries.**
