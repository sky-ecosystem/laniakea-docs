# Asset Type Treatment

**Status:** Draft (Phase 3 update, 2026-05-05)

Worked per-asset-class treatment under the new framework. Each asset class is expressed via the substrate primitives (book primitive, tranching, currency frame, projection models) and routed to the appropriate Primebook sub-book.

Companion to:
- [`book-primitive.md`](book-primitive.md), [`tranching.md`](tranching.md), [`currency-frame.md`](currency-frame.md) — substrate primitives
- [`riskbook-layer.md`](riskbook-layer.md), [`primebook-composition.md`](primebook-composition.md) — layer architecture
- [`asset-classification.md`](asset-classification.md) — canonical asset stress profiles
- [`projection-models.md`](projection-models.md) — projection patterns for complex positions
- [`capital-formula.md`](capital-formula.md) — final per-position capital math

---

## TL;DR

Each asset class has a structural shape (direct holding, tranched exobook, projected position) and a sub-book routing path. The new framework collapses several historically-distinct treatments — gap risk, FRTB drawdown — into uniform asset-stress propagation through tranche structures.

| Asset class | Structural shape | Routing path | Notes |
|---|---|---|---|
| Direct ETH/BTC | Terminal exoasset | `tradingbook` if liquid, else unmatched | No SPTP, no tranche structure |
| Sparklend (overcollateralized lending) | Senior tranche of perpetual ETH-collateralized exobook | `tradingbook` if liquid, else unmatched | No SPTP (perpetual); standard tranche math |
| NFAT (crypto-collateralized) | Senior tranche of fixed-term exobook | `structbook` (matched) | V1 carve-out: no rate-hedge capital |
| JAAA (CLO AAA) | Senior tranche of CLO exobook | `termbook`/`structbook` matched, with FRTB drawdown for tradeable secondary market | Standard tranche math + secondary market liquidity |
| Liquid TradFi (T-bills, MMF) | Direct holding, short SPTP | `termbook`/`structbook`/`tradingbook` | SPTP enables matching |
| Vanilla options | Position with projection model (Black-Scholes) | Riskbook → sub-book per nature | Projection-model risk haircut |
| ABF (private credit) | Senior tranche of ABF exobook | `structbook`/`termbook` matched | Sponsor retention is exoliab |

---

## Direct ETH/BTC holdings

| Component | Treatment |
|---|---|
| Structural shape | Terminal exoasset (no tranche structure) |
| Fundamental risk | Per-asset risk weight from [`asset-classification.md`](asset-classification.md) |
| Drawdown | Asset's canonical liquidity profile |
| SPTP | Infinite (no maturity) |
| Matching | Not eligible (no SPTP) |
| Routing | `tradingbook` if liquid + transferable, else unmatched |
| **Capital** | `Position Size × max(Risk Weight, Forced-Loss Capital)` |

The direct holding has no tranche structure. Forced-loss capital reads directly from the asset's drawdown distribution.

## Sparklend / overcollateralized crypto lending

| Component | Treatment |
|---|---|
| Structural shape | Senior tranche of perpetual ETH-collateralized exobook |
| Fundamental risk | Smart contract risk + oracle risk |
| Drawdown | ETH liquidity stress through junior cushion (per `tranching.md`) |
| SPTP | None (perpetual positions) |
| Matching | Not eligible (no SPTP) |
| Routing | `tradingbook` if liquid + transferable, else unmatched |
| **Capital** | `Position Size × max(Risk Weight, Asset-Stress-Through-Junior-Cushion)` |

The exobook structure:
```
Exobook (per-loan):
   asset side: ETH collateral (custodial or smart-contract)
   liability side (tranched):
      junior: borrower equity (exoliab, denom usd)
      senior: loan principal (held by Spark, denom usdc)
   rules: liquidation trigger on health-factor breach
   state: current collateral value, current health factor
```

Senior's risk = ETH liquidity stress, propagated through the junior cushion. Standard structured-product capital model — no special "gap risk" treatment (per `tranching.md` §6).

## NFAT (crypto-collateralized fixed-term)

| Component | Treatment |
|---|---|
| Structural shape | Senior tranche of fixed-term BTC/ETH/stETH exobook |
| Fundamental risk | Counterparty (custodian) + smart contract |
| Drawdown | Asset stress through tranche waterfall + denom-depeg stress |
| SPTP | Remaining contractual term (no stress modifier for v1) |
| Matching | Eligible for `structbook` |
| Routing | `structbook` (active for v1 test) |
| **Capital** | `Matched × RW + Unmatched × max(RW, Forced-Loss)` per [`capital-formula.md`](capital-formula.md) |

V1 carve-out: no rate-hedge capital required for matched portion (resumed in v2+).

V1 test `crypto-collateralized-USD-lending` Riskbook category sketch:
```metta
(book-category-def crypto-collateralized-USD-lending
   (frame usd)
   (composition-constraints
     (and (single-senior-tranche-positions)
          (asset-class-in (eth btc stETH))
          (denom-in (usdc usdt))))
   (equation-m2m
     (sum-over (held-senior-tranches)
       (lambda ($pos)
         (let* (($asset-stress  (asset-stress-profile (collateral-of $pos)))
                ($denom-depeg   (depeg-stress-profile (denom-of $pos)))
                ($junior-cushion (junior-tranche-size (exobook-of $pos))))
           (simulate-across-scenarios m2m-scenarios
             (lambda ($s)
               (+ (max 0 (- (apply-scenario $s $asset-stress) $junior-cushion))
                  (apply-scenario $s $denom-depeg)))))))))
```

## JAAA / CLO AAA

| Component | Treatment |
|---|---|
| Structural shape | Senior tranche of CLO exobook with deep junior cushion |
| Fundamental risk | Credit risk of underlying loans |
| Drawdown | Stressed loss waterfall + secondary-market liquidity stress |
| SPTP | ~3.5 years (~1,260 days) — credit-spread duration; same for rate duration |
| Matching | Eligible for `termbook`/`structbook` (bucket 84) |
| Routing | Matched portion → `termbook`/`structbook`; unmatched → `tradingbook` (FRTB drawdown applies) |
| **Capital** | `Matched × RW + Unmatched × max(RW, FRTB)` per [`capital-formula.md`](capital-formula.md) |

Note: JAAA modeling is **deferred for v1** due to recursive complexity (CLO of loans, with tranche subordination + active management + secondary market). The structural framing is in place; the full Riskbook category equation comes online once governance is ready to vet the recursive structure.

## Liquid TradFi (T-bills, MMF, STRB)

| Component | Treatment |
|---|---|
| Structural shape | Direct holding (no tranche structure for short-term TradFi) |
| Fundamental risk | Credit risk of underlying securities |
| Drawdown | FRTB-style drawdown for unmatched portion |
| SPTP | Term (with stress modifier for prepayment-bearing assets) |
| Matching | Eligible for `termbook`/`structbook` if SPTP fits |
| Routing | Per matching availability |
| **Capital** | `Matched × RW + Unmatched × max(RW, FRTB)` |

Short-duration T-bills have minimal rate risk and route to short-bucket matched treatment efficiently. Money market ETFs have near-zero SPTP and can match against the shortest buckets or trade directly.

## Vanilla options

| Component | Treatment |
|---|---|
| Structural shape | Position with projection model (Black-Scholes) |
| Fundamental risk | Counterparty (writer) — for held options; covered by structure for written options |
| Stress treatment | Black-Scholes stress projection per scenario (per [`projection-models.md`](projection-models.md)) |
| Model uncertainty haircut | ~0% (Black-Scholes is well-validated for vanilla) |
| Matching | Generally not (options don't have SPTP in the matching sense) |
| Routing | Riskbook category-dependent — typically `tradingbook` for liquid; unmatched otherwise |
| **Capital** | Per the Black-Scholes projection × scenario weights, plus default capital |

Path-dependent options (Asian, lookback, barrier) use Monte Carlo or analytic projections instead of Black-Scholes; categories may carry higher model-uncertainty haircuts.

## ABF (private credit / asset-backed finance)

| Component | Treatment |
|---|---|
| Structural shape | Senior tranche of ABF exobook (asset = real cash flows; junior = sponsor retention or equity tranche) |
| Fundamental risk | Credit risk of underlying receivables + sponsor performance |
| Drawdown | Stressed cash flow + junior cushion |
| SPTP | Per loan structure (typically fixed term) |
| Matching | Eligible for `termbook`/`structbook` if rate-neutral |
| Routing | Per matching availability and Halobook structure |
| **Capital** | Standard tranched-exobook capital math |

Off-chain ABF requires attestor-driven onboarding for the exobook state (collateral value, debt outstanding, sponsor health). The attestor schema and reconciliation cycle are tracked in [`open-questions.md`](open-questions.md).

## Hedge structures

For positions composed with hedges:

- **Tactical hedges** (specific position + specific hedge in one strategy) → live in one Riskbook with a category equation that knows the relationship (per [`riskbook-layer.md`](riskbook-layer.md) §5)
- **Portfolio hedges** (broad-market hedges across diverse positions) → live in the Hedgebook (per [`hedgebook.md`](hedgebook.md))

Currency hedges (e.g., USDC depeg hedge protecting USDC concentration across many Riskbooks) typically live in the Hedgebook.

---

## What changed from prior version

| Old framing | New framing |
|---|---|
| Liquid TradFi gets FRTB drawdown directly | Liquid TradFi gets matched/unmatched blend; unmatched portion gets FRTB |
| Crypto lending gets gap risk | Crypto lending = senior tranche of exobook; standard tranche math |
| TradFi overcollateralized = hybrid (gap + matching) | All overcollateralized lending = senior tranche of exobook |
| Risk weight, drawdown, SPTP as three separate properties | Full risk-type tuple (RW + drawdown + slippage + SPTP + correlations + currency) |
| Halobook applies liquidity downgrade | Halobook declares P + T (and other bundle exposure structure) per [`halobook-layer.md`](halobook-layer.md) |

The unifications are in [`tranching.md`](tranching.md) and [`risk-decomposition.md`](risk-decomposition.md). This doc just shows the result per asset class.

---

## File map

| Doc | Relationship |
|---|---|
| [`book-primitive.md`](book-primitive.md), [`tranching.md`](tranching.md), [`currency-frame.md`](currency-frame.md) | Substrate primitives every asset class uses |
| [`asset-classification.md`](asset-classification.md) | Per-asset canonical risk profiles consumed here |
| [`riskbook-layer.md`](riskbook-layer.md) | Riskbook category equations for each asset class |
| [`primebook-composition.md`](primebook-composition.md) | Sub-book routing decisions per asset class |
| [`projection-models.md`](projection-models.md) | Projections for vanilla options and complex positions |
| [`capital-formula.md`](capital-formula.md) | Per-position capital flow consuming the treatments here |
| [`examples.md`](examples.md) | Worked v1 test scenario combining several asset classes |
