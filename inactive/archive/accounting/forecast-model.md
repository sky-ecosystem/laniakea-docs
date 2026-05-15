# Sky Forecast Model

A modular Python forecast model for Sky that calculates monthly results and aggregates to quarters. This tool enables scenario planning, sensitivity analysis, and financial projections for the Sky ecosystem.

**Source:** [Laniakea Forecast Model](https://github.com/sky-ecosystem/laniakea-docs/tree/main/forecast_model)

---

## Overview

The forecast model simulates Sky's financial flows:

```
Rate Derivations → Agent Valuations → Supply → Revenue → Waterfall
```

### Key Capabilities

- **Monthly granularity** — Base unit is 1 month, aggregated to quarters
- **Scenario inheritance** — Bull/bear scenarios can extend base scenarios
- **Flexible inputs** — Trajectories, persistent changes, one-time impulses
- **TMF waterfall** — Implements the Treasury Management Function

---

## What It Models

### Supply Dynamics
- Base USDS supply growth
- Unrewarded USDS held by users
- Agent-specific supply impacts

### Revenue Calculation
- Stability fees based on rates (SOFR + spreads)
- Agent contributions (Spark, Grove, etc.)
- Costs (subsidized borrow, sRUSDS costs)

### TMF Waterfall
- Security & Maintenance allocation
- Backstop buffer filling
- Staking rewards distribution

### Agent Activity
- Binary active/inactive based on launch month
- Agent-specific valuations
- Farmable vs sellable token types

---

## Configuration Format

Scenarios are defined in YAML files with these components:

### Baseline Values

```yaml
baseline:
  spark_market_cap: 350000000
  base_usds: 9650000000
  sofr: "0.0370"
  savings_rate_spread: "0.0030"
  gross_revenue_rate_spread: "0.0030"
  security_rate: "0.21"
```

### Trajectories (Interpolated Values)

```yaml
trajectories:
  base_usds:
    points:
      1: 9650000000
      6: 12000000000
      12: 16000000000
    mode: linear    # or "step"
```

### Persistent Changes

```yaml
changes:
  3:
    sofr: "0.0360"    # Changes in month 3, persists
  7:
    spark_market_cap: 450000000
    security_rate: "0.15"
```

### One-Time Impulses

```yaml
impulses:
  10:
    backstop_withdrawal: 5000000  # Only applies to month 10
```

### Agent Launches

```yaml
agent_launches:
  spark: 1
  grove: 4
  keel: 6
  obex: 7
```

---

## Scenario Inheritance

Scenarios can extend other scenarios:

```yaml
# bull_2026.yaml
extends: base_2026

baseline:
  spark_market_cap: 500000000  # Override

changes:
  5:
    base_usds: 13000000000     # Add new change
```

Resolution order:
1. Load parent scenario
2. Merge baseline (child overrides)
3. Merge changes (child adds/overrides)
4. Merge impulses, trajectories, etc.

---

## Key Parameters

### Rate Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `sofr` | Base reference rate | "0.0370" (3.7%) |
| `savings_rate_spread` | Spread above SOFR for savings | "0.0030" |
| `gross_revenue_rate_spread` | Revenue spread | "0.0030" |
| `security_rate` | TMF Step 1 allocation | "0.21" (Genesis) |

### Supply Parameters

| Parameter | Description |
|-----------|-------------|
| `base_usds` | Total USDS supply |
| `unrewarded_usds_user` | USDS not earning savings rate |

### Agent Parameters

| Parameter | Description |
|-----------|-------------|
| `spark_market_cap` | Spark token market cap (for valuation) |
| Launch months | When each agent becomes active |

---

## Output Format

The model produces markdown reports with monthly and quarterly breakdowns:

```markdown
## Q1 (Jan-Mar)

| Month | USDS Supply | Gross Rev | Net Rev | Staking |
|-------|-------------|-----------|---------|---------|
| Jan   | 9,800.00M   | 35.12M    | 18.54M  | 10.85M  |
| Feb   | 10,060.00M  | 36.05M    | 19.10M  | 11.18M  |
| Mar   | 10,320.00M  | 36.98M    | 19.67M  | 11.51M  |
| **Q1**| —           | **108.15M** | **57.31M** | **33.54M** |

## Annual Summary

| Quarter | Gross Revenue | Net Revenue | Staking Rewards |
|---------|---------------|-------------|-----------------|
| Q1      | 108.15M       | 57.31M      | 33.54M          |
| Q2      | 121.40M       | 65.22M      | 38.15M          |
| ...     | ...           | ...         | ...             |
| **Year**| **537.65M**   | **294.48M** | **172.28M**     |
```

---

## Simplifications vs Full TMF

**Note:** The forecast model intentionally simplifies for practical forecasting:

| Aspect | Forecast Model | Full TMF |
|--------|----------------|----------|
| Waterfall steps | 3 (Security, Backstop, Staking) | 5 (includes Fortification, Burn) |
| Backstop rate | Fixed rate | Dynamic based on fill level |
| Use case | Scenario planning | Protocol specification |

The full TMF mechanics are documented in the whitepaper appendices.

---

## Running the Model

### CLI

```bash
# Run a scenario
python -m skyforecast run config/scenarios/base_2026.yaml

# Generate HTML dashboard
python run_dashboard.py

# Generate markdown report
python run_report.py
```

### Output Files

- `report.txt` — Markdown report
- `dashboard.html` — Interactive HTML dashboard

---

## Use Cases for /m/skyaccounting

### 1. Settlement Projections
Use the model to project what future settlements might look like under different conditions.

### 2. Scenario Comparisons
Compare base vs bull vs bear scenarios to understand sensitivity.

### 3. Parameter Impact Analysis
"What happens if SOFR drops by 50bps?" — Run a modified scenario to find out.

### 4. Agent Launch Impact
Model how new agent launches (Grove, Keel, etc.) affect revenue.

### 5. Backstop Analysis
Track how quickly the backstop buffer fills under different revenue scenarios.

---

## Key Insights

### Revenue Sensitivity

Revenue is highly sensitive to:
- SOFR (base rate)
- USDS supply growth
- Rate spreads

### Backstop Dynamics

At current scales (~$200M net revenue):
- Phase 1 applies (25% floor)
- Backstop fills relatively slowly
- Most surplus goes to staking rewards

### Agent Impact

Active agents contribute:
- Direct revenue from their operations
- Token farming/selling income
- Indirect supply growth effects

---

## Summary

1. **Sky Forecast Model** is a Python tool for financial projections
2. **Monthly granularity** with quarterly aggregation
3. **Flexible scenarios** with inheritance and overrides
4. **Models TMF waterfall** (simplified for forecasting)
5. **Available in Laniakea docs** — open source
6. **Use for** settlement projections, scenario analysis, parameter sensitivity

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| [Appendix C — TMF](../whitepaper/appendix-c-treasury-management-function.md) | Full TMF mechanics (model implements a simplified version) |
| [`genesis-capital.md`](genesis-capital.md) | Backstop targets and revenue retention rules the model tracks |
| [`daily-settlement-cycle.md`](daily-settlement-cycle.md) | Settlement mechanics that the model projects |
| [`../roadmap/roadmap-overview.md`](../roadmap/roadmap-overview.md) | Implementation phasing — model scenarios align to roadmap phases |
