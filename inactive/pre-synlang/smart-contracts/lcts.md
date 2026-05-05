# Liquidity Constrained Token Standard (LCTS) — Business Requirements

**Status:** Draft
**Last Updated:** 2026-02-04

---

## Executive Summary

The Liquidity Constrained Token Standard defines a queue-based system for token conversions that cannot occur instantly due to external capacity constraints. Users subscribe assets into a queue, receive fungible shares representing their queue position, and receive converted assets over time as capacity becomes available.

The system consists of two independent queue contracts—**SubscribeQueue** and **RedeemQueue**—each using a "generation" model where all subscribers in the same generation share proportionally in the conversion capacity allocated to that generation.

**Key feature (simplified): single generation + hard lock.**

- Each queue has **at most one** current generation that is ACTIVE or LOCKED.
- During the daily lock window, it is **impossible** to deposit, withdraw, or claim from the current generation.
- The queue can be **DORMANT** (no active generation) when unused; a generation is created **lazily** when a user first enters.
- A generation may span multiple days if capacity is constrained; the same generation locks/settles/unlocks each day until drained.

LCTS integrates with the protocol-wide daily settlement cycle (see `accounting/daily-settlement-cycle.md`).

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
| **Halo** | Halo Unit shares | Claims on Halo Units — default for capacity-constrained products |

These LCTS tokens are held by a variety of participants. Folios are one example of a standardized holding structure for LCTS tokens, but direct holders (EOAs), institutional accounts, and other contract-based structures also hold these tokens independently.

**Risk capital tokens (srUSDS, TEJRC, TISRC)** MUST use LCTS. No alternative exists. These tokens represent risk capital that absorbs losses in exchange for yield.

**Halo Units** use LCTS as the default token standard when Halos face constraints on both subscribe (strategy limits) and redeem (liquidity). Alternatives exist for Halos: NFATS for bespoke deals, stablecoin-style vaults for instant liquidity.

### The Core Problem

Without LCTS, capacity-constrained conversions would be first-come-first-served, creating:

- Gas wars for conversion slots
- Unfair advantage to sophisticated users with bots
- Poor UX for regular users

LCTS eliminates this by pooling users in a generation and distributing capacity proportionally.

---

## Goals

### Primary Goals

1. **Rate-Limited Conversions**
   - Conversions (subscribe or redeem) occur only when external capacity is available
   - An LCTS-pBEAM (operated by an authorized LPHA beacon, e.g. `lpha-lcts`) controls how much capacity is allocated each epoch
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

4. **Immediate Exit Option (ACTIVE only)**
   - Users in the current **ACTIVE** generation can exit at any time
   - Exiting returns both: unconverted underlying plus any accrued rewards
   - Exit is a complete withdrawal — no partial exits
   - **LOCKED** generations cannot be exited; users must wait until unlock/settlement

### Design Principles

1. **Generation Isolation**: Each generation is independent; finalized generations are immutable
2. **Gas Efficiency**: All operations are O(1) regardless of user count
3. **Minimal Trust**: Only the LCTS-pBEAM can lock/settle; all other logic is deterministic
4. **Settlement Integration**: Generation lifecycle is synchronized with the daily settlement cycle

---

## Settlement Cycle Integration (Daily)

LCTS is designed for the daily settlement cadence:

| Event | Target Time (UTC) | Window | Effect |
|-------|-------------------|--------|--------|
| **Lock** | 13:00 | start of processing | Current generation becomes LOCKED |
| **Settlement** | 16:00 | by end of processing | Locked generation is processed |
| **Unlock / Dormant** | immediately after settlement | — | Generation becomes ACTIVE again, or FINALIZED → DORMANT |

The lock window is bounded (≤3 hours). Operationally, some deployments may choose to skip cycles by not calling `lock()`/`settle()`; this is handled in userspace. Protocol-level risk capital tokens are intended to run on the full daily cadence.

### Queue / Generation States

| State | Meaning | User Actions |
|-------|---------|--------------|
| **DORMANT** | No current generation exists | Subscribe/redeem creates a new generation; claims from finalized gens allowed |
| **ACTIVE** | Current generation accepts flow | Subscribe/redeem, claim, claim-and-exit |
| **LOCKED** | Frozen during processing | No actions on current gen; claims from finalized gens allowed |
| **FINALIZED** | Fully converted, immutable | Claim final rewards only |

---

## Why Lock?

The daily lock window serves critical functions:

1. **Allocation accuracy** — Capacity allocation relies on known queue quantities; if users could mutate the queue during processing, allocations would be invalidated
2. **Settlement certainty** — The LPHA beacon needs fixed quantities to calculate proportional distributions
3. **Accounting integrity** — Blocking deposits/withdrawals/claims eliminates race conditions around share ratios and reward accounting

---

## Capacity Sources at Settlement (srUSDS Example)

For paired subscribe/redeem systems like srUSDS, settlement capacity typically comes from:

1. **Net flow netting** — Subscribe and redeem queues cancel each other out first
2. **OSRC capacity** — New srUSDS capacity (governance-originated pre-auction; auction-originated once auctions are live)
3. **Redemption capacity** — Governance-set limit per epoch (for redeems)

```
Example:
- SubscribeQueue total: $100M waiting
- RedeemQueue total:    $30M waiting
- OSRC capacity: $30M new minting

Settlement:
1. Net flow netting: $30M subscribe ↔ $30M redeem (matched)
2. Apply OSRC capacity: $30M more subscribe converts
3. Result:
   - RedeemQueue: fully processed ($30M → sUSDS)
   - SubscribeQueue: $60M processed, $40M remains
```

**Implication:** At most one queue accumulates a multi-day backlog. The side with excess demand spans days; the other side clears each epoch.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   LCTS-pBEAM (LPHA beacon)                       │
│         Determines capacity each epoch, calls lock/settle        │
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

---

## Terminology

| Term | Definition |
|------|------------|
| **Generation** | A cohort of subscribers that share capacity together; identified by a numeric ID |
| **Current Generation** | The single generation that may be ACTIVE or LOCKED (or absent, if DORMANT) |
| **FINALIZED Generation** | A past generation with `totalUnderlying = 0` and frozen `finalRewardPerToken` |
| **Shares** | Internal accounting units representing a user's proportional claim on a generation; non-transferable |
| **Underlying** | Asset deposited into the queue (sUSDS for subscribes, srUSDS for redeems) |
| **Reward** | Asset received from conversion (srUSDS for subscribes, sUSDS for redeems) |
| **Epoch** | One settlement cycle on the daily cadence |
| **Lock Window** | Time window where the current generation is LOCKED (no queue mutations) |
| **Moment of Settlement** | The time when the locked generation is processed for the epoch |
| **Capacity** | Amount of underlying that can be converted in one settlement |
| **Net Flow Netting** | Subscribe and redeem queues canceling each other out, reducing net conversion needs |
| **rewardPerToken** | Cumulative rewards distributed per share (accumulator pattern) |
| **rewardDebt** | Snapshot of rewardPerToken at time of user's entry (prevents claiming pre-entry rewards) |
| **LCTS-pBEAM** | pBEAM (Process BEAM) permission token held by an authorized LPHA beacon operator that can call lock/settle |
| **lpha-lcts** | The LPHA (Low-Power High-Authority) beacon operator that holds the LCTS-pBEAM. lpha-lcts is the beacon; LCTS-pBEAM is the permission it holds. See `synomics/macrosynomics/beacon-framework.md` for the beacon taxonomy |
| **Holding System** | Contract holding sUSDS backing srUSDS; receives funding, sources redemptions |

---

## Contract Behaviors (Per Queue)

### Generation State

Each queue maintains state for:

- **0 or 1 current generation** (ACTIVE or LOCKED), and
- **0+ finalized generations** (immutable, claimable).

**Current Generation State (if present):**

- **status**: ACTIVE | LOCKED
- **totalShares**
- **totalUnderlying**
- **rewardPerToken** (1e18 precision)

**Finalized Generation State (per genId):**

- **finalRewardPerToken**

### Generation Lifecycle

```
DORMANT ──(first subscribe/redeem)──► ACTIVE ──(lock)──► LOCKED ──(settle)──► ACTIVE
   ▲                                                         │
   │                                                         └────► FINALIZED → DORMANT
   │                                                              (if fully drained)
   └──────────────(last user exits; queue empty)──────────────────────────────────────┘
```

Rules:

1. A queue may be **DORMANT** (no current generation) when unused.
2. A user entering a dormant queue creates a new **ACTIVE** generation.
3. At lock time, the current generation becomes **LOCKED** (no new generation is created).
4. At settlement, the locked generation is processed. It either:
   - returns to **ACTIVE** (if `totalUnderlying > 0`), or
   - becomes **FINALIZED** and the queue becomes **DORMANT** (if fully drained).

### User Position State

Each user has one position per queue:

- **gen**: the generation ID this position belongs to
- **shares**: number of shares the user holds
- **rewardDebt**: rewardPerToken at time of entry (or last claim)

---

## SubscribeQueue Behaviors

### Subscribing

**Preconditions:**

- User has approved sufficient underlying to the queue contract
- Amount > 0
- Queue is **not LOCKED**

**Behavior:**

1. If the user has shares in a FINALIZED generation:
   - Settle that position first (see Settling below)
   - Clear the old position before proceeding

2. If the user has shares in a LOCKED generation:
   - **Blocked** — user must wait for settlement/unlock

3. If the queue is DORMANT:
   - Create a new generation and set it as the current ACTIVE generation

4. If the user already has shares in the ACTIVE generation:
   - Claim any pending rewards first (or equivalently, update rewardDebt to current rewardPerToken)

5. Calculate shares to mint:
   - If this is the first subscribe in the generation (`totalShares == 0`): `shares = amount` (1:1)
   - Otherwise: `shares = amount × totalShares ÷ totalUnderlying`

6. Update state:
   - `totalUnderlying += amount`
   - `totalShares += shares`
   - user.gen = current generation
   - user.shares += shares
   - user.rewardDebt = current rewardPerToken

7. Transfer underlying from user to queue contract

### Lock (LCTS-pBEAM Only)

**Preconditions:**

- Caller is the LCTS-pBEAM (held by an authorized LPHA beacon operator)
- Called at the configured lock time (daily target: 13:00 UTC)

**Behavior:**

- If the queue is DORMANT: no-op (nothing to lock)
- If current generation is ACTIVE: set it to LOCKED
- If already LOCKED: no-op or revert (implementation choice)

### Settlement (LCTS-pBEAM Only)

**Preconditions:**

- Caller is the LCTS-pBEAM
- Current generation exists and is LOCKED
- Called during the settlement window (daily target: settle by 16:00 UTC)
- `capacity` is the amount of underlying that can convert this epoch

**Behavior (single generation):**

1. Compute conversion amount:
   ```
   convertAmount = min(capacity, totalUnderlying)
   ```

2. Execute conversion:
   - Transfer `convertAmount` of underlying to the converter (e.g., Holding System)
   - Mint reward asset to the queue at current exchange rate
   - Update reward accumulator:
     ```
     rewardPerToken += rewardMinted × 1e18 ÷ totalShares
     ```
   - Reduce underlying:
     ```
     totalUnderlying -= convertAmount
     ```

3. Post-settlement state:
   - If `totalUnderlying == 0` (or `totalShares == 0`):
     - Store finalized state: `finalRewardPerToken = rewardPerToken`
     - Mark generation FINALIZED
     - Clear current generation → queue becomes DORMANT
   - Else:
     - Set status back to ACTIVE (unlocked)

### Claiming (Current Generation)

Claims against the current generation are only allowed when it is **ACTIVE**.

**Claim Rewards Only:**

- Pending rewards:
  ```
  pending = shares × (rewardPerToken - rewardDebt) ÷ 1e18
  ```
- Set `rewardDebt = rewardPerToken`
- Transfer `pending` reward asset to user

**Claim and Exit (Full Withdrawal):**

- Pending rewards:
  ```
  pending = shares × (rewardPerToken - rewardDebt) ÷ 1e18
  ```
- Proportional underlying:
  ```
  underlyingOut = shares × totalUnderlying ÷ totalShares
  ```
- Update totals:
  - `totalUnderlying -= underlyingOut`
  - `totalShares -= shares`
- Clear user position
- Transfer `pending` reward asset and `underlyingOut` underlying to user

### Lock Window Rules

When the current generation is **LOCKED**:

- **Deposits are blocked**
- **Withdrawals/exits are blocked**
- **Claims are blocked**

The only allowed user interaction is settling/claiming from **FINALIZED** generations (immutable).

### Settling (FINALIZED Generation)

**Preconditions:**

- User has shares in a FINALIZED generation

**Behavior:**

- Look up `finalRewardPerToken`
- Compute rewards:
  ```
  rewardsOut = shares × (finalRewardPerToken - rewardDebt) ÷ 1e18
  ```
- Clear user position
- Transfer `rewardsOut` reward asset to user

No underlying is returned for finalized generations (they drained to finalize).

---

## RedeemQueue Behaviors

The RedeemQueue is structurally identical to SubscribeQueue with asset directions reversed:

| Aspect | SubscribeQueue | RedeemQueue |
|--------|----------------|-------------|
| User action | subscribe with sUSDS | redeem with srUSDS |
| Underlying tracked | sUSDS | srUSDS |
| Reward distributed | srUSDS | sUSDS |
| Conversion direction | sUSDS → srUSDS | srUSDS → sUSDS |

All behaviors (subscribing, lock, settlement, claiming, settling) follow the same logic with these substitutions.

On settlement, srUSDS is burned and sUSDS is transferred from the Holding System to the queue for distribution.

---

## Invariants

### Share Fairness

1. **Proportional share minting**: `shares = amount × totalShares ÷ totalUnderlying`
2. **Equal reward per share**: rewardDebt prevents late subscribers from claiming earlier rewards

### Generation Integrity

3. **Finalized generations are immutable**: `finalRewardPerToken` never changes after finalization
4. **No residual underlying in finalized generations**: finalization requires `totalUnderlying == 0` (or queue empty)
5. **At most one current generation exists**: 0 or 1 generation is ACTIVE/LOCKED; no concurrent generations
6. **Lock blocks all current-gen mutations**: no deposits, exits, or claims on the current generation while LOCKED

### User Position Integrity

7. **One position per user per queue**: users cannot hold shares across multiple generations simultaneously
8. **Exit is always available while ACTIVE**: claim-and-exit works in ACTIVE state
9. **Exit/claim are blocked while LOCKED**: users must wait until settlement/unlock
10. **Shares are non-transferable**: queue positions cannot be transferred between addresses

### Conservation

11. **Underlying conservation**: `totalUnderlying` equals sum of users' proportional underlying claims
12. **Reward conservation**: rewards distributed equal rewards minted/received by the converter

---

## User Stories

### Story 1: Simple Subscribe and Full Conversion

1. User subscribes 1,000 sUSDS
   - First in generation: 1,000 shares
2. lpha-lcts settles with capacity = 1,000 (full conversion)
   - 1,000 sUSDS converts to (e.g.) 980 srUSDS
   - rewardPerToken = 0.98e18
   - totalUnderlying = 0 → FINALIZED → queue becomes DORMANT
3. User settles finalized generation and receives 980 srUSDS

---

### Story 2: Partial Conversion Over Multiple Daily Epochs

1. User subscribes 10,000 sUSDS → 10,000 shares
2. Day 1 settlement capacity = 2,000
   - rewardPerToken increases; totalUnderlying = 8,000
3. After settlement (ACTIVE), user claims rewards
4. Day 2 settlement capacity = 3,000
   - rewardPerToken increases; totalUnderlying = 5,000
5. User claims again
6. Process continues until drained → FINALIZED

---

### Story 3: Deposit Attempt During Lock

1. At 13:05 UTC, the queue is LOCKED for processing
2. User tries to subscribe 500 sUSDS
3. Transaction reverts: deposits are blocked during LOCKED
4. User retries after unlock (post-settlement) and succeeds

---

### Story 4: User Exits Before Generation Completes

1. User subscribes 5,000 sUSDS
2. After a partial settlement, user decides to exit during ACTIVE
3. User performs claim-and-exit:
   - Receives accrued srUSDS rewards + remaining proportional sUSDS

---

### Story 5: Queue Becomes Dormant, Then Restarts

1. Generation drains and finalizes at settlement
2. Queue becomes DORMANT (no current generation)
3. Later, a new user subscribes
4. A new generation is created and becomes ACTIVE

---

### Story 6: Multi-Epoch Spanning (Single Generation)

1. User subscribes $100,000 sUSDS
2. Day 1: capacity is limited; $20,000 converts; $80,000 remains
3. Day 2: $25,000 converts; $55,000 remains
4. Day 3: $55,000 converts; generation drains → FINALIZED → queue becomes DORMANT

Throughout: the generation is LOCKED during the daily lock window, and ACTIVE outside it.

---

### Story 7: RedeemQueue — Converting srUSDS to sUSDS

1. User redeems 1,000 srUSDS into RedeemQueue → 1,000 shares
2. Day 1 settlement capacity = 500
   - 500 srUSDS converts to (e.g.) 510 sUSDS; totalUnderlying = 500
3. User claims sUSDS during ACTIVE
4. Day 2: remaining converts; generation finalizes; user settles finalized generation

---

## Edge Cases

### Dormant Queue

**Scenario:** No one is using the queue; there is no current generation.

- A user enters → a new generation is created and becomes ACTIVE.

### Zero Capacity Epoch

**Scenario:** lpha-lcts sets capacity to 0 for an epoch.

- No conversion occurs; rewardPerToken unchanged.
- At settlement, the generation unlocks back to ACTIVE.

### Last User Exits the Current Generation

**Scenario:** The last user exits during ACTIVE.

- After exit, `totalShares == 0` and `totalUnderlying == 0`.
- The queue becomes DORMANT (implementation may clear the current generation).

### User Tries to Exit During Lock

**Scenario:** User needs funds during LOCKED.

- Withdrawals/exits are blocked until after settlement/unlock.
- Lock duration is bounded (≤3 hours on the daily schedule).

### Multiple Locked Generations

**Scenario:** Not possible under this model (no concurrent generations).

---

## Gas Complexity

| Operation | Complexity | Notes |
|-----------|------------|-------|
| subscribe/redeem | O(1) | May trigger O(1) settlement of a finalized position |
| lock | O(1) | Single status flip |
| settle | O(1) | Processes the single locked generation |
| claim / claim-and-exit | O(1) | Single storage read/write per user |
| settle (finalized) | O(1) | Single storage read/write per user |

---

## LCTS-pBEAM (LPHA Beacon) Integration

### Interface

The LCTS-pBEAM (held by the `lpha-lcts` beacon) calls:

- `SubscribeQueue.lock()`
- `RedeemQueue.lock()`
- `SubscribeQueue.settle(uint256 subscribeCapacity)`
- `RedeemQueue.settle(uint256 redeemCapacity)`

### Daily Operations

| Operation | Target Time (UTC) | Notes |
|----------|--------------------|------|
| Lock | 13:00 | Enter LOCKED; block all current-gen user actions |
| Settle | by 16:00 | Process locked generation; unlock or finalize |

### Capacity Determination (srUSDS)

The `lpha-lcts` beacon determines capacity based on:

1. Net flow netting
2. OSRC allocation (governance-originated pre-auction; auction results once auctions are live)
3. Per-epoch redemption limit (redeem side)
4. Target spread protection (subscribe side)
5. Guardrails (cBEAM-defined bounds)

### Target Spread Mechanism (srUSDS)

srUSDS has a governance-set **target spread** above SSR. The `lpha-lcts` beacon enforces this:

- If OSRC clearing yield (governance-set pre-auction; auction-cleared later) provides yield ≥ target spread: allow full subscribe capacity
- If demand would result in yield < target spread: reduce subscribe capacity to maintain spread

Redemption capacity is bounded by a governance-set per-epoch limit.

### Exchange Rate

The srUSDS exchange rate is updated each epoch:

- **Increases** from yield (OSRC clearing rate × time)
- **Decreases** from haircuts when losses occur

### Exchange Rate Query Interface (Fixed Rates Compatibility)

All LCTS tokens MUST expose a public on-chain function that returns the current exchange rate between the LCTS token and its underlying asset:

```
function exchangeRate() external view returns (uint256)
```

This returns the amount of underlying (in underlying precision) that 1e18 shares of the LCTS token are currently worth. The exchange rate changes at each settlement epoch as yield accrues or haircuts are applied.

This interface is required for integration with the **Fixed Rates Yield Splitter** (see `smart-contracts/fixed-rates.md`). The Yield Splitter uses the exchange rate to track yield accrual on deposited LCTS tokens and to correctly attribute yield between Principal Tokens (PT) and Yield Tokens (YT) across splitting buckets. Without a queryable exchange rate, LCTS tokens cannot participate in fixed-rate yield splitting.

---

## srUSDS Full Flow

### Subscribe Flow

```
User (sUSDS) → SubscribeQueue → [settle()] → Holding System (sUSDS)
                                    ↓
                              srUSDS minted to user (claimable)
```

### Redeem Flow

```
User (srUSDS) → RedeemQueue → [settle()] → srUSDS burned
                                   ↓
                        Holding System → sUSDS to user (claimable)
```

### Holding System

The Holding System is the backing contract for srUSDS:

**Holds:**
- sUSDS backing all outstanding srUSDS

**Receives funding from:**
- Prime PAUs (ongoing)
- Core Council multisig pre-funding (temporary)

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

1. Mint/burn location (in LCTS vs separate token contract)
2. Holding system architecture (separate contract vs integrated)

These are implementation choices that do not change the business requirements.

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| [`accounting/daily-settlement-cycle.md`](../accounting/daily-settlement-cycle.md) | Daily settlement timeline — LCTS lock/settle synchronized with this cycle |
| [`risk-framework/capital-formula.md`](../risk-framework/capital-formula.md) | srUSDS, TEJRC, TISRC as risk capital instruments in the capital formula |
| [`risk-framework/operational-risk-capital.md`](../risk-framework/operational-risk-capital.md) | ORC sizing linked to LCTS settlement cadence |
| [`smart-contracts/fixed-rates.md`](fixed-rates.md) | Fixed-rate yield splitting — requires LCTS exchange rate interface |
| [`sky-agents/halo-agents/portfolio-halo.md`](../sky-agents/halo-agents/portfolio-halo.md) | Portfolio Halos use LCTS as their token standard |
| [`roadmap/roadmap-overview.md`](../roadmap/roadmap-overview.md) | LCTS launches in Phase 4 |
