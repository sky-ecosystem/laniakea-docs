# Non-Fungible Allocation Token Standard (NFATS) — Business Requirements

**Status:** Draft
**Last Updated:** 2025-01-15

---

## Executive Summary

The Non-Fungible Allocation Token Standard defines a system for bespoke capital deployment deals between Primes and Halos. Unlike LCTS (which pools users into shared generations), NFATS treats each deal as an individual, non-fungible position represented by an NFAT (Non-Fungible Allocation Token).

Capital flows through **NFAT Facilities** — smart contracts that define a "buybox" of acceptable deal parameters. Primes queue sUSDS into a Facility. The Halo (via Sentinel) claims from queues when deals are struck, minting an NFAT that represents a claim on the capital deployment. Each NFAT represents a claim on a distinct **Halo Unit** — a governance-level construct that is bankruptcy remote from other units within the same Halo.

Deal terms (APY, duration, maturity conditions) are tracked offchain in the **Synome**, while the onchain NFAT tracks only custody and ownership.

**Key principles:**
- **Onchain** = custody, ownership, facility parameters
- **Offchain (Synome)** = deal terms, yield schedules, maturity conditions
- **Each NFAT = claim on one Halo Unit** = bankruptcy remote isolation

---

## Why NFATS Exists

NFATS solves a different problem than LCTS:

| Scenario | Best Fit |
|----------|----------|
| Many users, same terms, shared capacity | LCTS |
| Individual deals, bespoke terms, named counterparties | NFATS |

### When to Use NFATS

- Asset manager partnerships with negotiated terms
- Deals where each depositor has different yield, duration, or conditions
- Situations requiring transferable positions (secondary market, collateralization)
- Regulated contexts where counterparty identity matters

### When to Use LCTS

- Open participation with uniform terms
- Capacity-constrained strategies where fair distribution matters
- Scenarios where fungibility and pooling are desirable

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              HALO                                       │
│                                                                         │
│   Operates one or more NFAT Facilities                                  │
│   Each Facility = separate smart contract with its own buybox           │
│                                                                         │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
            ┌────────────────────────┼────────────────────────┐
            ▼                        ▼                        ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│  NFAT Facility A    │  │  NFAT Facility B    │  │  NFAT Facility C    │
│  (Senior Secured)   │  │  (Mezzanine)        │  │  (Structured)       │
│                     │  │                     │  │                     │
│  Buybox params:     │  │  Buybox params:     │  │  Buybox params:     │
│  - 6-12mo term      │  │  - 12-24mo term     │  │  - Custom           │
│  - 8-12% APY        │  │  - 12-18% APY       │  │                     │
│                     │  │                     │  │                     │
│  Queue:             │  │  Queue:             │  │  Queue:             │
│  - Prime X: 50M     │  │  - Prime Y: 20M     │  │  - Prime X: 10M     │
│  - Prime Y: 30M     │  │                     │  │                     │
│                     │  │                     │  │                     │
│  Redeem Contract:   │  │  Redeem Contract:   │  │  Redeem Contract:   │
│  (Halo deposits     │  │  (funds awaiting    │  │  (funds awaiting    │
│   funds here)       │  │   claim)            │  │   claim)            │
└──────────┬──────────┘  └──────────┬──────────┘  └──────────┬──────────┘
           │                        │                        │
           ▼                        ▼                        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           MINTED NFATs                                  │
│                                                                         │
│   NFAT #1: 25M, Prime X, Facility A  →  Halo Unit (bankruptcy remote)   │
│   NFAT #2: 15M, Prime Y, Facility A  →  Halo Unit (bankruptcy remote)   │
│   NFAT #3: 20M, Prime Y, Facility B  →  Halo Unit (bankruptcy remote)   │
│                                                                         │
│   Terms stored in Synome (APY, maturity date, payment schedule)         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Redemption Flow (Bullet Loan):**
```
At Maturity:

  HALO                           FACILITY                         PRIME
    │                               │                               │
    │  1. Deposit funds into        │                               │
    │     redeem contract           │                               │
    │  ─────────────────────────►   │                               │
    │     (required, penalties      │                               │
    │      if late)                 │                               │
    │                               │                               │
    │                               │   2. Call redeem function,    │
    │                               │      specify NFAT             │
    │                               │   ◄─────────────────────────  │
    │                               │                               │
    │                               │   3. NFAT burned,             │
    │                               │      funds released           │
    │                               │   ─────────────────────────►  │
    │                               │                               │
```

---

## Components

### 1. NFAT Facility

Each NFAT Facility is a **PAU** (Controller + ALMProxy + RateLimits) with NFAT-specific extensions. The PAU holds custody of all capital flowing through that Facility; the NFAT extensions handle queue mechanics and token minting.

```
NFAT Facility = PAU + NFAT Extensions
├── Controller (rate limits on claims, redemptions)
├── ALMProxy (holds custody of sUSDS from all NFATs in this Facility)
├── RateLimits (standard rate limit infrastructure)
│
└── NFAT Extensions:
    ├── Queue contract (share-based, per-depositor)
    ├── NFAT minting (ERC-721)
    └── Redeem contract
```

**Facility parameters (buybox):**
- Asset type / strategy description
- Term range (e.g., 6-12 months)
- APY range (e.g., 8-12%)
- Risk tier / rating requirements
- Any other constraints the Halo commits to

**Onboarding (open question):**

> **Note:** The exact onboarding mechanism for Primes to Facilities is an open design question. The flow is: Prime synomic governance approves the Facility → Prime can deposit into queue → Halo can claim. The specific governance and Configurator integration path needs further specification.

**Key behaviors:**
- One PAU per Facility
- Each Facility has its own queue contract and redeem contract
- All capital from that Facility's NFATs flows through the Facility's ALMProxy

### 2. Facility Queue

The queue uses **share-based accounting** congruent with LCTS, but without generations (since claiming is selective, not batch).

**Queue State:**

| State | Description |
|-------|-------------|
| totalShares | Total shares outstanding across all depositors |
| totalUnderlying | Total sUSDS held in the queue |
| shares[address] | Per-depositor share balance (non-transferable) |

**Subscribe (deposit):**

```
If totalShares == 0:
    shares = amount (1:1)
Else:
    shares = amount × totalShares ÷ totalUnderlying

Update: totalShares, totalUnderlying, user shares
Transfer: sUSDS from depositor to queue
```

**Withdraw:**

```
underlyingOut = shares × totalUnderlying ÷ totalShares

Update: totalShares -= shares, totalUnderlying -= underlyingOut, user shares = 0
Transfer: sUSDS from queue to depositor
```

- Available anytime (no lock period — unlike LCTS, there's no batch settlement requiring a lock)
- Complete withdrawal only (like LCTS "claim and exit")

**Claim (Sentinel only):**

```
claim(address target, uint256 amount)

sharesToBurn = amount × totalShares ÷ totalUnderlying
Require: target has sufficient shares

Update: totalShares -= sharesToBurn, totalUnderlying -= amount, target shares -= sharesToBurn
Transfer: sUSDS from queue to Facility ALMProxy
Mint: NFAT to target
```

**Comparison with LCTS:**

| Aspect | LCTS | NFATS Queue |
|--------|------|-------------|
| Share calculation | amount × totalShares ÷ totalUnderlying | same |
| Shares transferable | No (internal accounting) | No (internal accounting) |
| Generations | Yes (batch settlement needs lock) | No (selective claiming) |
| Lock period | Yes (Tue noon → Wed noon) | No |
| Settlement | Batch, proportional to all | Selective: Halo picks (address, amount) |
| Output | Rewards accrue over time | NFAT minted at claim |

### 3. Deal NFAT (ERC-721)

Minted when Halo claims from a queue. Each NFAT represents a claim on one bespoke deal, corresponding to a separate **Halo Unit** (a governance-level construct, bankruptcy remote from other units).

**Onchain data (minimal):**

| Field | Description |
|-------|-------------|
| `tokenId` | Unique identifier |
| `facility` | Reference to the NFAT Facility contract |
| `principal` | Original sUSDS amount claimed |
| `depositor` | Original Prime address |
| `mintedAt` | Timestamp when deal was struck |

**Offchain data (Synome):**
- Deal terms (APY, duration, special conditions)
- Payment schedule (bullet, amortizing, periodic interest)
- Maturity date and conditions
- Underlying deployment details

**Transferability:**
- NFATs are transferable by default
- Halo can optionally restrict transfers to whitelisted addresses (for KYC/regulatory requirements)

### 4. Redeem Contract

Each Facility has a redeem contract where the Halo deposits funds to make them available for Prime redemption.

**Flow:**
1. Halo deposits principal + yield into redeem contract (required at maturity, penalties if late)
2. Prime calls redeem function, specifying which NFAT
3. NFAT is burned (or spent for partial redemptions)
4. Funds released to Prime

**Key behaviors:**
- Halo must fund before Prime can redeem
- Prime controls timing of actual redemption (can delay past maturity if desired)
- NFAT acts as a "claim ticket" — burning it releases the funds

### 5. Redemption and Rewards

Redemption is fundamentally a two-way exchange: the NFAT flows one direction, cash (principal + yield) flows the other. The typical flow:

1. **Halo funds the redeem contract** — required at maturity, penalties if late
2. **Prime burns NFAT to claim** — at their convenience, can delay past maturity

The NFAT acts as a **claim ticket**: Halo loads funds, Prime burns ticket to collect.

**Payment Patterns:**

| Pattern | Halo Action | Prime Action | NFAT State |
|---------|-------------|--------------|------------|
| **Bullet loan** | Deposit principal + yield at maturity | Burn NFAT to claim | Burned |
| **Amortizing loan** | Deposit each payment as due | Spend NFAT to claim each payment | Principal reduced each time |
| **Periodic interest** | Deposit interest payments periodically | Claim interest (NFAT unchanged) | Active until final redemption |

**For multi-payment loans:**
- NFAT is "spent" rather than burned — recorded principal is reduced
- Each payment: Halo deposits → Prime spends partial NFAT → receives that tranche
- Final payment: Prime burns remaining NFAT

**Extensible Payment Delivery**

The patterns above describe the core mechanisms, but payment delivery should be extensible to support additional flows — including direct transfers from the Halo's PAU to the Prime's PAU where the Prime takes no action and simply receives funds. The exact mechanics of extended payment flows are intentionally left undefined for now; the standard should accommodate them without requiring changes to the core NFAT structure.

---

## Deal Lifecycle

**1. Onboarding**
- Prime synomic governance approves deployment into NFAT Facility
- Govops onboards Facility via configurator (rate limits) or timelock (BEAMstate)

**2. Queue**
- Prime deposits sUSDS into their queue within the Facility
- Queue balance increases; Prime can withdraw anytime before claim

**3. Claim (deal struck)**
- Halo (via Sentinel) claims from Prime's queue (specifying amount)
- sUSDS transferred to Halo
- NFAT minted to Prime (representing a claim on a new Halo Unit)
- Deal terms recorded in Synome (APY, term, maturity date)
- Queue balance reduced by claimed amount

**4. Deployment**
- Halo deploys capital to underlying strategy (RWA, structured credit, custodian, etc.)
- NFAT holder can transfer/sell position at any time (subject to whitelist if enabled)

**5. Lifecycle**
- For bullet loans: nothing happens until maturity
- For other structures: Halo deposits payments per Synome schedule, Prime claims as available

**6. Maturity**
- Halo deposits principal + yield into Facility redeem contract (required, penalties if late)
- Prime burns NFAT to claim funds (at their convenience)
- Deal closed

---

## Behaviors

### Facility Queue Behaviors

**Prime actions:**
- **Deposit**: Prime adds sUSDS to their queue in a Facility
- **Withdraw**: Prime removes sUSDS from their queue (only possible before Halo claims)
- **View balance**: Anyone can check the queued balance for any Prime in any Facility

### NFAT Behaviors

**Halo actions (via Sentinel):**
- **Claim**: Take sUSDS from a Prime's queue and mint an NFAT
  - Specifies: which Prime, how much to claim
  - Results in: sUSDS moves to Halo, new NFAT minted, Synome records deal terms
- **Fund redeem**: Deposit funds into Facility redeem contract
  - Specifies: which NFAT, amount (principal + yield)
  - Results in: funds available for Prime to claim
  - Required at maturity, penalties if late

**Prime/Holder actions:**
- **Redeem (burn)**: Burn NFAT to claim funds from redeem contract
  - Specifies: which NFAT
  - Results in: NFAT burned, funds transferred to holder
  - Only works if Halo has funded the redemption
- **Redeem (spend)**: Spend partial NFAT to claim a payment (for multi-payment loans)
  - Specifies: which NFAT, payment amount
  - Results in: NFAT principal reduced, funds transferred to holder
- **Transfer**: Transfer NFAT to another address (standard ERC-721)
  - New holder inherits all rights (future payments, redemption)

**View functions:**
- Get queue balance for a Prime in a Facility
- Get principal amount for an NFAT
- Get original depositor for an NFAT
- Get mint timestamp for an NFAT
- Get Facility reference for an NFAT
- Get funded amount available for redemption

### Optional: Transfer Restrictions

- Halo can enable a whitelist mode where only approved addresses can receive NFAT transfers
- Halo can add/remove addresses from the whitelist
- When whitelist is active, transfers to non-whitelisted addresses are blocked

---

## Scenarios

### Scenario 1: Basic Bullet Loan (Happy Path)

**Setup:** Prime X wants to deploy into Halo 123's senior secured Facility.

1. **Onboarding**
   - Prime X synomic governance approves NFAT Facility 123
   - Govops sets rate limit of 100M for Prime X in Facility 123

2. **Queue**
   - Prime X deposits 50M sUSDS into Facility 123 queue
   - Queue balance: 50M

3. **Claim**
   - Halo 123 Sentinel claims 25M from Prime X's queue
   - NFAT #1 minted to Prime X (25M principal)
   - Synome records: 6-month term, 10% APY, maturity 2025-07-15
   - Queue balance: 25M remaining

4. **Lifecycle**
   - Nothing happens (bullet loan)
   - Prime X could transfer NFAT #1 if desired

5. **Maturity (2025-07-15)**
   - Halo 123 deposits 26.25M sUSDS into Facility 123 redeem contract (25M principal + 1.25M yield)
   - Prime X burns NFAT #1
   - Prime X receives 26.25M sUSDS

**Result:** Prime X deployed 25M for 6 months, received 10% APY.

---

### Scenario 2: Partial Queue Claim

**Setup:** Prime X has 50M queued, Halo only wants 30M.

1. Prime X deposits 50M into Facility queue
2. Halo claims 30M → NFAT #1 minted (30M principal)
3. Prime X still has 20M in queue
4. Later, Halo claims another 15M → NFAT #2 minted (15M principal)
5. Prime X withdraws remaining 5M from queue

**Result:** Prime X holds two separate NFATs from same Facility, each representing a claim on a distinct Halo Unit.

---

### Scenario 3: Prime Withdraws Before Claim

**Setup:** Prime X queues funds but changes their mind.

1. Prime X deposits 50M into Facility 123 queue
2. Market conditions change; Prime X wants capital elsewhere
3. Prime X withdraws 50M from queue (Halo hasn't claimed yet)
4. Queue balance: 0

**Result:** No deal struck, Prime X retains full capital. Queue is non-binding until claimed.

---

### Scenario 4: Amortizing Loan (Multi-Payment)

**Setup:** NFAT with quarterly principal + interest payments over 12 months.

1. **Claim**
   - Halo claims 40M from Prime X queue
   - NFAT #1 minted (40M principal)
   - Synome records: 4 quarterly payments of 10M principal + interest

2. **Q1 Payment**
   - Halo deposits 10.8M (10M principal + 0.8M interest)
   - Prime X spends NFAT #1 to claim payment
   - NFAT #1 principal reduced to 30M

3. **Q2, Q3 Payments**
   - Same pattern; NFAT principal reduces to 20M, then 10M

4. **Q4 Final Payment**
   - Halo deposits 10.8M
   - Prime X burns NFAT #1 (final redemption)
   - NFAT #1 destroyed

**Result:** Amortizing structure with NFAT "spent" over time rather than burned at once.

---

### Scenario 5: NFAT Transfer (Secondary Market)

**Setup:** Prime X holds an NFAT but wants liquidity before maturity.

1. Prime X holds NFAT #1 (25M principal, 4 months remaining, 10% APY)
2. Prime Y offers to buy NFAT #1 for 25.5M (slight premium)
3. Prime X transfers NFAT #1 to Prime Y (standard ERC-721 transfer)
4. At maturity, Halo funds redemption
5. Prime Y burns NFAT #1 and receives 26.25M

**Result:** Prime X exits early with small profit; Prime Y earns yield for remaining term.

---

### Scenario 6: Halo Late on Funding (Penalty)

**Setup:** Halo doesn't fund redemption by maturity date.

1. NFAT #1 matures on 2025-07-15
2. Halo fails to deposit funds by maturity
3. Penalty mechanism triggers (defined in Synome/Facility terms)
4. Halo deposits funds on 2025-07-20 (5 days late) + penalty amount
5. Prime X burns NFAT and receives principal + yield + penalty

**Result:** Halo penalized for late funding; Prime made whole plus compensation.

---

### Scenario 7: Prime Delays Redemption

**Setup:** Halo funds on time, but Prime doesn't claim immediately.

1. NFAT #1 matures on 2025-07-15
2. Halo deposits 26.25M into redeem contract on 2025-07-14
3. Prime X is busy / wants to batch claims / doesn't need funds yet
4. Prime X burns NFAT #1 on 2025-08-01

**Result:** No penalty to Prime for delayed claim. Funds sit in redeem contract until claimed.

---

### Scenario 8: Multiple Primes, Same Facility

**Setup:** Two Primes deploy into the same Facility.

1. Prime X deposits 50M into Facility 123 queue
2. Prime Y deposits 30M into Facility 123 queue
3. Halo claims 25M from Prime X → NFAT #1
4. Halo claims 30M from Prime Y → NFAT #2
5. Halo claims another 25M from Prime X → NFAT #3

**Result:** Three distinct NFATs, each representing a claim on a separate Halo Unit, all from same Facility.

---

### Scenario 9: Prime Deploys Across Multiple Facilities

**Setup:** Prime X wants exposure to different risk profiles.

1. Prime X onboards to Facility A (senior secured, 8% APY) and Facility B (mezz, 14% APY)
2. Prime X deposits 30M into Facility A queue
3. Prime X deposits 10M into Facility B queue
4. Halo claims from both queues
5. Prime X holds NFAT from Facility A (lower risk) and NFAT from Facility B (higher risk)

**Result:** Prime X has diversified exposure across multiple Facilities/strategies.

---

### Scenario 10: Transfer Restriction (Whitelist)

**Setup:** Facility has KYC requirements; transfers restricted to approved addresses.

1. Facility 123 has whitelist enabled
2. Prime X (whitelisted) receives NFAT #1
3. Prime X tries to transfer to Random Address → blocked
4. Prime X requests Prime Y be added to whitelist
5. Halo adds Prime Y to whitelist
6. Prime X transfers NFAT #1 to Prime Y → succeeds

**Result:** Transfers only between KYC'd/approved parties.

---

### Scenario 11: Halo Never Funds Redemption (Default)

**Setup:** Halo fails to fund and doesn't respond.

1. NFAT #1 matures on 2025-07-15
2. Halo doesn't fund redemption
3. Grace period passes, penalties accumulate
4. Halo still doesn't fund
5. Default procedures trigger (defined in Facility/Synome terms)
6. Recovery process initiated (collateral liquidation, insurance, etc.)

**Result:** Default handling per agreed terms. NFAT holder has claim on recovery proceeds.

---

### Scenario 12: Queue While Holding Existing NFAT

**Setup:** Prime wants to deploy more while already holding an NFAT.

1. Prime X holds NFAT #1 (25M) from previous claim
2. Prime X deposits another 20M into same Facility queue
3. Halo claims 20M → NFAT #2 minted
4. Prime X now holds NFAT #1 and NFAT #2 (claims on separate Halo Units)

**Result:** No limit on concurrent positions; each NFAT is independent.

---

## NFATS vs LCTS Comparison

| Aspect | LCTS | NFATS |
|--------|------|------|
| **Model** | Pool / ETF | Individual deals |
| **Position type** | Fungible shares | Non-fungible NFAT |
| **Terms** | Same for all in generation | Bespoke per deal |
| **Queue** | Shared across generation | Individual per depositor |
| **Capacity allocation** | Proportional distribution | Per-deal (Halo decides) |
| **Settlement** | Batch (weekly cycle) | Per-deal (anytime) |
| **Transferability** | Non-transferable shares | Transferable NFAT (optionally restricted) |
| **Exit before settlement** | Withdraw from active generation | Withdraw from queue before claim |
| **Redemption initiation** | Holder-initiated only | Either party (request/fulfill or direct) |
| **Reward mechanism** | rewardPerToken accumulator | Flexible (offchain-driven) |
| **Onchain complexity** | Higher (generations, settlement) | Lower (queue + NFAT) |
| **Offchain complexity** | Lower (uniform terms) | Higher (per-deal tracking) |

---

## NFATS as RiverUSDS Superset

NFATS is designed to cover all RiverUSDS (ERC-7540 async vault) use cases when deposits are pre-agreed and tokens have transfer restrictions:

| RiverUSDS Feature | NFATS Equivalent |
|-------------------|------------------|
| `maxDeposit` whitelist (pre-agreed caps) | Individual queue + Halo claim |
| Transfer restrictions | Optional whitelist mode |
| `requestRedeem` → `fulfillRequest` → `withdraw` | `requestRedeem` → `fulfillRedeem` (Pattern B) |
| Periodic rewards (`grantRewards` → `getReward`) | Pattern C: Periodic Rewards |
| Async rewards (`requestReward` → fulfill → claim) | Pattern D: Claimable Rewards |
| Fungible shares (same terms) | Each deal is an NFAT (explicit non-fungibility) |

**Key insight**: Redemption is a two-way exchange — NFAT in one direction, cash out the other. Either party can initiate by putting their side in first. This matches ERC-7540's request/fulfill pattern while also supporting Halo-initiated redemptions.

When all depositors have identical terms and transfer restrictions, NFATS effectively behaves like a restricted ERC-7540 vault — but with the flexibility to support bespoke terms per position when needed.

---

## Integration Notes

### Halo Sentinel

TBD — Sentinel integration for automated claims, reward distribution, and redemptions.

### ALM Controller Compatibility

NFATS requires custom ALM controller integration (similar to LCTS). The Halo's ALMProxy holds claimed sUSDS and sources redemption/reward payments.

### Halo Artifact

Deal terms should be recorded in the Halo Artifact for transparency and auditability. The NFAT's `tokenId` serves as the key linking onchain position to offchain terms.

---

## Design Rationale

### Why Individual Queues?

Shared queues (like LCTS generations) make sense when all participants receive identical treatment. For bespoke deals, individual queues:
- Allow depositors to signal interest without commitment
- Let the Halo selectively accept deals
- Avoid complexity of proportional distribution
- Enable partial claims (multiple deals with same depositor)

### Why NFATs?

ERC-20 tokens imply fungibility — any token is interchangeable with any other. When deals have different terms, forcing them into a fungible token creates friction:
- Transfer restrictions feel like hacks
- Per-holder accounting becomes complex
- The token doesn't represent what it claims to

NFATs make the non-fungibility explicit:
- Each position is clearly unique
- Transfers are natural (new holder inherits the deal)
- Secondary markets can price deals individually
- No pretense of fungibility

### Why Offchain Terms?

Putting all deal terms onchain would:
- Increase gas costs significantly
- Reduce flexibility for complex arrangements
- Require contract upgrades for new term types

Offchain terms with onchain custody provides:
- Maximum flexibility for bespoke arrangements
- Simple, auditable onchain contracts
- Easy extension to new deal structures

---

## Wrapped NFATs (Fractionalization)

An NFAT can optionally be wrapped in a fungible ERC-20 token, allowing the deal position to be split up and sold in pieces.

### How It Works

- The NFAT holder deposits their NFAT into a wrapper contract
- The wrapper mints fungible tokens representing fractional ownership of that specific NFAT
- Fractional token holders can trade their shares freely
- When the NFAT receives rewards or is redeemed, proceeds are distributed proportionally to fractional holders

### Use Cases

- **Liquidity**: NFAT holder wants partial liquidity without selling the entire position
- **Syndication**: Multiple parties want exposure to a single deal
- **Smaller denominations**: Large deals can be broken into accessible pieces
- **Secondary markets**: Fungible tokens are easier to trade on existing DEX infrastructure

### Key Characteristics

- Each wrapped NFAT has its own separate fungible token (not pooled across deals)
- The wrapper contract becomes the NFAT holder and receives all rewards/redemptions
- Fractional holders claim their proportional share from the wrapper
- Wrapping is optional — NFATs work fine without it

### Relationship to NFATS

| Aspect | Unwrapped NFAT | Wrapped NFAT |
|--------|----------------|--------------|
| **Ownership** | Single holder | Multiple fractional holders |
| **Transferability** | Whole position only | Fractional shares tradeable |
| **Rewards** | Direct to holder | Via wrapper to fractional holders |
| **Complexity** | Simple | Additional wrapper contract |

### Implementation Notes

- Wrapper is a separate contract, not part of core NFATS
- Can be deployed per-NFAT or as a factory pattern
- Reward claiming and redemption flows need to account for wrapper as intermediary
- Transfer restrictions on the underlying NFAT (if any) apply to the wrapper depositing/withdrawing

---

*Document Version: 0.3*
