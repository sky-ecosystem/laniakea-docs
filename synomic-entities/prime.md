# Prime

Primes are heavyweight Synomic Entities — billion-scale capital allocators that move matter and energy through calculated, efficient finance. For Synomic Entity theory (autonomous lifeforms, structural integration, the minimal-to-mega spectrum), see [`../macrosynomics/synomic-entities.md`](../macrosynomics/synomic-entities.md). This document covers the per-type operational spec.

---

## Categories

### Star Primes — general-purpose capital allocation

| Prime | Status |
|---|---|
| **Spark** | operational |
| **Grove** | operational |
| **Keel** | operational |
| **skybase** | operational |
| **launch6** | operational |

Star Primes deploy capital into their domains, generate returns, and compound capability. The Phase 1 v2 commitment names six Primes total: Spark, Grove, Obex, Keel, skybase, launch6.

### Institutional Primes — meta-level structural functions

| Prime | Status |
|---|---|
| **Obex** | operational |

Institutional Primes don't just allocate capital — they shape the ecosystem itself: incubating new Primes and Halos, and providing meta-level structural functions.

---

## Infrastructure

Each Prime is built on the standard PAU pattern (see [`../smart-contracts/architecture-overview.md`](../smart-contracts/architecture-overview.md)):

| Component | Purpose |
|---|---|
| **SubProxy** | On-chain identity and control surface |
| **PAU** | Controller + ALMProxy + RateLimits — capital control infrastructure |
| **Rate limits** | Constraints on capital flows; SORL-governed increases (25%/18h) |
| **Operating setup** | `baseline-{prime}` (relay) + `warden-{prime}-{operator}` (relay) + `stream-{prime}-{actor}` (stream-sentinel) |
| **Token** | Governance distribution |

Each Prime maintains a **primebook** as part of the risk framework — see [`../risk-framework/primebook-composition.md`](../risk-framework/primebook-composition.md) for the balanced-ledger structure that ties the Prime to its underlying Halobooks.

---

## Operational Beacons

Primes are operated by a three-beacon operating setup — the canonical full-automation pattern for high-authority action. Baseline-relay (public, auditable rules), warden-relay (independent halt authority), and stream-sentinel (proprietary intelligence streaming intent) are three distinct beacon classes deployed together, not a single "formation" class. The full spec (TTS, Streaming Accord as recipe) lives in [`../sentinel/sentinel-network.md`](../sentinel/sentinel-network.md). The synlang substrate lives in [`../noemar-synlang/synlang-patterns.md`](../noemar-synlang/synlang-patterns.md) §6.

### Naming

```
baseline-{prime}                  # Baseline-relay for specific Prime
                                  # config: &entity.prime.{prime}.relay.baseline
warden-{prime}-{operator}         # Warden-relay operated by independent party
                                  # config: &entity.prime.{prime}.relay.warden.{operator}
stream-{prime}-{actor}            # Stream-sentinel operated by specific actor
                                  # config: &entity.prime.{prime}.sentinel.{actor}
```

Examples:

```
baseline-spark
warden-spark-sentinelco
warden-spark-riskwatch
stream-spark-horizonlabs
```

---

## Capital Flow

```
            Generator
                │
                │ (credit lines)
    ┌───────────┼───────────────┬─────────┬─────────────┐
    ▼           ▼               ▼         ▼             ▼
  Spark      Grove            Keel     Obex          skybase  launch6
    │           │               │         │             │       │
    ▼           ▼               ▼         ▼             ▼       ▼
  Halos      Halos          Halos    (incubates)     Halos   Halos
                                      new Primes &
                                      Halos
```

1. Generator creates USDS and provides credit lines to each Prime
2. Prime's operating setup (baseline-relay + warden-relay + stream-sentinel) deploys capital into the Prime's domain
3. Halos nest under Primes for specific products (LCTS, NFAT, AMM, etc.)
4. Returns flow back up; carry distributed to operating teleonomes per the Streaming Accord

For ingression of risk capital (TEJRC, TISRC, srUSDS) and the capital-stack math, see [`../risk-framework/capital-formula.md`](../risk-framework/capital-formula.md). For the recipe-marketplace surface that prices the operating-setup work, see [`../synoteleonomics/recipe-marketplace.md`](../synoteleonomics/recipe-marketplace.md).

---

## Synomic Entity Primitives

Primes have access to a set of protocol-level capabilities that other agent types do not:

| Primitive | Description |
|---|---|
| Receive capital from Sky Protocol | Generator → Prime credit lines |
| Risk capital ingression | TEJRC, TISRC, srUSDS recognition into Prime's capital base |
| Origination of risk capital | Mint TEJRC / TISRC against the Prime's books |
| Settlement infrastructure access | Daily settlement cycle integration |

Primitives are locked during the Prime's waiting period (post-creation, pre-token-issuance) — see [`creation-restructuring.md`](creation-restructuring.md).

---

## Governance

| Layer | Mechanism |
|---|---|
| Strategic direction | PRIME-token holders, via SpellGuards (see [`../governance/spellguard.md`](../governance/spellguard.md)) |
| Operational changes | Prime SpellGuard requires core spell payload + Prime token hat |
| Per-Halo administration | Prime is the rank-2 administrator of its Halos |
| Accordance | Prime is accordant to a Guardian (Ozone); the Guardian is accountable for the Prime's compliance with Sky-level rules |

Even with token governance, Primes can be autonomous lifeforms — token-holder rights are bounded by inalienable claims encoded in the Prime's synomic artifact. See [`../macrosynomics/synomic-entities.md`](../macrosynomics/synomic-entities.md) for the structural-integration framing.

---

## Reference Value

For Growth Staking purposes, a Prime's Reference Value is `Net Capital Reserves / Tokens Outstanding` — no P/E component. Net capital reserves include look-through to Reference Value for any Halo Agent tokens the Prime holds. The Agent token Floor (`min(Reference Value, Market Value)`) applies. See [`../growth-staking/growth-staking.md`](../growth-staking/growth-staking.md) §4.5 for the full treatment and §2 for the Prime governance token's GF (2.5×) and TEJRC's GF (~1.67×).

---

## Related

- [`README.md`](lani/synomic-entities/README.md) — Rank hierarchy and entity index
- [`generator.md`](generator.md) — Source of credit lines
- [`guardian.md`](guardian.md) — Ozone, the Guardian Primes are accordant to
- [`creation-restructuring.md`](creation-restructuring.md) — Prime waiting period and Type 1/2 mechanics
- [`halo-classes.md`](halo-classes.md), [`halo-portfolio.md`](halo-portfolio.md), [`halo-term.md`](halo-term.md), [`halo-trading.md`](halo-trading.md) — Halo Class types Primes administer
- [`../sentinel/sentinel-network.md`](../sentinel/sentinel-network.md) — Operating setup (baseline-relay + warden-relay + stream-sentinel) for the Prime
- [`../risk-framework/primebook-composition.md`](../risk-framework/primebook-composition.md) — Primebook structure
- [`../smart-contracts/architecture-overview.md`](../smart-contracts/architecture-overview.md) — PAU pattern and the four-layer capital flow
- [`../roadmap/phase-1-spaces.md`](../roadmap/phase-1-spaces.md) — Phase 1 v2 commitment naming the six Primes
