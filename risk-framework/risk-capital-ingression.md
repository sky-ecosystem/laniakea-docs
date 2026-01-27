# Risk Capital Ingression

**Status:** Draft
**Last Updated:** 2026-01-27

---

## Overview

Risk Capital Ingression defines how Primes receive and recognize external risk capital as part of their official capital base under the Sky Risk Framework.

| Term | Definition |
|------|------------|
| **Egression** | External party injects capital into a Prime |
| **Ingression** | Prime receives and recognizes that capital on its balance sheet |
| **Ingression Rate** | The ratio of effectively ingressed capital to nominally egressed capital (0 to 1) |

**Core Principle:** Not all egressed capital counts equally. The ingression rate depends on capital quality — synomic status, duration commitment, and the Prime's existing capital composition.

---

## The Universal Ingression Curve

All ingression uses the same curve shape: a **flat zone** followed by a **quarter circle**.

### Curve Shape

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
      |                                                        \
      |                                                        |
      |                                                        |
 0.0  +---------------------|----------------------------------|-----> Capital
      0                  anchor                               max
      |------- flat --------|------------ curve ---------------|
      |-------- 1x ---------|--------------- 2x ---------------|
```

**Three zones:**

| Zone | Range | Marginal Rate |
|------|-------|---------------|
| **Flat** | 0 to anchor | 1.0 (full ingression) |
| **Curve** | anchor to max | Quarter circle: √(1 - ((x - anchor)/(max - anchor))²) |
| **Cap** | beyond max | 0 (no additional ingression) |

### Formula

```
For x ≤ anchor:
    marginal_rate = 1.0

For anchor < x ≤ max:
    marginal_rate = √(1 - ((x - anchor) / (max - anchor))²)

For x > max:
    marginal_rate = 0
```

### Key Properties

- **Smooth transition** at anchor point (tangent is horizontal, no kink)
- **Steepens progressively** as you approach max
- **Vertical at max** (marginal rate hits zero)
- **Max effective capital** = anchor + (max - anchor) × π/4

---

## SRC Ingression (Senior Risk Capital)

SRC ingression rate depends on the Prime's effective JRC base.

### Parameters

| Parameter | Value |
|-----------|-------|
| **Anchor** | 1.5 × effective JRC |
| **Max** | 4.5 × effective JRC |
| **Ratio** | 3:1 (max = 3 × anchor) |

### Example with 100M Effective JRC

| SRC:JRC | SRC Nominal | Marginal Rate | Cumulative Effective | Efficiency |
|---------|-------------|---------------|----------------------|------------|
| 0.5:1 | 50M | 100% | 50M | 100% |
| 1:1 | 100M | 100% | 100M | 100% |
| 1.5:1 | 150M | 100% | 150M | 100% |
| 2:1 | 200M | 98.6% | 199.8M | 99.9% |
| 2.5:1 | 250M | 94.3% | 248.1M | 99.2% |
| 3:1 | 300M | 86.6% | 293.5M | 97.8% |
| 3.5:1 | 350M | 74.5% | 334.0M | 95.4% |
| 4:1 | 400M | 55.3% | 366.9M | 91.7% |
| 4.5:1 | 450M | 0% | 385.6M | 85.7% |
| 5:1 | 500M | 0% | 385.6M | 77.1% |

**Max theoretical effective SRC** = 1.5 × JRC + 3 × JRC × π/4 ≈ **3.86 × effective JRC**

---

## EJRC Ingression (External Junior Risk Capital)

EJRC ingression depends on two quality dimensions: **synomic status** and **duration commitment**.

### EJRC Types

| Type | Synomic | Duration | Mechanism |
|------|---------|----------|-----------|
| **Normie TEJRC** | No | Zero | LCTS token, anyone can participate |
| **Non-synomic duration** | No | Yes | Bespoke deal, funds → SubProxy, ecosystem accord in Synome |
| **Synomic duration** | Yes | Variable | Bespoke deal between Synomic agents, baseline sentinels interact |

### Quality Dimensions

**Synomic status:** Whether the egression decision was made by a framework encoded in the Synome — auditable, transparent, provably not stupid.

- Non-synomic: base multiplier (1×)
- Synomic: 2× multiplier on anchor and max

**Duration commitment:** How long the capital is committed before it can exit.

- Maximum useful duration: 24 months
- Minimum threshold: 3 months (below this, no duration credit)
- Linear scaling from 3 to 24 months

### EJRC Anchor/Max Formula

```
duration_multiplier = 1 + (months / 24)    for months ≥ 3
duration_multiplier = 1                     for months < 3

synomic_multiplier = 2    if synomic
synomic_multiplier = 1    if non-synomic

anchor = 1 × IJRC × synomic_multiplier × duration_multiplier
max = 3 × IJRC × synomic_multiplier × duration_multiplier
```

### EJRC Ingression Table

| Type | Duration | Duration Mult | Anchor | Max |
|------|----------|---------------|--------|-----|
| Non-synomic | 0-3mo | 1.0 | 1× | 3× |
| Non-synomic | 3mo | 1.125 | 1.125× | 3.375× |
| Non-synomic | 6mo | 1.25 | 1.25× | 3.75× |
| Non-synomic | 12mo | 1.5 | 1.5× | 4.5× |
| Non-synomic | 24mo | 2.0 | 2× | 6× |
| Synomic | 0-3mo | 1.0 | 2× | 6× |
| Synomic | 3mo | 1.125 | 2.25× | 6.75× |
| Synomic | 6mo | 1.25 | 2.5× | 7.5× |
| Synomic | 12mo | 1.5 | 3× | 9× |
| Synomic | 24mo | 2.0 | 4× | 12× |

---

## Duration Mechanics

### Structure Options

EJRC can be structured as:

| Structure | Mechanics | Exit |
|-----------|-----------|------|
| **Perpetual until called** | Runs indefinitely until one party calls exit | Call → countdown → exit |
| **Fixed term** | Agreed start-to-end duration | Auto-exits at end |

### Uningression Delay

The **uningression delay** is the countdown period after exit is called. It's agreed upfront and determines the load (quality) of the EJRC.

| Uningression Delay | Effect on Load |
|--------------------|----------------|
| 24 months (max) | Lowest load, highest quality |
| 12 months | Medium load |
| 6 months | Higher load |
| 3 months (min for credit) | Highest load that still gets duration credit |
| < 3 months | No duration credit |

**Key insight:** If you agree to a shorter uningression delay (e.g., 12 months), your perpetual phase load is as if you're always at that point in the countdown. The load is constant — capital doesn't get dumber just because time passes.

### Exit Mechanics

Either party can initiate exit:

| Initiator | Process |
|-----------|---------|
| **Egressor calls exit** | Countdown begins (based on agreed delay) → exit |
| **Prime releases** | Countdown begins (based on agreed delay) → exit |

**Instant exit rules:**

| Party | Instant Exit |
|-------|--------------|
| **Egressor** | Never allowed (abuse risk — could enable coordinated attacks) |
| **Prime** | Only if negotiated upfront |

**Why Prime might negotiate instant release:**
- Flexibility to swap capital sources
- New, cheaper EJRC becomes available
- Egressor accepts more risk → may demand higher yield

---

## Normie TEJRC (Tokenized EJRC)

TEJRC is the standard, tokenized form of EJRC accessible via LCTS.

### Subscribe (Ingression)

- Prime pulls from LCTS SubscribeQueue at will
- No limit on how fast Prime can ingress

### Redeem (Uningression)

- Prime sets redemption rate (e.g., 20% of ingressed TEJRC per week max)
- Plus minimum fixed amount (ensures some liquidity)
- Rate changes require governance + long delay (TEJRC holder protection)

### TEJRC Quality

TEJRC is always:
- **Non-synomic** (synomic EJRC uses bespoke bilateral deals)
- **Zero duration** (no contractual lock, just queue constraints)

This makes normie TEJRC the lowest quality EJRC with anchor = 1× IJRC, max = 3× IJRC.

---

## MC-Based Total RC Cap

The Prime token metrics provide an upper limit on **total effective ingression** (IJRC + EJRC + SRC). This ensures total leverage capacity is tied to market validation of the Prime.

### The Principle

A Prime's capital is only as credible as the market believes the Prime is. If the Prime token is worthless or illiquid, the Prime's "skin in the game" is meaningless — there's nothing of value at stake, or no genuine price discovery.

### Equivalent MC Calculation

Each metric converts to an **equivalent MC** via a multiplier. The effective MC is the minimum across all metrics.

```
effective_MC = min(actual_MC, equiv_MC_volume..., equiv_MC_turnover...)
```

### Metrics and Multipliers

**Volume Metrics (ADV = Average Daily Volume):**

| Metric | Healthy Level | Multiplier | Equivalent MC Formula |
|--------|---------------|------------|----------------------|
| Weekly ADV | 1.0% of MC | ×100 | weekly_adv × 100 |
| Monthly ADV | 0.8% of MC | ×125 | monthly_adv × 125 |
| Quarterly ADV | 0.6% of MC | ×167 | quarterly_adv × 167 |

**Turnover Metrics (unique tokens changing hands):**

| Metric | Healthy Level | Multiplier | Equivalent MC Formula |
|--------|---------------|------------|----------------------|
| Monthly turnover | 3.5% of supply | ×29 | monthly_turnover × MC × 29 |
| Quarterly turnover | 6.5% of supply | ×15 | quarterly_turnover × MC × 15 |
| Yearly turnover | 10% of supply | ×10 | yearly_turnover × MC × 10 |

**Note:** Turnover measures distinct tokens that changed hands, not just volume. High volume with low turnover indicates wash trading (same tokens traded back and forth).

### Worst-of-Observed Approach

The effective MC is the **minimum** of actual MC and all equivalent MCs:

```
effective_MC = min(
    actual_MC,
    weekly_adv × 100,
    monthly_adv × 125,
    quarterly_adv × 167,
    monthly_turnover × MC × 29,
    quarterly_turnover × MC × 15,
    yearly_turnover × MC × 10
)
```

**Why "worst of":** You need ALL signals to be healthy. One weak link caps everything.

| Scenario | What It Catches |
|----------|-----------------|
| High MC + low volume | Illiquid, price is stale |
| High volume + low turnover | Wash trading |
| High turnover + low MC | Token not valued by market |

### MC-Based Ingression Curve

| Parameter | Value |
|-----------|-------|
| **Anchor** | 5× effective MC |
| **Max** | 15× effective MC |
| **Ratio** | 3:1 (consistent with other curves) |

Same flat + quarter circle shape as other ingression curves.

### Example

**Prime with $100M effective MC:**

| Total Effective RC | Zone | Marginal Rate |
|--------------------|------|---------------|
| $0 - $500M | Flat | 100% |
| $500M - $1.5B | Curve | 100% → 0% |
| > $1.5B | Cap | 0% |

**Max theoretical total RC** = 5× + 10× × π/4 ≈ **12.85× effective MC**

### Worked Example: Bottleneck Identification

| Metric | Raw Value | Multiplier | Equivalent MC |
|--------|-----------|------------|---------------|
| Actual MC | $200M | — | $200M |
| Weekly ADV | $1.5M (0.75%) | ×100 | $150M |
| Monthly ADV | $1.2M (0.6%) | ×125 | $150M |
| Quarterly ADV | $1.0M (0.5%) | ×167 | $167M |
| Yearly turnover | 8% | ×10 | $160M |

```
effective_MC = min($200M, $150M, $150M, $167M, $160M) = $150M
```

**Bottleneck:** Weekly and monthly ADV are below healthy levels. The Prime can ingress up to:
- Anchor: $750M total effective RC (full rate)
- Max: ~$1.93B total effective RC (theoretical max)

### Independent Trader Registry (Future)

An additional metric is planned but TBD: **independent trader participation**.

Key principles:
- Reputation based on profitable Prime token trading across *multiple* Primes
- Indifference to which Prime signals genuine price discovery
- A trader who only trades one Prime's token could be an insider

This metric would add another equivalent MC to the worst-of calculation.

---

## Capital Requirement Calculation

For Prime capital adequacy:

```
Effective JRC = IJRC + Σ(EJRC_i × EJRC_ingression_rate_i)

Effective SRC = Σ(SRC_j × SRC_ingression_rate_j)

Total Effective Risk Capital = (Effective JRC + Effective SRC) × MC_multiplier

Capital Adequacy = Total Effective Risk Capital ≥ Required Risk Capital
```

Where Required Risk Capital comes from the General Risk Framework (SPTP matching, gap risk, etc.).

---

## Incentive Alignment

The continuous ingression rate creates natural incentives:

| Behavior | Incentive |
|----------|-----------|
| **Build IJRC first** | Higher ingression rates for subsequent EJRC and SRC |
| **Attract quality EJRC** | Synomic + long-duration EJRC ingresses more efficiently |
| **Maintain Prime token health** | MC-based cap rewards healthy token metrics |
| **Gradual scaling** | No cliff effects; smooth capital expansion |
| **Quality over quantity** | 10M at high rate > 20M at low rate |

---

## Summary

### Ingression Hierarchy

```
Prime Token Metrics → MC-based cap on total
          ↓
       IJRC (base)
          ↓
       EJRC (quality-adjusted)
          ↓
       SRC (JRC-ratio adjusted)
```

### Key Parameters

| Curve | Base | Anchor | Max | Ratio |
|-------|------|--------|-----|-------|
| EJRC (normie) | IJRC | 1× | 3× | 3:1 |
| EJRC (synomic, 24mo) | IJRC | 4× | 12× | 3:1 |
| SRC | Effective JRC | 1.5× | 4.5× | 3:1 |
| MC-based | Effective MC | 5× | 15× | 3:1 |

All curves use the same quarter-circle shape with 3:1 max-to-anchor ratio.

### MC Metrics Summary

| Metric | Healthy Level | Multiplier |
|--------|---------------|------------|
| Weekly ADV | 1.0% of MC | ×100 |
| Monthly ADV | 0.8% of MC | ×125 |
| Quarterly ADV | 0.6% of MC | ×167 |
| Monthly turnover | 3.5% of supply | ×29 |
| Quarterly turnover | 6.5% of supply | ×15 |
| Yearly turnover | 10% of supply | ×10 |

---

*This document defines the continuous ingression rate model. For LCTS queue mechanics, see `smart-contracts/lcts.md`. For capital requirements, see `risk-framework/README.md`.*
