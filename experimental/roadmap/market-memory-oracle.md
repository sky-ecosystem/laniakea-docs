# Market Memory Oracle — P1 Lean

Lean P1 view of [`../risk-framework/market-memory-oracle.md`](../risk-framework/market-memory-oracle.md). Canonical full body there; this file carries only what P1 binds to.

The Crypto Majors Oracle is a market-memory system, not a tick pusher. Raw source tapes live in archive nodes; oracle loop runs versioned reducers; the synome stores reducer outputs, rolling memories, and provenance checkpoints in `&entity.oracle.crypto-majors.ticks`.

## TL;DR

```
raw source tape in archive nodes
  -> versioned reducer formulas
  -> replay mode (historical) + live-tail mode (new events; same formula)
  -> compressed market-memory atoms in &entity.oracle.crypto-majors.ticks
```

Risk forms read reducer outputs + provenance, not the processing mode.

## 1. P1 topology (sudo at genesis)

```
&entity.oracle.crypto-majors.root          ; identity, supported universe, source/reducer registry
&entity.oracle.crypto-majors.market-data   ; beacon loop body + source/reducer config
&entity.oracle.crypto-majors.ticks         ; current state + rolling memory + reducer checkpoints
```

(`ticks` name retained for topology stability; content is broader than point ticks.)

## 2. Reducers

Versioned formulas, immutable by version. A change creates `*-v2`, never mutates `*-v1`. Same formula runs in replay (archive) and live-tail (new events) modes.

```metta
(market-reducer realized-vol-v1
   (inputs [trade-tape])
   (windows [1d 7d 30d 90d])
   (outputs [realized-vol]))
```

If a new reducer version is approved, archive nodes replay history with the new formula, catch up to real time, then the same reducer continues live. Old version outputs remain verifiable historical artifacts.

## 3. P1 output families

What the `custodial-crypto` risk form reads:

```metta
;; prices and pegs
(price-tick btc usd $price $T)
(price-tick eth usd $price $T)
(price-tick steth eth $basis $T)
(price-tick usdc usd $price $T)
(price-tick usdt usd $price $T)
(price-tick usds usd $price $T)

;; volatility, correlation, basis
(realized-vol btc (window 30d) (reducer realized-vol-v1) $vol $T)
(implied-vol eth (tenor 30d) (reducer implied-vol-v1) $vol $T)
(correlation btc eth (window 90d) (reducer corr-v1) $rho $T)
(basis-drawdown steth eth (window 365d) (reducer basis-v1) $drawdown $T)

;; liquidity and impact (impact curves usually matter more than raw order books)
(orderbook-depth btc usd (side sell) (within-bps 50) $notional $T)
(impact-curve btc usd
   (side sell) (sell-size 100000000) (horizon 4h)
   (reducer impact-v1) (slippage $x) $T)

;; liquidation overhang (market-wide forced selling at price-drop buckets)
(liquidation-overhang btc
   (price-drop -0.10) (reducer liquidation-overhang-v1)
   (estimated-forced-sell-notional $amount) $T)

;; funding, basis, leverage (live stress multipliers — crowded leverage worsens shocks)
(perp-funding btc (venue aggregate) $rate $T)
(perp-basis eth (tenor 30d) $basis $T)
(open-interest btc (venue aggregate) $notional $T)

;; rates and macro factors (factor state; oracle does not decide "rates up = X")
(rate-tick sofr $rate $T)
(rate-tick ust-2y $yield $T)
(rate-tick ust-10y $yield $T)
(macro-factor dxy $value $T)
(macro-factor vix $value $T)
(macro-factor move $value $T)

;; crash memories and quantiles (older history decays into distributional summaries)
(max-drawdown btc (window 365d) (reducer crash-shape-v1) $drawdown $T)
(steepest-crash eth (window 7d) (reducer crash-shape-v1) $drop $T)
(liquidity-quantile btc (window 365d) (quantile 0.05) $depth $T)
(vol-quantile eth (window 365d) (quantile 0.95) $vol $T)

;; data quality (risk forms should default-deny or haircut when stale/divergent/thin)
(market-data-freshness btc $seconds-old $T)
(source-count btc price $n $T)
(source-disagreement btc price $pct $T)
(venue-status coinbase degraded $T)
```

## 4. Scenario interface

Scenarios should be mostly references to reducer outputs:

```metta
(stress-scenario exchange-hack
   (semantic-trigger exchange-hack)
   (venue-availability-ref worst-major-venue-impairment)
   (liquidity-ref p95-liquidity-drought)
   (basis-ref worst-steth-eth-basis-break)
   (manual-override none)
   (approved-by $governance-ref))
```

Discipline: minimize free parameters; maximize references to reducer outputs; make any remaining semantic bridge explicit (e.g. "war means this bundle of rate-spike + liquidity-drought + crypto-risk-off reducer refs"). Later phases can replace thin semantic wrappers with causal models without changing the consumption path.

## 5. What does NOT belong here

Loan facts — collateral amount, debt outstanding, LT, liquidation bonus, maturity/TTM, borrower identity, disbursement account, collateral account, configurator whitelist. Those are exobook / `protocol-registry` / `CHAINREAD` / attestor-gated facts (see [`attestor-atom-schema.md`](attestor-atom-schema.md)).
