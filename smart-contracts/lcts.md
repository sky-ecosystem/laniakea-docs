# Liquidity Constrained Token Standard (LCTS) — Business Requirements

**Status:** Draft
**Last Updated:** 2026-01-27

---

## Executive Summary

The Liquidity Constrained Token Standard defines a queue-based system for token conversions that cannot occur instantly due to external capacity constraints. Users subscribe with assets into a queue, receive fungible shares representing their queue position, and receive converted assets over time as capacity becomes available.

The system consists of two independent queue contracts—SubscribeQueue and RedeemQueue—each using a "generation" model where all subscribers in the same generation share proportionally in the conversion capacity allocated to that generation.

**Key feature: Concurrent generations.** LCTS supports multiple generations existing simultaneously to integrate with the weekly settlement cycle. Each week, the active generation locks during the processing period while a new generation opens for deposits. This ensures auction calculations are based on known quantities while still allowing new users to participate.

---

## Why LCTS Exists

LCTS solves the problem: **how do you fairly distribute limited conversion capacity among many users?**

### Use Cases by Agent Type

LCTS is a general-purpose token standard used across multiple layers of the Sky Agent framework:

| Agent | Token | Description |
|-------|-------|-------------|
| **Generator** | srUSDS | External pooled Senior Risk Capital — global risk absorption for the generated asset |
| **Prime** | TEJRC | Tokenized External Junior Risk Capital — external parties providing junior risk capital to a Prime |
| **Prime** | TISRC | Tokenized Isolated Senior Risk Capital — senior risk capital scoped to a specific Prime |
| **Halo** | Halo Unit shares | Claims on Halo Units — the default token standard for capacity-constrained investment products |

**Risk capital tokens (srUSDS, TEJRC, TISRC)** MUST use LCTS. No alternative exists. These tokens represent risk capital that absorbs losses in exchange for yield.

**Halo Units** use LCTS as the default token standard. It's the natural fit when Halos face capacity constraints on both subscribe (strategy limits) and redeem (liquidity). Alternatives exist for Halos: NFATS for bespoke deals, stablecoin-style vaults for instant liquidity.

### The Core Problem

Without LCTS, capacity-constrained conversions would be first-come-first-served, creating:
- Gas wars for conversion slots
- Unfair advantage to sophisticated users with bots
- Poor UX for regular users

LCTS eliminates this by pooling all users in a generation and distributing capacity proportionally.

---

## Goals

### Primary Goals

1. **Rate-Limited Conversions**
   - Conversions (subscribe or redeem) occur only when external capacity is available
   - An LCTS-pBEAM (operated by a Sentinel) controls how much capacity is allocated each epoch
   - Users cannot bypass the queue to convert instantly

2. **Fair Proportional Distribution**
   - All users in the same generation share capacity proportionally
   - A user with 10% of the generation's shares receives 10% of the converted output
   - No first-come-first-served advantage within a generation

3. **Fungible Queue Positions**
   - Queue positions are represented as shares, not individual requests
   - Shares within a generation are interchangeable for accounting purposes
   - Users can subscribe multiple times, accumulating shares
   - Shares are non-transferable — they are internal accounting only, not tokens

4. **Immediate Exit Option (Active Generation Only)**
   - Users in the current **active** generation can exit at any time
   - Exiting returns both: unconverted underlying (subscribe asset) plus any accrued rewards (reward asset)
   - Users forfeit only their share of future capacity, not past rewards
   - Exit is a complete withdrawal — no partial exits
   - **Locked generations cannot exit** — during processing period, users must wait for settlement

### Design Principles

1. **Generation Isolation**: Each generation is independent; finalized generations are immutable
2. **Gas Efficiency**: All operations are O(1) regardless of user count
3. **Minimal Trust**: Only the LCTS-pBEAM can allocate capacity; all other logic is deterministic
4. **Settlement Cycle Integration**: Generation lifecycle is synchronized with a configurable settlement cycle

---

## Settlement Cycle Configuration

LCTS supports **configurable settlement cycles** to accommodate different Halo Class requirements. Each LCTS deployment specifies its cycle mode at initialization.

### Cycle Modes

| Mode | Lock Period | Settlement Frequency | Use Case |
|------|-------------|---------------------|----------|
| **Weekly** (default) | Tue 12:00 → Wed 12:00 UTC (24h) | Once per week | Standard srUSDS, large capacity pools |
| **Weekday** | Mon-Fri 12:00 → 15:00 UTC (3h) | Daily (weekdays only) | Higher velocity products, institutional flows |

### Generation States

| State | Description | User Actions |
|-------|-------------|--------------|
| **Active** | Accepting new deposits | Subscribe, withdraw, claim rewards |
| **Locked** | Frozen during processing period | Claim rewards only (no deposits, no withdrawals) |
| **Processing** | Being settled at Moment of Settlement | None (system processing) |
| **Finalized** | Fully converted | Claim final rewards only |

---

## Weekly Cycle (Default)

The weekly cycle follows the protocol-wide settlement schedule (see `weekly-settlement-cycle.md`).

### Weekly Timeline

```
Week N:
├── Before Tue noon: Gen 1 is ACTIVE (deposits, withdrawals allowed)
├── Tue 12:00 UTC (Lock):
│     Gen 1 → LOCKED (no new deposits, no withdrawals)
│     Gen 2 → ACTIVE (new deposits go here)
├── Wed 12:00 UTC (Settlement):
│     Gen 1 → PROCESSING → proportional settlement
│     Gen 1 → unlocks (users can claim, may have remaining balance)
│     Gen 2 remains ACTIVE
│
Week N+1:
├── Before Tue noon: Gen 2 is ACTIVE
├── Tue 12:00 UTC: Gen 2 → LOCKED, Gen 3 → ACTIVE
├── Wed 12:00 UTC: Gen 2 processed, etc.
```

### Multi-Week Generations

A generation may span multiple weeks if capacity is constrained:

```
Week 1: Gen 1 created with $100M, $30M converted → $70M remains
Week 2: Gen 1 still has $70M, $25M converted → $45M remains
Week 3: Gen 1 still has $45M, $45M converted → Gen 1 finalizes
```

Each cycle, the generation:
1. Locks at configured lock time (e.g., Tuesday 12:00 UTC for weekly mode)
2. Receives proportional capacity at settlement
3. Unlocks after settlement (users can claim rewards)
4. Returns to ACTIVE (if remaining underlying > 0) or becomes FINALIZED (if fully converted)

---

## Weekday Cycle

The weekday cycle enables daily settlements with a shorter lock period, suitable for higher-velocity products.

### Weekday Timeline

```
Monday:
├── Before 12:00 UTC: Gen 1 is ACTIVE
├── 12:00 UTC (Lock): Gen 1 → LOCKED, Gen 2 → ACTIVE
├── 15:00 UTC (Settlement): Gen 1 processed, unlocks
│
Tuesday:
├── Before 12:00 UTC: Gen 2 is ACTIVE (Gen 1 may still have remaining)
├── 12:00 UTC (Lock): Gen 2 → LOCKED, Gen 3 → ACTIVE
├── 15:00 UTC (Settlement): Gen 2 processed, unlocks
│
... (Wed, Thu, Fri follow same pattern) ...
│
Saturday-Sunday:
├── No locks, no settlements
├── Active generations remain ACTIVE
├── Users can deposit/withdraw freely
```

### Weekday Cycle Parameters

| Parameter | Value |
|-----------|-------|
| **Lock time** | 12:00 UTC (weekdays only) |
| **Settlement time** | 15:00 UTC (weekdays only) |
| **Lock duration** | 3 hours |
| **Operating days** | Monday–Friday |
| **Weekend behavior** | No processing; generations remain ACTIVE |

### Multi-Day Generations (Weekday)

Similar to weekly, a generation may span multiple days:

```
Monday: Gen 1 created with $50M, $15M converted → $35M remains
Tuesday: Gen 1 still has $35M, $20M converted → $15M remains
Wednesday: Gen 1 still has $15M, $15M converted → Gen 1 finalizes
```

---

## Why Lock Generations?

The lock period serves critical functions regardless of cycle mode:

1. **Auction accuracy** — OSRC auction bids are based on known SubscribeQueue demand; if users could withdraw during processing, auction matching would be invalidated
2. **Settlement certainty** — The Sentinel needs fixed quantities to calculate proportional distributions
3. **Rate integrity** — Clearing rates depend on stable supply/demand during processing

**Key insight:** All locked generations receive proportional capacity based on their current underlying amounts — no age-based priority. Older generations' only advantage is that they received settlements in earlier weeks; they get no favorable treatment in future processing periods.

### Capacity Sources at Settlement

Settlement capacity comes from three sources:

1. **Net flow netting** — Subscribe and redeem queues cancel each other out
2. **OSRC capacity** — New srUSDS capacity from auction (for subscribes)
3. **Redemption capacity** — Governance-set limit on weekly redemptions

```
Example:
- SubscribeQueue total: $100M waiting (across all locked generations)
- RedeemQueue total: $30M waiting
- OSRC auction capacity: $30M new minting

Settlement:
1. Net flow netting: $30M subscribe ↔ $30M redeem (matched)
2. Apply OSRC capacity: $30M more subscribe converts
3. Result:
   - RedeemQueue: fully processed ($30M → sUSDS)
   - SubscribeQueue: $60M processed, $40M remains
```

**Implication:** At most one queue has generations spanning multiple weeks. The side with excess demand accumulates; the other side clears each week.

### Proportional Distribution Across Generations

When multiple locked generations exist, settlement capacity is distributed proportionally:

```
Gen 1: $40M underlying (from 3 weeks ago)
Gen 2: $60M underlying (from 2 weeks ago)
Gen 3: $50M underlying (locked this week)

Total locked: $150M
Settlement capacity: $90M

Distribution:
- Gen 1 receives: $90M × (40/150) = $24M → $16M remains
- Gen 2 receives: $90M × (60/150) = $36M → $24M remains
- Gen 3 receives: $90M × (50/150) = $30M → $20M remains
```

All generations receive proportional capacity based on their current underlying amounts — no age-based priority. A user who deposited 3 weeks ago gets the same pro-rata treatment as a user who deposited last week. The only advantage of being earlier is having received settlements in previous weeks.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    LCTS-pBEAM (Sentinel)                         │
│         Determines capacity each epoch, calls settle()           │
└─────────────────────────────┬───────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│     SubscribeQueue      │     │      RedeemQueue        │
│                         │     │                         │
│  Underlying: sUSDS      │     │  Underlying: srUSDS     │
│  Reward: srUSDS         │     │  Reward: sUSDS          │
│                         │     │                         │
│  Users subscribe sUSDS  │     │  Users redeem srUSDS    │
│  Receive srUSDS over    │     │  Receive sUSDS over     │
│  time as capacity       │     │  time as capacity       │
│  allows                 │     │  allows                 │
└─────────────────────────┘     └─────────────────────────┘
```

### Terminology

| Term | Definition |
|------|------------|
| **Generation** | A cohort of subscribers that share capacity together; identified by a numeric ID |
| **Active Generation** | The generation currently accepting new deposits and withdrawals |
| **Locked Generation** | A generation frozen during the processing period; no deposits or withdrawals allowed |
| **Finalized Generation** | A generation that has been fully converted (totalUnderlying = 0) |
| **Shares** | Internal accounting units representing a user's proportional claim on a generation; non-transferable |
| **Underlying** | The asset deposited into the queue (sUSDS for subscribes, srUSDS for redeems) |
| **Reward** | The asset received from conversion (srUSDS for subscribes, sUSDS for redeems) |
| **Settlement Cycle** | Configurable cycle during which generations are processed. Weekly (default): Tue noon → Wed noon. Weekday: daily Mon-Fri 12:00 → 15:00 UTC |
| **Processing Period** | The lock period when generations await settlement. Weekly: 24h. Weekday: 3h |
| **Moment of Settlement** | The time when all locked generations are proportionally processed. Weekly: Wed 12:00 UTC. Weekday: 15:00 UTC |
| **Capacity** | The amount of underlying that can be converted in a single settlement |
| **Net Flow Netting** | Subscribe and redeem queues canceling each other out, reducing net conversion needs |
| **rewardPerToken** | Cumulative rewards distributed per share (accumulator pattern) |
| **rewardDebt** | Snapshot of rewardPerToken at time of user's entry (prevents claiming pre-entry rewards) |
| **LCTS-pBEAM** | pBEAM held by Sentinel that can call settle() to allocate capacity |
| **Holding System** | Contract holding sUSDS backing srUSDS; receives funding, sources redemptions |

---

## Contract Behaviors

### Generation State

Each queue maintains state for multiple concurrent generations:

**Global State:**
- **activeGen**: The numeric ID of the generation currently accepting deposits
- **generations[]**: Mapping of generation ID to generation state

**Per-Generation State:**
- **status**: ACTIVE | LOCKED | FINALIZED
- **totalShares**: Total shares outstanding for this generation
- **totalUnderlying**: Total unconverted underlying remaining in this generation
- **rewardPerToken**: Cumulative rewards per share distributed so far (1e18 precision)
- **finalRewardPerToken**: The rewardPerToken value at the moment of finalization (only set when finalized)

### Generation Lifecycle

```
ACTIVE → LOCKED → (settlement) → ACTIVE or FINALIZED
         ↑                           │
         └───────────────────────────┘
         (if still has remaining underlying after settlement)
```

1. **ACTIVE**: Generation is accepting new deposits; users can withdraw
2. **LOCKED**: Lock time triggers lock; no deposits or withdrawals during processing period
3. **Settlement**: Settlement time processes all locked generations proportionally
4. **Post-settlement**: If totalUnderlying > 0, generation returns to ACTIVE; if totalUnderlying = 0, generation becomes FINALIZED

*Lock and settlement times depend on cycle mode (weekly or weekday). See Settlement Cycle Configuration above.*

### User Position State

Each user has one position:

- **gen**: The generation this position belongs to
- **shares**: Number of shares the user holds
- **rewardDebt**: The rewardPerToken value when the user entered (or last claimed)

---

## SubscribeQueue Behaviors

### Subscribing

**Preconditions:**
- User has approved sufficient sUSDS to the queue contract
- Amount is greater than zero
- **Active generation exists** (there is always exactly one ACTIVE generation)

**Behavior:**

- If the user has shares in a finalized generation:
  - Settle that position first (see Settling below)
  - Clear the old position before proceeding

- If the user has shares in a locked generation:
  - User CANNOT subscribe to a new generation until their locked position is settled
  - Must wait for settlement at configured settlement time

- If the user has shares in the active generation:
  - Claim any pending rewards first (see Claiming Rewards below)
  - Update rewardDebt to current rewardPerToken

- Calculate shares to mint:
  - If this is the first subscribe in the generation (totalShares == 0): shares = subscribe amount (1:1)
  - Otherwise: shares = subscribeAmount × totalShares ÷ totalUnderlying

- Update state:
  - Add subscribe amount to totalUnderlying
  - Add calculated shares to totalShares
  - Set user's gen to activeGen
  - Add calculated shares to user's shares
  - Set user's rewardDebt to current rewardPerToken

- Transfer sUSDS from user to queue contract

### Lock Generation (LCTS-pBEAM Only)

**Preconditions:**
- Caller is the LCTS-pBEAM (held by Sentinel)
- Called at lock time (Weekly: Tue 12:00 UTC; Weekday: Mon-Fri 12:00 UTC)

**Behavior:**

- Set current active generation status to LOCKED
- Create new generation with status ACTIVE
- Increment activeGen to point to new generation

This ensures new deposits go to the new active generation while the locked generation awaits settlement.

### Settlement (LCTS-pBEAM Only)

**Preconditions:**
- Caller is the LCTS-pBEAM (held by Sentinel)
- Called at settlement time (Weekly: Wed 12:00 UTC; Weekday: Mon-Fri 15:00 UTC)
- subscribeCapacity is the total amount of sUSDS that can convert this cycle

**Behavior:**

Settlement processes ALL locked generations proportionally in a single transaction:

1. **Calculate total locked underlying:**
   ```
   totalLockedUnderlying = Σ (gen.totalUnderlying for all LOCKED generations)
   ```

2. **Distribute capacity proportionally to each locked generation:**
   ```
   For each LOCKED generation:
     genCapacity = subscribeCapacity × (gen.totalUnderlying / totalLockedUnderlying)
     convertAmount = minimum of (genCapacity, gen.totalUnderlying)
   ```

3. **Execute conversion for each generation:**
   - Transfer convertAmount of sUSDS to the Holding System
   - Mint srUSDS to queue at current exchange rate
   - Update reward accumulator: rewardPerToken += srUSDSMinted × 1e18 ÷ gen.totalShares
   - Reduce underlying: gen.totalUnderlying -= convertAmount

4. **Update generation states:**
   - If generation is fully drained (totalUnderlying == 0):
     - Store finalized state: finalRewardPerToken = rewardPerToken
     - Set status to FINALIZED
   - If generation still has underlying:
     - Set status back to ACTIVE (unlocked, users can withdraw again)

### Claiming (Active Generation)

**Preconditions:**
- User has shares in an ACTIVE generation
- Generation status is ACTIVE

**Behavior — Claim Rewards Only:**

- Calculate pending rewards:
  - pendingRewards = shares × (rewardPerToken - rewardDebt) ÷ 1e18

- Update user's rewardDebt to current rewardPerToken

- Transfer pendingRewards of srUSDS to user

**Behavior — Claim and Exit (Full Withdrawal):**

- Calculate pending rewards:
  - pendingRewards = shares × (rewardPerToken - rewardDebt) ÷ 1e18

- Calculate proportional underlying:
  - underlyingOut = shares × totalUnderlying ÷ totalShares

- Update totals:
  - totalUnderlying -= underlyingOut
  - totalShares -= shares

- Clear user position (set shares to 0)

- Transfer pendingRewards of srUSDS (reward asset) to user
- Transfer underlyingOut of sUSDS (subscribe asset) to user

User receives both assets and fully exits the queue.

### Claiming (Locked Generation)

**Preconditions:**
- User has shares in a LOCKED generation
- Generation status is LOCKED (during processing period)

**Behavior — Claim Rewards Only:**

- Calculate pending rewards:
  - pendingRewards = shares × (rewardPerToken - rewardDebt) ÷ 1e18

- Update user's rewardDebt to current rewardPerToken

- Transfer pendingRewards of srUSDS to user

**Behavior — Claim and Exit:**

- **NOT ALLOWED** during locked period
- User must wait for settlement at configured settlement time
- After settlement, generation returns to ACTIVE (if not finalized) and user can exit

### Settling (Finalized Generation)

**Preconditions:**
- User has shares in a FINALIZED generation
- Generation status is FINALIZED

**Behavior:**

- Look up the finalized generation's finalRewardPerToken

- Calculate total rewards:
  - rewardsOut = shares × (finalRewardPerToken - rewardDebt) ÷ 1e18

- No underlying to return (generation was fully drained to finalize)

- Clear user position (set shares to 0)

- Transfer rewardsOut of srUSDS to user

---

## RedeemQueue Behaviors

The RedeemQueue is structurally identical to SubscribeQueue with asset directions reversed:

| Aspect | SubscribeQueue | RedeemQueue |
|--------|----------------|-------------|
| User action | subscribe with sUSDS | redeem with srUSDS |
| Underlying tracked | sUSDS | srUSDS |
| Reward distributed | srUSDS | sUSDS |
| Conversion direction | sUSDS → srUSDS | srUSDS → sUSDS |

All behaviors (subscribing, settlement, claiming, settling) follow the same logic with these substitutions.

On settlement, srUSDS is burned and sUSDS is transferred from the Holding System to the queue for distribution.

---

## Invariants

### Share Fairness

1. **Proportional share minting**: New subscribers receive shares proportional to their contribution relative to remaining underlying
   - Formula: shares = amount × totalShares ÷ totalUnderlying
   - First subscriber in a generation receives 1:1 shares

2. **Equal reward per share**: Every share in a generation earns identical rewards, regardless of when within the generation it was acquired
   - The rewardDebt mechanism ensures late subscribers don't claim rewards from before their entry

### Generation Integrity

3. **Generations are immutable once finalized**: The finalRewardPerToken value never changes after finalization

4. **No residual underlying in finalized generations**: A generation only finalizes when totalUnderlying equals zero
   - Users settling from finalized generations receive only rewards, never underlying

5. **Exactly one ACTIVE generation exists at all times**: There is always one (and only one) generation accepting deposits
   - New active generation is created when previous one locks

6. **Locked generations cannot accept deposits or withdrawals**: During processing period, locked generations are frozen
   - Users can only claim accrued rewards, not exit

7. **All locked generations are processed proportionally**: Settlement distributes capacity based on current underlying amounts
   - No age-based priority — older generations get no favorable treatment
   - Each generation receives: capacity × (gen.underlying / total locked underlying)

### User Position Integrity

8. **One position per user per queue**: A user can only have shares in one generation at a time
   - Cannot subscribe to new generation while holding shares in locked generation
   - Must wait for settlement or settle finalized position first

9. **Active generation exit is always available**: Users in an ACTIVE generation can always claim and exit
   - They receive proportional underlying plus accrued rewards
   - No lock-up within an active generation

10. **Locked generation exit is blocked**: Users in a LOCKED generation cannot exit until settlement
    - They can claim rewards but not withdraw underlying
    - After settlement, generation returns to ACTIVE (if not finalized) and exit is available

11. **Shares are non-transferable**: Queue positions cannot be transferred between addresses
    - Each user's shares are tied to their address
    - No ERC-20 or other transfer mechanism exists

### Conservation

12. **Underlying conservation**: totalUnderlying equals the sum of all users' proportional underlying claims
    - Subscribes increase totalUnderlying; exits and settlements decrease it

13. **Reward conservation**: Total rewards distributed equals total rewards received from converter
    - rewardPerToken accumulator ensures exact accounting

### Cycle Integrity

14. **Lock happens exactly at configured lock time**: All active generations lock simultaneously at processing period start (e.g., Tuesday 12:00 UTC for weekly mode, 12:00 UTC each weekday for weekday mode)

15. **Settlement happens exactly at configured settlement time**: All locked generations are processed at Moment of Settlement (e.g., Wednesday 12:00 UTC for weekly mode, 15:00 UTC same day for weekday mode)

16. **New active generation created at lock time**: Users can always deposit, even during processing period (into new generation)

---

## User Stories

### Story 1: Simple Subscribe and Full Conversion

**As** a user,
**I want to** subscribe with sUSDS and receive srUSDS,
**So that** I can access the restricted token.

**Flow:**

1. User subscribes 1,000 sUSDS into SubscribeQueue
   - User is first in generation, receives 1,000 shares
   - totalShares = 1,000, totalUnderlying = 1,000

2. LCTS-pBEAM calls settle with capacity = 1,000 (full conversion)
   - 1,000 sUSDS converts to (e.g.) 980 srUSDS
   - rewardPerToken = 980 × 1e18 ÷ 1,000 = 0.98e18
   - totalUnderlying = 0 → generation finalizes
   - currentGen increments to 1

3. User claims from finalized generation
   - User's rewards = 1,000 × 0.98e18 ÷ 1e18 = 980 srUSDS
   - User receives 980 srUSDS

---

### Story 2: Partial Conversion Over Multiple Epochs

**As** a user,
**I want to** receive my srUSDS gradually as capacity becomes available,
**So that** I can access converted tokens without waiting for full conversion.

**Flow:**

1. User subscribes 10,000 sUSDS
   - Receives 10,000 shares

2. Epoch 1: LCTS-pBEAM settles with capacity = 2,000
   - 2,000 sUSDS converts to 1,960 srUSDS
   - rewardPerToken = 0.196e18
   - totalUnderlying = 8,000

3. User claims rewards (without exiting)
   - Receives 10,000 × 0.196e18 ÷ 1e18 = 1,960 srUSDS
   - Still has 10,000 shares, rewardDebt updated

4. Epoch 2: LCTS-pBEAM settles with capacity = 3,000
   - 3,000 sUSDS converts to 2,940 srUSDS
   - rewardPerToken = 0.196e18 + (2,940 × 1e18 ÷ 10,000) = 0.49e18
   - totalUnderlying = 5,000

5. User claims again
   - Pending = 10,000 × (0.49e18 - 0.196e18) ÷ 1e18 = 2,940 srUSDS
   - Total received so far: 4,900 srUSDS

6. (Process continues until generation finalizes)

---

### Story 3: Late Subscriber Joins Existing Generation

**As** a user,
**I want to** join a generation that already has subscribers,
**So that** I can participate in the current queue.

**Flow:**

1. Alice subscribes 1,000 sUSDS (first subscriber)
   - Alice: 1,000 shares
   - totalShares = 1,000, totalUnderlying = 1,000

2. LCTS-pBEAM settles with capacity = 200
   - 200 sUSDS converts to 196 srUSDS
   - rewardPerToken = 0.196e18
   - totalUnderlying = 800

3. Bob subscribes 800 sUSDS
   - Bob's shares = 800 × 1,000 ÷ 800 = 1,000 shares
   - totalShares = 2,000, totalUnderlying = 1,600
   - Bob's rewardDebt = 0.196e18 (he doesn't get Alice's past rewards)

4. LCTS-pBEAM settles with capacity = 1,600 (drains generation)
   - 1,600 sUSDS converts to 1,568 srUSDS
   - rewardPerToken = 0.196e18 + (1,568 × 1e18 ÷ 2,000) = 0.98e18
   - Generation finalizes

5. Alice claims:
   - Rewards = 1,000 × (0.98e18 - 0) ÷ 1e18 = 980 srUSDS

6. Bob claims:
   - Rewards = 1,000 × (0.98e18 - 0.196e18) ÷ 1e18 = 784 srUSDS

**Note:** Alice's 196 srUSDS from the first epoch plus 784 from the second = 980 total. Bob only receives rewards from after his entry.

---

### Story 4: User Exits Before Generation Completes

**As** a user,
**I want to** exit the queue early and get my assets back,
**So that** I can use my funds elsewhere.

**Flow:**

1. User subscribes 5,000 sUSDS
   - Receives 5,000 shares

2. LCTS-pBEAM settles with capacity = 1,000
   - 1,000 sUSDS converts to 980 srUSDS
   - rewardPerToken = 0.196e18
   - totalUnderlying = 4,000

3. User decides to exit (claim and exit)
   - Pending rewards = 5,000 × 0.196e18 ÷ 1e18 = 980 srUSDS
   - Proportional underlying = 5,000 × 4,000 ÷ 5,000 = 4,000 sUSDS
   - **User receives both:** 980 srUSDS (reward asset) + 4,000 sUSDS (subscribe asset)
   - totalShares = 0, totalUnderlying = 0
   - User has fully exited the queue

---

### Story 5: User Subscribes Across Generations

**As** a user,
**I want to** subscribe again after my previous generation finalized,
**So that** I can continue participating.

**Flow:**

1. User subscribes 1,000 sUSDS in Generation 0
   - Receives 1,000 shares in Gen 0

2. Generation 0 fully converts and finalizes
   - User has unclaimed position in Gen 0

3. User subscribes 500 sUSDS (new subscribe triggers settlement of old position)
   - System settles Gen 0 position: user receives srUSDS rewards
   - User receives 500 shares in Gen 1
   - Old Gen 0 position is cleared

---

### Story 6: Settlement Cycle with Lock Period

**As** a user,
**I want to** understand how my position is affected by the settlement cycle,
**So that** I can plan my deposits and withdrawals.

**Flow (Weekly Mode Example):**

1. **Monday:** User subscribes $10,000 sUSDS into Gen 1
   - Gen 1 is ACTIVE
   - User can withdraw at any time

2. **Before lock time:** User decides to stay
   - Still can withdraw if desired

3. **Lock time (Tue 12:00 UTC):** Processing Period begins
   - Gen 1 → LOCKED (user cannot withdraw)
   - Gen 2 → ACTIVE (new deposits go here)
   - User's friend deposits $5,000 into Gen 2

4. **During lock period:** User tries to withdraw
   - **Rejected** — Gen 1 is locked
   - User can claim accrued rewards but cannot exit

5. **Settlement time (Wed 12:00 UTC):** Moment of Settlement
   - Settlement capacity: $6,000
   - Gen 1 ($10,000) receives $6,000 proportionally
   - User receives $6,000 worth of srUSDS, $4,000 sUSDS remains
   - Gen 1 → ACTIVE (unlocked)

6. **After settlement:** User can now withdraw
   - User exits with remaining $4,000 sUSDS + any srUSDS rewards
   - Or user can stay for next settlement cycle

**Note:** In weekday mode, the same pattern applies daily (Mon-Fri) with a 3-hour lock period (12:00-15:00 UTC).

---

### Story 7: Multi-Cycle Generation Spanning

**As** a user,
**I want to** understand what happens when demand exceeds capacity for multiple cycles,
**So that** I know how long I might wait.

**Flow (Weekly Mode Example):**

1. **Cycle 1:** User subscribes $100,000 sUSDS
   - High demand, low capacity
   - Cycle 1 settlement: $20,000 converted (capacity limited)
   - User has $80,000 remaining in Gen 1

2. **Cycle 2:** Gen 1 locks again with $80,000
   - Settlement capacity: $25,000
   - User receives $25,000 more srUSDS
   - $55,000 remaining

3. **Cycle 3:** Gen 1 locks again with $55,000
   - Settlement capacity: $55,000+
   - Gen 1 fully drains → FINALIZED
   - User claims final srUSDS

**Note:** Throughout this process, the user's position was locked at each lock time and unlocked at each settlement time. They could have exited after any settlement (while ACTIVE) if they chose. In weekday mode, this same pattern occurs daily.

---

### Story 8: RedeemQueue — Converting srUSDS to sUSDS

**As** a user,
**I want to** convert my srUSDS back to sUSDS,
**So that** I can exit the restricted token.

**Flow:**

1. User redeems 1,000 srUSDS into RedeemQueue
   - Receives 1,000 shares
   - totalUnderlying = 1,000 (srUSDS)

2. LCTS-pBEAM settles with redeemCapacity = 500
   - 500 srUSDS converts to (e.g.) 510 sUSDS
   - rewardPerToken = 0.51e18
   - totalUnderlying = 500

3. User claims rewards
   - Receives 510 sUSDS
   - Still has 1,000 shares, 500 srUSDS proportionally remaining

4. LCTS-pBEAM settles with redeemCapacity = 500 (drains generation)
   - 500 srUSDS converts to 510 sUSDS
   - Generation finalizes

5. User claims from finalized generation
   - Receives remaining 510 sUSDS
   - Total received: 1,020 sUSDS

---

## Edge Cases

### Empty Generation

**Scenario:** Generation is created but drains in the same epoch.

- User subscribes 100 sUSDS
- LCTS-pBEAM settles with capacity = 100 (or more)
- Entire generation converts and finalizes immediately
- User can claim rewards right away

**Handling:** Normal finalization logic applies; no special case needed.

---

### Zero Capacity Epoch

**Scenario:** LCTS-pBEAM sets capacity to 0.

- No conversion occurs
- rewardPerToken remains unchanged
- totalUnderlying remains unchanged
- Generation persists

**Handling:** Settlement function exits early if capacity is 0 or totalUnderlying is 0.

---

### Last User Exits Current Generation

**Scenario:** The only user in a generation exits before finalization.

- User calls claim-and-exit
- totalShares goes to 0
- totalUnderlying goes to 0
- Generation does NOT finalize (finalization only happens via settle())

**Handling:**
- Generation remains active but empty
- Next subscriber starts fresh with 1:1 share ratio
- If LCTS-pBEAM calls settle, nothing happens (totalUnderlying = 0)

---

### Multiple Users Exit Partially

**Scenario:** Some users exit while others remain.

- Alice: 1,000 shares, Bob: 1,000 shares
- totalShares = 2,000, totalUnderlying = 2,000

- Alice exits:
  - Receives 1,000 underlying (proportional)
  - totalShares = 1,000, totalUnderlying = 1,000

- Bob remains with 1,000 shares
- Bob's proportional claim is now 1,000 underlying (100% of remaining)

**Handling:** Share/underlying ratio is maintained correctly; remaining users' proportional claims increase.

---

### User Subscribes Zero

**Scenario:** User calls subscribe with amount = 0.

**Handling:** Should revert or be rejected; zero subscribes have no meaningful effect.

---

### Rounding

**Scenario:** Share calculations result in non-integer values.

- Share minting: shares = amount × totalShares ÷ totalUnderlying
- Reward claiming: rewards = shares × deltaRewardPerToken ÷ 1e18

**Handling:**
- Use standard integer division (round down)
- Precision loss accumulates in contract's favor (dust remains)
- 1e18 precision on rewardPerToken minimizes per-user rounding errors

---

### User Wants to Exit During Lock Period

**Scenario:** User has position in locked generation and urgently needs to withdraw.

- User deposited before lock time, generation locked at processing period start
- User realizes during lock period they need the funds

**Handling:**
- User CANNOT withdraw during lock period (lock time → settlement time)
- User must wait until after settlement
- After settlement, if generation is not finalized, user can exit with remaining underlying
- The lock period duration (24 hours for weekly mode, 3 hours for weekday mode) is a known trade-off for auction/settlement integrity

---

### Multiple Locked Generations at Settlement

**Scenario:** Two or more generations are locked simultaneously.

- Gen 1 from prior cycles: $40M remaining
- Gen 2 from last cycle: $60M remaining
- Both locked at current lock time

**Handling:**
- Both generations are processed proportionally in same settlement
- Capacity distributed based on relative underlying amounts
- All locked generations unlock after settlement (return to ACTIVE or FINALIZED)

---

### User in Locked Generation Tries to Deposit into New Generation

**Scenario:** User has position in locked generation, wants to deposit more.

- User is in Gen 1 (LOCKED)
- Gen 2 is now ACTIVE
- User tries to subscribe more sUSDS

**Handling:**
- **Blocked** — User cannot have positions in multiple generations simultaneously
- User must wait for Gen 1 settlement
- After settlement, if Gen 1 finalizes, user can then deposit into Gen 2
- If Gen 1 returns to ACTIVE (not finalized), user can add to their Gen 1 position

---

## Gas Complexity

| Operation | Complexity | Notes |
|-----------|------------|-------|
| subscribe/redeem | O(1) | May trigger O(1) settlement of old position |
| settle | O(1) | Processes all users proportionally in constant time |
| claim (current gen) | O(1) | Single storage read/write per user |
| claim (old gen) | O(1) | Single storage read/write per user |

**Storage per generation:** 2 slots (finalRewardPerToken + finalized flag)

---

## LCTS-pBEAM (Sentinel) Integration

### Interface

The LCTS-pBEAM (held by lpha-lcts Sentinel) calls queue management functions:

- **SubscribeQueue.lock()**: Lock the active generation at configured lock time
- **RedeemQueue.lock()**: Lock the active generation at configured lock time
- **SubscribeQueue.settle(uint256 subscribeCapacity)**: Process all locked generations at settlement time
- **RedeemQueue.settle(uint256 redeemCapacity)**: Process all locked generations at settlement time

### Settlement Cycle Operations

| Cycle Mode | Lock Time | Settlement Time | Function Called |
|------------|-----------|-----------------|-----------------|
| **Weekly** | Tuesday 12:00 UTC | Wednesday 12:00 UTC | `lock()` then `settle()` on both queues |
| **Weekday** | Mon-Fri 12:00 UTC | Mon-Fri 15:00 UTC | `lock()` then `settle()` on both queues |

### Capacity Determination

The Sentinel (lpha-lcts) determines capacity based on:

1. **Net flow netting** — Subscribe and redeem queues cancel each other out first
2. **OSRC auction results** — New srUSDS capacity from auction (for subscribes)
3. **Redemption limit** — Governance-set maximum weekly redemptions (for redeems)
4. **Target spread protection** — Only allows subscribe capacity that maintains target spread above SSR (see below)
5. **Guardrails** — cBEAM-defined bounds on settlement amounts

### Target Spread Mechanism (srUSDS)

srUSDS has a **target spread** (initially set by governance) above SSR. The Sentinel enforces this:

**Subscribe capacity throttling:**
- If OSRC auction demand provides yield ≥ target spread: allow full capacity
- If auction demand would result in yield < target spread: reduce subscribe capacity to maintain spread
- This prevents sudden rate crashes when supply exceeds auction demand

**Redemption capacity:**
- Fixed limit per week (governance-set)
- A "decent chunk" always processed each week (ensures liquidity)
- When redemptions exceed limit, remaining users wait in queue

```
Example:
- Target spread: 2% above SSR
- OSRC auction demand at 2.5%: Full subscribe capacity allowed
- OSRC auction demand at 1.5%: Subscribe capacity reduced to match demand at 2%+
- Result: Rates don't crash below target spread
```

### Exchange Rate

The srUSDS exchange rate is set each settle() call:
- **Increases** from yield (OSRC auction clearing rate × time)
- **Decreases** from haircuts when losses occur

---

## srUSDS Full Flow

This section describes the complete flow for srUSDS (Senior Risk USDS), which serves as the canonical LCTS example.

### Subscribe Flow

```
User (sUSDS) → SubscribeQueue → [settle()] → Holding System (sUSDS)
                                    ↓
                              srUSDS minted to user
```

1. User subscribes sUSDS into SubscribeQueue
2. User receives shares proportional to contribution
3. srUSDS-LCTS-Sentinel calls settle() with capacity
4. sUSDS transferred to Holding System
5. srUSDS minted to queue at current exchange rate
6. User claims srUSDS as rewards accrue

### Redeem Flow

```
User (srUSDS) → RedeemQueue → [settle()] → srUSDS burned
                                   ↓
                        Holding System → sUSDS to user
```

1. User redeems srUSDS into RedeemQueue
2. User receives shares proportional to contribution
3. srUSDS-LCTS-Sentinel calls settle() with capacity
4. srUSDS burned
5. sUSDS transferred from Holding System to queue
6. User claims sUSDS as rewards accrue

### Holding System

The Holding System is the backing contract for srUSDS:

**Holds:**
- sUSDS backing all outstanding srUSDS

**Receives funding from:**
- Prime PAUs (ongoing)
- Core Council multisig pre-funded via spells (temporary, 1-2 years)

**Provides:**
- sUSDS for redemptions
- sUSDS for loss coverage (applied as haircut to exchange rate)

---

## Extra Requirements

### USDS Auto-Conversion

Users may hold USDS rather than sUSDS. When subscribing to an srUSDS LCTS:
- USDS should auto-convert to sUSDS before entering the queue
- This ensures users earn savings yield while waiting in the queue
- Implementation details left to developers

### Architecture Decisions for Developers

The following decisions should be made during implementation:

1. **Mint/burn location**: Whether srUSDS minting/burning happens in the LCTS contract or a separate contract
2. **Holding System architecture**: Whether the Holding System is a separate contract or integrated with the srUSDS token contract

These are implementation choices that don't affect the business requirements.
