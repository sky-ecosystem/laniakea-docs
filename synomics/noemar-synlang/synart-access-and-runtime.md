# Synart — Access Control and Runtime Architecture

**Status:** Working notes from design discussion. Companion to `synlang-context.md`.
**Scope:** The access control kernel, runtime architecture, and scaling principles that the synart's foundational primitives must rest on. Does NOT cover the constructors themselves (book/unit/halo) — those come after this layer is settled.

---

## Why this document exists

Before we can design `create-halo` / `create-class` / `create-book` / `issue-unit` properly, we need to know:

1. Who is allowed to call them? (access control model)
2. How does that "who" get authenticated and verified? (production runtime)
3. How does this all survive scaling to a large, possibly distributed Synome? (scale principles)

This document captures the conclusions reached, the rationale behind each one, and what we should commit to *now* in order to keep options open *later*.

---

# PART I — Access Control

## 1. Two authorization domains, kept separate

The Synome and the chain are **separate authorization domains**. They both root in the Council Beacon, but they cascade through different mechanisms.

| Domain | Substrate | Currency of authority |
|---|---|---|
| **Synome** | Atoms in the atomspace | Beacon registration with typed write scope |
| **Chain** | EVM contracts (PAU stack) | BEAM holdership (cBEAM, aBEAM) via BEAMTimeLock |

A GovOps team operating something like the Spark Term Halo holds **at least two credentials**:

- **Synome-side:** operates `lpha-nfat-spark` (a registered beacon with write rights to the relevant book/unit records)
- **Chain-side:** holds the **cBEAM** for the PAU (rate limits, controller calls, relayer/freezer)

These are granted by separate paths and revoked separately. `lpla-verify` is the reconciler — reads both worlds, flags drift.

**Synlang lives entirely in the Synome domain.** The constructors we'll write are Synome-writes. They check Synome-side authorization. They do *not* check or model chain-side BEAM holdership. The chain is grounded; from synlang's perspective, beacons emit opaque chain effects alongside their Synome writes.

---

## 2. Standard authorization patterns (background)

Three classical patterns inform the design:

1. **ACL (Access Control List)** — per-object permission lists. Doesn't scale: every object needs its own list.
2. **RBAC (Role-Based)** — principals get roles; roles get permissions. Postgres `GRANT` is this.
3. **Capability-based** — authority is a thing you hold; possession = authorization. OAuth scopes, BEAM tokens.

The BEAM hierarchy is already capability-shaped (a cBEAM is a thing you hold for a specific PAU, delegable, attenuable). We mirror that in synlang.

The right shape for our system: **role + sub-role** (or equivalently, role + scope). The role grants *verbs*; the sub-role grants *nouns* (which targets the verbs apply to).

> **Role grants verbs. Sub-role grants nouns.**

A principal can hold multiple sub-roles under the same role (operator of multiple classes); revoking a sub-role detaches one scope without touching others.

---

## 3. The standardized vocabulary

Three distinct concepts, three different names:

| Layer | What it asserts | Between |
|---|---|---|
| **Governance accord** | Mutual structural recognition between synomic agents | Agent ↔ agent (Guardian↔Prime, Prime↔Halo) |
| **Admin certification** | "This beacon is a recognized principal, and I (the certifier) carry liability for it" | Synomic agent → beacon |
| **Admin authorization** | "This beacon may do verb V on target T" | Certifier (or delegate) → beacon → specific scope |

Properties:

- **Governance accord** is bidirectional, long-lived, structural. It's what the system *is*.
- **Admin certification** carries liability. The certifier is on the hook for everything the beacon does, before any auth is granted.
- **Admin authorization** is the finest grain — many auths per beacon, easy to compose, instant to revoke.

Important: this **deliberately tightens existing usage**. The current docs say "GovOps becomes accordant to a PAU." Under our refined vocabulary, that usage moves under *administrative authorization*; "accordant" becomes reserved for governance accords (agent↔agent only).

---

## 4. The three-level interaction model

Three distinct acts, with deliberately different asymmetries:

| Level | Who can do it | What it asserts | Frequency |
|---|---|---|---|
| **Root** | Core Council, on Guardian token-holder vote | "This GovOps is hired under this Guardian" — top of an org tree | Rare, governance-paced |
| **Cert** | Any beacon with cert authority within its tree | "This sub-beacon is mine; I carry liability" — identity + liability propagation | Operational |
| **Auth** | Any certifier (or delegate) | "This beacon may do X on Y" — scoped capability | Operational, frequent |

The **"underwriting" frame** is the correct mental model:

- **Guardian roots** a GovOps = Guardian agrees to back this company. The vote is governance rigor calibrated to the financial stake. Root is slow, vote-gated, revocable instantly. It's an economic relationship masquerading as a permission.
- **Root beacon certs** operational beacons = the company's internal hiring. The GovOps takes its underwriting and distributes liability internally — the root beacon vouches for each operational beacon it certifies.
- **Root beacon sets auth** per certified beacon = least privilege. Each operational beacon gets exactly the scoped capability it needs. Even if compromised, the auth ceiling caps the damage.

```
Guardian
  ↓ root  (Core Council enacts on Guardian token-holder vote)
Root Beacon (the GovOps "company")
  ↓ cert + auth (per beacon, narrow scope)
Operational Beacons (lpha-nfat-style — the actual write-doers)
  ↓ constructor calls
Synome state
```

**Two structural properties:**

1. **Liability funnels.** Operational damage rolls up through narrow auth → cert at root → root underwritten by Guardian. One chain of accountability, queryable.
2. **Blast radius is bounded by auth.** Compromise an operational beacon → it can only do what its specific auth allows. Compromise the root beacon → can re-cert/re-auth its operational tree, but cannot exceed Guardian's accordancy ceiling. Compromise the Guardian → Core Council can revoke and rebuild.

---

## 5. The agent hierarchy and authorization as accordancy traversal

The Laniakea ranks (post-transition):

```
Core Council
    │  creates Guardian, sets root for GovOps
    ▼
Guardian  (Rank 1, lowest-level synomic agent for our purposes)
    │  governance accord with one or more Primes
    ▼
Prime (Rank 2)
    │  administers
    ▼
Halo (Rank 3)
    │  contains
    ▼
Class → Book → Unit
```

**Authorization is transitive accordancy traversal.** A GovOps's beacon is authorized for a Guardian. The Guardian is in governance accord with one or more Primes. Those Primes administer Halos. Halos contain Classes, Books, Units. To act on anything in this tree, the beacon's Guardian must reach the target via the accord/administration chain.

Two important properties:

- **Accordancy is generic.** Same shape between Guardian↔Prime, Prime↔Halo. Reusable structural relation.
- **Creation establishes accordancy as a side-effect.** When a beacon creates a new Prime via Guardian-X, the new Prime is automatically accordant with Guardian-X. When the beacon creates a Halo via Prime-Y, the new Halo is administered by Prime-Y. The creation atom IS the accordancy edge.

---

## 6. Synlang-native flexible role definitions

Rather than baking a rigid role enum into the kernel, role definitions are themselves first-class atoms.

```metta
;; Role definition — just data
(role-def book-operator
  (verbs write-book-record advance-book-state record-attestation)
  (scope-shape (in-class $class))
  (conditions (book-state-allows $verb $target)))   ; optional

;; Role grant — instantiates the template with a concrete scope
(role-grant spark-nfat-beacon book-operator (in-class spark-term-class-A))

;; Default authorization rule — kernel-level, generic
(= (can $principal $verb $target)
   (match &self
     (and (role-grant $principal $role $scope)
          (role-def $role (verbs $vs) (scope-shape $shape) ...)
          (verb-in $verb $vs)
          (scope-covers $scope $target))
     True))
```

The kernel: ~10 atoms, one rule. Everything else is data.

**What this unlocks:**

- **Ad hoc roles.** New beacon types defined by adding a `role-def` atom. No kernel change.
- **Role composition / extension.** Roles can extend others; the auth rule walks `extends` to gather verbs.
- **Parameterized scopes.** Scopes are expressions with variables — enumeration, predicate, or derived.
- **Role-specific conditions.** Some roles need extra constraints; these are part of the `role-def` and a second-tier auth rule picks them up.
- **Roles as rewriteable atoms.** Revoke a verb globally: edit the `role-def`. Attenuate a single principal's grant: edit their `role-grant`. Just `remove-atom` + `add-atom`.

**The tradeoff:** flexibility costs auditability. "Who can write to book-7?" becomes a graph traversal, not a table lookup. Mitigation: synlang IS a graph traversal language. Expose `(who-can $verb $target)` as a derived predicate.

**The meta-authority bootstrap.** Once roles are first-class data, defining/granting roles is itself privileged. Genesis principal: Core Council holds `root-authority`, which has the verbs `define-role`, `grant-role`, `revoke-role`. Two atoms in the genesis state; everything else derives from there.

---

## 7. The verb set for the kernel

Five governance/auth verbs cover the whole surface:

```
create-guardian      — Core Council direct
set-root             — Core Council, on Guardian vote
cert-beacon          — by any beacon holding cert authority
auth-beacon          — by certifier (or delegate)
revoke-*             — instant, cascades downward
```

Plus the constructors operational beacons actually call (`create-prime`, `create-halo`, `create-class`, `create-book`, `issue-unit`), each gated by an auth check that's a transitive-reach query through the accord/administration graph.

---

# PART II — Production Architecture

## 8. The simplest correct mental model

> One Synome runtime. Many beacons. Beacons are external processes that submit signed write requests; the runtime is the only thing that mutates atoms. Authorization is just a query against the current atomspace.

That's the entire architecture. Everything else is plumbing.

A beacon does exactly one thing: hold a private key, sign a proposed write, send it. The runtime does exactly one thing: verify the signature against the atomspace's record of the beacon's pubkey, check auth via match queries, accept or reject.

**What this means for the graph:**

1. **Beacon pubkeys are atoms.** `(beacon-pubkey lpha-nfat-spark <key-bytes>)` is part of what certification writes. The runtime consults this atom on every signature check. No external key registry.

2. **Constructor calls implicitly carry a verified caller.** From synlang's view, `(create-prime phoenix-team guardian-spark spark-prime)` reads as "the runtime received a valid signed request from phoenix-team." Crypto isn't modeled in synlang; we model who-said-what.

3. **The atomspace is the only source of truth for authorization.** No auth cache. Revocation is immediate and global the moment a `(cert ...)` atom is removed.

**What does NOT leak into the graph:**

Transport, beacon liveness, DDoS/overload, replication, beacon machine breakdown, beacon key compromise (auth scope caps blast radius). All handled outside synlang.

---

## 9. The gate — the trust-boundary primitive

The grounded atom that sits at the network ingress and validates incoming messages. Named **gate**, not "ingress" or "membrane" — because beacons are signal-emitters in the existing vocabulary, and gate is the natural civic counterpart (couriers from beacons arrive at the gate; the doorkeeper checks credentials).

Symmetric: every actor has both `gate-in` (receives) and `gate-out` (sends). The Synome is one (very important) lighthouse among others. Beacons can talk to other beacons directly; the Synome is just one common destination.

```
External world
      │
      │  (signed message: { beacon-id, payload, sig, nonce })
      │
      ▼
┌─────────────────────────────────────────────┐
│  GATE  (grounded native code)               │
│                                             │
│  1. Parse — reject malformed                │
│  2. Look up (beacon-pubkey $id $key) in &self│
│     — reject if absent                      │
│  3. Verify sig over payload using $key      │
│     — reject if bad                         │
│  4. Check nonce/sequence — reject if replay │
│  5. Rate-limit per beacon                   │
│                                             │
│  ⇒ emit verified internal event:            │
│     (verified-message $id $payload)         │
└─────────────────────────────────────────────┘
                    │
                    ▼
        Synlang reasoning layer
        (auth query, constructors, atom writes)
```

**Two-layer defense, each at the right level:**

| Layer | Where | What it checks | Speed |
|---|---|---|---|
| Sig check | Grounded (native crypto) | "Is this actually from claimed beacon?" | Microseconds |
| Auth check | Synlang query | "Is this beacon authorized for this action?" | Match query |

Sig check is the spam/DDoS filter. Auth check is access control. They're independent and both required.

**The pubkey atom is contractually load-bearing:** must exist for ingress to accept any message. Decert removes pubkey + cert + auths atomically — gate slams shut, no rate-limit slot consumed by the decerted beacon.

---

## 10. The heartbeat — pushing the loop into synlang

The principle: **functional core, imperative shell.** Push every decision into synlang; off-space is only the wall-clock metronome.

A grounded `delay` primitive (blocks N ms, returns) is enough to let the entire processing loop live in synlang:

```metta
(: run-forever (-> Atom))
(= (run-forever)
   (let* (($_ (try-tick))
          ($_ (delay (current-interval))))
     (run-forever)))                          ; tail call → next tick

(= (current-interval)
   (match &self (heartbeat-interval $ms) $ms))

(= (try-tick)
   (case (tick)
     (((Error $why) (log-tick-error $why))
      ($result      $result))))

(= (tick)
   (case (match &self (halt-heartbeat) halted)
     ((halted idle)
      (Empty (heartbeat)))))

(= (heartbeat)
   (let* (($_ (ingest-gate))         ; pull verified envelopes
          ($_ (drain-pending)))       ; process every pending message
     tick-complete))
```

**Off-space process becomes:**
```python
aether.boot(snapshot)
aether.eval("(run-forever)")     # blocks forever
```

Two lines. SIGTERM unwinds, atomspace flushes to disk, done.

**What this gives:**

- **Pause/resume is an atom write.** Add `(halt-heartbeat)` → pause. Remove → resume. No signals, no admin tools.
- **Interval is hot-editable.** Write `(heartbeat-interval 50)` and the next tick picks it up.
- **Multiple loops are trivial.** Fast loop for messages, slow loop for periodic bookkeeping — concurrent evals.
- **Crash-safety is automatic.** No off-space state to lose. Atomspace persists; pending messages survive.

The **AETHER runtime needs**: tail-call elimination on self-recursion, interruptible `delay`, error containment around `try-tick`. All standard for a Lisp-shaped evaluator.

---

## 11. Open verb dispatch via whitelist

Hardcoded per-verb dispatch is the wrong shape — it doesn't scale and isn't synlang-native. The right pattern uses homoiconicity: the message payload IS the s-expression to evaluate.

```metta
;; Whitelist atoms — what's externally callable at all
(external-verb create-prime  (target-arg 0))
(external-verb create-halo   (target-arg 0))
(external-verb cert-beacon   (target-arg 0))
(external-verb auth-beacon   (target-arg 0))
;; ... one atom per externally-callable verb

;; Single dispatch rule — no per-verb branches
(= (dispatch $caller $payload)
   (let* (($verb        (car $payload))
          ($args        (cdr $payload))
          ($whitelisted (match &self (external-verb $verb $_) True))
          ($target      (target-of $payload))
          ($authorized  (can $caller $verb $target)))
     (case (and $whitelisted $authorized)
       ((True  (eval (cons $verb (cons $caller $args))))    ; inject caller, evaluate
        (False (Error rejected $payload))))))
```

**Properties:**

- **Adding a verb = one atom + a constructor.** No editing of dispatch.
- **Closed by default.** Without an `(external-verb …)` atom, a verb is not externally callable, even if its handler exists.
- **Auth and dispatch are orthogonal.** Whitelist says "callable from outside at all"; auth says "this caller can call it on this target." Two independent gates.
- **The "target convention" is explicit metadata.** `(target-arg N)` field tells dispatch where to look. Different verbs put their target in different positions; dispatcher handles all.

Two small commitments this requires:
1. Every external verb has a target slot (use `*` for verbs whose authorization isn't target-bounded).
2. Caller injection is convention. Constructors take `$caller` as their first arg; dispatch injects it.

---

# PART III — Scaling and Multi-Space

## 12. The Synome is multi-Space by design

The architecture already commits to logical multi-Space via the artifact tiers (synart / telart / embart). The user's scoping decision: **focus on synart for now** (telart and embart are very different and can be addressed later).

Within synart, access patterns are wildly heterogeneous. Functional partitioning into sub-Spaces falls out naturally:

| Sub-Space | Contents | Read freq | Write freq | Volume |
|---|---|---|---|---|
| `&genesis` | Atlas, Axioms, Language Intent config | Constant | Near-immutable | Small |
| `&governance` | Cert, auth, agent registry, beacon pubkeys, root atoms | Constant | Slow (governance-paced) | Small-medium |
| `&operational` | Books, units, settlement records, attestations | Constant | Fast | Large |
| `&library` | Mesh knowledge, beliefs, RSI artifacts | Constant | Very fast (evidence flow) | Huge |

Mixing all of these in one physical Space puts a small slow-write governance lookup in the same index as a high-throughput evidence stream. Different profiles want different physical structures.

---

## 13. Hyperon's lesson: cross-Space writes are direct `add-atom`

Documented Hyperon mechanism for moving data:

> A space writes to another space by **holding a reference to that other space and calling `add-atom` on it.**

```metta
!(add-atom &target-space (Some Fact Here))
```

There is **no separate "data movement" primitive in Hyperon.** Only reads (`match` parameterized by Space) and writes (`add-atom` parameterized by Space). All "movement" happens at the storage layer (DAS rebalancing, proxy routing) invisibly.

This **simplifies our design significantly.** Earlier I had every cross-Space write going through gate-out/gate-in. That was wrong. The right factoring:

| Boundary type | Sig check | Auth check | Mechanism |
|---|---|---|---|
| External beacon → Synome | Yes (gate) | Yes (constructor) | Signed message, gate-in queue |
| One Synome runtime → another (federated) | Yes (gate) | Yes (constructor) | Signed message, gate-in queue |
| Cross-Space within one Synome runtime | **No** | Yes (constructor) | Direct `(add-atom &other-space ...)` |
| Same-Space write | No | Yes (constructor) | Direct `(add-atom &self ...)` |

**The gate is for *trust* boundaries, not *Space* boundaries.** Within one Synome runtime, all Spaces are in the same trust domain. Cross-Space writes are direct `add-atom`. The auth check inside the constructor is enough.

Concrete example:

```metta
(= (create-prime $caller $guardian $prime-id)
   (case (can $caller create-prime $guardian)        ; auth check (synlang)
     ((True
        (let* (($_ (add-atom &operational (: $prime-id Prime)))
               ($_ (add-atom &governance  (accordant $guardian $prime-id))))
          (Created prime $prime-id)))
      (False (Error unauthorized $caller)))))
```

Two `add-atom` calls into different Spaces. No gate-out, no message. The auth check is a regular synlang match against `&governance`.

---

## 14. Per-Space queues, single gate

If 1000 Spaces each have to filter every incoming message, that's wasteful. The right model: **one gate (trust boundary), N per-Space incoming queues, routing happens after verification.**

```
External beacons
   ↓ signed messages (each tagged with a verb)
   ↓
┌──────────────────────────────────────────────────┐
│   GATE  (single trust boundary)                  │
│   1. parse                                       │
│   2. verify sig (pubkey from replicated         │
│      &governance, lookup is local)               │
│   3. nonce/rate-limit                            │
│   4. read (verb-target-space $verb $space)       │
│   5. route verified message to that Space        │
└──────────────────────────────────────────────────┘
        ↓                 ↓               ↓
┌────────────┐    ┌────────────┐    ┌────────────┐
│ &incoming- │    │ &incoming- │    │ &incoming- │
│  governance│    │  operational│    │  library   │
└─────┬──────┘    └─────┬──────┘    └─────┬──────┘
      │ heartbeat       │                 │
      ▼                 ▼                 ▼
   &governance      &operational       &library
```

**Routing-as-data is now load-bearing.** The atom `(verb-target-space create-prime &operational)` is what tells the gate where messages go. Adding a new Space = register its verbs in the routing table. Repartitioning = edit the routing atoms. Senders never know which Space their write lands in.

The routing data is itself a hub atom — replicated to wherever the gate runs.

**Each heartbeat only sees its own queue.** Crypto verification and routing happen once at the gate, not per-Space.

---

## 15. Goertzel hardware: locality is physics

Goertzel/St. Clair's pattern-matching chip design (PIM grid of "cubes" with internal "vaults," graph partitioned across cubes, double-mesh trick for migrations) commits us to specific physical realities:

1. **Locality is enforced by physics.** Each cube holds a sub-graph; intra-cube queries are fast; inter-cube transfers are slow. This isn't an abstraction we can paper over — it's the cost structure of the hardware.

2. **Repartitioning requires freezing the grid.** Hence the double-mesh trick (two grids, freeze one to migrate, sync after). You cannot rebalance atoms while serving queries.

3. **Hub replication is the standard pattern.** Zipfian graphs have a few high-degree hubs; replicate them across cubes. Exactly the right pattern for cert/auth/pubkey atoms — small, ubiquitously read.

4. **Slowly-changing graphs are the sweet spot.** Wikipedia-in-logic. Pre-crunched datasets. Synart fits this perfectly. Aggressive mutation (which we don't have, because append-only) is what doesn't fit.

5. **The system is heterogeneous.** Pattern-matching chip + neural chip + hyper-vector chip + CPU, sharing memory via fast interconnect. So our "single Synome" concept is, at the hardware level, already multi-substrate.

**The temporal calibration that matters:** "repartitioning is expensive" is true at the cognitive scale (μs-ms, super-AGI doing RSI). At governance pace (days-months), repartitioning is just a scheduled migration. We can pick a partition layout for Phase 1, plan to refactor as we grow, and use the fork-and-promote pattern during the migration window.

| Scale | Repartitioning cost | Tolerance |
|---|---|---|
| **Cognition** (μs–ms) | Fatal — must use double-mesh | Cannot freeze |
| **Operational** (sec–min) | Painful — interrupts service | Tolerate seconds |
| **Settlement cycle** (hours–days) | Manageable — schedule around it | Tolerate maintenance windows |
| **Governance** (days–months) | Normal — scheduled migration | Tolerate hours of downtime |
| **Constitutional** (years) | Trivial — plenty of warning | Multi-day reorganizations are fine |

So the partition layout is a *high-stakes initial choice* but **not eternal**. Migration freedom (P6 routing-as-data, P15 Spaces split/merge) matters more than getting the initial split exactly right.

---

## 16. The 16 migration principles

Commitments that preserve flexibility across hardware and scale evolution:

### Locality
- **P1. Space is the unit of locality.** Within: pretend it's all one machine. Across: pretend you're sending a network message.
- **P2. Most operations are single-Space.** Cross-Space writes are explicit, named, and rare.
- **P3. Co-locate edges with their dominant access pattern.** `(accordant ...)` lives in `&governance` because that's the auth-read side.

### Naming
- **P4. Space references are logical names.** `&governance` is a name, not a physical pointer. Runtime maintains `(space-location $name $physical-address)`.
- **P5. Content addressing for atoms.** Already a permanent design choice. Atom hash = identity, regardless of which Space it lives in.
- **P6. Routing is data.** Where does verb V write? Look up `(verb-target-space V $space)`. Migrate by editing one atom.

### Causality
- **P7. Append-only.** Already a commitment. Snapshots / replication / rollback / audit are all trivial. Mutations would force complex coordination.
- **P8. Idempotent writes.** Content-addressed names or explicit nonces. Retries are always safe.
- **P9. No global ordering.** Within a Space: append-only log. Across: only causality (via nonces / message-IDs).

### Visibility
- **P10. Cross-Space dependencies are explicit.** A constructor that reads `&governance` and writes `&operational` says so in its definition.
- **P11. Provenance is first-class.** Every write knows what message produced it. Every belief knows what evidence produced it.
- **P12. Read/write patterns documented per verb.** `(verb-reads V $space)`, `(verb-writes V $space)`.

### Migration
- **P13. Partition layout is foundational but not eternal.** Initial split deserves thought; later repartitioning is a normal governance operation (at governance pace, not cognitive pace). Migration freedom > getting the initial split perfect.
- **P14. Each Space can run its own runtime version.** Stable gate protocol; independent AETHER upgrades per Space.
- **P15. Spaces can split or merge without breaking references.** Falls out of P4-P6.
- **P16. Major restructuring uses fork-promote (double-mesh).** Already in the architecture (crystallization interface). Generalizable: any expensive operation that would freeze the live system runs on a shadow.

---

## 17. The seven Phase 1 commitments

Most of the multi-Space discussion is deferrable. Build single-Space, single-gate, single-heartbeat — but commit to these seven from day 1, because retrofitting them later is genuinely painful:

**1. Space is always a parameter, never implicit.**
Write `(add-atom &operational ...)` and `(match &governance ...)` from day 1, even when both names alias to the same physical Space. Constructor signatures document what they touch; runtime can later split them without code changes.

**2. Append-only writes.**
Always `(add-atom ...)`. Remove via `(remove-atom ...)` only when explicitly modeling revocation. Required for: replication, audit, fork/promote, idempotency, content-addressing.

**3. Content-addressed names.**
A new entity's ID is a hash of (creator + nonce + content) or some content-determined symbol — not arbitrary auto-incrementing. Cross-Space references survive migration; idempotent retries are free.

**4. Open verb dispatch via whitelist atoms.**
`(external-verb $v ...)` pattern. When routing-as-data arrives, you add `(verb-target-space ...)` atoms alongside — dispatch shape is unchanged.

**5. The gate as a real primitive at the trust boundary, even if trivial.**
External writes go through `gate-in` even in Phase 1. Phase 1 gate may do basic sig verification and skip rate-limiting; what matters is that constructors only run on verified messages.

**6. The `(can $caller $verb $target)` predicate reads from a named auth Space.**
Today `&governance` may be the same physical Space as everything else, but the predicate is written `(match &governance ...)`. When `&governance` becomes its own Space later, no constructor changes.

**7. Idempotent constructors.**
Calling `(create-prime same-args)` twice produces the same atom or harmlessly no-ops. Achieved via content-addressing + check-before-write. Required for: retries, async replays, gate redelivery.

**The core insight:** these aren't really about scale — they're good design hygiene that incidentally makes scaling free. If you build a clean single-Space system that does these seven, "scale to multi-Space" is purely a runtime change: bind the Space names to different physical stores, add routing data, replicate hub atoms. The synlang code doesn't change.

**What's safely deferrable:**

- Multiple physical Spaces (start with one)
- Hub replication (no replication needed when there's only one Space)
- Per-Space gates and heartbeats (one of each is fine)
- Sharding by head-symbol within a Space
- Multi-core / PIM optimization
- Federation across Synome instances
- Double-mesh trick for migrations
- The routing atoms themselves (`(verb-target-space ...)`)

---

# PART IV — The Bootstrap Picture

## 18. Genesis state

Two atoms in genesis:

```metta
;; The meta-role that holds authority to define/grant/revoke roles
(role-def root-authority
  (verbs create-guardian set-root authorize-govops
         define-role grant-role revoke-role))

;; Core Council holds it
(role-grant core-council root-authority (scope unrestricted))
```

That's the seed. Everything else — every Guardian, every GovOps root, every operational beacon, every cert, every auth — derives from writes whose authorization traces back to this grant.

## 19. The bootstrap sequence

```metta
;; 1. Core Council creates a Guardian
(create-guardian core-council guardian-spark)
;; ⇒ adds (: guardian-spark Guardian)

;; 2. Guardian token-holders vote; Core Council enacts and sets the root
;;    for a GovOps under that Guardian
(set-root core-council phoenix-govops-root guardian-spark)
;; ⇒ adds (root phoenix-govops-root for-guardian guardian-spark)
;; ⇒ adds (beacon-pubkey phoenix-govops-root <key>)

;; 3. The GovOps root certifies operational beacons
(cert-beacon phoenix-govops-root lpha-nfat-spark)
;; ⇒ adds (cert lpha-nfat-spark by phoenix-govops-root)
;; ⇒ adds (beacon-pubkey lpha-nfat-spark <key>)

;; 4. The GovOps root authorizes specific scopes
(auth-beacon phoenix-govops-root lpha-nfat-spark
             create-book (in-class spark-class-A))

;; 5. Operational beacons make construction calls
;;    (signed messages arrive via gate-in; dispatch invokes constructor)
(create-prime lpha-nfat-spark guardian-spark spark-prime)
;; ⇒ ... and so on down the create-class / create-book / issue-unit chain
```

Every step's authority trace: operational beacon → GovOps root → Guardian → Core Council → genesis grant.

---

# PART V — How to Proceed

## 20. The order of operations to write the synart kernel

Suggested implementation order, each step buildable and testable in isolation:

1. **Genesis + the kernel auth rule.** Write `role-def`, `role-grant`, `(can $p $v $t)`. Seed Core Council with `root-authority`. Verify the rule answers correctly for trivial cases.

2. **The five governance/auth verbs.** `create-guardian`, `set-root`, `cert-beacon`, `auth-beacon`, `revoke-*`. Each is a constructor with an auth check.

3. **The gate primitive (trivial version).** Sig verification reading from `&governance`'s pubkey atoms; emits `(verified-message ...)` to `&incoming`. Phase 1 may stub the crypto; the *shape* is what matters.

4. **The dispatch + heartbeat loop in synlang.** `(external-verb …)` whitelist; the `(dispatch …)` rule; `(run-forever)` calling `(heartbeat)` calling `(drain-pending)`.

5. **The construction verbs in order.** `create-prime`, `create-halo`, `create-class`, `create-book`, `issue-unit`. Each builds on the accordancy chain established by predecessors.

6. **Test with a multi-Space-shaped layout.** All four named Spaces (`&genesis`, `&governance`, `&operational`, `&library`) aliased to one physical Space. Write code as if they were already separate.

## 21. Things still open / decisions to make later

- **Cert ceiling formal semantics.** Is full inheritance (child cert ceiling = parent's) the right default? Probably yes, but document explicitly.
- **Operational beacon as a kind, or just a beacon with no cert authority?** Lean: latter. Cert authority itself is an auth that may or may not be granted.
- **Voting machinery for Guardian token-holder vote.** Phase 1: opaque (Core Council enacts on assumed-valid vote). Future: model voting in synlang.
- **Schema for the buybox / init pattern in `issue-unit`.** Defer until working on the issue-unit constructor.
- **Telart and embart Space architecture.** Out of scope for this discussion. Each will be very different from synart and from each other.
- **Cross-Synome federation.** Out of scope for Phase 1. The gate-out/gate-in design accommodates it when needed.
- **Specific physical hardware bindings (PIM, CXL, etc.).** Out of scope. The principles preserve hardware-portability.

---

## 22. The one-line summary

**Build a single-Space synart with the seven Phase 1 commitments. The shape of the code is multi-Space; the implementation is single-Space. Scale becomes a runtime concern, never a synlang rewrite.**
