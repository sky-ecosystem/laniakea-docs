# Adversarial Analysis: Sky Risk Framework

**Status:** Draft
**Date:** 2026-02-01
**Purpose:** Critical review for framework architects with consideration of TradFi, regulatory, and institutional investor audiences

---

## Executive Summary

The Sky Risk Framework presents an ambitious attempt to create a unified capital adequacy regime for decentralised stablecoin operations. It combines genuinely innovative concepts (Lindy-based liability duration, SPTP matching) with adaptations of traditional finance mechanisms (FRTB-style drawdown, gap risk models).

**Strengths:**
- Coherent conceptual foundation distinguishing rate risk from credit spread risk
- Principled approach to matching asset duration with liability stability
- Recognition that capital quality matters (ingression curves)
- Sensible conservative defaults

**Critical Concerns:**
- Significant terminology and methodological gaps versus Basel IV/FRTB
- Insufficient specification for regulatory dialogue
- Several mechanisms appear over-engineered for their purpose
- Missing calibration evidence and validation framework

This analysis organises findings into five dimensions, each with specific recommendations.

---

## Part 1: Conceptual Soundness

### 1.1 Lindy-Based Liability Duration Model

**What it proposes:** Estimate liability duration by tracking USDS lot ages, assuming older lots represent more stable demand.

**What works:**
- The intuition is sound: money that has stayed in the system longer likely has stickier demand
- Double exponential decay model for structural caps is calibrated to actual bank run data (SVB, Credit Suisse)
- The 101-bucket granularity (0.5-month increments to 50 months) provides fine-grained matching

**Concerns:**

1. **Survivorship bias in lot age data.** Lots that haven't redeemed appear "sticky," but this conflates genuine long-term holders with:
   - Lost/abandoned wallets
   - Tokens locked in contracts that may unlock unpredictably
   - Holders waiting for a triggering event (exactly the ones who run when stressed)

2. **No stress calibration for the Lindy assumption itself.** The framework assumes Lindy-measured duration holds under stress, but the Lindy property is empirically weaker during crises. A lot that has stayed 12 months may have a 6-month expected remaining duration in normal times, but near-zero under a confidence shock.

3. **Circular dependency with SPTP capacity.** Liability duration determines SPTP capacity, which determines how assets can be matched, which affects the Prime's risk profile, which affects confidence in USDS, which affects redemption behaviour, which affects measured liability duration.

**Recommendation:** Introduce explicit stress haircuts on Lindy-measured duration. For example:
- Normal: 100% of measured duration
- Stressed: 50% of measured duration for buckets >12mo, 75% for 6-12mo
- Severely stressed: 25% floor for all durations

This would create a more conservative mapping and reduce reliance on the Lindy assumption holding during crises.

### 1.2 Rate Risk vs Credit Spread Risk Distinction

**What it proposes:** SPTP-matching protects against credit spread widening (mean-reverting) but not rate changes (potentially permanent). All fixed-rate exposure must be separately hedged.

**What works:**
- This is a genuinely useful distinction that maps to real economic behaviour
- The SSR (Sky Savings Rate) passthrough mechanism justifies treating rate risk differently
- Requiring explicit rate hedging is prudent

**Concerns:**

1. **The "rate-neutral" requirement is under-specified.** The framework states fixed-rate assets need hedging but doesn't specify:
   - Acceptable hedge instruments
   - Basis risk tolerances
   - Hedge ratio requirements
   - Roll risk treatment for shorter-dated hedges

2. **Credit spread risk assumed mean-reverting without evidence.** The SPTP mechanism assumes spreads eventually compress, but this requires:
   - Issuer survival to maturity
   - No credit migration (rating changes)
   - No liquidity deterioration in the specific instrument

   These conditions are correlated with the very stress scenarios SPTP is meant to address.

**Recommendation:**
- Specify acceptable hedge instruments and basis risk tolerances
- Add credit migration risk to the asset classification framework (not just fundamental risk weight, but transition probability)
- Clarify that SPTP protection is conditional on the issuer's continued creditworthiness

### 1.3 Gap Risk Model for Collateralised Lending

**What it proposes:** Capital for collateralised crypto lending based on jump-to-default plus liquidation loss, accounting for cascading liquidations.

**What works:**
- The recognition that collateral can gap through liquidation thresholds is correct
- Considering cascade effects from other participants is sophisticated
- The framework acknowledges this is inherently unmatched (no pull-to-par)

**Concerns:**

1. **Missing parameters.** The framework references "gap risk based on historical stress analysis" but provides no:
   - Historical stress scenarios with actual drawdown data
   - Liquidation timing assumptions
   - Market depth models
   - Cascade correlation factors

2. **Implicit assumption of liquidation execution.** Gap risk assumes you can liquidate. In severe stress:
   - Oracle prices may lag or fail
   - DEX liquidity may evaporate
   - Cascading liquidations may exceed any reasonable market depth
   - Smart contract bugs may prevent liquidation

**Recommendation:**
- Add explicit liquidation execution risk as a separate capital component
- Specify minimum oracle requirements (freshness, multiple sources)
- Define circuit breakers and their capital implications
- Reference specific historical events with quantified drawdown and recovery data (e.g., Luna collapse, FTX contagion)

### 1.4 SPTP Bucket Allocation (Tug-of-War Mechanism)

**What it proposes:** When measured SPTP capacity doesn't match reservations, Primes compete for capacity through a multi-round "tug-of-war" with distance decay and value-based priority.

**What works:**
- The basic intuition is correct: closer buckets should have priority
- Pro-rata collision resolution is fair
- The trading phase allows Pareto improvements

**Concerns:**

1. **Over-engineered for the problem.** The mechanism involves:
   - Multiple rounds and iterations
   - Distance decay with floors
   - Value-based strategy
   - Trading phases
   - Overreach trades
   - Cascade effects

   A simpler priority-based allocation (closest-first, then pro-rata for ties) would achieve similar outcomes with far less complexity.

2. **Gaming potential.** Sophisticated Primes can optimise their bucket positioning and timing to systematically extract value from less sophisticated participants.

3. **Computational burden.** Running this algorithm weekly across many Primes with fine-grained buckets may be resource-intensive.

**Recommendation:** Consider simplifying to:
- First pass: Primes claim capacity from their own bucket (full priority)
- Second pass: Remaining demand claims closest available buckets (pro-rata if contested)
- Third pass: Any remaining capacity allocated to highest-value use

This achieves 90% of the benefit with 20% of the complexity.

---

## Part 2: Basel IV / FRTB Alignment

### 2.1 Trading Book vs Banking Book Boundary

**FRTB requirement:** Clear boundary between trading book (mark-to-market, short-term trading intent) and banking book (hold-to-maturity or available-for-sale).

**Framework gap:** No explicit boundary definition. The SPTP mechanism implicitly creates something like a banking book treatment (hold to stressed pull-to-par) versus unmatched assets getting trading book treatment (FRTB drawdown), but this is not articulated in regulatory terms.

**Recommendation:** Explicitly define:
- Which assets receive "banking book" equivalent treatment (SPTP-matched)
- Which assets receive "trading book" equivalent treatment (unmatched, FRTB)
- Boundary conditions and switching rules
- Reclassification penalties (Basel IV imposes a 100% risk weight floor for 1 year on assets switching from trading to banking book)

### 2.2 Expected Shortfall Specification

**FRTB requirement:**
- Expected Shortfall at 97.5% confidence level
- Stressed calibration period
- Specific liquidity horizons: 10, 20, 40, 60, 120 days
- Separate ES calculations for modellable vs non-modellable risk factors

**Framework gap:** The document references "FRTB-style drawdown" and "Expected Shortfall" but doesn't specify:
- Confidence level (97.5%? 99%?)
- Observation period for calibration
- Liquidity horizon mapping for different asset types
- Treatment of non-modellable risk factors

**From `market-risk-frtb.md`:**
> "Inputs: Drawdown parameters by asset class (TBD)"

This is insufficient for regulatory dialogue.

**Recommendation:** Specify:
```
Asset Class          Liquidity Horizon    Stress Period     Confidence
-----------          ----------------     -------------     ----------
Investment grade     40 days              2008 GFC          97.5%
High yield           60 days              2008 GFC          97.5%
Crypto lending       120 days             Luna/FTX          97.5%
DeFi protocols       120 days             Luna/FTX          97.5%
```

### 2.3 Standardised Approach Risk Weights

**Basel IV requirement:** Risk weights based on external credit ratings or standardised categories:
- Sovereign: 0% to 150% based on rating
- Banks: 20% to 150% based on rating and SCRA grade
- Corporate: 20% to 150% based on rating
- Real estate: LTV-driven risk weights

**Framework approach:** Risk weights stated as:
- JAAA: 4-5% if matched, ~10% if unmatched
- Sparklend crypto: 1-2%+ based on gap risk

**Gap:** These numbers appear internally calibrated without mapping to regulatory categories. A TradFi audience will ask: "Where do these weights come from? How do they compare to standardised approach?"

**Recommendation:** Create mapping table:
```
Asset Type              Internal Weight    Basel IV SA Equiv    Reconciliation
----------              ---------------    -----------------    --------------
Aave USDS (AAA rated)   4-5% matched       ~8-12% SA            Conservative vs SA
Sparklend crypto        1-2%               N/A (no SA equiv)    Novel asset class
TradFi corporate IG     X%                 50-100% SA           [comparison]
```

### 2.4 Interest Rate Risk in the Banking Book (IRRBB)

**Basel IV requirement:** Banks must calculate interest rate risk for banking book exposures using standardised interest rate shocks, with Economic Value of Equity (EVE) and Net Interest Income (NII) metrics.

**Framework gap:** The SSR passthrough mechanism is mentioned, and rate hedging is required, but there is no IRRBB-equivalent framework for:
- EVE sensitivity to rate shocks
- NII impact analysis
- Outlier bank identification (15% of Tier 1 threshold under Basel IV)

**Recommendation:** Add IRRBB-equivalent section specifying:
- Standard rate shock scenarios (+/- 200bps parallel, flattening, steepening)
- Required metrics (EVE impact, NII impact)
- Threshold for additional capital

### 2.5 Default Risk Charge

**FRTB requirement:** Jump-to-default (JTD) charge for issuers, calculated per issuer with prescribed LGDs (75% for senior unsecured, 25% for covered bonds, etc.)

**Framework approach:** Gap risk model covers this for collateralised lending, but traditional credit instruments lack explicit JTD treatment.

**Recommendation:** Add explicit JTD framework for non-collateralised credit exposures:
- LGD assumptions by seniority
- Maturity scaling
- Netting and hedging recognition

### 2.6 Model Validation and Backtesting

**FRTB requirement:**
- Backtesting at 99% and 97.5% confidence levels
- Profit and Loss Attribution (PLA) tests
- Desk-level model approval
- Escalation and fallback to standardised approach

**Framework gap:** No mention of:
- Model validation requirements
- Backtesting frequency and thresholds
- Exception escalation procedures
- Fallback mechanisms

**Recommendation:** Add model governance section:
```
Validation Requirement          Frequency    Threshold         Action
----------------------          ---------    ---------         ------
P&L attribution                 Quarterly    Spearman >0.7     Review
1-day backtest (97.5%)          Daily        <12 exceptions    Pass
10-day backtest (99%)           Monthly      <4 exceptions     Pass
Annual model review             Annual       N/A               Required
```

---

## Part 3: Complexity Assessment

### 3.1 Terminology Proliferation

The framework introduces numerous novel terms that don't map cleanly to standard regulatory or finance vocabulary:

| Framework Term | Standard Equivalent | Issue |
|----------------|---------------------|-------|
| SPTP | Duration matching / ALM | Novel acronym, extra cognitive load |
| STRB | N/A | Unique to this framework |
| Lindy demand | Survival analysis | Novel application of Taleb concept |
| Ingression/egression | Subscription/redemption | Unusual terminology |
| Tug-of-war | Allocation algorithm | Colloquial, not technical |
| Synomic | N/A | Framework-specific |
| Beacon/Sentinel | N/A | Framework-specific |

**Problem:** Each novel term requires explanation and creates translation overhead for external audiences.

**Recommendation:**
- Create explicit glossary mapping framework terms to TradFi equivalents
- Consider using standard terminology where concepts are equivalent
- Reserve novel terms for genuinely novel concepts

### 3.2 Overlapping Mechanisms

The framework has multiple overlapping systems for capital and capacity management:

1. **Risk capital tiers:** IJRC, EJRC, SRC
2. **Ingression curves:** Quarter-circle with quality adjustments
3. **MC-based caps:** Worst-of liquidity metrics
4. **SPTP capacity:** Bucket allocation
5. **Tug-of-war:** Capacity redistribution
6. **Category caps:** Concentration limits with capacity rights
7. **ASC requirements:** Separate 5% peg defense capital

**Problem:** These systems interact in complex ways. A Prime must simultaneously satisfy:
- SPTP matching requirements
- Category cap constraints
- MC-based total cap
- Ingression curve efficiency
- ASC requirements
- Encumbrance ratio targets

**Recommendation:**
- Create unified capital stack diagram showing how all requirements interact
- Identify redundant constraints (if any)
- Simplify where requirements overlap

### 3.3 Weekly Settlement Cycle Complexity

The Tuesday-Wednesday settlement cycle involves:
1. Tuesday: OSRC auction, SPTP auction, LCTS settlement
2. Wednesday: Processing, generation creation
3. Queue management with multiple generations
4. Redemption rate limits
5. Subscribe queue pulls

**Problem:** The interaction between auction timing, queue generations, and redemption limits creates operational complexity that may be difficult to implement and audit.

**Recommendation:**
- Evaluate whether daily settlement (standard in TradFi) would reduce complexity
- If weekly is necessary, create detailed sequence diagrams and state machines
- Add specific failure mode handling

---

## Part 4: TradFi Credibility

### 4.1 Missing Calibration Evidence

Throughout the framework, critical parameters are stated without supporting evidence:

| Parameter | Value | Evidence Provided |
|-----------|-------|-------------------|
| Distance decay | 0.9 per bucket | None |
| Tug rate | 10% per round | None |
| MC multipliers | ×100 for weekly ADV | None |
| Ingression anchor/max | 3:1 ratio | None |
| ASC requirement | 5% | None |
| DAB proportion | 25% of ASC | None |
| EJRC duration multiplier | 1 + (months/24) | None |

**Problem:** A TradFi audience (regulators, institutional investors, auditors) will ask: "Where do these numbers come from? What analysis supports them?"

**Recommendation for each parameter:**
1. State the calibration methodology
2. Reference historical data used
3. Show sensitivity analysis
4. Document expert judgement rationale where data is unavailable

### 4.2 Stress Testing Framework Absence

**TradFi expectation:** Formal stress testing with:
- Defined scenarios (historical, hypothetical, reverse)
- Prescribed shocks to risk factors
- Capital adequacy under stress
- Recovery and resolution planning

**Framework gap:** No formal stress testing framework. The term "stressed" appears (e.g., "stressed pull-to-par") but without:
- Scenario definitions
- Prescribed stress magnitudes
- Reporting requirements

**Recommendation:** Add stress testing section:
```
Scenario             Type          Shocks Applied
--------             ----          --------------
GFC 2008             Historical    -40% equities, +300bps spreads, -5% GDP
Luna collapse        Historical    -99% crypto, +50% stablecoin redemption
Hypothetical severe  Forward       [defined shocks to all risk factors]
Reverse stress       Diagnostic    Find combination that causes failure
```

### 4.3 Regulatory Reporting Gap

**TradFi expectation:** Standardised reporting formats for:
- Capital adequacy ratios
- Large exposure reports
- Liquidity coverage ratios
- Net stable funding ratios

**Framework gap:** Internal metrics defined (CRR, TRRC, TRC, Encumbrance Ratio) but no mapping to standard regulatory reports.

**Recommendation:** Create reporting template section showing:
- Which framework metrics map to which regulatory reports
- Calculation methodology for each regulatory ratio
- Frequency and submission requirements

### 4.4 External Audit and Verification

**TradFi expectation:** Independent audit of:
- Risk model validation
- Capital calculations
- Internal controls
- Data integrity

**Framework gap:** Sentinel system provides internal verification, but no provision for external audit or regulatory examination.

**Recommendation:** Add section on:
- External audit requirements
- Audit scope and frequency
- Documentation retention
- Regulatory examination cooperation

---

## Part 5: Operational Feasibility

### 5.1 Data Requirements

The framework requires extensive data tracking:

| Data Item | Granularity | Retention | Challenge |
|-----------|-------------|-----------|-----------|
| USDS lot ages | Per wallet, per lot | Indefinite | Scale, privacy |
| Prime token trading | Weekly ADV, monthly turnover | Rolling | Exchange integration |
| Asset valuations | Daily minimum | Per asset | Oracle reliability |
| SPTP bucket capacity | Weekly | Historical | Computational load |

**Problem:** Some data requirements may be impractical:
- Lot age tracking across all wallets is computationally expensive
- Exchange trading data may not be available or reliable
- Oracle dependencies create single points of failure

**Recommendation:**
- Specify minimum viable data requirements vs nice-to-have
- Define data quality thresholds and fallback procedures
- Address privacy implications of wallet-level tracking

### 5.2 Computational Complexity

Several algorithms have high computational requirements:

| Algorithm | Complexity | Frequency |
|-----------|------------|-----------|
| Lindy measurement | O(n) where n = lots | Weekly |
| Tug-of-war | O(primes × buckets × rounds) | Weekly |
| Ingression calculation | O(capital tranches) | Per transaction |
| Category cap allocation | O(primes × categories) | Continuous |

**Problem:** As the system scales, these may become bottlenecks.

**Recommendation:**
- Provide computational complexity bounds
- Define maximum supported scale
- Specify hardware/infrastructure requirements

### 5.3 Timing and Sequencing Risks

The weekly settlement cycle creates timing dependencies:

1. Lindy measurement must complete before SPTP allocation
2. SPTP allocation must complete before capital calculation
3. Capital calculation must complete before reserve release
4. Reserve release must happen before Tuesday auction

**Problem:** Any delay cascades through the system.

**Recommendation:**
- Define SLA for each step
- Specify contingency procedures for missed deadlines
- Add buffer time in the cycle

---

## Part 6: Prioritised Recommendations

### Critical (Address Before Regulatory Engagement)

| # | Issue | Recommendation | Effort |
|---|-------|----------------|--------|
| 1 | Missing FRTB specification | Add confidence level, liquidity horizons, stress period | Medium |
| 2 | No banking/trading book boundary | Define explicit boundary and switching rules | Medium |
| 3 | Absent stress testing framework | Add scenario definitions and stress magnitudes | High |
| 4 | Missing calibration evidence | Document methodology for all key parameters | High |

### High (Address for TradFi Credibility)

| # | Issue | Recommendation | Effort |
|---|-------|----------------|--------|
| 5 | No model validation framework | Add backtesting, PLA, governance | Medium |
| 6 | Terminology translation | Create glossary mapping to TradFi terms | Low |
| 7 | Lindy stress haircuts | Add stress multipliers on measured duration | Low |
| 8 | Rate hedging specification | Define acceptable instruments, basis tolerances | Medium |

### Medium (Improve Robustness)

| # | Issue | Recommendation | Effort |
|---|-------|----------------|--------|
| 9 | Tug-of-war complexity | Consider simplification | Medium |
| 10 | Liquidation execution risk | Add separate capital component | Low |
| 11 | IRRBB equivalent | Add EVE/NII framework | Medium |
| 12 | Default risk charge | Add JTD for credit exposures | Medium |

### Lower (Polish and Completeness)

| # | Issue | Recommendation | Effort |
|---|-------|----------------|--------|
| 13 | Regulatory reporting format | Create template mapping | Low |
| 14 | External audit provisions | Add audit requirements section | Low |
| 15 | Computational bounds | Specify complexity and scale limits | Low |
| 16 | Data quality thresholds | Define minimums and fallbacks | Low |

---

## Conclusion

The Sky Risk Framework demonstrates thoughtful design and genuine innovation, particularly in its approach to liability duration estimation and the distinction between rate and credit spread risk. However, significant work is required before the framework can credibly engage with traditional finance audiences.

The most pressing gaps are:
1. **Regulatory alignment:** The "FRTB-style" treatment needs to become actual FRTB specification
2. **Evidence base:** Parameter calibration needs documented methodology
3. **Stress testing:** Formal scenarios with prescribed shocks are essential
4. **Simplification:** Some mechanisms (particularly tug-of-war) may benefit from reduction

The framework is intentionally principle-based at this stage, which is appropriate for design iteration. However, the transition to production will require the specificity that regulators and institutional counterparties expect.

---

## Appendix: Regulatory Reference Summary

### Key Basel IV / FRTB Sources

- [FRTB Overview (KPMG)](https://kpmg.com/de/en/home/insights/overview/basel-iv/basel-iv-fundamental-review-of-the-trading-book-frtb.html)
- [Expected Shortfall Design (BPI)](https://bpi.com/why-is-the-frtb-expected-shortfall-calculation-designed-as-it-is/)
- [FRTB Introductory Guide (SIFMA)](https://www.sifma.org/news/blog/the-fundamental-review-of-the-trading-book-frtb-an-introductory-guide)
- [FRTB Liquidity Horizons (Acuity)](https://www.acuitykp.com/frtb-scaling-risk-to-a-specific-liquidity-horizon/)
- [IRRBB Standard (BIS)](https://www.bis.org/bcbs/publ/d368.htm)
- [Credit Risk SA (BIS)](https://www.bis.org/publ/bcbsca04.pdf)
- [Basel IV Credit Risk SA (KPMG)](https://assets.kpmg.com/content/dam/kpmg/cn/pdf/en/2021/02/basel-iv-credit-risk-standardised-approach.pdf)
- [Basel IV Output Floor (Nordea)](https://www.nordea.com/en/news/basel-iv-is-here-what-you-need-to-know)

### Implementation Timeline Reference

| Jurisdiction | FRTB SA/SSA | FRTB IMA | Output Floor |
|--------------|-------------|----------|--------------|
| EU | Jan 2027 | Jan 2028 | 50% (2025) → 72.5% (2030) |
| Switzerland | Jan 2025 | Jan 2025 | Aligned with Basel |
| US | Uncertain | Uncertain | Uncertain |

---

*This document provides critical analysis for framework improvement. It should be read alongside the risk framework documents it references.*
