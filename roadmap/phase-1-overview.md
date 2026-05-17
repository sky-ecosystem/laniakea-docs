# Phase 1 — Fronts

**Status:** Orientation layer for Phase 1 — the entry point above [`phase-1-spaces.md`](phase-1-spaces.md) (the canonical Space-by-Space spec). Organized by *fronts*: units of focused attention, not topology units.
**Last Updated:** 2026-05-17

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

Six **operator fronts** — who runs it: `synserv` (+ Guardian/Ozone), `relay / synops operators`, `Attestor Oracle`, `Market Oracle`, `patch beacon`, `test-runner`.

---

## Read first — global guardrails

Cross-cutting things to know before touching any front, so nothing gets re-litigated or rabbitholed.

- **What's locked — don't relitigate.** Capital-math vocabulary, the naming convention, the 6-class beacon taxonomy. All settled. See [`phase-1-spaces.md`](phase-1-spaces.md) "Framing" and [`../roadstart/big-picture.md`](../roadstart/big-picture.md).
- **Build it once — the lift principle.** Code → synlang, data → atoms, from day 1. No Python placeholders that get rewritten. Black-box deferrals are honest scaffolds (real signature, opaque body). See [`roadmap-ideas.md`](roadmap-ideas.md).
- **Fix the consumption site, migrate the provenance.** Phase-invariant consumption sites make later transitions purely additive. Never cross-space-reference-then-fix-later. See [`roadmap-ideas.md`](roadmap-ideas.md) "Phase-invariant consumption sites."
- **What's deliberately deferred — the v1 carve-outs.** See [`v1-principles.md`](v1-principles.md) for the invariants distilled from the carve-outs. The carve-out list itself lives in [`phase-1-spaces.md`](phase-1-spaces.md).
- **Tempted to sudo mid-phase? You've started a new phase.** Any sudo event during Phase 1 is a phase boundary by construction.

---

## What a front is

A front is a **unit of focused attention** — "here is something important, here is what's hard about it, here is what to watch so you don't get sidetracked." A front is *not* a topology unit: it can span multiple entarts and overlap other fronts.

Two kinds today:

| Kind | Defined by | Per-front shape |
|---|---|---|
| **Structural** | the Spaces it covers ("where in the system") | what it is · Spaces it covers · challenges + watch out |
| **Operator** | the participant ("who runs it") | what it does · operational shape · challenges + watch out |

**The structural/operator split is a maturity gradient, not a permanent taxonomy.** Every operator is ultimately a local telart — as the system matures, each operator front crystallizes into a structural front (the operator *is* its telart, per substrate-as-identity). Near-term, operators are deliberately described as fuzzy human stuff because that is what makes Phase 1 legible as a normal roadmap plan. Over time the operator fronts converge into topology.

Because fronts cross-cut, the same component appears through several lenses — e.g. `synserv` is the heartbeat *machinery* (The Core), the rollup *loop body* (Prime–Halo), and an *operator* (the synserv front). That is intended, not a conflict.

---

## Structural fronts

### The Core — the engine

**What it is.** The substrate that lets the synome run signed, scheduled, scatter-gather loops at all. Thin but foundational.

**Spaces it covers.** `&core.syngate` (trust boundary), `&core.loop.synserv` (heartbeat loop body), `&core.registry.beacon` (beacon identities + cert/auth — absorbs the legacy Guardian root), `&core.registry.protocol` (global Configurator Unit refs), `&core.governance.requests` (Core Council request registry and later synodoxics handling surface), `&core.relay.govops` (Core govops relay loop + operational receipts), `&core.settlement` (DSC state), `&core.treasury` (Sky token-share facts), the grounded-atom surface (no registry Space — it's runtime). `&core.test-suite` is core substrate but counted under test-runner.

**Challenges + watch out.** Getting `syngate` right — *the* trust boundary, the one inspectable point where authority lives. Pinning down the baseline grounded-atom surface (which primitives, what signatures, what conformance tests). Grounded atoms are part of the runtime's evaluation surface, not Space content — no grounded registry to build. Risk-form equations are **not** here — they belong to Prime–Halo.

### Prime–Halo — the deliverable

**What it is.** Owns the Phase 1 deliverable: **real-time ER per Prime.** Everything else plugs in.

**Spaces it covers.** `&core.loop.synserv` rollup body; the 7 prime entarts (`root` / `primebook` / `structbook` / `relay` / `protocol-registry`); the 3 halo entarts (`root` / `nfat-term` halo class / `custodial-crypto` risk class / `custodial-crypto.attest-data` attestor loop / `relay` / `synops` / `protocol-registry`); constructor-made `halobook` / `riskbook` / `exobook`; market-memory atoms from `&entity.oracle.crypto-majors.ticks`; attestor gates; **patch beacon + insyn/exsyn TRRC split** (`TRRC = insynTRRC + exsynTRRC`, exsyn from `patch-{prime}` into each primebook); relay/synops verbs; the NFAT instrument; rollup path `exobook → riskbook → halobook → NFAT → primebook → ER`.

**Challenges + watch out.** ER as `TRRC / TRC` emitted per heartbeat. **Dynamic auto-wiring** — a new `exobook` constructor must be immediately live in the rollup (registry, parent pointers, sweep, attestor accord, oracle subscription) with zero follow-up sudo. Patch beacon must cohere with the insyn/exsyn split. Attestation is boolean admission, not data — quantitative is all insyn; per-halo risk-class copies stand in for canonical `&core.framework.risk.forms` (which doesn't exist in P1) until propagation ships. See [`attestor-atom-schema.md`](attestor-atom-schema.md).

### Demand Side — a major input

**What it is.** Structural Demand Resource (SDR): how much USDS liability is sticky enough to support matched assets at each TTM / SPTP tier. Feeds `structbook` matching, one input into the ER calculation.

**Spaces it covers.** `&entity.generator.usge.structural-demand` (lot-age surface, Lindy SDR algorithm/model outputs, SDR policy overlay, effective SDR bucket capacity atoms); `&entity.generator.usge.sdr-auction` (synserv-triggered ownership-weighted temporary SDR auction / splitter; structbooks read here); `&entity.generator.usge.protocol-registry` (USDS/DAI/sUSDS/sDAI ERC20 refs).

**Challenges + watch out.** P1 computes effective SDR bucket capacity rather than manually setting ordinary bucket capacity. The lot-age surface is scraped/reduced into usable atoms; Lindy SDR discounts fragile structure (same-age crowding, same-account concentration, churn, low-quality sources); the governance-set SDR policy overlay pulls the dynamic result down through caps, haircuts, eligible-source filters, and fallback bounds. The P1 `sdr-auction` body is a temporary equation, triggered by synserv during the daily DSC processing window; it reads effective SDR bucket capacity, Sky token share from `&core.treasury`, and IJRC from Prime roots, then splits every bucket pro-rata for the next epoch. Structbooks read only `(sdr-allocation …)` atoms; later real SDR auctions replace the writer/body without changing that read path. No sticky claims, durable SDR ownership, or carry-forward accounting.

---

## Operator fronts

Participant-defined, described in human/role terms near-term. Each converges to a local telart over time.

### synserv (+ Guardian / Ozone)

**What it does.** The central synomic node operated by Core Council govops, not a normal operator beacon. Runs the canonical heartbeat (`&core.loop.synserv`), sequences accepted synart writes, evaluates the rollup, advances DSC state, and emits `(prime-er …)` per tick. Singleton. **Guardian (Ozone)** is the rooting authority — in P1 it holds all sudo authority and the cert chain; genesis is a sequence of Guardian sudo writes.

**Operational shape.** Each tick: re-derive all book state from current input atoms, emit ER. At 13:00 UTC enter DSC processing (treasury refresh, lot-age surface refresh, Lindy SDR, policy overlay, SDR auction allocation); at 16:00 UTC advance the epoch. Constructor-made books picked up by the sweep. Failover: canonical breaks → Core Council out-of-band signs `(canonical-synserv-runner X)`, subscribers reconnect (failover is an atom write).

**Challenges + watch out.** Sole-sequencer is bottleneck/SPOF — P1 uses single-leader + hot standby. Genesis sudo is the one unconstrained write surface; integrity rests on off-space audit + operator diversity.

### relay / synops operators

**What it does.** Human-in-the-loop operational layer — P1 relay/synops beacons are deterministic teleonome-less programs, while govops is the human/institutional operator deciding what external actions to take. A `relay` is a synops-capable beacon with external/onchain actuation authority: it acts outside the synome and writes the corresponding synome record. A `synops-beacon` is in-synome operational mutation only. **Core-side** (`relay-core-govops`): Core govops request status, Configurator / aBEAM action records, and processing of requests from `&core.governance.requests`. **Prime-side** (`relay-prime-{id}`): deploy / rollover / withdraw NFAT exposure and record allocation / tx-confirmation atoms. **Halo-side relay** (`relay-halo-{id}`): constructors (`create-halobook` / `-riskbook` / `-exobook`), queue claims, conversions, `record-unit`, lifecycle transitions, funding confirmations, NFAT issuance records. **Halo-side synops** (`synops-halo-{id}`): proposed borrower setup, borrower-inclusion and class-modification requests to Core Council, and in-synome book-accounting assignments after relay receipts exist.

**Challenges + watch out.** Where the dynamic auto-wiring challenge bites — relay actions must produce immediately-live books with no follow-up sudo. Relay writes must stay causally tied to planned, executing, or confirmed external action, or to lifecycle transitions required to safely execute / record that action. Synops actions must stay in-synome: they can request Core Council action and assign book accounting against relay receipts, but cannot move PAU funds or grant Configurator inclusion. Halo class-modification requests are operational request/status atoms; applying the class change is still a phase boundary in P1. Govops also certs the patch beacon.

### Attestor operator

**What it does.** Operates the certed `attest-data` beacons writing boolean borrower-readiness, borrower-admission, riskbook, and exobook attestation atoms. P1 has no separate attestor entart Space; cert/auth content lives in `&core.registry.beacon`. For custodial-crypto it is *not* an oracle of loan facts (those are insyn) — it underwrites legal structure, borrower credit standing, account binding, custodian compliance, Configurator-inclusion readiness, and exobook term enforceability. Full schema: [`attestor-atom-schema.md`](attestor-atom-schema.md).

**Operational shape.** Underwrite proposed borrower setup → sign readiness boolean → Core Council inclusion path completes → sign final borrower admission. For loans, underwrite riskbook / exobook term surfaces. `refresh-due` approaches → re-underwrite (credit-review cadence, not market cadence). Material structural change (`scope-ref` mismatch) → re-attest. Stale → exobook drops from rollup (default-deny).

**Challenges + watch out.** Surviving open sub-question: `scope-ref` granularity (which exobook atoms count as "structural"). Don't rebuild the numeric-attestation model — it's boolean.

### Market Oracle (Crypto Majors Oracle)

**What it does.** Rank-2 Oracle Entity pushing current market-state and rolling market-memory atoms for the v1 universe (BTC, ETH, stETH, USDC, USDS, USDT, USD rates, macro factors) via `market-data` beacons into its entart root. Full catalog: [`market-memory-oracle.md`](market-memory-oracle.md).

**Operational shape.** Each tick: push current market data and reducer outputs. Archive nodes replay raw source tapes when a reducer version changes, catch up to real time, then the same reducer continues live. Feed divergence → provider redundancy / dispute.

**Challenges + watch out.** Provider redundancy, reducer provenance, archive-node replay, and dispute model are the trust surface. Scenario definitions should reference reducer outputs wherever possible; the remaining semantic bridge ("war = this bundle of reducer references") must be explicit.

### patch beacon

**What it does.** Per-Prime `patch-{prime}` exsyn-TRRC scaffold — govops-certed, Guardian-sudoed inline into each `&entity.prime.{id}.primebook` at genesis, writes `(exsyn-trrc-claim …)` atoms. The **insyn/exsyn bridge**: `TRRC = insynTRRC + exsynTRRC`. The one beacon class with **no regulated framework** — designed to **sunset** as legacy halos migrate to insyn.

**Challenges + watch out.** Deliberate scaffold, not architecture — keep it thin, keep the sunset path clear. No regulated framework is correct here, not a gap. Textbook insyn/exsyn phased-buildout device (see [`roadmap-ideas.md`](roadmap-ideas.md)).

### test-runner

**What it does.** Testing practice. Runs the synart-native acceptance suite against a **shadow frame**, not canonical: genesis → fork shadow → run suite → discard shadow → production. Each front contributes its own test atoms; the "risk form" normative spec lives here (conformance tests *are* the definition of the form in P1).

**Challenges + watch out.** Tests carry the normative "risk form" spec until a canonical Space does — load-bearing spec, not just verification. The test *machinery* is Core substrate; this front is the *practice*.

---

## File map

Full focused-mode file map: [`../roadstart/README.md`](../roadstart/README.md). Most-related to this orientation: [`phase-1-spaces.md`](phase-1-spaces.md) (canonical spec below this layer), [`p1-nfat-atom-trace.md`](p1-nfat-atom-trace.md) (atom-level NFAT trace), [`p1-borrower-nfat-user-scenario.md`](p1-borrower-nfat-user-scenario.md) (borrower-to-ER narrative scenario), [`roadmap-ideas.md`](roadmap-ideas.md) (lift / insyn-exsyn / phase-invariant patterns), [`v1-principles.md`](v1-principles.md) (16 invariants).
