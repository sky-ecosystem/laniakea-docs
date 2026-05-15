# Risk Framework

**Status:** Mostly target architecture. Phase 1 reality is a single black-box Riskbook risk form (`crypto-collateralized-USD-lending`); the layered model is real synlang scaffolding with most parameters carved out, deferred, or governance-set. ASC and `termbook` (tUSDS-matched) markets do not exist yet.
**Canonical home:** `laniakea-docs/risk-framework/`

---

## TL;DR

Capital math for the Sky stack. **Teleological grounding:** *in a correlated worst-case crash right now, what real claim do we have to real assets that survive?* Loss decomposes into **five atomic risk types**; capital lives at the irreducible portion of each. Substrate is a **6-tuple book** with universal equity invariant; tranching propagates loss through seniority structures uniformly, collapsing old "gap risk" vs "FRTB drawdown" into one `forced-loss-capital(asset-type)` math. The four-book stack (Riskbook → Halobook → Primebook → Genbook) splits responsibility: **Riskbook is the unit of regulation** (default risk + currency translation + tactical hedging); Halobook declares P/T (lockup/transferability) without modifying default; Primebook composes **five typed sub-books + unmatched** (each a risk-coverage contract). **Default-deny CRR 100%** for any composition the framework can't model. Output is per-Prime **TRRC**; ER = TRRC / TRC, target ≤ 0.90. **ORC** is a parallel track for operational/key-compromise risk (Rate Limit × TTS, posted by Guardians).

## Section map

| § | Topic |
|---|---|
| 1 | Five risk types + U/P/T |
| 2 | 6-tuple book + equity invariant |
| 3 | Tranching + waterfall + gap-risk unification |
| 4 | Currency frame vs instrument |
| 5 | Four-layer stack |
| 6 | Five typed sub-books |
| 7 | Hedgebook vs Riskbook hedging |
| 8 | Projection models |
| 9 | Asset classification + SPTP |
| 10 | Duration model (101 buckets, double-exponential caps) |
| 11 | Matching: credit-spread vs rate |
| 12 | Concentration: two levels |
| 13 | Capital formula → TRRC |
| 14 | Operational Risk Capital |
| 15 | Monitoring + sentinel integration |

---

## §1. Five risk types + U/P/T

| Type | Time signature | Capital approach |
|---|---|---|
| Default / fundamental | Permanent | Always required (RW) — irreducible |
| Credit-spread MTM | Mean-reverting (months) | Avoidable if hold-to-par |
| Rate cash-flow drag | Permanent until maturity / regime revert | Hedge or rate-hedge capital |
| Liquidity / fire-sale | Crystallizes only on forced sale | Avoidable if not forced to sell |
| Concentration amplification | Portfolio-level | Category caps + 100% CRR on excess |

**Default capital is always required.** Sub-book structure only reduces the *other* four. ASC and ORC are **parallel tracks** (operational obligations, not position-loss risks).

**U/P/T** splits liquidity into three layered questions: **U — Underlying unwind** (Riskbook): walks structure to terminal asset, applies stress through tranches; **P — Permitted unwind** (Halobook): lockups, approvals, notice; **T — Transfer market** (Halobook): can the wrapper be sold? Two exit paths: `U AND P`, or `T`. `tradingbook` needs `(U AND P) OR T`; `structbook`/`termbook` need neither (held to maturity); `ascbook` needs near-instantaneous T.

**Cross-default constraint:** default risk is set entirely at the Riskbook level; the Halobook never modifies it. Joint-default linkage requires composing positions in **a single Riskbook** with a risk form that knows the relationship.

## §2. Book primitive + equity invariant

Every book in the synome — Genbook, Primebook, Halobook, Riskbook, Exobook — is the same 6-tuple: `(assets, tranches, equity-tranche, rules, state, frame)`. Tranches' notional may be **rule-determined** (callable bonds, conversions, step-ups, triggered subordination).

**Equity invariant:** every book has exactly one equity tranche (most-junior, first-loss); book solvent iff equity > 0; equity → 0 triggers a defined unwind. Every book class needs a documented **equity-feed mechanism** (synserv computation / chain-read primitive / `attest-data-beacon` / mixed). Rules + state make books **financial state machines** — synart code that synserv runs; every warden can re-derive state from input atoms.

**Bankruptcy remoteness sits at the Riskbook level.** Within a Riskbook, fates are linked; across Riskbooks, fates are independent. **No netting across Riskbooks.**

## §3. Tranching + waterfall

Tranches: ordered claims `(seniority, holder, notional, denomination)`; loss waterfalls junior-to-senior. **New vocabulary:** **Exoasset** = terminal external asset (ETH/USDC/T-bills); **Exoliab** = tranche claim held by an external party (borrower equity, sponsor retention). The synome doesn't model the exoliab holder's full balance sheet — just cushion size protecting senior claims. **Cushion revaluation under stress** is required: if borrower equity is denominated in the same crashing asset, stress both consistently. Tranche rights: redemption / liquidation acceleration → P; transfer → T.

**Gap risk and FRTB drawdown unified.** Both were always asset-liquidity stress through structure. Unified term `forced-loss-capital(asset-type)` reads from the asset's canonical liquidity profile (§9), same math whether holder is direct, senior tranche, or junior tranche. Old `collateralized-lending-risk.md` and `market-risk-frtb.md` archived.

| Position | New framing |
|---|---|
| Sparklend USD vs ETH | Senior tranche of perpetual ETH-collateralized exobook |
| Crypto NFAT | Senior tranche of fixed-term BTC/ETH/stETH exobook |
| JAAA | Senior tranche of CLO exobook with deep junior cushion |
| Pure ETH | Terminal exoasset, no tranche |

## §4. Currency frame vs instrument

**Frame** = abstract unit of account (USD/EUR/BTC). **Instrument** = concrete realization with stress profile relative to frame. Three currency kinds: `unit-of-account` (no stress, abstract); `stablecoin-proxy` (depeg distribution: USDS/USDC/USDT/EURC); `native-volatile-asset` (volatility via oracle: BTC own frame, ETH USD-pair). Identity in `&core.registry.currency`; stress in `&core.framework.currency-stress` (split: identity rare, stress recalibrated).

**Frame inherits top-down** from the Generator: Genbook → Primebook → Halobook → Riskbook all USD-frame (USDS Generator → USD). **Riskbook is the translation layer** — accepts external assets in native denoms, applies depeg/FX stress, issues frame-pure units upward. **Multi-generator architecturally ready** (same machinery handles cross-currency translation today and cross-Generator translation later via `(serves-generator $prime $generator)` registry); v1 single-Generator. Tranche-frame mismatches deferred to v2+.

## §5. Four-layer stack

| Layer | Role |
|---|---|
| **Riskbook** | Unit of regulation. Matched-form-or-CRR-100. Default risk, currency translation, tactical hedging. Bankruptcy-remoteness boundary. |
| **Halobook** | Bundle exposure structure (rollover/lockup/options). Owns P + T. Aggregates Riskbook units with **no netting**. Never modifies default risk. |
| **Primebook** | Composes 5 typed sub-books + unmatched. Routes by structural eligibility. Issues **single Primeunit** upward. |
| **Genbook** | Holds Primeunits; system-wide concentration caps; backs USDS. Equity holder = Sky reserves. |

**Riskbook risk-form catalog** (`&core.framework.risk.forms`) is governance's primary risk-shaping lever. A risk form = synlang `composition-constraints` predicate (a *type* constraint, not a sanity check) + `equation-m2m`/`equation-htm` + `resolution-tier` (math / simulation / heuristic). Halos compete on **sourcing / composing / innovating**.

**Tactical hedging at Riskbook layer:** `abf-with-cds-cover`, `delta-neutral-eth-spot-perp`, convertible+short-stock — both legs in one Riskbook; the risk-form equation knows the relationship. Hedge legs in *different* Riskbooks get no relief — bankruptcy remoteness forbids cross-Riskbook netting.

**Halobook category** describes bundle exposure structure — what happens to per-position risks over the bundle's lifetime. Affects spread/rate/liquidity through structural features (rollover compounds spread duration; lockups worsen P; etc.). V1 catalog: `nfat-crypto-lending-fixed-term` only — passthrough, lockup-until-maturity, transfer=null.

## §6. Five typed sub-books

Sub-books are **risk-coverage contracts** declaring which non-default risks they cover:

| Sub-book | Default | Spread | Rate | Liquidity | Notes |
|---|---|---|---|---|---|
| `ascbook` | Capital | Capital | n/a | The product (must hold) | Peg-defense readiness |
| `tradingbook` | Capital | Forced-loss | Hedge or rate-cap | Forced-loss (FRTB) | Static; needs `(U AND P) OR T` |
| `termbook` | Capital | **Covered** | **Covered** | **Covered** | tUSDS YT match (Phase 2+; no positions in v1) |
| `structbook` | Capital | **Covered** | Capital required (v1: 0) | **Covered** | **Only active sub-book in v1** |
| `hedgebook` | Capital | Hedge-adj | Hedge-adj | Hedge-adj | Cross-position portfolio hedges |
| Unmatched | Capital | Forced-loss | Forced-loss | Forced-loss | Same as tradingbook minus FRTB-eligibility |

**Optimization-shaped** (`structbook`, `termbook`, `hedgebook`) blend matched/hedged and unmatched smoothly: `position CRR = matched × covered + unmatched × max(RW, forced-loss)`. No binary "treatment-coverage-failure" — capital rises continuously. Default optimization: greedy descending (longest TTM → longest bucket); Prime can override.

**Static-treatment** (`tradingbook`, `ascbook`, unmatched): uniform treatment, no allocation choice.

**Routing:** declarative by structural eligibility; pick most-capital-efficient eligible sub-book. **Treatment switches free** subject to structural prerequisites (can't fake `termbook` eligibility without an actual tUSDS-matched liability). No motivational scrutiny (would defeat private cognition). **Crash oracle** (Phase 2+, schema-only in v1) suspends switches in declared crash windows. Primebook still **issues a single Primeunit upward** — sub-books are internal composition.

## §7. Hedgebook vs Riskbook hedging

**Riskbook (tactical):** specific position + specific hedge in one strategy (ABF + matching CDS; delta-neutral spot/perp). **Hedgebook (portfolio):** hedge instrument at Prime level spanning many Halobooks (index-CDS over diverse credit; Circle-CDS over USDC concentration).

Hedgebook is the **first place cross-Halobook composition happens** in capital math. Hedge instruments held at Prime level; Hedgebook is read-only at Halobook level (observes exposures); does NOT merge bankruptcy estates — capital benefit through pricing, not legal merger. Hedgebook issues no separate unit.

**Hedge effectiveness is a quantified residual computation, not magic.** Equation explicitly models failure modes: counterparty risk (× survival prob), basis (× correlation), liquidity (closing slippage), tenor mismatch (roll cost / stub). Clean hedge → near-zero residual; sloppy → mostly capitalized. Hedgebook category catalog is governance-curated default-deny.

## §8. Projection models

Substrate handles direct holdings, tranche structures, linear claims; **anything more complex** uses a risk-form-declared **projection function**: `project: (position, scenario) → stress-loss-number`. Implementations: analytical (Black-Scholes), Monte Carlo, lattice, parametric, ML-based.

**Projection-model risk is its own capital dimension** — `model-uncertainty-haircut` is a form-level governance multiplier. Indicative: BS for vanilla ~0%; lattice American 0–5%; Heston/local-vol 5–10%; MC path-dependent 5–15%; novel parametric 20–30%; ML-based 30–50%; no projection → CRR 100%.

Rules (§2) and projections are **complementary** — a vanilla call has both a rule (max(spot−strike,0) at expiry) and a BS projection. Framework explicitly admits epistemic limits (multi-agent strategic equilibrium, subjective contracts, novel risk modes, recursive market impact); answer = conservative defaults + willingness to use CRR 100% + governance-paced expansion.

## §9. Asset classification + SPTP

Every terminal exoasset has **one canonical risk profile** in `&core.framework.risk.asset-profiles`. Load-bearing: every risk-form equation reads it (no inlining). Risk-type tuple: fundamental risk weight, drawdown distribution per scenario, slippage model, SPTP, correlations, currency dimension.

**Asset-level liquidity profile** = drawdown + slippage + correlations. The primitive that the unified `forced-loss-capital` math runs against.

**Stressed Pull-to-Par (SPTP)** matters because the scenario where duration matters *is* the stress scenario. `SPTP = Normal Pull-to-Par × Stress Modifier`. Empirical: JAAA 1.4× (2008-09 prepay slowdown 28%→9-15%); MBS 1.2-1.5×; T-bills/corporates 1.0×. Refinement: split into **credit-spread duration** (covered by `termbook` and `structbook`) vs **rate duration** (only `termbook`). ETH SPTP = infinite; Sparklend = none (perpetual).

## §10. Duration model (demand side)

Lives in the Generator's entart (`&entity.generator.usge.structural-demand`). Determines how much USDS liability is sticky enough to support matched assets at each duration tier.

**Lindy method:** for each USDS lot, expected remaining holding = current age × Lindy factor × conservative haircut (0.5–0.7×).

**101 buckets × 15 days each.** Bucket 84 = 1,260 days (JAAA); bucket 100 = 1,500+ days (structural/permanent base). Liability rounds DOWN; asset rounds UP (both conservative).

**Structural Maximum Caps: double-exponential** calibrated to bank-run empirics:
```
Cap(t) = A·e^(−λ₁t) + B·e^(−λ₂t)
A=10%, λ₁=0.35 (hot-money, half-life 1.0mo); B=0.70%, λ₂=0.0175 (sticky, half-life 19.8mo)
```
Calibrated to SVB / First Republic / Credit Suisse / Basel III LCR/NSFR / MMF crises. Targets: 75% remaining at 1mo, 55% at 3mo, 35% at 12mo, 10% at 50+mo.

**Two-layer capacity:** Layer 1 daily Lindy; Layer 2 apply structural caps top-down with overflow cascading downward. **Cumulative capacity at bucket N** = Σ effective capacity for buckets ≥ N.

**Allocation:** Phase 2+ = daily Lindy + daily Duration auctions + tug-of-war with own-bucket priority emergent (distance 0). **Phase 1 carve-out:** manual governance-set capacity, equal-split among Star Primes, fake-auction. Real-time lot-age tracking is an open question.

## §11. Matching: credit-spread vs rate

**Foundational distinction:** duration matching protects against **credit-spread risk**, not interest-rate risk. Credit spreads mean-revert (OU process; 2008 GFC ~6mo, COVID 2020 ~3wk after Fed); SSR stays flat / falls (flight to quality). Rate regimes shift over decades (Volcker; 15%→0% across 1980s-2010s); SSR rises → permanent negative carry on fixed-rate.

`termbook` covers spread AND rate (matched fixed/fixed via tUSDS YT — but tUSDS market is Phase 2+; schema only). `structbook` covers spread + liquidity but NOT rate (variable-rate structural demand) — Prime hedges or holds rate-hedge capital. **V1 carves out** rate-hedge capital for `structbook`.

Rate-hedge capital: `Fixed Exposure × Duration × Expected Rate Volatility × Confidence Multiplier` (additive to credit risk capital). **Smooth optimization**: capacity shrinks → blend shifts → CRR rises continuously, replacing binary matched/unmatched flags.

## §12. Concentration: two levels

**Primebook** (within a Prime's portfolio across its Halobooks; Prime can rebalance) and **Genbook** (system-wide across all Primes serving a Generator; Sky-systemic). Same mechanism: governance defines **Correlation Categories** (CLOs, US-based, real-estate, ETH-collateral) — non-mutually-exclusive; cap as % of relevant scope; excess gets **100% CRR**; **no stacking** (max-binding-category, not sum); **capacity rights ("grandfathered slices")** prevent new deployers from instantly displacing incumbents — `alloc[p][c]` shifts gradually toward Primes paying penalties; normalization period `T = max(asset_SPTP, 3 months)`.

Matched portion measured by notional/duration-value; unmatched by MTM.

**Cap calibration** via scenario engine: `L(c, s)` = stressed loss per $1 of category-c exposure under scenario s; `B(s)` = max portfolio loss. Method A (independent): `cap[c] = min_s B(s)/L(c,s)`. Method B (joint): `Σ_c cap[c]·L(c,s) ≤ B(s)`. Choice open.

**V1:** Genbook-level only with manual governance-set caps. Primebook-level deferred to Phase 3+. **Gross-of-hedge** in v1 (a Prime with $1B exposure + $900M index-CDS still has $1B *concentration* exposure; only $100M *capital* exposure).

## §13. Capital formula → TRRC

Per-position flow: (1) Riskbook risk-form match → equation gives per-position CRR (no match → CRR 100%). (2) Project asset stress through structure (waterfall / projection model / direct read). (3) Halobook exposure-structure adjustment; generate U/P/T. (4) Sub-book routing by structural eligibility (most capital-efficient). (5) Sub-book capital math (optimization blends or static). (6) Concentration excess penalty (100% CRR on excess; max-binding, not stacked).

```
TRRC[p] = Σ Position Capital + Σ Excess Capital
ER[p]   = TRRC[p] / TRC[p]    target ≤ 0.90
```

Per-sub-book formulas:
- `ascbook`: `size × max(RW, credit-spread-stress)`
- `tradingbook` / unmatched: `size × max(RW, forced-loss)`
- `termbook`: `matched × RW + unmatched × max(RW, forced-loss)` (3 risks covered on matched)
- `structbook`: termbook + `matched × rate-hedge-capital` (v1: 0)
- `hedgebook`: `hedged × hedge-residual + unhedged × natural-sub-book-CRR`

**TRC funding** spans JRC + EJRC + SRC tiers with ingression-adjusted recognition — see `accounting/capital-stack.md`. Capital committed but not yet ingressed counts at a discount.

**NFAT book-phase note:** per-NFAT CRR varies by phase (Filling = low, Deploying = high due to information opacity, At Rest = medium based on attested risk; CRR rises if re-attestation missed). Captured via the Riskbook risk-form equation reading book phase from synart state. Numeric calibration pending.

## §14. Operational Risk Capital (parallel track)

Different threat class from portfolio risk capital:

| Pool | Covers | Sized by | Posted by |
|---|---|---|---|
| Portfolio Risk Capital | Market / credit / duration / liquidity loss | CRR per §13 | Prime (JRC + EJRC + SRC) |
| **ORC** | Damage from compromised guardian | Rate Limit × TTS | Guardian (Accordant to Prime) |

Both required, additively.

**Phase 1 (pre-sentinel):** `ORC ≥ IRL × Accumulation × N = $100K × 1.0625 × N` (SORL=25%, TTS~24h). At N=10: ~$1.06M per guardian. Covers Type 1 (direct extraction); Type 2 (slippage grinding) has higher marginal harm but ~10% extraction rate.

**Sentinel-era:** `ORC ≥ Rate Limit × TTS`. Rate Limit = PAU's `maxAmount` (instantaneous buffer). TTS = Time to Shutdown — worst-case for wardens to detect+halt rogue Baseline. Example: $100M/day × 4h = $16.7M.

**Warden economics:** better wardens → lower TTS → lower ORC. Indicative: basic 1-warden manual TTS=24h ($100M ORC); standard 2-warden automated TTS=4h ($16.7M); premium 3+ diverse certified TTS=1h ($4.2M).

**Guardian Accord** parameterizes Scope / Rate limits / ORC / TTS / Penalties. Phase 1 implicit (GovOps under Core Council); sentinel era explicit smart contracts (Streaming Accord = specialized form). **Folio ORC:** automated folios get full TTS-based framework; **principal-control folios** have no TTS, no wardens, no ORC charge — bounded by rate limits + PAU architecture alone.

**PIV trading risk** is distinct from ORC — managed via on-chain enforcement (Delegated Intent Policy, per-window caps, EIP-1271 validation, vault balance isolation). See `trading/sky-intents.md`.

## §15. Monitoring + sentinel integration

Metrics: solvency (System Collateral Ratio, Surplus Buffer with **ABC target 1.5% post-Genesis, $125M Genesis interim** per TMF), liquidity, concentration, stress (VaR / cascades / oracle failure), operational, and new layered metrics — **per-sub-book CRR**, **equity-proximity** (real-time alert when any book's equity approaches zero), **treatment-switch frequency** (gaming detection).

Stress testing: scenarios + historical (Mar 2020 / May 2021 / Terra-Luna / FTX) + Monte Carlo + reverse stress. Severity Info → Warning → Alert → Critical. Path: automated → sentinel formation → human → governance → emergency. **Encumbrance Ratio enforcement** at ≤ 0.90 governance-pending; likely: rate-limit reduction, deployment freeze, escalating deleveraging timeline. Calibration must avoid pro-cyclical forced selling.

**Sentinel integration:** the framework is the calculation set sentinels and high-authority action beacons perform.
- **synserv verification (in-space calculation)** runs CRR / TRRC / TRC / ER as synart-resolved code against current input atoms. No off-loop opaque compute. Replaces deprecated `lpla-checker`.
- **`baseline-{prime}` (relay) / `warden-{prime}-{op}` (relay)** (Prime-side, Phase 9-10) — execution + independent halt; paired with `stream-{prime}-{actor}` (sentinel)
- **`baseline-{folio}` / `warden-{folio}-{op}` (relay) + `stream-{folio}-{actor}` (sentinel) / `principal-{owner}` (sentinel)** — automated folios full formation; principal-control rate-limit-only
- **`lcts-{halo}` / `nfat-{halo}` / `amm-{halo}` (relay)** — Halo-side high-authority action beacons (deterministic keepers)

**Default-deny CRR 100%** is the foundational pattern: Riskbook without category → 100%; exobook without category → 100%; recursion beyond `max-recursion-depth` → 100%; position type without projection model → 100%; hedge without Hedgebook category → 100%; asset class without full risk-type tuple → 100%. Same pattern as elsewhere in the synome (verb whitelists, recipe catalogs, runtime registry, telseed catalog). Innovation flows through **governance crystallization**, not ad-hoc favorable treatment.

---

## Key vocabulary

- **TRRC / TRC / ER** — Total Required Risk Capital / Total Risk Capital / TRRC÷TRC, target ≤0.90
- **6-tuple book** — `(assets, tranches, equity-tranche, rules, state, frame)`; universal
- **Equity invariant** — every book has exactly one equity tranche; equity→0 triggers unwind
- **Exoasset / Exoliab** — terminal external asset / external-party tranche claim (NEW vocabulary)
- **forced-loss-capital(asset-type)** — unified term replacing "gap risk" + "FRTB drawdown"
- **U / P / T** — Underlying-unwind / Permitted-unwind / Transfer-market liquidity dimensions
- **Frame vs Instrument** — abstract unit-of-account vs concrete realization with stress profile
- **Riskbook risk form** — composition-constraints + equation-m2m/htm + resolution-tier in `&core.framework.risk.forms`
- **Default-deny CRR 100%** — anything unmodeled → 100% CRR; forces governance crystallization
- **Risk-coverage contract** — a sub-book's declaration of which non-default risks it covers
- **ascbook / tradingbook / termbook / structbook / hedgebook** — the five typed sub-books
- **Optimization-shaped sub-book** — structbook/termbook/hedgebook; smooth matched+unmatched blend
- **Tactical hedge vs Hedgebook hedge** — within-Riskbook strategy vs portfolio overlay
- **Hedge residual CRR** — after-hedge exposure modeling counterparty/basis/closing/tenor failure
- **Projection model** — `(position, scenario) → stress-loss-number` for non-tranchable positions
- **Model-uncertainty haircut** — form-level multiplier for projection epistemics
- **Asset-level liquidity profile** — drawdown + slippage + correlations; load-bearing primitive
- **SPTP** — Stressed Pull-to-Par (split: credit-spread duration vs rate duration)
- **Lindy Duration Model** — per-lot expected remaining holding = age × Lindy × haircut
- **Duration buckets (101 × 15d)** — bucket 84 = 1,260d (JAAA); bucket 100 = 1,500+d
- **Structural caps (double-exponential)** — A·e^(−λ₁t)+B·e^(−λ₂t); bank-run-empirics-calibrated
- **Cumulative capacity** — higher-bucket capacity satisfies lower-bucket requirements
- **Concentration category / capacity rights** — governance-defined caps with grandfathered slices shifting to penalty-payers over T = max(SPTP, 3mo)
- **Method A / Method B** — independent worst-case caps vs joint-optimized caps
- **Gross-of-hedge / Net-of-hedge** — concentration counts raw vs after-hedge (v1 = gross)
- **ORC** — Operational Risk Capital — Rate Limit × TTS, posted by Guardian
- **TTS / IRL / SORL** — Time to Shutdown; Initial Rate Limit ($100K) / Second-Order RL (25%/18h)
- **Guardian Accord** — Scope / rate limits / ORC / TTS / penalties between Prime and guardian
- **Crash oracle** — Phase 2+; suspends sub-book treatment switches in declared crash windows
- **NFAT book-phase** — Filling / Deploying / At Rest CRR variation in Riskbook risk-form equation

## Cross-references

- `accounting/capital-stack.md` — funds TRRC: JRC/EJRC/SRC tiers, ingression curves
- `accounting/duration-allocation.md` — tug-of-war + OSRC + Duration auctions feeding `structbook`/`termbook`
- `accounting/settlement-cycle.md` — synserv heartbeat + real-time ER + 5-step closure
- `accounting/treasury-management.md` — TMF (canonical home post-migration)
- `roadmap/phase-1-spaces.md` — Phase 1 carve-outs (single-form black box, manual structural-demand, no rate-hedge for `structbook`, no crash oracle); worked v1 crypto-collateralized lending end-to-end
- `roadmap/v1-principles.md` — 13 v1 principles governing what's deferred / carved-out / governance-set vs target architecture
- `roadmap/asc-transition.md` — ASC track (peg-defense liquidity; ALM rental; PSM transition)
- `synomic-entities/prime.md`, `synomic-entities/halo*.md` — entities operating these books
- `smart-contracts/rate-limit-attacks.md` — Phase 1 ORC attack model; IRL/SORL derivation; Type 1/Type 2 harm
- `smart-contracts/configurator-unit.md` — canonical SORL parameters
- `trading/sentinel-network.md` — TTS determinants, warden economics, Streaming Accords
- `trading/sky-intents.md` — PIV trading risk via Delegated Intent Policy
- `macrosynomics/beacon-framework.md` — beacon taxonomy + in-space calculation; canonical home for `lpla-checker` collapse
- `noemar-synlang/listener-loops.md` — Phase 1 implementation sketch for synserv-resolved calculation
- `noemar-synlang/risk-framework.md` — existing four-book taxonomy (pending Phase-2 trim)

## File map

| File | What's in it that the summary doesn't have |
|---|---|
| `risk-decomposition.md` | Justification for these five types; full risk-type × sub-book coverage matrix row-by-row |
| `book-primitive.md` | Synlang for rule shapes (time/oracle/path-dependent); equity-feed mechanism table; worked v1 example → `roadmap/phase-1-spaces.md` |
| `tranching.md` | Worked Sparklend ETH-loan numerics; cushion-revaluation edge case; tranche-rights synlang |
| `currency-frame.md` | Full currency-def synlang; 1:1-lock calibration risk; tranche-frame mismatch deferral |
| `riskbook-layer.md` | Synlang risk-form-defs (`pure-eth-holding`, `abf-with-cds-cover`, `crypto-collateralized-USD-lending`); Halo three-skill competition; worked v1 example → `roadmap/phase-1-spaces.md`; v1 carve-outs → `roadmap/v1-principles.md` |
| `halobook-layer.md` | Halobook structural-feature × risk-type effect table; full v1 `nfat-crypto-lending-fixed-term` synlang; v1 example → `roadmap/phase-1-spaces.md` |
| `primebook-composition.md` | Optimization-preference modes; full crash-oracle synlang sketch; routing rule |
| `hedgebook.md` | Full `hedge-residual-crr` synlang with all four failure modes; `credit-portfolio-with-index-cds-overlay` sketch; USDC depeg-hedge pattern |
| `projection-models.md` | Position-types × projection-model-types taxonomy; epistemic-limits enumeration |
| `asset-classification.md` | `asset-form` synlang for ETH and JAAA; SPTP table per asset class with historical basis; per-data-space atom locations |
| `correlation-framework.md` | Reallocation rule; Method A vs B equations; outputs/reporting schema |
| `duration-model.md` | Bucket cumulative table (30d/90d/180d/360d/720d/1080d/1260d/1500+d %-gone); empirical bank-run sources; daily cycle |
| `matching.md` | Empirical defenses of mean-reversion vs regime-shift; rate-hedge capital worked example; per-asset-class matching applicability |
| `capital-formula.md` | Per-sub-book capital formulas with synlang detail; concentration-excess no-stacking equation; ingression mechanism; worked v1 example → `roadmap/phase-1-spaces.md`; v1 principles → `roadmap/v1-principles.md` |
| `asset-type-treatment.md` | Worked treatments per asset class (Direct ETH/BTC, Sparklend, NFAT, JAAA, T-bills/MMF, vanilla options, ABF); old-vs-new framing comparison; worked v1 example → `roadmap/phase-1-spaces.md` |
| `operational-risk-capital.md` | Phase 1 vs sentinel-era formulas; warden-quality table; Guardian Accord parameters; folio ORC distinction; PIV-vs-ORC boundary |
| `risk-monitoring.md` | Complete metric categories; stress testing types; severity-level table; ER-enforcement governance proposal |
| `sentinel-integration.md` | Per-beacon role table; full key-metrics table |
| `open-questions.md` | Living deferrals — Q24 attestor schema, Q26 v1 privacy buckets, Q27 crypto stress calibration, correlation framework specifics, USDS lot-age tracking |

