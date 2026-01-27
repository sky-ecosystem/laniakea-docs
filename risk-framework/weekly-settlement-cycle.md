# Weekly Settlement Cycle

**Status:** Draft
**Last Updated:** 2026-01-27

---

## Overview

The weekly settlement cycle is the heartbeat of Laniakea's resource allocation system. It operates on a fixed weekly schedule with three distinct periods:

### Weekly Timeline

| Period | Timing | Duration | Purpose |
|--------|--------|----------|---------|
| **Measurement Period** | Tuesday 12:00 UTC → Tuesday 12:00 UTC | 7 days | Data collection, bid submission |
| **Processing Period** | Tuesday 12:00 UTC → Wednesday 12:00 UTC | 24 hours | Calculation, verification, prepayment |
| **Moment of Settlement** | Wednesday 12:00 UTC | Instant | New parameters take effect |

```
Week N                              Week N+1
│                                   │
├── Measurement Period ────────────►├── Measurement Period ──────────►
│   (Tue noon → Tue noon)           │
│                                   │
│                    ├─ Processing ─┤
│                    │  (24 hours)  │
│                    │              │
│                    Tue noon       Wed noon
│                    Bids close     Settlement
│                    Auctions       New params
│                    revealed       take effect
```

### Settlement Sequence

1. **Measurement Period** (Tue → Tue)
   - OSRC and SPTP bids submitted (sealed)
   - Interest and distributions calculated on this period's data

2. **Processing Period** (Tue noon → Wed noon)
   - Auctions revealed and matched
   - Lindy measurement snapshot
   - Tug-of-war allocation
   - SPTP excess auction
   - Prepayments made (interest, distributions)
   - Verification and compliance checks

3. **Moment of Settlement** (Wed noon)
   - New OSRC allocations take effect
   - New SPTP capacity published
   - srUSDS exchange rate updated
   - LCTS queues settle
   - Penalties begin accruing for non-compliant actors

---

## Part 1: Prime Settlement

### Timing Model

Interest payments and distribution rewards are calculated based on the **Measurement Period** (Tuesday noon → Tuesday noon), and must be **prepaid before Moment of Settlement** (Wednesday noon).

```
Measurement Period          Processing Period      Settlement
(Tue noon → Tue noon)       (Tue noon → Wed noon)  (Wed noon)
│                           │                      │
│   Data collected here     │   Calculate owed     │   Must be paid by now
│   for interest/distrib    │   Prepay amounts     │   Penalties start if late
│                           │                      │
```

### Interest Payments (Prime → Generator)

Each Prime that has borrowed from a Generator must pay interest on outstanding debt.

**Calculation (stl-base):**

```
Interest Payment = Average Outstanding Debt × Weekly Rate

Where:
- Average Outstanding Debt = time-weighted average of debt over the Measurement Period
- Weekly Rate = Annual Base Rate / 52
```

**Process:**

1. **Tuesday noon:** Measurement Period ends, calculation begins
2. **During Processing Period:** stl-base calculates interest owed
3. **Before Wednesday noon:** stl-base submits interest payment transaction
4. **Wednesday noon:** Payment must be complete; penalties accrue if late

### Distribution Rewards (Generator → Prime)

Generators distribute rewards to Primes that have "tagged" addresses — addresses that have opted into receiving distributions.

**Calculation:**

1. Generator accumulates yield from various sources (SSR spread, fees, etc.) during Measurement Period
2. Distribution amounts calculated based on tagged balances
3. Distribution flows to tagged Prime addresses proportional to their tagged balances

**Process:**

1. **Tuesday noon:** Measurement Period ends
2. **During Processing Period:** Distribution calculations performed
3. **Before Wednesday noon:** Distribution transactions submitted
4. **Wednesday noon:** Distributions must be complete

**Tagged Addresses:**

- Primes can tag addresses to receive distributions
- Tagged addresses must meet certain criteria (e.g., minimum balance, duration)
- Tagging is voluntary — untagged balances don't receive distributions

### Late Payment Penalties

Any actor that fails to complete their obligations before Moment of Settlement (Wednesday noon) incurs penalties:

```
Penalty = Owed Amount × Penalty Rate × Time Late

Where:
- Time Late = hours past Wednesday noon UTC
- Penalty Rate = governance-set rate (e.g., 0.1% per hour)
```

**Penalty mechanics:**

- Penalties accrue continuously from Moment of Settlement until payment is made
- Penalty payments flow to the affected counterparty (e.g., Generator for late interest)
- Persistent lateness (e.g., >24h) may trigger escalation (alerts, restrictions, governance review)
- Penalty history is recorded in Synome for reputation tracking

---

## Part 2: lpha-auction (Auction Sentinel)

A new Sentinel type that runs sealed-bid auctions for OSRC and SPTP capacity.

### Architecture

**Level:** Generator (one lpha-auction per Generator)
**Operator:** Accordant GovOps

**Components:**

```
┌─────────────────────────────────────────────────────────────┐
│                    lpha-auction                               │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Bid Database │  │ Auction      │  │ Settlement       │  │
│  │ (Private)    │  │ Engine       │  │ Coordinator      │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│                                                              │
│  Receives signed bids from stl-base instances               │
│  Runs matching algorithm at settlement time                  │
│  Coordinates with lpha-lcts for LCTS settlement               │
└─────────────────────────────────────────────────────────────┘
```

### Bid Submission

1. Each Prime's stl-base connects to lpha-auction
2. stl-base submits bid messages signed with its private key
3. Bids are stored in lpha-auction's private database (sealed)
4. Bids are not revealed until settlement

**Bid Message Format:**

```
{
  prime_id: <Prime identifier>,
  auction_type: "OSRC" | "SPTP",
  bucket: <bucket number for SPTP, null for OSRC>,
  amount: <capacity amount requested>,
  max_rate: <maximum rate willing to pay>,
  signature: <stl-base private key signature>,
  timestamp: <submission time>
}
```

### Security Properties

- **Sealed bids:** No participant can see others' bids before settlement
- **Authenticity:** Signatures verify bids came from legitimate stl-base instances
- **Non-repudiation:** Signed bids cannot be denied after submission
- **Timing:** Bids accepted until cutoff; late bids rejected

---

## Part 3: OSRC Auction (Originated Senior Risk Capital)

### Purpose

Allocate srUSDS capacity to Primes. Primes that win OSRC auction capacity can use Senior Risk Capital as part of their capital structure.

### Auction Mechanics

**Type:** Sealed-bid, uniform-price auction (weekly)

**Process:**

1. **Bid Collection** (before settlement)
   - Each Prime's stl-base submits sealed bids to lpha-auction
   - Bid specifies: amount of OSRC wanted, maximum rate willing to pay

2. **Capacity Determination**
   - lpha-auction queries lpha-lcts for available srUSDS capacity
   - Available capacity = current srUSDS supply + pending SubscribeQueue conversions - pending RedeemQueue conversions

3. **Matching Algorithm**
   ```
   Sort bids by max_rate descending (highest willingness to pay first)

   clearing_rate = 0
   For each bid in sorted order:
     If cumulative_amount + bid.amount <= available_capacity:
       Fully match this bid
       cumulative_amount += bid.amount
       clearing_rate = bid.max_rate  // lowest matched rate so far
     Else if cumulative_amount < available_capacity:
       Partially match this bid
       matched_amount = available_capacity - cumulative_amount
       cumulative_amount = available_capacity
       clearing_rate = bid.max_rate
       Break
     Else:
       Break (no more capacity)

   All matched bidders pay clearing_rate
   ```

4. **Settlement**
   - lpha-auction publishes results (who won, clearing rate)
   - lpha-lcts updates srUSDS exchange rate based on clearing rate
   - lpha-lcts settles LCTS queues (converts sUSDS ↔ srUSDS)

### Uniform Price Rationale

All winners pay the same rate (the clearing rate = lowest matched bid):

- **Incentive compatibility:** Bidders bid their true willingness to pay
- **No winner's curse:** You never pay more than necessary to win
- **Fairness:** Small bidders with high willingness get same rate as large bidders

**Example:**

```
Available capacity: $100M

Bids:
- Prime A: $20M at 8% max
- Prime B: $50M at 6% max
- Prime C: $40M at 5% max
- Prime D: $30M at 4% max

Matching (highest to lowest):
- Prime A: $20M matched (cumulative: $20M)
- Prime B: $50M matched (cumulative: $70M)
- Prime C: $30M matched, $10M unmatched (cumulative: $100M)

Clearing rate: 5% (Prime C's rate, the lowest matched bid)

Result:
- Prime A pays 5% for $20M (bid 8%, saves 3%)
- Prime B pays 5% for $50M (bid 6%, saves 1%)
- Prime C pays 5% for $30M (bid 5%, no savings)
- Prime D: unmatched
```

### Weekly-Only Design

**No multi-week reservations.** Every Prime must re-bid every week.

**Rationale:**

Multi-week reservations create problems:
1. **Rate lock-in distortion:** Low locked-in rates reduce effective yields
2. **Capacity mismatch:** Reserved capacity may not match actual srUSDS supply
3. **Exit incentives:** srUSDS holders leave if yields are suppressed by old reservations
4. **Complexity:** Overpayment/underpayment scenarios require complex handling

Weekly auctions provide:
- Clean price discovery every week
- Rates reflect current market conditions
- srUSDS holders see real yields, make informed decisions
- Simple, predictable system

**Trade-off:** Primes have no duration certainty on SRC access. If rates spike, they pay up or lose access. This is acceptable because:
- Primes can manage rate risk through their own capital structure
- Weekly auctions are predictable — no surprise rate changes mid-week
- Market-clearing rates reflect true cost of risk capital

### OSRC Usage

Primes that win OSRC capacity:
- Can count the SRC toward their capital requirements (per Risk Framework)
- Must pay the clearing rate weekly until they stop using SRC
- Can reduce usage at any time (no lock-in on the Prime side)

---

## Part 4: SPTP Bucket Auction

### Purpose

Allocate SPTP capacity reservations to Primes. Reservations grant the right to claim SPTP capacity when Lindy measurement provides it.

### Relationship to OSRC

SPTP and OSRC are **separate auctions** serving different purposes:

| Aspect | OSRC Auction | SPTP Bucket Auction |
|--------|--------------|---------------------|
| **What's allocated** | Senior Risk Capital capacity | Duration-matching capacity |
| **Purpose** | Capital structure (loss absorption) | Capital treatment (risk weight vs FRTB) |
| **Pricing** | Rate paid to srUSDS holders | Price paid for reservation rights |
| **Duration** | Weekly (no reservations) | Can reserve for multiple weeks |

A Prime might:
- Win OSRC capacity (to use SRC in its capital structure)
- Win SPTP capacity (to get favorable capital treatment on its assets)
- Win both, one, or neither

### Auction Sequence

The SPTP auction follows a specific sequence where tug-of-war happens FIRST, then excess is auctioned:

```
1. Bid submission window opens
2. Bids submitted (sealed)
3. Bid window closes
4. Lindy measurement (snapshot at bid close)
5. Tug-of-war processes existing reservations against Lindy capacity
6. Excess capacity identified (Lindy capacity - consumed by reservations)
7. Auction matches bids against excess capacity
8. Winners pay uniform clearing price
9. New SPTP bucket capacity published to Synome
```

**Key insight:** The auction only allocates *excess* capacity that wasn't consumed by existing reservations via tug-of-war. This ensures:
- Existing reservation holders get their capacity first
- New capacity only comes from genuine Lindy growth
- No double-allocation of the same capacity

### Auction Mechanics

**Type:** Sealed-bid, uniform-price auction (per bucket, for excess capacity only)

**Process:**

1. **Bid Collection** (before close)
   - Each Prime's stl-base submits sealed bids to lpha-auction
   - Bid specifies: bucket number, amount, maximum price, duration (weeks)

2. **Tug-of-War First**
   - Lindy measured at bid close
   - Existing reservations claim capacity via tug-of-war
   - See `tugofwar.md` for algorithm

3. **Excess Capacity Calculation** (per bucket)
   ```
   Excess Capacity[bucket] = Lindy Capacity[bucket] - Consumed by Reservations[bucket]
   ```
   - If Lindy < total reservations, excess = 0 (no auction, shortfall handled by tug-of-war)
   - If Lindy > total reservations, excess available for auction

4. **Matching Algorithm** (per bucket with excess)
   - Sort bids by max_price descending
   - Match until excess capacity exhausted
   - All winners pay clearing price (lowest matched bid)

5. **Reservation Grant**
   - Winners receive reservations for specified duration
   - Reservations tracked in lpha-auction database
   - Published to Synome

### Multi-Week Reservations

Unlike OSRC, SPTP allows multi-week reservations:

**Rationale:**
- SPTP capacity is about duration matching, which is inherently longer-term
- Primes need planning certainty for asset acquisition
- Reservations don't directly affect other participants' yields (unlike OSRC rates)

**Mechanics:**
- Bid includes duration (1-52 weeks, or longer)
- Price is per-week
- Commitment: must pay for full duration even if Lindy capacity falls short
- If Lindy < reservation in future weeks, shortfall handled by tug-of-war pro-rata

### Secondary Market

Reservation holders can trade their reservations:

- Sell full or partial amounts
- Time-slice (sell weeks 5-10 of a 20-week reservation)
- Buyers get same rights as original auction winners
- Enables price discovery between auctions

---

## Part 5: LCTS Settlement

LCTS (Liquidity Constrained Token Standard) uses a multi-generation model synchronized with the weekly settlement cycle. See `smart-contracts/lcts.md` for the specification.

### LCTS Weekly Cycle

| Event | Timing | Action |
|-------|--------|--------|
| **Generation Lock** | Tuesday 12:00 UTC | Active generation locks; new generation opens for deposits |
| **Settlement** | Wednesday 12:00 UTC | All locked generations processed proportionally |
| **Unlock** | Wednesday 12:00 UTC | Processed generations return to ACTIVE (or FINALIZED if fully converted) |

### Why Multi-Generation?

During the 24-hour Processing Period, LCTS needs to:
1. Lock deposits so auction matching is based on known quantities
2. Allow new users to deposit (into a new generation)
3. Process all pending generations at Moment of Settlement

This creates concurrent generations:
- **Locked generations** — Awaiting settlement; no deposits or withdrawals
- **Active generation** — Accepting new deposits; withdrawals allowed

### srUSDS Settlement Flow

1. **Tuesday 12:00:** lpha-lcts locks active generations
   - SubscribeQueue generation → LOCKED
   - RedeemQueue generation → LOCKED
   - New active generations created for both queues

2. **During Processing Period:**
   - lpha-auction completes OSRC auction
   - Determines clearing rate and matched amounts
   - Publishes results

3. **Wednesday 12:00:** lpha-lcts settles all locked generations
   - Updates exchange rate based on clearing rate yield
   - Calculates settlement capacity (see below)
   - Calls settle() on SubscribeQueue and RedeemQueue
   - All locked generations receive proportional capacity

### Capacity Calculation

Settlement capacity for srUSDS comes from three sources:

```
Subscribe Capacity = Net Flow Netting + OSRC Capacity (throttled by target spread)
Redeem Capacity = Net Flow Netting + Weekly Redemption Limit
```

**Step 1: Net Flow Netting**

Subscribe and redeem queues cancel each other out first:

```
SubscribeQueue total (all locked generations): $100M
RedeemQueue total (all locked generations): $30M

Net flow netting: $30M matched both ways
- $30M subscribe converts to srUSDS
- $30M redeem converts to sUSDS

Remaining after netting:
- Subscribe demand: $70M still waiting
- Redeem demand: $0 (fully processed)
```

**Step 2: Apply Additional Capacity**

For subscribes after netting:
- OSRC capacity from auction determines how much more can convert
- Subject to target spread throttling (see below)

For redeems after netting:
- Weekly redemption limit (governance-set) determines how much more can convert
- Ensures "a decent chunk" always processes each week

**Step 3: Distribute to Generations Proportionally**

When multiple locked generations exist:

```
Gen 1: $40M underlying (from 2 weeks ago)
Gen 2: $60M underlying (locked this week)

Total locked: $100M
Settlement capacity: $60M

Distribution:
- Gen 1 receives: $60M × (40/100) = $24M → $16M remains
- Gen 2 receives: $60M × (60/100) = $36M → $24M remains
```

### Target Spread Mechanism

srUSDS has a **target spread** (governance-set) above SSR. This protects yield rates from crashing:

**Subscribe capacity throttling:**

```
If OSRC auction demand provides yield ≥ target spread:
  → Allow full subscribe capacity

If OSRC auction demand would result in yield < target spread:
  → Reduce subscribe capacity to maintain target spread
  → Excess demand waits in queue for next week
```

**Example:**
```
Target spread: 2% above SSR
SubscribeQueue demand after netting: $100M
OSRC auction demand at 2.5%: Full $100M converts
OSRC auction demand at 1.5%: Only $X converts (where X maintains 2% spread)
```

**Rationale:**
- Prevents sudden rate crashes when supply exceeds auction demand
- Protects existing srUSDS holders from yield dilution
- Creates natural equilibrium between supply and demand

**Redemption capacity:**

- Fixed limit per week (governance-set)
- A "decent chunk" always processes each week
- When redemptions exceed limit, remaining users wait in queue
- Large redemptions cause rates to spike (attracting new subscribers)

### One Queue Clears Each Week

Due to net flow netting, at most one queue has leftover demand:

- If subscribe > redeem: RedeemQueue fully clears, SubscribeQueue has remainder
- If redeem > subscribe: SubscribeQueue fully clears, RedeemQueue has remainder

This means only one side ever accumulates multi-week generations.

---

## Part 6: Tug-of-War Allocation

### Timing

Tug-of-war runs as part of the SPTP auction sequence, BEFORE the auction matches bids. This ensures existing reservations get their capacity first, and only genuine excess goes to auction.

### Process

1. **Lindy Measurement** (at bid window close)
   - Measure USDS lot ages
   - Calculate liability duration distribution
   - Apply structural caps per bucket

2. **Tug-of-War (Phase 1)**
   - All Primes with existing reservations tug for capacity simultaneously
   - Distance 0 (own bucket) = natural priority
   - Resolve collisions pro-rata
   - Multiple rounds until needs met or capacity exhausted

3. **Trading (Phase 2)**
   - Primes upgrade capacity mix
   - Release lowest-value capacity downward
   - Cascade until capacity finds a Prime that values it
   - Overreach trading for Pareto improvements

4. **Excess Identification**
   - After tug-of-war completes, calculate remaining capacity per bucket
   - This excess goes to the SPTP auction (Part 4)

5. **Capital Calculation** (after auction completes)
   - Apply Risk Framework formulas based on final allocation
   - Matched portions get risk-weight treatment
   - Unmatched portions get FRTB treatment

See `tugofwar.md` for full algorithm details.

### Reservation vs Lindy Mismatch

When Lindy-measured capacity ≠ total reservations:

**Lindy > Reservations:**
- Tug-of-war satisfies all existing reservations
- Excess capacity goes to SPTP auction
- New Primes can win capacity via auction

**Lindy < Reservations:**
- Shortfall situation
- Tug-of-war distributes available capacity pro-rata among reservations
- No excess for auction (auction clears with zero capacity)
- Primes still pay full reservation price (incentivizes accurate bidding)

---

## Part 7: Weekly Timeline

### Fixed Schedule

All times are **UTC**.

| Day/Time | Event | Actor |
|----------|-------|-------|
| **Tuesday 12:00** | Measurement Period ends | — |
| | Bid window closes (OSRC + SPTP) | lpha-auction |
| | **LCTS generations LOCKED** | lpha-lcts |
| | New active generation opens | lpha-lcts |
| | Processing Period begins | — |
| **Tuesday 12:00-14:00** | Auctions revealed and matched | lpha-auction |
| **Tuesday 14:00-16:00** | Lindy measurement snapshot | lpla-checker |
| **Tuesday 16:00-18:00** | Tug-of-war allocation | lpha-auction |
| **Tuesday 18:00-20:00** | SPTP excess auction matching | lpha-auction |
| **Tuesday 20:00-22:00** | Interest calculations finalized | stl-base (each Prime) |
| **Tuesday 22:00-24:00** | Distribution calculations finalized | lpla-checker |
| **Wednesday 00:00-08:00** | Prepayments submitted | stl-base |
| **Wednesday 08:00-12:00** | Verification and compliance checks | lpla-checker |
| **Wednesday 12:00** | **Moment of Settlement** | — |
| | New OSRC allocations take effect | lpha-auction |
| | New SPTP capacity published to Synome | lpha-auction |
| | srUSDS exchange rate updated | lpha-lcts |
| | **LCTS locked generations settle** | lpha-lcts |
| | Locked generations unlock (ACTIVE or FINALIZED) | lpha-lcts |
| | Capital calculations apply | lpla-checker |
| | Penalties begin for non-compliant actors | — |
| **Wednesday 12:00+** | Next Measurement Period begins | — |

### Key Timing Principles

1. **Bids close at Tuesday noon** — All sealed bids must be submitted before this time
2. **24-hour processing window** — Ample time to calculate, verify, and prepay
3. **Prepayment required** — Interest and distributions must arrive before Wednesday noon
4. **Atomic settlement** — All new parameters take effect simultaneously at Moment of Settlement
5. **Penalties for lateness** — Any actor not in compliance by Wednesday noon accrues penalties

### Sequencing Dependencies

```
Tue 12:00: Bids close + LCTS generations lock
    │
    ├─────────────────────────────────────────┐
    │                                         │
    ▼                                         ▼
Auctions revealed                    LCTS generations locked
    │                                (users can deposit into new gen,
    ▼                                 but cannot withdraw from locked)
OSRC matching
    │
    ▼
Lindy measurement
    │
    ▼
Tug-of-war (existing reservations)
    │
    ▼
SPTP excess auction (depends on tug-of-war output)
    │
    ▼
All results known → Prepayments can be calculated and submitted
    │
    ▼
Wed 12:00: Everything takes effect simultaneously
    │
    ├── LCTS locked generations settle proportionally
    ├── Exchange rates updated
    └── Generations unlock (ACTIVE or FINALIZED)
```

### Failure Handling

**Before Tuesday noon (bid submission):**
- **Bid submission failure:** Prime's bid not included; can resubmit until deadline
- **Late bid:** Rejected; must wait for next week

**During Processing Period (Tue noon → Wed noon):**
- **Auction processing failure:** Retry with exponential backoff; escalate to GovOps if persistent
- **Tug-of-war failure:** Use previous week's allocation temporarily; flag for investigation
- **Prepayment transaction failure:** Actor must retry; penalties will accrue if not resolved by Wednesday noon
- **LCTS lock failure:** Users in active generation remain able to withdraw; flag for investigation
- **User tries to withdraw from locked generation:** Transaction reverts; must wait for settlement

**At/After Moment of Settlement (Wed noon):**
- **Late prepayment:** Penalties accrue from Wednesday noon until payment completes
- **LCTS settlement failure:** Locked generations remain locked; retry immediately; users cannot withdraw until settled
- **LCTS unlock failure:** Generations remain in limbo; escalate to GovOps
- **Persistent non-compliance:** Escalation path (alerts → restrictions → governance review)

**LCTS-specific guarantees:**
- Users can ALWAYS deposit into the active generation (even during processing period)
- Users in locked generations can claim rewards but not withdraw underlying
- All locked generations receive proportional settlement capacity
- No user loses funds due to settlement failure — positions remain intact

---

## Open Questions

1. **Bid modification** — Can Primes modify/cancel bids before Tuesday noon cutoff, or is first bid final?

2. **Minimum bid increments** — Should there be minimum bid sizes or rate increments to prevent spam?

3. **Penalty rate calibration** — What's the right penalty rate? (e.g., 0.1% per hour = 2.4% per day)

4. **Escalation thresholds** — At what point does lateness trigger restrictions vs just penalties?

5. **SPTP reservation duration limits** — Max 52 weeks? Longer? Should there be a cap?

6. **Secondary market mechanics** — How exactly do SPTP reservation trades settle? Same weekly cycle or continuous?

7. **Emergency procedures** — What happens if systemic issue prevents settlement? (e.g., network outage, oracle failure)

---

## Connection to Other Documents

| Document | Relationship |
|----------|--------------|
| `README.md` | Risk framework index and entry point |
| `tugofwar.md` | Tug-of-war algorithm is part of this weekly cycle |
| `smart-contracts/lcts.md` | LCTS settlement is triggered by this cycle |
| `sentinel-network.md` | Defines lpha-auction, lpha-lcts, stl-base roles |

---

*This document describes the weekly settlement cycle. For capital requirement calculations, see `README.md`. For tug-of-war algorithm, see `tugofwar.md`.*
