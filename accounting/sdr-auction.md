# SDR Auction

**Status:** Phase 9+ design. Phase 1 uses the synserv-triggered ownership-weighted temporary SDR auction per [`roadmap/phase-1-spaces.md`](../roadmap/phase-1-spaces.md).
**Last Updated:** 2026-05-17

---

## Scope

How structural-demand-matching capacity gets allocated across Primes. The capacity itself is effective Structural Demand Resource (SDR): lot-age surface → Lindy SDR bucket capacity → SDR policy overlay → effective SDR bucket capacity — see [`risk-framework/sdr-model.md`](../risk-framework/sdr-model.md). This doc defines how that capacity flows through the temporary P1 SDR auction and through the **OSRC + SDR auction sequence**, including **tug-of-war among existing SDR reservations** (Phase 9+).

The capacity that lands here gets consumed by `structbook` (against structural USDS demand) and `termbook` (against tUSDS YT) per [`risk-framework/primebook-composition.md`](../risk-framework/primebook-composition.md).

---

## 1. Architectural placement

Capacity lives in the Generator's entart:

```
&entity.generator.usge.root
  ├── &entity.generator.usge.structural-demand   ← lot-age surface + effective SDR capacity atoms
  └── &entity.generator.usge.sdr-auction         ← allocation atoms / SDR auction body
```

This is the canonical location for:
- Effective SDR bucket capacity atoms (lot-age surface + Lindy SDR + SDR policy overlay)
- Per-Prime per-bucket SDR allocation atoms (pro-rata temporary body in Phase 1; auction-resolved in Phase 9+)
- Later auction infrastructure that changes allocation provenance without moving the consumer read path

Capacity flows out to each Prime's `structbook` (and `termbook` once tUSDS is live) via the matching mechanics in [`risk-framework/matching.md`](../risk-framework/matching.md). The structbook reads its allocation from the `sdr-auction` Space and consumes it across positions per the optimization in [`risk-framework/primebook-composition.md`](../risk-framework/primebook-composition.md) §4.

---

## 2. Bucket structure

The SDR Bucket system uses **51 buckets**, each representing **30 days**:

- Bucket 0 = 0 days (immediate liquidity)
- Bucket N covers `(N-1) × 30` to `N × 30` days
- Bucket 42 = 1,260 days (JAAA)
- Bucket 50 = 1,500+ days (structural / permanent base)

For the bucket math, structural-cap formula (double exponential decay calibrated to bank-run research), and Lindy SDR measurement, see [`risk-framework/sdr-model.md`](../risk-framework/sdr-model.md).

Distance decay in the Phase 9+ tug-of-war (§5) is per-bucket: distance 1 = 30 days, distance 5 = 150 days.

---

## 3. Phase 1 temporary SDR auction

In Phase 1, synserv triggers a temporary ownership-weighted pro-rata SDR auction during the daily DSC processing window. The auction body reads effective SDR bucket capacities from `&entity.generator.usge.structural-demand`, reads Sky token-share facts from `&core.treasury`, reads IJRC from Prime roots, and writes per-Prime per-bucket allocations into `&entity.generator.usge.sdr-auction`:

```metta
(sdr-allocation $prime $bucket $amount $epoch)
```

The P1 allocator equation:

```text
sky_effective_ownership(p) = 0.05 + 0.95 * sky_prime_token_share(p)
ownership_weight(p)        = sky_effective_ownership(p) * prime_ijrc(p)
allocation(p,bucket,epoch) = effective_sdr_bucket_capacity(bucket,epoch) * ownership_weight(p,epoch) / sum(active_prime_weights(epoch))
```

The Prime's structbook reads its current-epoch allocation atoms and consumes them; the rest of the synlang (sub-book routing, matched/unmatched blending in CRR computation) is unchanged from the later auction-mode design.

Phase 1 details:
- 7 Primes deploy into 3 P1 Halos
- All 51 buckets are split across active Primes by ownership weight each DSC epoch
- Missing, stale, or zero IJRC means zero allocation
- Unlaunched token shares still count as ownership through supplied treasury facts
- If there are no active positive weights, allocation rounds to zero; any rounding/dust remainder also rounds to zero
- Prior epoch allocations are historical; there is no unused-allocation carry-forward
- There is no P1 reservation market, sticky claim, durable SDR ownership, capacity debt, tug-of-war, or trading/upgrading path
- Lot-age surface, Lindy SDR, and the SDR policy overlay produce effective SDR bucket capacity in P1; governance sets the overlay, not the ordinary capacity result

Per [`roadmap/phase-1-spaces.md`](../roadmap/phase-1-spaces.md). The architecture is "write allocation atoms to the Generator's `sdr-auction` Space"; Phase 1 uses a simple synserv-run body, and the substrate is unchanged when real SDR auctions activate.

Auction submission is an `auction-{x}` beacon (relay class, per `macrosynomics/beacon-framework.md`). What makes it high-authority is the BEAM hierarchy and auth-scoped operation of the Generator, not the class. Matching itself is synserv-run code, not a beacon class.

---

## 4. Phase 9+ — the auction sequence

When per-Prime baseline-relay beacons (`baseline-{prime}`) deploy, sealed-bid auctions activate. The full sequence per epoch:

```
1.  Pre-auction governance allocation publishing (current state)
2.  Sealed-bid OSRC auction              ← uniform-price, daily, no multi-day reservations
3.  Sealed-bid SDR auction          ← multi-epoch reservations allowed
4.  Lindy measurement at lock window
5.  Tug-of-war among existing reservations    ← Phase 1 of allocation
6.  Trading among Primes                  ← Phase 2 of allocation, including overreach trades
7.  Excess capacity → SDR auction
```

Steps 5–7 run during the processing window (between submission lock and settlement). Step 4 establishes the per-bucket capacity that downstream allocation consumes.

### OSRC auction

Sealed-bid, **uniform-price**, **daily-only** (no multi-day reservations). Allocates srUSDS-backed capacity. All winners pay the clearing rate (lowest matched bid). Daily-only because:
- Multi-epoch rate lock-in distorts srUSDS yields
- Capacity must match actual srUSDS supply
- Old reservations would suppress yields and chase exit
- Daily auctions provide clean per-day price discovery

### SDR auction

Sealed-bid, uniform-price, **multi-epoch reservations allowed**. Allocates SDR capacity reservations to Primes. Multi-epoch is allowed because SDR capacity is about sticky demand and hold-to-par matching, and reservations don't directly affect other participants' yields the way OSRC reservations would suppress srUSDS yields.

### Architectural placement

OSRC auctions and SDR auctions are **high-authority action beacons** submitting allocation atoms into their Generator auction Spaces (`&entity.generator.usge.osrc-auction` for OSRC once added, `&entity.generator.usge.sdr-auction` for SDR). Bid submissions are signed verb-call shapes gated by `&core.syngate`:

```metta
;; sealed-bid submission (synlang verb shape, replacing legacy JSON format)
(submit-osrc-bid $prime $amount $max-rate $epoch)
(submit-sdr-bid $prime $bucket $amount $max-price $epochs)
```

The matching algorithm itself is **synart-resolved code** (synserv-run) — not a separate beacon class. This is consistent with the in-space calculation pattern (`macrosynomics/beacon-framework.md`): input beacons push data, synserv runs the matching equations, output state lands in the auction Space.

---

## 5. Tug-of-war among existing reservations (Phase 1 of allocation)

When Lindy-measured SDR capacity ≠ total reservations, all capacity is allocated through tugging. Existing reservation holders tug on buckets — including their own — to fill their need.

### Two phases inside allocation

1. **Tug-of-War.** Primes tug on all buckets (including their own) to fill their reserved need.
2. **Trading.** After need is met, Primes upgrade their capacity mix by trading up and cascading down.

### Tug strength

```
Base Tug = MAX(Remaining Need × Tug Rate, Reservation × Min Tug Floor)

Where:
  Remaining Need   = Reserved amount − Already allocated
  Tug Rate         = 10% per round
  Min Tug Floor    = 1% of reservation (prevents infinitesimal amounts)
```

The minimum floor ensures dust amounts get cleaned up rather than requiring infinite rounds.

### Distance decay

```
Distance Penalty = MAX((Distance Decay)^Distance, Min Distance Factor)

Effective Tug = Base Tug × Distance Penalty

Where:
  Distance            = |Your bucket − Target bucket|
  Distance Decay      = 0.9 (10% decay per bucket)
  Min Distance Factor = 0.10 (90% max penalty regardless of distance)
```

Even very distant buckets can still be tugged at 10% strength — preventing scenarios where distance makes amounts infinitesimally small.

**Example.** Prime at bucket 40, needs $100M, tugging at bucket 45:
- Base Tug = $100M × 10% = $10M
- Distance = 5
- Effective Tug = $10M × (0.9)^5 = $10M × 0.59 = $5.9M

### Effective value

Tugging UP and DOWN have different value:

| Direction | Effective Value | Rationale |
|---|---|---|
| **Tug UP** | 1.0 | Higher bucket = full match or better, no gap capital |
| **Tug DOWN** | Target Bucket / Your Bucket | Lower bucket = gap capital required, value degrades |

```
Tug UP value   = Effective Tug × 1.0
Tug DOWN value = Effective Tug × (Target Bucket / Your Bucket)
```

Primes tug in the direction with highest effective value first.

### Collision resolution

When multiple Primes tug at the same bucket:

```
Total Tug = Σ Effective Tugs on this bucket
Available = Excess capacity in bucket

If Total Tug ≤ Available:
  Everyone gets their full Effective Tug
Else:
  Pro-rata: Each Prime gets (Their Tug / Total Tug) × Available
  Unsatisfied remainder can redirect to untouched buckets
```

### Iteration limit

Cap iterations per round (e.g., max 10) to prevent infinite loops. Convergence is fast in practice: each iteration touches new buckets; tug strength is small relative to capacity; eventually all excess is allocated or all needs are met.

### Worked example

Setup:
```
Primes:
  Prime A (bucket 50) reserved $100M
  Prime B (bucket 35) reserved $100M
  Prime C (bucket 20) reserved $100M

Available capacity:
  Bucket 50: $60M (A's own bucket; can't fully cover)
  Bucket 55: $30M
  Bucket 45: $25M
  Bucket 40: $20M
  Bucket 35: $80M (B's own)
  Bucket 30: $35M
  Bucket 20: $100M (C's own; fully covers)
  Bucket 15: $15M
```

**Round 1, Iteration 1:** All Primes tug their own bucket (distance 0 = max value).
- Bucket 50: A tugs $10M, available $60M → A gets $10M
- Bucket 35: B tugs $10M, available $80M → B gets $10M
- Bucket 20: C tugs $10M, available $100M → C gets $10M

**Subsequent rounds:** Primes continue draining their own bucket. Eventually A's bucket 50 is empty; A tugs UP at bucket 55 (preferred over DOWN at 45 — same distance, but UP value = 1.0 vs DOWN value = 45/50 = 0.9). Rounds continue until all needs met or all capacity exhausted.

For full algorithm details on collision pro-rata, redirect rules, and edge cases, the trace above is illustrative; the formal mechanism is the same as in the pre-synlang `tugofwar.md`.

---

## 6. Trading among Primes (Phase 2 of allocation)

After Phase 1, all Primes have fulfilled their capacity needs but some may hold lower-tier capacity. Phase 2 allows upgrades.

### When trading activates

A Prime enters trading mode when:
1. Capacity need is fully met
2. It holds some lower-tier capacity (from buckets below its own)
3. Excess capacity exists in buckets above it

### Mechanics

```
For each Prime with lower-tier capacity:

  1. Tug at nearest bucket ABOVE with remaining excess
     (using same tug formulas — base + distance decay)

  2. For each unit of higher-tier capacity gained:
       Identify your LOWEST-value capacity currently held
       Release that capacity downward
       Send it to the HIGHEST bucket below that can use it

  3. Recipients of sent-down capacity either:
       Apply it to unmet need (if any), or
       Trade it themselves (if they also have lower-tier capacity)
```

### Cascade effect

```
Example:
  Prime A (bucket 50) holds capacity from bucket 35
  → A tugs at bucket 55, gets higher-tier capacity
  → A releases its bucket-35 capacity downward
  → Prime B (bucket 40) receives it — bucket-35 is lower-tier for B too
  → B trades: tugs at bucket 45, releases bucket-35 further down
  → Prime C (bucket 30) receives it — bucket-35 is HIGHER-tier for C (value!)
  → Cascade terminates
```

### Overreach trading

Special case: a Prime tugging at a distant higher bucket while another Prime sits between them holding intermediate capacity.

```
Setup:
  Prime A at bucket 30, tugging at bucket 50
  Prime B at bucket 40, holding capacity from bucket 35
  Bucket-35 capacity is "lower-tier" for B (below its bucket 40)
  Bucket-35 capacity is "higher-tier" for A (above its bucket 30)
```

A is "reaching past" B. But A would be equally happy with bucket-35 capacity (both bucket 35 and bucket 50 are higher-tier for A — effective value 1.0 either way). B is unhappy holding bucket-35 (lower-tier, requires gap capital).

**Overreach trade execution:**
1. Prime A offers its highest-tier capacity to Prime B (some bucket-50 capacity it just obtained)
2. Prime B gives Prime A its lower-tier capacity (bucket-35)
3. Both benefit:
   - A: still has higher-tier capacity (bucket 35 ≈ bucket 50 for matching purposes)
   - B: upgraded from bucket-35 to bucket-50 (no more gap capital)

Pareto-improving: one strictly benefits, the other is indifferent.

---

## 7. Excess capacity → SDR auction

After tug-of-war and trading, calculate remaining capacity per bucket. The excess goes to the **SDR auction**, which allocates it to bidders that didn't have prior reservations.

```
For each bucket N:
  Excess[N] = Lindy[N] − Consumed by reservations[N]

Bids from non-reservation Primes match against Excess[N] at clearing price.
```

If Lindy < total reservations for some bucket, excess = 0 (no auction; shortfall handled by tug-of-war pro-rata).

---

## 8. Tug strength formulas — summary table

| Quantity | Formula |
|---|---|
| Base Tug | `MAX(Remaining Need × Tug Rate, Reservation × Min Tug Floor)` |
| Distance Penalty | `MAX((Distance Decay)^Distance, Min Distance Factor)` |
| Effective Tug | `Base Tug × Distance Penalty` |
| Tug UP value | `Effective Tug × 1.0` |
| Tug DOWN value | `Effective Tug × (Target Bucket / Your Bucket)` |

| Parameter | Default | Description |
|---|---|---|
| Tug Rate | 10% | Portion of remaining need tugged per round |
| Min Tug Floor | 1% | Minimum tug as % of reservation (prevents dust) |
| Distance Decay | 0.9 | Multiplier per bucket of distance |
| Min Distance Factor | 0.10 | Floor for distance penalty |
| Max Iterations | 10 | Cap on redirects per round |
| Max Rounds | 100 | Cap on total rounds |

---

## 9. Capacity retention rules

When you pull capacity from another bucket:

| Pull Direction | SDR Bucket Tenor |
|---|---|
| **Tug UP** | Retains source bucket tenor (beneficial — you get higher-than-needed SDR) |
| **Tug DOWN** | Retains source bucket tenor (creates gap — source tenor < your bucket; gap capital required) |

**Example.** Prime at bucket 40 tugs DOWN from bucket 30 → gets capacity at bucket 30 tenor → 10-bucket gap → gap capital required for this portion.

---

## 10. Secondary market

Reservation holders can trade their reservations:
- Sell full or partial amounts
- Time-slice (sell epochs 5–10 of a 20-epoch reservation)
- Buyers get the same rights as original auction winners

Enables price discovery between auctions. Settlement details (exact daily cycle vs continuous) deferred to the Phase 9+ auction implementation.

---

## 11. Synlang form

Following the patterns in `noemar-synlang/topology.md` and `macrosynomics/beacon-framework.md`:

- **Submissions** as signed verb invocations through `&core.syngate`:
  - `(submit-osrc-bid …)`, `(submit-sdr-bid …)`, `(release-reservation …)`, `(trade-reservation …)`
- **Bid atoms** in the relevant Generator auction Space (sealed until processing window opens)
- **Matching** as synart-resolved code in `&core.loop.synserv` (in-space calculation per `noemar-synlang/listener-loops.md`)
- **Allocation outputs** as `(sdr-allocation $prime $bucket $amount $epoch)` atoms for SDR — same shape as the Phase 1 temporary SDR auction; only the body/source changes

Vocabulary: auction submission is an `auction-{x}` beacon (relay class). Pre-synlang docs used the JSON bid-message format; the current form is synlang verb-call shape.

---

## 12. Connection to risk framework

Per [`risk-framework/matching.md`](../risk-framework/matching.md), hold-to-par matching protects against **credit-spread risk**, not interest-rate risk:

| Sub-book | Covers credit-spread? | Covers rate? | Liability matched against |
|---|---|---|---|
| `termbook` | Yes (held to par) | Yes (matched fixed/fixed) | tUSDS-issued YT (Yield Tokens) |
| `structbook` | Yes (held to par) | Yes for SDR-matched P1 positions; future forms may require explicit rate hedge if the liability match does not cover rate | Structural USDS demand (SDR) |

Once allocated, capacity is consumed by the structbook (and termbook once tUSDS is live) per the matched/unmatched blend in [`risk-framework/primebook-composition.md`](../risk-framework/primebook-composition.md) §4. The blend shifts smoothly: when capacity shrinks, more position size falls into the unmatched portion; when capacity grows, more is matched. Capital requirement updates continuously — no binary "transition" event.

---

## 13. Open parameters

- **Tug rate** — 10% default; needs empirical calibration
- **Distance decay** — 0.9 default; empirical
- **Iteration limits** — max 10 per round, max 100 rounds
- **Cascade depth limits** — should there be a max cascade depth to prevent complexity?
- **Trading order** — should overreach trades happen before or after cascade trading?
- **Edge cases** — what happens with extreme Lindy shifts (e.g., all capacity disappears)?
- **Reservation term limits** — max reservation term in epochs (365 days? longer?)
- **Secondary market mechanics** — same daily cycle or continuous settlement?
- **Bid increments / spam control** — minimum bid sizes or rate increments

---

## File map

| Doc | Relationship |
|---|---|
| [`README.md`](lani/accounting/README.md) | Accounting directory index |
| [`settlement-cycle.md`](settlement-cycle.md) | OSRC + SDR submission flow runs on the same daily cadence |
| [`capital-stack.md`](capital-stack.md) | OSRC capacity feeds SRC ingression; SRC ingression depends on the JRC base |
| [`../risk-framework/sdr-model.md`](../risk-framework/sdr-model.md) | Lindy SDR + SDR policy overlay; bucket structure; P1 temporary SDR auction; Phase 9+ activation |
| [`../risk-framework/matching.md`](../risk-framework/matching.md) | Credit-spread vs rate distinction; termbook vs structbook |
| [`../risk-framework/primebook-composition.md`](../risk-framework/primebook-composition.md) | structbook / termbook capacity consumption; matched/unmatched blend |
| [`../roadmap/phase-1-spaces.md`](../roadmap/phase-1-spaces.md) | Phase 1 carve-out: synserv-triggered temporary SDR auction in `&entity.generator.usge.sdr-auction` |
| [`../noemar-synlang/topology.md`](../noemar-synlang/topology.md) | Entart subtree structure for the Generator's structural-demand subtree |
| [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) | Auction beacons as relay-class subkind (`auction-{x}` stem); legacy `lpha-auction` glossary entry |

---

## One-line summary

**SDR capacity per bucket is computed by the lot-age surface, Lindy SDR, and the SDR policy overlay in the Generator's structural-demand subtree, allocated in Phase 1 by a synserv-triggered ownership-weighted temporary SDR auction and from Phase 9+ by sealed-bid OSRC and SDR auctions plus a tug-of-war among existing reservations followed by trading and an excess-capacity auction — with bids as synlang verb calls, matching as synserv-run in-space code, and the same `(sdr-allocation …)` atom shape consumed downstream by `structbook` and `termbook` regardless of source.**
