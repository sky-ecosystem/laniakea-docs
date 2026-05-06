# Asset Classification

**Status:** Draft (Phase 3 update, 2026-05-05)

The canonical per-asset data the rest of the risk framework reads from. For the framework to compose correctly, each terminal exo asset needs **one canonical risk profile** that downstream structures inherit. Without this single source of truth, every category equation re-implements asset stress with potentially different assumptions, and consistency falls apart.

Companion to:
- [`risk-decomposition.md`](risk-decomposition.md) — the five risk types asset profiles support
- [`tranching.md`](tranching.md) — tranche math reads asset stress profiles to propagate through the waterfall
- [`currency-frame.md`](currency-frame.md) — currency taxonomy and per-instrument stress profiles
- [`asset-type-treatment.md`](asset-type-treatment.md) — worked treatments per asset class consuming the profiles defined here

---

## TL;DR

Every asset has a **risk-type tuple** — properties downstream consumers read to compute capital:

| Property | What it captures |
|---|---|
| **Fundamental risk weight (RW)** | Permanent loss probability — credit default, smart contract failure, counterparty failure, regulatory seizure |
| **Drawdown distribution** | Asset-level stress profile per scenario (severe-correlated-crash, credit-crisis, stable, etc.) |
| **Slippage model** | Realized loss as a function of size and stress conditions (forced-execution risk) |
| **Stressed pull-to-par (SPTP)** | Time to converge to fundamental value under stress (for assets with maturity) |
| **Correlations** | Joint-stress relationships with other assets |
| **Currency dimension** | Frame + instrument kind (per [`currency-frame.md`](currency-frame.md)) |

The **asset-level liquidity profile** — combining drawdown distribution, slippage model, and correlations — is the load-bearing primitive that the unified `forced-loss-capital` math runs against (per [`tranching.md`](tranching.md) and [`risk-decomposition.md`](risk-decomposition.md)).

Asset profile atoms live in `&core-framework-asset-stress-profile`. Adding a new asset class is governance-paced and requires populating each component.

---

## Section map

| § | Topic |
|---|---|
| 1 | The risk-type tuple |
| 2 | The asset-level liquidity profile |
| 3 | Stressed pull-to-par (SPTP) |
| 4 | Per-asset stress profile schema |
| 5 | Where the data lives |
| 6 | Consistency discipline |

---

## 1. The risk-type tuple

Each asset registers a complete tuple of properties that downstream consumers read:

### A. Fundamental risk (RW)

What can go wrong even if held to maturity:
- Credit default (the obligor stops paying)
- Smart contract failure (protocol bug, exploit)
- Counterparty failure (custody loss, exchange failure)
- Regulatory seizure

This is the irreducible risk that doesn't go away with time. Expressed as a **risk weight** percentage. Default capital is always required against it (per [`risk-decomposition.md`](risk-decomposition.md)).

In the new framework, RW is the **floor** of the capital envelope — combined with forced-sale terms via `max(RW, forced-loss-capital)` for un-matched positions.

### B. Drawdown distribution

How far the asset could fall from current price under stress, per scenario:

```metta
(asset-drawdown-distribution eth
   (scenario severe-correlated-crash (drop 0.55))
   (scenario credit-crisis           (drop 0.20))
   (scenario stable                  (drop 0.05)))
```

Calibrated empirically (historical crashes, stress sims). Read by tranche math (per [`tranching.md`](tranching.md)) and by `tradingbook` forced-loss equations.

### C. Slippage model

Realized loss as a function of position size and stress conditions:

```metta
(asset-slippage-model eth
   (depth-fn (impact-bp-per-million ...))
   (stress-multiplier (stress-1.0 1.0) (stress-2.0 2.5) (stress-3.0 5.0)))
```

Captures the size-dependent and condition-dependent execution cost of forced unwind. Read by `tradingbook` and by Hedgebook closing-loss math (per [`hedgebook.md`](hedgebook.md)).

### D. Stressed pull-to-par (SPTP)

For assets that mature or converge to a known value, the time to converge under stress (see §3 for full treatment).

### E. Correlations

Joint-stress relationships:

```metta
(correlation-with eth btc 0.85)
(correlation-with eth stETH 0.95)
```

Read by category equations to model joint stress. Critical for crash-scenario calibration; misspecified correlations are a major source of model error.

### F. Currency dimension

Per [`currency-frame.md`](currency-frame.md):
- Frame the asset is denominated in (USD, EUR, BTC)
- Currency kind (`unit-of-account`, `stablecoin-proxy`, `native-volatile-asset`)
- Stress profile relative to its frame (depeg for proxies, volatility for native assets)

---

## 2. The asset-level liquidity profile

The drawdown distribution + slippage model + correlations together form the **asset-level liquidity profile** — the primitive that the unified `forced-loss-capital` math runs against.

```metta
(asset-liquidity-profile eth
   (drawdown-distribution
      (scenario severe-correlated-crash (drop 0.55) (window 24h))
      (scenario credit-crisis           (drop 0.20) (window 7d))
      (scenario stable                  (drop 0.05) (window 30d)))
   (slippage-model
      (depth-fn (impact-bp-per-million ...)))
   (correlation-with btc   0.85)
   (correlation-with stETH 0.95))
```

Any category equation that touches ETH (a tranched exobook with ETH collateral, an ETH-only Riskbook, a structured product with ETH exposure) reads this profile and stresses against it. **No category re-derives ETH's risk from scratch.**

This is the load-bearing primitive that makes everything above compose correctly. Without it, every category equation re-implements asset stress with potentially different assumptions, and consistency falls apart.

### Why "stress profile" not just "drawdown"

The old framework had separate "drawdown risk" (FRTB-style for tradeables) and "gap risk" (for collateralized lending). Both were the same thing applied to different asset classes. The new framework unifies them via the asset-level liquidity profile: one canonical stress profile per asset, propagated through whatever structure sits over it (per [`tranching.md`](tranching.md) §6).

---

## 3. Stressed pull-to-par (SPTP)

For assets that mature or converge to a known value, **Stressed Pull-to-Par** is the time to converge to fundamental value under stress conditions.

### Why stressed pull-to-par

Normal pull-to-par (or WAL for amortizing assets) assumes typical prepayment and amortization patterns. But the scenario where asset duration matters for capital is precisely the stress scenario:
- During crises, prepayments slow dramatically (borrowers can't refinance)
- Amortization continues but reinvestment into new loans slows
- Pull-to-par extends, sometimes significantly

Using unstressed duration would be like stress-testing a lifeboat in calm seas. Duration matching validity must hold during stress.

### SPTP calculation

```
Stressed Pull-to-Par = Normal Pull-to-Par × Stress Modifier
```

The stress modifier is derived from historical worst-case prepayment slowdowns for equivalent asset classes:

| Asset Class | Normal Pull-to-Par | Stress Modifier | Stressed Pull-to-Par | Historical Basis |
|---|---|---|---|---|
| CLO AAA (JAAA) | ~2.5 years | 1.4× | ~3.5 years | 2008-2009: prepayments dropped from 28% to 9-15% |
| Agency MBS | Varies | 1.2-1.5× | Varies | Rate-dependent; extension risk in rising rate environments |
| Corporate bonds | To maturity | 1.0× | To maturity | Fixed maturity, no prepayment optionality |
| T-bills | To maturity | 1.0× | To maturity | Fixed maturity, no extension risk |
| Money market ETF | Near-zero | 1.0× | Near-zero | Daily liquidity, stable NAV |

**Key insight:** the stress modifier should reflect the *same* stress scenario that drives liability outflows. If a credit crisis causes both duration extension and depositor flight, the stressed pull-to-par ensures the asset-liability match remains valid under that scenario.

### SPTP refinement: spread duration vs rate duration

V1 carries a refinement deferred from prior versions: SPTP should split into two components:

| Component | What it measures | Covered in |
|---|---|---|
| **Credit-spread duration** | Time to convergence under spread stress (mean-reverting) | `termbook` and `structbook` cover this |
| **Rate duration** | Time to convergence under rate stress (potentially permanent regime shift) | Only `termbook` (matched fixed/fixed) covers this; `structbook` doesn't |

Both values per position. For v1 NFATs both equal the nominal term (no stress modifier — fixed-term contracts).

### Assets without SPTP

- **ETH:** Infinite (no pull-to-par — perpetual volatility)
- **Sparklend positions:** None (perpetual, no maturity)

Assets with no SPTP cannot be matched in `termbook`/`structbook` regardless of stress assumptions. They route to `tradingbook` (if liquid) or unmatched.

---

## 4. Per-asset stress profile schema

Putting it all together:

```metta
(asset-category eth
   (frame eth)                                            ; from currency-frame
   (currency-kind native-volatile-asset)
   (oracle-pair eth/usd)
   
   ;; Fundamental risk
   (risk-weight m2m 0.25)
   (risk-weight htm 0.20)
   
   ;; Drawdown / liquidity
   (drawdown-distribution
      (scenario severe-correlated-crash (drop 0.55) (window 24h))
      (scenario credit-crisis           (drop 0.20) (window 7d))
      (scenario stable                  (drop 0.05) (window 30d)))
   (slippage-model
      (depth-fn (impact-bp-per-million ...)))
   
   ;; SPTP (if applicable)
   (sptp infinite)                                        ; no maturity
   
   ;; Correlations
   (correlation-with btc   0.85)
   (correlation-with stETH 0.95))
```

For assets with SPTP:

```metta
(asset-category jaaa
   (frame usd)
   (currency-kind unit-of-account)
   
   (risk-weight m2m 0.05)
   (risk-weight htm 0.04)
   
   (drawdown-distribution ...)
   (slippage-model ...)
   
   ;; SPTP refinement
   (sptp credit-spread 1260)                              ; days; from credit-spread duration
   (sptp rate          1260)                              ; days; from rate duration
   
   (correlation-with us-treasuries 0.30)
   (correlation-with hy-credit     0.65))
```

The schema is open: new properties get added as the framework matures. Categories declare which properties they consume; consistency is checked at category registration.

---

## 5. Where the data lives

| Atoms | Space |
|---|---|
| Currency identity | `&core-registry-currency` |
| Currency stress profile | `&core-framework-currency-stress` |
| Per-asset risk weights | `&core-framework-asset-stress-profile` |
| Asset drawdown distributions | `&core-framework-asset-stress-profile` |
| Asset slippage models | `&core-framework-asset-stress-profile` |
| Asset correlations (joint) | `&core-framework-asset-correlations` |
| Stress scenarios (parameter vectors) | `&core-framework-stress-scenarios` |

The split between identity (rare changes) and stress profile (recalibrated more often) is intentional: identity is governance-paced; stress profiles are recalibrated as data accumulates and conditions change.

Every endoscraper, oracle, attestor, Riskbook category equation, projection model, sentinel formation, and warden reads from these spaces. They are universally replicated (per the synome's hub-replication of `&core-*` spaces).

---

## 6. Consistency discipline

The asset-level liquidity profile is the load-bearing primitive — the single source of truth that downstream consumers read. The discipline:

- **One profile per asset.** No category may inline its own asset stress assumptions.
- **Calibration is governance-paced.** Updating a stress profile is a governance act with rationale, not an ad-hoc fudge.
- **Every category equation that consumes a profile must declare which one.** Audit can verify that consumption matches declaration.
- **New asset classes require full schema.** Without all components (RW, drawdown, slippage, correlations, currency dimension, SPTP if applicable), the asset can't be onboarded — it would fall to CRR 100% (default-deny).

This discipline prevents the failure mode where every category re-derives asset stress with slightly different assumptions, producing apparent diversification through inconsistency.

---

## File map

| Doc | Relationship |
|---|---|
| [`risk-decomposition.md`](risk-decomposition.md) | The five risk types; asset profile feeds the forced-loss-capital math |
| [`tranching.md`](tranching.md) | Tranche waterfall reads asset drawdown distribution to propagate stress |
| [`currency-frame.md`](currency-frame.md) | Currency taxonomy and per-instrument stress profiles |
| [`asset-type-treatment.md`](asset-type-treatment.md) | Worked treatments per asset class consuming this data |
| [`riskbook-layer.md`](riskbook-layer.md) | Riskbook category equations consume asset profiles |
| [`projection-models.md`](projection-models.md) | Projection models for complex positions take asset profiles as inputs |
| [`matching.md`](matching.md) | SPTP-based matching mechanics |
| [`open-questions.md`](open-questions.md) | Crypto stress scenario calibration is one of the open items |
