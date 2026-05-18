# Phase 1 — A Space Perspective (v4)

**Status:** Draft v4 (2026-05-17 live-state cleanup — supersedes v3 of 2026-05-15)
**Last Updated:** 2026-05-17
**Scope:** Phase 1 expressed in terms of synart Space topology — what Spaces exist, what each holds, what flows in and out, what's fixed vs operational.

---

## Framing

**Deliverable:** real-time ER per Prime, emitted continuously, in production-quality synlang. Settlement and penalty action stay manual; the synome publishes ER, governance consumes externally.

P1-specific cuts (general lift / insyn-exsyn / DSC / phase-invariant patterns: [`roadmap-ideas.md`](roadmap-ideas.md); broader architecture context: [`../roadstart/big-picture.md`](../roadstart/big-picture.md)):

- **All 7 Primes active**, deploying into 3 P1 Halos (`spark-term`, `grove-term`, `maple-term`).
- **Per-entart local materialization.** Each halo carries its own halo-class + risk-class copies (attestor as sub-Space of the risk class). Each Prime, Halo, and the Generator carry their own `protocol-registry`. Local reads everywhere; no cross-entart hops in the rollup.
- **Halo class vs risk class.** Halo class = standard halobook terms + permitted risk classes (default policy template). Risk class = risk form + class-accordant attestor (attestor as sub-Space). All 3 halos share `nfat-term` × `custodial-crypto` but each materializes its own copies.
- **Halobooks / riskbooks / exobooks are constructor-made** by `relay-halo-{id}`, not sudo (deals come in bursts). `relay` means external/onchain action authority plus the corresponding in-synome operational record; govops is the human/institutional operator, not the beacon stem.
- **Attestation is boolean** with borrower / riskbook / exobook surfaces — see [`attestor-atom-schema.md`](attestor-atom-schema.md). Quantitative inputs all insyn (`CHAINREAD` + market memory); default-deny on stale/fail/missing.
- **Cert / auth all rooted in `&core.registry.beacon`.** Guardian's cert-chain content folds in here; no standing Guardian entart Space in P1.
- **Root holds registry + constructors only.** Operational logic lives in dedicated sub-Spaces. Universal across every entart type.

This phase doc answers four questions: (1) what Spaces exist after genesis, (2) what each holds and how it updates, (3) what I/O flows between beacons, gate, and Spaces, (4) what changes operationally vs sudo-only (any sudo event = phase boundary).

---

## Vocabulary refresher

General terms (sudo, gate-mediated write, DSC, market memory, phase-invariant consumption site) are defined in [`../roadstart/big-picture.md`](../roadstart/big-picture.md) and [`roadmap-ideas.md`](roadmap-ideas.md). Grounded execution terms (literal, special form, sigil, binding, implement, implement code blob, workcell, workcell hub) are defined in [`grounding-and-workcells.md`](grounding-and-workcells.md). P1-specific terms:

| Term | Meaning |
|---|---|
| **halo class** | Halobook policy template — standard terms, permitted risk classes, tranching / issuance presets, rate limits, relay/operator control keys. Lives per-halo at `&entity.halo.{id}.{halo-class-name}`. |
| **risk class** | Riskbook risk treatment — bundle of risk form + class-accordant attestor (attestor as sub-Space `…{risk-class-name}.attest-data`). |
| **risk form** | Synlang equation consuming oracle market memory + `CHAINREAD` inputs, returning per-risk-type CRR components. Lives inside the risk class Space. |
| **protocol-registry** | Per-entart chain-contract metadata (addresses + ABIs + event signatures). Each Prime, Halo, and the Generator owns its own. |
| **constructor** | A verb that allocates new Spaces. P1 has three: `create-halobook`, `create-riskbook`, `create-exobook`. |
| **relay** | Synops-capable beacon with external/onchain actuation authority. A relay performs or coordinates external action and writes the synome records needed for sequencing, lifecycle, accounting, and downstream derivation. |
| **synops-beacon** | In-synome operational mutation only, with no external/mainnet actuation authority. In P1, Halo synops beacons submit Core Council requests and record in-synome borrower/book-accounting changes without giving relay arbitrary administration scope. |

---

## Universal Spaces (sudo at genesis)

| Space | Holds | Operational? |
|---|---|---|
| `&core.bootstrap` | One-shot bootstrap Space: bootstrap recipe, boot manifest schema, P1 sigil / binding / implement code blob / workcell specs, loop requirement declarations, conformance hooks, and boot receipts. Materializes implement code blobs, binds sigils, registers workcell hubs, then becomes inert. | One-shot at boot; inert after successful bootstrap |
| `&core.syngate` | Gate state — nonce dedup window, per-pubkey rate-limit counters, external-verb whitelist, verb→target-Space routing table | Counters mutate per-message; whitelist + routing fixed |
| `&core.loop.synserv` | Synserv heartbeat loop body — synlang the runtime evaluates continuously; drives all derivations and ER emission | Fixed (loop body is the spec) |
| `&core.registry.beacon` | One row per beacon identity: pubkey, status, class, cert atoms, auth grants. Absorbs the legacy Guardian root's authority chain — Guardian's cert + auth content folds in here. | Fixed (status atoms can flip via sudo) |
| `&core.registry.protocol` | Canonical global protocol references — Configurator Unit addresses (`BEAMTimeLock`, `BEAMState`, `Configurator`), chain ids, ABIs / selectors, and provenance. Per-entart `protocol-registry` Spaces still hold local PAU / protocol refs. | Fixed in P1 (updates are phase-boundary writes) |
| `&core.governance.requests` | Core Council request registry — canonical inbox/history for requests addressed to Core Council, including Halo class-modification and borrower Configurator-inclusion requests. Holds request atoms, status, provenance, rationale/evidence refs, and later synodoxics handling refs. Does not execute requests. | Operational request/status records mutate; applying class changes is phase-boundary |
| `&core.relay.govops` | Core govops relay loop body plus operational receipt records for core-level Configurator / aBEAM actions and request handling. Does not own the request registry, does not grant sudo, and does not apply class changes inside P1. | Operational records mutate; loop body fixed |
| `&core.settlement` | Daily synomic settlement cycle state: cadence, cut/process times, epoch-zero, current-epoch, processing markers | Operational (synserv writes epoch/processing state) |
| `&core.treasury` | Sky treasury facts used by the P1 SDR auction and long-term external transparency: Sky-controlled addresses, Sky Prime token share by epoch, source/provenance | Operational (synserv-triggered treasury update; sudoed values for unlaunched tokens) |
| `&core.test-suite` | Test atom definitions + (folded) shadow-only test results + test-runner loop body | Operational (shadow only) |

**10 universal Spaces.**

Core Council requests have their own consumption site from day 1: `&core.governance.requests`. P1 request handling is manual / Core-govops-operated (`relay-core-govops` reads requests and writes statuses / receipts), but later synodoxics machinery reads the same request atoms and attaches derivation, evidence, recommendation, and spell-candidate refs in place. The request intake path does not move when that later process arrives.

What's deliberately *not* here vs. earlier drafts:
- `&core.meta-topology` — archetypes for constructor validation fold into the per-halo halo class atoms (each halo class declares the shapes its constructors validate against).
- `&core.registry.entity` — tree-walk via root sub-space registries is canonical.
- `&core.registry.halo-class` — replaced by per-halo class copies in each halo entart, per the phase-invariant consumption-site principle.
- `&core.registry.sigil`, `&core.registry.binding`, `&core.registry.workcell` — no ongoing P1 registries. P1 grounded execution catalogs live in the mega `.synlang` / `&core.bootstrap` boot surface and become active runtime bindings after bootstrap.
- `&core.framework.risk.categories` (and the broader `&core.framework.*` layer) — no canonical Space in P1; per-class risk forms live in halo entarts. Canonical source + propagation mechanism arrives in a later phase additively.
- `&core.protocol` — replaced by `&core.registry.protocol` for global protocol refs. Per-entart `protocol-registry` sub-Spaces still hold local PAU / protocol refs (each Prime, Halo, and the Generator own their own contract refs locally).
- `&core.test-results` — folded into `&core.test-suite`.
- `&core.loop.market-data`, `&core.loop.attest-data`, `&core.loop.relay.prime`, `&core.loop.relay.halo`, `&core.loop.synops.halo`, `&core.loop.test-runner` — per-entity instances hold their loop bodies in P1 (sudo-set, self-contained); canonical templates ship additively in a later phase, propagating into the same per-entity Spaces. Each per-entity Space remains the consumption site across phases.

---

## Generator (sudo at genesis)

| Space | Holds |
|---|---|
| `&entity.generator.usge.root` | USDS Generator entart root — identity, auth, sub-space registry |
| `&entity.generator.usge.structural-demand` | Structural Demand Resource (SDR) production: lot-age surface atoms, Lindy SDR algorithm/model outputs, SDR policy overlay, and effective SDR bucket capacity atoms |
| `&entity.generator.usge.sdr-auction` | Synserv-triggered temporary SDR auction body and per-Prime per-bucket SDR allocation atoms; structbooks read here for liability matching |
| `&entity.generator.usge.protocol-registry` | USDS / DAI / sUSDS / sDAI ERC20 contract addresses + ABIs + Transfer event signatures |

**4 Generator Spaces.**

Genbook (Primebook-unit aggregation backing USDS issuance) is deferred — P1's deliverable is real-time ER per Prime emitted at the primebook layer; Genbook tracking sits above the deliverable and lands at a later phase boundary alongside cross-Prime concentration enforcement.

P1 uses 30-day SDR buckets (51 total; bucket 50 is 1,500+ days). `structural-demand` owns the total-capacity pipeline:

```text
lot-age surface
  -> Lindy SDR algorithm
  -> Lindy SDR bucket capacity
  -> SDR policy overlay
  -> effective SDR bucket capacity
```

The **lot-age surface** is the reduced scrape of USDS / DAI / sUSDS / sDAI lot balances, ages, movements, account clustering, and source provenance. Raw transfer history stays in scraper/archive infrastructure; the synome stores the usable surface and provenance checkpoints. **Lindy SDR** is the dynamic model output: it converts the lot-age surface into bucket capacity while discounting fragile structure such as same-age crowding, same-account concentration, churn, and low-quality sources. The **SDR policy overlay** is governance-set: eligible sources, caps, haircuts, emergency bounds, and bootstrap/fallback values. The final output is `(effective-sdr-bucket-capacity {bucket} {amount} {epoch})`.

During the daily DSC processing window, synserv refreshes the lot-age surface, runs the Lindy SDR algorithm, applies the SDR policy overlay, then calls the temporary SDR auction body in `sdr-auction`. `sdr-auction` writes `(sdr-allocation {prime} {bucket} {amount} {epoch})` atoms for the next epoch. Structbooks read allocations where `epoch = current-epoch`. **The consumption site is fixed**: later real SDR auctions write the same allocation atom shape into the same Space — only the writer/body changes.

The P1 SDR auction's temporary equation is fully contained in `&entity.generator.usge.sdr-auction`:

```text
sky_effective_ownership(p) = 0.05 + 0.95 × sky_prime_token_share(p)
ownership_weight(p) = sky_effective_ownership(p) × prime_ijrc(p)
allocation(p, bucket) = effective_sdr_bucket_capacity(bucket) × ownership_weight(p) / Σ ownership_weight(active primes)
```

Weights are recomputed every DSC epoch from latest `&core.treasury` token-share facts and each Prime root's IJRC atom. A Prime with missing, stale, or zero IJRC receives zero allocation. Unlaunched token shares still count as ownership through supplied treasury facts. If there are no positive active Prime weights, allocation rounds to zero; any rounding/dust remainder also rounds to zero. Unused allocation has no carry-forward accounting: each epoch's atoms are the live SDR allocation for that epoch, and older atoms are historical.

`&core.treasury` stores the raw token-share fact; the temporary ownership-weight computation lives only in the `sdr-auction` body.

---

## Oracle Entity — sudo at genesis (×1)

Phase 1 has one oracle entity: Crypto Majors Oracle for market data. (Book Attestation Oracle, an entity that existed in earlier drafts, no longer has its own entart Space — its cert chain folds into `&core.registry.beacon`, and class-accordant borrower-readiness / borrower-admission / riskbook / exobook attestation atoms land directly in their target risk class or book Spaces.)

| Space | Holds |
|---|---|
| `&entity.oracle.crypto-majors.root` | Crypto Majors Oracle entart root — identity, auth, sub-space registry |
| `&entity.oracle.crypto-majors.market-data` | Market-data beacon loop body |
| `&entity.oracle.crypto-majors.ticks` | Market-memory atoms for the v1 universe (BTC, ETH, stETH, USDC, USDS, USDT, USD rates): price, basis, vol, correlation, liquidity/impact, liquidation-overhang, funding/OI, macro/rates, reducer checkpoints, data quality |

**3 Oracle Spaces.** Raw historical tapes are not stored in ordinary synome atoms. Archive nodes preserve raw source history; the oracle loop emits reducer outputs and provenance checkpoints into `ticks`. The same reducer formulas run in historical replay and live-tail modes, so new live data naturally becomes part of future historical memory.

---

## Per Prime — sudo at genesis (×7)

Phase 1 has 7 Primes — Spark, Grove, Obex, Keel, Skybase, Launch6, and one more (TBD).

| Space | Holds |
|---|---|
| `&entity.prime.{id}.root` | Prime entart root — identity, auth, sub-space registry, `(prime-trc {prime} {amount})` atom (TRC, sudo-set, governance-updated), per-Prime relay/operator config (allowed halos, deploy cadence, allocation strategy) |
| `&entity.prime.{id}.primebook` | Aggregates Halobook units the Prime holds via cross-book duality. Computes insynTRRC via synlang sweep across structbook. Holds `(exsyn-trrc-claim {prime} {amount} {timestamp})` atoms locally — written by the per-Prime `patch-{prime}` patch-beacon (sudoed inline at genesis). Reads TRC from root. Computes and emits `(prime-er {prime} {value} {timestamp})` real-time per heartbeat. |
| `&entity.prime.{id}.structbook` | The active Primebook sub-book. Reads NFAT units the Prime holds across all 3 halos via cross-book duality. Reads SDR allocations from `&entity.generator.usge.sdr-auction`. Computes matched/unmatched blend per position, structbook CRR per position. |
| `&entity.prime.{id}.relay` | `relay-prime-{id}` loop body: deploy / rollover / withdraw against the Prime's PAUs, plus allocation and transaction-confirmation records needed by the synome. Per-entity sudo-set in P1; canonical template propagation comes additively later. |
| `&entity.prime.{id}.protocol-registry` | This Prime's PAU contract refs — Controller + ALMProxy + RateLimits addresses + ABIs + relevant event signatures |

**5 Spaces × 7 Primes = 35 Spaces.**

All 7 Primes deploy capital into NFATs from the 3 P1 Halos. The structbook is the only active Primebook sub-book in v1; other sub-books (`ascbook`, `tradingbook`, `termbook`, `hedgebook`, unmatched) are deferred — see [`../roadstart/risk-framework.md`](../roadstart/risk-framework.md) "Sub-book taxonomy + coverage matrix".

---

## Per Halo — sudo at genesis (×3)

Phase 1 has 3 Halos: **spark-term**, **grove-term**, **maple-term**. All three use the same halo class (`nfat-term`) and risk class (`custodial-crypto`) but each materializes its own per-entart copies (phase-invariant consumption-site principle).

| Space | Holds |
|---|---|
| `&entity.halo.{id}.root` | Halo entart root — identity, auth, sub-space registry of constructor-made books, constructors (`create-halobook` / `create-riskbook` / `create-exobook`) and their archetypes |
| `&entity.halo.{id}.nfat-term` | **Halo class** — standard halobook terms (NFAT halo unit, max TTM 1y), permitted risk classes `[custodial-crypto]`, tranching presets, issuance presets, rate limits, relay/operator control keys |
| `&entity.halo.{id}.custodial-crypto` | **Risk class** — risk form (the stress-envelope equation that consumes market memory + `CHAINREAD` inputs and returns default/spread/rate/liquidity CRR components) |
| `&entity.halo.{id}.custodial-crypto.attest-data` | Class-accordant attestor loop body — writes boolean borrower-admission, riskbook, and exobook attestation atoms per [`attestor-atom-schema.md`](attestor-atom-schema.md) |
| `&entity.halo.{id}.relay` | `relay-halo-{id}` loop body — borrower setup records, constructors, lifecycle transitions, funding confirmations, and NFAT issuance records. It does not post attestations; attestations live in the class-accordant `attest-data` loop. Per-entity sudo-set in P1; canonical template propagation comes later. |
| `&entity.halo.{id}.synops` | `synops-halo-{id}` loop body and local outbox for in-synome operational requests, especially borrower-inclusion and class-modification requests addressed to Core Council through `&core.governance.requests`. Also records in-synome book-accounting assignments after relay receipts exist. No external/onchain actuation authority. |
| `&entity.halo.{id}.protocol-registry` | This Halo's PAU contract refs — Controller + ALMProxy + RateLimits addresses + ABIs |

**7 Spaces × 3 Halos = 21 Spaces.**

---

## Halo class and risk class

Phase 1 introduces two complementary class concepts per halo. The split decouples on-chain operational mechanics from risk-side characterization.

### Halo class — the halobook policy template

The halo class defines what happens when funds are deployed into the halo *without explicit terms*: the halo class fills in the defaults. In P1 the halo class for all 3 halos is `nfat-term`, which says:

- Funds in queue are converted to an **NFAT halo unit** with maximum TTM 1 year.
- The unit is deployed only into riskbooks of permitted risk classes — `[custodial-crypto]` in P1.
- Standard tranching and issuance presets apply.
- Rate limits and relay/operator control keys are bounded.

Halo unit holders can stay passive *because* the halo class's policy is bounded. Some halo classes will eventually be governance-mutable (parameters tunable by governance); others will be fully immutable (fixed ruleset, uniform risk/liquidity profile by design). Both forms fit the same Space; an immutability flag in the halo class atom is the mechanism.

The halo class lives at `&entity.halo.{halo-id}.{halo-class-name}` — the class name *is* the sub-kind. Each halo carries its own copy; canonical propagation arrives in a later phase additively.

### Risk class — the riskbook risk treatment

The risk class defines:

- **Risk form** — the equation that consumes oracle market memory + `CHAINREAD` inputs and returns per-risk-type CRR components (default-CRR, spread-CRR, rate-CRR, liquidity-CRR). P1 uses a max-approved-scenario-loss exobook waterfall model; CORE is calibration/reference material, not the direct CRR engine. See [`custodial-crypto-risk-form.md`](custodial-crypto-risk-form.md).
- **Class-accordant attestor** — the boolean admission / attestation gate, signed by an attest-data beacon, structurally a sub-Space of the risk class. It posts borrower admission at risk-class level and riskbook / exobook attestations at book level.

The risk class lives at `&entity.halo.{halo-id}.{risk-class-name}` (sibling to the halo class, not nested). The attestor loop lives at `&entity.halo.{halo-id}.{risk-class-name}.attest-data`.

### How they interact

The halo class **declares** which risk classes it deploys into via `(permitted-risk-classes {halo-class} [{risk-class-1} …])`. The risk class stands independently; the halo class merely references it for standard-terms deployment.

When the halo factory creates a riskbook:
1. Read the halo class for permitted risk classes (in P1: `[custodial-crypto]`).
2. Import the named risk class's risk form into the new riskbook.
3. Register the new riskbook under the halo root.
4. The attestor loop (sub-Space of the risk class) sweeps the halo root's sub-space registry for admitted borrowers, its-class riskbooks, and child exobooks, then writes the relevant admission / attestation atoms.

The riskbook anchors on the risk class directly — `(risk-class custodial-crypto)` in a riskbook resolves to the risk class Space, no need to walk through the halo class. Decoupling for future phases: if a halo class later admits multiple risk classes, or wants to swap one for another, no structural surgery — just update the `permitted-risk-classes` declaration.

---

## Constructor-made Spaces (per deal flow, unbounded)

These grow during operation as deals come in. All factory verbs respect halo-class accord and parent-pointer integrity.

| Space pattern | Constructor (caller) | Purpose |
|---|---|---|
| `&entity.halo.{id}.halobook.{hbk-id}` | `create-halobook` (`relay-halo-{id}`) | One per deal burst. References the halo class for standard terms. Issues NFAT units to Primes via `record-unit`. |
| `&entity.halo.{id}.riskbook.{rbk-id}` | `create-riskbook` (`relay-halo-{id}`) | Under a halobook. Bound to a risk class permitted by the halo class. Risk form imported in at creation. Riskbook-issued unit held by halobook via cross-book duality. |
| `&entity.halo.{id}.exobook.{loan-id}` | `create-exobook` (`relay-halo-{id}`) | Per-borrower loan. Asset side: collateral references (`CHAINREAD` against borrower's collateral account) or staged PAU cash before send. Tranches: senior (static notional in USDC/USDS/USDT), junior (notional-rule = residual equity). State: lifecycle, debt outstanding, funding confirmation, maturity/TTM. Rollup-gating borrower/riskbook admission lives in the risk class/riskbook attestation surfaces. |

A v1 halo with N active loans has roughly: 1–few halobooks, 1–few riskbooks, N exobooks.

---

## Attestation model

Four boolean surfaces, all schemas in [`attestor-atom-schema.md`](attestor-atom-schema.md):

- **Borrower readiness** (per risk class, in `&entity.halo.{id}.custodial-crypto`) — records that proposed borrower setup is legally / operationally / credit ready for Core Council Configurator inclusion. It does not claim the Configurator whitelist is already current.
- **Borrower admission** (per risk class, in `&entity.halo.{id}.custodial-crypto`) — records that borrower, disbursement account, collateral account, Configurator whitelist, custody, and legal framework are acceptable. `synops-halo-{id}` creates and records the proposed borrower setup shell and, after readiness attestation, submits the Core Council inclusion request. Core Council `aBEAM` / configurator whitelist admits the account setup through `relay-core-govops`; the class-accordant attestor then posts final borrower admission. The Halo relay cannot whitelist or admit a borrower alone.
- **Riskbook shared-structure attestation** (per riskbook) — legal-structure-enforceable / borrower-credit-standing / custodian-compliance over the riskbook's shared structural config.
- **Exobook term attestation** (per exobook) — term-enforceable / maturity-T / TTM-days-at-funding / cash-conversion-path-valid / disbursement-readiness.

Quantitative CRR inputs are all insyn (`CHAINREAD` for collateral, debt, funding state; market memory for price, liquidity, volatility). The attestor underwrites only what the chain can't show — legal, operational, credit, term.

**Default-deny:** without a fresh accordant `pass` atom (or if `fail` / stale / scope-mismatched), the borrower / riskbook / exobook is excluded from the rollup. The attestor loop body lives at `&entity.halo.{id}.custodial-crypto.attest-data` — class-accordance is structural (the attestor only operates on books bound to its class).

### Exobook staged lifecycle

Exobook + exo units can be created before funds are sent. In `ready-empty`, borrower setup, collateral address, term intent, and tranche skeleton are recorded but no assets have been assigned. After the Halo relay claims queued funds and records conversion receipts, `synops-halo-{id}` can assign in-synome book accounting into the selected riskbook/exobook path. After the funding tx confirms, the exobook becomes `funded-active` and the certified maturity/TTM becomes official for SDR matching. If the send or attestation fails, the assigned cash unwinds back to ordinary PAU cash. Full lifecycle diagram: [`attestor-atom-schema.md`](attestor-atom-schema.md) §5.

---

## Beacons (all run real synlang loops in Noemar)

| Identity | Class | Admin'd by | Loop body location |
|---|---|---|---|
| `synserv-canonical` | synserv | Core Council govops (singleton) | `&core.loop.synserv` |
| `market-data-crypto-majors-{provider}` | market-data-beacon | Crypto Majors Oracle | `&entity.oracle.crypto-majors.market-data` |
| `attest-data-{halo-id}` × 3 | attest-data-beacon | (cert + auth in `&core.registry.beacon`) | `&entity.halo.{id}.custodial-crypto.attest-data` |
| `patch-{prime}` × 7 | patch-beacon | govops (Guardian sudo cert at genesis) | sudoed inline into `&entity.prime.{id}.primebook` |
| `relay-core-govops` | relay | Core Council govops | `&core.relay.govops` |
| `relay-prime-{id}` × 7 | relay | Prime govops | `&entity.prime.{id}.relay` |
| `relay-halo-{id}` × 3 | relay | Halo govops | `&entity.halo.{id}.relay` |
| `synops-halo-{id}` × 3 | synops-beacon | Halo govops | `&entity.halo.{id}.synops` |
| `test-runner` | test | n/a | folded into `&core.test-suite` (shadow only) |

**~27 beacon identities** registered in `&core.registry.beacon` at genesis (1 synserv + 1+ market-data + 3 attest-data + 7 patch + 1 relay-core + 7 relay-prime + 3 relay-halo + 3 synops-halo + 1 test). All loop bodies are production-quality synlang evaluated by Noemar. Per-entity Spaces hold the loop bodies in P1 (self-contained); canonical loop templates ship additively in a later phase per the phase-invariant consumption-site pattern.

`synserv-canonical` is registered here for identity / loop resolution, but it is not a normal operator beacon. It is the central synomic node operated by Core Council govops: beacons submit external inputs or action records through syngate; synserv sequences accepted writes, derives state, advances DSC, and publishes official outputs.

`relay` is the coupled external-action + synome-record role. Relay writes must be causally tied to an external/onchain action, a planned external/onchain action, a confirmed external/onchain action, or a lifecycle transition required to safely execute or record that action. Pure synome-only administration belongs to `synops-beacon`, not to relay.

`synops-beacon` is the pure in-synome operational class. In P1 `synops-halo-{id}` can register proposed borrower setup atoms, submit Core Council requests, and assign book-accounting atoms after relay receipts exist. It has no capital movement, PAU execution, or Configurator authority.

Patch-beacons remain the one beacon class without a regulated framework — Guardian-sudoed primitives, govops-certed, with loop body + per-entity config sudoed inline into the target Space (no universal template, no oracle-entity hop). Designed to sunset as their use cases migrate to insyn-native machinery.

---

## Operational verbs

| Verb | Caller | Effect |
|---|---|---|
| `register-borrower-setup` | synops-halo-{id} | Writes proposed borrower setup shell / intent and operational references in the target risk class Space; external whitelist/configurator work remains Core Council / relay-core-governed and attestor-admitted |
| `create-halobook` | relay-halo-{id} | Allocates `&entity.halo.{id}.halobook.{hbk-id}`; registers under halo root with reference to halo class |
| `create-riskbook` | relay-halo-{id} | Allocates `&entity.halo.{id}.riskbook.{rbk-id}` under halobook; binds to a permitted risk class; imports risk form |
| `create-exobook` | relay-halo-{id} | Allocates `&entity.halo.{id}.exobook.{loan-id}` under riskbook; writes initial assets + tranches |
| `record-unit` | relay-halo-{id} | Issues NFAT unit in halobook (mints into Prime's PAU as primebook asset / halobook liability) |
| `transition-book` | relay-halo-{id} | Book lifecycle state transitions tied to external deployment / unwind flow |
| `update-exobook-state` | relay-halo-{id} | Updates lifecycle, funding confirmation / tx receipt references, and non-market exobook state within attestor scope |
| `request-borrower-inclusion` | synops-halo-{id} | Writes a local Halo request/outbox atom in `&entity.halo.{id}.synops` and a canonical Core Council request atom in `&core.governance.requests`, backed by borrower-readiness attestation. This requests Configurator inclusion; it does not grant it. |
| `assign-book-assets` | synops-halo-{id} | Writes in-synome accounting atoms assigning already-claimed / converted Halo-held funds from a halobook into the selected riskbook and exobook path. Requires relay receipts; moves no chain funds. |
| `request-class-modification` | synops-halo-{id} | Writes a local Halo request/outbox atom in `&entity.halo.{id}.synops` and a canonical Core Council request atom in `&core.governance.requests`. This is only a request; applying a class change is a phase-boundary action in P1. |
| `record-core-govops-action` | relay-core-govops | Writes Core govops request-status atoms in `&core.governance.requests` and operational receipt atoms in `&core.relay.govops` for request handling and core-level Configurator / aBEAM actions using refs from `&core.registry.protocol`; does not grant sudo. |
| `post-borrower-readiness-attestation` | attest-data-{halo-id} | Writes the boolean `borrower-readiness-attestation` atom into the target risk class Space |
| `post-borrower-admission` | attest-data-{halo-id} | Writes the boolean `custodial-borrower-admission` atom into the target risk class Space |
| `post-riskbook-attestation` | attest-data-{halo-id} | Writes the boolean `riskbook-attestation` atom into the target riskbook Space |
| `post-exobook-attestation` | attest-data-{halo-id} | Writes the boolean `exobook-term-attestation` atom into the target exobook Space |
| `deploy-into-nfat` | relay-prime-{id} | Increases Prime's holding of an NFAT unit; updates capital allocation / tx-confirmation atoms |
| `rollover-nfat` | relay-prime-{id} | At maturity, retires old NFAT, creates new under same/different halobook |
| `withdraw-from-nfat` | relay-prime-{id} | Reduces holding; returns capital to Prime root |
| `market-data-write-memory` | market-data-crypto-majors-{provider} | Pushes current-state atoms, reducer outputs, and reducer checkpoints to `&entity.oracle.crypto-majors.ticks` |
| `patch-write-exsyn-trrc` | patch-{prime} | Writes `(exsyn-trrc-claim {prime} {amount} {timestamp})` directly into `&entity.prime.{id}.primebook` |

**~20 operational verbs.** Epoch advancement is not an operational verb; synserv derives it from wall clock and writes `&core.settlement` state.

---

## Operational write surface

| Beacon | Reads | Writes |
|---|---|---|
| `market-data-crypto-majors-{provider}` | external feeds and archive-node reducer outputs: exchange APIs, on-chain DEXes, perp venues, options, rates, macro factors | `&entity.oracle.crypto-majors.ticks` (current market-state + rolling market-memory atoms) |
| `patch-{prime}` (patch-beacon) | external (off-space governance attestation about legacy halo TRRC for this Prime) | `&entity.prime.{id}.primebook` (`(exsyn-trrc-claim {prime} {amount} {timestamp})` atoms, written locally) |
| `attest-data-{halo-id}` (attest-data-beacon) | borrower setup, riskbook structural state, exobook term state, custodian / legal-counsel / borrower-credit assessments (off-space) | `(borrower-readiness-attestation _)`, `(custodial-borrower-admission _)`, `(riskbook-attestation _)`, and `(exobook-term-attestation _)` boolean atoms |
| `synops-halo-{id}` | proposed borrower setup, borrower-readiness attestations, Halo request intents, target class/risk-class refs, requested parameter diffs, relay receipts for already-held funds | proposed borrower setup atoms in the target risk class Space; `&entity.halo.{id}.synops` local outbox atoms; canonical request atoms in `&core.governance.requests`; in-synome book-accounting assignment atoms |
| `relay-core-govops` | `&core.governance.requests`, `&core.registry.protocol`, Core Council / Configurator operational queue, external tx receipts | request status atoms in `&core.governance.requests`; core-action receipt atoms in `&core.relay.govops`; external Configurator / aBEAM action records |
| `relay-halo-{id}` | halo root config, halo class, risk class, deal queue, planned / executing / confirmed external actions | new halobook/riskbook/exobook Spaces, lifecycle atoms, queue-claim / conversion / funding confirmations, tx receipts, NFAT issuance records |
| `relay-prime-{id}` | Prime root config, NFAT availability via cross-book duality, deploy schedule, planned / executing / confirmed external allocation actions | NFAT-holding updates in halobooks; capital allocation and tx-confirmation atoms in Prime root / relay-adjacent Spaces |
| `synserv-canonical` | all input atoms across the entart tree; chain state via `(CHAINREAD …)`; wall clock for DSC | derived state atoms in book Spaces; `&core.settlement` epoch/processing atoms; `&core.treasury` refresh writes; lot-age surface / Lindy SDR / SDR auction dispatch; `(prime-er _)` atoms in primebooks |
| `test-runner` | (shadow only) | test results within `&core.test-suite` (shadow only) |

The pattern: input beacons (market-data, attest-data, patch) write into their target Spaces; relay beacons run external-action-coupled constructors, lifecycle transitions, and capital flows; synserv runs the synlang heartbeat that drives all derived state and emits real-time ER.

---

## ER data flow (synserv heartbeat)

```
EXTERNAL INPUTS
  market-data-crypto-majors  ──→ &entity.oracle.crypto-majors.ticks
  patch-{prime}              ──→ &entity.prime.{id}.primebook ((exsyn-trrc-claim …))
  attest-data-{halo-id}      ──→ borrower-readiness / borrower-admission / riskbook / exobook attestation atoms
  synops-halo-{id}           ──→ borrower setup, borrower-inclusion requests, class-modification requests, assign-book-assets
  relay-core-govops          ──→ core request statuses / Configurator action records
  relay-halo-{id}            ──→ create-* / queue-claim / record-unit / conversion / transition / update-state / funding-confirmation
  relay-prime-{id}           ──→ deploy / rollover / withdraw / update-capital-allocation / tx-confirmation

SYNSERV HEARTBEAT (evaluating &core.loop.synserv)

  settlement / processing level
    read: wall clock + &core.settlement current-epoch
    if 13:00 UTC cut reached and processing not fired:
       write processing marker
       refresh &core.treasury token-share atoms
       refresh &entity.generator.usge.structural-demand lot-age surface
       run Lindy SDR algorithm + SDR policy overlay
       run temporary SDR auction for next epoch
    if 16:00 UTC settle reached:
       write next current-epoch atom

  exobook level
    read: CHAINREAD of collateral/debt/loan-terms + market-memory atoms + tranches + lifecycle
    derive: junior_residual via notional-rule, health_factor, staged/funded state, equity

  riskbook level
    read: borrower admission + attestation atom + child exobook derivations + crypto-majors market memory + risk form (from halo's risk class Space)
    if no fresh accordant attestation → riskbook excluded from rollup (and all exobooks under it)
    derive: per-position CRR components per exobook (default-CRR / spread-CRR / rate-CRR / liquidity-CRR)

  halobook level
    read: child riskbook units (cross-book duality)
    derive: aggregate exposure; NFAT atoms projected as Prime-side assets

  Prime structbook level
    read: NFAT units held (via cross-book duality from all 3 halos' halobooks)
        + current-epoch SDR allocations from &entity.generator.usge.sdr-auction
    derive: matched/unmatched blend; per-position CRR via structbook formula

  Prime primebook level
    read: structbook output → insynTRRC[prime]
        + (exsyn-trrc-claim prime _) from local primebook (written by patch-{prime}) → exsynTRRC[prime]
        = TRRC[prime]
        read: (prime-trc prime _) atom in &entity.prime.{id}.root → TRC[prime]
    emit: (prime-er prime value T) ← every heartbeat, real-time

  (Genbook level deferred — cross-Prime concentration enforcement arrives at a later phase)
```

---

## Frame Mechanism

Runtime feature for clone-and-test isolation — full mechanism in [`roadmap-ideas.md`](roadmap-ideas.md) "Frame mechanism". P1 use: genesis bootstraps canonical → fork to shadow → run test suite → discard → canonical verified by structural identity. Implementation: deep copy at P1's scale (~73 fixed Spaces); copy-on-write becomes valuable later.

---

## Test System

A synart-native acceptance suite. Tests live as atoms in `&core.test-suite`; results accumulate in the same Space (shadow-only). The whole suite is sudo-written at genesis. **Tests run against a shadow frame, not canonical**, using the Frame Mechanism.

Test categories for v4:

| Category | Verifies |
|---|---|
| **Topology** | All 73 fixed Spaces exist; sub-entart and sub-space registries point correctly; per-entart root contents present (TRC atom in prime roots, etc.) |
| **Bootstrap / grounding** | `&core.bootstrap` content present; literal / special form / sigil classification; binding resolution; implement code blob hash checks; workcell hub registration; shadow-frame binding to test workcells |
| **Auth atoms** | Each operational verb has correctly-placed auth atoms in `&core.registry.beacon`; counts match expected per Prime / Halo |
| **Beacon registry** | All ~27 identities present, status active, class atoms set, cert chains rooted |
| **Halo class / risk class** | All 3 halo entarts carry their `nfat-term` halo class and `custodial-crypto` risk class with the right shape; the attestor sub-Space is present and accordant |
| **Constructors** | `create-halobook` / `create-riskbook` / `create-exobook` happy-path + auth-failure + duplicate (idempotency); risk-form import on `create-riskbook` |
| **Attestation** | borrower readiness before inclusion, final borrower admission, `post-riskbook-attestation`, and `post-exobook-attestation` happy paths; rollup behavior with stale / fail / missing attestations (borrower, riskbook, or exobook excluded — default-deny) |
| **ER computation** | synserv-internal CRR + insynTRRC + exsynTRRC + TRC → real-time ER emission against synthetic positions |
| **Oracle inputs** | market-memory reducer outputs and current-state atoms (market-data-beacon); `(exsyn-trrc-claim _)` consumption from per-Prime primebook (patch-beacon write path) |
| **Settlement / SDR pipeline** | DSC epoch advance from mock clock; 13:00-16:00 processing idempotency; treasury refresh before allocation; lot-age surface refresh; Lindy SDR and policy-overlay outputs; `sdr-allocation` atoms stamped with next/current epoch as expected |
| **Relay / synops flows** | `register-borrower-setup`; `request-borrower-inclusion` and `request-class-modification` into `&core.governance.requests`; Core govops request status / Configurator action records; NFAT deploy / rollover / withdraw cycle; halo book setup; `assign-book-assets`; funding confirmation / tx receipt handling |
| **Gate-level** | bad sig rejected; replay rejected; rate-limit enforced; unknown verb / identity rejected |
| **Risk form conformance** | All 3 halos' `custodial-crypto` risk forms produce identical outputs on the same inputs (binds the per-class copies until canonical propagation ships) |

Genesis → shadow fork → test → discard shadow → production start.

---

## Genesis sudo sequence

After Phase 0 substrate is in place, Phase 1 genesis is a sequence of sudo writes. The order respects dependencies: universal infrastructure before entarts; entart roots and sub-spaces before their content; cert + auth in the beacon registry before beacon-pointed loop bodies.

1. Allocate the 10 universal Spaces (`&core.bootstrap`, `&core.syngate`, `&core.loop.synserv`, `&core.registry.beacon`, `&core.registry.protocol`, `&core.governance.requests`, `&core.relay.govops`, `&core.settlement`, `&core.treasury`, `&core.test-suite`).
2. Allocate the 4 Generator Spaces (`usge.root`, `usge.structural-demand`, `usge.sdr-auction`, `usge.protocol-registry`).
3. Allocate the 3 Oracle Spaces (`crypto-majors.root`, `crypto-majors.market-data`, `crypto-majors.ticks`).
4. Allocate the 35 per-Prime Spaces (×7 × {root, primebook, structbook, relay, protocol-registry}).
5. Allocate the 21 per-Halo Spaces (×3 × {root, nfat-term, custodial-crypto, custodial-crypto.attest-data, relay, synops, protocol-registry}).
6. Write `&core.bootstrap` content — bootstrap recipe, boot manifest schema, P1 sigil / binding / implement code blob / workcell specs, loop requirement declarations, conformance hooks, and empty boot receipts.
7. Write `&core.syngate`'s external-verb whitelist + verb→target-Space routing table.
8. Write all ~27 beacon identities into `&core.registry.beacon` with pubkeys, classes, statuses, cert atoms, auth grants. (This absorbs the legacy Guardian-root authority chain into the beacon registry.)
9. Write `&core.registry.protocol` content — Configurator Unit refs (`BEAMTimeLock`, `BEAMState`, `Configurator`), chain ids, ABIs / selectors, and provenance.
10. Write `&core.governance.requests` content — request schema, status taxonomy, empty canonical request registry, and reserved synodoxics-handling refs.
11. Write `&core.relay.govops` content — Core govops relay loop body and empty/current operational receipt state.
12. Write per-Prime configs into each `&entity.prime.{id}.root` — `(prime-trc {prime} {amount})` atom and relay/operator config.
13. Write per-Halo halo class content into each `&entity.halo.{id}.nfat-term` — standard terms (NFAT halo unit, max TTM 1y), `(permitted-risk-classes nfat-term [custodial-crypto])`, tranching / issuance presets, rate limits.
14. Write per-Halo risk class content into each `&entity.halo.{id}.custodial-crypto` — the stress-envelope risk form, scenario-binding config, and attestation gates.
15. Write per-Halo attestor loop bodies into each `&entity.halo.{id}.custodial-crypto.attest-data`.
16. Write per-Halo relay loop bodies into each `&entity.halo.{id}.relay`.
17. Write per-Halo synops loop bodies into each `&entity.halo.{id}.synops`.
18. Write per-Halo `protocol-registry` content — Halo PAU contract refs.
19. Write per-Prime relay loop bodies into each `&entity.prime.{id}.relay`.
20. Write per-Prime `protocol-registry` content — Prime PAU contract refs.
21. Write per-Prime `patch-{prime}` patch-beacon — loop body + per-entity config + auth, sudoed inline into each `&entity.prime.{id}.primebook`.
22. Write Generator `protocol-registry` content — USDS / DAI / sUSDS / sDAI ERC20 refs.
23. Write `&core.settlement` initial state — DSC cadence, 13:00 UTC cut, 16:00 UTC process-end / settle time, epoch-zero, current-epoch.
24. Write `&core.treasury` initial state — Sky-controlled addresses and sudoed token-share values for unlaunched Prime tokens.
25. Write Generator `structural-demand` initial state — 30-day SDR bucket definitions, lot-age surface source universe, Lindy SDR algorithm, SDR policy overlay, and empty/current effective SDR bucket capacity state.
26. Write Generator `sdr-auction` content — ownership-weighted temporary SDR auction body and empty/current allocation state.
27. Write Oracle `market-data` loop body into `&entity.oracle.crypto-majors.market-data`.
28. Write Oracle `ticks` initial state (empty, will populate from beacon writes/reducer outputs).
29. Write all test atoms + test-runner loop body into `&core.test-suite`.
30. Configure operator-level test credentials and boot manifest values (runtime config, not ordinary synart content).

After step 30, genesis sudo stops. The installer invokes `&core.bootstrap`; bootstrap materializes implement code blobs, binds sigils, registers workcell hubs, emits boot receipts, forks canonical → shadow, points shadow bindings at test workcells, runs the test suite, inspects, and discards or retains the shadow according to operator policy. Production starts after validation, with `&core.bootstrap` inert.

---

## What constitutes a phase boundary

By construction, **any sudo event in Phase 1 is a phase boundary**. Examples:

- Adding a new Prime
- Adding or moving a Halo
- Adding a new halo class or risk class (the per-halo class copies pattern accommodates this; new entries are sudo writes)
- Applying a Halo class-modification request (the request/status atoms are operational; the class change itself is a phase-boundary write)
- Adding new beacon classes
- Adding or changing post-bootstrap sigils, bindings, implement code blobs, or workcell hub specs
- Activating new sub-books (currently only `structbook` is active)
- Activating concentration caps
- Replacing the temporary SDR auction body with Prime-strategy-driven real SDR auctions (the `sdr-auction` Space's consumption shape stays fixed; only the writer/body changes — phase-invariant transition)
- Adding a later `&entity.generator.usge.osrc-auction` Space for OSRC auctions
- Activating canonical loop-template propagation (adds `&core.loop.relay.{prime,halo}`, `&core.loop.synops.halo`, `&core.loop.market-data` + propagation mechanism; per-entity Spaces stay where they are — phase-invariant transition)
- Activating canonical risk-form / halo-class source + propagation
- Activating settlement closure beyond DSC processing tasks (Phase 2 transition)
- Activating Growth Staking — adds `&core.framework.valuation` and related parameters
- Unfolding the risk framework from per-halo P1 copies to canonical scenario / asset-profile sources (adds `&core.framework.risk.scenarios`, `&core.framework.risk.asset-profiles`, etc.)
- Wiring up event-driven derivation (currently heartbeat sweep)
- Activating Genbook cross-Prime concentration enforcement

Each later phase is a topology delta — a precisely-specified set of sudo writes that extends what Phase 1 established. The substrate that books rest on never gets rewritten; new substrate gets added alongside.

---

## Worked Example: A Single NFAT Loan

A 6-month NFAT loan illustrating how the substrate primitives compose end-to-end. Spark-Term (one of the 3 P1 Halos) originates a custodial-crypto loan: $750K USDC against 1 BTC of borrower collateral. Spark Prime (one of the 7 Primes) deploys into the NFAT issued against this loan; the senior claim sits in Spark Prime's portion of Spark-Term's halobook.

### Step 1: Per-loan exobook setup

```
exo-book spark-term-loan-001
   asset: btc 1                                      ; collateral (CHAINREAD against borrower's on-chain account)
   tranches:
      seniority 0: borrower equity, $250K usd        ; ~25% cushion
      seniority 1: senior, $750K usdc                ; loan principal
   rules:
      health-factor-trigger (liquidate at HF < 1.05)
      maturity 180 days
   state:
      btc-value-usd $80000                            ; from market-data
      current-hf 1.07
   frame: usd
   ;; parent riskbook carries the (underwriting pass) attestation that gates rollup
   ;; (signed by attest-data-spark-term; covers this and any other exobooks in the same riskbook)
```

### Step 2: Risk-class match

Spark-Term's Riskbook (`&entity.halo.spark-term.riskbook.{rbk-id}`) holds the senior tranche of `spark-term-loan-001`. The Riskbook is bound to the `custodial-crypto` risk class (`&entity.halo.spark-term.custodial-crypto`), which permits this Riskbook's composition (single senior tranche, BTC collateral, USDC denom). The risk form was imported into the riskbook at `create-riskbook` time.

### Step 3: Stress-envelope risk form

Risk form applies the approved scenario library, takes the worst senior-loss outcome. One illustrative scenario — BTC drops 45%, USDC depeg ~5%, execution haircut from market-memory impact curves, junior cushion revalues with stressed asset:

- Asset value post-stress: $80K → $44K
- Junior cushion (stressed BTC value): $44K × ($250K / $80K) = ~$13.75K
- Effective senior loss = max(0, $36K − $13.75K) = $22.25K
- USDC depeg loss on $750K notional: $37.5K
- Total: $59.75K → loss fraction $59.75K / $750K ≈ 7.97%

Not expected loss — the senior exo-unit loss under the binding approved scenario. Feeds default-CRR; risk form also outputs spread-CRR / rate-CRR / liquidity-CRR.

### Step 4: Halobook P/T declarations

Spark-Term's halo class (`nfat-term`) declares:
- P (permitted unwind): only at maturity OR on health-factor breach
- T (transfer market): not transferable

### Step 5: Sub-book routing

Eligibility check at Spark Prime's Primebook level:
- `ascbook`: NO (not deep peg-defense liquid)
- `tradingbook`: NO (P AND T both restrictive — no exit path)
- `termbook`: NO (no tUSDS-matched liability)
- `structbook`: YES (has SPTP = 180 days, SDR allocation available)
- `hedgebook`: NO (no hedge instruments in v1 test)

→ Routes to Spark Prime's `structbook`. (In Phase 1 only `structbook` is the active Primebook sub-book; the others exist as schema placeholders.)

### Step 6: structbook capital math

Assume Spark Prime has been allocated $200M of bucket 6 (180 days) by the temporary SDR auction in `&entity.generator.usge.sdr-auction`, with $190M already matched → $10M capacity left.

For this $750K position:
- Matched: min($750K, $10M) = $750K (fully matched); capital = $750K × default-CRR ≈ $750K × 5% = $37.5K
- spread-CRR / rate-CRR / liquidity-CRR computed but non-binding for the matched portion
- **Position capital: ~$37.5K** (default only; structural matching covers credit-spread, rate, liquidity)

If capacity were exhausted before this loan landed: matched = $0, unmatched = $750K; capital = $750K × max(RW, forced-loss) = $750K × max(5%, 7.97%) = $59.8K → **position capital ~$59.8K**.

Smooth blend (per [`matching.md`](matching.md) §3): capital scales continuously with utilization — no binary cliff.

### Step 7: Concentration check

If aggregate ETH-backed lending exposure (across all loans, USDC and USDT denominated) at the Genbook level exceeds the governance-set cap on the "ETH-collateralized lending" category, the excess gets 100% CRR. V1 manual caps; the math is the same. Cross-Prime concentration enforcement at the Genbook is deferred in Phase 1 (Genbook itself is deferred).

### Scaling up: full-Prime computation

For a full Prime's NFAT holdings (say, Spark Prime holding NFATs against 1000 loans summing to $500M across the 3 P1 Halos):

```
Total Position Capital  = Σ_position (Matched × default-CRR + Unmatched × forced-loss/rate treatment)
Concentration Excess    = applicable category penalties
Total ASC + ORC         = parallel tracks (not in TRRC, but additive operational obligations)

Prime insynTRRC = Total Position Capital + Concentration Excess
Prime TRRC      = insynTRRC + exsynTRRC      ; exsyn from patch-{prime} writing into primebook
Prime ER        = TRRC / TRC
```

Each of the 7 Primes computes its own TRRC; cross-Prime aggregation at the Genbook is deferred.

Atom-level companion trace: [`p1-nfat-atom-trace.md`](p1-nfat-atom-trace.md) expands this example into constructor writes, attestor gates, heartbeat reads, risk-form outputs, `structbook` matching, and final `prime-er` emission.

---

## V1 Carve-outs

Deliberate Phase 1 simplifications. Each has a clear later-phase replacement; the substrate the books rest on does not get rewritten when these unlock.

1. **Structural-demand capacity is computed in P1.** The lot-age surface feeds the Lindy SDR algorithm, governance constrains the result with the SDR policy overlay, and `structural-demand` emits effective SDR bucket capacity. Governance-set values are policy/fallback inputs, not the ordinary source of bucket capacity.
2. **30-day SDR buckets** (51 total). Bucket N = N × 30 days; bucket 50 = 1,500+ days. Bucket size is independent of the daily settlement cadence.
3. **Daily synomic settlement cycle from day 1.** DSC is visible in synome; legacy monthly settlement remains out-of-band. DSC cut is 13:00 UTC, processing is 13:00-16:00 UTC, and epoch advance is synserv-derived from wall clock.
4. TTM range 0–12 months only (per `nfat-term` halo class).
5. SPTP = remaining nominal term (no stress modifier).
6. One Genbook (USDS) only — and Genbook itself is deferred in P1 (tracking only via the primebook layer).
7. Three Halos (spark-term, grove-term, maple-term) with seven Primes deploying into them.
8. Super-senior tranches only (mezzanine / equity-tranche holdings get CRR 100% by default-deny).
9. **Synserv-triggered temporary SDR auction** in `&entity.generator.usge.sdr-auction` — ownership-weighted temporary equation using effective SDR bucket capacity from `structural-demand`, Sky token share from `&core.treasury`, and per-Prime IJRC. There is no P1 reservation market, tug-of-war, sticky claim, durable SDR ownership, or carry-forward accounting. Real Prime-strategy-driven SDR auctions replace the body without relocating the read path.
10. Single halo class (`nfat-term`) with single risk class (`custodial-crypto`); NFAT halo-unit issuance at max 1y TTM, deploying into `custodial-crypto` riskbooks only.
11. Active sub-books: only `structbook`.
12. Tranche rights schema present but not exercised.
13. JAAA / CLO modeling deferred (recursive complexity).
14. DR, SDRR, tagging registry deferred; SDRR activates with real SDR auctions that pay fees.
15. Core Entity halo-mode deferred; legacy exposures remain out-of-band / patch-fed for P1.

Companion principles distilled from these decisions live in [`v1-principles.md`](v1-principles.md).

---

## Totals

| Category | Count |
|---|---|
| Core shared Spaces | 10 (`bootstrap`, `syngate`, `loop.synserv`, `registry.beacon`, `registry.protocol`, `governance.requests`, `relay.govops`, `settlement`, `treasury`, `test-suite`) |
| Generator (`usge`) | 4 |
| Oracle (`crypto-majors`) | 3 |
| Per-Prime ×7 (×5 each) | 35 |
| Per-Halo ×3 (×7 each) | 21 |
| **Fixed Spaces at genesis** | **73** |
| Constructor-made (per deal) | unbounded |
| Beacon identities | ~27 (1 synserv + 1+ market-data + 3 attest-data + 7 patch + 1 relay-core + 7 relay-prime + 3 relay-halo + 3 synops-halo + 1 test) |
| Constructors | 3 (`create-halobook`, `create-riskbook`, `create-exobook`) |
| Operational verbs | ~20 |

---

## File map

Full focused-mode file map: [`../roadstart/README.md`](../roadstart/README.md). Most-related to this doc:

- [`attestor-atom-schema.md`](attestor-atom-schema.md) — boolean attestation schemas referenced from "Attestation model"
- [`custodial-crypto-risk-form.md`](custodial-crypto-risk-form.md) — P1 lean risk-form body (full body at `../risk-framework/custodial-crypto-risk-form.md`)
- [`grounding-and-workcells.md`](grounding-and-workcells.md) — grounded execution / sigil / workcell / bootstrap model
- [`roadmap-ideas.md`](roadmap-ideas.md) — patterns this doc instantiates (lift, insyn/exsyn, phase-invariant)
- [`v1-principles.md`](v1-principles.md) — invariants distilled from the carve-outs section
- [`p1-nfat-atom-trace.md`](p1-nfat-atom-trace.md) — atom-level companion to the worked NFAT example
- [`p1-borrower-nfat-user-scenario.md`](p1-borrower-nfat-user-scenario.md) — narrative borrower-to-ER scenario using the same topology
- [`phase-1-overview.md`](phase-1-overview.md) — fronts-orientation layer above this canonical spec
