# Correlation Framework (Two-Level Concentration)

**Status:** Draft (Phase 3 update, 2026-05-05)

Concentration limits live at **two levels** in the new framework: Primebook (own categories) and Genbook (system-wide). The mechanism is unchanged — governance-defined categories with hard caps, 100% CRR on excess, capacity rights to prevent displacement — but the architectural placement is now explicit.

Companion to:
- [`risk-decomposition.md`](risk-decomposition.md) — concentration amplification is the fifth risk type
- [`primebook-composition.md`](primebook-composition.md) — Primebook-level concentration limits
- [`asset-classification.md`](asset-classification.md) — per-asset correlations feed scenario calibration
- [`hedgebook.md`](hedgebook.md) — concentration interaction with hedges (gross-of-hedge in v1)

---

## TL;DR

Two-level concentration framework:

| Level | What it limits | Why here |
|---|---|---|
| **Primebook** | Concentration within a Prime's own portfolio across its Halobooks | The Prime sees across its own Halos; can rebalance |
| **Genbook** | System-wide concentration across all Primes serving a Generator | Sky-level systemic stability; can't be managed by any single Prime |

The mechanism at both levels is the same:
1. Governance defines **Correlation Categories** (e.g., "CLOs", "US-based assets", "real estate")
2. Each category has a **cap** as % of the relevant scope (Primebook portfolio or system supply)
3. Every asset is classified into one or more categories at onboarding
4. If aggregate exposure exceeds a cap, the **excess portion** is subject to **100% CRR** (no leverage on the excess)
5. **Capacity rights** ("grandfathered slices") prevent new deployers from instantly displacing incumbents

The cap-enforcement mechanism is intentionally simple. The *choice of cap values* can be calibrated through scenario stress (see §3).

---

## Section map

| § | Topic |
|---|---|
| 1 | Why two levels |
| 2 | The mechanism (caps, excess penalty, capacity rights) |
| 3 | Scenario calibration |
| 4 | Hedge interaction (gross-of-hedge in v1) |
| 5 | Outputs and reporting |
| 6 | Open questions |

---

## 1. Why two levels

A single Prime can rebalance within its own portfolio: if Spark is over-concentrated in CLOs, Spark can rotate exposure into different categories. This is **Primebook-level concentration** — limits on a Prime's own portfolio.

System-wide concentration is different: even if every Prime is individually well-diversified, the aggregate across all Primes serving the same Generator could be over-concentrated. Spark holds 8% CLOs, Grove holds 12%, Keel holds 6%, Obex holds 4% — all individually fine, but in aggregate 30% of USDS supply is backing CLOs. **Genbook-level concentration** addresses this.

The two levels are independent:
- A Prime can be over its Primebook cap on a category but under the Genbook share (the Prime is too concentrated; reduce within-Prime)
- A Prime can be under its Primebook cap but over the Genbook share (the system is too concentrated; the Prime gets pro-rata penalty even though it's individually fine)

| Failure mode | Caught by |
|---|---|
| Single Prime over-concentrated | Primebook category cap |
| Multiple Primes individually OK but aggregate over-concentrated | Genbook category cap |
| Prime adds to a category that's already at Genbook cap | Genbook excess penalty (Prime pays even though it's not individually over-cap) |

V1 implementation: Genbook-level only (per the original `correlation-framework.md`). Primebook-level concentration deferred to Phase 3+. This doc reflects the target architecture; v1 manages concentration at one level.

---

## 2. The mechanism

### Categories

A category is an arbitrary governance-defined label used for concentration limits. Examples: "CLOs", "US-based assets", "40-50 month duration", "real estate", "ETH-backed lending".

Categories are not mutually exclusive. An ETH-backed loan to a US-based borrower might be in three categories: ETH-collateral, USD-denominated, US-jurisdiction.

```metta
(concentration-category-def clos
   (description "Collateralized Loan Obligations and CLO derivatives")
   (membership-test (asset-class-in (jaaa cmaa cml private-clo)))
   (cap-percent 0.10))                                     ; 10% of total portfolio
```

Categories live in `&core-framework-concentration` (per [`asset-classification.md`](asset-classification.md) §5).

### Exposure measure

Caps are measured on a unified "portfolio exposure" basis, but the measurement differs by treatment:

- **Matched exposure** (`structbook` / `termbook` matched portion): measured using notional / duration-value (the "hold-to-maturity" relevant size)
- **Unmatched exposure** (`tradingbook` / unmatched portion): measured using market value (MTM)

Interpretation: if an exposure is treated as forced-sale (unmatched), it consumes category capacity by its MTM size; if it is treated as duration-matched, it consumes by notional.

### Cap and excess penalty

For each category `c`:

```
cap_amount[c] = cap_percent[c] × total_portfolio
excess[c] = max(0, exposure_total[c] - cap_amount[c])
```

Only the **excess portion** receives the **100% CRR** penalty. The 100% CRR penalty is applied **once** (not stacked) even if an exposure is tagged into multiple categories — the Prime pays the maximum binding category, not the sum.

```metta
(= (effective-crr $position)
   (max (base-crr $position)
        (excess-portion-crr $position)))
```

### Capacity rights ("grandfathered slices")

To prevent new deployers from instantly pushing old holders out of a capped category, each category maintains a per-Prime non-transferable allocation:

- `alloc[p][c]` = Prime `p`'s current "in-cap" share for category `c`
- `Σ_p alloc[p][c] = cap_amount[c]`

This allocation changes gradually based on which Primes have been paying the over-cap penalty.

**Normalization period:**
```
T = max(asset_SPTP, 3 months)
```

Longer-duration assets take longer to normalize; very short durations still have a minimum normalization of 3 months.

**Reallocation rule (daily settlement):**
- Compute each Prime's category exposure `E[p][c]`
- Compute "penalized amount" `P[p][c] = max(0, E[p][c] - alloc[p][c])`
- Update allocations by shifting capacity toward Primes that have been paying penalties, with rate `α = (1 epoch) / T`

Mechanically: if you are over-cap by `P`, then over time `T` you earn roughly `P` of in-cap capacity. That earned capacity comes from existing in-cap allocations, which pushes incumbents into partial penalty and triggers a "fight back" dynamic.

The exact update function (EMA vs explicit per-epoch reallocation) is an open question (per [`open-questions.md`](open-questions.md)).

---

## 3. Scenario calibration

The cap system is intentionally simple to enforce. The *choice of cap values* gets updated over time using a scenario stress engine.

### Scenario engine

Define a scenario set `S` (credit crisis, crypto crash, stablecoin confidence shock, etc.). For each scenario `s` and category `c`, estimate the **loss severity per unit exposure**:

- `L(c, s)` = stressed loss per $1 of category exposure under scenario `s`

Choose caps such that portfolio losses remain within a governance-defined **loss budget**:

- `B(s)` = maximum portfolio loss fraction tolerated under scenario `s`

This turns "correlation" into a concrete calibration surface rather than an abstract covariance matrix.

### Two ways to derive caps

**Method A (simple, independent caps):**

```
cap_percent[c] = min_s ( B(s) / L(c, s) )
```

"Even if the entire allowed slice of category `c` is held, the portfolio survives each scenario's budget." Simple and robust but conservative — ignores interactions.

**Method B (joint optimization):**

```
For each scenario s:
  Σ_c cap_percent[c] * L(c, s) ≤ B(s)
```

Subject to additional governance constraints (floors/ceilings per category, max change per update, policy overrides). Allows preferred composition while satisfying scenario constraints.

The choice between Method A and Method B is one of the open questions (per [`open-questions.md`](open-questions.md)).

### Governance controls

Governance sets:
- Scenario set `S` and budgets `B(s)`
- Cap update cadence (daily at settlement vs monthly)
- Smoothing / rate limits on cap changes (e.g., ±X% per update)
- Emergency freeze: ability to halt cap updates while keeping enforcement active

---

## 4. Hedge interaction (gross-of-hedge in v1)

Concentration limits interact with hedge accounting. Two extremes:

| Approach | What it counts |
|---|---|
| **Gross-of-hedge** | Concentration measured on raw exposure, ignoring hedges |
| **Net-of-hedge** | Concentration measured on residual after hedges applied |

V1: **gross-of-hedge.** Hedges reduce capital but don't eliminate concentration concerns. A Prime with $1B credit exposure and $900M index-CDS hedge has $100M residual credit risk for capital purposes but $1B credit exposure for concentration purposes.

Why gross: a hedge can fail (counterparty risk, basis blow-out, liquidity on closing). The structural concentration is the real exposure; the hedge is a partial offset against capital, not a structural replacement.

V2+ may add hybrid: `effective_concentration = max(net_of_hedge, gross × hedge_failure_haircut)`. Deferred.

---

## 5. Outputs and reporting

Per category `c`:
- `cap_percent[c]`, `cap_amount[c]`
- `exposure_total[c]`
- `utilization[c] = exposure_total[c] / cap_amount[c]`

Per Prime `p` and category `c`:
- `alloc[p][c]`
- `E[p][c]`
- `P[p][c]` (penalized / over-allocation amount)

Portfolio-level:
- Total over-cap exposure (non-stacked)
- Total 100%-CRR-required capital due to category caps

These outputs flow to sentinel-integration and risk-monitoring:
- Sentinels read concentration utilization for scaling / rebalancing decisions
- Risk monitoring alerts when utilization approaches caps
- Settlement processes apply the excess penalty per epoch

---

## 6. Open questions

Tracked in [`open-questions.md`](open-questions.md):

1. **Allocation update function** — EMA vs explicit per-epoch reallocation, where it lives (beacon vs on-chain vs governance process)
2. **Multi-category assets without double counting** — binding category vs portfolio-wide max penalty
3. **Per-Prime vs per-Prime-type vs global caps** — whose limits apply at which level
4. **Category versioning and migration** — how categories evolve when governance changes definitions
5. **Method A vs Method B** — which cap-calibration method should be canonical
6. **Definition of `L(c, s)`** — minimal data required to safely add a new category

V1 implementation focuses on Genbook-level concentration with manual governance-set caps; the full two-level architecture and scenario calibration come online in later phases.

---

## File map

| Doc | Relationship |
|---|---|
| [`risk-decomposition.md`](risk-decomposition.md) | Concentration is the fifth risk type |
| [`primebook-composition.md`](primebook-composition.md) | Primebook-level concentration limits live in Halobook category constraints (deferred for v1) |
| [`asset-classification.md`](asset-classification.md) | Per-asset correlations feed scenario calibration |
| [`hedgebook.md`](hedgebook.md) | Hedges reduce capital but not concentration in v1 |
| [`capital-formula.md`](capital-formula.md) | Excess penalty contributes to per-position capital |
| [`risk-monitoring.md`](risk-monitoring.md) | Utilization metrics surface concentration approach |
| [`open-questions.md`](open-questions.md) | Specific calibration questions tracked here |
