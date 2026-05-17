# SDR Model (Demand Side)

**Status:** Draft (updated to Phase 1 live design, 2026-05-17)
**Last Updated:** 2026-05-17

Structural Demand Resource (SDR) analysis for `structbook` and `termbook` matching. Determines how much of the USDS liability base is short-term (could demand liquidity soon) versus long-term (sticky, unlikely to redeem). Capacity flows into Primebook sub-book matching per [`primebook-composition.md`](primebook-composition.md).

Companion to:
- [`primebook-composition.md`](primebook-composition.md) — `structbook` and `termbook` consume SDR capacity
- [`matching.md`](matching.md) — credit-spread vs rate distinction; how capacity is consumed
- [`asset-classification.md`](asset-classification.md) — Stressed Pull-to-Par split into credit-spread pull-to-par horizon vs interest-rate duration

---

## Architectural placement

Structural demand for USDS holding lives in the **Generator's entart**:

```
&entity.generator.usge.root
  ├── &entity.generator.usge.structural-demand   ← lot-age surface + effective SDR capacity atoms
  └── &entity.generator.usge.sdr-auction         ← allocation atoms / temporary SDR auction body
```

This is where:
- `structural-demand` holds the lot-age surface, Lindy SDR output, SDR policy overlay, and effective SDR bucket capacities consumed by the SDR auction
- `sdr-auction` writes per-Prime per-bucket SDR allocation atoms consumed by structbooks
- later real SDR auctions can replace the temporary allocation body without moving the structbook read path

Phase 1 computes bucket capacities from the scraped/reduced lot-age surface. Lindy SDR converts observed liability stickiness into dynamic bucket capacity, the governance-set SDR policy overlay pulls that result down through caps / haircuts / eligibility / fallback bounds, and the temporary SDR auction splits effective capacity by ownership weight. See [`../roadmap/phase-1-spaces.md`](../roadmap/phase-1-spaces.md).

---

## SDR Capacity Analysis (Demand Side)

### Purpose

Determine how much of the USDS liability base is short-term (could demand liquidity soon) versus long-term (sticky, unlikely to redeem). The output is per-bucket SDR capacity — how much of the liability base can be used to cover assets at each TTM / SPTP tier.

### Method: Lindy SDR algorithm

For each lot of USDS:
1. Measure current age (time since last transfer)
2. Expected remaining holding time = current age × Lindy factor
3. Apply conservative haircut (e.g., 0.5× or 0.7× instead of 1× pure Lindy)

### SDR Bucket Structure

The SDR Bucket system uses a two-layer capacity calculation:
1. **Daily Lindy SDR** — dynamic calculation of structural-demand capacity from the lot-age surface
2. **Structural Maximum Caps** — governance-set upper limits per bucket, derived from empirical bank run research

#### Bucket Definitions

The system uses **51 buckets**, each representing **30 days**:

| Bucket | Tenor | Bucket | Tenor |
|--------|----------|--------|----------|
| 0 | 0 days | 25 | 750 days |
| 1 | 30 days | ... | ... |
| 2 | 60 days | 42 | 1,260 days (JAAA) |
| ... | ... | 50 | 1,500+ days |

**Bucket semantics:**
- **Liability side:** Bucket N contains structural demand with expected remaining stickiness ≥ N × 30 days
- **Asset side:** Bucket N is required for assets with SPTP (Stressed Pull-to-Par) in the range [(N-1) × 30, N × 30) days
- **Bucket 50:** Captures all liabilities with expected remaining stickiness ≥ 1,500 days (the structural/permanent base)

#### SDR Policy Maximum Caps: Double Exponential Model

The SDR policy cap curve follows a **double exponential decay** model calibrated to empirical bank run data:

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
| **30 days** | 1 | 75.2% | 25% | Acute stress phase |
| **90 days** | 3 | 54.6% | 45% | Peak stress; nearly half gone |
| **180 days** | 6 | 44.8% | 55% | Post-acute; committed holders remain |
| **360 days** | 12 | 35.8% | 64% | Survived full stress cycle |
| **720 days** | 24 | 23.5% | 76% | Structural holders only |
| **1,080 days** | 36 | 15.5% | 85% | Deep Lindy territory |
| **1,260 days (JAAA)** | 42 | 12.6% | 87% | SDR capacity for CLO AAA |
| **1,500+ days** | 50 | 9.5% | 90% | Permanent/structural base |

*Note: These caps represent maximum allowable allocation even if Lindy measurement suggests higher capacity. Governance may adjust parameters based on observed USDS holder behavior.*

#### Two-Layer Capacity Calculation

**Layer 1: Lindy SDR.** Measure USDS / DAI / sUSDS / sDAI lot ages and convert them into raw SDR bucket capacity. The model discounts fragile structure such as same-age crowding, same-account concentration, churn, and low-quality sources.

**Layer 2: Apply SDR policy overlay.** For each bucket from longest to shortest:

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
- Lindy says bucket 24 (720 days) has $500M (5% of portfolio)
- Bucket 24 cap is 2% = $200M
- Result: Bucket 24 gets $200M, remaining $300M trickles to bucket 23 (690 days)
- If bucket 23 also exceeds its cap after adding overflow, it trickles further down

#### Conservative Rounding Rules

| Side | Rule | Rationale |
|---|---|---|
| **Liabilities** | Round DOWN to nearest bucket | A 40-day liability → bucket 1 (30 days). Conservative: assumes earlier redemption. |
| **Assets** | Round UP to nearest bucket | An asset with 1,250-day SPTP → bucket 42 (1,260 days). Conservative: requires stickier liabilities / higher SDR buckets. |

#### Cumulative Capacity for Matching

An asset can match against its required bucket AND all higher buckets. Higher-tier capacity can always fulfill lower-tier requirements.

**Example:**
- An asset with 360-day SPTP requires bucket 12
- Available capacity = bucket 12 + bucket 13 + ... + bucket 50 (cumulative)
- A 720-day liability can match a 360-day asset (but not vice versa)

```
Cumulative Capacity at Bucket N = Σ (Effective Capacity for all buckets ≥ N)
```

---

## Capacity feeds Primebook `structbook`

The Generator's structural-demand atoms produce `(effective-sdr-bucket-capacity $bucket $amount $epoch)` per bucket. These flow into:
- `structbook` matching: positions matched against structural USDS demand (per [`primebook-composition.md`](primebook-composition.md))
- The matching mechanics: cumulative capacity per [`matching.md`](matching.md)
- Smooth blending of matched/unmatched portions per the optimization-shaped sub-book pattern

---

## Capacity Allocation System

SDR Bucket capacity is allocated to Primes through the Generator's `sdr-auction` Space. Full real SDR auctions are Phase 9+ (`../accounting/sdr-auction.md`). P1 uses a synserv-triggered ownership-weighted temporary SDR auction that writes the same allocation atom shape real auctions will later write:

```metta
(sdr-allocation $prime $bucket $amount $epoch)
```

`structbook` consumes that atom shape and does not depend on how the allocation was produced. P1 can therefore use the simplest allocator body, while later SDR auctions, tug-of-war, upgrading, trading, or Prime strategies replace only the writer/body behind the same read path.

P1 allocator:

```text
sky_effective_ownership(p) = 0.05 + 0.95 × sky_prime_token_share(p)
ownership_weight(p) = sky_effective_ownership(p) × prime_ijrc(p)
allocation(p, bucket, epoch) = effective_sdr_bucket_capacity(bucket, epoch) × ownership_weight(p, epoch) / Σ ownership_weight(active primes, epoch)
```

The temporary ownership-weight equation lives entirely in `&entity.generator.usge.sdr-auction`. `&core.treasury` stores only raw long-term facts such as Sky's token share of each Prime. Per-Prime IJRC is read from the Prime root. Weights are recomputed each DSC epoch from the latest treasury facts and Prime IJRC atoms.

### P1 edge rules

- A Prime with missing, stale, or zero IJRC has `ownership_weight = 0` and receives zero allocation.
- Unlaunched Prime token shares still count as ownership; their values are sudoed or otherwise supplied as treasury facts until live token data exists.
- If there are no positive active Prime weights, allocations round to zero. Any rounding/dust remainder also rounds to zero. The no-active-prime state is treated as system shutdown/out-of-scope for P1 operation.
- Bucket capacities may change each epoch. The allocator applies the latest capacity atoms for that epoch.
- Allocations do not expire in the reservation-right sense and do not carry forward. Each epoch's atoms are the live SDR allocation for that epoch; prior epoch atoms are historical.
- There is no P1 reservation market, durable SDR ownership, sticky claim, capacity debt, tug-of-war, upgrade/trading path, or unused-allocation carry-forward.
- If a Prime's capacity share falls, its next-epoch matched portion can shrink; unmatched exposure grows and ER reflects the new capital requirement. Any temporary penalty forgiveness is out-of-band and does not alter ER.

### Daily Cycle

| Event | Frequency | Description |
|---|---|---|
| Treasury refresh | Daily | Refresh Sky token-share facts, including supplied values for unlaunched tokens |
| Lot-age / Lindy SDR | Daily | Refresh lot-age surface, run Lindy SDR, apply SDR policy overlay, and write effective SDR bucket capacities in `structural-demand` |
| Temporary SDR auction | Daily | Split every effective SDR bucket across active Primes by ownership weight and write allocation atoms |
| Settlement | Daily | Advance the DSC epoch; structbooks consume current-epoch allocation atoms |

P1's daily synomic settlement cycle triggers treasury refresh, lot-age surface refresh, Lindy SDR, the SDR policy overlay, and the temporary SDR auction during the 13:00-16:00 UTC processing window. Structbooks consume allocation atoms stamped with the active daily epoch.

---

## Open questions

**USDS lot-age tracking infrastructure.** Exact source universe, reducer catalog, account-clustering rules, same-age crowding discount, and data-quality fallback behavior for the lot-age surface. The P1 topology assumes this pipeline is live; implementation still needs the precise scraper/reducer contract.

---

## File map

| Doc | Relationship |
|---|---|
| [`primebook-composition.md`](primebook-composition.md) | `structbook` and `termbook` consume bucket capacity for matching |
| [`matching.md`](matching.md) | How capacity is consumed; credit-spread vs rate distinction |
| [`asset-classification.md`](asset-classification.md) | SPTP split into credit-spread pull-to-par horizon vs interest-rate duration |
| [`capital-formula.md`](capital-formula.md) | Final capital computation incorporates matched/unmatched blend |
| [`../accounting/sdr-auction.md`](../accounting/sdr-auction.md) | Target tug-of-war + OSRC and SDR auctions |
| [`../roadmap/phase-1-spaces.md`](../roadmap/phase-1-spaces.md) | Phase 1 live topology: lot-age surface, Lindy SDR, policy overlay, temporary SDR auction, structbook consumption |
