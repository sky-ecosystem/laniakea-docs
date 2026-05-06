# Synome Risk Framework — Additional Information from 2026-05-03 Session

**Date:** 2026-05-03
**Status:** Continuation notes from `risk-framework-redesign-2026-05-03.md`. Captures new insights and refinements that emerged after the original comprehensive doc was written.
**Purpose:** Save context before clearing the conversation. Pair with the original doc to have full picture.

---

## TL;DR — what's new since the original doc

Five substantive additions/refinements to the framework:

1. **U/P/T three-dimensional liquidity decomposition** — splits "liquidity" into Underlying-unwind / Permitted-unwind / Transfer-market, each living in different layers
2. **Halobook reframed as "bundle exposure structure"** (general) — not just liquidity adjustment; affects any risk type via structural features (rollover, lockup, embedded options, etc.)
3. **Cross-default → Riskbook constraint** — joint-default structures must live in a single Riskbook; Halobook NEVER modifies default risk
4. **Sub-books as optimization engines vs static-treatment** — `structbook`, `termbook`, `hedgebook` are optimization-shaped (continuous blending); `tradingbook`, `ascbook` are static treatment
5. **Treatment-switch policy** — one-position-one-sub-book at a time; switches free subject to structural prerequisites; crash-oracle handles peak fudging risk; no motivational checks (preserves stream-sentinel privacy)

Plus: **TTM ≠ default risk in snapshot-stress framing** (an important conceptual clarification that simplifies the layering).

---

## 1. The U/P/T three-dimensional liquidity decomposition

Earlier framing (in original doc) treated Halobook as "applies a liquidity downgrade to the Riskbook output." That was hand-wavy. Cleaner framing:

There are **three different liquidity questions**, each living in a different place:

| | What it answers | Where it lives |
|---|---|---|
| **U — Underlying unwind** | *Can* the underlying be unwound? (digging into the Riskbook → exobooks → exo assets) | Riskbook output (composition + asset stress profiles + tranche waterfall) |
| **P — Permitted unwind** | *May* we actually execute that unwind? (lockups, governance approvals, third-party consents, notice periods, contractual restrictions) | Halobook declaration |
| **T — Transfer market** | Can the Halo unit *itself* be sold to a willing buyer? (sidesteps U and P entirely) | Halobook declaration (with market-depth atoms) |

Two paths to "exit a position":
- **Path 1: Unwind underlying** — requires `U AND P`
- **Path 2: Transfer the wrapper** — requires `T`

Effective liquidity for downstream consumers = best available path.

**Sub-book eligibility maps to dimensions:**

| Sub-book | Liquidity requirement |
|---|---|
| `structbook` / `termbook` | None — held to maturity, matched against liability |
| `tradingbook` | `(U AND P) OR T` — need to be able to exit somehow |
| `ascbook` | `T` (or near-instantaneous `U AND P`) — needs immediate availability |
| `hedgebook` | Depends on hedge structure; probably needs `T` for the hedge leg |
| Unmatched | Whatever liquidity exists determines the forced-loss term |

**Schema:**
```metta
;; Riskbook output (U)
(underlying-liquidity-profile $position
   (drawdown-distribution ...)
   (slippage-by-size ...)
   (unwind-time-distribution ...))

;; Halobook category declaration (P)
(permitted-unwind $halo-unit
   (lockup-until $date)
   (approval-required $authority)
   (notice-period $days)
   (early-unwind-conditions ...))     ; e.g., "only on health-factor breach"

;; Halobook category declaration (T)
(transfer-market $halo-unit
   (transferable True/False)
   (market-depth-profile ...)
   (acceptable-buyers $registry-ref))
```

**Tranche rights schema (from original doc Q23) is now resolved naturally:** redemption rights, liquidation acceleration, transfer rights are how P and T are expressed. Not a separate "rights" layer.

**For v1 crypto-lending test:**
- U = derived from BTC/ETH/stETH stress profiles + tranche waterfall (computed)
- P = "only at maturity OR health-factor breach" (constrained)
- T = null (NFATs not actively traded)
- → Routes to `structbook` because U/P/T limitations don't matter when matched

---

## 2. Halobook as "bundle exposure structure" (general framing)

Earlier framing: "Halobook applies liquidity adjustments." That was too narrow.

**Cleaner framing:** The Halobook category declares the bundle's **exposure structure** — what happens to per-position risks over the bundle's lifetime, given the bundle's terms (rollovers, lockups, transferability, embedded options, etc.). This affects ANY risk type via the exposure structure, not just liquidity.

| Halobook structural feature | Default | Spread | Rate | Liquidity |
|---|---|---|---|---|
| Rollover (any flavor) | Never (cross-default constraint) | Compounds spread duration if held to par | Compounds rate duration unless reset | Worsens P |
| Lockup, no transfer | Never | Same | Same | Worsens P |
| Prepayment option (issuer-held) | Never | Negative convexity | Negative convexity | Same |
| Joint-and-several obligation | **Disallowed at Halobook level** — must be in single Riskbook | — | — | — |

**Architectural division of labor:**
- **Riskbook output:** per-position snapshot risk vector at one moment (default, spread-sensitivity, rate-duration, U)
- **Halobook category:** declares exposure structure — how those per-position risks compound/aggregate over the bundle lifetime
- **Halobook output:** bundle-level risk vector that's the composition of per-position risks × exposure structure

For v1 crypto-lending: NFATs are fixed-term, no rollover/options/convertibles. Per-period risks pass through unchanged. Halobook category = `nfat-crypto-lending-fixed-term` (just declares lockup + null-transferability).

---

## 3. Cross-default → Riskbook constraint

**Architectural invariant:** Default risk is set entirely at the Riskbook level. Halobook NEVER modifies default risk. Any structural feature that would change joint-default behavior must be captured by composing the relevant positions in a single Riskbook with a category that understands their joint behavior.

**What's a cross-default clause:** Contractual provision saying "if borrower defaults on any of its OTHER debts (above some threshold), this debt is also in default — even if currently performing." Common in TradFi to prevent strategic-default and force creditor coordination.

**Why disallow them at Halobook level:** Allowing cross-Halobook default linkages would mean Halobook category equations need to model joint-default behavior. Cleaner: force structurally-linked positions into a single Riskbook (same pattern as `abf-with-cds-cover` — both legs in one Riskbook, category equation knows the relationship).

**Implications:**
- Cross-Halo cross-default would require a single Riskbook holding positions from both Halos → same Halo operationally owns the Riskbook (so it's not really cross-Halo anymore)
- This forces clean operational alignment: legal/operational ownership = Riskbook boundary = unit of joint-default modeling
- Cross-Halo cross-default would be governance-weird anyway (different operators, different risk teams)

---

## 4. Sub-books as optimization engines (vs static containers)

Earlier framing treated all sub-books symmetrically — each "covers" certain risks. But under continuous capacity/hedge availability, that's binary and brittle. Cleaner framing:

**Optimization-shaped sub-books** (run internal optimization to maximize coverage, produce blended CRR):

| Sub-book | Optimization |
|---|---|
| `structbook` | Allocate available bucket capacity to positions to minimize total CRR |
| `termbook` | Allocate available tUSDS-matched liabilities to positions |
| `hedgebook` | Allocate available hedge instruments to positions to minimize residual risk |

**Static-treatment sub-books** (uniform treatment, no internal optimization):

| Sub-book | Treatment |
|---|---|
| `tradingbook` | All positions get FRTB-style forced-loss capital |
| `ascbook` | ASC-eligibility check (binary) |
| Unmatched | All positions get max(RW, forced-loss) |

**Position-level CRR formula in optimization sub-books:**
```
structbook position CRR = matched_portion × RW
                        + unmatched_portion × max(RW, forced-loss-capital)

hedgebook position CRR = hedged_portion × hedge_residual_CRR
                       + unhedged_portion × natural_sub_book_CRR
```

**Key insight:** when capacity/hedges shrink, the blend shifts smoothly toward unmatched/unhedged. No binary "transition" event. Capital requirement updates continuously.

This dissolves Q6 (treatment-coverage-failure) and Q7 (hedge breakdown transitions) from the original doc — they were predicated on binary coverage that doesn't exist in this framing.

**Combinatorial optimization in scarce-capacity scenarios:**

When not everything can be matched/hedged, choice of allocation matters. Default optimization: greedy descending (match longest-TTM to longest-bucket capacity, cumulative downward). Prime can declare alternative preferences:

```metta
(optimization-preference greedy-min-total-crr)
;; or
(optimization-preference priority-order
   (priorities (highest-unmatched-crr-first)))
;; or  
(optimization-preference manual
   (allocations (... explicit per-position match amounts ...)))
```

For v1 crypto-lending: default greedy descending; no Prime overrides exercised.

---

## 5. Treatment-switch policy

**One-position-one-sub-book at a time.** A position is in exactly one sub-book; the within-sub-book optimization handles internal blending (matched/unmatched portions).

**Switching is free** — Prime can re-classify a position to a different sub-book whenever they want, subject to **structural prerequisites**:

| Sub-book | Structural prerequisite (cannot be faked) |
|---|---|
| `structbook` | Available bucket capacity allocation; position TTM in eligible range |
| `termbook` | Actual tUSDS-matched liability paired up; position TTM matches |
| `hedgebook` | Hedge instrument actually held on Prime's books + composition constraint satisfied |
| `tradingbook` | Position has the U/T liquidity profile |
| `ascbook` | ASC eligibility (deep peg-defense liquidity, < 15min convertibility) |

**No motivational scrutiny.** Originally I proposed "Prime must declare a reason for switches; wardens check reason validity." User objected: this would force stream-sentinel strategy disclosure (defeats the point of private cognition). Replaced with structural prerequisites only.

**Crash oracle as residual control:**

The remaining gaming surface is "switching at strategically chosen moments" — most acute mid-crash. Crash oracle:

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

**For v1 test:** no crash oracle implementation; free switching; record events; deal with problems if/when they emerge. Gaming risk is low with 3 known GovOps operators and modest portfolios.

**Architectural placement for the rewrite:**
- `risk-decomposition.md` and `primebook-composition.md`: state the structural-prerequisite principle
- Each sub-book documents its eligibility constraints
- Treatment switches recorded in audit trail
- Crash oracle deferred to Phase 2+ doc

---

## 6. TTM ≠ default risk in snapshot-stress framing

Important conceptual clarification: longer TTM does NOT directly increase default risk in our framework.

Our framework asks: "if a worst-case stress event hits **right now** and we have to liquidate, what's the loss?" Point-in-time question.

For a 90-day loan vs. a 365-day loan against the same borrower with the same collateral:
- Borrower's solvency in stress = same
- Collateral value in stress = same
- Liquidation mechanics = same
- **Snapshot default loss = same**

Where TTM matters:
- **Cumulative default probability over life** — yes, but framework doesn't measure this
- **Spread duration** — more time for spread events to compound (credit-spread MTM exposure)
- **Rate duration** — fixed-rate exposure scales with duration if not hedged/reset
- **Liquidity (P)** — longer waits for natural maturity exit

So my earlier "rollover compounds default risk" claim was wrong. Rollover compounds spread + rate + liquidity exposure, not default in the snapshot framing.

---

## 7. Refined answers to specific Q numbers from original doc

**Q1 (Halobook downgrade semantics):** Resolved via U/P/T decomposition (above).

**Q2 (SPTP split credit-spread vs rate):** YES split. Two values per position: `credit-spread-duration` and `rate-duration`. Termbook covers both; structbook covers only credit-spread (rate needs hedging or v1 carve-out). For v1 NFATs both values = nominal term.

**Q3 (Tranche-cushion revaluation under stress):** Just a category-equation correctness requirement — must stress both asset side AND tranche cushion sizes consistently in each scenario. No new architectural primitive needed.

**Q4-Q5 (Multi-tranche / tranche-frame mismatches):** Confirmed deferred for v1.

**Q6 (Treatment-coverage-failure):** Dissolves under optimization-sub-book framing. Capacity shrinks → blend shifts smoothly toward unmatched_portion → CRR rises continuously → operational/governance discipline (existing breach-response mechanisms) handles overall capital ratio.

**Q7 (Hedge breakdown transitions):** Dissolves the same way. Hedge availability shrinks → hedged_portion shrinks → CRR rises continuously. Hedge breakdown is just "available hedge supply went down."

**Q8 (Routing Halobook units to sub-books):** Default = declarative routing by structural eligibility, picking most capital-efficient eligible sub-book. Override = Prime can manually classify (subject to structural prerequisites). Treatment switches are free (subject to structural prerequisites + crash-oracle constraints).

**Q9 (Hedge declaration mechanism):** Prime declares hedge candidates + available hedge instruments; hedgebook's optimization figures out best pairing. Cleaner than fixed hedge groups.

```metta
(hedge-candidate $halo-unit)
(hedge-instrument $position)
```

**Q10 (Cross-Halobook flow into Hedgebook):** Hedge instruments must be held by the Prime directly, NOT within other Halobooks (preserves bankruptcy-remoteness). Hedgebook reads Halobook-unit exposures + Prime-level hedge instruments.

**Q11 (Hedgebook unit issuance):** No separate unit. Hedgebook just contributes its CRR to the Primebook total like any other sub-book. Primebook still issues a single Primeunit upward to Genbook.

**Q12 (Concentration interaction with hedges):** v1 = concentration on gross exposure (no hedge relief). v2+ may add `effective_concentration = max(net_of_hedge, gross × hedge_failure_haircut)`.

**Q13 (Currency identifier registry):** `&core-registry-currency` with one atom per currency. Properties (depeg profiles, FX stress) probably in parallel `&core-framework-currency-stress` Space (separate because stress profiles are recalibrated more often than identity is registered).

**Q14 (Cross-frame conversion rules):** `&core-framework-fx-stress` with per-pair atoms (not per-currency, because correlations and asymmetric stress matter). V1 USDS-only: not exercised.

**Q15 (Multi-generator Primes):** Future scope. Schema: `(serves-generator $prime $generator)` registry; one Primebook per generator served.

**Q16 (1:1 lock stale calibration):** Each currency stress profile carries calibration metadata `(last-calibrated $date) (calibration-confidence $level)`. Governance cadence for recalibration. Sentinel-style alarms when realized depeg approaches modeled limits. V1: hand-tuned conservative profiles, no automated alarms.

**Q17 (Generator's place in authority chain):** RESOLVED 2026-05-03. Single operational guardian model: Ozone is the only Guardian; USGE Generator and all Primes (Spark, Grove, Keel, Obex, others as added) are direct children of Ozone in the accordancy graph. Multiple GovOps teams coexist under Ozone, each scoped to the entity it administers (Spark operator runs Spark Prime, USGE operator runs USGE Generator, etc.). Existing Guardian/GovOps separation from `synart-access-and-runtime.md` §4 holds — only the Guardian count is collapsed to one. Topology updates landed in `topology.md`, `syn-overview.md`, `synart-access-and-runtime.md`, `settlement-cycle-example.md`, `risk-framework-redesign-2026-05-03.md`, `govops-synlang-patterns.md`.

**Q18-Q33:** All settled per the original doc's recommendations. Nothing has changed those answers in this session.

---

## 8. New items A-G from original doc — current state

These were flagged at end of original doc as "things noticed during answering Q1-Q33." Current thinking:

**A. Halobook category vocabulary for v1.** Resolved. Halobook category for the test = `nfat-crypto-lending-fixed-term` (lockup until maturity, no transferability, no rollover, passthrough on per-period risks). Schema supports more elaborate Halobook categories later.

**B. Real-time computation cadence.** Recommend (b): equity computations and matching status update real-time (driven by price/oracle); category-catalog changes and structural-demand updates apply at next settlement boundary. Cleaner separation. Confirm before rewrite.

**C. Beacon implementation for new framework.** `lpla-checker` algorithm needs significant updates (asset-stress-profile lookup, tranche waterfall, Halobook adjustment, sub-book routing, matched/unmatched split). May want to split across multiple beacons (one per layer). **WORTH A SEPARATE DESIGN PASS** but probably after the rewrite.

**D. Migration / transition strategy.** Existing positions need reclassification into new model. Probably governance-paced one-time mapping. Defer the actual mapping; focus on new model first.

**E. Scraper deployment model.** Structural-demand scrapers follow endoscraper pattern: synserv runs canonical, verifiers shadow, disagreements escalate. Lives in `&entity-generator-usge-structural-demand-scrapers`.

**F. Genbook's frame and operations.** Genbook in USD frame, pure aggregation v1, equity tranche held by Sky (linked to TMF target — 1.5% of USDS supply post-Genesis). The TMF capital provides the Genbook's equity invariant cushion.

**G. Default-deny CRR 100% pattern.** Make this a foundational architectural rule alongside the equity invariant. It IS the catalog-curation discipline that makes the framework safe.

---

## 9. Remaining open questions before rewrite

**REQUIRES YOUR INPUT:**

1. **Q17: Generator's place in the authority chain** — RESOLVED 2026-05-03 (see §7). Single operational guardian Ozone; USGE Generator + all Primes accordant to Ozone. Topology updates have landed.

2. **Item B: Real-time computation cadence** — confirm hot-path real-time + settlement-boundary-batch hybrid is the right model.

3. **Item D: Migration strategy timing** — defer until after rewrite, or address concurrently?

4. **Item C scope** — does beacon implementation get its own design pass, or is it part of the rewrite?

**RESOLVED BUT WORTH CONFIRMING:**

5. **Tranche-frame mismatches deferred to v2+** — confirmed?
6. **Multi-tranche holdings deferred to v1** — confirmed (super-senior only)?
7. **JAAA / CLO modeling deferred** — confirmed?
8. **Termbook / tUSDS mechanism deferred** — confirmed v1 has tUSDS market not built; only structbook actually exercised?
9. **Halobook category catalog for v1** — only `nfat-crypto-lending-fixed-term` (passthrough)? Future categories deferred?

---

## 10. Suggested next steps for the rewrite

Once Q17 and items B/C/D are resolved:

**Phase 1: Core conceptual docs (highest priority)**

1. Write `risk-decomposition.md` (laniakea-docs/risk-framework/) — the conceptual root. Includes:
   - Five risk types
   - Teleological grounding (continue/liquidate decision)
   - Risk-types × layer × sub-book-coverage matrix
   - Why "gap risk" and "FRTB drawdown" unify as `forced-loss-capital`
   - U/P/T liquidity decomposition
   - Cross-default → Riskbook constraint
   - Default-deny CRR 100% as foundational pattern

2. Write `book-primitive.md` — substrate definition. Includes:
   - 6-tuple book primitive
   - Equity invariant
   - Tranching as first-class
   - Rules attached to books
   - Real-time equity recomputation

3. Write `tranching.md` — first-class tranching mechanics. Includes:
   - Exoassets/exoliabs vocabulary
   - Senior/junior/equity tranches
   - Loss propagation through waterfall
   - Tranche rights schema (now P + T declarations)
   - Re-framing of overcollateralized lending

4. Write `currency-frame.md` — frame vs instrument distinction.

**Phase 2: Layer-specific docs**

5. Write `riskbook-layer.md` — Riskbook as default-risk layer + currency unification + tactical hedging.

6. Write `halobook-layer.md` — Halobook as bundle exposure structure + P/T declarations.

7. Write `primebook-composition.md` — Primebook as composition of typed sub-books, with optimization-engine vs static-treatment distinction.

8. Write `hedgebook.md` — Hedgebook details (two-level hedging, optimization, breakdown handling).

9. Write `projection-models.md` — projection pattern.

**Phase 3: Updates to existing docs**

10. Update `matching.md` to reflect smooth-blending optimization framing.
11. Update `duration-model.md` for Generator-entart placement.
12. Update `correlation-framework.md` for two-level concentration (Primebook + Genbook).
13. Update `capital-formula.md` as downstream consumer of the new layered model.
14. Rewrite `asset-type-treatment.md` with new framework.
15. Update `asc.md` and `operational-risk-capital.md` to clarify they're parallel tracks.
16. Update `examples.md` with new framework worked examples.

**Phase 4: noemar-synlang updates**

17. Update `topology.md` (entity types, sub-kinds, entart tree examples).
18. Major rewrite of `noemar-synlang/risk-framework.md`.
19. Update `synlang-patterns.md` for tranches, rules, projection-model declarations.
20. Update `syn-overview.md`, `syn-tel-emb.md`, `settlement-cycle-example.md`.

---

## 11. Cross-reference: where to find things

For full context, use both docs:
- **Original doc:** `risk-framework-redesign-2026-05-03.md` — captures Parts 1-8 (architectural primitives, test setup, plan for editing, Q1-Q33, future work, key insights, appendices)
- **This doc:** `synome-extra-info.md` — captures the additional refinements and clarifications from the continuation session

If reading from scratch:
1. Read `risk-framework-redesign-2026-05-03.md` first for the full picture
2. Read this doc as updates/refinements
3. Resolve Q17 and items B/C/D before starting rewrite
