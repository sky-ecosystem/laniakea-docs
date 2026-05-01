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

## 4. The Space family pattern

For one Prime, the natural split is a small *Space family*:

```
&spark-governance      auth, policies, covenants, registry, cross-book rules
&spark-usds-book       USDS units, books, states, er-samples
&spark-cnys-book       CNYS units, books, states, er-samples
&skeleton              constitutional axioms (CRR table, covenant shape)
```

Governance holds policy + a registry of which book Spaces participate.
Book Spaces hold operational state only — they don't know about each
other or about governance.

---

## 5. The registry pattern

Inside `&spark-governance`:

```metta
(prime-book-space spark-prime &spark-usds-book)
(prime-book-space spark-prime &spark-cnys-book)
```

Cross-book rules iterate the registry — they never hard-code book Spaces.
Adding `&spark-eurs-book` later requires no rule changes. The registry is
the **honest barrier**: a partial-sync teleonome can diff its sync set
against the registry to know exactly what it's missing.

---

## 6. The asymmetry rule

| Direction | OK? | Why |
|---|---|---|
| Governance → book (read) | yes | governance owns policy; needs operational state |
| Governance → book (write) | yes | constructors live in governance; direct `add-atom` |
| Book → governance | **avoid** | couples books transitively; breaks self-containment |
| Book → book (cross) | **avoid** | governance is the only mediator |

If a rule needs cross-book context, it lives in governance. Books stay
flat and replicable in isolation.

---

## 7. Partial sync and rule/data co-location

**Rules are atoms in some Space.** If you don't sync `&spark-governance`,
you don't get governance's rules — they're not in your runtime at all.
The symbol is unbound; you can't accidentally call it.

So the common case is clean: partial sync gives partial *capabilities*,
and unavailable capabilities just aren't there to call.

A USDS-only embodiment with `&skeleton + &spark-usds-book`:

- ✓ `(book-state book-B7)` — single-Space
- ✓ `(book-exposure-here)` — local rule, lives in the book Space
- ✗ `(prime-exposure spark-prime)` — rule lives in governance, which it didn't sync

---

## 8. The dangerous case

You have a rule but not all the Spaces it reaches into. Concretely:
sync `&spark-governance` (for policy) but skip `&spark-cnys-book` (only
care about USDS). Now `prime-exposure` walks the registry and tries to
match against an unbound Space.

| Semantic | Behavior | Use when |
|---|---|---|
| **Hard fail** | throws; rule refuses to answer | safety-critical (covenant checks) |
| **Lazy fetch** | runtime pulls missing Space from canonical synart | DAS pattern; one-shots |
| **Empty match** | treats unbound as no atoms; silently underestimates | **never** — silent wrong answers |

Empty-match is the trap. Default must be hard-fail; lazy-fetch is opt-in.

---

## 9. Declarative reads and capability introspection

Every rule declares its reads. Don't manually wrap safe vs unsafe — make
it static:

```metta
(rule-reads prime-exposure &spark-governance)
(rule-reads prime-exposure &skeleton)
(rule-reads prime-exposure via-registry prime-book-space)

(= (can-evaluate $rule)
   (forall $s (rule-reads $rule $s) (have-synced $s)))
```

The teleonome introspects before invoking. The runtime can also enforce:
refuse to evaluate a rule whose reads aren't satisfied.

For graceful degradation, offer `*-local` partial-view variants that
explicitly skip unsynced Spaces and mark results as partial. But the
*real* answer is the next section.

---

## 10. Each Space is locally consistent

Design each Space so it's **internally complete** for some purpose:

- `&spark-usds-book` — locally consistent for USDS-book reasoning
- `&spark-governance` — locally consistent for Spark policy/authority
- The combination — gives aggregate views that don't exist in any
  single Space (Prime ER, multi-book covenants)

If you skip a Space, you lose views that needed it. You don't lose any
view that lived purely in the Spaces you kept.

---

## 11. Local-by-default; global as scatter-gather

The architectural principle:

> **Every Space tries to compute everything locally as much as possible.
> Cross-Space rules are scatter-gather: ship the rule to each target
> Space, run it locally against `&self`, return small results, aggregate.**

Same insight that drives MapReduce / Spark / DAS-style query routing.
Push computation to data; don't pull data to a coordinator. For our
setup it's especially clean because rules are atoms — "ship the rule" is
literally `(add-atom &target rule)`.

---

## 12. The two-step rule shape

The local rule is **portable** — it uses `&self` so it runs in whatever
Space hosts it:

```metta
;; lives in &spark-governance — the local rule body
(= (book-exposure-here)
   (sum (collapse
     (match &self (unit $u) (unit-risk-weight $u)))))

;; the global rule — declarative: target set + local rule + combinator
(global-rule prime-exposure
   (targets    via-registry prime-book-space)
   (local-rule book-exposure-here)
   (combine    sum))

;; runner — generic across all global rules
(= (eval-global $rule $prime)
   (let* (($targets (resolve-targets $rule $prime))
          ($locals  (collapse (map (run-in $rule) $targets))))
     (combine-with $rule $locals)))
```

`book-exposure-here` is *spaceless* until projected. It runs against
whatever `&self` it lands in.

---

## 13. What scatter-gather buys

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
   Mobile-code security collapses to "what code did governance author."

---

## 14. Aggregator design

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
isn't local — it's a coordinator, and lives in governance.

---

## 15. Rule publication as broadcast

When a global rule's master version updates, the new version flows out
to every target Space. The pattern is **publish-subscribe via the
canonical replication channel**.

```metta
;; master in &spark-governance
(global-rule book-exposure-here
   (version 7)
   (targets via-registry prime-book-space)
   (rule-deps unit-risk-weight crr-of)
   (space-reads &self &skeleton))

;; master rule body
(= (book-exposure-here) <body-v7>)
(rule-version book-exposure-here 7)
```

On update v7 → v8, synserv:

1. Writes new body + version atoms in `&spark-governance`, retracts old.
2. Walks the registry → list of target Spaces.
3. For each target: retracts old projection, adds new projection plus
   provenance: `(rule-source book-exposure-here &spark-governance)`.

Each target Space replicates to its subscribers normally. A teleonome
watching only `&spark-usds-book` sees the rule atom change — same
mechanism it uses for any other update. **No special "code update" path.
Rules ride with the data.**

---

## 16. Materialized views + CDC

Worth naming what this reinvents:

| Database concept | Synart analog |
|---|---|
| Source table | Master rule atom in `&spark-governance` |
| Materialized view | Rule projection in target Space |
| CDC stream | Synserv's projection step on update |
| View refresh | Eager (immediate) for governance-paced rules |
| Foreign key / provenance | `(rule-source …)` atom on each projection |

Tells us which problems are already solved (consistency models,
retraction propagation, schema migration) and which need our own
answers (rule dependency closure, partial-sync subscription).

---

## 17. Subtleties to keep in view

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

**c) Eager vs lazy fetch.** Eager publish is the default for governance
rules (small, slow-changing, broadcast on update). Lazy fetch is opt-in
for one-shot queries against unsynced Spaces. Empty-match is never the
default.

---

## 18. Subscription patterns

| Teleonome | Subscribes to | Why |
|---|---|---|
| Spark risk monitor | `&skeleton` + `&spark-governance` + all book Spaces | full ER picture |
| USDS-only liquidity bot | `&skeleton` + `&spark-usds-book` | watches USDS state |
| Pure governance auditor | `&skeleton` + every `&*-governance` | reads policies, ignores ops |
| Settlement aggregator | `&global-settlement` + every `&*-governance` | Prime-wide rollups |

The Space split lines up with real access-pattern boundaries. Any of
these subscribers gets rule updates affecting their Spaces automatically.

---

## 19. The full Phase 1 commitment list

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

These aren't really about scale — they're hygiene that makes scaling free.

---

## 20. The one-line summary

**Each Space owns its local rules and computes locally by default.
Cross-Space rules are scatter-gather: ship the local rule to every
target, run against `&self`, aggregate small results. Rules ride with
data through replication, so partial-sync subscribers stay current
without subscribing to governance.**
