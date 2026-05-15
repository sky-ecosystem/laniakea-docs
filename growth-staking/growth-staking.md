# Growth Staking

**Status:** Draft (synlang-native rewrite)
**Last Updated:** 2026-05-08

---

## TL;DR

Growth Staking aligns SKY governance token holders with ecosystem innovation. SKY stakers must also hold **growth assets** — Synomic Entity governance tokens (Generator, Guardian, Prime, Halo) and Prime junior risk capital (TEJRC) — to unlock staking rewards. Each eligible asset has a **Growth Factor (GF)** that multiplies its contribution to the staking requirement; passive yield wrappers (sUSDS, srUSDS, Halo Units, stUSDS) are excluded.

Every value in the staking-factor calculation enters at **Reference Value** — derived from a global P/E model with governance-set Base P/E, per-stream Modifier and Variance, and a linear-with-caps growth score — never spot market price. This makes the system immune to speculative price swings on either side of the formula. Forfeited rewards (from stakers below 100% staking factor) flow back into the TMF aggregation in `&core.settlement`. The borrow surface for growth stakers is **stUSDS**, a Morpho-pool-style lending product that captures **10% of the borrower spread** as Sky Core revenue.

---

## Translation note (pre-synlang → synomics)

For readers coming from pre-synlang material in `inactive/archive/growth-staking/`:

| Pre-synlang | Post-synlang | Notes |
|---|---|---|
| SGA | USDS | Generator-issued asset; v1 has one Generator (USGE) |
| sSGA | sUSDS | Savings token |
| srSGA, ESRC | srUSDS | Generator senior risk capital (merged naming) |
| stSCST | stUSDS | The lending product, re-specified per §5 below |
| SCST spread / duration / risk-fee | Sky Core revenue (Generator pass-through + stUSDS spread) | See §4.2 |
| Folio Agent | Folio | Already migrated — see [`../synomic-entities/folio.md`](../synomic-entities/folio.md) |
| Sky Agents | Synomic Entities | See [`../synomic-entities/`](../synomic-entities/) |

---

## Section map

| § | Topic |
|---|---|
| 1 | Overview |
| 2 | The Growth Factor |
| 3 | Reward Scaling |
| 4 | Reference Valuation |
| 5 | stUSDS — borrow surface for growth stakers |
| 6 | The Folio |
| 7 | Entity-Internal Growth Staking |
| 8 | Incentive Effects |
| 9 | Anti-Gaming |
| 10 | Synlang Form |
| 11 | Phase 1 Carve-Outs |
| 12 | Open Items |
| 13 | File map |

---

## 1. Overview

Growth Staking is the mechanism by which SKY governance and ecosystem investment are coupled at the protocol level. A SKY holder cannot earn staking rewards by staking SKY alone — they must also hold growth assets that satisfy a staking requirement scaled to their staked SKY. The more directly a growth asset contributes to ecosystem innovation, the higher its Growth Factor.

Eligible growth assets are deliberately limited to instruments that require an individual investment decision and carry meaningful risk: **Synomic Entity governance tokens** (Generator, Guardian, Prime, Halo) and **Prime junior risk capital** (TEJRC). Passive yield wrappers — savings tokens, senior risk capital, Halo Units, stUSDS — are excluded. This keeps Growth Staking pointed at the live edge of innovation rather than at safe carry.

The result is a direct economic link between governance participation (staking SKY) and investment in the ecosystem's equity-like growth layer: passive SKY holders earn nothing; capital must take a position on a specific Synomic Entity to unlock yield.

---

## 2. The Growth Factor

Each eligible growth asset has a **Growth Factor (GF)** — a multiplier on the asset's Reference Value that determines how much it counts toward unlocking staking rewards.

| Category | Assets | Growth Factor | Effect |
|---|---|---|---|
| **Synomic Entity governance tokens** | Generator, Guardian, Prime, Halo | 2.5× | $1 counts as $2.50 |
| **Junior risk capital** | TEJRC (per-Prime) | ~1.67× | $1 counts as $1.67 |

**Excluded assets:** srUSDS (senior risk capital), TISRC, sUSDS, fixed-rate sUSDS, Halo Units (Portfolio / Term / Trading shares), stUSDS, LCTS queue positions, USDS, SKY itself (denominator-only). These are passive holdings that don't require an active investment thesis — Growth Staking is reserved for capital that flows into innovation through individual judgment.

Excluded by entity type: **Core Controlled** and **Recovery** entities are tokenless and explicitly excluded ([`../synomic-entities/core-controlled.md`](../synomic-entities/core-controlled.md), [`../synomic-entities/recovery.md`](../synomic-entities/recovery.md)). **Folios** are tokenless and serve as the staking vehicle — they are not themselves growth assets (§6).

---

## 3. Reward Scaling

Rewards scale linearly from 0% to 100% based on how much of the staking requirement is satisfied. All values use **Reference Values** — fundamentals-based prices that filter out speculative swings (see §4).

```
Staking Factor  = min(1, Σ(Asset Reference Value_i × Growth Factor_i) / SKY Reference Value)

Staking Rewards = Base Staking Yield × Staked SKY × Staking Factor
```

**Example** — a SKY position worth $100k at SKY Reference Value, holding only Prime tokens (GF 2.5×):

| Prime tokens held (Reference Value) | GF-adjusted value | Staking Factor |
|---|---|---|
| $0 | $0 | 0% |
| $20k | $50k ($20k × 2.5) | 50% |
| $40k | $100k ($40k × 2.5) | 100% |

When multiple growth assets are held, each is converted to its GF-adjusted Reference Value and the contributions are summed:

```
Total GF Reference Value = Σ (Asset Reference Value_i × GF_i)
Staking Factor           = min(1, Total GF Reference Value / Staked SKY Reference Value)
```

**Multi-asset example** — $100k staked SKY (Reference Value), holding $20k Spark (governance, GF 2.5×) + $18k Spark TEJRC (GF ~1.67×):

```
GF Value       = ($20k × 2.5) + ($18k × 1.67) = $50k + $30k = $80k
Staking Factor = min(1, $80k / $100k) = 80%
```

If SKY's market price then doubles on speculation while protocol revenue stays flat, the SKY Reference Value is unchanged — this staker still earns 80%, not 40%.

### Forfeited rewards

Stakers below 100% staking factor leave unclaimed rewards on the table. **Forfeited rewards re-enter the Treasury Management Function (TMF) waterfall**, aggregated into `&core.settlement` alongside the rest of Sky's epoch flows. They are not redistributed to fully-qualifying stakers — the design rewards activation, not concentration.

```
Forfeited per epoch = (1 − Staking Factor) × Base Yield × Staked SKY
                   → flows to TMF aggregation in &core.settlement
```

See [`../accounting/settlement-cycle.md`](../accounting/settlement-cycle.md) for the TMF / `&core.settlement` mechanics.

---

## 4. Reference Valuation

All values in the staking factor calculation — both the growth asset numerator and the staked SKY denominator — use **Reference Values** derived from fundamentals rather than spot market prices. This makes the entire Growth Staking system immune to speculative price swings in any token, including SKY itself.

The core principle: if nothing changes about the actual economics of the ecosystem, nothing should change about a staker's reward percentage.

```
Staking Factor = min(1, Total GF Reference Value / Staked SKY Reference Value)
```

Every token enters this formula at its Reference Value, never its spot market price.

### 4.1 Global P/E Model

Reference Values for revenue-generating assets are derived from a **global P/E model** with three governance-set parameters per income stream:

**Global parameter (governance-set):** Base P/E (e.g., 15)

**Per-income-stream parameters:**
- **Modifier** — multiplier on Base P/E to get the center P/E for this income stream
- **Variance** — fractional range around the center P/E
- **Growth score** — converted from trailing revenue growth via a **linear-with-caps** mapping (see below); positions the actual P/E within the variance window

```
Center P/E   = Global Base P/E × Modifier
Band         = Center P/E × Variance
Actual P/E   = Center − Band + (score / 100) × (2 × Band)

Growth score = clamp(growth_rate / target_growth_rate × 100, 0, 100)
```

The growth score is governance-tunable per income stream via `target_growth_rate` (the growth rate that maps to a perfect score of 100). Values below 0% or above 100% are clamped — the linear-with-caps shape is deliberately simple and predictable.

**Trailing revenue window:** **trailing 12 months annualized (T12M)**. This is the default lookback for all P/E inputs. Governance-tunable; shorter windows are more responsive but more volatile. T12M is the chosen balance.

**Example** — Base P/E = 15, Modifier = 1.0, Variance = 0.3, growth rate = 18% against a 24% target:

```
Growth score = clamp(18 / 24 × 100, 0, 100) = 75
Center P/E   = 15 × 1.0 = 15
Band         = 15 × 0.3 = 4.5
Actual P/E   = 15 − 4.5 + (75/100) × (2 × 4.5) = 10.5 + 6.75 = 17.25
```

This model lets governance express views on income quality (Modifier), uncertainty (Variance), and growth momentum (the growth-score mapping), all anchored to a single Base P/E that can be adjusted for market conditions.

### 4.2 SKY Reference Value

SKY is valued using the global P/E model applied to Sky Core's revenue streams:

```
SKY Reference Value = (SKY Core Revenue × Actual P/E
                     + SKY Special Revenue × Special P/E)
                     / SKY Circulating Supply
```

**SKY Core revenue** (standard P/E — Modifier, Variance, growth score as above):
- USDS spread (interest rate margin on USDS credit)
- USDS risk capital fees (fees on srUSDS, TISRC, TEJRC)
- **stUSDS spread** — 10% of borrower spread above base rate (per §5)
- Entity upkeep (50 bps/year on entity token supply; see [`../accounting/entity-fees.md`](../accounting/entity-fees.md))
- Guardian accord fees
- USDS duration income (duration matching revenue)
- 5% share of Generator revenue

**SKY special revenue** (separate Modifier / Variance — typically discounted):
- Synomic Entity creation fee token sales (5% of newly issued entity tokens)

Special revenue receives a separate Modifier (typically < 1.0) because token sale income is lumpy and non-recurring. Governance sets the special Modifier and Variance independently.

Updated at each settlement based on T12M trailing revenue.

**Effect:** If SKY market price doubles on speculation but protocol revenue hasn't changed, the Reference Value stays the same — stakers' staking factors are unchanged. Conversely, if protocol revenue doubles, the Reference Value rises to reflect genuine growth, and stakers naturally need more growth assets to maintain 100%.

### 4.3 Generator Reference Value

Generators are valued as a combination of standard P/E on operating revenue plus book value on stability capital:

```
Generator Reference Value = (Generator Revenue × Actual P/E + ISRC Book Value)
                            / Tokens Outstanding
```

**Generator revenue** (standard P/E — keeps 95% of gross, 5% to Sky Core):
- USDS fees (on USDS and other Generator-issued asset transactions)
- USDS spread (interest rate margin on Generator-issued assets)
- USDS risk capital fees (fees on srUSDS, TISRC, TEJRC)
- USDS duration income (duration matching revenue)

**Generator book value:**
- ISRC holdings (stability capital overflow, SBE dry powder)

ISRC (Internal Senior Risk Capital) is valued at par — no P/E applied to capital reserves.

### 4.4 Guardian Reference Value

Guardians (Ozone is the single operational Guardian — see [`../synomic-entities/guardian.md`](../synomic-entities/guardian.md)) are valued using P/E on operating income plus book value on SKY holdings:

```
Guardian Reference Value = (Accord Fee Income × Actual P/E + SKY Holdings Book Value)
                           / Tokens Outstanding
```

- **Accord fees** — recurring revenue from Guardian Accord relationships with Primes and other entities. Valued via the global P/E model.
- **SKY holdings** — SKY tokens held by the Guardian, valued at SKY Reference Value (book value, no P/E multiplier on holdings).
- **sUSDS** — Used as operational collateral. The sUSDS income feeds the P/E component (as part of accord fee income), but the sUSDS balance itself is not counted as book value to avoid double-counting.

### 4.5 Prime Reference Value

Primes are valued at net capital reserves — no P/E component:

```
Prime Reference Value = Net Capital Reserves / Tokens Outstanding
```

Net capital reserves include look-through to Reference Value for any Halo Synomic Entity tokens the Prime holds.

A Prime holding $500M in capital reserves with 10B tokens outstanding has a Reference Value of $0.05 per token. If the market price is $0.08, the staking factor calculation uses $0.05. If the market price is $0.03, the staking factor calculation uses $0.03 (per the floor in §4.7).

### 4.6 Halo Reference Value

Halos are valued using capital reserves plus earnings:

```
Halo Reference Value = (Capital Reserves + Annual Earnings × Actual P/E)
                       / Tokens Outstanding
```

Earnings are valued via the global P/E model. Capital reserves are valued at par.

**Early-stage Halos:** A newly capitalized Halo with no earnings history can still count toward the favorable Synomic Entity token Growth Factor — provided its synomic artifacts demonstrate that the capital is being actively spent on genuine growth (building technology, deploying infrastructure, etc.). This is a qualitative assessment based on observable synomic activity, not just capital sitting idle. Once earnings materialize, the P/E component takes over as the primary value driver.

### 4.7 Synomic Entity Token Floor

Synomic Entity tokens are valued at the **lower of Reference Value or market value**:

```
Effective Value = min(Reference Value, Market Value)
```

The min() floor ensures that if an Synomic Entity token's market price collapses below fundamentals (distressed sale, illiquidity), the staking factor calculation reflects the worse reality.

The asymmetry is deliberate: you can't inflate growth asset values by pumping, but genuine impairment does reduce your staking factor credit. SKY uses Reference Value directly (not min) because the denominator should be stable — a SKY dump shouldn't make it trivially easy to earn full rewards.

### 4.8 TEJRC

TEJRC is valued at its on-chain redemption value — no Reference Value adjustment needed, since the token is directly backed by underlying capital at a known ratio.

### 4.9 Tokenized vs Tokenless

Not all Synomic Entities participate in Growth Staking as growth assets:

| Entity | Tokenized | Growth Asset |
|---|---|---|
| **Guardian** (Ozone) | Yes | Yes (governance token GF 2.5×) |
| **Prime** | Yes; also issues TISRC, TEJRC | Yes (governance token GF 2.5×, TEJRC GF ~1.67×; TISRC excluded) |
| **Generator** | Yes; also issues srUSDS, sUSDS, fixed-rate sUSDS, stUSDS | Yes (governance token GF 2.5×; all other issued tokens excluded) |
| **Halo** | Yes; also issues Halo Units | Yes (governance token GF 2.5×; Halo Units excluded) |
| **Core Controlled** | No | No |
| **Recovery** | No | No |
| **Folio** | No | No (is the staking vehicle) |

### 4.10 Why Reference Values Throughout

Using fundamental values on both sides of the staking factor formula creates a system where the staking relationship reflects real economic reality:

| Scenario | Market price effect | Staking factor effect |
|---|---|---|
| SKY pumps speculatively | SKY market price rises | No change — SKY Reference Value unchanged |
| Synomic Entity token pumps speculatively | Synomic Entity market price rises | No change — Synomic Entity Reference Value unchanged |
| Protocol revenue grows | SKY Reference Value rises | Stakers need more growth assets — correct, the ecosystem is bigger |
| Prime deploys more capital | Prime Reference Value rises | Staker gets more GF credit — correct, real capital at work |
| SKY dumps on panic selling | SKY market price falls | No change — SKY Reference Value unchanged |
| Synomic Entity token dumps | Synomic Entity market price falls below Reference | Staking factor uses market price (per §4.7 floor) — correct, reflects real impairment |

---

## 5. stUSDS — borrow surface for growth stakers

**stUSDS** is a Morpho-pool-style lending product that creates a borrow surface for growth stakers and a yield surface for USDS holders. It plays two roles simultaneously: passive yield instrument for depositors, and leverage instrument for growth stakers who want to scale up their growth-asset exposure.

### Two sides

| Side | Action | Mechanics |
|---|---|---|
| **Depositor** | Deposits USDS, receives stUSDS shares | ERC-4626-like; share price reflects accrued interest |
| **Borrower** | Posts eligible collateral, draws USDS at variable rate | Morpho-pool utilization-based rate model |

**Eligible collateral** *(open — confirm in governance)*: growth assets in the borrower's Folio (Synomic Entity governance tokens, TEJRC) plus staked SKY. Borrowing supports leveraged growth-asset accumulation — borrowers use the proceeds to acquire more GF-eligible assets, raising their staking factor.

### Rate model

```
Borrow Rate  = Base Rate + Spread(utilization)

Lender Rate  = (Spread × 0.90) × utilization              ; 90% to depositors
Sky Core Fee = (Spread × 0.10) × utilization × notional   ; 10% to Sky Core
```

The Sky Core fee is the **stUSDS spread** referenced as a Core revenue line in SKY Reference Value (§4.2). It is captured by Sky Core, not by the Generator — stUSDS is operated as a Generator-adjacent lending product, but the spread fee is an independent stream from USDS spread / risk-capital fees.

### Eligibility and exclusion

- **stUSDS itself is excluded from growth-asset eligibility.** It is a passive yield wrapper for the depositor — the underlying USDS earns interest, but holding stUSDS doesn't require an active investment thesis. Excluded for the same reason sUSDS, srUSDS, and Halo Units are.
- **Other Generators (multi-Generator future)** follow the same pattern: staked variants of each Generator's primary asset (e.g., a hypothetical stEURS) would be excluded by the same rule. The exclusion is structural, not USDS-specific.

### Open items (deferred to writeup-time / governance, not blocking)

- Exact eligible-collateral set: Prime tokens? TEJRC? Staked SKY? All of the above?
- Liquidation mechanics under collateral collapse
- Base-rate reference: USGE base rate vs Sky Savings Rate vs other?

A future `smart-contracts/stusds.md` can be promoted later if needed; this migration does not write a smart-contract spec for stUSDS.

---

## 6. The Folio

To participate in Growth Staking, a SKY holder creates a **Folio** — a standardized rank-3 holding structure that serves as a self-contained staking and investment vehicle. See [`../synomic-entities/folio.md`](../synomic-entities/folio.md) for the full operational spec.

Key properties:
- **Instant creation** via auto-accord — any SKY holder
- **Tokenless**, single owner (the principal), no Halo Units
- **PAU-based** — holds staked SKY + growth-asset portfolio
- **Two operating modes** — automated (sentinel formation) or principal control (principal sentinel)
- **Type 1 Restructure** — graduate to Standard Halo or Prime when ready (see [`../synomic-entities/creation-restructuring.md`](../synomic-entities/creation-restructuring.md))

The Folio reads its staking factor from synserv-derived atoms (see §10) and receives reward distributions at each settlement boundary.

---

## 7. Entity-Internal Growth Staking

Primes and Halos that hold SKY in their treasuries automatically earn Growth Staking rewards — the Synomic Entity's own book value counts as its growth-asset portfolio at GF 2.5×. No separate Folio is needed; the Synomic Entity itself functions as one.

A Prime effectively counts as a SKY staker with all of its own tokens in its Folio. Same for a Halo holding SKY.

**Example** — A Prime with $500M Reference Value holding SKY worth $10M at SKY Reference Value:

```
GF Reference Value = $500M × 2.5 = $1.25B effective
Staking Factor on $10M SKY = min(1, $1.25B / $10M) = 100%
```

Any Synomic Entity with meaningful book value trivially satisfies the growth requirement, making SKY holdings essentially free yield for Synomic Entities. This creates a structural incentive for Primes and Halos to accumulate SKY in their treasuries — aligning Synomic Entity operations with protocol governance and creating natural demand for SKY from the innovation layer itself.

### Double-counting

This creates an accepted paradox: a Synomic Entity's book value is used twice for staking factor purposes — once by the Synomic Entity itself (to unlock staking rewards on its own SKY holdings), and a second time by external token holders (who hold the Synomic Entity's tokens as growth assets in their Folios). The same underlying book value supports both claims. This is by design — the double-counting amplifies the incentive to build genuine book value within Synomic Entities, and the protocol accepts this as a worthwhile tradeoff for the alignment it creates.

---

## 8. Incentive Effects

### Capital flow from passive to active

Growth Staking creates a direct incentive to convert passive holdings into active innovation investment:

```
$100k sUSDS (or other passive holding) → GF value: $0 (excluded)
    ↓ invest into a Prime
$100k in Prime tokens                  → GF value: $100k × 2.5 = $250k effective
```

Holding savings tokens, senior risk capital, Halo Units, or stUSDS earns no staking factor. Stakers who want rewards must take a position on a specific Synomic Entity — picking which Prime, Halo, Generator, or Guardian to back, or which Prime's first-loss tranche (TEJRC) to underwrite.

### Ecosystem alignment

- **SKY whales** must become active ecosystem participants — passive governance holders earn nothing
- **Synomic Entity token demand** is structurally supported by stakers seeking efficient GF
- **Junior risk capital supply** increases as stakers underwrite specific Primes via TEJRC for GF credit
- **Mercenary staking** is eliminated — holding SKY alone earns nothing, and neither does parking capital in passive yield wrappers

### Natural segmentation

- **Concentrated stakers** → hold Synomic Entity governance tokens (GF 2.5×) → maximum capital efficiency, full equity exposure to a chosen Synomic Entity
- **Underwriters** → hold one or more Primes' TEJRC (GF ~1.67×) → first-loss exposure to a specific Prime's book without governance responsibility
- **Mixed** → blend governance tokens and TEJRC across Synomic Entities to express a portfolio thesis
- **Leveraged stakers** → borrow USDS via stUSDS against existing growth assets to increase position size

There is no passive tier. Earning Growth Staking rewards requires picking specific Synomic Entities to back.

---

## 9. Anti-Gaming

The primary defense against manipulation is the **Reference Valuation framework** — market price movements don't affect the staking factor calculation in either direction. You cannot inflate staking factor value by pumping Synomic Entity token prices, and you cannot reduce your staking factor requirement by pumping SKY.

A secondary concern is **hollow entities** — Primes or Halos created solely to warehouse capital and claim favorable GF without genuine innovation activity. Defenses:

1. **Mechanical (day one):** Reference Values are based on actual capital reserves (Primes) or earnings (Halos), so capital must be genuinely deployed or revenue genuinely earned.
2. **Synomic monitoring (when needed):** Governance can monitor the synomic artifacts of Primes and Halos. A real level of intelligent synomic activity must be observed for a Synomic Entity's tokens to maintain GF eligibility. This monitoring layer is deferred — implemented only when manipulation attempts actually occur.

The same monitoring applies to potentially hollow TEJRC positions.

---

## 10. Synlang Form

Following the patterns in [`../noemar-synlang/topology.md`](../noemar-synlang/topology.md) §6 (synome-root layers) and the synlang-form template in [`../accounting/duration-allocation.md`](../accounting/duration-allocation.md) §11.

### Where parameters live

```metta
;; &core.framework.valuation              ← NEW Space (governance-set)
   (base-pe $value)                        ; global Base P/E
   (pe-modifier $stream $value)            ; per-income-stream
   (pe-variance $stream $value)
   (growth-score-target $stream $value)    ; for linear-with-caps mapping
   (revenue-trailing-window months 12)     ; T12M default
   (growth-factor entity-governance 25)     ; GF 2.5× (×10 for int math)
   (growth-factor tejrc 17)                ; GF ~1.67×
   (forfeit-target tmf-waterfall)          ; forfeited rewards → TMF

;; &core.framework.fee                     ← existing
   (stusds-sky-core-share 10)              ; 10% of borrower spread
   (stusds-base-rate $value)               ; governance-set in v1
```

### Where derived values land

```metta
;; &entity.{type}.{id}.root
   (reference-value $entity $value $epoch)            ; per-entity RefValue

;; &entity.folio.{id}.root
   (staking-factor $folio $value $epoch)              ; per-folio
   (gf-portfolio-value $folio $value $epoch)

;; &core.settlement
   (epoch-staking-rewards-paid $amount)
   (epoch-staking-rewards-forfeited $amount)          ; flows to TMF aggregation
```

### What synserv computes (in-space calculation per `beacon-framework.md` §4)

1. Per epoch: T12M revenue per income stream, per entity
2. Per epoch: growth score = `clamp(actual / target × 100, 0, 100)`
3. Per epoch: actual P/E per stream via the formula in §4.1
4. Per epoch: Reference Value per entity (per-entity formulas in §4.3–§4.6)
5. Per Folio per epoch: GF-adjusted portfolio value (Σ across held growth assets)
6. Per Folio per epoch: staking factor = `min(1, GF value / staked SKY RefValue)`
7. Per Folio per settlement: rewards paid = `base yield × staked × factor`
8. Per epoch global: forfeited = `(1 − factor) × base yield × staked`, summed across folios → emitted to `&core.settlement` for TMF aggregation

The settlement-cycle integration is a per-epoch closure step alongside the existing five-step Prime closure (see [`../accounting/settlement-cycle.md`](../accounting/settlement-cycle.md)).

---

## 11. Phase 1 Carve-Outs

Growth Staking activates after Phase 1 — see [`../roadmap/README.md`](../roadmap/README.md) for the phase progression. Phase 1 itself emits real-time ER per Prime as the deliverable; staking rewards are not yet distributed via synserv.

When Growth Staking does activate, the following are sudo-set carve-outs (per the `roadmap-ideas.md` insyn/exsyn pattern and lift principle):

- **All P/E parameters** — Base P/E, per-stream Modifiers, Variances, growth-score targets — sudo-set at the activation boundary in `&core.framework.valuation`
- **Trailing revenue figures** — insyn for active synomic Primes (real synlang on real Primebook positions); **exsyn-oracle** for legacy core vaults / PSM during transition. Ratio shifts toward all-insyn as more halos migrate (the exsyn number shrinks, synlang code unchanged)
- **Hollow-entity monitoring** — deferred; no rule atoms in v1. Activated only if manipulation attempts emerge
- **stUSDS borrow rate** — governance-set in v1, becomes utilization-driven in a later phase when `&core.loop.stusds` activates
- **Growth Factor values** — sudo-set at activation; governance-tunable thereafter

Each adjustment is a topology delta (sudo write into the relevant `&core.framework.*` Space), not a code rewrite.

---

## 12. Open Items

These remain open for the next governance pass; they don't block the spec.

- **Growth Factor revision cadence and authority** — quarterly governance vote? Derived from on-chain metrics?
- **Base P/E revision cadence** — how often is the global Base P/E revisited?
- **Measurement timing** — snapshot at settlement boundary, or time-weighted average to prevent flash-positioning?
- **New Synomic Entities with no history** — a new Prime with zero capital reserves or a new Halo with zero earnings has zero Reference Value. Likely intended ("prove value before getting GF credit") — confirm.
- **stUSDS exact collateral set, liquidation mechanics, and base-rate reference** — see §5
- **Hollow-entity synomic monitoring rule shapes** — defined when needed
- **Reference Value divergence** — what happens if SKY market price diverges extremely from Reference Value (e.g., 10× above or below)? Purely informational, or governance-triggered recalibration?

---

## 13. File map

| Doc | Relationship |
|---|---|
| [`README.md`](laniakea-docs/growth-staking/README.md) | Growth Staking directory index |
| [`../synomic-entities/folio.md`](../synomic-entities/folio.md) | Folio — required vehicle for Growth Staking participation |
| [`../synomic-entities/prime.md`](../synomic-entities/prime.md) | Prime Reference Value (§4.5) |
| [`../synomic-entities/generator.md`](../synomic-entities/generator.md) | Generator Reference Value (§4.3); USDS / srUSDS naming |
| [`../synomic-entities/guardian.md`](../synomic-entities/guardian.md) | Guardian Reference Value (§4.4); Ozone single operational guardian |
| [`../synomic-entities/halo-classes.md`](../synomic-entities/halo-classes.md) | Halo Reference Value (§4.6); Halo Units excluded from growth assets |
| [`../synomic-entities/creation-restructuring.md`](../synomic-entities/creation-restructuring.md) | Type 1 Restructure — Folio → Halo / Prime |
| [`../synomic-entities/core-controlled.md`](../synomic-entities/core-controlled.md) | Excluded from Growth Staking (tokenless rank-1) |
| [`../synomic-entities/recovery.md`](../synomic-entities/recovery.md) | Excluded from Growth Staking (tokenless rank-1) |
| [`../accounting/settlement-cycle.md`](../accounting/settlement-cycle.md) | Reward distribution, forfeited-reward flow into TMF aggregation in `&core.settlement` |
| [`../accounting/capital-stack.md`](../accounting/capital-stack.md) | TEJRC / srUSDS / sUSDS naming and the capital tranches Growth Staking references |
| [`../noemar-synlang/topology.md`](../noemar-synlang/topology.md) | Synome root layering and `&core.framework.*` naming convention used in §10 |
| [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) | In-space calculation pattern referenced in §10 |
| [`../roadmap/README.md`](../roadmap/README.md) | Phase progression — Growth Staking activates post-Phase-1 |
| [`../roadmap/phase-1-spaces.md`](../roadmap/phase-1-spaces.md) | Phase 1 carve-out pattern; `&core.framework.*` Space layout |

---

## One-line summary

**Growth Staking conditions SKY staking rewards on holdings of growth assets (Synomic Entity governance tokens at GF 2.5×, TEJRC at GF ~1.67×) measured at fundamentals-based Reference Values from a global P/E model with linear-with-caps growth scores and a T12M trailing window — with stUSDS as a Morpho-pool borrow surface for leverage (10% of borrower spread to Sky Core), Folios as the entry vehicle, forfeited rewards flowing to the TMF, and the whole thing implemented in synlang as governance facts in `&core.framework.valuation` plus synserv-computed Reference Values, staking factors, and reward atoms — with Phase 1 carve-outs limited to sudo-set P/E parameters and exsyn-oracle gap-filling for legacy revenue.**
