# Capital Formula

**Last Updated:** 2026-01-27

## The Capital Formula

This file defines how the major risk components combine into a single required capital number. Each component’s calibration details live in its own module.

For any Prime's portfolio, total capital requirement is:

```
Total Capital = Σ (Matched Portion × Risk Weight)
              + Σ (Unmatched Portion × FRTB Drawdown)
              + Category Cap Penalties
```

**Per-position calculation:**

For each position with stressed pull-to-par:
```
SPTP Capacity = Cumulative liability amount in buckets ≥ SPTP bucket
Matched Portion = min(Position Size, Available SPTP Capacity)
Unmatched Portion = Position Size - Matched Portion

Position Capital = (Matched Portion × Risk Weight) + (Unmatched Portion × FRTB Drawdown)
```

For positions without pull-to-par (crypto lending, perpetuals):
```
Position Capital = Position Size × Gap Risk CRR
```

## Where Each Component Is Defined

- **Duration + matching:** `duration-model.md`, `matching.md`
- **Fundamental risk weight:** `asset-classification.md` (risk weight primitive) + `asset-type-treatment.md` (how it applies)
- **Market risk / FRTB drawdown:** `market-risk-frtb.md`
- **Collateralized lending gap risk:** `collateralized-lending-risk.md`
- **Category caps (concentration limits):** `correlation-framework.md`

**SPTP capacity consumption:**
- Positions consume SPTP capacity in order of matching
- Once capacity at a bucket is consumed, additional positions at that SPTP are unmatched
- Capacity at longer buckets can match shorter-SPTP assets (a 48mo bucket can match a 12mo SPTP asset)

Category caps enforce concentration limits via 100% CRR on excess (see `correlation-framework.md`).

---
