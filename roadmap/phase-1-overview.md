# Phase 1 — Fronts

**Status:** Orientation layer for Phase 1 — the entry point above [`phase-1-spaces.md`](phase-1-spaces.md) (the canonical Space-by-Space spec). Organized by *fronts*: units of focused attention, not topology units.
**Last Updated:** 2026-05-14

---

## TL;DR

Phase 1's single deliverable: **real-time ER per Prime, emitted continuously, computed in production-quality synlang.** Settlement and penalty action stay manual; the synome publishes ER, governance consumes it externally.

The work divides into **fronts**. A front is a unit of focused attention on something important to get Phase 1 done — a region of the system, a participant, a challenge, a use-case. Fronts cross-cut topology and cross-cut each other; the same thing (synserv, the patch beacon) shows up through more than one lens, by design.

Three **structural fronts** — where in the system:

| Front | Role |
|---|---|
| **The Core** | the engine — can the substrate run signed, scheduled, scatter-gather loops at all |
| **Prime–Halo** | the deliverable — the ER calculation and everything that plugs into it |
| **Demand Side** | a major input — structural-demand capacity feeding `structbook` matching |

Six **operator fronts** — who runs it: `synserv` (+ Guardian/Ozone), `govops`, `Attestor Oracle`, `Market Oracle`, `patch beacon`, `test-runner`.

---

## Read first — global guardrails

Cross-cutting things to know before touching any front, so nothing gets re-litigated or rabbitholed.

- **What's locked — don't relitigate.** Capital-math vocabulary, the naming convention, the 6-class beacon taxonomy. All settled. See [`p1-design-followups.md`](p1-design-followups.md) §0.
- **Build it once — the lift principle.** Code → synlang, data → atoms, from day 1. No Python placeholders that get rewritten. Black-box deferrals are honest scaffolds (real signature, opaque body). See [`roadmap-ideas.md`](roadmap-ideas.md).
- **Fix the consumption site, migrate the provenance.** Phase-invariant consumption sites make later transitions purely additive. Never cross-space-reference-then-fix-later. See [`roadmap-ideas.md`](roadmap-ideas.md) "Phase-invariant consumption sites."
- **What's deliberately deferred — the 13 v1 carve-outs.** See [`v1-principles.md`](v1-principles.md) for the invariants distilled from the carve-outs. The carve-out list itself lives in [`phase-1-spaces.md`](phase-1-spaces.md) (reconciled to v3 with the structural-demand-runs-live revision baked into carve-out #1).
- **Tempted to sudo mid-phase? You've started a new phase.** Any sudo event during Phase 1 is a phase boundary by construction.

---

## What a front is

A front is a **unit of focused attention** — "here is something important, here is what's hard about it, here is what to watch so you don't get sidetracked." A front is *not* a topology unit: it can span multiple entarts and overlap other fronts.

Two kinds today:

| Kind | Defined by | Per-front shape |
|---|---|---|
| **Structural** | the Spaces it covers ("where in the system") | what it is · Spaces it covers · challenges · watch out |
| **Operator** | the participant ("who runs it") | what it does · user scenarios · how it plugs in · challenges · watch out |

**The structural/operator split is a maturity gradient, not a permanent taxonomy.** Every operator is ultimately a local telart — as the system matures, each operator front crystallizes into a structural front (the operator *is* its telart, per substrate-as-identity). Near-term, operators are deliberately described as fuzzy human stuff — roles, scenarios, who-does-what — because that is what makes Phase 1 legible as a normal roadmap plan. Over time the operator fronts converge into topology.

Because fronts cross-cut, the same component appears through several lenses — e.g. `synserv` is the heartbeat *machinery* (The Core), the rollup *loop body* (Prime–Halo), and an *operator* (the synserv front). That is intended, not a conflict.

---

## Structural fronts

### The Core — the engine

**What it is.** The substrate that lets the synome run signed, scheduled, scatter-gather loops at all. Thin but foundational; everything else stands on it.

**Spaces it covers.** `&core.syngate` (trust-boundary primitive); `&core.loop.synserv` (heartbeat loop body); `&core.registry.beacon` (beacon identities + cert/auth — absorbs the legacy Guardian root's authority chain); the grounded-atom surface (baseline primitives + conformance machinery — assumed-in-runtime, **no registry Space**). (`&core.test-suite` is core substrate but counted under the test-runner front below.)

**Challenges.** Getting `syngate` right — it is *the* trust boundary, the one inspectable point where authority lives. Pinning down the baseline grounded-atom surface — which primitives, what signatures, what conformance tests.

**Watch out.** Grounded atoms are part of the runtime's evaluation surface, not Space content — there is no grounded registry to build (see [`p1-design-followups.md`](p1-design-followups.md) and the grounded-atoms reasoning). Risk-form equations are **not** here — they belong to Prime–Halo.

### Prime–Halo — the deliverable

**What it is.** The front that owns the Phase 1 deliverable: **real-time ER per Prime.** Everything else plugs into and works toward the ER calculation.

**Spaces it covers.** The `&core.loop.synserv` *body* (the rollup logic itself); the 7 prime entarts (`root` / `primebook` / `structbook` / `relay` / `protocol-registry`); the 3 halo entarts (`root` / `nfat-term` halo class / `custodial-crypto` risk class / `custodial-crypto.attest-data` attestor loop / `relay` / `protocol-registry`); constructor-made `halobook` / `riskbook` / `exobook` Spaces; market-data ticks from `&entity.oracle.crypto-majors.ticks`; the boolean attestor gate; the **patch beacon + insyn/exsyn TRRC split** (`TRRC = insynTRRC + exsynTRRC`, exsyn supplied by `patch-{prime}` into each `&entity.prime.{id}.primebook`); govops verbs; the NFAT instrument (Halo↔Prime); the rollup path `exobook → riskbook → halobook → NFAT → primebook → ER`.

**Challenges.** The **ER calculation everything plugs into** — `ER = TRRC / TRC`, emitted as `(prime-er $prime $value $T)` per heartbeat. **Dynamic auto-wiring** — a constructor *connects*, it doesn't just allocate: a new `exobook` must be immediately live in the rollup (registry, parent pointers, synserv sweep, attestor accord, oracle subscription) with zero follow-up sudo. Making the patch beacon cohere with the insyn/exsyn split.

**Watch out.** The attestation is a **boolean admission gate, not a data source** — see [`attestor-atom-schema.md`](attestor-atom-schema.md). Everything quantitative is **insyn** (`chain-read` + `market-data`). No instrument borrower↔Halo — the loan disbursement is plain book atoms; the NFAT exists only Halo↔Prime. Risk forms live in per-halo risk class Spaces (`&entity.halo.{id}.custodial-crypto`) — no canonical `&core.framework.risk.forms` Space in P1; conformance tests bind the per-halo copies until canonical propagation ships.

### Demand Side — a major input

**What it is.** Structural-demand capacity: how much USDS liability is sticky enough to support matched assets at each duration tier. Feeds `structbook` matching, which is one input into the Prime–Halo ER calculation.

**Spaces it covers.** The **endoscraper** grounded-atom cluster; `&entity.generator.usge.structural-demand` (scraped USDS/DAI/sUSDS/sDAI holder + lot-age data + the structural-demand equation — Lindy + structural caps — runs live in P1); `&entity.generator.usge.auction` (the **fake-auction infra** — sudo-set per-Prime per-bucket allocation atoms; structbooks read here); `&entity.generator.usge.protocol-registry` (USDS/DAI/sUSDS/sDAI ERC20 contract refs). Per-protocol metadata for chain-reads lives in per-entart `protocol-registry` sub-Spaces (each Prime, Halo, and the Generator carries its own), not a single `&core.protocol`.

**Challenges.** **Open-ended search/indexing over chainstate** — the endoscraper is not a point-lookup; it discovers and iterates over holder data, not "verify a known hash." Which grounded atoms the endoscraper exposes (the point-lookup `chain-read` plus open-ended-search primitives). The synlang↔endoscraper control dynamic — synlang "remote-controlling" the indexer.

**Watch out.** Prime–Halo has the **simple** endoscraper case (synserv verifying a relay's claim about a known mainnet tx) — don't conflate it with this front's open-ended case. The **fake auction must write `(structural-demand-allocation …)` atoms into the same consumption site, same shape** the future real auction (Prime-strategy-driven OSRC + Duration auctions) will — `structbook` matching reads allocation atoms identically whether sudo-written (P1) or auction-cleared (Phase 9+); only the writer changes. Capacity is computed live; *allocation* stays fake/sudo.

---

## Operator fronts

Participant-defined, described in human/role terms near-term. Each converges to a local telart over time.

### synserv (+ Guardian / Ozone)

**What it does.** `synserv` runs the canonical heartbeat (`&core.loop.synserv`), is the sole sequencer of synart writes, evaluates the rollup, and emits `(prime-er …)` per tick. Singleton. The **Guardian (Ozone)** is the authority that roots it — in P1 it holds all sudo authority and the cert chain; genesis is a sequence of Guardian sudo writes. "Who runs the canonical instance, and under what authority."

**User scenarios.** Each tick: re-derive all book state from current input atoms, emit ER. A constructor-made book appears mid-stream → the sweep picks it up. Genesis: sudo writes the 64 fixed Spaces and seeds cert/auth content into `&core.registry.beacon` (the authority root — no standing Guardian Space). Failover: canonical synserv breaks → Core Council out-of-band signs `(canonical-synserv-runner X)`, subscribers reconnect — failover is an atom write.

**How it plugs in.** It *is* the engine that runs the Prime–Halo rollup; it reads what the oracle / govops / patch-beacon fronts write; it uses The Core's `syngate` + grounded atoms.

**Challenges / watch out.** Sole-sequencer is a bottleneck/SPOF — Phase 1 is single-leader + hot standby. Genesis sudo is the one unconstrained write surface; integrity rests on off-space audit + operator diversity.

### govops

**What it does.** The human-in-the-loop operational layer — Phase 1 beacons are deterministic programs, teleonome-less; govops is humans deciding what txs to send. **Prime-side** (`govops-prime`): deploy / rollover / withdraw. **Halo-side** (`govops-halo`): runs the constructors (`create-halobook` / `-riskbook` / `-exobook`), `record-unit`, lifecycle transitions, `update-exobook-state`.

**User scenarios.** A new deal arrives → `govops-halo` runs `create-exobook` / `create-riskbook` / `record-unit`. A Prime deploys capital → `govops-prime` runs `deploy-into-nfat`. At maturity → `rollover-nfat` or `withdraw-from-nfat`.

**How it plugs in.** Operates the Prime–Halo front's constructor-made book machinery and Prime deployment. Also certs the patch beacon (see the patch-beacon front).

**Challenges / watch out.** This is where the dynamic auto-wiring challenge bites — govops actions must produce immediately-live books with no follow-up sudo.

### Attestor Oracle (Book Attestation Oracle)

**What it does.** A rank-2 Oracle Entity that owns the attestor cert chain and operates `attest-data` beacons writing the **boolean** `riskbook-attestation` atom — one per riskbook, the legal / operational / credit underwriter for the riskbook's exobooks. For custodial-crypto it is *not* an oracle of loan facts (those are insyn); it underwrites legal structure, borrower credit standing, and custodian compliance. Full schema: [`attestor-atom-schema.md`](attestor-atom-schema.md).

**User scenarios.** Underwrite a new custodial-crypto loan's legal/ops/credit → sign the boolean. `refresh-due` approaches → re-underwrite (credit-review cadence, not market cadence). A material structural change (`scope-ref` mismatch) → re-attest. An attestation goes stale → the exobook drops out of the rollup (default-deny).

**How it plugs in.** The boolean gates whether the Prime–Halo front's exobooks roll up. Owns the cert chain that makes attestations recognizable.

**Challenges / watch out.** The surviving open sub-question is `scope-ref` granularity — which exobook atoms count as "structural." Don't rebuild the numeric-attestation model — it's a boolean.

### Market Oracle (Crypto Majors Oracle)

**What it does.** A rank-2 Oracle Entity that pushes price / liquidity / funding-rate ticks for the v1 universe (BTC, ETH, stETH, USDC) via `market-data` beacons into its entart root.

**User scenarios.** Each tick: push current market data. A feed diverges → provider redundancy / dispute.

**How it plugs in.** The live input the Prime–Halo front's risk-form equations consume for CRR computation. Distinct from the Attestor Oracle by trust model — objective, oracle-pushable from public venues.

**Challenges / watch out.** Provider redundancy and the dispute model are the trust surface; calibration of crypto stress scenarios is a governance open item.

### patch beacon

**What it does.** The per-Prime `patch-{prime}` exsyn-TRRC scaffold — govops-certed, Guardian-sudoed inline into each `&entity.prime.{id}.primebook` at genesis, writes `(exsyn-trrc-claim …)` atoms. The **insyn/exsyn bridge**: `TRRC = insynTRRC + exsynTRRC`, where exsyn covers legacy halos not yet synlang-native. The one beacon class with **no regulated framework** — designed to **sunset** as legacy halos migrate to insyn.

**User scenarios.** A legacy halo's TRRC needs updating → the patch beacon writes an `exsyn-trrc-claim` into the Prime's primebook. Over time, as halos migrate to insyn-native machinery, the exsyn component shrinks toward zero and the patch beacon retires — *with no change to the synlang that reads it.*

**How it plugs in.** Supplies the exsyn half of the Prime–Halo front's ER calculation. Govops-certed (relationship to the govops front). It is a textbook insyn/exsyn phased-buildout device — see [`roadmap-ideas.md`](roadmap-ideas.md).

**Challenges / watch out.** It is a deliberate scaffold, not architecture — keep it thin, keep the sunset path clear. No regulated framework is correct here, not a gap.

### test-runner

**What it does.** The testing practice. Runs the synart-native acceptance suite against a **shadow frame**, not canonical: the genesis → fork shadow → run suite → discard shadow → production flow. Each front contributes its own test atoms; the "risk form" normative spec lives here (conformance tests *are* the definition of the form in P1).

**User scenarios.** Genesis bootstrap → fork to shadow → run the full suite → discard → production starts on validation. A new front lands → it contributes test atoms to `&core.test-suite`. A dynamically-relevant change → re-run conformance in shadow before promotion.

**How it plugs in.** Uses The Core's test machinery (the two Spaces + the frame mechanism). Verifies every other front — it is the cross-cutting conformance lens.

**Challenges / watch out.** Tests carry the normative "risk form" spec until a canonical Space does — the test suite is load-bearing spec, not just verification. The test *machinery* is Core substrate; this front is the *practice*.

---

## Phase 1 topology by front

The 64 fixed Spaces sudo-allocated at genesis, grouped by which front *owns* them. Operator fronts that don't own additional Spaces (synserv+Guardian, govops, Attestor Oracle, patch beacon) operate Spaces inside the structural fronts they touch.

### Structural fronts

**The Core — 3**
- `&core.syngate` — trust boundary
- `&core.loop.synserv` — heartbeat loop body
- `&core.registry.beacon` — beacon identities + cert/auth (absorbs the legacy Guardian root)

**Prime–Halo — 53 fixed + unbounded constructor-made**

Per Prime ×7 — 35 Spaces:
- `&entity.prime.{id}.root` — registry + TRC atom + govops config
- `&entity.prime.{id}.primebook` — insynTRRC + exsyn-trrc-claim atoms; emits `(prime-er …)`
- `&entity.prime.{id}.structbook` — matched/unmatched blend; reads auction allocations
- `&entity.prime.{id}.relay` — govops-prime loop body
- `&entity.prime.{id}.protocol-registry` — Prime's PAU contract refs

Per Halo ×3 (spark-term / grove-term / maple-term) — 18 Spaces:
- `&entity.halo.{id}.root` — registry + constructors
- `&entity.halo.{id}.nfat-term` — halo class (standard halobook terms + permitted risk classes)
- `&entity.halo.{id}.custodial-crypto` — risk class (risk form)
- `&entity.halo.{id}.custodial-crypto.attest-data` — class-accordant attestor loop body
- `&entity.halo.{id}.relay` — govops-halo loop body
- `&entity.halo.{id}.protocol-registry` — Halo's PAU contract refs

Plus unbounded constructor-made `halobook` / `riskbook` / `exobook` per deal flow.

**Demand Side — 4**
- `&entity.generator.usge.root` — registry
- `&entity.generator.usge.structural-demand` — scraped holder data + capacity equation
- `&entity.generator.usge.auction` — fake-auction allocation atoms (structbooks read here)
- `&entity.generator.usge.protocol-registry` — USDS / DAI / sUSDS / sDAI ERC20 refs

### Operator-front-owned Spaces (additional)

**Market Oracle — 3**
- `&entity.oracle.crypto-majors.root` — registry
- `&entity.oracle.crypto-majors.market-data` — market-data beacon loop body
- `&entity.oracle.crypto-majors.ticks` — price / liquidity / funding atoms

**test-runner — 1**
- `&core.test-suite` — test atoms + runner loop + results (shadow-only writes)

### Operator fronts that don't own additional Spaces

- **synserv (+ Guardian/Ozone)** — operates `&core.loop.synserv` (Core). Genesis sudo writes happen via this front but produce no standing Guardian Space; cert/auth content folds into `&core.registry.beacon`.
- **govops** — operates `&entity.prime.{id}.relay` (×7) and `&entity.halo.{id}.relay` (×3); runs the halo constructors.
- **Attestor Oracle** — operates `&entity.halo.{id}.custodial-crypto.attest-data` (×3, one per halo class instance); cert/auth in `&core.registry.beacon`.
- **patch beacon** — loop body + per-Prime config sudoed inline into each `&entity.prime.{id}.primebook` (×7); no separate Space.

### Cross-cutting reads — where the rollup spans Spaces

- synserv reads the entire entart tree on each heartbeat.
- `&entity.prime.{id}.structbook` reads `&entity.generator.usge.auction` for matching allocations.
- The risk form in each `&entity.halo.{id}.custodial-crypto` reads `&entity.oracle.crypto-majors.ticks` for market data.
- `(chain-read …)` calls resolve through whichever entart's `protocol-registry` is relevant (Prime PAUs, Halo PAUs, Generator ERC20s).

**Totals: 3 + 53 + 4 + 3 + 1 = 64 fixed Spaces** + unbounded constructor-made.

---

## File map

| Doc | Relationship |
|---|---|
| [`phase-1-spaces.md`](phase-1-spaces.md) | Canonical Space-by-Space Phase 1 spec (v3) — the detail under this orientation layer |
| [`p1-design-followups.md`](p1-design-followups.md) | What's locked (§0) + the open design threads (attestor schema resolved, risk-form signature, CORE integration, atom-level trace) |
| [`roadmap-ideas.md`](roadmap-ideas.md) | The lift principle, insyn/exsyn, black-box deferral, phase-invariant consumption sites — the iterative-development discipline the fronts are built on |
| [`v1-principles.md`](v1-principles.md) | The 13 v1 invariants / carve-outs (#1 revised — see the Demand Side front) |
| [`attestor-atom-schema.md`](attestor-atom-schema.md) | The boolean `riskbook-attestation` schema — anchors the Attestor Oracle front |
| [`../risk-framework/`](../risk-framework/) | The risk framework the Prime–Halo rollup computes; `riskbook-layer.md` is the home of the risk-form concept |
| [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) | The 6-class beacon taxonomy the operator fronts instantiate |
| [`../noemar-synlang/topology.md`](../noemar-synlang/topology.md) | Six-layer synome root, entart pattern, naming convention |
