# Asset Classification

**Last Updated:** 2026-01-27

## Asset Classification

Every asset has three relevant characteristics:

### A. Fundamental Risk (Risk Weight)

What can go wrong even if you hold to maturity?
- Credit default
- Smart contract failure
- Counterparty failure
- Regulatory seizure

This is the irreducible risk that doesn't go away with time. Expressed as a **risk weight** percentage.

### B. Mark-to-Market Risk (Drawdown)

How far could this asset fall from current price before recovering?

Measured as Expected Shortfall at a confidence level (e.g., 97.5%) over a relevant stress horizon. This is the FRTB-inspired concept — the loss you'd realize if forced to sell during a stress period.

See `market-risk-frtb.md` for the drawdown treatment module.

### C. Stressed Pull-to-Par

For assets that mature or converge to a known value, we use **Stressed Pull-to-Par** — the time until an asset converges to its fundamental value under stress conditions.

**Why Stressed Pull-to-Par?**

Normal pull-to-par (or WAL for amortizing assets) assumes typical prepayment and amortization patterns. But the scenario where asset duration matters for capital is precisely the stress scenario:
- During crises, prepayments slow dramatically (borrowers can't refinance)
- Amortization continues but reinvestment into new loans slows
- Pull-to-par extends, sometimes significantly

Using unstressed duration would be like stress-testing a lifeboat in calm seas. SPTP-matching validity must hold during stress.

**Stressed Pull-to-Par Calculation**

```
Stressed Pull-to-Par = Normal Pull-to-Par × Stress Modifier
```

The stress modifier is derived from historical worst-case prepayment slowdowns for equivalent asset classes:

| Asset Class | Normal Pull-to-Par | Stress Modifier | Stressed Pull-to-Par | Historical Basis |
|-------------|-------------------|-----------------|---------------------|------------------|
| CLO AAA (JAAA) | ~2.5 years | 1.3-1.4x | ~3.25-3.5 years | 2008-2009: prepayments dropped from 28% to 9-15% |
| Agency MBS | Varies | 1.2-1.5x | Varies | Rate-dependent; extension risk in rising rate environments |
| Corporate bonds | To maturity | 1.0x | To maturity | Fixed maturity, no prepayment optionality |
| T-bills | To maturity | 1.0x | To maturity | Fixed maturity, no extension risk |
| Money market ETF | Near-zero | 1.0x | Near-zero | Daily liquidity, stable NAV |

**Key insight:** The stress modifier should reflect the *same* stress scenario that drives liability outflows. If a credit crisis causes both duration extension and depositor flight, the stressed pull-to-par ensures the asset-liability match remains valid under that scenario.

**Assets without Pull-to-Par**

- **ETH:** Infinite (no pull to par — perpetual volatility)
- **Sparklend positions:** None (perpetual, no maturity)

Assets with no pull-to-par cannot be SPTP-matched regardless of stress assumptions.

---
