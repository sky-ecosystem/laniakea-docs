# Duration Model (Demand Side)

**Last Updated:** 2026-01-27

## Liability Duration Analysis (Demand Side)

### Purpose

Determine how much of the USDS liability base is short-term (could demand liquidity soon) versus long-term (sticky, unlikely to redeem).

### Method: Lindy-Based Demand Model

For each lot of USDS:
1. Measure current age (time since last transfer)
2. Expected remaining holding time = current age × Lindy factor
3. Apply conservative haircut (e.g., 0.5x or 0.7x instead of 1x pure Lindy)

### SPTP Bucket Structure

The SPTP bucket system uses a two-layer capacity calculation:
1. **Weekly Lindy Measurement** — Dynamic calculation of liability duration distribution
2. **Structural Maximum Caps** — Governance-set upper limits per bucket, derived from empirical bank run research

#### Bucket Definitions

The system uses **101 buckets**, each representing 0.5 months (15 days):

| Bucket | Duration | Bucket | Duration |
|--------|----------|--------|----------|
| 0 | 0 months | 50 | 25 months |
| 1 | 0.5 months | ... | ... |
| 2 | 1 month | 84 | 42 months (JAAA) |
| ... | ... | 100 | 50+ months |

**Bucket semantics:**
- **Liability side:** Bucket N contains liabilities with expected remaining duration ≥ N × 0.5 months
- **Asset side:** Bucket N is required for assets with SPTP in the range [(N-1) × 0.5, N × 0.5) months
- **Bucket 100:** Captures all liabilities with expected duration ≥ 50 months (the structural/permanent base)

#### Structural Maximum Caps: Double Exponential Model

The structural caps follow a **double exponential decay** model calibrated to empirical bank run data:

```
Individual Cap(t) = A × e^(-λ₁ × t) + B × e^(-λ₂ × t)
```

**Research-Calibrated Parameters:**

| Parameter | Value | Meaning |
|-----------|-------|---------|
| **A** | 10% | Hot money amplitude |
| **λ₁** | 0.35 | Hot money decay rate (half-life = 1.0 months) |
| **B** | 0.70% | Sticky money amplitude |
| **λ₂** | 0.0175 | Sticky money decay rate (half-life = 19.8 months) |

**Empirical Calibration Basis:**

The parameters were fitted to match the aggressive end of empirical bank run research:

| Horizon | Target | Empirical Basis |
|---------|--------|-----------------|
| 1 month | 75% | SVB lost 25% in 1 day, 87% over 2 days; First Republic lost 37% in 2 days |
| 3 months | 55% | First Republic: 57% gone by end Q1 2023; Credit Suisse: 29% deposits gone Q1 |
| 6 months | 45% | Credit Suisse: ~40% over 6 months |
| 12 months | 35% | NSFR implies 5-10% retail runoff/year, but 50%+ wholesale |
| 24 months | 25% | Beyond 1 year, only structural holders remain |
| 36 months | 15% | Deep Lindy territory |
| 50+ months | 10% | Structural/permanent base |

**Key Research Sources:**
- Basel III LCR/NSFR frameworks
- March 2023 bank runs: SVB, Signature Bank, First Republic, Credit Suisse
- MMF crisis data: September 2008 (26% in 2 weeks), March 2020 (30% in 2 weeks)
- ECB/Fed deposit behavior studies

#### Full Bucket Table

| Bucket | Months | Individual | Cumulative |     | Bucket | Months | Individual | Cumulative |
| ------ | ------ | ---------- | ---------- | --- | ------ | ------ | ---------- | ---------- |
| 0      | 0.0    | 14.4061%   | 100.0000%  |     | 51     | 25.5   | 0.3861%    | 22.3357%   |
| 1      | 0.5    | 10.4138%   | 85.5939%   |     | 52     | 26.0   | 0.3794%    | 21.9496%   |
| 2      | 1.0    | 7.5959%    | 75.1801%   |     | 53     | 26.5   | 0.3728%    | 21.5703%   |
| 3      | 1.5    | 5.6057%    | 67.5843%   |     | 54     | 27.0   | 0.3663%    | 21.1975%   |
| 4      | 2.0    | 4.1988%    | 61.9786%   |     | 55     | 27.5   | 0.3600%    | 20.8312%   |
| 5      | 2.5    | 3.2031%    | 57.7798%   |     | 56     | 28.0   | 0.3537%    | 20.4712%   |
| 6      | 3.0    | 2.4972%    | 54.5766%   |     | 57     | 28.5   | 0.3476%    | 20.1175%   |
| 7      | 3.5    | 1.9956%    | 52.0794%   |     | 58     | 29.0   | 0.3415%    | 19.7699%   |
| 8      | 4.0    | 1.6381%    | 50.0838%   |     | 59     | 29.5   | 0.3356%    | 19.4284%   |
| 9      | 4.5    | 1.3821%    | 48.4457%   |     | 60     | 30.0   | 0.3298%    | 19.0928%   |
| 10     | 5.0    | 1.1977%    | 47.0637%   |     | 61     | 30.5   | 0.3241%    | 18.7630%   |
| 11     | 5.5    | 1.0639%    | 45.8660%   |     | 62     | 31.0   | 0.3185%    | 18.4389%   |
| 12     | 6.0    | 0.9658%    | 44.8020%   |     | 63     | 31.5   | 0.3129%    | 18.1204%   |
| 13     | 6.5    | 0.8930%    | 43.8362%   |     | 64     | 32.0   | 0.3075%    | 17.8075%   |
| 14     | 7.0    | 0.8379%    | 42.9432%   |     | 65     | 32.5   | 0.3022%    | 17.5000%   |
| 15     | 7.5    | 0.7955%    | 42.1053%   |     | 66     | 33.0   | 0.2969%    | 17.1978%   |
| 16     | 8.0    | 0.7621%    | 41.3098%   |     | 67     | 33.5   | 0.2918%    | 16.9009%   |
| 17     | 8.5    | 0.7350%    | 40.5477%   |     | 68     | 34.0   | 0.2867%    | 16.6091%   |
| 18     | 9.0    | 0.7125%    | 39.8127%   |     | 69     | 34.5   | 0.2817%    | 16.3224%   |
| 19     | 9.5    | 0.6933%    | 39.1002%   |     | 70     | 35.0   | 0.2769%    | 16.0407%   |
| 20     | 10.0   | 0.6764%    | 38.4069%   |     | 71     | 35.5   | 0.2721%    | 15.7638%   |
| 21     | 10.5   | 0.6613%    | 37.7305%   |     | 72     | 36.0   | 0.2673%    | 15.4918%   |
| 22     | 11.0   | 0.6474%    | 37.0692%   |     | 73     | 36.5   | 0.2627%    | 15.2244%   |
| 23     | 11.5   | 0.6345%    | 36.4218%   |     | 74     | 37.0   | 0.2581%    | 14.9617%   |
| 24     | 12.0   | 0.6223%    | 35.7874%   |     | 75     | 37.5   | 0.2537%    | 14.7036%   |
| 25     | 12.5   | 0.6106%    | 35.1651%   |     | 76     | 38.0   | 0.2493%    | 14.4499%   |
| 26     | 13.0   | 0.5994%    | 34.5545%   |     | 77     | 38.5   | 0.2449%    | 14.2007%   |
| 27     | 13.5   | 0.5886%    | 33.9550%   |     | 78     | 39.0   | 0.2407%    | 13.9557%   |
| 28     | 14.0   | 0.5781%    | 33.3664%   |     | 79     | 39.5   | 0.2365%    | 13.7151%   |
| 29     | 14.5   | 0.5679%    | 32.7883%   |     | 80     | 40.0   | 0.2324%    | 13.4786%   |
| 30     | 15.0   | 0.5579%    | 32.2204%   |     | 81     | 40.5   | 0.2284%    | 13.2461%   |
| 31     | 15.5   | 0.5481%    | 31.6625%   |     | 82     | 41.0   | 0.2244%    | 13.0178%   |
| 32     | 16.0   | 0.5385%    | 31.1144%   |     | 83     | 41.5   | 0.2205%    | 12.7934%   |
| 33     | 16.5   | 0.5291%    | 30.5759%   |     | 84     | 42.0   | 0.2167%    | 12.5728%   |
| 34     | 17.0   | 0.5199%    | 30.0468%   |     | 85     | 42.5   | 0.2129%    | 12.3561%   |
| 35     | 17.5   | 0.5109%    | 29.5269%   |     | 86     | 43.0   | 0.2092%    | 12.1432%   |
| 36     | 18.0   | 0.5020%    | 29.0160%   |     | 87     | 43.5   | 0.2056%    | 11.9340%   |
| 37     | 18.5   | 0.4933%    | 28.5140%   |     | 88     | 44.0   | 0.2020%    | 11.7284%   |
| 38     | 19.0   | 0.4847%    | 28.0207%   |     | 89     | 44.5   | 0.1985%    | 11.5263%   |
| 39     | 19.5   | 0.4763%    | 27.5360%   |     | 90     | 45.0   | 0.1951%    | 11.3278%   |
| 40     | 20.0   | 0.4680%    | 27.0597%   |     | 91     | 45.5   | 0.1917%    | 11.1327%   |
| 41     | 20.5   | 0.4599%    | 26.5917%   |     | 92     | 46.0   | 0.1884%    | 10.9410%   |
| 42     | 21.0   | 0.4519%    | 26.1318%   |     | 93     | 46.5   | 0.1851%    | 10.7526%   |
| 43     | 21.5   | 0.4441%    | 25.6799%   |     | 94     | 47.0   | 0.1819%    | 10.5675%   |
| 44     | 22.0   | 0.4364%    | 25.2358%   |     | 95     | 47.5   | 0.1787%    | 10.3856%   |
| 45     | 22.5   | 0.4288%    | 24.7995%   |     | 96     | 48.0   | 0.1756%    | 10.2068%   |
| 46     | 23.0   | 0.4214%    | 24.3707%   |     | 97     | 48.5   | 0.1726%    | 10.0312%   |
| 47     | 23.5   | 0.4141%    | 23.9493%   |     | 98     | 49.0   | 0.1696%    | 9.8586%    |
| 48     | 24.0   | 0.4069%    | 23.5352%   |     | 99     | 49.5   | 0.1667%    | 9.6890%    |
| 49     | 24.5   | 0.3998%    | 23.1284%   |     | 100    | 50.0+  | 9.5223%    | 9.5223%    |
| 50     | 25.0   | 0.3929%    | 22.7286%   |     |        |        |            |            |

**Reading the table:**
- **Individual:** Maximum % of portfolio that can be in this specific bucket alone
- **Cumulative:** Maximum % of portfolio that can be in this bucket OR higher (used for asset matching)
- **Bucket 100:** The 9.52% cumulative includes the tail beyond 50 months — the structural/permanent holder base

#### Key Checkpoints

| Horizon | Bucket | Cumulative | ~% Gone | Interpretation |
|---------|--------|------------|---------|----------------|
| **1 month** | 2 | 75.2% | 25% | Acute stress phase |
| **3 months** | 6 | 54.6% | 45% | Peak stress; nearly half gone |
| **6 months** | 12 | 44.8% | 55% | Post-acute; committed holders remain |
| **12 months** | 24 | 35.8% | 64% | Survived full stress cycle |
| **24 months** | 48 | 23.5% | 76% | Structural holders only |
| **36 months** | 72 | 15.5% | 85% | Deep Lindy territory |
| **42 months (JAAA)** | 84 | 12.6% | 87% | SPTP capacity for CLO AAA |
| **50 months+** | 100 | 9.5% | 90% | Permanent/structural base |

*Note: These caps represent maximum allowable allocation even if Lindy measurement suggests higher capacity. Governance may adjust parameters based on observed USDS holder behavior.*

#### Two-Layer Capacity Calculation

**Layer 1: Weekly Lindy Measurement**
Every week, measure USDS lot ages and calculate expected remaining duration to produce a "raw" liability distribution.

**Layer 2: Apply Structural Caps**
For each bucket from longest to shortest:
```
Raw Capacity = Lindy-measured liability amount for this bucket
Cap = Max Cap % × Total Portfolio

If Raw Capacity > Cap:
  Effective Capacity = Cap
  Overflow = Raw Capacity - Cap
  → Overflow trickles down to next-lower bucket
Else:
  Effective Capacity = Raw Capacity
```

**Example:**
- Total portfolio: $10B
- Lindy says 48mo bucket has $500M (5% of portfolio)
- 48mo cap is 2% = $200M
- Result: 48mo gets $200M, remaining $300M trickles to 45mo bucket
- If 45mo also exceeds its cap after adding overflow, it trickles further down

#### Conservative Rounding Rules

| Side | Rule | Rationale |
|------|------|-----------|
| **Liabilities** | Round DOWN to nearest bucket | A 5.5-week liability → 5wk bucket. Conservative: assumes earlier redemption. |
| **Assets** | Round UP to nearest bucket | A 3.5-year SPTP asset → 42mo bucket. Conservative: requires longer-duration liabilities. |

#### Cumulative Capacity for Matching

An asset can match against its required bucket AND all higher buckets. Higher-tier capacity can always fulfill lower-tier requirements.

**Example:**
- Asset with 12mo SPTP requires 12mo bucket
- Available capacity = 12mo + 15mo + 18mo + ... + 48mo (cumulative)
- A 48mo liability can match a 12mo asset (but not vice versa)

```
Cumulative Capacity at Bucket N = Σ (Effective Capacity for all buckets ≥ N)
```

---

### SPTP Capacity Reservation System

SPTP bucket capacity is allocated to Primes through a reservation system. Primes acquire reservations via weekly auctions, then can resell them on a secondary market.

#### Core Principles

1. **Reservations at your bucket have first claim** — You get capacity from your reserved bucket before anyone else can touch it
2. **Excess capacity redistributes via tug-of-war** — When Lindy doesn't match reservations, excess flows to Primes with unmet need
3. **Full secondary market flexibility** — Time-sliced ownership, partial amounts, arbitrary durations

#### Weekly Cycle

| Event | Frequency | Description |
|-------|-----------|-------------|
| Lindy measurement | Weekly | Measure USDS lot ages, calculate liability duration distribution |
| SPTP auctions | Weekly | Auction unreserved capacity in each bucket |
| Own-bucket allocation | Weekly | Reservations claim from their bucket first |
| Tug-of-war | Weekly | Redistribute excess capacity to unmet need |
| Settlement | Weekly | Process deposits, redemptions, yield distribution |

#### Primary Auction

Auctions occur when unreserved capacity exists at a bucket. Primes bid price-per-week for capacity amounts. Highest bidders win. Winners receive reservations starting next period.

#### Secondary Market

Reservation holders can sell portions of their ownership with time-sliced schedules. Buyers can immediately resell, enabling complex ownership structures.

#### Capacity Allocation

All capacity is allocated through tugging — there's no special "own bucket first" phase. Primes tug at their own bucket with distance 0 (no decay), giving them natural priority there. But if their bucket is empty and a neighbor is full, they can still effectively tug nearby buckets.

**Phase 1: Tug-of-War**

All Primes tug for capacity simultaneously:
- Distance 0 (own bucket) = full tug strength, maximum effective value
- Distance N = tug decays by 0.9^N (floor at 10%)
- Tugging UP = effective value 1.0
- Tugging DOWN = effective value = target/your bucket
- Collisions resolved pro-rata
- Multiple rounds until all needs met or capacity exhausted

**Phase 2: Trading**

After needs are met, Primes can trade up:
- Tug at higher buckets with remaining excess
- Release lowest-value capacity downward
- Cascade until capacity finds a Prime that values it

**See `tugofwar.md` for full algorithm details.**

#### Capacity Duration Rules

| How Acquired | Duration You Get |
|--------------|------------------|
| From own bucket (distance 0) | Your bucket's duration (full match) |
| Tugged from higher bucket | Source bucket's duration (overkill but fine) |
| Tugged from lower bucket | Source bucket's duration (creates gap → gap capital required) |

---
