# Correlation Framework (Category Caps + Capacity Rights)

**Last Updated:** 2026-01-27
**Status:** Draft

This framework has two layers:

1. **Enforcement (simple):** governance defines arbitrary **categories** with **hard caps**; any exposure above a cap is forced to be fully capitalized (100% CRR). “Capacity rights” prevent new deployers from instantly displacing incumbents.
2. **Calibration (model-driven):** governance (or governance-controlled automation) uses **regular scenario stress calculations** to set and update those caps over time.

## Core Idea

1. Governance defines a set of **Correlation Categories** (examples: “CLOs”, “US-based assets”, “40–50 month duration”, “real estate”).
2. Each category has a **cap** as a percentage of the total portfolio (e.g., “CLOs ≤ 10% of USDS supply”).
3. Every asset is classified into one or more categories at onboarding.
4. If aggregate exposure exceeds a category cap, the **excess portion** is subject to **100% CRR** (no leverage on the excess).
5. Each category also has non-transferable **capacity rights** (“grandfathered slices”) that evolve over time based on first-come-first-serve, and when cap is reached, through sustained payment of the 100% CRR penalty.

## Why This Exists

Duration matching (ALDM with Duration Buckets + caps) prevents classic maturity mismatch, but it does not stop the system from concentrating into a single correlated risk type (e.g., "lots of CLO-like credit") by adding more risk capital. This framework makes "we simply don't want more of this risk" enforceable.

## How Caps Are Set (Scenario Calibration)

The cap system is intentionally simple to enforce. The *choice of cap values* can be updated over time using a scenario stress engine.

### Scenario Engine (Concept)

Define a scenario set `S` (e.g., credit crisis, crypto crash, stablecoin confidence shock). For each scenario `s` and category `c`, estimate the **loss severity per unit exposure**:

- `L(c, s)` = stressed loss per $1 of category exposure under scenario `s`

Then choose caps such that portfolio losses remain within a governance-defined **loss budget**:

- `B(s)` = maximum portfolio loss fraction tolerated under scenario `s` (or equivalent solvency constraint)

This turns “correlation” into a concrete calibration surface rather than an abstract covariance matrix.

### Exposure Basis for Calibration

Use the same exposure basis as enforcement:

- **Matched exposure:** notional / duration-value
- **Unmatched exposure:** market value (MTM)

Scenario calibration may run in either of two modes:

1. **Static matching mode:** treat matched/unmatched splits as measured for the current week and calibrate caps using those exposures.
2. **Scenario matching mode:** allow scenarios (especially run/confidence scenarios) to reduce matching capacity, increasing unmatched exposure and therefore increasing `L(c, s)` for duration-sensitive categories.

### Two Ways to Derive Caps

#### Method A (Simple, Independent Caps)

Set each category’s cap from a worst-case scenario bound:

```
cap_percent[c] = min_s ( B(s) / L(c, s) )
```

Interpretation: “even if the entire allowed slice of category `c` is held, the portfolio survives each scenario’s budget.”

This method is simple and robust but conservative because it ignores interactions among categories.

#### Method B (Joint Caps via Optimization)

Choose caps jointly to satisfy scenario constraints while allowing a preferred composition:

```
For each scenario s:
  Σ_c cap_percent[c] * L(c, s) ≤ B(s)
```

Subject to additional governance constraints:
- floors/ceilings per category
- maximum change per update (rate limit)
- policy overrides (legal/compliance “never exceed” caps)

### Governance Controls for Calibration

Governance should set:
- Scenario set `S` and budgets `B(s)`
- Cap update cadence (weekly at settlement vs monthly)
- Smoothing / rate limits on cap changes (e.g., ±X% per update)
- Emergency freeze: ability to halt cap updates while keeping enforcement active

## Definitions

### Category

An arbitrary governance-defined label used for concentration limits.

### Exposure Measure (Matched vs Unmatched)

Caps are measured on a unified “portfolio exposure” basis, but the measurement differs by treatment:

- **Matched exposure:** measured using notional / duration-value (the "hold-to-maturity" relevant size).
- **Unmatched exposure:** measured using market value (MTM).

Interpretation: if an exposure is treated as forced-sale (unmatched), it consumes category capacity by its MTM size; if it is treated as duration-matched, it consumes by notional.

### Category Cap

For category `c`:

```
cap_amount[c] = cap_percent[c] × total_portfolio
```

Where `total_portfolio` is defined at the system level (e.g., “USDS supply”).

### Over-Cap Portion and Penalty

For each category `c`, define:

```
excess[c] = max(0, exposure_total[c] - cap_amount[c])
```

Only the **excess portion** receives the **100% CRR** penalty.

The 100% CRR penalty is applied **once** (not stacked) even if an exposure is tagged into multiple categories.

## Capacity Rights (“Grandfathered Slices”)

To prevent new deployers from instantly pushing old holders out of a capped category, each category maintains a per-Prime non-transferable allocation:

- `alloc[p][c]` = Prime `p`’s current “in-cap” share for category `c`
- `Σ_p alloc[p][c] = cap_amount[c]`

This allocation changes gradually over time based on which Primes have been paying the over-cap penalty.

### Normalization Period

For a given exposure, the “speed” at which over-cap penalty converts into allocation is governed by:

```
T = max(asset_SPTP, 3 months)
```

Intuition: longer-duration assets take longer to normalize; very short durations still have a minimum normalization of 3 months.

## Reallocation Rule (Weekly Settlement)

At each weekly settlement:

1. Compute each Prime’s category exposure `E[p][c]` (using matched/notional vs unmatched/MTM).
2. Compute “penalized amount”:

```
P[p][c] = max(0, E[p][c] - alloc[p][c])
```

This is the portion that is currently over that Prime’s in-cap allocation for the category and therefore faces 100% CRR.

3. Update allocations by shifting capacity toward Primes that have been paying penalties, with rate:

```
α = (1 week) / T
```

Mechanically, the intent is:
- If you are over-cap by `P`, then over time `T` you earn roughly `P` of in-cap capacity.
- That earned capacity comes from the existing in-cap allocations, which pushes incumbents into partial penalty and triggers a “fight back” dynamic.

**Implementation note:** the exact update function can be implemented as an exponential moving average of penalized amounts or as a direct reallocation step. The key invariant is that long-run allocations reflect “who paid the most 100% CRR penalty for how long,” normalized by `T`.

## Enforcement in the Capital Formula

The over-cap portion of an exposure is forced to 100% CRR:

```
CRR_effective = min(1.0, CRR_base + cap_penalty_addon)
```

Where `cap_penalty_addon` is sized such that the over-cap portion’s required capital equals its exposure amount.

## Outputs (For Sentinel / Reporting)

Per category `c`:
- `cap_percent[c]`, `cap_amount[c]`
- `exposure_total[c]`
- `utilization[c] = exposure_total[c] / cap_amount[c]`

Per Prime `p` and category `c`:
- `alloc[p][c]`
- `E[p][c]`
- `P[p][c]` (penalized / over-allocation amount)

Portfolio-level:
- total over-cap exposure (non-stacked)
- total 100%-CRR-required capital due to category caps

## Open Questions

1. What is the exact “allocation update” function (EMA vs explicit weekly reallocation), and where does it live (Sentinel vs on-chain vs governance process)?
2. How to compute category exposure for multi-category assets without double counting while still enforcing caps (binding category vs portfolio-wide max penalty)?
3. Should caps be defined per-Prime, per-Prime-type, or only globally across all Primes?
4. How are categories versioned and migrated when governance changes category definitions?
5. Which cap-calibration method should be canonical (independent worst-case caps vs joint optimization)?
6. What is the minimal definition of `L(c, s)` required to safely add a new category?
