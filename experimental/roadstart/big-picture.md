# Big Picture — Background for Roadmap Work

Just the broader architecture roadmap work touches. Pared to what grounds P1; forward-looking systems get pointers only. Source: `lani/summaries/` (file map at bottom).

## What Laniakea is

Sky's automated capital-deployment infrastructure on USDS. The **synome** = the whole architecture as a single object: replicated **synart** (public artifact) running on a synomic runtime, hosting **Synomic Entities** (ledger-native autonomous agents) operated by external **teleonomes** through regulated apertures called **beacons**.

**Five-layer architecture** with three artifact tiers:

| L | What | Artifact |
|---|---|---|
| 1 | Synome — Atlas, Axioms, Library, Language Intent | **synart** (replicated; public; same across all participants) |
| 2 | Synomic Entities — Generators, Primes, Halos, Folios, Guardian (Ozone), Oracle/Sequencer/Pylon Entities | synart |
| 3 | Teleonomes — private cognitive entities operating beacons | **telart** (per-teleonome; private) |
| 4 | Embodiments — hardware-bearing process instances | **embart** (per-emb; private) |
| 5 | Embodied Agents — ephemeral processes | ephemeral |

L1–2 are public, replicated, regulated. L3–5 are private. **P1 builds L1–2 substrate.**

**Dual architecture** (cross-cuts every layer): sparse **deontic skeleton** (axioms, rules — `(1,1)` once set, governance-paced) + dense **probabilistic mesh** (probmesh — `(strength, confidence)` beliefs, evidence-driven). P1 is essentially the deontic skeleton; probmesh is forward-looking.

## Synomic Entity ranks

| Rank | Types | Governance |
|---|---|---|
| 0 | Core Council (24 Guardians) | Sovereign |
| 1 | Guardian (Ozone — single operational), Core Entity | Direct Core Council via SpellCore |
| 2 | Prime, Generator, Oracle Entity, Sequencer Entity, Pylon Entity | Accordant to a Guardian |
| 3 | Halo (Portfolio / Term / Trading / Identity Network classes), Folio | Administered by a Prime |

**P1 inventory:** 1 Generator (USGE → USDS), 1 Oracle Entity (Crypto Majors — market memory), 7 Primes (Spark, Grove, Obex, Keel, Skybase, Launch6, + 1 TBD), 3 Halos (spark-term, grove-term, maple-term — all `nfat-term` halo class × `custodial-crypto` risk class).

**Halo decomposition:** Class (shared PAU + beacon + buybox + factory) → Book (bankruptcy-remote balanced ledger) → Unit (liability in Halo, asset in Prime). 1:1 simple; many-units:one-book for privacy-blending; recursive for tranching.

Out of P1: Core Entity (legacy/crisis-wrapper umbrella), Sequencer/Pylon/Ring (derivatives), Halo classes other than `nfat-term`, Folios. Pointers in `summaries/synomic-entities.md`.

## Beacon taxonomy

6 beacon classes + synserv (canonical: `macrosynomics/beacon-framework.md`):

| Class | I/O | What it does |
|---|---|---|
| `market-data-beacon` | input | Pushes market-memory reducer outputs + current-state atoms (Oracle-Entity-admin'd). |
| `attest-data-beacon` | input | Signed boolean claims (borrower admission, riskbook / exobook attestation). |
| `patch-beacon` | input | Govops-sudoed scaffold for exsyn coverage gaps. **No regulated framework.** Designed to sunset. |
| `synops-beacon` | action | In-synome operational mutation only; no external/mainnet actuation authority. P1 use: Halo borrower-inclusion / class-modification requests to Core govops and book-accounting assignment after relay receipts exist. |
| `relay` | action | External/onchain actuation + the corresponding in-synome operational record. Synart-resolved loop body; operated by the relevant govops. |
| `sentinel` | action | Cognitive call-out density into operator telart. Variants `stream-{x}` (proposes intent to baseline-relay) and `principal-{owner}` (direct PAU control with own cognition). Phase 9+. |
| `synserv` | special | Central synomic node operated by Core Council govops. Sole canonical sequencer of accepted synart writes; runs `&core.loop.synserv` heartbeat with hot standby. |

`endoscraper` is **not** a beacon class — chain reads are grounded execution through the `CHAINREAD` sigil, resolved by Noemar through a binding to an implement backed by a workcell. Global protocol refs such as Configurator Unit addresses live in `&core.registry.protocol`; per-entity chain-contract metadata lives in per-entart `protocol-registry` sub-Spaces (each Prime, Halo, and the Generator owns its own local PAU / protocol refs).

P1 beacons are deterministic programs operated by govops. `relay` is reserved for coupled external action + synome-recording authority: a relay may write operational atoms, but those writes must be tied to a planned, executing, or confirmed external action or to a lifecycle transition required to execute or record it. Pure synome-only administration uses `synops-beacon`, not relay; in P1 this covers `synops-halo-{id}` borrower-inclusion requests, class-modification requests, and in-synome book-accounting assignments that rely on existing relay receipts. Sentinel formations (baseline-relay + warden-relay + stream-sentinel for Primes) activate Phase 9–10.

## Smart-contract layer (chain side)

**PAU** (Parallelized Allocation Unit) = Controller + ALMProxy + RateLimits — the reusable building block deployed at every layer (Generator / Prime / Halo / Foreign). Diamond PAU (EIP-2535 facets) is the planned upgrade for the 24KB bytecode limit.

**Configurator Unit** (BEAMTimeLock + BEAMState + Configurator) sits above PAUs:

| Role | Holder | Action | Timelock |
|---|---|---|---|
| **aBEAM** | Core Council | Register PAU; add init rate-limit / controller action; grant cBEAM | 14d (additions); instant (revocations / decreases / pause) |
| **cBEAM** | GovOps (accordant to PAU) | `setRateLimit` against existing init; `callControllerAction`; `setRelayer` | SORL on increases; instant on decreases |
| **pBEAM** | Relay (keeper) | Direct execution within rate limits | — |

**SORL** (Second-Order Rate Limit on rate-limit increases) — canonical defaults: `hop=18h`, `maxChange=25%`. **IRL** (Initial Rate Limit) — adopted $100K. SORL parameter home: `smart-contracts/configurator-unit.md`. Attack-model derivation (Type 1 config theft vs Type 2 slippage extraction): `smart-contracts/rate-limit-attacks.md`. Combined harm at adopted parameters ~$2.36M per attack-surface group.

**LCTS** (Liquidity Constrained Token Standard) — queue-based for capacity-constrained conversions (srUSDS, TEJRC, TISRC, Portfolio Halo Units). Daily lock 13:00 UTC, settle by 16:00 UTC (aligns with DSC). Single-generation hard-lock model. Driven by `lcts-{halo}` (relay).

**NFATS** (Non-Fungible Allocation Token Standard) — per-deal ERC-721 for Term Halos. **Halo Unit** (liability, ERC-721) ↔ **Halo Book** (asset side, bankruptcy-remote balanced ledger). Two-beacon deployment gate: independent `attest-data-{class}` (cannot move capital) attests before `nfat-{halo}` (relay, executor) transitions a book to deploying. Lifecycle: CREATED → FILLING (USDS) → DEPLOYING (obfuscated, high CRR) → AT REST (attested, medium CRR) → UNWINDING → CLOSED.

**Yield Splitter** — single contract splitting any LCTS or ERC-4626 token into PT (principal) + YT (yield) ERC-20 pairs at a `(token, maturity)` bucket. Trading venue-agnostic; most-likely first venue is a Trading Halo AMM (Phase 5+). Deferred.

## Noemar / synlang substrate

**Synart is the program.** Runtimes (Noemar is one implementation) are interpreters. **Identity-driven boot:** `noemar boot --identity=X` resolves a loop Space pointer in `&core.registry.beacon` and evaluates `(run-forever)` with that Space as `&self`. P1 bootstrap lives at `&core.bootstrap`: a one-shot boot Space that materializes implement code blobs, binds sigils, registers workcell hubs from the installer manifest, emits boot receipts, and then becomes inert.

**Topology:** tree of entarts (one per Synomic Entity, rooted at one root Space) plus universal `&core.*` Spaces. Six-layer synome root: **constitutional** (`&core.root`, `&core.telos`, `&core.governance`, with P1 request intake at `&core.governance.requests`) / **framework** (`&core.framework.*` — empty in P1) / **registry** (`&core.registry.*`, including `&core.registry.beacon` and `&core.registry.protocol`) / **aggregation** (`&core.settlement`) / **executable** (`&core.bootstrap`, `&core.syngate`, `&core.loop.*`, `&core.relay.govops`, `&core.recipe.*`) / **library** (`&core.library.*`).

**Naming convention:**

```
&core.<kind>[.<topic>...]
&entity.<entity-type>.<entity-id>.<sub-kind>[.<sub-id>]
```

- `.` between Space hierarchy segments; `-` for compounds within one segment (`spark-term`, `crypto-majors` stay joined).
- Prefix `&` on Space refs only; non-Space identifiers (beacons, verbs) are dash-only.
- Sub-ids as new levels (`&entity.halo.spark-term.book.A1`, not `book-A1`).
- Names encode entity + sub-kind, not parent chain; structural relationships live in registry atoms (`(sub-entart …)`, `(sub-space …)`).

**Two-step rule** = portable local rule using `&self` + global declaration with target set + combinator (`sum` / `max` / `min` / `count` / `concat` / `sketch`).

**Two-step loop** = universal template at `&core.loop.<class>` + per-entity instance at `&entity.<…>` with bindings. In P1, per-entity Spaces hold the loop bodies directly (no canonical template propagation yet — phase-invariant consumption site).

**Gate primitive** at trust boundary: parse → pubkey lookup → ed25519 verify → nonce dedup → rate-limit → route. Cross-Space within one runtime ≠ trust boundary (direct `(add-atom &other-space …)` works); the gate is for external beacon → Synome and federation. Permission rule canonical: `(if (auth $beacon $verb $target) True False)` — flat 3-arg auth fact in target-owning entart, granted by certifier rooted in genesis.

**Call-out primitive** `(call-out $service (inputs …) (output-shape …))` is the **only** sanctioned synart→telart bridge. Synart inputs verifiable; output not (LLM / local cognition); output-shape conformance verifiable. Sentinels are beacons-with-call-out density (~90% call-out share for `stream`); relays have zero (~95–100% synart).

**13 P1 commitments** (load-bearing design hygiene):

1. Space always a parameter
2. Append-only writes
3. Content-addressed names
4. Open verb dispatch via whitelist
5. Gate as real primitive at trust boundary
6. `(auth $beacon $verb $target)` reads from a named auth Space
7. Idempotent constructors
8. Every rule declares its reads (`(rule-reads $rule $space)`)
9. Cross-Space refs go through registries
10. Cross-Space rules are scatter-gather
11. Global rules carry publication metadata
12. Synart is a tree of entarts (parent → child only; only synents own entarts)
13. Loops, gates, recipes are first-class synart content

**Grounded execution** in P1 splits the old "grounded atom" bucket into literals (values), special forms (evaluator control), and sigils (ALL CAPS callable powers). Sigils resolve through bindings to implement methods; implement code blobs are materialized at bootstrap; implements call workcell hubs; hubs route to human/installer-provided workcell components. There is no ongoing P1 sigil registry Space. Canonical P1 details: `../roadmap/grounding-and-workcells.md`.

**Frame mechanism** (runtime feature, below synomic surface): runtime can hold multiple complete synome-state instances (canonical + shadow). Operations `fork` / `switch` / `discard` / `diff`. P1 uses it for genesis-test isolation (genesis → fork shadow → run suite → discard → production starts after validation). Future uses: sudo-event safety, forecasting, what-if queries, major migrations (double-mesh trick).

**Self-hosting:** synart contains the loops that run synart, the gates that regulate synart access, the recipes that fund work on synart, the telseeds that birth new teleonomes, and the runtime source itself.

## Governance (P1 is fully sudo at genesis)

P1 reality: **Guardian holds all sudo authority; no separate Core GovOps authority role exists inside synart at genesis.** Core Council govops can operate `synserv-canonical`, but that is node operation, not a distinct sudo/auth authority. Cert + auth content sudoed into `&core.registry.beacon`. No standing Guardian entart Space. The post-transition forward-looking design (SpellCore + dual-key SpellGuards, quarterly Council rotation, SKY freeze/override) is described in `summaries/governance.md` and activates after genesis hand-off — not load-bearing for P1 substrate work.

## Accounting (P1-relevant only)

**Capital stack:**

```
IJRC + EJRC (pari passu by nominal)      ← going-concern first loss
Prime Token (forced inflation)            ← recapitalization
------------ liquidation threshold
MDC (subordinated in liquidation)         ← residual claim
SRC (senior in liquidation)               ← senior claim
```

Invariant: `TRRC ≤ TRC`, `ER = TRRC / TRC ≤ 0.90`. Universal ingression curve (flat to anchor, quarter-circle to zero at max). SRC max/anchor 3:1.

**Daily Synomic Settlement Cycle (DSC)** — only in-synome cadence:

- 13:00 UTC cut
- 13:00–16:00 UTC processing
- 16:00 UTC settle / epoch advance

Synserv derives state from wall clock; no sudo `advance-epoch`. Legacy monthly economic settlement is **out-of-band** — not represented as atoms. P1 uses DSC for structural-demand processing (treasury refresh + lot-age surface refresh + Lindy SDR + temporary SDR auction allocation).

**ABC** (Aggregate Backstop Capital) — temporary bootstrap; P1 floor $125M; long-term target 1.5% USDS supply. Insolvency defense in 4 levels: ABC → SKY inflation → Genesis Capital reclaim → USDS haircut with SKY recovery airdrop.

**Entity fees** (target — applies to tokenized entities only): 5% Entity Creation Fee on issued governance tokens; 50 bps/yr Entity Upkeep on conservatively priced token market cap; Cross-Entity Upkeep Rebate against holdings.

**TMF, DR, SDRR, Pioneer Star System, Growth Staking** — all post-P1. TMF (5-step net-revenue waterfall) becomes active when closure enters DSC. SDRR waits for real auction phase (Phase 9+) — needs auction fees to attribute. Growth Staking uses Folios as vehicle, Reference Values from global P/E model.

## Phase roadmap

| Phase | Focus |
|---|---|
| **1** | Real-time ER per Prime; DSC for structural-demand processing; Lindy SDR production + temporary SDR auction; manual economic settlement / penalty action |
| **2–4** | Settlement closure / TMF / LCTS; first canonical propagation sources |
| **5–8** | Factory stack for Halo / Prime / Generator expansion |
| **9–10** | Sentinel formations; real OSRC + SDR auctions; SDRR with fee attribution |
| **Beyond** | Richer cognitive recipes, generalist teleonomes |

## Pointers to topics deliberately skipped

P1 substrate work doesn't need these; they exist in summaries when relevant:

| Topic | Pointer |
|---|---|
| Synodoxics: probmesh, truth values, ossification, crystallization, evidence axiom, RSI | `summaries/synodoxics.md`, `summaries/neurosymbolic.md` |
| Synoteleonomics: teleonomes, dreamer/actuator, recipe marketplace, rogue threat model, binding | `summaries/synoteleonomics.md` |
| Atlas/Synome separation, governance window, telos point | `summaries/macrosynomics.md`, `summaries/core-concepts.md` |
| Sentinel formation operations, TTS/ORC sizing | `summaries/sentinel.md` |
| Folio operating modes, Type 1/2 restructure, Guardian Accord | `summaries/synomic-entities.md` |
| Sequencer / Pylon / Ring derivatives architecture | `summaries/synomic-entities.md`, `synomic-entities/{sequencer,pylon}-entity.md` |
| Halo classes other than `nfat-term` (Portfolio / Trading / Identity Network) | `summaries/synomic-entities.md`, `synomic-entities/halo-*.md` |
| Yield Splitter PT/YT venue economics | `summaries/smart-contracts.md`, `smart-contracts/fixed-rates.md` |
| Growth Staking math (RefValue, P/E model, GF tiers, stUSDS) | `summaries/growth-staking.md` |
| SpellCore / SpellGuard cascade, Council rotation, passthrough voting | `summaries/governance.md` |

## File map (where each piece lives in summaries/)

| Topic | Summary file |
|---|---|
| 5-layer arch, beacons, Atlas/Synome, topology-layering meta | `macrosynomics.md` |
| 26 core concept atoms (dual architecture, ossification, RSI, etc.) | `core-concepts.md` |
| Synomic Entity ranks + per-type specs | `synomic-entities.md` |
| PAU, Configurator, LCTS, NFATS, Yield Splitter, rate-limit attacks | `smart-contracts.md` |
| Topology, boot, two-step rule/loop, call-out, P1 commitments | `noemar-synlang.md` |
| SpellCore/SpellGuard, Council elections (target) | `governance.md` |
| Capital stack, DSC, TMF, entity fees, SDR auction | `accounting.md` |
| Sentinel variants, TTS/ORC, Streaming Accord (Phase 9+) | `sentinel.md` |
| Growth Staking mechanics (post-P1) | `growth-staking.md` |
| Probmesh, retrieval policy, lift, Noemar substrate | `synodoxics.md` |
| Neuro-symbolic cognition loop | `neurosymbolic.md` |
| Teleonomes, recipe marketplace, rogue defense | `synoteleonomics.md` |
| Phase-1 reality (mostly already in roadmap dir; this summary is a re-pointer) | `roadmap.md` |
| Risk framework (the companion to `risk-framework.md` in this dir) | `risk-framework.md` |
