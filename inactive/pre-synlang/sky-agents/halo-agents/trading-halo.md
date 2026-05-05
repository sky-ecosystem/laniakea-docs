# Trading Halo — Business Overview

**Status:** Draft
**Last Updated:** 2026-03-01

---

## Executive Summary

A **Trading Halo** is a Halo Class type that operates an AMM (Automated Market Maker) smart contract, using predeposited USDS from its PAU to market make assets that are already onboarded onto the Configurator. Unlike Portfolio Halos (pooled yield products) and Term Halos (bespoke capital deployment), a Trading Halo provides **liquidity services** — enabling instant trades against a programmatic counterparty.

The core use case is **instant settlement for RWAs**. When a user holds t-bills or other RWA tokens and wants USDS now, the Trading Halo's AMM buys the RWA instantly at a spread, then redeems the underlying with the issuer over the normal settlement cycle (days). The spread compensates for the time value of capital and settlement risk. The same infrastructure supports **active market making** of ecosystem assets like JAAA — providing continuous two-sided liquidity and earning spreads.

**Key value proposition**: Any RWA token already onboarded onto the Configurator can immediately gain instant liquidity through a Trading Halo, without requiring the underlying issuer to provide instant redemptions. Primes benefit because their capital earns spread revenue while providing a service that makes the entire ecosystem more liquid.

---

## Why Trading Halos Exist

### The Instant Settlement Problem

RWA tokens have a structural liquidity mismatch:

- **Users want instant liquidity** — sell t-bills and receive USDS immediately
- **Issuers settle in days** — t-bill redemptions take T+1 to T+3; private credit can take weeks
- **DeFi expects atomic swaps** — users coming from DeFi expect sub-second finality

Without a Trading Halo, users who want to exit an RWA position must either:
1. Queue a redemption with the issuer and wait days
2. Find a willing counterparty on Sky Intents or an external exchange (liquidity may be thin)
3. Sell at a steep discount to a sophisticated buyer who can warehouse the position

A Trading Halo solves this by sitting between users and issuer settlement — absorbing the time delay and charging a spread for the service.

### The Market Making Problem

Many ecosystem assets (Halo Unit tokens, risk capital tokens, Prime tokens) need continuous liquidity to function well:

- **Price discovery** — assets need active trading to establish fair prices
- **Rebalancing** — Primes and users need to enter/exit positions smoothly
- **Composability** — DeFi protocols that integrate these tokens need predictable liquidity

A Trading Halo provides **always-on liquidity** via its AMM, ensuring these assets can be traded at any time with predictable pricing.

---

## How It Works

### Capital Flow

```
                          PRIMES
                            |
                            | Allocate USDS via normal PAU infrastructure
                            v
┌───────────────────────────────────────────────────────┐
│                    TRADING HALO                        │
│                                                        │
│   ┌──────────┐      ┌──────────────────────────────┐  │
│   │   PAU    │      │          AMM CONTRACT         │  │
│   │          │─────>│                                │  │
│   │ (USDS   │      │  USDS Pool <──> RWA Pool       │  │
│   │  from   │      │                                │  │
│   │  Primes)│      │  Users sell RWA, get USDS      │  │
│   │          │      │  Users buy RWA, pay USDS       │  │
│   └──────────┘      └──────────────┬─────────────────┘  │
│                                    |                     │
│                     ┌──────────────┴──────────────┐     │
│                     |                             |     │
│                     v                             v     │
│            Accumulated RWA             Spread Revenue   │
│            inventory                   (in USDS)        │
│                     |                                    │
│                     | Redeem with issuer                 │
│                     v                                    │
│            USDS returned to pool                        │
│            (T+1 to T+N depending on asset)              │
│                                                        │
└───────────────────────────────────────────────────────┘
```

### The Trading Cycle (T-Bill Example)

1. **Prime allocates USDS** to the Trading Halo via normal allocation infrastructure (rate-limited, SORL-governed)
2. **USDS flows to AMM pool** — the AMM holds predeposited USDS as trading liquidity
3. **User sells t-bill tokens** to the AMM — receives USDS instantly at a spread below NAV
4. **Trading Halo holds t-bill inventory** — the t-bill tokens sit in the AMM/PAU
5. **Trading Halo redeems t-bills** with the issuer through normal channels (T+1 to T+3)
6. **Issuer settles** — USDS flows back into the AMM pool, replenishing liquidity
7. **Spread captured** — the difference between what the user received and the redemption value is the Halo's revenue

### The Market Making Cycle (JAAA Example)

1. **AMM is funded** with USDS and seeded with initial JAAA inventory
2. **AMM quotes two-sided prices** — bid (buy JAAA) and ask (sell JAAA) around a reference price
3. **Users trade** — buying and selling JAAA against the AMM
4. **AMM earns spread** — the bid-ask spread captures revenue on each round trip
5. **Inventory rebalanced** — when the AMM accumulates excess JAAA, it can be redeemed or reallocated; when JAAA inventory is low, more can be sourced from Primes' existing positions

---

## Architecture

### Trading Halo Class

A Trading Halo Class defines the shared infrastructure for a set of trading pools:

| Component | Description |
|---|---|
| **PAU** | Standard Controller + ALMProxy + RateLimits — holds USDS from Prime allocations |
| **AMM Contract** | Pricing logic, pool management, swap execution — the core mechanism |
| **Supported Assets** | Assets the AMM can trade — must be already onboarded onto the Configurator |
| **Pricing Parameters** | Spread ranges, oracle references, depth/slippage curves |
| **LPHA Beacon** | `lpha-amm` — operates the AMM within governance-defined parameters |

### AMM Design

The AMM is a **programmatic counterparty** that executes swaps at deterministic prices:

| Property | Description |
|---|---|
| **Pricing** | Oracle-referenced with configurable spread — not a constant-product curve |
| **Direction** | Two-sided: buys and sells the supported asset against USDS |
| **Spread** | Governance-configured per asset — compensates for settlement delay, capital cost, and risk |
| **Depth** | Rate-limited — maximum swap size and throughput constrained by PAU rate limits |
| **Inventory** | The AMM holds both USDS and the traded asset; inventory mix changes with trading activity |

**Why oracle-referenced pricing, not constant-product:**

Constant-product AMMs (Uniswap-style) suffer from impermanent loss and require external arbitrageurs to maintain price accuracy. For RWAs with known NAVs and predictable redemption values, oracle-referenced pricing is simpler and more capital efficient:

- Price tracks the asset's NAV (from an approved oracle or the issuer's reported NAV)
- Spread is applied symmetrically or asymmetrically around NAV
- No impermanent loss — the Halo always trades at a known spread to fair value
- No dependence on external arbitrageurs for price accuracy

### Configurator Integration

The assets a Trading Halo can trade must be **already onboarded onto the Configurator** — meaning:

- Core Council has approved the asset via BEAMTimeLock
- Init rate limits exist for the asset
- Primes can already allocate to/from the asset through their PAUs

This is critical: the Trading Halo doesn't create new asset exposure for the ecosystem. It provides liquidity for assets that are already part of the governed allocation universe. When a Trading Halo buys t-bills from a user, those t-bills are the same tokens that Primes already hold and manage — the Trading Halo is just providing a faster entry/exit path.

---

## Use Cases

### Use Case 1: Instant T-Bill Settlement

**Problem:** A user holds tokenized t-bills and wants USDS now. The issuer's redemption process takes T+1 to T+3.

**Solution:**

```
USER                    TRADING HALO                    T-BILL ISSUER
  |                           |                               |
  |  1. Sell 100K t-bills     |                               |
  |  ────────────────────────>|                               |
  |                           |                               |
  |  2. Receive 99.95K USDS   |                               |
  |  <────────────────────────|                               |
  |  (instant, 5bps spread)   |                               |
  |                           |                               |
  |                           |  3. Redeem t-bills            |
  |                           |  ────────────────────────────>|
  |                           |                               |
  |                           |  4. Receive 100K USDS (T+1)  |
  |                           |  <────────────────────────────|
  |                           |                               |
  |                           |  5. USDS back in pool         |
  |                           |  (50 USDS spread captured)    |
```

**Economics:**
- User gets instant liquidity at a small spread (e.g., 5bps)
- Trading Halo earns 5bps on 100K = 50 USDS for 1-3 days of capital lockup
- Annualized: this is attractive yield on the USDS deployed to the pool

**Scale:** With 50M USDS in the pool and average 1-day settlement, the Trading Halo can process ~50M in daily t-bill redemptions while maintaining full liquidity replenishment.

### Use Case 2: Active Market Making (JAAA)

**Problem:** JAAA (a CLO-related Halo Unit token) needs continuous liquidity for price discovery and portfolio rebalancing.

**Solution:**

```
BUYERS/SELLERS              TRADING HALO
      |                          |
      |  Buy 500K JAAA          |
      |  ───────────────────────>|  AMM sells JAAA from inventory
      |  <───────────────────────|  at ask price (NAV + spread)
      |                          |
      |  Sell 300K JAAA          |
      |  ───────────────────────>|  AMM buys JAAA into inventory
      |  <───────────────────────|  at bid price (NAV - spread)
      |                          |
      |                          |  Net: sold 200K JAAA
      |                          |  Earned spread on 800K volume
```

**Economics:**
- Two-sided spread (e.g., 10bps total) on all volume
- Inventory risk managed through oracle pricing and position limits
- Excess JAAA inventory can be redeemed through normal Halo channels
- JAAA deficit can be sourced by buying from Primes' existing allocations

### Use Case 3: Prime Portfolio Rebalancing

**Problem:** A Prime wants to quickly exit an RWA position without waiting for the underlying redemption queue.

**Solution:** The Prime sells RWA tokens to the Trading Halo's AMM for instant USDS, then reallocates elsewhere. The Trading Halo handles the slow redemption process. This is especially valuable during market stress when Primes need to rebalance quickly.

---

## Halo Class Structure

### How Class/Book/Unit Maps to a Trading Halo

The Trading Halo adapts the standard Halo architecture:

**Halo Class** = the Trading Halo's shared infrastructure (PAU + AMM + supported assets + pricing parameters). This is the unit of smart contract deployment and governance.

**Halo Units** = individual trading pools within the Class. Each Unit is a specific asset pair (e.g., USDS/t-bill, USDS/JAAA). Units can use LCTS shares so that multiple Primes providing capital to the same trading pool receive proportional exposure to the pool's spread revenue and inventory risk.

**Halo Books** = the asset-side containers holding trading inventory. Each book holds the RWA inventory accumulated through trading activity. For a t-bill trading pool, the book holds t-bills pending redemption. Book isolation means that if one asset's redemption fails, other trading pools are unaffected.

```
Trading Halo Class
  (PAU + AMM Contract + lpha-amm + pricing parameters)
  |
  +-- Unit: USDS / T-Bill Pool
  |     |
  |     +-- Book: T-bill inventory pending redemption
  |     |     (T-bills bought from users, awaiting issuer settlement)
  |     |
  |     +-- LCTS shares representing Prime capital contributions
  |
  +-- Unit: USDS / JAAA Pool
        |
        +-- Book: JAAA inventory
        |     (JAAA tokens held as market-making inventory)
        |
        +-- LCTS shares representing Prime capital contributions
```

### What Varies Per Unit

| Parameter | Variation |
|---|---|
| **Asset pair** | Which RWA token is traded against USDS |
| **Spread** | Asset-specific: tighter for highly liquid assets (t-bills), wider for less liquid (private credit) |
| **Pool depth** | How much USDS is allocated to this trading pair |
| **Settlement cycle** | How long it takes to redeem the underlying (T+1 for t-bills, longer for others) |
| **Position limits** | Maximum inventory the AMM can accumulate before pausing buys |

---

## Beacon: lpha-amm

The Trading Halo is operated by **lpha-amm**, an LPHA beacon that manages the AMM within governance-defined parameters.

| Property | Description |
|---|---|
| **Type** | LPHA (Low Power, High Authority) — deterministic rule execution |
| **Pricing** | Sets AMM prices based on oracle feeds and configured spreads |
| **Redemption** | Initiates underlying asset redemptions when inventory thresholds are reached |
| **Rebalancing** | Adjusts pool parameters within governance bounds |
| **Cannot** | Change spread parameters, add new trading pairs, or move capital outside PAU rate limits |

### Operational Cycle

```
lpha-amm daily operations:

1. UPDATE PRICING
   - Fetch oracle prices for all supported assets
   - Apply configured spreads
   - Update AMM price curves

2. MANAGE INVENTORY
   - Check inventory levels against thresholds
   - If t-bill inventory > threshold: initiate redemption batch
   - If JAAA inventory out of bounds: adjust pricing to rebalance

3. PROCESS REDEMPTIONS
   - Monitor pending issuer redemptions
   - When issuer settles: route USDS back to AMM pool
   - Update pool state

4. REPORT
   - Post pool state, inventory levels, and P&L to Synome
   - Flag any anomalies (missed redemptions, inventory breaches)
```

### Sentinel Upgrade Path

For active market making strategies (like JAAA), the beacon could be upgraded from an LPHA beacon to a **sentinel formation** in later phases:

- **stl-base** makes dynamic pricing decisions — adjusting spreads based on market conditions, inventory levels, and cross-venue pricing
- **stl-stream** optimizes inventory management — deciding when to source or offload inventory
- **stl-warden** provides independent oversight — monitoring for mispricing, excessive inventory, or abnormal trading patterns

This upgrade path follows the standard beacon progression: deterministic rules first (LPHA), proprietary intelligence later (HPHA sentinel).

---

## Revenue Model

### Spread Revenue

The primary revenue source is the bid-ask spread on trades:

| Asset Type | Typical Spread | Rationale |
|---|---|---|
| **T-bills** (T+1 settlement) | 2-10 bps | Low risk, fast settlement, tight pricing |
| **Money market funds** (T+1 to T+3) | 5-15 bps | Low risk, moderate settlement delay |
| **CLO tranches** (JAAA) | 10-30 bps | Medium risk, active market making |
| **Private credit tokens** | 25-100 bps | Higher risk, longer settlement, less liquid |

### Revenue Distribution

Spread revenue flows to the capital providers (Primes) proportional to their allocation:

1. **User trades with AMM** — spread captured in USDS
2. **Spread accrues to pool** — increases the value of LCTS shares
3. **Primes earn spread** — via their pro-rata share of the pool

This is analogous to how LP fees work in DeFi AMMs, but with oracle-referenced pricing instead of constant-product curves.

### Capital Efficiency

The Trading Halo's capital efficiency depends on the settlement cycle:

| Settlement Time | Capital Turns/Year | Effective Yield (at 5bps spread) |
|---|---|---|
| T+1 | ~250 | ~12.5% |
| T+3 | ~83 | ~4.2% |
| T+7 | ~36 | ~1.8% |

Shorter settlement cycles mean the same USDS pool can process more volume, amplifying spread revenue. T-bill instant settlement is particularly attractive because the fast settlement cycle enables high capital turnover.

---

## Risk Management

### Inventory Risk

The primary risk is that the Trading Halo accumulates RWA inventory that cannot be redeemed at expected value:

| Risk | Mitigation |
|---|---|
| **Issuer default** | Same risk as direct Prime holdings — governed by Halo Artifact and risk framework |
| **Settlement delay** | Spread compensates for expected delay; position limits cap exposure |
| **Inventory concentration** | Per-asset position limits prevent over-accumulation |
| **Oracle failure** | AMM pauses trading if oracle is stale or unavailable |

### Rate Limit Protection

All capital flows through the standard PAU rate limit infrastructure:

- **Prime → Trading Halo**: Rate-limited allocation (SORL-governed increases)
- **AMM swap size**: Constrained by per-asset rate limits on the PAU
- **Redemption outflows**: Rate-limited transfers to issuer redemption endpoints

### Emergency Response

| Scenario | Response |
|---|---|
| **Issuer redemption fails** | lpha-amm pauses buys for that asset; existing inventory held until resolution |
| **Oracle manipulation** | AMM automatically pauses if oracle deviation exceeds threshold |
| **Excessive inventory** | AMM widens spread or pauses buys to halt accumulation |
| **Market stress** | GovOps can instantly decrease rate limits to zero (no SORL constraint on decreases) |

---

## Comparison with Other Halo Types

| Dimension | Portfolio Halo | Term Halo | Trading Halo |
|---|---|---|---|
| **Mechanism** | LCTS queues | NFAT facilities | AMM pools |
| **User interaction** | Queue → wait → receive shares | Negotiate → NFAT minted | Swap instantly |
| **Settlement** | Daily batch (lock/settle cycle) | Per-deal | Atomic (instant) |
| **Revenue** | Yield from deployed capital | Yield from deployed capital | Spread from trading activity |
| **Capital deployment** | Into external strategies | Into bespoke deals | Held as trading liquidity + temporary RWA inventory |
| **LPHA Beacon** | lpha-lcts | lpha-nfat + lpha-attest | lpha-amm |
| **Time horizon** | Long-term (months/years) | Per-deal (weeks/months) | Short-term (days for settlement cycle) |
| **Capacity constraint** | Strategy capacity | Buybox parameters | Pool depth (USDS available) |

---

## Integration with Existing Infrastructure

### Configurator Prerequisite

A Trading Halo can only trade assets that are **already onboarded onto the Configurator**:

1. Core Council approves the asset via BEAMTimeLock (init rate limits, init controller actions)
2. GovOps sets rate limits for the Trading Halo's PAU
3. lpha-amm can now include the asset in the AMM

This means the Trading Halo never introduces new asset exposure to the ecosystem — it provides liquidity for assets that governance has already approved.

### Sky Intents Complementarity

Trading Halos and Sky Intents serve different liquidity needs:

| | Trading Halo (AMM) | Sky Intents (Orderbook) |
|---|---|---|
| **Liquidity type** | Programmatic, always-on | Order-driven, depends on counterparties |
| **Price discovery** | Oracle-referenced + spread | Market-determined via matching |
| **Best for** | Predictable assets with known NAV (t-bills, money markets) | Volatile or complex assets needing price discovery |
| **Settlement** | Atomic on-chain swap | Batch settlement via lpha-exchange |

The two systems complement each other: Trading Halos provide baseline liquidity (you can always trade at the spread), while Sky Intents enable price discovery and potentially better prices when counterparties are available. A sophisticated user might check both venues before executing.

A Trading Halo could also **participate as a counterparty on Sky Intents** — posting intents to buy or sell RWAs through the orderbook as an additional channel.

### Prime Allocation

Primes allocate to Trading Halos through the same infrastructure used for any Halo:

- Normal Prime → Halo PAU allocation (rate-limited, SORL-governed)
- LCTS shares represent the Prime's claim on the trading pool
- Multiple Primes can allocate to the same Trading Halo Unit, sharing spread revenue proportionally

---

## Launching a Trading Halo Unit

### Process

1. **Define trading parameters** — asset pair, spread range, position limits, settlement cycle
2. **Verify Configurator onboarding** — confirm the asset has approved inits
3. **Deploy infrastructure** — PAU + AMM contract (manual w/ spells in early phases; factory in Phase 5+)
4. **Configure lpha-amm** — pricing oracle, spread parameters, inventory thresholds
5. **Governance approval** — Halo Artifact Edit with Unit specifications
6. **Prime allocation** — Primes allocate USDS to the pool; AMM goes live

### Timeline

| Phase | Duration |
|---|---|
| Parameter definition | 1 week |
| Smart contract deployment | Days (factory) |
| Governance approval | ~1 week |
| Prime capital allocation | Immediate after approval (rate-limited ramp) |
| **Total** | **2-3 weeks** |

---

## Summary

Trading Halos provide **instant liquidity** for RWA tokens and ecosystem assets through AMM-based market making:

- **AMM-based** — programmatic counterparty with oracle-referenced pricing and configurable spreads
- **Instant settlement** — users trade atomically; the Halo absorbs the underlying settlement delay
- **Spread revenue** — capital providers (Primes) earn spreads instead of traditional yield
- **Configurator-gated** — can only trade assets already approved by governance
- **PAU-integrated** — standard rate-limited infrastructure for all capital flows
- **Complements Sky Intents** — provides baseline liquidity alongside orderbook-driven price discovery
- **Upgradeable** — starts with lpha-amm (LPHA), can upgrade to sentinel formation for active strategies

The core insight: **settlement delay is a solvable problem with capital.** By deploying USDS into a Trading Halo, Primes convert time delay into spread revenue — and the entire ecosystem gains instant liquidity for assets that would otherwise require days to exit.

---

## Related Documents

| Document | Relationship |
|---|---|
| `agent-type-halos.md` | Halos as a Synomic Agent type |
| `halo-class-book-unit.md` | Class/Book/Unit architecture |
| `portfolio-halo.md` | Portfolio Halo (LCTS-based alternative) |
| `term-halo.md` | Term Halo (NFAT-based alternative) |
| `../smart-contracts/configurator-unit.md` | Configurator — asset onboarding prerequisite |
| `../smart-contracts/lcts.md` | LCTS — token standard for Prime capital contributions |
| `../trading/sky-intents.md` | Sky Intents — complementary orderbook-based trading |

---

*Document Version: 0.1*
*Last Updated: 2026-03-01*
