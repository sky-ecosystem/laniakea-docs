# Risk Decomposition

**Status:** Draft (Phase 2 conceptual core, 2026-05-05)

The conceptual root of the risk framework. Defines what kinds of loss the framework recognizes, how each composes through the book stack, and the discipline (default-deny) that keeps the catalog honest.

Companion to:
- `book-primitive.md` — the substrate (6-tuple book + equity invariant) that risk decomposition computes against
- `tranching.md` — how loss propagates through seniority structures
- `currency-frame.md` — how positions in different denominations translate into a common accounting frame

---

## TL;DR

The framework decomposes loss into **five atomic risk types**, each with distinct time signature and stress response. Capital is required against the irreducible portion of each risk that the position can't cover through structure (matching, hedging, tranche cushion, or held-to-maturity treatment).

The teleological grounding is one binary question: **"could we liquidate everything we need to right now if a worst-case crash happened?"** All risk math serves that decision.

The discipline is **default-deny**: any Riskbook composition that doesn't match a registered category gets CRR (Capital Ratio Requirement) 100%. Innovation flows through governance crystallization; no ad-hoc favorable treatment.

---

## Section map

| § | Topic |
|---|---|
| 1 | Teleological grounding |
| 2 | The five risk types |
| 3 | Why gap risk and FRTB drawdown unify |
| 4 | U/P/T liquidity decomposition |
| 5 | Cross-default → Riskbook constraint |
| 6 | The risk-type × layer coverage matrix |
| 7 | Default-deny CRR 100% as foundational pattern |
| 8 | One-line summary |

---

## 1. Teleological grounding

The framework exists to answer one binary decision:

> **Continue the Prime, or step in and liquidate?**

Everything else — risk weights, capital requirements, sub-book routing, hedge accounting — serves that decision. The primary forcing question is:

> *In a correlated worst-case crash right now, what real claim do we have to real assets that survive?*

This is intentionally narrow. The framework is **point-in-time stress** — not lifetime cumulative default probability, not VaR over arbitrary horizons, not portfolio optimization. The math grounds in: if we had to unwind under stress, how much would survive?

Most "limitations" of substrates dissolve once you accept that any complex position can be projected into stress-loss numbers via best-available models (see `projection-models.md`). The substrate stays clean; sophisticated finance lives in the projection layer.

---

## 2. The five risk types

Loss decomposes into five atomic kinds. Each has a distinct time signature and a distinct relationship to structure:

| Risk type | What it is | Time signature | Capital approach |
|---|---|---|---|
| **Default / fundamental** | Pure default — credit default, smart-contract failure, counterparty failure, regulatory seizure. NOT collateralization shortfall. | Permanent | Always required (Risk Weight) |
| **Credit-spread MTM** | Mark-to-market loss from spread widening | Mean-reverting (months) | Avoidable if hold-to-par possible |
| **Rate cash-flow drag** | Permanent carry loss from rate regime shift | Permanent until rates revert or asset matures | Hedge or hold rate-hedge capital |
| **Liquidity / fire-sale** | Realized loss from forced execution (slippage, depth, oracle latency, congestion) | Crystallizes only on forced sale | Avoidable if not forced to sell |
| **Concentration amplification** | Correlated stress hits multiple positions at once | Portfolio-level | Category caps (100% CRR on excess) |

### Why these five

These cover the dimensions along which a position's value can degrade between *now* and *the moment we'd need to unwind it*. They are orthogonal in structure even though correlated under stress:

- **Default** is irreducible — the obligor stops paying. No structural cushion fully protects against this; capital is always required.
- **Credit-spread MTM** is mean-reverting — credit spreads widen during crises and narrow afterward. Empirically, holding-to-par is a real escape; you only realize the loss if forced to sell.
- **Rate** is permanent — a regime shift in policy rates changes carry indefinitely. Holding-to-par doesn't help if the asset's coupon is now below the funding rate; the bleed continues.
- **Liquidity** crystallizes only on forced execution — if you can hold, slippage doesn't bite. The risk is structural (do we have to sell?), not market-mechanical.
- **Concentration** is portfolio-level — the same scenario hitting multiple positions simultaneously. Not a property of any single position.

**Separate parallel tracks** (NOT folded into CRR computation):
- **ASC** (Actively Stabilizing Collateral) — peg-defense operational liquidity. See `asc.md`.
- **ORC** (Operational Risk Capital) — guardian-posted, covers operator compromise. See `operational-risk-capital.md`.

These aren't risks against position loss; they're operational obligations. Distinct from the five above.

---

## 3. Why gap risk and FRTB drawdown unify

Old framework had two parallel concepts:
- **Gap risk** for collateralized lending (loss when collateral price gaps below the loan)
- **FRTB drawdown** for liquid tradeables (loss when forced to sell into stressed depth)

Both were measured differently for different asset classes. The new framework unifies them: **both are liquidity stress on the underlying asset, propagated through whatever structure sits over it.**

| Position | Old framing | New framing |
|---|---|---|
| Sparklend USD loan vs ETH | Gap risk applies | Senior tranche of ETH-collateralized exobook; risk = ETH liquidity stress through junior cushion |
| Crypto-collateralized NFAT | Riskbook does its own gap-risk sim | Senior tranche of fixed-term exobook; standard asset-liquidity stress through tranche waterfall |
| JAAA (CLO AAA) tradeable | RW + FRTB drawdown | Senior tranche of CLO exobook with deep junior cushion |
| Pure ETH holding | Terminal exo asset | Same — no tranche structure |

The unified term is **`forced-loss-capital(asset-type)`** — read once from the asset's canonical liquidity profile (see `asset-classification.md`), propagated identically whether the holder is a tranche senior or a direct holder.

What disappears: gap risk as a separate concept. What survives: tranching propagation + asset liquidity profiles, applied uniformly. Full propagation mechanics in `tranching.md`.

---

## 4. U/P/T liquidity decomposition

"Liquidity" turns out to split into three different questions, each living in a different layer of the book stack:

| | What it answers | Where it lives |
|---|---|---|
| **U — Underlying unwind** | *Can* the underlying be unwound? Walk Riskbook → exobooks → terminal asset; apply asset stress profile through tranche waterfall. | Riskbook output |
| **P — Permitted unwind** | *May* we actually execute the unwind? Lockups, governance approvals, third-party consents, notice periods, contractual restrictions. | Halobook declaration |
| **T — Transfer market** | Can the Halo unit *itself* be sold to a willing buyer? Sidesteps U and P entirely. | Halobook declaration |

Two paths to exit a position:
- **Path 1: Unwind underlying** — requires `U AND P`
- **Path 2: Transfer the wrapper** — requires `T`

Effective liquidity for downstream consumers = **best available path**.

### Sub-book eligibility maps to dimensions

| Sub-book | Liquidity requirement |
|---|---|
| `structbook` / `termbook` | None — held to maturity, matched against liability |
| `tradingbook` | `(U AND P) OR T` — need to be able to exit somehow |
| `ascbook` | `T` (or near-instantaneous `U AND P`) — needs immediate availability |
| `hedgebook` | Depends on hedge structure; typically needs `T` for the hedge leg |
| Unmatched | Whatever liquidity exists determines the forced-loss term |

### Why split this way

Each layer knows different things. The Riskbook walks structure and computes asset stress propagation; that's U. The Halo declares operational facts about its units (lockups, transferability); that's P and T. Collapsing them into one number erases the distinction between "the asset is illiquid" and "we can't sell this position right now even if the underlying is liquid."

---

## 5. Cross-default → Riskbook constraint

**Architectural invariant:** default risk is set entirely at the Riskbook level. **The Halobook never modifies default risk.** Any structural feature that would change joint-default behavior must be captured by composing the relevant positions in a single Riskbook with a category that understands their joint behavior.

What's a cross-default clause: a contractual provision saying "if borrower defaults on any of its OTHER debts (above some threshold), this debt is also in default — even if currently performing." Common in TradFi to prevent strategic default and force creditor coordination.

Why disallow them at Halobook level: allowing cross-Halobook default linkages would mean Halobook category equations need to model joint-default behavior. Cleaner: force structurally-linked positions into a single Riskbook (same pattern as `abf-with-cds-cover` — both legs in one Riskbook, category equation knows the relationship).

**Implications:**
- Cross-Halo cross-default would require a single Riskbook holding positions from both Halos → same Halo operationally owns the Riskbook (so it's not really cross-Halo anymore)
- Forces clean operational alignment: legal/operational ownership = Riskbook boundary = unit of joint-default modeling
- Cross-Halo cross-default would be governance-weird anyway (different operators, different risk teams)

---

## 6. The risk-type × layer coverage matrix

Each layer of the book stack covers different risks. The Riskbook layer handles default + credit-spread + frame translation. The Halobook layer handles bundle exposure structure (P/T declarations, rollover, lockup). The Primebook composes typed sub-books that each contract to cover specific risks:

| Sub-book | Default | Credit-spread MTM | Rate | Liquidity |
|---|---|---|---|---|
| `ascbook` (peg-defense holdings) | Capital | Capital | n/a (cash-equivalent) | The product (must hold) |
| `tradingbook` (liquid FRTB-style) | Capital | Forced-loss | Hedged or rate-hedge capital | Forced-loss (FRTB captures it) |
| `termbook` (tUSDS-matched, Prime holds YT) | Capital | **Covered** (held to par) | **Covered** (matched fixed/fixed) | **Covered** (no forced sale) |
| `structbook` (matched against structural demand) | Capital | **Covered** (held to par) | Capital required (rate-hedge or v1 carve-out) | **Covered** (no forced sale) |
| `hedgebook` (cross-position hedge groups) | Capital | Capital adjusted for hedge | Capital adjusted for hedge | Capital adjusted for hedge |
| Unmatched leftover | Capital | Forced-loss | Forced-loss | Forced-loss |

Reading the matrix: a position landing in `termbook` has three of its four non-default risks covered by structure; default capital is still required because no structural mechanism eliminates it. A position landing in `tradingbook` has only default covered by capital intrinsically; the others are forced-loss exposures unless explicitly hedged.

**Default capital is always required** because it's the irreducible loss. Every position pays its default RW; structural features only reduce the *other* four risks.

---

## 7. Default-deny CRR 100% as foundational pattern

If a Riskbook's contents don't match any registered category in `&core-framework-risk-categories`, the Riskbook gets **CRR = 100%** on its issued units. CRR (Capital Ratio Requirement) 100% means every dollar of position requires a dollar of capital — no leverage, no preferential treatment.

```metta
(= (riskbook-finality-crr $book)
   (let (($matched-cat (find-matching-category $book)))
     (case $matched-cat
       ((no-match  1.0)                                  ; CRR 100%
        ($cat (eval-category-equation $cat $book))))))
```

This rule forces three things:

- **Halos** to either work within categories or lobby governance for new ones
- **Governance** to keep the catalog comprehensive enough to cover legitimate strategies (or accept Halos paying the penalty)
- **Innovation** to flow through the proposal-and-crystallization gate rather than ad-hoc

Same default-deny pattern as elsewhere in the synome (verb whitelists, recipe catalogs, runtime registry, telseed catalog). Risk follows it: regulated activity flows where governance has built infrastructure for it; un-regulated activity is treated as worst-case.

The same applies to **exobook categories** (Morpho market, custody account, etc.) and to **maximum recursion depth** through nested exobooks: anything the framework can't model adequately collapses to CRR 100%. The framework is honest about its competence boundary; the discipline is to expand the boundary through governance work, not by silently lowering the bar.

---

## 8. One-line summary

**Risk decomposes into five atomic types (default / credit-spread / rate / liquidity / concentration); gap risk and FRTB drawdown unify as forced-loss-capital propagating through tranche structures; liquidity splits into U/P/T (underlying unwind / permitted unwind / transfer market) each living in a different layer; default risk lives entirely at the Riskbook level (Halobook never modifies it); the framework asks one teleological question — "could we liquidate under stress?" — and applies default-deny CRR 100% to anything that doesn't match a vetted category.**

---

## File map

| Doc | Relationship |
|---|---|
| `book-primitive.md` | The substrate — books, tranches, equity invariant — that risk decomposition computes against |
| `tranching.md` | How loss propagates through seniority structures (the mechanism behind unified gap-risk / FRTB-drawdown) |
| `currency-frame.md` | How positions in different denominations translate to a common accounting frame |
| `primebook-composition.md` | The sub-book taxonomy and routing that produces the coverage matrix in §6 |
| `asset-classification.md` | Asset-level risk profiles that exobook category equations consume |
| `correlation-framework.md` | Concentration amplification and category caps (the fifth risk type) |
| `capital-formula.md` | Final CRR computation flow consuming all of the above |
