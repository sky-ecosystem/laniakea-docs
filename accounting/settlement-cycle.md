# Settlement Cycle

**Status:** Draft (synlang-native rewrite)
**Last Updated:** 2026-05-07

---

## TL;DR

Synserv runs a heartbeat that continuously derives **real-time ER per Prime** in synlang. At each settlement boundary (a governance fact: monthly in Phase 1, daily from Phase 3+), settlement closure runs as synart-resolved code: per-Prime net amounts are computed in parallel against each Prime's entart subtree (max debt fees − idle reimbursement − sUSDS spread profit − Sky Direct shortfall + breach penalty + synart resource fee), then a Phase 2 global aggregation sums everything into `&core.settlement` (TMF waterfall: treasury, ecosystem, etc.). The synlang shape doesn't change with cadence — only the epoch length and operational automation level do.

---

## 1. The settlement architecture

Settlement is a property of the synserv heartbeat plus an epoch-boundary closure pass. Three things run together:

| Activity | Cadence | Where |
|---|---|---|
| **Real-time ER emission** | Per heartbeat (continuous) | `&entity.prime.{id}.primebook` |
| **Per-Prime settlement closure** | Per epoch boundary (governance-set) | `&entity.prime.{id}.root` |
| **Global aggregation** | After all per-Prime closures confirm | `&core.settlement` |

The canonical synserv loop is `&core.loop.synserv`. It evaluates the heartbeat body — driving all derived state and emitting `(prime-er $prime $value $timestamp)` atoms continuously — and at the epoch boundary runs the closure rules that reduce the epoch's event log into per-Prime net amounts. The two-phase pattern (parallel per-Prime → sequential global aggregation) follows from data dependency: per-Prime computations are independent; aggregation needs all per-Prime outputs.

This doc is the canonical home for the two-phase settlement closure, the cycle gantt, and the rolling two-epoch retention model.

---

## 2. The five-step per-Prime computation, synlang-native

Each Prime's settlement reconciles borrowing costs against credits earned from holding assets productively. The five-step methodology is unchanged from pre-synlang accounting; the framing is now synart-resolved code reading time-weighted aggregates from the Prime's entart subtree.

### Step 1 — Maximum debt fees

The starting point is what the Prime would owe if there were no reimbursements.

```metta
;; in &entity.prime.{id}.root
(= (prime-debt-fee $prime $epoch)
   (let* (($d (time-weighted-debt $prime $epoch))      ; from Genbook unit holdings
          ($r (match &core.framework.fee
                 (base-rate-per-epoch $epoch $r) $r)))
     (* $d $r)))
```

`time-weighted-debt` reads the Prime's outstanding Genbook unit notional integrated over the epoch. The base rate is a governance-set fact in `&core.framework.fee`. (Legacy "ilk debt" terminology refers to the same quantity — Generator debt expressed as Genbook unit notional.)

### Step 2 — Idle USDS/DAI reimbursement

Primes hold idle USDS/DAI across many locations (PSM3, ALMProxy, third-party lending, AMM pools). Idle assets earn the Base Rate; the Prime gets reimbursed at the same rate paid in Step 1, avoiding double-counting.

```metta
;; scatter-gather across the Prime's primebook sub-spaces tracking USDS/DAI positions
(= (idle-usds-reimbursement $prime $epoch)
   (let* (($b (sum (collapse
                   (match &entity.prime.{id}.primebook
                     (idle-position $prime usds $loc $balance $epoch)
                     (time-weighted $balance)))))
          ($r (base-rate-per-epoch $epoch)))
     (* $b $r)))
```

The pattern is a scatter-gather across the Prime's primebook sub-spaces. Each location appears as an `idle-position` atom written by the Prime's govops beacon plus synserv-run code calling the `chain-read` grounded primitive (on-chain locations) or attest-data beacons (off-chain locations); the rule sums their time-weighted balances.

### Step 3 — sUSDS spread profit

Primes also hold sUSDS across the same locations. sUSDS earns the Savings Rate (= Base Rate + spread). Step 1 already accounts for the Base Rate portion; here the Prime captures only the spread.

```metta
(= (susds-spread-profit $prime $epoch)
   (let* (($b (sum (collapse
                   (match &entity.prime.{id}.primebook
                     (idle-position $prime susds $loc $balance $epoch)
                     (time-weighted $balance)))))
          ($s (match &core.framework.fee
                 (savings-rate-spread $epoch $s) $s)))
     (* $b $s)))
```

Same scatter-gather shape as Step 2, restricted to sUSDS-shaped positions. The spread is a governance-set fact.

### Step 4 — Sky Direct shortfall reimbursement

Sky Direct allocations are governance-mandated capital deployments. For each, the settlement compares actual yield against the Base Rate. Below Base Rate, the Prime is made whole; at-or-above, Sky captures all profits.

```metta
(= (sky-direct-shortfall $prime $epoch)
   (sum (collapse
     (match &entity.prime.{id}.primebook
       (sky-direct-allocation $prime $alloc $epoch
          (exposure $e) (actual-profit $a))
       (max 0 (- (* $e (base-rate-per-epoch $epoch)) $a))))))
```

The asymmetric structure — Prime protected from downside, Sky takes all upside — is unchanged from pre-synlang accounting; it compensates Sky for governance allocation risk.

### Step 5 — Net amount

```metta
(= (epoch-net-owed $prime $epoch)
   (let* (($f  (prime-debt-fee          $prime $epoch))
          ($i  (idle-usds-reimbursement $prime $epoch))
          ($s  (susds-spread-profit     $prime $epoch))
          ($d  (sky-direct-shortfall    $prime $epoch))
          ($p  (epoch-penalty-owed      $prime $epoch))   ; §6 below
          ($r  (synart-resource-fee     $prime $epoch))) ; §10 below
     (- (+ $f $p $r) (+ $i $s $d))))
```

Positive net = Prime owes; negative = Prime has profit. The result is written into `&entity.prime.{id}.root` as `(epoch-net-owed $prime $epoch $amount)` and mirrored into `&core.settlement` for global aggregation.

**Time-weighting** runs through every aggregate. **Base Rate netting** (Step 1 charges, Step 2 credits) prevents double-counting; sUSDS profit (Step 3) captures only the spread.

---

## 3. Real-time ER emission

The heartbeat doesn't wait for an epoch boundary to publish ER. Per `roadmap/phase-1-spaces.md`, synserv emits `(prime-er $prime $value $timestamp)` continuously per heartbeat:

```
synserv heartbeat (evaluating &core.loop.synserv)

  ... derive insynTRRC[prime] from structbook sweep
  ... read (exsyn-trrc-claim $prime _) from book-attestation oracle
  TRRC[prime] = insynTRRC[prime] + exsynTRRC[prime]
  TRC[prime]  = (prime-trc $prime _) atom in &entity.prime.{id}.root
  emit:  (prime-er $prime (/ TRRC TRC) $now)
```

ER is **derived, not stored** — each heartbeat recomputes from current input atoms. ER samples accumulate during the epoch in the Prime's primebook Space; the rolling two-epoch window keeps them around through the next settlement.

This is what makes Phase 1's deliverable possible: governance can read ER off the synome at any cadence it likes, even though formal settlement closure is still monthly.

### The rolling two-epoch retention model

Synart is the canonical real-time event log, but it is **not a permanent event store**. Each entart Space holds the most-recently-settled epoch alongside the currently-streaming one — a rolling **two-epoch window per Space**. Pruning happens at the *next* settlement boundary: when epoch N is settled, epoch N−1's events are pruned. The on-chain transactions are the long-term historical canonical record.

| Time | What synart holds (per Space) |
|---|---|
| During epoch N+1, after epoch N settled | Epoch N (just-settled, retained) + Epoch N+1 (streaming) |
| At epoch N+1 close | Settlement runs against epoch N+1 events |
| After epoch N+1 settled | Epoch N pruned; epoch N+1 retained; epoch N+2 begins streaming |

**Why two epochs and not one:** the just-settled epoch must remain readable while wardens, verifier embs, dispute resolution, and re-derivation are still running against it. Pruning epoch N at the moment N closes would destroy the comparison surface. Two-epoch retention gives one full epoch's worth of late re-derivation budget; longer windows would inflate replication bandwidth without changing the failure-mode envelope.

**What this means for cost:** synart resource consumption (per §10 below) is bounded by retention, not by total history. A Halo posting 10 events/sec pays for 2 × epoch-length × 10 events of retention, not for unbounded accumulation. Long-term forensics requires either out-of-band archive nodes (running the `archive` loop with full retention) or the on-chain transaction record.

**What must persist beyond an epoch** must be promoted to a settlement-tier atom (which lives in `&core.settlement` indefinitely until governance decides otherwise) or written to an out-of-band archive before pruning.

---

## 4. Two-phase settlement closure at the epoch boundary

When the epoch closes, synserv runs the closure pass:

### Phase 1 — Per-Prime parallel

Each Prime's `epoch-net-owed` is computed independently against its own entart subtree. No cross-Prime coordination. The synlang reads:
- Genbook unit holdings (debt fee math)
- Primebook sub-space `idle-position` atoms (idle reimbursement, sUSDS profit)
- Primebook `sky-direct-allocation` atoms (shortfall)
- Primebook ER samples accumulated during the epoch (breach penalty, §6)
- Synart resource consumption (§10)

The result is one settlement record per Prime in `&entity.prime.{id}.root`. From Phase 2 onward, Prime beacons consume that record and execute on-chain settlement transactions; in Phase 1, governance reads it and acts manually.

### Phase 2 — Global aggregation

After all per-Prime closures confirm, synserv aggregates into `&core.settlement`:

```metta
;; Phase 2 closure inside synserv — scatter-gather across Prime entarts
(= (sky-net $epoch)
   (let* (($income  (sum (collapse
                          (match &entity.prime.*.root
                            (epoch-net-owed $prime $epoch $amt) $amt))))
          ($outflow (... distribution rewards, etc.))
          (...))
     (- $income $outflow)))

;; results written into &core.settlement
(epoch-sky-net      $epoch $amount)
(epoch-treasury     $epoch (* $amount $treasury-split))
(epoch-ecosystem    $epoch (* $amount $ecosystem-split))
(epoch-burn         $epoch (* $amount $burn-split))
(epoch-staking      $epoch (* $amount $staking-split))
```

`&core.settlement` is universal — every embodiment subscribed to it sees the same TMF waterfall outputs (treasury, ecosystem fund, smart burn, staking rewards) regardless of which subtree they replicate. The waterfall splits are governance-set in `&core.framework.fee`.

---

## 5. Cadence is a governance fact

The cadence is encoded as an atom, not as architecture:

```metta
;; in &core.framework.fee
(settlement-cadence monthly)        ; Phase 1 reality
;; replaced at the Phase 3 boundary by:
(settlement-cadence daily)
```

The synlang doesn't change at the boundary. The closure body is the same; only the epoch length and event-log retention period change. Phase 1's monthly cadence is a Phase-1-operational fact, not a permanent design — operational details during transition (manual processing, end-of-following-month, lumpy expense recognition) are out-of-band knowledge and not currently documented in the corpus.

The Phase 3 transition lights up daily settlement; Phases 9+ activate full beacon-operated execution. Each is a sudo-set boundary (cadence atom replaced; tests re-run; production resumes) rather than a code rewrite.

---

## 6. Late-payment penalty mechanics

If a Prime's max-ER during the epoch breached its covenant, settlement applies a penalty:

```metta
;; in &entity.prime.{id}.root (per noemar-synlang/settlement-cycle-example.md §7)
(= (epoch-max-er $prime $epoch)
   (max (collapse
     (match &self (er-sample $prime $epoch $t $v) $v))))

(= (epoch-breach $prime $epoch)
   (let* (($m (epoch-max-er $prime $epoch))
          ($c (match &self (er-covenant $prime $c) $c)))
     (max 0 (- $m $c))))

(= (epoch-penalty-owed $prime $epoch)
   (let* (($b (epoch-breach $prime $epoch))
          ($r (match &self (penalty-rate      $prime $r) $r))
          ($k (match &self (available-capital $prime $k) $k)))
     (/ (* $b (* $r $k)) 10000)))                  ; bp × % × capital scaled
```

The penalty rate comes from `&core.framework.fee`. Penalty atoms feed Step 5 (`epoch-net-owed`) and the global aggregation. The covenant target is `ER ≤ 0.90`.

In Phase 1, breach detection runs in synlang on the real-time ER stream; settlement actions remain manual. From Phase 2 onward, settlement closure writes a settlement record that Prime beacons execute on-chain; persistent late payment escalates via cert/auth chain (revoke auth atom, governance review).

For the worked example (one Prime, one breach event, full closure), see [`noemar-synlang/settlement-cycle-example.md`](../noemar-synlang/settlement-cycle-example.md).

---

## 7. OSRC and Duration submission flow

OSRC and Duration capacity allocation feed into the same daily cadence (Phase 3+). Per the Phase 9+ design:
- OSRC auctions (sealed-bid, uniform-price, daily) allocate srUSDS-backed capacity to Primes.
- Duration auctions (sealed-bid, uniform-price, multi-epoch reservations allowed) allocate structural-demand-matching capacity to Primes.

Both run as **high-authority action beacons** submitting allocation atoms to the Generator's `&entity.generator.usge.structural-demand.auction` Space. Matching is synart-resolved code — not a separate beacon class.

In Phase 1 the auction is a sudo-set "fake auction" — governance writes per-Prime per-bucket allocations directly. The architecture is the same; the bid-matching code simply isn't invoked. See [`duration-allocation.md`](duration-allocation.md) for full design and Phase 1 carve-out.

Auction submission is an `auction-{x}` relay-class beacon (per `macrosynomics/beacon-framework.md`). It submits allocation atoms; the matching engine itself is synserv-run code.

---

## 8. LCTS settlement

LCTS (Liquidity Constrained Token Standard) settlement synchronizes with the daily cadence once srUSDS is live (Phase 4). LCTS settlement is a separate scatter-gather with its own queue mechanics — net flow netting between SubscribeQueue and RedeemQueue, then OSRC capacity for excess subscribes / daily redemption limit for excess redeems, throttled by target spread.

The LCTS spec currently lives at `inactive/pre-synlang/smart-contracts/lcts.md` and is pending its own synlang-native rewrite. LCTS settlement transactions are submitted by per-Halo `lcts-{halo}` relay-class beacons.

---

## 9. Late payment escalation (operational)

A Prime that fails to settle on time:
- Penalty accrues continuously per `epoch-penalty-owed` (rate from `&core.framework.fee`).
- Penalty payments flow to the affected counterparty (Generator for late interest; Sky-net otherwise).
- Persistent lateness escalates via the cert/auth chain — revoke the offending beacon's auth atoms, re-cert from above, ultimately legal recourse via the Guardian.
- All escalation events are append-only synart history pruned at the next settlement; serious breaches are written to a settlement-tier atom or external archive before pruning.

Failure modes (replication staleness, hot-spotting, partitions) live in [`noemar-synlang/scaling.md`](../noemar-synlang/scaling.md).

---

## 9b. Growth staking distribution

Growth Staking rewards and forfeitures are reconciled at each settlement boundary alongside the per-Prime closure. Synserv computes per-Folio staking factors against synserv-derived Reference Values (per [`../growth-staking/growth-staking.md`](../growth-staking/growth-staking.md) §10) and emits two atoms into `&core.settlement`:

```metta
(epoch-staking-rewards-paid       $amount)
(epoch-staking-rewards-forfeited  $amount)   ; from stakers below 100% factor → TMF aggregation
```

Forfeited rewards re-enter the TMF waterfall (rather than being redistributed to fully-qualifying stakers), so the net effect on `epoch-sky-net` is the difference between `(base-yield × Σ staked-sky)` and `epoch-staking-rewards-paid`. Growth Staking activates post-Phase-1; Phase 1 doesn't run this distribution path.

---

## 10. Synart resource consumption

Each Prime pays for the synart resources its beacons consume — per-atom write, per-atom-day retention, per-byte replication out, per-match query. The fees are governance-set in `&core.framework.fee`. Self-regulating volume via pricing: parsimony falls out automatically (a Halo posting 1 event/sec instead of 10/sec pays 10× less); legitimate high-frequency operations pay accordingly. Pricing is a governance lever — adjust the curves to encourage/discourage behaviors.

```metta
;; in &entity.prime.{id}.root
(= (synart-resource-fee $prime $epoch)
   (sum (collapse
     (match &self
       (resource-meter $prime $kind $count $epoch)
       (* $count (fee-per-unit $kind))))))
```

The fee enters Step 5 (`epoch-net-owed`) like any other amount the Prime owes. Parsimony falls out automatically: a beacon posting 1 event/sec instead of 10/sec pays 10× less.

---

## 11. Vocabulary translation (legacy → current)

| Pre-synlang term | Current equivalent | Notes |
|---|---|---|
| `lpla-checker` (legacy beacon class) | Retired — synserv-run in-space calculation + verifier emb | Per `noemar-synlang/listener-loops.md` and `macrosynomics/beacon-framework.md`. The verification role survives but as synart-resolved code plus a separate `verifier` class, not a single beacon. |
| `lpha-auction` (legacy beacon name) | `auction-{x}` (relay class) | Per `beacon-framework.md`; matching itself is synserv-run code. |
| `lpha-lcts` (legacy beacon name) | `lcts-{halo}` (relay class) | LCTS spec pending synlang-native rewrite. |
| Bid message JSON format | Synlang verb-call shape | Bids are signed verb invocations gated by `&core.syngate`. |
| Net flow netting JSON pseudocode | Synlang scatter-gather | Inside the LCTS settlement closure (Phase 4+). |
| "Manual monthly process executed end of following month" | Phase 1 operational reality | Out-of-band during transition; not architecture. |
| State-based CRR (`(crr filling 5)`) | Content-based risk form | CRR comes from Riskbook risk forms consuming structure + oracle inputs (per `risk-framework/riskbook-layer.md`). Phase labels manifest as different exo units pointing to different exo books, not as a state attribute. |

---

## 12. Open parameters

- Penalty rate calibration for daily cadence (Phase 3+)
- Settlement cadence sudo-set in `&core.framework.fee` — exact phase-boundary timing tied to baseline-relay (per-Prime `baseline-{prime}`) deployment readiness
- Bid modification policy (can a Prime cancel a bid before lock? — Phase 9+ auction question)
- Reservation duration limits in epochs (Phase 9+ Duration auction)
- Emergency procedures for systemic settlement failure (network outage, oracle compromise) — handled by failover (`canonical-synserv-runner` reassignment per `roadmap/roadmap-ideas.md`) plus mature-state sudo escape hatch

---

## File map

| Doc | Relationship |
|---|---|
| [`README.md`](laniakea-docs/accounting/README.md) | Accounting directory index |
| [`capital-stack.md`](capital-stack.md) | TRC funding side; settlement Step 1 reads Genbook unit notional set up here |
| [`duration-allocation.md`](duration-allocation.md) | OSRC + Duration auctions feeding the per-epoch capacity that settlement consumes |
| [`../risk-framework/capital-formula.md`](../risk-framework/capital-formula.md) | TRRC computation that ER divides into; Step 5 of the per-Prime closure consumes ER samples derived against TRRC |
| [`../noemar-synlang/settlement-cycle-example.md`](../noemar-synlang/settlement-cycle-example.md) | Worked synlang ER → breach → penalty trace for one Prime over one epoch |
| [`../noemar-synlang/listener-loops.md`](../noemar-synlang/listener-loops.md) | In-space calculation pattern (synserv-run code, not a beacon class) |
| [`../noemar-synlang/runtime.md`](../noemar-synlang/runtime.md) | Gate primitive, heartbeat shape, auth model |
| [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) | Two-tier authority + I/O role; §11 legacy-name glossary |
| [`../roadmap/phase-1-spaces.md`](../roadmap/phase-1-spaces.md) | Phase 1 ER pipeline, structural-demand auction Space, real-time ER emission |
| [`../growth-staking/growth-staking.md`](../growth-staking/growth-staking.md) | Growth Staking reward / forfeiture distribution path through `&core.settlement` (§9b) |
| [`../noemar-synlang/scaling.md`](../noemar-synlang/scaling.md) | Replication, partial sync, hot-spotting, partitions |

---

## One-line summary

**Settlement is the synserv heartbeat publishing real-time ER per Prime continuously, plus an epoch-boundary closure pass that runs the five-step per-Prime computation in synlang (debt fees − idle reimbursement − sUSDS spread profit − Sky Direct shortfall + breach penalty + synart resource fee) in parallel across Primes, then aggregates into `&core.settlement` (TMF waterfall) — with cadence as a governance fact (monthly Phase 1 → daily Phase 3+) the synlang doesn't care about.**
