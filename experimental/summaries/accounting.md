# Accounting

**Status:** Mixed target architecture and live P1. P1 synome sees the daily synomic settlement cycle (DSC) only, used for structural-demand processing and epoch state. Legacy monthly economic reconciliation remains out-of-band and is not represented by atoms. Capital stack / entity fees / TMF / SDR auction remain target specs with explicit P1 carve-outs. DR/SDRR/tagging are not P1 synome functionality; SDRR waits for real SDR auctions with fees.
**Canonical home:** `lani/accounting/`

---

## TL;DR

Accounting defines how capital is sourced, ingressed, settled, and distributed after the Risk Framework decides what capital is required. The P1 live surface is narrow: continuous Prime ER emission, DSC epoch state, lot-age surface / Lindy SDR / SDR policy overlay processing, and a synserv-triggered temporary SDR auction. Economic settlement closure, TMF, DR/SDRR, and Sky Direct accounting remain out-of-band or later-phase.

## Section Map

§1 Settlement cycle · §2 Capital stack · §3 Genesis Capital / ABC · §4 TMF · §5 Entity fees · §6 DR/SDRR/Pioneer · §7 Isolated deployment / MDC · §8 SDR auction · §9 Vocabulary

## §1 Settlement Cycle

`accounting/settlement-cycle.md`.

**P1 live state**

- Real-time ER is emitted per Prime every heartbeat.
- `&core.settlement` holds the daily synomic settlement clock:
  - cut: 13:00 UTC;
  - processing: 13:00-16:00 UTC;
  - settle / epoch advance: 16:00 UTC.
- Synserv derives settlement state from wall clock and advances the epoch; there is no sudo `advance-epoch` loop.
- At the cut, synserv dispatches processing tasks. In P1 the only economic processing task is structural-demand SDR allocation.
- Legacy monthly settlement is an out-of-band operational reality, not an in-synome cycle.

**Target closure**

The later settlement closure has three concurrent activities:

1. real-time ER emission;
2. per-Prime closure at epoch boundary;
3. global aggregation into `&core.settlement`.

The per-Prime closure's 5 steps are max debt fees, idle USDS/DAI reimbursement, sUSDS spread profit, Sky Direct shortfall, and net amount. TMF consumes the aggregate result. P1 does not run this closure in synome.

**Retention.** Synart keeps the current epoch and most-recently-settled epoch. Longer forensics require archive loops / source-chain reads / settlement-tier promotion.

## §2 Capital Stack

`accounting/capital-stack.md`.

```
IJRC + EJRC   (pari passu by nominal)         <- going-concern first loss
Prime Token   (forced inflation)              <- recapitalization
------------------------------ liquidation threshold
MDC           (subordinated in liquidation)   <- residual claim
SRC           (senior in liquidation)         <- senior claim
```

Ingression determines leverage capacity; nominal capital absorbs losses. Universal ingression curve: flat to anchor, quarter-circle to zero at max. SRC max/anchor is 3:1; MC cap also uses the flat-plus-quarter-circle curve.

EJRC quality dimensions: synomic multiplier and term multiplier. Normie TEJRC, non-synomic term commitment, and synomic term commitment remain the main types.

Capital invariant: `TRRC <= TRC`, `ER = TRRC / TRC <= 0.90`. Breaches are visible from the live ER stream; penalty action is later-phase / manual in P1.

## §3 Genesis Capital / ABC

Genesis Capital is temporary bootstrap capital. ABC = total Genesis Capital minus allocated Genesis Capital. P1 ABC floor is $125M; long-term target is 1.5% of USDS supply. Retention currently operates in the out-of-band settlement reality.

Insolvency defense simplifies the whitepaper's seven steps into four levels:

1. ABC absorbs first;
2. SKY inflation;
3. Genesis Capital reclaim;
4. USDS haircut with SKY recovery airdrop.

## §4 Treasury Management Function

`accounting/treasury-management.md`.

TMF is the target 5-step waterfall over net revenue:

1. Security & Maintenance;
2. ABC;
3. Fortification Conserver;
4. Smart Burn Engine;
5. Staking.

Net Revenue Ratio: `revenue / (revenue + 3B)`, capped at 1.0. P1 does not run TMF in synome; it becomes relevant when closure / global aggregation enters DSC.

## §5 Synomic Entity Fees

`accounting/entity-fees.md`.

Tokenized entities pay:

- 5% Entity Creation Fee on all governance tokens issued;
- 50 bps/year Entity Upkeep Fee on conservatively priced token market cap;
- Cross-Entity Upkeep Rebate against holdings of other entity tokens.

Tokenless entities pay neither. The 50 bps upkeep stream is the economic basis for treating Sky as having a baseline 5% structural claim in the P1 temporary SDR auction's ownership formula. That formula lives in `&entity.generator.usge.sdr-auction`, not in the fee system.

## §6 DR / SDRR / Pioneer Star System

`accounting/distribution-rewards.md`.

DR and SDRR are target incentive systems, not P1 synome mechanisms.

- **DR** rewards USDS adoption by tagged balance. It needs a tagging registry and revenue source in synome before activation.
- **SDRR** rewards sticky demand and requires real SDR auctions with reservation fees. It is deferred until the real auction phase (Phase 9+).
- **Pioneer Star System** remains the target per-chain Star-Prime growth program, with auto-tagging and unbalanced supply-fee authority once the reward/tagging stack is active.

This resolves the old ambiguity: without real auction fees, SDRR has nothing to attribute.

## §7 Isolated Deployment / MDC

`accounting/isolated-deployment.md`.

Isolated deployment ring-fences capital outside Prime TRRC with no leverage: deployed assets <= isolated committed capital. Main use case is internal egression as EJRC between Primes. MDC remains speculative mezzanine deployment capital: subordinated to SRC in liquidation, senior to JRC only in liquidation, not a leverage instrument.

## §8 SDR Auction

`accounting/sdr-auction.md` plus `risk-framework/sdr-model.md`.

P1 structural-demand placement:

```
&entity.generator.usge.structural-demand
&entity.generator.usge.sdr-auction
```

**P1 live state**

- 51 buckets, 30 days each.
- Bucket N = N * 30 days; bucket 50 = 1500+ days.
- `structural-demand` stores lot-age surface, Lindy SDR, SDR policy overlay, and effective SDR bucket capacity atoms.
- Synserv triggers the temporary SDR auction during DSC processing.
- The auction writes `(sdr-allocation $prime $bucket $amount $epoch)` into `sdr-auction`.
- Structbooks read current-epoch allocation atoms.

**Temporary P1 SDR auction equation**

```
sky_effective_ownership(p) = 0.05 + 0.95 * sky_prime_token_share(p)
ownership_weight(p)        = sky_effective_ownership(p) * prime_ijrc(p)
allocation(p,bucket)       = effective_sdr_bucket_capacity(bucket) * ownership_weight(p) / sum(active_prime_weights)
```

All active Primes participate. `&core.treasury` supplies raw Sky token-share facts, including supplied values for unlaunched tokens; `prime-ijrc` comes from each Prime root. Missing, stale, or zero IJRC means zero allocation. If no active Prime has positive weight, allocation rounds to zero; any rounding/dust remainder also rounds to zero. Unused allocation does not carry forward; current-epoch atoms are the live SDR allocation for `structbook`. The ownership-weight formula is temporary and contained entirely in `sdr-auction`.

**Later target**

Real OSRC + SDR auctions, tug-of-war, trading, overreach, and secondary markets replace the temporary body while preserving the allocation atom shape and structbook read path. SDRR activates only once real auctions pay fees.

## Key Vocabulary

- **DSC** — daily synomic settlement cycle, the only in-synome cadence.
- **TRC / IJRC / EJRC / SRC / MDC** — Total Risk Capital and its capital tiers.
- **Effective vs nominal capital** — ingression rate determines leverage capacity; nominal absorbs losses.
- **ABC** — Aggregate Backstop Capital.
- **NRR** — Net Revenue Ratio.
- **TMF** — Treasury Management Function.
- **Entity Creation / Upkeep Fee** — 5% creation and 50 bps/year market-cap upkeep.
- **DR / SDRR** — Distribution Rewards / Structural Demand Resource Rewards; deferred from P1 synome.
- **SDR Bucket** — one of 51 30-day buckets.
- **SDR** — Structural Demand Resource.
- **Lindy SDR** — dynamic structural-demand model output from the lot-age surface.
- **SDR policy overlay** — governance-set caps, haircuts, source filters, and fallback bounds.
- **P1 SDR auction** — temporary-equation body allocating effective SDR by Sky ownership-weighted IJRC.
- **Tug-of-war** — later real auction allocation phase.
- **Synart resource fee** — target per-atom / retention / replication / query cost model.

## Cross-References

- `risk-framework/capital-formula.md` — TRRC computation accounting funds.
- `risk-framework/sdr-model.md` — 30-day buckets and structural-demand capacity.
- `risk-framework/matching.md`, `risk-framework/primebook-composition.md` — structbook/termbook consumption.
- `roadmap/phase-1-spaces.md` — P1 DSC, Lindy SDR, temporary SDR auction, treasury, ER pipeline.
- `noemar-synlang/settlement-cycle-example.md` — worked ER / breach / penalty example.
- `macrosynomics/beacon-framework.md` — beacon taxonomy and action relay naming.
- `growth-staking/growth-staking.md` — staking activation and forfeiture path.

## File Map

| File | What it adds beyond this summary |
|---|---|
| `settlement-cycle.md` | Full target closure logic, DSC notes, retention model |
| `capital-stack.md` | Ingression tables, MC bottleneck, Genesis Capital mechanics |
| `treasury-management.md` | NRR table, ABC formulas, SBE examples |
| `entity-fees.md` | Unified creation/upkeep/rebate fee rule |
| `distribution-rewards.md` | DR/SDRR/Pioneer target mechanics; SDRR deferred until real auctions |
| `isolated-deployment.md` | Isolated deployment and MDC details |
| `sdr-auction.md` | Target OSRC / SDR auction and tug-of-war mechanics |
| `forecast-model.md` | Python forecast model pointer |
