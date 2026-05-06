# Capital Formula

**Status:** Draft (Phase 3 update, 2026-05-05)

The downstream consumer of the layered risk model. Defines how Riskbook category equations, sub-book composition, hedge accounting, and concentration penalties combine into a single Total Required Risk Capital (TRRC) number per Prime.

Companion to:
- [`risk-decomposition.md`](risk-decomposition.md) — the five risk types and the coverage matrix
- [`riskbook-layer.md`](riskbook-layer.md) — Riskbook category match produces per-position CRR
- [`primebook-composition.md`](primebook-composition.md) — sub-book routing determines which risks are covered
- [`hedgebook.md`](hedgebook.md) — hedge residuals contribute via the Hedgebook sub-book
- [`correlation-framework.md`](correlation-framework.md) — concentration penalties (excess CRR 100%) layer on top

---

## TL;DR

Per-position computation flow:

```
1. Look up position's Riskbook category equation
2. Project asset stress through tranche waterfall (or projection model for non-tranched)
3. Apply Halobook adjustment if any (P/T declarations affect routing)
4. Route to Primebook sub-book based on structural eligibility
5. Sub-book determines which risks are covered vs require capital
6. Apply concentration excess penalty if applicable
7. Sum to position capital
```

Total Required Risk Capital:

```
TRRC = Σ Position Capital + Concentration Excess Penalties
```

The blended formula for an optimization-shaped sub-book (`structbook`, `termbook`, `hedgebook`):

```
Position Capital = matched_or_hedged_portion × covered_treatment_CRR
                 + unmatched_or_unhedged_portion × forced-loss_CRR
```

For static-treatment sub-books (`tradingbook`, `ascbook`, unmatched): uniform forced-loss across the position.

---

## Section map

| § | Topic |
|---|---|
| 1 | The per-position computation flow |
| 2 | Per-sub-book CRR formulas |
| 3 | Concentration excess penalty |
| 4 | TRRC aggregation |
| 5 | Capital funding |
| 6 | NFAT book-phase note |

---

## 1. The per-position computation flow

For each position held by a Prime:

```
Step 1: Riskbook category match
  → If matched: equation produces per-position CRR (default + currency translation + tactical hedging)
  → If no match: CRR = 100% (default-deny per risk-decomposition.md §7)
                 (and the rest of the flow is skipped)

Step 2: Project asset stress through structure
  → For tranched-exobook positions: waterfall propagation per tranching.md
  → For non-tranched complex positions: projection model per projection-models.md
  → For direct holdings: read drawdown distribution from asset-classification.md

Step 3: Halobook exposure structure adjustment
  → Apply rollover, lockup, embedded-option effects
  → Generate U/P/T declarations for downstream routing

Step 4: Sub-book routing
  → Match structural eligibility to most capital-efficient eligible sub-book
  → ascbook (peg-defense), tradingbook (FRTB-style), termbook (tUSDS-matched),
    structbook (structural-demand-matched), hedgebook (cross-position hedged), or unmatched

Step 5: Sub-book capital math
  → Optimization-shaped: blend matched/hedged portion with unmatched portion
  → Static-treatment: uniform per-sub-book CRR

Step 6: Concentration excess
  → Compute concentration utilization per category
  → Apply 100% CRR on excess portion (per correlation-framework.md)

Step 7: Position capital = sum of treatments × position size
```

---

## 2. Per-sub-book CRR formulas

### `ascbook` (static)

```
Position Capital = Position Size × max(Risk Weight, Credit-Spread Stress)
```

Liquidity isn't a risk — it's the product. Capital against default + credit-spread MTM.

### `tradingbook` (static, FRTB-style)

```
Position Capital = Position Size × max(Risk Weight, Forced-Loss Capital)
```

Where `Forced-Loss Capital = stressed drawdown` for the asset (per [`asset-classification.md`](asset-classification.md)). Default + forced-loss envelope; rate hedging additive if applicable.

### `termbook` (optimization, fully matched)

```
Matched Portion = min(Position Size, Available Term Capacity)
Unmatched Portion = Position Size - Matched Portion

Position Capital = Matched Portion × Risk Weight
                 + Unmatched Portion × max(Risk Weight, Forced-Loss Capital)
```

Three risks covered (credit-spread, rate, liquidity) on the matched portion. Unmatched portion falls through to forced-loss treatment.

### `structbook` (optimization, partially matched)

```
Matched Portion = min(Position Size, Available Structural-Demand Capacity)
Unmatched Portion = Position Size - Matched Portion

Position Capital = Matched Portion × Risk Weight
                 + Matched Portion × Rate-Hedge Capital   ; v1 carve-out: 0
                 + Unmatched Portion × max(Risk Weight, Forced-Loss Capital)
```

Credit-spread + liquidity covered on matched portion. Rate-hedge capital required for matched portion (carved out for v1). Unmatched falls through.

### `hedgebook` (optimization, hedge residual)

```
Hedged Portion = min(Position Size, Available Hedge Capacity)
Unhedged Portion = Position Size - Hedged Portion

Position Capital = Hedged Portion × Hedge Residual CRR
                 + Unhedged Portion × Natural Sub-Book CRR
```

`Hedge Residual CRR` from the Hedgebook category equation (per [`hedgebook.md`](hedgebook.md) §5) — explicitly models counterparty / basis / liquidity / tenor failure. Unhedged portion falls back to whatever sub-book the position would otherwise route to.

### Unmatched leftover (static)

```
Position Capital = Position Size × max(Risk Weight, Forced-Loss Capital)
```

Same form as `tradingbook` but without the FRTB-eligibility (no liquid trading expected).

---

## 3. Concentration excess penalty

If a Prime exceeds its in-cap allocation for any category (per [`correlation-framework.md`](correlation-framework.md)), the excess portion gets 100% CRR:

```
For category c:
   alloc[p][c] = Prime p's in-cap allocation for category c
   E[p][c]     = Prime p's exposure in category c
   excess[p][c] = max(0, E[p][c] - alloc[p][c])
   
Excess Capital[p][c] = excess[p][c] × 1.0   ; 100% CRR
```

Per the no-stacking rule (per [`correlation-framework.md`](correlation-framework.md) §2): if a position is in multiple categories, the binding category penalty applies (max), not the sum.

---

## 4. TRRC aggregation

Total Required Risk Capital across the Prime's portfolio:

```
TRRC[p] = Σ_position Position Capital[position]
        + Σ_category Excess Capital[p][c]
```

Encumbrance Ratio:

```
ER[p] = TRRC[p] / TRC[p]
```

Where `TRC[p]` is Total Risk Capital actually held (JRC + EJRC + SRC, per `accounting/risk-capital-ingression.md`). Target: `ER ≤ 0.90`. Breach drives penalties at settlement.

---

## 5. Capital funding

This formula outputs **TRRC** (Total Required Risk Capital). For how TRRC is funded across JRC/SRC tiers with ingression-adjusted recognition, see `accounting/risk-capital-ingression.md` (in `inactive/pre-synlang/`; pending its own synlang-native rewrite).

The ingression mechanism handles the time delay between commitment and recognition of external risk capital. Capital that has committed to back the Prime but hasn't yet ingressed counts at a discount; once ingressed, full notional applies.

---

## 6. NFAT book-phase note

For positions held via Term Halo books (NFATs), CRR varies by book phase:
- **Filling** — low CRR (book is still being assembled)
- **Deploying** — high CRR (information opacity during obfuscated deployment)
- **At Rest** — medium CRR (based on attested risk characteristics)
- CRR increases if re-attestation is missed

In the new framework, these phase-dependent CRRs are captured via the Riskbook category's equation, not as separate state-based CRR atoms. The category equation reads the book's current phase from synart state and applies the appropriate stress treatment per phase. See `smart-contracts/nfats.md` (in `inactive/pre-synlang/`) for the qualitative book-phase incentive structure. Numeric CRR calibration values for NFAT book-phases are pending.

---

## File map

| Doc | Relationship |
|---|---|
| [`risk-decomposition.md`](risk-decomposition.md) | The five risk types and the coverage matrix |
| [`riskbook-layer.md`](riskbook-layer.md) | Riskbook category match produces per-position CRR |
| [`primebook-composition.md`](primebook-composition.md) | Sub-book routing determines which risks are covered |
| [`hedgebook.md`](hedgebook.md) | Hedge residuals via Hedgebook category equation |
| [`correlation-framework.md`](correlation-framework.md) | Concentration excess penalty |
| [`matching.md`](matching.md) | Matched/unmatched blend in `termbook`/`structbook` |
| [`asset-classification.md`](asset-classification.md) | Asset-level stress profiles consumed by stress projection |
| [`projection-models.md`](projection-models.md) | Projections for non-tranched complex positions |
| [`asset-type-treatment.md`](asset-type-treatment.md) | Worked treatment per asset class |
| [`examples.md`](examples.md) | Worked end-to-end TRRC computation in v1 test scenario |
