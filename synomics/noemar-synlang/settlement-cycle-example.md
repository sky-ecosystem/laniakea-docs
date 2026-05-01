# Settlement Cycle — Synlang Worked Example

A minimal end-to-end synlang sketch of a daily settlement cycle for one
Prime. Demonstrates the load-bearing primitives: seed state, auth grants,
permission rules, derived encumbrance ratio, real-time event samples,
covenant check, and penalty calculation.

Companion to `syn-overview.md`. Uses the standardized shapes from there
(simplified `auth`-only permission rules, `soter-govops` naming, two-phase
settlement with global aggregation).

---

## Scenario

`spark-prime` already has unit `u-001` deployed in `book-A1` (50 notional,
state `at-rest`). It deploys a new unit `u-002` into `book-B7` (state
`filling` → `deploying`) with notional 75. Available capital is 100. ER
covenant is ≤ 0.90. The new deployment breaches the covenant; settlement
calculates the penalty.

Integer / basis-point math (×100) is used throughout to avoid floats.

---

## 1. Seed state — `&operational`

```metta
(prime spark-prime)
(halo  spark-halo)        (halo-prime  spark-halo spark-prime)
(book  book-A1)           (parent-halo book-A1 spark-halo) (book-state book-A1 at-rest)
(book  book-B7)           (parent-halo book-B7 spark-halo) (book-state book-B7 filling)

(unit u-001)              (unit-book u-001 book-A1) (unit-notional u-001 50)

(available-capital spark-prime 100)
(er-covenant       spark-prime 90)     ; 0.90
(penalty-rate      spark-prime 10)     ; 10% per breach-unit per epoch
```

## 2. CRR table (book-state → risk factor ×100)

```metta
(crr filling      5)
(crr deploying  100)
(crr at-rest     40)
(crr unwinding   60)
(crr offboarding 80)
(crr closed       0)
```

## 3. Auth grants — `&governance` (governance-paced; what `permits` reads)

```metta
(auth lpha-nfat-spark issue-unit      book-B7)
(auth lpha-nfat-spark transition-book book-B7)
```

## 4. Permission rules — one shape per verb, body is just `auth`

```metta
(= (permits $beacon (issue-unit $book $unit $notional $nonce))
   (if (auth $beacon issue-unit $book) True False))

(= (permits $beacon (transition-book $book $src $dst $nonce))
   (if (auth $beacon transition-book $book) True False))
```

Default-deny is enforced by absence of a matching rule and absence of an
`auth` fact.

## 5. Risk-weight of one unit

```metta
(= (unit-risk-weight $u)
   (let* (($n (match &operational (unit-notional $u $n) $n))
          ($b (match &operational (unit-book     $u $b) $b))
          ($s (match &operational (book-state    $b $s) $s))
          ($c (match &operational (crr           $s $c) $c)))
     (/ (* $n $c) 100)))
```

## 6. Prime ER (×100, so 95 means 0.95)

```metta
(= (prime-exposure $prime)
   (sum (collapse
     (match &operational
       (and (halo-prime  $halo  $prime)
            (parent-halo $book  $halo)
            (unit-book   $u     $book))
       (unit-risk-weight $u)))))

(= (er $prime)
   (let* (($e (prime-exposure $prime))
          ($k (match &operational (available-capital $prime $k) $k)))
     (/ (* $e 100) $k)))
```

ER is *derived*, not stored. Adding or removing a unit changes its value
automatically — no bookkeeping atom to keep in sync.

## 7. The deployment — two beacon submissions

```metta
;; (issue-unit book-B7 u-002 75 sn42)
;; (transition-book book-B7 filling deploying sn43)
```

Effects (Python) only validate structural preconditions (target exists,
not duplicate, source state matches) and write atoms. Authority was
already decided by `permits` before the effect ran.

After both submissions accept, the timeline reads:

| t  | event                              | exposure | ER   |
|----|------------------------------------|----------|------|
| t₀ | seed (only u-001 at-rest)          | 20       | 0.20 |
| t₁ | issue-unit u-002 (book-B7 filling) | 23.75    | 0.24 |
| t₂ | transition B7 → deploying          | 95       | 0.95 ← breach |

## 8. Per-epoch ER samples — streamed by beacons in real time

```metta
(er-sample spark-prime 2026-05-01 t0 20)
(er-sample spark-prime 2026-05-01 t1 24)
(er-sample spark-prime 2026-05-01 t2 95)
```

These atoms accumulate in synart during the epoch. The rolling 2-epoch
window keeps them around through the next settlement, then prunes.

## 9. Settlement closure — runs inside synserv at epoch close

```metta
(= (epoch-max-er $prime $epoch)
   (max (collapse
     (match &operational (er-sample $prime $epoch $t $v) $v))))

(= (epoch-breach $prime $epoch)
   (let* (($m (epoch-max-er $prime $epoch))
          ($c (match &operational (er-covenant $prime $c) $c)))
     (max 0 (- $m $c))))

(= (epoch-penalty $prime $epoch)
   (let* (($b (epoch-breach     $prime $epoch))
          ($r (match &operational (penalty-rate      $prime $r) $r))
          ($k (match &operational (available-capital $prime $k) $k)))
     ;; breach (bp/100) × rate (%) × capital, scaled out of 10000
     (/ (* $b (* $r $k)) 10000)))
```

For this cycle:

- max-er = 95, covenant = 90 → breach = 5
- penalty = 5 × 10 × 100 / 10000 = **0.5**

## 10. Settlement write — flows into global aggregation

```metta
;; (settle-epoch spark-prime 2026-05-01 sn99) effect writes:
(epoch-settled       spark-prime 2026-05-01)
(epoch-penalty-owed  spark-prime 2026-05-01 0.5)

;; mirrored into &global-settlement for Sky-wide reconciliation:
;; (add-atom &global-settlement (epoch-penalty-owed spark-prime 2026-05-01 0.5))
```

Phase 2 of settlement aggregates all Primes' `epoch-penalty-owed` atoms
into `&global-settlement` for deterministic Sky-wide reconciliation.

---

## What's load-bearing here

- **ER is a rule, not an atom.** Storing it would create reconciliation
  bugs the moment a unit moves. Deriving it from facts means it's always
  consistent with current state.
- **Permission rules are uniform.** Body is always `(if (auth …) True False)`.
  Authority decisions live entirely in `&governance` `auth` facts; rules
  themselves are mechanical.
- **Settlement is a closure over append-only samples.** No "current ER"
  variable to mutate. The epoch's max is recomputed from samples, breach
  and penalty fall out of three more facts.
- **Adding state is adding atoms.** New CRR factor, new penalty schedule,
  new Prime — all just more atoms. No rule edits.

The whole loop is ~70 lines of synlang.
