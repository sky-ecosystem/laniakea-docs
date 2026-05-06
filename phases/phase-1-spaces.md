# Phase 1 — A Space Perspective (v2)

**Status:** Draft v2 (2026-05-06 redesign pass)
**Last Updated:** 2026-05-06
**Scope:** Phase 1 expressed in terms of synart Space topology — what Spaces exist, what each holds, what flows in and out, what's fixed vs operational.

---

## Framing

Phase 1's deliverable: **real-time ER per Prime, emitted continuously, computed in production-quality synlang.** Settlement and penalty action remain manual in Phase 1; the synome publishes ER, governance consumes it externally.

The architectural cut that drives everything below:

- **All logic in synlang from day 1.** No Python placeholders that get rewritten later. CRR equations, category match, sub-book routing, ER, equity invariants, health factors, loop bodies — all production synlang evaluated by Noemar. Python remains only for grounded primitives the runtime calls into (ed25519 verification, atom storage, network I/O, basic numeric ops). See `phases-ideas.md` "The lift principle."
- **Insyn/exsyn TRRC split.** TRRC = insynTRRC (synlang on Phase 1 halos' real positions) + exsynTRRC (oracle-fed gap-filler from legacy halos). TRC is fully synome-tracked at the Prime level. ER = TRRC / TRC.
- **6 Primes all active**, all deploying into 3 P1 Halos.
- **Halobooks/riskbooks/exobooks are constructor-made**, not sudo, since deals come in bursts.
- **Risk framework treated as a black box.** `&core-framework-risk-categories` holds one category in v1 (`crypto-collateralized-USD-lending`); the equation consumes oracle price+liquidity + exobook attestation and returns CRR. Internals deferred.
- **Attestation is one-per-exobook**, signed by a class-accordant attestor; without it the exobook can't roll up. This is the integrity check that makes the rollup trustworthy.
- **Root/cert/auth all sudo-set at genesis.** No Core GovOps role; the Guardian is the seat of authority with all role-defs/grants/certs sudo-written.

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
| **gate-mediated write** | Signed beacon submission through `&core-syngate`; sig + nonce + rate + auth + constructor execution. The normal operational path. |
| **constructor** | A verb that allocates new Spaces. Phase 1 has three: `create-halobook`, `create-riskbook`, `create-exobook`. |
| **fixed at genesis** | Sudo-written once during bootstrap; never changes during Phase 1. |
| **operational** | Atoms that change during Phase 1 via gate-mediated writes from registered beacons. |

---

## Universal Spaces (sudo at genesis)

| Space | Holds | Operational? |
|---|---|---|
| `&core-root` | Top-level sub-entart registry — Guardian + Generator + 6 Primes + 3 Halos | Fixed |
| `&core-syngate` | Gate state — nonce dedup window, per-pubkey rate-limit counters, external-verb whitelist, verb→target-Space routing table | Counters mutate per-message; whitelist + routing fixed |
| `&core-meta-topology` | Archetypes — declares valid shapes for halobook / riskbook / exobook / tranche / unit / attestation atoms; constructor validation reads here | Fixed |
| `&core-registry-beacon` | One row per beacon identity: pubkey, status, class, loop-pointer, per-entity-config-pointer | Fixed (status atoms can flip via sudo) |
| `&core-registry-entity` | Denormalized entity index mirroring the entart tree | Fixed at genesis; extended on book creation |
| `&core-registry-halo-class` | Halo class definitions — per class: riskbook category, accordant attestors, allowed collateral assets, custodian config | Fixed (3 classes for v1) |
| `&core-framework-risk-categories` | Riskbook category catalog — v1 has one: `crypto-collateralized-USD-lending`. The category equation is a synlang function consuming oracle price+liquidity + exobook attestation, returning CRR. Internal mechanics deferred (black-box). | Fixed |
| `&core-oracle` | All oracle-pushed atoms: per-asset price+liquidity ticks (BTC/ETH/stETH/USDC) and per-Prime `(exsyn-trrc-claim _)` | Operational |
| `&core-test-suite` | Test atom definitions | Fixed (extended by sudo on phase boundary) |
| `&core-test-results` | Test outcomes — written only in shadow frame | Operational (shadow only) |
| `&core-loop-synserv` | Synserv heartbeat — synlang body the runtime evaluates continuously; drives all derivations and ER emission | Fixed (loop body is the spec) |
| `&core-loop-oracle` | Universal template for oracle beacons (price+liquidity push) | Fixed |
| `&core-loop-oracle-exsyn` | Universal template for exo-quantity oracles (exsynTRRC) | Fixed |
| `&core-loop-attestor` | Universal template for class-accordant attestors; per-class config injected at boot | Fixed |
| `&core-loop-govops-prime` | Universal template for Prime govops beacons; per-Prime config injected at boot | Fixed |
| `&core-loop-govops-halo` | Universal template for Halo govops beacons; per-Halo config injected at boot | Fixed |
| `&core-loop-test-runner` | Test runner loop template (shadow only) | Fixed |

**17 universal Spaces.**

Note on loop templates: in v2, beacons run real synlang loops evaluated by Noemar. The templates contain canonical loop bodies; per-entity configs (in registry entries or entart roots) inject identity-specific parameters at boot per the two-step loop pattern (`topology.md §17`).

---

## Guardian (sudo at genesis)

| Space | Holds |
|---|---|
| `&entity-guardian-ozone-root` | Single operational guardian. Holds **all sudo-set authority state**: role-defs (`root-authority`, beacon classes), role-grants, cert atoms for every Phase 1 beacon. Sub-entart registry of generator + 6 primes + 3 halos. **Replaces Core GovOps as the seat of authority.** |

---

## Generator (sudo at genesis)

| Space | Holds |
|---|---|
| `&entity-generator-usge-root` | USDS Generator entart root; serves all 6 Primes |
| `&entity-generator-usge-genbook` | Aggregation of Primebook units from all 6 Primes; backs USDS issuance (Phase 1: tracking only, cross-Prime concentration deferred) |
| `&entity-generator-usge-structural-demand-auction` | Per-Prime per-bucket capacity allocations (sudo-set "fake auction"); 6 Primes × ~100 buckets of allocation atoms |

**3 Generator Spaces.**

---

## Per Prime — sudo at genesis (×6: spark, grove, obex, keel, skybase, launch6)

| Space | Holds |
|---|---|
| `&entity-prime-{id}-root` | Prime entart root. Auth atoms for the Prime's govops-prime beacon. Per-Prime govops config (which halos, deploy cadence, allocation strategy). **`(prime-trc {prime} {amount})` atom** — TRC, sudo-set at genesis, governance-updated. Optional per-halo capital allocation atoms for govops bookkeeping. |
| `&entity-prime-{id}-primebook` | Aggregates Halobook units the Prime holds. Computes insynTRRC via synlang sweep across structbook. Reads `(exsyn-trrc-claim {prime} _)` from `&core-oracle` for exsynTRRC. Reads TRC from root. Computes and emits `(prime-er {prime} {value} {timestamp})` real-time per heartbeat. |
| `&entity-prime-{id}-structbook` | The active Primebook sub-book. Reads NFAT units the Prime holds across all 3 halos via cross-book duality. Reads bucket allocations from generator structural-demand-auction. Computes matched/unmatched blend per position, structbook CRR per position. |

**3 Spaces × 6 Primes = 18 Spaces.**

In Phase 1, all 6 Primes deploy capital into NFATs from the 3 P1 Halos. The structbook is the only active Primebook sub-book in v1; other sub-books (`ascbook`, `tradingbook`, `termbook`, `hedgebook`, unmatched) are deferred per `risk-framework/primebook-composition.md`.

---

## Per Halo — sudo at genesis (×3)

| Space | Holds |
|---|---|
| `&entity-halo-{id}-root` | Halo entart root. Carries `(halo-class {halo} {class-id})` atom referencing its class in `&core-registry-halo-class`. Auth atoms for the halo's govops-halo beacon and its accordant attestor. Per-Halo govops config (allowed collateral, deal-size bounds). Sub-Space registry of constructor-made halobooks/riskbooks/exobooks. |

**3 Halo Spaces.**

Plus 3 halo class atoms in `&core-registry-halo-class`. Each class declares its riskbook category, accordant attestor, allowed collateral assets, custodian config.

---

## Constructor-made Spaces (per deal flow, unbounded)

These grow during operation as deals come in. All factory verbs respect class accord and parent-pointer integrity.

| Space pattern | Constructor (caller) | Purpose |
|---|---|---|
| `&entity-halo-{id}-halobook-{hbk-id}` | `create-halobook` (govops-halo) | One per deal burst. References halo class. Issues NFAT units to Primes via `record-unit`. |
| `&entity-halo-{id}-riskbook-{rbk-id}` | `create-riskbook` (govops-halo) | Under a halobook. Matches the class's riskbook category. Riskbook-issued unit held by halobook via cross-book duality. |
| `&entity-halo-{id}-exobook-{loan-id}` | `create-exobook` (govops-halo) | Per-borrower loan. Asset side: collateral references. Tranches: senior (static notional in USDC/USDT), junior (notional-rule = residual equity). State: lifecycle, debt outstanding. **Holds the exobook attestation atom** that closes the exobook for rollup. |

A v1 halo with N active loans has roughly: 1-few halobooks, 1-few riskbooks, N exobooks.

---

## Attestation model

**One attestation per exobook**, written by the class-accordant attestor:

```metta
;; in &entity-halo-{id}-exobook-{loan-id}
(exobook-attestation {loan-id}
   (attestor {attestor-id})                        ; must be class-accordant
   (timestamp T) (refresh-due T+24h)
   (assets-attested
      ((asset btc) (amount 1) (custodian _) (account _))
      ((asset eth) (amount 0)))
   (debt-outstanding 44000)
   (status all-good)
   (sig "..."))
```

The attestation **closes** the exobook: it's the single signed claim that all exoassets are valid and the loan structure is intact. Without a fresh accordant attestation, the exobook **does not roll up** — the riskbook category equation excludes it (default-deny), and the Prime's structbook can't account for the position. This is the integrity discipline that keeps attestors honest and prevents stale data from poisoning the rollup.

No Tier A/B split. The attestor walks the exobook, verifies assets at the custodian, signs one atom, posts via `post-exobook-attestation`.

---

## Beacons (all run real synlang loops in Noemar)

| Identity | Class | Loop template | Per-entity config |
|---|---|---|---|
| `synserv-canonical` | synserv | `&core-loop-synserv` | n/a (singleton) |
| `oracle-prices-{provider}` | oracle | `&core-loop-oracle` | per-provider in registry |
| `oracle-exsyn-{provider}` | oracle-exsyn | `&core-loop-oracle-exsyn` | per-provider in registry |
| `attestor-{class-id}` × 3 | attestor | `&core-loop-attestor` | per-class config in `&core-registry-halo-class` |
| `govops-prime-{id}` × 6 | govops-prime | `&core-loop-govops-prime` | per-Prime config in `&entity-prime-{id}-root` |
| `govops-halo-{id}` × 3 | govops-halo | `&core-loop-govops-halo` | per-Halo config in `&entity-halo-{id}-root` |
| `test-runner` | test | `&core-loop-test-runner` | shadow only |

**~15 beacon identities** registered in `&core-registry-beacon` at genesis. All loop bodies are production-quality synlang evaluated by Noemar. Pubkeys, status atoms, class atoms, loop-pointer atoms, and per-entity-config-pointer atoms all sudo-written.

---

## Operational verbs

| Verb | Caller | Effect |
|---|---|---|
| `create-halobook` | govops-halo | Allocates `&entity-halo-{id}-halobook-{hbk-id}`; registers under halo + class |
| `create-riskbook` | govops-halo | Allocates `&entity-halo-{id}-riskbook-{rbk-id}` under halobook |
| `create-exobook` | govops-halo | Allocates `&entity-halo-{id}-exobook-{loan-id}` under riskbook; writes initial assets + tranches |
| `record-unit` | govops-halo | Issues NFAT unit in halobook (`unit` atom: issuer/holder/notional/bucket/sptp) |
| `transition-book` | govops-halo | Book lifecycle state transitions |
| `update-exobook-state` | govops-halo | Updates attested asset structure, debt, etc. (within attestor's window) |
| `post-exobook-attestation` | attestor-{class-id} | Writes the exobook attestation atom |
| `deploy-into-nfat` | govops-prime | Increases Prime's holding of an NFAT unit; updates capital allocation atoms |
| `rollover-nfat` | govops-prime | At maturity, retires old NFAT, creates new under same/different halobook |
| `withdraw-from-nfat` | govops-prime | Reduces holding; returns capital to Prime root |
| `oracle-write-tick` | oracle-{provider} | Pushes price+liquidity atom to `&core-oracle` |
| `oracle-write-exsyn-trrc` | oracle-exsyn-{provider} | Pushes `(exsyn-trrc-claim {prime} {amount})` to `&core-oracle` |

**~12 operational verbs.**

---

## Operational write surface

| Beacon | Reads | Writes |
|---|---|---|
| `oracle-prices-{provider}` | external feeds (off-space) | `&core-oracle` (price+liquidity ticks) |
| `oracle-exsyn-{provider}` | external (off-space governance attestation) | `&core-oracle` (exsyn-trrc-claim) |
| `attestor-{class-id}` | exobook state under accordant halos, custodian APIs (off-space) | `(exobook-attestation _)` atoms in exobook Spaces |
| `govops-halo-{id}` | halo root config, class config, deal queue (off-space) | new halobook/riskbook/exobook Spaces; lifecycle + state atoms within |
| `govops-prime-{id}` | Prime root config, NFAT availability via cross-book duality, deploy schedule | NFAT-holding updates in halobooks; capital allocation atoms in Prime root |
| `synserv-canonical` | all input atoms across the entart tree | derived state atoms in book Spaces; `(prime-er _)` in primebooks |
| `test-runner` | (shadow only) | `&core-test-results` (shadow only) |

The pattern: input beacons (oracles, attestors) write into staging or book Spaces; govops beacons run constructors and capital flows; synserv runs the synlang heartbeat that drives all derived state and emits real-time ER.

---

## ER data flow (synserv heartbeat)

```
EXTERNAL INPUTS
  oracle-prices ─────→ &core-oracle (price + liquidity per asset)
  oracle-exsyn ────────→ &core-oracle ((exsyn-trrc-claim prime _) only)
  attestor-{class} ──→ exobook attestation atoms in exobook Spaces
  govops-halo-{id} ──→ create-* / record-unit / transition / update-state
  govops-prime-{id} ─→ deploy / rollover / withdraw / update-capital-allocation

SYNSERV HEARTBEAT (evaluating &core-loop-synserv)

  exobook level
    read: attestation atom + asset list + tranches + oracle prices+liquidity
    derive: junior_residual via notional-rule, health_factor, equity, attested status
    if no fresh accordant attestation → exobook excluded from rollup

  riskbook level
    read: child exobook derivations + oracle (price+liquidity) + framework category equation
    derive: per-position CRR (category equation = black box consuming the inputs)

  halobook level
    read: child riskbook units (cross-book duality)
    derive: aggregate exposure; NFAT atoms projected as Prime-side assets

  Prime structbook level
    read: NFAT units held (via cross-book duality from all 3 halos' halobooks)
        + bucket allocations from generator structural-demand-auction
    derive: matched/unmatched blend; per-position CRR via structbook formula

  Prime primebook level
    read: structbook output → insynTRRC[prime]
        + (exsyn-trrc-claim prime _) from &core-oracle → exsynTRRC[prime]
        = TRRC[prime]
        read: (prime-trc prime _) atom in &entity-prime-{id}-root → TRC[prime]
    emit: (prime-er prime value T) ← every heartbeat, real-time

  genbook level
    read: Primebook units from all 6 Primes via cross-book duality
    Phase 1: tracking only; cross-Prime concentration deferred
```

---

## Frame Mechanism

A **frame** is a complete instance of synome state — every Space, every atom. The runtime can hold multiple frames simultaneously and operate against a chosen one (the active frame). Operations: `fork(source, new-id)`, `switch(frame-id)`, `discard(frame-id)`, `diff(a, b)`. Lives below the synomic surface — runtime feature, not a synart concept.

Phase 1 use case: clone-and-test isolation. Genesis bootstraps canonical → fork to shadow → run tests against shadow → discard shadow → canonical verified by structural identity.

Implementation: deep copy at this scale (~42 fixed Spaces, modest atom count); becomes copy-on-write at larger states later.

Future use cases: sudo event safety (apply to shadow first, observe, promote), forecasting, what-if queries, major migrations / repartitioning.

---

## Test System

A synart-native acceptance suite. Tests live as atoms in `&core-test-suite`; outcomes accumulate in `&core-test-results`. The whole suite is sudo-written at genesis. **Tests run against a shadow frame, not canonical**, using the Frame Mechanism.

Test categories for v2:

| Category | Verifies |
|---|---|
| **Topology** | All 42 fixed Spaces exist; sub-entart registries point correctly; entity index matches the actual tree |
| **Auth atoms** | Each operational verb has correctly-placed auth atoms; counts match expected per Prime / Halo |
| **Beacon registry** | All ~15 identities present, status active, class atoms set, loop pointers + config pointers set |
| **Risk framework** | The one risk category atom present and well-formed; class-attestor accord wired |
| **Halo classes** | 3 class atoms in registry; accordant attestors registered correctly |
| **Constructors** | `create-halobook` / `create-riskbook` / `create-exobook` happy-path + auth-failure + duplicate (idempotency) |
| **Attestation** | `post-exobook-attestation` happy-path; rollup behavior with stale/missing attestation (exobook excluded) |
| **ER computation** | synserv-internal CRR + insynTRRC + exsynTRRC + TRC → real-time ER emission against synthetic positions |
| **Oracle inputs** | tick processing; `(exsyn-trrc-claim _)` consumption |
| **Govops flows** | NFAT deploy / rollover / withdraw cycle; halo book setup |
| **Gate-level** | bad sig rejected; replay rejected; rate-limit enforced; unknown verb / identity rejected |

Genesis → shadow fork → test → discard shadow → production start (per `phases-ideas.md` "Frame mechanism" section).

---

## Genesis sudo sequence

After Phase 0 substrate is in place, Phase 1 genesis is a sequence of sudo writes:

1. Allocate the 17 universal Spaces
2. Allocate the 4 singleton Spaces (Guardian, Generator + Genbook + structural-demand-auction)
3. Allocate the 18 per-Prime Spaces (root, primebook, structbook × 6)
4. Allocate the 3 per-Halo root Spaces
5. Write the genesis authority chain into `&entity-guardian-ozone-root`: role-defs, role-grants, cert atoms for every Phase 1 beacon (~15 identities)
6. Write the risk category atom into `&core-framework-risk-categories` (`crypto-collateralized-USD-lending` with category equation signature; body deferred)
7. Write archetype atoms into `&core-meta-topology` (halobook / riskbook / exobook / tranche / attestation / unit shapes)
8. Write external-verb whitelist into `&core-syngate` (~12 operational verbs + input verbs)
9. Write routing table into `&core-syngate` (verb → target-Space mappings)
10. Write the 3 halo class atoms into `&core-registry-halo-class` (riskbook category, accordant attestor, allowed collateral, custodian config per class)
11. Register all ~15 beacon identities in `&core-registry-beacon` with pubkeys, classes, statuses, loop pointers, per-entity-config pointers
12. Write per-Prime configs in each `&entity-prime-{id}-root` (`(prime-trc _)` atom, govops-prime config)
13. Write per-Halo configs in each `&entity-halo-{id}-root` (class binding, govops-halo config)
14. Write structural-demand auction allocations into `&entity-generator-usge-structural-demand-auction` (per-Prime per-bucket; sudo-set fake auction)
15. Write the entity index into `&core-registry-entity` (denormalized mirror)
16. Write all test atoms into `&core-test-suite`; initialize `&core-test-results` empty
17. Configure operator-level test credentials (runtime config, not synart content)

After step 17, sudo stops. Runtime forks canonical → shadow, switches to shadow, runs the test suite, inspects, discards. Production starts after validation.

---

## What constitutes a phase boundary

By construction, **any sudo event in Phase 1 is a phase boundary**. Examples:

- Adding a new Prime
- Adding or moving a Halo
- Changing the risk category or adding a new one
- Adding new beacon classes
- Activating new sub-books (currently only `structbook` is active)
- Activating concentration caps
- Replacing the fake auction with real auctions
- Activating settlement closure (Phase 2 transition)
- Unfolding the risk framework category from black-box to detailed (would add `&core-framework-stress-scenarios`, `&core-framework-asset-stress-profile`, `&core-framework-asset-history` universal Spaces)
- Wiring up event-driven derivation (currently heartbeat sweep)

Each later phase is a topology delta — a precisely-specified set of sudo writes that extends what Phase 1 established. The substrate that books rest on never gets rewritten; new substrate gets added alongside.

---

## Totals

| Category | Count |
|---|---|
| Universal Spaces | 17 |
| Guardian | 1 |
| Generator | 3 |
| Per-Prime (×6 × 3) | 18 |
| Per-Halo (×3 × 1) | 3 |
| **Fixed Spaces at genesis** | **42** |
| Halo class atoms (registry) | 3 |
| Risk category atoms (registry) | 1 |
| Constructor-made (per deal) | unbounded |
| Beacon identities | ~15 |
| Constructors | 3 (`create-halobook`, `create-riskbook`, `create-exobook`) |
| Operational verbs | ~12 |

---

## File map

| Doc | Relationship |
|---|---|
| `phases-ideas.md` | Vocabulary, conventions, design notes, **the lift principle**, sudo staircase |
| `../noemar-synlang/topology.md` | Canonical topology reference (six-layer synome root, entart pattern, naming convention, Phase 1 commitments). This doc is the Phase 1 instantiation of those patterns. |
| `../macrosynomics/topology-layers.md` | Telos / axioms / topology / population layering and sudo discipline |
| `../macrosynomics/beacon-framework.md` | Two-tier authority + I/O role taxonomy; Phase 1 beacons are instances |
| `../noemar-synlang/runtime.md` | Auth model, gate primitive, construction verb pattern |
| `../risk-framework/` | Risk framework conceptual core; v1 collapses to one category equation as black box |
| `../inactive/pre-synlang/roadmap/phase1/` | Pre-synlang Phase 1 specs in older Synome-MVP vocabulary; mapping in `phases-ideas.md` |

---

## One-line summary

**Phase 1 v2 is 42 fixed Spaces (17 universal + Guardian + Generator's 3 + 6 Primes' 3 each + 3 Halos' 1 each) sudo-allocated at genesis, plus 3 constructors (halobook/riskbook/exobook factories) growing per deal flow, ~15 beacon identities running real synlang loops in Noemar, and a synserv heartbeat that derives real-time ER per Prime as `TRRC = insynTRRC + exsynTRRC` over fully-synome-tracked TRC; the risk framework is held opaque, attestation closes each exobook for rollup, root/cert/auth all sudo at genesis, and the synlang is production-quality lift from day 1, not Python placeholders.**
