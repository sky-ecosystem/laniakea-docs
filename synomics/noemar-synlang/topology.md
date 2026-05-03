# Topology — Spaces, Entarts, Artifacts, and the Self-Hosting Synart

Defines the structure of the canonical synome: how Spaces are organized
across artifact tiers, what lives at synome root vs in entarts, the
universal Spaces that hold loops and gates and recipes, the naming
convention, and the architectural rules that govern composition.

Companion to:
- `syn-overview.md` (concept map and the five levels of self-reference)
- `syn-tel-emb.md` (artifact tiers in depth + the recipe marketplace)
- `boot-model.md` (identity-driven boot — how Spaces become running roles)
- `synart-access-and-runtime.md` (auth model + runtime architecture)
- `scaling.md` (operational concerns and failure modes when this becomes a networked system)

The driving requirements:

- **Modular sync.** A teleonome can subscribe to any subset of the
  synart; serious teleonomes sync everything; light embodiments may sync
  one Prime's USDS book. Both are first-class.
- **Locality.** Rules and loops execute close to the atoms they read.
- **Composable.** Adding new entities or universal Spaces shouldn't
  require schema rewrites.
- **Future-proof.** The structure outlives any specific Phase 1
  implementation.
- **Self-hosting.** The synart contains its own loops, gates, recipes,
  runtime source, and bootstrap procedure. Programs and data share one
  substrate.

---

## TL;DR — the architecture in one page

**The seven load-bearing decisions:**

1. **Spaces are grounded atoms with a uniform API.** Name them in synlang
   from day 1; the binding from logical name → physical backend is a
   runtime concern.
2. **Spaces hold data, rules, AND programs.** Loops, gates, and recipes
   are first-class atoms in synart, replicated alongside state. The
   synart is the program that the runtime interprets.
3. **Synart is a tree of entarts plus universal Spaces.** Each synomic
   entity (Guardian, Prime, Halo) owns an **entart** — a subtree rooted
   at its own root Space. The synome root holds universal Spaces in six
   structured layers.
4. **Synome root has six layers.** Constitutional, framework, registry,
   aggregation, executable, library — each with consistent mechanics
   within and characteristic update cadences across.
5. **Operators and beacons are external.** Only synomic agents own
   entarts. Beacons are connective tissue between external operators
   and the entart tree; teleonomes are external too.
6. **Local-by-default, scatter-gather for global.** Cross-Space rules
   and loops ship a portable `&self`-body to each target, run locally,
   aggregate small results.
7. **Rules and loops ride with data.** Both are atoms; both replicate
   to subscribers through the same channel as state. Partial-sync
   teleonomes stay current automatically; identity-driven boot picks
   them up at evaluation time.

**The synome root layers:**

| Layer | Representative Spaces |
|---|---|
| Constitutional | `&core-root`, `&core-telos`, `&core-skeleton`, `&core-governance`, `&core-protocol` |
| Framework | `&core-framework-risk`, `&core-framework-distribution`, `&core-framework-fee` |
| Registry | `&core-registry-entity`, `&core-registry-beacon`, `&core-registry-contract` |
| Aggregation | `&core-settlement`, `&core-escalation`, `&core-endoscrapers` |
| Executable | `&core-syngate`, `&core-telgate`, `&core-loop-<class>` |
| Library | `&core-library-runtime-<impl>`, `&core-library-telseed-<config>`, `&core-library-corpus-<domain>`, `&core-library-published-<topic>` |

**The four artifact types:**

| Artifact | Tree shape | Replication | Privacy |
|---|---|---|---|
| Synart | synome root + entart subtrees | global (synserv → all participants) | public |
| Entart | one synent's subtree of synart | inherits synart replication | scoped via auth |
| Telart | per-teleonome tree of Spaces | within own emb fleet | private to that tel |
| Embart | per-embodiment tree of Spaces | local only (never replicated) | private to that emb |

Full economic and content treatment in `syn-tel-emb.md`.

**The naming convention:**

```
core-<kind>[-<topic>...]                                  // synome-level
entity-<entity-type>-<entity-id>-<sub-kind>[-<sub-id>]    // entart-level
```

**An entart tree (Ozone single-guardian topology, Spark expanded):**

```
&core-root
  └── &entity-guardian-ozone-root              ← single operational guardian
        ├── &entity-generator-usge-root        ← USDS Generator
        ├── &entity-prime-spark-root
        │     ├── &entity-prime-spark-sentinel-baseline   ← per-Prime sentinel formations
        │     ├── &entity-prime-spark-sentinel-stream
        │     ├── &entity-prime-spark-sentinel-warden
        │     ├── &entity-halo-spark-term-root
        │     │     ├── &entity-halo-spark-term-book-usds
        │     │     └── &entity-halo-spark-term-book-cnys
        │     └── &entity-halo-spark-trade-root
        │           └── &entity-halo-spark-trade-book-amm
        ├── &entity-prime-grove-root
        └── &entity-prime-obex-root
```

**Thirteen Phase 1 commitments** (§20) — hygiene that makes scaling free.

---

## Section map

| § | Topic | Core idea |
|---|---|---|
| 1 | Hyperon Spaces basics | Spaces as grounded atoms; data + rules + programs; gate ≠ Space boundary |
| 2 | Taxonomy mapping | Synome / telart / embart aligns with Hyperon's split |
| 3 | The four artifact types | Synart, entart, telart, embart — trees of Spaces with distinct replication |
| 4 | Four sharding axes | Authority / tenant / temperature / cadence — orthogonal |
| 5 | The entart concept | Synart's tree-of-entarts structure |
| 6 | Synome root: six layers | Constitutional / framework / registry / aggregation / executable / library |
| 7 | Four meta-patterns | Frameworks propagate; registries hold identity; aggregations collect; specifications execute |
| 8 | The self-hosting architecture | Synart contains its own programs; identity boots roles; five levels of self-reference |
| 9 | Naming convention | `core-<kind>` and `entity-<type>-<id>-<sub-kind>` keyword vocabulary |
| 10 | Operators and beacons external | Not entart owners; connective tissue |
| 11 | Example: Spark's entart family | Full tree with sentinel + book Spaces |
| 12 | Registry pattern | `(sub-entart …)` and `(sub-space …)` |
| 13 | Asymmetry rule | Parent → child only; peers via common ancestor |
| 14 | Local consistency | Each Space self-complete for some purpose |
| 15 | Local-by-default | Scatter-gather for cross-Space; push code to data |
| 16 | Two-step rule shape | Portable `&self` body + global declaration |
| 17 | Two-step loop shape | Universal template + per-entity instance |
| 18 | Aggregator design | Trivial / concat / sketch classes |
| 19 | Phase 1 commitments | Thirteen total |
| 20 | Pattern families to build | What's sketched, what's open |
| 21 | One-line summary | Whole architecture compressed |

---

## 1. What's load-bearing about Hyperon Spaces

Five facts from the Hyperon model do most of the work:

1. **Spaces are grounded atoms with a uniform API.** A Space is a value;
   `(match $space …)` is a regular call. Synlang names Spaces from day 1;
   the binding from logical name → physical backend is a runtime concern.
   Splitting later doesn't change synlang code.
2. **Spaces hold data, rules, AND programs.** A Space's atoms can be
   facts (`(unit nfat-7 …)`), rules (`(= (unit-risk-weight $u) …)`), or
   loop bodies (`(= (run-forever) …)`). The runtime treats all three
   uniformly — they're all atoms, queryable by the same primitives.
   This is what makes self-hosting possible: programs are content.
3. **DAS is the substrate the canonical synart wants.** Slowly-changing
   graph of truth, partitioned across machines, parallel match,
   hub-replication for high-degree atoms.
4. **Cross-Space ≠ trust boundary.** Within one Synome runtime, all
   Spaces share trust. Cross-Space writes are direct `add-atom`. The gate
   sits only at runtime ingress.
5. **Spaces don't solve consistency, conflicts, or attention.** Those
   live above the Space API. Synserv (sole sequencer) handles
   consistency; gate + nonces handle conflicts; per-Space subscription
   handles attention.

Fact 2 is the most consequential addition versus the original four.
Once you accept it, the synome architecture's self-hosting properties
follow naturally — see §8.

---

## 2. Taxonomy mapping

| Hyperon concept | Synome concept | Notes |
|---|---|---|
| Canonical rules / invariants | **Deontic skeleton** | replicated, gate-mediated |
| Domain knowledge base | **Canonical probmesh / library** | replicated, gate-mediated |
| Teleonome long-term memory | **Telart** + local probmesh | per-teleonome, replicated within own emb fleet |
| Embodiment working memory | **Embart** / operational workspace | per-embodiment, never replicated |
| DAS / deep memory | Synart's storage substrate | underneath all canonical state |

Synome / telart / embart is "many small fast Spaces + shared canonical
Spaces + distributed deep Spaces + explicit bridges."

The next section spells out the four artifact types in depth — this
table is just the Hyperon mapping.

---

## 3. The four artifact types

The synome has four artifact tiers, each a **tree of Spaces** with
distinct replication and privacy properties:

### Synart — the canonical tree

| | |
|---|---|
| Tree shape | synome root layers (`&core-*`) + entart subtrees (`&entity-*`) per synomic agent |
| Replication | global — synserv → every participant (modulo selective sync) |
| Privacy | public; read access universal |
| Authority | governance writes via constructors; gate-mediated |
| Mutability | append-only / governance-revocable |
| Content | open-source SOTA: knowledge corpora, framework parameters, registries, loops, gates, recipes, runtime source, telseeds, published alpha, settlement aggregations |

Synart is "the commons brain." Every running participant pulls from it.
Detailed treatment in `syn-tel-emb.md` §1.

### Entart — a synent's subtree of synart

| | |
|---|---|
| Tree shape | one root Space (`&entity-<type>-<id>-root`) plus sub-Spaces registered through `(sub-entart …)` and `(sub-space …)` atoms |
| Replication | inherits synart replication |
| Privacy | scoped via auth atoms — anyone can read, only authed identities can write |
| Authority | the synomic agent (Guardian / Prime / Halo) and parent-chain delegates |
| Content | identity, sub-entart and sub-Space registries, scope-local policies, cross-sub-entart rules, per-entity loop instances |

An entart is the structural unit of synart. The synart is the union of
all entarts plus the synome root's universal Spaces. See §5.

### Telart — per-teleonome private state

| | |
|---|---|
| Tree shape | telgate (instance of `&core-telgate`), alpha store, call-out services, strategy config, dreamart, experience archive, endowment record |
| Replication | within one tel's own emb fleet only |
| Privacy | private to that tel; no other tel sees it |
| Authority | the teleonome (and its identity) |
| Content | proprietary alpha, accumulated RSI lift, private data, dreamer output, founder bequest, telgate state |

Telart is "the teleonome's moat." Detailed treatment in `syn-tel-emb.md`
§2.

### Embart — per-embodiment hardware-local state

| | |
|---|---|
| Tree shape | one execution Space per running loop, a working-memory Space, transient cycle state |
| Replication | none — local to one embodiment |
| Privacy | private to that emb |
| Authority | the runtime process |
| Content | per-loop execution context, current cognitive scratchpad, draft proposals, transient working state |

Embart is "hardware-local working state." Detailed treatment in
`syn-tel-emb.md` §3.

### Authority hierarchy

The replication / privacy gradient also defines an authority hierarchy:

```
synart  >  telart  >  embart
(public, vetted)  (private, alpha)  (local, transient)
```

Crystallization promotes telart content into synart through a
peer-review-shaped publication gate. Embart content gets promoted
into telart through the tel's own internal review (typically dreamer
output → strategy adoption). The gradient runs from "what's true and
shared" down to "what one emb is doing right now."

---

## 4. The four sharding axes

Sharding isn't one decision. There are at least four roughly-orthogonal
axes:

| Axis | Examples |
|---|---|
| **A. Authority** | constitutional / governance / operational / library |
| **B. Tenant** | per-Prime, per-Halo, per-Class |
| **C. Temperature** | hot (active samples) / warm (last settled) / cold (history) |
| **D. Cadence** | near-immutable axioms / slow-write governance / fast-write events / probabilistic mesh |

A single Space sits at one point on each axis. Backend choice follows
from the cell.

The executable layer (loops, gates) and library layer (runtimes,
telseeds, corpora) fit naturally in this axis space — they're
universal-replication × constitutional-cadence × authority-governance.
No new axis is needed; the existing four cover the new content
classes.

---

## 5. The entart concept

A **synomic entity** (synent) is one of the agent types that constitutes
the synome: Guardian, Prime, Halo. Every synent owns an **entart** — its
slice of the synart, structured as a subtree of Spaces rooted at one
**root Space**.

The synart is the union of all entarts plus the synome root's universal
`&core-*` Spaces. Every non-universal Space belongs to exactly one
entart's subtree. Universal Spaces (`&core-*`) are owned by the
**synome root entart** and are replicated everywhere.

### What lives in a root Space

The root Space is the synent's identity *and* the entry point into its
subtree:

```metta
;; identity
(synent spark-prime)
(synent-type spark-prime prime)
(synent-name spark-prime "Spark Prime")
(parent-entart spark-prime ozone)

;; sub-entart registry (nested entities, each has its own root)
(sub-entart spark-prime spark-term-halo  &entity-halo-spark-term-root)
(sub-entart spark-prime spark-trade-halo &entity-halo-spark-trade-root)

;; leaf Space registry (directly attached, no further nesting)
(sub-space spark-prime &entity-prime-spark-config)

;; per-entity loop instances (Phase 9-10+)
(sub-space spark-prime &entity-prime-spark-sentinel-baseline)
(sub-space spark-prime &entity-prime-spark-sentinel-stream)
(sub-space spark-prime &entity-prime-spark-sentinel-warden)

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
5. **Reference asymmetry generalizes** (§13): parent → child only; peers
   via common ancestor.
6. **Per-entity programs.** When the synome knows an entity's full
   structure, it can host a fully-configured loop instance for that
   entity inside its entart (see §17 — two-step loop shape).

---

## 6. Synome root: six layers

The synome root entart holds universal Spaces, organized into six layers
with consistent mechanics within each layer.

### Constitutional layer

The bedrock. Different rooms with different rules; all
universally-replicated, all rarely-written.

| Space | Contents | Change cadence |
|---|---|---|
| `&core-root` | Synome root entart's root Space; sub-entart and sub-space registries | governance-paced |
| `&core-telos` | Apex axiom — what the system is for | constitutional (~never) |
| `&core-skeleton` | Constitutional axioms, types, invariants | constitutional rewrite |
| `&core-governance` | Core Council legislative chamber, including the bootstrap seed (`role-def root-authority`, `role-grant core-council`) as initial state | governance-paced |
| `&core-protocol` | Chain protocol specifications — contract addresses, ABIs, event signatures, the canonical "what to look for on chain" reference for endoscrapers and verifiers | governance-paced |

`&core-protocol` is sibling-of-`&core-skeleton` in role: skeleton tells
us what must be true about ledger state; protocol tells us how to *read*
ledger state. Both rarely change, both universally replicated.

### Framework layer

Universal shapes + parameter bounds. Each entart gets its own values
constrained by the framework via layered tightening. Updates project
out via scatter-gather.

| Space | Contents |
|---|---|
| `&core-framework-risk` | ER formula, covenant arithmetic, loop/depth/repeat heuristic parameters |
| `&core-framework-risk-categories` | Catalog of risk categories at three levels (exo asset / exobook / riskbook); each category carries a parameterized stress-simulation equation. See `risk-framework.md` §3-§4. |
| `&core-framework-stress-scenarios` | Library of stress scenarios used by category equations (severe-correlated-crash, credit-crisis, etc.); see `risk-framework.md` §6 |
| `&core-framework-concentration` | Concentration categories + global limits (deferred); see `risk-framework.md` §13 |
| `&core-framework-distribution` | Distribution rewards rate, integration boost shapes |
| `&core-framework-fee` | Agent upkeep, protocol fees, fee shapes, recipe pricing levers |

### Registry layer

Flat identity indexes for things whose actual state lives elsewhere
(external processes, on chain, or in entart subtrees). Push/pull
onboarding (proposed → accepted). Authority comes from cert/auth atoms
elsewhere, not from registration.

| Space | Contents |
|---|---|
| `&core-registry-entity` | All entarts (denormalized index for discovery; tree is canonical) |
| `&core-registry-beacon` | All beacons + tels (operators are external; pubkey + status + class + loop pointer here — see `boot-model.md` §4) |
| `&core-registry-contract` | All on-chain contracts (state lives on chain; thin reference layer) |
| `&core-registry-exo-book` | All monitored exo books — external structures the synome reads but doesn't control (Morpho markets, custody accounts, real-world claims). Populated by external endoscrapers. See `risk-framework.md` §3. |

### Aggregation layer

Where Phase-2 scatter-gather outputs land. Each entart computes locally;
synserv aggregates into these Spaces. Also where the verification
inflow stages.

| Space | Contents |
|---|---|
| `&core-settlement` | Sky-wide financial aggregation (penalties owed, distributions, fees, settlement totals) |
| `&core-escalation` | Disputes, slashing reports, contested operations, verification disagreements |
| `&core-endoscrapers` | Endoscraper output staging — raw scraped chain events, processed and streamed to relevant entart Spaces, then pruned |

### Executable layer

The synome's continuous machinery — gates that mediate ingress, loops
that run roles, recipes that bundle loops with economics. **This is
where the synome's program lives.**

```
Gates:
  &core-syngate                     — synserv's gate (synserv runs the canonical instance)
  &core-telgate                     — universal telgate spec (every tel runs an instance with
                                       state in their telart)

Loops (universal templates):
  &core-loop-synserv                — synserv heartbeat
  &core-loop-beacon-<class>         — per beacon class (lpla, lpha, hpla, hpha)
  &core-loop-sentinel-<formation>   — Baseline / Stream / Warden patterns
  &core-loop-endoscraper-<protocol> — chain-scraping verifier per protocol component
  &core-loop-archive                — full event capture
  &core-loop-verifier               — generic re-derivation

Recipes (loops bundled with economics — see syn-tel-emb.md §8):
  &core-recipe-* (loop body + payment terms + slashing + auth requirements)
```

Universal templates in this layer; per-entity instances live in entarts
(see §17). Identity boots an emb against either a universal template
(generic role) or a per-entity instance (specialized role).

#### Endoscraper vs exoscraper

Endoscrapers (in scope for current design) read **internal protocol
smart contract state** on **public blockchains** — fully deterministic,
publicly auditable, no insurance overhead. They write into
`&core-endoscrapers` for processing, then forward verified data to the
relevant entart Spaces.

Exoscrapers (out of scope, term reserved) would read **external APIs,
proprietary feeds, off-chain services** — uncertain provenance, requires
governance review, fallback, dispute resolution. Exoscraper design is
deferred.

#### The verification cycle

Endoscrapers enable independent verification of beacon and sentinel
claims:

```
1. Sentinel/Baseline decides to act (e.g., sell NFAT-X)
2. Beacon executes on-chain transaction
3. Sentinel writes to synart: tx hash + state delta + strategy justification pointer
4. Endoscraper independently scrapes the same chain event
5. Reconciler atom fires when both arrive: agreement → settle; disagreement → &core-escalation
```

This is the operational form of "synserv verifies what beacons report."

### Library layer

The synome's commons content — the open-source substrate that every
participant can pull from.

| Sub-pattern | Contents |
|---|---|
| `&core-library-runtime-<impl>` | Atomspace runtime source (Noemar et al.); versioned, hash-addressed, signed |
| `&core-library-telseed-<config>` | Telseed catalog — vetted starting configurations for new tels |
| `&core-library-corpus-<domain>` | Knowledge corpora (financial, scientific, technical, governance) |
| `&core-library-published-<topic>` | Crystallized alpha promoted from telart through the publication gate |

Library Spaces are large by volume but slow-changing. Replication
strategy: aggressive caching at subscribers; partial sync for embs that
only need certain corpora. See `scaling.md` for load implications.

The library is the deepest version of self-hosting — not only does the
synart contain its own loops and gates, it contains the *source code
of the runtime that interprets it.* See §8.

---

## 7. Four meta-patterns

The six-layer factoring is descriptive; the four meta-patterns
underneath it are *prescriptive*. When someone proposes a new universal
Space, ask "is this a framework, registry, aggregation, or
specification?" — the answer determines its mechanics. If it's none of
those, push back.

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
&core-settlement / &core-escalation / &core-endoscrapers
```

- Scatter-gather collection at synserv
- Settlement-paced, event-paced, or stream-paced writes
- Read by everyone, written only by synserv aggregator
- "Single source of truth" for Sky-wide totals or processed inflow

### Specifications (executable code, replicated)

```
loop / gate / recipe atoms  →  &core-loop-* / &core-syngate / &core-telgate / &core-recipe-*
                                     │
                                     │ replicated to every participant
                                     ▼
runtime evaluates the Space     →  identity-driven boot picks entry point
```

- Universal canonical executable specifications
- Read by anyone instantiating the role (any conforming runtime)
- Replicated to all participants — even those who won't run the role
  (so verifier embs can shadow-execute, governance can audit, etc.)
- Versioned via global rule publication metadata
- Updated rarely — constitutional-grade governance for changes
- Per-entity specializations live in entarts (§17)

This is the fourth meta-pattern, distinct from the first three. It's
what makes self-hosting work: programs are atoms, replicated through
the same channel as state, evaluated by runtimes that mount the synart
as `&self`-context.

---

## 8. The self-hosting architecture

The synart contains its own programs. The runtime is just an
interpreter pointed at synart with an identity. This section captures
the structural consequences at the topology level. Depth treatment of
the boot mechanism lives in `boot-model.md`; depth treatment of the
economic engine that funds it lives in `syn-tel-emb.md` §8.

### The five levels of self-reference

Canonical home for this enumeration is `syn-overview.md`. Brief listing
here for topological context:

1. **Self-hosting** — synart contains the loops that run synart
2. **Self-regulating** — synart contains the gates that regulate synart access
3. **Self-paying** — synart contains the recipes that fund work on synart
4. **Self-seeding** — synart contains the telseeds that birth new teleonomes
5. **Self-improving** — synart funds the runtime / library / probmesh work that synart runs on

Every level rests on the executable + library layers of the synome
root being load-bearing. A topology that puts loops outside synart, or
runtime source outside synart, can't achieve any of these levels.

### The spec/instance collapse

In typical software architectures, code and running instances are
separate: you install the program, then run instances. In the synome:

- Code is in `&core-loop-*` (universal templates) and `&entity-*-<sub-kind>` (per-entity instances)
- Running an instance = pointing a runtime at the Space and evaluating its `(run-forever)` with that Space as `&self`
- There's no install step; the synart copy *is* the program

This collapses what would be three concepts elsewhere — the source code,
the deployed binary, the running process — into one substrate plus an
interpreter. See `boot-model.md` for the runtime mechanics.

### Identity-driven boot

```
noemar boot --identity=X --key=… --synart=…
   ↓
mount synart
   ↓
look up X in &core-registry-beacon → loop pointer
   ↓
evaluate (run-forever) with that Space as &self
```

One boot procedure, many roles. Synserv, beacons, sentinels, archive
embs, verifiers — all the same machine, parameterized by identity. The
identity determines which loop runs and (via auth atoms) what writes
count as canonical.

### The recipe marketplace at topology level

The executable + library layers together constitute a regulated
marketplace for monetizing AGI capability. Recipes (loops + economics +
auth + slashing) are the products. Teleonomes are diversified providers.

Topologically, recipes live in the executable layer (or factored as
`&core-recipe-*` adjacent to it). The economics atoms attached to a
recipe live in the framework layer (`&core-framework-fee`). The catalog
itself — which recipes exist, in what state — is governance-curated
content in `&core-governance`.

Canonical economic treatment is `syn-tel-emb.md` §8. Topology's role
is just to host the structures.

---

## 9. The naming convention

Two patterns, one for each scope:

```
core-<kind>[-<topic>...]                                  // synome-level
entity-<entity-type>-<entity-id>-<sub-kind>[-<sub-id>]    // entart-level
```

Reserved keyword vocabulary:

| Slot | Values |
|---|---|
| `core <kind>` | `root`, `telos`, `skeleton`, `governance`, `protocol`, `framework`, `registry`, `settlement`, `escalation`, `endoscrapers`, `syngate`, `telgate`, `loop`, `recipe`, `library` |
| `loop <kind>` (within `&core-loop-*`) | `synserv`, `beacon-<class>`, `sentinel-<formation>`, `endoscraper-<protocol>`, `archive`, `verifier` |
| `library <kind>` (within `&core-library-*`) | `runtime-<impl>`, `telseed-<config>`, `corpus-<domain>`, `published-<topic>` |
| `entity <type>` | `guardian`, `generator`, `prime`, `halo` (extensible: `foreign` for cross-chain, etc.) |
| `entity <sub-kind>` | `root`, `primebook`, `halobook`, `riskbook-<rb-id>`, `genbook`, `structural-demand`, `structural-demand-scrapers`, `structural-demand-auction`, `book`, `class`, `config`, `history`, `sentinel-<formation>` (book-type sub-kinds reflect the four-book taxonomy from `risk-framework.md` §1) |

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
&core-protocol
&core-framework-risk
&core-framework-distribution
&core-framework-fee
&core-registry-entity
&core-registry-beacon
&core-registry-contract
&core-settlement
&core-escalation
&core-endoscrapers
&core-syngate
&core-telgate
&core-loop-synserv
&core-loop-beacon-lpla-checker
&core-loop-sentinel-baseline
&core-loop-endoscraper-spark-pau
&core-library-runtime-noemar-v0.x
&core-library-telseed-research-v2
&core-library-corpus-financial
```

Entart-level:

```
&entity-guardian-ozone-root                  Ozone — single operational guardian
&entity-generator-usge-root                  USDS Generator entart root
&entity-generator-usge-genbook               Genbook — Primeunits in, USDS out
&entity-generator-usge-structural-demand     structural demand capacity + distribution
&entity-prime-spark-root                     Spark Prime's entart root
&entity-prime-spark-primebook                Spark's Primebook (aggregates Halobook units)
&entity-prime-spark-config                   config sub-Space attached to Spark Prime root
&entity-prime-spark-sentinel-baseline        Spark Prime's per-entity Sentinel-Baseline loop instance
&entity-prime-spark-sentinel-stream
&entity-prime-spark-sentinel-warden
&entity-halo-spark-term-root                 Spark Term Halo's entart root
&entity-halo-spark-term-halobook             Spark Term Halo's Halobook
&entity-halo-spark-term-book-usds            USDS book leaf in Spark Term Halo
&entity-halo-spark-term-book-cnys            CNYS book leaf
&entity-halo-spark-trade-root                Spark Trade Halo's entart root
&entity-halo-spark-trade-book-amm            AMM book leaf
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

## 10. Operators and beacons are external

A **beacon** is an external process — running on an embodiment somewhere
with a private key. It interacts with the synart only via gate-mediated
submissions. There's no internal "beacon state" inside synart, only
*facts about the beacon*.

**Beacons aren't entarts.** Facts about beacons live where they're used:

| Fact about beacon | Lives in | Why |
|---|---|---|
| Pubkey + status + class + loop pointer | `&core-registry-beacon` | needed at the gate for sig verification + at boot for loop resolution, globally |
| `(cert beacon-X by-ozone)` | `&entity-guardian-ozone-root` | guardian holds underwriting liability |
| `(auth beacon-X verb target)` | entart owning the target | target's owner controls auth |
| Submission history | wherever it wrote | provenance follows writes |

There's no place where you'd say "this is the beacon's stuff"
cohesively. Entarts are for synomic *agents* (Guardian, Prime, Halo) —
the structural units of the synome. Beacons are *connective tissue*
between external operators and that structure.

### Operators (including teleonomes) are external too

Operators of all kinds — companies (soter-govops, devcos), teleonomes,
Core Council members, individual humans — are external. They run
embodiments which run beacons; the beacons are registered, certed, and
authed through the entart tree, but operators themselves aren't *in*
the tree. Their internal state is in telart (per-teleonome) or off-
synart entirely.

This is a clean separation:

- **Entart owners** = synomic agents (structural units)
- **Operators** = external entities running embodiments (humans, companies, teleonomes)
- **Beacons** = the connective tissue between them

See `syn-tel-emb.md` for full treatment of how teleonomes' telart and
embart trees relate to the synart they participate in.

### Push/pull beacon registration

```
1. Push: beacon proposes itself
   (beacon-pending beacon-X (pubkey "ab9c…") (operator soter-govops) (class lpha))

2. Pull: governance accepts
   (beacon-accepted beacon-X)
   (beacon-status beacon-X active)

3. Cert: rooted in the Guardian's entart
   ;; in &entity-guardian-ozone-root
   (cert beacon-X by-ozone)

4. Auth: granted in entarts whose parent chain includes Ozone
   ;; in &entity-prime-spark-root or further down
   (auth beacon-X issue-unit book-B7)
```

"Accordant to the Guardian" cleanly cashes out as "the entart's parent
chain reaches Ozone." Beacons certed by `ozone` can be authed anywhere
in Ozone's subtree — `spark-prime`, `spark-term-halo`, `usge`, etc.
Since Ozone is the single operational guardian, this currently means
"any entity in the synome."

---

## 11. Example — the Ozone entart family

```
&core-root
  │
  └── &entity-guardian-ozone-root                    Ozone — single operational guardian;
        │                                            vote outcomes; cert-atoms for all
        │                                            GovOps teams' beacons
        │
        ├── &entity-generator-usge-root              USDS Generator entart root
        │     ├── &entity-generator-usge-genbook     Genbook — holds Primeunits, issues USDS
        │     └── &entity-generator-usge-structural-demand
        │           ├── &entity-generator-usge-structural-demand-scrapers
        │           └── &entity-generator-usge-structural-demand-auction
        │
        ├── &entity-prime-spark-root                 Prime auth, policies, halo registry, cross-halo rules
        │     │
        │     ├── &entity-prime-spark-primebook      Prime's aggregation book; holds Halobook units; issues to Genbook
        │     │
        │     ├── &entity-prime-spark-sentinel-baseline    per-Prime sentinel formations
        │     ├── &entity-prime-spark-sentinel-stream       (each holds entity-specific config +
        │     ├── &entity-prime-spark-sentinel-warden        reference to universal loop template)
        │     │
        │     ├── &entity-halo-spark-term-root             halo policies, registry of riskbooks
        │     │     ├── &entity-halo-spark-term-halobook   Halo's aggregation book; holds Riskbook units; issues to Primebook
        │     │     ├── &entity-halo-spark-term-riskbook-A Riskbook (matches a registered category, e.g. abf-with-cds-cover)
        │     │     ├── &entity-halo-spark-term-riskbook-B Riskbook (matches a different category, e.g. morpho-lending)
        │     │     └── &entity-halo-spark-term-riskbook-C Riskbook (yet another category)
        │     │
        │     └── &entity-halo-spark-trade-root
        │           ├── &entity-halo-spark-trade-halobook
        │           └── &entity-halo-spark-trade-riskbook-D
        │
        ├── &entity-prime-grove-root                 Star Prime — similar structure to Spark
        └── &entity-prime-obex-root                  Institutional Prime — similar structure
```

Each root holds identity + registries + scope-local policies +
cross-sub-entart rules. The four-book taxonomy from `risk-framework.md`
§1 is reflected in the Space layout: each Prime has one Primebook;
each Halo has one Halobook plus one or more Riskbooks; the Generator
has one Genbook. Per-entity sentinel Spaces (Phase 9-10+) hold
entity-specific configurations of universal loop templates — see §17.

**Single-guardian topology:** Ozone is the only Guardian; USGE and all
Primes are direct children. Multiple GovOps teams (e.g., the Spark
operator, the Grove operator, the USGE operator) are rooted under
Ozone; each operates the entity it administers. The Guardian/GovOps
separation from `synart-access-and-runtime.md` §4 holds — only the
Guardian count is collapsed to one.

Operationally, there's also an endoscraper running in synserv that
verifies Spark's claims:

```
&core-loop-endoscraper-spark-pau   universal scraper for Spark PAU contracts
                                    (synserv runs; reads &core-protocol;
                                     writes verified events into entart leaves
                                     and stages raw output in &core-endoscrapers)
```

The endoscraper doesn't live in Spark's entart — it's universal
synserv machinery that *verifies* Spark's entart. See §6 (executable
layer).

---

## 12. The registry pattern

Inside an entart root, registry atoms name what's underneath:

```metta
;; in &entity-prime-spark-root
(sub-entart spark-prime spark-term-halo  &entity-halo-spark-term-root)
(sub-entart spark-prime spark-trade-halo &entity-halo-spark-trade-root)
(sub-space  spark-prime &entity-prime-spark-sentinel-baseline)
(sub-space  spark-prime &entity-prime-spark-sentinel-stream)
(sub-space  spark-prime &entity-prime-spark-sentinel-warden)

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

## 13. The asymmetry rule

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

## 14. Each Space is locally consistent

Design each Space so it's **internally complete** for some purpose:

- `&entity-halo-spark-term-book-usds` — locally consistent for USDS-book reasoning
- `&entity-prime-spark-root` — locally consistent for Spark policy/authority
- `&entity-prime-spark-sentinel-baseline` — locally consistent for running Spark's Baseline (config + reference)
- The combination — gives aggregate views that don't exist in any
  single Space (Prime ER, multi-Halo covenants)

If you skip a Space, you lose views that needed it. You don't lose any
view that lived purely in the Spaces you kept.

---

## 15. Local-by-default; global as scatter-gather

The architectural principle:

> **Every Space tries to compute everything locally as much as possible.
> Cross-Space rules are scatter-gather: ship the rule to each target
> Space, run it locally against `&self`, return small results, aggregate.**

Same insight that drives MapReduce / Spark / DAS-style query routing.
Push computation to data; don't pull data to a coordinator. For our
setup it's especially clean because rules are atoms — "ship the rule"
is literally `(add-atom &target rule)`.

Same principle applies to loops (§17): ship a portable loop body that
uses `&self`, run it in whichever entart Space hosts it.

---

## 16. The two-step rule shape

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

## 17. The two-step loop shape

The same pattern applies to loops. **Loops live at two levels:**

| Level | Where | Role |
|---|---|---|
| Universal template | `&core-loop-<class>` | portable loop body using `&self`; canonical, audited |
| Per-entity instance | `&entity-<type>-<id>-<sub-kind>` | entity-specific config + binding context for the template |

### Example — Sentinel-Baseline for Spark

```metta
;; ── Universal template in &core-loop-sentinel-baseline ────────────
(= (run-forever)
   (let* (($_ (heartbeat))
          ($_ (delay (current-interval))))
     (run-forever)))

(= (heartbeat)
   (let* (($entity      (match &self (entity-bound-to $e) $e))
          ($market-state (snapshot-market $entity))
          ($strategy    (match &self (strategy-id $s) $s))
          ;; designated call-out into local cognition
          ($candidate (call-out llm-rank
                        (inputs $market-state $strategy)
                        (output-shape allocation-id)))
          ($safe? (within-baseline-envelope $candidate $entity)))
     (case $safe?
       ((True (gate-out (sign-and-emit $candidate)))
        (False (audit-rejected $candidate))))))

;; ── Per-Prime instance in &entity-prime-spark-sentinel-baseline ───
(entity-bound-to spark-prime)
(strategy-id     spark-baseline-strategy-v3)
(current-interval 30s)
(target-halos    spark-term-halo spark-trade-halo)
(rar-threshold   0.05)
(import-loop     &core-loop-sentinel-baseline)
```

### Why this works

The synome can preconfigure each entity's loop Spaces because the
entity's structure is **fully described in synart**. The loop doesn't
do dynamic config-lookup at runtime; the config is baked into the
entity Space at the moment the entity is fully described.

When an emb boots "as Spark Prime's Baseline sentinel," it boots with
`&entity-prime-spark-sentinel-baseline` as `&self`. The loop body
imported from the universal template runs in that context. Same code,
different entity bindings.

### Properties that fall out

- **Cleaner audit trail.** Reading `&entity-prime-spark-sentinel-baseline`
  tells you exactly what configuration this entity will run.
- **Cleaner runtime.** No dynamic resolution of config; it's all bound
  at the entity Space.
- **Cleaner upgrade path.** Improve the universal template; entity
  Spaces unchanged. Or update one entity's config; template unchanged.
- **Different entities, different configurations, same code.** Spark and
  Grove both run Sentinel-Baseline against the same template, but
  each has its own per-entity Space with its own bindings.
- **Verifier embs use the same Space.** A Warden verifying Spark's
  Baseline boots with the same per-entity Space; runs the same code;
  derives the same expected behavior. Shadow execution from §8 falls
  out naturally.

---

## 18. Aggregator design

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

## 19. The full Phase 1 commitment list

Original seven from `synart-access-and-runtime.md`:

1. Space is always a parameter, never implicit.
2. Append-only writes.
3. Content-addressed names.
4. Open verb dispatch via whitelist atoms.
5. Gate as real primitive at trust boundary.
6. `(can …)` reads from a named auth Space.
7. Idempotent constructors.

Added by structural design:

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

Added by self-hosting:

13. **Loops, gates, and recipes are first-class synart content.**
    Universal templates live in the executable synome-root layer
    (`&core-loop-*`, `&core-syngate`, `&core-telgate`, `&core-recipe-*`);
    entity-specific configurations live in entarts referencing those
    templates (§17). Identity selects entry point at boot
    (`boot-model.md`).

These aren't really about scale — they're good design hygiene that
incidentally makes scaling free. If you build a clean single-Space
system that does these thirteen, "scale to multi-Space" is purely a
runtime change: bind the Space names to different physical stores, add
routing data, replicate hub atoms. The synlang code doesn't change.

---

## 20. Pattern families to build

The structural layer is settled. The synlang patterns that live
*inside* it — the actual constructors, lifecycle rules, and governance
flows — are at varying maturity. This is the open work surface.

| Pattern family | Scope | Status |
|---|---|---|
| Authority chain (Council → Guardian → Prime → Halo) | synart | Sketched; full hierarchy not built |
| Beacon lifecycle (cert / auth / revoke / status transitions) | `&core-registry-beacon` + per-Guardian cert atoms | Old demo uses direct `space.add`; no constructor |
| Agent construction (Directive + Axioms + Resources = Agent) | synart | Not started |
| Accordancy edges between synents | per-entart roots | Old demo uses `(administers …)`; canonical pattern is parent-entart links + `(auth …)` per `settlement-cycle-example.md` |
| Governance proposals (vote / ratify / enact) | `&core-governance` | Not started |
| State machines | per-entart leaf Spaces | Old demo covers Book lifecycle; broader pattern abstractable |
| Attestation gates / two-beacon patterns | per-entart leaf Spaces | Old demo covers single-actor; multi-beacon split not built |
| Crystallization commits (mesh → skeleton promotion) | `&core-library-published-*` → `&core-skeleton` | Not started |
| Rate limits & enforcement caps (LPLA / LPHA / HPLA / HPHA) | per-entart roots | Not started |
| Cross-entart atomic writes | multi-Space within one synserv | Conventions defined, not exercised |
| Revocation cascades (Guardian collapse → propagation) | down-tree from `&entity-guardian-*-root` | Not started |
| Sentinel formations (Baseline / Stream / Warden) | `&core-loop-sentinel-*` + per-entity Spaces | Patterns documented in `synlang-patterns.md`; integration not built |
| Recipe marketplace catalog | `&core-loop-*` + `&core-recipe-*` + `&core-framework-fee` | Concept documented in `syn-tel-emb.md` §8; minimal recipes only in Phase 1 |
| Risk framework (four-book taxonomy + categories + stress simulation) | `&core-framework-risk-*` + `&core-registry-exo-book` + per-entart books | Documented in `risk-framework.md`; concentration L3 (Halobook/Primebook category constraints) design deferred |
| Stress scenario library | `&core-framework-stress-scenarios` | Concept in `risk-framework.md` §6; library not populated |
| Riskbook category catalog | `&core-framework-risk-categories` (riskbook level) | Concept in `risk-framework.md` §4; catalog not populated; default-deny CRR 100% means category catalog completeness is governance priority |
| Endoscraper-driven exo book registry | `&core-registry-exo-book` populated by external endoscrapers | Pattern documented; per-protocol endoscraper implementations not built |
| Endoscraper class | `&core-loop-endoscraper-*` + `&core-endoscrapers` | Pattern documented; per-protocol implementations not built |
| Telseed catalog | `&core-library-telseed-*` | Concept documented in `syn-tel-emb.md` §4; no live catalog yet |
| Atomspace runtime conformance | `&core-library-runtime-*` + governance test atoms | Conformance suite not built |

Each row is a candidate for its own focused design pass.

---

## 21. The one-line summary

**Synart is a tree of entarts plus a six-layer synome root holding
universal Spaces — constitutional axioms and chain protocol;
parameterized framework shapes; flat identity registries; aggregation
outputs; the executable layer of loops/gates/recipes that *are* the
synome's program; and the library layer of runtimes/telseeds/corpora/
published alpha that's the open-source commons. Four meta-patterns
(frameworks propagate, registries identify, aggregations collect,
specifications execute); operators and beacons are external; per-entity
loop instances reference universal templates via the two-step pattern;
the whole stack is self-hosting, with identity-driven boot resolving
which loop Space a runtime evaluates as `&self`.**
