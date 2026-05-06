# Book Primitive

**Status:** Draft (Phase 2 conceptual core, 2026-05-05)

The substrate of the risk framework. Defines what a book IS — the universal 6-tuple shape every book follows, the equity invariant that makes books well-defined, and the rules that turn books into financial state machines.

Companion to:
- `risk-decomposition.md` — what kinds of loss the substrate computes
- `tranching.md` — how the tranches dimension of the 6-tuple actually works
- `currency-frame.md` — how the frame dimension works

---

## TL;DR

A book is a 6-tuple:

```
Book = (assets, tranches, equity-tranche, rules, state, frame)
```

Every book has a designated equity tranche (most-junior, first-loss). Books are solvent iff equity > 0. When equity hits zero, an unwind procedure triggers. **The equity invariant is universal** — exobooks, riskbooks, halobooks, primebooks, the Generator's Genbook all follow the same shape.

Rules turn books into financial state machines, structurally identical to smart contracts. Real-time equity recomputation is the load-bearing requirement: every book class must have an equity-feed mechanism documented at onboarding.

---

## Section map

| § | Topic |
|---|---|
| 1 | The 6-tuple |
| 2 | The equity invariant |
| 3 | Tranches generalize from "fixed claim" to "rule-bearing claim" |
| 4 | Rules and state — books as financial state machines |
| 5 | Real-time recomputation as load-bearing infrastructure |
| 6 | Bankruptcy remoteness through equity boundaries |
| 7 | One-line summary |

---

## 1. The 6-tuple

```
Book = (assets, tranches, equity-tranche, rules, state, frame)
```

| Component | What it is |
|---|---|
| **Assets** | Exo assets (terminal — ETH, USDC, T-bills) plus units of other books on the asset side |
| **Tranches** | Ordered claims with seniority (loss-absorption order); claim amount may be rule-determined, not just fixed notional |
| **Equity tranche** | The designated residual / first-loss absorber; universal invariant; always exactly one |
| **Rules** | Deterministic state-transition functions ("when X, do Y; at time T, do Z; if oracle V, evaluate W") |
| **State** | Temporal, path-dependent, or oracle-dependent values that rules read and update |
| **Frame** | The unit of account in which the book's numbers are measured (USD, EUR, BTC) |

This generalizes the older "balanced ledger" definition of a book by adding rules (computational dynamics), state (temporal context), and an explicit frame (currency unit). The first two — `assets` and `tranches` — were already present in some form. The other four are new structural requirements.

What this gives:
- **Conditional payoffs** (options, CDS, insurance) express naturally as rules
- **Time evolution** (interest accrual, expiry, liquidation triggers) is rule + state, not a separate mechanism
- **Path dependence** (barrier options, Asian averaging, accumulators) just needs more state
- **Currency consistency** (everything in the book is denominated in `frame`) is structurally enforced, not a convention

---

## 2. The equity invariant

> **Every book has a designated equity tranche, always the most-junior, first-loss absorber. The book is solvent iff equity > 0. When equity hits zero, an unwind procedure triggers.**

This is universal. Every book type in the synome has it:

| Book type | Equity holder | Unwind mechanism |
|---|---|---|
| Exobook (overcollateralized loan) | External borrower | Protocol-level liquidation |
| Exobook (CLO etc.) | Equity-tranche holder | Per the structure's contractual mechanics — synome observes |
| Riskbook | The Halo (operator) | Governance/operational wind-down |
| Halobook | The Halo | Same |
| Primebook | The Prime | Same |
| Genbook | Sky (protocol surplus) | Drawdown of Sky reserves before USDS itself is at risk |

The equity tranche is always **most-junior** by construction. Loss waterfalls absorb to equity first; when equity is exhausted, loss eats into the next-junior tranche, and the book triggers unwind.

### Why this is structural, not bookkeeping

The universal balance-sheet identity (assets − liabilities = equity) is well-known. What's structurally enforced here is that **every book is required to know its equity in real-time**, that **the equity is held by exactly one named entity**, and that **hitting zero triggers a defined unwind procedure**. There's no book without an equity tranche; there's no book without an unwind mechanism. The invariant gives every book a coherent failure mode.

---

## 3. Tranches generalize from "fixed claim" to "rule-bearing claim"

In simple structured finance, a tranche has a fixed notional and a fixed seniority position. The new framework keeps seniority but **the claim amount may be rule-determined**:

```metta
(book-tranche my-bond
   (seniority 1)
   (holder spark-halo)
   (notional 1000000)                                    ; static
   (denom usd))

(book-tranche callable-tranche
   (seniority 1)
   (holder some-investor)
   (notional-rule (callable-payoff $strike $expiry))     ; rule-determined
   (denom usd))
```

Seniority still defines loss absorption order. The *amount* of the claim can depend on rules + state.

This handles:
- Callable bonds (issuer can call away the bond at par)
- Conversion options (convertible bond — claim amount depends on whether converted)
- Step-up coupons (claim grows over time per a defined rule)
- Triggered subordination (junior tranche becomes senior under specific conditions)

The seniority order is fixed at book creation; the claim amounts within that order can be arbitrary deterministic functions. See `tranching.md` for the full waterfall semantics and exoasset/exoliab vocabulary.

---

## 4. Rules and state — books as financial state machines

Rules attached to books make them **financial state machines** — structurally identical to smart contracts (state + rules + transitions) but with the extra structure (asset/liability/seniority/equity invariant) that makes risk reasoning natural.

Examples of rule shapes:

```metta
;; Time-triggered: at expiry, deliver underlying
(book-rule expiry-settlement
   (when (>= now (book-state $book expiry)))
   (do (transfer-underlying-to senior-tranche)))

;; Oracle-triggered: liquidation on health-factor breach
(book-rule liquidation-trigger
   (when (< (oracle-derived-health $book) (book-state $book liq-threshold)))
   (do (liquidate-collateral) (settle-tranches)))

;; Path-dependent: accumulate interest
(book-rule interest-accrual
   (when (tick-elapsed))
   (do (update-state interest-accrued (+ prior-accrual (per-tick-rate)))))
```

Rules are deterministic. State is the persistent context they read and write. Together, they let books express any contract that can be encoded as a state machine — which is most of structured finance.

### Where the calculation actually lives

Rules execute in synserv-resolved in-space computation (per `../macrosynomics/beacon-framework.md` §4). Beacons push input atoms (chain reads, oracle prices, attestations) into book spaces; synserv keeps each book's derived state (equity, CRR, breach flags) consistent with current input atoms in real time. The rule is synart code; synserv runs it.

This makes rules **fully verifiable**: any warden can re-derive the book's state by reading the same input atoms and applying the same rule. The calculation is not opaque off-loop compute; it's substrate-resolved synlang.

---

## 5. Real-time recomputation as load-bearing infrastructure

> Every book must always know its current equity in real-time.

This drives data infrastructure requirements at every book type:

| Book type | Equity feed mechanism |
|---|---|
| Internal books (Riskbook, Halobook, Primebook, Genbook) | Computed from synart state — synserv re-derives equity from current input atoms |
| On-chain exobooks (Morpho, Sparklend, etc.) | Endoscrapers compute equity from chain reads |
| Off-chain exobooks (custody, ABF, real-world receivables) | Attestor-published numbers (signed, with slashing surface for proven-false attestations) |
| Mixed-chain exobooks | Combination — endoscrapers for the on-chain portions, attestors for the off-chain portions |

Each new asset class brought into the system requires a documented equity-feed mechanism at onboarding. This is the operational price of the equity invariant: it's not enough to *say* every book has equity; the system has to *know* it continuously.

### Why real-time matters

Assets fluctuate (especially non-pegged ETH/BTC). Liabilities accrue (interest, time-decay). Equity = assets − liabilities is a moving quantity. If the system only knew equity at settlement boundaries, it couldn't:
- Trigger unwinds promptly when equity approaches zero
- Compute current CRR for upstream books that hold this book's units
- Detect proximity-to-breach early (before crisis)
- Verify that beacon-claimed states match observable reality

Real-time equity is the foundation everything upstream rests on.

---

## 6. Bankruptcy remoteness through equity boundaries

The equity invariant gives bankruptcy remoteness a precise operational meaning:

> An unwind of one book cannot propagate loss upward past its equity holder. Independent equity = independent unwind boundary.

When a book's equity is exhausted and the book unwinds:
- Senior tranches recover whatever the assets cover
- Junior tranches absorb proportional losses up to their notional
- The equity holder has been wiped out (by definition — that's what triggered the unwind)
- The shortfall (if any) is borne by the equity holder, not propagated to upstream consumers

For nested books: if Halobook A holds a Riskbook unit, and that Riskbook hits its equity floor, the Halobook unit's value falls but the Halobook itself doesn't necessarily unwind — the Halobook's own equity holder absorbs the loss first.

Bankruptcy remoteness sits at the **Riskbook level** in the Sky stack: across Riskbooks, fates are unlinked, so no netting across boundaries. Within a Riskbook, positions share fate — they're inside the unit of linked default. Halobook and Primebook are pure aggregators above this boundary.

---

## 7. One-line summary

**Every book is a 6-tuple (assets, tranches, equity-tranche, rules, state, frame); every book has a designated equity tranche that absorbs loss first and triggers unwind when exhausted; rules + state turn books into financial state machines that synserv runs in-space; real-time equity recomputation is the operational price of the equity invariant; bankruptcy remoteness lives at the Riskbook level — within a Riskbook, fates are linked; across Riskbooks, equity boundaries are independent unwind boundaries.**

---

## File map

| Doc | Relationship |
|---|---|
| `risk-decomposition.md` | The risk types that this substrate computes against |
| `tranching.md` | The tranches dimension — seniority, waterfall, exoassets/exoliabs |
| `currency-frame.md` | The frame dimension — units of account, instrument-vs-frame |
| `riskbook-layer.md` | The unit of regulation; where matched categories produce CRR |
| `halobook-layer.md` | Bundle exposure structure built on top of the book primitive |
| `primebook-composition.md` | Composition of typed sub-books; aggregation across Halobooks |
| `../noemar-synlang/risk-framework.md` | Existing four-book taxonomy; pending Phase-2 trim once these new docs land |
