# Settlement Cycle — Synlang Worked Example

A minimal end-to-end synlang sketch of one settlement cycle for one
Prime, demonstrating the load-bearing primitives: seed state across an
entart subtree, auth grants, permission rules, derived encumbrance
ratio, real-time event samples, covenant check, and penalty calculation.

Companion to `topology.md` (the Space layout this uses) and
`syn-overview.md`. Uses the synome root (`&core-*`) plus the
entart tree (`&entity-*`) defined in `topology.md`.

---

## Scenario

`spark-prime` already has unit `u-001` deployed in `book-A1` (50
notional, state `at-rest`). It deploys a new unit `u-002` into `book-B7`
(state `filling` → `deploying`) with notional 75. Available capital is
100. ER covenant is ≤ 0.90. The new deployment breaches the covenant;
settlement calculates the penalty.

Integer / basis-point math (×100) is used throughout to avoid floats.

---

## The Spaces involved

```
&core-framework-risk                      universal CRR table (replicated everywhere)

&entity-prime-spark-root                  Spark Prime: identity, capital,
                                          covenant, penalty rate, sub-entart
                                          registry, ER samples, settlement record

  └── &entity-halo-spark-term-root        Spark Term Halo: identity, book
                                          registry, auth grants for book actions

        ├── &entity-halo-spark-term-book-A1   book-A1 leaf: state + units
        └── &entity-halo-spark-term-book-B7   book-B7 leaf: state + units

&core-settlement                          Sky-wide settlement aggregation
                                          (Phase 2 of settlement)
```

Auth grants for actions on `book-B7` live in `&entity-halo-spark-term-root`
— per `topology.md` §10, auth lives in the entart owning the target,
and the target (`book-B7`) is owned by the halo.

---

## 1. Seed state

```metta
;; ─── &core-framework-risk ────────────────────────────────────────
(crr filling      5)
(crr deploying  100)
(crr at-rest     40)
(crr unwinding   60)
(crr offboarding 80)
(crr closed       0)

;; ─── &entity-prime-spark-root ────────────────────────────────────
(synent        spark-prime)
(synent-type   spark-prime prime)
(parent-entart spark-prime ozone)
(sub-entart    spark-prime spark-term-halo &entity-halo-spark-term-root)

(available-capital spark-prime 100)
(er-covenant       spark-prime 90)     ; 0.90
(penalty-rate      spark-prime 10)     ; 10% per breach-unit per epoch

;; ─── &entity-halo-spark-term-root ────────────────────────────────
(synent        spark-term-halo)
(synent-type   spark-term-halo halo)
(parent-entart spark-term-halo spark-prime)
(sub-space     spark-term-halo &entity-halo-spark-term-book-A1)
(sub-space     spark-term-halo &entity-halo-spark-term-book-B7)

;; auth grants — target's owner controls auth (topology §8)
(auth lpha-nfat-spark issue-unit      book-B7)
(auth lpha-nfat-spark transition-book book-B7)

;; ─── &entity-halo-spark-term-book-A1 ─────────────────────────────
(book          book-A1)
(book-state    book-A1 at-rest)
(unit          u-001)
(unit-book     u-001 book-A1)
(unit-notional u-001 50)

;; ─── &entity-halo-spark-term-book-B7 ─────────────────────────────
(book       book-B7)
(book-state book-B7 filling)
;; (no units yet — book is filling)
```

## 2. Permission rules — live where the auth atoms live

```metta
;; in &entity-halo-spark-term-root
(= (permits $beacon (issue-unit $book $unit $notional $nonce))
   (if (auth $beacon issue-unit $book) True False))

(= (permits $beacon (transition-book $book $src $dst $nonce))
   (if (auth $beacon transition-book $book) True False))
```

Default-deny is enforced by absence of a matching rule and absence of
an `auth` fact.

## 3. Risk-weight of one unit — local to the book leaf

```metta
;; runs in whichever book-leaf Space hosts the unit
(= (unit-risk-weight $u)
   (let* (($n (match &self                (unit-notional $u $n) $n))
          ($b (match &self                (unit-book     $u $b) $b))
          ($s (match &self                (book-state    $b $s) $s))
          ($c (match &core-framework-risk (crr           $s $c) $c)))
     (/ (* $n $c) 100)))
```

Three reads from `&self` (the book leaf hosting the rule), one read
from the universal `&core-framework-risk`. No cross-entart reach.

## 4. Prime ER — scatter-gather across book leaves

```metta
;; the local rule, projected onto each book leaf
(= (book-exposure-here)
   (sum (collapse
     (match &self (unit $u) (unit-risk-weight $u)))))

;; declared at &entity-prime-spark-root — runs on demand
(global-rule prime-exposure
   (targets    via-registry sub-space     ; recurse: halos → their books
               from         spark-prime)
   (local-rule book-exposure-here)
   (combine    sum))

;; in &entity-prime-spark-root
(= (er $prime)
   (let* (($e (prime-exposure $prime))                          ; scatter-gather
          ($k (match &self (available-capital $prime $k) $k))) ; local
     (/ (* $e 100) $k)))                                        ; ×100 → bp
```

ER is *derived*, not stored. Adding or removing a unit in any book leaf
changes its value automatically — no bookkeeping atom to keep in sync.

## 5. The deployment — two beacon submissions

```metta
;; (issue-unit book-B7 u-002 75 sn42)
;; (transition-book book-B7 filling deploying sn43)
```

Effects (Python) only validate structural preconditions (target exists,
not duplicate, source state matches) and write atoms into
`&entity-halo-spark-term-book-B7`. Authority was already decided by
`permits` before the effect ran.

After both submissions accept, the timeline reads:

| t  | event                              | exposure | ER   |
|----|------------------------------------|----------|------|
| t₀ | seed (only u-001 at-rest)          | 20       | 0.20 |
| t₁ | issue-unit u-002 (book-B7 filling) | 23.75    | 0.24 |
| t₂ | transition B7 → deploying          | 95       | 0.95 ← breach |

## 6. Per-epoch ER samples — streamed by beacons in real time

```metta
;; written into &entity-prime-spark-root
(er-sample spark-prime 2026-05-01 t0 20)
(er-sample spark-prime 2026-05-01 t1 24)
(er-sample spark-prime 2026-05-01 t2 95)
```

These atoms accumulate during the epoch. The rolling 2-epoch window
keeps them around through the next settlement, then prunes.

## 7. Settlement closure — runs inside synserv at epoch close

```metta
;; in &entity-prime-spark-root
(= (epoch-max-er $prime $epoch)
   (max (collapse
     (match &self (er-sample $prime $epoch $t $v) $v))))

(= (epoch-breach $prime $epoch)
   (let* (($m (epoch-max-er $prime $epoch))
          ($c (match &self (er-covenant $prime $c) $c)))
     (max 0 (- $m $c))))

(= (epoch-penalty $prime $epoch)
   (let* (($b (epoch-breach     $prime $epoch))
          ($r (match &self (penalty-rate      $prime $r) $r))
          ($k (match &self (available-capital $prime $k) $k)))
     ;; breach (bp/100) × rate (%) × capital, scaled out of 10000
     (/ (* $b (* $r $k)) 10000)))
```

For this cycle:

- max-er = 95, covenant = 90 → breach = 5
- penalty = 5 × 10 × 100 / 10000 = **0.5**

## 8. Settlement write — flows into global aggregation

```metta
;; (settle-epoch spark-prime 2026-05-01 sn99) effect writes into
;; &entity-prime-spark-root:
(epoch-settled      spark-prime 2026-05-01)
(epoch-penalty-owed spark-prime 2026-05-01 0.5)

;; mirrored into &core-settlement for Sky-wide reconciliation:
;; (add-atom &core-settlement (epoch-penalty-owed spark-prime 2026-05-01 0.5))
```

Phase 2 of settlement is itself a scatter-gather: synserv aggregates
all Primes' `epoch-penalty-owed` atoms into `&core-settlement` for
deterministic Sky-wide reconciliation.

---

## What's load-bearing here

- **ER is a rule, not an atom.** Storing it would create reconciliation
  bugs the moment a unit moves. Deriving it from facts means it's
  always consistent with current state.
- **Permission rules are uniform.** Body is always
  `(if (auth …) True False)`. Authority decisions live entirely in
  `auth` atoms placed in the entart owning the target; rules
  themselves are mechanical.
- **Local-by-default.** `unit-risk-weight` reads only `&self` and the
  universal `&core-*` layer. No rule reaches across siblings; cross-
  entart aggregation is scatter-gather (`prime-exposure`) coordinated
  at the common ancestor.
- **Settlement is a closure over append-only samples.** No "current
  ER" variable to mutate. The epoch's max is recomputed from samples,
  breach and penalty fall out of three more facts.
- **Adding state is adding atoms.** New CRR factor, new penalty
  schedule, new Prime — all just more atoms. No rule edits.

The whole loop is ~70 lines of synlang spread across the entart tree.
