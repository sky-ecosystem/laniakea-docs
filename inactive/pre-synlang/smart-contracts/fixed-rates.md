# Fixed Rates — Yield Splitter

**Status:** Draft
**Last Updated:** 2026-02-06

---

## Executive Summary

The Fixed Rates system enables any yield-bearing token in the Sky ecosystem to be split into a **Principal Token (PT)** and a **Yield Token (YT)** for a specific maturity date. PT holders lock in a fixed rate; YT holders receive all variable yield until maturity.

A single **Yield Splitter** contract manages all tokens and maturities through **splitting buckets** — one bucket per (token, maturity) pair. Anyone can create a new bucket for any supported token and any future maturity. PT and YT are standard ERC-20 tokens, traded on exchange halos (limit orderbook exchanges) — no custom AMM is required.

**Key feature:** Generic, permissionless yield splitting across the entire Sky token ecosystem — sUSDS, srUSDS, sSGA, srSGA, TEJRC, TISRC, Halo LCTS tokens, and any future yield-bearing token that exposes an exchange rate.

---

## Why Fixed Rates Exist

Variable-rate yield tokens (sUSDS earning SSR, srUSDS earning SSR + risk premium, etc.) expose holders to rate volatility. Users and institutions may want:

- **Fixed-rate exposure**: Lock in a known yield for a known period (buy PT at a discount)
- **Leveraged variable-rate exposure**: Amplify exposure to rate changes (buy YT)
- **Rate speculation**: Express a view on whether rates will rise or fall
- **Duration matching**: Match fixed liabilities with fixed-rate assets

Without a splitting mechanism, the only way to get fixed-rate exposure in the Sky ecosystem is through bespoke OTC deals. The Yield Splitter makes this self-service and composable.

---

## Goals

### Primary Goals

1. **Generic across all yield-bearing Sky tokens**
   - sUSDS, sSGA (ERC-4626 savings vaults)
   - srUSDS, srSGA, TEJRC, TISRC (LCTS risk capital tokens)
   - Halo LCTS tokens
   - Any future token that exposes the required exchange rate interface

2. **Single contract, many buckets**
   - One deployed Yield Splitter manages all (token, maturity) combinations
   - Each bucket is independent — no cross-bucket dependencies

3. **Permissionless bucket creation**
   - Anyone can create a new bucket for any supported token and any future maturity date
   - No governance approval required to split a new token or choose a new maturity

4. **Standard ERC-20 PT and YT**
   - PT and YT are fully transferable ERC-20 tokens
   - Tradeable on exchange halos via standard limit orderbooks

5. **No custom AMM**
   - Trading and price discovery happen on exchange halos (limit orderbook exchanges)
   - The Yield Splitter only handles splitting, merging, and redemption

### Design Principles

1. **Separation of splitting and trading**: The Yield Splitter is purely a token transformation contract; trading is handled by exchange halos
2. **Exchange rate as the only dependency**: The Yield Splitter requires exactly one thing from each supported token — a queryable on-chain exchange rate
3. **PT is a zero-coupon bond**: PT trades at a discount and redeems at par at maturity; the discount is the implied fixed rate
4. **YT captures all yield**: Between split and maturity, all yield accrual goes to YT holders
5. **Safe degradation**: If a token's exchange rate stops updating, PT holders are unaffected; YT simply earns no yield during that period

---

## Terminology

| Term | Definition |
|------|------------|
| **Yield Splitter** | The single contract that manages all splitting buckets |
| **Bucket** | A (token, maturity) pair with its own PT, YT, and accounting state |
| **Principal Token (PT)** | ERC-20 token redeemable 1:1 for the underlying asset at maturity (in accounting-asset terms) |
| **Yield Token (YT)** | ERC-20 token representing the right to all yield accrued on the deposited collateral until maturity; worthless after maturity |
| **Maturity** | The timestamp at which PT becomes redeemable and YT stops accruing |
| **Split** | Depositing a yield-bearing token and receiving equal quantities of PT and YT |
| **Merge** | Burning equal quantities of PT and YT to recover the deposited yield-bearing token (before maturity) |
| **Exchange Rate** | The on-chain queryable rate between a yield-bearing token and its underlying asset |
| **PY Index** | The Yield Splitter's tracked exchange rate for a bucket, used to compute yield attribution; ratchets upward only |
| **Underlying Asset** | The base asset that the yield-bearing token denominates against (e.g., USDS for sUSDS, sUSDS for srUSDS) |

---

## Supported Token Interface

Any yield-bearing token can be used with the Yield Splitter if it exposes:

```
function exchangeRate() external view returns (uint256)
```

This returns the current value of 1e18 token shares in underlying-asset terms. The exchange rate must be:
- Queryable on-chain at any time (view function)
- Monotonically non-decreasing under normal operation (yield accrual)
- Updated at least once per settlement epoch

**ERC-4626 vaults** (sUSDS, sSGA) satisfy this via `convertToAssets(1e18)`.

**LCTS tokens** (srUSDS, srSGA, TEJRC, TISRC, Halo LCTS tokens) satisfy this via the exchange rate query interface defined in `smart-contracts/lcts.md`.

### Token Registration

Before a token can be used in splitting buckets, it must be registered with the Yield Splitter. Registration records:
- The token address
- The underlying asset address
- The exchange rate function selector (defaulting to `exchangeRate()`)

Registration is permissionless — anyone can register a token as long as it exposes a valid exchange rate function. Registration is a one-time operation per token.

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                         Yield Splitter                                │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │  Token Registry                                              │     │
│  │  ┌──────────┬──────────────────┬─────────────────────────┐  │     │
│  │  │ Token    │ Underlying       │ Exchange Rate Fn         │  │     │
│  │  ├──────────┼──────────────────┼─────────────────────────┤  │     │
│  │  │ sUSDS    │ USDS             │ convertToAssets(1e18)    │  │     │
│  │  │ srUSDS   │ sUSDS            │ exchangeRate()           │  │     │
│  │  │ sSGA     │ SGA              │ convertToAssets(1e18)    │  │     │
│  │  │ srSGA    │ sSGA             │ exchangeRate()           │  │     │
│  │  │ TEJRC    │ (per-Prime)      │ exchangeRate()           │  │     │
│  │  │ ...      │ ...              │ ...                      │  │     │
│  │  └──────────┴──────────────────┴─────────────────────────┘  │     │
│  └─────────────────────────────────────────────────────────────┘     │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │  Splitting Buckets                                           │     │
│  │                                                              │     │
│  │  Bucket (sUSDS, 2026-06-30)                                  │     │
│  │    ├── PT-sUSDS-JUN26  (ERC-20 clone)                        │     │
│  │    ├── YT-sUSDS-JUN26  (ERC-20 clone)                        │     │
│  │    ├── PY Index: 1.045e18                                    │     │
│  │    └── Total deposited: 5,000,000 sUSDS                      │     │
│  │                                                              │     │
│  │  Bucket (srUSDS, 2026-09-30)                                 │     │
│  │    ├── PT-srUSDS-SEP26  (ERC-20 clone)                       │     │
│  │    ├── YT-srUSDS-SEP26  (ERC-20 clone)                       │     │
│  │    ├── PY Index: 1.012e18                                    │     │
│  │    └── Total deposited: 2,000,000 srUSDS                     │     │
│  │                                                              │     │
│  │  Bucket (TEJRC-SparkPrime, 2026-12-31)                       │     │
│  │    ├── PT-TEJRC-SP-DEC26                                     │     │
│  │    ├── YT-TEJRC-SP-DEC26                                     │     │
│  │    └── ...                                                   │     │
│  └─────────────────────────────────────────────────────────────┘     │
│                                                                      │
│  Trading: Exchange Halos (limit orderbook)                           │
│    PT and YT are standard ERC-20s → listed and traded on exchanges   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Bucket Lifecycle

```
(anyone calls createBucket) ──► ACTIVE ──────────────────────► MATURED
                                  │                               │
                                  │  split / merge / claimYield   │  redeemPT
                                  │  (normal operations)          │  (PT → underlying)
                                  │                               │
                                  └───────────────────────────────┘
```

### Creating a Bucket

**Preconditions:**
- Token is registered in the Token Registry
- Maturity timestamp is in the future
- No bucket already exists for this (token, maturity) pair

**Behavior:**

1. Deploy PT ERC-20 clone (via CREATE2 for deterministic address)
2. Deploy YT ERC-20 clone (via CREATE2 for deterministic address)
3. Initialize bucket state:
   - `token`: the yield-bearing token address
   - `maturity`: the maturity timestamp
   - `pyIndex`: current exchange rate of the token (snapshot at creation)
   - `ptToken`: deployed PT address
   - `ytToken`: deployed YT address
   - `totalDeposited`: 0

**Anyone can call this.** In practice, exchange halos will create buckets for the maturities they want to list markets for.

---

## Core Operations

### Split

Deposit a yield-bearing token and receive equal quantities of PT and YT.

**Preconditions:**
- Bucket exists and has not matured
- User has approved sufficient token to the Yield Splitter
- Amount > 0

**Behavior:**

1. Update PY Index (see Yield Accounting below)
2. Transfer `amount` of yield-bearing token from user to Yield Splitter
3. Calculate PT/YT to mint:
   ```
   ptAmount = amount × currentExchangeRate / 1e18
   ytAmount = ptAmount
   ```
   PT/YT are minted in underlying-asset-denominated units: 1 PT = 1 unit of underlying at maturity.
4. Mint `ptAmount` PT tokens to user
5. Mint `ytAmount` YT tokens to user
6. Record user's YT position for yield tracking:
   - `ytRewardIndex[user] = pyIndex`
7. Update `totalDeposited += amount`

**Example:** User deposits 100 sUSDS when sUSDS exchange rate is 1.05 USDS/sUSDS.
- `ptAmount = 100 × 1.05e18 / 1e18 = 105` PT-sUSDS (redeemable for 105 USDS worth at maturity)
- `ytAmount = 105` YT-sUSDS (earns yield on 100 sUSDS until maturity)

### Merge

Burn equal quantities of PT and YT to recover the deposited yield-bearing token. Available only before maturity.

**Preconditions:**
- Bucket exists and has not matured
- User holds equal amounts of PT and YT for this bucket
- Amount > 0

**Behavior:**

1. Update PY Index
2. Claim any pending yield for the user's YT position
3. Burn `amount` PT tokens from user
4. Burn `amount` YT tokens from user
5. Calculate yield-bearing tokens to return:
   ```
   tokensOut = amount × 1e18 / currentExchangeRate
   ```
6. Transfer `tokensOut` yield-bearing tokens to user
7. Update `totalDeposited -= tokensOut`

### Redeem PT (After Maturity Only)

Burn PT to receive the underlying asset at the maturity exchange rate.

**Preconditions:**
- Bucket has matured (`block.timestamp >= maturity`)
- User holds PT for this bucket
- Amount > 0

**Behavior:**

1. If this is the first redemption after maturity, snapshot the final exchange rate:
   ```
   finalExchangeRate = token.exchangeRate()   // captured once at first post-maturity interaction
   ```
2. Burn `amount` PT from user
3. Calculate yield-bearing tokens to release:
   ```
   tokensOut = amount × 1e18 / finalExchangeRate
   ```
4. Transfer `tokensOut` yield-bearing tokens to user (user receives them at their current value, which includes all yield up to the point of redemption)

**Note:** PT redeems for the underlying *accounting asset* value, not a fixed quantity of the yield-bearing token. 1 PT-sUSDS = 1 USDS worth of sUSDS at maturity.

### Claim Yield (YT Holders)

Claim accrued yield for YT held in a bucket. Available anytime before or at maturity.

**Preconditions:**
- User holds YT for this bucket
- There is unclaimed yield

**Behavior:**

1. Update PY Index
2. Calculate pending yield:
   ```
   yieldPerUnit = pyIndex - ytRewardIndex[user]
   pendingYield = ytBalance × yieldPerUnit / 1e18
   ```
3. Convert pending yield to yield-bearing tokens:
   ```
   tokensOut = pendingYield × 1e18 / currentExchangeRate
   ```
4. Update `ytRewardIndex[user] = pyIndex`
5. Transfer `tokensOut` yield-bearing tokens to user
6. Update `totalDeposited -= tokensOut`

**After maturity:** YT holders can claim any remaining unclaimed yield, but no further yield accrues. YT tokens have no redemption value — only the yield they accumulated.

---

## Yield Accounting (PY Index)

The PY Index tracks how much yield has accrued per unit of PT/YT since the bucket was created.

### Update Rule

```
newRate = token.exchangeRate()
pyIndex = max(pyIndex, newRate)    // ratchet: only goes up
```

The ratchet ensures that if a token's exchange rate temporarily drops (e.g., a haircut on srUSDS), the loss is absorbed by YT holders (they receive less yield) rather than affecting PT holders' principal claim.

### Yield Attribution

All yield generated by the deposited tokens between split time and maturity goes to YT holders. PT holders receive no yield — their return comes from buying PT at a discount (the implied fixed rate).

```
Implied Fixed Rate ≈ (Face Value / PT Price)^(1 / years_to_maturity) - 1
```

For example: PT-sUSDS maturing in 6 months trading at $0.97 implies a ~6.2% annualized fixed rate.

### Negative Yield (Haircut) Handling

If a token's exchange rate decreases (e.g., srUSDS takes a loss haircut):

1. PY Index does **not** decrease (ratchet)
2. YT yield accrual pauses — no new yield is distributed until the exchange rate recovers above the PY Index
3. PT redemption at maturity is based on the **actual exchange rate at maturity**, not the PY Index
4. If the exchange rate at maturity is below the PY Index (i.e., losses were never recovered), PT holders absorb the shortfall — they redeem below par

**Risk hierarchy:** YT absorbs moderate rate decreases (paused yield). PT absorbs extreme, unrecovered losses (below-par redemption). This mirrors zero-coupon bond credit risk.

---

## PT and YT Token Design

### Deployment

PT and YT tokens are deployed as minimal ERC-20 clones (EIP-1167 or equivalent) via CREATE2 for deterministic addresses. Each bucket gets its own PT and YT contract.

### Naming Convention

```
PT: "PT-{TOKEN}-{MATURITY}"    e.g. "PT-sUSDS-JUN26", "PT-srSGA-DEC26"
YT: "YT-{TOKEN}-{MATURITY}"    e.g. "YT-sUSDS-JUN26", "YT-srSGA-DEC26"
```

### Properties

| Property | PT | YT |
|----------|-----|-----|
| **ERC-20** | Yes | Yes |
| **Transferable** | Yes | Yes |
| **Tradeable on exchange halos** | Yes | Yes |
| **Denomination** | 1 PT = 1 underlying asset unit at maturity | 1 YT = yield on 1 underlying unit until maturity |
| **Value at maturity** | Redeemable at par (1:1 underlying) | Zero (no further yield) |
| **Value before maturity** | Trades at discount (discount = fixed rate) | Trades based on expected remaining yield |
| **Minting** | Only by Yield Splitter (on split) | Only by Yield Splitter (on split) |
| **Burning** | Only by Yield Splitter (on merge or redeem) | Only by Yield Splitter (on merge) |

### YT Transfer Hook

When YT is transferred between addresses, the Yield Splitter must update yield accounting:
- Settle pending yield for the sender
- Update `ytRewardIndex` for both sender and receiver

This requires YT token transfers to call back into the Yield Splitter. Implementation options:
- YT contract calls `Splitter.onYTTransfer(from, to, amount)` on every transfer
- Or the Yield Splitter itself is the YT token contract (internal accounting)

---

## Trading on Exchange Halos

PT and YT are standard ERC-20 tokens. They trade on **exchange halos** — limit orderbook exchanges in the Sky ecosystem.

### Why Orderbooks Work (No Custom AMM Needed)

PT is economically identical to a zero-coupon bond. Zero-coupon bonds (Treasury bills, STRIPS) are among the most actively traded instruments in traditional finance, all on orderbook markets. The reasons DeFi protocols like Pendle use custom AMMs — poor on-chain orderbook infrastructure, gas costs, MEV vulnerability — do not apply when functional limit orderbook exchanges exist.

Orderbooks provide:
- **Natural multi-maturity support**: All maturities trade on the same exchange; no need to deploy a new AMM pool per maturity
- **Professional market making**: Market makers can quote tight spreads using standard fixed-income pricing
- **Better capital efficiency**: No locked LP capital in specialized curves
- **Standard price discovery**: Bid/ask spreads directly reveal the market-implied fixed rate

### Exchange Halo Responsibilities

Exchange halos that list PT/YT markets are expected to:
1. Create splitting buckets for the maturities they want to support
2. List PT and YT trading pairs (typically PT/underlying and YT/underlying)
3. Provide standard orderbook infrastructure (matching engine, settlement)

### Implied Rate Discovery

The market-clearing price of PT on the orderbook directly reveals the fixed rate:

```
Implied Fixed Rate = (1 / PT_Price)^(1 / years_to_maturity) - 1
```

No special oracle or AMM curve is needed. The orderbook price *is* the rate.

---

## Invariants

### Fundamental

1. **Split conservation**: For every split, `PT_minted == YT_minted` (equal quantities always)
2. **Merge requires both**: Merging requires equal amounts of PT and YT from the same bucket
3. **PT par redemption**: At maturity, 1 PT redeems for 1 unit of the underlying accounting asset (in yield-bearing token terms at the maturity exchange rate)
4. **YT yield capture**: All yield accrued on deposited collateral between split and maturity is attributable to YT holders

### Bucket Integrity

5. **One bucket per (token, maturity)**: No duplicate buckets
6. **Deterministic addresses**: PT and YT addresses are derivable from (token, maturity) via CREATE2
7. **Maturity is immutable**: A bucket's maturity timestamp cannot change after creation
8. **PY Index ratchet**: PY Index is monotonically non-decreasing

### Safety

9. **No operations on matured buckets except PT redemption and final YT yield claim**
10. **Exchange rate dependency**: If a token's exchange rate function reverts, split/merge/claim operations for that token's buckets revert — no silent failures
11. **PT/YT supply always balanced**: `ptToken.totalSupply() == ytToken.totalSupply()` at all times

---

## User Stories

### Story 1: Lock in a Fixed Rate on sUSDS

Alice holds 10,000 sUSDS and wants to lock in a fixed rate for 6 months.

1. Alice splits 10,000 sUSDS in the (sUSDS, 2026-06-30) bucket
   - Receives 10,500 PT-sUSDS-JUN26 and 10,500 YT-sUSDS-JUN26 (at 1.05 exchange rate)
2. Alice sells 10,500 YT-sUSDS-JUN26 on an exchange halo for ~450 sUSDS (market-priced)
3. Alice holds 10,500 PT-sUSDS-JUN26
4. At maturity, Alice redeems 10,500 PT for 10,500 USDS worth of sUSDS

**Result:** Alice locked in a fixed return. Her effective rate was determined by the price she received for the YT.

### Story 2: Speculate on Rising SSR

Bob thinks SSR will increase. He wants leveraged exposure to the variable rate.

1. Bob buys 50,000 YT-sUSDS-JUN26 on an exchange halo at a discount
2. Over the next 6 months, SSR is higher than the market expected
3. Bob claims yield periodically — the yield exceeds what he paid for the YT

**Result:** Bob profited from his correct rate prediction. His return was leveraged because he paid a fraction of the notional for the YT.

### Story 3: Market Maker Splits and Sells Both Sides

An exchange halo operator creates the (srUSDS, 2026-09-30) bucket and provides liquidity.

1. Operator splits 1,000,000 srUSDS → 1,012,000 PT + 1,012,000 YT
2. Operator lists both PT and YT on the orderbook with bid/ask spreads
3. Fixed-rate seekers buy PT; variable-rate speculators buy YT
4. Operator earns the spread

**Result:** The exchange halo facilitates fixed-rate and variable-rate markets for srUSDS.

### Story 4: Merge Before Maturity

Carol split sUSDS but changes her mind.

1. Carol holds 5,000 PT-sUSDS-JUN26 and 5,000 YT-sUSDS-JUN26
2. Carol calls merge with amount = 5,000
3. Yield Splitter claims any accrued yield for Carol's YT, burns both PT and YT, returns sUSDS

**Result:** Carol exits cleanly with her original sUSDS plus any yield earned while split.

### Story 5: LCTS Token (TEJRC) Fixed Rate

A Prime's external junior risk capital holders want fixed-rate exposure.

1. Exchange halo creates bucket (TEJRC-SparkPrime, 2026-12-31)
2. TEJRC holder splits 100,000 TEJRC → PT + YT
3. PT-TEJRC trades at a discount reflecting the market's view of Spark Prime's risk premium
4. YT-TEJRC trades based on expected TEJRC yield over the remaining term

**Result:** Fixed-rate and variable-rate markets emerge for Prime-specific risk capital.

---

## Edge Cases

### Token Exchange Rate Stops Updating

**Scenario:** A token's exchange rate function returns the same value for multiple epochs.

- PY Index remains unchanged; no yield accrues to YT holders
- PT remains redeemable at maturity at whatever the exchange rate is at that time
- No special handling needed — the system naturally pauses yield distribution

### Negative Yield (Exchange Rate Decreases)

**Scenario:** srUSDS takes a loss haircut, reducing its exchange rate.

- PY Index ratchet holds — it does not decrease
- YT yield accrual pauses until the exchange rate recovers above the PY Index
- If unrecovered at maturity, PT holders redeem below par (they absorb the credit loss)

### Bucket Created But Never Used

**Scenario:** Someone creates a bucket but no one ever splits into it.

- PT and YT contracts are deployed but have zero supply
- No gas cost beyond the initial bucket creation
- No cleanup needed — empty buckets are inert

### Maturity Passes With Unclaimed Yield

**Scenario:** YT holder has not claimed yield when maturity arrives.

- YT holder can still call claimYield after maturity to receive all accrued yield
- No yield accrues after maturity — but previously accrued yield is not lost
- YT tokens have no redemption value beyond the unclaimed yield

### Very Long Maturity

**Scenario:** Someone creates a bucket with a 10-year maturity.

- Functionally identical to a shorter maturity, just with more time for yield to accrue
- PT trades at a steeper discount (higher implied rate for longer duration)
- No protocol-level restriction on maturity length

---

## Gas Complexity

| Operation | Complexity | Notes |
|-----------|------------|-------|
| createBucket | O(1) | Deploys two ERC-20 clones (CREATE2) |
| split | O(1) | Transfer + mint PT + mint YT + update index |
| merge | O(1) | Claim yield + burn PT + burn YT + transfer |
| redeemPT | O(1) | Burn PT + transfer |
| claimYield | O(1) | Compute pending + transfer |
| registerToken | O(1) | Store token metadata |

---

## The Two Layers (Scope Clarification)

Fixed-rate systems involve two distinct layers:

| Layer | What It Does | This Spec |
|-------|-------------|-----------|
| **Splitting (Yield Splitter)** | Split yield-bearing tokens into PT + YT, track yield, handle redemption | **In scope** |
| **Trading (Exchange Halos)** | Price discovery, orderbook matching, market making, maturity date selection | **Out of scope** — handled by exchange halos |

This spec covers only the splitting layer. The trading layer is the responsibility of exchange halo operators, who use standard limit orderbook infrastructure to facilitate PT/YT markets. No custom AMM, no specialized curve, no protocol-level liquidity management.

The separation is deliberate: the Yield Splitter is a neutral infrastructure contract; exchange halos compete on execution quality, spread, and maturity selection.

---

## Roadmap Status

Not yet assigned to a roadmap phase. Depends on LCTS exchange rate interfaces (Phase 4+) and Exchange Halos (also unscheduled). See the [Unscheduled Specifications](../roadmap/roadmap-overview.md#unscheduled-specifications) section of the roadmap overview.

---

## Related Documents

| Document | Relevance |
|----------|-----------|
| `smart-contracts/lcts.md` | LCTS exchange rate interface required for LCTS token compatibility |
| `smart-contracts/architecture-overview.md` | System architecture context |
| `trading/sentinel-network.md` | Exchange halo operations |
| `synomics/macrosynomics/beacon-framework.md` | Beacon taxonomy for any automated interactions |
