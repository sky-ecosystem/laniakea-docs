# Phase 1 Design — Follow-ups After Naming Sweep + Topology Redesign

**Status:** Working doc. Captures the remaining pickup items after the 2026-05-17 live-state cleanup (66 fixed Spaces, daily DSC, `&core.treasury`, market-memory oracle, 30-day SDR buckets, ownership-weighted pro-rata SDR allocator, custodial-crypto stress-envelope risk form). §1.1-§1.3 are resolved at design level; the exact scenario catalog, exact reducer catalog, and atom-level heartbeat trace remain.

**Reusable as context after conversation clears.** Read [`phase-1-spaces.md`](phase-1-spaces.md) first for the P1 spec; this doc is the pickup list for what to do next.

---

## §0 What's locked (don't re-litigate)

### Capital math vocabulary

- **default-CRR / spread-CRR / rate-CRR / liquidity-CRR** — per-risk-type capital fractions, per position. default-CRR is the irreducible floor (always required); others gated by sub-book coverage.
- **concentration-CRR** — portfolio-level, not per-position; over-cap excess × 100%.
- **Position CRR** — composed per sub-book using `max()` for alternative loss paths (default vs forced-loss) and `+` for additive (rate).
- **RRC** = Position CRR × Exposure (per-position $).
- **TRRC** = Σ RRC + Concentration Excess (per-Prime $).
- **TRC** = held risk capital.
- **ER** = TRRC / TRC.
- **No Basel-style 8% adequacy multiplier.** Per-risk-type CRRs are stress-calibrated directly.

### Naming convention (canonical: [`../noemar-synlang/topology.md`](../noemar-synlang/topology.md) §9)

- `.` for hierarchy, `-` for compounds within a segment
- Beacons: dash-only, no sigil
- Stem ≠ class (class is registry metadata)
- Risk-framework subspaces (when they exist post-P1) nest under `&core.framework.risk.*`
- Versions live in atoms, not Space names
- Sub-ids as new levels (`book.A1`); compound ids preserved (`spark-term`)

### Beacon class taxonomy (canonical: [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md))

6 classes + synserv:
- `market-data-beacon`, `attest-data-beacon`, `patch-beacon` (input)
- `relay`, `sentinel` (action; sentinel has variants stream + principal-sentinel)
- `synserv` (special)

**Endoscraper** is a grounded runtime primitive `(chain-read $contract $slot)`, not a beacon class. Per-protocol metadata lives in per-entart `protocol-registry` sub-Spaces in P1 — each Prime, Halo, and the Generator carries its own contract refs locally (per [`phase-1-spaces.md`](phase-1-spaces.md); supersedes the older single `&core.protocol` placement).

### Rename: risk category → risk form / risk class

The `category → form` rename applies at all three risk levels (exo-asset, exobook, riskbook). At the riskbook layer this nests inside the new `risk class` concept introduced in the 2026-05-15 topology redesign:

- `risk-category-def` → `risk-form-def`
- `&core.framework.risk.categories` → `&core.framework.risk.forms` (post-P1; no such Space in P1)
- "risk category equation" → "risk-form equation" or just "risk form"
- "category match" → "form match" / "risk-class match"
- A riskbook is bound to a **risk class** (a bundle of risk form + class-accordant attestor); the risk class lives per-halo at `&entity.halo.{id}.{risk-class-name}` with the attestor as a sub-Space at `…{risk-class-name}.attest-data`.

**Unchanged** (different sibling concepts): `book-category-def` (halobook), `concentration-category-def` (correlation).

### Phase 1 reality

- All 7 Primes active; 3 P1 Halos (spark-term, grove-term, maple-term).
- No sentinels in P1 — only relays controlled manually by govops.
- **Risk framework via per-halo risk class** (`custodial-crypto` carrying the risk form + attestor sub-Space); P1 body shape is the stress-envelope exobook waterfall in [`../risk-framework/custodial-crypto-risk-form.md`](../risk-framework/custodial-crypto-risk-form.md); **no canonical `&core.framework.risk.*` Space in P1** — canonical sources ship additively at later phase boundaries via the phase-invariant consumption-site pattern.
- **Single halo class** (`nfat-term`) per halo; all 3 halos share the class declaration `(permitted-risk-classes nfat-term [custodial-crypto])`.
- Insyn/exsyn TRRC split; patch-beacon per Prime (×7) for legacy exsyn, sudoed inline into each primebook.
- Synserv emits real-time `(prime-er {prime} {value} T)` per heartbeat and drives the daily DSC epoch state from wall clock.
- **66 fixed Spaces** sudoed at genesis.

---

## §1 Critical unresolved items

The unresolved work groups into four threads. The most load-bearing is §1.1.

### 1.1 Attestor atom schema (Q24) — RESOLVED for custodial-crypto (2026-05-14)

Resolved for the Phase 1 `custodial-crypto` risk class and updated on 2026-05-17 with borrower-admission / staged-exobook lifecycle. Full design in [`attestor-atom-schema.md`](attestor-atom-schema.md).

**The reframe.** For custodial-crypto, every quantitative CRR input is insyn or market-memory derived — collateral amount, debt outstanding, LT, liquidation bonus, funding confirmation, and derived LTV come from `chain-read` on the borrower's visible on-chain accounts and the loan contract; price, order-book depth, volatility history, liquidation overhang, funding/OI, and rates/macro factors come from market-memory reducer outputs. The attestor is therefore *not* an oracle of loan facts. It is a legal / operational / credit underwriter of what the chain cannot show. It gates borrower admission at the risk-class level (disbursement account, collateral account, configurator whitelist, first-contact setup) and verifies deal-specific exobook facts such as term / maturity enforceability.

The original `phase-1-spaces.md` sketch carried `assets-attested` / `debt-outstanding` / 24h `refresh-due` — all wrong-headed under this reframe. Those fields are now insyn or market-memory derived; the schema drops them. The cadence is admission / term / credit-review-paced. See [`attestor-atom-schema.md`](attestor-atom-schema.md) for borrower admission, the staged pre-send lifecycle, the default-deny gate, and the slashing surface.

In the 2026-05-15 topology redesign the attestor loop body itself moved structurally — it now lives as a sub-Space of the per-halo risk class (`&entity.halo.{id}.custodial-crypto.attest-data`), not as a sibling at the halo-entart level. Class-accordance is therefore *structural*: the attestor operates only on riskbooks bound to its risk class, because its loop Space sits inside the risk class's subtree.

**Open sub-question that survives:** exact `scope-ref` predicate list — the *principle* is settled (`scope-ref` covers borrower admission, structural configuration, account binding, and term facts, not market state), but the exact atom predicates that force re-attestation should be enumerated while building the v1 attestor.

**Out of scope here:** opaque-RWA risk classes (legacy HVB-style) have no on-chain visibility and need a richer numeric attestation schema. Not a Phase 1 risk class; deferred.

**Cross-refs:** [`attestor-atom-schema.md`](attestor-atom-schema.md). (The historical `../risk-framework/open-questions.md` reference is no longer reachable — the file was removed in the corpus reorg. Q24 is resolved here for custodial-crypto; Q26 — privacy buckets — largely dissolves for custodial-crypto since the boolean attestation carries no loan-level numbers to bucket.)

### 1.2 Risk-form signature — RESOLVED direction (2026-05-17)

The `custodial-crypto` risk form (the equation inside the per-halo risk class) has a production-lift signature and P1 body direction. Full design in [`../risk-framework/custodial-crypto-risk-form.md`](../risk-framework/custodial-crypto-risk-form.md).

**Inputs the signature must accept:**
- The Riskbook itself (for composition-constraint matching).
- Per-position loan state via grounded `(chain-read …)` — collateral asset + amount, debt outstanding, LT, liquidation bonus, derived LTV, funding confirmation, and maturity/TTM. The contract refs the call resolves against come from the halo's `protocol-registry`.
- The boolean attestation gate (from §1.1) — **admission only**, not a data source: `underwriting != pass` or stale → position excluded (default-deny); the equation may branch on `borrower-credit-standing`.
- Per-asset market memory from `market-data-beacon` outputs in `&entity.oracle.crypto-majors.ticks` — price, basis, vol, correlation, impact curves, liquidation overhang, funding/OI, rates/macro factors, data-quality metadata.

In P1 these inputs feed a stress-envelope waterfall. The framework-layer data Spaces that an eventually-matured body would consume — canonical per-asset profiles, canonical stress scenarios, currency stress — **don't exist in P1** (no `&core.framework.*` Space at all per the topology redesign). Per-halo risk class copies and conformance tests carry the binding spec until canonical propagation ships.

**Outputs the signature must produce:**
- Per-position default-CRR, spread-CRR, rate-CRR, liquidity-CRR.
- Position-level composition per the matched/unmatched blend.

**Critical:** rate-CRR is computed in P1. SDR matching makes spread/rate/liquidity non-binding only for the matched portion. Exobook asset-side impairment under the worst approved scenario is default-CRR and is never covered by matching.

### 1.3 CORE model integration — RESOLVED direction (2026-05-17)

BA Labs maintains a live CORE model at `core.data.blockanalitica.com/crr/` that produces CRR via t-Copula stress simulation across thousands of paths. It prices useful drivers: LTV-vs-LT distance, collateral volatility, order-book liquidity, borrower concentration, and collateral correlation.

This is calibration/reference material for P1, not the binding risk-form engine.

**Post-§1.1 reframe:** CORE's inputs (LTV, LT, liquidation bonus, collateral asset, borrow value, order-book depth, price history, HHI) are now entirely insyn or market-memory derived — `chain-read` + reducer outputs, zero attestor dependency. The integration question collapses to purely *where CORE's math runs*, not how it gets its inputs.

**Decision:** do not call CORE for the binding P1 CRR scalar. P1 uses named approved stress scenarios, applies them to the exobook asset side, runs the liability waterfall, and takes the maximum senior exo-unit loss. CORE can sanity-check and calibrate shocks / liquidation haircuts, but it does not bypass the synomic scenario library or per-risk-type decomposition.

**Cross-refs:** the CORE Model doc lives at `risk-repo/CORE_model/`; P1 binding spec lives in [`../risk-framework/custodial-crypto-risk-form.md`](../risk-framework/custodial-crypto-risk-form.md).

### 1.4 End-to-end atom-level NFAT walkthrough

The worked example in [`phase-1-spaces.md`](phase-1-spaces.md) "Worked Example: A Single NFAT Loan" shows the arithmetic (BTC drops 45% → $59.8K loss fraction 7.97%) but not the atom-level synlang machinery. A trace at each step would expose any gaps in the schemas from §1.1–§1.3.

**What to extend:**
- Show each atom that gets read/written at each heartbeat step.
- Show how attestation + market-memory data composes into per-risk-type CRRs via the risk form.
- Show the sub-book routing decision concretely (match check against composition-constraints).
- Show the matched/unmatched blend computation with actual atom reads (including the auction allocations read from `&entity.generator.usge.auction`).
- Show the upward rollup: exobook derivations → riskbook CRR atoms → halobook aggregation → Prime structbook RRC → primebook insynTRRC + exsyn-trrc-claim → final ER emission.

**Forcing trigger:** now. §1.1-§1.3 are settled enough for the atom trace; exact scenario constants and reducer catalog can stay symbolic.

---

## §2 Recommended sequence

```
1. Attestor schema (§1.1)                       ← RESOLVED 2026-05-14 (custodial-crypto)
       │
       ├── 2a. Risk-form signature (§1.2)       ← RESOLVED 2026-05-17
       │
       └── 2b. CORE integration (§1.3)           ← RESOLVED 2026-05-17
                    │
                    ▼
           3. End-to-end atom trace (§1.4)       ← next
```

Schema first because it defines which facts are legal/operational gates rather than numeric model inputs. With that split settled, the risk-form signature and CORE role are concrete enough; the end-to-end trace ties it all together.

---

## §3 Smaller cleanup items (deferred-OK)

These don't block P1 design work but should be tracked:

### 3.1 Agent-flagged Space-name judgment calls

From the 2026-05-13 naming sweep, three Space names were chosen by agents without explicit spec coverage. None of these Spaces exist in P1 (the framework layer is empty in P1), but they're candidate names for when those Spaces eventually appear at a later phase boundary:

- **`&core.framework.risk.crash-oracle`** (in `risk-framework/primebook-composition.md`, `risk-monitoring.md`) — nested under risk; could plausibly be flat at `&core.framework.crash-oracle` if it's not strictly a risk concept.
- **`&core.framework.prime-token-metrics`** (in `accounting/capital-stack.md`) — left flat at framework level. Could alternatively live under `&core.registry.prime-token-metrics` if it's better thought of as registry data.
- **`&core.registry.cross-prime-flows`** (in `accounting/isolated-deployment.md`) — compound id preserved. Not in the canonical reserved-vocabulary table; pattern is consistent but worth confirming.

### 3.2 Other clean-todo passes still open

Pass A (naming) resolved 2026-05-13. The `category → form` corpus-wide rename is in progress. Remaining passes in [`../summaries/clean-todo.md`](../summaries/clean-todo.md):

- Pass B: stub-spec graduation (Oracle Entity, Sequencer Entity, Pylon Entity, Diamond PAU, Folio PAU)
- Pass E: detail-file token-bloat audit (highest-leverage corpus-quality pass)
- Pass F: numeric-fact source-of-truth designation
- Pass G: canonical-home claim integrity audit
- §12: beacon-class conceptual treatment (sentinel / relay / market-data / attest-data — synodoxics work)

### 3.3 Phase boundary deferrals

Items explicitly out of P1 scope:

- Exact crypto stress scenario catalog (Q27) — pending governance discussion; mechanism is settled as max approved scenario loss
- Exact market-memory reducer catalog — mechanism settled, output families in [`../risk-framework/market-memory-oracle.md`](../risk-framework/market-memory-oracle.md)
- Growth Staking activation — Phase 2+ (P/E parameters, GF values sudo-set at activation)
- Sentinel formations + Streaming Accord — Phase 9–10
- Sub-books beyond `structbook` (ascbook, tradingbook, termbook, hedgebook) — Phase 2+
- Crash oracle implementation — Phase 2+
- Concentration excess penalty enforcement — Phase 3+
- Genbook cross-Prime concentration enforcement — Phase 2+
- Canonical loop-template propagation (per-entity loop Spaces hold their bodies in P1; templates ship additively in a later phase per the phase-invariant consumption-site pattern)
- Canonical risk-form source + propagation into per-halo risk class Spaces — later phase

**Note:** Real-time Lindy / USDS lot-age tracking is deferred again. P1 uses governance-set bucket capacities in `&entity.generator.usge.structural-demand`. What is live is the **daily synserv-triggered pro-rata SDR allocator** in `&entity.generator.usge.auction`, using the temporary ownership-weight formula. The auction Space is the phase-invariant consumption site — real auctions later write the same atom shape into the same Space; only the body/writer changes. P1 has no reservation market, sticky claims, durable SDR ownership, or carry-forward accounting.

---

## §4 Reading order for a fresh session

To pick this up cold:

1. Read this doc top to bottom (~5 min).
2. Read [`phase-1-overview.md`](phase-1-overview.md) for the fronts framing (~5 min).
3. Read [`phase-1-spaces.md`](phase-1-spaces.md) — at minimum the "Worked Example: A Single NFAT Loan", "Attestation model", and "Halo class and risk class" sections (~10 min).
4. Read [`attestor-atom-schema.md`](attestor-atom-schema.md) — the resolved §1.1 design (~5 min).
5. Read [`../risk-framework/riskbook-layer.md`](../risk-framework/riskbook-layer.md) §8 examples (the v1 risk-form sketch) (~5 min).
6. Read [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) §4 (the 6-class taxonomy + endoscraper-as-primitive) (~5 min).
7. (Optional) Read the BA Labs CORE doc at `risk-repo/CORE_model/CORE Model – General Guidelines for CRR.md`.

After step 6, the §1 items above should be concretely workable.

---

## File map

| Doc | Role |
|---|---|
| This file | Working pickup list after the 2026-05-13 naming sweep + 2026-05-15 topology redesign |
| [`attestor-atom-schema.md`](attestor-atom-schema.md) | Resolves §1.1 for custodial-crypto — the boolean attestation schema |
| [`phase-1-spaces.md`](phase-1-spaces.md) | Canonical P1 spec (v4 live-state cleanup); the worked NFAT example anchors the remaining atom trace work |
| [`phase-1-overview.md`](phase-1-overview.md) | Orientation entry point — Phase 1 organized by *fronts* (structural + operator) |
| [`v1-principles.md`](v1-principles.md) | The 13 P1 invariants — anything proposed should compose with these |
| [`roadmap-ideas.md`](roadmap-ideas.md) | Lift principle, insyn/exsyn pattern, sudo staircase, frame mechanism, phase-invariant consumption sites |
| [`../summaries/clean-todo.md`](../summaries/clean-todo.md) | Pass-tracker for corpus-wide cleanup work; §12 beacon-class conceptual treatment |
