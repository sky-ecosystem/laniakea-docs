# Phase 1 — A Space Perspective (v4)

**Status:** Draft v4 (2026-05-17 live-state cleanup — supersedes v3 of 2026-05-15)
**Last Updated:** 2026-05-17
**Scope:** Phase 1 expressed in terms of synart Space topology — what Spaces exist, what each holds, what flows in and out, what's fixed vs operational.

---

## Framing

Phase 1's deliverable: **real-time ER per Prime, emitted continuously, computed in production-quality synlang.** Settlement and penalty action remain manual in Phase 1; the synome publishes ER, governance consumes it externally.

The architectural cuts that drive everything below:

- **All logic in synlang from day 1.** No Python placeholders that get rewritten later. CRR equations, sub-book routing, ER, equity invariants, health factors, loop bodies — all production synlang evaluated by Noemar. Python remains only for grounded primitives the runtime calls into (ed25519 verification, atom storage, network I/O, basic numeric ops, the `(chain-read …)` endoscraper primitive). See [`roadmap-ideas.md`](roadmap-ideas.md) "The lift principle."
- **Insyn/exsyn TRRC split.** `TRRC = insynTRRC + exsynTRRC`; TRC fully synome-tracked; `ER = TRRC / TRC` emitted per heartbeat. insyn comes from the rollup over the 3 P1 halos' real positions; exsyn comes from a per-Prime `patch-{prime}` patch-beacon writing `(exsyn-trrc-claim …)` directly into each `&entity.prime.{id}.primebook`.
- **Daily synomic settlement cycle (DSC).** P1 has one in-synome settlement clock: daily cut at 13:00 UTC, processing window 13:00-16:00 UTC, settle/advance at 16:00 UTC. Legacy monthly settlement remains out-of-band and invisible to the synome. `&core.settlement` holds the daily epoch state; `&core.loop.synserv` advances it from wall clock and dispatches processing tasks.
- **Phase-invariant consumption sites.** Where a thing is *read from* is fixed in P1; only the provenance of what's written there can migrate later. Risk forms, loop bodies, structural-demand allocations all materialize at their consumption sites in P1; canonical sources (and propagation mechanisms) ship additively in later phases without relocating anything. See [`roadmap-ideas.md`](roadmap-ideas.md) "Phase-invariant consumption sites."
- **Per-entart local materialization.** Each halo carries its own copy of its halo class and risk class (with the class-accordant attestor loop as a sub-Space of the risk class). Each Prime, Halo, and the Generator carry their own `protocol-registry` with the chain contract refs they specifically need. Local reads everywhere; no cross-entart hops for the rollup.
- **Halo class vs risk class.** Two complementary class concepts per halo. The **halo class** defines standard halobook terms plus permitted risk classes (the policy template for halobook construction when funds are deployed without explicit terms). The **risk class** holds the risk form (the CRR equation) and the class-accordant attestor as a sub-Space. All 3 P1 halos share `nfat-term` × `custodial-crypto` but each materializes its own copies.
- **7 Primes all active**, deploying into the 3 P1 Halos (spark-term, grove-term, maple-term).
- **Halobooks / riskbooks / exobooks are constructor-made** by govops-halo, not sudo, since deals come in bursts.
- **Attestation is boolean, with borrower-admission and exobook surfaces.** Per [`attestor-atom-schema.md`](attestor-atom-schema.md), the class-accordant attest-data beacon underwrites legal / operational / credit facts the chain can't show. Borrower admission lives at the risk-class / halo-class level (disbursement account, collateral account, configurator whitelist, first-contact setup); exobook-level attestation gates deal-specific facts such as term / maturity enforceability. Quantitative inputs are insyn or market-memory derived (`chain-read` + market memory). Without fresh accordant pass atoms, the borrower or exobook is excluded from the rollup (default-deny).
- **Cert / auth all rooted in `&core.registry.beacon`.** The Guardian's cert-chain content folds into the beacon registry; no standing Guardian entart Space in P1.
- **Root holds registry + constructors only.** Operational logic (loop bodies, computations) lives in dedicated sub-Spaces. Universal pattern across every entart type.

This phase doc answers four questions:
1. What Spaces exist after genesis
2. What each holds and how it updates
3. What I/O flows between beacons, gate, and Spaces
4. What changes operationally vs sudo-only (any sudo event = phase boundary)

---

## Vocabulary refresher

| Term | Meaning |
|---|---|
| **sudo** | Direct atomspace write; bypasses gate. Used for genesis bootstrap and rare amendments. Off-space audit log + operator diversity for integrity. |
| **gate-mediated write** | Signed beacon submission through `&core.syngate`; sig + nonce + rate + auth + constructor execution. The normal operational path. |
| **constructor** | A verb that allocates new Spaces. Phase 1 has three: `create-halobook`, `create-riskbook`, `create-exobook`. |
| **fixed at genesis** | Sudo-written once during bootstrap; never changes during Phase 1. |
| **operational** | Atoms that change during Phase 1 via gate-mediated writes from registered beacons. |
| **halo class** | Halobook policy template — standard terms, permitted risk classes, tranching / issuance presets, rate limits, govops control keys. Lives per-halo at `&entity.halo.{id}.{halo-class-name}`. |
| **risk class** | Riskbook risk treatment — the bundle of risk form + class-accordant attestor. The attestor lives as a sub-Space (`…{risk-class-name}.attest-data`). |
| **risk form** | The synlang equation that consumes oracle market memory + `chain-read` inputs and returns per-risk-type CRR components. Lives inside the risk class Space. |
| **protocol-registry** | Per-entart chain-contract metadata (addresses + ABIs + event signatures). Each Prime, Halo, and the Generator owns its own. |
| **DSC** | Daily synomic settlement cycle: the only settlement cadence visible to the synome in P1. Legacy monthly settlement is out-of-band. |
| **market memory** | Compressed reducer outputs from source market tapes, emitted by the Crypto Majors Oracle into `&entity.oracle.crypto-majors.ticks`. |
| **phase-invariant consumption site** | A read location whose path stays the same across phases; only the *provenance* of what's written there can migrate. See [`roadmap-ideas.md`](roadmap-ideas.md). |

---

## Universal Spaces (sudo at genesis)

| Space | Holds | Operational? |
|---|---|---|
| `&core.syngate` | Gate state — nonce dedup window, per-pubkey rate-limit counters, external-verb whitelist, verb→target-Space routing table | Counters mutate per-message; whitelist + routing fixed |
| `&core.loop.synserv` | Synserv heartbeat loop body — synlang the runtime evaluates continuously; drives all derivations and ER emission | Fixed (loop body is the spec) |
| `&core.registry.beacon` | One row per beacon identity: pubkey, status, class, cert atoms, auth grants. Absorbs the legacy Guardian root's authority chain — Guardian's cert + auth content folds in here. | Fixed (status atoms can flip via sudo) |
| `&core.settlement` | Daily synomic settlement cycle state: cadence, cut/process times, epoch-zero, current-epoch, processing markers | Operational (synserv writes epoch/processing state) |
| `&core.treasury` | Sky treasury facts used by the P1 SDR allocator and long-term external transparency: Sky-controlled addresses, Sky Prime token share by epoch, source/provenance | Operational (synserv-triggered treasury update; sudoed values for unlaunched tokens) |
| `&core.test-suite` | Test atom definitions + (folded) shadow-only test results + test-runner loop body | Operational (shadow only) |

**6 universal Spaces.**

What's deliberately *not* here vs. earlier drafts:
- `&core.meta-topology` — archetypes for constructor validation fold into the per-halo halo class atoms (each halo class declares the shapes its constructors validate against).
- `&core.registry.entity` — tree-walk via root sub-space registries is canonical.
- `&core.registry.halo-class` — replaced by per-halo class copies in each halo entart, per the phase-invariant consumption-site principle.
- `&core.framework.risk.categories` (and the broader `&core.framework.*` layer) — no canonical Space in P1; per-class risk forms live in halo entarts. Canonical source + propagation mechanism arrives in a later phase additively.
- `&core.protocol` — chain-protocol metadata moved to per-entart `protocol-registry` sub-Spaces (each Prime, Halo, and the Generator own their own contract refs locally).
- `&core.test-results` — folded into `&core.test-suite`.
- `&core.loop.market-data`, `&core.loop.attest-data`, `&core.loop.relay.govops-prime`, `&core.loop.relay.govops-halo`, `&core.loop.test-runner` — per-entity instances hold their loop bodies in P1 (sudo-set, self-contained); canonical templates ship additively in a later phase, propagating into the same per-entity Spaces. Each per-entity Space remains the consumption site across phases.

---

## Generator (sudo at genesis)

| Space | Holds |
|---|---|
| `&entity.generator.usge.root` | USDS Generator entart root — identity, auth, sub-space registry |
| `&entity.generator.usge.structural-demand` | Structural-demand bucket capacity atoms. P1 capacities are governance/sudo-set; Lindy + lot-age computation lands later without moving the read path |
| `&entity.generator.usge.auction` | Synserv-triggered pro-rata SDR allocator body and per-Prime per-bucket allocation atoms; structbooks read here for liability matching |
| `&entity.generator.usge.protocol-registry` | USDS / DAI / sUSDS / sDAI ERC20 contract addresses + ABIs + Transfer event signatures |

**4 Generator Spaces.**

Genbook (Primebook-unit aggregation backing USDS issuance) is deferred — P1's deliverable is real-time ER per Prime emitted at the primebook layer; Genbook tracking sits above the deliverable and lands at a later phase boundary alongside cross-Prime concentration enforcement.

P1 uses 30-day buckets (51 total; bucket 50 is 1,500+ days). Bucket capacities are governance-set atoms in `structural-demand`. During the daily DSC processing window, synserv calls the pro-rata SDR allocator body in `auction`, which writes `(structural-demand-allocation {prime} {bucket} {amount} {epoch})` atoms for the next epoch. Structbooks read allocations where `epoch = current-epoch`. **The consumption site is fixed**: in a later phase, real auctions write the same atom shape into the same Space — only the writer changes.

The P1 allocator's temporary equation is fully contained in `&entity.generator.usge.auction`:

```text
sky_effective_ownership(p) = 0.05 + 0.95 × sky_prime_token_share(p)
ownership_weight(p) = sky_effective_ownership(p) × prime_ijrc(p)
allocation(p, bucket) = bucket_capacity(bucket) × ownership_weight(p) / Σ ownership_weight(active primes)
```

Weights are recomputed every DSC epoch from latest `&core.treasury` token-share facts and each Prime root's IJRC atom. A Prime with missing, stale, or zero IJRC receives zero allocation. Unlaunched token shares still count as ownership through supplied treasury facts. If there are no positive active Prime weights, allocation rounds to zero; any rounding/dust remainder also rounds to zero. Unused allocation has no carry-forward accounting: each epoch's atoms are the live SDR allocation for that epoch, and older atoms are historical.

`&core.treasury` stores the raw token-share fact; the temporary ownership-weight computation lives only in the allocator body.

---

## Oracle Entity — sudo at genesis (×1)

Phase 1 has one oracle entity: Crypto Majors Oracle for market data. (Book Attestation Oracle, an entity that existed in earlier drafts, no longer has its own entart Space — its cert chain folds into `&core.registry.beacon`, and class-accordant borrower/riskbook/exobook attestation atoms land directly in their target risk class or book Spaces.)

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
| `&entity.prime.{id}.root` | Prime entart root — identity, auth, sub-space registry, `(prime-trc {prime} {amount})` atom (TRC, sudo-set, governance-updated), per-Prime govops config (allowed halos, deploy cadence, allocation strategy) |
| `&entity.prime.{id}.primebook` | Aggregates Halobook units the Prime holds via cross-book duality. Computes insynTRRC via synlang sweep across structbook. Holds `(exsyn-trrc-claim {prime} {amount} {timestamp})` atoms locally — written by the per-Prime `patch-{prime}` patch-beacon (sudoed inline at genesis). Reads TRC from root. Computes and emits `(prime-er {prime} {value} {timestamp})` real-time per heartbeat. |
| `&entity.prime.{id}.structbook` | The active Primebook sub-book. Reads NFAT units the Prime holds across all 3 halos via cross-book duality. Reads bucket allocations from `&entity.generator.usge.auction`. Computes matched/unmatched blend per position, structbook CRR per position. |
| `&entity.prime.{id}.relay` | Govops-prime beacon's loop body (deploy / rollover / withdraw against the Prime's PAUs). Per-entity sudo-set in P1; canonical template propagation comes additively later. |
| `&entity.prime.{id}.protocol-registry` | This Prime's PAU contract refs — Controller + ALMProxy + RateLimits addresses + ABIs + relevant event signatures |

**5 Spaces × 7 Primes = 35 Spaces.**

All 7 Primes deploy capital into NFATs from the 3 P1 Halos. The structbook is the only active Primebook sub-book in v1; other sub-books (`ascbook`, `tradingbook`, `termbook`, `hedgebook`, unmatched) are deferred per `risk-framework/primebook-composition.md`.

---

## Per Halo — sudo at genesis (×3)

Phase 1 has 3 Halos: **spark-term**, **grove-term**, **maple-term**. All three use the same halo class (`nfat-term`) and risk class (`custodial-crypto`) but each materializes its own per-entart copies (phase-invariant consumption-site principle).

| Space | Holds |
|---|---|
| `&entity.halo.{id}.root` | Halo entart root — identity, auth, sub-space registry of constructor-made books, constructors (`create-halobook` / `create-riskbook` / `create-exobook`) and their archetypes |
| `&entity.halo.{id}.nfat-term` | **Halo class** — standard halobook terms (NFAT halo unit, max TTM 1y), permitted risk classes `[custodial-crypto]`, tranching presets, issuance presets, rate limits, govops control keys |
| `&entity.halo.{id}.custodial-crypto` | **Risk class** — risk form (the stress-envelope equation that consumes market memory + `chain-read` inputs and returns default/spread/rate/liquidity CRR components) |
| `&entity.halo.{id}.custodial-crypto.attest-data` | Class-accordant attestor loop body — writes boolean borrower-admission, riskbook, and exobook attestation atoms per [`attestor-atom-schema.md`](attestor-atom-schema.md) |
| `&entity.halo.{id}.relay` | Govops-halo beacon's loop body — runs constructors, lifecycle transitions, attestation posting. Per-entity sudo-set in P1; canonical template propagation comes later. |
| `&entity.halo.{id}.protocol-registry` | This Halo's PAU contract refs — Controller + ALMProxy + RateLimits addresses + ABIs |

**6 Spaces × 3 Halos = 18 Spaces.**

---

## Halo class and risk class

Phase 1 introduces two complementary class concepts per halo. The split decouples on-chain operational mechanics from risk-side characterization.

### Halo class — the halobook policy template

The halo class defines what happens when funds are deployed into the halo *without explicit terms*: the halo class fills in the defaults. In P1 the halo class for all 3 halos is `nfat-term`, which says:

- Funds in queue are converted to an **NFAT halo unit** with maximum TTM 1 year.
- The unit is deployed only into riskbooks of permitted risk classes — `[custodial-crypto]` in P1.
- Standard tranching and issuance presets apply.
- Rate limits and govops control keys are bounded.

Halo unit holders can stay passive *because* the halo class's policy is bounded. Some halo classes will eventually be governance-mutable (parameters tunable by governance); others will be fully immutable (fixed ruleset, uniform risk/liquidity profile by design). Both forms fit the same Space; an immutability flag in the halo class atom is the mechanism.

The halo class lives at `&entity.halo.{halo-id}.{halo-class-name}` — the class name *is* the sub-kind. Each halo carries its own copy; canonical propagation arrives in a later phase additively.

### Risk class — the riskbook risk treatment

The risk class defines:

- **Risk form** — the equation that consumes oracle market memory + `chain-read` inputs and returns per-risk-type CRR components (default-CRR, spread-CRR, rate-CRR, liquidity-CRR). P1 uses a max-approved-scenario-loss exobook waterfall model; CORE is calibration/reference material, not the direct CRR engine. See [`../risk-framework/custodial-crypto-risk-form.md`](../risk-framework/custodial-crypto-risk-form.md).
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
| `&entity.halo.{id}.halobook.{hbk-id}` | `create-halobook` (govops-halo) | One per deal burst. References the halo class for standard terms. Issues NFAT units to Primes via `record-unit`. |
| `&entity.halo.{id}.riskbook.{rbk-id}` | `create-riskbook` (govops-halo) | Under a halobook. Bound to a risk class permitted by the halo class. Risk form imported in at creation. Riskbook-issued unit held by halobook via cross-book duality. |
| `&entity.halo.{id}.exobook.{loan-id}` | `create-exobook` (govops-halo) | Per-borrower loan. Asset side: collateral references (`chain-read` against borrower's collateral account) or staged PAU cash before send. Tranches: senior (static notional in USDC/USDS/USDT), junior (notional-rule = residual equity). State: lifecycle, debt outstanding, funding confirmation, maturity/TTM. Rollup-gating borrower/riskbook admission lives in the risk class/riskbook attestation surfaces. |

A v1 halo with N active loans has roughly: 1–few halobooks, 1–few riskbooks, N exobooks.

---

## Attestation model

Custodial-crypto has three attestation surfaces: borrower admission, riskbook shared-structure attestation, and exobook term attestation.

**Borrower admission / first-contact attestation** lives at the risk-class level. It records that the borrower, disbursement account, collateral account, Configurator whitelist path, custody setup, and legal framework are acceptable for this halo's `custodial-crypto` class. The Halo relay cannot unilaterally create this authority surface: halo govops coordinates with Core Council so the relevant aBEAM/configurator path whitelists the borrower/account setup. The halo relay is the Halo PAU relay for pBEAM and cBEAM execution, but new borrower admission needs the Core Council / aBEAM whitelist process plus the special first-contact attestation.

```metta
;; in &entity.halo.{id}.custodial-crypto
(custodial-borrower-admission {borrower-id}
   (disbursement-account ethereum {addr})       ; where principal is sent
   (collateral-account    ethereum {addr})       ; account tracked/liquidated against
   (configurator-whitelist ok)
   (legal-framework ok)
   (account-binding ok)
   (custody-setup ok)
   (status ok)
   (scope-ref {borrower-setup-hash}))
```

**Riskbook shared-structure attestation** remains boolean and class-accordant. For Phase 1's `custodial-crypto` risk class every quantitative CRR input is insyn (`chain-read` for collateral, debt, and funding state; market-memory atoms for price, liquidity, volatility), so the attestor is a legal / operational / credit underwriter, not an oracle of loan facts.

```metta
;; in &entity.halo.{id}.riskbook.{rbk-id}
(riskbook-attestation {rbk-id}
   (attestor      {attest-data-{halo-id}-id})  ; must be class-accordant
   (timestamp     T)
   (refresh-due   T+{review-cadence})          ; credit-review paced, governance-set per halo class
   (underwriting  pass)                        ; pass | fail — gates the riskbook's shared setup
   (claims                                     ; itemized liability surface
      (legal-structure-enforceable  true)
      (borrower-credit-standing     normal)    ; normal | watch | impaired
      (custodian-compliance-current true))
   (scope-ref     {structural-config-hash})    ; binds the boolean to shared borrower/custodian/legal structure
   (sig           "..."))
```

**Exobook term attestation** is per individual exobook. The main P1 variable fact is term: the attestor verifies that the stated maturity / TTM and cash-conversion terms are true and enforceable. The risk form uses that certified term only after funding confirmation.

```metta
;; in &entity.halo.{id}.exobook.{loan-id}
(exobook-term-attestation {loan-id}
   (attestor      {attest-data-{halo-id}-id})
   (timestamp     T)
   (refresh-due   T+{review-cadence})
   (underwriting  pass)
   (claims
      (term-enforceable           true)
      (maturity-T                 {maturity-T})
      (ttm-days-at-funding        {ttm-days})
      (cash-conversion-path-valid true))
   (scope-ref     {exobook-term-config-hash})
   (sig           "..."))
```

The attestations **gate** rollup: borrower admission admits the borrower; riskbook attestation admits the shared legal/custody setup; exobook term attestation admits the individual loan's term. Without fresh accordant pass atoms — `fail`, stale (`now > refresh-due`), or missing — the relevant borrower, riskbook, or exobook **does not roll up**. This is the integrity discipline that keeps attestors honest and prevents stale legal/credit facts from poisoning the rollup.

The attestor loop body lives at `&entity.halo.{id}.custodial-crypto.attest-data` — structurally owned by the risk class. The class-accordance is therefore structural: the attestor operates only on borrower admissions, riskbooks, and exobooks bound to its class.

### Exobook staged lifecycle

The exobook and exo units can be created before funds are sent to the borrower. In the staged state, the exobook contains reserved USDC / USDS / USDT still sitting inside the Halo PAU. The money is operationally committed to the relay strategy, but it is not yet borrower credit exposure and not yet SDR-matchable term exposure.

```text
borrower admitted
  -> exobook + exo units created in staged/pre-send state
  -> PAU cash reserved
  -> exobook term attestation posted
  -> relay sends funds to disbursement account
  -> funding tx confirms
  -> exobook becomes funded/active
  -> certified maturity/TTM becomes official for SDR matching
```

If the send or attestation fails, the reserve unwinds back to ordinary PAU cash. The position never becomes active term exposure.

---

## Beacons (all run real synlang loops in Noemar)

| Identity | Class | Admin'd by | Loop body location |
|---|---|---|---|
| `synserv-canonical` | synserv | Core Council (singleton) | `&core.loop.synserv` |
| `market-data-crypto-majors-{provider}` | market-data-beacon | Crypto Majors Oracle | `&entity.oracle.crypto-majors.market-data` |
| `attest-data-{halo-id}` × 3 | attest-data-beacon | (cert + auth in `&core.registry.beacon`) | `&entity.halo.{id}.custodial-crypto.attest-data` |
| `patch-{prime}` × 7 | patch-beacon | govops (Guardian sudo cert at genesis) | sudoed inline into `&entity.prime.{id}.primebook` |
| `govops-prime-{id}` × 7 | relay (stem `govops-prime`) | each Prime | `&entity.prime.{id}.relay` |
| `govops-halo-{id}` × 3 | relay (stem `govops-halo`) | each Halo | `&entity.halo.{id}.relay` |
| `test-runner` | test | n/a | folded into `&core.test-suite` (shadow only) |

**~23 beacon identities** registered in `&core.registry.beacon` at genesis (1 synserv + 1+ market-data + 3 attest-data + 7 patch + 7 govops-prime + 3 govops-halo + 1 test). All loop bodies are production-quality synlang evaluated by Noemar. Per-entity Spaces hold the loop bodies in P1 (self-contained); canonical loop templates ship additively in a later phase per the phase-invariant consumption-site pattern.

Patch-beacons remain the one beacon class without a regulated framework — Guardian-sudoed primitives, govops-certed, with loop body + per-entity config sudoed inline into the target Space (no universal template, no oracle-entity hop). Designed to sunset as their use cases migrate to insyn-native machinery.

---

## Operational verbs

| Verb | Caller | Effect |
|---|---|---|
| `create-halobook` | govops-halo | Allocates `&entity.halo.{id}.halobook.{hbk-id}`; registers under halo root with reference to halo class |
| `create-riskbook` | govops-halo | Allocates `&entity.halo.{id}.riskbook.{rbk-id}` under halobook; binds to a permitted risk class; imports risk form |
| `create-exobook` | govops-halo | Allocates `&entity.halo.{id}.exobook.{loan-id}` under riskbook; writes initial assets + tranches |
| `record-unit` | govops-halo | Issues NFAT unit in halobook (mints into Prime's PAU as primebook asset / halobook liability) |
| `transition-book` | govops-halo | Book lifecycle state transitions |
| `update-exobook-state` | govops-halo | Updates lifecycle, funding confirmation, and non-market exobook state within attestor scope |
| `post-borrower-admission` | attest-data-{halo-id} | Writes the boolean `custodial-borrower-admission` atom into the target risk class Space |
| `post-riskbook-attestation` | attest-data-{halo-id} | Writes the boolean `riskbook-attestation` atom into the target riskbook Space |
| `post-exobook-attestation` | attest-data-{halo-id} | Writes the boolean `exobook-term-attestation` atom into the target exobook Space |
| `deploy-into-nfat` | govops-prime | Increases Prime's holding of an NFAT unit; updates capital allocation atoms |
| `rollover-nfat` | govops-prime | At maturity, retires old NFAT, creates new under same/different halobook |
| `withdraw-from-nfat` | govops-prime | Reduces holding; returns capital to Prime root |
| `market-data-write-memory` | market-data-crypto-majors-{provider} | Pushes current-state atoms, reducer outputs, and reducer checkpoints to `&entity.oracle.crypto-majors.ticks` |
| `patch-write-exsyn-trrc` | patch-{prime} | Writes `(exsyn-trrc-claim {prime} {amount} {timestamp})` directly into `&entity.prime.{id}.primebook` |

**~14 operational verbs.** Epoch advancement is not an operational verb; synserv derives it from wall clock and writes `&core.settlement` state.

---

## Operational write surface

| Beacon | Reads | Writes |
|---|---|---|
| `market-data-crypto-majors-{provider}` | external feeds and archive-node reducer outputs: exchange APIs, on-chain DEXes, perp venues, options, rates, macro factors | `&entity.oracle.crypto-majors.ticks` (current market-state + rolling market-memory atoms) |
| `patch-{prime}` (patch-beacon) | external (off-space governance attestation about legacy halo TRRC for this Prime) | `&entity.prime.{id}.primebook` (`(exsyn-trrc-claim {prime} {amount} {timestamp})` atoms, written locally) |
| `attest-data-{halo-id}` (attest-data-beacon) | borrower setup, riskbook structural state, exobook term state, custodian / legal-counsel / borrower-credit assessments (off-space) | `(custodial-borrower-admission _)`, `(riskbook-attestation _)`, and `(exobook-term-attestation _)` boolean atoms |
| `govops-halo-{id}` | halo root config, halo class, risk class, deal queue (off-space) | new halobook/riskbook/exobook Spaces; lifecycle + state atoms within |
| `govops-prime-{id}` | Prime root config, NFAT availability via cross-book duality, deploy schedule | NFAT-holding updates in halobooks; capital allocation atoms in Prime root |
| `synserv-canonical` | all input atoms across the entart tree; chain state via `(chain-read …)`; wall clock for DSC | derived state atoms in book Spaces; `&core.settlement` epoch/processing atoms; `&core.treasury` refresh writes; SDR allocation dispatch; `(prime-er _)` atoms in primebooks |
| `test-runner` | (shadow only) | test results within `&core.test-suite` (shadow only) |

The pattern: input beacons (market-data, attest-data, patch) write into their target Spaces; govops beacons run constructors and capital flows; synserv runs the synlang heartbeat that drives all derived state and emits real-time ER.

---

## ER data flow (synserv heartbeat)

```
EXTERNAL INPUTS
  market-data-crypto-majors  ──→ &entity.oracle.crypto-majors.ticks
  patch-{prime}              ──→ &entity.prime.{id}.primebook ((exsyn-trrc-claim …))
  attest-data-{halo-id}      ──→ borrower/riskbook/exobook attestation atoms
  govops-halo-{id}           ──→ create-* / record-unit / transition / update-state
  govops-prime-{id}          ──→ deploy / rollover / withdraw / update-capital-allocation

SYNSERV HEARTBEAT (evaluating &core.loop.synserv)

  settlement / processing level
    read: wall clock + &core.settlement current-epoch
    if 13:00 UTC cut reached and processing not fired:
       write processing marker
       refresh &core.treasury token-share atoms
       run pro-rata SDR allocator for next epoch
    if 16:00 UTC settle reached:
       write next current-epoch atom

  exobook level
    read: chain-read of collateral/debt/loan-terms + market-memory atoms + tranches + lifecycle
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
        + current-epoch bucket allocations from &entity.generator.usge.auction
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

A **frame** is a complete instance of synome state — every Space, every atom. The runtime can hold multiple frames simultaneously and operate against a chosen one (the active frame). Operations: `fork(source, new-id)`, `switch(frame-id)`, `discard(frame-id)`, `diff(a, b)`. Lives below the synomic surface — runtime feature, not a synart concept.

Phase 1 use case: clone-and-test isolation. Genesis bootstraps canonical → fork to shadow → run tests against shadow → discard shadow → canonical verified by structural identity.

Implementation: deep copy at this scale (~66 fixed Spaces, modest atom count); becomes copy-on-write at larger states later.

Future use cases: sudo event safety (apply to shadow first, observe, promote), forecasting, what-if queries, major migrations / repartitioning.

---

## Test System

A synart-native acceptance suite. Tests live as atoms in `&core.test-suite`; results accumulate in the same Space (shadow-only). The whole suite is sudo-written at genesis. **Tests run against a shadow frame, not canonical**, using the Frame Mechanism.

Test categories for v4:

| Category | Verifies |
|---|---|
| **Topology** | All 66 fixed Spaces exist; sub-entart and sub-space registries point correctly; per-entart root contents present (TRC atom in prime roots, etc.) |
| **Auth atoms** | Each operational verb has correctly-placed auth atoms in `&core.registry.beacon`; counts match expected per Prime / Halo |
| **Beacon registry** | All ~23 identities present, status active, class atoms set, cert chains rooted |
| **Halo class / risk class** | All 3 halo entarts carry their `nfat-term` halo class and `custodial-crypto` risk class with the right shape; the attestor sub-Space is present and accordant |
| **Constructors** | `create-halobook` / `create-riskbook` / `create-exobook` happy-path + auth-failure + duplicate (idempotency); risk-form import on `create-riskbook` |
| **Attestation** | borrower admission, `post-riskbook-attestation`, and `post-exobook-attestation` happy paths; rollup behavior with stale / fail / missing attestations (borrower, riskbook, or exobook excluded — default-deny) |
| **ER computation** | synserv-internal CRR + insynTRRC + exsynTRRC + TRC → real-time ER emission against synthetic positions |
| **Oracle inputs** | market-memory reducer outputs and current-state atoms (market-data-beacon); `(exsyn-trrc-claim _)` consumption from per-Prime primebook (patch-beacon write path) |
| **Settlement / SDR allocator** | DSC epoch advance from mock clock; 13:00-16:00 processing idempotency; treasury refresh before allocation; allocation atoms stamped with next/current epoch as expected |
| **Govops flows** | NFAT deploy / rollover / withdraw cycle; halo book setup |
| **Gate-level** | bad sig rejected; replay rejected; rate-limit enforced; unknown verb / identity rejected |
| **Risk form conformance** | All 3 halos' `custodial-crypto` risk forms produce identical outputs on the same inputs (binds the per-class copies until canonical propagation ships) |

Genesis → shadow fork → test → discard shadow → production start.

---

## Genesis sudo sequence

After Phase 0 substrate is in place, Phase 1 genesis is a sequence of sudo writes. The order respects dependencies: universal infrastructure before entarts; entart roots and sub-spaces before their content; cert + auth in the beacon registry before beacon-pointed loop bodies.

1. Allocate the 6 universal Spaces (`&core.syngate`, `&core.loop.synserv`, `&core.registry.beacon`, `&core.settlement`, `&core.treasury`, `&core.test-suite`).
2. Allocate the 4 Generator Spaces (`usge.root`, `usge.structural-demand`, `usge.auction`, `usge.protocol-registry`).
3. Allocate the 3 Oracle Spaces (`crypto-majors.root`, `crypto-majors.market-data`, `crypto-majors.ticks`).
4. Allocate the 35 per-Prime Spaces (×7 × {root, primebook, structbook, relay, protocol-registry}).
5. Allocate the 18 per-Halo Spaces (×3 × {root, nfat-term, custodial-crypto, custodial-crypto.attest-data, relay, protocol-registry}).
6. Write `&core.syngate`'s external-verb whitelist + verb→target-Space routing table.
7. Write all ~23 beacon identities into `&core.registry.beacon` with pubkeys, classes, statuses, cert atoms, auth grants. (This absorbs the legacy Guardian-root authority chain into the beacon registry.)
8. Write per-Prime configs into each `&entity.prime.{id}.root` — `(prime-trc {prime} {amount})` atom and govops config.
9. Write per-Halo halo class content into each `&entity.halo.{id}.nfat-term` — standard terms (NFAT halo unit, max TTM 1y), `(permitted-risk-classes nfat-term [custodial-crypto])`, tranching / issuance presets, rate limits.
10. Write per-Halo risk class content into each `&entity.halo.{id}.custodial-crypto` — the stress-envelope risk form, scenario-binding config, and attestation gates.
11. Write per-Halo attestor loop bodies into each `&entity.halo.{id}.custodial-crypto.attest-data`.
12. Write per-Halo govops loop bodies into each `&entity.halo.{id}.relay`.
13. Write per-Halo `protocol-registry` content — Halo PAU contract refs.
14. Write per-Prime govops loop bodies into each `&entity.prime.{id}.relay`.
15. Write per-Prime `protocol-registry` content — Prime PAU contract refs.
16. Write per-Prime `patch-{prime}` patch-beacon — loop body + per-entity config + auth, sudoed inline into each `&entity.prime.{id}.primebook`.
17. Write Generator `protocol-registry` content — USDS / DAI / sUSDS / sDAI ERC20 contract refs.
18. Write `&core.settlement` initial state — DSC cadence, 13:00 UTC cut, 16:00 UTC process-end / settle time, epoch-zero, current-epoch.
19. Write `&core.treasury` initial state — Sky-controlled addresses and sudoed token-share values for unlaunched Prime tokens.
20. Write Generator `structural-demand` initial state — 30-day bucket definitions and governance-set bucket capacity values.
21. Write Generator `auction` content — ownership-weighted pro-rata SDR allocator body and empty/current allocation state.
22. Write Oracle `market-data` loop body into `&entity.oracle.crypto-majors.market-data`.
23. Write Oracle `ticks` initial state (empty, will populate from beacon writes/reducer outputs).
24. Write all test atoms + test-runner loop body into `&core.test-suite`.
25. Configure operator-level test credentials (runtime config, not synart content).

After step 25, sudo stops. Runtime forks canonical → shadow, switches to shadow, runs the test suite, inspects, discards. Production starts after validation.

---

## What constitutes a phase boundary

By construction, **any sudo event in Phase 1 is a phase boundary**. Examples:

- Adding a new Prime
- Adding or moving a Halo
- Adding a new halo class or risk class (the per-halo class copies pattern accommodates this; new entries are sudo writes)
- Adding new beacon classes
- Activating new sub-books (currently only `structbook` is active)
- Activating concentration caps
- Replacing the pro-rata SDR allocator with Prime-strategy-driven OSRC + Duration auctions (the auction Space's consumption shape stays fixed; only the writer changes — phase-invariant transition)
- Activating canonical loop-template propagation (adds `&core.loop.relay.govops-{prime,halo}`, `&core.loop.market-data` + propagation mechanism; per-entity Spaces stay where they are — phase-invariant transition)
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
   asset: btc 1                                      ; collateral (chain-read against borrower's on-chain account)
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

Risk form applies the approved scenario library and takes the worst senior-loss outcome. One illustrative scenario:
- BTC drops 45% → asset value falls from $80K to $44K
- USDC depeg stress: ~5%
- execution/liquidation haircut read from market-memory impact curves
- Junior cushion revalues consistently with the stressed asset side

Illustrative loss math:
- Asset value post-stress: $44K
- Junior cushion (in stressed BTC value): $44K × ($250K / $80K) = ~$13.75K
- Effective senior loss = max(0, asset_drop − junior_cushion) = max(0, $36K − $13.75K) = $22.25K
- USDC depeg loss on $750K notional: $750K × 0.05 = $37.5K
- Total stress loss: $59.75K
- Loss fraction: $59.75K / $750K ≈ 7.97%

This loss fraction is not expected loss. It is the senior exo-unit loss under the binding approved scenario. The risk form outputs all four components: default-CRR, spread-CRR, rate-CRR, liquidity-CRR. For this example, the exobook asset-side impairment feeds default-CRR.

### Step 4: Halobook P/T declarations

Spark-Term's halo class (`nfat-term`) declares:
- P (permitted unwind): only at maturity OR on health-factor breach
- T (transfer market): not transferable

### Step 5: Sub-book routing

Eligibility check at Spark Prime's Primebook level:
- `ascbook`: NO (not deep peg-defense liquid)
- `tradingbook`: NO (P AND T both restrictive — no exit path)
- `termbook`: NO (no tUSDS-matched liability)
- `structbook`: YES (has SPTP = 180 days, structural-demand capacity available)
- `hedgebook`: NO (no hedge instruments in v1 test)

→ Routes to Spark Prime's `structbook`. (In Phase 1 only `structbook` is the active Primebook sub-book; the others exist as schema placeholders.)

### Step 6: structbook capital math

Assume Spark Prime has been allocated $200M of bucket 6 (180 days under the 30-day bucket system) by the synserv-triggered pro-rata SDR allocator in `&entity.generator.usge.auction`.

For this single NFAT position held by Spark Prime:
- Position size: $750K
- Available capacity at bucket 6: $200M minus already-matched
- Assume $190M already matched, so $10M capacity remaining
- Matched portion: min($750K, $10M) = $750K (fully matched)
- Unmatched portion: $0

`structbook` capital:
- Matched: $750K × default-CRR ≈ $750K × 5% = $37.5K
- spread-CRR, rate-CRR, and liquidity-CRR are computed by the risk form but non-binding for the SDR-matched portion
- Unmatched: $0
- **Position capital: ~$37.5K** (default risk only; structural matching covers credit-spread, rate, and liquidity)

If capacity were exhausted before this loan landed:
- Matched portion: $0 (capacity full)
- Unmatched portion: $750K
- Unmatched capital: $750K × max(RW, Forced-Loss) ≈ $750K × max(5%, 7.97%) = $750K × 7.97% = $59.8K
- **Position capital: ~$59.8K**

The smooth blend (per `risk-framework/matching.md` §4) means capital scales continuously with capacity utilization — no binary cliff.

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

---

## V1 Carve-outs

Deliberate Phase 1 simplifications. Each has a clear later-phase replacement; the substrate the books rest on does not get rewritten when these unlock.

1. **Structural-demand capacity is governance-set in P1.** Lindy + structural caps and the open-ended lot-age endoscraper surface are deferred. The capacity atom shape and read path are fixed.
2. **30-day duration buckets** (51 total). Bucket N = N × 30 days; bucket 50 = 1,500+ days. Bucket size is independent of the daily settlement cadence.
3. **Daily synomic settlement cycle from day 1.** DSC is visible in synome; legacy monthly settlement remains out-of-band. DSC cut is 13:00 UTC, processing is 13:00-16:00 UTC, and epoch advance is synserv-derived from wall clock.
4. TTM range 0–12 months only (per `nfat-term` halo class).
5. SPTP = remaining nominal term (no stress modifier).
6. One Genbook (USDS) only — and Genbook itself is deferred in P1 (tracking only via the primebook layer).
7. Three Halos (spark-term, grove-term, maple-term) with seven Primes deploying into them.
8. Super-senior tranches only (mezzanine / equity-tranche holdings get CRR 100% by default-deny).
9. **Synserv-triggered pro-rata SDR allocator** in `&entity.generator.usge.auction` — ownership-weighted temporary equation using Sky token share from `&core.treasury` and per-Prime IJRC. There is no P1 reservation market, tug-of-war, sticky claim, durable SDR ownership, or carry-forward accounting. Real Prime-strategy-driven OSRC + Duration auctions replace the body without relocating the read path.
10. Single halo class (`nfat-term`) with single risk class (`custodial-crypto`); NFAT halo-unit issuance at max 1y TTM, deploying into `custodial-crypto` riskbooks only.
11. Active sub-books: only `structbook`.
12. Tranche rights schema present but not exercised.
13. JAAA / CLO modeling deferred (recursive complexity).
14. DR, LDR, tagging registry deferred; LDR activates with real structural-demand auctions that pay fees.
15. Core Entity halo-mode deferred; legacy exposures remain out-of-band / patch-fed for P1.

Companion principles distilled from these decisions live in [`v1-principles.md`](v1-principles.md).

---

## Totals

| Category | Count |
|---|---|
| Core shared Spaces | 6 (`syngate`, `loop.synserv`, `registry.beacon`, `settlement`, `treasury`, `test-suite`) |
| Generator (`usge`) | 4 |
| Oracle (`crypto-majors`) | 3 |
| Per-Prime ×7 (×5 each) | 35 |
| Per-Halo ×3 (×6 each) | 18 |
| **Fixed Spaces at genesis** | **66** |
| Constructor-made (per deal) | unbounded |
| Beacon identities | ~23 (1 synserv + 1+ market-data + 3 attest-data + 7 patch + 7 govops-prime + 3 govops-halo + 1 test) |
| Constructors | 3 (`create-halobook`, `create-riskbook`, `create-exobook`) |
| Operational verbs | ~14 |

---

## File map

| Doc | Relationship |
|---|---|
| [`phase-1-overview.md`](phase-1-overview.md) | Orientation entry point — Phase 1 organized by *fronts* (structural + operator). This doc is the canonical Space-by-Space detail under that orientation. |
| [`roadmap-ideas.md`](roadmap-ideas.md) | Vocabulary, conventions, design notes — the **lift principle**, sudo staircase, insyn/exsyn pattern, phase-invariant consumption sites. |
| [`v1-principles.md`](v1-principles.md) | Companion principles distilled from the Phase 1 carve-outs (SPTP, default-deny, smooth blend, currency-frame, etc.). |
| [`attestor-atom-schema.md`](attestor-atom-schema.md) | Borrower admission plus boolean riskbook/exobook attestation schema for the `custodial-crypto` risk class — design + rationale. |
| [`p1-design-followups.md`](p1-design-followups.md) | Current pickup list after this cleanup: atom-level trace and exact scenario/reducer catalogs remain open; attestor and risk-form direction are resolved. |
| `../noemar-synlang/topology.md` | Canonical topology reference (six-layer synome root, entart pattern, naming convention). This doc is the Phase 1 instantiation of those patterns. |
| `../macrosynomics/beacon-framework.md` | Two-tier authority + I/O role taxonomy; Phase 1 beacons are instances. |
| `../noemar-synlang/runtime.md` | Auth model, gate primitive, construction verb pattern. |
| `../risk-framework/` | Risk framework conceptual core; v1 collapses to one risk class (`custodial-crypto`) carrying the stress-envelope exobook-waterfall risk form. |
| `../inactive/archive/roadmap/phase1/` | Pre-synlang Phase 1 specs in older Synome-MVP vocabulary; vocabulary mapping in `roadmap-ideas.md`. |

---

## One-line summary

**Phase 1 v4 is 66 fixed Spaces — 6 universal Core (syngate, synserv loop, beacon registry, settlement, treasury, test suite), 4 Generator (root, structural-demand, auction, protocol-registry), 3 Oracle (crypto-majors root + market-data loop + ticks/market-memory), 35 per-Prime (×7 × {root, primebook, structbook, relay, protocol-registry}), and 18 per-Halo (×3 × {root, nfat-term halo class, custodial-crypto risk class, custodial-crypto.attest-data attestor loop, relay, protocol-registry}) — sudo-allocated at genesis, plus 3 constructors (halobook/riskbook/exobook factories) growing per deal flow, ~23 beacon identities running real synlang loops in Noemar with cert/auth rooted in the beacon registry, a daily synomic settlement cycle advanced by synserv from wall clock, a treasury refresh + ownership-weighted pro-rata SDR allocator during the 13:00-16:00 UTC processing window, and a heartbeat that derives real-time ER per Prime as TRRC/TRC where TRRC = insynTRRC + exsynTRRC; the P1 risk framework is one stress-envelope custodial-crypto risk form per halo, attestation is boolean/admission-focused with borrower and exobook term surfaces, market data is market-memory reducer output, and the synlang is production-quality lift from day 1, not Python placeholders.**
