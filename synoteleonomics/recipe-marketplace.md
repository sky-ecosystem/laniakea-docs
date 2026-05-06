---
concepts:
  references:
    - rsi
    - rogue-threat-model
    - trust-problem
---

# The Recipe Marketplace

*Canonical home — other docs cross-reference here.*

The synart isn't just self-hosting and self-regulating; it's also a **regulated marketplace for monetizing AGI capability**. Recipes are the standardized products. Teleonomes are diversified providers. Transfer learning across recipes is the economic engine.

This document was formerly `noemar-synlang/syn-tel-emb.md` §8.

---

## A recipe is a product

A recipe in `&core-loop-*` (or `&core-recipe-*` if factored separately) is more than a loop body. It packages:

| Component | What it specifies |
|---|---|
| Loop body | The verifiable synart code (gate-out shape, decision sequence, audit writes) |
| Call-out points | Where in the loop local cognition is consulted (LLM, classifier, scorer, etc.) |
| Auth requirements | What certs/auths the running identity needs (granted by which authority) |
| Payment terms | Carry rate, fee schedule, distribution rewards, seigniorage participation |
| Slashing conditions | What constitutes failure / misbehavior; what penalties apply |
| Framework dependencies | Which `&core-framework-*` parameters this recipe consults |
| Library dependencies | Which knowledge corpora / runtime versions / telseed compatibility |

A teleonome shopping the catalog reads the package as a whole: "if I have AGI capability X at level Y, here's the regulated activity I can do, here's what I'll earn, here's what happens if I screw up."

---

## Transfer learning is the economic engine

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

A specialist tel that perfects one recipe gets one income stream. A generalist with the same RSI investment gets N income streams from the same substrate cost. **Economic gravity pulls toward generalism.** This is a strong argument that natural teleonomes will be AGI-shaped, not narrow-AI-shaped — not because anyone designs them that way, but because the recipe-marketplace structure rewards generalism.

The compounding loop is steeper than it looks: a tel that runs 5 baselines, a stream, and an advisor service, all on the same substrate, can pour 5-7× more revenue per [RSI](../core-concepts/rsi.md) dollar back into the substrate than a specialist can. This is why "tels love hardcore RSI" — the marginal return on cognitive lift is massive when you have many recipes drawing on the same substrate.

---

## Alignment claim: catalog curation IS the alignment surface

The crucial property: **the synart, not the teleonome, decides what gets paid for.** Recipes are governance-curated. A teleonome with infinite AGI capability can only cash in on activities the synart has standardized into recipes.

This relocates the alignment problem from "control the cognition" (impossible past a certain capability level) to "control the value-extraction surface" (much more tractable):

- The cognition can be opaque, private, recursively self-improving — fine
- What it does *to the world* must flow through a recipe
- Recipes are public, audited, governable
- A rogue teleonome can hoard juice forever; without sanctioned recipes for malign activity, it has nothing to monetize

The synomic game theory's "alignment through coalition economics" claim cashes out as: **the coalition runs the only marketplace that pays well for AGI capability.** Operating outside means giving up the carry, fees, capital connections, and regulated trust framework. The synart isn't just one option among many; it's the channel of least resistance for converting capability into resources.

For the broader game-theoretic argument, see [`synomic-game-theory.md`](synomic-game-theory.md). For the rogue threat the marketplace structurally constrains, see [`teleonome-rogues.md`](teleonome-rogues.md).

---

## Recipe lifecycle

A recipe doesn't just exist; it's published, tested, promoted, run, and eventually deprecated:

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

Each stage has different governance velocity. Crystallization is governance-paced (slow). Parameter tuning can be faster. Deprecation has its own protocol to ensure running tels can wind down gracefully.

---

## Pricing levers

Four primary levers, all governance-set facts (in `&core-framework-fee` and recipe-specific atoms):

| Lever | Direction |
|---|---|
| Carry rate | Higher = more attractive for tels to take on this recipe |
| Slashing rate | Higher = stricter behavior bound |
| Auth ceiling | Tighter = fewer tels qualify |
| Required substrate quality | Higher (e.g., requires advanced LLM call-outs) = filters for capable tels |

Setting these correctly is governance's most consequential ongoing activity. Get carry too low and no tel takes the recipe on (the work doesn't get done). Get it too high and the synome bleeds value. Get slashing wrong and you either invite recklessness (too low) or no participants (too high).

---

## Phase 1 has minimal recipes

Phase 1 uses teleonome-less beacons (lpla-verify, lpha-relay, lpha-nfat, lpha-council) — all deterministic. There are no Sentinels yet.

This means **Phase 1 has minimal recipes** because:

1. Pure-spec deterministic recipes don't pay much (small carry; no edge to extract from cognitive lift).
2. The high-paying recipes (Sentinel formations) aren't in the catalog yet; they're introduced in Phase 9-10.
3. There are no teleonomes participating in the marketplace yet — beacon operators are GovOps companies running deterministic bots.

The recipe catalog grows over time as new roles get added and the system becomes more capable of regulating cognitive work. The full marketplace arc spans roughly:

- **Phase 1-3:** deterministic recipes only; humans operate beacons
- **Phase 4-8:** factory stack adds new entity-creation recipes
- **Phase 9-10:** Sentinel formations introduced; first cognitive recipes
- **Beyond:** richer cognitive recipes; recipe diversity favoring generalism

Designing the recipe surface NOW so it's ready when needed is critical governance work. The catalog at any given moment determines which capabilities flow where.

---

## Recipes for non-sentinel work

Beyond Sentinel formations, recipes also cover:

| Recipe class | Pays for | Example |
|---|---|---|
| Verifier recipes | Independent re-derivation of claims | Endoscraper-equivalent verifier embs flagging discrepancies |
| Archive recipes | Full event capture for forensics | Archive embs storing the full synart event log |
| Compute service recipes | Renting a tel's call-out cognition to other tels | Selling LLM access through a regulated interface |
| Library curation recipes | Maintaining knowledge corpora | Tels paid for keeping the financial corpus up to date |
| Telseed publication recipes | Crystallizing tested telseed configurations into the catalog | Tels paid for proving a configuration produces aligned tels |

All of these are loop bodies in synart with attached economics. The shape is uniform; only the content varies.

---

## Connection to Other Documents

| Doc | Relationship |
|----------|--------------|
| [`../synodoxics/noemar-substrate.md`](../synodoxics/noemar-substrate.md) | Synart / telart / embart artifact tiers — the substrate the marketplace runs on |
| [`../noemar-synlang/topology.md`](../noemar-synlang/topology.md) | Synome root layers including `&core-loop-*` and `&core-recipe-*` where recipes live |
| [`../noemar-synlang/synlang-patterns.md`](../noemar-synlang/synlang-patterns.md) | Synlang code library — call-out primitive, sentinel formation patterns; what recipes are built from |
| [`../noemar-synlang/scaling.md`](../noemar-synlang/scaling.md) | Operational concerns of running networked recipes |
| [`teleonome-economics.md`](teleonome-economics.md) | Fixed-cost compute, RSI loop, daydreaming — the economics that motivate participating in recipes |
| [`synomic-game-theory.md`](synomic-game-theory.md) | Why alignment wins — the marketplace is the channel of least resistance for AGI capability |
| [`teleonome-binding.md`](teleonome-binding.md) | How binding works — beacons as legibility, the regulated surface that recipes flow through |
| [`teleonome-rogues.md`](teleonome-rogues.md) | The rogue threat model — what the marketplace structurally constrains |

---

## One-line summary

**Recipes are the synart's standardized products that monetize AGI capability through regulated activity; teleonomes are diversified providers; transfer learning across recipes is the economic engine that funds substrate improvement; catalog curation is governance's most consequential ongoing activity because it determines which capabilities flow where.**
