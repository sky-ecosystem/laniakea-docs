# Market Risk (FRTB-Style Drawdown for Unmatched Liquid Assets)

**Last Updated:** 2026-01-27

This document defines the drawdown-based capital treatment used for the **unmatched portion** of assets that must be resilient to forced sale during stress.

## Core Question

If we were forced to liquidate during stress, what loss could we realize at a conservative confidence level?

## FRTB-Style Drawdown (Concept)

We model this as an Expected Shortfall-style drawdown concept (FRTB-inspired), over a chosen stress horizon.

This is the “market risk drawdown” capital component.

## Inputs (To Be Calibrated)

- Confidence level (e.g., 97.5%)
- Stress horizon (e.g., 10 trading days)
- Stressed calibration approach (historical window / scenario set)
- Liquidity assumptions (can we liquidate at modelled prices?)

## Outputs

- `frtb_drawdown_CRR` for eligible liquid TradFi assets (or per-asset-class calibration parameters that convert to a CRR)

## Combination Rule

`frtb_drawdown_CRR` is the **forced-sale** capital term for liquid assets. In the capital formula it is combined with fundamental risk (risk weight) via a simple loss envelope:

```
Unmatched Capital = Position Size × max(Risk Weight, FRTB Drawdown)
```

See `capital-formula.md` and `matching.md` for the matched/unmatched split.

## Connections

- Asset primitive definition: `asset-classification.md` (drawdown risk)
- Matched vs unmatched treatment: `matching.md`
- Capital composition: `capital-formula.md`
- Examples: `asset-type-treatment.md`
