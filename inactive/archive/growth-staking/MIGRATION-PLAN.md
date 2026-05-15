# Growth Staking Migration — Execution Plan

**Goal:** Migrate `growth-staking.md` into the active post-synlang corpus as a new top-level `growth-staking/` directory. Translate vocabulary, add a stUSDS section, add a synlang form section, update cross-references.

**Output location:** `laniakea-docs/growth-staking/`

---

## 1. Context to load (cold-start checklist)

Read these in order. Total ~30k tokens, all required to execute correctly.

### Source material
- `inactive/pre-synlang/growth-staking/growth-staking.md` — the spec being migrated
- `inactive/pre-synlang/growth-staking/README.md` — pointer doc
- This file (`MIGRATION-PLAN.md`)

### Active hooks that already reference growth-staking (sweep targets)
- `synomic-entities/folio.md` — has §"Growth Staking" + 2 file-map entries pointing at `inactive/pre-synlang/...` with "(rewrite pending)"
- `synomic-entities/creation-restructuring.md` — file-map entry; §"Folio seeds a Prime" example mentions GF 2.5×
- `synomic-entities/core-controlled.md` — declares "Excluded from Growth Staking"
- `synomic-entities/recovery.md` — declares "Excluded from Growth Staking"
- `synomic-entities/README.md` — Related list
- `README.md` (top-level) — `growth-staking` listed under inactive directory table

### Vocabulary references (to verify post-synlang naming during the swap)
- `accounting/capital-stack.md` — canonical TEJRC / TISRC / srUSDS / IJRC / EJRC vocabulary
- `synomic-entities/generator.md` — Generator / USGE / USDS naming
- `synomic-entities/prime.md` — Prime token / risk-capital ingression
- `synomic-entities/guardian.md` — Ozone (single operational Guardian)
- `synomic-entities/halo-classes.md` — Halo Class / Book / Unit
- `smart-contracts/lcts.md` — LCTS-issued tokens (srUSDS, TEJRC, TISRC)

### Synlang patterns to mirror
- `accounting/settlement-cycle.md` §1–§5 — synserv heartbeat shape, atom shapes, governance facts in `&core-framework-fee`, two-phase settlement
- `accounting/duration-allocation.md` §11 ("Synlang form") — clean template for the synlang section to add
- `phases/phase-1-spaces.md` — Phase 1 carve-out pattern + `&core-framework-*` Space layout
- `phases/phases-ideas.md` — insyn/exsyn pattern + lift principle (don't write Python placeholders)
- `noemar-synlang/topology.md` §6 (synome-root layers) — naming convention `&core-framework-*`

### High-level
- `README.md` — top-level repo index (will be updated)
- `synomics-overview.md` §8, §11, §19 — settlement cadence, scaling economics

---

## 2. Decisions baked in

These were settled in conversation; treat them as fixed. Don't re-debate.

| # | Decision | Implication for writeup |
|---|---|---|
| 1 | **stUSDS is a Morpho-pool-style lending product.** USDS holders deposit into stUSDS; capital becomes available for growth stakers to borrow at a variable rate. Sky Core earns **10% of the spread above the base rate**. | Add a new §"stUSDS — borrow surface for growth stakers" to `growth-staking.md`. Add `stUSDS spread (10% of borrower spread above base rate)` as a line in SKY Reference Value's Core Revenue list. Confirm stUSDS itself is **excluded** from growth-asset eligibility (passive yield wrapper for depositors). |
| 2 | **Trailing revenue window: T12M annualized.** | Replace the "open question" in the source's §"Open Design Questions" with a concrete value. Note in writeup that this is governance-tunable. |
| 3 | **Growth score → P/E mapping: linear with caps.** Score is `clamp(growth_rate / target_growth_rate × 100, 0, 100)`. | Replace the abstract "score (0–100)" with this concrete formula in §"Global P/E Model". |
| 4 | **Forfeited rewards flow to TMF.** Stakers below 100% staking factor leave unclaimed rewards on the table; those rewards re-enter the Treasury Management Function waterfall. | One sentence in §"Reward Scaling" + one line in the settlement cross-ref. |
| 5 | **Single-file spec.** Don't split Reference Valuation into its own doc. | Keep `growth-staking.md` as the single content file under `growth-staking/`. |

---

## 3. Output structure

```
laniakea-docs/
├── growth-staking/                      ← new top-level directory
│   ├── README.md                        ← directory index, scope, relations
│   └── growth-staking.md                ← migrated + updated spec
└── inactive/pre-synlang/growth-staking/
    ├── README.md                        ← leave as-is (history)
    ├── growth-staking.md                ← leave as-is (history)
    └── MIGRATION-PLAN.md                ← this file (leave as-is after execution)
```

The active doc replaces the inactive one in cross-refs, but the inactive directory stays put as historical record (matches the existing pattern for other inactive content).

---

## 4. New `growth-staking.md` outline

Use this section ordering. Source content maps cleanly onto it; new sections marked **NEW**.

1. **Overview** — what growth staking is, what's eligible, why
2. **The Growth Factor** — GF tiers table; eligible/excluded asset list
3. **Reward Scaling** — staking factor formula; multi-asset example; forfeited rewards → TMF (decision 4)
4. **Reference Valuation** — header explaining "fundamentals everywhere"
   - 4.1 **Global P/E Model** — Base P/E, Modifier, Variance, growth score (linear with caps per decision 3); worked example
   - 4.2 **SKY Reference Value** — Core revenue list (incl. **stUSDS spread per decision 1**) + Special revenue
   - 4.3 **Generator Reference Value** — operating revenue + ISRC book value
   - 4.4 **Guardian Reference Value** — accord fee income + SKY holdings
   - 4.5 **Prime Reference Value** — net capital reserves only
   - 4.6 **Halo Reference Value** — capital reserves + earnings × P/E
   - 4.7 **Agent Token Floor** — `min(Reference, Market)`
   - 4.8 **TEJRC** — redemption value
   - 4.9 **Tokenized vs Tokenless** — table of which agents participate
   - 4.10 **Why Reference Values throughout** — scenarios table
5. **stUSDS** — **NEW** — see §5 of this plan for content sketch
6. **The Folio** — entry point; link to `synomic-entities/folio.md` for entity spec
7. **Agent-Internal Growth Staking** — Prime/Halo treasuries; double-counting paradox
8. **Incentive Effects** — capital flow, ecosystem alignment, segmentation
9. **Anti-Gaming** — Reference Valuation as primary defense; hollow-agent monitoring
10. **Synlang Form** — **NEW** — see §6 of this plan for content sketch
11. **Phase 1 Carve-Outs** — **NEW** — see §7 of this plan for content sketch
12. **Open Items** — trim source's "Open Design Questions" against decisions baked in
13. **File map** — cross-refs to active corpus

---

## 5. New §5 "stUSDS" — content sketch

```
stUSDS is a Morpho-pool-style lending product that creates a borrow surface
for growth stakers and a yield surface for USDS holders.

Two sides:
| Side | Action | Mechanics |
|---|---|---|
| Depositor | Deposits USDS, receives stUSDS shares | ERC-4626-like; share price reflects accrued interest |
| Borrower | Posts eligible collateral, draws USDS at variable rate | Morpho-pool utilization-based rate model |

Eligible collateral (open: confirm in writeup): growth assets in the
borrower's folio (Agent governance tokens, TEJRC) plus staked SKY.
Borrowing supports leveraged growth-asset accumulation — borrowers use
the proceeds to acquire more GF-eligible assets, raising their staking
factor.

Rate model:
  Borrow Rate = Base Rate + Spread(utilization)
  Lender Rate = (Spread × 0.90) × utilization        ; 90% to depositors
  Sky Core Fee = (Spread × 0.10) × utilization × notional   ; 10% to Sky Core

The Sky Core fee enters SKY Reference Value as a Core revenue line
(see §4.2).

Eligibility:
- stUSDS itself is EXCLUDED from growth-asset eligibility — it's a passive
  yield wrapper for the depositor and doesn't count toward staking factor.
- Other Generators (multi-Generator future) follow the same pattern:
  staked variants of each Generator's primary asset (e.g., stEURS) are
  excluded by the same rule.
```

**Open in writeup, not in plan:** exact collateral set, liquidation mechanics, base-rate reference (USGE base rate vs Sky Savings Rate). Mark these "(open)" in the new doc; don't block on them.

**Do not write a smart-contract spec for stUSDS in this migration.** A future `smart-contracts/stusds.md` can be promoted later if needed.

---

## 6. New §10 "Synlang Form" — content sketch

Mirror the shape of `accounting/duration-allocation.md` §11. Atom shapes, where atoms live, what synserv computes, what's sudo at Phase 1.

```
### Where parameters live
- &core-framework-valuation                         ← NEW Space
    (base-pe $value)                                ; global Base P/E
    (pe-modifier $stream $value)                    ; per-income-stream
    (pe-variance $stream $value)
    (growth-score-target $stream $value)            ; for linear-with-caps mapping
    (growth-factor agent-governance 25)             ; GF 2.5× (×10 for int math)
    (growth-factor tejrc 17)                        ; GF ~1.67×
    (forfeit-target tmf-waterfall)                  ; decision 4

- &core-framework-fee                                ; existing
    (stusds-sky-core-share 10)                      ; 10% of borrower spread

### Where derived values land
- &entity-{type}-{id}-root
    (reference-value $entity $value $epoch)         ; per-agent RefValue
- &entity-folio-{id}-root
    (staking-factor $folio $value $epoch)           ; per-folio
    (gf-portfolio-value $folio $value $epoch)
- &core-settlement
    (epoch-staking-rewards-paid $amount)
    (epoch-staking-rewards-forfeited $amount)       ; flows to TMF

### What synserv computes (in-space calculation per beacon-framework.md §4)
1. Per epoch: trailing-T12M revenue per income stream, per agent
2. Per epoch: growth score = clamp(actual / target × 100, 0, 100)
3. Per epoch: actual P/E per stream via the formula in §4.1
4. Per epoch: Reference Value per agent (per-agent formulas in §4.3-§4.6)
5. Per Folio per epoch: GF-adjusted portfolio value
6. Per Folio per epoch: staking factor = min(1, GF value / staked SKY RefValue)
7. Per Folio per settlement: rewards paid = base yield × staked × factor
8. Per epoch global: forfeited = (1 - factor) × base yield × staked, summed
   → emitted to &core-settlement for TMF aggregation

### Phase 1 carve-outs
- All P/E params, Modifiers, Variances, growth-score targets sudo-set at genesis
- Trailing revenue figures: insyn for active synomic Primes, exsyn-oracle for
  legacy core vaults / PSM during transition (per phases-ideas.md insyn/exsyn pattern)
- Hollow-agent monitoring deferred (no rule atoms in v1)
- stUSDS borrow rate: governance-set in v1, becomes utilization-driven in
  later phase
```

---

## 7. New §11 "Phase 1 Carve-Outs" — content sketch

Short — just the bullet list above plus a note that growth staking activates after Phase 1 (deferred per `phases/README.md` table). Confirm phase placement during writeup; if it's earlier than I'm assuming, adjust.

---

## 8. Vocabulary translation

Apply during the swap. Include this table at the top of the new doc as a "translation note" for readers coming from pre-synlang material.

| Pre-synlang | Post-synlang | Notes |
|---|---|---|
| SGA | USDS | Generator-issued asset; v1 has one Generator (USGE) |
| sSGA | sUSDS | savings token |
| srSGA | srUSDS | Generator senior risk capital |
| ESRC | srUSDS | merged into srUSDS naming |
| stSCST | stUSDS | the lending product per decision 1 — re-specified |
| SCST spread / duration / risk-fee | Sky Core revenue (Generator pass-through + stUSDS spread) | route to SKY Core revenue line items in §4.2 |
| Folio Agent | Folio | already migrated in `synomic-entities/folio.md` |
| Sky Agents | Synomic Agents / Synomic Entities | match `synomic-entities/` |

Sweep the source doc top-to-bottom; the mechanical part is straightforward. Watch for stale paths in the existing "Related" / "See" links — replace with active equivalents:
- `sky-agents/folio-agents/agent-type-folios.md` → `synomic-entities/folio.md`
- `sky-agents/halo-agents/agent-type-halos.md` → `synomic-entities/halo-classes.md`
- `sky-agents/agent-creation-restructuring/` → `synomic-entities/creation-restructuring.md`

---

## 9. Active-corpus updates (cross-reference sweep)

After `growth-staking/growth-staking.md` is in place, update these files. Each is a small surgical edit.

| File | Change |
|---|---|
| `README.md` (top level) | Add `growth-staking/` row to Active table; remove from Inactive note in §"Repo Layout"; add to Key Documents if appropriate |
| `synomic-entities/folio.md` | §"Growth Staking" body link `inactive/...growth-staking.md` → `../growth-staking/growth-staking.md`; same in file-map (2 spots) |
| `synomic-entities/creation-restructuring.md` | File-map entry: same link swap |
| `synomic-entities/core-controlled.md` | Add link to `../growth-staking/growth-staking.md` from "Excluded from Growth Staking" row |
| `synomic-entities/recovery.md` | Same as core-controlled.md |
| `synomic-entities/README.md` | Add `../growth-staking/` to Related list |
| `synomic-entities/prime.md` | Add a 1-paragraph stub §"Reference Value" linking to `../growth-staking/growth-staking.md#prime-reference-value` |
| `synomic-entities/generator.md` | Same stub, link to `#generator-reference-value` |
| `synomic-entities/guardian.md` | Same stub, link to `#guardian-reference-value` |
| `synomic-entities/halo-classes.md` | Same stub, link to `#halo-reference-value` |
| `accounting/settlement-cycle.md` | Add a §"Growth staking distribution" — 1 paragraph + cross-ref. Forfeited rewards flow to TMF aggregation in `&core-settlement` |
| `phases/phase-1-spaces.md` | Add a one-line note in carve-outs: growth staking activates post-Phase-1; P/E params sudo-set if needed earlier |

---

## 10. Don't-touch list

- `inactive/pre-synlang/growth-staking/` source files — leave as historical record
- The risk-framework — growth staking is orthogonal to TRRC math; do not touch `risk-framework/` files
- `accounting/capital-stack.md` — TRC structure is separate; do not edit
- LCTS / NFAT specs — unaffected by this migration
- Any `noemar-synlang/` files except as cross-ref targets

---

## 11. Execution order

1. Read all of §1 context
2. Verify decisions in §2 still hold (ask user if anything looks ambiguous)
3. Create `growth-staking/` directory
4. Write `growth-staking/README.md` (small index, mirror style of `accounting/README.md`)
5. Write `growth-staking/growth-staking.md` per outline §4, with content sketches §5–§7 and vocab swap §8
6. Sweep the cross-refs per §9
7. Verify by `grep -rn 'inactive/pre-synlang/growth-staking'` — should now appear only in `inactive/` itself
8. Read top-level `README.md` after edits to confirm directory tables look right

---

## 12. Estimated size after execution

- `growth-staking/README.md`: ~30 lines
- `growth-staking/growth-staking.md`: ~400 lines (source ~316 + stUSDS section + synlang section + phase-1 section, minus dropped open questions)
- 12 active files touched with surgical edits

---

## 13. Things to mark "(open)" in the new spec, not in this plan

These are real open questions the writeup should preserve, but they don't block execution:

- stUSDS exact collateral set (Prime tokens? TEJRC? Staked SKY? All of them?)
- stUSDS liquidation mechanics
- stUSDS base-rate reference (which rate is "base" — USGE base rate vs SSR vs other?)
- Hollow-agent synomic monitoring rule shapes
- Reference Value divergence handling (extreme market vs reference gaps)
- Measurement timing (snapshot vs time-weighted)
- New-Agent zero-RefValue handling

Carry these forward as `(open)` lines in the writeup so the next governance pass has a clean to-do list.

---

## 14. Sanity checks before declaring done

- [ ] `grep -rn 'inactive/pre-synlang/growth-staking' laniakea-docs/` — should match only inside `inactive/` itself
- [ ] No occurrence of `SGA`, `SCST`, `Folio Agent`, `Sky Agents`, `ESRC` in the new doc
- [ ] `growth-staking/growth-staking.md` references resolve (`folio.md`, `prime.md`, etc.)
- [ ] Top-level README's directory tables show `growth-staking/` under Active
- [ ] All 5 decisions in §2 are concretely reflected in the writeup
