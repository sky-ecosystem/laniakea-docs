# Market Memory Oracle

**Status:** Phase 1 live design. Canonical risk-framework view of the Crypto Majors Oracle's data surface.
**Last Updated:** 2026-05-17

The Crypto Majors Oracle is not merely a tick pusher. It is a **market memory system**: raw source tapes live in archive nodes; the oracle loop runs versioned reducers over those tapes; the synome stores reducer outputs, rolling memories, and provenance checkpoints.

---

## TL;DR

```
raw source tape in archive nodes
  -> versioned reducer formulas
  -> replay mode for historical backfill
  -> live-tail mode for new events
  -> compressed market-memory atoms in &entity.oracle.crypto-majors.ticks
```

The same reducer formula must run in both modes. If a new reducer version is approved, archive nodes replay historical raw data using the new formula, catch up to real time, then the same reducer continues live. Governance approves reducer versions and scenario mappings; it does not manually rewrite history.

---

## 1. Placement

P1 already has the topology:

```text
&entity.oracle.crypto-majors.root
&entity.oracle.crypto-majors.market-data
&entity.oracle.crypto-majors.ticks
```

- `root` holds identity, supported universe, source registry, and reducer registry.
- `market-data` holds the market-data beacon loop body plus source/reducer config.
- `ticks` holds current market-state atoms, rolling memory atoms, and reducer checkpoints.

The Space name `ticks` is retained for topology stability even though its content is broader than point ticks.

---

## 2. Raw Source Tapes

With archive storage assumed available, preserve raw inputs as close to source form as practical:

- spot trades
- spot order-book deltas and snapshots
- perp/futures trades
- perp/futures order books
- funding rates
- open interest
- liquidation prints and liquidation estimates
- options chain quotes, trades, and open interest
- on-chain DEX swaps and pool state
- stETH protocol state and stETH/ETH pool state
- stablecoin peg trades, supply, redemptions, and reserve facts where available
- rates and yield-curve data
- macro indices/factors
- venue status, outages, and source-quality metadata

The synome does not store these raw tapes as ordinary atoms. Archive nodes do. The synome stores compressed outputs and provenance references.

---

## 3. Reducers

A reducer is a versioned formula that turns raw tapes into market-memory atoms:

```metta
(market-reducer realized-vol-v1
   (inputs [trade-tape])
   (windows [1d 7d 30d 90d])
   (outputs [realized-vol]))

(market-reducer crash-shape-v1
   (inputs [price-tape])
   (windows [1d 7d 30d 365d])
   (outputs [max-drawdown steepest-crash recovery-time]))
```

Reducers are immutable by version. A change in understanding creates `*-v2`, not a mutation of `*-v1`.

Execution modes:

- **Replay mode:** archive tape range -> backfilled summary atoms.
- **Live-tail mode:** new source events -> updated summary atoms.

The output does not reveal which mode produced it. Risk forms read the reducer output and provenance, not the processing mode.

---

## 4. P1 Output Families

### Prices And Pegs

```metta
(price-tick btc usd $price $T)
(price-tick eth usd $price $T)
(price-tick steth eth $basis $T)
(price-tick usdc usd $price $T)
(price-tick usdt usd $price $T)
(price-tick usds usd $price $T)
```

### Volatility, Correlation, And Basis

```metta
(realized-vol btc (window 30d) (reducer realized-vol-v1) $vol $T)
(implied-vol eth (tenor 30d) (reducer implied-vol-v1) $vol $T)
(correlation btc eth (window 90d) (reducer corr-v1) $rho $T)
(basis-drawdown steth eth (window 365d) (reducer basis-v1) $drawdown $T)
```

### Liquidity And Market Impact

```metta
(orderbook-depth btc usd (side sell) (within-bps 50) $notional $T)

(impact-curve btc usd
   (side sell)
   (sell-size 100000000)
   (horizon 4h)
   (reducer impact-v1)
   (slippage $x)
   $T)
```

Risk forms usually need impact curves more than raw order books: "if we must sell $X over horizon H, what stressed haircut should we assume?"

### Liquidation Overhang

```metta
(liquidation-overhang btc
   (price-drop -0.10)
   (reducer liquidation-overhang-v1)
   (estimated-forced-sell-notional $amount)
   $T)
```

This captures market-wide forced selling if BTC/ETH falls through a price-drop bucket.

### Funding, Basis, And Leverage

```metta
(perp-funding btc (venue aggregate) $rate $T)
(perp-basis eth (tenor 30d) $basis $T)
(open-interest btc (venue aggregate) $notional $T)
```

These can act as live stress multipliers. Crowded leverage makes the same price shock worse.

### Rates And Macro Factors

```metta
(rate-tick sofr $rate $T)
(rate-tick ust-2y $yield $T)
(rate-tick ust-10y $yield $T)
(macro-factor dxy $value $T)
(macro-factor vix $value $T)
(macro-factor move $value $T)
```

The oracle does not decide "rates up 300 bps means BTC down X." Scenario definitions map semantic events to reducer references. The oracle streams factor state and rolling memories.

### Crash Memories And Quantiles

```metta
(max-drawdown btc (window 365d) (reducer crash-shape-v1) $drawdown $T)
(steepest-crash eth (window 7d) (reducer crash-shape-v1) $drop $T)
(liquidity-quantile btc (window 365d) (quantile 0.05) $depth $T)
(vol-quantile eth (window 365d) (quantile 0.95) $vol $T)
```

Recent history can keep finer summaries; older history decays into distributional summaries, extremes, quantiles, and regime descriptors.

### Data Quality

```metta
(market-data-freshness btc $seconds-old $T)
(source-count btc price $n $T)
(source-disagreement btc price $pct $T)
(venue-status coinbase degraded $T)
```

Risk forms should default-deny or apply punitive haircuts when critical market memory is stale, divergent, or sourced from too few venues.

---

## 5. Scenario Interface

Scenarios should be mostly references to market-memory outputs:

```metta
(stress-scenario exchange-hack
   (semantic-trigger exchange-hack)
   (venue-availability-ref worst-major-venue-impairment)
   (liquidity-ref p95-liquidity-drought)
   (basis-ref worst-steth-eth-basis-break)
   (manual-override none)
   (approved-by $governance-ref))
```

Durable discipline:

- Minimize free parameters.
- Maximize references to reducer outputs.
- Make the remaining semantic bridge explicit.

P1 can use thin semantic wrappers such as `war-rate-spike` or `exchange-hack`. Later phases can replace those with richer causal models without changing the risk-form read path.

---

## 6. What Does Not Belong Here

The market-memory oracle does not store loan facts:

- collateral amount
- debt outstanding
- liquidation threshold
- liquidation bonus
- maturity / TTM
- borrower identity
- disbursement account
- collateral account
- configurator whitelist status

Those are exobook, protocol-registry, chain-read, or attestor-gated facts. The oracle supplies market state and market memory only.

---

## 7. Reprocessing

When the compression approach changes:

1. Governance approves a new reducer version.
2. Archive nodes replay historical raw tapes with that reducer.
3. Replayed outputs land as new-version atoms with provenance checkpoints.
4. Once replay catches up to real time, the reducer switches to live-tail mode.
5. Risk forms migrate to the new reducer version at the relevant phase boundary.

Old reducer outputs remain verifiable historical artifacts. They are not mutated.

---

## 8. File Map

| Doc | Relationship |
|---|---|
| `custodial-crypto-risk-form.md` | Consumes market-memory atoms for scenario-loss computation |
| `riskbook-layer.md` | Riskbook layer where the risk form reads these outputs |
| `asset-classification.md` | Canonical asset stress profiles can be derived from reducer outputs |
| `../roadmap/phase-1-spaces.md` | P1 topology for the Crypto Majors Oracle |
| `../macrosynomics/beacon-framework.md` | `market-data-beacon` class definition |

