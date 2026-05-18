# Risk Framework

**Status:** Target framework plus live P1 instantiation. Phase 1 has one risk class (`custodial-crypto`) materialized per P1 Halo, a stress-envelope risk form for BTC/ETH/stETH-backed exobooks, 30-day SDR buckets, Lindy SDR bucket capacity, an SDR policy overlay, an ownership-weighted temporary SDR auction, and real-time Prime ER. ASC / termbook / hedgebook / Genbook concentration machinery are mostly target architecture or later-phase.
**Canonical home:** `lani/risk-framework/`

---

## TL;DR

Capital math asks: *in a correlated worst-case crash right now, what real claim do we have to real assets that survive?* Loss decomposes into default/fundamental, spread, rate, liquidity, and concentration risk. Books are the universal 6-tuple `(assets, tranches, equity-tranche, rules, state, frame)` with junior-to-senior loss waterfalls. The four-layer stack is Riskbook -> Halobook -> Primebook -> Genbook. Primebook routes exposures into typed sub-books; P1 only activates `structbook`.

P1 `custodial-crypto` does not use expected loss as the capital standard. It runs approved stress scenarios through exobook asset-side impairment and liability waterfall, then capitalizes the **maximum approved scenario loss** to the senior liability / exo unit. Expected loss may later be useful for pricing, but P1 solvency capital is stress-envelope capital.

## Section Map

§1 Risk types · §2 Book primitive · §3 Tranching · §4 Currency frame · §5 Stack · §6 Sub-books · §7 Projection / scenarios · §8 Asset classification + SPTP · §9 SDR model · §10 Matching · §11 Custodial-crypto P1 form · §12 Market-memory oracle · §13 Concentration · §14 Formula / TRRC · §15 ORC / monitoring

## §1 Risk Types

| Type | Time signature | Capital approach |
|---|---|---|
| Default / fundamental | Permanent | Always capitalized |
| Credit-spread MTM | Mean-reverting | Covered by structural/term matching if hold-to-par is credible |
| Rate cash-flow drag | Persistent until maturity / regime shift | Hedge or hold rate capital; computed in P1 |
| Liquidity / fire-sale | Crystallizes only on forced sale | Covered if no forced-sale path; otherwise forced-loss |
| Concentration amplification | Portfolio-level | Category caps + 100% CRR on excess |

Default risk is always required. Sub-books only reduce non-default risks. ASC and ORC are parallel tracks, not position-loss risks inside TRRC.

## §2 Book Primitive

Every book is a 6-tuple with a single equity tranche. Solvent iff equity > 0; equity -> 0 triggers a defined unwind. Rules and state make books financial state machines synserv can re-derive. Bankruptcy remoteness sits at the Riskbook level: no netting across Riskbooks.

## §3 Tranching / Waterfall

Tranches are ordered claims `(seniority, holder, notional, denomination)`. Loss flows junior-to-senior. Exoasset = terminal external asset; exoliab = external-party tranche claim. Cushion revaluation under stress is required, especially when junior cushion is denominated in the same crashing asset. Old "gap risk" and FRTB drawdown collapse into `forced-loss-capital(asset-type)`.

## §4 Currency Frame

Frame = abstract unit of account; instrument = concrete realization with stress profile. Genbook / Primebook / Halobook / Riskbook inherit USD frame from the USDS Generator. Riskbook is the translation layer: it accepts native assets, applies depeg / FX / asset stress, and issues frame-pure claims upward.

## §5 Four-Layer Stack

| Layer | Role |
|---|---|
| **Riskbook** | Unit of regulation; default risk, currency translation, tactical hedging, bankruptcy-remoteness boundary |
| **Halobook** | Bundle exposure structure; owns P/T; never modifies default risk |
| **Primebook** | Composes typed sub-books + unmatched; issues one Primeunit upward |
| **Genbook** | Holds Primeunits; system-wide concentration; deferred in P1 |

Risk form = the equation inside a risk class. P1 has one risk form: `custodial-crypto`, copied into each P1 Halo's risk class Space.

## §6 Typed Sub-Books

| Sub-book | Default | Spread | Rate | Liquidity | P1 status |
|---|---|---|---|---|---|
| `ascbook` | Capital | Capital | n/a | Must hold | Deferred |
| `tradingbook` | Capital | Forced-loss | Hedge/rate capital | Forced-loss | Deferred |
| `termbook` | Capital | Covered | Covered | Covered | Deferred |
| `structbook` | Capital | Covered when SDR-matched | Covered when SDR-matched in P1 | Covered when SDR-matched | Active |
| `hedgebook` | Capital | Hedge residual | Hedge residual | Hedge residual | Deferred |
| Unmatched | Capital | Forced-loss | Forced-loss / rate capital | Forced-loss | Active fallback |

P1 still computes rate-CRR. The carve-out is not "rate ignored"; it is "SDR matching makes rate risk non-binding for the matched structbook portion." Unmatched exposure carries rate treatment.

## §7 Projection / Scenarios

Projection functions map `(position, scenario) -> stress-loss-number`. Mature framework supports analytical, lattice, Monte Carlo, parametric, and ML projections with model-uncertainty haircuts. P1 favors many simple approved scenarios over one overengineered model: historical worst crash, rate spike, rate crash, exchange hack, liquidity freeze, war / macro shock, stETH depeg, stablecoin depeg, and similar categories. Exact scenario catalog remains open.

Scenarios should minimize arbitrary inputs by referencing market-memory reducer outputs wherever possible. Any semantic bridge ("war means this bundle of rate-spike, liquidity drought, and crypto risk-off references") must be explicit.

## §8 Asset Classification + SPTP

Terminal exoassets have canonical risk profiles: fundamental RW, drawdown distribution, slippage model, SPTP, correlations, and currency stress. SPTP = stressed pull-to-par, because the stress scenario is when pull-to-par timing matters. Examples: JAAA SPTP 1,260 days; BTC/ETH terminal spot assets have no pull-to-par; fixed-term NFAT loans use remaining nominal term in P1.

## §9 SDR Model

Structural-demand capacity lives in `&entity.generator.usge.structural-demand`.

P1 live state:

- 30-day buckets, 51 total.
- Bucket N = N * 30 days; bucket 50 = 1,500+ days.
- JAAA 1,260-day SPTP -> bucket 42.
- 180-day P1 NFAT -> bucket 6.
- Bucket capacities are computed as effective SDR bucket capacity atoms in P1.
- Live Lindy lot-age scraping, SDR policy overlay processing, and open-ended holder iteration are part of the P1 structural-demand surface.

Target Lindy model: expected remaining holding = lot age × Lindy factor × conservative haircut. Structural maximum caps use the double-exponential curve calibrated to bank-run empirics:

```
Cap(t) = A*e^(-lambda1*t) + B*e^(-lambda2*t)
A = 10%, lambda1 = 0.35
B = 0.70%, lambda2 = 0.0175
```

Capacity at bucket N is cumulative over buckets >= N.

P1 allocation is simple by design: every DSC epoch, synserv refreshes the lot-age surface, runs Lindy SDR, applies the SDR policy overlay, reads Prime ownership weights, writes current-epoch `(sdr-allocation $prime $bucket $amount $epoch)` atoms in `&entity.generator.usge.sdr-auction`, and `structbook` consumes only those atoms. There is no P1 reservation market, durable SDR ownership, sticky claim, or carry-forward accounting.

## §10 Matching

Hold-to-par matching protects against credit-spread risk by supporting hold-to-par behavior. In P1, SDR matching also makes rate and liquidity non-binding for the matched structbook portion by design. Default/fundamental risk remains capitalized.

Structbook formula shape:

```
matched_capital   = matched * default_crr
unmatched_capital = unmatched * max(default_crr, forced_loss_crr) + unmatched * rate_crr
position_capital  = matched_capital + unmatched_capital
```

Exact implementation may keep spread/liquidity terms explicit, but matched SDR sets them non-binding in P1.

## §11 Custodial-Crypto P1 Risk Form

Canonical detail: `custodial-crypto-risk-form.md`.

The P1 form takes exobooks with BTC/ETH/stETH collateral and senior USD liabilities. It runs approved scenarios over asset prices, liquidity, funding, volatility, liquidation overhang, depeg/basis, and rates/macro reducer outputs. For each exobook and scenario:

```
stressed_asset_value = sum(collateral_i * stressed_price_i * executable_haircut_i) - liquidation_costs
senior_loss          = min(senior_notional, max(0, senior_notional - stressed_asset_value))
default_crr          = max_s(senior_loss_s) / senior_notional
```

The risk form outputs four components: `default-CRR`, `spread-CRR`, `rate-CRR`, `liquidity-CRR`. CORE is used for calibration, reference scenarios, and sanity checks, not as a 1:1 engine.

## §12 Market-Memory Oracle

Canonical detail: `market-memory-oracle.md`.

Crypto Majors Oracle is a market-memory oracle. Archive nodes hold raw source tapes. Synome stores versioned reducer outputs and checkpoints. The same reducer formulas run in replay mode over historical tapes and live-tail mode over new events. If the reducer approach changes, archive nodes replay history with the new formulas, catch up, and the same formulas continue live.

Minimum P1 output families:

- price / peg / basis;
- volatility and drawdown;
- cross-asset correlations;
- orderbook depth / market-impact curves;
- liquidation overhang;
- perp funding / open interest / basis;
- rates and macro factors;
- data-quality and source-health atoms;
- reducer checkpoints.

## §13 Concentration

Two levels: Primebook (within a Prime) and Genbook (system-wide). Governance defines non-mutually-exclusive correlation categories; excess gets 100% CRR; no stacking, max-binding category only. P1 Genbook enforcement is deferred, but formulas and monitoring shape remain target.

## §14 Capital Formula -> TRRC

Flow: risk form -> Halobook P/T -> Primebook routing -> sub-book capital -> concentration -> TRRC.

```
TRRC[p] = sum(position_capital) + sum(excess_capital)
ER[p]   = TRRC[p] / TRC[p]
target ER <= 0.90
```

TRC funding spans IJRC / EJRC / SRC tiers with ingression-adjusted recognition. `prime-ijrc` is read by the P1 temporary SDR auction for ownership-weight allocation.

## §15 ORC / Monitoring

ORC is parallel to portfolio capital: Guardian / operator damage is sized as Rate Limit × TTS. P1 uses the pre-sentinel IRL/SORL approximation; sentinel-era ORC becomes explicit in Guardian Accords. Monitoring includes solvency, liquidity, concentration, stress, operational, per-sub-book CRR, equity proximity, and treatment-switch frequency.

## Key Vocabulary

- **TRRC / TRC / ER** — Total Required Risk Capital / Total Risk Capital / TRRC÷TRC
- **6-tuple book** — universal book primitive
- **Equity invariant** — exactly one equity tranche; equity -> 0 triggers unwind
- **Exoasset / Exoliab** — terminal external asset / external-party tranche claim
- **Forced-loss capital** — unified gap / fire-sale loss primitive
- **U / P / T** — underlying unwind / permitted unwind / transfer market
- **Risk form** — equation inside a risk class
- **Stress-envelope capital** — max approved scenario loss, not expected loss
- **Market memory** — reducer outputs + checkpoints from archive-node source tapes
- **SPTP** — stressed pull-to-par
- **SDR bucket** — one of 51 30-day buckets
- **SDR** — Structural Demand Resource used by `structbook`
- **Lindy SDR** — dynamic structural-demand model output from the lot-age surface
- **SDR policy overlay** — governance-set caps, haircuts, source filters, and fallback bounds
- **P1 SDR auction** — temporary pro-rata body allocating every effective SDR bucket by ownership weight
- **ORC** — Operational Risk Capital

## Cross-References

- `roadmap/phase-1-spaces.md` — live P1 topology and worked NFAT example
- `risk-framework/custodial-crypto-risk-form.md` — P1 risk form
- `risk-framework/market-memory-oracle.md` — Crypto Majors market-memory design
- `risk-framework/sdr-model.md` — bucket capacity and Lindy target model
- `risk-framework/matching.md` — SDR matching treatment
- `risk-framework/primebook-composition.md` — sub-book routing
- `accounting/sdr-auction.md` — target real auction / tug-of-war design
- `accounting/capital-stack.md` — funds TRRC
- `macrosynomics/beacon-framework.md` — market-data / attest-data / patch-beacon classes

## File Map

| File | What's in it that the summary doesn't have |
|---|---|
| `risk-decomposition.md` | Risk-type justification and sub-book coverage matrix |
| `book-primitive.md` | Universal book synlang and equity-feed mechanisms |
| `tranching.md` | Waterfall mechanics and cushion revaluation |
| `currency-frame.md` | Frame / instrument synlang |
| `riskbook-layer.md` | Risk-form catalog shape and P1 custodial-crypto sketch |
| `custodial-crypto-risk-form.md` | P1 max-scenario-loss model, component outputs, CORE role |
| `market-memory-oracle.md` | Raw archive / reducer / replay-live-tail design |
| `halobook-layer.md` | Halobook structural features and `nfat-term` |
| `primebook-composition.md` | Routing, sub-book formulas, crash-oracle sketch |
| `hedgebook.md` | Hedge residual CRR model |
| `projection-models.md` | Projection taxonomy and model-risk haircuts |
| `asset-classification.md` | Canonical asset profiles and SPTP tables |
| `correlation-framework.md` | Concentration categories, cap equations, and capacity-rights mechanics |
| `sdr-model.md` | 30-day SDR buckets, Lindy SDR, SDR policy overlay, P1 temporary SDR auction inputs |
| `matching.md` | Spread/rate/liquidity matching distinctions |
| `capital-formula.md` | Per-sub-book capital formulas and worked P1 logic |
| `asset-type-treatment.md` | Asset-class treatment examples |
| `operational-risk-capital.md` | P1 and sentinel-era ORC formulas |
| `risk-monitoring.md` | Metrics, stress testing, ER enforcement proposal |
| `sentinel-integration.md` | Later sentinel / warden integration |
