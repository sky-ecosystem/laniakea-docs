# Laniakea-Docs Clean-Up Plan

**Date:** 2026-05-04
**Scope:** Synomics + risk-framework. First step toward a synlang-native repo.

---

## Strategic Direction

Three coordinated moves:

1. **Reorg the repo** — flatten `synomics/` to top level; everything not yet synlang-native moves into a new `inactive/pre-synlang/` workbench; significantly-changed-or-replaced files get archived in a new `inactive/archive/` for context. **(Phase 1 — DONE)**
2. **Tighten `noemar-synlang/` scope** — keep the directory, but reframe it as the **technical reference for the Noemar runtime + synlang** that everything else assumes familiarity with. Risk content + conceptual layering moves out; tech specifics stay/come in.
3. **Reconcile contradictions** — beacon framework collapse, Ozone single-guardian topology, risk framework redesign, synodoxics/neurosymbolic boundary fix.

End state: `risk-framework/` + the synomics subdiscipline directories at top level + `noemar-synlang/` (tech reference) + `inactive/pre-synlang/` (legacy) + `inactive/archive/` (context). No `synomics/` parent.

---

## Execution Status

Working tool. Tick boxes as tasks complete; add log entries when meaningful work happens. Detailed phase descriptions are preserved below for reference.

### Revised sequence (2026-05-05)

Re-ordered from the original "Recommended Execution Order" because:

- `laniakea-docs/README.md` is broken — still lists `synomics/`, `whitepaper/`, `accounting/`, etc. as top-level dirs, none of which exist post-reorg.
- `lift.md` pointers are dangling in 5 active docs (`synodoxics/noemar-substrate.md`, `neurosymbolic/cognition-as-manipulation.md`, `neurosymbolic/attention-allocation.md`, `neurosymbolic/neuro-symbolic-cognition.md`, `core-concepts/rsi.md`).
- Phase 5.2 (Ozone) is partially done in noemar-synlang/ — remaining laniakea-docs side is small.
- Phase 5.1 (beacons) is bigger than originally scoped — vocabulary referenced widely.

| # | Item | Status |
|---|---|---|
| 1 | Phase 1 — Reorg (synomics/ flattened, inactive/ created) | ✅ Done |
| 2 | README fix + Phase 1 follow-up | ✅ Done |
| 3 | Phase 5.3 — Synodoxics ↔ Neurosymbolic boundary | ✅ Done |
| 4 | Phase 5.2 finalization (laniakea-docs side) | ✅ Done |
| 5 | Phase 4 — Lift consolidation | ✅ Done |
| 6 | Phase 5.1 — Beacon framework collapse | ✅ Done |
| 7 | Phase 3 — noemar-synlang rescope | ✅ Done |
| 8 | Phase 2 — Risk framework rewrite (multi-session; see `inactive/archive/rewrite-plan-final.md`) | ✅ Done (Phases 0-6 all complete) |
| 9 | Phase 6 — Reframing pointers | ✅ Done |

### Detailed checklist

#### Item 2 — README fix + Phase 1 follow-up
- [x] Update `laniakea-docs/README.md` Contents table to match actual top-level dirs
- [x] Update Key Documents table (links to moved docs)
- [x] Move subdiscipline framing from `inactive/archive/synomics-README.md` into `core-concepts/README.md`
- [x] Add brief synomics-as-"data-and-AI-governance" mention to root `README.md`
- [x] Verify root README internal links resolve

#### Item 3 — Phase 5.3 — Synodoxics ↔ Neurosymbolic boundary
- [x] Move `synodoxics/neuro-symbolic-cognition.md` → `neurosymbolic/neuro-symbolic-cognition.md`
- [x] Update `synodoxics/README.md` (remove moved doc; tighten framing)
- [x] Update `neurosymbolic/README.md` (add new doc as foundational architectural commitment)
- [x] Sweep inline pointers in both directories (10 files updated total)

#### Item 4 — Phase 5.2 finalization (laniakea-docs side)
- [x] `macrosynomics/atlas-synome-separation.md` (rank table + Guardian description)
- [x] `macrosynomics/synomic-agents.md` (rank table + Ozone clarification note)
- [x] `core-concepts/four-layer-enforcement-stack.md` — N/A (no Guardian refs; the four-layer stack is Synome→Council→Superstructure→Teleonomes, conceptually upstream of the Guardian rank hierarchy)
- [x] Sweep for any other "multiple guardians" refs — caught `risk-framework/operational-risk-capital.md` (line 112 "multiple guardians" → "multiple Accordants") and `macrosynomics/synome-layers.md` (rank table)

#### Item 5 — Phase 4 — Lift consolidation
- [x] Read `inactive/archive/lift.md` (44KB) and `inactive/archive/lift-weakness.md` (24KB) in full
- [x] Synthesize into `synodoxics/lift.md` (~10–15KB) — landed at ~18KB / 200 lines, slight overshoot but covers all required content (definition, lifted/grounded, false lift, opaque grounded primitives, net lift after costs, meta-lift / self-hosting, weakness's three channels + composition law + budget-capped, the synthesis line). Cut: aerodynamic metaphor, deep vocabulary list, repeated phrasings, philosophical asides
- [x] `synodoxics/README.md` updated — added "Vocabulary" section listing `lift.md` and updated dependency graph
- [x] Fix inline pointers:
  - [x] `synodoxics/noemar-substrate.md` — `[../lift.md](../lift.md)` → `[lift.md](lift.md)` (same dir)
  - [x] `neurosymbolic/cognition-as-manipulation.md` — N/A (no existing lift reference; the doc covers context-manipulation mechanics, not the opaque-grounded-primitive framing — that lives in `neuro-symbolic-cognition.md`. No natural insertion point)
  - [x] `neurosymbolic/attention-allocation.md` — `[lift](../lift.md)` → `[lift](../synodoxics/lift.md)`
  - [x] `neurosymbolic/neuro-symbolic-cognition.md` — `[lift](../lift.md)` → `[lift](../synodoxics/lift.md)`
  - [x] `core-concepts/rsi.md` — `[../lift.md](../lift.md)` → `[../synodoxics/lift.md](../synodoxics/lift.md)`
  - [x] `synoteleonomics/teleonome-economics.md` — added one-line lift pointer to RSI section ("In lift vocabulary: meta-lift in operation...")

#### Item 6 — Phase 5.1 — Beacon framework collapse

##### Scoping (2026-05-05)

**Goal.** Replace the LPLA/LPHA/HPLA/HPHA 2×2 (power × authority) with a two-tier **authority-only** framing. Power-as-axis retires because cognition has moved into synart-resolved in-space computation; embodiment cognitive capability is no longer load-bearing for beacon classification. Beacons become pure I/O: they witness, sign, and submit; calculation lives in synart.

**Resolved framing (per `clean-up-plan.md` §Phase 5 above):**

- **High authority** — certified by a synomic agent; auth-scoped to specific verbs/targets; operates a Synomic Agent (Prime/Halo/Generator/Guardian). Includes deterministic relayers, executors, and sentinel formations (Baseline/Stream/Warden + Principal).
- **Low authority** — no Synomic Agent operation. Either passive observation (reporting, scraping, attesting) OR direct teleonome-to-teleonome interaction (peer-to-peer trading, arbitrage, cooperation).
- **Two-role taxonomy under authority** (from `noemar-synlang/beacons.md`, sketch-grade) — input beacons (endoscraper / oracle / attestor) push data into book spaces; action beacons (relayer / executor / sentinel formation) emit chain txs based on synart state. **Deliberately non-prescriptive.** Concrete classes are first-cut. The two-tier authority is what's load-bearing; input/action is a working cut.
- **`lpla-checker` disappears.** Calculation moves into in-space computation per `noemar-synlang/listener-loops.md`. The verification *role* survives — but as synserv-run code reading the same scraped state, not as a separate beacon class.
- **Sentinel formations survive intact.** stl-base / stl-stream / stl-warden / stl-principal are high-authority action beacons (not "HPHA"). The Baseline/Stream/Warden naming and the formation pattern are unchanged.
- **BEAM hierarchy stays.** pBEAM/cBEAM/aBEAM are chain-side authorization roles, orthogonal to the beacon taxonomy. They appear in the high-authority section as the on-chain mechanism that makes a relay/council beacon "high authority" in the smart-contract sense.
- **Embodiment power levels stay.** `synome-layers.md`'s light/medium/heavy distinction is about hardware-aware cognition (per `neurosymbolic/hardware-aware-cognition.md`), not beacon power. Reframe the beacon-profile column in that table as authority-tier examples instead of LPLA/HPLA labels.

##### Open questions for user before execution

1. **LPLA/LPHA/HPLA/HPHA — fully retire, or keep as historical glossary entry?**
   - Option A: Demote to a brief "Historical naming" appendix in `macrosynomics/beacon-framework.md` glossary, mapping each to authority-tier + role. Sweep all narrative usage. Recommended.
   - Option B: Keep the four-letter codes as live shortcuts (e.g., "LPHA" = "low-authority data input") and add the two-tier framing on top. Cheaper, but doesn't actually collapse the framework.
   - Default: A. Cleanly collapsed framework + glossary anchor.

2. **`noemar-synlang/beacons.md` and `listener-loops.md` — absorb fully into `macrosynomics/beacon-framework.md`, or leave them as Phase-1-implementation sketches and just point?**
   - Plan §3.2 has both moving out of `noemar-synlang/` (per Phase 3). Phase 5.1 should absorb the *content* into `macrosynomics/beacon-framework.md` so the conceptual story is complete. The Phase 3 deletions of those source files come later.
   - Default: Absorb the conceptual core (two-role taxonomy, in-space calculation, old→new mapping). Leave the per-protocol implementation sketches as deferred-to-Phase-1 notes.

3. **Specific named classes (`lpha-nfat`, `lpha-lcts`, `lpha-rate`, `stl-base-{prime}`, etc.) — keep names, retag, or rename?**
   - These names are operational identifiers used in `risk-framework/sentinel-integration.md`, `synomic-agents.md`, etc. The `lp/hp` prefix encodes the retired power axis.
   - Option A: Keep the names as-is (legacy identifiers, mapped in glossary). Sentinel-integration table just gets a header rephrased.
   - Option B: Rename systematically (`lpha-nfat` → `nfat-keeper` or similar). High churn across multiple docs.
   - Default: A. Names are sticky; rebadging the framework doesn't require renaming every operational beacon.

4. **`core-concepts/beacon-framework.md` — full rewrite around authority tier, or retire and merge into a different concept doc?**
   - The atomic concept currently defines the 2×2 matrix as the central abstraction. With the matrix gone, the concept page should redefine "beacon" around authority + I/O role.
   - Default: Full rewrite. Keep as atomic concept. ~30 lines.

##### Surface area

**Heavy rewrites (2):**
- `macrosynomics/beacon-framework.md` — 34 tier-code hits + 1 lpla-checker. Full rewrite, absorb noemar-synlang content, ~400→500 lines.
- `macrosynomics/short-term-actuators.md` — 17 tier-code hits + 1 lpla-checker. Phase 1 beacon set reframed as authority tier + role.

**Atomic concept rewrite (1):**
- `core-concepts/beacon-framework.md` — 3 tier-code hits. Redefine around authority tier, drop the 2×2.

**Risk-framework targeted edits (3):**
- `risk-framework/sentinel-integration.md` — 4 tier-code hits + 2 lpla-checker. Drop "LPHA Beacons" / "Halo-Side LPHA Beacons" headers; lpla-checker row in Protocol-Level Beacons table moves to "synserv-run verification" or gets dropped.
- `risk-framework/risk-monitoring.md` — 0 tier-code, 2 lpla-checker. Replace "lpla-checker" with synserv/in-space calculation reference.
- `risk-framework/README.md` — 0 tier-code, 1 lpla-checker. Update the "resolved" item to point at the new beacon-framework.md instead of noemar-synlang sketches.

**Sweeps (1-line / few-line edits, 8 files):**
- `core-concepts/binding-mechanics.md:11` — replace 2×2 prose with two-tier prose
- `macrosynomics/README.md:24` — replace "(power x authority matrix: LPLA/LPHA/HPLA/HPHA)" with "(two-tier authority + I/O role)"
- `macrosynomics/synome-overview.md:44` — "classified by power × authority into LPLA/LPHA/HPLA/HPHA" → "classified by authority tier"
- `macrosynomics/synome-layers.md:198-199` — beacon profile column rephrased (no LPLA/LPHA labels)
- `macrosynomics/synomic-agents.md:366` — "High Authority beacons (LPHA, HPHA)" → "High Authority beacons (deterministic keepers and sentinel formations)"
- `macrosynomics/atlas-synome-separation.md:477` — `lpla-checker` row in beacon table → "synserv verifier" or drop
- `synoteleonomics/actuator-perspective.md:81` — "LPLA, LPHA, HPLA, HPHA classifications" → "two-tier authority classification"
- `synoteleonomics/teleonome-binding.md:35-36` — replace 2×2 table with two-tier framing (4 → 2 cells)
- `synoteleonomics/teleonome-economics.md:216` — "HPHA sentinel actions" → "high-authority sentinel actions"

**Absorb (content target = `macrosynomics/beacon-framework.md`; source files stay until Phase 3):**
- `noemar-synlang/beacons.md` — two-role taxonomy + old→new mapping table
- `noemar-synlang/listener-loops.md` — in-space calculation pattern; why it's load-bearing for the new framing

**Skip (Phase 3 territory — touch only if cross-references break):**
- `noemar-synlang/topology.md`, `synlang-patterns.md`, `syn-tel-emb.md`, `telseed-bootstrap-example.md`, `govops-synlang-patterns.md` — the `noemar-synlang/` rewrite happens in Item 7 / Phase 3.

##### Per-file edit plan

| File | Action | Line refs |
|---|---|---|
| `macrosynomics/beacon-framework.md` | Full rewrite. New structure: §1 Why beacons / §2 Definition + properties / §3 Authority tier (the load-bearing axis) / §4 I/O role under authority (input vs action; non-prescriptive) / §5 Concrete beacon classes (one section per class, using legacy `lp*-*` names where they exist) / §6 Sentinel formations as the high-authority action subclass / §7 BEAM hierarchy (chain-side authority, orthogonal) / §8 Lifecycle / §9 Multi-beacon reality / §10 Connections / §11 Glossary (incl. historical LPLA/LPHA/HPLA/HPHA mapping) | Rewrite whole file |
| `macrosynomics/short-term-actuators.md` | Replace power/authority axis prose (lines ~31-37). Reframe Phase 1 beacon set table as authority tier + role: lpla-verify (low-auth, input/verification), lpha-relay (high-auth, action/executor), lpha-nfat (high-auth, action/executor + record-writer), lpha-council (high-auth, governance writes). Drop "Phase 1 beacons are all Low-Power" framing. Update axes table and "Mapping to Full Synome Architecture" section | ~31-37, ~46-114, ~145-170 |
| `core-concepts/beacon-framework.md` | Replace the 2×2 with the two-tier authority table. Rewrite Key Properties bullets. Update Sentinel formations bullet ("distinguished HPHA subclass" → "distinguished high-authority action subclass"). Keep BEAM section unchanged. | Lines 11-25 |
| `risk-framework/sentinel-integration.md` | Replace "Risk Framework provides the calculations that sentinel formations and LPHA beacons perform" with "...high-authority action beacons perform". Rename "Halo-Side LPHA Beacons" header → "Halo-Side Action Beacons". Rename "LPHA Beacons" header → "Halo Reporting Beacons". Drop or rewrite "lpla-checker" row in Protocol-Level Beacons table → "synserv verification" pointing to `noemar-synlang/listener-loops.md`. Drop the LPHA explanatory note (line 42). | Lines 7, 35, 42, 44; lpla-checker rows |
| `risk-framework/risk-monitoring.md` | "Automated detection (lpla-checker, warden sentinels)" → "Automated detection (synserv verification, warden sentinels)". Other lpla-checker hit similar | 2 sites |
| `risk-framework/README.md` | Update the resolved bullet to read past-tense and point at `macrosynomics/beacon-framework.md` | Line 47 |
| `core-concepts/binding-mechanics.md` | Replace lines 11 prose: "The beacon power × authority matrix determines oversight: LPLA (...) LPHA (...) HPLA (...) HPHA (...)" → "Beacon authority determines oversight: low-authority beacons (passive reporting OR peer-to-peer teleonome interaction) face minimal oversight; high-authority beacons (operating Synomic Agents) are scoped, observable, revocable" | Line 11 |
| `macrosynomics/README.md` | Line 24: drop "(power x authority matrix: LPLA/LPHA/HPLA/HPHA)" → "(two-tier authority, I/O role under it)" | Line 24 |
| `macrosynomics/synome-overview.md` | Line 44: replace "classified by power × authority into LPLA/LPHA/HPLA/HPHA" with "classified by authority tier (low / high), with I/O role (input / action) underneath" | Line 44 |
| `macrosynomics/synome-layers.md` | Lines 198-199: beacon profile column → "passive observation; simple action keepers" / "Sentinels, peer-to-peer trading, sophisticated keepers" — drop LPLA/HPLA labels | Lines 198-199 |
| `macrosynomics/synomic-agents.md` | Line 366: "High Authority beacons (LPHA, HPHA) act on behalf of Synomic Agents" → "High-authority beacons act on behalf of Synomic Agents" | Line 366 |
| `macrosynomics/atlas-synome-separation.md` | Line 477: lpla-checker row in beacon table → "synserv verification" with brief explanation that calculation is now in-space | Line 477 |
| `synoteleonomics/actuator-perspective.md` | Line 81: replace 2×2 reference with two-tier authority reference | Line 81 |
| `synoteleonomics/teleonome-binding.md` | Lines 35-36: replace 4-cell 2×2 with 2-cell two-tier table | Lines 35-36 |
| `synoteleonomics/teleonome-economics.md` | Line 216: "HPHA sentinel actions" → "high-authority sentinel actions" | Line 216 |

##### Execution order

Recommended batching to minimize churn:

1. **Rewrite `core-concepts/beacon-framework.md`** first (atomic concept; defines the framing). Short doc, low risk.
2. **Rewrite `macrosynomics/beacon-framework.md`** absorbing `noemar-synlang/beacons.md` + `listener-loops.md`. Heavy lift; do it right after the atomic concept lands.
3. **Rewrite `macrosynomics/short-term-actuators.md`** (Phase 1 beacon set; cross-checks against the new framework).
4. **Risk-framework batch** (3 files: sentinel-integration, risk-monitoring, README) — they all reference lpla-checker the same way.
5. **Sweeps batch** (8 files, mostly 1-2 line edits each).
6. **Verification grep** — after batches: `grep -rE "LPLA|LPHA|HPLA|HPHA" --include="*.md" .` should only show hits in (a) the new beacon-framework glossary appendix, (b) the `clean-up-plan.md` log/scoping itself, and (c) `noemar-synlang/` files (handled in Phase 3 / Item 7), and (d) `inactive/`. `grep -r "lpla-checker"` should only show hits in (a) the new beacon-framework historical mapping, (b) `clean-up-plan.md`, (c) `noemar-synlang/` files, and (d) `inactive/`.

##### Acceptance criteria

- [x] No active narrative doc uses "LPLA/LPHA/HPLA/HPHA" as the primary classification (only in glossary/historical mapping in `macrosynomics/beacon-framework.md`)
- [x] No active narrative doc claims `lpla-checker` is a beacon class — references either replaced with "synserv verification" or removed
- [x] `core-concepts/beacon-framework.md` and `macrosynomics/beacon-framework.md` use the two-tier authority framing as the load-bearing axis
- [x] Sentinel formations described as "high-authority action subclass" not "HPHA subclass"
- [x] BEAM hierarchy section preserved intact (chain-side authorization, orthogonal to beacon taxonomy)
- [x] Embodiment power levels in `synome-layers.md` rephrased without LPLA/HPLA labels
- [x] No broken links into `noemar-synlang/beacons.md` or `noemar-synlang/listener-loops.md` (those source files stay until Phase 3, but the conceptual content lives in `macrosynomics/beacon-framework.md` after this phase)

##### Checklist

- [x] **Resolve open questions 1-4 above with user** — all four defaults approved
- [x] Rewrite `core-concepts/beacon-framework.md` (two-tier authority)
- [x] Rewrite `macrosynomics/beacon-framework.md` (full rewrite + absorb noemar-synlang/beacons.md + noemar-synlang/listener-loops.md content)
- [x] Rewrite `macrosynomics/short-term-actuators.md` (Phase 1 beacons reframed)
- [x] Update `risk-framework/sentinel-integration.md` (drop LPHA headers, replace lpla-checker)
- [x] Update `risk-framework/risk-monitoring.md` (replace lpla-checker references)
- [x] Update `risk-framework/README.md` (point at new beacon-framework)
- [x] Sweep `core-concepts/binding-mechanics.md` (line 11)
- [x] Sweep `macrosynomics/README.md` (line 24)
- [x] Sweep `macrosynomics/synome-overview.md` (line 44)
- [x] Sweep `macrosynomics/synome-layers.md` (lines 198-199)
- [x] Sweep `macrosynomics/synomic-agents.md` (line 366)
- [x] Sweep `macrosynomics/atlas-synome-separation.md` (line 477)
- [x] Sweep `synoteleonomics/actuator-perspective.md` (line 81)
- [x] Sweep `synoteleonomics/teleonome-binding.md` (lines 35-36)
- [x] Sweep `synoteleonomics/teleonome-economics.md` (line 216)
- [x] Verification grep — no LPLA/LPHA/HPLA/HPHA in active narrative; no `lpla-checker` outside historical/`noemar-synlang/`/`inactive/`

#### Item 7 — Phase 3 — noemar-synlang rescope
- [x] Move `synodoxics/synlang.md` → `noemar-synlang/synlang.md`
- [x] Rename `noemar-synlang/synart-access-and-runtime.md` → `noemar-synlang/runtime.md`
- [x] Move `noemar-synlang/topology-population-probmesh.md` → `macrosynomics/topology-layers.md`
- [x] Move `noemar-synlang/syn-overview.md` → `laniakea-docs/synomics-overview.md`
- [x] Split `noemar-synlang/syn-tel-emb.md`:
  - [x] Artifact-tier content → merge into `synodoxics/noemar-substrate.md`
  - [x] §8 recipe marketplace → `synoteleonomics/recipe-marketplace.md`
- [x] Archive `noemar-synlang/govops-synlang-patterns.md`
- [x] Rewrite `noemar-synlang/README.md` as tight tech-reference intro
- [x] Update `synodoxics/noemar-substrate.md` (artifact tiers + telseeds + bootstrap + atomspace runtimes + resilience + alignment implications all absorbed)
- [x] Archive working notes: `notes1.md`, `risk-framework-redesign-2026-05-03.md`, `synome-extra-info.md`, `rewrite-plan-final.md` all moved to `inactive/archive/` (2026-05-05, after Item 8 rewrite consumed their content). `noemar-synlang/README.md` updated to remove the "Phase 2 content (pending rewrite/move)" framing and replace with "Working notes (archived)" listing. `risk-framework/open-questions.md` cross-references updated to `../inactive/archive/risk-framework-redesign-2026-05-03.md`.

#### Item 8 — Phase 2 — Risk framework rewrite
**Multi-session. The plan-of-record (`rewrite-plan-final.md`) is now archived in `inactive/archive/`; original Phase 0-6 sequence executed in full.**

Phase 0 (unblocking decisions):
- [x] Keel — confirmed Spark/Grove/Keel/Obex all accordant to Ozone; entart-tree examples in `topology.md`, `synomics-overview.md`, `risk-framework-redesign-2026-05-03.md` (×2), and `synome-extra-info.md` updated to include Keel between Grove and Obex

New conceptual docs in dependency order:
- [x] `risk-framework/risk-decomposition.md` — 212 lines; 5 risk types, U/P/T, cross-default constraint, default-deny CRR 100%, coverage matrix
- [x] `risk-framework/book-primitive.md` — 214 lines; 6-tuple book, equity invariant, rules-as-state-machine, real-time recomputation, bankruptcy remoteness at Riskbook level
- [x] `risk-framework/tranching.md` — 214 lines; exoassets/exoliabs, waterfall semantics, worked Sparklend example, gap-risk unification
- [x] `risk-framework/currency-frame.md` — 187 lines; frame vs instrument, currency taxonomy, frame inheritance top-down, Riskbook as translation layer, multi-generator readiness

New layer docs:
- [x] `risk-framework/riskbook-layer.md` — 261 lines; unit of regulation, composition constraints, default lives here, currency translation, tactical hedging, bankruptcy-remoteness boundary, category catalog as governance lever, three worked examples
- [x] `risk-framework/halobook-layer.md` — 220 lines; bundle exposure structure (general framing), P+T declarations, what Halobook can/cannot affect, no-netting aggregation, single-unit issuance, v1 catalog
- [x] `risk-framework/primebook-composition.md` — 296 lines; five sub-books + unmatched as risk-coverage contracts, optimization-shaped vs static-treatment, declarative routing, treatment-switch policy with structural prerequisites, crash-oracle deferred, single Primeunit upward
- [x] `risk-framework/hedgebook.md` — 231 lines; two-level hedging, when Riskbook vs Hedgebook applies, cross-Halobook composition preserving bankruptcy-remoteness, optimization-shaped, hedge failure modes (counterparty/basis/liquidity/tenor), currency hedges
- [x] `risk-framework/projection-models.md` — 204 lines; projection contract, category-declared models, examples by position type, rules vs projections complementary, projection-model risk as own capital dimension via model-uncertainty haircut, what the framework cannot model

Update existing:
- [x] `risk-framework/README.md` — full rewrite; new module index in dependency order; reading order from foundational primitives to layer architecture to consuming docs; Open Items updated to mark gap-risk and FRTB-drawdown as resolved
- [x] `risk-framework/asset-classification.md` — extended to full risk-type tuple; asset-level liquidity profile primitive section; SPTP refinement (credit-spread vs rate duration); per-asset stress profile schema
- [x] `risk-framework/capital-formula.md` — full rewrite; per-position computation flow consuming the new layered model; per-sub-book CRR formulas; concentration excess penalty; TRRC aggregation
- [x] `risk-framework/asset-type-treatment.md` — full rewrite; each asset class via new framework (direct ETH/BTC, Sparklend, NFAT, JAAA, liquid TradFi, vanilla options, ABF, hedges); what-changed-from-prior-version table
- [x] `risk-framework/matching.md` — full rewrite preserving credit-spread vs rate distinction (load-bearing); reframed as smooth optimization between matched + unmatched portions; termbook vs structbook treatment
- [x] `risk-framework/duration-model.md` — Generator-entart placement section; Phase 1 manual-allocation carve-out; references to primebook-composition.md for sub-book consumption
- [x] `risk-framework/correlation-framework.md` — full rewrite as two-level concentration (Primebook + Genbook); hedge interaction (gross-of-hedge in v1)
- [x] `risk-framework/sentinel-integration.md` — Key Metrics table updated to reference new docs (primebook-composition, hedgebook); added Per-sub-book CRR and Equity proximity rows
- [x] `risk-framework/risk-monitoring.md` — added Sub-book and Equity Metrics section (per-sub-book CRR, equity proximity, treatment-switch frequency)
- [x] `risk-framework/examples.md` — full rewrite; v1 crypto-collateralized lending test as canonical worked example; full setup, position structure, walking through one position end-to-end, scaling up to full Prime, summary principles
- [x] `risk-framework/asc.md` — small edit; clarified parallel-track status; added ASC-eligible holdings route to `ascbook` reference
- [x] `risk-framework/operational-risk-capital.md` — small edit; clarified parallel-track status; updated portfolio-vs-operational comparison table

Archive + delete:
- [x] `risk-framework/collateralized-lending-risk.md` — moved to `inactive/archive/collateralized-lending-risk.md`; gap risk no longer a separate concept (folded into `tranching.md`)
- [x] `risk-framework/market-risk-frtb.md` — moved to `inactive/archive/market-risk-frtb.md`; FRTB drawdown no longer a separate concept (folded into `tranching.md` / `asset-type-treatment.md`)

noemar-synlang trim:
- [x] `noemar-synlang/risk-framework.md` — trimmed from 1612 lines / 62KB to 764 lines / 28KB (~53% line reduction). Repositioned as synlang-flavored complement: atom shapes for the four-book taxonomy, category atom shapes (three types), Riskbook composition constraints in synlang, stress simulation patterns, four-tier resolution as synlang code, loop and recursion handling, default-deny CRR-100% mechanism, five worked examples (kept all), cross-doc invariants. Conceptual material defers explicitly to `../risk-framework/` canonical docs.

Consistency sweep:
- [x] No remaining "gap risk" as separate concept — verified clean; remaining mentions are all explicitly historical or describe the unified treatment
- [x] No remaining "FRTB drawdown" as separate concept — same; surviving usage is "FRTB-style forced-loss treatment" applied to the unmatched portion in `tradingbook` (the math name; not a separate concept)
- [x] No remaining state-based CRR table in active corpus — `synomics-overview.md` §7 rewritten to reference new framework with deprecation note; `noemar-synlang/settlement-cycle-example.md` flagged at top with status note pointing at new framework (pending Phase 5 rewrite)
- [x] No remaining "three Star Primes" without Keel — Phase 0 Keel fix; remaining mentions correctly identify Spark/Grove/Keel as the 3 Star Primes
- [x] No remaining `lpla-checker` as beacon class — done in Item 6 (Phase 5.1) prior session
- [x] No remaining old four-book taxonomy without currency frame / equity invariant / tranching — the four-book taxonomy is preserved (it's correct in the new framework); Phase 1 docs (`book-primitive.md`, `currency-frame.md`, `tranching.md`) provide the missing primitives, referenced from all consuming docs

#### Item 9 — Phase 6 — Reframing pointers
- [x] `synoteleonomics/teleonome-economics.md` — added "The Recipe Marketplace" section after Synlang-Native Economics; recipe marketplace as the alignment-via-economics surface; teleonome economics + marketplace read together
- [x] `synoteleonomics/synomic-game-theory.md` — added "How Cooperation Cashes Out: The Recipe Marketplace" section after the closing argument; the game-theoretic claim cashes out through the marketplace as the structural mechanism
- [x] `synoteleonomics/teleonome-binding.md` — added "The Recipe Marketplace as Binding Surface" section after the Directive Override; binding has two surfaces (legibility via beacons, economic via recipes)
- [x] `macrosynomics/synome-overview.md` — added "Self-hosting" section after Implementation Pathways; five levels of self-reference enumeration with cross-refs to boot-model.md, topology.md, and synomics-overview.md §10.5

### Log

Format: `YYYY-MM-DD — what was done`

- 2026-05-04 — Phase 1 complete (synomics/ flattened, inactive/ created)
- 2026-05-05 — Plan reviewed; sequence revised; checklists added
- 2026-05-05 — Item 2 done: root README rewritten (Contents + Key Documents + synomics framing); synomics overview folded into `core-concepts/README.md`; 22 internal links verified
- 2026-05-05 — Item 3 done: `neuro-symbolic-cognition.md` moved synodoxics→neurosymbolic; both READMEs restructured (synodoxics framing tightened to substrate+language; neurosymbolic now hosts the foundational architectural commitment); 10 inline pointers updated across the corpus
- 2026-05-05 — Item 4 done: Ozone single-Guardian model landed in laniakea-docs side. Rank tables in 3 files updated ("Accordant to a Guardian" → "Accordant to Ozone"); Ozone clarification note added to `synomic-agents.md`; Guardian description in `atlas-synome-separation.md` extended; `operational-risk-capital.md` line 112 fixed ("multiple guardians" → "multiple Accordants"). `core-concepts/four-layer-enforcement-stack.md` had no Guardian refs and needed no change
- 2026-05-05 — Item 5 done: Lift consolidation. `synodoxics/lift.md` synthesized from the two `inactive/archive/` source files (68KB → 18KB, ~74% reduction), covering definition, lifted/grounded, false lift, opaque grounded primitives, net lift after costs, meta-lift/self-hosting, weakness as cost-algebra (three channels + composition law + budget-capped), and the synthesis. 4 broken `../lift.md` pointers fixed in `synodoxics/noemar-substrate.md`, `neurosymbolic/attention-allocation.md`, `neurosymbolic/neuro-symbolic-cognition.md`, `core-concepts/rsi.md`. New one-line pointer added to `synoteleonomics/teleonome-economics.md` RSI section. `cognition-as-manipulation.md` skipped — no natural insertion point. `synodoxics/README.md` updated with Vocabulary section + dependency graph note
- 2026-05-05 — Item 6 done: Phase 5.1 beacon framework collapse. Two-tier authority + I/O role replaces the LPLA/LPHA/HPLA/HPHA 2×2 across the active narrative. `core-concepts/beacon-framework.md` rewritten around authority tier (~50 lines). `macrosynomics/beacon-framework.md` fully rewritten (12 sections, ~530 lines), absorbing the conceptual core of `noemar-synlang/beacons.md` (two-role taxonomy, old→new mapping) and `noemar-synlang/listener-loops.md` (in-space calculation pattern). `macrosynomics/short-term-actuators.md` rewritten — Phase 1 beacon set reframed as authority tier + I/O role; "all Low-Power" framing dropped. Risk-framework batch (3 files): `sentinel-integration.md` drops "LPHA Beacons" / "Halo-Side LPHA Beacons" headers, replaces `lpla-checker` row with "synserv verification (in-space calculation)"; `risk-monitoring.md` replaces 2 lpla-checker references with synserv verification; `risk-framework/README.md` resolved-item points at new beacon-framework + listener-loops sketch. 9 single-line sweeps: `core-concepts/binding-mechanics.md`, `macrosynomics/README.md`, `macrosynomics/synome-overview.md`, `macrosynomics/synome-layers.md` (light/medium beacon profile rephrased), `macrosynomics/synomic-agents.md`, `macrosynomics/atlas-synome-separation.md` (lpla-checker row → synserv verification), `synoteleonomics/actuator-perspective.md`, `synoteleonomics/teleonome-binding.md` (4-cell 2×2 → 2-row two-tier table), `synoteleonomics/teleonome-economics.md`. Verification greps clean: tier codes only in `clean-up-plan.md` + the new beacon-framework glossary appendix; `lpla-checker` only in `clean-up-plan.md` + the new historical mapping. Legacy operational identifiers (`lpha-nfat`, `stl-base-{prime}`, `hpla-trade-{actor}`, etc.) retained as stable handles per the approved defaults — only the framework itself was rebadged. `noemar-synlang/beacons.md` and `noemar-synlang/listener-loops.md` remain as source files for Phase 3 (Item 7) cleanup; the conceptual content lives in `macrosynomics/beacon-framework.md` from this point
- 2026-05-05 — Final follow-through on Items 7-8 closeout: (a) **Working notes archived** — moved `notes1.md`, `rewrite-plan-final.md`, `risk-framework-redesign-2026-05-03.md`, `synome-extra-info.md` from `noemar-synlang/` to `inactive/archive/` (Item 7's deferred sub-task; their substrate has been consumed by the Item 8 rewrite). `noemar-synlang/README.md` updated to remove "Phase 2 content (pending rewrite/move)" framing and replace with "Working notes (archived)" listing. `risk-framework/open-questions.md` cross-references updated to `../inactive/archive/risk-framework-redesign-2026-05-03.md`. `clean-up-plan.md` Item 8 row + Item 8 description updated to reference the archived plan-of-record. `noemar-synlang/` now has 12 files (was 16). (b) **noemar-synlang Phase 5 smaller updates** that the rewrite-plan-final.md called for but weren't in `clean-up-plan.md` Item 8's checkbox list: `topology.md` §9 sub-kind vocabulary extended with `ascbook`/`tradingbook`/`termbook`/`structbook`/`hedgebook`/`unmatched` (the Primebook composition sub-books per `../risk-framework/primebook-composition.md`); `runtime.md` §3 standardized vocabulary got a new note documenting the **attestor** beacon class introduced by the risk framework rewrite; `scaling.md` §14 open scaling questions got two new items (j) structural-demand scraper bandwidth and (k) per-pair FX stress profile load; `synlang-patterns.md` got two new sections — §7 Tranche-rule patterns (static / rule-determined notional / step-up coupon / triggered subordination / tranche rights P+T declarations) and §8 Projection-model declaration patterns (Black-Scholes for vanilla options, Monte Carlo for path-dependent, lattice for callable bonds, parametric for CDS, with model-uncertainty haircut as a category property); `settlement-cycle-example.md` got a §3.5 Content-based version showing how the unit-risk-weight rule looks under content-based CRR (Riskbook category match + four-tier resolution) while preserving the doc's synlang-machinery focus, and a refreshed reading-note replacing the prior status note. **Cleanup is now genuinely complete** — every checkbox in `clean-up-plan.md` ticked, all `rewrite-plan-final.md` Phase 5 actions executed, and active corpus has no dangling references to archived files.
- 2026-05-05 — Item 9 (Phase 6 — Reframing pointers) done: four pointer-additions across the active corpus. `synoteleonomics/teleonome-economics.md` got a new "The Recipe Marketplace" section after the Synlang-Native Economics section; `synoteleonomics/synomic-game-theory.md` got a new "How Cooperation Cashes Out: The Recipe Marketplace" section after the closing argument (the game-theoretic claim now cashes out through the marketplace as structural mechanism); `synoteleonomics/teleonome-binding.md` got a new "The Recipe Marketplace as Binding Surface" section reframing binding as having two surfaces (legibility via beacons, economic via recipes); `macrosynomics/synome-overview.md` got a new "Self-hosting" section after Implementation Pathways covering the five levels of self-reference with cross-refs to `boot-model.md`, `topology.md`, and `synomics-overview.md` §10.5. **The clean-up plan is now fully complete.** All nine items closed.
- 2026-05-05 — Item 8 Phase 6 (consistency sweep) done: all six sweep items verified clean — no remaining "gap risk" or "FRTB drawdown" as separate concepts; no remaining state-based CRR table in active corpus (`synomics-overview.md` §7 rewritten to reference new framework with deprecation note explaining the retirement; `noemar-synlang/settlement-cycle-example.md` flagged at top with status note); no "three Star Primes" without Keel; no `lpla-checker` as beacon class (done prior); no old four-book taxonomy without currency-frame/equity-invariant/tranching primitives (the four-book taxonomy is preserved as correct; Phase 1 docs provide the missing primitives). Item 8 (Phase 2 of the original cleanup plan) is now fully complete: Phase 0 ✅ (Keel), Phase 1 ✅ (4 conceptual core docs), Phase 2 ✅ (5 layer docs), Phase 3 ✅ (12 existing docs updated), Phase 4 ✅ (2 superseded docs archived), Phase 5 ✅ (`noemar-synlang/risk-framework.md` trimmed 1612 → 764 lines), Phase 6 ✅ (consistency sweep clean).
- 2026-05-05 — Item 8 Phase 5 done: `noemar-synlang/risk-framework.md` trimmed from 1612 lines / 62KB to 764 lines / 28KB (~53% reduction). Repositioned as the synlang-flavored complement to the canonical conceptual docs in `../risk-framework/`. Kept: atom shapes for the four-book taxonomy, category atom shapes (three types), Riskbook composition constraints in synlang, stress simulation patterns, four-tier resolution as synlang code, loop and recursion handling, default-deny CRR-100% mechanism, all five worked examples (the technical-reference value), cross-doc invariants. Dropped: conceptual content now in `../risk-framework/` (book taxonomy explanation, category framework explanation, per-book-type computation flow narrative, stress simulation conceptual treatment, govops/endoscraper division narrative). All synlang code patterns retained.
- 2026-05-05 — Item 8 Phases 3 + 4 done: 12 existing risk-framework/ docs updated and 2 superseded docs archived. Updates: `README.md` (full rewrite — new module index in dependency order, foundational-primitives-first reading order, Open Items refreshed), `asset-classification.md` (full rewrite — full risk-type tuple, asset-level liquidity profile primitive, SPTP credit-spread/rate split), `capital-formula.md` (full rewrite — per-position flow consuming the layered model, per-sub-book CRR formulas, TRRC aggregation), `asset-type-treatment.md` (full rewrite — each class via new framework, what-changed table), `matching.md` (full rewrite — credit-spread vs rate distinction preserved, smooth optimization framing replaces binary matched/unmatched), `duration-model.md` (added Generator-entart placement and Phase-1 manual-allocation carve-out), `correlation-framework.md` (full rewrite — two-level concentration, gross-of-hedge in v1), `sentinel-integration.md` (Key Metrics table refreshed with new doc references plus Per-sub-book CRR and Equity-proximity rows), `risk-monitoring.md` (added Sub-book and Equity Metrics section), `examples.md` (full rewrite — v1 crypto-collateralized lending test as canonical end-to-end worked example), `asc.md` and `operational-risk-capital.md` (small parallel-track clarifications and routing-to-ascbook reference). Archived: `collateralized-lending-risk.md` → `inactive/archive/` (gap risk no longer separate concept), `market-risk-frtb.md` → `inactive/archive/` (FRTB drawdown no longer separate concept). Verification greps clean: no dangling references to archived files in active corpus; remaining "gap risk" / "FRTB drawdown" mentions are explicitly historical or describe the unified treatment. Active risk-framework/ now has 22 files totaling 4561 lines. Phase 5 (noemar-synlang/risk-framework.md trim from 62KB → ~25KB) and Phase 6 (cross-cutting consistency sweep across the wider corpus) still pending.
- 2026-05-05 — Item 8 Phase 2 done: five layer docs written in `risk-framework/` — `riskbook-layer.md` (261 lines: unit of regulation, composition constraints, default + currency translation lives here, tactical hedging, bankruptcy-remoteness boundary, category catalog as governance lever, three worked examples covering pure-eth-holding / abf-with-cds-cover / crypto-collateralized-USD-lending), `halobook-layer.md` (220 lines: bundle exposure structure as the general framing — not just liquidity, P+T declarations from the U/P/T decomposition, what Halobook can/cannot affect, no-netting aggregation across Riskbooks, single-unit issuance, v1 `nfat-crypto-lending-fixed-term` catalog), `primebook-composition.md` (296 lines: five sub-books + unmatched as risk-coverage contracts, optimization-shaped vs static-treatment distinction, declarative routing by structural eligibility, treatment-switch policy with structural prerequisites and no motivational scrutiny, crash-oracle schema deferred to Phase 2+, single Primeunit upward to Genbook), `hedgebook.md` (231 lines: two-level hedging architecture, Riskbook tactical vs Hedgebook portfolio applicability, cross-Halobook composition while preserving bankruptcy-remoteness, optimization-shaped pairing of Prime-held hedge instruments to Halobook unit exposures, explicit hedge-failure-mode modeling — counterparty/basis/liquidity/tenor — with the residual-risk equation, currency hedges as a major use case), `projection-models.md` (204 lines: the projection contract `(position, scenario) → stress-loss-number`, category-declared models, examples by position type from Black-Scholes for vanilla options to lattice/Monte-Carlo/parametric, rules and projections as complementary, projection-model risk as own capital dimension via category-level model-uncertainty haircut, honest enumeration of what the framework cannot model). All five within target range. Substrate: §1.6-1.10 of `noemar-synlang/risk-framework-redesign-2026-05-03.md` plus §1-§4 of `noemar-synlang/synome-extra-info.md`. Phase 3 (revising 12 existing docs) and Phase 4 (archive + delete 2 superseded docs) still pending.
- 2026-05-05 — Item 8 Phase 1 done: four conceptual core docs written in `risk-framework/` in dependency order — `risk-decomposition.md` (212 lines: 5 risk types, U/P/T liquidity, cross-default constraint, coverage matrix, default-deny CRR 100%), `book-primitive.md` (214 lines: 6-tuple book, equity invariant, rules + state, real-time recomputation, bankruptcy remoteness), `tranching.md` (214 lines: exoassets/exoliabs vocabulary, waterfall semantics with worked Sparklend example, gap-risk unification, P+T tranche rights), `currency-frame.md` (187 lines: frame vs instrument, three-currency taxonomy with stress profiles, frame inheritance top-down from Generator, Riskbook as translation layer, multi-generator readiness via N=1). All four within ~150-250-line target. Substrate: Parts 1-3 of `noemar-synlang/risk-framework-redesign-2026-05-03.md` plus refinements §1, §3, §6 from `noemar-synlang/synome-extra-info.md`. Each doc has TL;DR, section map, one-line summary, and file map. Cross-references between the four are dense; cross-references to existing risk-framework/ docs and forward-references to Phase-2 layer docs are in place. Phase 2 (layer docs) and Phase 3 (revising existing docs) still pending.
- 2026-05-05 — Item 8 Phase 0 done: Keel question resolved (Spark/Grove/Keel/Obex all accordant to Ozone per CLAUDE.md). Five sites updated: `synomics-overview.md` (Ozone children listing), `noemar-synlang/topology.md` (TL;DR tree + §11 Ozone entart family example), `noemar-synlang/risk-framework-redesign-2026-05-03.md` (Part 2 generator section + Appendix A), `noemar-synlang/synome-extra-info.md` (Q17 resolution note). Verification grep clean: only remaining `Spark/Grove/Obex` hits in active corpus are in `notes1.md` and `rewrite-plan-final.md` describing the issue itself, plus `inactive/`. The "3 Star Primes (Spark, Grove, Keel)" v1-test phrasing is correct as-is — those ARE the 3 Star Primes per CLAUDE.md.
- 2026-05-05 — Item 7 done: Phase 3 noemar-synlang rescope. Five file moves: `synodoxics/synlang.md` → `noemar-synlang/synlang.md` (language reference belongs in tech reference dir); `noemar-synlang/synart-access-and-runtime.md` renamed to `noemar-synlang/runtime.md` (shorter, scoped); `noemar-synlang/topology-population-probmesh.md` → `macrosynomics/topology-layers.md` (meta-architectural layering, not Noemar tech); `noemar-synlang/syn-overview.md` → top-level `synomics-overview.md` (concept map covering everything); `noemar-synlang/govops-synlang-patterns.md` → `inactive/archive/` (historical demo). One file split: `noemar-synlang/syn-tel-emb.md` → §§1-7, 9 (artifact tiers + telseeds + bootstrap + atomspace runtimes + resilience + alignment implications) absorbed into `synodoxics/noemar-substrate.md` as new sections; §8 recipe marketplace extracted to new `synoteleonomics/recipe-marketplace.md` (canonical home); source file deleted. Two rewrites: `noemar-synlang/README.md` rewritten as tight tech-reference intro with new reading order, file map, "where things moved" pointers, vocabulary cheat sheet, cross-doc invariants; `synodoxics/noemar-substrate.md` extended with five new sections (Artifact Tiers, Telseeds and Bootstrap, Atomspace Runtimes, Resilience Model, Alignment Implications). Cross-reference cleanup: ~30 inbound references updated across `macrosynomics/`, `synodoxics/`, `synoteleonomics/`, `noemar-synlang/`, top-level `README.md`, and `risk-framework/open-questions.md`. Top-level README updated: directory descriptions reflect the rescope (synodoxics now hosts Noemar substrate, noemar-synlang is "Noemar runtime + synlang technical reference"); beacon-framework key-doc description updated to "two-tier authority + I/O role under it"; synomics-overview.md added as Implementation-first entry point. `macrosynomics/README.md` extended with "Meta-Architectural Layering" section pointing to `topology-layers.md`. `synoteleonomics/README.md` extended with "Marketplace" section pointing to `recipe-marketplace.md`. `synodoxics/README.md` updated to remove `synlang.md` from reading order, point at `noemar-synlang/synlang.md`. Verification: no broken refs to moved/renamed/deleted files in active docs; all "formerly X" mentions in destination files are intentional explanatory context. Working notes (`notes1.md`, `rewrite-plan-final.md`, `risk-framework-redesign-2026-05-03.md`, `synome-extra-info.md`) and Phase 2 files (`risk-framework.md`, `settlement-cycle-example.md`) remain in `noemar-synlang/`; their refs are updated where it doesn't conflict with their pending-rewrite status. Working note archive+delete deferred to Phase 2 per original plan

---

## Phase 1 — The Reorg (DONE)

Already executed. Final structure:

```
laniakea-docs/
├── README.md
├── clean-up-plan.md             (this file)
├── core-concepts/
├── hearth/
├── macrosynomics/
├── neurosymbolic/
├── noemar-synlang/              (rescoped in Phase 3)
├── synodoxics/
├── synoteleonomics/
├── risk-framework/
└── inactive/
    ├── pre-synlang/             (11 legacy dirs)
    └── archive/                 (lift.md, lift-weakness.md, synomics-README.md, synomics-summary.md)
```

The `synomics/` parent directory is gone; subdiscipline dirs are at top level. The plan has been moved to root.

**Follow-up still owed for Phase 1:**
- Split `inactive/archive/synomics-README.md` content: subdiscipline framing → `core-concepts/README.md`; brief synomics-as-"data-and-AI-governance" mention → top-level `laniakea-docs/README.md`.

---

## Phase 2 — Risk Framework Rewrite

Executes `noemar-synlang/rewrite-plan-final.md` Phase 0-6. **All synlang content goes inline with conceptual content** in `risk-framework/` — no synlang-flavored remnant.

### 2.1 New conceptual docs in `risk-framework/`

`risk-decomposition.md`, `book-primitive.md`, `tranching.md`, `currency-frame.md`, `riskbook-layer.md`, `halobook-layer.md`, `primebook-composition.md`, `hedgebook.md`, `projection-models.md`.

### 2.2 Update existing `risk-framework/` docs

`README.md`, `asset-classification.md`, `capital-formula.md`, `asset-type-treatment.md`, `matching.md`, `duration-model.md`, `correlation-framework.md`, `sentinel-integration.md`, `risk-monitoring.md`, `examples.md`, `asc.md`, `operational-risk-capital.md`.

### 2.3 Archive + delete superseded

- `risk-framework/collateralized-lending-risk.md` → `inactive/archive/` → delete
- `risk-framework/market-risk-frtb.md` → `inactive/archive/` → delete

### 2.4 Source material handling (from noemar-synlang)

- `risk-framework.md` → `inactive/archive/` → content distributed across §2.1 docs → original deleted
- `risk-framework-redesign-2026-05-03.md` → `inactive/archive/` → delete
- `synome-extra-info.md` → `inactive/archive/` → delete
- `notes1.md` → `inactive/archive/` → delete
- `settlement-cycle-example.md` → `inactive/archive/` → folded into `risk-framework/examples.md`

---

## Phase 3 — Rescope `noemar-synlang/` as Tech Reference

**New framing:** `noemar-synlang/` is the canonical home for the **Noemar runtime + synlang** technical specifics. Everything else in the repo assumes familiarity; this is where readers go to find out what Noemar is, how the runtime works, what synlang looks like in practice, and how the substrate is organized.

Analogous to a `smart-contracts/` directory in a financial protocol — distinct from conceptual docs, answers "how is this actually implemented."

### 3.1 What stays / comes in (the tech-reference set)

| File | Status / source |
|---|---|
| `synlang.md` | **Move IN from `synodoxics/synlang.md`** — pure language reference belongs here |
| `synlang-patterns.md` | Stays — code library / idioms (4-constructor, call-out primitive, sentinel formations, platonic kernel) |
| `runtime.md` | Stays — auth, gate, heartbeat, dispatch (rename from `synart-access-and-runtime.md`) |
| `boot-model.md` | Stays — identity-driven boot |
| `scaling.md` | Stays — operational concerns of running networked synart |
| `listener-loops.md` | Stays — in-space calculation pattern |
| `topology.md` | Stays — synart Space topology (where data lives, naming convention, entart tree). Borderline macrosynomics, but it's the "what's in the synart" reference that synlang code reads against |
| `telseed-bootstrap-example.md` | Stays — worked Noemar boot example |
| `README.md` | Rewrite as tight intro to the dir as substrate reference |

### 3.2 What moves out

| Source | Destination |
|---|---|
| `risk-framework.md` + `settlement-cycle-example.md` | `risk-framework/` (per Phase 2) |
| `beacons.md` | merge into `macrosynomics/beacon-framework.md` (per Phase 5.1) |
| `topology-population-probmesh.md` | `macrosynomics/topology-layers.md` (telos/axioms/topology/population — conceptual layering, not Noemar tech) |
| `syn-overview.md` | top-level `laniakea-docs/synomics-overview.md` (concept map covering everything; broader than Noemar/synlang). Replaces `inactive/archive/synomics-summary.md` role. |
| `syn-tel-emb.md` (artifact-tier portion) | merge into `synodoxics/noemar-substrate.md` (or kept inline if it's already there; the synart/telart/embart treatment is shared-brain content) |
| `syn-tel-emb.md` (recipe-marketplace portion §8) | `synoteleonomics/recipe-marketplace.md` |
| `govops-synlang-patterns.md` | `inactive/archive/` (already flagged historical demo) |

### 3.3 Working notes (handled per Phase 2.4)

`notes1.md`, `risk-framework-redesign-2026-05-03.md`, `synome-extra-info.md`, `rewrite-plan-final.md` (after Phase 2 executes) → `inactive/archive/` → delete.

### 3.4 Sibling adjustment in synodoxics

`synodoxics/noemar-substrate.md` — keep in synodoxics (epistemic-cycle / RSI / Rule-Author Agent angle = "shared brain" content), but tighten and add a clear pointer to `noemar-synlang/` for runtime mechanics. Don't duplicate the runtime architecture — point to it.

---

## Phase 4 — `lift` / `lift-weakness` Consolidation

**Source files (read these as input):**
- `inactive/archive/lift.md` (44KB, original)
- `inactive/archive/lift-weakness.md` (24KB, original)

**Destination (create new):** `synodoxics/lift.md` — consolidated, sharp, useful. Target ~10-15KB. Contains everything load-bearing:

- Definition (lift = accumulated reusable understanding; what cognition leaves behind when it makes future cognition easier)
- Lifted vs grounded duality
- False lift (cost side; what to detect and revise)
- Opaque grounded primitives (LLMs, neural matchers, JIT paths — calibrate per context, lift the dispatch, wrap with checks)
- Meta-lift / RSI / lift-the-lifters / self-hosting
- Net lift after costs as the optimization target
- Weakness as cost-algebra (the companion concept): three channels (evidential / cultural / pragmatic), composition law, budget-capped weakness for opaque primitives
- The synthesis: lift is what to grow; weakness is how to weigh it; meta-lift is learning to weigh better

Aggressively cut: aerodynamic metaphor exposition, repeated phrasings, philosophical asides, deep vocabulary lists.

**Strategic inline pointers** (one short callout each, not duplication):

- `synodoxics/noemar-substrate.md` — existing "lift framing" callout points to `lift.md`
- `neurosymbolic/neuro-symbolic-cognition.md` (after Phase 5.3 move) — existing "emo as opaque grounded primitive" callout points to `lift.md`
- `core-concepts/rsi.md` — frontmatter quote tightened, points to `lift.md`
- `synoteleonomics/teleonome-economics.md` — RSI section gets a one-line pointer

Discipline: lift vocabulary lives in one place. Other docs reference, don't restate.

---

## Phase 5 — Hard Contradictions & Boundary Fixes

### 5.1 Beacon framework collapse

**Framing.** Beacons are the **legible action surface of a teleonome** — cognition stays private in telart, action flows through registered, gate-mediated, cert/auth-scoped beacons. Calculation has moved into synart-resolved in-space computation; beacons are pure I/O.

**Authority is the load-bearing axis:**

| Tier | What it is |
|---|---|
| **High authority** | Certified by a synomic agent; auth-scoped to specific verbs/targets; operates a Synomic Agent |
| **Low authority** | No Synomic Agent operation; passive observation OR peer-to-peer teleonome interaction |

**Deliberately non-prescriptive.** The shape underneath authority (input/action per `beacons.md`, or another cut) is left to Phase 1 implementation. Concrete classes (endoscraper/oracle/attestor/relayer/executor/sentinel formation) are first-cut sketches.

**Power-as-axis retires.** With cognition in synart, embodiment cognitive capability is no longer a load-bearing classification axis.

**Affected docs.**
- `macrosynomics/beacon-framework.md` — replace 2×2 with two-tier authority framing; absorb `noemar-synlang/beacons.md` + `noemar-synlang/listener-loops.md`; demote LPLA/LPHA/HPLA/HPHA to historical naming; remove `lpla-checker`.
- `macrosynomics/short-term-actuators.md` — Phase 1 beacons reframed as high-authority (govops-operated) vs low-authority (verify-only).
- `core-concepts/beacon-framework.md` — atomic concept; rewrite around authority tier.
- `risk-framework/sentinel-integration.md` + `risk-framework/risk-monitoring.md` — `lpla-checker` references stale; role moved into synart.

### 5.2 Single guardian (Ozone)

Resolved 2026-05-03 (`noemar-synlang/notes1.md` Q17): **Ozone is the single operational guardian**; USGE Generator + all Primes are direct children. Guardian remains rank-1 type; only count collapses.

**Affected docs:** `macrosynomics/atlas-synome-separation.md`, `macrosynomics/synomic-agents.md`, `core-concepts/four-layer-enforcement-stack.md` — small surgical edits.

### 5.3 Synodoxics ↔ Neurosymbolic boundary

**The framing.** Synodoxics = "shared brain" content (what makes decentralized public AI work — synart, mesh, retrieval, security, substrate). Neurosymbolic = "individual brain" content (what makes any AI under this architecture good at thinking — emo, attention, query mechanics, hardware).

**One-move fix:** `synodoxics/neuro-symbolic-cognition.md` → `neurosymbolic/neuro-symbolic-cognition.md`. Its content is single-emo cognition (synlang as cognitive language, symbolic-neural loop, context as bottleneck) — structurally a neurosymbolic doc.

Update cross-references: `synodoxics/README.md`, `neurosymbolic/README.md`, and inline pointers in both directories.

(Risk framework redesign already absorbed into Phase 2.)

---

## Phase 6 — Reframing Pointers

Now natural since destinations exist post-Phase 3:

- `synoteleonomics/teleonome-economics.md`, `synomic-game-theory.md`, `teleonome-binding.md` — one paragraph each pointing to `synoteleonomics/recipe-marketplace.md` as canonical for the alignment-via-economics surface.
- `macrosynomics/synome-overview.md` — add "Self-hosting" section pointing to `noemar-synlang/boot-model.md` + `noemar-synlang/topology.md` (executable layer).

---

## Recommended Execution Order

(Superseded 2026-05-05 — see **Execution Status** section near the top of this document for the current sequence and progress tracking.)

Original sequence preserved for reference:

1. **Phase 1 (reorg)** — DONE.
2. **Phase 5.2 (Ozone)** — small surface, quick win.
3. **Phase 5.3 (synodoxics ↔ neurosymbolic boundary)** — single file move + cross-ref updates.
4. **Phase 5.1 (beacons)** — moderate; absorbs `beacons.md` + `listener-loops.md` from noemar-synlang.
5. **Phase 4 (lift/weakness)** — can run in parallel with Phase 5.
6. **Phase 3 (noemar-synlang rescope)** — content moves out + `synlang.md` moves in + `README.md` rewrite.
7. **Phase 2 (risk rewrite)** — biggest content scope; uses `inactive/archive/` as source.
8. **Phase 6 (reframing pointers)** — last, after destinations exist.

---

## Net Size Impact

| Stage | Δ |
|---|---|
| Phase 1 reorg | 0 (done) |
| Phase 2 risk rewrite (new docs +50KB; deletions -10KB; archive captures pre-state) | +40KB net in risk-framework/ |
| Phase 3 rescope (~150KB redistributed; `synlang.md` moves in; archive captures intermediate state) | small net change |
| Phase 4 lift reduction (68KB → ~12KB; original archived) | -56KB in active corpus |
| Working notes + summary deletion (after archive) | -110KB |
| Phase 5.3 single file move | 0 |
| Cross-reference updates | 0 |
| **Net active corpus** | **~-125KB** |
| **`inactive/archive/` accumulates** | **~150-200KB** |

Active corpus shrinks meaningfully and gets more coherent; archive keeps context for anything significantly modified.

---

## Out of Scope

- Updating `agent-work/CLAUDE.md` directory-structure section (separate pass after dust settles).
- The other directories now in `inactive/pre-synlang/` — they wait their turn for synlang nativity.
- Cross-reference link updates throughout — execution work, not planning work.
