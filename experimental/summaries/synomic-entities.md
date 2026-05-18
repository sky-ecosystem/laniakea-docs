# Synomic Entities

**Status:** Mixed — Phase 1 live topology (7 active Primes / 3 P1 Halos / daily synomic settlement cycle / deterministic relay beacons / no Core Entity halo-mode) differs from target architecture (sentinel formations, NFAT facilities, Identity Networks, Core Entity crisis wrappers, Type 2 restructure). Three rank-2 entity types beyond Prime/Generator (Oracle, Sequencer, Pylon) are stub-spec'd; the rank-1 **Core Entity** type operates in several target modes but is not instantiated in P1. Open question stubs remain: Sequencer beacon class names, Oracle/Sequencer fee model, attestation calibration, Pylon assurance-fund sizing parameters, recovery-tool defaults per Ring.
**Canonical home:** `lani/synomic-entities/`

---

## TL;DR

Per-type operational specs for every Synomic Entity. Theory of *what* entities are lives in `macrosynomics/synomic-entities.md`; this directory is the engineering surface — infrastructure, lifecycle, beacon set, integration. Four ranks: **0** Core Council; **1** Guardian (Ozone) / Core Entity; **2** Prime / Generator / Oracle Entity / Sequencer Entity / Pylon Entity; **3** Halo (4 Classes) / Folio. All non-rank-1 creations route through a **Guardian Accord** (auto-accord for Folios). Halos decompose into **Class** (shared PAU + beacon + buybox + factory) → **Book** (bankruptcy-remote balanced ledger) → **Unit** (liability in Halo's book, asset in Prime's). Operational beacon naming: per-Prime `baseline-{prime}` / `warden-{prime}-{op}` (class: relay) and `stream-{prime}-{actor}` / `principal-{owner}` (class: sentinel) for high-authority real-time control; per-Halo relays (`lcts-{halo}`, `nfat-{halo}`, `amm-{halo}`, `identity-{network}`) for deterministic action; rank-2 types use `market-data-*`, `attest-data-*`, `patch-*`, `sequencer-*`, `pylon-{entity}` classes (taxonomy in flux). Per-entity Reference Value formulas drive Growth Staking GF (most types 2.5×). The **Core Entity** unifies legacy/general-purpose ops (**halo mode**) and crisis-wrapper duty (**busted prime/halo mode**); future modes may be added. The **Pylon + Ring + Sequencer** model (Pylons take principal risk and contribute to per-Ring assurance funds; Rings live inside Sequencer entarts as sub-structures; Sequencers hold no collateral and bear only revocability-based trust) avoids the ADL pattern of perpetual exchanges via pre-funded mutualization + winner-haircut recovery.

## Section map

| § | Topic |
|---|---|
| 1 | Rank hierarchy + Guardian Accord + restructure types |
| 2 | Rank 1 — Guardian (Ozone), Core Entity (modes) |
| 3 | Rank 2 — Generator, Prime, Oracle Entity, Sequencer Entity, Pylon Entity (with Ring coalitions) |
| 4 | Rank 3 — Halo Class/Book/Unit + 4 Class types |
| 5 | Rank 3 — Folio |
| 6 | Beacon naming + Reference Value summary |

---

## §1 Hierarchy, accord, restructure

| Rank | Types | Governance |
|---|---|---|
| 0 | Core Council | Sovereign |
| 1 | Guardian (Ozone), Core Entity | Direct Core Council via SpellCore |
| 2 | Prime, Generator, Oracle Entity, Sequencer Entity, Pylon Entity | Accordant to a Guardian |
| 3 | Halo (4 Classes), Folio | Administered by a Prime; transitively accordant |

**Guardian Accord** (Request → Accord → Execution): operational gate for all rank-2/-3 creation. Rank-1 entities bypass and are SpellCore-created directly. Folios use a programmatic **auto-accord** (instant, fee-free).

| Creation Target | Flow |
|---|---|
| Folio | Auto-accord → instant; no fee |
| Standard Halo | Guardian Accord → admin-controlled (un-tokenized; can issue tokens later) |
| Prime | Guardian Accord → admin → **waiting period** (Synomic Entity Primitives locked) → token issuance (95% to creator, 5% creation fee) → Primitives unlock |
| Oracle / Sequencer / Pylon | Guardian Accord under SpellCore + 5% creation fee (Oracle/Sequencer tokenless or limited-token; Pylon tokenized — Prime-style 5% creation + 50 bps upkeep) |
| Core Entity (any mode) | SpellCore action — no Guardian Accord (rank-1 bypass) |
| Guardian | Governance + collateral |
| Generator | Governance (rare; foundational) |

**Synomic Entity Primitives** (Prime-only): receive Generator capital, ingression participation, originate risk capital (TEJRC/TISRC), settlement-cycle access. Locked during waiting period.

**Restructure types**: **Type 1** — A creates B, transfers assets in, receives ownership/tokens (Prime-target invokes waiting period + 95/5 fee). Available to all incl. Folios. **Type 2** — A spins ops + parts of synomic artifact into new admin-controlled Halo; optionally upgrades A's own type (Halo→Prime). A keeps identity + token; holders carry through. All except Folios. Open questions: Halo→Prime permissioning, Type 2 reversibility, Guardian selection mechanism, ongoing accord obligations. The 5% creation-fee discussion in `creation-restructuring.md` cross-links inline to `accounting/entity-fees.md` (canonical Entity Creation Fee 5%, Entity Upkeep 50 bps/yr, Cross-Entity Upkeep Rebate).

---

## §2 Rank 1 — Core-regulated entities

### Guardian (Ozone)

Single operational Guardian post-transition; consolidates legacy Facilitator / Aligned Delegate / Executor roles. Privileged operations under collateral + slashing. Legacy *Accordant* term retained for GovOps holding cBEAMs.

| Tier | Function | Slashing for |
|---|---|---|
| **Core Guardians** | Atlas interpretation, populate the 24-seat Core Council, oversee Operational Guardians | Misinterpretation, misalignment, bad-faith interpretation |
| **Operational Guardians (Ozone)** | Routine privileged ops for Primes/Halos | Execution failures; malicious behavior |

**Authority cascade**: SpellCore (16/24 hat) → Council Beacon → aBEAMs → Operational Guardian → cBEAMs → Accordant GovOps → pBEAMs → PAU ops. **Operational ORC = Rate Limit × TTS** (per `trading/sentinel-network.md`). Slashing: incorrect/failed/delayed = partial; bad-faith interpretation (Core only) = variable; malicious = full + exclusion. Collateral locked for the role term, released on exit after challenge period. **Guardian-collapse handling sits *outside* the two scoped Core Entity modes** (halo mode + busted prime/halo mode); the post-transition design assumes Ozone is the single operational Guardian, and a future Core Entity mode (e.g., a Guardian-wrap mode) or alternative Core Council protocol is expected to cover it. Ozone's ORC sized to cover the transition.

### Core Entity

Rank-1 tokenless Core Council vehicle — SpellCore-created, excluded from Growth Staking, no own collateral (extension of Core Council authority). The single type operates in one of several modes; **initially two modes are defined; future modes may be added** as new use cases emerge. Each instance is single-mode by default (immutable identity, like all Synomic Entities); to change mode, create a new entity.

**halo mode — Legacy Management / General-Purpose Ops.** Standardized wrapper for legacy protocol positions not yet operated by a Prime — Morpho vaults, Aave pools, SparkLend exposures, pre-Agent-framework RWA positions. Same risk framework + reporting as a Halo; Core-Council governance instead of Halo / Prime governance. Beyond legacy assets, also general-purpose: bridge-side custody, Core-Council-funded experiments, cross-Prime asset coordination. Indefinite term. **Exits:** transfer to Prime ownership (assets become standard Halos) or systematic wind-down.

**busted prime/halo mode — Crisis Wrapper for failed Prime or Halo.** Activated when a rank-2 Prime or rank-3 Halo collapses (insolvency, governance failure, security breach, fraud / misconduct requiring immediate operational takeover). Assumes operational control of the wrapped entity's mandate, downstream tree (the wrapped Prime's Halos, etc.), and associated risk capital (TEJRC / TISRC / srUSDS) under emergency SpellCore authority. **Resolution paths:** restoration (hand mandate back to a healthy Prime / Halo) / orderly wind-down / restructuring / loss absorption (waterfall in `risk-framework/capital-formula.md`). Dissolves once the wrapped entity is resolved. The wrapped entity's risk capital and any sized Guardian ORC fund the transition; the Core Entity inherits authority but not collateral risk.

**Out of scope for the initial two modes:** Guardian-collapse handling — expected to be addressed by a future Core Entity mode (e.g., a Guardian-wrap mode) or an alternative Core Council protocol. Cross-Guardian crisis is a flagged future concern.

Compared to a Guardian: tokenless, no collateral, direct Core Council authority via SpellCore (vs collateral-backed accord, slashable). Compared to a Prime: no Synomic Entity Primitives, no capital-deployment role. Compared to a Halo: no Class / Book / Unit structure; Core-Council-administered.

---

## §3 Rank 2 — Generator, Prime, and the new entity types

### Generator (USDS)

Singular per stablecoin; foundational; SpellCore-governed. Creates the medium *of* capital — does not allocate. Credit flow: Generator → Prime credit lines → Halos → returns flow back up. Operational beacon `lcts-{generator}` (class: relay) runs srUSDS LCTS. **Risk capital originated via Generator pBEAM**: only **srUSDS** (Senior Risk Capital, end-user held). Primes originate Prime-scoped TEJRC/TISRC via their own pBEAMs — Generator does not own these. Generator revenue (USDS fees, spread, risk-capital fees, USDS SDR income) split 95/5 with Sky Core.

### Prime

Heavyweight billion-scale capital allocators. Two categories:

| Category | Members | Status |
|---|---|---|
| **Star Primes** | Spark, Grove, Keel, skybase, launch6 | Operational |
| **Institutional Primes** | Obex | Operational — incubates new Primes and Halos (meta-structural) |
| **Seventh Prime** | TBD | Active in P1 topology; concrete naming can land as a phase-boundary update |

Phase 1 v4 topology has **7 active Primes**. The five Star Primes are the "Genesis Stars" eligible for the Pioneer Star System; Obex remains the Institutional Prime; the seventh Prime is active in topology even if its final public name remains TBD.

**Infrastructure**: SubProxy + standard PAU + sentinel formation (per-Prime `baseline-{prime}` / `warden-{prime}-{op}` relays + `stream-{prime}-{actor}` sentinels) + governance token + primebook. SORL-bound rate-limit increases (25%/18h); decreases instant.

**Governance**: PRIME-token SpellGuards (core spell payload + Prime-token hat); Prime is rank-2 administrator of its Halos; accordant to Ozone. Token-holder rights bounded by inalienable claims in the Prime's synomic artifact.

### Oracle Entity *(stub spec)*

Domain-specific data provider; tokenless rank-2. First-class entity rather than a universal `&core.oracle` Space. Owns its own beacon cert chain + per-entity registry config; independently revocable; bears slashing for misbehavior (stale / missing data, incorrect attestation, collusion). One Oracle Entity per data domain — Phase 1 names two instantiations:

| Entity | Domain |
|---|---|
| **Crypto Majors Oracle** | Market-memory reducer outputs and current-state atoms for BTC/ETH/stETH/USDC/USDT: price, peg/basis, volatility, correlation, depth/impact, liquidation overhang, funding/OI, rates/macro, data quality |
| **Book Attestation Oracle** | Cert chain for class-accordant attest-data beacons. Custodial-crypto uses borrower admission plus riskbook/exobook attestation surfaces; legacy-halo exsyn-TRRC claims **out of scope** here |

The split is by trust model: market data is objective and oracle-pushable from public venues; attestation is signed claims about exobook state the synome can't directly verify (custody balances, exobook structural integrity).

**Beacon classes** (two, input class per beacon framework): `market-data-beacon` (`&core.loop.market-data`, push market-memory reducer outputs and current-state atoms to the Oracle Entity entart), `attest-data-beacon` (`&core.loop.attest-data`, walk borrower / riskbook / exobook state + sign attestation atoms into the target risk class or book). **Operational verbs**: `market-data-write-memory`, `post-borrower-admission`, `post-riskbook-attestation`, `post-exobook-attestation`.

**exsyn-TRRC mechanism is not an Oracle Entity beacon.** Per-Prime exsyn-TRRC scaffolding is handled by govops-operated **patch-beacons** sudoed directly into each `&entity.prime.{id}.primebook` at genesis — unregulated scaffolds (no framework, no loop template, no oracle-entity ownership), designed to sunset as insyn coverage grows. Discipline borne by govops, not oracle-entity slashing.

Default-deny is the safety baseline (no fresh accordant attestation → exobook excluded from rollup). Open: fee model for tokenless entities, slashing magnitudes, decentralization requirements (multi-source vs single-provider), cross-entity data dependencies (e.g., attest-data-beacons reading market-data feeds), future entity types (off-chain rates, cross-chain state, equities).

### Sequencer Entity *(stub spec)*

Orderbook sequencer / matcher — sees order flow, runs matching algorithm, returns trade prints; **also hosts Rings as sub-structures inside its entart** (Rings live at `&entity.sequencer.{id}.ring.{ring-id}`). **No inventory, no principal positions, no collateral, no slashing, no participation in any loss waterfall** (this is the key separator from Pylon Entity). Tokenless or limited-token; rank-2; one Sequencer Entity per matching venue. Orderbook matching is a first-class entity rather than a Halo class. **Trust enforcement is purely revocability-based**: synomic registry as audit trail (order receipt → sequence → match log), Oracle-Entity audit of behavior, Core Council retirement on misbehavior. Sequencer's only skin in the game is the right to operate; revocation is catastrophic for the operating organization. Analogous to a registered exchange — operational trust enforced externally rather than capital-bearing.

**Use cases**: derivatives matching (host Rings under which Pylon Entities take principal positions and contribute to the Ring's assurance fund); spot trading (orderbook for tokenized assets — PT/YT, halo units; no Ring needed); cross-Halo unit secondary markets. Multiple Sequencer Entities can coexist; consumers route to whichever Sequencer supports their products. Sequencer Entities are independent — not bound to any specific Pylon or Ring.

**Beacon classes** (TBD): likely `sequencer-receive` / `sequencer-match` / `sequencer-cancel` (core matching), plus `sequencer-ring-admin` (process Ring-level accord operations) and `sequencer-recovery` (execute Ring recovery-tool sequence). **Capital model**: none. No operational collateral, no slashing bond. Operational-harm recourse is a known gap — there's no automatic on-chain financial recourse for Sequencer misbehavior beyond revocation; severe harm escalates to Core Council governance, potentially restitution from Sky ABC if systemically significant. Open: sequencing model, matching algorithm and order types, censorship resistance, MEV evidence trail, fee structure (per-trade / Ring-hosting subscription / split with Sky Core), relationship to LCTS, cross-Sequencer price coherence, Hyperliquid analog.

### Pylon Entity *(stub spec)*

Broker-dealer analog — takes principal positions in derivatives, faces Primes / Folios as customers, contributes to Ring assurance funds, absorbs own customer-default losses with own capital. **Tokenized** (Pylon governance token; decentralized capital-weighted governance via token holders, Prime-style). Standard **5% creation fee + 50 bps/yr upkeep** applies. Multiple Pylons coexist; a Pylon may belong to one or more **Ring coalitions** across one or more Sequencer Entities.

**Ring coalition** — an inter-Pylon accord pattern, *not itself an entity*. **Lives inside the hosting Sequencer Entity's entart** (e.g., `&entity.sequencer.{seq-id}.ring.{ring-id}`). Each Ring is parameterized by product, Pylon membership (≥2 Pylons), assurance-fund target, margin schedules, and recovery-tool spec. **Minimum viable Ring = ≥2 Pylons + ≥1 Sequencer + accord protocol.** Pylons may have criss-cross memberships (Sequencer A hosts BTC perps with Pylons P1-P4; Sequencer B hosts its own BTC perps with P3, P4, P7-P9; same P1 may participate in three Rings across two Sequencers). Per-Ring pledges are siloed. **Ring creation is a product decision, not an entity-creation decision** — coalition proposes parameters, Sequencer instantiates, Pylons pledge. Value capture (creation fee + upkeep) accrues at Pylon level; Rings have no entity fees because they aren't entities.

**Three-layer capital structure**: (1) Sky regulatory minimum (entity-viability floor; never touched by trading); (2) Extra capital (voluntary cushion; absorbs Pylon's OWN customer-default residuals first; **NOT touchable by Ring mutualization**); (3) Per-Ring pledges (contributions to specific Rings' assurance funds; consumed in mutualization waterfall). The asymmetry is the key property: **extra capital is at risk only when the Pylon's own underwriting fails; other Pylons' failures can only reach the Pylon's per-Ring pledges, never its general balance sheet.** This is the FCM/CME structure transcribed (extra capital = ANC analog; per-Ring pledge = guaranty-fund contribution analog).

**Two waterfalls** with cleanly separated cascades:

| Waterfall | When | Layers |
|---|---|---|
| **Own-customer default** | Pylon X's customer defaults in Ring R | (1) customer margin; (2) Pylon X's extra capital; (3) Pylon X's per-Ring-R pledge; (4) surviving Pylons' per-Ring-R pledges; (5) VMGH on Ring R winners |
| **Ring mutualization** (peer-Pylon-failure triggered) | Pylon Y in Ring R has been exhausted by Y's own customer default | (1) defaulter Y's per-Ring-R pledge; (2) surviving Pylons' per-Ring-R pledges only — **extra capital is NOT touched**; (3) VMGH |

**What's absent**: no Sequencer participation (no collateral); no Ring-entity SITG (no Ring entity); **no assessments** (Pylons commit at most pre-funded pledges; no callable layer); no Sky backstop in normal operation (recovery tools cap loss; ABC backstop only for Core-Council-sanctioned systemically-significant Rings, exceptional not default). **LSOC-style customer collateral segregation**: customer margin held in dedicated synomic structures, bankruptcy-remote, not Pylon equity; capital-adequacy calibrated against gross customer risk margin (Reg 1.17 8% analog).

**SORL-bounded pledge rebalancing**: pledge increases instant, decreases gated by epoch boundary + lockup; full Ring exit requires longer lockup with continued obligation through window (prevents reactive escape from mutualization). **Differentiation**: pricing (effective spread above raw Ring matching cost); relationship structure (capacity reservations, volume tiers, preferred routing); Ring portfolio (specialization vs broad participation); capital efficiency. **Cross-margin offset between Rings is a Pylon-level commercial product, not a Ring-level rule** — Pylons broad across correlated Rings can offer cross-margin packages single-Ring Pylons can't match (FCM-style bundling moat).

**Regulation via risk treatment**: Core Council doesn't directly approve Rings. Prime CRR for Ring-issued units reads Ring characteristics (coverage ratio, Pylon HHI, attestation cadence, recovery-tool spec) from the risk-framework risk form. Weak Rings get high CRR → Primes need more TRC → demand drops → Ring reforms or dies. **Macroprudential regulation via risk-form tuning**, analogous to Basel risk weights.

**Beacon classes** (TBD): `pylon-{entity}` (high-authority action; class: relay), `pylon-monitor-{x}` (low-authority observation; class: relay), sentinel formations (per-Pylon `baseline-{pylon}` / `warden-{pylon}-{op}` relays + `stream-{pylon}-{actor}` sentinels) for real-time risk at later phases. Customers (Primes, Folios, other entities) sign bilateral terms with Pylons — naturally encoded as ecosystem accords for pre-negotiated relationships.

Open: per-Pylon floor + Cover-N target calibration, pledge-rebalancing friction parameters, customer abstraction (on- vs off-synome), cross-margin product spec template, liquidation mechanics, default-cascade response, sentinel-formation operation, Sky-backstop sanctioning criteria for systemically significant Rings, recovery-tool default templates, attestation cadence floor.

---

## §4 Rank 3 — Halos (Class / Book / Unit + 4 Class types)

### Layered architecture

`Class` (shared PAU + beacon + legal buybox + factory) → `Book` (balanced ledger, bankruptcy-remote isolation boundary; pari-passu within, fully isolated across; blended assets enable privacy; recursive) → `Unit` (liability in Halo book ↔ asset in Prime book; specific terms, transferability).

**Unit-to-Book mapping**: 1:1:1 | many Units : 1 Book (privacy-blended) | recursive (tranching). **Book lifecycle**: Created → Filling (USDS at agent rate, low CRR) → Deploying (high CRR — "Schrödinger's risk" obfuscation) → At Rest (attested, medium CRR; re-attestation cadence affects CRR) → Unwinding → Closed. Numeric CRRs owned by `risk-framework/capital-formula.md`.

**Legal mapping**: BVI SPC (entity/segregated portfolio/share) is materially stronger than Delaware Series LLC — BVI segregation is statutorily court-tested; Delaware untested. Hybrid at scale: statutory for high-value books, contractual for smaller.

**Spectrum**: Standard Classes (Portfolio/Term/Trading) + Special Classes (Identity Network only — orderbook matching lives at rank-2 as Sequencer Entity, not as a Halo class). Halos span minimal (no token, autonomous lifeform) → complex governed institutional products. **Halo Units excluded from Growth Staking** (passive yield wrappers). Early-stage Halos with no earnings can still earn GF 2.5× if synomic artifacts demonstrate genuine deployment.

### Four Class types

| Class | Token | Beacon(s) | Mechanism | Use |
|---|---|---|---|---|
| **Portfolio** (Standard) | LCTS — pooled, fungible | `lcts-{halo}` (relay) | Queue → generation lock/settle → fungible shares | Open participation, uniform terms; capacity-constrained strategies; redemption with settlement delay (RWA, T-bills, MMFs, CLO tranches) |
| **Term** (Standard) | NFATS — non-fungible, bespoke | `nfat-{halo}` (relay, executor) + `attest-data-{provider}` (input) | **Two-beacon deployment gate**: attestation must be present before book → deploying | Asset-manager partnerships; negotiated terms; transferable/collateralizable positions |
| **Trading** (Standard) | LCTS-shaped pool shares | `amm-{halo}` (relay, executor; can upgrade to sentinel formation) | Oracle-referenced AMM (NOT constant-product — no impermanent loss) | Instant settlement for RWAs (T-bill T+1, captures spread); active MM (JAAA, ecosystem tokens). Can only trade Configurator-onboarded assets |
| **Identity Network** (Special) | (no capital-deployment Units) | `identity-{network}` (relay) | On-chain registry (simple address set) + off-chain legal KYC entity; Synome holds attestation metadata | KYC/identity for permissioned tokens (US Accredited, Non-US QIB, Institutional). Token issuer configures accepted networks |

### Class-specific architectural invariants

- **Portfolio**: LCTS solves pooled-redemption fairness. Once a new Unit is properly onboarded, **every Prime simultaneously rebalances into it** via sentinel formations — coordinated deployment, not gradual ramp. Tranching = same Class, multiple Units (Senior/Junior).
- **Term**: Two-beacon gate is the invariant — `attest-data-{class}` (independent Sky-whitelisted Attestor; **cannot** move capital, mint, or change book status) writes attestations into Synome; `nfat-{halo}` (relay) cannot transition book → deploying without attestation. Buybox (e.g. 6-24mo / 5M-100M / 8-15% APY) defines autonomous-operation envelope. Two terms-source modes: General buybox vs **Ecosystem accord** (pre-negotiated, overrides buybox). Re-attestation cadence at At-Rest affects CRR. Privacy: blended assets per book → individual loan terms unrecoverable from NFAT data.
- **Trading**: Oracle-referenced AMM (no impermanent loss). Spread tiers ~2-100 bps by asset type; capital-turn math T+1 ≈ 250 turns/yr (~12.5% at 5 bps). Sentinel-upgrade path for active MM. Emergency: oracle-deviation auto-pause; GovOps instantly drops rate limits to zero. Can only trade Configurator-onboarded assets.
- **Identity Network**: Restricted Halo — **prohibited** from deploying capital, accepting investment deposits, or issuing yield-bearing tokens. Permitted: registry, KYC legal entity, fees, governance token, cross-recognition. On-chain interface intentionally minimal (`isMember/add/remove/batch`); heavy lifting (attestation type, expiry, linked addresses, jurisdiction) in Synome; KYC documents + personal identity off-chain. Multi-address per entity; expiry/revocation removes ALL linked addresses. Restrictions enforced at the **token level** — when a Halo Unit / Prime token is configured with accepted networks, transfers revert if the recipient is non-member; trading venues inherit automatically.

---

## §5 Rank 3 — Folio

Standardized supply-side holding structure — both on-chain agent (PAU + teleonome) and principal-controlled vehicle linked to legal entities. Tokenless; no Units; single owner; instant creation via auto-accord. **Required vehicle for Growth Staking**: PAU holds staked SKY + growth assets + strategy positions; at each daily settlement (target arch), system measures total staking factor and airdrops reward. Reinvestment: when SF capacity exists, stake more SKY; when at capacity, acquire growth assets (expanding capacity). Sentinels can automate the cycle.

**Principal + Directive**: principal's primary control instrument is the **directive** — human-language investment philosophy / risk appetite / constraints. Automated mode: Baseline follows directive. Principal-control mode: principal executes against directive directly.

| Mode | Beacons | Notes |
|---|---|---|
| **Automated** | `baseline-{folio}` / `warden-{folio}-{op}` (relay) + `stream-{folio}-{actor}` (sentinel) | Standard formation; same protection as Prime-scale capital |
| **Principal Control** | `principal-{owner}` (sentinel, variant principal-sentinel; no formation) | Direct PAU control; no Guardian Accord, no Baseline service, no GovOps intermediary. Rate limits apply but formation-level protections (Baseline fail-safe, Stream/Warden monitoring, Guardian collateral) absent. Expected users: companies already running Streams elsewhere |

**Folio ≠ Halo — relationship is inverted**. A Halo wraps a legal entity (Halo is outer shell). A Folio is controlled BY the principal *through* legal entities (entity structure is the principal's governance surface). Standardized best-practice legal structures available off-the-shelf, or principals supply their own. **Restructuring**: Type 1 only (no Type 2).

---

## §6 Beacon naming + Reference Value

### Beacon identifiers (legacy retained where they exist; new rank-2 classes are **in flux** — see per-type stub specs; classified per `macrosynomics/beacon-framework.md`)

| Pattern | Class | Used by |
|---|---|---|
| `baseline-{x}` / `warden-{x}-{op}` (relay), `stream-{x}-{actor}` (sentinel) | High-authority action — sentinel formation | Prime, Folio (auto), Halo (sentinel-upgraded Trading) |
| `principal-{owner}` (sentinel, variant principal-sentinel) | High-authority action — principal sentinel (no formation) | Folio (principal-control) |
| `lcts-{x}` (relay) | High-authority action — executor (deterministic) | Generator, Portfolio Halo |
| `nfat-{x}` (relay) | High-authority action — executor | Term Halo |
| `attest-data-{provider}` | High-authority **input** — attestor (replaces legacy `lpha-attest-{provider}`) | Term Halo (independent Sky-whitelisted; cannot move capital) |
| `amm-{x}` (relay) | High-authority action — executor (sentinel-upgradable) | Trading Halo |
| `identity-{network}` (relay) | High-authority action — executor (sole registry writer) | Identity Network |
| `market-data-{domain}-{provider}` | Input — `market-data-beacon` class; push market-memory reducer outputs and current-state atoms | Oracle Entity (Crypto Majors) |
| `attest-data-{halo-class}` | Input — `attest-data-beacon` class; walk exobook + sign attestation atom | Oracle Entity (Book Attestation) |
| `patch-{target}` | `patch-beacon` class — govops-sudoed scaffold, no oracle-entity ownership, no regulated framework, designed to sunset | govops (Phase 1 use: per-Prime exsyn-TRRC writes into `&entity.prime.{id}.primebook`) |
| `sequencer-receive / match / cancel`, `sequencer-ring-admin`, `sequencer-recovery` | TBD — sequencing / matching / cancel / Ring admin / recovery-tool execution | Sequencer Entity |
| `pylon-{entity}` (relay), `pylon-monitor-{x}` (relay) | High-authority action + low-authority observation | Pylon Entity |

Sentinels have **call-out density** + continuous real-time control; relay-class beacons execute pre-agreed deterministic rules. See `noemar-synlang/synlang-patterns.md` §6 for the bridging continuum.

### Reference Value formulas (Growth Staking)

| Entity | Formula | GF |
|---|---|---|
| **Generator** | `(Revenue × Actual P/E + ISRC Book Value) / Tokens` | 2.5× |
| **Guardian** | `(Accord Fee Income × Actual P/E + SKY Holdings Book Value) / Tokens` (sUSDS-as-collateral feeds P/E component, not double-counted) | 2.5× |
| **Prime** | `Net Capital Reserves / Tokens` (no P/E; look-through to held Halo tokens; Floor `min(RV, Market)`) | 2.5× governance, ~1.67× TEJRC |
| **Halo** | `(Capital Reserves + Annual Earnings × Actual P/E) / Tokens` | 2.5× |
| **Pylon** *(stub)* | TBD — tokenized (governance token; capital-weighted decentralized governance), Prime-style 5% creation + 50 bps upkeep | TBD (likely 2.5×) |
| **Oracle / Sequencer** *(stub)* | TBD — tokenless; fee-model open (Entity Creation Fee 5% + Upkeep 50 bps/yr applicability open) | n/a (tokenless) |
| **Folio** | (no governance token; Folio is the *vehicle* for growth assets) | — |
| **Core Entity** | (excluded) | — |

Detailed treatment in `growth-staking/growth-staking.md` §2 + §4.3-§4.6.

---

## Key vocabulary

| Term | One-line |
|---|---|
| **Synomic Entity** | Sky's autonomous on-chain agent (legacy: "Synomic Agent" / "Sky Agent") |
| **Guardian Accord** | Bilateral agreement with Ozone enabling rank-2/-3 creation; auto-accord variant for Folios |
| **Type 1 / Type 2 Restructure** | A creates B with assets transferred / A spins ops into a new Halo it controls (optional Halo→Prime upgrade) |
| **Synomic Entity Primitives** | Prime-exclusive capabilities (Generator capital, ingression, originate risk capital, settlement access); locked during waiting period |
| **Halo Class / Book / Unit** | Shared infra unit / bankruptcy-remote ledger / liability-asset connector |
| **Buybox** | Class-defined autonomous-operation envelope |
| **Two-beacon deployment gate** | Term Halo invariant — attestor gates `nfat-{halo}` book transition |
| **Ecosystem accord** | Pre-negotiated Term Halo terms overriding buybox |
| **Schrödinger's risk** | Deploying-phase Term-book obfuscation (high CRR until At Rest) |
| **Directive** | Folio principal's human-language guidance |
| **Principal sentinel** | Folio direct PAU control (no formation) |
| **Star / Institutional Prime** | General-purpose vs meta-structural Prime category |
| **Pioneer Star System** | The five Genesis Star Primes' status (mechanics in `accounting/distribution-rewards.md`) |
| **Core Entity halo mode / busted prime/halo mode** | Single rank-1 type; initially two scoped modes — halo mode (legacy/general-purpose ops, old "Core Halos") and busted prime/halo mode (wraps a failed Prime or Halo, old "Recovery Entity"). Future modes possible (e.g., Guardian-wrap). |
| **Oracle Entity** | Domain-specific tokenless rank-2 data provider with own beacon cert chain (replaces universal `&core.oracle` Space) |
| **Sequencer Entity** | Rank-2 orderbook sequencer / matcher + Ring host; no inventory; no collateral; no participation in any loss waterfall; trust by revocability |
| **Pylon Entity** | Rank-2 broker-dealer member analog; takes principal positions in derivatives; three-layer capital (regulatory minimum + extra capital + per-Ring pledges); extra capital absorbs own customer defaults but is shielded from Ring mutualization |
| **Ring coalition** | Inter-Pylon accord pattern hosted inside a Sequencer's entart (not itself an entity) — shared assurance fund + mutualized default exposure; replaces ADL with pre-funded mutualization + VMGH winner haircut |
| **Assurance fund** | Aggregate of Pylons' per-Ring pledges; the Ring's mutualized default-absorption pool |
| **VMGH** | Variation margin gains haircutting — recovery tool consuming winners' gains pro-rata when assurance fund is exhausted |

---

## Cross-references

- `macrosynomics/synomic-entities.md` — Synomic Entity theory (canonical home)
- `macrosynomics/beacon-framework.md` — beacon taxonomy
- `smart-contracts/architecture-overview.md`, `configurator-unit.md`, `lcts.md`, `nfats.md` — PAU + four-layer flow; BEAM cascade; token standards
- `smart-contracts/fixed-rates.md` — PT/YT use case for Sequencer Entity
- `risk-framework/book-primitive.md`, `halobook-layer.md`, `primebook-composition.md`, `capital-formula.md` — formal book structure; CRR; loss waterfall
- `trading/sentinel-network.md` — formation spec; TTS-driven ORC
- `noemar-synlang/synlang-patterns.md` §6 — call-out continuum; `runtime.md` §3-§7 — cert/auth chain
- `governance/spellguard.md`, `core-council-elections.md` — SpellCore + 24-Council elections
- `growth-staking/growth-staking.md` — GF tiers + Reference Value formulas
- `synoteleonomics/recipe-marketplace.md` — Streaming Accord; entity-operating work pricing
- `accounting/entity-fees.md`, `distribution-rewards.md` — fees; DR/SDRR/Pioneer Star System
- `roadmap/phase-1-spaces.md` — Phase 1 v4 topology (66 fixed Spaces, 7 Primes, 3 P1 Halos, DSC, treasury, market-memory oracle)

---

## File map

| File | What's in it the summary doesn't have |
|---|---|
| `creation-restructuring.md` | Worked Type 1 (Folio → "Alpha" Prime: before/during/after with token splits); worked Type 2 (Halo "Beta" upgrades to Prime, spins ops into "Beta Operations"); rank-1 creation paths for both Core Entity modes (halo mode indefinite, busted prime/halo mode crisis-temporary); full open-questions table; inline link to `accounting/entity-fees.md` at the 5% creation-fee mention |
| `guardian.md` | Full slashing-condition table; lifecycle phases (Registration / Operation / Exit); sUSDS-as-collateral non-double-counting detail; full authority cascade diagram; Crisis Successor section explicitly notes Guardian-collapse handling sits *outside* the two scoped Core Entity modes (future Guardian-wrap mode or alternative protocol expected) |
| `core-entity.md` | Full halo mode / busted prime/halo mode table treatment ("initially two; future modes may be added"); legacy-asset examples (Morpho/Aave/SparkLend); busted-mode activation triggers (Prime collapse, Halo collapse, misconduct) + resolution-path table (restoration / wind-down / restructuring / loss absorption); comparison vs Guardian / Prime / Halo; future-mode open question (e.g., Guardian-wrap); single-mode-per-instance default (immutable identity) |
| `generator.md` | Full credit-flow diagram; explicit Prime ↔ Generator risk-capital ownership distinction; 95/5 revenue split |
| `prime.md` | Star vs Institutional categorization; six named operational Primes plus the seventh active P1 topology slot; waiting-period Primitives-locked detail |
| `oracle-entity.md` | Phase 1 instantiations (Crypto Majors market memory / Book Attestation, latter narrowed to attestor cert chain only) with split rationale (objective reducer outputs vs signed-claim trust models); two beacon classes (`market-data-beacon`, `attest-data-beacon`); per-Prime `patch-beacon` scaffolds for exsyn-TRRC sudoed into each primebook; operational verbs; trust-model + default-deny safety baseline; open-questions list (fees, slashing magnitudes, decentralization, cross-entity data dependencies, future entity types) |
| `sequencer-entity.md` | What-distinguishes (sees order flow, sequences, hosts Rings as sub-structures, no principal positions, NO collateral); trust-by-revocability rationale; Ring-hosting mechanics (Rings live inside Sequencer entart; criss-cross Pylon membership across Sequencers); use cases (derivatives matching with Pylon principal-bearing; spot trading; cross-Halo unit secondary); full open-questions list (sequencing model, matching algo, censorship resistance, MEV evidence, fees / Ring-hosting subscription, LCTS relationship, cross-Sequencer coherence, operational-harm recourse gap, Hyperliquid analog) |
| `pylon-entity.md` | Three-layer capital structure (Sky regulatory minimum + voluntary extra capital + per-Ring pledges); two-waterfall design (own-customer default vs Ring mutualization) with extra-capital asymmetry (only at risk from own underwriting, shielded from peer-Pylon failures); LSOC-style customer collateral segregation; Reg 1.17 8%-of-risk-margin analog calibration; Ring lives in Sequencer entart with criss-cross membership across Sequencers; Ring creation as product-listing-not-entity-creation; SORL-bounded pledge rebalancing; two-layer risk management (Pylon-to-Ring uniform vs Pylon-to-customer bilateral); pricing + relationship + Ring portfolio as differentiation surface; cross-margin offset as Pylon-level commercial product (FCM-bundling moat); assurance-fund sizing rule (per-Pylon floor + Cover-N target); recovery-tool taxonomy (VMGH default + optional tear-up / forced allocation / dissolution); regulation-via-risk-treatment lever (Core Council tunes the risk form for Ring units, not directly approving Rings); open-questions list |
| `halo-classes.md` | Full Class/Book/Unit decision matrix; recursive book example; book-lifecycle CRR phases; CLO senior/junior worked example; 1:1:1 degenerate case; full BVI vs Delaware mapping; "4 Class types" enumeration (Standard: Portfolio/Term/Trading; Special: Identity Network) |
| `halo-portfolio.md` | "Every Prime simultaneously rebalances" capital-efficiency thesis; Class-level tranching diagram; Halo Artifact vs Unit Artifact split; launch table; Fortification Conserver as default-ownership backstop |
| `halo-term.md` | Full two-beacon ASCII sequence; 8-step capital-flow lifecycle; example buybox values; sentinel-vs-`nfat-{halo}` comparison; ~4-8wk launch timeline |
| `halo-trading.md` | Daily `amm-{halo}` cycle; spread-by-asset table; capital-turns-per-year math; oracle-referenced vs constant-product rationale; emergency response; ~2-3wk launch timeline |
| `halo-identity-network.md` | Permitted vs prohibited matrix; full fee taxonomy; on-chain registry interface; multi-address rules; KYC processing flow; regulatory compliance scope (AML/KYC/GDPR/CCPA/sanctions); revocation triggers; example networks table; full open-questions list; "Connection to Trading Venues" (token-level enforcement, settlement-revert mechanic) |
| `folio.md` | Full PAU contents example; reward reinvestment cycle; Folio ↔ Halo property comparison; legal-structure inversion explanation; both operating-mode beacon sets in detail |
