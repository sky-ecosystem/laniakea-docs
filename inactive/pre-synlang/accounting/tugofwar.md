# Duration Capacity Tug-of-War Mechanism

**Status:** Draft
**Last Updated:** 2026-01-27

---

## Overview

When Lindy-measured duration capacity doesn't match reservations, all capacity must be allocated through tugging. The Tug-of-War mechanism allocates capacity fairly based on need, distance, and effective value.

**Two phases:**
1. **Phase 1: Tug-of-War** — Primes tug on all buckets (including their own) to fill their need
2. **Phase 2: Trading** — Primes upgrade their capacity mix by trading up and cascading down

**Key insight:** Primes tug at their own bucket with distance 0 (no decay), so they naturally have priority there. But if their bucket is empty and a neighbor is full, they're not at a huge disadvantage — they can still tug nearby buckets effectively.

### Bucket Structure

The duration system uses **101 buckets**, each representing **15 days**. Bucket 0 = 0 days (immediate liquidity), bucket 84 = 1,260 days (JAAA CLO AAA), bucket 100 = 1,500+ days (structural/permanent). Distance decay is per-bucket, so distance 1 = 15 days, distance 5 = 75 days. See `../risk-framework/duration-model.md` for the full bucket table and structural caps.

### Phase Dependencies

Tug-of-war is a **Phase 9+** mechanism. In Phases 3–8 (pre-auction mode), governance allocates duration capacity directly — no tug-of-war, no excess auction. Tug-of-war activates when `stl-base` enables reservation-based auctions (Phase 9). See `daily-settlement-cycle.md` for how the settlement cycle handles both pre-auction and auction modes.

---

## Core Concepts

### Tug Strength

Each Prime with unmet need exerts "tug" on nearby buckets with excess capacity.

```
Base Tug = MAX(Remaining Need × Tug Rate, Reservation × Min Tug Floor)

Where:
- Remaining Need = Reserved amount - Already allocated
- Tug Rate = 10% per round
- Min Tug Floor = 1% of reservation (prevents infinitely small amounts)
```

The minimum floor ensures dust amounts eventually get cleaned up rather than requiring infinite rounds.

### Distance Decay

Tug strength decays with distance, but with a floor to prevent infinitely small values.

```
Distance Penalty = MAX((Distance Decay)^Distance, Min Distance Factor)

Effective Tug = Base Tug × Distance Penalty

Where:
- Distance = |Your bucket - Target bucket|
- Distance Decay = 0.9 (10% decay per bucket)
- Min Distance Factor = 0.10 (90% max penalty, regardless of distance)
```

This means even very distant buckets can still be tugged at 10% strength, preventing scenarios where distance makes amounts infinitesimally small.

**Example:**
```
Prime at bucket 40, needs $100M, tugging at bucket 45:
- Base Tug = $100M × 10% = $10M
- Distance = 5
- Effective Tug = $10M × (0.9)^5 = $10M × 0.59 = $5.9M
```

### Effective Value

Tugging UP (higher buckets) and tugging DOWN (lower buckets) have different value:

| Direction | Effective Value | Rationale |
|-----------|-----------------|-----------|
| **Tug UP** | 1.0 | Higher bucket = full match or better, no gap capital |
| **Tug DOWN** | Target Bucket / Your Bucket | Lower bucket = gap capital required, value degrades |

```
Tug UP value = Effective Tug × 1.0
Tug DOWN value = Effective Tug × (Target Bucket / Your Bucket)
```

**Example:**
```
Prime at bucket 40:
- Tug UP at bucket 45: value = $5.9M × 1.0 = $5.9M
- Tug DOWN at bucket 35: value = $5.9M × (35/40) = $5.2M

→ Prime prefers tugging UP (higher effective value)
```

### Strategic Choice

Primes tug in the direction with highest effective value first. This naturally causes:
- Primes to prefer nearby high buckets over distant high buckets
- Primes to prefer nearby low buckets over distant high buckets (at some crossover point)
- Primes to compete for valuable excess capacity

---

## The Algorithm

### Phase 1: Tug-of-War

All capacity starts in the available pool. Primes tug to claim capacity, including from their own bucket (distance 0).

Multiple **rounds**, each round has multiple **iterations**.

#### Initial State

```
For each bucket N:
  Available[N] = min(Lindy[N], Structural Cap[N])

For each Prime:
  Remaining Need = Reserved amount (nothing allocated yet)
```

#### Round Structure

```
For each round until no unmet need or no available capacity remains:

  Iteration 1:
    Each Prime with unmet need declares tug on highest-value bucket
    Resolve collisions (pro-rata if contested)
    Mark allocated buckets as "touched" for this round
    Primes with unsatisfied tug continue to Iteration 2

  Iteration 2:
    Primes redirect unsatisfied tug to next-highest-value UNTOUCHED bucket
    Resolve collisions
    Mark newly allocated buckets as "touched"
    Continue until no more redirects possible

  Update remaining needs
  Reset "touched" status for next round
```

#### Collision Resolution

When multiple Primes tug at the same bucket:

```
Total Tug = Sum of all Effective Tugs on this bucket
Available = Excess capacity in bucket

If Total Tug <= Available:
  Everyone gets their full Effective Tug
Else:
  Pro-rata: Each Prime gets (Their Tug / Total Tug) × Available
  Unsatisfied remainder can redirect to untouched buckets
```

#### Redirect Rules

1. **Only redirect unsatisfied portion** — If you got partial allocation, only the remainder redirects
2. **Only to untouched buckets** — Cannot redirect to a bucket already allocated this round
3. **Recalculate effective value** — Next-best option based on remaining untouched buckets
4. **Strength continues to decay** — The redirect uses whatever tug strength you had left

#### Iteration Limit

To prevent infinite loops, cap iterations per round (e.g., max 10 iterations). In practice, convergence should happen quickly since:
- Each iteration touches new buckets
- Tug strength is small relative to capacity
- Eventually all excess is allocated or all needs are met

---

## Worked Example

### Setup

```
Primes:
- Prime A: bucket 50, reserved $100M
- Prime B: bucket 35, reserved $100M
- Prime C: bucket 20, reserved $100M

Available capacity:
- Bucket 50: $60M (A's own bucket, but not enough for full reservation)
- Bucket 55: $30M
- Bucket 45: $25M
- Bucket 40: $20M
- Bucket 35: $80M (B's own bucket)
- Bucket 30: $35M
- Bucket 20: $100M (C's own bucket, fully covers C's need)
- Bucket 15: $15M

Parameters:
- Tug Rate: 10%
- Distance Decay: 0.9 per bucket
```

### Round 1

**Iteration 1: Initial tugs**

Prime A (bucket 50, needs $100M):
```
Base Tug = $100M × 10% = $10M

Options (by effective value):
- Bucket 50 (0 distance): $10M × 0.9^0 × 1.0 = $10M value ← OWN BUCKET, BEST
- Bucket 55 (5 up): $10M × 0.9^5 × 1.0 = $5.9M value
- Bucket 45 (5 down): $10M × 0.9^5 × (45/50) = $5.3M value

→ A tugs at bucket 50 (own bucket) with effective tug $10M
```

Prime B (bucket 35, needs $100M):
```
Base Tug = $100M × 10% = $10M

Options (by effective value):
- Bucket 35 (0 distance): $10M × 0.9^0 × 1.0 = $10M value ← OWN BUCKET, BEST
- Bucket 40 (5 up): $10M × 0.9^5 × 1.0 = $5.9M value
- Bucket 30 (5 down): $10M × 0.9^5 × (30/35) = $5.1M value

→ B tugs at bucket 35 (own bucket) with effective tug $10M
```

Prime C (bucket 20, needs $100M):
```
→ C tugs at bucket 20 (own bucket) with effective tug $10M
```

**Resolution:**
- Bucket 50: A tugs $10M, available $60M → A gets $10M
- Bucket 35: B tugs $10M, available $80M → B gets $10M
- Bucket 20: C tugs $10M, available $100M → C gets $10M

All Primes tug their own bucket first (distance 0 = max value).

### Round 2

**Updated state:**
```
- A: needs $100M - $10M = $90M
- B: needs $100M - $10M = $90M
- C: needs $100M - $10M = $90M

Remaining capacity:
- Bucket 50: $50M
- Bucket 55: $30M
- Bucket 45: $25M
- Bucket 40: $20M
- Bucket 35: $70M
- Bucket 30: $35M
- Bucket 20: $90M
- Bucket 15: $15M
```

**Iteration 1:**

All Primes still prefer their own bucket (distance 0, best value):
- A tugs bucket 50: $9M
- B tugs bucket 35: $9M
- C tugs bucket 20: $9M

*...rounds continue, each Prime draining their own bucket first...*

### Later Rounds (A's bucket depleted)

Eventually bucket 50 is empty. Now A must look elsewhere:

```
A (bucket 50, still has need remaining):

Options (by effective value):
- Bucket 55 (5 up): tug × 0.9^5 × 1.0 = 0.59 × tug
- Bucket 45 (5 down): tug × 0.9^5 × (45/50) = 0.53 × tug

→ A tugs at bucket 55 (higher bucket preferred)
```

If B still has plenty in bucket 35, B continues tugging there while A starts pulling from 55.

*...rounds continue until all needs met or all capacity exhausted...*

---

### Phase 2: Trading

After Phase 1 (tug-of-war), all Primes have fulfilled their capacity needs. However, some Primes may be holding lower-tier capacity (from lower buckets) when higher-tier capacity still exists above them. Phase 2 allows Primes to upgrade their capacity mix through trading.

#### When Trading Activates

A Prime enters trading mode when:
1. Its capacity need is fully met (no unmet need remaining)
2. It holds some lower-tier capacity (from buckets below its own)
3. Excess capacity exists in buckets above it

#### Trading Mechanics

```
For each Prime with lower-tier capacity:

  1. Tug at nearest bucket ABOVE with remaining excess
     (using same tug strength and distance decay formulas)

  2. For each unit of higher-tier capacity gained:
     - Identify your LOWEST-value capacity currently held
     - Release that capacity downward
     - Send it to the HIGHEST bucket below that can use it

  3. Recipients of sent-down capacity either:
     - Apply it to unmet need (if any remains), or
     - Trade it themselves (if they also have lower-tier capacity)
```

#### Cascade Effect

Trading can trigger cascades:

```
Example:
- Prime A (bucket 50) holds capacity from bucket 35
- Prime A tugs at bucket 55, gets higher-tier capacity
- Prime A releases its bucket-35 capacity downward
- Prime B (bucket 40) receives it — but bucket-35 is lower-tier for B too
- Prime B trades: tugs at bucket 45, releases bucket-35 further down
- Prime C (bucket 30) receives it — bucket-35 is HIGHER-tier for C (value!)
- Cascade terminates
```

The cascade continues until the released capacity reaches a Prime for whom it's not lower-tier, or until it falls below all Primes.

#### Trading Tug Strength

Trading uses the same tug mechanics as Phase 1:
- Base Tug with minimum floor
- Distance decay with minimum factor
- Pro-rata collision resolution

The difference is that trading Primes aren't filling unmet need — they're upgrading their capacity mix.

---

### Overreach Trading

A special case occurs when a Prime is tugging at a distant higher bucket while another Prime sits between them holding intermediate capacity.

#### The Overreach Scenario

```
Setup:
- Prime A at bucket 30, tugging at bucket 50
- Prime B at bucket 40, holding capacity from bucket 35
- Bucket-35 capacity is "lower-tier" for Prime B (below its bucket 40)
- Bucket-35 capacity is "higher-tier" for Prime A (above its bucket 30)

Insight:
- Prime A is "reaching past" Prime B to get bucket-50 capacity
- But Prime A would be equally happy with bucket-35 capacity (both are higher-tier for A)
- Prime B is unhappy holding bucket-35 capacity (it's lower-tier for B, requires gap capital)
```

#### Overreach Trade Execution

When an overreaching Prime and an intermediate Prime can both benefit:

```
Overreach Trade:
1. Prime A offers its HIGHEST-tier capacity to Prime B
   (e.g., some bucket-50 capacity it just obtained)

2. Prime B gives Prime A its lower-tier capacity
   (e.g., bucket-35 capacity that requires gap capital for B)

3. Both benefit:
   - Prime A: still has higher-tier capacity (35 ≈ 50 for matching purposes, both above 30)
   - Prime B: upgraded from bucket-35 to bucket-50 capacity (no more gap capital)
```

#### Why This Works

For the overreaching Prime (A at bucket 30):
- Any capacity from bucket ≥ 30 counts as "higher-tier" (effective value = 1.0)
- Bucket 35 and bucket 50 are equivalent from A's perspective
- Trading bucket-50 for bucket-35 costs A nothing

For the intermediate Prime (B at bucket 40):
- Bucket-35 capacity has effective value = 35/40 = 0.875 (lower-tier, gap capital needed)
- Bucket-50 capacity has effective value = 1.0 (higher-tier, no gap)
- The trade strictly improves B's position

#### Detection and Execution

```
For each overreaching tug (Prime A tugging bucket N above intermediate Prime B):

  If Prime B holds capacity from bucket M where:
    - M < B's bucket (lower-tier for B)
    - M > A's bucket (higher-tier for A)

  Then execute overreach trade:
    - A gives B some of A's capacity from buckets > M
    - B gives A equivalent amount from bucket M
```

Overreach trades are Pareto-improving: one party strictly benefits, the other is indifferent.

---

## Capacity Retention Rules

When you pull capacity from another bucket:

| Pull Direction | Capacity Duration |
|----------------|-------------------|
| **Tug UP** | Retains source bucket duration (beneficial — you get higher-than-needed duration) |
| **Tug DOWN** | Retains source bucket duration (creates gap — source duration < your bucket) |

**Example:**
- Prime at bucket 40 tugs down from bucket 30
- Gets capacity at bucket 30 duration
- Has 10-bucket gap → gap capital required for this portion

---

## Properties of the Mechanism

### Fairness

1. **Distance-based priority** — Closer Primes get more from nearby excess
2. **Pro-rata on collision** — No arbitrary ordering when multiple Primes want same bucket
3. **Value-based strategy** — Primes naturally optimize for their best outcome

### Efficiency

1. **Capacity flows to where it's valued** — Higher-bucket Primes get higher-bucket excess
2. **No waste** — All excess eventually allocated (if there's demand)
3. **Pareto-improving** — Redistribution makes some better off, none worse off

### Predictability

1. **Deterministic** — Same inputs → same outputs
2. **No gaming** — Small tug strength eliminates first-mover advantage
3. **Convergent** — Algorithm terminates in bounded iterations

---

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| **Tug Rate** | 10% | Portion of remaining need tugged per round |
| **Min Tug Floor** | 1% | Minimum tug as % of reservation (prevents dust) |
| **Distance Decay** | 0.9 | Multiplier per bucket of distance (10% decay) |
| **Min Distance Factor** | 0.10 | Floor for distance penalty (90% max decay) |
| **Max Iterations** | 10 | Cap on redirects per round |
| **Max Rounds** | 100 | Cap on total rounds |

The floor parameters ensure convergence:
- **Min Tug Floor** prevents infinitely small tug amounts as remaining need shrinks
- **Min Distance Factor** prevents infinitely small effective tugs at distant buckets

Together, these guarantee that dust amounts get cleaned up in bounded iterations rather than requiring infinite rounds.

---

## Connection to Risk Framework

The Tug-of-War mechanism is part of the daily duration capacity allocation process (ALDM):

1. **Lindy Measurement** — Calculate liability duration distribution
2. **Structural Caps** — Apply governance caps per bucket
3. **Tug-of-War** — All Primes tug for capacity, including their own bucket (Phase 1)
4. **Trading** — Upgrade capacity mix, cascade excess downward (Phase 2)
5. **Capital Calculation** — Apply Risk Framework formulas based on final allocation

See `../risk-framework/README.md` for the broader capital requirement framework.

---

## Open Questions

1. **Parameter calibration** — What tug rate and decay values produce best behavior?
2. **Edge cases** — What happens with extreme Lindy shifts (e.g., all capacity disappears)?
3. **Trading order** — Should overreach trades happen before or after cascade trading?
4. **Cascade depth limits** — Should there be a max cascade depth to prevent complexity?

---

*This document describes the duration capacity redistribution mechanism. For the broader risk framework, see `../risk-framework/README.md`.*
