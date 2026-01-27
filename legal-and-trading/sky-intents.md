# Sky Intents

**Status:** Draft
**Pillar:** 8
**Last Updated:** 2026-01-27

---

> **Draft note:** This document is an early draft and needs feedback on: (1) settlement validation rules (rounding, partial fills), and (2) cross-chain intent design. Resolved: intent format semantics (exact-in vs exact-out), Prime delegated trading guardrails, and fee design (output-based abstraction for trading, rate-enshrined for future lending).

## Executive Summary

Sky Intents is an intent-based trading protocol that enables:
- **Trading without arbitrary transfer ability** — Primes can trade via Sentinels without exposing PAUs to unrestricted withdrawals
- **Fair matching** — Centralized orderbook matching by trusted operators, eliminating adversarial MEV extraction
- **Permissioned trading** — Identity Network integration enables tokens restricted to verified counterparties

The system consists of two components:
1. **Intent Protocol** — On-chain settlement layer for signed trading intents
2. **Exchange Halo** — Special Halo type that operates orderbook infrastructure

Together, these create a hybrid exchange: CEX-like orderbooks for speed and fairness, on-chain settlement for transparency and self-custody.

Sky Intents also supports **direct peer-to-peer settlement**: any actor can settle compatible signed intents on-chain without going through a centralized matching engine. Centralized orderbooks and batch settlement are an optional (but expected-to-be-common) mode for efficiency and fairness.

---

## Why Sky Intents Exists

### Problem 1: Trading Without Trust

Primes need to trade rapidly — rebalancing portfolios, market making, arbitrage. But giving Sentinels arbitrary transfer ability is dangerous:
- A compromised stl-base could drain the PAU
- Rate limits help but are blunt instruments
- Need fine-grained control: "can trade, but can't withdraw"

**Solution:** Intent-based trading. Sentinels create intents that can ONLY be settled as trades, not arbitrary transfers.

### Problem 2: Adversarial MEV Extraction

On-chain orderbooks suffer from MEV extraction by anonymous actors:
- Searchers front-run large orders
- Validators reorder transactions for profit
- Users get worse prices than they should

**Solution:** Off-chain orderbook with centralized matching by trusted operators. Orders matched fairly (time priority), then settled on-chain in batches. MEV opportunity shifted from adversarial extractors to governed, accountable exchange operators.

### Problem 3: Counterparty Restrictions

Many Halo Units have issuers or participants who prefer or require verified counterparties:
- Private credit products → institutional investors only
- Certain asset classes → accredited/qualified investors preferred
- Some products → jurisdiction-specific participant requirements

**Solution:** Per-market Identity Network requirements. Exchange Halo specifies which Identity Networks are accepted; settlement contract verifies attestations.

---

## Intent Protocol

### What is an Intent?

An intent is a signed message authorizing a specific trade. Sky Intents supports two intent types to avoid ambiguous price-constraint semantics:

1. **Exact-in (sell intent):** “Sell up to X of token A, but only at or above price P.”
2. **Exact-out (buy intent):** “Buy up to Y of token B, but only at or below price P.”

These are the minimal shapes needed to express limit and market-style orders with clear constraints, while supporting partial fills via on-chain fill tracking (rather than additional, confusing per-intent caps).

#### Intent Type A: Exact-in (sell intent)

Fields:
- Maker (signer)
- Token In (asset being sold)
- Token Out (asset being bought)
- `amountInMax` (maximum total input authorized across all fills)
- `minOutPerIn` (price floor, expressed as output per 1 unit of input; fixed-point)
- Expiry
- Nonce
- `allowPartialFill`
- Signature

Semantics: “I authorize selling up to `amountInMax` of Token In for Token Out at a price no worse than `minOutPerIn`, before time T.”

#### Intent Type B: Exact-out (buy intent)

Fields:
- Maker (signer)
- Token In (asset being paid)
- Token Out (asset being bought)
- `amountOutMax` (maximum total output authorized across all fills)
- `maxInPerOut` (price ceiling, expressed as input per 1 unit of output; fixed-point)
- Expiry
- Nonce
- `allowPartialFill`
- Signature

Semantics: “I authorize buying up to `amountOutMax` of Token Out, paying in Token In at a price no worse than `maxInPerOut`, before time T.”

### Intent Properties

| Property | Description |
|----------|-------------|
| **Non-transferable** | Intent authorizes a trade, not an arbitrary transfer |
| **Revocable** | Maker can cancel before settlement |
| **Expiring** | Automatically invalid after expiry |
| **Partial-fillable** | Can be filled in portions |
| **Composable** | Multiple intents can settle atomically |

### Intent Creation

Intents can be created by:

1. **Users directly** — Sign intent with personal wallet
2. **Sentinels on behalf of Primes** — stl-base signs within authorized bounds

For Sentinels:
```
Intent bounds (governance-set):
- Max slippage: e.g., 1% from oracle price
- Max amount per intent: e.g., $1M
- Rate limit: e.g., $10M per hour
- Allowed pairs: e.g., USDS ↔ sUSDS only
```

Sentinels CANNOT create intents outside these bounds. This is the "trading without arbitrary transfer" guarantee.

### Intent Settlement

Settlement is atomic and on-chain:

```
Settlement process:
  1. Verify all signatures are valid
  2. Check all intents are not expired or cancelled
  3. Verify fill amounts are within intent bounds
  4. Execute atomic swap of all tokens
     - Each token transfer may check Identity Network membership (token-level)
     - If any transfer fails, entire batch reverts
  5. Mark intents as filled (partially or fully)
```

Either ALL trades in a batch succeed, or NONE do. No partial settlement of a batch.

**Price constraint enforcement (per fill):**
- **Exact-in:** require `amountOutFill >= amountInFill * minOutPerIn` (with an explicit rounding rule).
- **Exact-out:** require `amountInFill <= amountOutFill * maxInPerOut` (with an explicit rounding rule).

### Intent Cancellation

Makers can cancel intents before settlement:

```
Cancel intent:
  - Maker calls cancel with nonce
  - Settlement contract marks nonce as used
  - Intent with that nonce can no longer settle

Cancel batch:
  - Maker provides list of nonces
  - All nonces marked as used in single transaction
```

Cancelled intents cannot be settled. The matching engine removes cancelled orders from the book.

---

## Exchange Halo

### What is an Exchange Halo?

An Exchange Halo is a special Halo type that operates trading infrastructure:
- Runs an orderbook (off-chain, centralized)
- Matches orders fairly
- Creates settlement batches
- Specifies Identity Network requirements per market

Exchange Halos are **infrastructure providers**, not capital deployers. Like Identity Networks, they have restricted activities.

### Exchange Halo vs Regular Halo

| Aspect | Regular Halo | Exchange Halo |
|--------|--------------|---------------|
| **Primary activity** | Deploy capital, generate yield | Operate trading infrastructure |
| **Revenue source** | Investment returns | Trading fees |
| **Capital deployment** | Yes | No (prohibited) |
| **Asset custody** | Holds assets via PAU | No custody (intents settle peer-to-peer) |
| **Operated by** | lpha-lcts | lpha-exchange |

### Market Configuration

Each Exchange Halo defines markets:

```
Market configuration:
  - Base Token: the asset being traded (e.g., JAAA-Halo-Unit)
  - Quote Token: the pricing currency (e.g., USDS)
  - Maker Fee: fee for limit order providers (basis points)
  - Taker Fee: fee for market order takers (basis points)
  - Min Order Size: minimum order size
  - Tick Size: price increment
  - Active: whether market is trading

Note: Identity restrictions come from the tokens themselves, not the market config.
```

### Fee Model

Exchange Halos generate revenue from trading fees:

| Fee Type | Description |
|----------|-------------|
| **Maker fee** | Fee paid by limit order providers |
| **Taker fee** | Fee paid by market order takers |
| **Settlement fee** | Small fee for on-chain settlement gas |

Typical structure: maker rebate (negative fee) to encourage liquidity, taker fee to generate revenue.

### Fee Design Principle: Output-Based Abstraction

**Key insight:** For trading intents, fees can be **abstracted into outputs** rather than enshrined as a separate field in the intent specification.

#### How It Works

The user signs an intent specifying input and outputs. Fees are encoded as additional output recipients:

```
User signs:
  Input:  1000 USDS
  Outputs:
    - 995 sUSDS to user (minimum)
    - Fee output to Exchange Halo (implicit in execution)
```

At settlement, the actual distribution might be:
```
  Input:  1000 USDS
  Execution:
    - 997 sUSDS to user (2 sUSDS price improvement)
    - 1 sUSDS worth to Exchange Halo (taker fee)
    - 2 sUSDS worth to filler (profit from spread)
```

#### Why This Design

| Approach | Pros | Cons |
|----------|------|------|
| **Explicit fee field** | Clear, auditable | Inflexible; requires intent format changes for new fee types |
| **Output-based (chosen)** | Flexible; supports multiple recipients | Fee less visible to user |

The output-based model allows:
- Multiple fee recipients (protocol, integrator, referrer)
- Fee splits without changing intent format
- Uniform treatment: fee is just "where tokens go"

#### Comparison to Other Protocols

| Protocol | Fee in Intent? | Mechanism |
|----------|----------------|-----------|
| **CoW Protocol** | Yes (`feeAmount` field) | User signs gas fee; protocol fee extracted separately |
| **UniswapX** | No | Fee implicit in Dutch auction decay |
| **ERC-7683** | No | Deferred to `orderData` implementation |
| **Sky Intents** | No | Fee implicit in output distribution |

#### Implication for Settlement Contract

The settlement contract should support multiple output recipients per intent, where one or more outputs can be designated as fee outputs:

```solidity
struct Output {
    address token;
    uint256 amount;
    address recipient;  // Can be user, feeCollector, or other
}
```

Fee attribution (who gets what share) is determined by the Exchange Halo's fee schedule and applied at settlement time — the user only signs the minimum they accept.

### Multiple Exchange Halos

Multiple Exchange Halos can operate simultaneously:
- **Competition** — Users choose based on fees, liquidity, markets offered
- **Specialization** — Different Exchange Halos for different market types
- **Redundancy** — If one Exchange Halo fails, others continue operating

---

## Exchange Operator (lpha-exchange)

### Overview

**lpha-exchange** operates the off-chain orderbook and matching engine for an Exchange Halo. Exchange operators are LPHA (Low Power, High Authority) beacons — they operate on behalf of Exchange Halos with high authority but execute deterministically based on governance rules. See `beacon-framework.md` for the full beacon taxonomy.

**Level:** Per Exchange Halo
**Operator:** Exchange Halo GovOps

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           lpha-exchange                                    │
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐  │
│  │   Order Gateway  │  │  Matching Engine │  │  Settlement Builder  │  │
│  │                  │  │                  │  │                      │  │
│  │  - Receive orders│  │  - Price-time    │  │  - Create batches    │  │
│  │  - Validate      │  │    priority      │  │  - Submit on-chain   │  │
│  │  - Rate limit    │  │  - Fair matching │  │  - Handle failures   │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────────┘  │
│           │                    │                       │                │
│           └────────────────────┴───────────────────────┘                │
│                                │                                         │
│                         ┌──────┴──────┐                                 │
│                         │  Orderbook  │                                 │
│                         │  Database   │                                 │
│                         └─────────────┘                                 │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Order Lifecycle

```
1. SUBMIT
   User sends order to lpha-exchange (off-chain API)
   - Order type: LIMIT, MARKET, IOC, FOK
   - Includes signed intent (or intent is created on match)

2. VALIDATE
   lpha-exchange validates:
   - Signature validity
   - Balance sufficiency (query on-chain)
   - Identity Network attestation (for restricted markets)
   - Rate limits (if Sentinel-created)

3. PLACE
   Order added to orderbook
   - Limit orders: placed at specified price
   - Market orders: immediately match against book

4. MATCH
   Matching engine runs continuously:
   - Price-time priority (best price, then earliest)
   - No reordering, no front-running
   - Matched orders create trade records

5. SETTLE
   Periodically (or on threshold):
   - lpha-exchange creates settlement batch
   - Submits to on-chain settlement contract
   - Atomic execution of all matched trades

6. CANCEL
   User can cancel at any time before settlement:
   - Order removed from book
   - Intent cancelled on-chain (if already created)
```

### Matching Engine

The matching engine operates with strict fairness guarantees:

| Property | Implementation |
|----------|----------------|
| **Price-time priority** | Best price wins; ties broken by submission time |
| **No front-running** | lpha-exchange cannot see orders before placement |
| **Deterministic** | Same inputs produce same matches |
| **Auditable** | Match records stored for verification |

### Settlement Batching

lpha-exchange batches trades for efficiency:

```
Settlement triggers:
- Time-based: Every N seconds (e.g., 1 second)
- Size-based: When batch reaches N trades
- Value-based: When batch value exceeds $X
```

Batching reduces gas costs and enables atomic cross-market settlement.

### Failure Handling

| Failure | Handling |
|---------|----------|
| **Settlement revert** | Retry with subset; isolate failing trades |
| **Balance insufficient** | Cancel order, notify user |
| **Attestation expired** | Cancel order, notify user |
| **lpha-exchange downtime** | Orders remain in book; resume on recovery |

---

## Prime Integration

### Overview

For Primes, Sky Intents must support **delegated trading** without granting arbitrary withdrawal ability, and with hard limits that cap worst-case losses and trading volume.

Sky Intents treats Prime trading as a three-part integration:
1. **Prime Intent Vault** (on-chain) — a restricted trading sub-account with bounded funds and policy.
2. **Intent signing** (off-chain) — stl-base produces signatures within delegated limits.
3. **Settlement** (on-chain) — the settlement contract executes transfers atomically based on validated intents.

### Prime Intent Vault (restricted trading sub-account)

Primes do **not** expose their full PAU/treasury balances directly to the intent settlement contract. Instead, each Prime maintains a dedicated **Prime Intent Vault**:

- Holds **bounded “working capital”** for trading.
- Is funded/drained through the Prime’s normal PAU/Controller operations (so movement into/out of the vault is governed by the same PAU rate-limit and SORL mechanics used elsewhere).
- Grants the settlement contract permission to move assets **only from the vault**, so the maximum loss from compromised delegated trading is capped by the vault’s balance (not the Prime’s entire PAU).

This isolates trading risk while keeping capital motion consistent with the Allocation System guardrails.

### Delegated intent policy (limits that cap damage)

The Prime Intent Vault enforces (or is configured with) an explicit policy that defines what delegated trading is allowed to do.

Example policy surface (per Prime, per token/pair, or per venue):
- **Allowed pairs / assets** (explicit allowlist)
- **Max slippage** relative to a reference price
- **Max single-intent notional**
- **Max notional per time window** (e.g., hourly/daily)
- **Expiry bounds** (min/max TTL)
- **Optional:** max outstanding open intents, max net position change per window

These limits are intended to be governance-configured and monitored, in the same spirit as PAU rate limits: **instant decreases, constrained increases** (via a timelock/SORL-like process).

#### Oracle requirement (Prime delegated trading)

For Prime delegated trading, slippage limits must reference an **approved on-chain oracle**:
- Any asset without an approved oracle is **not eligible** for delegated trading via the Prime Intent Vault (it may still be tradable by users at their own risk).
- Slippage checks are enforced **at fill time**, using the oracle price observed during settlement (not at intent signing time).

#### Stateful limit consumption

Signature validation (including EIP-1271) is necessary but not sufficient for enforcing time-window limits (hourly/daily), because those limits require **stateful consumption**.

The intended model is:
- Settlement verifies that the maker is authorized (EOA signature or EIP-1271 for contract makers).
- Settlement then calls a **stateful vault hook** to enforce and consume limits before any transfers occur.

Example (conceptual) interface:
`vault.validateAndConsumeFill(intent, fill)` → reverts if policy is violated; otherwise updates vault accounting for per-window caps and proceeds.

### stl-base Trading

stl-base can create trading intents within governance-set bounds:

```
Trading Bounds (per Prime):
{
    "allowed_pairs": [
        {"base": "USDS", "quote": "sUSDS"},
        {"base": "JAAA-Halo", "quote": "USDS"}
    ],
    "max_slippage_bps": 100,        // 1% max slippage
    "max_intent_amount": 1000000,    // $1M per intent
    "hourly_rate_limit": 10000000,   // $10M per hour
    "daily_rate_limit": 50000000     // $50M per day
}
```

stl-base creates intents within these bounds; the Prime Intent Vault and settlement logic enforce them.

### How intents are authorized (EOA vs contract signing)

For user wallets, the maker is typically an EOA and signature verification is standard EIP-712.

For Prime trading via a Prime Intent Vault, the maker can be a **contract** (the vault) that accepts delegated signatures:
- stl-base signs the intent payload using an authorized key.
- The settlement contract validates the maker signature via **EIP-1271** (contract signature validation) against the Prime Intent Vault.
- The Prime Intent Vault can reject signatures that exceed delegated limits, and separately enforce **stateful** per-window limits at settlement time via a vault hook.

This makes delegated limits enforceable on-chain without giving stl-base arbitrary transfer rights.

### Trading Flow for Primes

```
1. stl-stream (optimizer) determines desired trade
   "Sell $500K USDS for sUSDS at current rate"

2. stl-stream sends intent to stl-base
   - Validates against bounds
   - If compliant, stl-base signs intent

3. stl-base submits order to lpha-exchange
   - Order placed in orderbook
   - Matches against other orders

4. lpha-exchange creates settlement batch
   - Includes Prime's matched trade
   - Submits to settlement contract

5. Settlement contract executes
   - Transfers USDS from Prime Intent Vault
   - Transfers sUSDS to Prime Intent Vault
   - Atomic, no intermediate states
```

### Why This is Safe

The delegated trading model provides safety guarantees:

| Concern | Mitigation |
|---------|------------|
| **Compromised stl-base** | Can only produce signatures accepted by the Prime Intent Vault policy; cannot withdraw funds directly |
| **Bad trades** | On-chain price constraints (minOutPerIn / maxInPerOut) + slippage bounds restrict execution |
| **Excessive volume** | Notional-per-window limits cap trading throughput; vault funding is also rate-limited via PAU |
| **Wrong assets** | Allowed pairs/asset allowlists restrict what can be traded |
| **Blast radius** | Only the Prime Intent Vault balance is exposed to settlement; full Prime PAU is not |

Even a fully compromised stl-base can only make bounded trades, not arbitrary withdrawals.

---

## User Trading (Non-Prime)

### Direct User Flow

Users who aren't Primes trade directly with their own wallets:

```
1. User signs intent with their wallet
   "Sell 1000 USDS for at least 990 sUSDS, expires in 1 hour"

2. User submits order to lpha-exchange
   - Order placed in orderbook
   - Intent stored (already signed)

3. Matching engine matches against counterparty
   - Price-time priority
   - Fair matching

4. lpha-exchange creates settlement batch
   - User's matched trade included
   - Submitted to settlement contract

5. Settlement contract executes
   - Transfers tokens between user and counterparty
   - Atomic execution
```

### When Users Sign

Users sign intents **before** order submission:
- User specifies price, amount, and expiry
- Signs intent authorizing the trade
- Submits signed intent + order to lpha-exchange
- If order matches, intent already authorized — settlement can proceed

### User vs Prime Differences

| Aspect | User | Prime |
|--------|------|-------|
| **Who signs** | User directly | stl-base (within bounds) |
| **Bounds enforcement** | None (user's choice) | Governance-set limits |
| **Rate limits** | None (user's capital) | SORL-controlled |
| **Source of funds** | User's wallet | PAU |

### Wallet Requirements

To trade on Sky Intents, users need:
- Wallet with tokens to sell
- Allowance granted to settlement contract
- Signed intent (created during order submission)
- For restricted tokens: membership in an accepted Identity Network

---

## Identity Network Integration

### Token-Level Restrictions

Identity restrictions are enforced **at the token level**, not the exchange level. The token issuer configures which Identity Networks are accepted, and the token contract checks membership on every transfer.

The exchange doesn't need separate identity checks — it just attempts the trade:

```
Settlement Flow:
  1. lpha-exchange submits settlement batch
  2. Settlement contract executes token transfers
  3. Each token's transfer function checks: is recipient in an accepted Identity Network?
     - If yes → transfer succeeds
     - If no → transfer reverts → entire settlement fails
```

This means:
- **Unrestricted tokens** (USDS, SKY) — Anyone can trade, no identity check
- **Restricted tokens** (some Halo Units, some Prime tokens) — Only Identity Network members can receive

### Order Visibility (Optional)

Exchange Halos MAY restrict order visibility for better UX:
- **Public book:** All orders visible to all participants
- **Filtered book:** Orders involving restricted tokens only visible to eligible counterparties

This is a UX optimization — it prevents users from seeing orders they can't fill. The actual restriction enforcement happens at the token level.

### Attestation Events

lpha-exchange can subscribe to Identity Network events:

```
Events from lpha-identity:
  - MemberAdded(address)
  - MemberRemoved(address)
```

When an address is removed, lpha-exchange can proactively:
1. Cancel open orders from that address for restricted tokens
2. Prevent new order submission for restricted tokens

This is optional — even without proactive cancellation, the settlement would simply fail when the token transfer reverts.

---

## Tradeable Assets

### All Sky Assets

Sky Intents supports trading all Sky ecosystem assets:

| Category | Assets |
|----------|--------|
| **Core tokens** | USDS, sUSDS, SKY |
| **Risk capital** | srUSDS, TEJRC, TISRC |
| **Halo units** | All Halo Unit tokens |
| **Prime tokens** | SPK, GROVE, etc. |
| **Legacy** | DAI, MKR (if listed) |

### Token Types

Identity requirements are set by token issuers, not exchanges:

| Token Type | Examples | Identity Required |
|------------|----------|-------------------|
| **Unrestricted** | USDS, sUSDS, SKY | No — anyone can hold |
| **Restricted Halo Units** | JAAA-Halo, Private-Credit-Halo | Yes — issuer configured |
| **Restricted Prime Tokens** | Institutional Prime tokens | Yes — Prime configured |
| **Risk capital** | srUSDS, TEJRC, TISRC | Depends on token config |

### Cross-Exchange Arbitrage

Multiple Exchange Halos may list the same pair:
- Price differences create arbitrage opportunities
- Arbitrageurs equalize prices across venues
- Liquidity fragments but price discovery improves

---

## Security Model

### MEV Trade-offs

Sky Intents shifts MEV extraction from on-chain actors (searchers, validators) to the exchange operator. This is a deliberate trade-off:

| On-Chain DEX | Sky Intents |
|--------------|-------------|
| MEV extracted by searchers/validators | MEV opportunity exists for exchange operator |
| Permissionless extraction | Trusted operator (reputation at stake) |
| Unpredictable, adversarial | Predictable, governed |

**What's prevented:**
- Random searchers cannot front-run (no mempool visibility)
- Validators cannot reorder (matching happens off-chain)
- Sandwich attacks impossible (batch settlement, no insertion)

**What's shifted:**
- Exchange operator COULD theoretically front-run orders
- Exchange operator COULD theoretically delay settlement for advantage
- Exchange operator COULD theoretically preferentially match orders

The system relies on exchange operator incentives (reputation, fees, governance oversight) rather than cryptographic guarantees.

### lpha-exchange Trust Model

Users trust lpha-exchange to:
1. **Match fairly** — Price-time priority, no preferential treatment
2. **Settle promptly** — Submit batches without undue delay
3. **Not censor** — Accept all valid orders
4. **Not front-run** — Not exploit order flow information

Why this works:
- **Reputation** — Exchange Halos compete; bad actors lose users
- **Multiple Exchange Halos** — Users can switch to alternatives
- **Auditable logs** — Match records stored for post-hoc verification
- **Governance oversight** — Exchange Halos subject to Sky governance
- **Slashing** — Penalties for provable misconduct

### Rate Limit Protection

Sky Intents rate limiting for Primes is intended to mirror the Allocation System’s guardrail philosophy:

1. **Funding rate limits (PAU-level):** capital moved into/out of the Prime Intent Vault is done via normal PAU/Controller flows and is subject to the Prime’s configured `RateLimits` and SORL-style constraints (instant decreases; constrained increases).

2. **Trading policy limits (intent-level):** the Prime Intent Vault’s delegated policy caps per-intent notional and notional per time window, and restricts allowed assets/pairs and slippage bounds. These limits bound how much damage a compromised delegated signer can cause before governance/operations can intervene.

### Failure Modes

| Failure | Impact | Recovery |
|---------|--------|----------|
| **lpha-exchange down** | No new matches; existing orders preserved | Resume on recovery |
| **Settlement contract paused** | No settlements; orders accumulate | Governance unpauses |
| **Identity Network down** | Can't verify new attestations | Use cached status; degrade gracefully |
| **Bad settlement batch** | Batch reverts | Retry with subset |

---

## Contract Architecture

### Core Contracts

```
Intent Settlement Contract:
  - Settle (permissionless): execute compatible signed intents atomically (direct P2P settlement is allowed)
  - SettleBatch (optional mode): execute a batch produced by an Exchange Halo matching engine (expected to be common for efficiency)
  - Cancel: allow makers to cancel their intents by nonce
  - Permissions:
      - Direct settlement is permissionless (any submitter can pay gas to settle valid intents)
      - Exchange Halo batch submission may be restricted to authorized Exchange Halos for fee attribution, market operations, and governance accountability

Exchange Halo Registry:
  - Register: add new Exchange Halos
  - Create Market: define trading pairs and fees
  - Update Market: modify market parameters

Intent Validator (library):
  - Validate intent signatures and bounds
  - Compute intent hashes for deduplication
```

### Integration Points

```
Intent Settlement Contract:
  → Token contracts (executes transfers, tokens enforce identity restrictions)
  → PAUs (source/destination for Prime trades)
  → Synome (trade logging)

lpha-exchange:
  → Intent Settlement Contract (submit settlement batches)
  → stl-base instances (receive Prime orders)
  → Identity Networks (optional eligibility pre-checks for UX)

P2P settler (any actor):
  → Intent Settlement Contract (submit direct settlements)
```

---

## Future: Lending Intents

Sky Intents is designed for trading, but the intent architecture should support **lending intents** in the future. This section documents how fee design differs between trading and lending.

### Why Lending Intents Are Different

| Aspect | Trading Intent | Lending Intent |
|--------|----------------|----------------|
| **Core economic term** | Price (exchange ratio) | Rate (time value of money) |
| **Time dimension** | Atomic (instant) | Continuous (over loan life) |
| **Fee extraction** | One-time at execution | Ongoing via interest spread |
| **State** | Stateless after settlement | Stateful (loan persists) |

### Trading: Fee Can Be Abstracted

Trading is atomic. Once the swap executes, the relationship ends. The fee is simply part of "where tokens go" at the moment of execution — it can be implicit in the output distribution.

### Lending: Spread Must Be Enshrined

Lending is continuous. The loan persists over time, and interest accrues. The "fee" is the **rate spread** between what the borrower pays and what the lender receives.

**Example:**
```
Lender intent:  "Lend USDC at 4.5% APR minimum"
Borrower intent: "Borrow USDC at 5.0% APR maximum"

Match at 4.75%:
  - Borrower pays 4.75% APR
  - Lender receives 4.5% APR
  - 0.25% spread = protocol/curator fee
```

**Why the rate can't be abstracted:**

1. **Interest accrues continuously** — Need the rate to calculate daily/block-by-block
2. **Loan state changes** — Early repayment, extension, liquidation all need rate math
3. **Rate IS the economic term** — Unlike trading where the amount is the term

If you tried to abstract lending like trading:
```
"Give 100 USDC now, receive 105 USDC in 90 days"
```

This breaks when:
- Loan repaid at day 45 → How much interest is owed?
- Loan extended to day 180 → At what rate?
- Partial repayment → How to split principal vs interest?

### Unified Intent Architecture

To support both trading and lending in the same system:

```solidity
struct SkyIntent {
    address maker;
    uint256 nonce;
    uint32 expiry;
    bytes32 intentType;      // "TRADE" | "BORROW" | "LEND"
    bytes intentData;        // Type-specific parameters
}

// Trading: fee abstracted into outputs
struct TradeIntentData {
    address tokenIn;
    uint256 amountIn;
    Output[] outputs;        // Includes user + implicit fee recipients
}

// Lending: rate enshrined as first-class field
struct LendIntentData {
    address loanToken;
    uint256 amount;
    uint256 minRateBps;      // Rate is first-class
    uint256 minTermSeconds;
    address[] collateralTokens;
    uint256 maxLtvBps;
}

struct BorrowIntentData {
    address loanToken;
    uint256 amount;
    uint256 maxRateBps;      // Rate is first-class
    uint256 termSeconds;
    address collateralToken;
    uint256 collateralAmount;
}
```

### Design Principle Summary

| Intent Type | Fee Representation | Why |
|-------------|-------------------|-----|
| **Trading** | Implicit in outputs | Atomic; fee is just "where tokens go" |
| **Lending** | Explicit rate field | Continuous; rate determines ongoing accrual |

This principle ensures the intent specification is **minimal yet complete** for each use case.

---

## Open Questions

1. **Settlement frequency** — How often should batches settle? 1 second? 10 seconds? Event-driven?

2. **Gas costs** — Who pays settlement gas? Exchange Halo? Pro-rata among traders?

3. **Partial fills** — How are partial fills handled for maker rebates?

4. **Cross-chain** — How do intents work for assets on different chains?

5. **Oracle integration** — Which oracle(s) are approved per asset, and how do we handle stale/missing oracle updates at settlement time?

6. **Emergency pause** — Can governance pause specific markets? All trading?

7. **Order types** — What order types beyond limit/market? Stop-loss? Trailing?

---

## Connection to Other Documents

| Document | Relationship |
|----------|--------------|
| `identity-network.md` | Identity Networks enable token-level transfer restrictions |
| `beacon-framework.md` | lpha-exchange is defined as an LPHA beacon |
| `risk-framework/README.md` | Risk framework governs Prime trading bounds |

---

## Scenarios (Illustrative)

These scenarios are intended to make the end-to-end delegated trading flow concrete. They are illustrative (not a complete spec) and should be refined with implementation feedback.

### Scenario 1: Prime enables delegated trading safely (setup)

1. **Prime deploys a Prime Intent Vault** (a restricted trading sub-account).
2. **Governance/GovOps configures the vault policy**:
   - allowed pairs/assets
   - approved on-chain oracle feeds per asset
   - slippage bounds (enforced at fill time)
   - per-intent notional cap
   - per-window notional caps (hourly/daily)
   - expiry bounds
3. **Prime PAU is configured to fund the vault** using normal Controller operations (subject to `RateLimits` + SORL-style constraints on increases).
4. **Prime authorizes delegated signing**:
   - vault recognizes `stl-base` (or a GovOps-controlled key) as an authorized delegated signer for intents
   - settlement verifies maker authorization via EIP-1271 against the vault
5. **Prime restricts settlement permissions**:
   - settlement contract is allowed to move assets *from the vault only* (not from the full Prime PAU/ALMProxy balance).

Result: delegated trading is “live”, but only within a bounded trading balance and bounded policy.

### Scenario 2: Normal rebalance trade (USDS ↔ sUSDS)

1. `stl-stream` proposes: “sell 500k USDS for sUSDS.”
2. `stl-base` constructs an **exact-in** intent from the Prime Intent Vault:
   - `amountInMax = 500k USDS`
   - `minOutPerIn` computed from the oracle price with the configured slippage haircut
   - expiry within policy bounds
3. `lpha-exchange` matches the order off-chain and submits a settlement batch.
4. Settlement:
   - validates the vault’s EIP-1271 signature
   - calls the vault’s **stateful** validation hook (enforces allowed pair, oracle availability, fill-time slippage, and consumes per-window notional)
   - executes token transfers atomically

### Scenario 3: Normal market-making / repeated small fills

1. Vault is funded with a limited working balance (e.g., 2m USDS) via PAU-controlled funding flows.
2. `stl-base` places many small intents over time (e.g., 50k notional each).
3. Per-window caps allow continuous trading up to the configured rate, but cannot exceed it.
4. If the vault balance is exhausted, further fills fail until the vault is re-funded (again via PAU-controlled funding flows).

### Scenario 4: Malfunction — tries to trade too much (blocked by caps)

1. `stl-base` attempts to submit an intent for 25m notional in a single trade.
2. Vault policy rejects it because it exceeds `max_intent_amount`.
3. Even if it splits into multiple intents:
   - the first few fills may succeed up to the per-window cap
   - subsequent fills revert once the per-window cap is consumed

Outcome: trading throughput is bounded; the system fails closed once limits are hit.

### Scenario 5: Attack — tries to execute at a catastrophic price (blocked at fill time)

1. `stl-base` submits an intent with a permissive price bound (or a stale intent is matched late).
2. At settlement time the vault enforces fill-time slippage using the oracle price:
   - if the matched fill is outside `max_slippage_bps`, the vault hook reverts
3. The batch is retried without the failing fill (or the failing order is cancelled).

Outcome: catastrophic mispricing is blocked by on-chain oracle-referenced checks at settlement time.

### Scenario 6: Attack — tries to trade an asset without an approved oracle (blocked)

1. `stl-base` submits an intent involving an asset that has no approved oracle feed in the vault policy.
2. Vault validation rejects the fill (or rejects the intent up-front).

Outcome: delegated trading is limited to oracle-supported assets only.

### Scenario 7: Emergency response — revoke trading quickly

If abnormal behavior is detected:
1. **Instant limit decrease:** governance/GovOps reduces vault caps immediately (policy change designed to allow instant decreases).
2. **Revoke delegated signer:** remove the `stl-base` key from the vault’s authorized signer set (future intents fail EIP-1271).
3. **Stop funding:** reduce PAU funding rate limits to zero (or near-zero) to prevent adding more working capital.
4. **Drain working capital:** move assets out of the vault back into Prime custody via normal PAU/Controller operations (subject to configured outflow limits).

Outcome: the blast radius is limited to the vault balance, and the system can be shut down without giving `stl-base` any arbitrary transfer path.

---

*This document defines Sky Intents. For identity verification, see identity-network.md.*
