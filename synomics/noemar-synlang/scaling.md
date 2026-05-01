# Scaling — Synart Spaces, Sharding, and Distributed Computation

How the canonical synart partitions, replicates, composes, and propagates
rules across Spaces. Companion to `syn-overview.md` and `synart-access-and-runtime.md`.

The driving requirements:

- **Modular sync.** A teleonome can subscribe to any subset of the synart;
  serious teleonomes sync everything; light embodiments may sync just one
  Prime's USDS book. Both must be first-class.
- **Locality of execution.** Rules execute close to the atoms they read.
  Cross-Space coordination is messaging, not centralized pulling.
- **Self-updating subscriptions.** A teleonome watching only one Space
  receives rule updates that affect that Space without needing to track
  governance.

---

## TL;DR — the architecture in one page

**The six load-bearing decisions:**

1. **Spaces are grounded atoms with a uniform API.** Name them in synlang
   from day 1; the binding from logical name → physical backend is a
   runtime concern. Splitting later doesn't change synlang code.
2. **Synart is a tree of entarts.** Each synomic entity (Guardian, Prime,
   Halo, …) owns an **entart** — a subtree of Spaces rooted at its own
   root Space. The root holds identity, registries, auth, policy, and
   cross-sub-entart rules. The synart is the union of all entarts.
3. **Each Space is locally consistent for some purpose.** A book Space
   is self-contained for book-local reasoning; an entart root is
   self-contained for that entity's policy. Cross-Space rules give
   *aggregate views* that don't exist in any single Space.
4. **Rules are atoms, co-located with data.** If you don't sync a Space,
   you don't get its rules — they're not in your runtime at all. Partial
   sync = partial capabilities, with no silent breakage.
5. **Local-by-default, scatter-gather for global.** Cross-Space rules
   ship a portable local body (using `&self`) to each target, run
   against local data, return small results, aggregate. No central
   pulling.
6. **Rule updates propagate via the same replication channel as data.**
   Master rule in entart root → synserv projects to each target Space →
   subscribers replicate normally → rules stay current. No special code
   path.

**The natural entart tree:**

```
synome (root entart)
  &skeleton              universal axioms — replicated everywhere
  &genesis               Core Council, root authority
  &global-settlement     Sky-wide rollups
  │
  └── guardian-spark entart
        &spark-guardian
        │
        └── soter-govops entart
              &soter-govops
              │
              └── spark-prime entart
                    &spark-prime    auth, policies, halo registry, cross-halo rules
                    │
                    ├── spark-term-halo entart
                    │     &spark-term-halo        halo policies, book registry
                    │     &spark-term-usds-book   leaf
                    │     &spark-term-cnys-book   leaf
                    │
                    └── spark-trade-halo entart
                          &spark-trade-halo
                          &spark-trade-amm-book
```

Each entart root names its sub-entarts and leaf Spaces via registries;
authority and policy cascade down with **layered tightening** (each level
can add stricter rules but never weaken parent rules).

**Sharding has four orthogonal axes:** authority (genesis / governance /
operational / library), tenant (per-Prime, per-Halo), temperature (hot /
warm / cold), cadence (immutable / slow / fast / probabilistic). A
single Space sits at one point on each.

**Partial sync semantics:** a rule's reads are declared up front; runtime
refuses to evaluate a rule whose reads aren't satisfied. Default for
unbound Spaces is hard-fail; lazy-fetch is opt-in; empty-match is never
the default (silent wrong answers).

**Twelve Phase 1 commitments** (§20): seven original + five added by this
doc — every rule declares its reads (8), cross-Space references go
through registries (9), cross-Space rules are scatter-gather (10), global
rules carry publication metadata (11), entarts are subtrees with
parent→child reference asymmetry (12).

---

## Section map

| § | Topic | Core idea |
|---|---|---|
| 1 | Hyperon Spaces basics | Spaces as grounded atoms; DAS as substrate; gate ≠ Space boundary |
| 2 | Taxonomy mapping | Synome / telart / embart aligns with Hyperon's "many small + shared canonical + deep distributed" |
| 3 | Four sharding axes | Authority / tenant / temperature / cadence — orthogonal |
| 4 | The entart concept | Synart is a tree of entity-rooted subtrees; root Space = entity identity + registry |
| 5 | Example entart | Spark Prime's entart: root + halo entarts + leaf book Spaces |
| 6 | Registry pattern | Root names sub-entarts and sub-spaces; rules iterate registry |
| 7 | Asymmetry rule | Parent → child references only; peers go through common ancestor |
| 8 | Partial sync basics | Rules co-locate with data; missing Space = missing capability |
| 9 | The dangerous case | Have rule but not all reads → must hard-fail, never empty-match |
| 10 | Declarative reads | `(rule-reads $rule $space)` enables capability introspection |
| 11 | Local consistency | Each Space self-complete for some purpose; aggregates need union |
| 12 | Local-by-default principle | Scatter-gather for cross-Space; push code to data |
| 13 | Two-step rule shape | Portable `&self` body + global declaration with targets + combiner |
| 14 | What scatter-gather buys | Locality, partial-sync participation, actor model, bounded trust |
| 15 | Aggregator design | Sum/max/count trivial; percentiles need sketches |
| 16 | Rule publication | Master + projections; synserv broadcasts on update |
| 17 | Materialized views + CDC | Names what we reinvented |
| 18 | Subtleties | Transitive deps; version skew; eager vs lazy fetch |
| 19 | Subscription patterns | Real teleonome shapes lined up with the entart split |
| 20 | Phase 1 commitments | Twelve total — hygiene that makes scaling free |
| 21 | One-line summary | The whole architecture compressed |

---

## 1. What's load-bearing about Hyperon Spaces

Four facts from the Hyperon model do most of the work:

1. **Spaces are grounded atoms with a uniform API.** `&operational` is a
   value; `(match &operational …)` is a regular call. Synlang names Spaces
   from day 1; the binding from logical name → physical backend is a
   runtime concern. Splitting a Space later doesn't change synlang code.
2. **DAS is the substrate the canonical synart wants.** Slowly-changing
   graph of truth, partitioned across machines, parallel match,
   hub-replication for high-degree atoms.
3. **Cross-Space ≠ trust boundary.** Within one Synome runtime, all
   Spaces share trust. Cross-Space writes are direct `add-atom`. The gate
   sits only at runtime ingress.
4. **Spaces don't solve consistency, conflicts, or attention.** Those are
   architectural decisions above the Space API. Synserv (sole sequencer)
   handles consistency; gate + nonces handle conflicts; per-Space
   subscription handles attention.

---

## 2. Taxonomy mapping

| Hyperon concept | Synome concept | Notes |
|---|---|---|
| Canonical rules / invariants | **Deontic skeleton** | replicated, gate-mediated |
| Domain knowledge base | **Canonical probmesh** | replicated, gate-mediated |
| Teleonome long-term memory | **Telart** + local probmesh | per-teleonome, not replicated |
| Embodiment working memory | **Embart** / operational workspace | per-embodiment |
| DAS / deep memory | Synart's storage substrate | underneath all canonical state |

Synome / telart / embart is exactly "many small fast Spaces + shared
canonical Spaces + distributed deep Spaces + explicit bridges."

---

## 3. The four sharding axes

Sharding isn't one decision. There are at least four roughly-orthogonal axes:

| Axis | Examples |
|---|---|
| **A. Authority** | `&genesis` / `&governance` / `&operational` / `&library` |
| **B. Tenant** | per-Prime, per-Halo, per-Class |
| **C. Temperature** | hot (active epoch's er-samples) / warm (last settled) / cold (history) |
| **D. Cadence** | near-immutable axioms / slow-write governance / fast-write events / probabilistic mesh |

A single physical Space sits at one point on each axis. A Space might be
`(operational × spark-prime × hot × fast-write)`; another is
`(governance × global × cold × slow-write)`. Backend choice follows from
the cell.

---

## 4. The entart concept

A **synomic entity** (synent) is one of the agent types that constitutes
the synome: Guardian, GovOps, Prime, Halo, and so on. Every synent owns
an **entart** — its slice of the synart, structured as a subtree of
Spaces rooted at one **root Space**.

The synart is the union of all entarts. Every non-universal Space
belongs to exactly one entart's subtree. Universal Spaces (`&skeleton`,
`&genesis`, `&global-settlement`) are owned by the **synome root entart**
at the top of the tree and are replicated everywhere.

### The synart as a tree of entarts

```
synome (root entart)
  &skeleton              universal axioms — replicated everywhere
  &genesis               Core Council, root authority
  &global-settlement     Sky-wide rollups
  │
  └── guardian-spark entart
        &spark-guardian        vote results, GovOps roots
        │
        └── soter-govops entart
              &soter-govops    company-level: which beacons, which Primes
              │
              └── spark-prime entart
                    &spark-prime          auth, policies, halo registry
                    │
                    ├── spark-term-halo entart
                    │     &spark-term-halo        halo policies, book registry
                    │     &spark-term-usds-book   leaf
                    │     &spark-term-cnys-book   leaf
                    │
                    └── spark-trade-halo entart
                          &spark-trade-halo
                          &spark-trade-amm-book
```

Each entart is a **subtree rooted at one root Space**. The root names
what's underneath. Recursive composition: an entart contains sub-entarts
(each itself an entart) plus leaf Spaces directly attached to it.

### What lives in a root Space

The root Space is the synent's identity *and* the entry point into its
subtree:

```metta
;; identity
(synent spark-prime)
(synent-type spark-prime prime)
(synent-name spark-prime "Spark Prime")
(parent-entart spark-prime soter-govops)

;; sub-entart registry (nested entities, each has its own root)
(sub-entart spark-prime spark-term-halo  &spark-term-halo)
(sub-entart spark-prime spark-trade-halo &spark-trade-halo)

;; leaf Space registry (directly attached, no further nesting)
(sub-space spark-prime &spark-prime-config)

;; auth grants for this entity's scope
(auth lpha-nfat-spark issue-unit …)

;; policies
(er-covenant  spark-prime 90)
(penalty-rate spark-prime 10)

;; cross-sub-entart rules (governance-shaped, scatter-gather)
(global-rule prime-exposure
   (targets via-registry sub-entart spark-prime)
   (local-rule book-exposure-here)
   (combine sum))
```

### The four artifact types

| Artifact | Scope | Replication | Owner |
|---|---|---|---|
| **Synart** | Whole canonical synome | gate-mediated, broadly replicated | The synome |
| **Entart** | One synent's subtree of synart | inherits synart replication | One synent |
| **Telart** | One teleonome's private state | not replicated | One teleonome |
| **Embart** | One embodiment's local workspace | ephemeral | One embodiment |

Entart is the **structural** artifact — a slice of synart with a name
and a root. Telart and embart are **separate** artifacts with different
replication scope. The synome is the union of all entarts; a teleonome
is one entart of the canonical synart plus its telart plus its
embodiments.

### Layered tightening for policy composition

When policies cascade down the tree, the discipline is **monotonic
tightening**: each level can add stricter rules but never weaken parent
rules. Skeleton sets invariants no one weakens; a Halo with stricter ER
than its Prime is fine; a Halo with looser ER than its Prime is rejected
at registration. Predictable, auditable, mirrors how legal hierarchies
work (federal → state → city, never reversed).

### What entarts give you

1. **Sync becomes tree-walk.** "Give me Spark's entart" = sync
   `&spark-prime`, walk its `(sub-entart …)` and `(sub-space …)`
   registries, recurse. Selective sync = "stop the recursion at this
   depth" or "skip these branches."
2. **Authority cascades down the tree.** Each root authorizes its
   sub-entarts. Guardian roots Prime; Prime roots Halo; Halo registers
   books. The accordancy chain becomes "the path between two roots."
3. **Lifecycle is atomic and structural.** Create an entart = atomically
   add its root + register it in parent's `(sub-entart …)`. Destroy =
   walk subtree, retract, unregister. Whole entities live and die as
   units.
4. **Identity has a concrete home.** `(synent-of &space)` walks up the
   tree to the owning entart's root. `(parent-entart spark-prime)` walks
   to the next root up.
5. **Reference asymmetry generalizes.** Parent → child references go
   through the registry; peers communicate through their common ancestor
   (see §7).

---

## 5. Example: Spark Prime's entart

For Spark Prime specifically, the entart is:

```
spark-prime entart
  &spark-prime           auth, policies, covenants, halo registry, cross-halo rules
  │
  ├── spark-term-halo entart
  │     &spark-term-halo        halo policies, book registry
  │     &spark-term-usds-book   USDS units, books, states, samples + local rules
  │     &spark-term-cnys-book   CNYS units, books, states, samples + local rules
  │
  └── spark-trade-halo entart
        &spark-trade-halo
        &spark-trade-amm-book
```

`&spark-prime` is the root: it holds Spark's identity, its auth grants,
its covenants and penalty schedules, the registry of its sub-entarts
(the Halos), and the cross-Halo aggregation rules. Each Halo is itself
an entart, with its own root holding halo-level policies and the
registry of its book Spaces. Book Spaces are leaves: operational atoms
plus the local rules that operate on them.

This Space family is exactly *Spark Prime's entart*.

---

## 6. The registry pattern

Inside an entart root, registry atoms name what's underneath:

```metta
;; in &spark-prime
(sub-entart spark-prime spark-term-halo  &spark-term-halo)
(sub-entart spark-prime spark-trade-halo &spark-trade-halo)

;; in &spark-term-halo
(sub-space spark-term-halo &spark-term-usds-book)
(sub-space spark-term-halo &spark-term-cnys-book)
```

Two registry kinds:

- `(sub-entart $self $child-id $child-root)` — the child is itself an
  entart with its own root. Sync recurses into it.
- `(sub-space $self $space)` — leaf Space directly attached to this
  root, no further nesting.

Cross-Space rules iterate the registry — they never hard-code Space
references. Adding `&spark-eurs-book` later requires no rule changes.
The registry is the **honest barrier**: a partial-sync teleonome can
diff its sync set against the registry to know exactly what it's
missing.

---

## 7. The asymmetry rule

Generalized from "governance reaches into books, books don't reach
across" to a rule about the entart tree:

| Direction | OK? | Why |
|---|---|---|
| Parent → child (read) | yes | parent owns policy/coordination; needs child state |
| Parent → child (write) | yes | constructors live at parent; direct `add-atom` into child |
| Child → parent | **avoid** | couples child to parent's other children transitively |
| Peer → peer (siblings) | **avoid** | go through common ancestor |
| Universal Spaces (`&skeleton`) | always readable | replicated everywhere |

If a rule needs cross-sibling context (e.g., rule about both
`spark-term-halo` and `spark-trade-halo`), it lives at their common
ancestor (`&spark-prime`). Sub-entarts stay flat and replicable in
isolation; only the common ancestor knows about both children.

---

## 8. Partial sync and rule/data co-location

**Rules are atoms in some Space.** If you don't sync `&spark-prime`, you
don't get the cross-Halo rules — they're not in your runtime at all.
The symbol is unbound; you can't accidentally call it.

So the common case is clean: partial sync gives partial *capabilities*,
and unavailable capabilities just aren't there to call.

A USDS-only embodiment with `&skeleton + &spark-term-usds-book`:

- ✓ `(book-state book-B7)` — single-Space
- ✓ `(book-exposure-here)` — local rule, lives in the book Space
- ✗ `(prime-exposure spark-prime)` — rule lives in `&spark-prime`, which it didn't sync

---

## 9. The dangerous case

You have a rule but not all the Spaces it reaches into. Concretely:
sync `&spark-prime` (for policy) but skip `&spark-trade-halo` (only
care about term). Now `prime-exposure` walks the registry and tries to
match against an unbound Space.

| Semantic | Behavior | Use when |
|---|---|---|
| **Hard fail** | throws; rule refuses to answer | safety-critical (covenant checks) |
| **Lazy fetch** | runtime pulls missing Space from canonical synart | DAS pattern; one-shots |
| **Empty match** | treats unbound as no atoms; silently underestimates | **never** — silent wrong answers |

Empty-match is the trap. Default must be hard-fail; lazy-fetch is opt-in.

---

## 10. Declarative reads and capability introspection

Every rule declares its reads. Don't manually wrap safe vs unsafe — make
it static:

```metta
(rule-reads prime-exposure &spark-prime)
(rule-reads prime-exposure &skeleton)
(rule-reads prime-exposure via-registry sub-entart)

(= (can-evaluate $rule)
   (forall $s (rule-reads $rule $s) (have-synced $s)))
```

The teleonome introspects before invoking. The runtime can also enforce:
refuse to evaluate a rule whose reads aren't satisfied.

For graceful degradation, offer `*-local` partial-view variants that
explicitly skip unsynced Spaces and mark results as partial. But the
*real* answer is the next section.

---

## 11. Each Space is locally consistent

Design each Space so it's **internally complete** for some purpose:

- `&spark-term-usds-book` — locally consistent for USDS-book reasoning
- `&spark-prime` — locally consistent for Spark policy/authority
- The combination — gives aggregate views that don't exist in any
  single Space (Prime ER, multi-Halo covenants)

If you skip a Space, you lose views that needed it. You don't lose any
view that lived purely in the Spaces you kept.

---

## 12. Local-by-default; global as scatter-gather

The architectural principle:

> **Every Space tries to compute everything locally as much as possible.
> Cross-Space rules are scatter-gather: ship the rule to each target
> Space, run it locally against `&self`, return small results, aggregate.**

Same insight that drives MapReduce / Spark / DAS-style query routing.
Push computation to data; don't pull data to a coordinator. For our
setup it's especially clean because rules are atoms — "ship the rule" is
literally `(add-atom &target rule)`.

---

## 13. The two-step rule shape

The local rule is **portable** — it uses `&self` so it runs in whatever
Space hosts it:

```metta
;; lives in &spark-prime — the local rule body
(= (book-exposure-here)
   (sum (collapse
     (match &self (unit $u) (unit-risk-weight $u)))))

;; the global rule — declarative: target set + local rule + combinator
(global-rule prime-exposure
   (targets    via-registry sub-entart)
   (local-rule book-exposure-here)
   (combine    sum))

;; runner — generic across all global rules
(= (eval-global $rule $entity)
   (let* (($targets (resolve-targets $rule $entity))
          ($locals  (collapse (map (run-in $rule) $targets))))
     (combine-with $rule $locals)))
```

`book-exposure-here` is *spaceless* until projected. It runs against
whatever `&self` it lands in.

For nested entart trees, `resolve-targets` may recurse — running
`prime-exposure` on a Prime walks its halo registry, then each halo's
book registry, projecting the local rule to every leaf book Space.

---

## 14. What scatter-gather buys

1. **Locality of execution.** Rule runs near its data. Bandwidth = small
   rule + small result, not all atoms shipped to a coordinator.
2. **Partial sync becomes free.** A USDS-only teleonome runs the same
   `book-exposure-here` against its own slice. No `*-local` shadow rule.
3. **Partial-sync participation.** A light embodiment can *contribute* to
   Prime-wide computations: synserv ships the rule, embodiment runs it
   on its slice, returns. No sync upgrade required to participate.
4. **Each Space is an autonomous actor.** "Run this rule, return
   answer" — Erlang-shaped, Goertzel-cube-shaped.
5. **Aggregators are the only cross-Space surface.** Sum, max, min,
   count, top-K, distinct cover almost every cross-Space rule.
6. **Trust is contained.** Synserv ships rules; beacons can't push code.
   Mobile-code security collapses to "what code did entart roots author."

---

## 15. Aggregator design

| Class | Examples | Combiner |
|---|---|---|
| Trivial | sum, max, min, count, any, all | direct |
| Concat | top-K, distinct, list | merge + cap |
| Sketch | percentile, distinct-count, quantile | t-digest, HLL |

Most synart aggregations (total exposure, max ER, count of breaches,
sum of penalties) are in the trivial class. Non-additive aggregations
need sketches; flag them when designing the rule.

**Discipline:** local rules may only reach into `&self` and universally-
replicated Spaces (`&skeleton`). Anything that needs another partition
isn't local — it's a coordinator, and lives at the parent entart root.

---

## 16. Rule publication as broadcast

When a global rule's master version updates, the new version flows out
to every target Space. The pattern is **publish-subscribe via the
canonical replication channel**.

```metta
;; master in &spark-prime
(global-rule book-exposure-here
   (version 7)
   (targets via-registry sub-entart)
   (rule-deps unit-risk-weight crr-of)
   (space-reads &self &skeleton))

;; master rule body
(= (book-exposure-here) <body-v7>)
(rule-version book-exposure-here 7)
```

On update v7 → v8, synserv:

1. Writes new body + version atoms in `&spark-prime`, retracts old.
2. Walks the registry → list of target Spaces.
3. For each target: retracts old projection, adds new projection plus
   provenance: `(rule-source book-exposure-here &spark-prime)`.

Each target Space replicates to its subscribers normally. A teleonome
watching only `&spark-term-usds-book` sees the rule atom change — same
mechanism it uses for any other update. **No special "code update" path.
Rules ride with the data.**

---

## 17. Materialized views + CDC

Worth naming what this reinvents:

| Database concept | Synart analog |
|---|---|
| Source table | Master rule atom in entart root |
| Materialized view | Rule projection in target Space |
| CDC stream | Synserv's projection step on update |
| View refresh | Eager (immediate) for governance-paced rules |
| Foreign key / provenance | `(rule-source …)` atom on each projection |

Tells us which problems are already solved (consistency models,
retraction propagation, schema migration) and which need our own
answers (rule dependency closure, partial-sync subscription).

---

## 18. Subtleties to keep in view

**a) Transitive rule dependencies.** If `book-exposure-here` calls
`unit-risk-weight`, both ship together. Publication step closes over
rule deps and projects the package. The runner refuses to project unless
every dep is itself either projected or universally replicated.

**b) Version skew during scatter-gather.** If `eval-global` runs across
five books while a v7→v8 rollout is in flight, three may run v7 and two
v8. For sum-shaped aggregations rarely matters; for safety-critical
paths, synserv stamps the eval with a target version and any target
running an older copy refuses or upgrades first. In practice, rule
updates are governance-paced (days/weeks) and aggregations are
settlement-paced (minutes) — windows almost never overlap.

**c) Eager vs lazy fetch.** Eager publish is the default for entart-root
rules (small, slow-changing, broadcast on update). Lazy fetch is opt-in
for one-shot queries against unsynced Spaces. Empty-match is never the
default.

---

## 19. Subscription patterns

Subscriptions are entart-tree subscriptions:

| Teleonome | Subscribes to | Why |
|---|---|---|
| Spark risk monitor | `&skeleton` + full `spark-prime` entart | full ER picture |
| USDS-only liquidity bot | `&skeleton` + just `&spark-term-usds-book` | watches one leaf |
| Pure governance auditor | `&skeleton` + every entart root, no leaves | reads policies, ignores ops |
| Settlement aggregator | `&global-settlement` + every Prime root | Prime-wide rollups |

The entart tree maps directly onto real access-pattern boundaries. Any
of these subscribers gets rule updates affecting their Spaces
automatically — rules ride with data.

---

## 20. The full Phase 1 commitment list

Original seven from `synart-access-and-runtime.md`:

1. Space is always a parameter, never implicit.
2. Append-only writes.
3. Content-addressed names.
4. Open verb dispatch via whitelist atoms.
5. Gate as real primitive at trust boundary.
6. `(can …)` reads from a named auth Space.
7. Idempotent constructors.

Added by this document:

8. **Every rule declares its reads.** `(rule-reads $rule $space)`
   alongside the rule. Trivial in Phase 1; load-bearing once partial sync
   is real.
9. **Cross-Space references go through registries, never hard-coded
   names.** Same discipline as P4-P6, applied to "which Spaces does this
   rule reach."
10. **Cross-Space rules are scatter-gather, not direct multi-match.** A
    rule with cross-Space reads is structured as
    (local-rule, targets, combinator). Direct `(match $other …)` is
    reserved for genuinely tightly-coupled facts (e.g., reading
    `&skeleton`'s CRR table, which is universal).
11. **Global rules carry their own publication metadata.** A
    `global-rule` declaration enumerates
    `(version, targets, rule-deps, space-reads, combinator)`. Synserv
    projects on update; targets retract on master retraction. Provenance
    atom rides with every projection.
12. **Synart is a tree of entarts.** Each synomic entity owns an entart
    rooted at one root Space. Cross-entart references go parent → child
    only; peers communicate through their common ancestor. Policies
    cascade with monotonic tightening (children may add stricter rules,
    never weaken parent rules).

These aren't really about scale — they're hygiene that makes scaling free.

---

## 21. The one-line summary

**Synart is a tree of entarts; each entart owns its local rules and
computes locally by default. Cross-entart rules are scatter-gather: ship
the local rule to every target, run against `&self`, aggregate small
results. Rules ride with data through replication, so partial-sync
subscribers stay current without subscribing to ancestors.**
