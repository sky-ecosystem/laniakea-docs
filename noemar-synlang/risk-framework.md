# Risk Framework — Synlang Reference

**Status:** Trimmed (Phase 5, 2026-05-05)

The synlang-flavored complement to the canonical conceptual docs in [`../risk-framework/`](../risk-framework/README.md). This doc covers atom shapes, equation forms, four-tier resolution as synlang code, and worked examples. **Conceptual content lives in `../risk-framework/`** — this is the technical reference for what the atoms and equations actually look like.

> **Major rewrite history.** The previous version of this doc (62KB, ~1612 lines) was load-bearing for the four-book taxonomy and the category framework as conceptual treatment. That conceptual content has been promoted to canonical docs in `../risk-framework/`:
> - [`risk-decomposition.md`](../risk-framework/risk-decomposition.md) — five risk types, U/P/T, gap-risk unification, default-deny CRR 100%
> - [`book-primitive.md`](../risk-framework/book-primitive.md) — 6-tuple book, equity invariant, rules + state
> - [`tranching.md`](../risk-framework/tranching.md) — exoassets/exoliabs, waterfall, gap-risk unification
> - [`currency-frame.md`](../risk-framework/currency-frame.md) — frame vs instrument, Riskbook as translation layer
> - [`riskbook-layer.md`](../risk-framework/riskbook-layer.md), [`halobook-layer.md`](../risk-framework/halobook-layer.md), [`primebook-composition.md`](../risk-framework/primebook-composition.md), [`hedgebook.md`](../risk-framework/hedgebook.md), [`projection-models.md`](../risk-framework/projection-models.md) — layer architecture
> 
> Read those first for conceptual context. This doc is the synlang-side reference for what the atoms look like in practice.

Companion to:
- [`topology.md`](topology.md) — Space layout: `&core-framework-risk-*` and `&core-registry-exo-book` live here
- [`synlang-patterns.md`](synlang-patterns.md) — the conservation-network framing (books as nodes, units as edges)
- [`runtime.md`](runtime.md) — how exo book state gets pushed through the gate
- [`settlement-cycle-example.md`](settlement-cycle-example.md) — worked settlement (uses old state-based CRR; pending update)

---

## TL;DR

The risk model rests on these primitives (canonical treatment in `../risk-framework/`):

- **Books come in four kinds**: Primebook, Halobook, Riskbook, Exobook (plus the Generator's Genbook above)
- **Riskbook is the unit of regulation** — must match a registered category or get CRR 100% (default-deny)
- **Equations are stress simulations**, not static formulas — evaluated against a library of governance-curated stress scenarios
- **Four-tier resolution hierarchy** — math → simulation → heuristics → max-risk, falling through on failure
- **Both M2M and HTM** propagate continuously up the stack; Primebook selects per-position via sub-book routing
- **In-space calculation** — synserv runs category equations against current input atoms in real time

This doc shows the **synlang shapes** for all of the above.

---

## Section map

| § | Topic |
|---|---|
| 1 | Atom shapes for the four-book taxonomy |
| 2 | Category atom shapes (three types) |
| 3 | Riskbook composition constraints in synlang |
| 4 | Stress simulation patterns |
| 5 | Four-tier resolution as synlang code |
| 6 | Loop and recursion handling in synlang |
| 7 | Default-deny CRR-100% mechanism |
| 8 | Worked examples |
| 9 | Cross-doc invariants |

---

## 1. Atom shapes for the four-book taxonomy

Each book type has specific atoms identifying its role in the stack. Books live in their entity's entart per [`topology.md`](topology.md).

### Primebook

```metta
;; ──── &entity-prime-spark-primebook ────
(book-type primebook)
(parent-generator usge-generator-interface)
(sub-halobook spark-credit-halobook ...)
(sub-halobook spark-trade-halobook  ...)
(holds (endo-unit u-hb-credit-bond) 3000000)
(holds (endo-unit u-hb-trade-bond)  2000000)

;; Sub-book composition (per ../risk-framework/primebook-composition.md)
(sub-book spark-prime ascbook       ...)
(sub-book spark-prime tradingbook   ...)
(sub-book spark-prime termbook      ...)
(sub-book spark-prime structbook    ...)        ; active in v1 test
(sub-book spark-prime hedgebook     ...)
(sub-book spark-prime unmatched     ...)
```

### Halobook

```metta
;; ──── &entity-halo-spark-credit-halobook ────
(book-type halobook)
(book-category nfat-crypto-lending-fixed-term)
(parent-primebook spark-primebook)
(sub-riskbook spark-credit-riskbook-A &entity-halo-spark-credit-riskbook-A)
(sub-riskbook spark-credit-riskbook-B &entity-halo-spark-credit-riskbook-B)
(holds (endo-unit u-rb-a-bond) 1000000)
(holds (endo-unit u-rb-b-bond) 2000000)
(issues (endo-unit u-hb-credit-bond) (notional 3000000))

;; Halobook category P + T declarations (per ../risk-framework/halobook-layer.md)
(permitted-unwind u-hb-credit-bond
   (lockup-until-maturity true)
   (early-unwind-on-health-factor-breach true))
(transfer-market u-hb-credit-bond (transferable false))
```

### Riskbook

```metta
;; ──── &entity-halo-spark-credit-riskbook-A ────
(book-type riskbook)
(book-category abf-with-cds-cover)
(parent-halobook spark-credit-halobook)

(holds (exo-unit u-001) abf-deal-X 1000000)
(holds (exo-unit u-002) cds-on-abf-deal-X 950000)
(issues (endo-unit u-rb-a-bond) (notional 1000000))

;; Frame inheritance from Generator (per ../risk-framework/currency-frame.md)
(book-frame usd)
```

### Exobook

```metta
;; ──── &core-registry-exo-book entry ────
(exo-book sparklend-eth-pool-001
   (category overcollateralized-eth-lending))

(exo-book-asset sparklend-eth-pool-001 eth 1000)         ; 1000 ETH

(exo-book-tranche sparklend-eth-pool-001
   (seniority 0)
   (holder borrower-XYZ)                                  ; exoliab
   (notional 750000)
   (denom usd))

(exo-book-tranche sparklend-eth-pool-001
   (seniority 1)
   (holder spark-halo-A)
   (notional 1750000)
   (denom usd))
```

The `seniority 0` tranche is the equity tranche per [`book-primitive.md`](../risk-framework/book-primitive.md) §2.

---

## 2. Category atom shapes (three types)

All categories live in `&core-framework-risk-categories`. They share a common shape but apply at different levels.

### Common shape

```metta
(risk-category-def $name
   (level <exo-asset | exobook | riskbook>)
   (variables [<named inputs needed at evaluation>])
   (equation-m2m  <synlang form taking variables → CRR>)
   (equation-htm  <synlang form taking variables → CRR>)
   (resolution-tier <math | simulation | heuristic | max-risk>)
   (composition-constraints <only for riskbook level>)
   (description "..."))
```

### Type 1: Exo asset categories (terminal)

```metta
(risk-category-def eth
   (level exo-asset)
   (variables [])
   (equation-m2m (constant 0.25))
   (equation-htm (constant 0.20))
   (resolution-tier math)
   (description "Native ETH on Ethereum; market liquidation recourse"))

(risk-category-def usdc
   (level exo-asset)
   (variables [])
   (equation-m2m (constant 0.05))
   (equation-htm (constant 0.04))
   (resolution-tier math))

(risk-category-def treasury-bill-direct
   (level exo-asset)
   (variables [])
   (equation-m2m (constant 0.02))
   (equation-htm (constant 0.005))
   (resolution-tier math))
```

M2M is higher than HTM for nearly all assets — mark-to-market sensitivity exposes more volatility than buying-and-holding.

### Type 2: Exobook categories (infrastructure)

These represent external structures the synome monitors. Equations walk into the Exobook's own assets/liabilities.

```metta
(risk-category-def morpho-market
   (level exobook)
   (variables [(state $book) (collateralization-data $cdata) (liquidation-rules $rules)])
   (equation-m2m
      (simulate-loss-under-scenarios m2m-scenarios
         (lambda ($scenario)
            (let* (($collateral-after (apply-stress $cdata $scenario))
                   ($debt-survives    (apply-debt-stress $book $scenario))
                   ($recovery (compute-recovery $collateral-after $debt-survives $rules)))
              (- 1.0 (/ $recovery (debt-of $book)))))
         (combiner take-worst)))
   (resolution-tier simulation))

(risk-category-def morpho-vault
   (level exobook)
   (variables [(state $book) (allocations $allocs)])
   (equation-m2m
      ;; iterate child markets, compute their risks under same scenario, weighted by allocation
      ...)
   (resolution-tier simulation))

(risk-category-def custody-major
   (level exobook)
   (variables [(custodian $c) (counterparty-rating $cr) (jurisdiction $j)])
   (equation-m2m ...)
   (resolution-tier simulation))
```

### Type 3: Riskbook categories (the load-bearing economic citizens)

```metta
(risk-category-def abf-with-cds-cover
   (level riskbook)
   (variables [(coverage-ratio $cr) (cds-counterparty-rating $cprat)])
   (composition-constraints
      (and (count-of (units-where (asset-class abf-claim)) = 1)
           (count-of (units-where (asset-class cds-cover))  = 1)
           (forall $cds (units-where (asset-class cds-cover))
                       (cds-references-credit-asset-in-same-book $cds))
           (>= (cds-notional / abf-notional) 0.90)))
   (equation-m2m
      (simulate-across-scenarios m2m-scenarios
         (lambda ($scenario)
            (let* (($abf-default-prob (apply-credit-stress $scenario))
                   ($cds-effective-payout
                      (* (cds-notional)
                         (cds-counterparty-survival-prob $cprat $scenario)))
                   ($expected-loss
                      (* $abf-default-prob
                         (max 0 (- (abf-notional) $cds-effective-payout)))))
              (/ $expected-loss (abf-notional))))
         (combiner take-worst)))
   (resolution-tier simulation))

(risk-category-def pure-eth-holding
   (level riskbook)
   (variables [])
   (composition-constraints
      (and (count-of (asset-class eth) >= 1)
           (count-of (asset-class != eth) = 0)))
   (equation-m2m (* (sum-of-notionals) (lookup-rw eth m2m)))
   (equation-htm (* (sum-of-notionals) (lookup-rw eth htm)))
   (resolution-tier math))

(risk-category-def crypto-collateralized-USD-lending
   (level riskbook)
   (frame usd)
   (composition-constraints
      (and (single-senior-tranche-positions)
           (asset-class-in (eth btc stETH))
           (denom-in (usdc usdt))))
   (equation-m2m
      (sum-over (held-senior-tranches)
         (lambda ($pos)
            (let* (($asset-stress  (asset-stress-profile (collateral-of $pos)))
                   ($denom-depeg   (depeg-stress-profile (denom-of $pos)))
                   ($junior-cushion (junior-tranche-size (exobook-of $pos))))
              (simulate-across-scenarios m2m-scenarios
                (lambda ($s)
                  (+ (max 0 (- (apply-scenario $s $asset-stress) $junior-cushion))
                     (apply-scenario $s $denom-depeg))))))))
   (resolution-tier simulation))
```

The category catalog is governance-curated (per [`riskbook-layer.md`](../risk-framework/riskbook-layer.md) §7).

---

## 3. Riskbook composition constraints in synlang

A Riskbook category's `composition-constraints` clause is a synlang predicate over the Riskbook's contents. For category match, it must evaluate to True.

```metta
(= (find-matching-category $book)
   (case (collapse
            (match &core-framework-risk-categories
               (and (risk-category-def $cat (level riskbook) ...)
                    (eval-composition-constraint $cat $book))
               $cat))
     ((empty       no-match)
      (($cat) $cat)                                       ; exactly one match
      (($cat1 $cat2 ...) (Error multiple-categories-match $book)))))
```

If multiple categories match, that's a category-design error: categories should be disjoint by composition. Governance is responsible for keeping the catalog clean.

Default-deny is enforced by `no-match`:

```metta
(= (riskbook-finality-rw $book $treatment)
   (let (($cat (find-matching-category $book)))
     (case $cat
       ((no-match (notional-of-issued-units $book))         ; CRR = 100%
        ($c (* (notional-of-issued-units $book)
               (eval-equation $c $book $treatment)))))))
```

---

## 4. Stress simulation patterns

Stress scenarios live in `&core-framework-stress-scenarios`:

```metta
(stress-scenario-def severe-correlated-crash
   (description "2008-style coordinated crash across crypto + traditional")
   (params
      (eth-drop -0.55)
      (btc-drop -0.45)
      (stable-major-depeg-prob 0.05)
      (credit-spreads-widen-bps 800)
      (correlation-uplift 1.6)
      (defi-protocol-risk-uplift 1.8)
      (custody-counterparty-default-prob 0.02)
      (real-estate-residential-drop -0.30)
      ;; ... full vector
      ))

(stress-scenario-def credit-crisis
   (description "Credit-cycle-led downturn; less crypto-correlated")
   (params ...))

(stress-scenario-def stable-conditions
   (description "Base case; no major stress")
   (params (all-stress-uplift 0.0)))
```

Categories declare which scenarios their equations apply:

```metta
(risk-category-def abf-with-cds-cover
   ...
   (m2m-scenarios [severe-correlated-crash credit-crisis liquidity-crisis])
   (htm-scenarios [severe-correlated-crash credit-crisis])
   ...)
```

The simulation pattern:

```metta
(= (simulate-across-scenarios $scenarios $loss-fn $combiner)
   (let (($losses (collapse (map $loss-fn $scenarios))))
     (apply-combiner $combiner $losses)))

(= (apply-combiner $combiner $losses)
   (case $combiner
     ((take-worst                  (max-of $losses))
      (probability-weighted-mean   (weighted-mean $losses))
      ...)))
```

---

## 5. Four-tier resolution as synlang code

Each category equation declares its `resolution-tier`. The framework attempts the highest tier first; falls through on failure.

```metta
(= (eval-equation $cat $book $treatment)
   (case (resolution-tier-of $cat)
     ((math       (eval-equation-tier1 $cat $book $treatment))
      (simulation (eval-equation-tier2 $cat $book $treatment))
      (heuristic  (eval-equation-tier3 $cat $book $treatment))
      (max-risk   (eval-equation-tier4 $cat $book $treatment)))))
```

### Tier 1 (math) sketch

```metta
(= (eval-equation-tier1 $cat $book $treatment)
   (case (analytic-form-of $cat $treatment)
     ((closed-form (apply-formula $cat $book))
      (linear-system (solve-linear-system $cat $book))
      (none Error))))
```

### Tier 2 (simulation) sketch

```metta
(= (eval-equation-tier2 $cat $book $treatment)
   (let (($scenarios (m2m-or-htm-scenarios $cat $treatment))
         ($combiner (combiner-of $cat))
         ($losses (collapse
                    (map (lambda ($s) (simulate-loss $cat $book $s))
                         $scenarios))))
     (apply-combiner $combiner $losses)))
```

### Tier 3 (heuristic) sketch

```metta
(= (eval-equation-tier3 $cat $book $treatment)
   (let* (($best-effort-rw (best-effort-estimate $cat $book $treatment))
          ($depth (recursion-depth-of $book))
          ($depth-penalty (* $depth (depth-penalty-per-level)))
          ($cycle-penalty (case (cycle-detected $book)
                            ((True (loop-penalty-multiplier))
                             (False 1.0))))
          ($repeat-penalty (case (repeated-terminals $book)
                             ((True (repeated-terminal-penalty))
                              (False 1.0)))))
     (min 1.0
          (* $best-effort-rw $cycle-penalty $repeat-penalty
             (+ 1.0 $depth-penalty)))))
```

Heuristic parameters live in `&core-framework-risk` (governance-tunable):

```metta
(loop-penalty-multiplier 1.5)
(depth-penalty-per-level 0.05)
(max-recursion-depth 8)
(repeated-terminal-penalty 1.3)
```

### Tier 4 (max-risk) — final fallback

```metta
(= (eval-equation-tier4 $cat $book $treatment)
   (notional-of-issued-units $book))                     ; CRR = 100%
```

---

## 6. Loop and recursion handling in synlang

Loops happen in real DeFi composability — vaults of vaults, circular hypothecation. The framework handles them via the four-tier hierarchy.

### Cycle detection

```metta
(= (exobook-rw-with-loop-handling $book $treatment $depth $visited)
   (cond
     ((> $depth (max-recursion-depth))
        (notional-of-issued-units $book))                  ; CRR 100%
     ((in-set $book $visited)
        (* (loop-penalty-multiplier) (best-effort-rw $book $treatment)))
     (True
        (let* (($visited' (add-to-set $book $visited))
               ($cat (exobook-category $book))
               ($child-rws (recurse-children $book $cat $treatment (+ $depth 1) $visited'))
               ($raw-rw (eval-category-equation $cat $book $child-rws))
               ($depth-mult (+ 1.0 (* $depth (depth-penalty-per-level))))
               ($repeat-mult (case (repeated-terminals-across-paths $book)
                                ((True (repeated-terminal-penalty))
                                 (False 1.0)))))
          (min 1.0 (* $raw-rw $depth-mult $repeat-mult))))))
```

### Iterative simulation

```metta
(= (iterative-simulate $book $scenario $iters $damping)
   (let-loop ($state (initial-state $book) (i 0))
      (case (>= $i $iters)
        ((True $state)
         (False
            (let* (($next   (one-step-update $state $scenario))
                   ($damped (interpolate $state $next $damping)))
              (if (converged? $state $damped)
                  $damped
                  (iter $damped (+ $i 1)))))))))
```

Damping prevents oscillation. Iteration cap prevents runaway. If convergence isn't achieved, fall through to tier 3.

---

## 7. Default-deny CRR-100% mechanism

Three places this manifests structurally:

```metta
;; 1. Riskbook without matching category
(= (riskbook-finality-crr $book)
   (case (find-matching-category $book)
     ((no-match 1.0)                                       ; CRR 100%
      ($cat (eval-equation $cat $book m2m)))))

;; 2. Exobook beyond max recursion depth
(= (exobook-rw-bounded $book $depth)
   (cond
     ((> $depth (max-recursion-depth)) 1.0)                ; CRR 100%
     ...))

;; 3. Exobook without matching category
(= (exobook-rw $book $treatment)
   (case (exobook-category $book)
     ((no-category 1.0)                                    ; CRR 100%
      ($cat (eval-equation $cat $book $treatment)))))
```

For full conceptual treatment, see [`risk-decomposition.md`](../risk-framework/risk-decomposition.md) §7.

---

## 8. Worked examples

Five examples covering the model's expressive range. For the canonical end-to-end v1 test scenario, see [`../risk-framework/examples.md`](../risk-framework/examples.md).

### Example A — Pure ETH Riskbook (terminal, math tier)

```metta
;; in &core-framework-risk-categories
(risk-category-def eth (level exo-asset) (m2m 0.25) (htm 0.20))

(risk-category-def pure-eth-holding
   (level riskbook)
   (composition-constraints (only-asset-class eth))
   (equation-m2m (* (sum-of-notionals) (lookup-rw eth m2m)))
   (equation-htm (* (sum-of-notionals) (lookup-rw eth htm)))
   (resolution-tier math))

;; in &entity-halo-spark-eth-riskbook-A
(book-type riskbook)
(book-category pure-eth-holding)
(holds eth-asset 1000)                                   ; 1000 ETH
(issues (endo-unit u-rb-A-bond) (notional 1000))         ; 1000 ETH equiv
```

Computation:

```
riskbook-finality-rw(spark-eth-rb-A, m2m):
   matched-category = pure-eth-holding
   resolution-tier = math
   apply equation: 1000 × 0.25 = 250 ETH-equiv risk weight
   ⇒ M2M CRR = 250/1000 = 0.25 = 25%
```

### Example B — Morpho lending Riskbook (Exobook recursion, simulation tier)

A Halo holds a Morpho-vault exo unit. The Riskbook category invokes recursion through Morpho's structure.

```metta
(risk-category-def morpho-borrow-position
   (level exobook)
   (variables [(coll-value $cv) (debt $d) (liq-thresh $lt)])
   (equation-m2m (simulate-borrow-position-loss $cv $d $lt))
   (resolution-tier simulation))

(risk-category-def morpho-market
   (level exobook)
   (equation-m2m (sum-children-weighted) (then-floor 0.30))
   (resolution-tier simulation))

(risk-category-def morpho-vault
   (level exobook)
   (equation-m2m (allocation-weighted-sum) (then-floor 0.35))
   (resolution-tier simulation))

(risk-category-def morpho-lending
   (level riskbook)
   (composition-constraints (units-pointing-to-morpho-vault-or-market))
   (equation-m2m (sum-over-units (lambda ($u) (* (notional $u) (exobook-rw (issuer $u) m2m)))))
   (resolution-tier simulation))

;; exo book registry
(exo-book morpho-eth-vault       (category morpho-vault))
(exo-book morpho-market-X        (category morpho-market))
(exo-book borrower-pos-1         (category morpho-borrow-position))
(exo-book eth                    (category eth))

(exo-book-holds morpho-eth-vault morpho-market-X 1.0)         ; 100% in market X
(exo-book-holds morpho-market-X borrower-pos-1 1.0)
(exo-book-asset borrower-pos-1 eth 150)
(exo-book-liability borrower-pos-1 owed-to-morpho-X 100)

(book-type riskbook)
(book-category morpho-lending)
(holds (exo-unit u-001) morpho-eth-vault 1000000)
```

Computation under severe-correlated-crash:

```
exobook-rw(borrower-pos-1, m2m, scenario=severe-correlated-crash):
   coll-value (current) = 150 ETH × $4000 = $600,000
   coll-value (post-stress) = $600,000 × (1 - 0.55) = $270,000
   debt = $400,000
   recovery = min($270,000, $400,000) = $270,000
   loss-fraction = 1 - 270000/400000 = 0.325

exobook-rw(morpho-market-X, m2m):
   weighted-sum-of-children = 0.325
   floor = 0.30
   ⇒ 0.325

exobook-rw(morpho-eth-vault, m2m):
   allocation-weighted-sum = 0.325
   floor = 0.35
   ⇒ 0.35

riskbook-finality-rw(spark-defi-rb-B, m2m):
   $1,000,000 × 0.35 = $350,000
   ⇒ M2M CRR = 35%
```

### Example C — ABF + CDS Riskbook (offsetting positions)

```metta
(risk-category-def abf-with-cds-cover
   (level riskbook)
   (composition-constraints
      (and (count-of (asset-class abf-claim)) = 1)
           (count-of (asset-class cds-cover)) = 1)
           (cds-references-credit-asset-in-same-book ...)
           (>= (cds-notional / abf-notional) 0.90)))
   (equation-m2m
      (simulate-across-scenarios m2m-scenarios
         (lambda ($scenario)
            (let* (($abf-default-prob (apply-credit-stress $scenario abf-deal))
                   ($abf-loss-on-default (- 1.0 (abf-recovery-rate $scenario)))
                   ($cds-counterparty-survival (cds-counterparty-survival-prob $scenario))
                   ($cds-effective-payout
                      (* (cds-notional)
                         $cds-counterparty-survival
                         (cds-payout-ratio $scenario)))
                   ($expected-loss
                      (* $abf-default-prob
                         (max 0 (- (abf-notional) $cds-effective-payout)))))
              (/ $expected-loss (abf-notional))))
         (combiner take-worst)))
   (resolution-tier simulation))

(book-type riskbook)
(book-category abf-with-cds-cover)
(holds (exo-unit u-001) abf-deal-D 1000000)
(holds (exo-unit u-002) cds-on-abf-deal-D 950000)        ; 95% coverage
```

Computation under severe-correlated-crash:

```
abf-default-prob = 0.20
abf-recovery-rate = 0.40
cds-counterparty-survival = 0.75 (counterparty stressed)
cds-payout-ratio (if survives) = 1.0

cds-effective-payout = 950,000 × 0.75 × 1.0 = 712,500

if ABF defaults:
   gross loss = 1,000,000 × 0.60 = 600,000
   net loss (after CDS) = max(0, 600,000 - 712,500) = 0      ; CDS covers fully

if ABF doesn't default (probability 0.80):
   no loss

expected-loss = 0.20 × 0 + 0.80 × 0 = 0
```

The CDS effectively transforms a high-risk credit position (~12% RW unhedged) into a much lower risk position (~4-5% RW). The remaining risk is **counterparty residual** — the risk that the CDS issuer fails to pay.

### Example D — Multi-Riskbook Halo composition

A Halo wants exposure to ABF (with CDS protection) AND Morpho lending. Each gets its own Riskbook with appropriate category. Halobook aggregates without netting.

```metta
;; Two Riskbooks under one Halo
(book-type riskbook (book-category abf-with-cds-cover) ...)        ; spark-credit-rb-A
(book-type riskbook (book-category morpho-lending) ...)            ; spark-credit-rb-B

;; Halobook aggregating both
(book-type halobook)
(sub-riskbook spark-credit-rb-A)
(sub-riskbook spark-credit-rb-B)
(holds (endo-unit u-rb-a-bond) 1000000)
(holds (endo-unit u-rb-b-bond) 2000000)
(issues (endo-unit u-hb-bond) (notional 3000000))
```

Computation:

```
Halobook RW (M2M)  = (1,000,000 × 0.044) + (2,000,000 × 0.35)
                  = 44,000 + 700,000
                  = 744,000
   ⇒ M2M CRR = 744,000 / 3,000,000 = 0.248 ≈ 25%
```

Cross-Riskbook correlation isn't credited at the Halobook level. Bankruptcy-remoteness across Riskbooks forbids netting (per [`riskbook-layer.md`](../risk-framework/riskbook-layer.md) §6).

### Example E — Looped exposure (heuristic tier fallback)

A Halo holds an exo unit pointing to Vault-Alpha, which holds positions in Vault-Beta, which holds positions back in Vault-Alpha (a loop).

```metta
(exo-book vault-alpha (category opaque-vault))
(exo-book vault-beta  (category opaque-vault))
(exo-book-holds vault-alpha vault-beta 1.0)                  ; alpha 100% in beta
(exo-book-holds vault-beta vault-alpha 1.0)                  ; beta 100% in alpha
(exo-book-asset ... eth 100)

(book-category vault-of-vaults)
(holds (exo-unit u-001) vault-alpha 1000000)
```

Computation walks down with cycle detection:

```
exobook-rw-with-loop-handling(vault-alpha, m2m, depth=0, visited=∅):
   recurse into children with visited = {vault-alpha}
   
   exobook-rw-with-loop-handling(vault-beta, m2m, depth=1, visited={vault-alpha}):
      recurse into children with visited = {vault-alpha, vault-beta}
      
      exobook-rw-with-loop-handling(vault-alpha, m2m, depth=2, visited={vault-alpha, vault-beta}):
         CYCLE DETECTED
         → return 1.5 × 0.5 = 0.75

      vault-beta's RW = (1.0 × 0.75) = 0.75
      depth-multiplier = 1.05
      vault-beta's adjusted = 0.75 × 1.05 = 0.7875

   vault-alpha's RW = 0.7875

⇒ Riskbook M2M CRR ≈ 79%
```

The looped structure ends up with very high CRR (~79%) due to the cycle penalty. **Looped structures are still possible but economically discouraged.** A Halo that wants to use them pays real capital cost; a Halo that doesn't can avoid them.

---

## 9. Cross-doc invariants

Things that should be true across all docs touching the risk model:

- The four book types (Primebook, Halobook, Riskbook, Exobook) are stable; the Generator's Genbook sits above
- Riskbook is the unit of regulation — must match a registered category or get CRR 100%
- The equity invariant holds at every book (per [`book-primitive.md`](../risk-framework/book-primitive.md))
- Frame inheritance runs top-down from the Generator (per [`currency-frame.md`](../risk-framework/currency-frame.md))
- Tranches are ordered claims with seniority; the most-junior is always the equity tranche (per [`tranching.md`](../risk-framework/tranching.md))
- Default risk lives entirely at the Riskbook level; Halobook never modifies it (per [`risk-decomposition.md`](../risk-framework/risk-decomposition.md) §5)
- Five risk types: default, credit-spread MTM, rate, liquidity, concentration (per [`risk-decomposition.md`](../risk-framework/risk-decomposition.md))
- U/P/T liquidity decomposition: U at Riskbook, P + T at Halobook (per [`risk-decomposition.md`](../risk-framework/risk-decomposition.md) §4)
- Five sub-books in Primebook: ascbook, tradingbook, termbook, structbook, hedgebook (plus unmatched) (per [`primebook-composition.md`](../risk-framework/primebook-composition.md))
- Four-tier resolution: math → simulation → heuristic → max-risk
- Default-deny CRR 100% applies anywhere the framework can't model adequately

If a doc contradicts one of these, that's a doc bug.

---

## File map

| Doc | Relationship |
|---|---|
| [`../risk-framework/`](../risk-framework/README.md) | Canonical conceptual treatment of the risk framework |
| [`topology.md`](topology.md) | Where `&core-framework-risk-categories`, `&core-framework-stress-scenarios`, `&core-registry-exo-book` live structurally |
| [`synlang-patterns.md`](synlang-patterns.md) | Conservation-network framing (books-as-nodes, units-as-edges) |
| [`runtime.md`](runtime.md) | Auth, gates, telgate / syngate — how Halo govops pushes state through, how endoscrapers verify |
| [`boot-model.md`](boot-model.md) | How endoscraper loops boot to populate exo book registry |
| [`scaling.md`](scaling.md) | Hot-spotting on `&core-registry-exo-book`; endoscraper bandwidth; simulation computation cost |
| [`settlement-cycle-example.md`](settlement-cycle-example.md) | Worked settlement (uses old state-based CRR; pending update) |
