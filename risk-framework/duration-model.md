# Duration Model (Demand Side)

**Status:** Draft (Phase 3 update, 2026-05-05)
**Last Updated:** 2026-05-05

Liability duration analysis for `structbook` and `termbook` matching. Determines how much of the USDS liability base is short-term (could demand liquidity soon) versus long-term (sticky, unlikely to redeem). Capacity flows into Primebook sub-book matching per [`primebook-composition.md`](primebook-composition.md).

Companion to:
- [`primebook-composition.md`](primebook-composition.md) — `structbook` and `termbook` consume duration capacity
- [`matching.md`](matching.md) — credit-spread vs rate distinction; how capacity is consumed
- [`asset-classification.md`](asset-classification.md) — Stressed Pull-to-Par split into credit-spread vs rate duration

---

## Architectural placement

Structural demand for USDS holding lives in the **Generator's entart**:

```
&entity-generator-usge-root
  └── &entity-generator-usge-structural-demand
        ├── &entity-generator-usge-structural-demand-scrapers   ← grounded scraper outputs
        └── &entity-generator-usge-structural-demand-auction    ← capacity allocation
```

This is where:
- Scrapers populate raw lot-age data (USDS, DAI, sUSDS holders)
- Lindy + structural-cap math computes per-bucket capacity
- Auction (or fake-auction in v1) distributes capacity across Primes

**Phase 1 manual-allocation carve-out:** v1 uses manual governance-set capacity (Lindy + structural caps from existing parameters; data-team scraper will replace later). Equal-split distribution across the 3 Star Primes (Spark/Grove/Keel) per bucket. Real-time scraping and auctions come online in later phases.

---

## Liability Duration Analysis (Demand Side)

### Purpose

Determine how much of the USDS liability base is short-term (could demand liquidity soon) versus long-term (sticky, unlikely to redeem). The output is per-bucket capacity — how much of the liability base can be used to cover assets at each duration tier.

### Method: Lindy Duration Model

For each lot of USDS:
1. Measure current age (time since last transfer)
2. Expected remaining holding time = current age × Lindy factor
3. Apply conservative haircut (e.g., 0.5× or 0.7× instead of 1× pure Lindy)

### Duration Bucket Structure

The Duration Bucket system uses a two-layer capacity calculation:
1. **Daily Lindy Measurement** — dynamic calculation of liability duration distribution
2. **Structural Maximum Caps** — governance-set upper limits per bucket, derived from empirical bank run research

#### Bucket Definitions

The system uses **101 buckets**, each representing **15 days**:

| Bucket | Duration | Bucket | Duration |
|--------|----------|--------|----------|
| 0 | 0 days | 50 | 750 days |
| 1 | 15 days | ... | ... |
| 2 | 30 days | 84 | 1,260 days (JAAA) |
| ... | ... | 100 | 1,500+ days |

**Bucket semantics:**
- **Liability side:** Bucket N contains liabilities with expected remaining duration ≥ N × 15 days
- **Asset side:** Bucket N is required for assets with SPTP (Stressed Pull-to-Par) in the range [(N-1) × 15, N × 15) days
- **Bucket 100:** Captures all liabilities with expected duration ≥ 1,500 days (the structural/permanent base)

#### Structural Maximum Caps: Double Exponential Model

The structural caps follow a **double exponential decay** model calibrated to empirical bank run data:

```
Individual Cap(t) = A × e^(-λ₁ × t) + B × e^(-λ₂ × t)
```

**Research-Calibrated Parameters:**

| Parameter | Value | Meaning |
|---|---|---|
| **A** | 10% | Hot money amplitude |
| **λ₁** | 0.35 | Hot money decay rate (half-life = 1.0 months) |
| **B** | 0.70% | Sticky money amplitude |
| **λ₂** | 0.0175 | Sticky money decay rate (half-life = 19.8 months) |

**Empirical Calibration Basis:**

The parameters were fitted to match the aggressive end of empirical bank run research:

| Horizon | Target | Empirical Basis |
|---|---|---|
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

#### Key Checkpoints

| Horizon | Bucket | Cumulative | ~% Gone | Interpretation |
|---|---|---|---|---|
| **30 days** | 2 | 75.2% | 25% | Acute stress phase |
| **90 days** | 6 | 54.6% | 45% | Peak stress; nearly half gone |
| **180 days** | 12 | 44.8% | 55% | Post-acute; committed holders remain |
| **360 days** | 24 | 35.8% | 64% | Survived full stress cycle |
| **720 days** | 48 | 23.5% | 76% | Structural holders only |
| **1,080 days** | 72 | 15.5% | 85% | Deep Lindy territory |
| **1,260 days (JAAA)** | 84 | 12.6% | 87% | Duration capacity for CLO AAA |
| **1,500+ days** | 100 | 9.5% | 90% | Permanent/structural base |

*Note: These caps represent maximum allowable allocation even if Lindy measurement suggests higher capacity. Governance may adjust parameters based on observed USDS holder behavior.*

#### Two-Layer Capacity Calculation

**Layer 1: Daily Lindy Measurement.** Every day, measure USDS lot ages and calculate expected remaining duration to produce a "raw" liability distribution.

**Layer 2: Apply Structural Caps.** For each bucket from longest to shortest:

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
- Lindy says bucket 48 (720 days) has $500M (5% of portfolio)
- Bucket 48 cap is 2% = $200M
- Result: Bucket 48 gets $200M, remaining $300M trickles to bucket 45 (675 days)
- If bucket 45 also exceeds its cap after adding overflow, it trickles further down

#### Conservative Rounding Rules

| Side | Rule | Rationale |
|---|---|---|
| **Liabilities** | Round DOWN to nearest bucket | A 40-day liability → bucket 2 (30 days). Conservative: assumes earlier redemption. |
| **Assets** | Round UP to nearest bucket | An asset with 1,250-day SPTP → bucket 84 (1,260 days). Conservative: requires longer-duration liabilities. |

#### Cumulative Capacity for Matching

An asset can match against its required bucket AND all higher buckets. Higher-tier capacity can always fulfill lower-tier requirements.

**Example:**
- An asset with 360-day SPTP requires bucket 24
- Available capacity = bucket 24 + bucket 30 + bucket 36 + ... + bucket 48 (cumulative)
- A 720-day liability can match a 360-day asset (but not vice versa)

```
Cumulative Capacity at Bucket N = Σ (Effective Capacity for all buckets ≥ N)
```

---

## Capacity feeds Primebook `structbook`

The Generator's structural-demand atoms produce `(structural-demand-capacity bucket-N <amount>)` per bucket. These flow into:
- `structbook` matching: positions matched against structural USDS demand (per [`primebook-composition.md`](primebook-composition.md))
- The matching mechanics: cumulative capacity per [`matching.md`](matching.md)
- Smooth blending of matched/unmatched portions per the optimization-shaped sub-book pattern

---

## Capacity Reservation System (Phase 9+)

> **Phase note:** The tug-of-war mechanism and duration auctions described below are **Phase 9+ features**. Prior phases use manual, governance-directed duration matching allocations.

Duration Bucket capacity is allocated to Primes through a reservation system. Primes acquire reservations via daily auctions, then can resell them on a secondary market.

### Core Principles

1. **Own-bucket priority is emergent** — Primes tug at their own bucket with distance 0 (no decay), giving them natural priority without a separate allocation phase
2. **All capacity allocated via tug-of-war** — When Lindy doesn't match reservations, the tug-of-war mechanism redistributes capacity to Primes with unmet need
3. **Full secondary market flexibility** — Time-sliced ownership, partial amounts, arbitrary durations

### Daily Cycle

| Event | Frequency | Description |
|---|---|---|
| Lindy measurement | Daily | Measure USDS lot ages, calculate liability duration distribution |
| Duration auctions | Daily | Auction unreserved capacity in each bucket |
| Tug-of-war | Daily | Allocate all capacity (own-bucket priority emergent from distance-0 tugging) |
| Settlement | Daily | Process deposits, redemptions, yield distribution |

### V1 carve-outs

V1 simplifications (in lieu of the full reservation system):
- **Manual governance-set capacity** initially (Lindy + structural caps from existing parameters; data-team scraper will replace later)
- **Equal-split distribution** among the 3 Star Primes (1/3 each per bucket) — implemented as the "fake auction" pattern
- **No tug-of-war** — capacity is just split, no redistribution
- **No real auctions** — same interface as the eventual real auction will use; only the strategy changes later

The fake-auction approach lets the auction interface get built and exercised without committing to bid-evaluation logic prematurely. Same data flow, different strategy.

---

## File map

| Doc | Relationship |
|---|---|
| [`primebook-composition.md`](primebook-composition.md) | `structbook` and `termbook` consume bucket capacity for matching |
| [`matching.md`](matching.md) | How capacity is consumed; credit-spread vs rate distinction |
| [`asset-classification.md`](asset-classification.md) | SPTP split into credit-spread vs rate duration |
| [`capital-formula.md`](capital-formula.md) | Final capital computation incorporates matched/unmatched blend |
| [`open-questions.md`](open-questions.md) | USDS lot-age tracking infrastructure is one of the open items |
