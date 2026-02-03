# Matching

**Last Updated:** 2026-01-27

## Rate Risk vs Credit Spread Risk

Duration matching (ALDM) is designed to protect against **credit spread risk**, not **interest rate risk**. This distinction is fundamental to understanding when duration matching provides value and when it doesn't.

### Why the Distinction Matters

**Credit spread risk** and **interest rate risk** behave fundamentally differently:

| Risk Type | Behavior | SSR Response | Duration Matching Applicability |
|-----------|----------|--------------|-------------------|
| **Credit spread widening** | Mean-reverting; cyclical | SSR stays flat or falls (flight to quality) | ALDM protects — temporary MTM loss, no cash flow mismatch |
| **General rate rise** | Can be permanent (regime shift) | SSR rises | ALDM does NOT protect — ongoing cash flow mismatch |

### The Mechanism

**Why credit spread risk is manageable with duration matching:**

1. Credit spread widening causes asset prices to fall temporarily
2. But SSR (Sky Savings Rate) doesn't rise — it tracks general rate levels, not credit spreads
3. During credit stress, USDS often benefits from flight-to-quality, potentially *lowering* SSR
4. The Prime has no cash flow mismatch — it can afford to wait
5. As credit spreads compress (empirically mean-reverting), asset prices recover
6. Duration matching ensures the Prime has time to wait for recovery

**Why rate risk is NOT manageable with duration matching:**

1. General rate rise (e.g., Fed hikes) causes SSR to rise permanently
2. If the Prime holds fixed-rate assets, it earns the old lower rate
3. This creates ongoing negative carry: pays SSR + margin, earns old rate
4. This isn't a temporary MTM shock — it's permanent cash flow drag
5. Duration matching doesn't help because there's no "pull to par" on the rate differential itself
6. The Prime will bleed continuously until the asset matures or rates fall

### Empirical Support

**Credit spreads are mean-reverting:**
- Research shows "significant evidence of mean reversion, especially for higher-rated spreads"
- Credit spread indices are modeled using Ornstein-Uhlenbeck processes (mean-reverting systems)
- 2008 GFC: ~6+ months to recover; COVID-19 2020: ~3 weeks after Fed intervention
- Counter-cyclical behavior: widen during contractions, narrow during expansions

**Interest rates can shift permanently:**
- Monetary policy regime changes are documented (e.g., Volcker era)
- The move from ~15% rates (1980s) to ~0% (2010s) wasn't mean reversion — it was a multi-decade regime shift
- Recent research challenges the assumption that monetary policy is "neutral" in the long run

### Rate Hedging Requirement

**All Prime fixed-rate exposure must be rate-hedged.** Duration matching eligibility requires that positions be rate-neutral relative to SSR.

#### Methods of Rate Hedging

| Method | Description | When to Use |
|--------|-------------|-------------|
| **Floating-rate assets** | Asset yield tracks market rates naturally | Preferred for CLOs (most are floating-rate) |
| **Interest rate swaps** | Swap fixed receipts for floating | Convert fixed-rate bonds to floating exposure |
| **Duration matching** | Match asset duration to liability duration | When liabilities have predictable duration |
| **Rate hedging capital** | Hold extra capital to cover expected rate loss | When hedging instruments unavailable or costly |

#### Rate Hedging Capital Calculation

If a Prime holds unhedged fixed-rate exposure, it must hold capital to cover the expected loss from rate movements:

```
Rate Hedge Capital = Fixed Rate Exposure × Duration × Expected Rate Volatility × Confidence Multiplier
```

**Example:**
- $100M fixed-rate bonds, 3-year duration
- Expected rate volatility: 200bps at 95% confidence
- Rate Hedge Capital = $100M × 3 × 2% × 1.65 = $9.9M

This capital is **in addition to** credit risk capital, not a substitute for it.

### Duration Matching Eligibility Summary

For an asset to be eligible for matched treatment, it must satisfy **both** conditions:

1. **Has stressed pull-to-par** ≤ matched liability tier duration (existing requirement)
2. **Is rate-neutral relative to SSR** — either:
   - Asset is floating-rate (natural hedge), OR
   - Asset is hedged via swap/derivative, OR
   - Prime holds rate hedging capital for unhedged fixed-rate portion

```
Match Eligible = (Has Pull-to-Par) AND (Rate Neutral OR Rate Hedge Capital Held)
```

### What This Means for Asset Types

| Asset | Rate Exposure | Typical Handling | Match Eligible? |
|-------|---------------|------------------|----------------|
| **JAAA (CLO AAA)** | Floating-rate (SOFR + spread) | Natural hedge | ✓ Yes |
| **Fixed-rate corporate bonds** | Fixed-rate | Must swap to floating or hold rate capital | Conditional |
| **T-bills (short duration)** | Fixed but short | Minimal rate risk due to short duration | ✓ Yes |
| **Long-duration treasuries** | Fixed, long duration | Must hedge or hold significant rate capital | Conditional |
| **Sparklend** | Floating-rate (typically) | N/A — no pull-to-par regardless | ✗ No (no SPTP) |

### The Value Proposition of Duration Matching

With rate risk properly hedged, duration matching (ALDM) allows Primes to:

- **Avoid hedging credit spread risk** on long-duration variable-rate assets
- **Take credit spread exposure** for yield while managing capital efficiently
- **Wait out temporary credit dislocations** without forced sales

This is the core value: duration matching lets Primes capture credit spread (which is compensated and mean-reverting) while requiring them to hedge rate risk (which can be permanent and catastrophic if unhedged).

---

## The Matching Principle

Assets can be matched against liability tiers based on their stressed pull-to-par:

### Matched Assets (Duration-Matched Treatment)

**Condition:** Asset stressed pull-to-par ≤ matched liability tier duration

**Treatment:**
- Forced realization probability is low
- Capital requirement = **Risk Weight only**
- You only need capital for fundamental risk (credit, smart contract, etc.)

### Unmatched Assets (FRTB Treatment)

**Condition:** Asset stressed pull-to-par > liability tier duration, OR no pull-to-par

**Treatment:**
- Forced realization probability is high
- Capital requirement = **Full stressed drawdown**
- Must cover mark-to-market loss at relevant confidence level

### Matching Example

| Asset | Stressed Pull-to-Par | Required Bucket | If Matched | If Unmatched |
|-------|---------------------|-----------------|------------|--------------|
| JAAA | ~42 months (30mo × 1.4x) | 42mo | ~4-5% risk weight | ~10% FRTB |
| 90-day T-bill | ~13 weeks (no stress modifier) | 3mo | ~0.5% risk weight | ~2% FRTB |
| 4-week T-bill | 4 weeks (no stress modifier) | 4wk | ~0.2% risk weight | ~1% FRTB |
| Sparklend | None | Cannot match | N/A | Gap risk capital |

### Partial Matching (Split Treatment)

When an asset position exceeds available duration capacity, the position is split into matched and unmatched portions. Each portion receives its appropriate capital treatment.

**Example:**
- Hold $500M JAAA (SPTP = 42 months, requires 42mo bucket)
- Cumulative duration capacity at 42mo+: $300M

| Portion | Amount | Treatment | CRR | Capital Required |
|---------|--------|-----------|-----|------------------|
| Matched | $300M | Duration-matched (risk weight) | 5% | $15M |
| Unmatched | $200M | FRTB (drawdown) | 10% | $20M |
| **Total** | $500M | — | — | **$35M** |

**Calculation:**
```
Matched Amount = min(Position Size, Available Duration Capacity at required bucket)
Unmatched Amount = Position Size - Matched Amount

Capital = (Matched Amount × Risk Weight) + (Unmatched Amount × FRTB Drawdown)
```

**Key property:** As duration capacity grows (longer-duration liabilities accumulate), more of each position can be matched, reducing overall capital requirements. This creates natural incentive alignment — sticky liabilities enable more efficient capital deployment.

---
