# Examples and Principles

**Last Updated:** 2026-01-27

## Current Practice vs. Proposed

### JAAA Specifically

| Aspect | Current | Proposed |
|--------|---------|----------|
| Capital requirement | 1.6% CRR regardless of liability matching | 4-5% if matched to 42mo bucket; ~10% if unmatched |
| Justification | Fixed percentage | Depends on cumulative SPTP capacity at 42mo+ |

**Implication:** The $1B JAAA position (SPTP = 42mo) is only justifiable at low capital if there's $1B+ of cumulative SPTP capacity in 42mo through 50mo+ buckets. If only $600M capacity exists at 42mo+, the remaining $400M JAAA requires full FRTB capital.

### Sparklend

| Aspect | Current | Proposed |
|--------|---------|----------|
| Capital requirement | 0.1% CRR | 1-2%+ based on gap risk model |
| SPTP-matching | N/A | Not available (no pull-to-par) |

### Overall Portfolio

| Aspect | Current | Proposed |
|--------|---------|----------|
| Methodology | Different approaches stitched together | Unified framework |
| SPTP capacity | Not explicitly tracked | Liability duration determines SPTP capacity |
| Asset competition | Implicit | All assets compete for limited SPTP capacity based on pull-to-par |

---

## Summary of Principles

1. **Liability duration determines SPTP capacity.** Use Lindy-based demand analysis to measure how much of your liability base is short-term vs long-term.

2. **Use Stressed Pull-to-Par for asset duration.** Asset pull-to-par is calculated as Normal Pull-to-Par × Stress Modifier, where the stress modifier reflects historical worst-case prepayment/amortization slowdowns for that asset class.

3. **SPTP protects against credit spread risk, not rate risk.** Credit spreads are mean-reverting and don't affect SSR; rate changes can be permanent and create ongoing cash flow mismatch. SPTP lets Primes avoid hedging credit spreads while requiring rate hedging.

4. **All fixed-rate exposure must be rate-hedged.** Either through floating-rate assets, swaps/derivatives, or by holding rate hedging capital. Unhedged rate risk cannot be SPTP-matched.

5. **Stressed pull-to-par determines SPTP-matching eligibility.** Only assets with stressed pull-to-par ≤ liability tier duration AND rate-neutral exposure can be SPTP-matched.

6. **Matched assets get risk weight treatment.** You only need capital for fundamental risk (credit, smart contract, etc.).

7. **Unmatched assets get FRTB treatment.** You need capital for full stressed drawdown over the relevant forced-sale horizon.

8. **Crypto lending is inherently unmatched.** No pull-to-par means no SPTP-matching relief. Capital must cover gap risk based on historical stress analysis.

9. **Correlation groups prevent diversification illusions.** Capital must survive each stress scenario applied to its correlated asset group.

10. **Conservative by default.** When uncertain about liability duration or asset characteristics, assume short-duration liabilities and full drawdown risk.

---
