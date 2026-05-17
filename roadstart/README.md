# Focused-Work Mode Entry

Phase execution (P1, P2, …). Load: this dir (`roadstart/`) + `../roadmap/` — that's the entire focused-mode preload set. **No dependencies on files outside these two dirs.** Skip `../summaries/` and the rest of the broader corpus. Big-picture mode (Laniakea-wide thinking) entry: `../summaries/README.md`.

The roadmap dir carries **lean P1-scoped versions** of four risk-framework files (`custodial-crypto-risk-form.md`, `matching.md`, `capital-formula.md`, `market-memory-oracle.md`). Their canonical verbose bodies remain at `../risk-framework/`; the lean roadmap copies carry only what P1 binds to and link back for theory / multi-phase content.

## Reading order from cold

1. `big-picture.md` — Laniakea architecture context the roadmap assumes
2. `risk-framework.md` — risk concepts the roadmap assumes (P1-binding details in lean files below)
3. `../roadmap/phase-1-overview.md` — Phase 1 by fronts (orientation layer)
4. `../roadmap/phase-1-spaces.md` — canonical Phase 1 Space-by-Space spec
5. `../roadmap/v1-principles.md` — current P1 invariants (one line each)
6. `../roadmap/attestor-atom-schema.md` — canonical attestor schema
7. `../roadmap/custodial-crypto-risk-form.md` — lean: THE P1 binding risk form body
8. `../roadmap/matching.md` — lean: smooth matched/unmatched blend formula
9. `../roadmap/capital-formula.md` — lean: per-position formulas + TRRC + ER
10. `../roadmap/market-memory-oracle.md` — lean: oracle inputs the risk form consumes
11. `../roadmap/roadmap-ideas.md` — design patterns (lift, insyn/exsyn, sudo staircase, phase-invariant)
12. `../roadmap/p1-nfat-atom-trace.md` — resolved atom-level NFAT heartbeat trace
13. `../roadmap/p1-borrower-nfat-user-scenario.md` — narrative borrower-to-ER scenario
14. `../roadmap/asc-transition.md` — ASC/DAB details (parallel track to TRRC)

## File map

| Doc | Role |
|---|---|
| `big-picture.md` | 5-layer arch, beacon taxonomy, smart contracts (PAU/Configurator/LCTS/NFATS), Noemar substrate, governance, accounting/DSC, phase ladder |
| `risk-framework.md` | 5 risk types, book primitive, tranching + waterfall, currency frame, sub-book taxonomy, default-deny, capital formula, custodial-crypto form body, SDR model, asset risk-type tuple |
| `../roadmap/phase-1-overview.md` | Fronts orientation (structural + operator) above the canonical Space spec |
| `../roadmap/phase-1-spaces.md` | Canonical Phase 1 v4: 72 Spaces, halo class/risk class, constructors, beacons, verbs, ER data flow, genesis sudo sequence, worked NFAT example, V1 carve-outs |
| `../roadmap/v1-principles.md` | 16 invariants distilled from P1 design |
| `../roadmap/attestor-atom-schema.md` | Borrower readiness/admission + riskbook/exobook attestation schemas, ready-empty/funded-active lifecycle, default-deny gate, slashing surface |
| `../roadmap/custodial-crypto-risk-form.md` | **Lean** — P1 binding risk-form body: composition scope, exobook waterfall, CRR component outputs, riskbook aggregation, structbook consumption |
| `../roadmap/matching.md` | **Lean** — smooth blend formula, cumulative capacity matching, P1 SDR allocation source, termbook-vs-structbook |
| `../roadmap/capital-formula.md` | **Lean** — per-position flow, structbook formula (only P1-active), TRRC aggregation, ER target |
| `../roadmap/market-memory-oracle.md` | **Lean** — reducer concept, P1 output families catalog, scenario interface |
| `../roadmap/roadmap-ideas.md` | Sudo staircase, frame mechanism, lift principle and its sub-patterns (code/data, insyn/exsyn, black-box, temporary-equation, phase-invariant), DSC, market-memory, don't-rabbit-hole |
| `../roadmap/p1-nfat-atom-trace.md` | Atom-level NFAT trace: constructor writes, attestor gates, risk-form execution, structbook matching, TRRC / ER rollup |
| `../roadmap/p1-borrower-nfat-user-scenario.md` | User/operator scenario: borrower readiness → Core inclusion → ready-empty books → queue claim / NFAT mint → disbursement → zero-SDR ER update |
| `../roadmap/asc-transition.md` | ASC/DAB/peg-defense detailed mechanics, PSM transition to Grove |

## Pre-synlang ↔ synlang vocabulary mapping

For reading legacy `inactive/pre-synlang/roadmap/` material:

| Pre-synlang term | Synlang-native equivalent |
|---|---|
| Synome-MVP | Universal Spaces (`&core.*`) + per-entity entart subtrees |
| Halo Books (in Synome-MVP) | Factory-created `&entity.halo.<id>.halobook.<hbk-id>` Spaces |
| Halo Units | Atoms inside book Spaces (one unit atom per NFAT) |
| Risk Framework (Synome-MVP entity) | `&core.framework.risk` content (P1 has no `&core.framework.*`; per-halo risk class copies stand in) |
| Attestations (Synome-MVP entity) | Atoms inside book Spaces (gated by class-accordant attest-data auth) |
| Core Halo entries | Atoms in (a future) `&core.registry.corehalo`; P1 collapses into the existing 3 halos |
| LPLA / LPHA / HPLA / HPHA codes | Two-tier authority + I/O role under it; legacy `hpla-` prefix survives only on legacy peer-to-peer beacons |
| `lpla-checker` (legacy beacon class) | Synserv-run in-space calculation — no longer a separate beacon |
