# Cleanup TODO

Tracker for deferred cleanup work across the laniakea-docs corpus. Items identified during summary review and the input-beacon rename pass (2026-05). Grouped by theme; rough sequence proposed in §0.

## §0 Suggested sequence

Most are independent, a few have order dependencies:

1. **Pass A — Fractal naming** (§1) is the keystone. Many other items name things; doing them before naming conventions are resolved means re-doing them.
2. **Pass B — Stub-spec graduation** (§2) depends on Pass A for beacon class names and instance identifier shapes.
3. **Pass C — Open-questions consolidation** (§3) is light, can happen anytime — useful before Pass B so each stub-spec sees its full open-question list in one place.
4. **Pass D — Legacy-state sunset audit** (§4) is independent and light.
5. **Pass E — Detail-file token-bloat audit** (§5) is the highest-leverage corpus-quality pass given the LLM-first design (detail files should be pure reference; summaries carry orientation). Best done after A so renames don't have to be repeated inside detail files.
6. **Pass F — Numeric-fact source-of-truth** (§6) is structural; sequence independent.
7. **Pass G — Canonical-home claim integrity** (§7) is focused; light. Anytime.
8. **Pass H — Final hygiene** (§8, §9, §10) is polish, last.

Recommended order: C → A → D → E → F → G → B → H. (C done 2026-05-11. **A done 2026-05-13** — see §1 note. **D done 2026-05-15** by deletion of `legacy-state.md`; **Pass H2 also closed** by the same deletion.)

---

## §1 Fractal naming pass (Pass A) — RESOLVED 2026-05-13

The naming convention has been locked in and swept across the corpus. Canonical reference: [`../noemar-synlang/topology.md`](../noemar-synlang/topology.md) §9. Decisions:

- **Delimiter:** `.` for hierarchy between Space-name segments; `-` for compounds within one segment. Forces explicit disambiguation between phrase-names and real sub-hierarchies.
- **Sigil:** `&` retained on every Space reference; non-Space identifiers (beacons, verbs) are dash-only, no sigil.
- **Beacon-class taxonomy collapsed to 6 (plus synserv):** `market-data-beacon`, `attest-data-beacon`, `patch-beacon`, `relay`, `sentinel`, `synserv`. Endoscraper retired as a class — it is now a grounded runtime primitive (`(chain-read $contract $slot)`) accessible from any rule in any Space. Per-protocol metadata lives in `&core.protocol`.
- **Sentinel/relay reclassification:** what was "sentinel formation (Baseline / Stream / Warden / Principal)" is now three classes — `baseline-{prime}` (relay, deterministic), `warden-{prime}-{op}` (relay, deterministic halt monitor), `stream-{prime}-{actor}` (sentinel, variant stream), `principal-{owner}` (sentinel, variant principal-sentinel). Cognitive density is the load-bearing differentiator between relay (none) and sentinel (call-out density into operator telart).
- **LPLA/LPHA/HPLA/HPHA prefixes stripped** on new identifiers. The four-letter codes encoded the retired power-axis. `hpla-` prefix survives only on legacy peer-to-peer trade beacon names (`hpla-trade-*`) as a stable handle.
- **Versions move out of Space names** into atoms (e.g., `(runtime-version noemar 0.1.0)`).
- **Sub-ids as new levels** (`&entity.halo.spark-term.book.A1`, not `book-A1`); **compound ids preserved** as one segment (`spark-term`, `crypto-majors` stay joined by `-`).
- **Risk-framework subspaces nest** under `&core.framework.risk.*` (forms, scenarios, asset-profiles, concentration). Previously flat under `&core.framework.*`. Note: the `category → form` rename landed in the 2026-05-15 sweep; `&core.framework.risk.categories` was renamed to `&core.framework.risk.forms` and no `&core.framework.*` Space exists in P1 (canonical source ships at a later phase boundary).
- **`&core.endoscrapers` Space deleted** — endoscraper is a primitive, no staging needed.
- **Sentinel loops not in `&core.loop.*`** — strategy is per-operator, lives in `&entity.<type>.<id>.sentinel.<actor>` with cognitive call-outs into operator telart.

Sweep details remain valid as references; original §1 enumeration below is preserved for history.

### 1.0 Historical enumeration (pre-resolution)

The corpus had multiple overlapping name-spaces that had evolved piecemeal:

The corpus has multiple overlapping name-spaces that have evolved piecemeal:

- **Space names** — `&core-…`, `&entity-<type>-<id>-<sub-kind>` (sigil convention)
- **Class taxonomies** — `market-data-beacon`, `attest-data-beacon`, `patch-beacon`, `endoscraper`, etc.
- **Beacon instance identifiers** — used as the *subject* in registry atoms (e.g. `market-data-crypto-majors-chainlink`)
- **Operational identifier prefixes** — legacy `lpha-`, `lpla-`, `hpha-`, `hpla-` (semantically empty after authority-axis retirement, but still appear on ~214 deployed beacon-name strings)
- **Operational verbs** — `oracle-write-tick` → `market-data-write-tick` (partially renamed); many others
- **Recipe / loop / framework Space sub-naming** — `&core-loop-<class>`, `&core-recipe-*`, `&core-framework-*`

The principled question: which prefixes carry meaning, which are decoration, what is the canonical shape for each name-space?

### 1.1 Known deferred items

- **`lpha-attest` (bare form)** in 9 files: `smart-contracts/nfats.md`, `synomic-entities/halo-term.md`, `synomic-entities/halo-classes.md`, `synomic-entities/halo-portfolio.md`, `summaries/sentinel.md`, `sentinel/sentinel-network.md`, `roadmap/roadmap-ideas.md`, `summaries/smart-contracts.md`, `summaries/synomic-entities.md`. Resolve as part of LPLA/HPLA prefix decision.
- **LPLA/LPHA/HPLA/HPHA prefix question** — 214 occurrences. Four-quadrant authority×power matrix retired but prefixes survive on identifiers. Decide: (a) strip them everywhere, (b) keep as legacy convention with explicit translation table, or (c) hybrid.
- **`lpla-checker`** — listed in old→new mapping tables as a deleted beacon class. Decide whether to keep the migration row or delete it once Pass A resolves.
- **`oracle-write-exsyn-trrc`** verb remnant in `roadmap/phase-1-spaces.md:314` — currently in a "X in place of retired Y" sentence.

### 1.2 Suggested deliverable

A `noemar-synlang/naming-conventions.md` (or section in existing `topology.md`) that:
- Enumerates every name-space with its sigil/prefix rules.
- States the instance-identifier convention (class-derived prefix without redundant class-suffix; e.g., `market-data-beacon` class → `market-data-{X}` instance).
- Documents the LPLA/LPHA decision with rationale.
- Provides a single legacy→current translation table for each rename.
- Becomes the reference for any future class taxonomy change.

After this lands, sweep corpus-wide.

---

## §2 Stub-spec graduation (Pass B)

Several rank-2 entities and on-chain pieces are explicitly stub-spec'd. Each has enough detail to look load-bearing but not enough to act on. The half-state is worse than either pole.

| Stub | Open items | Suggested action |
|---|---|---|
| **Oracle Entity** | Fee model for tokenless entities (does 5% + 50 bps apply?), slashing magnitudes, decentralization requirements, cross-entity data dependencies | Closest to decision — Phase 1 already names two instantiations. Promote to target architecture or explicitly mark sections "deferred to Phase N" with decision criteria. |
| **Sequencer Entity** (`synomic-entities/sequencer-entity.md`) | Beacon class names (`sequencer-receive` / `-match` / `-cancel` tentative), sequencing model, matching algorithm, censorship resistance, MEV evidence trail, fee structure, cross-Sequencer price coherence | Decide beacon class names as part of Pass A. Other items defer with clear decision criteria. |
| **Pylon Entity** (`synomic-entities/pylon-entity.md`) | Per-Ring assurance-fund pool implementation, customer abstraction, inter-Pylon clearing protocol, margin schedules, cross-Ring positions, liquidation mechanics, default-cascade response | Largest stub — likely needs its own design doc. Defer until clearing/derivatives roadmap firms. |
| **Core Entity (additional modes)** | Currently two scoped modes (halo / busted-prime-or-halo). Guardian-collapse handling deliberately out of scope. | Track in `core-entity.md`: "future modes may include Guardian-wrap" with criteria for adding one. |
| **Diamond PAU** | Facet sets defined per phase; current spec is placeholder | Promote to full target spec when first non-monolithic PAU ships. |
| **Folio PAU spec** | Currently deferred entirely | Write a full spec when Folio creation goes live. |

---

## §3 Open-questions consolidation (Pass C) — **DONE 2026-05-11**

Resolved with option (b) — inline-only, no central register. The
canonical home for each open question is the doc whose scope it
belongs to; cross-cutting questions live in one home with
cross-refs from siblings.

Actions taken:

- Deleted standalone `risk-framework/open-questions.md`; its 5
  entries re-homed:
  - Q24 attestor schema → `noemar-synlang/beacons.md` Open questions (item 6)
  - Q26 privacy buckets → `risk-framework/riskbook-layer.md` §9
  - Q27 crypto stress calibration → `risk-framework/asset-classification.md` §7
  - Correlation specifics → `risk-framework/correlation-framework.md` §6 (content already inline; cross-link to standalone removed)
  - USDS lot-age tracking → `risk-framework/duration-model.md` Open questions
- Updated all dangling cross-refs (asset-type-treatment.md, currency-frame.md, scaling.md, runtime.md) to point at new homes.
- De-duplicated `macrosynomics/beacon-framework.md` ↔ `noemar-synlang/beacons.md`: canonical list lives in noemar-synlang/beacons.md; macrosynomics now points to it.
- Promoted inline NFATS open items in `smart-contracts/nfats.md` (Prime→Facility onboarding mechanism, `nfat-{halo}` relay integration) into a dedicated Open Questions section.
- Phase-1 carve-outs in `roadmap/phase-1-spaces.md` are scoped decisions, not open questions — left in place under §V1 Carve-outs.
- Per-entity stub-spec open questions (Oracle / Sequencer / Pylon / Core / Halo Identity / Creation-Restructuring) already had inline Open Questions sections and were left in place — they're stub-spec scope, owned by Pass B (stub-spec graduation).
- `growth-staking/growth-staking.md` §5 + §12 already serve the dedicated-section role; kept as is.
- `synodoxics/noemar-substrate.md` "What's Still Being Designed" already serves the role; kept as is.

Standardization note: most sections now follow a What / Why / Forcing trigger pattern, though the older inline-list style survives in some files (atlas-synome-separation.md, halo-identity-network.md, topology-layers.md §9). Tightening these to the standard template is light editorial work and deferred to a later polish pass (Pass H).

---

## §4 Legacy-state sunset audit (Pass D) — RESOLVED 2026-05-15

`roadmap/legacy-state.md` was deleted along with the `&core.framework.fee` cadence-atom reference it contained. The legacy content (monthly settlement reality, three legacy asset categories, CCB reclass, SBE config) is no longer in the corpus; operational reality during transition is treated as out-of-band knowledge. This pass is closed by deletion of the audited file.

---

## §5 Detail-file token-bloat audit (Pass E)

The repo is designed for LLM consumption: root README + `summaries/` (all 14 files) is the default loaded context; detail files are paged in surgically. Per this design, detail files should be **pure reference** — formulas, atom shapes, worked examples, parameter tables, edge cases — and carry no orientation layer.

Most detail files almost certainly have orientation duplication with their summary: status banners at the top, TL;DR / intro prose, section maps, Cross-references sections, Key vocabulary sections, File map sections. Each byte of this is waste because the LLM already has it from the summary.

**Suggested action:**

1. Pick the largest 3–5 detail files (by token weight) as a sample. Candidates: `smart-contracts/nfats.md`, `noemar-synlang/topology.md`, `risk-framework/capital-formula.md`, `accounting/settlement-cycle.md`, `synomic-entities/halo-term.md`.
2. For each, identify orientation content (status banners, intro prose explaining what the doc is, section maps, cross-ref lists, glossary-style vocab definitions, doc-shape file maps).
3. Strip orientation; keep only pure reference. Measure token reduction.
4. From the sample, derive rules for the corpus-wide pass.

Rules to apply (likely):
- Drop status banners from detail files. Status lives in the summary.
- Drop intro / TL;DR / "what this doc is" preambles. The summary's TL;DR + section map covers it.
- Drop section maps at top of detail files. Headings serve the same function in a file already opened.
- Drop Cross-references sections from detail files — or trim to *forward* pointers (deeper detail) only. Summary handles lateral cross-refs.
- Drop Key vocabulary sections from detail files unless they introduce terms not in the summary.
- Drop File map sections from detail files. The summary has it.

After the sweep, detail files should typically be 20–40% lighter with no information loss for an LLM that has summaries loaded.

---

## §6 Numeric-fact source-of-truth (Pass F)

Specific parameters appear quoted across many docs:

- SORL = 25%/18h
- IRL = $100K
- ABC floor = $125M (Phase 1); target 1.5% of USDS supply (post-Genesis)
- 5% Entity Creation Fee
- 50 bps/yr Entity Upkeep Fee
- ER target ≤ 0.90
- TTS components (warden tick + call-out latency + halt propagation)
- LCTS daily lock 13:00 UTC / settle 16:00 UTC
- Various phase numbering and entity counts ("six operational Primes")

If one number changes, the others drift silently. **Suggested action:** either (a) designate one canonical location per numeric parameter (others link to it without duplicating the value), or (b) accept duplication and add a sync script. (a) is the better long-term shape but needs an initial designation pass.

Phase numbering ("Phase 1 / 2–4 / 5–8 / 9–10") and entity counts should also have a single source.

---

## §7 Canonical-home claim integrity (Pass G)

15 files use the phrase "canonical home" to mark themselves authoritative for some concept. Verify:
- Every claim points to a file that exists.
- No concept has two "canonical home" claims (duplication).
- Every concept that should have one *does*.

Light pass — one grep + walkthrough. Worth doing before §6 (since canonical-home designations naturally pair with numeric-fact designations).

---

## §8 patch-beacon scaffold formalization (Pass H1)

`patch-beacon` is described inconsistently — both as a one-off Phase-1 hack AND a reusable pattern for future scaffolds. Pick one:

- **A. One-off:** write the explicit migration plan from `patch-{prime}` exsyn-TRRC to insyn coverage, with target phase. Mark the class for retirement.
- **B. Reusable:** give it a real spec — admission criteria, audit requirements, mandatory sunset triggers per instance, governance review pattern.

Currently docs imply B but only specify A.

---

## §9 SBE current-vs-target cross-reference (Pass H2) — RESOLVED 2026-05-15

`roadmap/legacy-state.md` was deleted; there is no separate doc describing the current SBE fixed-buyback config to cross-reference. This pass is closed by deletion of the cross-ref target.

---

## §10 Status-marker hygiene (Pass H3)

"Live / mostly target / mixed / speculative" is inconsistently applied. **Suggested action:** tighten to:

| State | Definition |
|---|---|
| **Live** | All claims in this scope reflect deployed/operational reality |
| **Partial** | Some claims live, some target; section headers call out their own status |
| **Target** | All claims describe target architecture; not yet operational |
| **Speculative** | Designs under active evolution; major shape changes expected |

Apply uniformly at section level where status varies within a doc. Update `summaries/README.md` Index status column once ladder is finalized.

---

## §11 Other small items

- **`trading/` references** — directory removed; 15 references across the corpus still point to it. Sweep: redirect to `sentinel/` where applicable, delete otherwise. Root `README.md` Active table still lists `trading/` as a top-level dir.
- **Dangling `dir/README.md` links in root `README.md`** — 7 broken links in Key Documents (`core-concepts/README.md`, `risk-framework/README.md`, `synomic-entities/README.md`, `smart-contracts/README.md`, `trading/README.md`, `governance/README.md`, `roadmap/README.md`) plus one malformed (`trading/README.md` → `(laniakea-docs/sentinel/README.md)`). Per design intent, dir READMEs intentionally don't exist; the links should be deleted or repointed to `summaries/<dir>.md`. **Doing this now alongside §11 update.**
- **Glossary / acronym registry** — ~30+ acronyms (TRRC, TRC, SORL, IRL, JRC, SRC, MDC, ABC, CCB, SBE, NRR, TMF, TTS, ORC, RTI, GF, DR, LDR, ASC, DAB, SPTP, HF, RW, CRR, PSM, NFAT, LCTS, PAU, BEAM, PT, YT…) defined inline in many files. Old whitepaper had `appendix-f-glossary.md`. Active corpus doesn't have a central glossary. Decide: add one, or formally point to per-doc Key Vocabulary sections.
- **"In flux" marker consistency** — content tagged "in flux," "TBD," "stub spec," "deferred," "open" with inconsistent vocabulary. Tighten to a small set (alongside §10 status ladder) so they're greppable.
- **`trading/` → `sentinel/` migration note** — add a one-line history stub somewhere (probably root README) so git-blame and historical readers aren't confused.
- **`summaries/core-concepts.md`** — telos-point definition now lives there (post-hearth merge); sweep for any remaining stale `hearth/` pointers in the corpus.
- **Synomic Agent → Synomic Entity rename** — described as "fully landed" in `core-concepts.md` but `growth-staking.md` summary still references "Sky Agents preserved as historical LHS." Either finish the sweep or stop claiming it's done.

---

## §12 Beacon-class conceptual treatment (open)

Resolution of Pass A clarified the beacon taxonomy mechanically (6 classes + synserv) but **the conceptual treatment of the four "real" beacon classes is still open**. Each of `sentinel`, `relay`, `market-data-beacon`, `attest-data-beacon` represents a kind of trust relationship that needs proper synodoxics treatment before later phases:

- **What governance criteria** admit a new instance of each class (which market-data provider, which attestor class, which sentinel operator, which baseline-relay scope)?
- **What synodoxics arguments** justify the trust model — provider redundancy & dispute (market-data), slashing & class-accordance (attest-data), bounds + warden coverage (sentinel), deterministic verifiability (relay)?
- **What structural constructors** (factory shapes) would later instantiate new instances under governance gating, vs the current Phase 1 sudo-inline pattern?

Phase 1 uses sudo-inline stand-ins for all of these — defensible at small scale (governance manually vets each), doesn't scale.

**Patch-beacon explicitly excluded** — it has no regulated framework by design, sudoed inline as a Guardian-issued scaffold, designed to sunset. No synodoxics or structural-constructor work needed; just clean retirement criteria per use case.

**Suggested deliverable:** a synodoxics-style probmesh treatment per class, eventually crystallizable into structural-constructor specs. Most natural home is probably a `noemar-synlang/beacons.md` expansion or a new `synodoxics/beacon-classes.md` doc. Not in scope for the v1 substrate work.

---

## Tracking

When picking up a pass:
- Update this file's status for that pass (e.g., "Pass A — in progress, started 2026-XX-XX").
- Cross-link any new docs created (e.g., `noemar-synlang/naming-conventions.md`) from here.
- After completion, mark the pass complete with a date and delete or archive resolved items.
