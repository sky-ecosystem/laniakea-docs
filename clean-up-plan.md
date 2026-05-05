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
| 5 | Phase 4 — Lift consolidation | ⬜ |
| 6 | Phase 5.1 — Beacon framework collapse | ⬜ |
| 7 | Phase 3 — noemar-synlang rescope | ⬜ |
| 8 | Phase 2 — Risk framework rewrite (multi-session; see `noemar-synlang/rewrite-plan-final.md`) | ⬜ |
| 9 | Phase 6 — Reframing pointers | ⬜ |

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
- [ ] Read `inactive/archive/lift.md` (44KB) and `inactive/archive/lift-weakness.md` (24KB) in full
- [ ] Synthesize into `synodoxics/lift.md` (~10–15KB) — see Phase 4 details below for required content
- [ ] Fix inline pointers:
  - [ ] `synodoxics/noemar-substrate.md`
  - [ ] `neurosymbolic/cognition-as-manipulation.md`
  - [ ] `neurosymbolic/attention-allocation.md`
  - [ ] `neurosymbolic/neuro-symbolic-cognition.md`
  - [ ] `core-concepts/rsi.md`
  - [ ] `synoteleonomics/teleonome-economics.md`

#### Item 6 — Phase 5.1 — Beacon framework collapse
**Pause for scoping discussion before execution — bigger ripple than originally estimated.**
- [ ] Rewrite `macrosynomics/beacon-framework.md` with two-tier authority framing
- [ ] Absorb `noemar-synlang/beacons.md` + `noemar-synlang/listener-loops.md` content
- [ ] Demote LPLA/LPHA/HPLA/HPHA to historical naming
- [ ] Rewrite `core-concepts/beacon-framework.md` around authority tier
- [ ] Update `macrosynomics/short-term-actuators.md`
- [ ] Update `risk-framework/sentinel-integration.md` (remove lpla-checker)
- [ ] Update `risk-framework/risk-monitoring.md` (remove lpla-checker)
- [ ] Sweep `core-concepts/binding-mechanics.md`
- [ ] Sweep `synoteleonomics/teleonome-binding.md`
- [ ] Sweep any remaining LPLA/LPHA/HPLA/HPHA hits

#### Item 7 — Phase 3 — noemar-synlang rescope
- [ ] Move `synodoxics/synlang.md` → `noemar-synlang/synlang.md`
- [ ] Rename `noemar-synlang/synart-access-and-runtime.md` → `noemar-synlang/runtime.md`
- [ ] Move `noemar-synlang/topology-population-probmesh.md` → `macrosynomics/topology-layers.md`
- [ ] Move `noemar-synlang/syn-overview.md` → `laniakea-docs/synomics-overview.md`
- [ ] Split `noemar-synlang/syn-tel-emb.md`:
  - [ ] Artifact-tier content → merge into `synodoxics/noemar-substrate.md`
  - [ ] §8 recipe marketplace → `synoteleonomics/recipe-marketplace.md`
- [ ] Archive `noemar-synlang/govops-synlang-patterns.md`
- [ ] Rewrite `noemar-synlang/README.md` as tight tech-reference intro
- [ ] Update `synodoxics/noemar-substrate.md` (tighten + add `noemar-synlang/` pointer)
- [ ] Archive + delete working notes: `notes1.md`, `risk-framework-redesign-2026-05-03.md`, `synome-extra-info.md`, `rewrite-plan-final.md` (after Phase 2 consumes their content)

#### Item 8 — Phase 2 — Risk framework rewrite
**Multi-session. Read `noemar-synlang/rewrite-plan-final.md` first for full detail.**

New conceptual docs in dependency order:
- [ ] `risk-framework/risk-decomposition.md`
- [ ] `risk-framework/book-primitive.md`
- [ ] `risk-framework/tranching.md`
- [ ] `risk-framework/currency-frame.md`

New layer docs:
- [ ] `risk-framework/riskbook-layer.md`
- [ ] `risk-framework/halobook-layer.md`
- [ ] `risk-framework/primebook-composition.md`
- [ ] `risk-framework/hedgebook.md`
- [ ] `risk-framework/projection-models.md`

Update existing:
- [ ] `risk-framework/README.md`
- [ ] `risk-framework/asset-classification.md`
- [ ] `risk-framework/capital-formula.md`
- [ ] `risk-framework/asset-type-treatment.md`
- [ ] `risk-framework/matching.md`
- [ ] `risk-framework/duration-model.md`
- [ ] `risk-framework/correlation-framework.md`
- [ ] `risk-framework/sentinel-integration.md`
- [ ] `risk-framework/risk-monitoring.md`
- [ ] `risk-framework/examples.md`
- [ ] `risk-framework/asc.md`
- [ ] `risk-framework/operational-risk-capital.md`

Archive + delete:
- [ ] `risk-framework/collateralized-lending-risk.md`
- [ ] `risk-framework/market-risk-frtb.md`

noemar-synlang trim:
- [ ] `noemar-synlang/risk-framework.md` (62KB → ~25KB) — coordinate with Item 7

Consistency sweep:
- [ ] No remaining "gap risk" as separate concept
- [ ] No remaining "FRTB drawdown" as separate concept
- [ ] No remaining state-based CRR table
- [ ] No remaining "three Star Primes" without Keel
- [ ] No remaining `lpla-checker` as beacon class
- [ ] No remaining old four-book taxonomy without currency frame / equity invariant / tranching

#### Item 9 — Phase 6 — Reframing pointers
- [ ] `synoteleonomics/teleonome-economics.md` — pointer to `recipe-marketplace.md`
- [ ] `synoteleonomics/synomic-game-theory.md` — same
- [ ] `synoteleonomics/teleonome-binding.md` — same
- [ ] `macrosynomics/synome-overview.md` — add "Self-hosting" section pointing to `noemar-synlang/boot-model.md` + `noemar-synlang/topology.md`

### Log

Format: `YYYY-MM-DD — what was done`

- 2026-05-04 — Phase 1 complete (synomics/ flattened, inactive/ created)
- 2026-05-05 — Plan reviewed; sequence revised; checklists added
- 2026-05-05 — Item 2 done: root README rewritten (Contents + Key Documents + synomics framing); synomics overview folded into `core-concepts/README.md`; 22 internal links verified
- 2026-05-05 — Item 3 done: `neuro-symbolic-cognition.md` moved synodoxics→neurosymbolic; both READMEs restructured (synodoxics framing tightened to substrate+language; neurosymbolic now hosts the foundational architectural commitment); 10 inline pointers updated across the corpus
- 2026-05-05 — Item 4 done: Ozone single-Guardian model landed in laniakea-docs side. Rank tables in 3 files updated ("Accordant to a Guardian" → "Accordant to Ozone"); Ozone clarification note added to `synomic-agents.md`; Guardian description in `atlas-synome-separation.md` extended; `operational-risk-capital.md` line 112 fixed ("multiple guardians" → "multiple Accordants"). `core-concepts/four-layer-enforcement-stack.md` had no Guardian refs and needed no change

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
