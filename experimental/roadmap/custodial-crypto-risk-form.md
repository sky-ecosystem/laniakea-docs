# Custodial-Crypto Risk Form — P1 Lean

Lean P1 view of [`../risk-framework/custodial-crypto-risk-form.md`](../risk-framework/custodial-crypto-risk-form.md). Canonical full body there; this file carries only what P1 binds to (no multi-phase considerations, no theory beyond binding). Update the canonical first; sync here if it changes binding P1 facts.

The Phase 1 risk-form model for fixed-term custodial crypto lending: BTC / ETH / stETH collateral backing senior USD-frame exo units. Lives per-halo at `&entity.halo.{id}.custodial-crypto`.

## TL;DR

**Stress-envelope waterfall** — not expected loss:

```
approved scenario library
  -> apply shocks to each exobook's collateral asset side
  -> translate stressed assets into USD frame
  -> run the exobook liability waterfall
  -> senior exo-unit loss per scenario
  -> default-CRR = worst approved scenario loss / senior notional
```

The capital question is: can the senior exo unit survive the stress scenarios governance says must be survivable? CORE is calibration/reference only; the binding model is the explicit scenario library + exobook waterfall.

## 1. Composition scope

```metta
(risk-form custodial-crypto
   (level riskbook)
   (frame usd)
   (composition-constraints
      (and (senior-tranche-only)
           (collateral-asset-in [btc eth steth])
           (senior-denom-in [usdc usds usdt])
           (term-to-maturity <= 1y)
           (halo-class nfat-term))))
```

No mezzanine / equity tranche holdings in P1. Anything outside the form falls through to default-deny CRR 100%.

## 2. Inputs

- **Exobook state** via `CHAINREAD` and exobook atoms: collateral asset+amount, collateral account, senior notional+denom, borrower junior cushion, LT/liquidation bonus/current LTV, maturity/TTM, lifecycle state. Staged loans (funds still in PAU) are not yet funded exposure; term recognition starts at funding confirmation unless the legal term is an absolute date.
- **Attestation gates** (boolean admission-only — see [`attestor-atom-schema.md`](attestor-atom-schema.md)): borrower admission + exobook term attestation. Default-deny on missing/stale/fail. The attestor provides no quantitative inputs.
- **Market memory** from `&entity.oracle.crypto-majors.ticks` (full catalog in [`market-memory-oracle.md`](market-memory-oracle.md)): prices, pegs, vol, correlation, basis, depth/impact curves, liquidation overhang, funding/OI, rates/macro, data quality.
- **Scenario library** — named stress envelopes, ideally referencing market-memory reducer outputs:
  ```metta
  (stress-scenario worst-historical-crypto-crash
     (btc-shock-ref worst-btc-drawdown)
     (eth-shock-ref worst-eth-drawdown)
     (steth-basis-ref worst-steth-eth-basis-break)
     (liquidity-ref p95-liquidity-drought))
  ```
  Semantic scenarios (`war-rate-spike`, `exchange-hack`) allowed in P1 but their discretionary bridge must be explicit ("war = bundle of rate-spike + liquidity-drought + crypto-risk-off reducer refs"). Future causal models replace the bridge without changing the consumption path.

## 3. Exobook waterfall

For each exobook `e` and scenario `s`:

```text
stressed_asset_value(e, s)
  = Σ collateral_i(e) × stressed_price_i(s) × executable_haircut_i(e, s)
    - liquidation_costs(e, s)

senior_loss(e, s)
  = min(senior_notional(e),
        max(0, senior_notional(e) - stressed_asset_value(e, s)))
```

Equivalent tranche framing: `asset_loss − junior_cushion`, with scenario-consistent junior cushion revaluation. The first form is usually safer in implementation.

## 4. Component output

```metta
(custodial-crypto-crr-components $exobook
   (default-crr   $default)
   (spread-crr    $spread)
   (rate-crr      $rate)
   (liquidity-crr $liquidity)
   (binding-scenario $scenario))
```

- **default-CRR** = `max_s senior_loss(e, s) / senior_notional(e)`. Includes collateral collapse, stETH basis break, stablecoin depeg, liquidation slippage. Structural-demand matching **never** removes default-CRR.
- **spread-CRR** — MTM loss if Prime must mark/sell before maturity. Covered by SDR held-to-par for the matched structbook portion.
- **rate-CRR** — term funding/carry mismatch over remaining TTM. Computed in P1. SDR matching makes it non-binding for the matched portion.
- **liquidity-CRR** — exit loss on the riskbook/halobook wrapper itself (distinct from collateral liquidation slippage, which is in default-CRR).

## 5. Riskbook aggregation

```text
riskbook_loss(r, s) = Σ senior_loss(e, s) for e in r
riskbook_default_crr(r) = max_s riskbook_loss(r, s) / total_senior_notional(r)
```

Aggregate by shared scenario, not by summing each exobook's individual worst case — preserves correlation. Halobook aggregation is pure summation across Riskbook units; no cross-riskbook netting.

## 6. Prime structbook consumption

```text
matched capital   = matched_notional × default-CRR
unmatched capital = unmatched_notional × max(default-CRR, spread/liquidity forced-loss)
                  + unmatched_notional × rate-CRR
```

In P1 only `structbook` is active. SDR matching covers spread, rate, and liquidity for the matched portion (Prime holds to maturity against structural demand); never default-CRR. Full formula: [`capital-formula.md`](capital-formula.md).

## 7. CORE role

Calibration/reference only — not the binding CRR engine, not called via `call-out`. Use for: shock-magnitude sanity, LTV nonlinearity, liquidation execution haircuts from depth, comparison against expected-loss models, future scenario revisions. Do NOT use for: returning binding CRR, replacing the exobook waterfall, hiding scenario probabilities behind an opaque external call.
