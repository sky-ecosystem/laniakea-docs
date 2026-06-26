# SpellGuard System: Validator Map + Clarifications Needed

**Type:** Questions / Clarifications Needed + Suggestions  
**Related Documents:**  
- `governance-transition/spellguard-system.md`  
- `governance-transition/council-beam-authority.md`  
- `governance-transition/transition-plan.md`  
- `smart-contracts/configurator-unit.md`  
- `legal-and-trading/sentinel-network.md`  
- `legal-and-trading/passthrough-halo.md`  

**Author Background:** Sky Spell Validator

---

## Purpose

This input document provides:
1. A **validator map** of the post-transition SpellGuard system and where verification responsibility shifts
2. A focused list of **clarifications needed** to make independent validation practical
3. **Recommended documentation additions** that are low-friction to merge

---

## 1. What Changes for Validators

### 1.1 Layered Spell Flow (Post-Transition)

```
SpellCore (Core Council Guardian hat, 16/24)
    │  core spell payload
    ▼
Prime SpellGuard (Prime token hat + core payload)
    │  prime spell payload
    ▼
Halo SpellGuard (Halo token hat + prime payload)
    │  arbitrary execution (Halo-level)
    ▼
Operational execution via BEAM hierarchy → PAUs
```

### 1.2 Authority Graph (Where Envelope Risk Lives)

The primary validator shift: the critical risk is increasingly **"what authority envelope did this SpellCore spell create"**, not only "what calls does this spell execute."

```
SpellCore → Council Beacon (HPHA) → aBEAMs → cBEAMs → pBEAMs → PAU execution
                │
                └── All Synome write rights originate here
```

A single SpellCore spell touching the Council Beacon can restructure all downstream operational authority. Under the legacy model, each spell's scope was largely self-contained. Under SpellGuard, authority is a graph — spells increasingly modify the graph and envelopes, while day-to-day operations occur inside the envelope.

### 1.3 Operator Taxonomy (A First-Class Nuance)

Not every Halo is operated by a Sentinel. This distinction matters for accountability and for correctly interpreting what "automatic operation" means in governance context:

- **Prime PAUs** are operated by **Sentinel formations** (`stl-base` / `stl-stream` / `stl-warden`) — continuous real-time control with discretionary intelligence
- **Many Halo-side mechanics** (e.g., LCTS processing via `lpha-lcts`, identity registry via `lpha-identity`) are operated by **LPHA beacons** — deterministic rule executors with no discretion

"Halo operator" and "Sentinel" are not interchangeable. SpellGuard documentation should make this explicit wherever automatic capital deployment or accountability for failures is described.

---

## 2. What Validators Need to Verify (High Level)

Three concurrent concerns apply to every SpellGuard spell:

1. **Payload chain correctness** — is each layer's payload actually authorized by the layer above, and can an independent reviewer confirm this on-chain?

2. **Scope lock enforcement** — when docs state "Prime SpellGuard cannot modify Prime state," what is the concrete mechanism, and how does a validator confirm it holds for a specific deployment?

3. **Safety control parameterization** — are freeze thresholds, cancel semantics, override conditions, and force-override behavior defined precisely enough for independent verification, or do they currently rely on convention?

---

## 3. Clarifications Needed

### 3.1 Payload References and Chain Verification

- What is the **format** of a SpellCore payload reference to a Prime spell — address, hash, spell ID, or tuple? Without a specified format, validators cannot independently verify payload chain correctness.
- What is the format of a Prime payload reference to a Halo spell?
- Where can validators read the authoritative payload pointer on-chain, and how do they recompute or confirm it?

### 3.2 Prime "Locked by Factory" Boundary

The SpellGuard document states Prime SpellGuard "can only trigger Halo spells (cannot modify Prime state — locked by Laniakea factory)." This is a critical invariant stated narratively. What is the mechanical boundary?
- A selector allowlist or denylist?
- Explicit prohibition on certain call types?
- Inability to mutate BEAM ownership paths?

What is the minimal set of facts a validator should check to confirm a specific Prime is correctly locked? For safe validation, it is strongly recommended this be specified technically — either as on-chain enforcement, or if documented as convention, with explicit controls and an audit procedure.

### 3.3 BEAMTimeLock Verification Basics

- How is a queued operation ID derived? The `salt` parameter in `configurator-unit.md` is part of this — its role in operation-ID uniqueness should be explicitly illustrated.
- A canonical worked example is needed: aBEAM grants cBEAM — showing operation ID derivation, scheduling, delay, and how a validator independently confirms the queued operation.

### 3.4 Freeze / Cancel / Override Semantics

The SpellGuard document uses qualitative phrasing — "tiny minority → hours," "larger minority → days," "full quorum → override." For safe validation, it is strongly recommended these thresholds be numeric before deployment — either enforced on-chain, or if left as governance convention, documented with explicit controls and a stated rationale. Open questions:
- What are the specific thresholds and durations?
- Who has unfreeze authority in each mechanism?
- What prevents a Guardian from freezing the system as leverage rather than emergency response? The anti-paralysis mechanism (2/3rds mutual freeze) addresses rogue Guardians but not good-faith poor judgment.
- Are freeze and cancel distinct final states (cancel irreversible; freeze temporary)? The contract behavior should make this explicit.

### 3.5 Force Override

Force override is described as "emergency use / by convention, not used in normal operation." This is the highest-risk underdocumented mechanism in the post-transition system. Two questions should be resolved in documentation:

**Enforcement model:** Is the intended design on-chain enforcement or a documented governance convention? Either may be acceptable — but the documentation should clearly state which, and if convention, what controls and logging accompany it. For safe validation, on-chain enforcement is strongly recommended.

**Interaction with SKY holder freeze:** If a SpellCore spell invokes force override, does the graduated SKY holder freeze mechanism still apply before execution? This determines whether SKY holder sovereignty is preserved in emergency scenarios and should be stated explicitly.

### 3.6 Transition Period Coexistence

The transition plan is criteria-gated with no fixed timeline, meaning legacy and new models may coexist:
- During Phase 1 dual-operation, which model governs execution — legacy Executive Votes or SpellCore? Is there a defined switchover point?
- How are in-flight governance actions handled if the system switches regimes mid-queue?
- If a Guardian Action Precedent contradicts an existing Facilitator Action Precedent during dual-operation, which takes precedence? The hierarchy should be explicitly stated.

### 3.7 Rate Limit Evaluation and TTS

The Sentinel Network document (`legal-and-trading/sentinel-network.md`) establishes that Maximum Damage = Rate Limit × TTS, with Required Risk Capital ≥ Rate Limit × TTS. Rate limit changes cannot be fully evaluated for Atlas compliance without reference to the current TTS of the formation's Warden set. Should rate limit spell evaluation formally require TTS disclosure alongside SORL compliance (20% per 18-hour hop; see `smart-contracts/configurator-unit.md`)?

### 3.8 Synome Write Right Recovery

The Council Beacon document notes that if the Council Beacon is frozen or the Core Council dismissed, Synome write access halts. What is the documented recovery path? This should not be left to inference.

---

## 4. Recommended Documentation Additions

Low-friction additions that would reduce validator error most immediately:

1. **Validator checklist sections** in `spellguard-system.md`, `council-beam-authority.md`, and `configurator-unit.md` — a concise list of what to verify for each action type at that layer.

2. **Two worked examples** in `configurator-unit.md`:
   - Example A: aBEAM grants cBEAM — operation ID derivation, timelock scheduling, delay, and independent verification steps
   - Example B: Emergency rate limit decrease to zero followed by staged SORL ramp — illustrating the fast-decrease / constrained-increase asymmetry in practice

3. **Operator taxonomy note** in `spellguard-system.md` — distinguishing Prime Sentinel formations from Halo LPHA keepers wherever automatic capital deployment or accountability is described

4. **Force override clarification box** in `spellguard-system.md` — intended enforcement model (on-chain vs. convention), required logging or precedent expectations, and interaction with SKY freeze/override

5. **Synome write right recovery pathway** in `council-beam-authority.md` — what happens when write access halts and how governance restores it

---

## 5. Legacy-to-New Verification Mapping

| Legacy Validator Focus | Post-Transition Equivalent | Why It Changes |
|------------------------|---------------------------|----------------|
| "What does this spell do?" | "What authority envelope did this spell create?" | Authority is now a layered graph; one spell can restructure all downstream operational authority |
| SubSpell validation (StarGuard) | Payload chain validation across SpellGuard layers | Must verify references across layers, not within one spell |
| Rate limit parameter checks | Rate limit + SORL compliance + TTS-adjusted Maximum Damage | TTS is now a required input to rate limit assessment |
| Contract authorization (`rely`/`deny`) | Council Beacon → aBEAM grant correctness | Traces through 4-level BEAM hierarchy |
| Emergency parameter zero-out | Instant aBEAM removal or individual Guardian BEAM freeze | Must verify which emergency path is appropriate and that timelock is correctly bypassed |
| Atlas alignment check | Atlas assertion → Synome constraint mapping | Must verify constraint exists in Synome, not only that human intent is satisfied |

---

*Submitted as an input document aimed at making the SpellGuard governance transition independently verifiable by Guardians and community reviewers. Corrections and engagement welcome.*
