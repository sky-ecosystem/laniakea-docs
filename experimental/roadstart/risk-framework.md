# Risk Framework — Essentials for Roadmap Work

Just the risk-framework concepts the roadmap assumes but doesn't define. Drop-in companion to `lani/roadmap/`. Source: `lani/risk-framework/` (file map at bottom).

## Five risk types

| Type                            | Time signature                               | Coverage                                        |
| ------------------------------- | -------------------------------------------- | ----------------------------------------------- |
| **Default / fundamental**       | Permanent                                    | Capital always required (irreducible floor)     |
| **Credit-spread MTM**           | Mean-reverting                               | Held-to-par via SDR / term matching             |
| **Rate cash-flow drag**         | Permanent until rates revert / asset matures | Match (fixed/fixed), hedge, or rate-CRR capital |
| **Liquidity / fire-sale**       | Crystallizes only on forced sale             | Held-to-par or transferability                  |
| **Concentration amplification** | Portfolio-level                              | Category caps + 100% CRR on excess              |

Default capital is always required. Sub-books only modify the other four. ASC (peg-defense liquidity) and ORC (operator-posted capital) are **parallel tracks**, not folded into TRRC.

Teleological grounding: *in a correlated worst-case crash right now, what real claim do we have to real assets that survive?* Point-in-time stress, not lifetime cumulative PD.

## Book primitive

Every book is a 6-tuple `(assets, tranches, equity-tranche, rules, state, frame)`. Universal invariants:

- Exactly one designated **equity tranche** (most-junior, first-loss).
- Solvent iff equity > 0; equity → 0 triggers a defined unwind.
- **Real-time equity recomputation** required — every book class declares an equity-feed mechanism at onboarding (`CHAINREAD` sigil, `attest-data` beacon, or synserv-derived).
- Bankruptcy remoteness lives at the **Riskbook** level; no netting across Riskbooks.

Rules execute as synart-resolved code that synserv runs in-space against current input atoms. Any warden re-runs them and gets the same answer.

## Tranching + exo vocabulary

Tranches are ordered claims `(seniority, holder, notional, denomination)`. Notional may be static or rule-determined (callable, step-up, convertible, triggered subordination).

- **Exoasset** — terminal external asset (ETH, USDC, T-bills).
- **Exoliab** — tranche held by an external party (borrower equity in an overcollateralized loan; sponsor retention in a CLO).

Waterfall: most-junior absorbs first up to its full notional; remainder flows to the next-junior, etc. For a single senior tranche over collateral:

```
senior_loss = max(0, asset_drop − junior_cushion)
```

**Cushion revaluation under stress is mandatory.** If the junior cushion is denominated in the same crashing asset (borrower equity in ETH against a USD loan), stress both consistently in the scenario.

Anything overcollateralized — Sparklend, NFAT, CLO tranches, ABF — expresses as a senior tranche of a tranched exobook. "Gap risk" is not a separate concept; it's asset-stress propagated through the tranche structure.

## Currency frame

- **Frame** = abstract unit of account (USD, EUR, BTC). Inherits top-down from the Generator. v1 is single-Generator (USGE → USDS → USD).
- **Instrument** = concrete realization with its own stress profile relative to its frame. Three kinds: `unit-of-account` (USD itself; not held), `stablecoin-proxy` (USDS/USDC/USDT — depeg stress), `native-volatile-asset` (BTC/ETH — volatility stress).

The **Riskbook is the translation layer**: below it, native denominations; above it, everything is frame-pure. Depeg / FX / asset stress applied here.

## Four-layer stack roles

| Layer | Role |
|---|---|
| **Riskbook** | Unit of regulation. Matches a registered **risk form** or gets CRR 100%. Default risk set entirely here. Currency translation here. Tactical hedging within one strategy lives here (both legs in one Riskbook). Bankruptcy-remoteness boundary. |
| **Halobook** | Bundle exposure structure. Declares **P** (permitted unwind: lockups, governance approvals) and **T** (transfer market: transferability). Never modifies default risk. Pure summation across Riskbooks (no netting, no cross-Riskbook hedging). Issues one Halobook unit upward. |
| **Primebook** | Composes typed sub-books (below). Routes each Halobook unit by structural eligibility. Issues one Primeunit upward. |
| **Genbook** | Aggregates Primeunits; system-wide concentration. **Deferred in P1.** |

**U/P/T liquidity decomposition**: **U** = underlying unwind feasible? (Riskbook walks structure + applies stress). **P** = permitted to execute? (Halobook declares lockups/approvals). **T** = wrapper itself sellable? (Halobook declares transferability). Two exit paths: `U AND P` (unwind) or `T` (transfer). Sub-book eligibility maps to these.

**Cross-default → Riskbook constraint.** Joint-default behavior must live in one Riskbook with a category that understands it. No cross-Halobook default linkages. Forces clean operational alignment: legal/operational ownership = Riskbook boundary = unit of joint-default modeling.

## Sub-book taxonomy + coverage matrix

| Sub-book | Default | Spread | Rate | Liquidity | P1 status |
|---|---|---|---|---|---|
| `ascbook` (peg-defense) | Capital | Capital | n/a | Product (must hold) | Deferred (ASC tracked out-of-band per `asc-transition.md`) |
| `tradingbook` (FRTB-style) | Capital | Forced-loss | Hedge or capital | Forced-loss | Deferred |
| `termbook` (tUSDS YT match) | Capital | Covered (held to par) | Covered (fixed/fixed) | Covered | Deferred (no tUSDS market yet) |
| `structbook` matched (SDR) | Capital | **Covered** | **Covered (P1 SDR match)** | **Covered** | **Active P1** |
| `structbook` unmatched | Capital | Forced-loss | Rate-CRR | Forced-loss | Active fallback |
| `hedgebook` | Capital | Adjusted for hedge | Adjusted | Adjusted | Deferred |
| Unmatched leftover | Capital | Forced-loss | Forced-loss | Forced-loss | Active fallback |

Default capital is always required because it's irreducible. Sub-book structure only reduces the other four.

Routing is declarative by structural eligibility (Halobook P/T + asset SPTP + capacity). **Switching between sub-books is free** subject to prerequisites — no motivational scrutiny (would force strategy disclosure). Crash-oracle to suspend switches mid-crash is Phase 2+; schema slot reserved.

Sub-books split **optimization-shaped** (`structbook`, `termbook`, `hedgebook` — run internal optimization over capacity) vs **static-treatment** (`tradingbook`, `ascbook`, unmatched). Optimization sub-books blend matched + unmatched portions smoothly as capacity shifts — no binary transition events.

## Default-deny CRR 100%

Triggers in three places:
1. Riskbook without matching risk form.
2. Exobook beyond max recursion depth.
3. Exobook without matching risk form.

Same pattern as verb whitelists / recipe catalogs elsewhere — regulated activity flows where governance has built infrastructure; un-regulated activity is treated as worst-case. Innovation flows through governance crystallization, not ad-hoc.

## Capital formula

Per position:

```
position_capital = (sub-book formula over CRR components × position size)
```

`structbook` (P1-active sub-book):

```
matched_capital   = matched × default-CRR
unmatched_capital = unmatched × max(default-CRR, forced-loss-capital) + unmatched × rate-CRR
position_capital  = matched_capital + unmatched_capital
```

Aggregation:

```
TRRC[p] = Σ position_capital + concentration_excess
ER[p]   = TRRC[p] / TRC[p]      ; target ≤ 0.90
```

Concentration excess (deferred enforcement in P1): excess portion × 100% CRR; max binding category only (no stacking).

`TRC[p]` is held risk capital across JRC/EJRC/SRC tiers with ingression-adjusted recognition (`accounting/capital-stack.md`).

## Custodial-crypto risk form (the P1 form body)

Stress-envelope waterfall — **not** expected-loss. Lives per-halo at `&entity.halo.{id}.custodial-crypto`. Composition scope:

```
(composition-constraints
   (and (senior-tranche-only)
        (collateral-asset-in [btc eth steth])
        (senior-denom-in [usdc usds usdt])
        (term-to-maturity <= 1y)
        (halo-class nfat-term)))
```

For each exobook `e` and scenario `s`:

```
stressed_asset_value(e,s) = Σ collateral_i × stressed_price_i(s) × executable_haircut_i(e,s) − liquidation_costs
senior_loss(e,s)          = min(senior_notional, max(0, senior_notional − stressed_asset_value(e,s)))
default-CRR(e)            = max_s senior_loss(e,s) / senior_notional
```

Output four components: `default-CRR`, `spread-CRR`, `rate-CRR`, `liquidity-CRR` plus `binding-scenario`. SDR matching at the Prime layer can make spread/rate/liquidity non-binding for the matched portion; **it never removes default-CRR**.

Inputs:
- exobook state (collateral, debt, LT, liquidation bonus, current LTV, maturity, funding-confirmation) via `CHAINREAD`
- borrower-admission + exobook-term attestation gates (default-deny if missing/stale/fail)
- market-memory from `&entity.oracle.crypto-majors.ticks` (price/peg, vol, correlation, depth/impact, liquidation overhang, funding/OI, rates/macro, data-quality)
- approved scenario library (worst-historical-crash, exchange-hack, stETH-basis-break, depeg, war/rate-spike, etc.) — scenarios reference reducer outputs wherever possible; semantic bridges explicit

**CORE** (BA Labs CRR model) is calibration/reference — sanity-check shocks and liquidation haircuts; **not** the binding CRR engine, not called via `call-out`.

Riskbook aggregation preserves correlation: `riskbook_loss(r,s) = Σ senior_loss(e,s)`; `riskbook_default_crr = max_s riskbook_loss / total_senior_notional`. No cross-Riskbook netting.

Full body: `risk-framework/custodial-crypto-risk-form.md`.

## SDR model + matching

**Buckets:** 51 total, 30 days each. Bucket N = N × 30 days; bucket 50 = 1,500+ days. JAAA (1,260-day SPTP) → bucket 42. P1 180-day NFAT → bucket 6.

**SPTP** (Stressed Pull-to-Par) = nominal pull-to-par × stress modifier. Reflects historical worst-case prepayment/amortization slowdowns (e.g., CLO AAA: 1.4× modifier from 2008–9 data). Split into credit-spread pull-to-par horizon vs interest-rate duration (V1 NFAT: both = nominal term, no stress modifier). Assets with no SPTP (ETH, perpetual lending) cannot be matched — route to `tradingbook` or unmatched.

**Matching eligibility** = `SPTP ≤ liability bucket tenor` AND a rate treatment (floating-rate, swap, rate-hedge capital, or in P1 SDR-matched).

**Structural Demand Resource (SDR) pipeline** lives in `&entity.generator.usge.structural-demand`: lot-age surface → Lindy SDR algorithm → Lindy SDR bucket capacity → SDR policy overlay → effective SDR bucket capacity. The lot-age surface is scraped/reduced from USDS / DAI / sUSDS / sDAI lots; Lindy SDR discounts fragile structure such as same-age crowding, same-account concentration, churn, and low-quality sources. The governance-set SDR policy overlay constrains the dynamic result with eligible-source filters, caps, haircuts, emergency bounds, and bootstrap/fallback values. `&entity.generator.usge.sdr-auction` splits effective SDR bucket capacity across Primes by ownership weight.

**Rounding convention** (conservative): liabilities round **down** to nearest bucket; assets round **up**. Cumulative capacity matching — an asset can match against its required bucket AND all higher buckets.

**Continuous, not binary.** Capacity shrinkage smoothly raises blended CRR — no transition event:

```
capacity utilization shifts → matched/unmatched ratio shifts → position_capital recomputes
```

## Asset risk-type tuple

Each canonical asset (target home: `&core.framework.risk.asset-profiles`) carries:

- **Fundamental risk weight (RW)** — irreducible loss probability (credit default, smart-contract failure, custody failure, regulatory seizure)
- **Drawdown distribution** per scenario
- **Slippage model** (size + stress conditions)
- **SPTP** (split into credit-spread pull-to-par horizon vs interest-rate duration)
- **Correlations** with other assets (joint-stress)
- **Currency dimension** (frame + kind + stress profile)

Together: drawdown + slippage + correlations = **asset-level liquidity profile**, the primitive the unified `forced-loss-capital` math runs against. No risk form may inline its own asset stress assumptions — single source of truth, governance-paced calibration.

In P1 there's no canonical asset-profiles Space; per-halo risk class carries the relevant copy. Phase-invariant consumption site — later canonical propagation lands additively.

## Risk forms — what they are

A risk form is a synlang object declaring:

- `(level …)` — exo-asset / exobook / riskbook
- `(frame …)` — accounting frame (e.g., usd)
- `(composition-constraints …)` — predicate over the book's contents that must evaluate True; non-match → CRR 100%
- `(variables …)` — what the equation needs
- `(equation-m2m …)` / `(equation-htm …)` / `(equation-default …)` — the math
- `(resolution-tier …)` — `math` (closed-form) / `simulation` (Monte-Carlo / stress-scenario sweep) / `heuristic` (with depth/cycle/repeat penalties) / `max-risk` (full notional → CRR 100%)

The risk-form catalog is governance's primary risk-shaping lever: add/tune/deprecate; Halos lobby for new forms when their strategy doesn't fit existing ones.

## Hedging — two levels

| Level | Scope | Examples |
|---|---|---|
| **Riskbook (tactical)** | Within one coherent strategy / single composition | ABF + matching CDS in one Riskbook; long ETH spot + short ETH perp |
| **Hedgebook (portfolio)** | Across diverse Halobook positions at Prime level | Single index-CDS hedging credit across many Halobooks; USDC depeg hedge across many Riskbooks |

Hedge effectiveness is **quantified residual-risk computation** — counterparty risk × basis correlation × closing slippage × tenor mismatch. Clean hedge → near-zero residual; sloppy hedge → mostly capitalized. No "hedge magic."

Hedgebook deferred in P1.

## Concentration framework (deferred enforcement in P1)

Two levels: **Primebook** (within a Prime's portfolio) and **Genbook** (system-wide). Mechanism: governance defines correlation categories (non-mutually-exclusive); each has a cap (% of scope); excess portion × 100% CRR; max binding category only (no stacking). **Capacity rights** ("grandfathered slices") prevent new deployers from instantly displacing incumbents — normalization period `T = max(asset_SPTP, 3 months)`.

V1 measures gross-of-hedge.

P1 implements neither level enforcement; mechanism is fully target.

## Projection models (for complex non-tranchable positions)

The substrate handles directly-modelable positions (asset holdings, tranches, linear claims). Anything more complex (vanilla options, callable bonds, MBS with prepayment, CDS, Asian/lookback, cat bonds, convertibles, variance swaps) gets a **projection model** declared by its category: `(position, scenario) → stress-loss-number`. Analytical / lattice / Monte Carlo / parametric / ML.

**Model-uncertainty haircut** is a first-class capital dimension — categories with newer / less-tested / more-parameterized models carry an explicit multiplier on top of the projected number. Categories without a projection → CRR 100%.

Not relevant to P1 (one risk form, exobook waterfall only).

## ORC + risk monitoring (later-phase context)

**ORC** (Operational Risk Capital) — operator-posted, parallel to portfolio TRRC, covers damage from a compromised guardian:

- **Phase 1:** `ORC ≥ IRL × accumulation × N` with IRL = $100K, accumulation factor 1.0625 at SORL=25%, N = surface count. ~$1.06M per guardian for N=10. Type 1 attack model from `smart-contracts/rate-limit-attacks.md` (canonical home for SORL parameters).
- **Operating-setup era (Phase 9+):** `ORC ≥ Rate Limit × TTS`, where `TTS = warden tick + synart re-derive + halt propagation`. Better wardens → lower TTS → lower ORC.

**Monitoring metrics** (surfaced for operators/governance, mostly later-phase): per-sub-book CRR, equity proximity, treatment-switch frequency. ER enforcement schedule (target ≤ 0.90) needs a governance proposal — likely rate-limit reduction, deployment freeze, mandatory deleveraging timeline.

## File map (where each piece lives)

| Topic | Source |
|---|---|
| Five risk types, U/P/T, default-deny | `risk-decomposition.md` |
| 6-tuple book + equity invariant | `book-primitive.md` |
| Exoasset/exoliab + waterfall + cushion revaluation | `tranching.md` |
| Frame vs instrument, Riskbook translation | `currency-frame.md` |
| Riskbook layer (unit of regulation) | `riskbook-layer.md` |
| Halobook layer (P/T, no netting) | `halobook-layer.md` |
| Sub-book taxonomy + routing + optimization shape | `primebook-composition.md` |
| Custodial-crypto P1 form body (worked math) | `custodial-crypto-risk-form.md` |
| 30-day SDR buckets + Lindy SDR + SDR policy overlay | `sdr-model.md` |
| Smooth matched/unmatched blend + cumulative capacity | `matching.md` |
| Per-position formulas + TRRC + ER | `capital-formula.md` |
| Asset risk-type tuple + SPTP refinement | `asset-classification.md` |
| Market memory reducer catalog + scenario interface | `market-memory-oracle.md` |
| Two-level concentration + capacity rights | `correlation-framework.md` |
| ORC + TTS economics + IRL/SORL derivation | `operational-risk-capital.md`, `smart-contracts/rate-limit-attacks.md` |
| Risk monitoring metrics + ER enforcement | `risk-monitoring.md` |
| Per-asset-class treatments + projection models | `asset-type-treatment.md`, `projection-models.md` |
| Hedgebook (deferred) | `hedgebook.md` |
| Sentinel integration (later-phase) | `sentinel-integration.md` |
