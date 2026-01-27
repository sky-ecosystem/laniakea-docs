# Risk Framework

**Status:** Draft
**Last Updated:** 2026-01-27

This folder contains the modular Risk Framework documentation.

## Module Index

- `duration-model.md` — Liability duration analysis, SPTP buckets, structural caps, capacity reservation.
- `asset-classification.md` — Asset characteristics: fundamental risk, drawdown risk, stressed pull-to-par.
- `matching.md` — Rate risk vs credit spread risk, SPTP eligibility, matched/unmatched treatment, partial matching.
- `asset-type-treatment.md` — Worked treatments for major asset types (TradFi, crypto lending, hybrid).
- `collateralized-lending-risk.md` — Jump-to-default + liquidation loss (gap risk) for collateralized lending.
- `market-risk-frtb.md` — FRTB-style drawdown treatment for unmatched liquid assets.
- `asc.md` — Actively Stabilizing Collateral (ASC): ALM requirements, latent/resting liquidity, renting, peg defense.
- `capital-formula.md` — Capital formulas and computation flow.
- `correlation-framework.md` — Category caps + capacity rights (concentration limits via 100% CRR on excess).
- `examples.md` — Current vs proposed examples + summary principles.
- `sentinel-integration.md` — Output metrics and how Sentinel uses the framework.

## Core Principle

Capital requirements should reflect: **what is the maximum loss we could be forced to realize?**

## Open Items

1. **Correlation framework specifics** — Stress calibration, multi-group assets, aggregation method
2. **Data infrastructure** — How to track USDS lot ages for liability duration analysis
3. **Halo Unit treatment** — How do Halo Unit tokens get classified? (Likely as unmatched given redemption constraints)
4. **Rate limit integration** — How capital requirements translate to PAU rate limits
5. **Beacon implementation** — Formulas and algorithms for lpla-checker calculations

---

*This document defines the Risk Framework. For Sentinel integration details, see the Sentinel Network document.*
