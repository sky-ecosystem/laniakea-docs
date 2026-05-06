# Risk Framework Rewrite — Final Plan

**Date:** 2026-05-03
**Status:** Plan of record. Supersedes Part 4–5 of `risk-framework-redesign-2026-05-03.md` and §10–§11 of `synome-extra-info.md`.
**Scope:** Propagate the redesigned risk framework into canonical docs (`laniakea-docs/risk-framework/` + `noemar-synlang/`); cut working-notes content; resolve cross-doc inconsistencies.

---

## What changed since the old plan was written

The old plan (Part 4–5 of `risk-framework-redesign-2026-05-03.md`) was written before:

- **Ozone single-guardian** topology landed (Q17 resolved)
- **`listener-loops.md`** + **`beacons.md`** sketches landed (calculation moves into synart; old beacon classes collapse into input/action two-role taxonomy)
- **`open-questions.md`** tracker created (5 active deferred items)
- **U/P/T liquidity decomposition**, **Halobook-as-bundle-exposure-structure** (general, not just liquidity), **optimization-vs-static sub-books**, **cross-default → Riskbook constraint** (all in `synome-extra-info.md`)
- The user established a **stylistic preference** for tight, focused docs (~150–250 lines) with implementation deferred — not 500+ line comprehensive treatments

Three implications:

1. The old plan over-specs files. The substrate is settled enough that fewer/shorter docs work.
2. The working-notes docs themselves should be **deleted after propagation**, not retained alongside.
3. The consolidation is a real cut, not just additions.

---

## The plan

### Phase 0 — One unblocking decision (~5 min)

- **Keel:** confirm Spark/Grove/Keel/Obex are all accordant to Ozone (and update any "three Star Primes" example to four). Decision affects examples in `topology.md`, `syn-overview.md`, and the v1 test scenario.

### Phase 1 — Conceptual core (laniakea-docs/risk-framework/, NEW)

Four short docs (~150–200 lines each), in dependency order:

1. **`risk-decomposition.md`** — 5 risk types · teleological grounding · sub-book coverage matrix · U/P/T liquidity · why gap risk unifies into liquidity · cross-default → Riskbook · default-deny CRR 100% as foundational
2. **`book-primitive.md`** — 6-tuple · equity invariant · real-time recomputation · books-as-state-machines
3. **`tranching.md`** — exoasset/exoliab · seniority + waterfall · P/T rights · re-framing overcollateralized lending (subsumes the old gap-risk + FRTB-drawdown duality)
4. **`currency-frame.md`** — frame vs instrument · currency taxonomy · Riskbook as translation layer · v1 single-frame note

### Phase 2 — Layer docs (laniakea-docs/risk-framework/, NEW)

5. **`riskbook-layer.md`** — default + frame translation + tactical hedging
6. **`halobook-layer.md`** — *bundle exposure structure* (general; not just liquidity) · P/T declarations
7. **`primebook-composition.md`** — sub-books as risk-coverage contracts · optimization vs static · treatment-switch policy · crash-oracle deferred
8. **`hedgebook.md`** — two-level hedging · hedge-failure modeling · currency hedges
9. **`projection-models.md`** — projection pattern · projection-model risk dimension

### Phase 3 — Update existing risk-framework/ docs

Each is a real edit pass, but most should *shrink*:

| File | Action |
|---|---|
| `README.md` | New module index; foundational primitives at top; updated open items |
| `asset-classification.md` | Extend to full risk-type tuple; add asset-level liquidity profile primitive (load-bearing) |
| `matching.md` | Preserve credit-spread vs rate insight; reframe as sub-book optimization |
| `capital-formula.md` | Downstream consumer of new layered model |
| `correlation-framework.md` | Two-level concentration (Primebook + Genbook) |
| `duration-model.md` | Generator-entart placement; Phase 1 manual-allocation carve-out |
| `asset-type-treatment.md` | Rewrite each class via new framework |
| `sentinel-integration.md` | Update beacon outputs to reflect listener-loops + two-role taxonomy |
| `risk-monitoring.md` | Add per-sub-book CRR, equity-proximity alerts |
| `examples.md` | Replace with the v1 crypto-lending test as canonical worked example |
| `asc.md`, `operational-risk-capital.md` | Small updates clarifying parallel-track status |

### Phase 4 — Deletions (the cut)

| Delete | Why |
|---|---|
| `risk-framework/collateralized-lending-risk.md` | Folded into `tranching.md` (gap risk is no longer a separate concept) |
| `risk-framework/market-risk-frtb.md` | Folded into `tranching.md` / `asset-type-treatment.md` (`forced-loss-capital` is unified) |
| `noemar-synlang/risk-framework-redesign-2026-05-03.md` | Working notes; content propagated |
| `noemar-synlang/synome-extra-info.md` | Working notes; content propagated |
| `noemar-synlang/notes1.md` | Session handoff; obsolete after propagation |

### Phase 5 — noemar-synlang updates

The big lift is **`noemar-synlang/risk-framework.md`** (62KB / ~1600 lines, currently load-bearing for the four-book + categories model and uses old state-based CRR framing in the worked-example tail).

**Recommended:** trim to ~25KB / ~600–800 lines, repositioned as the *synlang-flavored* treatment (atom shapes, equation forms, four-tier resolution as synlang code, 5 worked examples). Conceptual material defers to `laniakea-docs/risk-framework/`.

(Alternative: split into 4–5 files. Recommend against — adds navigation cost without saving lines.)

Smaller updates:

| File | Change |
|---|---|
| `topology.md` | Add `generator` entity type + sub-book sub-kinds + hedgebook to keyword vocabulary; entart examples |
| `syn-overview.md` | Risk-framework section refs new docs |
| `synlang-patterns.md` | Add tranche-rule + projection-model declaration patterns |
| `settlement-cycle-example.md` | Replace state-based CRR with content-based (use v1 test as canonical example) |
| `synart-access-and-runtime.md` | Note attestor as new beacon class |
| `scaling.md` | Note structural-demand scrapers, per-pair FX stress profile load |

### Phase 6 — Cross-cutting consistency sweep

Single pass to verify no remaining references to:

- "gap risk" as separate concept (→ liquidity / forced-loss-capital)
- "FRTB drawdown" as separate concept
- Old state-based CRR table (`(crr filling 5)` etc.)
- "three Star Primes" without Keel
- `lpla-checker` as a beacon class (it disappears per `beacons.md`)
- Old four-book taxonomy without currency frame / equity invariant / tranching

---

## Outstanding decisions worth getting up front

1. **Keel** (Phase 0) — single sentence
2. **Length target** for the new conceptual docs — confirm ~150–250 lines is right (per `notes1.md` guidance)
3. **`noemar-synlang/risk-framework.md` strategy** — trim (recommended) vs split into 4–5 files
4. **Beacon implementation update** (`lpla-checker` algorithm rewrite) — separate later pass, or part of this work? Recommend **separate**; this rewrite is conceptual/structural, beacon impl is mechanical follow-on
5. **Real-time computation cadence** (item B from `synome-extra-info.md` §8) — confirm hot-path real-time + settlement-batch hybrid before it's baked into the new docs
6. **Migration of existing on-chain positions** into the new model — defer entirely (governance work, post-rewrite)

---

## Scope and net delta

| | Before | After (est.) |
|---|---|---|
| `risk-framework/` files | 15 | 22 (9 new − 2 deleted) |
| `risk-framework/` size | ~88 KB | ~140 KB (more conceptual coverage) |
| `noemar-synlang/` files | 17 | 14 (3 deleted) |
| `noemar-synlang/` size | ~446 KB | ~330 KB (trimming `risk-framework.md` + 3 deletions) |
| **Total** | **~534 KB** | **~470 KB** (~12% smaller, much better organized) |

The net-savings is real but modest — the bigger win is **moving working-notes content into a clean canonical structure** that future readers can enter at any of the 4 conceptual roots.

---

## Suggested execution order (turn-by-turn)

**Phase 0 → Phase 1 (4 docs, may be one turn each or batched 2-at-a-time) → Phase 2 (5 docs) → Phase 3 updates (batchable) → Phase 4 deletions (one turn) → Phase 5 (noemar-synlang trim is the big single turn; small updates batchable) → Phase 6 sweep**.

Phase 1 is highest-value first work. After Phase 2 lands, the canonical structure exists even if Phase 3+ hasn't propagated yet — that's a stable resting point.

---

## Reading order for someone catching up cold

1. This document — the plan of record
2. `risk-framework-redesign-2026-05-03.md` Parts 1–3 + 6–8 (substrate; will be deleted in Phase 4 but read before deletion if needed for context)
3. `synome-extra-info.md` §1–§8 (refinements; same)
4. `notes1.md` (session handoff; same)
5. Existing `laniakea-docs/risk-framework/*.md` files (what's being rewritten)
6. Existing `noemar-synlang/risk-framework.md` (what's being trimmed)

After Phase 1–2 land, the entry point shifts to:

1. This document
2. `laniakea-docs/risk-framework/risk-decomposition.md` → `book-primitive.md` → `tranching.md` → `currency-frame.md`
3. Layer docs in dependency order
4. Existing material as updated
