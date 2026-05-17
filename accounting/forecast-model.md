# Forecast Model

**Status:** Pointer-only — source code lives in `inactive/pre-synlang/forecast_model/`.
**Last Updated:** 2026-05-07

---

## What it is

The Sky Forecast Model is a **modular Python forecasting tool** that simulates Sky's monthly financial flows and aggregates to quarters. Used for scenario planning, sensitivity analysis, and financial projections — not for production settlement (settlement runs in synlang via synserv; see [`settlement-cycle.md`](settlement-cycle.md)).

Source: [`inactive/pre-synlang/forecast_model/`](../inactive/pre-synlang/forecast_model/)

---

## What it models

- **Supply dynamics** — Base USDS growth, unrewarded USDS, agent-specific supply impacts
- **Revenue** — Stability fees (SOFR + spreads), Prime contributions, costs (subsidized borrow, srUSDS costs)
- **TMF waterfall** — Simplified: Security & Maintenance, Backstop, Staking (full TMF has 5 steps including Fortification + Burn — see whitepaper Appendix C)
- **Agent activity** — Binary active/inactive based on launch month, agent-specific valuations, farmable vs sellable token types

Scenarios are YAML files with baseline values, trajectories (interpolated points), persistent changes (apply from month N onward), one-time impulses (single month), and agent launch months. Scenarios can extend other scenarios via `extends:`.

---

## Connection to active accounting

- **Settlement projections** — projects what future per-Prime + global settlement outputs would look like under different supply / rate assumptions; complements [`settlement-cycle.md`](settlement-cycle.md) which describes the synlang-native runtime mechanism.
- **Capital stack tracking** — tracks Aggregate Backstop Capital growth under TMF retention rules; complements [`capital-stack.md`](capital-stack.md) §8 which defines the targets and phase-out logic.

The model intentionally simplifies (3-step waterfall vs the full 5-step TMF; fixed-rate backstop vs dynamic) because it's a planning tool, not a protocol specification.

---

## Running it

```bash
# Run a scenario
python -m skyforecast run config/scenarios/base_2026.yaml

# Generate HTML dashboard
python run_dashboard.py

# Generate markdown report
python run_report.py
```

Outputs: `report.txt` (markdown), `dashboard.html` (interactive).

---

## File map

| Doc | Relationship |
|---|---|
| [`README.md`](lani/accounting/README.md) | Accounting directory index |
| [`settlement-cycle.md`](settlement-cycle.md) | The synlang-native settlement architecture this model projects against |
| [`capital-stack.md`](capital-stack.md) | ABC growth and TMF retention this model tracks |
| [`../inactive/pre-synlang/forecast_model/`](../inactive/pre-synlang/forecast_model/) | Source code, scenarios, and forecast spec |
| [`../inactive/pre-synlang/forecast_model/forecast-spec.md`](../inactive/pre-synlang/forecast_model/forecast-spec.md) | Detailed model specification |
| [`../inactive/pre-synlang/whitepaper/appendix-c-treasury-management-function.md`](../inactive/pre-synlang/whitepaper/appendix-c-treasury-management-function.md) | Canonical TMF (full 5-step waterfall) |
