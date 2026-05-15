# Growth Staking

**Status:** speculative — entire mechanism activates **post-Phase-1**. Phase 1 emits real-time ER per Prime; staking rewards are not yet distributed via synserv. P/E parameters and GF values are sudo-set at the activation boundary.
**Canonical home:** `laniakea-docs/growth-staking/`

---

## TL;DR

Growth Staking conditions SKY staking rewards on parallel holdings of **growth assets** — Synomic Entity governance tokens (Generator/Guardian/Prime/Halo) at **GF 2.5×** and Prime junior risk capital (TEJRC) at **GF ~1.67×**. Passive yield wrappers (sUSDS, srUSDS, fixed-rate sUSDS, Halo Units, stUSDS, TISRC) are excluded. All values enter the staking-factor formula at **Reference Value** — fundamentals from a global P/E model (Base P/E × per-stream Modifier ± Variance, positioned by linear-with-caps growth score on T12M revenue) — never spot, on either side. Stakers below 100% factor forfeit yield to the TMF aggregation in `&core.settlement` (not redistributed). Leverage surface is **stUSDS**, a Morpho-pool USDS lending product where Sky Core captures **10% of the borrower spread**. Stakers participate via a **Folio** (rank-3 tokenless single-owner PAU); Primes/Halos with treasury SKY are auto-folios.

## Section map

| § | Topic |
|---|---|
| 1 | Mechanism in one screen |
| 2 | Growth Factor tiers and exclusions |
| 3 | Reward scaling and forfeiture |
| 4 | Reference Valuation — global P/E model + per-entity formulas |
| 5 | stUSDS borrow surface |
| 6 | Folio integration and entity-internal staking |
| 7 | Anti-gaming |
| 8 | Synlang form |
| 9 | Phase 1 carve-outs and open items |

---

## §1 Mechanism

```
Staking Factor  = min(1, Σ(Asset_RefValue_i × GF_i) / Staked_SKY_RefValue)
Staking Rewards = Base Staking Yield × Staked SKY × Staking Factor
```

Both sides use Reference Values, so the mechanism is immune in both directions to speculative price movement: pumping Synomic Entity tokens does not inflate credit; dumping SKY does not reduce the requirement. Thesis: passive SKY holders earn nothing, parking USDS in passive wrappers earns no GF credit either — capital must take a directional position on a specific Synomic Entity (governance equity or first-loss tranche) to unlock yield. Mercenary staking is eliminated by construction.

## §2 Growth Factor tiers and exclusions

| Category | Assets | GF | Effect |
|---|---|---|---|
| Synomic Entity governance tokens | Generator, Guardian, Prime, Halo | **2.5×** | $1 RefValue counts as $2.50 |
| Junior risk capital | TEJRC (per-Prime) | **~1.67×** | $1 RefValue counts as $1.67 |

GF integers are stored ×10 in synlang (`(growth-factor entity-governance 25)`, `(growth-factor tejrc 17)`).

**Excluded** (passive — no investment thesis): srUSDS, TISRC, sUSDS, fixed-rate sUSDS, Halo Units (Portfolio/Term/Trading shares), stUSDS, LCTS queue positions, USDS, SKY itself (denominator-only). Core Controlled and Recovery entities are tokenless and excluded by type. Folios are tokenless and serve as the staking vehicle.

The stUSDS exclusion is **structural, not USDS-specific**: in a multi-Generator future, staked variants of any Generator's primary asset (e.g. hypothetical stEURS) are excluded by the same rule.

## §3 Reward scaling and forfeiture

Rewards scale linearly 0–100% as the Folio's GF-adjusted RefValue rises toward staked SKY RefValue. **Forfeited rewards do not redistribute** to fully-qualifying stakers — they flow back into the TMF waterfall via `&core.settlement` aggregation. Design rewards activation, not concentration. See `accounting/settlement-cycle.md` and `accounting/treasury-management.md`.

## §4 Reference Valuation

The whole system rests on this layer. Spot prices never appear in the staking formula.

### 4.1 Global P/E model

Three governance-set parameters per income stream, anchored to one Base P/E:

```
Center P/E   = Base_P/E × Modifier
Band         = Center P/E × Variance              (fractional half-width)
Growth score = clamp(growth_rate / target_growth_rate × 100, 0, 100)   ; linear-with-caps
Actual P/E   = Center − Band + (score / 100) × (2 × Band)
```

**Trailing revenue window:** **T12M** (trailing 12-month annualized) — governance-tunable. Linear-with-caps is deliberately simple; clamped flat outside [0,100].

### 4.2 Per-entity formulas (numerators)

| Entity | Formula | Notes |
|---|---|---|
| **SKY** | `(CoreRev × P/E + SpecialRev × Special P/E) / CircSupply` | Special revenue (creation-fee token sales) uses a separate Modifier (typically <1.0) — lumpy |
| **Generator** | `(GenRev × P/E + ISRC BookValue) / Tokens` | Generator keeps 95% gross; 5% feeds Sky Core. ISRC at par. |
| **Guardian** | `(AccordFee × P/E + SKY Holdings BV) / Tokens` | sUSDS income feeds P/E; sUSDS balance not double-counted as BV |
| **Prime** | `Net Capital Reserves / Tokens` | **No P/E** — pure BV. Look-through to Halo RefValue for held Halo tokens |
| **Halo** | `(Capital Reserves + Earnings × P/E) / Tokens` | Early-stage Halos qualify on observable active deployment, even pre-earnings |
| **TEJRC** | On-chain redemption value | Directly backed at known ratio — no P/E |

**SKY Core revenue lines** (standard P/E): USDS spread, USDS risk-capital fees, **stUSDS spread** (10% of borrower spread), Entity Upkeep (50 bps/yr — `accounting/entity-fees.md`), Guardian accord fees, USDS duration income, **5% of Generator revenue**. **SKY Special revenue:** entity creation fee token sales (5% of newly issued tokens).

### 4.3 Synomic Entity token floor (asymmetric)

```
Effective Value = min(Reference Value, Market Value)
```

If a Synomic Entity token's market price collapses below fundamentals (distress, illiquidity), the worse value is used — so impairment shows up in the staker's factor. SKY itself is **not** floored: the denominator must be stable; a SKY dump should not make full rewards trivially earnable.

### 4.4 Net effect

Speculative pumps/dumps on either side leave the staking factor unchanged. Genuine economic changes (protocol revenue growth, Prime capital deployment) move RefValues correctly. Genuine Synomic Entity token impairment below fundamentals shows up via the §4.3 market floor.

## §5 stUSDS — Morpho-pool borrow surface

Two-sided lending product, Generator-adjacent (issued by Generator, but the spread fee is a **Sky Core** stream, not a Generator stream).

| Side | Action | Mechanics |
|---|---|---|
| Depositor | Deposits USDS, receives stUSDS shares | ERC-4626-style; share price accrues interest |
| Borrower | Posts collateral, draws USDS | Variable rate via Morpho-pool utilization model |

```
Borrow Rate  = Base Rate + Spread(utilization)
Lender Rate  = (Spread × 0.90) × utilization              ; 90% to depositors
Sky Core Fee = (Spread × 0.10) × utilization × notional   ; 10% to Sky Core (the "stUSDS spread")
```

**Eligible collateral (open):** growth assets in the borrower's Folio (Synomic Entity governance tokens, TEJRC) plus staked SKY. Proceeds buy more GF-eligible assets, raising the staker's factor. **stUSDS is itself excluded from GF eligibility** — depositor side is passive yield.

**Open** (deferred to governance / a future `smart-contracts/stusds.md`): exact eligible-collateral set; liquidation mechanics under collateral collapse; base-rate reference (USGE base vs Sky Savings Rate vs other). Phase 1 carve-out: borrow rate is governance-set; becomes utilization-driven when `&core.loop.stusds` activates.

## §6 Folio integration and entity-internal staking

**Folio** (rank-3, tokenless, single-owner PAU vehicle — full spec `synomic-entities/folio.md`): instant creation via auto-accord; holds staked SKY + growth-asset portfolio; two operating modes (automated sentinel formation or principal control); **Type 1 Restructure** path graduates to Standard Halo or Prime (`synomic-entities/creation-restructuring.md`); reads staking factor from synserv atoms; receives reward distributions per settlement.

**Entity-Internal Growth Staking.** Primes/Halos with treasury SKY auto-earn — the Synomic Entity functions as its own Folio with book value at GF 2.5×; any meaningful BV trivially clears 100% factor.

**Accepted double-counting.** A Synomic Entity's book value supports staking-factor claims twice (the entity's own SKY treasury + external Folios holding the entity's tokens). By design: amplifies incentive to build BV; creates structural SKY demand from the innovation layer.

## §7 Anti-gaming

**Primary defense — Reference Valuation.** Spot price moves don't affect the staking factor in either direction.

**Secondary — hollow entities** (Primes/Halos created solely to warehouse capital and farm GF):
1. *Mechanical (day one):* RefValues anchor to actual capital reserves (Primes) or earnings (Halos) — capital must really be deployed, revenue really earned.
2. *Synomic monitoring (deferred):* governance can monitor a Prime's or Halo's synomic artifacts for genuine intelligent activity, requiring a real activity threshold to maintain GF eligibility. No rule atoms in v1; activated only if manipulation emerges. Same monitoring extends to potentially hollow TEJRC positions.

## §8 Synlang form

Following the synome-root layering in `noemar-synlang/topology.md` §6 and the in-space-calculation pattern in `macrosynomics/beacon-framework.md` §4. Calculation is **synserv in-space, not in beacons.**

**Parameters (governance-set)** live in a **new** `&core.framework.valuation` Space (`base-pe`, `pe-modifier $stream`, `pe-variance $stream`, `growth-score-target $stream`, `revenue-trailing-window months 12`, `growth-factor entity-governance 25`, `growth-factor tejrc 17` — ×10 int-encoded —, `forfeit-target tmf-waterfall`); stUSDS parameters (`stusds-sky-core-share 10`, `stusds-base-rate $value`) are sudo-set in v1, with Space location TBD.

**Derived values:** `(reference-value $entity $value $epoch)` lands in each `&entity.{type}.{id}.root`; `(staking-factor $folio $value $epoch)` and `(gf-portfolio-value $folio $value $epoch)` in `&entity.folio.{id}.root`; `(epoch-staking-rewards-paid $amount)` and `(epoch-staking-rewards-forfeited $amount)` in `&core.settlement`.

**Synserv per-epoch closure** (added alongside the existing 5-step Prime closure): T12M revenue per income stream per entity → growth score → actual P/E per stream → RefValue per entity (§4.2 formulas) → per-Folio GF-adjusted portfolio value → staking factor → rewards paid → forfeitures summed and emitted to `&core.settlement` for TMF aggregation.

## §9 Phase 1 carve-outs and open items

**Activation:** post-Phase-1. Phase 1 deliverable is real-time ER per Prime; Growth Staking does not distribute rewards yet.

**Sudo-set carve-outs at activation** (insyn/exsyn pattern; topology deltas in `&core.framework.valuation`, not code rewrites): all P/E parameters (Base, Modifiers, Variances, growth-score targets) sudo-set; GF values (2.5×, ~1.67×) sudo-set; trailing revenue is **insyn** for active synomic Primes (real synlang on Primebook positions) and **exsyn-oracle** for legacy core vaults / PSM during transition (ratio shifts toward all-insyn as halos migrate; synlang unchanged); stUSDS borrow rate governance-set in v1, becomes utilization-driven once `&core.loop.stusds` activates; hollow-entity monitoring deferred (no rule atoms in v1; reactive activation).

**Open** (non-blocking): GF revision cadence and authority; Base P/E revision cadence; measurement timing (settlement-boundary snapshot vs time-weighted to prevent flash-positioning); new Synomic Entities with no history have zero RefValue (likely intended — confirm); behavior under extreme SKY market/RefValue divergence (informational or governance-triggered recalibration).

---

## Key vocabulary

| Term | Meaning |
|---|---|
| **Growth Factor (GF)** | RefValue multiplier: 2.5× for Synomic Entity governance tokens, ~1.67× for TEJRC |
| **Reference Value (RefValue)** | Fundamentals price from global P/E model (or book value for Primes); replaces spot in the formula |
| **Global P/E model** | Base P/E × Modifier ± Variance, positioned by linear-with-caps growth score on T12M revenue |
| **Staking Factor** | `min(1, Σ(asset_RefValue × GF) / staked_SKY_RefValue)`; linear on rewards |
| **Synomic Entity token floor** | `min(RefValue, MarketValue)` for Synomic Entity tokens; asymmetric (SKY not floored) |
| **stUSDS** | Morpho-pool USDS lending product. 90% spread → depositors; **10% → Sky Core (the "stUSDS spread")** |
| **Entity-Internal Growth Staking** | Primes/Halos with treasury SKY auto-qualify as folios via own book value × 2.5× |
| **Folio** | Rank-3 tokenless single-owner PAU vehicle — participation surface (`synomic-entities/folio.md`) |
| **Forfeited rewards** | `(1 − factor) × base yield × staked` → TMF via `&core.settlement`; not redistributed |
| **Hollow entity** | Prime/Halo warehousing capital without activity — defended by RefValue + (deferred) synomic-activity monitoring |
| **Linear-with-caps** | Growth-rate → score mapping, clamped to [0, 100] |
| **T12M** | Trailing 12-month annualized revenue window |

## Cross-references

- `synomic-entities/folio.md` — participation vehicle (full operational spec)
- `synomic-entities/{prime,generator,guardian,halo-classes}.md` — per-entity RefValue inputs
- `synomic-entities/creation-restructuring.md` — Type 1 Restructure (Folio → Halo / Prime)
- `synomic-entities/{core-controlled,recovery}.md` — tokenless rank-1 entities (excluded)
- `accounting/settlement-cycle.md` — closure heartbeat, forfeited-reward sink
- `accounting/treasury-management.md` — TMF waterfall (forfeitures land here)
- `accounting/entity-fees.md` — 50 bps Entity Upkeep feeding SKY Core revenue
- `accounting/capital-stack.md` — TEJRC / srUSDS / sUSDS naming and tranches
- `noemar-synlang/topology.md` — synome-root layering, `&core.framework.*` naming
- `macrosynomics/beacon-framework.md` — in-space calculation pattern (synserv, not beacons)
- `roadmap/{phase-1-spaces,README}.md` — Phase 1 carve-out pattern; activation gating
- `inactive/archive/growth-staking/` — pre-synlang historical source (out of scope)

## File map

| File | What's in it that the summary doesn't have |
|---|---|
| `growth-staking.md` | Full spec. Compressed away here: numeric worked examples (multi-asset staking factor table, P/E worked example, $500M Prime entity-internal example, passive→active flow); pre-synlang→post-synlang translation table (SGA/sSGA/srSGA-ESRC/stSCST/Folio Agent; "Sky Agents" preserved as historical LHS → Synomic Entities); per-row §4.10 scenarios table; full incentive-effects narrative (passive→active flow; ecosystem alignment; natural segmentation tiers — concentrated stakers, underwriters, mixed, leveraged); GF int-encoding convention (×10); Special P/E discussion for entity creation fee token sales; the rationale for not flooring the SKY denominator. |
