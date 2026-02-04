# Rate Limit Attack Vectors and Parameter Calibration

**Status:** Draft
**Last Updated:** 2026-02-04

---

## Executive Summary

This document analyzes two categories of attacks that constrain the choice of Initial Rate Limit (IRL) and Second-Order Rate Limit (SORL) parameters. Both attacks require a compromised executor (relayer key + cBEAM), but differ in profitability and mechanism.

The key insight is that IRL and SORL are not independent choices—they are constrained by a bootstrap target (e.g., reach 100M/day within 30 days). Higher SORL allows lower IRL and vice versa. The optimization finds the combination that minimizes total weighted harm from both attack types.

**Optimal parameters (for 100M/day target in 30 days):**
- **SORL: ~25-26%** (when modeling a second bump at `t=18h` within `TTF=24h`)
- **IRL: ~$97-124K** (implied by `IRL = 100M / (1 + SORL)^30`)

---

## Attack Categories

### Type 1: Configuration Theft

**Mechanism:**
- Attacker onboards a rate limit to an uninitialized or misconfigured vault
- Rate limit accumulates from zero over time
- Attacker waits until just before freeze (maximizing accumulated amount)
- Attacker executes attack that drains 100% of deposited funds

**Example: Morpho Vault Donation Attack**
```
T+0:     Attacker onboards IRL to uninitialized Morpho vault
         Rate limit = 0, starts accumulating at slope
T+0→18h: Accumulates at original slope
T+18h:   SORL increase applied (earliest possible given `hop=18h`)
         New max = IRL × (1 + SORL)
         New slope = slope × (1 + SORL)
T+18→24h: Accumulates at new slope
T+24h:   Attacker deposits full accumulated amount
         Manipulates vault exchange rate via donation
         Withdraws, draining entire deposit
         Freeze activates (too late)
```

**Key Properties:**
- Attacker profit = 100% of loss (direct theft)
- One-time per misconfigured surface
- Bounded by IRL and SORL accumulation
- Requires minimal attacker capital (just gas)
- Eliminable if slippage limits are set atomically with onboarding

---

### Type 2: Operational Extraction

**Mechanism:**
- Attacker cycles capital through operational routes that have inherent spread/slippage
- Each cycle causes damage to the system (slippage loss)
- Attacker captures a fraction of this damage as profit (via MEV or shorting)

**Example: Uniswap Slippage Grinding**
```
T+0:     Attacker increases rate limit (if `hop` allows), then swaps full rate limit through Uniswap
         System loses ~1% to slippage
         Attacker captures ~10% of loss via sandwich MEV
T+12h:   Rate limit replenishes, attacker repeats
T+18h:   Second SORL increase possible (if `hop=18h`), attacker continues
T+24h:   Freeze activates
```

**Key Properties:**
- Attacker profit = ~10% of loss (partial extraction)
- Repeatable while attacker has access
- Scales with achieved rate limit
- Requires attacker capital (for sandwich execution)
- Cannot be eliminated, only constrained

---

### Type 2 Profit Models

**MEV Extraction:**
- Attacker sandwiches their own transaction
- Captures ~10% of slippage as profit
- Requires capital equal to attack size
- Most common approach

**Shorting:**
- Attacker opens leveraged short position before attack
- Profits from price decline caused by damage
- Rough model: $100M loss → ~1-2% price impact → ~$1-2M short profit
- Extraction rate: ~1-2% (worse than MEV)
- Less traceable but more uncertain

**Conclusion:** Rational attacker uses MEV when possible. We model 10% extraction rate.

---

## Model Parameters

### Fixed Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Target Rate Limit | 100M/day | Steady-state operational rate limit |
| Bootstrap Time | 30 days | Time to reach target from IRL |
| Time to Freeze (TTF) | 24 hours | Detection → full shutdown |
| SORL Hop (`hop`) | 18 hours | **Onchain** cooldown between increases |
| Peacetime SORL cadence | Once per 24h | **Policy**: how often we exercise SORL in normal ops |
| SORL Cycles in Bootstrap | 30 | One per day for 30 days (peacetime cadence) |
| Damage Rate | 1% | Loss per Type 2 cycle |
| Extraction Rate | 10% | Attacker profit share (Type 2) |
| Type 2 Cycles per TTF | 2 | Round-trips possible in 24h |

### Calibrated Multipliers

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Theft Multiplier | 3× | Type 1 (theft) weighted 3× more harmful than Type 2 (loss) |
| Surface Ratio (R) | 3× | Type 2 has 3× more attack surfaces than Type 1 |

**Theft Multiplier Rationale:**

Theft is more harmful than equivalent loss because:
- Attacker profit rate: 100% (Type 1) vs 10% (Type 2)
- Higher profit = stronger attacker incentive
- Theft directly enriches attacker, funding future attacks
- 3× is conservative (profit ratio suggests 10×, adjusted for risk factors)

**Surface Ratio Rationale:**

Type 2 has more attack surfaces because:
- Type 1 requires misconfigured/initializing vaults (limited)
- Type 2 works on any operational route (many)
- Estimated 3× more operational surfaces than initialization surfaces

### Damage Rate Assumption

Fixed at 1% for this model.

The 100M/day target represents major, liquid routes (deep Uniswap pools, primary DEX pairs). These high-volume routes naturally have low slippage (~1%).

Higher slippage routes exist but have proportionally lower rate limits:

| Route Type | Slippage | Typical Rate Limit | Contribution |
|------------|----------|-------------------|--------------|
| Major pairs | ~1% | 100M/day | Primary exposure |
| Mid-tier | ~2-3% | 10-30M/day | Captured in N |
| Exotic | ~5%+ | <5M/day | Negligible |

The N multiplier implicitly captures aggregate exposure across routes of varying slippage/size.

---

## The IRL-SORL Constraint

IRL and SORL are linked by the **peacetime** bootstrap requirement (one SORL step per day):

```
IRL × (1 + SORL)^30 = 100M
```

Solving for IRL:
```
IRL = 100M / (1 + SORL)^30
```

| SORL | (1+SORL)^30 | Required IRL |
|------|-------------|--------------|
| 15% | 66.21 | $1.51M |
| 20% | 237.38 | $421K |
| 25% | 807.79 | $124K |
| 26% | 1,025.93 | $97K |
| 27% | 1,300.50 | $77K |
| 28% | 1,645.50 | $61K |
| 30% | 2,620.00 | $38K |
| 35% | 8,128.55 | $12.3K |

**The tradeoff:**
- Higher SORL → Lower IRL → Less Type 1 exposure
- Higher SORL → More marginal headroom per TTF → More Type 2 marginal exposure

---

## Harm Model

### What We're Optimizing

**Not optimizing:** Base exposure at steady state (100M/day exists regardless of IRL/SORL choice)

**Optimizing:**
- Type 1: Full IRL exposure (initialization theft)
- Type 2: **Marginal** SORL exposure (additional damage from SORL increase within TTF)

### Type 1 Harm Formula

```
Type 1 Harm = IRL × Accumulation × Theft_Multiplier × N₁
```

Where:
- Accumulation = (1 + 0.25 × SORL) — accounts for partial SORL increase in 24h
- Theft_Multiplier = 3
- N₁ = number of Type 1 attack surfaces

### Type 2 Marginal Harm Formula

```
Type 2 Marginal Harm = Base × Headroom × Damage_Rate × Cycles × N₂
```

Where:
- Base = 100M (target rate limit)
- Headroom = average marginal increase within `TTF=24h`
  - With `hop=18h` and attacker increasing at `t=0` and `t=18h`:  
    `Headroom = 0.75×SORL + 0.25×((1+SORL)^2 - 1) = 1.25×SORL + 0.25×SORL^2`
- Damage_Rate = 1%
- Cycles = 2 (per TTF)
- N₂ = 3 × N₁ (surface ratio)

Simplified:
```
Type 2 Marginal Harm = 100M × (1.25×SORL + 0.25×SORL^2) × 0.02 × 3 × N₁
                     = 6M × (1.25×SORL + 0.25×SORL^2) × N₁
```

**Note:** If the attacker cannot use the second bump within `TTF` (cooldown not available), approximate `Headroom ≈ SORL`.

### Total Harm

```
Total Harm = Type 1 Harm + Type 2 Marginal Harm
           = N₁ × [3 × IRL × (1 + 0.25×SORL) + 6M × (1.25×SORL + 0.25×SORL^2)]
```

**Critical insight:** N₁ factors out completely. The absolute number of attack surfaces doesn't affect the optimal SORL—it only scales total harm proportionally. What matters are the **ratios** (theft multiplier and surface ratio).

---

## Optimization Results

Minimizing Total Harm per N₁:

| SORL | IRL | Type 1 Harm | Type 2 Marginal | **Total** |
|------|-----|-------------|-----------------|-----------|
| 20% | $421K | $1.33M | $1.56M | $2.89M |
| 22% | $257K | $812K | $1.72M | $2.53M |
| 24% | $158K | $501K | $1.89M | $2.39M |
| 25% | $124K | $395K | $1.97M | $2.36M |
| **26%** | **$97K** | **$311K** | **$2.05M** | **$2.36M** |
| 27% | $77K | $246K | $2.13M | $2.38M |
| 28% | $61K | $195K | $2.22M | $2.41M |
| 30% | $38K | $123K | $2.39M | $2.51M |
| 35% | $12.3K | $40K | $2.81M | $2.85M |

**Optimal (continuous): SORL ≈ 25.5%, IRL ≈ $109K**  
**Optimal (integer): SORL = 26%, IRL ≈ $97K**

At this point, marginal reductions in Type 1 harm (from higher SORL) equal marginal increases in Type 2 harm.

---

## Sensitivity Analysis

### Effect of Theft Multiplier

| Theft Multiplier | Optimal SORL | Optimal IRL |
|------------------|--------------|-------------|
| 2× | ~24% | ~$162K |
| **3×** | **~25.5%** | **~$109K** |
| 5× | ~27.6% | ~$67K |
| 10× | ~30.5% | ~$34K |

Higher theft multiplier → Higher optimal SORL (prioritize reducing Type 1 by lowering IRL)

### Effect of Surface Ratio (R = N₂/N₁)

| Surface Ratio | Optimal SORL | Optimal IRL |
|---------------|--------------|-------------|
| 1× | ~30% | ~$38K |
| **3×** | **~25.5%** | **~$109K** |
| 5× | ~23.5% | ~$179K |
| 10× | ~20.8% | ~$349K |

Higher surface ratio → Lower optimal SORL (prioritize reducing Type 2 marginal)

### Effect of Target Rate Limit

| Target | Optimal SORL | Optimal IRL | Type 1 Harm | Type 2 Marginal |
|--------|--------------|-------------|-------------|-----------------|
| 10M/day | ~25.5% | ~$10.9K | ~$35K | ~$201K |
| 50M/day | ~25.5% | ~$54.7K | ~$175K | ~$1.01M |
| **100M/day** | **~25.5%** | **~$109K** | **~$349K** | **~$2.01M** |
| 500M/day | ~25.5% | ~$547K | ~$1.75M | ~$10.1M |

Optimal SORL percentage is independent of target scale—only absolute values change.

---

## Attacker Capital Requirements

**Type 1 (Configuration Theft):**
- Minimal capital required
- Just gas costs to execute transactions
- All profit comes from the misconfigured vault itself
- This makes Type 1 highly attractive (infinite ROI)

**Type 2 (Operational Extraction):**
- MEV sandwich requires capital ≈ attack size
- Shorting requires margin capital (~10% of position at 10× leverage)
- Limits who can execute large-scale Type 2 attacks
- Provides natural friction against Type 2

**Implication:** Type 1's low capital requirement is another reason to weight it more heavily in the harm model (captured in the 3× theft multiplier).

---

## Recommendations

### Primary Recommendation

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **SORL** | **26%** | Best integer % near the continuous optimum |
| **IRL** | **~$97K** | Derived from SORL given 30-day bootstrap to 100M |

### Bootstrap Timeline at Recommended Parameters

| Day | Rate Limit | Notes |
|-----|------------|-------|
| 0 | ~$97K | Initial |
| 7 | ~$491K | Week 1 |
| 14 | ~$2.48M | Week 2 |
| 21 | ~$12.5M | Week 3 |
| 28 | ~$63M | Week 4 |
| 30 | $100M | Target reached |

### Operational Risk Capital Requirement

Executor should hold operational risk capital covering worst-case loss:

```
ORC ≥ Type 1 Max Loss × N₁
    = ~$97K × 1.065 × 10
    = ~$1.04M per executor (for N₁ = 10)
```

---

## Mitigations Beyond Parameters

| Attack | Mitigation | Effect |
|--------|------------|--------|
| Type 1 | Atomic slippage limit on onboarding | Eliminates attack entirely |
| Type 1 | Lower IRL | Reduces max loss |
| Type 2 | Lower SORL | Slows ramp to dangerous marginal exposure |
| Type 2 | Rate limit caps in governance | Hard ceiling on exposure |
| Both | Faster TTF (better monitoring) | Reduces window |
| Both | Higher ORC requirements | Ensures executor skin in game |

**Priority mitigation:** Make slippage limit configuration atomic with vault onboarding. This eliminates Type 1 entirely, allowing the model to optimize purely for Type 2 (which would suggest lower SORL, higher IRL under the same bootstrap constraint).

---

## Summary

| Aspect | Type 1 (Theft) | Type 2 (Extraction) |
|--------|----------------|---------------------|
| Mechanism | Misconfigured vault drain | Slippage grinding |
| Example | Morpho donation attack | Uniswap sandwich |
| Attacker profit | 100% of loss | ~10% of loss |
| Capital required | Minimal (gas) | Significant (≈ attack size) |
| Occurrence | One-time per surface | Repeatable |
| What we optimize | Full IRL exposure | Marginal SORL exposure |
| Primary control | IRL | SORL |
| Eliminable? | Yes (atomic config) | No (inherent to DEX) |

**Key Formula:**
```
Total Harm = N₁ × [3 × IRL × (1 + 0.25×SORL) + 6M × (1.25×SORL + 0.25×SORL^2)]

Subject to: IRL × (1 + SORL)^30 = Target
```

**Optimal Solution (100M/day target):**
- SORL = 26%
- IRL ≈ $97K
- Total Harm ≈ $2.36M per N₁

---

## Appendix: Derivation of Accumulation Factor

With rate limit starting at 0 and slope = IRL / 24h:

```
T = 0 to 18h: Accumulates at original slope
  Accumulated = IRL × (18/24) = 0.75 × IRL

T = 18h: SORL applied
  New slope = slope × (1 + SORL)

T = 18h to 24h: Accumulates at new slope
  Additional = IRL × (1 + SORL) × (6/24) = 0.25 × IRL × (1 + SORL)

Total at T = 24h:
  = 0.75 × IRL + 0.25 × IRL × (1 + SORL)
  = IRL × (0.75 + 0.25 + 0.25 × SORL)
  = IRL × (1 + 0.25 × SORL)
```

For SORL = 26%: Accumulation factor = 1.065

---

*Document Version: 0.1*
