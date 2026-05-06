# Primebook Composition

**Status:** Draft (Phase 2 layer doc, 2026-05-05)

The Primebook is no longer a flat aggregator. It's a **composition of typed sub-books**, where each sub-book is a *risk-coverage contract* — a declaration of which risks it covers and under what conditions. This doc defines the sub-book taxonomy, the optimization-vs-static distinction, the routing rules, and the treatment-switch policy.

Companion to:
- `book-primitive.md` — Primebook is one specialization of the 6-tuple book
- `risk-decomposition.md` — the risk-type × sub-book coverage matrix originates here
- `halobook-layer.md` — what sits below; what gets routed into the sub-books
- `riskbook-layer.md` — the regulated unit; what eventually rolls up
- `hedgebook.md` — one of the sub-books, deserves its own treatment

---

## TL;DR

The Primebook composes **five typed sub-books** (plus an "unmatched" leftover):

| Sub-book | Role |
|---|---|
| `ascbook` | ASC-eligible holdings (peg-defense readiness — see `asc.md`) |
| `tradingbook` | Liquid holdings, FRTB-style forced-loss treatment |
| `termbook` | TTM units matched against tUSDS-issued YT (Prime holds YT) |
| `structbook` | TTM units matched against structural USDS demand |
| `hedgebook` | Cross-position hedge groups (see `hedgebook.md`) |
| (unmatched leftover) | Whatever didn't fit anywhere |

Each sub-book is a **risk-coverage contract**: it declares which of the four non-default risks it covers (credit-spread MTM, rate, liquidity) under what conditions. Default capital is always required — sub-books only modify the *other* risks.

Sub-books split into **optimization-shaped** (run internal optimization to maximize coverage) and **static-treatment** (uniform treatment, no internal optimization). The Primebook still issues a **single Primeunit upward** to the Genbook — the sub-books are internal composition for risk treatment, not external products.

---

## Section map

| § | Topic |
|---|---|
| 1 | The Primebook composes sub-books |
| 2 | Sub-books as risk-coverage contracts |
| 3 | The five sub-book types + unmatched |
| 4 | Optimization-shaped vs static-treatment |
| 5 | Routing Halobook units to sub-books |
| 6 | Treatment-switch policy |
| 7 | Crash oracle (deferred) |
| 8 | The single Primeunit upward |
| 9 | One-line summary |

---

## 1. The Primebook composes sub-books

In earlier framing, the Primebook was a flat aggregator across Halobook units. The new framing recognizes that **Halobook units carry different risk treatments** — some matched against fixed liabilities (no forced-sale risk), some held for trading (forced-sale risk applies), some held for peg defense (must be liquid).

The Primebook routes each Halobook unit to a **typed sub-book** based on its declared characteristics (U/P/T from `risk-decomposition.md` §4, plus the Halobook's exposure structure). Each sub-book has its own category equation that determines capital for the routed positions.

Why this structure: a flat aggregator can't distinguish a position matched against a 2-year fixed liability (no forced-loss capital required) from a position with the same risk vector held for sale (forced-loss capital required). Sub-book composition makes the distinction explicit.

```
Primebook
  ├── ascbook         (ASC-eligible holdings)
  ├── tradingbook     (liquid FRTB-style)
  ├── termbook        (tUSDS-matched)
  ├── structbook      (matched against structural demand)
  ├── hedgebook       (cross-position hedge groups)
  └── unmatched       (what didn't fit)
       │
       ▼
   single Primeunit issued upward to Genbook
```

---

## 2. Sub-books as risk-coverage contracts

Each sub-book is a **contract about which risks it covers**:

| Sub-book | Default | Credit-spread MTM | Rate | Liquidity |
|---|---|---|---|---|
| `ascbook` | Capital | Capital | n/a (cash-equivalent) | The product (must hold) |
| `tradingbook` | Capital | Forced-loss | Hedged or rate-hedge capital | Forced-loss (FRTB captures it) |
| `termbook` | Capital | **Covered** (held to par; matched fixed/fixed) | **Covered** (matched fixed/fixed via tUSDS YT) | **Covered** (no forced sale) |
| `structbook` | Capital | **Covered** (held to par) | Capital required (rate-hedge or v1 carve-out) | **Covered** (no forced sale) |
| `hedgebook` | Capital | Capital adjusted for hedge | Capital adjusted for hedge | Capital adjusted for hedge |
| Unmatched | Capital | Forced-loss | Forced-loss | Forced-loss |

Reading the matrix: a position landing in `termbook` has **three of its four non-default risks covered by structure**; default capital is still required because no structural mechanism eliminates default. A position landing in `tradingbook` has only default covered intrinsically; the others are forced-loss exposures unless explicitly hedged.

**Default capital is always required** because it's the irreducible loss. Every position pays its default RW; sub-book structure only reduces the *other* four risks.

---

## 3. The five sub-book types + unmatched

### `ascbook` — peg-defense readiness

Holdings that qualify as Actively Stabilizing Collateral (per `asc.md`). Liquidity isn't a risk to capitalize; it's the *product* — these holdings must remain immediately deployable for peg defense. Capital required against default and credit-spread; rate and liquidity are inapplicable (cash-equivalent / must-hold).

### `tradingbook` — liquid FRTB-style

Liquid holdings expected to trade. Capital under the standard FRTB-style forced-loss model. Eligibility: position must satisfy `(U AND P) OR T` from the U/P/T decomposition.

### `termbook` — tUSDS-matched

TTM (term-to-maturity) units matched against tUSDS-issued YT (Yield Tokens). The Prime holds the YT side, the Halo holds the bond side; the matched position is fixed/fixed (rate hedged) and held-to-par (no forced sale). Three risks covered: credit-spread MTM (held to par), rate (matched), liquidity (no forced sale). Default capital remains.

**Note:** tUSDS / YT split market is itself a Phase 2+ feature; the v1 risk framework has the schema and category but the tUSDS/YT market isn't live yet.

### `structbook` — matched against structural USDS demand

TTM units matched against structural demand for USDS holding (per `duration-model.md`). Held to par; spread MTM and liquidity are covered. **Rate is NOT covered** because structural demand is variable-rate; the Prime must hedge or hold rate-hedge capital. (V1 carve-out: rate-hedge capital relaxed for the test.)

### `hedgebook` — cross-position hedge groups

Cross-Halobook hedge structures composed at the Prime level. Optimization sub-book that pairs hedge instruments with eligible Halobook unit exposures. Full treatment in `hedgebook.md`.

### Unmatched leftover

Anything that didn't fit any of the above gets treated as forced-loss across all three non-default risks — equivalent to the `tradingbook` treatment without the FRTB-eligibility benefits.

---

## 4. Optimization-shaped vs static-treatment

Sub-books split into two operational modes:

### Optimization-shaped (run internal optimization)

| Sub-book | Optimization |
|---|---|
| `structbook` | Allocate available bucket capacity to positions to minimize total CRR |
| `termbook` | Allocate available tUSDS-matched liabilities to positions |
| `hedgebook` | Allocate available hedge instruments to positions to minimize residual risk |

Position-level CRR formula in optimization sub-books:

```
structbook position CRR = matched_portion × RW
                        + unmatched_portion × max(RW, forced-loss-capital)

hedgebook position CRR = hedged_portion × hedge_residual_CRR
                       + unhedged_portion × natural_sub_book_CRR
```

**Key insight:** when capacity/hedges shrink, the blend shifts smoothly toward unmatched/unhedged. No binary "transition" event. Capital requirement updates continuously.

This dissolves the old "treatment-coverage-failure" and "hedge-breakdown-transition" problems — they were predicated on binary coverage that doesn't exist in this framing.

### Static-treatment (uniform treatment, no internal optimization)

| Sub-book | Treatment |
|---|---|
| `tradingbook` | All positions get FRTB-style forced-loss capital |
| `ascbook` | ASC-eligibility check (binary) |
| Unmatched | All positions get max(RW, forced-loss) |

Static sub-books just classify their members — no allocation choice to make.

### Combinatorial optimization in scarce-capacity scenarios

When not everything can be matched/hedged, *which* positions get matched matters. Default optimization: greedy descending (longest-TTM to longest-bucket capacity, cumulative downward). Prime can declare alternative preferences:

```metta
(optimization-preference greedy-min-total-crr)
;; or
(optimization-preference priority-order
   (priorities (highest-unmatched-crr-first)))
;; or
(optimization-preference manual
   (allocations (... explicit per-position match amounts ...)))
```

For v1: default greedy descending; no Prime overrides exercised.

---

## 5. Routing Halobook units to sub-books

Routing happens at the Primebook layer. The default rule is **declarative routing by structural eligibility, picking the most capital-efficient eligible sub-book**.

```metta
(= (route-to-sub-book $halo-unit)
   (case (eligible-sub-books $halo-unit)
     ((empty            unmatched)
      ((subbooks ...)   (most-capital-efficient (subbooks ...))))))
```

Eligibility per sub-book:

| Sub-book | Structural prerequisite |
|---|---|
| `ascbook` | ASC eligibility (deep peg-defense liquidity, < 15min convertibility) |
| `tradingbook` | Has U/T liquidity profile; (U AND P) OR T |
| `termbook` | Actual tUSDS-matched liability paired up; position TTM matches |
| `structbook` | Available bucket capacity allocation; position TTM in eligible range |
| `hedgebook` | Hedge instrument actually held by Prime + composition constraint satisfied |

Manual override is allowed: Prime can re-classify a position to a different eligible sub-book, subject to the same structural prerequisites.

---

## 6. Treatment-switch policy

**One-position-one-sub-book at a time.** A position is in exactly one sub-book; the within-sub-book optimization handles internal blending (matched/unmatched portions).

**Switching is free** — Prime can re-classify a position to a different sub-book whenever they want, subject to the structural prerequisites in §5. The structural prerequisites cannot be faked: you can't claim termbook eligibility without an actual tUSDS-matched liability paired up.

**No motivational scrutiny.** Prime is not required to declare reasons for switches — that would force stream-sentinel strategy disclosure, defeating the privacy of private cognition. Structural prerequisites are the only check.

This eliminates the gaming concern except for one residual: switching at strategically chosen moments (most acute mid-crash). The defense is the crash oracle (§7).

### Why this works

The optimization sub-books make capital flow smoothly with capacity; switching during a crash to escape unfavorable treatment doesn't gain much because:
- Crash → spread blowout → forced-loss term in `tradingbook` rises
- Crash → bucket capacity shrinks → matched_portion in `structbook` shrinks → blended CRR rises
- The arithmetic doesn't reward gaming; the crash penalty applies regardless

---

## 7. Crash oracle (deferred)

The remaining gaming surface is "switching at strategically chosen moments — most acute mid-crash, when the optimization-blended CRR is rising fast."

The deferred mechanism: a **crash oracle** that suspends treatment switches during a declared crash window.

```metta
;; in &core-framework-crash-oracle (universal)
(crash-trigger-conditions
   (or (asset-drop btc -0.30 over-window 24h)
       (asset-drop eth -0.30 over-window 24h)
       (correlation-spike $threshold)
       (settlement-delay $threshold)
       (manual-trigger by-governance)))

(crash-state-active False)                           ; flipped True when triggers fire
(crash-state-active-since $timestamp)
(crash-state-cooldown-period 24h)
```

When crash state is active:
- All treatment switches blocked (structural error at gate)
- Switches in lookback window (e.g., 24h before trigger) reversible at next settlement
- Cooldown after crash resolution before switches resume

**For v1 test:** no crash oracle implementation; free switching; record events; deal with problems if/when they emerge. Gaming risk is low with 3 known GovOps operators (Spark/Grove/Keel) and modest portfolios.

Crash oracle is on the Phase 2+ implementation surface; the schema is here so the v1 design doesn't preclude it.

---

## 8. The single Primeunit upward

After all sub-book composition, the Primebook still issues **a single Primeunit upward to the Genbook**. The sub-books are internal composition for risk treatment, not external products.

```
Primebook holds:
   ascbook    (subset of Halobook units)
   tradingbook (subset)
   termbook    (subset)
   structbook  (subset)
   hedgebook   (subset)
   unmatched   (subset)
       │
       │ each sub-book contributes its CRR-weighted exposure
       │
       ▼
   Aggregate Primebook CRR
       │
       ▼
   Single Primeunit issued to Genbook (notional + risk vector)
```

The Genbook holds Primeunits from all serving Primes, applies concentration caps via the correlation framework (per `correlation-framework.md`), and ultimately backs USDS issuance.

---

## 9. One-line summary

**The Primebook composes five typed sub-books (ascbook / tradingbook / termbook / structbook / hedgebook) plus an unmatched leftover; each sub-book is a risk-coverage contract declaring which non-default risks it covers; optimization sub-books (structbook / termbook / hedgebook) blend matched and unmatched portions smoothly, while static sub-books (tradingbook / ascbook / unmatched) apply uniform treatment; routing is declarative by structural eligibility; treatment switches are free subject to structural prerequisites; the Primebook still issues one Primeunit upward to the Genbook.**

---

## File map

| Doc | Relationship |
|---|---|
| `book-primitive.md` | Primebook is one specialization of the 6-tuple book |
| `risk-decomposition.md` | The risk-type × sub-book coverage matrix originates here |
| `halobook-layer.md` | Halobook units routed into sub-books |
| `riskbook-layer.md` | The regulated unit; CRR ultimately rolls up from here |
| `hedgebook.md` | One of the sub-books, deserves its own treatment |
| `matching.md` | termbook/structbook matching mechanics — credit-spread vs rate distinction |
| `duration-model.md` | structural demand allocation (Lindy + structural caps) feeding `structbook` |
| `correlation-framework.md` | Concentration limits applied at Primebook + Genbook |
| `capital-formula.md` | Final CRR computation flow integrating all sub-books |
