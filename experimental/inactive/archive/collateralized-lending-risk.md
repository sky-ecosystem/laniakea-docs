# Collateralized Lending Risk (Jump-to-Default + Liquidation Loss)

**Last Updated:** 2026-01-27

This document covers risk for collateralized lending positions where losses arise from **fast price moves**, **liquidation mechanics**, and **execution/oracle constraints** (as opposed to pull-to-par duration mechanics).

## Core Question

In a stressed event, what loss can occur **before liquidations can restore solvency**?

This is the “gap risk / liquidation shortfall” capital component.

## Components

### 1) Jump-to-Default / Price Gap

Collateral can move discontinuously (or effectively discontinuously relative to liquidation throughput), creating undercollateralized positions.

### 2) Liquidation Loss Given Default (LGD)

Even if liquidations execute, realized loss can be amplified by:
- auction slippage / AMM depth
- oracle latency or failure modes
- congestion and delayed keepers
- collateral correlation (everyone selling the same collateral)

### 3) Protocol/Mechanism Risk

Even with adequate collateralization, failures can create loss:
- smart contract bugs
- oracle manipulation / stale feeds
- governance/key compromise (where relevant)

## Gap Risk Capital (Current Placeholder)

Gap risk is the bad debt that occurs when collateral prices crash faster than liquidations can execute.

**Approach:**
1. Analyze historical crash data (flash crashes, black swan events)
2. Model health factor distribution under stress — not assuming all positions jump to HF=1
3. Calculate expected bad debt for instantaneous price gaps of X% (derived from historical worst cases)
4. Size capital to survive the worst-case scenario at chosen confidence level

**Key insight:** The distribution matters — some positions are well-overcollateralized, others are marginal.

## Outputs

- `gap_risk_CRR` (capital ratio requirement for collateralized lending exposures)
- Optional: breakouts for `jump_risk`, `liquidation_LGD`, and `mechanism_risk` if we want a more granular reporting model

## Combination Rule

`gap_risk_CRR` is the **forced-liquidation / shortfall** capital term for collateralized lending exposures. In the capital formula it is combined with fundamental risk (risk weight) via a loss envelope:

```
Position Capital = Position Size × max(Risk Weight, Gap Risk CRR)
```

See `capital-formula.md` for how this connects to other asset types.

## Connections

- Capital composition: `capital-formula.md`
- Asset examples: `asset-type-treatment.md`
