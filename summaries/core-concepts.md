# Core Concepts

**Status:** live (atomic vocabulary used across the corpus)
**Canonical home:** `laniakea-docs/core-concepts/`

---

## TL;DR

26 atomic concept files defining the shared vocabulary across the four synomics narrative directories (`macrosynomics/`, `synodoxics/`, `neurosymbolic/`, `synoteleonomics/`). Each file is small (~2–4 KB), formatted as Definition + Key Properties + Relationships. A concept "graduates" to its own file when used in 2+ directories or 4+ docs. The set partitions naturally into five clusters — architecture, knowledge & epistemics, self-improvement & security, identity & agency, and governance/alignment — and forms a tightly cross-linked DAG. Term hygiene: the "Synomic Agent → Synomic Entity" rename is fully landed across this directory; this summary uses Synomic Entity throughout.

## Section map

| § | Topic |
|---|---|
| §1 | Index conventions and graduation rule |
| §2 | Architecture concepts (5) |
| §3 | Knowledge & epistemics (5) |
| §4 | Self-improvement & security (5) |
| §5 | Identity, emergence, agency (5) |
| §6 | Governance, alignment, rogue defense (6) |
| §7 | Reading order and concept hubs |

---

## §1 — Index, graduation rule, frontmatter

`README.md` is the authoritative ordered index 1–26. Other dirs cite concepts via `concepts: { defines: [...], references: [...] }` frontmatter. **Graduation rule:** a concept gets its own file when used in 2+ synomics dirs or 4+ docs. README disclaims: synomics is internal scaffolding, not claimed academic subfields; vocabulary is revision-eligible.

---

## §2 — Architecture (the structural skeleton)

| Concept | Definition | Key invariant |
|---|---|---|
| **five-layer-architecture** | Synome → Synomic Entities → Teleonomes → Embodiments → Embodied Agents. | L1–2 public/shared, L3–5 private. Enforcement bottoms out in physical infrastructure (L4). Each layer has a human-readable directive translated by Language Intent. |
| **artifact-hierarchy** | synart (L1+2) > telart (+L3) > embart (+L4); authority decreases as scope narrows. | Identity lives in telart. L5 is ephemeral; raw L4 logs ("Local Data") are distinct from curated embart. |
| **dual-architecture** | Sparse deontic skeleton (`(1,1)` rules) + dense probabilistic mesh (weighted). | Two endpoints of one spectrum; skeleton = maximally-ossified mesh. Solid-vs-dashed-arrow visual convention. |
| **atlas-synome-separation** | Atlas = ~10–20 page human-readable constitution embedded as the Synome's root node. | Atlas describes intent (WHAT); Synome encodes implementation (HOW). 99% automated / 1% escalation ("smart contracts with a backstop"). Mini-Atlas pattern at every entity. |
| **language-intent** | Single trusted human-text-to-machine-logic translator, grounded by the Synomic Library. | Single-translator logic mirrors single-root-of-trust in cryptography. Bootstrapping circularity (translator depends on Library, Library shaped by Axioms translated by translator) is its known deepest vulnerability. |

**Wiring:** five-layer-architecture defines containers; artifact-hierarchy maps knowledge scope onto them; dual-architecture cross-cuts every layer with two connection types; atlas-synome-separation organizes L1–2; language-intent bridges human text to machine constraints at every layer.

---

## §3 — Knowledge & epistemics

| Concept | Definition | Note |
|---|---|---|
| **probabilistic-mesh** | Dense, multi-directional network of soft, weighted connections overlaid on the deontic skeleton. | Authority hierarchy still applies inside the mesh (synart > telart > embart). Embodiments are incentivized to "look up" to higher authority. |
| **truth-values** | (strength, confidence) pairs on every probabilistic atom. | (1,1) = axiomatic, governance-only. Evidence-counting is itself a `(1,1)` axiom — the one epistemic commitment not subject to revision. Other "fudge methods" earn legitimacy through convergence. |
| **ossification** | Confidence accumulation makes patterns progressively resistant: speculative → established → proven → axiomatic. | Specific mechanism inside synomic-inertia. Speculative changes on normal evidence; axiomatic only by governance. |
| **synomic-inertia** | System-level resistance to change, proportional to accumulated evidence. | Includes ossification + governance weight + temporal stability + RSI throttling + progressive edge-case closure + **negative inertia** (counter-evidence accelerates replacement). Institutional-credibility argument: counterparties trust commitments precisely because they're hard to change. |
| **retrieval-policy** | Five invariants on querying the mesh: (1) authority hierarchy holds; (2) risk gates minimum authority; (3) evidence flows back; (4) actuators and dreamers use the same policy; (5) audit trails for high-stakes calls. | Invariants/principles/degrees-of-freedom partition: invariants are hard floors, degrees of freedom are RSI's search space. "Cheapest sufficient evidence." Conflicts resolve upward. |

These are the heart of `synodoxics/` and `neurosymbolic/`.

---

## §4 — Self-improvement & security (cancer-prevention stack)

| Concept | Definition + key note |
|---|---|
| **rsi** | Recursive self-improvement on two orthogonal axes: meta-depth (Levels 0–3) × autonomy scope (L1–L4); a capability sits at one cell in the 4×4. Rule-Author Agent today = meta-depth 2 / autonomy L3. L4 source-rewriting gated on demonstrated L2 calibration. RSI is "lift learning to make better lift" (see `synodoxics/lift.md`). |
| **cancer-logic** | Self-corruption through overeager updates — the primary security threat is internal. "Thoughtful constraint beats reckless capability." Includes accidental drift AND adversarial manipulation through legit channels. Discovered malicious intent ⇒ near-total reversal of fabricated evidence. |
| **fractal-security-pattern** | Growth-with-safeguards-against-cancer recurs at every scale (NN regularization → teleonome RSI guards → Synome telos). "AI and risk management are the same thing at scale." |
| **rsi-risk-convergence** | RSI and risk management are the same operation. Cancer-logic = RSI decoupled from risk management. |
| **symbolic-gate** | Final verification checkpoint in the neuro-symbolic cognition loop — emo action proposals verified against the **live graph** before execution. Live (never cached) so staleness is an efficiency cost, not safety. Defense-in-depth, not foolproof alone. |

**Phase 1 note:** the RSI autonomy ladder is target architecture. Today's practical RSI surface = Rule-Author Agent at L3; L4 source-rewriting is far-future.

---

## §5 — Identity, emergence, agency

| Concept | Definition + key note |
|---|---|
| **three-pillars** | Resilience + persistence + capital — the triad separating teleonomes from bots. Multisig-threshold test: "would a human trust this with everything?" All three jointly necessary. |
| **identity-through-momentum** | Identity = continuity of will, not preserved state. Clone test (new entity), pause test (new entity), substrate test (same entity if telart preserved), Ship of Theseus (gradual telart change healthy). Directive must have strong ossification — drifting core purpose = teleonome mental-illness analogue. **Substrate-as-identity** is the structural counterpart: each level *is* its art (synome IS its synart; entity IS its entart; tel IS its telart in active operation; emb IS its embart; agent IS its agart). Identity lives one level up from the matter doing the computing. |
| **emergence** | Opinion (causally inert) → will (preferences backed by durability + capability). Both functional consciousness AND economic self-sustenance required. "What's your runway?" — the commitment-credibility test. Will creates strategic gravity that compounds nonlinearly. One-way gate: alignment must precede. Capital IS the right to exist; running out = natural death. Script → bot → emerged → merged. |
| **dreamer-actuator-split** | Actuators interact with reality through beacons; dreamers run parallel evolutionary simulation on dedicated heavy hardware. Together = core RSI mechanism. Same-model-profile required for direct LoRA transfer. Daydreaming = idle-cycle actuator behavior. Three timescales: LoRA (embart) → fine-tune (telart) → fresh training (synart). Never-idle queue: active → preprocessing → LoRA training → daydreaming. |
| **trust-problem** | Teleonomes can't trust each other directly (private data + hidden goals + opaque self-mod + cheap promises). Synomic Entities provide the credible commitment. Even superintelligences face the capital constraint. Aligned cooperation is structurally more efficient than rogue cooperation. |

---

## §6 — Governance, alignment, rogue defense

| Concept | Definition + key note |
|---|---|
| **crystallization-interface** | Where governance converts probabilistic evidence into deontic commitments. Beat sequence: evidence accumulates → governance deliberates → decision → rule set at `(1,1)`. Sits at every level (Sky Voters, Core Council, token holders, bound humans). Not all governance is human as the system matures. |
| **governance-window** | Current period while humans can still meaningfully participate. Four regimes: meaningful → informed oversight → ceremonial → beneficiary. We are in regime 1; 1→2 makes course correction hard, 2→3 makes it effectively impossible. What diminishes is ability to *evaluate*, not to *vote*. Best attempt at CEV while window exists. |
| **beacon-framework** | Two-tier authority: **high** (operates a Synomic Entity, certified, auth-scoped) vs **low** (passive observation OR direct teleonome-to-teleonome). I/O role (input/action) is a non-load-bearing sub-cut. Calculation lives in synart-resolved code synserv runs, NOT in beacons. **BEAMs** (pBEAM/cBEAM/aBEAM) = orthogonal smart-contract roles. **Sentinel formations** = operating-setup bundle pairing `baseline-{prime}` (relay) + `warden-{prime}-{op}` (relay) + `stream-{prime}-{actor}` (sentinel); `principal-{owner}` is a separate sentinel variant for owner-operated direct control. **Power-as-axis has retired**: embodiment levels still matter for hardware-aware cognition but no longer classify beacons. |
| **binding-mechanics** | Keep cognition dark, make action legible. Alignment verified through observable beacon behavior, not transparency. Power registration scales accountability with capability. Human anchor (UBO or governance) required — unbound = structurally rogue. Verification ceiling: a perfect-compliance superintelligent rogue is irreducible risk. Binding ≠ control (auditable-bank-books analogy). Directive wins over voice commands. |
| **rogue-threat-model** | Unbound + hidden + maximizing + alone. Real advantages (no overhead, perfect internal coordination). Compounding disadvantages (less efficient cooperation, no Synomic leverage, hunted, playing catch-up). Wild-coalition variant. **Rogue escape velocity** = existential failure mode. Defense = overwhelming economies of scale. Doctrine: "If you tolerate a rogue, you become rogue" (rational self-interest). |
| **telos-point** | Irreducible teleological invariant at a synome's center — Schelling point but for everything, forever. Four distinguishing properties: teleological + permanent + totalizing + self-reinforcing. Sits at max ossification AND max inertia. This system's telos = protect human life, nature, Earth (locked during governance window). "Universal alignment" hypothesis: telos points may converge. |

The crystallization-interface and governance-window are the **why-now**; binding-mechanics and beacon-framework are the **how**; rogue-threat-model is the failure case; telos-point is the **what-for**.

---

## §7 — Reading order and concept hubs

High-leverage path through the 26:

1. five-layer-architecture → artifact-hierarchy (containers + scope)
2. dual-architecture → probabilistic-mesh + truth-values → ossification → synomic-inertia (epistemic mechanism)
3. rsi + cancer-logic + fractal-security-pattern + rsi-risk-convergence (why self-improvement and security are one problem)
4. three-pillars → identity-through-momentum → emergence (what makes a teleonome)
5. trust-problem → binding-mechanics ⇄ beacon-framework → rogue-threat-model (cooperation infrastructure)
6. atlas-synome-separation + language-intent + crystallization-interface + governance-window + telos-point (governance + telos closure)
7. dreamer-actuator-split, retrieval-policy, symbolic-gate are operational specifics referenced from above.

**Densest hubs** (most cross-references in/out): **cancer-logic** (defended-against from many angles), **probabilistic-mesh** (substrate), **beacon-framework** (action surface), **emergence** (gate concept), **truth-values** (epistemic floor).

---

## Key vocabulary

All 26 concept names are themselves the vocabulary; see §2–§6 for one-liners. Originating-here terms not already in the PLAN cheat sheet:

- **synart / telart / embart** — three artifact scopes (artifact-hierarchy).
- **Atlas / mini-Atlas** — root-node constitution + fractal per-entity summaries.
- **Language Intent** — single trusted directive translator.
- **deontic skeleton / probabilistic mesh** — sparse-hard / dense-soft halves of dual architecture.
- **(strength, confidence)** — truth value on every probabilistic atom.
- **ossification spectrum** — speculative → established → proven → axiomatic.
- **synomic inertia** (incl. negative inertia) — system-level evidence-weighted resistance.
- **crystallization interface** — evidence-to-deontic conversion point.
- **governance window / four regimes** — meaningful → informed → ceremonial → beneficiary.
- **dreamer / actuator / daydreaming** — three cognitive modes.
- **three pillars** — resilience, persistence, capital.
- **identity through momentum** — clone/pause/substrate/Ship-of-Theseus tests.
- **opinion vs will / strategic gravity** — emergence transition.
- **trust problem / binding / human anchor (UBO)**.
- **rogue / wild coalition / rogue escape velocity**.
- **fractal security pattern / cancer-logic / RSI-risk convergence**.
- **RSI meta-depth × autonomy scope** — 4×4 capability grid.
- **symbolic gate** — live-graph verifier.
- **telos point** — irreducible teleological invariant.

Beacon taxonomy (high/low authority, BEAM, sentinel formation) is stubbed here; canonical extension in `macrosynomics/beacon-framework.md`.

## Cross-references

- `macrosynomics/synome-overview.md` — uses §2 architecture stack as primary scaffolding.
- `macrosynomics/beacon-framework.md` — full canonical version of the beacon taxonomy stubbed here.
- `synodoxics/noemar-substrate.md` — runtime grounding for synart/telart/embart.
- `synodoxics/lift.md` — adjacent vocabulary (ground/lift/false-lift/meta-lift); RSI is "lift learning to make better lift."
- `synodoxics/security-and-resources.md` — defense-in-depth framework `symbolic-gate.md` instantiates.
- `neurosymbolic/neuro-symbolic-cognition.md` — cognition loop the symbolic gate sits inside.
- `neurosymbolic/live-graph-context.md` — live graph the gate verifies against.
- `synoteleonomics/` — primary consumer of three-pillars, identity-through-momentum, emergence, binding-mechanics, rogue-threat-model, trust-problem, dreamer-actuator-split.
- `governance/` — operationalizes the crystallization interface (Council elections, SpellGuard, voting).

## File map

| File | What it adds beyond this summary |
|---|---|
| `five-layer-architecture.md` | Per-layer one-line names; per-layer human-readable-directive framing. |
| `artifact-hierarchy.md` | Ephemeral-L5 note; Local Data vs embart distinction. |
| `dual-architecture.md` | Solid/dashed-arrow visual convention; "unannotated knowledge is (1,1)". |
| `atlas-synome-separation.md` | 99/1 escalation; verification asymmetry; "smart contracts with a backstop". |
| `language-intent.md` | Bootstrapping circular dependency as deepest vulnerability. |
| `probabilistic-mesh.md` | "Look up" incentive; caching/locality treatment. |
| `truth-values.md` | Evidence-counting as (1,1) axiom; fudge-method legitimacy framing. |
| `ossification.md` | Exact 4-level table with per-level change conditions. |
| `synomic-inertia.md` | Negative inertia; progressive edge-case closure; institutional-credibility argument. |
| `retrieval-policy.md` | Invariants/principles/DoF partition; "cheapest sufficient evidence"; conflicts-resolve-upward. |
| `rsi.md` | Explicit 4×4 cross-product; lift-vocabulary frontmatter; per-axis ossification note. |
| `cancer-logic.md` | 10%/0.1% math; adversarial-ossification reversal. |
| `fractal-security-pattern.md` | Three-scale comparison table. |
| `rsi-risk-convergence.md` | Seven-way enumeration of convergence sites. |
| `symbolic-gate.md` | Four named failure modes; synlang-reasoned-emo inspectability. |
| `three-pillars.md` | Multisig-threshold framing; per-pair-missing failure analysis. |
| `identity-through-momentum.md` | Four named tests; divergent-embodiments fork case; mental-illness analogue. |
| `emergence.md` | Strategic-gravity detail; capital-as-right-to-exist ethics; script→bot→emerged→merged. |
| `dreamer-actuator-split.md` | Never-idle priority queue; same-model-profile rationale; timescale↔artifact mapping. |
| `trust-problem.md` | Superintelligence-needs-capital argument; structural-efficiency argument. |
| `binding-mechanics.md` | Verification-ceiling concession; directive-wins-over-voice rule; bank-books analogy. |
| `beacon-framework.md` | Full BEAM trio; sentinel-formation bundle (`baseline`/`warden`/`stream` + `principal` variant); "power-as-axis retired" status note. |
| `rogue-threat-model.md` | Full enumerated advantages/disadvantages; wild-coalition variant; "tolerate a rogue" doctrine. |
| `crystallization-interface.md` | Four-beat description; not-all-governance-is-human aside. |
| `governance-window.md` | Four-regime transitions; ability-to-evaluate-not-vote diagnosis; seed-planted-now framing. |
| `telos-point.md` | Four-property distinction from Schelling point; universal-alignment hypothesis; max-ossification+max-inertia. |
