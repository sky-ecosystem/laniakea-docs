# Topology — Spaces, Entarts, Artifacts, and the Self-Hosting Synart

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

### What multi-Space architecture actually buys

A persistent confusion is that "more Spaces = more scaling." In practice the wins are structural, not throughput-related:

| Real wins | Not real wins |
|---|---|
| Replication topology granularity (per-entart subscription — light embs sync just one leaf) | Raw query perf (indexes do that) |
| Lifecycle isolation (archive closed entities) | Trust separation within one runtime (cross-Space ≠ trust boundary; see fact 4) |
| Mobility / repartitioning unit | Failure isolation (operational discipline does this) |
| Fork-promote / staging (RSI, mesh) | Most "scaling" claims |
| Independent runtime versioning | |
| Conceptual / authority alignment (entart = synent) | |
| Executable specifications co-located with state (loops, gates, recipes are atoms — fact 2) | |

Skeleton (deontic) is multi-Space but each Space's role is structural-authority, not throughput. Canonical probmesh is genuinely multi-Space (domains, hypothesis testing, PIM mapping). Local probmesh is per-teleonome plus fork-promote staging. When you propose a new Space, ask: which of the left-column wins does it actually deliver? If the answer is "none" — push back.

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

## 3. The five artifact types

The synome has five artifact tiers, each a **tree of Spaces** with
distinct replication and privacy properties. Each level *is* its art —
the substrate-correspondence is the identity, not a separable
association. A synome is just its synart; a Synomic Entity is just its
entart; a teleonome is just its telart in active operation; an
embodiment is just its embart on hardware; an agent is just its agart
being evaluated by a runtime.

### Synart — the canonical tree

| | |
|---|---|
| Tree shape | synome root layers (`&core.*`) + entart subtrees (`&entity.*`) per synomic entity |
| Replication | global — synserv → every participant (modulo selective sync) |
| Privacy | public; read access universal |
| Authority | governance writes via constructors; gate-mediated |
| Mutability | append-only / governance-revocable |
| Content | open-source SOTA: knowledge corpora, framework parameters, registries, loops, gates, recipes, runtime source, telseeds, published alpha, settlement aggregations |

Synart is "the commons brain." Every running participant pulls from it.
Detailed treatment in `../synodoxics/noemar-substrate.md` "Synart as commons brain".

### Entart — a synent's subtree of synart

| | |
|---|---|
| Tree shape | one root Space (`&entity.<type>.<id>.root`) plus sub-Spaces registered through `(sub-entart …)` and `(sub-space …)` atoms |
| Replication | inherits synart replication |
| Privacy | scoped via auth atoms — anyone can read, only authed identities can write |
| Authority | the synomic entity (Guardian / Prime / Halo) and parent-chain delegates |
| Content | identity, sub-entart and sub-Space registries, scope-local policies, cross-sub-entart rules, per-entity loop instances |

An entart is the structural unit of synart. The synart is the union of
all entarts plus the synome root's universal Spaces. See §5.

### Telart — per-teleonome private state

| | |
|---|---|
| Tree shape | telgate (instance of `&core.telgate`), alpha store, call-out services, strategy config, dreamart, experience archive, endowment record |
| Replication | within one tel's own emb fleet only |
| Privacy | private to that tel; no other tel sees it |
| Authority | the teleonome (and its identity) |
| Content | proprietary alpha, accumulated RSI lift, private data, dreamer output, founder bequest, telgate state |

Telart is "the teleonome's moat." Detailed treatment in `../synodoxics/noemar-substrate.md` "Telart as proprietary alpha".

### Embart — per-embodiment hardware-local state

| | |
|---|---|
| Tree shape | embgate state, per-loop execution Spaces, working-memory Space, isolated secrets (private keys), transient cycle state, speculative agarts |
| Replication | none — local to one embodiment |
| Privacy | private to that emb |
| Authority | the runtime process; the teleonome that owns this embodiment |
| Content | per-loop execution context, current cognitive scratchpad, draft proposals, transient working state, per-emb secrets that must NOT replicate, dreamer-generated speculative agarts under evaluation |

Embart is "hardware-local working state." It is also the only place
where per-emb-isolated state legitimately lives — private keys, hot-
wallet ephemeral state, anything where fleet-wide replication would be
a *bug*. Detailed treatment in `../synodoxics/noemar-substrate.md`
"Embart as hardware-local".

### Agart — per-agent subtree (the unit of agency)

| | |
|---|---|
| Tree shape | agart root Space (loop body or pointer to universal template, bindings, sub-space registry) plus sub-spaces for working memory, scratch, experience, cognitive sub-spaces, and convention-named I/O contract Spaces |
| Replication | inherits its host tier — agarts in telart replicate across the tel's fleet; agarts in embart are local only |
| Privacy | inherits its host tier |
| Authority | the agent's identity; ultimately the teleonome that owns it |
| Content | the active program: loop atoms, current bindings, accumulated experience, working state, output queues that Beacons consume from |

An agart is the structural unit of agency — the substrate of an
**agent** (a program in continuous evaluation).

### Constructor / instance pattern (agarts work like frameworks)

A telart-resident agart is a **constructor / template** (the spec the
tel keeps as part of its moat). To *run* it on a specific emb, the
runtime instantiates the constructor by copying it into that emb's
embart, where it becomes an **active mutable instance**. Each emb
running the same agart has its own embart instance; when the telart
constructor updates, embart instances reinstantiate.

```
&telart-{tel-id}-agart-{name}              ← constructor (template, immutable spec)
       │
       │  instantiate (copy + bind)
       ▼
&embart-{emb-id}-agart-{name}              ← instance (active, mutable, per-emb)
       │
       │  consolidation (selective lift back to constructor)
       ▼
   updated constructor in telart
```

This is structurally identical to other constructor/instance patterns
(class/object, gen_server module/process, container image/running
container, the two-step loop pattern §17 applied at the whole-agart
level).

### Lifecycle stages (where an agart lives)

| Stage | Tier | Mode | Notes |
|---|---|---|---|
| **Speculative** | embart only | one-off | Dreamer-generated, under evaluation, no telart constructor yet; promotes upward if it proves out, otherwise discarded |
| **Constructor** | telart | template | Proven; part of the tel's moat; replicates across the tel's emb fleet via telart spread |
| **Instance** | embart | active | Materialized copy of the constructor on a specific emb; the runtime evaluates this; mutable working state diverges from the constructor over time |
| **Crystallized** | synart (as Beacon Space or Data Space) | published | Output promoted to commons; **transforms in kind** (Agent Space → Beacon Space if it becomes a public protocol/recipe; Agent Space → Data Space if it's a corpus contribution); not a tier promotion alone but a *change of role* |

Speculative agarts have no telart constructor — they exist only in the
embart of the emb that's currently exploring them. Promoted, they
become telart constructors and then can be instantiated on any of the
tel's embs. See §3.5 for kind vs tier orthogonality.

### Authority hierarchy

The replication / privacy gradient also defines an authority hierarchy:

```
synart  >  entart  >  telart  >  embart  >  agart
(public, vetted)   (entity-scoped)   (private, alpha)   (local, transient)   (per-program)
```

Below agart is **off-synomic substrate** — runtime, OS, hardware,
electricity, network. Owned and managed by the teleonome that operates
the embodiment, but not modeled by the synome.

Crystallization promotes telart content into synart through a
peer-review-shaped publication gate. Embart content gets promoted
into telart through the tel's own internal review (typically dreamer
output → strategy adoption). The gradient runs from "what's true and
shared" down to "what one emb is doing right now."

---

## 3.5. Space kinds — Agent / Beacon / Data (orthogonal to tier)

Tier (synart / entart / telart / embart / agart) tells you about
replication, privacy, and authority. **Kind** tells you about the role
the Space plays in the cognition + comms substrate. The two are
orthogonal: a Data Space can live in any tier; an Agent Space lives in
agarts (in telart or embart); Beacon Spaces live only in synart.

| Kind | Role | Typical placement |
|---|---|---|
| **Beacon Space** | Regulated standardized comms aperture. Gates, beacon loops, recipes — the legible action surface. | synart only — comms must be public/auditable |
| **Agent Space** | Autonomous loop with NN-in-the-loop; pattern matching, RSI, risk reasoning; the seat of agency. Lives inside an agart. | telart (proven), embart (speculative). Never in synart — agency is private by design. |
| **Data Space** | Inert pattern-match environment; queryable atom set. Six sub-kinds match the synome-root layers. | All tiers — no kind/tier coupling. High-isolation Data Spaces (per-emb secrets) live in embart. |

**Note on naming:** *gates are programs, not beacons.* `&core.syngate`,
`&core.telgate`, and the per-tel "embgate" implementations are Beacon
Spaces holding gate *code* — libraries that beacons run. Synserv,
sentinels, and `relay-*` keepers are *beacons* (active processes) that
*use* the gate programs. The distinction matters because beacons are
the active regulated participants; gates are the protocol substrate
they go through.

### Six sub-kinds of Data Space

The synome-root layers (§6) are essentially the kinds of synart Data
Spaces by update mechanics:

| Sub-kind | Examples | Update profile |
|---|---|---|
| Constitutional | `&core.root`, `&core.telos`, `&core.skeleton`, `&core.governance`, `&core.protocol` | ~never; governance flag-day |
| Framework | `&core.framework.*` — universal parameterized shapes | Governance-paced; scatter-gather projection on update |
| Registry | `&core.registry.*` — flat identity indexes | Push/pull onboarding |
| Aggregation | `&core.settlement`, `&core.escalation` — synserv-only-write outputs | Synserv writes at boundaries or as events arrive |
| Library | `&core.library.*` — large slow-changing knowledge content | Slow; large content |
| Operational | Per-entity entart leaves (book Spaces, real-time event streams) | High-frequency atom writes during operation |

### Why Beacon Spaces are synart-only

The legibility principle: action surface must be public, auditable,
re-derivable by Wardens. Beacon Spaces are the regulated apertures
through which agents reach the world; their content (loop bodies, gate
code, recipe bundles) must be visible to all participants.

### Why Agent Spaces are telart/embart only

The privacy principle: cognition is private by design. Agent Spaces
hold proprietary alpha, RSI lift, dreamer outputs, calibration
patterns. If they were in synart, they'd be replicated everywhere and
the moat would dissolve. They live in agarts within telart (proven) or
embart (speculative).

When telart-resident agart content gets crystallized into synart, it
**changes kind**: Agent Space → Beacon Space (if it becomes a regulated
protocol/recipe other tels can run) or Agent Space → Data Space (if
it's a knowledge corpus contribution). The crystallization is a
transformation of role, not a privacy violation — the agent's *output*
becomes public; the cognition that produced it stays private.

### Agent ↔ Beacon comms via convention-named embart Spaces

The dominant pattern for Agent ↔ Beacon communication is **a
convention-named Space in embart**, not synchronous call-out. The
Beacon Space's published I/O contract specifies a Space name in embart
(typically a function of class + booting identity) and a content
schema. The Agent populates that Space at its own cadence; the Beacon
reads it on each tick. Async, batched, decoupled in time. The
synchronous `(call-out …)` primitive remains for genuinely-need-an-
answer-now cases, but the mailbox-via-embart pattern handles most
real Agent ↔ Beacon flow.

Each Warden running the same Beacon for the same entity has its own
embart populated by its own Agent — that's what produces the
divergence signal at the Beacon-output level (synart) when proposals
disagree past tolerance.

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

A **synomic entity** (synent) is one of the entity types that constitutes
the synome: Guardian, Prime, Halo. Every synent owns an **entart** — its
slice of the synart, structured as a subtree of Spaces rooted at one
**root Space**.

The synart is the union of all entarts plus the synome root's universal
`&core.*` Spaces. Every non-universal Space belongs to exactly one
entart's subtree. Universal Spaces (`&core.*`) are owned by the
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
(sub-entart spark-prime spark-term-halo  &entity.halo.spark-term.root)
(sub-entart spark-prime spark-trade-halo &entity.halo.spark-trade.root)

;; leaf Space registry (directly attached, no further nesting)
(sub-space spark-prime &entity.prime.spark.config)

;; per-entity loop instances (Phase 9-10+)
(sub-space spark-prime &entity.prime.spark.relay.baseline)
(sub-space spark-prime &entity.prime.spark.sentinel.stream)
(sub-space spark-prime &entity.prime.spark.relay.warden)

;; auth grants for this entity's scope
(auth nfat-spark issue-unit …)

;; policies — local values within bounds set by &core.framework.risk
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
can add stricter rules but never weaken parent rules. `&core.skeleton`
sets invariants no one weakens; `&core.framework.risk` sets bounds that
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
| `&core.root` | Synome root entart's root Space; sub-entart and sub-space registries | governance-paced |
| `&core.telos` | Apex axiom — what the system is for | constitutional (~never) |
| `&core.skeleton` | Constitutional axioms, types, invariants | constitutional rewrite |
| `&core.governance` | Core Council legislative chamber, including the bootstrap seed (`role-def root-authority`, `role-grant core-council`) as initial state | governance-paced |
| `&core.protocol` | Chain protocol specifications — contract addresses, ABIs, event signatures, the canonical "what to look for on chain" reference for endoscrapers and verifiers | governance-paced |

`&core.protocol` is sibling-of-`&core.skeleton` in role: skeleton tells
us what must be true about ledger state; protocol tells us how to *read*
ledger state. Both rarely change, both universally replicated.

### Framework layer

Universal shapes + parameter bounds. Each entart gets its own values
constrained by the framework via layered tightening. Updates project
out via scatter-gather.

| Space | Contents |
|---|---|
| `&core.framework.risk` | ER formula, covenant arithmetic, loop/depth/repeat heuristic parameters |
| `&core.framework.risk.forms` | Catalog of risk forms at three levels (exo asset / exobook / riskbook); each form carries a parameterized stress-simulation equation. See `risk-framework.md` §3-§4. |
| `&core.framework.risk.scenarios` | Library of stress scenarios used by risk-form equations (severe-correlated-crash, credit-crisis, etc.); see `risk-framework.md` §6 |
| `&core.framework.risk.concentration` | Concentration categories + global limits (deferred); see `risk-framework.md` §13 |
| `&core.framework.distribution` | Distribution rewards rate shapes |
| `&core.framework.fee` | Entity upkeep (50 bps/yr — see [`../accounting/entity-fees.md`](../accounting/entity-fees.md)), protocol fees, fee shapes, recipe pricing levers |

### Registry layer

Flat identity indexes for things whose actual state lives elsewhere
(external processes, on chain, or in entart subtrees). Push/pull
onboarding (proposed → accepted). Authority comes from cert/auth atoms
elsewhere, not from registration.

| Space | Contents |
|---|---|
| `&core.registry.entity` | All entarts (denormalized index for discovery; tree is canonical) |
| `&core.registry.beacon` | All beacons + tels (operators are external; pubkey + status + class + loop pointer here — see `boot-model.md` §4) |
| `&core.registry.contract` | All on-chain contracts (state lives on chain; thin reference layer) |
| `&core.registry.exo-book` | All monitored exo books — external structures the synome reads but doesn't control (Morpho markets, custody accounts, real-world claims). Populated by external endoscrapers. See `risk-framework.md` §3. |

### Aggregation layer

Where Phase-2 scatter-gather outputs land. Each entart computes locally;
synserv aggregates into these Spaces. Also where the verification
inflow stages.

| Space | Contents |
|---|---|
| `&core.settlement` | Sky-wide financial aggregation (penalties owed, distributions, fees, settlement totals) |
| `&core.escalation` | Disputes, slashing reports, contested operations, verification disagreements |

(There is no `&core.endoscrapers` Space. Endoscraper is a grounded
runtime primitive — `(chain-read $contract $slot)` style — accessible
from any rule in any Space, returning current Ethereum mainnet state.
Per-protocol metadata lives in `&core.protocol`. See "Endoscraper as
grounded primitive" below.)

### Executable layer

The synome's continuous machinery — gates that mediate ingress, loops
that run roles, recipes that bundle loops with economics. **This is
where the synome's program lives.**

```
Gates (programs, not beacons — beacons USE these):
  &core.syngate                     — synserv's gate (synserv runs the canonical instance)
  &core.telgate                     — universal telgate spec (every tel runs an instance with
                                       state in their telart)
  (no &core.embgate)                — see standardization gradient below

Loops (universal templates):
  &core.loop.synserv                — synserv heartbeat
  &core.loop.relay.<stem>           — deterministic action: baseline / warden / nfat / lcts / amm / ...
  &core.loop.market-data            — market-data-beacon class (off-chain price/liquidity/funding feeds)
  &core.loop.attest-data            — attest-data-beacon class (signed off-chain claims)
  &core.loop.archive                — full event capture
  &core.loop.verifier               — generic re-derivation

  (No &core.loop.sentinel.* — sentinel loops live in the entart of the
   entity they operate on, because the strategy is per-operator and
   carries cognitive call-outs into operator telart. See sentinel/.)

  (No &core.loop.endoscraper.* — endoscraper is a grounded primitive,
   not a class with a loop. Any rule that needs chain state calls
   `(chain-read …)` directly against `&core.protocol` metadata.)

  (No &core.loop.patch — patch-beacons are Guardian-sudoed scaffolds
   with no universal template; per-instance loop body + config sudoed
   inline into the target Space.)

Recipes (loops bundled with economics — see ../synoteleonomics/recipe-marketplace.md):
  &core.recipe.* (loop body + payment terms + slashing + auth requirements)
```

Universal templates in this layer; per-entity instances live in entarts
(see §17). Identity boots an emb against either a universal template
(generic role) or a per-entity instance (specialized role).

#### Standardization gradient: syngate → telgate → embgate

The three gate primitives sit on a deliberate gradient — visibility is
the inverse of standardization at every tier:

| Gate | Used between | Standardization |
|---|---|---|
| **syngate** (`&core.syngate`) | external participants ↔ synserv | **Maximally standardized** — one canonical spec, one canonical synserv. Federation requires it; auditability requires it; public regulated surface. |
| **telgate** (`&core.telgate` spec; per-tel instance) | tel ↔ tel; tel ↔ synomic public layer | **Standard spec, per-tel deployment.** Inter-tel coordination needs a common protocol, but each tel runs its own instance with its own keys, peers, rate-limit posture. |
| **embgate** (per-tel implementation, no canonical spec) | a tel's emb ↔ another of the same tel's embs | **Deliberately non-standard.** Pure opsec — the tel's internal coordination layer; tels are *expected* to diverge from any reference (TOR-like onion routing, custom encryption, mix networks, decoy traffic, steganographic tunnels). A reference embgate may ship in `&core.library.runtime.*` for tels with weak opsec needs, but a serious tel treats it as a starting floor, not a ceiling. |

The synomic vocabulary stops at the embgate boundary. The synome can
mandate that **inputs/outputs at the embgate boundary** conform to
schemas (a Beacon Space can demand certain content in its embart shared
Space — see §3.5), but it cannot mandate the *transport* that delivers
the content there. That transport is the tel's expense and the tel's
defensive moat.

#### Endoscraper as grounded primitive (in scope)

Endoscraper reads **internal protocol smart contract state** on
**public blockchains** — fully deterministic, publicly auditable, no
insurance overhead. It is a **grounded runtime primitive**, not a
beacon class: any rule in any Space can call `(chain-read …)` (or
equivalent) and get current mainnet state. Per-protocol metadata
(contract addresses, ABIs, event signatures) lives in `&core.protocol`;
the primitive consumes that metadata when called.

Because endoscraper is grounded, there is no staging Space, no
per-protocol loop, no separate beacon registry entry. Wardens
re-deriving sentinel/relay decisions call the same primitive — the
"second source" is the runtime guarantee, not a separately-operated
beacon.

#### Exoscraper (out of scope, term reserved)

Exoscrapers would read **external APIs, proprietary feeds, off-chain
services** — uncertain provenance, requires governance review,
fallback, dispute resolution. Different trust model than the chain-read
primitive. Exoscraper design is deferred.

#### Verification under grounded endoscraper

Because endoscraper is a primitive that any rule can call, verification
no longer requires a separately-operated scraper. The pattern:

```
1. Sentinel/relay decides to act (e.g., sell NFAT-X)
2. Action beacon (relay) executes on-chain transaction
3. Decision writes to synart: tx hash + state delta + justification pointer
4. Warden re-derives the decision by calling `(chain-read …)` against
   the same `&core.protocol` references, applying the same synart code
5. Disagreement → &core.escalation; agreement → settle
```

The runtime guarantees deterministic chain reads; any warden calling
the primitive gets the same answer. The verification source is the
primitive itself, not a peer scraper.

This is the operational form of "synserv verifies what beacons report."

### Library layer

The synome's commons content — the open-source substrate that every
participant can pull from.

| Sub-pattern | Contents |
|---|---|
| `&core.library.runtime.<impl>` | Atomspace runtime source (Noemar et al.); versioned, hash-addressed, signed |
| `&core.library.telseed.<config>` | Telseed catalog — vetted starting configurations for new tels |
| `&core.library.corpus.<domain>` | Knowledge corpora (financial, scientific, technical, governance) |
| `&core.library.published.<topic>` | Crystallized alpha promoted from telart through the publication gate |

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
shape (CRR formula, ER arithmetic, covenant bounds)  →  &core.framework.*
                                                          │
                                                          │ scatter-gather projection
                                                          ▼
per-entart values (Spark's covenant=90, Grove's=85)  →  each &entity.*.root
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
identity row in &core.registry.*
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
&core.settlement / &core.escalation
```

- Scatter-gather collection at synserv
- Settlement-paced, event-paced, or stream-paced writes
- Read by everyone, written only by synserv aggregator
- "Single source of truth" for Sky-wide totals or processed inflow

### Specifications (executable code, replicated)

```
loop / gate / recipe atoms  →  &core.loop.* / &core.syngate / &core.telgate / &core.recipe.*
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
economic engine that funds it lives in `../synoteleonomics/recipe-marketplace.md`.

### The five levels of self-reference

The synart's self-hosting properties stack into five levels. **This section is the canonical home for the enumeration**; other docs reference here.

1. **Self-hosting** — synart contains the loops that run synart. The synserv loop is in `&core.loop.synserv`; deterministic action loops in `&core.loop.relay.<stem>`; input-class loops in `&core.loop.market-data` and `&core.loop.attest-data`; archive/verifier loops in `&core.loop.archive` / `&core.loop.verifier`. Sentinel loops live in the entart of the entity they operate on (per-operator strategy with call-outs into operator telart); patch-beacon loops are sudoed inline at their target Space; endoscraper is a grounded primitive with no loop. Identity-driven boot picks them all up.
2. **Self-regulating** — synart contains the gates that regulate synart access. `&core.syngate` is the synserv's gate; `&core.telgate` is the universal spec each tel runs an instance of. The trust boundary is itself synart code.
3. **Self-paying** — synart contains the recipes that fund work on synart. Recipes (loops bundled with `&core.framework.fee` economics and auth requirements) are the standardized products; teleonomes earn carry by running them. The marketplace that pays for participation is part of the substrate participants run on. Canonical recipe-marketplace treatment: [`../synoteleonomics/recipe-marketplace.md`](../synoteleonomics/recipe-marketplace.md).
4. **Self-seeding** — synart contains the telseeds that birth new teleonomes (`&core.library.telseed.*`). New tels boot against synart and grow from there. The reproductive material is in the substrate.
5. **Self-improving** — synart contains the runtime source itself (`&core.library.runtime.noemar` and alt impls; version atoms inside). Recipe revenue funds substrate research; substrate research lands back in synart; next-generation tels start from improved foundations. **The synome funds its own substrate research with the value it captures from substrate use.**

This is structurally tighter than open-source models (where development is funded externally) or smart-contract platforms (where contracts run on chains the contracts didn't fund). The marketplace running on the substrate pays for the substrate's improvement; you can't fork the development engine without forking the productive economy.

Every level rests on the executable + library layers of the synome root being load-bearing. A topology that puts loops outside synart, or runtime source outside synart, can't achieve any of these levels. For the boot mechanics enabling level 1: [`boot-model.md`](boot-model.md). For the artifact tiers (synart/telart/embart): [`../synodoxics/noemar-substrate.md`](../synodoxics/noemar-substrate.md).

### The spec/instance collapse

In typical software architectures, code and running instances are
separate: you install the program, then run instances. In the synome:

- Code is in `&core.loop.*` (universal templates) and `&entity.*-<sub-kind>` (per-entity instances)
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
look up X in &core.registry.beacon → loop pointer
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
`&core.recipe.*` adjacent to it). The economics atoms attached to a
recipe live in the framework layer (`&core.framework.fee`). The catalog
itself — which recipes exist, in what state — is governance-curated
content in `&core.governance`.

Canonical economic treatment is `../synoteleonomics/recipe-marketplace.md`. Topology's role
is just to host the structures.

---

## 9. The naming convention

### Delimiters

```
.     hierarchy boundary (one segment to the next)
-     compound word within a single segment
```

`.` separates levels; `-` joins multi-word names that belong to one
level. The convention forces the writer to decide whether a name is a
real sub-hierarchy or a compound phrase — they look different and parse
unambiguously.

### Space patterns

```
&core.<kind>[.<topic>...]                                  // synome-level
&entity.<type>.<id>[.<sub-kind>[.<sub-id>]]                // entart-level
&self                                                       // portable reference in two-step rule templates
```

Sigil `&` marks every Space reference. Non-Space identifiers (beacons,
verbs) are dash-separated, no sigil — visually distinct.

### Reserved keyword vocabulary

| Slot | Values |
|---|---|
| `core.<kind>` | `root`, `telos`, `skeleton`, `governance`, `protocol`, `framework`, `registry`, `settlement`, `escalation`, `syngate`, `telgate`, `loop`, `recipe`, `library` |
| `core.framework.<topic>` | `risk` (umbrella), `risk.forms`, `risk.scenarios`, `risk.asset-profiles`, `risk.concentration`, `fee`, `distribution`, `currency-stress` |
| `core.loop.<class>` | `synserv`, `relay.<stem>`, `market-data`, `attest-data`, `archive`, `verifier` (no `endoscraper` — that's a grounded primitive; no `sentinel` — sentinels live in entarts) |
| `core.library.<sub-type>.<impl>` | `runtime.<impl>`, `telseed.<config>`, `corpus.<domain>`, `published.<topic>` |
| `entity.<type>` | `guardian`, `generator`, `prime`, `halo`, `oracle`, `folio`, `core`, `sequencer`, `pylon` (extensible) |
| `entity.<...>.<sub-kind>` | `root`, `primebook`, `halobook`, `riskbook`, `exobook`, `genbook`, `structural-demand` (compound), `auction`, `structbook`, `tradingbook`, `termbook`, `ascbook`, `hedgebook`, `config`, `sentinel` (the in-entart sentinel binding Space) |

Sub-ids of book types nest as their own level: `&entity.halo.spark-term.book.A1` (where `A1` is the book id under sub-kind `book`).

### Versions

Versions do **not** appear in Space names. A runtime impl Space is
`&core.library.runtime.noemar`; its version is an atom inside:
`(runtime-version noemar 0.1.0)`. Same for telseeds, corpora, etc.

### Compound ids

Multi-word entity ids stay one segment with internal hyphens:

| Type | Compound id examples |
|---|---|
| Halo | `spark-term`, `spark-trade`, `spark-credit` |
| Oracle | `crypto-majors`, `book-attestation` |
| Generator | `usge` |
| Guardian | `ozone` |

So `&entity.halo.spark-term.root` — `spark-term` is one segment, the
hyphen is compound joiner.

### Examples (canonical)

Synome-level:

```
&core.root
&core.telos
&core.skeleton
&core.governance
&core.protocol
&core.framework.risk                          umbrella — ER formula, heuristic params
&core.framework.risk.forms               catalog
&core.framework.risk.scenarios                stress scenarios library
&core.framework.risk.asset-profiles           per-asset risk-type CRR inputs
&core.framework.risk.concentration            concentration categories + caps
&core.framework.currency-stress               per-currency depeg / FX profiles
&core.framework.fee
&core.framework.distribution
&core.registry.entity
&core.registry.beacon
&core.registry.contract
&core.registry.exo-book
&core.registry.currency
&core.registry.halo-class
&core.settlement
&core.escalation
&core.syngate
&core.telgate
&core.loop.synserv
&core.loop.relay.baseline                     universal relay template per stem
&core.loop.relay.warden
&core.loop.relay.nfat
&core.loop.relay.lcts
&core.loop.market-data                        universal market-data template
&core.loop.attest-data                        universal attest-data template
&core.library.runtime.noemar
&core.library.telseed.research
&core.library.corpus.financial
```

Entart-level:

```
&entity.guardian.ozone.root                   Ozone — single operational guardian
&entity.generator.usge.root                   USDS Generator entart root
&entity.generator.usge.genbook                Genbook — Primeunits in, USDS out
&entity.generator.usge.structural-demand      lot-age surface + effective SDR bucket capacity
&entity.generator.usge.sdr-auction            SDR allocation atoms / auction body
&entity.oracle.crypto-majors.root             Crypto Majors Oracle entart root
&entity.oracle.book-attestation.root          Book Attestation Oracle entart root
&entity.prime.spark.root                      Spark Prime's entart root
&entity.prime.spark.primebook                 Spark's Primebook
&entity.prime.spark.structbook                Spark's structbook sub-book
&entity.prime.spark.config                    config sub-Space
&entity.halo.spark-term.root                  Spark-Term Halo (spark-term is compound id)
&entity.halo.spark-term.halobook
&entity.halo.spark-term.book.A1               sub-id A1 as deeper level under sub-kind book
&entity.halo.spark-trade.root
&entity.halo.spark-trade.book.amm-001
```

### Naming is decoupled from tree topology

The Space name encodes the entity id + sub-kind, not the parent chain.
A Space named `&entity.halo.spark-term.book.A1` is registered under
`&entity.halo.spark-term.root` via
`(sub-space spark-term &entity.halo.spark-term.book.A1)`. The name
tells you which entity owns it; the registry tells you the structural
relationship.

This means a Space can move to a different parent during a
reorganization without changing its name.

### Beacon identifier naming

Beacons are not Spaces. Their identifiers use dash-only, no dots, no
sigil:

```
<stem>-<owner>[-<disambiguator>]
```

- `<stem>` describes work role (`baseline`, `warden`, `nfat`, `lcts`, `amm`, `market-data`, `attest-data`, `patch`, `govops`)
- `<owner>` is the entity id the beacon operates for (`spark`, `usge`, `crypto-majors`)
- Optional `<disambiguator>` (provider, sub-strategy)

Visual rule: **dots and `&` = Space**; **dashes only, no sigil = beacon
or verb**. Class is registry metadata, not part of the name; multiple
stems can share one class (all `baseline-`, `warden-`, `nfat-`, `lcts-`,
`amm-` stems are class `relay`).

For the canonical beacon-class taxonomy and per-class registry
mechanics, see [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md).

---

## 10. Operators and beacons are external

A **beacon** is an external process — running on an embodiment somewhere
with a private key. It interacts with the synart only via gate-mediated
submissions. There's no internal "beacon state" inside synart, only
*facts about the beacon*.

**Beacons aren't entarts.** Facts about beacons live where they're used:

| Fact about beacon | Lives in | Why |
|---|---|---|
| Pubkey + status + class + loop pointer | `&core.registry.beacon` | needed at the gate for sig verification + at boot for loop resolution, globally |
| `(cert beacon-X by-ozone)` | `&entity.guardian.ozone.root` | guardian holds underwriting liability |
| `(auth beacon-X verb target)` | entart owning the target | target's owner controls auth |
| Submission history | wherever it wrote | provenance follows writes |

There's no place where you'd say "this is the beacon's stuff"
cohesively. Entarts are for synomic *entities* (Guardian, Prime, Halo) —
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

- **Entart owners** = synomic entities (structural units)
- **Operators** = external entities running embodiments (humans, companies, teleonomes)
- **Beacons** = the connective tissue between them

See `../synodoxics/noemar-substrate.md` for full treatment of how teleonomes' telart and
embart trees relate to the synart they participate in.

### Push/pull beacon registration

```
1. Push: beacon proposes itself
   (beacon-pending beacon-X (pubkey "ab9c…") (operator soter-govops) (class relay))

2. Pull: governance accepts
   (beacon-accepted beacon-X)
   (beacon-status beacon-X active)

3. Cert: rooted in the Guardian's entart
   ;; in &entity.guardian.ozone.root
   (cert beacon-X by-ozone)

4. Auth: granted in entarts whose parent chain includes Ozone
   ;; in &entity.prime.spark.root or further down
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
&core.root
  │
  └── &entity.guardian.ozone.root                    Ozone — single operational guardian;
        │                                            vote outcomes; cert-atoms for all
        │                                            GovOps teams' beacons
        │
        ├── &entity.generator.usge.root              USDS Generator entart root
        │     ├── &entity.generator.usge.genbook     Genbook — holds Primeunits, issues USDS
        │     ├── &entity.generator.usge.structural-demand
        │     └── &entity.generator.usge.sdr-auction
        │
        ├── &entity.prime.spark.root                 Prime auth, policies, halo registry, cross-halo rules
        │     │
        │     ├── &entity.prime.spark.primebook      Prime's aggregation book; holds Halobook units; issues to Genbook
        │     │
        │     ├── &entity.prime.spark.relay.baseline    per-Prime operating setup
        │     ├── &entity.prime.spark.sentinel.stream       (each holds entity-specific config +
        │     ├── &entity.prime.spark.relay.warden        reference to universal loop template)
        │     │
        │     ├── &entity.halo.spark-term.root             halo policies, registry of riskbooks
        │     │     ├── &entity.halo.spark-term.halobook   Halo's aggregation book; holds Riskbook units; issues to Primebook
        │     │     ├── &entity.halo.spark-term.riskbook.A Riskbook (matches a registered risk form, e.g. abf-with-cds-cover)
        │     │     ├── &entity.halo.spark-term.riskbook.B Riskbook (matches a different risk form, e.g. morpho-lending)
        │     │     └── &entity.halo.spark-term.riskbook.C Riskbook (yet another risk form)
        │     │
        │     └── &entity.halo.spark-trade.root
        │           ├── &entity.halo.spark-trade.halobook
        │           └── &entity.halo.spark-trade.riskbook.D
        │
        ├── &entity.prime.grove.root                 Star Prime — similar structure to Spark
        ├── &entity.prime.keel.root                  Star Prime — similar structure to Spark
        └── &entity.prime.obex.root                  Institutional Prime — similar structure
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
separation from `runtime.md` §4 holds — only the
Guardian count is collapsed to one.

Operationally, the grounded **endoscraper primitive** is available to
any rule in any Space — synserv, wardens, sentinels, govops relays all
call `(chain-read …)` against `&core.protocol` metadata to fetch
current Ethereum mainnet state. There's no per-Prime "endoscraper
beacon" running in synserv; chain state is a runtime guarantee, not a
staged Space. Wardens that re-derive Spark's claims call the primitive
themselves and verify against the same `&core.protocol` references.
See §6 ("Endoscraper as grounded primitive").

---

## 12. The registry pattern

Inside an entart root, registry atoms name what's underneath:

```metta
;; in &entity.prime.spark.root
(sub-entart spark-prime spark-term-halo  &entity.halo.spark-term.root)
(sub-entart spark-prime spark-trade-halo &entity.halo.spark-trade.root)
(sub-space  spark-prime &entity.prime.spark.relay.baseline)
(sub-space  spark-prime &entity.prime.spark.sentinel.stream)
(sub-space  spark-prime &entity.prime.spark.relay.warden)

;; in &entity.halo.spark-term.root
(sub-space spark-term-halo &entity.halo.spark-term.book.usds)
(sub-space spark-term-halo &entity.halo.spark-term.book.cnys)
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
| Universal Spaces (`&core.*`) | always readable | replicated everywhere |

If a rule needs cross-sibling context (a rule about both Spark Term and
Spark Trade Halos), it lives at their common ancestor
(`&entity.prime.spark.root`). Sub-entarts stay flat and replicable in
isolation; only the common ancestor knows about both.

---

## 14. Each Space is locally consistent

Design each Space so it's **internally complete** for some purpose:

- `&entity.halo.spark-term.book.usds` — locally consistent for USDS-book reasoning
- `&entity.prime.spark.root` — locally consistent for Spark policy/authority
- `&entity.prime.spark.relay.baseline` — locally consistent for running Spark's Baseline (config + reference)
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
;; lives in &entity.prime.spark.root — the local rule body
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
| Universal template | `&core.loop.<class>` | portable loop body using `&self`; canonical, audited |
| Per-entity instance | `&entity.<type>.<id>.<sub-kind>` | entity-specific config + binding context for the template |

### Example — Relay-Baseline for Spark

Baseline is a deterministic relay: it reads synart-resolved strategy
state and emits PAU txs. No call-outs into local cognition — the
strategy is fully verifiable from synart inputs. (A sentinel feeding
intent into this baseline would live separately, in Spark's entart
under `sentinel.<actor>`, with cognitive call-outs into operator
telart.)

```metta
;; ── Universal template in &core.loop.relay.baseline ────────────
(= (run-forever)
   (let* (($_ (heartbeat))
          ($_ (delay (current-interval))))
     (run-forever)))

(= (heartbeat)
   (let* (($entity      (match &self (entity-bound-to $e) $e))
          ($chain-state  (chain-read (target-pau $entity)))    ; grounded primitive
          ($strategy    (match &self (strategy-id $s) $s))
          ($candidate   (compute-rebalance $chain-state $strategy))
          ($safe? (within-baseline-envelope $candidate $entity)))
     (case $safe?
       ((True (gate-out (sign-and-emit $candidate)))
        (False (audit-rejected $candidate))))))

;; ── Per-Prime instance in &entity.prime.spark.relay.baseline ───
(entity-bound-to spark-prime)
(strategy-id     spark-baseline-strategy-v3)
(current-interval 30s)
(target-halos    spark-term spark-trade)
(rar-threshold   0.05)
(import-loop     &core.loop.relay.baseline)
```

### Why this works

The synome can preconfigure each entity's loop Spaces because the
entity's structure is **fully described in synart**. The loop doesn't
do dynamic config-lookup at runtime; the config is baked into the
entity Space at the moment the entity is fully described.

When an emb boots "as Spark Prime's Baseline sentinel," it boots with
`&entity.prime.spark.relay.baseline` as `&self`. The loop body
imported from the universal template runs in that context. Same code,
different entity bindings.

### Properties that fall out

- **Cleaner audit trail.** Reading `&entity.prime.spark.relay.baseline`
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

### The loop taxonomy

Embodiments are configured by which loops they activate. Each loop owns a **workspace Space** in embart — the operational tier in concrete form (per the four-tier knowledge view in [`../synodoxics/noemar-substrate.md`](../synodoxics/noemar-substrate.md)).

| Loop | Activates | Args | Workspace contents |
|---|---|---|---|
| `synserv` | synome heartbeat, sequencer, write acceptance, replication out | governance-replica? | gate-in queue, replication cursor |
| `relay.<stem>` | deterministic action: emit chain txs or freeze BEAMs from synart state | per-entity config Space (e.g. `&entity.prime.spark.relay.baseline`) | chain obs via grounded primitive, decision state |
| `market-data` | push off-chain price/liquidity/funding ticks to oracle entart | per-provider config | latest tick batches |
| `attest-data` | push signed riskbook attestations (one per riskbook, covering its exobooks) | per-class config | pending claims |
| `archive` | full event capture | scope, retention | full historical event log |
| `verifier` | re-derive + flag discrepancies | scope, cadence | mirrored events, challenge drafts |
| `dreamer` | evolutionary simulation in dreamart | population size, fitness fn | candidate strategies, simulated worlds |
| `sentinel.<variant>` | cognitive action class — stream proposes intent within bounds, principal-sentinel directly operates a folio | per-entity sentinel Space in entart + telart agart for cognition | local cognition state + call-out provenance |

All loop bodies are synart-resolved Spaces. The taxonomy above shows which loops an embodiment activates (which identity it boots as / which class it registered for); it does **not** show where the loop code lives. Code is universal in `&core.loop.*` (and per-entity instances in entarts for entity-bound loops); embart holds only execution context per running loop. Loops compose on one embodiment — same runtime, different activations. Workspaces are the operational-tier Spaces — private, ephemeral, never gated.

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
replicated Spaces (`&core.*`). Anything that needs another partition
isn't local — it's a coordinator, and lives at the parent entart root.

---

## 19. The full Phase 1 commitment list

Original seven from `runtime.md`:

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
    convention. Operators and beacons are external; only synomic entities
    own entarts.

Added by self-hosting:

13. **Loops, gates, and recipes are first-class synart content.**
    Universal templates live in the executable synome-root layer
    (`&core.loop.*`, `&core.syngate`, `&core.telgate`, `&core.recipe.*`);
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
| Beacon lifecycle (cert / auth / revoke / status transitions) | `&core.registry.beacon` + per-Guardian cert atoms | Old demo uses direct `space.add`; no constructor |
| Entity construction (Directive + Axioms + Resources = Entity) | synart | Not started |
| Accordancy edges between synents | per-entart roots | Old demo uses `(administers …)`; canonical pattern is parent-entart links + `(auth …)` per `settlement-cycle-example.md` |
| Governance proposals (vote / ratify / enact) | `&core.governance` | Not started |
| State machines | per-entart leaf Spaces | Old demo covers Book lifecycle; broader pattern abstractable |
| Attestation gates / two-beacon patterns | per-entart leaf Spaces | Old demo covers single-actor; multi-beacon split not built |
| Crystallization commits (mesh → skeleton promotion) | `&core.library.published.*` → `&core.skeleton` | Not started |
| Rate limits & enforcement caps | per-entart roots | Not started |
| Cross-entart atomic writes | multi-Space within one synserv | Conventions defined, not exercised |
| Revocation cascades (Guardian collapse → propagation) | down-tree from `&entity.guardian.*.root` | Not started |
| Relay class (baseline / warden / nfat / lcts / amm / ...) | `&core.loop.relay.<stem>` + per-entity Spaces in entarts | Templates documented in `synlang-patterns.md`; P1 govops relays manually controlled |
| Sentinel class (stream / principal-sentinel) | Per-entity sentinel Space in entart (e.g. `&entity.prime.<id>.sentinel.<actor>`) + call-outs into operator telart | Forward-looking; not in P1 scope |
| Recipe marketplace catalog | `&core.loop.*` + `&core.recipe.*` + `&core.framework.fee` | Concept documented in `../synoteleonomics/recipe-marketplace.md`; minimal recipes only in Phase 1 |
| Risk framework (four-book taxonomy + categories + stress simulation) | `&core.framework.risk.*` + `&core.registry.exo-book` + per-entart books | Documented in `risk-framework.md`; concentration L3 (Halobook/Primebook category constraints) design deferred |
| Stress scenario library | `&core.framework.risk.scenarios` | Concept in `risk-framework.md` §6; library not populated |
| Riskbook risk-form catalog | `&core.framework.risk.forms` (riskbook level) | Concept in `risk-framework.md` §4; catalog not populated; default-deny CRR 100% means risk-form catalog completeness is governance priority |
| Exo book registry | `&core.registry.exo-book` populated by govops/attestor flows | Pattern documented; per-protocol detail in `&core.protocol` |
| Endoscraper (grounded primitive) | `&core.protocol` metadata + `(chain-read …)` runtime primitive | Conceptual treatment pending (see clean-todo); P1 has Phase-1 stand-ins sudoed inline |
| Telseed catalog | `&core.library.telseed.*` | Concept documented in `../synodoxics/noemar-substrate.md` "Telseeds and Bootstrap"; no live catalog yet |
| Atomspace runtime conformance | `&core.library.runtime.*` + governance test atoms | Conformance suite not built |

Each row is a candidate for its own focused design pass.
