# Halobook Layer

**Status:** Draft (Phase 2 layer doc, 2026-05-05)

The Halobook is the **bundle exposure structure** layer. It declares the operational facts that affect how per-position risks compound or aggregate over the bundle's lifetime — rollovers, lockups, transferability, embedded options. The Halobook does NOT modify default risk (per cross-default → Riskbook constraint).

Companion to:
- `book-primitive.md` — Halobook is one specialization of the 6-tuple book
- `risk-decomposition.md` — U/P/T liquidity decomposition (Halobook owns P and T declarations)
- `riskbook-layer.md` — what sits below; the unit of regulation
- `primebook-composition.md` — what sits above; sub-book composition

---

## TL;DR

A Halobook:
- **Aggregates Riskbook units** from all Riskbooks owned by the Halo
- **Declares P and T** — Permitted unwind (lockups, governance approvals) and Transfer market (transferability) for its issued units
- **Captures bundle exposure structure** — how per-position risks compound over the bundle's lifetime via rollover, lockup, embedded options, etc.
- **Does NOT modify default risk** — that lives at the Riskbook layer entirely
- **Issues a single Halobook unit upward** to the Primebook

The Halobook category declaration shapes how upstream books (Primebook, sub-books) interpret the bundle. It's *the operational facts about the bundle*, not a re-derivation of underlying risk.

---

## Section map

| § | Topic |
|---|---|
| 1 | The Halobook's role: bundle exposure structure |
| 2 | P and T declarations |
| 3 | What Halobook categories CAN affect |
| 4 | What Halobook categories CANNOT affect |
| 5 | Aggregation across Riskbooks: no netting |
| 6 | Halobook unit issuance |
| 7 | The v1 Halobook category catalog |
| 8 | One-line summary |

---

## 1. The Halobook's role: bundle exposure structure

Earlier framing treated the Halobook as "applies a liquidity downgrade to Riskbook output." That was too narrow. Cleaner framing:

> The Halobook category declares the bundle's **exposure structure** — what happens to per-position risks over the bundle's lifetime, given the bundle's terms (rollovers, lockups, transferability, embedded options, etc.). This affects ANY risk type via the exposure structure, not just liquidity.

Architectural division of labor:
- **Riskbook output:** per-position snapshot risk vector at one moment (default, spread-sensitivity, rate-duration, U)
- **Halobook category:** declares exposure structure — how those per-position risks compound/aggregate over the bundle lifetime
- **Halobook output:** bundle-level risk vector that's the composition of per-position risks × exposure structure

For v1 crypto-lending: NFATs are fixed-term, no rollover/options/convertibles. Per-period risks pass through unchanged. Halobook category = `nfat-crypto-lending-fixed-term` (just declares lockup + null-transferability).

---

## 2. P and T declarations

The U/P/T liquidity decomposition (per `risk-decomposition.md` §4) places **P** (Permitted unwind) and **T** (Transfer market) at the Halobook layer:

| Dimension | Question | Halobook declaration |
|---|---|---|
| **P — Permitted unwind** | *May* we actually execute the unwind? | `(permitted-unwind ...)` |
| **T — Transfer market** | Can the Halo unit *itself* be sold to a willing buyer? | `(transfer-market ...)` |

**U** (Underlying unwind) is computed at the Riskbook layer — it walks structure and applies asset stress. The Halobook doesn't recompute U; it declares the operational facts that constrain whether U is actually exercisable.

```metta
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

Two paths to exit a position:
- **Path 1: Unwind underlying** — requires `U AND P` (Riskbook says U is feasible AND Halobook declares P permits)
- **Path 2: Transfer the wrapper** — requires `T` (Halobook declares the unit itself can be sold)

The downstream sub-book router (per `primebook-composition.md`) reads these declarations to determine where the Halobook unit can land — `tradingbook` requires `(U AND P) OR T`; `structbook`/`termbook` require neither (held to maturity).

---

## 3. What Halobook categories CAN affect

A Halobook category declaration shapes upstream consumption in several ways. The structural feature dimension affects the risk vector:

| Halobook structural feature | Spread | Rate | Liquidity |
|---|---|---|---|
| Rollover (any flavor) | Compounds spread duration if held to par | Compounds rate duration unless reset | Worsens P |
| Lockup, no transfer | Same | Same | Worsens P |
| Prepayment option (issuer-held) | Negative convexity | Negative convexity | Same |
| Embedded options | Variable, depends on option | Variable | Variable |
| Open transferability | Same | Same | Improves T |

The Halobook layer is where these features get declared and propagated upward. The category equation (when category-match succeeds) describes how the risk vector flows through.

---

## 4. What Halobook categories CANNOT affect

> **Default risk is set entirely at the Riskbook level. The Halobook NEVER modifies default risk.**

This is the architectural invariant from `risk-decomposition.md` §5 and `riskbook-layer.md` §3. Any structural feature that would change joint-default behavior (cross-default clauses, joint-and-several obligations, mutual subordination across positions) must be captured by composing the relevant positions in a single Riskbook with a category that understands their joint behavior.

What this rules out at the Halobook layer:
- Cross-Halobook default linkages (joint-and-several obligations spanning Halos)
- Halobook-level credit enhancement
- Halobook-level subordination structures across Riskbooks

If a strategy genuinely requires joint-default modeling, the legally-linked positions must live in one Riskbook with one Halo operationally owning them. This forces clean operational alignment.

---

## 5. Aggregation across Riskbooks: no netting

A Halobook holds Riskbook units from all Riskbooks owned by the Halo. Aggregation is **pure summation**:

```metta
(= (halobook-rw $halobook $treatment)
   (sum-over (held-riskbook-units $halobook)
      (lambda ($u)
         (* (notional-held $halobook $u)
            (riskbook-rw (issuer-of $u) $treatment)))))
```

**No cross-Riskbook netting.** Two Riskbooks suffering in the same crash (likely — both have credit-cycle exposure) contribute their losses additively, not net. The Halo doesn't get a netting benefit across Riskbooks because bankruptcy-remoteness forbids it (per `riskbook-layer.md` §6).

**No cross-Riskbook hedging.** A CDS in one Riskbook protecting an ABF in another Riskbook gets no recognition at the Halobook layer. To get hedge relief, the legs must be in the same Riskbook (per `riskbook-layer.md` §5) or in the Hedgebook (per `hedgebook.md`).

This is the architectural cost of bankruptcy remoteness: real capital cost in exchange for structural protection.

---

## 6. Halobook unit issuance

The Halobook issues a single endo unit upward to the Primebook. This unit carries:

| Property | What it specifies |
|---|---|
| **Notional** | Aggregate of held Riskbook unit notionals (in the Halobook's frame) |
| **Risk vector** | Composition of per-Riskbook risk vectors × Halobook exposure structure |
| **U declaration** | Computed from underlying Riskbook structure |
| **P declaration** | From Halobook category (lockup, approval-required, notice-period, etc.) |
| **T declaration** | From Halobook category (transferability, market-depth) |
| **Frame** | Inherited from the Generator (USD for v1) |

```metta
;; ──── &entity-halo-spark-credit-halobook ────
(book-type halobook)
(book-category nfat-crypto-lending-fixed-term)
(parent-primebook spark-primebook)
(sub-riskbook spark-credit-riskbook-A &entity-halo-spark-credit-riskbook-A)
(sub-riskbook spark-credit-riskbook-B &entity-halo-spark-credit-riskbook-B)
(holds (endo-unit u-rb-a-bond) 1000000)
(holds (endo-unit u-rb-b-bond) 2000000)
(issues (endo-unit u-hb-bond) (notional 3000000))
(permitted-unwind u-hb-bond (lockup-until-maturity) (early-unwind-on-health-factor-breach))
(transfer-market u-hb-bond (transferable False))
```

The Primebook sub-book router consumes the U/P/T declarations to decide which sub-book the unit lands in (per `primebook-composition.md`).

---

## 7. The v1 Halobook category catalog

V1 has a minimal Halobook catalog. The crypto-collateralized lending test uses one category:

```metta
(book-category-def nfat-crypto-lending-fixed-term
   (frame usd)
   (composition-constraints
      (units-pointing-to-fixed-term-crypto-collateralized-riskbooks))
   (exposure-structure
      (rollover none)
      (lockup until-maturity)
      (transferability none)
      (per-period-risk-passthrough true))
   (permitted-unwind-decl
      (lockup-until-maturity true)
      (early-unwind-on-health-factor-breach true))
   (transfer-market-decl
      (transferable false)))
```

V1 carve-outs:
- **Halobook category as passthrough.** No liquidity adjustment; per-period risks pass through unchanged because NFATs have no rollover/options/convertibles.
- **Single category.** Other Halobook categories (open-ended trading, rolling credit, structured derivatives) deferred to v2+.
- **No transferability.** Secondary markets for NFATs are deferred. P=lockup-until-maturity, T=null.

The future catalog grows over time as Halos propose new structures and governance crystallizes them. Each new category is a small governance act that includes assigning composition constraints, exposure structure, and U/P/T declarations.

---

## 8. One-line summary

**The Halobook declares the bundle exposure structure (rollover, lockup, transferability, embedded options) and owns the P + T declarations from the U/P/T liquidity decomposition; it aggregates Riskbook units without netting (bankruptcy-remoteness across Riskbooks) and never modifies default risk (which lives entirely at the Riskbook layer); the Halobook category catalog is governance-paced and grows as new bundle structures get crystallized.**

---

## File map

| Doc | Relationship |
|---|---|
| `book-primitive.md` | Halobook is one specialization of the 6-tuple book |
| `risk-decomposition.md` | U/P/T liquidity decomposition; Halobook owns P + T |
| `riskbook-layer.md` | The layer below; unit of regulation; default risk lives there |
| `primebook-composition.md` | The layer above; sub-books read U/P/T to route the Halobook unit |
| `currency-frame.md` | Halobook inherits Generator's frame; doesn't translate |
| `tranching.md` | Halobook holds Riskbook units which themselves may hold tranche claims |
| `examples.md` | Worked v1 test uses `nfat-crypto-lending-fixed-term` |
