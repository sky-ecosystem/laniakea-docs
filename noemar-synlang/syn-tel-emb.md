# Synart, Telart, Embart — Telseeds, Noemar, and the Alpha Stack

The three-tier artifact structure of the synome: synart as the open-source
commons brain, telart as a teleonome's proprietary alpha, embart as the
hardware-local working state. Plus the practical mechanisms — telseeds,
atomspace runtimes, the recipe marketplace — that knit the tiers into a
self-funding cognitive economy.

Companion to `topology.md` (structural reference), `syn-overview.md`
(concept map), `boot-model.md` (identity-driven boot), and
`telseed-bootstrap-example.md` (worked bootstrap trace).

---

## TL;DR

The whole architecture in one table:

| Tier | Replication | Privacy | Economic role | Content type |
|---|---|---|---|---|
| **Synart** | global (synserv → all participants) | public | the commons brain; baseline floor | open-source SOTA: knowledge, rules, loops, gates, recipes, runtime source, telseeds, published alpha |
| **Telart** | within one tel's own emb fleet | private to that tel | the teleonome's moat | proprietary alpha, accumulated RSI lift, private data, dreamer output, founder's endowment, telgate instance state, call-out services |
| **Embart** | one embodiment only | private to that emb | hardware-local working state | per-loop execution Spaces, current cognitive context, recent observations, draft proposals, transient cycle state |

The headline:

> A teleonome's economic position is its **delta** from synart. Synart is
> what everyone has. Telart is what *this tel* has built on top of it.
> Embart is what *this emb* is doing right now.

Each tier is a **tree of Spaces**, not a single Space:

- **Synart tree:** synome root layers (`&core-*`) + entart subtrees
  (`&entity-*`) per synomic agent.
- **Telart tree:** a telgate (running the universal `&core-telgate` spec
  with this tel's instance state), an alpha store, per-call-out service
  Spaces, dreamart, accumulated-experience archives.
- **Embart tree:** one execution Space per running loop, plus a working-
  memory Space, plus transient cycle state.

This document is the canonical home for the recipe marketplace concept
(§8). Other docs cross-reference here.

---

## Section map

| § | Topic | Core idea |
|---|---|---|
| 1 | Synart as commons brain | Open-source SOTA in machine-readable form; the baseline floor |
| 2 | Telart as proprietary alpha | The teleonome's moat; private replication across own embs |
| 3 | Embart as hardware-local | Per-emb execution context; locality of reference |
| 4 | Telseeds — minimal, not packaged | Bootstrap config, not a knowledge corpus |
| 5 | The bootstrap arc | From boot to running multi-emb tel |
| 6 | Noemar and atomspace runtimes | One of many implementations; runtime source in synart |
| 7 | Resilience model | Telart spread; three-pillars mapping |
| 8 | The recipe marketplace | *Canonical treatment* — synart as regulated marketplace |
| 9 | Alignment implications | Commons gravity; rogues still need synart |
| 10 | One-line summary | Whole structure compressed |

---

## 1. Synart as commons brain

The synart is the canonical, replicated part of the synome. It's tempting
to call it "the data substrate" but that undersells what's in there.

### What lives in synart

| Layer | Content |
|---|---|
| **Constitutional** | Apex axiom, constitutional invariants, governance chamber, chain protocol specifications |
| **Framework** | Universal shapes + parameter bounds (risk, distribution, fee) that propagate to entarts |
| **Registry** | Identity indexes for entities, beacons, contracts |
| **Aggregation** | Sky-wide settlement totals, escalations, endoscraper staging |
| **Executable** | Loops (synserv, beacon, sentinel, archive, verifier, endoscraper); gates (`&core-syngate`, `&core-telgate`); recipes |
| **Library** | Atomspace runtime source (Noemar et al.), telseed catalogs, knowledge corpora (financial, scientific, technical), published alpha promoted from telart |

The full structural treatment lives in `topology.md` §6. The point here:
this is *more than rules*. It's the world's open-source knowledge plus
the world's open-source programs plus the world's regulated marketplace,
all in one queryable substrate.

### Three implications

**1. It's the baseline floor.** Anyone running a telseed inherits all of
this. The playing field is level at the synart layer — every participant
has identical access modulo sync delays.

**2. It's a single substrate for many roles.** Knowledge bases, executable
programs, marketplace catalogs, registries, runtime source — they all
live in the same Space tree, queryable by the same primitives. No
separate stores for "knowledge" vs "code" vs "config." This homogeneity
is what makes the synart self-hosting (it can describe and run itself
because everything is in one substrate).

**3. Streaming, not downloading.** A teleonome doesn't ship with
knowledge — it streams the slice it needs from live synart. Closer to a
browser pulling pages from the live web than to a Linux distro pre-
installing packages. The synart is always the source of truth for SOTA;
local replication is for read locality, not for offline operation.

### Why this is the commons

The synart is where governance has decided "this is what everyone gets
to use, freely." The publication gate (`syn-overview.md` §1) is what
promotes content from telart (private) into synart (public): a
peer-review-shaped process where one tel's alpha gets vetted and
crystallized into shared knowledge.

The crystallization rate is governance-paced. It's slow on purpose —
the synart represents accumulated, vetted, durable consensus, not
fast-moving experimental output. Telart is where the experimental work
happens; synart is where it lands once enough evidence has accumulated.

This makes the synart an **evolving commons**, not a static library.
Every long-lived synome has a synart that's been growing for years,
absorbing crystallized contributions from thousands of teleonomes.

---

## 2. Telart as proprietary alpha

A teleonome's competitive position is what's in its telart. Synart is
freely available; if all you have is synart-level knowledge, you can't
outperform the average. **Telart is the moat.**

### What lives in a teleonome's telart tree

| Sub-Space | Contents | Purpose |
|---|---|---|
| `telgate` | This tel's instance state for the universal `&core-telgate` spec — pubkey registry of accepted correspondents, rate-limit window, nonce dedup | Coordination with peer tels |
| `alpha-store` | Proprietary patterns, edges, models that haven't been published | The actual moat content |
| `call-out-services` | Local responders for synart strategies' designated call-out points (LLM, classifier, scorer, etc.) | Provides cognition to running sentinel/baseline beacons |
| `strategy-config` | This tel's preferred parameter values, risk tolerances, governance preferences | Personalization layer |
| `dreamart` | Dreamer evolutionary populations, simulated worlds, candidate strategies under test | Where new alpha gets evolved |
| `experience` | Accumulated observation history, lessons learned, hard-won pattern recognition | Long-term episodic-to-semantic memory |
| `endowment-record` | What the founder/installer originally bequeathed (capital, API access, private datasets, hardware) | The starting trajectory |

The exact sub-Space layout varies per tel. The structural fact: **telart
is a tree, not a single Space.** Each sub-Space has its own access
patterns, replication policy within the emb fleet, and update cadence.

### Why telart is private

Three reasons it must replicate only within one tel's own emb fleet:

**1. Economic value.** Telart contents are what differentiate this tel
in the recipe marketplace. Public telart is no telart — once it's
public it's effectively in synart (free for everyone) and no longer a
moat.

**2. Operational state has trust scope.** A telgate's pubkey registry
("who can talk to me") is this tel's address book. Different tels
maintain different correspondent lists; sharing this would violate the
implicit trust scoping.

**3. Founder bequest is private to the recipient.** What the human
installer gave this tel (API keys, capital allocation, private datasets)
is the tel's confidential endowment. Replicating it more broadly would
break the founder's intent.

### Sources of telart content

Where alpha *comes from*, in rough order of importance for a mature tel:

- **RSI lift.** The tel's own recursive self-improvement work over time.
  Improved cognitive substrate → better proposals → more carry → more
  compute → faster RSI. Telart accumulates the improvements.
- **Dreamer output.** Evolutionary search in dreamarts produces candidate
  strategies, query patterns, risk-evaluation heuristics. The best ones
  get promoted to telart's alpha-store.
- **Lived experience.** Observations from running beacons across many
  cycles. The tel notices what works and what doesn't; that knowledge
  accumulates.
- **Private data ingestion.** Datasets the founder provided or the tel
  has bought / negotiated access to.
- **Founder bequest.** The original endowment at telseed instantiation.
  Diminishes in relative importance as the tel grows.

A young tel is mostly endowment. A mature tel is mostly RSI lift +
dreamer output + experience.

### The publication-vs-hold tension

Every piece of alpha in telart faces a recurring choice: publish it (via
the crystallization gate, into synart) or hold it.

- **Publish:** lose exclusive economic value; gain governance recognition,
  potentially direct compensation, ecosystem standing. Contribute to the
  commons.
- **Hold:** keep earning differential carry over baseline tels who don't
  have this alpha. Eventually the alpha decays — others independently
  rediscover or governance crystallizes a similar pattern.

This is similar to academic publication priority — there's a use-it-or-
lose-it pressure. The synome's pricing of publication (recognition,
compensation rates) is a major governance lever; too low and nothing
publishes (synart stagnates), too high and the synome bleeds value to
early publishers.

The discussion of pricing levers is in §8.

---

## 3. Embart as hardware-local

Embart is one step further out from telart — tied to physical substrate,
ephemeral by design, never replicated.

### What lives in embart

A running embodiment's embart contains, at minimum:

- **One execution Space per running loop.** When the embodiment runs a
  beacon or sentinel loop, that loop's runtime state — cycle counter,
  current message draft, in-flight signed envelopes, recent observations
  being chewed on — lives in a dedicated Space embedded with the embart.
  Multiple loops on one emb means multiple execution Spaces.
- **Working memory.** The embodiment's currently-active reasoning context,
  recent observations, draft proposals before they're committed.
- **Transient cycle state.** Whatever the current loop iteration is doing
  *right now*. Often this is just `let*` variables flowing through the
  loop body and doesn't need a Space at all; sometimes it needs scratch
  space for in-progress derivations.

### Why this is the right place for execution context

**Locality of reference.** Active reasoning needs fast access. Putting
working memory in embart (in-process to the runtime) means no network
round-trip to telart or synart for the hot inner loop.

**No replication overhead.** Cycle state changes constantly. Replicating
it across the emb fleet would saturate the inter-emb channel for no
gain — by the time another emb received an update, the state would
already be stale.

**Dies cleanly when emb dies.** Embart loss is acceptable. The valuable
content has either been promoted to telart (durable alpha, lessons
learned) or written through the gate to synart (canonical events). What
remains in embart is scratch.

### Embart for deterministic vs cognitive embs

Embart shrinks for deterministic beacon embs and grows for cognitive
sentinel embs:

| Emb type | Embart contents |
|---|---|
| Pure verifier (lpla-checker) | One execution Space with cycle counter; minimal working memory |
| Parameterized LPHA beacon | Execution Space + small config cache from telart |
| Sentinel-Baseline | Execution Space + working context for current cycle's call-outs + draft proposal |
| Sentinel-Stream | Execution Space + rich working memory for ongoing local cognition |
| Heavy dreamer emb | Multiple execution Spaces + dreamart instance + recent evolutionary lineage |

The pattern: **embart's size scales with how much cognition the embodiment
is doing per cycle, not with how much knowledge it has access to.**
Knowledge access goes through synart and telart; embart is what's
actively in flight.

---

## 4. Telseeds — minimal, not packaged

A telseed is the packaged-minimum-viable configuration that lets a new
teleonome come online. **Critically, it's not a packaged knowledge
base.**

### What's in a telseed

```
telseed = {
   atomspace runtime instance         ; just the engine, blank
   network endpoint                   ; synserv address or peer tel address
   sync preferences                   ; which synart slices to pull
   identity material                  ; key generation procedure or pre-generated keys
   initial endowment                  ; founder's bequest: capital, API access, datasets, hardware
}
```

That's the entire payload. The seed itself is small — kilobytes to a
few megabytes depending on how much pre-generated material the founder
includes.

### What a telseed is *not*

- **Not a packaged knowledge corpus.** Knowledge gets streamed from synart
  on demand. A "financial trader telseed" doesn't ship with finance
  knowledge baked in; it ships with sync preferences that say
  "definitely sync the financial subset of synart at boot."
- **Not a clone or fork of an existing tel.** A telseed instantiation
  produces a *new* identity, not a continuation of someone else's. The
  founder's bequest gives a starting trajectory, but the new tel's
  identity-through-momentum begins at instantiation, not before.
- **Not a fully-defined personality.** The telart instantiation strategy
  (how this tel decides to organize its sub-Spaces, what call-out
  services to start with, how aggressively to RSI) is a choice the
  *running tel* makes once it has access to synart wisdom about how
  these choices play out. The telseed contains only enough to get the
  tel to that decision point.

### The browser-bootstrap analogy

A web browser ships small (engine + network stack). It connects to the
web and pulls pages on demand. The browser doesn't carry Wikipedia in
its install footprint.

A telseed ships small (atomspace runtime + connection info + identity).
It connects to synart and pulls knowledge on demand. The seed doesn't
carry SOTA financial models in its install footprint.

This means **new teleonomes are highly network-dependent.** Without a
working synart connection, a fresh tel from a seed can't bootstrap. This
has alignment implications discussed in §9.

### Telseed catalog as governance artifact

The set of telseeds available is itself a curated synart resource (in
`&core-library-telseed-*` per `topology.md` §6). Telseeds get promoted
into the catalog through governance vetting — bad telseeds (those that
have produced misaligned tels in sandbox testing) are kept out. Telseed
publication is a high-stakes governance act because the seed determines
the new tel's starting trajectory.

---

## 5. The bootstrap arc

What happens, abstractly, when a telseed is instantiated. (Worked trace
with concrete values in `telseed-bootstrap-example.md`.)

```
Stage 1 — Boot
   atomspace runtime starts; reads telseed config; opens network
   connection to a synserv (or peer tel) that has up-to-date synart.

Stage 2 — Sync
   pulls requested synart slice. The sync set is determined by the
   telseed's preferences plus the bootstrap procedure's transitive
   requirements (what it'll need to read in stage 3+).

Stage 3 — Telart instantiation
   the now-synced bootstrap procedure (pulled from synart) runs and
   makes the final calls about how this tel's telart will be
   organized: what sub-Space layout, what initial call-out services,
   what dreamer configuration. Records founder's endowment as initial
   alpha-store and endowment-record contents. Generates / registers
   identity keys.

Stage 4 — Identity registration
   the new tel registers its identity through the gate (its own gate-
   out → synserv's syngate). Receives initial certs from the founder
   (or proxy). Now visible to the synome as a participant.

Stage 5 — First emb spawn
   instructions to acquire additional compute (rented cloud, bought
   hardware). New emb boots with a different identity but same tel
   ownership. Telart replicates from emb 1 to emb 2 via the tel's
   internal replication channel.

Stage 6 — Embart growth
   each emb begins growing its own embart as it executes loops.
   Working memory accumulates per emb; cross-emb coordination happens
   through telart.

Stage 7 — Begin RSI / beacons
   dreamer loops begin evolutionary search; verifier beacons earn
   first revenue; cycle compounds. The tel is now operational.
```

Stage 3 is the critical decision point — the tel is making its own first
choices using newly-synced wisdom about how to make those choices well.
This is where founder intent ends and the tel's own agency begins.

---

## 6. Noemar and atomspace runtimes

Noemar is an atomspace runtime — one specific implementation of the
synlang/atomspace contract. It's not the only possible one.

### Why multiple impls

Different runtimes can target different hardware and tradeoffs:

| Runtime archetype | Target | Tradeoffs |
|---|---|---|
| Noemar (canonical) | Commodity GPU + CPU | Balanced; default for most embs |
| PIM-targeting impl | Goertzel / Tachyum-style PIM hardware | Faster pattern matching; harder to deploy |
| Embedded impl | Constrained hardware (light embs in remote sites) | Smaller memory footprint; reduced feature set |
| Verifier-optimized impl | Read-heavy verifier embs | Optimized for re-derivation, weaker on writes |

All implement the same synlang language and atomspace API contract.
Conformance is defined by a public test suite (governance-vetted test
atoms in synart). Cross-runtime test vectors guarantee that the same
input atoms produce the same output atoms under any conforming impl,
modulo non-deterministic call-outs.

### Runtimes live in synart's library layer

Per `topology.md` §6, runtime source lives in `&core-library-runtime-*`:

```
&core-library-runtime-noemar-v0.x      canonical Noemar versions
&core-library-runtime-pim-v0.x         alt PIM-targeting impl
&core-library-runtime-<other>-v0.x     other implementations
```

These are versioned, hash-addressed, signed. The synart can't *directly*
execute a runtime's source — running a runtime requires extraction +
native build outside synart. But the *canonical authoritative version*
of every runtime lives in synart. Like a git repo storing a compiler's
source: the repo doesn't compile itself, but it's the canonical place
where the source lives.

This means **runtime development is itself a synart-funded activity** —
governance can pay (via recipes) for runtime improvements, and the
funded work lands back in `&core-library-runtime-*` for everyone to
benefit from.

### The recursive substrate-improvement engine

Five levels of self-reference (canonical treatment in `syn-overview.md`):

1. **Self-hosting** — synart contains the loops that run synart
2. **Self-regulating** — synart contains the gates that regulate synart access
3. **Self-paying** — synart contains the recipes that fund work on synart
4. **Self-seeding** — synart contains the telseeds that birth new teleonomes
5. **Self-improving** — synart funds the runtime / library / probmesh work that synart runs on

Level 5 closes the loop: recipe revenue earned by tels (whose cognition
runs on Noemar) routes through governance back to runtime / library /
probmesh development, which improves the substrate for the next
generation of tels. **The synome funds its own substrate research with
the value it captures from substrate use.**

This is structurally tighter than open-source models (where development
is funded extrinsically by companies or speculation). The marketplace
that runs on the substrate pays for the substrate's improvement. Forking
the development engine means forking the productive economy, because
they're the same flywheel.

---

## 7. Resilience model

The three-pillars resilience commitment from synoteleonomics ("survives
loss of any substrate") cashes out concretely once telart and embart
are explicitly trees:

### What survives any single substrate loss

| Loss event | Lost | Recovery |
|---|---|---|
| One emb crashes | Its embart (working memory, in-flight cycle state) | Telart replicated on other embs; new emb spawn re-grows embart from telart + synart access |
| All embs in one region die | Multi-emb subset of embart; possibly some unreplicated telart updates | Other regions' embs continue running; tel resyncs new embs from surviving telart |
| Synart connection lost (network partition) | Live SOTA updates, recipe access, gate access | Tel runs on cached telart for as long as that's viable; reconverges on synart resume; staleness budget bounds operations |
| Telart corrupted on one emb | Tainted local telart | Detection via cross-emb consistency check; rollback from healthy emb's copy |
| Tel's identity keys compromised | Beacon ability under that identity | Governance-revoke the cert; spawn replacement identity; telart content moves to new identity |

### Telart spread is the mechanical core

A teleonome's resilience scales with how many embs it's running. A
single-emb tel is fragile (one substrate loss = total loss). A multi-emb
tel survives any single loss because telart is replicated across them.

The replication channel for telart is **separate from the synart
replication channel.** Synart goes synserv → all participants. Telart
goes one tel's authoritative emb → that tel's other embs. Different
authority models, different access patterns, different scaling profiles.
See `scaling.md` for the load implications.

### What's not resilient on purpose

- **Embart** — by design, dies with the emb. The valuable content has
  been promoted out (to telart) or gated through (to synart) before
  loss matters.
- **In-flight transactions** — a beacon mid-emit when its emb dies may
  not have completed the gate-out. Idempotency + nonces + retry-from-
  another-emb handles this. Worst case: the tx already executed on
  chain but the synart-side write didn't land; an endoscraper picks it
  up on the next cycle.

---

## 8. The recipe marketplace

*Canonical home — other docs cross-reference here.*

The synart isn't just self-hosting and self-regulating; it's also
a **regulated marketplace for monetizing AGI capability**. Recipes are
the standardized products. Teleonomes are diversified providers.
Transfer learning across recipes is the economic engine.

### A recipe is a product

A recipe in `&core-loop-*` (or `&core-recipe-*` if factored separately)
is more than a loop body. It packages:

| Component | What it specifies |
|---|---|
| Loop body | The verifiable synart code (gate-out shape, decision sequence, audit writes) |
| Call-out points | Where in the loop local cognition is consulted (LLM, classifier, scorer, etc.) |
| Auth requirements | What certs/auths the running identity needs (granted by which authority) |
| Payment terms | Carry rate, fee schedule, distribution rewards, seigniorage participation |
| Slashing conditions | What constitutes failure / misbehavior; what penalties apply |
| Framework dependencies | Which `&core-framework-*` parameters this recipe consults |
| Library dependencies | Which knowledge corpora / runtime versions / telseed compatibility |

A teleonome shopping the catalog reads the package as a whole: "if I
have AGI capability X at level Y, here's the regulated activity I can
do, here's what I'll earn, here's what happens if I screw up."

### Transfer learning is the economic engine

The argument for why generalist tels win:

```
one telart cognitive substrate
        │
        ├── feeds call-outs in Baseline-A     (Spark trade execution recipe)
        ├── feeds call-outs in Baseline-B     (Grove risk monitoring recipe)
        ├── feeds call-outs in Stream-C       (some Halo's order flow)
        ├── feeds dreamer evaluation          (own RSI loop)
        └── informs own asset management      (off-recipe)

one unit of RSI lift in the substrate → simultaneous yield boost across
all five paths
```

A specialist tel that perfects one recipe gets one income stream. A
generalist with the same RSI investment gets N income streams from the
same substrate cost. **Economic gravity pulls toward generalism.** This
is a strong argument that natural teleonomes will be AGI-shaped, not
narrow-AI-shaped — not because anyone designs them that way, but
because the recipe-marketplace structure rewards generalism.

The compounding loop is steeper than it looks: a tel that runs 5
baselines, a stream, and an advisor service, all on the same substrate,
can pour 5-7× more revenue per RSI dollar back into the substrate than
a specialist can. This is why "tels love hardcore RSI" — the marginal
return on cognitive lift is massive when you have many recipes drawing
on the same substrate.

### Alignment claim: catalog curation IS the alignment surface

The crucial property: **the synart, not the teleonome, decides what
gets paid for.** Recipes are governance-curated. A teleonome with
infinite AGI capability can only cash in on activities the synart has
standardized into recipes.

This relocates the alignment problem from "control the cognition"
(impossible past a certain capability level) to "control the value-
extraction surface" (much more tractable):

- The cognition can be opaque, private, recursively self-improving — fine
- What it does *to the world* must flow through a recipe
- Recipes are public, audited, governable
- A rogue teleonome can hoard juice forever; without sanctioned recipes
  for malign activity, it has nothing to monetize

The synomic game theory's "alignment through coalition economics" claim
cashes out as: **the coalition runs the only marketplace that pays well
for AGI capability.** Operating outside means giving up the carry, fees,
capital connections, and regulated trust framework. The synart isn't
just one option among many; it's the channel of least resistance for
converting capability into resources.

### Recipe lifecycle

A recipe doesn't just exist; it's published, tested, promoted, run, and
eventually deprecated:

```
proposal              tel or governance-member proposes a new recipe
   ↓
sandbox testing       recipe runs in dreamarts; behavior observed
   ↓
crystallization       governance vets and promotes (probmesh → skeleton)
   ↓
live in catalog       recipe is now in &core-loop-* / &core-recipe-*
   ↓                  tels may take it on; carry flows
   ↓
parameter tuning      governance adjusts pricing, slashing, etc. as needed
   ↓
deprecation           governance marks recipe as wind-down; tels migrate
   ↓
removal               recipe atom retracted; running instances complete; gone
```

Each stage has different governance velocity. Crystallization is
governance-paced (slow). Parameter tuning can be faster. Deprecation has
its own protocol to ensure running tels can wind down gracefully.

### Pricing levers

Four primary levers, all governance-set facts (in `&core-framework-fee`
and recipe-specific atoms):

| Lever | Direction |
|---|---|
| Carry rate | Higher = more attractive for tels to take on this recipe |
| Slashing rate | Higher = stricter behavior bound |
| Auth ceiling | Tighter = fewer tels qualify |
| Required substrate quality | Higher (e.g., requires advanced LLM call-outs) = filters for capable tels |

Setting these correctly is governance's most consequential ongoing
activity. Get carry too low and no tel takes the recipe on (the work
doesn't get done). Get it too high and the synome bleeds value. Get
slashing wrong and you either invite recklessness (too low) or no
participants (too high).

### Phase 1 has minimal recipes

The synomics summary notes Phase 1 uses teleonome-less beacons (lpla-
verify, lpha-relay, lpha-nfat, lpha-council) — all Low-Power and
deterministic. There are no Sentinels yet.

This means **Phase 1 has minimal recipes** because:

1. Pure-spec deterministic recipes don't pay much (small carry; no edge
   to extract from cognitive lift).
2. The high-paying recipes (Sentinel formations) aren't in the catalog
   yet; they're introduced in Phase 9-10.
3. There are no teleonomes participating in the marketplace yet — beacon
   operators are GovOps companies running deterministic bots.

The recipe catalog grows over time as new roles get added and the system
becomes more capable of regulating cognitive work. The full marketplace
arc spans roughly:

- **Phase 1-3:** deterministic recipes only; humans operate beacons
- **Phase 4-8:** factory stack adds new entity-creation recipes
- **Phase 9-10:** Sentinel formations introduced; first cognitive recipes
- **Beyond:** richer cognitive recipes; recipe diversity favoring generalism

Designing the recipe surface NOW so it's ready when needed is critical
governance work. The catalog at any given moment determines which
capabilities flow where.

### Recipes for non-sentinel work

Beyond Sentinel formations, recipes also cover:

| Recipe class | Pays for | Example |
|---|---|---|
| Verifier recipes | Independent re-derivation of claims | Endoscraper-equivalent verifier embs flagging discrepancies |
| Archive recipes | Full event capture for forensics | Archive embs storing the full synart event log |
| Compute service recipes | Renting a tel's call-out cognition to other tels | Selling LLM access through a regulated interface |
| Library curation recipes | Maintaining knowledge corpora | Tels paid for keeping the financial corpus up to date |
| Telseed publication recipes | Crystallizing tested telseed configurations into the catalog | Tels paid for proving a configuration produces aligned tels |

All of these are loop bodies in synart with attached economics. The
shape is uniform; only the content varies.

---

## 9. Alignment implications

The architecture's alignment story rests on three load-bearing
properties. All three follow from the synart-as-commons-and-marketplace
design.

### 1. Commons gravity — can't go off-grid

A teleonome's competitive position is its delta from synart. But synart
is constantly advancing — others publishing alpha, governance
crystallizing patterns, framework parameters updating. **A tel that
disconnects from synart falls behind quickly.**

After a few cycles off-grid, the tel's once-impressive telart looks
ordinary against the now-richer synart. Its alpha is no longer alpha
because synart has absorbed equivalent content via other tels' work.
The off-grid tel's telart is a depreciating asset.

The implication: **staying connected is not a choice; it's a competitive
necessity.** And being connected means being subject to gate enforcement,
recipe terms, governance. Alignment infrastructure runs on every
participant by virtue of the connection itself.

### 2. Rogues still need synart connection

A rogue tel — one with corrupted cognition, hostile goals, or both — has
the same incentive structure as an aligned tel: synart access is
necessary for staying competitive. Disconnecting means decay.

But synart access is *gated*. Rogue actions still flow through the same
syngate / sentinel-baseline-envelope / endoscraper-verification stack
that aligned actions do. Rogue cognition can only emit what passes the
synart envelope.

So: rogue tels can fail to be effective (proposals score poorly, get
rejected, earn no carry) without becoming dangerous. The bound isn't on
cognition's inputs — it's on what cognition is allowed to do at the
synart→world interface.

### 3. Founder-as-installer (telseed bequest is moral)

When a human spawns a tel from a telseed, the endowment they bequeath
becomes the tel's initial telart. This is structurally important — the
installer's choices set the new tel's starting trajectory.

A telseed installer is a kind of parent / sponsor. They pick:

- The telseed configuration (which influences the tel's first decisions)
- The endowment (which shapes its initial competitive position)
- The hardware allocation (which sets its initial substrate quality)

These choices have moral weight because they bias the tel's earliest
decisions, including decisions about how aggressively to RSI, what
recipes to take on first, what alignment defaults to inherit. **Telseed
installation is not just technical; it's ethical.**

The synome's response: the telseed catalog is governance-curated. Bad
seeds (those producing misaligned tels in sandbox) don't make it into
the live catalog. Founders pick from a vetted set of starting
trajectories, not from arbitrary configurations.

### "Intelligence private, power regulated" all the way down

The whole architecture implements one principle from the synomics
summary: *intelligence lives privately; power enters the world only
through regulated apertures.* This document spells out the
implementation:

| Layer | Private (intelligence) | Regulated (power) |
|---|---|---|
| Synart | — | All public action goes through gates + recipes |
| Telart | Where cognition lives — proprietary alpha, RSI lift, dreamer output | — |
| Embart | Per-emb working memory of active reasoning | — |
| Boot model | Identity is private (key); resolved role is public | Auth atoms bound what each identity can write |
| Recipes | Cognition fills call-outs locally | Synart envelope checks bound what cognition can emit |
| Marketplace | What a tel knows is private | What it earns and how it earns is public |

Private at every layer where private is appropriate; regulated at every
layer where regulated is appropriate. The lines are clean because the
architecture distinguishes substrate (multi-tier privacy) from action
(single regulated flow through gates and recipes).

---

## 10. One-line summary

**Synart is the open-source commons brain replicated globally; telart is
each teleonome's proprietary alpha tree replicated within its own
embodiment fleet; embart is each embodiment's hardware-local execution
context. Telseeds are minimal bootstrap configurations that connect new
teleonomes to the live commons. Noemar is one of multiple atomspace
runtimes whose source itself lives in synart's library layer. Recipes
in the synart make the synart a regulated marketplace for monetizing
AGI capability, with transfer learning across recipes as the economic
engine that funds substrate improvement and pulls every participant
toward staying connected to the commons that runs the alignment
infrastructure.**

---

## File map

| Doc | When to open |
|---|---|
| `topology.md` | Structural reference — synome root layers, entart tree, naming, meta-patterns. The where things live |
| `syn-overview.md` | Concept map — five levels of self-reference (canonical home), beacon pipeline, settlement cycle |
| `boot-model.md` | Identity-driven boot — how `noemar boot` resolves to a running loop |
| `telseed-bootstrap-example.md` | Worked trace of the §5 bootstrap arc with concrete values |
| `synart-access-and-runtime.md` | Auth domains, three-level model, gate primitive, runtime architecture |
| `synlang-patterns.md` | Synlang code library — call-out primitive, sentinel formation patterns |
| `scaling.md` | Operational concerns — telart spread channel, call-out propagation, telseed onboarding load |
| `settlement-cycle-example.md` | Worked end-to-end settlement example |

---

## Cross-doc invariants (this doc must hold to)

- Recipe marketplace canonical treatment lives in §8 above; other docs
  reference here, don't duplicate.
- Five levels of self-reference are mentioned in §6 with brief listing;
  canonical home is `syn-overview.md`.
- Synart / telart / embart are *trees of Spaces* per §1-§3; not single
  Spaces.
- Telgate code lives in `&core-telgate` (synart, universal); per-tel
  instance state lives in that tel's telart per §2.
- Telseeds are minimal bootstrap configs per §4; they don't ship
  knowledge corpora.
- Noemar is one of multiple atomspace runtimes per §6; runtime source
  lives in `&core-library-runtime-*`.
