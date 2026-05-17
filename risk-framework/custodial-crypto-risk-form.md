# Custodial-Crypto Risk Form

**Status:** Phase 1 live design. Canonical home for the `custodial-crypto` risk-form body shape used by the three P1 term Halos.
**Last Updated:** 2026-05-17

This document specifies the Phase 1 risk-form model for fixed-term custodial crypto lending: BTC / ETH / stETH collateral backing senior USD-frame exo units. It supersedes the older CORE-as-direct-CRR sketch in `riskbook-layer.md` and `asset-type-treatment.md`.

---

## TL;DR

The P1 `custodial-crypto` risk form is a **stress-envelope waterfall model**:

```
approved scenario library
  -> apply shocks to each exobook's collateral asset side
  -> translate stressed assets into USD frame
  -> run the exobook liability waterfall
  -> compute senior exo-unit loss per scenario
  -> default-CRR = worst approved scenario senior loss / senior notional
```

It is not an expected-loss model. Expected loss requires probabilities for scenarios and is useful for pricing, provisioning, and profitability. P1 capital uses the **maximum approved scenario loss** because the capital question is: can the senior exo unit survive the stress scenarios governance says must be survivable?

CORE is calibration and sanity-check material, not the P1 source of truth. CORE's useful levers - LTV distance to liquidation threshold, volatility, executable order-book depth, liquidation bonus, borrower concentration, and crypto tail correlation - inform scenario parameters and reducer design. The binding synomic model is the explicit scenario library plus exobook waterfall.

---

## 1. Composition Scope

The P1 risk form matches riskbooks holding senior tranches of fixed-term custodial crypto exobooks:

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

No mezzanine or equity tranche holdings get recognized in P1. Anything outside the form falls through to default-deny CRR 100%.

---

## 2. Inputs

### Exobook State

Read from exobook atoms and `chain-read` via the Halo protocol registry:

- collateral asset and amount
- collateral account
- senior exo-unit notional and denomination
- borrower junior cushion / residual equity
- liquidation threshold, liquidation bonus, and current LTV
- maturity / term-to-maturity
- exobook lifecycle state

For staged loans, the exobook and exo units can exist before funds leave the Halo PAU. During this state the exobook contains reserved USDC / USDS / USDT still sitting in the PAU and is not yet a funded borrower exposure. Term recognition starts only after funding confirmation, unless the legal term is explicitly an absolute maturity date.

### Admission And Term Attestations

The risk form checks two attestation surfaces:

- **Borrower admission** in the per-halo risk class: borrower, disbursement account, collateral account, configurator whitelist, custody setup, and legal framework are acceptable.
- **Exobook term attestation** at the individual loan level: the stated maturity / TTM and cash-conversion terms are true and enforceable for that exobook.

The attestor does not provide quantitative CRR inputs. It gates whether the exobook can roll up and whether its term can be used for structural-demand matching.

### Market Memory

Read from `&entity.oracle.crypto-majors.ticks`, which stores market-memory reducer outputs rather than just raw ticks. Required live/rolling inputs include:

- BTC / ETH / stETH prices and stETH-ETH basis
- USDC / USDS / USDT peg state
- realized and implied volatility
- correlations, especially BTC-ETH and ETH-stETH
- order-book depth and impact curves
- liquidation overhang by price-drop bucket
- perp funding, basis, and open interest
- rates and macro factor states used by approved scenarios
- data-quality atoms: freshness, source count, source disagreement, venue status

The risk form does not read raw historical tapes. Archive nodes preserve raw source tapes; oracle reducers emit compressed memories and provenance checkpoints. See `market-memory-oracle.md`.

### Scenario Library

P1 scenarios are named stress envelopes. They should minimize arbitrary parameters by referencing market-memory reducers wherever possible:

```metta
(stress-scenario worst-historical-crypto-crash
   (btc-shock-ref worst-btc-drawdown)
   (eth-shock-ref worst-eth-drawdown)
   (steth-basis-ref worst-steth-eth-basis-break)
   (liquidity-ref p95-liquidity-drought))
```

Semantic scenarios such as `war-rate-spike` or `exchange-hack` are allowed in P1, but their discretionary bridge must be explicit: "war means this bundle of rate-spike, liquidity-drought, and crypto-risk-off reducer references." A future causal model can replace that bridge without changing the risk-form consumption path.

---

## 3. Exobook Waterfall

For each exobook `e` and scenario `s`:

```text
stressed_asset_value(e, s)
  = Σ collateral_i(e)
      × stressed_price_i(s)
      × executable_haircut_i(e, s)
    - liquidation_costs(e, s)
```

The senior exo-unit loss is:

```text
senior_loss(e, s)
  = min(senior_notional(e),
        max(0, senior_notional(e) - stressed_asset_value(e, s)))
```

Equivalent tranche framing:

```text
asset_loss(e, s) = current_asset_value(e) - stressed_asset_value(e, s)
junior_cushion(e, s) = scenario-consistent junior cushion value
senior_loss(e, s) = max(0, asset_loss(e, s) - junior_cushion(e, s))
```

The first form is usually safer in implementation because it directly asks whether enough stressed assets survive to pay the senior claim.

---

## 4. Component Output

The risk form outputs all four per-risk-type components:

```metta
(custodial-crypto-crr-components $exobook
   (default-crr   $default)
   (spread-crr    $spread)
   (rate-crr      $rate)
   (liquidity-crr $liquidity)
   (binding-scenario $scenario))
```

### Default-CRR

For P1, default-CRR is the senior exo-unit impairment under the worst approved exobook asset-side scenario:

```text
default-CRR(e) = max_s senior_loss(e, s) / senior_notional(e)
```

Collateral price collapse, stETH basis break, stablecoin denomination stress, and liquidation slippage that reduce exobook recovery are part of default-CRR. Structural-demand matching at the Prime layer cannot remove this risk: if the exobook assets fail to cover the senior exo unit, the senior claim is impaired.

### Spread-CRR

Spread-CRR is the mark-to-market loss on the senior/riskbook/halo unit if the Prime must mark or sell before maturity. For P1 matched `structbook` positions this is covered by SDR held-to-par treatment. It still gets computed so unmatched portions can fall through to forced-loss treatment.

### Rate-CRR

Rate-CRR is term funding / carry mismatch over remaining TTM. It is computed in P1. SDR matching nullifies rate-CRR for the matched portion of the Prime's structbook position. This replaces the older "rate waived" language: the risk exists and is output; matched SDR makes it non-binding for matched capital.

### Liquidity-CRR

Liquidity-CRR is the exit loss of the riskbook/halobook unit itself if the Prime must sell or unwind the wrapper. It is distinct from collateral liquidation slippage inside the exobook waterfall, which belongs in default-CRR because it changes senior recovery.

---

## 5. Riskbook Aggregation

Riskbooks aggregate by shared scenario, not by summing each exobook's individual worst case:

```text
riskbook_loss(r, s) = Σ senior_loss(e, s) for e in riskbook r
riskbook_default_crr(r) = max_s riskbook_loss(r, s) / total_senior_notional(r)
```

This preserves correlation. If BTC, ETH, and stETH crash together in the same scenario, losses aggregate under that same scenario. Cross-riskbook netting is never allowed; Halobook aggregation is pure summation across Riskbook units.

---

## 6. Prime Structbook Consumption

The Prime receives the Halobook unit carrying the risk vector. The structbook then applies SDR matching:

```text
matched capital
  = matched_notional × default-CRR

unmatched capital
  = unmatched_notional × max(default-CRR, spread/liquidity forced-loss)
    + unmatched_notional × rate-CRR
```

In P1, only `structbook` is active. SDR matching covers spread, rate, and liquidity for the matched portion because the Prime can hold the unit to maturity against structural demand. It never covers default-CRR.

---

## 7. CORE Role

CORE is not integrated as a direct `(call-out core-crr ...)` capital engine in P1.

Use CORE for:

- calibrating shock magnitudes and sanity-checking LTV nonlinearity
- estimating liquidation execution haircuts from market depth
- comparing scenario-envelope outputs against expected-loss / pricing models
- informing future scenario library revisions

Do not use CORE for:

- returning the binding CRR scalar
- replacing the exobook waterfall
- hiding scenario probabilities or discretionary assumptions inside an opaque external call

If later phases integrate CORE-style computation directly, it should output scenario losses or calibration artifacts, not bypass the synomic risk-form decomposition.

---

## 8. File Map

| Doc | Relationship |
|---|---|
| `riskbook-layer.md` | Riskbook is the unit of regulation; this doc is the concrete P1 form body for `custodial-crypto` |
| `tranching.md` | Liability waterfall mechanics |
| `capital-formula.md` | Prime-level matched/unmatched capital consumption |
| `market-memory-oracle.md` | Market data and reducer outputs consumed by this form |
| `../roadmap/attestor-atom-schema.md` | Borrower / riskbook admission gate |
| `../roadmap/phase-1-spaces.md` | P1 topology and worked NFAT flow |
