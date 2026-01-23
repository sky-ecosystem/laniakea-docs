# Sky Forecast Model Strategy

**Status:** Draft
**Last Updated:** 2026-01-08

---

## Overview

A modular Python forecast model for Sky. Calculates monthly results, aggregates to quarters. Features flexible input specification with persistent changes, one-time impulses, value trajectories, scenario inheritance, and named time periods.

---

## Design Principles

### 1. Monthly Granularity

```
Month 1 → Month 2 → Month 3  =  Q1 (sum)
Month 4 → Month 5 → Month 6  =  Q2 (sum)
...
```

- **Base unit:** 1 month
- **Period factor:** `1/12` (monthly portion of annual rate)
- **Agent activity:** Binary — active if `current_month >= launch_month`

### 2. Calculation Order

```
Rate Derivations → Agent Valuations → Supply → Revenue → Waterfall
```

### 3. Input Resolution Order

For each month, inputs are resolved in this order:

```
1. Load base scenario (if `extends` specified)
2. Start with `baseline` values
3. Compute `trajectories` for this month
4. Apply `changes` (cumulative, persistent)
5. Apply `impulses` (this month only, then reset)
6. Process `events` list (alternative syntax)
```

### 4. Conventions

| Convention | Rule |
|------------|------|
| **Money** | Base unit USD. Format with "M" suffix in outputs only. |
| **Rates** | Annualized decimals as strings (`"0.0370"`). |
| **Period factor** | Monthly = `1/12`. |
| **Signs** | Costs are negative (`subsidized_borrow: -650000`). |
| **Months** | 1=Jan, 12=Dec. Multi-year: 13=Year2 Jan, etc. |

---

## Directory Structure

```
forecast_model/
├── config/
│   ├── constants/
│   │   ├── agents.yaml
│   │   └── model.yaml
│   └── scenarios/
│       ├── base_2025.yaml
│       ├── bull_2025.yaml      # extends: base_2025
│       └── bear_2025.yaml
│
├── src/skyforecast/
│   ├── core/                   # Pure calculations
│   │   ├── rates.py
│   │   ├── agents.py
│   │   ├── supply.py
│   │   ├── revenue.py
│   │   └── waterfall.py
│   ├── loaders/
│   │   ├── models.py           # Pydantic models
│   │   ├── yaml_loader.py
│   │   └── resolver.py         # Input resolution logic
│   ├── outputs/
│   │   └── markdown.py
│   ├── engine.py
│   └── cli.py
```

---

## Configuration Format

### Feature 1: Baseline + Changes + Impulses

```yaml
name: "Base 2025"
months: 12

baseline:
  spark_market_cap: 350000000
  base_usds: 9650000000
  sofr: "0.0370"
  # ... all default values

# Persistent level changes (carry forward until next change)
changes:
  3:
    sofr: "0.0360"
  7:
    spark_market_cap: 450000000
    base_usds: 12000000000

# One-time events (apply only to that month, reset after)
impulses:
  10:
    backstop_withdrawal: 5000000
  6:
    one_time_income: 2000000
```

**Resolution:**
- `changes` accumulate: month 8 still has `spark_market_cap: 450000000`
- `impulses` reset: month 11 has `backstop_withdrawal: 0`

---

### Feature 2: Events List (Alternative Syntax)

```yaml
events:
  - month: 4
    type: set                    # persistent change
    values:
      base_usds: 10500000000

  - month: 7
    type: set
    values:
      spark_market_cap: 450000000

  - month: 10
    type: impulse                # one-time only
    values:
      backstop_withdrawal: 5000000

  - month: 6
    type: agent_launch
    agent: grove
```

**Note:** `events` and `changes`/`impulses` can coexist; events are processed last.

---

### Feature 3: Trajectories (Interpolation)

```yaml
trajectories:
  base_usds:
    points:
      1: 9650000000
      6: 12000000000
      12: 16000000000
    mode: linear                 # interpolate between points

  spark_market_cap:
    points:
      1: 350000000
      7: 450000000
    mode: step                   # jump at point, hold until next
```

**Modes:**
- `step`: Value jumps at specified month, holds until next point
- `linear`: Linear interpolation between points

---

### Feature 4: Scenario Inheritance

```yaml
# bull_2025.yaml
extends: base_2025

# Override baseline values
baseline:
  spark_market_cap: 500000000

# Add/override changes
changes:
  5:
    base_usds: 13000000000

# Add impulses
impulses:
  4:
    launch_bonus: 5000000
```

**Resolution:**
1. Load `base_2025.yaml` fully
2. Merge `baseline` (child overrides parent)
3. Merge `changes` (child adds/overrides specific months)
4. Merge `impulses` (child adds/overrides specific months)
5. Merge `trajectories`, `events`, `agent_launches`

---

### Feature 5: Named Periods

```yaml
periods:
  h1: [1, 2, 3, 4, 5, 6]
  h2: [7, 8, 9, 10, 11, 12]
  q1: [1, 2, 3]
  q2: [4, 5, 6]
  q3: [7, 8, 9]
  q4: [10, 11, 12]

# Use named periods anywhere month numbers are accepted
changes:
  h2:                            # applies to month 7 (first of period)
    security_rate: "0.15"
  q4:
    spark_market_cap: 500000000

impulses:
  q2:                            # applies to month 4 (first of period)
    mid_year_bonus: 3000000

agent_launches:
  grove: q2                      # launches month 4
  obex: h2                       # launches month 7
```

**Resolution:** Named periods resolve to their first month for point-in-time events (launches, changes), or expand for ranges where applicable.

---

## Complete Example

```yaml
name: "Base 2025"
description: "Conservative baseline projection"
months: 12

# Named periods for convenience
periods:
  h1: [1, 2, 3, 4, 5, 6]
  h2: [7, 8, 9, 10, 11, 12]

# Agent launches (month number or period name)
agent_launches:
  spark: 1
  grove: 4
  keel: 6
  obex: h2

# Default values for all months
baseline:
  spark_market_cap: 350000000
  base_usds: 9650000000
  unrewarded_usds_user: 3700000000
  sofr: "0.0370"
  savings_rate_spread: "0.0030"
  gross_revenue_rate_spread: "0.0030"
  farm_yield_spread: "0.0040"
  sell_token_rate: "0.25"
  security_rate: "0.20"
  subsidized_borrow: -650000
  srusds_cost: -400000

# Values that change over time (interpolated)
trajectories:
  base_usds:
    points:
      1: 9650000000
      12: 16000000000
    mode: linear

# Discrete level changes (persist)
changes:
  3:
    sofr: "0.0360"
  h2:
    spark_market_cap: 450000000
    security_rate: "0.15"

# One-time events (don't persist)
impulses:
  10:
    backstop_withdrawal: 5000000
```

---

## Core Modules

### `resolver.py` — Input Resolution

```python
def resolve_month_inputs(
    month: int,
    baseline: dict,
    changes: dict[int, dict],
    impulses: dict[int, dict],
    trajectories: dict[str, Trajectory],
    periods: dict[str, list[int]],
) -> dict:
    """
    Resolve all inputs for a specific month.

    Order:
    1. Start with baseline
    2. Apply trajectories (computed values)
    3. Apply cumulative changes up to this month
    4. Apply impulses for this month only
    """
    result = baseline.copy()

    # Apply trajectories
    for field, traj in trajectories.items():
        result[field] = traj.value_at(month)

    # Apply cumulative changes
    for m in range(1, month + 1):
        if m in changes:
            result.update(changes[m])

    # Apply impulses (this month only)
    if month in impulses:
        result.update(impulses[month])

    return result


def resolve_period_name(
    value: int | str,
    periods: dict[str, list[int]],
) -> int:
    """Convert period name to month number (first month of period)."""
    if isinstance(value, int):
        return value
    if value in periods:
        return periods[value][0]
    raise ValueError(f"Unknown period: {value}")
```

### `agents.py` — Binary Active/Inactive

```python
def is_agent_active(launch_month: int, current_month: int) -> bool:
    """Agent is active if current month >= launch month."""
    return launch_month > 0 and current_month >= launch_month

def aggregate_active_agents(
    agents: list[AgentDefinition],
    agent_launches: dict[str, int],
    current_month: int,
    spark_market_cap: Decimal,
) -> tuple[Decimal, Decimal]:
    """Sum active agent values by type. Returns (farmable, sellable)."""
    farmable = Decimal("0")
    sellable = Decimal("0")

    for agent in agents:
        launch = agent_launches.get(agent.name, 0)
        if is_agent_active(launch, current_month):
            value = calculate_agent_value(agent, spark_market_cap)
            if agent.agent_type == "FARM":
                farmable += value
            else:
                sellable += value

    return farmable, sellable
```

### `engine.py` — Monthly Loop

```python
def run_scenario(scenario: ResolvedScenario) -> ScenarioResults:
    """Run all months and aggregate to quarters."""
    monthly_results = []

    for month in range(1, scenario.months + 1):
        inputs = resolve_month_inputs(month, ...)
        result = run_month(month, inputs, ...)
        monthly_results.append(result)

    # Aggregate to quarters
    quarters = [
        aggregate_quarter(monthly_results[0:3]),   # Q1
        aggregate_quarter(monthly_results[3:6]),   # Q2
        aggregate_quarter(monthly_results[6:9]),   # Q3
        aggregate_quarter(monthly_results[9:12]),  # Q4
    ]

    return ScenarioResults(
        monthly=monthly_results,
        quarterly=quarters,
        annual=aggregate_annual(quarters),
    )
```

---

## Output Format

```markdown
# Base 2025

## Q1 (Jan-Mar)

| Month | USDS Supply | Gross Rev | Net Rev | Staking |
|-------|-------------|-----------|---------|---------|
| Jan   | 9,800.00M   | 35.12M    | 18.54M  | 10.85M  |
| Feb   | 10,060.00M  | 36.05M    | 19.10M  | 11.18M  |
| Mar   | 10,320.00M  | 36.98M    | 19.67M  | 11.51M  |
| **Q1**| —           | **108.15M** | **57.31M** | **33.54M** |

## Q2 (Apr-Jun)
...

## Annual Summary

| Quarter | Gross Revenue | Net Revenue | Staking Rewards |
|---------|---------------|-------------|-----------------|
| Q1      | 108.15M       | 57.31M      | 33.54M          |
| Q2      | 121.40M       | 65.22M      | 38.15M          |
| Q3      | 145.80M       | 80.50M      | 47.09M          |
| Q4      | 162.30M       | 91.45M      | 53.50M          |
| **Year**| **537.65M**   | **294.48M** | **172.28M**     |
```

---

## Implementation Checklist

### Phase 1: Monthly Engine

- [x] Project scaffolding
- [x] Core calculation modules
- [ ] Config models (baseline, changes, impulses, trajectories, periods)
- [ ] Input resolver
- [ ] Scenario inheritance loader
- [ ] Named period resolution
- [ ] Monthly engine loop
- [ ] Quarterly aggregation
- [ ] Updated markdown output

### Phase 2: Polish

- [ ] Scenario comparison
- [ ] JSON export
- [ ] Multi-year support

---

*This strategy document serves as the blueprint for implementation.*
