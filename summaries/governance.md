# Governance

**Status:** mostly target — SpellCore + SpellGuard layered model is the post-transition design. Phase 1 v2 reality has authority fully sudo at genesis (no Core GovOps role yet, Guardian holds everything), so the dual-key cascade and SKY freeze/override surfaces described here activate as governance hands off from sudo. Quarterly Council rotation, incentive-enforced passthrough voting, and BEAM-level freeze are constitutional design.
**Canonical home:** `laniakea-docs/governance/`

---

## TL;DR

Governance describes the practical voting and ratification surface that humans and token holders actually touch. Spells flow top-down through three layers — **SpellCore** (Core Council, 24 Guardians, 16/24 hat), **Prime SpellGuard** (core payload + Prime token hat), **Halo SpellGuard** (prime payload + Halo token hat) — with **dual-key authorization** at every layer below SpellCore. Below those, freeze/cancel/override is graduated by holder mass: SKY holders can freeze SpellCore at minority and *dismiss* the entire Council at full quorum (the constitutional fail-safe); Prime/Halo token holders can freeze and cancel spells but cannot dismiss anyone. The Council itself is rotated quarterly by SKY-holder polls (6 seats per quarter, full cycle 4 quarters), with passthrough voting from agent token holders to the SKY position and growth-staking-reward forfeiture as the participation enforcement. BEAMs sit adjacent to spells: any single Guardian can freeze any BEAM instantly (rogue/compromise response), with 16/24 mutual-freeze as the anti-paralysis backstop.

## Section map

| § | Topic |
|---|---|
| §1 | Three-layer spell cascade (SpellCore → Prime SpellGuard → Halo SpellGuard) |
| §2 | Core Council composition and rotation |
| §3 | Passthrough voting and incentive enforcement |
| §4 | SKY holder freeze and override |
| §5 | Per-level freeze and cancel |
| §6 | BEAM-level freeze and mutual-freeze backstop |
| §7 | Force override |
| §8 | Ratification thresholds + legacy mapping |

---

## §1 — Three-layer spell cascade

```
SpellCore (Core Council Guardian vote, 16/24 hat)
    │  SKY holders: freeze / override
    ▼  core spell payload
Prime SpellGuard  (Prime token hat + core payload)
    │  Prime holders: freeze / cancel; can only trigger Halo spells
    ▼  prime spell payload
Halo SpellGuard  (Halo token hat + prime payload)
       Halo holders: freeze / cancel; arbitrary execution within bounded surface
```

**SpellCore** replaces the legacy SKY-driven Executive Vote. Voting tokens are **Core Council Guardian tokens, not SKY**; a core spell hats at **16/24** Guardians. SpellCore is intentionally narrow — the constitutional aperture between the human/governance layer and the machine layer. It controls: setting the Council Beacon (roots all on-chain authority), overriding BEAM ownership in emergencies, setting Synome write rights, providing the core payload that Prime SpellGuards require, modifying Council composition (bounded by quarterly rotation), and force-override on Primes/Halos. Operational mechanics (rate-limit changes, init approvals, relayer assignments) happen further down the BEAM cascade and require specific BEAM grants — *not* SpellCore spells.

**SpellGuards** (Prime, Halo) extend the legacy StarGuard subspell-parking pattern with freeze/cancel and a **dual-key** requirement: top-down payload from the layer above, plus bottom-up token hat from that layer's own holders. Neither alone suffices.

| SpellGuard | Payload required | Hat required | Scope |
|---|---|---|---|
| Prime SpellGuard | Core spell payload pointing to this Prime spell | Prime token holder majority | Can only trigger Halo spells (Prime state locked by Laniakea factory) |
| Halo SpellGuard | Prime spell payload pointing to this Halo spell | Halo token holder majority | Arbitrary execution within Halo's bounded surface |

Why "Prime state locked": Primes are produced by the Laniakea factory (target architecture, Phases 5–8) with their internal state immutable post-instantiation; the only thing a Prime spell can do is trigger Halo spells beneath it.

## §2 — Core Council composition and rotation

| Property | Value |
|---|---|
| Council size | 24 Guardians |
| Hat threshold | 16/24 (2/3 supermajority) |
| Voting tokens | Core Council Guardian tokens |
| Rotation cadence | Quarterly |
| Seats rotated | 6 of 24 (full cycle every 4 quarters) |
| Rotation mechanism | Direct SKY-holder polls (not SpellCore spells) |
| Implementation | Council enacts the poll result in next regular SpellCore spell |

**Self-modification.** The Council uses SpellCore to modify its own membership (add/remove/replace Guardians) via regular spells subject to 16/24. Self-modification is bounded by SKY-holder freeze/override and by quarterly rotation.

**Rotation anchor.** Rotation is anchored to **SKY holders**, not the sitting Council. Even with the 16/24 hat, the Council cannot block a quarterly seat poll — only execute its result. This is the structural guard against Council entrenchment.

## §3 — Passthrough voting and incentive enforcement

**Passthrough voting.** Prime, Generator, Halo, and Folio token holders whose agents hold SKY must pass votes through (`agent-token holder → agent's SKY position → quarterly poll`). Structural reason: without passthrough, agents holding large SKY balances could either abstain (no representation for their holders) or vote unilaterally (no agency for their holders).

**Incentive enforcement.** Failure to vote in quarterly polls means **no growth staking rewards** for the failing token holder — economically enforced, not legally required. Compounds against passive holding. Growth staking activates post-Phase-1 (`growth-staking/`).

## §4 — SKY holder freeze and override on SpellCore

SKY holders no longer trigger spells under the post-transition model — that role passes to the Core Council. SKY holders retain ultimate sovereignty through a **graduated response** on SpellCore:

| SKY opposition level | Effect |
|---|---|
| Tiny minority against | Freeze for a few hours |
| Larger minority against | Freeze for a few days |
| Full quorum | **Override** — entire Core Council dismissed |

**Override consequences.** At full-quorum override, all 24 Guardians are dismissed; governance reverts to direct SKY control, which can then either pass spells directly (legacy MakerDAO model) or select a new Council. The asymmetry — freeze at tiny minority, override at full quorum — means disagreement freezes the system but only broad consensus dismisses the Council. Constitutional fail-safe, not a routine lever.

## §5 — Per-level freeze and cancel

At Prime and Halo levels the response is **freeze-then-cancel** rather than freeze-then-override.

| Mechanism | Where | Effect |
|---|---|---|
| Freeze / Override | SpellCore only | Graduated freeze → Council dismissal at full quorum |
| Freeze / Cancel | Prime and Halo SpellGuards | Graduated freeze → spell fully cancelled (no entity dismissal) |

Constitutional reasoning: the Core level is the only level whose dismissal route exists, because it is the only level with constitutional authority over its parent (SKY holders). Prime/Halo levels have no constitutional authority over the Core, so there is no body to dismiss — only the offending spell.

## §6 — BEAM-level freeze and the mutual-freeze backstop

BEAMs (on-chain access cascade — `smart-contracts/configurator-unit.md`) sit adjacent to spell governance with their own freeze surface.

- **Individual Guardian freeze.** Any **single** Council Guardian can immediately freeze/cancel any BEAM (aBEAM/cBEAM/pBEAM). Emergency response — halt compromised or rogue ops instantly.
- **SKY holder freeze.** SKY holders can freeze BEAMs via the same graduated response as SpellCore freeze.
- **Anti-paralysis: mutual freeze.** A rogue Guardian could freeze everything; the backstop is **16/24** Guardians voting to revoke another Guardian's freeze/cancel ability.

**Asymmetry by design.** Halt threshold (any single Guardian) ≪ advance threshold (16/24) ≈ remove-blocker threshold (16/24). Always easier to stop than to advance or to remove someone trying to stop. Safety-favoring asymmetry.

## §7 — Force override (emergency)

The Core Council can **force spells on Primes (and by extension Halos) without the Prime/Halo token hat**, bypassing dual-key.

| Property | Value |
|---|---|
| Authority | Core Council via SpellCore |
| Scope | Push spells to any Prime or Halo without their token holder approval |
| Convention | Emergency use only — not exercised in normal operations |
| Backstop | SKY holders retain freeze/override on SpellCore itself |

Exists because the Council may need to act when Prime/Halo holders cannot coordinate in time, or when a Prime/Halo is acting against system interests. The SKY-holder backstop is what keeps it bounded.

## §8 — Ratification thresholds summary

| Action | Threshold | Time |
|---|---|---|
| SpellCore spell hatted | 16/24 Guardians | Per spell |
| SKY freeze on SpellCore | Tiny minority → larger minority | Hours → days |
| SKY override of SpellCore | Full quorum | Constitutional emergency |
| Prime SpellGuard hatted | Prime token majority + core payload | Per spell |
| Halo SpellGuard hatted | Halo token majority + prime payload | Per spell |
| Per-level freeze | Token-holder minority | Hours → days |
| Per-level cancel | Larger minority | Days |
| BEAM freeze (individual) | Single Guardian | Instant |
| BEAM freeze (SKY) | SKY graduated response | Hours → days |
| Revoke rogue Guardian freeze | 16/24 Guardians | Per vote |
| Quarterly Council rotation | SKY-holder poll | Quarterly |

Legacy mapping (briefly): Executive Vote → SpellCore (Guardian-token hat); StarGuard subspell parking → SpellGuards with dual-key + freeze/cancel; governance pause (GSM) → force override + mutual freeze. Full table in `spellguard.md`.

---

## Key vocabulary

- **SpellCore** — Top-level spell mechanism operated by the Core Council; replaces SKY-driven Executive Vote. Voting tokens are Core Council Guardian tokens.
- **SpellGuard** — Spell-parking + dual-key authorization mechanism at Prime and Halo levels. Extends legacy StarGuard.
- **Hat / hatted** — A spell is "hatted" when it has reached its threshold and can execute (16/24 at Core, token majority at Prime/Halo).
- **Dual-key authorization** — Each SpellGuard requires both a top-down payload (from layer above) and a bottom-up token hat (from its own holders).
- **Force override** — Core Council power to push spells through Primes/Halos without their token hat (emergency only).
- **Override (SKY)** — Full-quorum SKY response that dismisses the entire 24-seat Council. Distinct from "force override."
- **Passthrough voting** — Prime/Generator/Halo/Folio token holders pass votes through to the SKY position their agent holds, propagating to quarterly polls.
- **Council Beacon** — On-chain root of authority set by SpellCore; everything aBEAM/cBEAM/pBEAM derives from it (canonical: `smart-contracts/configurator-unit.md`).
- **Quarterly rotation** — 6 of 24 Council seats rotated each quarter via direct SKY-holder polls (full cycle: 4 quarters).
- **Mutual freeze** — 16/24 Council vote that revokes another Guardian's BEAM-freeze authority. Anti-paralysis against rogue Guardians.

## Cross-references

- `smart-contracts/configurator-unit.md` — On-chain BEAM cascade beneath the Council Beacon (aBEAM/cBEAM/pBEAM)
- `noemar-synlang/runtime.md` §3–§7 — Synlang-side cert and auth chain
- `synomic-entities/guardian.md` — Ozone (single operational Guardian) and Guardian rank specifics
- `macrosynomics/atlas-synome-separation.md` — Constitutional/operational split that grounds the governance surface
- `core-concepts/governance-window.md` — Governance regime context
- `synoteleonomics/recipe-marketplace.md` — Recipe marketplace governance (catalog curation, pricing levers)
- `growth-staking/` — Growth staking rewards (the lever incentive enforcement uses)

## File map

| File | What's in it that the summary doesn't have |
|---|---|
| `core-council-elections.md` | Specific framing of "self-modification" as Council using SpellCore on its own membership; explicit chain diagram for passthrough; explanation of why participation is "economically enforced rather than legally required" and how it compounds. Cross-links to `../macrosynomics/synomic-entities.md` for the rank hierarchy that situates Guardians among other Synomic Entity ranks. |
| `spellguard.md` | Full ASCII layer diagram with payload arrows; full legacy-vs-post-transition aspect-by-aspect comparison table; the explicit "Prime SpellGuard cannot modify Prime state — locked by Laniakea factory" note. |
| `voting-mechanics.md` | The three asymmetry-by-design rationales (freeze vs override, per-level vs Core, halt vs advance vs remove blocker); the constitutional reasoning for why Prime/Halo cancel doesn't dismiss any body; ASCII rogue-Guardian sequence diagram; references the Synomic Entity rank model when discussing which entities hold which voting rights. |
