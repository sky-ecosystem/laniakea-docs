# Roadmap

**Status:** `phase-1-overview.md` is the orientation entry point (fronts framing); `phase-1-spaces.md` v3 is the canonical Space-by-Space spec (post-2026-05-15 topology redesign — 64 fixed Spaces, 7 Primes, 3 Halos with halo class + risk class); `p1-design-followups.md` is the open-design pickup list with §1.1 (attestor schema) resolved; `attestor-atom-schema.md` carries the resolved boolean attestation schema; `roadmap-ideas.md` is conventions / lift principle / phase-invariant consumption sites (live as guidance); `v1-principles.md` distills the thirteen invariants; `asc-transition.md` is partly live (PSM still active, ASC ramping).
**Canonical home:** `laniakea-docs/roadmap/`

---

## TL;DR

Carve-out layer for Laniakea: main corpus describes target architecture, roadmap docs hold what's live now and how each phase advances by topology delta. Covers the **Phase 1 v3 spec** (64 fixed Spaces, 7 Primes deploying into 3 P1 Halos — spark-term, grove-term, maple-term — with `nfat-term` halo class × `custodial-crypto` risk class per halo, real-time ER, all-synlang, manual settlement) with its worked NFAT walkthrough and 13 carve-outs; the **fronts framing** (3 structural + 6 operator fronts) as the orientation layer; the lift principle + insyn/exsyn pattern + phase-invariant consumption sites governing phased buildout; the thirteen v1 principles distilled as substrate invariants; ASC/DAB peg-defense mid-transition from PSM; the resolved boolean attestor schema; and the present-day legacy operational reality (monthly settlement cadence, legacy core vaults / PSM / legacy RWA, CCB reclassification, SBE fixed buyback). **`phase-1-overview.md` is the entry point for orientation; `phase-1-spaces.md` for canonical detail**; everything else supporting.

## Section map

§1 Directory contract + phase progression · §2 Phase 1 v3 reality · §3 Fronts framing · §4 Lift principle + phase-invariant consumption sites · §5 Insyn/exsyn (canonical) · §6 Sudo/exospell/endospell + frame · §7 ASC/DAB/Peg Defense + PSM transition · §8 Phase 1 beacons · §9 V1 worked example + carve-outs · §10 V1 principles · §11 Attestor schema

## §1 Directory contract + phase progression

Main-corpus docs describe target state; "in Phase X this isn't built" hedging belongs here. Roadmap docs are **space-perspective** — each phase as a topology delta, answering: (1) what Spaces exist, (2) what each holds + cadence + operational vs fixed, (3) I/O between beacons/gate/Spaces, (4) what changes operationally vs sudo-only. **Any sudo event during a phase is a phase boundary by construction.** Fronts are units of focused attention orthogonal to topology (some structural-defined, some operator-defined — see §3).

| Phase | Focus |
|---|---|
| **1** | Real-time ER per Prime; manual settlement; 7 Primes into 3 P1 Halos; structural-demand equation runs live; manual auction allocations; deterministic recipes |
| **2–4** | Daily settlement; LCTS launch (srUSDS); governed (pre-auction) allocations; canonical `&core.framework.*` Space + propagation |
| **5–8** | Factory stack — Halo / Prime / Generator factories |
| **9–10** | Sentinel formations; OSRC + Duration auctions via per-Prime `baseline-{prime}` relays + paired `stream-{prime}-{actor}` sentinels; first cognitive recipes |
| **Beyond** | Richer cognitive recipes; recipe diversity favoring generalism |

Each later phase = precisely-specified sudo writes extending Phase 1. Substrate never gets rewritten; new substrate is added alongside (additive-only transitions via the phase-invariant consumption-site pattern).

## §2 Phase 1 v3 reality

**Single deliverable:** real-time ER per Prime, emitted continuously in production-quality synlang. Settlement and penalty action remain manual.

### Topology totals

| Category | Count |
|---|---|
| Universal `&core.*` (syngate, loop.synserv, registry.beacon, test-suite) | 4 |
| Generator (`usge`: root + structural-demand + auction + protocol-registry) | 4 |
| Oracle (Crypto Majors: root + market-data + ticks) | 3 |
| Per-Prime ×7 (root + primebook + structbook + relay + protocol-registry) | 35 |
| Per-Halo ×3 (root + nfat-term + custodial-crypto + custodial-crypto.attest-data + relay + protocol-registry) | 18 |
| **Fixed Spaces at genesis** | **64** |
| Constructor-made (per deal) | unbounded |
| Beacon identities / Constructors / Operational verbs | ~23 / 3 / ~12 |

### Architectural cuts

- **All logic in synlang from day 1.** CRR, sub-book routing, ER, equity invariants, health factors, loop bodies — all production synlang in Noemar. Python only for grounded primitives.
- **Insyn/exsyn TRRC split.** `TRRC = insynTRRC + exsynTRRC`; TRC fully synome-tracked; `ER = TRRC / TRC`. exsyn-TRRC claims live in each `&entity.prime.{id}.primebook`, written by a per-Prime `patch-{prime}` patch-beacon (no oracle-entity hop).
- **Phase-invariant consumption sites.** Risk forms, loop bodies, and structural-demand allocations all materialize at their consumption sites in P1; canonical sources ship additively in later phases without relocating anything.
- **Per-entart local materialization.** Each halo carries its own copy of its halo class + risk class + attestor sub-Space. Each Prime, Halo, and the Generator carry their own `protocol-registry` with the chain contract refs they specifically need.
- **Halo class vs risk class.** Halo class (`nfat-term`) defines halobook policy + permitted risk classes; risk class (`custodial-crypto`) carries the risk form (CRR equation) + class-accordant attestor as sub-Space. All 3 P1 halos share `nfat-term` × `custodial-crypto` but each materializes its own copies.
- **7 Primes all active** (Spark, Grove, Obex, Keel, skybase, launch6, and a 7th TBD) into 3 P1 Halos (spark-term, grove-term, maple-term).
- **Risk framework as black box.** Per-halo risk class carries the risk form; signature real, body deferred. No canonical `&core.framework.*` Space in P1.
- **Boolean attestation per exobook** (class-accordant attestor); without fresh accordant `(underwriting pass)`, exobook excluded from rollup (default-deny). See [`../roadmap/attestor-atom-schema.md`](../roadmap/attestor-atom-schema.md).
- **Authority rooted in `&core.registry.beacon`.** No standing Guardian entart Space in P1; Guardian's cert + auth content sudoed into the beacon registry at genesis.
- **Root holds registry + constructors only.** Operational logic lives in dedicated sub-Spaces. Universal pattern across every entart type.
- **Halobooks / riskbooks / exobooks are constructor-made** (govops-halo), not sudo.
- **One Oracle entity**: Crypto Majors (price/liquidity/funding for BTC/ETH/stETH/USDC). Book Attestation Oracle has no entart Space — its cert chain folds into the beacon registry and attestations land directly in exobooks.
- **Frame mechanism** for clone-and-test: genesis → fork to shadow → run synart-native test suite → discard → production.

**ER data flow:** crypto-majors market-data writes into `&entity.oracle.crypto-majors.ticks`; per-Halo class-accordant attestors write boolean `riskbook-attestation` atoms into riskbook Spaces (one per riskbook, covering all exobooks under it); per-Prime patch-beacons sudo-write `(exsyn-trrc-claim …)` directly into each primebook; synserv evaluates `&core.loop.synserv` and derives upward: exobook (junior_residual, HF) → riskbook (attestation gate + child exobooks) → CRR via the risk form → halobook NFAT projection → Prime structbook matched/unmatched blend with auction allocations → primebook reads its local exsyn-TRRC claim plus structbook insyn-TRRC and emits `(prime-er prime value T)` per heartbeat.

**Phase boundary examples:** adding Prime/Halo/risk class; activating a sub-book (only `structbook` active in v1); concentration caps; real Prime-strategy-driven auctions replacing the fake auction; canonical loop-template propagation; canonical risk-form source + propagation; settlement closure (Phase 2); Growth Staking activation; unfolding risk framework (adds `&core.framework.risk.scenarios` / `risk.asset-profiles` / `risk.asset-history`); event-driven derivation; Genbook cross-Prime concentration enforcement.

## §3 Fronts framing

The orientation layer for Phase 1, organized by *fronts* — units of focused attention orthogonal to topology. Each front cross-cuts the entart tree; the same component (synserv, patch beacon) shows up through more than one front by design.

**Structural fronts** (where in the system):
- **The Core** — substrate: `&core.syngate`, `&core.loop.synserv`, `&core.registry.beacon`, `&core.test-suite` (4 Spaces).
- **Prime–Halo** — the deliverable: the ER calculation and everything that plugs into it. 53 fixed Spaces (35 Prime + 18 Halo entart) + unbounded constructor-made.
- **Demand Side** — major input: structural-demand capacity, fake auction, Generator ERC20 metadata (4 Generator Spaces).

**Operator fronts** (who runs it):
- **synserv (+ Guardian/Ozone)** — canonical heartbeat runner; Guardian holds genesis sudo authority but no standing entart Space.
- **govops** — humans-in-the-loop running constructors and deploy / rollover / withdraw flows.
- **Attestor Oracle** — operates the per-halo class-accordant attestor loops (sub-Space of each halo's risk class).
- **Market Oracle** — owns the crypto-majors entart (3 Spaces).
- **patch beacon** — exsyn-TRRC scaffold per Prime (sudoed inline; designed to sunset).
- **test-runner** — testing practice; tests carry the normative risk-form spec until canonical propagation ships.

Full treatment in `phase-1-overview.md`. The structural/operator split is a maturity gradient, not a permanent taxonomy — operator fronts converge to local telarts over time.

## §4 Lift principle + phase-invariant consumption sites

Phase 1 builds **production-quality lift** that doesn't get rewritten. Bar: *if we'd build it in Python now and rewrite in synlang later, build it in synlang now.* **Code → synlang** (every rule, equation, derivation, loop body, predicate); **data → atoms** (stress parameters, profiles, allocations, governance numbers — sudo-set in v1, consuming equations are real synlang); **black-box deferrals** are honest scaffolds — function whose body is opaque is fine **if the signature is real synlang**. The custodial-crypto risk form is v1's example: production signature, opaque body, no rewrite when matured.

**Phase-invariant consumption sites** make later transitions purely additive. Fix where a thing is *read from* in P1; let provenance migrate behind it. The risk form's read site is `&entity.halo.{id}.custodial-crypto` (per-halo); the loop body's read site is `&entity.{type}.{id}.relay`; the structural-demand allocations' read site is `&entity.generator.usge.auction`. In all cases, a later canonical source + propagation refreshes the same Space without relocating reads. Local extensions in the per-entity Space can coexist with propagated content (overlay pattern). Test for any deferred component: does building it now exercise architecture we'll otherwise miss, or is it speculative scaffolding? If speculative, defer.

## §5 Insyn/exsyn (canonical home: `roadmap-ideas.md`)

Canonical mechanism for **phased synome buildout**. At any phase, some capabilities are insyn (synome-native, real synlang on real atoms), some exsyn (oracle/govops-fed gap-filler from infrastructure not yet synlang-native). Spanning aggregations: `quantity = insyn-component + exsyn-component`. Distinct from `endo`/`exo` (graph membership) — insyn/exsyn is about **epistemic provenance**.

Phase 1: `TRRC = insynTRRC + exsynTRRC`. As halos migrate, exsyn shrinks toward zero; **synlang code does not change at the migration boundary**. The Phase 1 exsyn-bridge is a per-Prime `patch-{prime}` patch-beacon ×7 (govops-certed, sudoed inline at genesis into each primebook); it sunsets per-Prime as insyn coverage grows. The patch-beacon class itself is the reusable scaffold pattern for any future hack of this nature — Guardian-sudoed primitive, no regulated framework, designed to retire.

Fits when: associative quantity, clean contributor split, trustable provider, one-way trajectory. Doesn't fit: cross-contributor interactions (correlation matrices), same-trust-deficit provider, undefined trajectory — those use black-box deferral. Other domains: per-concentration-category exposure, total USDS backing, Genbook cross-Prime aggregations, telart→synart migration, cross-chain (native insyn + foreign exsyn).

## §6 Sudo staircase + frame mechanism

| Mechanism | Adds | When |
|---|---|---|
| **sudo** | direct write, bypasses gate | Always: genesis, then rare phase-boundary or emergency |
| **exospell** | gating + timelock + visibility + cancellability via `&core.spells` (24–48h maturation) | Mid phases; *not in Phase 1* |
| **endospell** | + cryptographic binding to a synodoxics PLN derivation; substrate verifies the diff | Mature state; needs probmesh + synodoxics |

Sudo never disappears; usage shrinks from "the only mechanism" (Phase 0–1) to "escape hatch" (mature). Integrity: off-space audit log + operator diversity. **Failover is an atom write** — backup synserv operators run the same loop with independent state; if canonical breaks, Core Council out-of-band signs `(canonical-synserv-runner X)`, subscribers reconnect. Obviates "emergency sudo" as a distinct concept.

**Frame mechanism:** runtime feature, not a synart concept. A frame is a complete instance of synome state; runtime can hold multiple. Operations: `fork`, `switch`, `discard`, `diff`. Phase 1 use: clone-and-test isolation. Future: sudo event safety (apply to shadow first), forecasting, what-if for endospell candidates, migrations. Phase 1 deep-copy; copy-on-write later.

## §7 ASC / DAB / Peg Defense

Operational ALM each Prime must satisfy. **Parallel track to portfolio risk capital — not folded into TRRC.**

| Parameter | Value |
|---|---|
| ASC minimum | 5% of Primebook Assets (excludes USDS) |
| Resting ASC bid floor | ≥ 0.999 USD/USDS (10 bps downside) |
| Latent ASC | ≤ 15 min auto convertibility; cap 25% of total ASC |
| DAB | 25% of required ASC; for-sale at ≤ 1.001 USD/USDS |
| Peg Defense trigger | Avg USDS on LayerZero DEXes < 0.999 |
| Peg Defense buy rate | ≥ 6.25% of ASC requirement / 6h |

**Resting ASC** = atomically executable bids or verifiable same-spread arrangements (LitePSM/PSM3, USDS-paired Curve/Uniswap, GUNI pools). **Latent ASC** = cash stables convertible within 15 min (non-USDS Curve/Uniswap, SparkLend/Aave/Morpho, Prime ALM Proxy). Failures have no explicit penalty near-term but must be detected and reported. **Incentives** tied to Base Rate vs T-Bill spread. **ALM Rental:** Primes trade ASC + DAB + Peg Defense as a bundle.

**PSM transition (live):** Sky Core manages legacy PSM during ASC rollout. **LitePSM control is being transitioned to Grove**; post-transition Grove manages as an ASC asset (paying Base Rate). USDC in PSM uniquely capital-efficient. Target: ASC = comprehensive ALM layer; PSM becomes implementation detail of Grove's liquidity ops. ASC-eligible holdings route to Primebook `ascbook` (deferred in P1 — only `structbook` active).

## §8 Phase 1 beacons

Phase 1 beacons are **deterministic programs, not AI** — teleonome-less. Authority follows the two-tier framework (high-authority operates a Synomic Entity; low-authority = passive observation or teleonome-to-teleonome). Legacy `lp*` prefixes are retired in favor of class-derived names.

Position verification, settlement processing, and CRR calculation move into **synart-resolved in-space synserv computation** — not separate beacon classes. v3 identities (~23 total): synserv-canonical, market-data-crypto-majors-{provider} (market-data-beacon), attest-data-{halo-id} × 3 (attest-data-beacon), patch-{prime} × 7 (patch-beacon), govops-prime-{id} × 7, govops-halo-{id} × 3, test-runner. Loop bodies live in per-entity Spaces in P1 (sudo-set, self-contained); canonical loop templates ship additively later via the phase-invariant consumption-site pattern. **Patch-beacons are the one class without a regulated framework** — Guardian-sudoed primitives whose loop body and per-entity config are sudoed inline into the target Space (no universal template, no oracle-entity ownership); the Phase 1 use case is the per-Prime exsyn-TRRC scaffold writing into each primebook, and the class itself is reusable for any future gap-filler scaffold.

| Class | Notes |
|---|---|
| `synserv` | Heartbeat, runs `&core.loop.synserv` |
| `market-data-beacon` | Renamed from `oracle`; pushes price/liquidity/funding-rate ticks |
| `attest-data-beacon` | Renamed from `attestor`; per-class identities are `attest-data-{halo-id}`; loop bodies live as sub-Spaces of risk class Spaces (`&entity.halo.{id}.custodial-crypto.attest-data`) |
| `patch-beacon` | New; replaces the retired `oracle-exsyn` class. govops-certed, no regulated framework, sudoed inline, designed to sunset |
| `govops-prime` / `govops-halo` | Per-entity governance ops; loop bodies in per-entity `relay` Spaces |
| `test` | Shadow-frame only |

**Evolution:** Phase 1 (deterministic beacons + Synome-MVP) → Phases 9–10 (sentinel-formation operating setups: per-Prime `baseline-{prime}` + `warden-{prime}-{op}` relays + `stream-{prime}-{actor}` sentinels + `principal-{owner}` variant; proto-teleonomes) → Beyond (full teleonomes with directives, telart, dreamer/actuator, RSI). Invariants: synome trumps beacon; SORL 25%/18h up, instant down; audit trail; R/W/X separation; human governance backstop; cancer-logic security.

## §9 V1 worked example + carve-outs

The worked example lives in `phase-1-spaces.md`, framed against the 7-Primes / 3-Halos topology. Spark-Term (one of the 3 P1 Halos) originates a 6-month custodial loan: $750K USDC against 1 BTC; Spark Prime deploys into the resulting NFAT.

Seven steps: (1) **exobook setup** — `btc 1`, $250K junior + $750K senior, HF 1.05, maturity 180d; (2) **risk-class match** — the riskbook is bound to Spark-Term's `custodial-crypto` risk class (the risk form is imported into the riskbook at `create-riskbook` time); (3) **asset stress** under `severe-correlated-crash`: BTC −45% ($80K → $44K), USDC depeg 5%, stressed junior $44K × ($250K/$80K) ≈ $13.75K, senior loss = max(0, $36K − $13.75K) = $22.25K, USDC depeg = $37.5K, **total ≈ $59.75K (~7.97%)**; (4) **halobook P/T** — unwind at maturity/HF only, not transferable (per `nfat-term` halo class); (5) **sub-book routing** — only `structbook` eligible; (6) **structbook capital** — given $10M remaining bucket-12 capacity: matched $750K, capital ≈ $750K × 5% RW = **$37.5K** (rate-hedge waived); if capacity full, unmatched = $750K × max(5%, 7.97%) ≈ **$59.8K** — smooth blend per `risk-framework/matching.md` §4, no binary cliff; (7) **concentration check** at Genbook (deferred in v1; Genbook itself deferred).

**Full-Prime scaling:**

```
Prime insynTRRC = Σ (Matched × RW + Unmatched × Forced-Loss) + Concentration Excess
Prime TRRC      = insynTRRC + exsynTRRC          ; ASC + ORC parallel, not in TRRC
Prime ER        = TRRC / TRC
```

`exsynTRRC` is read locally from `(exsyn-trrc-claim {prime} _)` atoms in `&entity.prime.{id}.primebook`, written there by `patch-{prime}` (no oracle-entity hop).

**13 V1 carve-outs (in `phase-1-spaces.md`):** (1) structural-demand equation runs live in P1 (Lindy + structural caps fed by endoscraper-scraped holder data); allocations remain manual per #9; (2) equal-split sudo distribution; (3) no rate-hedge capital for matched; (4) TTM 0–12 months; (5) SPTP = remaining nominal term; (6) one Genbook (USDS — and Genbook itself deferred); (7) three Halos × seven Primes; (8) super-senior tranches only (mezz/equity → CRR 100%); (9) manual structural demand allocations (fake auction in `&entity.generator.usge.auction`); (10) single halo class (`nfat-term`) × single risk class (`custodial-crypto`); (11) only `structbook` active; (12) tranche rights schema present but not exercised; (13) JAAA/CLO modeling deferred. Each has a clear later-phase replacement.

## §10 V1 principles (`v1-principles.md`)

Thirteen invariants distilled from the carve-outs and the worked NFAT example. Each survives every later phase; what unlocks (auctions, daily settlement, factory stack, sentinel formations, multi-form risk framework) extends them without contradiction.

1. **Liability duration determines duration capacity** (Lindy Duration Model).
2. **Use SPTP for asset duration** — stress-modified pull-to-par (v1 carve-out: no stress modifier yet).
3. **Duration matching protects against credit spread risk, not rate risk** — spreads mean-revert; rate shifts don't.
4. **All fixed-rate exposure must be rate-hedged** (or hold rate-hedge capital) for matched treatment (v1: waived for matched NFAT).
5. **SPTP determines duration matching eligibility** — SPTP ≤ liability tier duration AND rate-neutral.
6. **Matched positions get risk-weight treatment** — capital only for fundamental risk.
7. **Unmatched positions get forced-loss treatment** — `max(RW, forced-loss-capital)`.
8. **Crypto lending is structurally tranched** — senior risk = asset stress through junior cushion; gap risk unified into standard tranche math.
9. **Concentration limits prevent diversification illusions** — capital must survive each stress on its correlated group.
10. **Default-deny is the discipline** — anything not adequately modeled gets CRR 100%. Phase 1 instance: an exobook without a fresh accordant attestation does not roll up.
11. **Sub-book composition is continuous, not binary** — matched/unmatched blend smoothly with capacity utilization.
12. **Currency frame ≠ instrument** — frame is the unit of account (USD); instruments translate with declared stress.
13. **Real-time equity recomputation is the operational invariant** — drives the synserv heartbeat, attestor cadence, and the lift-from-day-1 commitment.

## §11 Attestor schema (`attestor-atom-schema.md`)

**RESOLVED 2026-05-14** for the Phase 1 `custodial-crypto` risk class.

For custodial-crypto, every quantitative CRR input is **insyn** — collateral, debt, LT, liquidation-bonus, LTV all come from `chain-read`; price, liquidity, vol from `market-data-beacon`. The attestor is therefore *not* an oracle of loan facts — it's a **legal / operational / credit underwriter** of what the chain can't show. Its output is **boolean** (`underwriting pass | fail` + an itemized `claims` block + three-state `borrower-credit-standing`).

The attestor loop body lives as a sub-Space of the per-halo risk class (`&entity.halo.{id}.custodial-crypto.attest-data`), making class-accordance structural: the attestor operates only on riskbooks bound to its risk class.

Default-deny gate: without a fresh accordant `(underwriting pass)`, the exobook does not roll up. The risk form excludes it; the Prime's structbook can't account for the position. Cadence is **credit-review-paced**, not market-paced — none of the legal/credit/custodian facts move with price.

Itemized `claims` block is the slashing surface — magnitudes calibrated per claim. Magnitudes themselves live in the Oracle Entity stub-spec (clean-todo Pass B).

**Open sub-question:** `scope-ref` granularity — exactly which exobook atom predicates count as "structural" (and therefore re-attestation-forcing). Forcing trigger: building the v1 attestor.

## Pre-synlang ↔ synlang vocabulary (partial)

Synome-MVP → universal `&core.*` + per-entity entart subtrees · Halo Books → constructor-made `&entity.halo.{id}.halobook.{hbk-id}` · Halo Units → atoms in book Spaces · Risk Framework (entity) → per-halo risk class Spaces in P1; canonical `&core.framework.risk.forms` post-P1 · Attestations (entity) → boolean atoms in exobook Spaces (attestor-gated) · LPLA/LPHA/HPLA/HPHA → two-tier authority + I/O role (legacy prefixes retired except on kept peer-to-peer `hpla-{trade|arb|coop}-…` identifiers) · `lpla-checker` → synserv-run in-space calculation, not a separate beacon · `oracle` class → `market-data-beacon` · `attestor` class → `attest-data-beacon` · `oracle-exsyn-{class}` → retired; replaced by per-Prime `patch-beacon` instances writing directly into primebooks · "risk category" → "risk form" (the equation) inside "risk class" (the bundle with class-accordant attestor) at the riskbook layer.

## Key vocabulary

Terms originating in this directory (others — sudo, gate, entart, TRRC, etc. — are defined elsewhere):

- **exospell** — Core-Council-signed timelocked gate-mediated mutation in `&core.spells` (24–48h maturation, cancellable); not in Phase 1
- **endospell** — exospell whose diff is cryptographically bound to a synodoxics PLN derivation; mature state
- **Frame** — runtime instance of complete synome state; fork/switch/discard/diff; not a synart concept
- **Lift principle** — synlang-first, production-quality; code → synlang, data → atoms
- **Phase-invariant consumption site** — read location whose path is fixed across phases; only provenance migrates (sudo-authored → propagated-from-canonical)
- **Black-box deferral** — declare synlang signature now, leave body opaque; permanent signature, body fills later without rewrite
- **insyn / exsyn** — epistemic provenance distinction; canonical phased-buildout device
- **patch-beacon** — Guardian-sudoed beacon class with no regulated framework; loop body and per-entity config sudoed inline into a target Space; Phase 1 instance is per-Prime exsyn-TRRC scaffold writing into each primebook; designed to sunset as use cases migrate to insyn
- **Halo class** — halobook policy template per halo (standard terms, permitted risk classes, tranching, issuance presets, rate limits, govops control keys). P1: all 3 halos use `nfat-term`.
- **Risk class** — riskbook risk treatment per halo: bundle of risk form + class-accordant attestor (attestor loop as sub-Space). P1: all 3 halos use `custodial-crypto`.
- **Risk form** — the synlang equation inside a risk class that consumes `chain-read` + market-data + boolean attestation gate and returns per-risk-type CRR components.
- **protocol-registry** — per-entart chain-contract metadata sub-Space (addresses + ABIs + event signatures). Each Prime / Halo / Generator owns its own.
- **Phase boundary** — by construction, any sudo event during a phase
- **ASC / DAB** — Actively Stabilizing Collateral / Demand Absorption Buffer; Prime ALM obligations parallel to TRRC
- **Peg Defense Event** — average USDS on LayerZero DEXes < 0.999; Primes must buy at ≥ 6.25% of ASC/6h
- **ALM Rental** — Prime-to-Prime trading of ASC/DAB/peg-defense as a bundle
- **Teleonome-less beacon** — Phase 1 deterministic program with no autonomous mission
- **Core Entity** — legacy core vault standardized under Core Council governance, sitting at Halo layer pre-Prime/Halo architecture
- **CCB reclassification** — end-Jan 2026 removal of Core Council Buffer from Aggregate Backstop Capital; transfer-point expense recognition replaces disbursement-point
- **SBE BEAM** — governance-controlled execution surface for the dynamic-burn SBE; ships post-Phase-2

## Cross-references

`noemar-synlang/topology.md` (canonical six-layer synome root + entart pattern + naming) · `noemar-synlang/runtime.md` (auth, gate, two-step rule + loop patterns) · `macrosynomics/topology-layers.md` (telos/axioms/topology/population layering, sudo discipline) · `macrosynomics/beacon-framework.md` (authority + I/O taxonomy; market-data / attest-data / patch class definitions) · `risk-framework/` (target framework; Phase 1 collapses to one risk class with a black-box risk form) · `risk-framework/primebook-composition.md` (sub-book taxonomy; only `structbook` active in v1) · `risk-framework/matching.md` (matched/unmatched capital blend; rate-hedge waiver) · `roadmap/asc-transition.md` (PSM as Resting ASC during transition) · `accounting/settlement-cycle.md` (synserv heartbeat + 5-step closure, Phase 2) · `accounting/capital-stack.md` (Aggregate Backstop Capital, CCB removal) · `growth-staking/growth-staking.md` §11 (activation as phase boundary) · `synodoxics/lift.md` (lift/meta-lift/weakness vocabulary) · `inactive/archive/whitepaper/appendix-c-treasury-management-function.md` (canonical TMF; dynamic SBE formula).

## File map

| File | What it adds beyond this summary |
|---|---|
| `phase-1-overview.md` | Orientation entry point — Phase 1 organized by *fronts* (3 structural + 6 operator); topology-by-front enumeration of all 64 fixed Spaces; global guardrails ("read first") |
| `phase-1-spaces.md` | Canonical Phase 1 v3 spec. Full Space-by-Space tables; halo class + risk class section; attestation model with boolean schema; operational verb + write-surface tables; 23-step genesis sudo sequence; test category table; ER ASCII diagram; full worked NFAT example; 13 V1 carve-outs |
| `p1-design-followups.md` | Open-design pickup list. §1.1 attestor schema RESOLVED; §1.2 risk-form signature, §1.3 CORE integration, §1.4 atom trace open; §3 cleanup items + phase-boundary deferrals |
| `attestor-atom-schema.md` | The resolved boolean `riskbook-attestation` schema for the `custodial-crypto` risk class (one attestation per riskbook, covering its exobooks). Reframe rationale; default-deny gate; slashing surface; `scope-ref` granularity open |
| `roadmap-ideas.md` | Vocabulary in depth; Phase-0 substrate sketch; full lift-principle do/don't lists; insyn/exsyn fit criteria + patch-beacon as canonical exsyn-bridge scaffold; **phase-invariant consumption-sites principle** (additive-only transitions); phase doc template for Phases 2–10; design takeaways and open questions |
| `v1-principles.md` | The 13 principles with carve-out flags spelled out (SPTP stress-modifier waiver, rate-hedge waiver); full prose per principle |
| `asc-transition.md` | Full resting/latent ASC eligibility lists; DAB qualifying forms; peg-defense execution mechanics; Grove/LitePSM ownership transition; "ASC point" rental economics |
