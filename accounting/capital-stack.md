# Capital Stack

**Status:** Draft (synlang-native rewrite)
**Last Updated:** 2026-05-07

---

## TL;DR

This doc is the **TRC funding side** of the Prime capital math. The Risk Framework (`risk-framework/capital-formula.md`) outputs **TRRC** — Total Required Risk Capital. This doc defines how Primes hold capital that satisfies that requirement: the four tranches (IJRC / EJRC / SRC / MDC), the universal **ingression curve** that translates nominal capital into effective capital recognized for leverage, the **MC-based total RC cap** that ties leverage to market validation of the Prime token, the temporary **Genesis Capital** bootstrap layer, and the **insolvency defense hierarchy** (the multi-level loss waterfall behind USDS). All of this is orthogonal to TRRC computation: ingression decides how much external capital counts; loss absorption uses **nominal** capital. ORC (Operational Risk Capital) and ASC (Active Stability Capital) sit on parallel tracks and are pointed to, not duplicated here.

---

## Section map

| § | Topic |
|---|---|
| 1 | The four capital tranches |
| 2 | The universal ingression curve |
| 3 | SRC ingression |
| 4 | EJRC ingression |
| 5 | Duration mechanics |
| 6 | Tokenized EJRC (normie TEJRC) |
| 7 | MC-based total RC cap |
| 8 | Genesis Capital |
| 9 | Guardian Agent capital structure |
| 10 | Insolvency defense hierarchy |
| 11 | 21% → 10% S&M Budget transition |
| 12 | Capital adequacy formula |
| 13 | ORC and ASC parallel tracks |

---

## 1. The four capital tranches

A Prime's capital base composes from four tranches with distinct loss-absorption behavior:

```
IJRC + EJRC   (pari passu, proportional to nominal)   ← going-concern first loss
Prime Token   (forced inflation before liquidation)    ← recapitalization
────────────────────────────────── liquidation threshold
MDC           (subordinated claim in liquidation)      ← liquidation residual
SRC           (senior claim in liquidation)            ← liquidation senior
```

| Tranche | Full name | Source | Role |
|---|---|---|---|
| **IJRC** | Internal Junior Risk Capital | The Prime's own capital | First-loss in going-concern |
| **EJRC** | External Junior Risk Capital | External providers (LCTS or bespoke) | First-loss alongside IJRC, pari passu by nominal |
| **SRC** | Senior Risk Capital | srUSDS holders (governance-allocated; auction-allocated post-Phase 9) | Senior in liquidation; sits behind JRC + Prime Token in going-concern |
| **MDC** | Mezzanine Deployment Capital (speculative) | Isolated capital only (TISRC-style) | Not a leverage instrument — direct 1:1 deployment; subordinated to SRC in liquidation, senior to JRC in liquidation only |

**Going-concern loss sequence:**
1. Operating losses absorbed by JRC (IJRC + EJRC, proportional to nominal — see "Ingression vs loss absorption" below)
2. If JRC exhausted, Prime Token inflated until the hole is covered or the market stops buying
3. If inflation can't cover, Prime liquidates

**Liquidation:** SRC paid first; MDC receives the residual; JRC and Prime Token holders get nothing (their claims were extinguished going-concern).

**Ingression vs loss absorption.** The ingression rate determines how much *leverage* a Prime can take — it is a capital adequacy measure. Loss absorption uses **nominal** capital. If a Prime has $100M nominal EJRC, the full $100M absorbs losses regardless of the ingression-adjusted effective value.

---

## 2. The universal ingression curve

All ingression uses the same curve shape: a flat zone followed by a quarter circle.

```
Marginal
Rate
      |
      |
 1.0  |====================-----------_____
      |                                    ----___
      |                                          ---__
      |                                               --_
      |                                                  -_
      |                                                    -
      |                                                     \
      |                                                      \
      |                                                       \
      |                                                        |
 0.0  +---------------------|----------------------------------|-----> Capital
      0                  anchor                               max
      |------- flat --------|------------ curve ---------------|
      |-------- 1x ---------|--------------- 2x ---------------|
```

**Three zones:**

| Zone | Range | Marginal rate |
|---|---|---|
| Flat | 0 to anchor | 1.0 (full ingression) |
| Curve | anchor to max | √(1 − ((x − anchor) / (max − anchor))²) |
| Cap | beyond max | 0 |

```
For x ≤ anchor:    marginal_rate = 1.0
For anchor < x ≤ max: marginal_rate = √(1 − ((x − anchor) / (max − anchor))²)
For x > max:       marginal_rate = 0
```

**Properties:**
- Smooth transition at anchor (tangent horizontal, no kink)
- Steepens progressively toward max
- Vertical at max (marginal rate hits zero)
- Max effective capital = anchor + (max − anchor) × π/4

The same shape governs SRC ingression, EJRC ingression, and the MC-based cap, all with a 3:1 max:anchor ratio.

---

## 3. SRC ingression

SRC ingression rate depends on the Prime's effective JRC base.

| Parameter | Value |
|---|---|
| Anchor | 1.5 × effective JRC |
| Max | 4.5 × effective JRC |
| Ratio | 3:1 |

### Example with $100M effective JRC

| SRC : JRC | SRC nominal | Marginal rate | Cumulative effective | Efficiency |
|---|---|---|---|---|
| 0.5 : 1 | $50M | 100% | $50M | 100% |
| 1 : 1 | $100M | 100% | $100M | 100% |
| 1.5 : 1 | $150M | 100% | $150M | 100% |
| 2 : 1 | $200M | 98.6% | $199.8M | 99.9% |
| 2.5 : 1 | $250M | 94.3% | $248.1M | 99.2% |
| 3 : 1 | $300M | 86.6% | $293.5M | 97.8% |
| 3.5 : 1 | $350M | 74.5% | $334.0M | 95.4% |
| 4 : 1 | $400M | 55.3% | $366.9M | 91.7% |
| 4.5 : 1 | $450M | 0% | $385.6M | 85.7% |
| 5 : 1 | $500M | 0% | $385.6M | 77.1% |

Max theoretical effective SRC = 1.5 × JRC + 3 × JRC × π/4 ≈ **3.86 × effective JRC**.

---

## 4. EJRC ingression

EJRC ingression depends on two quality dimensions: **synomic status** and **duration commitment**.

### EJRC types

| Type | Synomic | Duration | Mechanism |
|---|---|---|---|
| Normie TEJRC | No | Zero | LCTS token; anyone can participate |
| Non-synomic duration | No | Yes | Bespoke; funds → SubProxy; ecosystem accord in entart |
| Synomic duration | Yes | Variable | Bespoke between synomic entities; baseline sentinels interact |

### Quality dimensions

**Synomic status** — whether the egression decision was made by a framework encoded in the synome:
- Non-synomic: 1× multiplier
- Synomic: 2× multiplier on anchor and max

**Duration commitment** — how long capital is committed before exit:
- Maximum useful duration: 24 months
- Minimum threshold: 3 months (below this, no duration credit)
- Linear scaling 3 → 24 months

### Anchor / max formula

```
duration_multiplier = 1 + (months / 24)    for months ≥ 3
duration_multiplier = 1                     for months < 3

synomic_multiplier = 2    if synomic, 1 otherwise

anchor = 1 × IJRC × synomic_multiplier × duration_multiplier
max    = 3 × IJRC × synomic_multiplier × duration_multiplier
```

### Ingression table

| Type | Duration | Duration mult | Anchor | Max |
|---|---|---|---|---|
| Non-synomic | 0–3mo | 1.0 | 1× | 3× |
| Non-synomic | 3mo | 1.125 | 1.125× | 3.375× |
| Non-synomic | 6mo | 1.25 | 1.25× | 3.75× |
| Non-synomic | 12mo | 1.5 | 1.5× | 4.5× |
| Non-synomic | 24mo | 2.0 | 2× | 6× |
| Synomic | 0–3mo | 1.0 | 2× | 6× |
| Synomic | 3mo | 1.125 | 2.25× | 6.75× |
| Synomic | 6mo | 1.25 | 2.5× | 7.5× |
| Synomic | 12mo | 1.5 | 3× | 9× |
| Synomic | 24mo | 2.0 | 4× | 12× |

---

## 5. Duration mechanics

EJRC can be structured two ways:

| Structure | Mechanics | Exit |
|---|---|---|
| Perpetual until called | Runs indefinitely | Call → countdown → exit |
| Fixed term | Agreed start-to-end duration | Auto-exits at end |

**Synlang reframing:** duration commitments live as cert-bearing facts in the Prime's entart subtree. The capital provider's commitment, the agreed uningression delay, and the current countdown state are all atoms in `&entity.prime.{id}.root` (or a sub-Space the govops-prime beacon manages). The synlang reads these to compute `duration_multiplier` for ingression purposes and to enforce the exit countdown.

### Uningression delay

The countdown after exit is called. Agreed upfront; determines load (quality):

| Uningression delay | Effect on load |
|---|---|
| 24 months (max) | Lowest load, highest quality |
| 12 months | Medium load |
| 6 months | Higher load |
| 3 months (min for credit) | Highest load with duration credit |
| < 3 months | No duration credit |

If the agreed uningression delay is short, the perpetual phase load is as if you're always at that point in the countdown. Load is constant; capital doesn't get dumber as time passes.

### Exit mechanics

Either party can initiate. **Egressor instant exit** never allowed (abuse risk — coordinated attacks). **Prime instant release** only if negotiated upfront (e.g., to swap to cheaper EJRC).

---

## 6. Normie TEJRC (tokenized EJRC)

TEJRC is the standard tokenized form of EJRC, accessible via LCTS.

| Operation | Mechanics |
|---|---|
| Subscribe (ingression) | Prime pulls from LCTS SubscribeQueue at will; no rate limit on ingression |
| Redeem (uningression) | Prime sets redemption rate (e.g., 20%/week max) + minimum fixed amount; rate changes require governance + long delay (TEJRC holder protection) |

TEJRC is always **non-synomic** and **zero duration** — anchor = 1× IJRC, max = 3× IJRC. The lowest-quality EJRC, but the most accessible.

For LCTS queue mechanics, see `inactive/pre-synlang/smart-contracts/lcts.md` (pending its own synlang-native rewrite).

---

## 7. MC-based total RC cap

Total effective ingression (IJRC + EJRC + SRC) is capped by the Prime token's market metrics. A Prime's capital is only as credible as the market believes the Prime is — if the token is worthless or illiquid, "skin in the game" is meaningless.

### Effective MC calculation

Each metric converts to an **equivalent MC** via a multiplier. Effective MC is the **minimum** across all metrics (worst-of-observed):

```
effective_MC = min(actual_MC,
                   weekly_adv × 100,
                   monthly_adv × 125,
                   quarterly_adv × 167,
                   monthly_turnover × MC × 29,
                   quarterly_turnover × MC × 15,
                   yearly_turnover × MC × 10)
```

| Metric | Healthy level | Multiplier |
|---|---|---|
| Weekly ADV | 1.0% of MC | ×100 |
| Monthly ADV | 0.8% of MC | ×125 |
| Quarterly ADV | 0.6% of MC | ×167 |
| Monthly turnover | 3.5% of supply | ×29 |
| Quarterly turnover | 6.5% of supply | ×15 |
| Yearly turnover | 10% of supply | ×10 |

Why "worst of": all signals must be healthy. One weak link caps everything.

| Scenario | What it catches |
|---|---|
| High MC + low volume | Illiquid, price stale |
| High volume + low turnover | Wash trading |
| High turnover + low MC | Token not market-valued |

These metrics are **market-data + attest-data exsyn inputs** in Phase 1 (exchange APIs, on-chain DEX state, perp venues). The data lands in a governance-set sub-Space (e.g., `&core.framework.prime-token-metrics`) where `effective_MC` is derived per Prime. The architecture is in place; the live wiring matures with Phase 1+ market-data / attest-data beacon deployments.

### MC-based ingression curve

| Parameter | Value |
|---|---|
| Anchor | 5 × effective MC |
| Max | 15 × effective MC |
| Ratio | 3:1 |

Same flat + quarter-circle shape. Max theoretical total RC = 5 + 10 × π/4 ≈ **12.85 × effective MC**.

### Worked example: bottleneck identification

Prime with the following metrics:

| Metric | Raw value | Multiplier | Equivalent MC |
|---|---|---|---|
| Actual MC | $200M | — | $200M |
| Weekly ADV | $1.5M (0.75%) | ×100 | $150M |
| Monthly ADV | $1.2M (0.6%) | ×125 | $150M |
| Quarterly ADV | $1.0M (0.5%) | ×167 | $167M |
| Yearly turnover | 8% | ×10 | $160M |

```
effective_MC = min($200M, $150M, $150M, $167M, $160M) = $150M
```

Bottleneck: weekly and monthly ADV are below healthy levels. Total effective RC ≤ ~$1.93B theoretical max.

### Independent trader registry (future)

A planned additional metric: **independent trader participation** — reputation based on profitable Prime token trading across *multiple* Primes. A trader who only trades one Prime's token could be an insider; cross-Prime trading signals genuine price discovery. Adds another equivalent MC to the worst-of calculation. Not yet implemented.

---

## 8. Genesis Capital

**Genesis Capital** is a temporary mechanism designed to bootstrap Sky's agent ecosystem. Allocated from Sky Core into Genesis Agents to seed diversity and innovation; remains as backstop capital within the system. Genesis Capital allocation is **not an expense** — it's a capital deployment.

| Term | Definition |
|---|---|
| **Allocated Genesis Capital** | Specific funds deployed to Genesis Agents — primary purpose: bootstrap. Subtracted when calculating safety margin. |
| **Aggregate Backstop Capital** | The safety net: `Total Genesis Capital − Allocated Genesis Capital`. Excess capital backing USDS beyond standard collateral. |
| **Genesis Capital Backstop Mechanism** | The portion held by Genesis Agents that Sky can reclaim as a last line of defense (Defense Level 3 — see §10). |

The Core Council Buffer was previously included in the ABC formula; it has been reclassified as operational capital. (Reclassification details are out-of-band during transition; not currently documented in the corpus.)

### Capital target and revenue retention

| Item | Value |
|---|---|
| Phase 1 ABC target | $125M (Phase 1 safety floor; up from current $37M) |
| Long-term target (post-Genesis) | 1.5% of total USDS supply (per the TMF — see whitepaper Appendix C) |
| Revenue retention requirement | 25% of net revenue after S&M allocation, every monthly settlement, until target reached |

When the $125M target is reached:
- Minimum retention requirement ceases
- TMF allocations shift primarily toward staking rewards
- Smart Burn Engine can operate at full capacity

### Phase-out logic

Genesis Capital is temporary — intended to be in place during 2026 and 2027. Phased out by Genesis Agents that have launched liquid tokens with at least $10M average daily volume.

```
At each Monthly Settlement:
  IF a Genesis Agent has had an actively launched token
     with average daily volume ≥ $10M during the past month
  AND IF Aggregate Backstop Capital ≥ $50M
  THEN the Genesis Agent phases out $1M of Genesis Capital
  ADDITIONAL: +$1M phased out for every $10M of ABC above $50M
```

**Example:** Two Genesis Agents with fully liquid tokens; ABC at $58M. Each phases out $1M (total $2M); ABC drops to $56M. Next month, if ABC grows to $64M, each phases out $2M.

**Key principle:** Total Genesis Capital can only go DOWN over time, eventually reaching full phase-out and removal of the mechanism.

### The nine Genesis Agents

The number was consolidated to simplify and accelerate the Genesis phase. Reconciles with the rank hierarchy in `macrosynomics/synomic-entities.md`: Ozone is the single operational Guardian (Rank 1); Star Primes and the Institutional Prime are direct children of Ozone (Rank 2); Halos sit below Primes (Rank 3).

**Five Genesis Star Primes:**
1. **Spark** — already capitalized
2. **Grove** — DeFi credit infrastructure
3. **Keel** — ecosystem development
4. **Star 4** — unannounced (Q1 2026)
5. **Star 5** — unannounced (Q1 2026)

**One Genesis Institutional Prime:**
- **Obex** — already capitalized

**Three Genesis Guardian Agents** — distinct from governance Guardians (see `inactive/pre-synlang/whitepaper/appendix-f-glossary.md` "Guardian Role Mapping"); slated to receive $25M each in Genesis Capital.

**No other agents beyond this group will receive Genesis Capital.**

| Metric (Q1 2026) | Estimate |
|---|---|
| Currently allocated Genesis Capital | Spark + Obex |
| Remaining to allocate | 7 agents |
| Projected total Allocated Genesis Capital | ~$120M |
| Projected ABC (Q1) | $50–60M range |

---

## 9. Guardian Agent capital structure

Each of the three Guardian Agents receives $25M in Genesis Capital.

### Ring-fenced buffers (per planned Ecosystem Accords)

- **$20M per agent** ring-fenced as a Core Council and GovOps Support Buffer.

The buffer must be spent entirely in support of Sky Ecosystem development before Guardians may use internal capital for token buybacks or staking rewards. Before it is spent, the buffer can still serve as Operational Risk Capital for the Guardian's Guardian Accords (dual-use).

### Two goals

1. **Core Council transition.** Provide resources for the Core Council to transition off the 21% Genesis Phase S&M Budget without leaning on SFF. Frees SFF to invest in long-term revenue-generating and cost-reducing assets.
2. **Bootstrap GovOps.** Build operational GovOps capabilities without charging Guardian Accord Fees from Primes during the Genesis Phase. Gives GovOps teams and Guardians runway to build service capabilities before negotiating medium-term Accords.

---

## 10. Insolvency defense hierarchy

Four levels:

### Level 1: Aggregate Backstop Capital

If a Star Prime's losses exceed its collateral, ABC absorbs first.

### Level 2: SKY token inflation

If ABC goes negative after one or more Synomic Entities are fully liquidated, SKY tokens are inflated to cover the shortfall.

### Level 3: Genesis Capital Backstop Mechanism

If SKY price collapses to zero and cannot generate further funding, Sky reclaims capital from Genesis Agents through the backstop mechanism.

If reclaimed capital is sufficient: Genesis Agent token holders (who covered the loss after SKY was diluted to zero) receive an airdrop of the new SKY supply.

### Level 4: USDS haircut (final resort)

If the Genesis backstop is insufficient, the final loss is socialized among USDS holders via a haircut.

USDS holders receive the airdrop of the new SKY supply, allowing them to configure the system to use future returns to recover the original 1:1 USDS peg.

### Relationship to the 7-step waterfall

The whitepaper specifies a more granular **7-step loss absorption waterfall**. The 4-level view above is a Genesis-Capital-perspective simplification:

| 7-step waterfall (whitepaper) | 4-level view |
|---|---|
| 1. FLC (First Loss Capital) | Level 1 (ABC) |
| 2. JRC (Junior Risk Capital) | Level 1 (ABC) |
| 3. Agent Token Inflation | Level 1 (ABC) |
| 4. SRC Pool | Level 1 (ABC) |
| 5. SKY Token Inflation | Level 2 |
| 6. Genesis Capital Haircut | Level 3 |
| 7. USDS Peg Adjustment | Level 4 |

For the canonical 7-step treatment, see `inactive/pre-synlang/whitepaper/sky-whitepaper.md` Part 6.

---

## 11. 21% → 10% S&M Budget transition

| State | Cap |
|---|---|
| Current (Genesis Phase) | 21% of net revenue |
| Target (post-Genesis) | 10% of net revenue |

Transition expected before end of 2026. Once established, the **10% upper limit becomes permanent and cannot be increased** — a substantial boost to long-term protocol profitability and a hard structural commitment to cost control.

---

## 12. Capital adequacy formula

For Prime capital adequacy:

```
Effective JRC = IJRC + Σ(EJRC_i × EJRC_ingression_rate_i)

Effective SRC = Σ(SRC_j × SRC_ingression_rate_j)

Total Risk Capital (TRC) = (Effective JRC + Effective SRC) × MC_multiplier

Capital Adequacy: TRC ≥ TRRC
```

Where TRRC comes from `risk-framework/capital-formula.md` (duration matching, gap risk, sub-book composition, concentration penalties).

The encumbrance ratio target is `ER = TRRC / TRC ≤ 0.90`. Breach drives penalties at settlement (see [`settlement-cycle.md`](settlement-cycle.md) §6).

This formula covers **portfolio risk capital only**. ORC and ASC sit on parallel tracks (§13).

---

## 13. ORC and ASC parallel tracks

**Operational Risk Capital (ORC).** Operational, rather than portfolio, risk. Sized by `Rate Limit × TTS`; guardian-funded; outside the portfolio adequacy check above. See [`../risk-framework/operational-risk-capital.md`](../risk-framework/operational-risk-capital.md).

**Active Stability Capital (ASC).** Capital deployed to peg-defense-eligible holdings (deep liquidity, < 15min convertibility). Routed to the `ascbook` sub-book per [`../risk-framework/primebook-composition.md`](../risk-framework/primebook-composition.md). See [`../risk-framework/asc.md`](../risk-framework/asc.md).

Both are capital-adequacy-relevant but evaluated alongside the portfolio TRC adequacy, not inside it.

---

## File map

| Doc | Relationship |
|---|---|
| [`README.md`](laniakea-docs/accounting/README.md) | Accounting directory index |
| [`settlement-cycle.md`](settlement-cycle.md) | Settlement reads `time-weighted-debt` against the JRC/SRC structure defined here |
| [`isolated-deployment.md`](isolated-deployment.md) | Isolated deployment is outside the ingression curve; reduces effective JRC |
| [`../risk-framework/capital-formula.md`](../risk-framework/capital-formula.md) | TRRC computation; this doc supplies the funding-side of `ER = TRRC / TRC` |
| [`../risk-framework/book-primitive.md`](../risk-framework/book-primitive.md) | 6-tuple book structure; equity invariant (Prime's equity tranche = JRC + Prime Token claims) |
| [`../risk-framework/tranching.md`](../risk-framework/tranching.md) | Exoassets / exoliabs / waterfall; tranches as rule-bearing claims |
| [`../risk-framework/currency-frame.md`](../risk-framework/currency-frame.md) | Frame inheritance for capital denominations (USD frame top-down) |
| [`../risk-framework/riskbook-layer.md`](../risk-framework/riskbook-layer.md) | Where risk-form match sits |
| [`../risk-framework/halobook-layer.md`](../risk-framework/halobook-layer.md) | Bundle exposure structure |
| [`../risk-framework/asc.md`](../risk-framework/asc.md) | ASC parallel track |
| [`../risk-framework/operational-risk-capital.md`](../risk-framework/operational-risk-capital.md) | ORC parallel track |
| [`../synoteleonomics/recipe-marketplace.md`](../synoteleonomics/recipe-marketplace.md) | Carry distribution (post-Phase 9 Stream sentinel revenue feeds back into capital formation) |
| [`../macrosynomics/synomic-entities.md`](../macrosynomics/synomic-entities.md) | Rank hierarchy: Ozone (Rank 1) > rank-2 entities (Primes, Generators, Oracle, Exchange, House, Core) > Halos (Rank 3) |

---

## One-line summary

**A Prime's capital is four tranches (IJRC / EJRC / SRC / MDC) ingressed through a universal flat-plus-quarter-circle curve into effective capital, capped by the Prime token's worst-of-observed market metrics, temporarily backstopped by Genesis Capital with a $125M ABC floor and a 25% retention rule until target, defended in insolvency by a 4-level hierarchy (ABC → SKY inflation → Genesis reclaim → USDS haircut) — all of it the funding side of `ER = TRRC / TRC ≤ 0.90`, with ORC and ASC on parallel tracks pointed to but not duplicated here.**
