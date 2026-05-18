# Capital Formula

## 1. The per-position computation flow

For each position held by a Prime:

```
Step 1: Riskbook risk-form match
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

Position Capital = Matched Portion × default-CRR
                 + Unmatched Portion × max(default-CRR, Forced-Loss Capital)
                 + Unmatched Portion × rate-CRR
```

Credit-spread, rate, and liquidity are covered on the SDR-matched portion in P1. The risk form still calculates spread-CRR, rate-CRR, and liquidity-CRR; they become non-binding only to the extent the position is matched. Unmatched falls through to forced-loss plus rate treatment. Default-CRR is always required.

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

Where `TRC[p]` is Total Risk Capital actually held (JRC + EJRC + SRC, per [`../accounting/capital-stack.md`](../accounting/capital-stack.md)). Target: `ER ≤ 0.90`. Breach drives penalties at settlement.

## 5. Capital funding

This formula outputs **TRRC** (Total Required Risk Capital). For how TRRC is funded across JRC/SRC tiers with ingression-adjusted recognition, see [`../accounting/capital-stack.md`](../accounting/capital-stack.md).

The ingression mechanism handles the time delay between commitment and recognition of external risk capital. Capital that has committed to back the Prime but hasn't yet ingressed counts at a discount; once ingressed, full notional applies.

## 6. NFAT book-phase note

For positions held via Term Halo books (NFATs), CRR varies by book phase:
- **Filling** — low CRR (book is still being assembled)
- **Deploying** — high CRR (information opacity during obfuscated deployment)
- **At Rest** — medium CRR (based on attested risk characteristics)
- CRR increases if re-attestation is missed

In the new framework, these phase-dependent CRRs are captured via the Riskbook risk form's equation, not as separate state-based CRR atoms. The risk-form equation reads the book's current phase from synart state and applies the appropriate stress treatment per phase. See [`../smart-contracts/nfats.md`](../smart-contracts/nfats.md) for the qualitative book-phase incentive structure. Numeric CRR calibration values for NFAT book-phases are pending.
