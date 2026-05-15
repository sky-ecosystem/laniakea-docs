# Accounting

**Status:** Mixed. Settlement architecture and capital-stack math are target-architecture spec with explicit Phase 1 carve-outs (monthly manual settlement, sudo-set "fake auction", fixed SBE, exsynTRRC for legacy halos). TMF, Entity Fees, DR/LDR are live. Pioneer Star System available. MDC speculative. Current legacy operational reality (legacy core vaults, PSM, legacy RWA, CCB reclass, current SBE config) is no longer documented in the corpus — treated as out-of-band knowledge during transition.
**Canonical home:** `laniakea-docs/accounting/`

---

## TL;DR

The funding side of the capital math. Risk Framework decides *what* capital is required (TRRC); accounting defines *how* capital is sourced, ingressed, settled, distributed. Five operational arteries: (1) **settlement cycle** — synserv heartbeat publishing real-time ER per Prime continuously plus an epoch-boundary 5-step closure → global aggregation into `&core.settlement`; (2) **capital stack** — IJRC/EJRC/SRC/MDC tranches ingressed through a universal flat-plus-quarter-circle curve, capped by Prime token's worst-of-observed market metrics, temporarily backstopped by Genesis Capital with $125M ABC floor; (3) **TMF** — 5-step sequential revenue waterfall (S&M → ABC → Fortification → Smart Burn → Staking) scaled by Net Revenue Ratio; (4) **Synomic Entity fees** — unified rule for tokenized entities only: 5% Creation + 50 bps/yr Upkeep on **token market cap** (conservative-priced) paid in own tokens, plus Cross-Entity Upkeep Rebate; tokenless types (Folio, Core, Oracle, Sequencer) pay neither; (5) **DR/LDR/Pioneer** — tiered USDS-adoption rewards, sticky-demand splits, 3-year per-chain Star Prime privileges. **Cadence is a governance fact**, not architecture: monthly Phase 1 → daily Phase 3+; the synlang doesn't change.

## Section map

| § | Topic |
|---|---|
| 1 | Settlement cycle |
| 2 | Capital stack |
| 3 | Genesis Capital + insolvency defense |
| 4 | TMF |
| 5 | Synomic Entity fees |
| 6 | DR / LDR / Pioneer Star System |
| 7 | Isolated deployment + MDC |
| 8 | Duration allocation |
| 9 | Legacy reality (cross-reference) |

---

## §1 Settlement cycle

`accounting/settlement-cycle.md`. Three concurrent activities: real-time ER emission (per heartbeat, in `&entity.prime.{id}.primebook`), per-Prime settlement closure (per epoch boundary, in `&entity.prime.{id}.root`), global aggregation (in `&core.settlement`). ER is **derived, not stored** — `(prime-er $prime $value $timestamp)` re-emitted each heartbeat from current `insynTRRC + exsynTRRC` and `prime-trc`. Continuous emission is the Phase 1 deliverable.

**5-step per-Prime computation:**
1. **Max debt fees** — `time-weighted-debt × base-rate`.
2. **Idle USDS/DAI reimbursement** — scatter-gather over `idle-position` × Base Rate (cancels Step 1 double-count).
3. **sUSDS spread profit** — same scatter-gather restricted to sUSDS, × Savings-Rate-spread.
4. **Sky Direct shortfall** — `max(0, exposure × base-rate − actual-profit)`. Asymmetric: Prime made whole on downside, Sky takes all upside.
5. **Net amount** — `(debt + penalty + synart-resource-fee) − (idle + sUSDS + Sky-Direct)`.

**Two-phase closure.** Per-Prime parallel against own entart, then scatter-gather aggregation into `&core.settlement` writing `epoch-sky-net`, `epoch-treasury`, `epoch-ecosystem`, `epoch-burn`, `epoch-staking` (TMF outputs).

**Cadence:** monthly in Phase 1 (operated out-of-band), daily at Phase 3+. The atom-driven cadence parameter and the Space it lives in are TBD; synlang body unchanged across the cadence transition.

**Penalty.** Per-epoch breach = `max(0, max-ER − covenant)`; covenant ER ≤ 0.90; penalty = `breach × penalty-rate × available-capital / 10000`. Phase 1 detects in synlang on live ER stream; settlement actions remain manual until Phase 2+.

**Synart resource fee.** Per-atom write / per-day retention / per-byte replication / per-match query. Parsimony emergent: 10× event rate → 10× fee.

**Rolling two-epoch retention.** Synart is the canonical real-time event log but **not** a permanent event store. Each entart Space holds the most-recently-settled epoch alongside the currently-streaming one. Pruning runs at the *next* settlement boundary: when epoch N settles, epoch N−1 prunes. Two epochs (not one) gives wardens, verifier embs, and dispute resolution one full epoch's late-re-derivation budget without inflating replication bandwidth. On-chain transactions are the long-term historical record; long-term forensics requires running an `archive` loop or reading on-chain. Anything that must persist beyond an epoch must be promoted to a settlement-tier atom or written to an out-of-band archive before pruning. This bounds synart resource cost by retention, not by total history.

**Growth Staking distribution.** `epoch-staking-rewards-paid` and `epoch-staking-rewards-forfeited` emitted into `&core.settlement`; forfeitures re-enter TMF aggregation. Inactive in Phase 1.

## §2 Capital stack

`accounting/capital-stack.md`.

```
IJRC + EJRC   (pari passu by nominal)         ← going-concern first loss
Prime Token   (forced inflation)              ← recapitalization
─────────────────────────────── liquidation threshold
MDC           (subordinated in liquidation)   ← residual claim
SRC           (senior in liquidation)         ← senior claim
```

Going-concern: losses → JRC by nominal → if exhausted, Prime Token inflated → if inflation can't cover, liquidate. **Ingression decides leverage; nominal absorbs losses.**

**Universal ingression curve:** flat (rate 1.0) up to `anchor`, quarter-circle `√(1 − ((x − anchor)/(max − anchor))²)` to zero at `max`. 3:1 max:anchor. Smooth tangent at anchor; vertical at max. Max effective = `anchor + (max − anchor) × π/4`.

| Curve | Anchor | Max | Theoretical max effective |
|---|---|---|---|
| SRC | 1.5 × eff JRC | 4.5 × eff JRC | ~3.86 × JRC |
| MC cap (total RC) | 5 × eff MC | 15 × eff MC | ~12.85 × MC |
| EJRC | `1 × IJRC × syn × dur` | `3 × IJRC × syn × dur` | varies |

**EJRC quality dimensions.** Synomic = 2× / non-synomic = 1×; duration multiplier = `1 + months/24` for months ≥ 3, else 1; max useful = 24 months.

EJRC types: **Normie TEJRC** (LCTS, non-synomic, zero-duration → 1×/3×); **non-synomic duration** (bespoke, SubProxy + ecosystem accord); **synomic duration** (between synomic agents).

**Duration mechanics.** Perpetual-until-called or fixed-term. Uningression delay (24/12/6/3 mo) determines load — load constant at agreed delay's level. Egressor instant exit never allowed; Prime instant release only if pre-negotiated.

**MC-based total RC cap.** Effective MC = **min** across actual MC, weekly/monthly/quarterly ADV (×100/125/167), monthly/quarterly/yearly turnover (×29/15/10). Worst-of-observed catches illiquid (high MC, low volume), wash trading (high volume, low turnover), unvalued (high turnover, low MC). Future: independent-trader-registry. Phase 1: oracle-fed exsyn.

**Capital adequacy invariant:** `TRRC ≤ TRC`, `ER = TRRC / TRC ≤ 0.90`. Breach drives §1 penalty.

**ORC and ASC** sit on parallel tracks (Rate Limit × TTS for ORC; ascbook routing for ASC) — capital-adequacy-relevant but evaluated alongside, not inside, portfolio TRC. See `risk-framework/operational-risk-capital.md` and `risk-framework/asc.md`.

## §3 Genesis Capital + insolvency defense

Temporary bootstrap mechanism (2026–2027). **Allocated Genesis Capital** vs **Aggregate Backstop Capital (ABC)** = `Total − Allocated`. Phase 1 ABC floor **$125M**; long-term post-Genesis target **1.5% of USDS supply**. Retention: **25%** of net revenue after S&M every monthly settlement until target.

**Phase-out:** each Genesis Agent with launched token having ≥$10M ADV phases out $1M/month if ABC ≥ $50M, +$1M per $10M of ABC above $50M. Total Genesis Capital monotonically decreasing.

**Nine Genesis Agents:** Five Star Primes (Spark, Grove, Keel, Star 4, Star 5) + Institutional Prime (Obex) + three Genesis Guardian Agents ($25M each, distinct from governance Guardians). No others.

**Guardian capital:** $25M each; $20M ring-fenced as Core Council and GovOps Support Buffer (must be spent on Sky Ecosystem development before internal capital used for buybacks/staking; dual-use as ORC for Guardian Accords until then). Goals: Core Council off 21% S&M; bootstrap GovOps without Accord Fees during Genesis.

**Insolvency defense — 4-level (simplification of whitepaper's 7-step):**
1. ABC absorbs first
2. SKY token inflation
3. Genesis Capital reclaim (Genesis Agent token holders airdropped new SKY supply if reclaim sufficient)
4. USDS haircut (USDS holders airdropped new SKY supply to recover peg)

7→4 mapping: FLC + JRC + Agent Token Inflation + SRC Pool collapse to Level 1; SKY Inflation → Level 2; Genesis Haircut → Level 3; USDS Peg Adjustment → Level 4. Canonical 7-step in `inactive/pre-synlang/whitepaper/sky-whitepaper.md` Part 6.

## §4 Treasury Management Function

`accounting/treasury-management.md`. 5-step sequential waterfall over net revenue, USDS-denominated.

**Net Revenue Ratio (NRR):** `nrr = revenue / (revenue + 3B)` for revenue < 1T; capped at 1.0. Hyperbolic; prevents quadratic drag on staking at low scale. (200M → 0.0625; 3B → 0.5; 10B → 0.77; 100B → 0.97.)

| Step | Rate |
|---|---|
| 1. S&M | 21% Genesis / 4–10% post-Genesis (10% **permanent ceiling**) |
| 2. ABC | Three sub-phases: Safety Floor (`max(0.25, fill_factor × 0.5 × max(nrr,0.10)) × step1_result` if buffer < $125M); Filling (dynamic rate); Hard Cap (0% if ≥ target) |
| 3. Fortification Conserver | `0.20 × nrr × step2_result` |
| 4. SBE | `0.20 × nrr × step3_result` |
| 5. Staking | 100% remainder |

**Current SBE temporary config:** Steps 4+5 unified → fixed ~$300K/day SKY buyback distributed to stakers. Activates dynamic `Burn Rate = (1 − MC/TMC) × 50%` once SBE BEAM ships (Phase 2+). Counter-cyclical.

## §5 Synomic Entity fees

Live (`accounting/entity-fees.md`).

**Unified rule.** Any Synomic Entity with active governance tokens pays a single uniform fee structure; tokenless entities pay neither fee. Same rate, same mechanics, same denomination across every tokenized entity type.

| Mechanism | Direction | Rate | Trigger |
|---|---|---|---|
| Entity Creation Fee | Sky receives entity tokens | **5%** of all governance tokens issued | Any issuance: genesis, distribution, fundraising, restructuring |
| Entity Upkeep Fee | Entity pays Sky in own tokens | **50 bps/yr** of entity token **market cap** | Continuous; settled at boundary |
| Cross-Entity Upkeep Rebate | Reduces upkeep owed | Proportional to other entities' tokens held, priced **conservatively** | Continuous |

**Supply → market cap shift.** Upkeep is now assessed against the entity's governance-token **market cap** (using the same conservative-pricing methodology as the rebate), not total token supply. Conservative pricing protects Sky against settlement-window manipulation in either direction; the spread between conservative and live mid accrues to Sky as additional revenue, mirroring the rebate side.

**Token-status mapping** (canonical per `synomic-entities/README.md`):

- **Tokenized — pay both fees:** Generator, Prime, Guardian, **Pylon Entity** (rank-2 broker-dealer analog with capital-weighted governance token), governed Halo.
- **Tokenless — pay neither:** Folio, **Core Entity** (single Core-Council vehicle covering both legacy-asset management and crisis-wrapper roles), **Oracle Entity** (domain-specific data provider), **Sequencer Entity** (orderbook sequencer / matcher and Ring host; no collateral, trust enforced by revocability rather than slashing), minimal/simple Halo.

Tokenless entities do not appear in Growth Staking valuations and generate no Entity Creation or Upkeep revenue for Sky Core. Where they earn their keep through other channels (usage fees, maker-taker spreads), those are specified per-type in the entity's own document, independent of the unified fee rule.

**Rebate:** `rebate_credit = holdings_value (conservative) × 0.005`; `upkeep_after = max(0, gross_upkeep − rebate_credit)`. Cannot go negative. Conservative pricing extracts spread for Sky while incentivizing cross-entity holdings → ecosystem cohesion + Growth Staking alignment (cross-holdings double as growth assets).

**Denomination.** Both fees paid in the entity's own governance tokens, not USDS. Sky Core can hold, stake, use the holdings to claim its own Cross-Entity Upkeep Rebates, or sell over time.

**Cadence.** Upkeep accrues continuously, realized at each settlement boundary (monthly Phase 1 → daily Phase 2+). Creation Fees realized at the issuance event itself — the 5% slice mints alongside the rest of the issuance and routes to Sky Core in the same transaction.

For Type 1 Restructure: 5% deducted from creator's allocation (95/5). See `synomic-entities/creation-restructuring.md`.

**Open questions** (down to two): conservative-pricing oracle source/window/aggregation rule (finalized at framework level, not yet pinned to a specific implementation); rebate eligibility for tokenless holders (e.g. Core Entity holding Prime tokens during a busted-prime wrap has no upkeep liability against which to apply a rebate).

## §6 Distribution Rewards / LDR / Pioneer Star System

Live (`accounting/distribution-rewards.md`). Three Sky-funded incentives, paid from gross revenue **before** TMF.

**DR — 4 tiers** by branding strength of demand-side moat:

| Tier | Rate | Criteria |
|---|---|---|
| 0 | No DR | Excluded / ineligible |
| 1 | 0 bps | Untagged (still LDR-eligible) |
| 2 | 10 bps | Unbranded complex products with <90% sUSDS backing |
| 3 | 20 bps | "USDS"-named products **OR** unbranded ≥90% sUSDS backing |
| 4 | 50 bps | Direct USDS/sUSDS holding with clear Sky branding (Boosted DR) |

**Tagging.** On-chain (transaction codes) or off-chain (Guardian + GovOps verification). 10-year tag duration; last tagger wins; non-transferable. Primes set integrator splits independently.

**LDR.** **2/3 to tagging Prime, 1/3 to Sky.** Rewards Primes that source *sticky* demand feeding the ALDM system. When a Prime reserves capacity and **tugs** (per §8), LDR flows to the Prime that tagged the actually-tugged USDS, not the original target. Tier 1 (0 bps DR) addresses still earn LDR.

**Pioneer Star System** (Star Primes only — Spark, Grove, Keel, skybase, launch6; Obex excluded):
- 3-year Pioneer Phase per chain. One Pioneer Star per chain; Stars can have multiple chains.
- Designation: chain team/foundation + Star verification + Core Council strategic-alignment review.
- **Auto-tagging** of all untagged USDS/sUSDS on chain during phase; one-time permanent tag at end. Boosted DR not on auto-tags.
- **Pioneer Rewards:** SSR-equivalent on **Unrewarded USDS** (USDS not earning SSR via sUSDS or other Synomic Entity holdings) → Pioneer Star's SubProxy each settlement.
- **Unbalanced Supply Fee authority:** 20 bps/yr on supply unmatched by demand. Offsets: 1:1 tagged demand or 3× ADV via ASC liquidity. Exemptions via Ecosystem Accord (cannot be revoked after significant investment).
- **De-designation** by chain team pauses 3-year clock; future Pioneer Star resumes from where stopped.

## §7 Isolated deployment + MDC

`accounting/isolated-deployment.md`. Ring-fences capital outside the Prime's TRRC. **No leverage** — direct 1:1 deployment.

**Constraint:** `Isolated deployed assets ≤ Isolated capital committed`. Excluded from portfolio TRRC; losses reduce backing capital directly; recorded separately in entart with cross-Prime provenance via `&core.registry.cross-prime-flows`.

**Eligible:** IJRC, EJRC, MDC. **Not eligible:** SRC.

**Effect:** Isolated IJRC/EJRC reduces effective JRC for leverage purposes (cuts SRC ingression, MDC capacity).

**Primary use case — internal egression as EJRC.** Prime A designates capital for isolated deployment into Prime B as EJRC. Paired atoms in respective entarts (`isolated-deployment-asset` in A, `ejrc-ingressed` in B); cross-reference enables multi-hop traceability. Prime A exposure = exactly committed capital, 1:1 ring-fenced; Prime B treats EJRC normally through ingression curve.

**MDC (speculative).** Mezzanine Deployment Capital. Subordinated to SRC in liquidation only; senior to JRC in liquidation only. **Not a leverage instrument** — direct 1:1 deployment, no CRR/risk-weight, not in TRRC. MDC capital itself is the full risk buffer.

- Going-concern: untouched. Liquidation: SRC paid first; MDC residual; JRC + Prime Token nothing.
- **Capacity limit:** `MDC ≤ 3 × (IJRC + all EJRC nominal)`. Skin-in-game signal + indirect liquidation-probability bound, not loss-sharing. 3× preliminary.
- **Funding source:** isolated capital only (TISRC-style). GSRC cannot fund MDC.
- Yield > SRC reflecting probability-weighted liquidation shortfall.

## §8 Duration allocation

`accounting/duration-allocation.md`. How structural-demand-matching capacity flows to Primes.

**Architectural placement:** Generator's entart subtree:
```
&entity.generator.usge.structural-demand
  ├── .scrapers (raw lot-age data; Lindy + caps math)
  └── .auction (per-Prime per-bucket allocation atoms)
```
Capacity consumed by `structbook` (against structural USDS demand) and `termbook` (against tUSDS YT) per `risk-framework/primebook-composition.md`.

**Bucket structure: 101 buckets × 15 days each.** Bucket 0 = 0d; bucket 84 = 1,260d (JAAA); bucket 100 = 1,500+d (structural / permanent base).

**Phase 1 ("fake auction"):** governance writes `(structural-demand-allocation $prime $bucket $amount $epoch)` directly. Equal-split among active Star Primes per bucket. Architecture identical to Phase 9+; only allocation-atom *source* differs.

**Phase 9+ auction sequence:**
1. Pre-auction governance allocation publishing
2. Sealed-bid OSRC auction — uniform-price, **daily-only** (multi-epoch reservations would distort srUSDS yields)
3. Sealed-bid Duration auction — uniform-price, **multi-epoch reservations allowed**
4. Lindy measurement at lock window
5. Tug-of-war among existing reservations
6. Trading among Primes (including overreach)
7. Excess capacity → Duration auction

Bids as signed verb invocations through `&core.syngate`: `(submit-osrc-bid …)`, `(submit-duration-bid …)`. Matching is synart-resolved code (synserv-run). Legacy `auction-{x}` (class: relay) is the high-authority action beacon name; it submits, doesn't match.

**Tug-of-war (allocation Phase 1):**
- `Base Tug = max(Remaining Need × 10%, Reservation × 1%)`.
- `Distance Penalty = max(0.9^Distance, 0.10)`.
- `Effective Tug = Base × Distance Penalty`.
- **Direction value:** Tug UP = 1.0; Tug DOWN = `Target/Your` (gap capital required).
- **Collisions:** pro-rata if oversubscribed; remainder redirects.
- **Caps:** 10 iterations/round, 100 rounds.

**Trading (allocation Phase 2):** Primes upgrade by tugging higher buckets and cascading lower-tier capacity downward. **Overreach trading:** Pareto-improving swap — high-needing Prime offers high-tier capacity to intermediate Prime in exchange for intermediate's lower-tier holdings.

**Capacity retention:** UP retains source duration (beneficial); DOWN retains source duration (gap forms — gap capital required for differential).

**Excess** (Lindy − reservations) per bucket → Duration auction for non-reservation Primes at clearing price.

**Secondary market:** reservations transferable in full / partial / time-sliced.

**Risk-framework connection:** matching protects credit-spread risk, not interest-rate risk. `termbook` covers both (matched fixed/fixed against tUSDS YT); `structbook` covers credit-spread but not rate (rate-hedge or v1 carve-out, against structural USDS demand). Matched/unmatched blend smooth.

## Key vocabulary

Defined here (not duplicated from shared context):

- **TRC** — Total Risk Capital actually held; `((IJRC + EJRC × ingression) + (SRC × ingression)) × MC_multiplier`.
- **IJRC / EJRC / SRC / MDC** — Internal Junior / External Junior / Senior / Mezzanine Deployment Capital.
- **TEJRC** — Tokenized EJRC (LCTS-accessible, always non-synomic + zero-duration).
- **Effective vs nominal capital** — ingression rate determines leverage capacity; nominal absorbs losses.
- **Effective MC** — worst-of-observed Prime token market metrics; feeds total-RC cap.
- **Aggregate Backstop Capital (ABC)** — `Total Genesis Capital − Allocated` (post Jan-2026 CCB removal).
- **Net Revenue Ratio (NRR)** — `revenue / (revenue + 3B)`; scales TMF Steps 3–4.
- **Treasury Management Function (TMF)** — 5-step sequential revenue waterfall.
- **Smart Burn Engine (SBE)** — TMF Step 4 SKY buyback; currently fixed, dynamic post-BEAM.
- **Entity Creation Fee** — 5% of all entity governance tokens issued, paid in entity tokens to Sky Core.
- **Entity Upkeep Fee** — **50 bps/yr** of entity token **market cap** (conservative-priced), paid in own tokens.
- **Cross-Entity Upkeep Rebate** — discount on upkeep proportional to other entities' tokens held; conservative pricing → spread to Sky.
- **Distribution Rewards (DR)** — 4-tier (0/0/10/20/50 bps) USDS-adoption rewards routed to tagging Prime.
- **Liability Duration Rewards (LDR)** — 2/3 Prime / 1/3 Sky split of duration-bucket fees.
- **Pioneer Star System** — 3-year per-chain Star-Prime privileges (auto-tag + Pioneer Rewards + Unbalanced Supply Fee authority).
- **Unbalanced Supply Fee** — 20 bps/yr a Pioneer Star can charge on supply unmatched by demand.
- **Isolated deployment** — ring-fenced 1:1 capital deployment outside TRRC; primary use = internal egression as EJRC.
- **Tug-of-war** — Phase 9+ allocation phase: Primes tug across Duration Buckets to fill reservation needs.
- **Duration Bucket** — one of 101 buckets, 15 days each.
- **OSRC auction** — daily-only sealed-bid uniform-price, srUSDS-backed capacity.
- **Duration auction** — multi-epoch sealed-bid uniform-price, structural-demand-matching capacity.
- **Synart resource fee** — per-atom write / per-day retention / per-byte replication / per-match query.
- **Sky Direct shortfall** — asymmetric reimbursement: Prime made whole below Base Rate, Sky takes upside above.

## Cross-references

- `risk-framework/capital-formula.md` — TRRC computation accounting consumes
- `risk-framework/duration-model.md` — Lindy + structural caps; bucket math
- `risk-framework/matching.md`, `risk-framework/primebook-composition.md` — structbook/termbook capacity consumption
- `risk-framework/asc.md`, `risk-framework/operational-risk-capital.md` — parallel-track capital
- `risk-framework/book-primitive.md`, `risk-framework/tranching.md` — book structure, exoassets/exoliabs/waterfall
- `roadmap/phase-1-spaces.md` — ER pipeline, fake auction, monthly cadence carve-out
- `noemar-synlang/settlement-cycle-example.md` — worked synlang ER → breach → penalty
- `noemar-synlang/listener-loops.md` — in-space calculation pattern
- `macrosynomics/beacon-framework.md` §4, §11 — two-tier authority + I/O role; current operational identifiers (`auction-{x}`, `lcts-{halo}`; retired: `lpla-checker`)
- `synomic-entities/creation-restructuring.md` — Type 1/2 Restructure events triggering Creation Fee
- `growth-staking/growth-staking.md` — forfeitures re-enter TMF; cross-entity holdings double as growth assets
- `inactive/pre-synlang/whitepaper/sky-whitepaper.md` Part 6 — canonical 7-step loss waterfall
- `inactive/pre-synlang/forecast_model/` — Python forecast model

## File map

| File | What it adds beyond this summary |
|---|---|
| `settlement-cycle.md` | Full synlang code for each of the 5 steps; OSRC/Duration submission flow detail; LCTS settlement (Phase 4+); late-payment escalation cert/auth chain; legacy → current vocabulary translation table |
| `capital-stack.md` | Full SRC ingression table (0.5×–5× JRC); full EJRC anchor/max table over duration × synomic; MC bottleneck worked example; 7-step → 4-level waterfall mapping; Guardian capital structure rationale; nine Genesis Agents detail |
| `treasury-management.md` | Full NRR table; ABC three-phase formulas; complete worked examples (Genesis low-revenue + post-Genesis high-revenue); current-vs-target SBE behavior |
| `entity-fees.md` | Unified rule (5% Creation + 50 bps/yr market-cap Upkeep + Cross-Entity Rebate) with full token-status table covering all entity types; market-cap valuation + conservative-pricing oracle mechanics; rebate worked example for a Star Prime holding Grove + Halo tokens; Type 1 Restructure 95/5 split; settlement-integration cadence; two remaining open questions (oracle source/window, tokenless-holder rebate eligibility) |
| `distribution-rewards.md` | Tier 3a vs 3b path detail; tagging mechanics; LDR worked example with bucket-share distribution math; Pioneer designation + de-designation; Unbalanced Supply Fee offsets detail |
| `isolated-deployment.md` | Synlang form of paired isolated-deployment / ejrc-ingressed atoms; full MDC speculative section (capacity limit rationale, yield argument); vocabulary discipline (synome/synart/telart) |
| `duration-allocation.md` | Tug-of-war worked example with iteration trace; cascade trading example; overreach Pareto argument; full parameter defaults table; Phase 1/9+ structural identity |
| `forecast-model.md` | Pointer to Python `inactive/pre-synlang/forecast_model/`; what model simplifies (3-step waterfall, fixed backstop) and why; run commands |

