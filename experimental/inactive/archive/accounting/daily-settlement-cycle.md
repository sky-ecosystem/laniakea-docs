# Daily Settlement Cycle

**Status:** Draft
**Last Updated:** 2026-02-04

---

## Overview

The daily settlement cycle is the heartbeat of Laniakea's resource allocation system. It operates on a fixed daily schedule with a short lock window for processing and a single daily moment when all changes take effect.

> **Phasing note:** In early phases, Sky governance directly originates/allocates srUSDS capacity and manually allocates liability duration matching. Sealed-bid OSRC and Duration auctions begin only once Prime-side `stl-base` is deployed; until then, allocation is top-down (no bids, no matching engine).

> **Scope note:** This daily settlement cycle governs protocol-level resource allocation (risk capital, duration capacity, LCTS queues). Sky Intents — the intent-based trading system — operates on a separate, continuous settlement cadence (1-10 second batches) with atomic on-chain settlement of bilateral, cryptographically proven deals. Sky Intents settlement is independent of this daily cycle. See `trading/sky-intents.md`.

### Daily Timeline

All times are **UTC**.

| Period | Timing | Duration | Purpose |
|--------|--------|----------|---------|
| **Active Window** | 16:00 → 13:00 | 21 hours | Data collection, allocation submission (bids post-`stl-base`), deposits/withdrawals |
| **Processing Window (Lock)** | 13:00 → 16:00 | ≤ 3 hours | Calculation, verification, prepayment |
| **Moment of Settlement** | 16:00 | Instant | New parameters take effect |

```
Day N                              Day N+1
│                                  │
├── Active Window ────────────────►├── Active Window ────────────────►
│   (16:00 → 13:00)                │
│                                  │
│                    ├ Processing ─┤
│                    │ (≤3h lock)  │
│                    │             │
│                    13:00         16:00
│                    Lock +        Settlement
│                    bids close    new params take effect
```

### Settlement Sequence

1. **Active Window** (16:00 → 13:00)
   - OSRC and Duration submissions collected (sealed bids once `stl-base` is live; governance allocations pre-auction)
   - Normal deposits/withdrawals permitted (including LCTS queues)

2. **Processing Window** (13:00 → 16:00)
   - Submission window closes and state is locked for settlement-critical systems
   - Allocations determined (auction matching once `stl-base` is live; governance allocations pre-auction)
   - Lindy measurement snapshot and duration allocation processing (manual pre-auction; tug-of-war/auction in auction mode)
   - Category cap reallocation — update per-Prime category allocations based on penalized exposures (see `../risk-framework/correlation-framework.md`)
   - Prepayments made (interest, distributions)
   - Verification and compliance checks
   - Active Stability Capital (ASC) requirements — including peg defense allocation and DAB — interact with settlement. See `risk-framework/asc.md`

3. **Moment of Settlement** (16:00)
   - New OSRC allocations take effect
   - New Duration capacity published
   - srUSDS exchange rate updated
   - LCTS queues settle
   - Encumbrance ratio (allocated / available capital) monitored against the ≤90% target from the risk framework (see `risk-framework/capital-formula.md`)
   - Penalties begin accruing for non-compliant actors

### Optional Skips (e.g., Weekends)

Some deployments may choose to skip specific cycles (commonly weekends) as an operational choice. This is handled in userspace by simply not calling the lock/settle actions for those cycles. When a cycle is skipped:

- Systems remain in their **ACTIVE** state (no lock window is entered).
- Bid windows extend until the next executed lock.
- The next executed settlement processes the accumulated state for the longer interval.

Protocol-level risk capital tokens are intended to run on the full daily cadence; skip behavior is primarily relevant for specific Halo operators.

---

## Part 1: Prime Settlement

### Timing Model

Interest payments and distribution rewards are calculated on the most recent epoch’s state and must be **prepaid before Moment of Settlement** (16:00).

```
Active Window              Processing Window        Settlement
(16:00 → 13:00)            (13:00 → 16:00)          (16:00)
│                          │                        │
│   Data collected here    │   Calculate + verify   │   Must be paid by now
│   for interest/distrib   │   Prepay amounts       │   Penalties start if late
│                          │                        │
```

### Interest Payments (Prime → Generator)

Each Prime that has borrowed from a Generator must pay interest on outstanding debt.

**Calculation (`stl-base` once deployed; otherwise GovOps automation):**

```
Interest Payment = Average Outstanding Debt × Daily Rate

Where:
- Average Outstanding Debt = time-weighted average of debt over the epoch
- Daily Rate = Annual Base Rate / 365
```

**Process:**

1. **13:00:** Processing Window begins; calculation finalization begins
2. **During Processing Window:** stl-base calculates interest owed
3. **Before 16:00:** stl-base submits interest payment transaction
4. **16:00:** Payment must be complete; penalties accrue if late

### Distribution Rewards (Generator → Prime)

Generators distribute rewards to Primes that have "tagged" addresses — addresses that have opted into receiving distributions.

**Calculation:**

1. Generator accumulates yield from various sources (SSR spread, fees, etc.) during the epoch
2. Distribution amounts calculated based on tagged balances
3. Distribution flows to tagged Prime addresses proportional to their tagged balances

**Process:**

1. **13:00:** Processing Window begins
2. **During Processing Window:** Distribution calculations performed
3. **Before 16:00:** Distribution transactions submitted
4. **16:00:** Distributions must be complete

**Tagged Addresses:**

- Primes can tag addresses to receive distributions
- Tagged addresses must meet certain criteria (e.g., minimum balance, duration)
- Tagging is voluntary — untagged balances don't receive distributions

### Late Payment Penalties

Any actor that fails to complete their obligations before Moment of Settlement (16:00) incurs penalties:

```
Penalty = Owed Amount × Penalty Rate × Time Late

Where:
- Time Late = hours past 16:00 UTC
- Penalty Rate = governance-set rate (e.g., 0.1% per hour)
```

**Penalty mechanics:**

- Penalties accrue continuously from Moment of Settlement until payment is made
- Penalty payments flow to the affected counterparty (e.g., Generator for late interest)
- Persistent lateness (e.g., >24h) may trigger escalation (alerts, restrictions, governance review)
- Penalty history is recorded in Synome for reputation tracking

---

## Part 2: lpha-auction (Allocation/Auction Beacon)

An **LPHA beacon** that coordinates OSRC and Duration capacity allocation on the daily cadence.

- **Pre-auction mode:** publishes governance-set allocations (no bids, no matching engine)
- **Auction mode:** runs sealed-bid matching based on `stl-base` submissions

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
│  Receives signed bids from stl-base instances (auction mode)  │
│  Or consumes governance-set allocations (pre-auction mode)    │
│  Runs matching algorithm during processing window (auction)   │
│  Coordinates with lpha-lcts for LCTS settlement               │
└─────────────────────────────────────────────────────────────┘
```

### Bid Submission

Auction submission begins once Prime-side `stl-base` is deployed. Before that, governance publishes allocations directly (no bids).

1. Each Prime's stl-base connects to lpha-auction (auction mode)
2. stl-base submits bid messages signed with its private key
3. Bids are stored in lpha-auction's private database (sealed)
4. Bids are not revealed until processing/settlement

**Bid Message Format:**

```
{
  prime_id: <Prime identifier>,
  auction_type: "OSRC" | "Duration",
  bucket: <bucket number for Duration, null for OSRC>,
  amount: <capacity amount requested>,
  max_rate: <maximum rate willing to pay>,
  signature: <stl-base private key signature>,
  timestamp: <submission time>
}
```

### Security Properties

- **Sealed bids:** No participant can see others' bids before processing window
- **Authenticity:** Signatures verify bids came from legitimate stl-base instances
- **Non-repudiation:** Signed bids cannot be denied after submission
- **Timing:** Bids accepted until cutoff; late bids rejected

---

## Part 3: OSRC Auction (Originated Senior Risk Capital)

> **Activation:** OSRC auctions begin once Prime-side `stl-base` is deployed. Prior to that, OSRC allocations are governance-set and published top-down.

### Purpose

Allocate srUSDS capacity to Primes. Primes that win OSRC auction capacity can use Senior Risk Capital as part of their capital structure.

### Auction Mechanics

**Type:** Sealed-bid, uniform-price auction (daily)

**Process:**

1. **Bid Collection** (during Active Window)
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

### Daily-Only Design

**No multi-day reservations.** Every Prime must re-bid each day.

**Rationale:**

Multi-epoch reservations create problems:
1. **Rate lock-in distortion:** Low locked-in rates reduce effective yields
2. **Capacity mismatch:** Reserved capacity may not match actual srUSDS supply
3. **Exit incentives:** srUSDS holders leave if yields are suppressed by old reservations
4. **Complexity:** Overpayment/underpayment scenarios require complex handling

Daily auctions provide:
- Clean price discovery each day
- Rates reflect current market conditions
- srUSDS holders see real yields, make informed decisions
- Simple, predictable system

**Trade-off:** Primes have no long-duration certainty on SRC access. If rates spike, they pay up or lose access. This is acceptable because:
- Primes can manage rate risk through their own capital structure
- Daily auctions are predictable — no surprise rate changes mid-day
- Market-clearing rates reflect true cost of risk capital

### OSRC Usage

Primes that win OSRC capacity:
- Can count the SRC toward their capital requirements (per Risk Framework)
- Must pay the clearing rate each epoch until they stop using SRC
- Can reduce usage at any time (no lock-in on the Prime side)

---

## Part 4: Duration Bucket Auction

> **Activation:** Duration auctions begin once Prime-side `stl-base` is deployed. Prior to that, duration capacity is allocated manually by governance (top-down).

### Purpose

Allocate Duration capacity reservations to Primes. Reservations grant the right to claim Duration capacity when Lindy measurement provides it.

### Relationship to OSRC

Duration and OSRC are **separate auctions** serving different purposes:

| Aspect | OSRC Auction | Duration Bucket Auction |
|--------|--------------|---------------------|
| **What's allocated** | Senior Risk Capital capacity | Duration-matching capacity |
| **Purpose** | Capital structure (loss absorption) | Capital treatment (risk-weight-only vs forced-loss treatment) |
| **Pricing** | Rate paid to srUSDS holders | Price paid for reservation rights |
| **Duration** | Daily (no reservations) | Can reserve for multiple epochs |

A Prime might:
- Win OSRC capacity (to use SRC in its capital structure)
- Win Duration capacity (to get favorable capital treatment on its assets)
- Win both, one, or neither

### Auction Sequence

The Duration auction follows a specific sequence where tug-of-war happens FIRST, then excess is auctioned:

```
1. Bid submission window opens
2. Bids submitted (sealed)
3. Bid window closes (13:00)
4. Lindy measurement (snapshot)
5. Tug-of-war processes existing reservations against Lindy capacity
6. Excess capacity identified (Lindy capacity - consumed by reservations)
7. Auction matches bids against excess capacity
8. Winners pay uniform clearing price
9. New Duration bucket capacity published to Synome
```

**Key insight:** The auction only allocates *excess* capacity that wasn't consumed by existing reservations via tug-of-war. This ensures:
- Existing reservation holders get their capacity first
- New capacity only comes from genuine Lindy growth
- No double-allocation of the same capacity

### Auction Mechanics

**Type:** Sealed-bid, uniform-price auction (per bucket, for excess capacity only)

**Process:**

1. **Bid Collection** (during Active Window)
   - Each Prime's stl-base submits sealed bids to lpha-auction
   - Bid specifies: bucket number, amount, maximum price, duration (epochs)

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

### Multi-Epoch Reservations

Unlike OSRC, Duration allows multi-epoch reservations:

**Rationale:**
- Duration capacity is about duration matching, which is inherently longer-term
- Primes need planning certainty for asset acquisition
- Reservations don't directly affect other participants' yields (unlike OSRC rates)

**Mechanics:**
- Bid includes duration (in settlement epochs)
- Price is per-epoch
- Commitment: must pay for full duration even if Lindy capacity falls short
- If Lindy < reservation in future epochs, shortfall handled by tug-of-war pro-rata

### Secondary Market

Reservation holders can trade their reservations:

- Sell full or partial amounts
- Time-slice (sell epochs 5-10 of a 20-epoch reservation)
- Buyers get same rights as original auction winners
- Enables price discovery between auctions

---

## Part 5: LCTS Settlement

LCTS (Liquidity Constrained Token Standard) settlement is synchronized with the daily settlement cycle. See `smart-contracts/lcts.md` for the queue specification.

### LCTS Daily Cycle

| Event | Timing | Action |
|-------|--------|--------|
| **Lock** | 13:00 UTC | LCTS enters LOCKED; deposits/withdrawals/claims blocked for the current generation |
| **Settlement** | 16:00 UTC | Locked generation processed; exchange rates updated |
| **Unlock / Dormant** | 16:00 UTC | Generation returns to ACTIVE (if not fully converted) or FINALIZED + queue becomes DORMANT (if fully converted) |

### Simplified Single-Generation Model

The daily cycle removes the need for concurrent generations:

- At most **one** current generation per queue is ever ACTIVE or LOCKED.
- During the lock window, users simply wait (≤ 3 hours); new deposits do not spill into a “next” generation.
- If a generation fully converts, the queue becomes **DORMANT** until the next user action creates a new generation.
- Users may always claim from **FINALIZED** generations (immutable), including during the lock window.

### srUSDS Settlement Flow

1. **13:00:** lpha-lcts locks the current generations (if any)
   - SubscribeQueue current generation → LOCKED
   - RedeemQueue current generation → LOCKED

2. **During Processing Window:**
   - lpha-auction publishes OSRC and Duration results
     - governance allocations (pre-auction mode)
     - auction-cleared allocations (auction mode, once `stl-base` is live)

3. **16:00:** lpha-lcts settles the locked generations
   - Updates exchange rate based on clearing rate yield
   - Calculates settlement capacity (see below)
   - Calls settle() on SubscribeQueue and RedeemQueue
   - Unlocks (ACTIVE) or finalizes (FINALIZED → DORMANT)

### Capacity Calculation

Settlement capacity for srUSDS comes from three sources:

```
Subscribe Capacity = Net Flow Netting + OSRC Capacity (governance-originated pre-auction; auction-allocated later; throttled by target spread)
Redeem Capacity = Net Flow Netting + Daily Redemption Limit
```

**Step 1: Net Flow Netting**

Subscribe and redeem queues cancel each other out first:

```
SubscribeQueue total: $100M
RedeemQueue total:    $30M

Net flow netting: $30M matched both ways
- $30M subscribe converts to srUSDS
- $30M redeem converts to sUSDS

Remaining after netting:
- Subscribe demand: $70M still waiting
- Redeem demand: $0 (fully processed)
```

**Step 2: Apply Additional Capacity**

For subscribes after netting:
- OSRC capacity (governance-originated pre-auction; auction-allocated later) determines how much more can convert
- Subject to target spread throttling (see below)

For redeems after netting:
- Daily redemption limit (governance-set) determines how much more can convert

### Target Spread Mechanism

srUSDS has a **target spread** (governance-set) above SSR. This protects yield rates from crashing:

**Subscribe capacity throttling:**

```
If OSRC clearing yield (governance-set pre-auction; auction-cleared later) provides yield ≥ target spread:
  → Allow full subscribe capacity

If OSRC clearing yield would result in yield < target spread:
  → Reduce subscribe capacity to maintain target spread
  → Excess demand waits in queue for the next epoch
```

**Rationale:**
- Prevents sudden rate crashes when supply exceeds auction demand
- Protects existing srUSDS holders from yield dilution
- Creates natural equilibrium between supply and demand

### One Queue Spans Multiple Days

Due to net flow netting, at most one queue has leftover demand after netting:

- If subscribe > redeem: RedeemQueue clears, SubscribeQueue retains backlog
- If redeem > subscribe: SubscribeQueue clears, RedeemQueue retains backlog

The queue with backlog can span multiple days as partial conversions occur at each daily settlement.

---

## Part 6: Tug-of-War Allocation

### Timing

Tug-of-war runs during the Processing Window once duration capacity is allocated via the auction mechanism. In pre-auction mode, governance may allocate capacity directly (no tug-of-war, no excess auction).

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
   - This excess goes to the Duration auction

5. **Capital Calculation** (after auction completes)
   - Apply Risk Framework formulas based on final allocation
   - Matched portions get risk-weight treatment
   - Unmatched portions get forced-loss treatment (e.g., `max(RW, FRTB drawdown)` for liquid assets)

See `tugofwar.md` for full algorithm details.

### Reservation vs Lindy Mismatch

When Lindy-measured capacity ≠ total reservations:

**Lindy > Reservations:**
- Tug-of-war satisfies all existing reservations
- Excess capacity goes to Duration auction
- New Primes can win capacity via auction

**Lindy < Reservations:**
- Shortfall situation
- Tug-of-war distributes available capacity pro-rata among reservations
- No excess for auction (auction clears with zero capacity)
- Primes still pay full reservation price (incentivizes accurate bidding)

---

## Part 7: Daily Timeline

### Fixed Schedule

All times are **UTC**.

| Time | Event | Actor |
|------|-------|-------|
| **13:00** | Active Window ends; submission window closes (OSRC + Duration) | lpha-auction |
| | LCTS queues lock (if active) | lpha-lcts |
| | Processing Window begins | — |
| **13:00 → 16:00** | Allocations, measurement, category cap reallocation, prepayments, verification (auctions+tug-of-war in auction mode) | lpha-auction / lpla-checker / stl-base |
| **16:00** | **Moment of Settlement** | — |
| | New OSRC allocations take effect | lpha-auction |
| | New Duration capacity published to Synome | lpha-auction |
| | srUSDS exchange rate updated | lpha-lcts |
| | LCTS queues settle + unlock/finalize | lpha-lcts |
| | Capital calculations apply | lpla-checker |
| | Penalties begin for non-compliant actors | — |
| **16:00 → 13:00** | Next Active Window (bids open, deposits/withdrawals allowed) | — |

### Key Timing Principles

1. **Bids close at 13:00** — All sealed bids must be submitted before this time
2. **Short processing window** — Systems must calculate, verify, and prepay within ≤3 hours
3. **Prepayment required** — Interest and distributions must arrive before 16:00
4. **Atomic settlement** — All new parameters take effect simultaneously at Moment of Settlement
5. **Penalties for lateness** — Any actor not in compliance by 16:00 accrues penalties

### Sequencing Dependencies

```
13:00: Submissions close + LCTS locks
    │
    ▼
Allocations determined (auction matching or governance)
    │
    ▼
Lindy measurement
    │
    ▼
Tug-of-war (existing reservations)
    │
    ▼
Duration excess auction (depends on tug-of-war output)
    │
    ▼
Category cap reallocation (depends on final exposures)
    │
    ▼
All results known → Prepayments calculated + submitted
    │
    ▼
16:00: Everything takes effect simultaneously
    ├── Exchange rates updated
    ├── LCTS queues settle
    └── Penalties begin (if non-compliant)
```

### Failure Handling

**Before 13:00 (bid submission):**
- **Bid submission failure:** Prime's bid not included; can resubmit until deadline
- **Late bid:** Rejected; must wait for next cycle

**During Processing Window (13:00 → 16:00):**
- **Auction processing failure:** Retry with exponential backoff; escalate to GovOps if persistent
- **Tug-of-war failure:** Use previous allocation temporarily; flag for investigation
- **Prepayment transaction failure:** Actor must retry; penalties accrue if not resolved by 16:00
- **LCTS lock failure:** Queue remains ACTIVE; flag for investigation; do not settle until locked
- **User tries to interact with locked generation:** Transaction reverts; must wait for unlock

**At/After Moment of Settlement (16:00):**
- **Late prepayment:** Penalties accrue from 16:00 until payment completes
- **LCTS settlement failure:** Generation remains locked; retry immediately; users cannot interact until settled
- **Persistent non-compliance:** Escalation path (alerts → restrictions → governance review)

**LCTS-specific guarantees (daily model):**
- Deposits/withdrawals/claims are **blocked during lock** for the current generation
- At most one generation per queue is ACTIVE/LOCKED at a time
- Users can always claim from FINALIZED generations
- No user loses funds due to settlement failure — positions remain intact

---

## Open Questions

1. **Bid modification** — Can Primes modify/cancel bids before 13:00 cutoff, or is first bid final?
2. **Minimum bid increments** — Should there be minimum bid sizes or rate increments to prevent spam?
3. **Penalty rate calibration** — What's the right penalty rate for a daily cadence?
4. **Escalation thresholds** — At what point does lateness trigger restrictions vs just penalties?
5. **Reservation duration limits** — Max duration in epochs? (e.g., 365 days) Longer?
6. **Secondary market mechanics** — How exactly do Duration reservation trades settle? Same daily cycle or continuous?
7. **Emergency procedures** — What happens if systemic issue prevents settlement? (network outage, oracle failure)

---

## Connection to Other Documents

| Document | Relationship |
|----------|--------------|
| `books-and-units.md` | Settlement updates book states — the balanced ledgers at each layer |
| `../risk-framework/README.md` | Risk framework index and entry point |
| `tugofwar.md` | Tug-of-war algorithm is part of this daily cycle |
| `smart-contracts/lcts.md` | LCTS settlement is triggered by this cycle |
| `trading/sentinel-network.md` | Defines lpha-auction, lpha-lcts, stl-base roles |

---

*This document describes the daily settlement cycle. For capital requirement calculations, see `../risk-framework/README.md`. For tug-of-war algorithm, see `tugofwar.md`.*
