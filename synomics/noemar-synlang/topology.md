# Topology — Synart Spaces, Entarts, and Naming

Defines the structure of the canonical synart: how Spaces are organized,
what an entart is, what lives at synome root vs in entarts, the naming
convention, and the architectural rules that govern composition.

Companion to `scaling.md` (operational concerns and failure modes when
this becomes a networked system) and `synart-access-and-runtime.md`
(auth model + runtime).

The driving requirements:

- **Modular sync.** A teleonome can subscribe to any subset of the
  synart; serious teleonomes sync everything; light embodiments may sync
  one Prime's USDS book. Both are first-class.
- **Locality.** Rules execute close to the atoms they read.
- **Composable.** Adding new entities or universal Spaces shouldn't
  require schema rewrites.
- **Future-proof.** The structure outlives any specific Phase 1
  implementation.

---

## TL;DR — the architecture in one page

**The six load-bearing decisions:**

1. **Spaces are grounded atoms with a uniform API.** Name them in synlang
   from day 1; the binding from logical name → physical backend is a
   runtime concern.
2. **Synart is a tree of entarts.** Each synomic entity (Guardian, Prime,
   Halo) owns an **entart** — a subtree of Spaces rooted at its own root
   Space. The synart is the union of all entarts.
3. **Synome root has four layers.** Constitutional (telos / skeleton /
   governance), framework (universal shapes that propagate), registry
   (identity indexes), aggregation (Phase-2 outputs).
4. **Operators and beacons are external.** Only synomic agents own
   entarts. Beacons are connective tissue between external operators
   and the entart tree.
5. **Local-by-default, scatter-gather for global.** Cross-Space rules
   ship a portable `&self`-body to each target, run locally, aggregate
   small results.
6. **Rules ride with data.** Rules are atoms; they replicate to
   subscribers through the same channel as state. Partial-sync
   teleonomes stay current automatically.

**The synome root layers:**

| Layer | Spaces |
|---|---|
| Constitutional | `&core-root`, `&core-telos`, `&core-skeleton`, `&core-governance` |
| Framework | `&core-framework-risk`, `&core-framework-distribution`, `&core-framework-fee` |
| Registry | `&core-registry-entity`, `&core-registry-beacon`, `&core-registry-contract` |
| Aggregation | `&core-settlement`, `&core-escalation` |
| Deferred | `&core-library` (probmesh canonical) |

**The naming convention:**

```
core-<kind>[-<topic>...]                                  // synome-level
entity-<entity-type>-<entity-id>-<sub-kind>[-<sub-id>]    // entart-level
```

**An entart tree (Spark):**

```
&core-root
  └── &entity-guardian-spark-root
        └── &entity-prime-spark-root
              ├── &entity-halo-spark-term-root
              │     ├── &entity-halo-spark-term-book-usds
              │     └── &entity-halo-spark-term-book-cnys
              └── &entity-halo-spark-trade-root
                    └── &entity-halo-spark-trade-book-amm
```

**Twelve Phase 1 commitments** (§16) — hygiene that makes scaling free.

---

## Section map

| § | Topic | Core idea |
|---|---|---|
| 1 | Hyperon Spaces basics | Spaces as grounded atoms; DAS substrate; gate ≠ Space boundary |
| 2 | Taxonomy mapping | Synome / telart / embart aligns with Hyperon's split |
| 3 | Four sharding axes | Authority / tenant / temperature / cadence — orthogonal |
| 4 | The entart concept | Synart is a tree of entity-rooted subtrees |
| 5 | Synome root layers | Constitutional / framework / registry / aggregation |
| 6 | Three meta-patterns | Frameworks propagate; registries are flat; aggregations collect |
| 7 | Naming convention | `core-<kind>` and `entity-<type>-<id>-<sub-kind>` |
| 8 | Operators and beacons | External; not entart owners; connective tissue |
| 9 | Example: Spark's entart | Full tree with new naming |
| 10 | Registry pattern | `(sub-entart …)` and `(sub-space …)` |
| 11 | Asymmetry rule | Parent → child only; peers via common ancestor |
| 12 | Local consistency | Each Space self-complete for some purpose |
| 13 | Local-by-default principle | Scatter-gather for cross-Space; push code to data |
| 14 | Two-step rule shape | Portable `&self` body + global declaration |
| 15 | Aggregator design | Trivial / concat / sketch classes |
| 16 | Phase 1 commitments | Twelve total |
| 17 | One-line summary | Whole architecture compressed |

---

## 1. What's load-bearing about Hyperon Spaces

Four facts from the Hyperon model do most of the work:

1. **Spaces are grounded atoms with a uniform API.** A Space is a value;
   `(match $space …)` is a regular call. Synlang names Spaces from day 1;
   the binding from logical name → physical backend is a runtime concern.
   Splitting later doesn't change synlang code.
2. **DAS is the substrate the canonical synart wants.** Slowly-changing
   graph of truth, partitioned across machines, parallel match,
   hub-replication for high-degree atoms.
3. **Cross-Space ≠ trust boundary.** Within one Synome runtime, all
   Spaces share trust. Cross-Space writes are direct `add-atom`. The gate
   sits only at runtime ingress.
4. **Spaces don't solve consistency, conflicts, or attention.** Those
   live above the Space API. Synserv (sole sequencer) handles
   consistency; gate + nonces handle conflicts; per-Space subscription
   handles attention.

---

## 2. Taxonomy mapping

| Hyperon concept | Synome concept | Notes |
|---|---|---|
| Canonical rules / invariants | **Deontic skeleton** | replicated, gate-mediated |
| Domain knowledge base | **Canonical probmesh** | replicated, gate-mediated |
| Teleonome long-term memory | **Telart** + local probmesh | per-teleonome, not replicated |
| Embodiment working memory | **Embart** / operational workspace | per-embodiment |
| DAS / deep memory | Synart's storage substrate | underneath all canonical state |

Synome / telart / embart is "many small fast Spaces + shared canonical
Spaces + distributed deep Spaces + explicit bridges."

---

## 3. The four sharding axes

Sharding isn't one decision. There are at least four roughly-orthogonal axes:

| Axis | Examples |
|---|---|
| **A. Authority** | constitutional / governance / operational / library |
| **B. Tenant** | per-Prime, per-Halo, per-Class |
| **C. Temperature** | hot (active samples) / warm (last settled) / cold (history) |
| **D. Cadence** | near-immutable axioms / slow-write governance / fast-write events / probabilistic mesh |

A single Space sits at one point on each axis. Backend choice follows
from the cell.

---

## 4. The entart concept

A **synomic entity** (synent) is one of the agent types that constitutes
the synome: Guardian, Prime, Halo. Every synent owns an **entart** — its
slice of the synart, structured as a subtree of Spaces rooted at one
**root Space**.

The synart is the union of all entarts. Every non-universal Space
belongs to exactly one entart's subtree. Universal Spaces (`&core-*`)
are owned by the **synome root entart** and are replicated everywhere.

### What lives in a root Space

The root Space is the synent's identity *and* the entry point into its
subtree:

```metta
;; identity
(synent spark-prime)
(synent-type spark-prime prime)
(synent-name spark-prime "Spark Prime")
(parent-entart spark-prime spark-guardian)

;; sub-entart registry (nested entities, each has its own root)
(sub-entart spark-prime spark-term-halo  &entity-halo-spark-term-root)
(sub-entart spark-prime spark-trade-halo &entity-halo-spark-trade-root)

;; leaf Space registry (directly attached, no further nesting)
(sub-space spark-prime &entity-prime-spark-config)

;; auth grants for this entity's scope
(auth lpha-nfat-spark issue-unit …)

;; policies — local values within bounds set by &core-framework-risk
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
replication scope.

### Layered tightening for policy composition

Policies cascade down the tree with **monotonic tightening**: each level
can add stricter rules but never weaken parent rules. `&core-skeleton`
sets invariants no one weakens; `&core-framework-risk` sets bounds that
each Prime can tighten within. A Halo with stricter ER than its Prime
is fine; a Halo with looser ER than its Prime is rejected at registration.

Mirrors how legal hierarchies work (federal → state → city, never reversed).

### What entarts give you

1. **Sync becomes tree-walk.** "Give me Spark's entart" = sync the root,
   walk its registries, recurse. Selective sync = "stop the recursion
   at this depth" or "skip these branches."
2. **Authority cascades.** Each root authorizes its sub-entarts. The
   accordancy chain is "the path between two roots."
3. **Lifecycle is atomic and structural.** Create = atomically add root +
   register in parent. Destroy = walk subtree, retract, unregister.
4. **Identity has a concrete home.** `(synent-of &space)` walks up the
   tree. `(parent-entart spark-prime)` walks to the next root.
5. **Reference asymmetry generalizes** (§11): parent → child only; peers
   via common ancestor.

---

## 5. Synome root layers

The synome root entart holds universal Spaces, organized into four
layers with consistent mechanics within each layer.

### Constitutional layer

The bedrock. Different rooms with different rules; all
universally-replicated, all rarely-written.

| Space | Contents | Change cadence |
|---|---|---|
| `&core-root` | Synome root entart's root Space; sub-entart and sub-space registries | governance-paced |
| `&core-telos` | Apex axiom — what the system is for | constitutional (~never) |
| `&core-skeleton` | Constitutional axioms, types, invariants | constitutional rewrite |
| `&core-governance` | Core Council legislative chamber, including the bootstrap seed (`role-def root-authority`, `role-grant core-council`) as initial state | governance-paced |

### Framework layer

Universal shapes + parameter bounds. Each entart gets its own values
constrained by the framework via layered tightening. Updates project
out via scatter-gather.

| Space | Contents |
|---|---|
| `&core-framework-risk` | CRR table, ER formula, covenant arithmetic |
| `&core-framework-distribution` | Distribution rewards rate, integration boost shapes |
| `&core-framework-fee` | Agent upkeep, protocol fees, fee shapes |

### Registry layer

Flat identity indexes for things whose actual state lives elsewhere
(external processes, on chain, or in entart subtrees). Push/pull
onboarding (proposed → accepted). Authority comes from cert/auth atoms
elsewhere, not from registration.

| Space | Contents |
|---|---|
| `&core-registry-entity` | All entarts (denormalized index for discovery; tree is canonical) |
| `&core-registry-beacon` | All beacons (operators are external; pubkey + status here) |
| `&core-registry-contract` | All on-chain contracts (state lives on chain; thin reference layer) |

### Aggregation layer

Where Phase-2 scatter-gather outputs land. Each entart computes locally;
synserv aggregates into these Spaces.

| Space | Contents |
|---|---|
| `&core-settlement` | Sky-wide financial aggregation (penalties owed, distributions, fees, settlement totals) |
| `&core-escalation` | Disputes, slashing reports, contested operations |

### Deferred

| Space | Contents |
|---|---|
| `&core-library` | Canonical probmesh claims (publication-gate output) — own design pass |

---

## 6. Three meta-patterns

The four-layer factoring is descriptive; the three meta-patterns
underneath it are *prescriptive*. When someone proposes a new universal
Space, ask "is this a framework, registry, or aggregation?" — the
answer determines its mechanics. If it's none of those, push back.

### Frameworks (universal shape + bounds)

```
shape (CRR formula, ER arithmetic, covenant bounds)  →  &core-framework-*
                                                          │
                                                          │ scatter-gather projection
                                                          ▼
per-entart values (Spark's covenant=90, Grove's=85)  →  each &entity-*-root
```

- Universal at synome root, replicated everywhere
- Define rule shape + parameter bounds, not per-entity values
- Per-entity values live in each entart, constrained by framework
- Updates project out via scatter-gather (publication mechanism)
- Governance-paced changes

### Registries (flat identity index)

```
external state (beacon process, on-chain contract, or entart subtree)
                            │
                            │ push proposal → pull accept
                            ▼
identity row in &core-registry-*
```

- Push (proposal from external) → pull (governance accept)
- Pure identity, no authority granted by registration
- Denormalized index for fast queries (vs walking the tree / chain / network)
- Authority for the registered thing lives elsewhere (cert/auth atoms in entarts)

### Aggregations (scatter-gather collection)

```
each entart computes locally  →  Phase 1
       │
       │ synserv aggregates
       ▼
&core-settlement / &core-escalation
```

- Scatter-gather collection at synserv
- Settlement-paced or event-paced writes
- Read by everyone, written only by synserv aggregator
- "Single source of truth" for Sky-wide totals

---

## 7. The naming convention

Two patterns, one for each scope:

```
core-<kind>[-<topic>...]                                  // synome-level
entity-<entity-type>-<entity-id>-<sub-kind>[-<sub-id>]    // entart-level
```

Reserved keyword vocabulary:

| Slot | Values |
|---|---|
| `core <kind>` | `root`, `telos`, `skeleton`, `governance`, `framework`, `registry`, `settlement`, `escalation`, `library` |
| `entity <type>` | `guardian`, `prime`, `halo` (extensible: `foreign` for cross-chain, etc.) |
| `entity <sub-kind>` | `root`, `book`, `class`, `config`, `history` (extensible per real Space patterns) |

Adding a keyword is governance-paced; using one is free. Each keyword
carries semantics about replication, access, and update mechanics —
adding one is meaningful.

### Examples

Synome-level:

```
&core-root
&core-telos
&core-skeleton
&core-governance
&core-framework-risk
&core-framework-distribution
&core-framework-fee
&core-registry-entity
&core-registry-beacon
&core-registry-contract
&core-settlement
&core-escalation
```

Entart-level:

```
&entity-guardian-spark-root        Guardian Spark's entart root
&entity-prime-spark-root           Spark Prime's entart root
&entity-prime-spark-config         config sub-Space attached to Spark Prime root
&entity-halo-spark-term-root       Spark Term Halo's entart root
&entity-halo-spark-term-book-usds  USDS book leaf in Spark Term Halo
&entity-halo-spark-term-book-cnys  CNYS book leaf
&entity-halo-spark-trade-root      Spark Trade Halo's entart root
&entity-halo-spark-trade-book-amm  AMM book leaf
```

### Naming is decoupled from tree topology

The Space name encodes the entity ID + the sub-kind. It does **not**
encode the parent chain. A Space named `&entity-halo-spark-term-book-usds`
is registered under `&entity-halo-spark-term-root` via
`(sub-space spark-term-halo &entity-halo-spark-term-book-usds)`. The
name tells you which entity owns it; the registry tells you the
structural relationship.

This means a Space can later move to a different parent (during a
reorganization) without changing its name.

---

## 8. Operators and beacons are external

A **beacon** is an external process — running on a server somewhere with
a private key. It interacts with the synart only via gate-mediated
submissions. There's no internal "beacon state" inside synart, only
*facts about the beacon*.

**Beacons aren't entarts.** Facts about beacons live where they're used:

| Fact about beacon | Lives in | Why |
|---|---|---|
| Pubkey + status + class | `&core-registry-beacon` | needed at the gate for sig verification, globally |
| `(cert beacon-X by-spark-guardian)` | `&entity-guardian-spark-root` | guardian holds underwriting liability |
| `(auth beacon-X verb target)` | entart owning the target | target's owner controls auth |
| Submission history | wherever it wrote | provenance follows writes |

There's no place where you'd say "this is the beacon's stuff"
cohesively. Entarts are for synomic *agents* (Guardian, Prime, Halo) —
the structural units of the synome. Beacons are *connective tissue*
between external operators and that structure.

### Operators are external too

Operators of all kinds — companies (soter-govops, devcos), teleonomes,
Core Council members, individual humans — are external. They run
beacons; the beacons are registered, certed, and authed through the
entart tree, but operators themselves aren't *in* the tree. Their
internal state is in telart (per-teleonome) or off-synart entirely.

This is a clean separation:

- **Entart owners** = synomic agents (structural units)
- **Operators** = external entities running beacons (humans, companies, teleonomes)
- **Beacons** = the connective tissue between them

### Push/pull beacon registration

```
1. Push: beacon proposes itself
   (beacon-pending beacon-X (pubkey "ab9c…") (operator soter-govops) (class lpha))

2. Pull: governance accepts
   (beacon-accepted beacon-X)
   (beacon-status beacon-X active)

3. Cert: rooted in a Guardian's entart
   ;; in &entity-guardian-spark-root
   (cert beacon-X by-spark-guardian)

4. Auth: granted in entarts whose parent chain includes that Guardian
   ;; in &entity-prime-spark-root or further down
   (auth beacon-X issue-unit book-B7)
```

"Accordant to the Guardian" cleanly cashes out as "the entart's parent
chain reaches that Guardian." Beacons certed by `spark-guardian` can be
authed in `spark-prime`, `spark-term-halo`, etc. — the whole subtree
under that Guardian.

---

## 9. Example — Spark's entart family

```
&core-root
  │
  └── &entity-guardian-spark-root              vote outcomes; cert-atoms for soter-govops's beacons
        │
        └── &entity-prime-spark-root           Prime auth, policies, halo registry, cross-halo rules
              │
              ├── &entity-halo-spark-term-root           halo policies, book registry
              │     ├── &entity-halo-spark-term-book-usds   USDS units, books, states, samples
              │     └── &entity-halo-spark-term-book-cnys   CNYS units, books, states, samples
              │
              └── &entity-halo-spark-trade-root
                    └── &entity-halo-spark-trade-book-amm
```

Each root holds identity + registries + scope-local policies +
cross-sub-entart rules. Leaf Spaces (books) hold operational state +
local rules that operate on it.

---

## 10. The registry pattern

Inside an entart root, registry atoms name what's underneath:

```metta
;; in &entity-prime-spark-root
(sub-entart spark-prime spark-term-halo  &entity-halo-spark-term-root)
(sub-entart spark-prime spark-trade-halo &entity-halo-spark-trade-root)

;; in &entity-halo-spark-term-root
(sub-space spark-term-halo &entity-halo-spark-term-book-usds)
(sub-space spark-term-halo &entity-halo-spark-term-book-cnys)
```

Two registry kinds:

- `(sub-entart $self $child-id $child-root)` — the child is itself an
  entart with its own root; sync recurses into it.
- `(sub-space $self $space)` — leaf Space directly attached to this
  root; no further nesting.

Cross-Space rules iterate the registry — they never hard-code Space
references. Adding a new sub-entart or leaf Space requires no rule
changes. The registry is the **honest barrier**: a partial-sync
teleonome can diff its sync set against the registry to know exactly
what it's missing.

---

## 11. The asymmetry rule

Generalized to the entart tree:

| Direction | OK? | Why |
|---|---|---|
| Parent → child (read) | yes | parent owns policy/coordination; needs child state |
| Parent → child (write) | yes | constructors live at parent; direct `add-atom` into child |
| Child → parent | **avoid** | couples child to parent's other children transitively |
| Peer → peer (siblings) | **avoid** | go through common ancestor |
| Universal Spaces (`&core-*`) | always readable | replicated everywhere |

If a rule needs cross-sibling context (a rule about both Spark Term and
Spark Trade Halos), it lives at their common ancestor
(`&entity-prime-spark-root`). Sub-entarts stay flat and replicable in
isolation; only the common ancestor knows about both.

---

## 12. Each Space is locally consistent

Design each Space so it's **internally complete** for some purpose:

- `&entity-halo-spark-term-book-usds` — locally consistent for USDS-book reasoning
- `&entity-prime-spark-root` — locally consistent for Spark policy/authority
- The combination — gives aggregate views that don't exist in any
  single Space (Prime ER, multi-Halo covenants)

If you skip a Space, you lose views that needed it. You don't lose any
view that lived purely in the Spaces you kept.

---

## 13. Local-by-default; global as scatter-gather

The architectural principle:

> **Every Space tries to compute everything locally as much as possible.
> Cross-Space rules are scatter-gather: ship the rule to each target
> Space, run it locally against `&self`, return small results, aggregate.**

Same insight that drives MapReduce / Spark / DAS-style query routing.
Push computation to data; don't pull data to a coordinator. For our
setup it's especially clean because rules are atoms — "ship the rule"
is literally `(add-atom &target rule)`.

---

## 14. The two-step rule shape

The local rule is **portable** — it uses `&self` so it runs in whatever
Space hosts it:

```metta
;; lives in &entity-prime-spark-root — the local rule body
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
replicated Spaces (`&core-*`). Anything that needs another partition
isn't local — it's a coordinator, and lives at the parent entart root.

---

## 16. The full Phase 1 commitment list

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
   alongside the rule. Trivial in Phase 1; load-bearing once partial
   sync is real.
9. **Cross-Space references go through registries, never hard-coded
   names.**
10. **Cross-Space rules are scatter-gather, not direct multi-match.**
11. **Global rules carry their own publication metadata** —
    `(version, targets, rule-deps, space-reads, combinator)` — and
    project on update with provenance atoms.
12. **Synart is a tree of entarts.** Each synomic entity owns an entart
    rooted at one root Space. Cross-entart references go parent → child
    only; peers via common ancestor. Policies cascade with monotonic
    tightening. Naming follows the `core-…` / `entity-<type>-<id>-…`
    convention. Operators and beacons are external; only synomic agents
    own entarts.

---

## 17. The one-line summary

**Synart is a tree of entarts; each entart owns its local rules and
computes locally by default. The synome root has four layers
(constitutional, framework, registry, aggregation) with three meta-
patterns (frameworks propagate via scatter-gather, registries hold
identity for things with state elsewhere, aggregations collect
scatter-gather outputs). Operators and beacons are external; only
synomic agents own entarts.**
