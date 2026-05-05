# Accounting

**Status:** Draft
**Last Updated:** 2026-02-12

Settlement operations, auction mechanics, and capital recognition for the Laniakea system.

## Module Index

- `books-and-units.md` — Books (balanced ledgers, assets = liabilities) and Units (cross-book links) as foundational accounting primitives. How the recursive book pattern chains the capital stack from Generator through Prime to Halo.
- `daily-settlement-cycle.md` — Daily settlement timeline, OSRC and Duration auctions, LCTS settlement, prepayments, penalties.
- `tugofwar.md` — Tug-of-war algorithm for duration capacity allocation when reservations exceed availability.
- `risk-capital-ingression.md` — How external capital (EJRC, SRC) is recognized on Prime balance sheets: ingression curves, quality multipliers, MC-based caps.
- `genesis-capital.md` — Temporary seed capital for Genesis Agents: Aggregate Backstop Capital, insolvency defense hierarchy, phase-out mechanics, Guardian buffers.
- `current-accounting.md` — How accounting currently works: monthly settlement cycle, legacy exceptions (core vaults, PSM, legacy RWA), Core Council Buffer reclassification, income/expense taxonomy.
- `prime-settlement-methodology.md` — Five-step Prime settlement calculation: debt fees, idle USDS/DAI reimbursement, sUSDS spread profit, Sky Direct exposure handling, net amount.
- `forecast-model.md` — Python forecasting tool: scenario configuration, parameter reference, revenue projections.

### Future Coverage (Phase 9+)

The following accounting topics are defined in the roadmap but not yet covered here. They will be documented as implementation approaches:

- **Carry mechanism** — `Carry = (Actual PnL - Simulated Baseline PnL) × Performance Fee Ratio`; accounting for carry distribution between Baseline and Stream sentinels
- **TTS-based ORC** — Operational Risk Capital requirements sized by `Rate Limit × TTS`; how ORC is posted, tracked, and released

See `../roadmap/roadmap-overview.md` (Phases 9–10) and `../trading/sentinel-network.md` for the design specifications.

## Relationship to Risk Framework

The Risk Framework (`risk-framework/`) defines *what* capital is required. This directory defines *how* capital flows, settles, and gets allocated:

- **Settlement cycle** operationalizes the daily cadence for auctions, payments, and LCTS settlement
- **Tug-of-war** distributes scarce duration capacity (measured by the Risk Framework's Lindy model) across Primes
- **Risk capital ingression** determines how much of externally provided capital counts toward Risk Framework requirements

---

*For capital requirement calculations, see `risk-framework/README.md`.*
