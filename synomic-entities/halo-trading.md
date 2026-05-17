# Trading Halo

A Trading Halo is a Standard Halo Class that operates an **AMM** (Automated Market Maker) using predeposited USDS to market-make assets already onboarded onto the Configurator. Unlike Portfolio Halos (pooled yield products) and Term Halos (bespoke deals), a Trading Halo provides **liquidity services** — instant trades against a programmatic counterparty.

For the Class / Book / Unit architecture, see [`halo-classes.md`](halo-classes.md).

---

## Core Use Cases

### 1. Instant settlement for RWAs

When a user holds tokenized t-bills and wants USDS now, the Trading Halo's AMM buys the RWA instantly at a spread, then redeems the underlying with the issuer over the normal settlement cycle (T+1 to T+3). The spread compensates for time value of capital and settlement risk.

### 2. Active market making of ecosystem assets

For Halo Unit tokens, risk capital tokens (TEJRC, TISRC), and Prime tokens that need continuous liquidity, the AMM provides always-on two-sided quotes. Earning bid-ask spread, managing inventory, supporting price discovery and rebalancing.

---

## Why Trading Halos Exist

### The instant settlement problem

RWA tokens have a structural liquidity mismatch: users want instant liquidity, issuers settle in days, DeFi expects atomic swaps. Without a Trading Halo, exit options are queue-and-wait, thin orderbook venues, or steep-discount sale to a sophisticated buyer.

### The market making problem

Many ecosystem assets need continuous liquidity for price discovery, rebalancing, and composability with DeFi protocols. A Trading Halo provides predictable always-on liquidity via its AMM.

---

## Architecture

```
                          PRIMES
                            |
                            | Allocate USDS via PAU infrastructure
                            v
┌───────────────────────────────────────────────────────┐
│                    TRADING HALO                        │
│                                                        │
│   ┌──────────┐      ┌──────────────────────────────┐  │
│   │   PAU    │      │          AMM CONTRACT         │  │
│   │          │─────>│                                │  │
│   │ (USDS    │      │  USDS Pool <──> RWA Pool       │  │
│   │  from    │      │                                │  │
│   │  Primes) │      │  Users sell RWA, get USDS      │  │
│   │          │      │  Users buy RWA, pay USDS       │  │
│   └──────────┘      └──────────────┬─────────────────┘  │
│                                    |                     │
│                     ┌──────────────┴──────────────┐     │
│                     v                             v     │
│            Accumulated RWA             Spread Revenue   │
│            inventory                   (in USDS)        │
│                     |                                    │
│                     | Redeem with issuer (T+1 to T+N)    │
│                     v                                    │
│            USDS returned to pool                         │
└───────────────────────────────────────────────────────┘
```

### Trading Halo Class

| Component | Description |
|---|---|
| **PAU** | Standard Controller + ALMProxy + RateLimits — holds USDS from Prime allocations |
| **AMM Contract** | Pricing logic, pool management, swap execution — the core mechanism |
| **Supported Assets** | Assets the AMM can trade — must be already onboarded onto the Configurator |
| **Pricing Parameters** | Spread ranges, oracle references, depth/slippage curves |
| **amm-{halo}** | Relay beacon (class `relay`) — operates the AMM within governance bounds |

### AMM design

A programmatic counterparty executing swaps at deterministic prices.

| Property | Description |
|---|---|
| Pricing | Oracle-referenced with configurable spread (not constant-product) |
| Direction | Two-sided: buys and sells the asset against USDS |
| Spread | Governance-configured per asset — compensates for settlement delay, capital cost, risk |
| Depth | Rate-limited — max swap size and throughput constrained by PAU rate limits |
| Inventory | AMM holds both USDS and the traded asset; mix changes with trading activity |

### Why oracle-referenced (not constant-product)

Constant-product AMMs (Uniswap-style) suffer from impermanent loss and require external arbitrageurs to maintain price accuracy. For RWAs with known NAVs and predictable redemption values, oracle-referenced pricing is simpler and more capital efficient: price tracks NAV from approved oracle / issuer-reported NAV; spread is applied symmetrically or asymmetrically; no impermanent loss; no dependence on external arbitrageurs.

---

## Configurator Integration

A Trading Halo can only trade assets **already onboarded onto the Configurator** — meaning Core Council has approved the asset via BEAMTimeLock, init rate limits exist, and Primes can already allocate to/from the asset through their PAUs. The Trading Halo doesn't create new asset exposure for the ecosystem; it provides a faster entry/exit path for existing positions.

For Configurator mechanics, see [`../smart-contracts/configurator-unit.md`](../smart-contracts/configurator-unit.md).

---

## Trading Cycles

### T-bill instant settlement

```
USER                    TRADING HALO                    T-BILL ISSUER
  |                           |                               |
  |  1. Sell 100K t-bills     |                               |
  |  ────────────────────────>|                               |
  |                           |                               |
  |  2. Receive 99.95K USDS   |                               |
  |  <────────────────────────|                               |
  |  (instant, 5bps spread)   |                               |
  |                           |  3. Redeem t-bills            |
  |                           |  ────────────────────────────>|
  |                           |  4. Receive 100K USDS (T+1)   |
  |                           |  <────────────────────────────|
  |                           |  5. USDS back in pool         |
  |                           |  (50 USDS spread captured)    |
```

User gets instant liquidity at a small spread; Trading Halo earns the spread for 1-3 days of capital lockup. With $50M in the pool and average T+1 settlement, the Halo can process ~$50M in daily redemptions while maintaining full liquidity replenishment.

### Active market making (e.g., JAAA)

AMM quotes two-sided prices around a reference NAV; users buy and sell against the AMM; bid-ask spread captures revenue on each round trip; inventory rebalanced via redemption (excess) or sourcing from Primes (deficit).

### Prime portfolio rebalancing

A Prime sells RWA tokens to the Trading Halo's AMM for instant USDS, then reallocates elsewhere. Trading Halo handles the slow underlying redemption. Especially valuable during market stress.

---

## Class / Book / Unit Mapping

The Trading Halo adapts the standard Halo architecture:

```
Trading Halo Class
  (PAU + AMM Contract + amm-{halo} + pricing parameters)
  |
  +-- Unit: USDS / T-Bill Pool
  |     |
  |     +-- Book: T-bill inventory pending redemption
  |     |
  |     +-- LCTS shares representing Prime capital contributions
  |
  +-- Unit: USDS / JAAA Pool
        |
        +-- Book: JAAA inventory
        |
        +-- LCTS shares representing Prime capital contributions
```

| What varies per Unit | Description |
|---|---|
| Asset pair | Which token traded against USDS |
| Spread | Asset-specific (tighter for liquid, wider for illiquid) |
| Pool depth | USDS allocation per pair |
| Settlement cycle | T+1 for t-bills, longer for others |
| Position limits | Max inventory before pausing buys |

Multiple Primes can allocate to the same Unit; LCTS shares give pro-rata claim on the pool's spread revenue and inventory risk. See [`../smart-contracts/lcts.md`](../smart-contracts/lcts.md).

---

## amm-{halo} Operations

`amm-{halo}` is a relay beacon (class `relay`) — deterministic rule execution within governance-defined parameters. See [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md).

### Daily cycle

| Step | Action |
|---|---|
| 1 — Update pricing | Fetch oracle prices; apply configured spreads; update AMM price curves |
| 2 — Manage inventory | Check inventory levels against thresholds; initiate redemption batches; adjust pricing to rebalance |
| 3 — Process redemptions | Monitor pending issuer redemptions; route returned USDS back to pool |
| 4 — Report | Post pool state, inventory, P&L to Synome; flag anomalies |

### Sentinel upgrade path

For active market-making strategies (like JAAA), the operation may upgrade from a plain `amm-{halo}` relay to a full operating setup — `baseline-{halo}` relay + `warden-{halo}-{op}` relay + `stream-{halo}-{actor}` stream-sentinel — adding call-out density for dynamic pricing, inventory management, and proprietary intelligence. See [`../noemar-synlang/synlang-patterns.md`](../noemar-synlang/synlang-patterns.md) §6 for the call-out continuum that connects deterministic relays to stream-sentinels.

---

## Revenue Model

### Spread

| Asset Type | Typical Spread | Rationale |
|---|---|---|
| T-bills (T+1) | 2-10 bps | Low risk, fast settlement |
| Money market funds (T+1 to T+3) | 5-15 bps | Low risk, moderate delay |
| CLO tranches (JAAA) | 10-30 bps | Medium risk, active market making |
| Private credit tokens | 25-100 bps | Higher risk, longer settlement |

### Capital efficiency

Depends on settlement cycle:

| Settlement | Capital Turns/Year | Effective Yield (at 5bps) |
|---|---|---|
| T+1 | ~250 | ~12.5% |
| T+3 | ~83 | ~4.2% |
| T+7 | ~36 | ~1.8% |

Shorter cycles enable higher capital turnover. T-bill instant settlement is particularly attractive because the fast cycle amplifies spread revenue.

---

## Risk Management

| Risk | Mitigation |
|---|---|
| Issuer default | Same risk as direct Prime holdings — governed by Halo Artifact and risk framework |
| Settlement delay | Spread compensates expected delay; position limits cap exposure |
| Inventory concentration | Per-asset position limits prevent over-accumulation |
| Oracle failure | AMM pauses trading if oracle is stale or unavailable |

### Rate limit protection

All flows through PAU rate limits: Prime → Halo allocation (SORL-governed); AMM swap size (per-asset rate limits); redemption outflows (rate-limited transfers to issuer endpoints).

### Emergency response

| Scenario | Response |
|---|---|
| Issuer redemption fails | `amm-{halo}` pauses buys for that asset; existing inventory held |
| Oracle manipulation | AMM auto-pauses if oracle deviation exceeds threshold |
| Excessive inventory | AMM widens spread or pauses buys |
| Market stress | GovOps instantly decreases rate limits to zero (no SORL constraint on decreases) |

---

## Launching a Trading Halo Unit

| Step | Time / Window |
|---|---|
| 1. Parameter definition (asset pair, spread, position limits, settlement cycle) | 1 week |
| 2. Verify Configurator onboarding (asset has approved inits) | — |
| 3. Smart contract deployment (PAU + AMM contract) | Days (factory) |
| 4. Configure `amm-{halo}` (oracle, spread, inventory thresholds) | Days |
| 5. Governance approval (Halo Artifact Edit) | ~1 week |
| 6. Prime allocation | Immediate after approval (rate-limited ramp) |
| **Total** | **2-3 weeks** |

---

## Related

- [`halo-classes.md`](halo-classes.md) — Class / Book / Unit architecture
- [`halo-portfolio.md`](halo-portfolio.md) — LCTS-based alternative
- [`halo-term.md`](halo-term.md) — NFAT-based alternative
- [`prime.md`](prime.md) — Primes that allocate to Trading Halos
- [`../smart-contracts/configurator-unit.md`](../smart-contracts/configurator-unit.md) — Configurator (asset onboarding prerequisite)
- [`../smart-contracts/lcts.md`](../smart-contracts/lcts.md) — LCTS shares for Prime contributions
- [`../sentinel/sentinel-network.md`](../sentinel/sentinel-network.md) — Operating-setup upgrade path
- [`../noemar-synlang/synlang-patterns.md`](../noemar-synlang/synlang-patterns.md) §6 — Call-out continuum (deterministic relay → stream-sentinel)
