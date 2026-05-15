# Sky Forecast Model — Specification

**Last updated:** 2026-04-13
**Active scenario:** `config/scenarios/q2_2026_to_q1_2027.yaml`

---

## Calculation order (per month)

Rate derivations → Extensions pass 1 (all except PSM) → Legacy agent valuations → Supply → PSM extension pass 2 (needs total supply) → Revenue → Waterfall

---

## Constants

`config/constants/model.yaml`

| Constant | Value | Used in |
|---|---|---|
| `farm_emission_rate` | 0.25 | Supply: unrewarded_usds_farm |
| `backstop_rate` | 0.25 | Waterfall: backstop split |

`src/skyforecast/core/revenue.py` (hardcoded)

| Tier | Rate | Applied to |
|---|---|---|
| Tier 2 | 10 bps | `susds × tier2_ratio` |
| Tier 3 | 20 bps | `susds × tier3_ratio` |
| Tier 4 | 50 bps | `susds × tier4_ratio` |

---

## Rate derivations

All rates annualised decimals. Monthly factor = 1/12 applied at point of use.

- `SSR` = SOFR + `savings_rate_spread`
- `GRR` = SSR + `gross_revenue_rate_spread`
- `farm_yield` = SSR + `farm_yield_spread`

---

## Supply

- `unrewarded_usds_farm` = `farmable_tokens` × `farm_emission_rate` / `farm_yield`
- `avg_usds_supply` = `base_usds` + `unrewarded_usds_farm`
  - `base_usds` here is already boosted by the token_farming extension's `supply_boost`
- `avg_unrewarded_usds` = `unrewarded_usds_user` + `unrewarded_usds_farm`
- `avg_susds_supply` = `avg_usds_supply` − `avg_unrewarded_usds`

**Key behaviour:** `unrewarded_usds_user` does not add to total USDS supply — it only shifts supply out of the sUSDS bucket. Increasing it reduces savings expense without reducing gross revenue.

---

## Revenue

- `token_sales_income` = `sellable_tokens` × `sell_token_rate` × 1/12
- `gross_revenue` = `avg_usds_supply` × GRR × 1/12 + `token_sales_income` + extension `gross_revenue_adjustments`
- `savings_expense` = `avg_susds_supply` × SSR × 1/12
- `distribution_rewards` = sum of tier costs (see tier constants above) × 1/12
- `net_revenue` = `gross_revenue` − `savings_expense` − `distribution_rewards` − extension `cost_adjustments`

---

## Waterfall (3-step TMF)

Simplification of the full 5-step TMF: Fortification Conserver and Smart Burn Engine omitted. Backstop uses fixed rate rather than dynamic buffer-fill formula.

- `security_budget` = `net_revenue` × `security_rate`
- `after_security` = `net_revenue` − `security_budget`
- `backstop_contribution` = `after_security` × `backstop_rate` (0.25)
- `staking_rewards` = `after_security` × 0.75
- `net_profit` = `after_security` (= backstop_contribution + staking_rewards)

The model does **not** track aggregate backstop balances, genesis-capital phase-out, or backstop spending. Only the waterfall allocation itself is modeled.

---

## Agents (`config/constants/agents.yaml`)

- Type `FARM`: `value` = `spark_market_cap` × `market_cap_ratio` × `ownership_ratio` → goes into `farmable_tokens`
- Type `SELL`: same formula → goes into `sellable_tokens` → `token_sales_income`
- `market_cap_ratio` is `null` for Spark (uses raw `spark_market_cap`)
- Agent active if `current_month >= launch_month` and `launch_month > 0`

**Known limitation:** The legacy agent system and the `token_farming` extension both compute a supply boost from the same Spark/Grove/Keel holdings, causing double-counting in `avg_usds_supply`. The legacy system is slated for removal; the token_farming extension is the intended mechanism.

---

## Extensions

Extensions return an `ExtensionResults` with these fields and sign conventions:

| Field | Sign | Effect |
|---|---|---|
| `gross_revenue_adjustment` | positive = income, negative = drag | Added to gross_revenue |
| `cost_adjustment` | positive = cost | Subtracted from net_revenue |
| `supply_boost` | always positive | Added to base_usds before supply calc |

---

### psm_exposure

Models collateral earning below base rate. Amount = `total_usds` × `psm_pct` (per-month overridable via scenario) or fixed `amount`. PSM rate = SOFR + `spread` (negative). Drag = (GRR − PSM_rate) × amount × 1/12. Runs in pass 2 because it needs `total_usds` from supply calc.

---

### subsidized_borrow

Primes receive $2B total at a rate that decays linearly from SOFR to GRR over `duration_months`. Decay factor = months_elapsed / duration. Subsidised rate = SOFR + decay_factor × (GRR − SOFR). Cost = (GRR − subsidised_rate) × total_amount × 1/12. Inactive before `start_month` and after `start_month + duration_months`.

---

### srusds_cost

Fixed annual cost for senior risk capital. Monthly cost = `annual_cost` / 12. Always active while enabled.

---

### token_farming

For each active star (current_month ≥ launch_month and months_active < duration_months):
- Market cap: Spark uses `spark_market_cap` from scenario inputs (falls back to config); others use `market_cap_pct` × spark_market_cap
- Monthly distribution = holdings_value × `distribution_rate` × 1/12
- Supply boost = total_monthly_distribution / (`farm_yield` × 1/12)

Supply boost represents the capital attracted to earn the farming yield.

---

### usdt_subsidy

$150M USDT earns `rate_factor` × SSR instead of PSM rate. Foregone income = amount × (psm_rate − usdt_rate) × 1/12. Positive foregone income → `cost_adjustment`. Negative (USDT rate > PSM rate) → `gross_revenue_adjustment`.

---

### genesis_prime

For each active prime (current_month ≥ launch_month): market_cap = `market_cap_pct` × spark_market_cap. Monthly token sales = holdings × `sell_rate` × 1/12. Positive `gross_revenue_adjustment`. No duration limit.

---

### core_vaults

Fixed-rate debt earning above GRR. Monthly benefit = `debt` × (`vault_rate` − GRR) × 1/12. Positive `gross_revenue_adjustment`. If vault_rate < GRR, this becomes a drag.

---

### agent_creation_fee

Sky receives ownership stake in non-star agents and sells at `sell_rate_annual` × market_cap × 1/12. Active from `launch_month`. Positive `gross_revenue_adjustment`.

---

## Configuration

### Input resolution order (per month)

1. `baseline` values
2. `trajectories` (override baseline for specified fields)
3. Cumulative `changes` up to and including current month
4. `impulses` for current month only (reset next month)
5. `events` list processed as set / impulse / agent_launch

Trajectories override baseline. Changes accumulate. Impulses do not persist.

### Trajectory modes

- `step`: holds value from the specified point until the next point
- `linear`: interpolates between points
- Before first point: first point value used. After last point: last point value used.

### Scenario inheritance

Child `extends` parent. Baseline: child overrides parent per-key. Changes/impulses: merged per-month, child overrides parent for same month. Trajectories: child replaces parent for same field. Agent launches: child overrides parent per-agent.

### Named periods

Built-in: `q1`=[1-3], `q2`=[4-6], `q3`=[7-9], `q4`=[10-12], `h1`=[1-6], `h2`=[7-12]. Custom via `periods` key. Names resolve to their **first month** for changes and launches.

### Month display

Scenario fields `start_month` (default 1) and `start_year` (default 2026) control output labels only — they do not affect calculations. Calendar month = ((model_month − 1 + start_month − 1) % 12) + 1. Quarter labels derived from start_month and start_year.

---

## Extension month numbering

Extension configs use the same month numbering as the active scenario. When the scenario starts in April (start_month=4), model M1=April. Extension `launch_month`, `start_month`, and `end_month` must be set accordingly. Months before the model window are expressed as zero or negative integers.
