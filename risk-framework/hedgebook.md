# Hedgebook

**Status:** Draft (Phase 2 layer doc, 2026-05-05)

The Hedgebook is the Primebook sub-book where well-defined hedge pairs/groups get composed across the Prime's diverse portfolio. Distinct from Riskbook-level (tactical) hedging, Hedgebook hedges are portfolio-level — broad-market hedges across positions in different Halobooks. The category equation rewards anti-correlation; **residual basis risk after the hedge is what gets capital-charged**, not either leg's standalone risk.

Companion to:
- `primebook-composition.md` — Hedgebook is one of the typed sub-books
- `riskbook-layer.md` — tactical hedging within a single coherent strategy lives here, not Hedgebook
- `risk-decomposition.md` — the four non-default risks the Hedgebook can adjust
- `correlation-framework.md` — concentration limits interact with hedge accounting

---

## TL;DR

Two distinct levels of hedging:

| Level | Scope | Examples |
|---|---|---|
| **Riskbook (tactical)** | Within one coherent strategy / single composition | `abf-with-cds-cover` (ABF claim + matching CDS in same Riskbook); `delta-neutral-eth-spot-perp` (long spot + short perp) |
| **Hedgebook (portfolio)** | Across the Prime's diverse portfolio | Long credit via Halobook A + index-CDS hedge via Halobook B; USDC concentration across Riskbooks + Circle-CDS hedge separately |

Hedgebook explicitly models hedge failure modes: counterparty risk, basis risk, liquidity on closing the hedge under stress. The output is a quantified residual-risk computation, not "hedge magic."

---

## Section map

| § | Topic |
|---|---|
| 1 | Two-level hedging architecture |
| 2 | When Riskbook-level vs Hedgebook-level applies |
| 3 | Hedgebook as cross-Halobook composition |
| 4 | Optimization within the Hedgebook |
| 5 | Hedge failure modes explicitly modeled |
| 6 | Currency hedges via Hedgebook |
| 7 | Hedgebook category equations |
| 8 | One-line summary |

---

## 1. Two-level hedging architecture

Hedging happens at two distinct architectural levels, each with its own scope and economics:

```
Riskbook-level (tactical):
  - Specific position + specific hedge in same Riskbook
  - Hedge math expressed by the Riskbook category equation
  - Bankruptcy-remote within one Riskbook

Hedgebook-level (portfolio):
  - Hedge instrument held at Prime level, hedging exposure across multiple Halobooks
  - Hedge math expressed by Hedgebook category equation (optimization)
  - Cross-Halobook composition without breaking bankruptcy-remoteness
```

The Riskbook is for hedges that are part of one strategy: an ABF claim with its CDS, a long spot with its perp short. These are tightly-defined relationships between specific instruments.

The Hedgebook is for hedges that span the Prime's portfolio: a single index-CDS hedging credit exposure across many Halobooks, a USDC depeg hedge protecting USDC concentration across many Riskbooks. These are broad-market hedges where the hedge instrument can't naturally live inside any one Riskbook.

---

## 2. When Riskbook-level vs Hedgebook-level applies

| Use Riskbook hedging when... | Use Hedgebook hedging when... |
|---|---|
| Hedge is specific to one position | Hedge covers exposure across many positions |
| Both legs are part of one coherent strategy | Hedge is a portfolio-level overlay |
| Hedge math is captured by a registered Riskbook category | Hedge math is portfolio-residual computation |
| Bankruptcy-remoteness within one Riskbook is appropriate | Hedge instrument needs to span Halobooks |

**Examples that fit Riskbook:**
- `abf-with-cds-cover` — ABF claim + CDS-on-same-ABF in one Riskbook
- `delta-neutral-eth-spot-perp` — long ETH spot + short ETH perp, balanced
- Convertible bond + short common stock as a delta hedge

**Examples that fit Hedgebook:**
- Long credit positions across multiple Halobooks + index-CDS hedge held at Prime level
- USDC concentration across many Riskbooks + Circle-CDS hedge or USDC/USDT FX hedge
- Rate exposure across many fixed-rate positions + interest-rate-swap hedge

The Hedgebook can only meaningfully evaluate hedges between **cleanly-defined positions** — Riskbook output. Messy exobooks can't be hedged in the Hedgebook because the hedge math depends on knowing what you're hedging precisely.

---

## 3. Hedgebook as cross-Halobook composition

The Hedgebook is the **first place cross-Halobook composition happens** in the Prime's risk computation. This is delicate because bankruptcy-remoteness must be preserved.

The mechanism:
- Hedge instruments are **held at the Prime level**, not within any Halobook
- The Hedgebook is **read-only at the Halobook level** — it observes Halobook unit exposures and composes for capital purposes
- The Hedgebook does **NOT actually merge bankruptcy estates** — Halobook units retain their bankruptcy-remote structure
- The capital benefit flows through pricing, not through legal merger

```metta
;; Prime declares a hedge instrument held at Prime level
(prime-hedge-instrument spark-prime hedge-001
   (instrument-class index-cds)
   (notional 50000000)
   (counterparty major-dealer-X)
   (hedge-target credit-exposure))

;; Prime declares Halobook unit exposures eligible for hedging
(hedge-candidate spark-prime $halo-unit)

;; Hedgebook composition pairs them
(hedgebook-pairing spark-prime hedge-001 [(halo-unit-A 30M) (halo-unit-B 20M)])
```

The Hedgebook unit issuance: **no separate unit**. The Hedgebook just contributes its CRR to the Primebook total like any other sub-book. Halobook units that participate get "claimed" by Hedgebook composition; their natural-sub-book contribution is replaced.

---

## 4. Optimization within the Hedgebook

The Hedgebook is one of the **optimization-shaped** sub-books (per `primebook-composition.md` §4). It runs internal optimization to maximize coverage given the hedge instruments available:

```
hedgebook position CRR = hedged_portion × hedge_residual_CRR
                       + unhedged_portion × natural_sub_book_CRR
```

When hedge availability shrinks (e.g., hedge instrument matures or is partially consumed), `hedged_portion` shrinks, blended CRR rises smoothly. No binary "hedge-breakdown" event.

Default allocation: pair hedge instruments to highest-CRR Halobook unit exposures first. Prime can declare alternative preferences (specific pairings, manual overrides) per the optimization-preference mechanism.

The optimization is bounded by:
- Hedge instrument availability (Prime's actual holdings)
- Composition constraints in the Hedgebook category (instrument type matches exposure type)
- Currency frame compatibility (hedge instrument and exposure must translate to a common frame for the math to compose)

---

## 5. Hedge failure modes explicitly modeled

The Hedgebook does NOT hand out "hedge magic." Hedge effectiveness is a **quantified residual-risk computation** that explicitly models failure modes:

| Failure mode | What it is | How the equation models it |
|---|---|---|
| **Counterparty risk** | CDS issuer fails to pay | Effective payout = notional × counterparty-survival-probability under scenario |
| **Basis risk** | Hedge instrument doesn't track the specific exposure | Residual = exposure × (1 − correlation) |
| **Liquidity risk** | Hedge can't be closed under stress | Closing-loss = notional × stress-slippage profile |
| **Tenor mismatch** | Hedge expires before exposure | Roll cost / stub exposure |

Clean hedge → near-zero residual. Sloppy hedge → mostly capitalized. The equation tells the truth about what you actually have:

```metta
(= (hedge-residual-crr $hedge-pair $scenario)
   (let* (($exposure         (exposure-amount $hedge-pair))
          ($cp-survival      (counterparty-survival-prob $hedge-pair $scenario))
          ($basis-correlation (basis-correlation-under-stress $hedge-pair $scenario))
          ($closing-slippage (closing-stress-slippage $hedge-pair $scenario))
          ($effective-payout
             (* $exposure $cp-survival $basis-correlation
                (- 1.0 $closing-slippage))))
     (max 0 (- $exposure $effective-payout))))
```

Rule of thumb: a hedge with a major-dealer counterparty (high survival), tight basis (high correlation), and deep secondary market (low closing slippage) gives substantial CRR reduction. A hedge with a stressed counterparty, loose basis, or thin secondary market gives little.

---

## 6. Currency hedges via Hedgebook

A natural use case: a Prime hedging system-wide USDC depeg risk with a Circle-CDS or USDC/USDT FX hedge. The hedge lives in the Hedgebook, providing CRR reduction across the Prime's USDC exposure across many Riskbooks.

```metta
(prime-hedge-instrument spark-prime usdc-depeg-hedge
   (instrument-class circle-cds)
   (notional 100000000)
   (counterparty circle-internal)
   (hedge-target usdc-depeg))

;; Halobook units with USDC exposure are hedge-candidates
(hedge-candidate spark-prime $halo-unit-with-usdc-exposure)
```

The Hedgebook category equation factors USDC's depeg-stress profile (per `currency-frame.md`) and the CDS's payoff under depeg, producing a residual after-hedge USDC exposure CRR.

This is a powerful pattern: instead of every Riskbook holding USDC having to internally model depeg risk, the Prime puts a single hedge in place at portfolio level and the Hedgebook absorbs the math.

---

## 7. Hedgebook category equations

A Hedgebook category specifies:
- **Eligible instrument types** (CDS, IRS, FX hedge, perp short, etc.)
- **Eligible exposure types** (credit, rate, FX, currency, etc.)
- **Composition constraints** (e.g., CDS notional ≥ 80% of credit exposure)
- **Equation** that produces residual-risk CRR per scenario

Example sketch:

```metta
(book-category-def credit-portfolio-with-index-cds-overlay
   (level hedgebook)
   (eligible-instruments [index-cds index-tranche-cds])
   (eligible-exposures [credit-exposure-aggregate])
   (composition-constraints
      (and (cds-notional-coverage-at-least 0.80)
           (cds-counterparty-rating-at-least investment-grade)))
   (equation-m2m
      (sum-over (hedgebook-pairings)
         (lambda ($pair $scenario)
            (hedge-residual-crr $pair $scenario))))
   (resolution-tier simulation))
```

Like Riskbook categories, Hedgebook categories are governance-curated and follow the default-deny pattern: a hedge composition that doesn't match a registered Hedgebook category gets no relief — the underlying positions fall back to their natural sub-book treatment.

---

## 8. One-line summary

**Hedgebook is portfolio-level hedging across the Prime's diverse positions, distinct from Riskbook-level tactical hedging within a single coherent strategy; hedge instruments held at Prime level pair against Halobook unit exposures via Hedgebook category equations that explicitly model hedge failure modes (counterparty risk, basis risk, closing slippage, tenor mismatch); the math is residual-risk computation, not hedge magic — clean hedges give near-zero residual, sloppy hedges give little; Hedgebook is one of the optimization-shaped sub-books, blending hedged and unhedged portions smoothly as availability shifts.**

---

## File map

| Doc | Relationship |
|---|---|
| `primebook-composition.md` | Hedgebook is one of the typed sub-books composed by the Primebook |
| `riskbook-layer.md` | Tactical hedging (within a single strategy) lives here, not Hedgebook |
| `risk-decomposition.md` | The four non-default risks Hedgebook can adjust; counterparty residual is a real cost |
| `currency-frame.md` | Currency hedges read depeg-stress profiles from here |
| `correlation-framework.md` | Concentration limits interact with hedge accounting (gross-of-hedge in v1) |
| `capital-formula.md` | Hedgebook CRR contributes to Primebook total |
