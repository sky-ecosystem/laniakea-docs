# Synart — Access Control and Runtime Architecture

**Status:** Working notes from design discussion. Companion to `topology.md` (structure), `synlang-patterns.md` (code library), and `syn-overview.md` (concept map).
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

2. **Constructor calls implicitly carry a verified caller.** From synlang's view, `(create-prime spark-govops-root ozone spark-prime)` reads as "the runtime received a valid signed request from spark-govops-root." Crypto isn't modeled in synlang; we model who-said-what.

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

> **Note:** This section documents the synserv loop specifically — the
> concrete `(run-forever)` shape that the canonical synserv runs. The
> *abstract* identity-driven boot model that this is one application
> of (any conforming runtime + any synart-resolved loop, parameterized
> by identity) lives in `boot-model.md`. Read this section for "how
> synserv runs"; read `boot-model.md` for "how any role boots, of which
> synserv is one."

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

## 11.5. Identity-driven boot

The §10 heartbeat shape generalizes: **every loop in the synome boots
the same way.** Different identities resolve to different loops; the
runtime invocation is uniform.

```
noemar boot --identity=X --key=path/to/key.pem --synart=endpoint
   ↓
mount synart
   ↓
look up X in &core-registry-beacon → loop pointer
   ↓
evaluate (run-forever) with that Space as &self
```

What's local-only: the private key file. Everything else (which loop,
which Spaces to subscribe, which auth applies, which gates to run)
flows from synart based on identity.

Synserv boots with this same procedure — its identity (e.g.,
`core-synserv-canonical`) resolves to `&core-loop-synserv`. Beacons,
sentinels, archive embs, verifier embs, endoscrapers all use the same
boot path with their own identities resolving to their own loop
Spaces.

For depth — including the spec/instance collapse (`Spaces are the
program; runtimes are the interpreter`), shadow execution properties,
hot-swap modes, and failure handling — see `boot-model.md` (canonical).

---

## 11.6. The call-out primitive

A synlang form for synart-resolved loops to consult local cognition at
strategy-designated points. The synart→telart bridge.

```metta
(call-out $service
   (inputs <input-atoms…>)
   (output-shape <expected-shape>))
```

When a loop hits a `(call-out …)`, the runtime resolves `$service`
against the booting identity's telart call-out registry, marshals
inputs across the synart→telart boundary, validates the response shape,
and returns the validated value to the surrounding synart code.

The call-out is the **only sanctioned mechanism** for synart-resolved
code to consult local cognition. Direct telart access from synart loops
is forbidden because it would break the audit story.

Verifiability profile:

- Inputs to the call-out: fully verifiable (derived from synart state).
- Call-out output: NOT verifiable (non-deterministic LLM/cognition).
- Output-shape conformance: verifiable.
- What the strategy does with the output: fully verifiable.

This is what lets Sentinel-Baseline run ~95% verifiable code while
still consulting LLM cognition at carefully-chosen decision points —
wardens re-derive everything except the LLM output and halt on
disagreement past tolerance.

For the canonical synlang form and the Sentinel formation patterns
that use it, see `synlang-patterns.md` §5-§6.

---

# PART III — Scaling and Multi-Space

## 12. The Synome is multi-Space by design

The architecture already commits to logical multi-Space via the artifact tiers (synart / telart / embart). The scoping for this document: **focus on synart** (telart and embart are different and can be addressed later).

Within synart, access patterns are wildly heterogeneous and functional partitioning into sub-Spaces falls out naturally. The canonical layout is the **six-layer synome root + entart tree** defined in `topology.md` §6:

- **Constitutional:** `&core-root`, `&core-telos`, `&core-skeleton`, `&core-governance`, `&core-protocol`
- **Framework:** `&core-framework-risk`, `&core-framework-distribution`, `&core-framework-fee`
- **Registry:** `&core-registry-entity`, `&core-registry-beacon`, `&core-registry-contract`
- **Aggregation:** `&core-settlement`, `&core-escalation`, `&core-endoscrapers`
- **Executable:** `&core-syngate`, `&core-telgate`, `&core-loop-<class>`, `&core-recipe-*`
- **Library:** `&core-library-runtime-<impl>`, `&core-library-telseed-<config>`, `&core-library-corpus-<domain>`, `&core-library-published-<topic>`
- **Per-entity entart subtrees:** `&entity-<type>-<id>-<sub-kind>` (Guardian / Prime / Halo / their books / per-entity sentinel formations)

Mixing all of these in one physical Space would put a small slow-write governance lookup in the same index as a high-throughput event stream from a busy book — different profiles want different physical structures. See `topology.md` for the full taxonomy and the four meta-patterns (frameworks / registries / aggregations / specifications) that govern composition.

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

Concrete example: creating a Prime writes to multiple Spaces atomically — the new Prime's root entart, the parent Guardian's sub-entart registry, and the global entity registry.

```metta
(= (create-prime $caller $guardian $prime-id $prime-root-space)
   (case (can $caller create-prime $guardian)              ; auth check (synlang)
     ((True
        (let* (($_ (add-atom $prime-root-space             (synent $prime-id)))
               ($_ (add-atom $prime-root-space             (parent-entart $prime-id $guardian)))
               ($_ (add-atom &entity-guardian-ozone-root   (sub-entart $guardian $prime-id $prime-root-space)))
               ($_ (add-atom &core-registry-entity         (entart-id $prime-id prime $prime-root-space))))
          (Created prime $prime-id)))
      (False (Error unauthorized $caller)))))
```

Four `add-atom` calls into different Spaces. No gate-out, no message. The auth check is a regular synlang match wherever auth atoms live for this verb.

---

## 14. Per-Space queues, single gate

If many Spaces each have to filter every incoming message, that's wasteful. The right model: **one gate (trust boundary), N per-Space incoming queues, routing happens after verification.**

```
External beacons
   ↓ signed messages (each tagged with a verb + target)
   ↓
┌──────────────────────────────────────────────────┐
│   GATE  (single trust boundary)                  │
│   1. parse                                       │
│   2. verify sig (pubkey from replicated          │
│      &core-registry-beacon, lookup is local)     │
│   3. nonce/rate-limit                            │
│   4. resolve (verb-target-space $verb $target)   │
│   5. route verified message to that Space        │
└──────────────────────────────────────────────────┘
        ↓                       ↓                       ↓
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ &incoming-       │  │ &incoming-       │  │ &incoming-       │
│  core-governance │  │  entity-prime-   │  │  entity-halo-    │
│                  │  │  spark-root      │  │  spark-term-...  │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         │ heartbeat            │                     │
         ▼                      ▼                     ▼
   &core-governance     &entity-prime-       &entity-halo-
                        spark-root           spark-term-…
```

**Routing-as-data is now load-bearing.** The atom `(verb-target-space create-prime &core-registry-entity)` is what tells the gate where messages go. Adding a new entart = register its inbound verbs in the routing table. Repartitioning = edit the routing atoms. Senders never know which Space their write lands in.

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
- **P3. Co-locate edges with their dominant access pattern.** Auth atoms live in the entart owning the verb's target — that's the side reading them at gate time.

### Naming
- **P4. Space references are logical names.** `&core-governance` and `&entity-prime-spark-root` are names, not physical pointers. Runtime maintains `(space-location $name $physical-address)`.
- **P5. Content addressing for atoms.** Already a permanent design choice. Atom hash = identity, regardless of which Space it lives in.
- **P6. Routing is data.** Where does verb V write? Look up `(verb-target-space V $space)`. Migrate by editing one atom.

### Causality
- **P7. Append-only.** Already a commitment. Snapshots / replication / rollback / audit are all trivial. Mutations would force complex coordination.
- **P8. Idempotent writes.** Content-addressed names or explicit nonces. Retries are always safe.
- **P9. No global ordering.** Within a Space: append-only log. Across: only causality (via nonces / message-IDs).

### Visibility
- **P10. Cross-Space dependencies are explicit.** A constructor that reads `&core-registry-beacon` and writes into an entart subtree says so in its definition.
- **P11. Provenance is first-class.** Every write knows what message produced it. Every belief knows what evidence produced it.
- **P12. Read/write patterns documented per verb.** `(verb-reads V $space)`, `(verb-writes V $space)`.

### Migration
- **P13. Partition layout is foundational but not eternal.** Initial split deserves thought; later repartitioning is a normal governance operation (at governance pace, not cognitive pace). Migration freedom > getting the initial split perfect.
- **P14. Each Space can run its own runtime version.** Stable gate protocol; independent AETHER upgrades per Space.
- **P15. Spaces can split or merge without breaking references.** Falls out of P4-P6.
- **P16. Major restructuring uses fork-promote (double-mesh).** Already in the architecture (crystallization interface). Generalizable: any expensive operation that would freeze the live system runs on a shadow.

---

## 17. The seven Phase 1 commitments

> These are the **original seven**, with full rationale below. `topology.md` §19 adds **six more** (rule-reads declarations, registry-mediated cross-Space refs, scatter-gather rule shape, rule publication metadata, the entart tree itself, and the synart-as-program commitment) — making **thirteen total**. The seven here remain canonical; the additions cover structural commitments that weren't in scope when this section was written.

Most of the multi-Space discussion is deferrable. Build single-Space, single-gate, single-heartbeat — but commit to these seven from day 1, because retrofitting them later is genuinely painful:

**1. Space is always a parameter, never implicit.**
Write `(add-atom &entity-prime-spark-root ...)` and `(match &core-governance ...)` from day 1, even when both names alias to the same physical Space. Constructor signatures document what they touch; runtime can later split them without code changes.

**2. Append-only writes.**
Always `(add-atom ...)`. Remove via `(remove-atom ...)` only when explicitly modeling revocation. Required for: replication, audit, fork/promote, idempotency, content-addressing.

**3. Content-addressed names.**
A new entity's ID is a hash of (creator + nonce + content) or some content-determined symbol — not arbitrary auto-incrementing. Cross-Space references survive migration; idempotent retries are free.

**4. Open verb dispatch via whitelist atoms.**
`(external-verb $v ...)` pattern. When routing-as-data arrives, you add `(verb-target-space ...)` atoms alongside — dispatch shape is unchanged.

**5. The gate as a real primitive at the trust boundary, even if trivial.**
External writes go through `gate-in` even in Phase 1. Phase 1 gate may do basic sig verification and skip rate-limiting; what matters is that constructors only run on verified messages.

**6. The `(can $caller $verb $target)` predicate reads from a named auth Space.**
Today `&core-governance` may be the same physical Space as everything else, but the predicate is written `(match &core-governance ...)` (or against the appropriate entart Space). When the physical layout splits later, no constructor changes.

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

Two atoms ship in the initial state of `&core-governance` — there is no separate `&genesis` Space, the bootstrap seed lives directly in the constitutional layer (per `topology.md` §6):

```metta
;; in &core-governance — initial state

;; The meta-role that holds authority to define/grant/revoke roles
(role-def root-authority
  (verbs create-guardian set-root authorize-govops
         define-role grant-role revoke-role))

;; Core Council holds it
(role-grant core-council root-authority (scope unrestricted))
```

That's the seed. Everything else — every Guardian entart, every GovOps root, every operational beacon, every cert, every auth — derives from writes whose authorization traces back to this grant.

## 19. The bootstrap sequence

```metta
;; 1. Core Council creates the single operational Guardian — Ozone
(create-guardian core-council ozone)
;; ⇒ adds (: ozone Guardian)

;; 2. Ozone token-holders vote; Core Council enacts and sets a root
;;    for each GovOps team operating under Ozone (one per administered
;;    entity — Spark operator, Grove operator, USGE operator, etc.)
(set-root core-council spark-govops-root ozone)
;; ⇒ adds (root spark-govops-root for-guardian ozone)
;; ⇒ adds (beacon-pubkey spark-govops-root <key>)

(set-root core-council usge-govops-root ozone)
;; ⇒ adds (root usge-govops-root for-guardian ozone)
;; ⇒ adds (beacon-pubkey usge-govops-root <key>)

;; 3. Each GovOps root certifies its own operational beacons
(cert-beacon spark-govops-root lpha-nfat-spark)
;; ⇒ adds (cert lpha-nfat-spark by spark-govops-root)
;; ⇒ adds (beacon-pubkey lpha-nfat-spark <key>)

;; 4. The GovOps root authorizes specific scopes
(auth-beacon spark-govops-root lpha-nfat-spark
             create-book (in-class spark-class-A))

;; 5. Operational beacons make construction calls
;;    (signed messages arrive via gate-in; dispatch invokes constructor)
(create-prime lpha-nfat-spark ozone spark-prime)
;; ⇒ ... and so on down the create-class / create-book / issue-unit chain

;; 6. The Generator is created the same way — accordant to Ozone, not a
;;    separate Guardian
(create-generator lpha-usge-bootstrap ozone usge)
;; ⇒ adds (synent usge), (parent-entart usge ozone)
```

Every step's authority trace: operational beacon → GovOps root → Ozone → Core Council → genesis grant. Multiple GovOps teams coexist under Ozone; each is scoped to the entity it administers.

---

# PART V — How to Proceed

## 20. The order of operations to write the synart kernel

Suggested implementation order, each step buildable and testable in isolation:

1. **Genesis + the kernel auth rule.** Write `role-def`, `role-grant`, `(can $p $v $t)`. Seed Core Council with `root-authority`. Verify the rule answers correctly for trivial cases.

2. **The five governance/auth verbs.** `create-guardian`, `set-root`, `cert-beacon`, `auth-beacon`, `revoke-*`. Each is a constructor with an auth check.

3. **The gate primitive (trivial version).** Sig verification reading from `&core-registry-beacon`'s pubkey atoms; emits `(verified-message ...)` to `&incoming`. Phase 1 may stub the crypto; the *shape* is what matters.

4. **The dispatch + heartbeat loop in synlang.** `(external-verb …)` whitelist; the `(dispatch …)` rule; `(run-forever)` calling `(heartbeat)` calling `(drain-pending)`.

5. **The construction verbs in order.** `create-prime`, `create-halo`, `create-class`, `create-book`, `issue-unit`. Each builds on the accordancy chain established by predecessors.

6. **Test with the entart-tree-shaped layout.** Synome root `&core-*` Spaces plus a small entart subtree (one Guardian → one Prime → one Halo → one or two book leaves) all aliased to one physical Space. Write code as if they were already separate — the synlang is identical whether they're one backing store or many.

## 20.5. Telseed bootstrap

A new teleonome comes online via a telseed — a minimal package
(atomspace runtime + connection info + sync prefs + identity material +
initial endowment) that connects to live synart and grows from there.
Telseeds don't ship knowledge corpora; they stream from synart on
connect.

The bootstrap arc:

1. Boot atomspace runtime with telseed config
2. Connect to synserv (or peer tel)
3. Sync requested synart slice (per sync-policy)
4. Telart instantiation — bootstrap procedure (now synced from synart)
   makes calls about telart sub-Space layout, registers identity
5. First emb spawn — replicate telart to additional embs for resilience
6. Begin dreamer / beacon loops; first revenue
7. Compounding: revenue + RSI → telart growth → more recipe-taking

Concept: `syn-tel-emb.md` §4-§5. Worked trace with concrete identities
and timings: `telseed-bootstrap-example.md`.

The synart-access perspective on this: telseed bootstrap is just
identity-driven boot (§11.5 / `boot-model.md`) starting from a fresh
identity that has no prior synart presence. The key extra step is
that the founder vouches for the new identity through their existing
auth chain, letting the new tel register through the gate.

---

## 21. Things still open / decisions to make later

- **Cert ceiling formal semantics.** Is full inheritance (child cert ceiling = parent's) the right default? Probably yes, but document explicitly.
- **Operational beacon as a kind, or just a beacon with no cert authority?** Lean: latter. Cert authority itself is an auth that may or may not be granted.
- **Voting machinery for Guardian token-holder vote.** Phase 1: opaque (Core Council enacts on assumed-valid vote). Future: model voting in synlang.
- **Schema for the buybox / init pattern in `issue-unit`.** Defer until working on the issue-unit constructor.
- **Cross-Synome federation.** Out of scope for Phase 1. The gate-out/gate-in design accommodates it when needed; telgate code applies symmetrically across synome boundaries.
- **Specific physical hardware bindings (PIM, CXL, etc.).** Out of scope. The principles preserve hardware-portability.
- **Exoscraper architecture.** Out of scope for current design. Endoscrapers (deterministic chain reads) are in scope; exoscrapers (external API reads with insurance) are deferred — see `topology.md` §6.

---

## 22. The one-line summary

**Build a single-Space synart with the seven Phase 1 commitments documented here (thirteen total per `topology.md` §19); identity-driven boot (§11.5 / `boot-model.md`) makes the synart self-hosting; the call-out primitive (§11.6) admits local cognition at synart-designated points; the shape of the code is multi-Space; the implementation is single-Space; scale becomes a runtime concern, never a synlang rewrite.**
