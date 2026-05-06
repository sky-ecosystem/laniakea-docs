# Risk Framework

**Status:** Draft (Phase 2 rewrite landed 2026-05-05; Phase 3 in progress)
**Last Updated:** 2026-05-05

This folder contains the modular Risk Framework documentation. Reading order: foundational primitives → layered architecture → consuming docs (mechanics, computation, examples) → operations and parallel tracks.

---

## Reading order

### Foundational primitives (start here)

The conceptual core. Every other doc builds on these.

| Doc | Topic |
|---|---|
| [`risk-decomposition.md`](risk-decomposition.md) | The five risk types, U/P/T liquidity decomposition, why gap risk and FRTB drawdown unify, default-deny CRR 100%, the risk-type × layer coverage matrix |
| [`book-primitive.md`](book-primitive.md) | The 6-tuple book (assets, tranches, equity-tranche, rules, state, frame); the equity invariant; books as financial state machines; bankruptcy remoteness at the Riskbook level |
| [`tranching.md`](tranching.md) | Tranches as ordered claims; exoassets vs exoliabs; loss propagation through the waterfall; re-framing of overcollateralized lending; why gap risk disappears |
| [`currency-frame.md`](currency-frame.md) | Frame vs instrument; currency taxonomy; frame inheritance top-down from the Generator; the Riskbook as translation layer |

### Layer architecture

The four-book stack specialized from the substrate.

| Doc | Topic |
|---|---|
| [`riskbook-layer.md`](riskbook-layer.md) | The unit of regulation; default risk lives here entirely; currency translation; tactical hedging; bankruptcy-remoteness boundary; the category catalog as governance lever |
| [`halobook-layer.md`](halobook-layer.md) | Bundle exposure structure (general framing); P + T declarations; rollover, lockup, transferability, embedded options; no-netting aggregation across Riskbooks |
| [`primebook-composition.md`](primebook-composition.md) | The five typed sub-books (ascbook, tradingbook, termbook, structbook, hedgebook) + unmatched; sub-books as risk-coverage contracts; optimization-shaped vs static-treatment; declarative routing; treatment-switch policy |
| [`hedgebook.md`](hedgebook.md) | Two-level hedging — Riskbook tactical vs Hedgebook portfolio; cross-Halobook composition preserving bankruptcy-remoteness; explicit hedge-failure-mode modeling; currency hedges |
| [`projection-models.md`](projection-models.md) | The projection contract `(position, scenario) → stress-loss`; categories declare projection models; rules vs projections complementary; projection-model risk as own capital dimension via model-uncertainty haircut |

### Foundational data and primitives

| Doc | Topic |
|---|---|
| [`asset-classification.md`](asset-classification.md) | Per-asset canonical risk profile (drawdown distribution, slippage model, correlations); asset-level liquidity profile primitive; full risk-type tuple per asset |
| [`correlation-framework.md`](correlation-framework.md) | Two-level concentration (Primebook + Genbook); category caps + capacity rights; 100% CRR on excess; scenario calibration |
| [`duration-model.md`](duration-model.md) | Lindy Duration Model for liability duration analysis; Duration Buckets (101 buckets × 15 days); structural maximum caps; capacity reservation for `structbook` matching; manual-allocation Phase 1 carve-out |

### Computation

| Doc | Topic |
|---|---|
| [`matching.md`](matching.md) | Credit-spread vs rate distinction (the load-bearing insight); duration matching as `structbook`/`termbook` optimization; partial matching as continuous blend |
| [`capital-formula.md`](capital-formula.md) | Per-position capital computation flow consuming the layered model; matched / unmatched / hedged blending; output as Total Required Risk Capital (TRRC) |
| [`asset-type-treatment.md`](asset-type-treatment.md) | Worked treatment per asset class via the new framework — tranched-exobook structure where applicable, projection model where applicable, sub-book routing |

### Examples and operations

| Doc | Topic |
|---|---|
| [`examples.md`](examples.md) | Worked v1 crypto-collateralized lending test as canonical end-to-end example; principles summary |
| [`risk-monitoring.md`](risk-monitoring.md) | Metric categories, stress testing, anomaly detection, escalation procedures; per-sub-book CRR; equity-proximity alerts |
| [`sentinel-integration.md`](sentinel-integration.md) | How beacons consume risk framework outputs; synserv verification (in-space calculation); sub-book CRR exposure for sentinel formations |

### Parallel tracks

ASC and ORC are operational obligations, distinct from CRR-based portfolio risk capital.

| Doc | Topic |
|---|---|
| [`asc.md`](asc.md) | Actively Stabilizing Collateral — peg-defense operational liquidity; ALM rental; transition away from PSM. Parallel track to portfolio risk capital. |
| [`operational-risk-capital.md`](operational-risk-capital.md) | ORC — guardian-posted capital covering execution-authority compromise damage; rate limit ↔ capital linkage; warden economics. Parallel track to portfolio risk capital. |

### Open questions

| Doc | Topic |
|---|---|
| [`open-questions.md`](open-questions.md) | Living tracker of deferred design questions — attestor schema, privacy buckets for v1 crypto-lending test, crypto stress calibration, correlation framework calibration specifics, USDS lot-age tracking |

---

## Core principle

Capital requirements should reflect: **what is the maximum loss we could be forced to realize?**

The framework asks one teleological question:

> *In a correlated worst-case crash right now, what real claim do we have to real assets that survive?*

Everything else — risk weights, sub-book routing, hedge accounting — serves the binary decision: continue the Prime, or step in and liquidate.

---

## Default-deny architecture

A foundational pattern: anything the framework can't model adequately gets CRR 100%.

- Riskbook without registered category → CRR 100%
- Exobook without registered category → CRR 100%
- Recursion beyond `max-recursion-depth` → CRR 100%
- Position type without declared projection model → CRR 100%

This forces governance to keep catalogs comprehensive and forces innovation through the proposal-and-crystallization gate. The framework is honest about its competence boundary; the discipline is to expand the boundary through governance work.

---

## Open Items

Active deferred questions tracked in [`open-questions.md`](open-questions.md):
- Correlation framework calibration specifics
- USDS lot-age tracking infrastructure
- Attestor schema for off-chain claim attestation
- Privacy buckets for v1 crypto-lending test (LTV/term/jurisdiction/custodian boundaries)
- Crypto stress scenario calibration

Resolved items kept here for history:
- ~~**Halo Unit treatment**~~ — Halo Units are look-through to underlying assets; treatment determined by Primebook sub-book routing per `primebook-composition.md`
- ~~**Rate limit integration**~~ — Addressed in `operational-risk-capital.md`
- ~~**Beacon implementation (lpla-checker)**~~ — Superseded by the beacon framework collapse: `lpla-checker` as a class disappears, calculation moves into synart-resolved in-space computation that synserv runs. See [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) (canonical) and [`../noemar-synlang/listener-loops.md`](../noemar-synlang/listener-loops.md) (Phase 1 implementation sketch).
- ~~**Gap risk as separate concept**~~ — Folded into `tranching.md` (loss propagation through waterfall) and `risk-decomposition.md` (forced-loss-capital is the unified term). Source doc archived to `inactive/archive/collateralized-lending-risk.md`.
- ~~**FRTB drawdown as separate concept**~~ — Folded into `tranching.md` and `asset-type-treatment.md` via the same forced-loss-capital unification. Source doc archived to `inactive/archive/market-risk-frtb.md`.

---

## Related: Accounting

Settlement operations, auction mechanics, and capital recognition live in `accounting/`:

- [`../accounting/daily-settlement-cycle.md`](../inactive/pre-synlang/accounting/daily-settlement-cycle.md) — Daily settlement timeline, auctions, LCTS settlement
- [`../accounting/tugofwar.md`](../inactive/pre-synlang/accounting/tugofwar.md) — Tug-of-war algorithm for duration capacity allocation
- [`../accounting/risk-capital-ingression.md`](../inactive/pre-synlang/accounting/risk-capital-ingression.md) — How external capital is recognized on Prime balance sheets

(These are in `inactive/pre-synlang/` pending their own synlang-native rewrite.)

---

## Token Standards

| Document | Relevance |
|---|---|
| [`../inactive/pre-synlang/smart-contracts/lcts.md`](../inactive/pre-synlang/smart-contracts/lcts.md) | LCTS tokens (srUSDS, TEJRC, TISRC) are risk capital instruments sized by this framework |

---

## Planned Modules

| Module | Scope | Current Coverage |
|---|---|---|
| **Trading Execution Risk** | Settlement failure, stale oracle prices, counterparty default between match and settlement | Currently managed via on-chain enforcement in PIVs (see [`../inactive/pre-synlang/trading/sky-intents.md`](../inactive/pre-synlang/trading/sky-intents.md)). Formal risk module pending. |

*This document defines the Risk Framework. For Sentinel integration details, see [`sentinel-integration.md`](sentinel-integration.md).*
