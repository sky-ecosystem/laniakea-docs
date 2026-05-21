# Synomics: Retrieval/Crystallization Anti-Cancer Clarifications (Draft Input)

**Type:** Suggestions + Clarifications  
**Scope:** macrosynomics core concepts (retrieval, crystallization, cancer logic, fractal security pattern)  
**Goal:** Make invariants / interface behavior implementable without changing philosophy; reduce ambiguity around “contradiction reporting” vs “authority inversion”; add minimal auditability hooks.

---

## Summary

This input proposes small additions to the synomics docs to operationalize the “cognitive firewall”/“synomic immune system” framing already implied by:
- Retrieval Policy invariants (authority ordering, risk-gated authority, evidence feedback, parity, audit trails)
- Crystallization Interface (probabilistic → deontic bridge; governance at all levels)
- Cancer-Logic (internal self-corruption through overeager updates)
- Fractal Security Pattern (growth + safeguards recur at every scale)

Primary contribution: define a **non-punitive contradiction reporting path** and a **versioned synart amendment pipeline**, so legitimate emergent truths can be escalated safely without triggering false-positive containment—while preserving zero-trust of lower-authority knowledge in action.

---

## Proposed Additions

### 1) `macrosynomics/retrieval-policy.md`

**Target section:** Definition / Key Properties (near invariants #1–#5)  
**Proposed block (pasteable):**

#### Contradiction reporting is permitted (and not authority inversion)

An embodiment may observe patterns in **embart** that appear to conflict with higher-authority commitments in **synart** (axioms, definitions, rules). Reporting such contradictions upward through sanctioned channels is permitted and does **not** constitute authority inversion.  

Authority inversion occurs only when an embodiment **acts** as if low-authority knowledge overrides high-authority commitments (e.g., bypassing synart constraints, executing high-stakes actions based on embart-only beliefs, or promoting unvetted patterns as deontic rules).

This distinction is necessary to avoid auto-immune failure: the system must tolerate anomaly reporting while rejecting illegitimate authority escalation.

---

#### Audit trail minimum fields (for high-stakes decisions)

For decisions above the “high-stakes” threshold (risk classification is a degree of freedom), the audit trail MUST record, at minimum:

- **Decision class / risk class**
- **Embodiment identifier** (instance + embodiment)
- **Authority levels consulted** (synart/telart/embart) and retrieval ordering
- **Queried nodes / references** (IDs or content hashes) for each consulted authority level
- **Truth-values** (strength, confidence) for non-deontic evidence used
- **Constraint/invariant set checked** (IDs) and check outcome (pass/fail)
- **Action executed** (aperture invoked) and observed outcome reference
- **Language Intent version** (or ruleset hash) used to map commitments → invariants

The intent is not to expose cognition, but to make action legible and verifiable.

---

#### Invariant violation signals (guardian monitoring hooks)

Violations (or repeated near-violations) of retrieval invariants are indicators of cancer-logic risk. Examples include:

- Attempts to **invert/bypass** authority ordering (synart > telart > embart)
- Repeated attempts to justify high-stakes actions using **quarantined** or low-confidence evidence
- **Confidence inflation** without corresponding evidence diversity/time durability
- **Source monoculture** (single feed dominates evidence)
- **Self-reference loops** (recent outputs treated as independent evidence)
- Rising rate of **proof obligation failures** paired with repeated execution attempts

These signals are behavior-based and do not require interpreting latent reasoning.

---

### 2) `macrosynomics/crystallization-interface.md`

**Target section:** Key Properties (after “(1,1) truth values”)  
**Proposed block (pasteable):**

#### (1,1) indicates binding commitment, not metaphysical certainty

A crystallized rule with a (1,1) truth value is a **binding commitment for action** until amended through an appropriate governance pathway. This does not imply irrevisable truth. Amendments should be explicit, versioned, and subject to higher evidence burden than the original crystallization threshold.

---

#### Candidate rules and versioned amendments (Synart update pipeline)

To avoid cancer-logic and auto-immune failure, emergent patterns from lower-authority layers must not directly rewrite synart. Instead, the system uses a staged amendment pathway:

1. **Contradiction report (non-deontic):** A lower-authority observation can be raised as a contradiction to an existing commitment, with provenance and truth-values, explicitly marked “report-only.”
2. **Quarantined candidate node:** The proposed pattern is stored as a candidate rule in the probabilistic mesh, defaulting to **Speculative**. It may inform monitoring/simulation but cannot satisfy proof obligations for high-stakes actions.
3. **Replication & durability:** The candidate must survive cross-embodiment replication, source diversity checks, and time durability thresholds.
4. **Dreamer stress tests:** The candidate is tested in constrained/simulated settings to evaluate predictive utility and adversarial poisoning hypotheses, preserving actuator/dreamer parity.
5. **Axiom Patch Proposal (APP):** Governance produces a concrete proposal mapping “what changes” (commitment text) to “what enforces it” (invariant diff) via Language Intent.
6. **Versioned synart update:** Synart updates are applied as **explicit versions** (vN → vN+1) with clear effective time, blast radius notes, and rollback/override plan.

Containment is triggered by **premature deontic use** (acting as if the candidate is already binding), not by filing contradiction reports.

---

### 3) `macrosynomics/cancer-logic.md`

**Target section:** Definition / Key Properties  
**Proposed block (pasteable):**

#### Synthetic evidence feedback loops (metastasis pattern)

A high-risk cancer-logic mode is a **self-evidence feedback loop**:

1) A bad pattern enters the probabilistic mesh  
2) It influences decisions  
3) Decisions produce outcomes that are logged as “evidence”  
4) The evidence increases confidence in the bad pattern  
5) The pattern gains influence and spreads

This metastasis can occur without explicit external attack; it may also be induced by adversaries through evidence fabrication.

Defenses include: audit trails tying actions to cited evidence and invariants, cross-embodiment replication requirements for high-impact claims, and strict gating of when outcomes may be treated as independent evidence.

---

#### Non-punitive anomaly reporting vs authority inversion

Cancer-logic is defined by weakening invariants or bypassing governance. Reporting contradictions through sanctioned channels is not cancer-logic; **acting** as if lower authority overrides higher authority is.

This separation prevents auto-immune responses while maintaining strict enforcement against privilege escalation.

---

### 4) `macrosynomics/fractal-security-pattern.md`

**Target section:** Definition / Key Properties (after the table)  
**Proposed block (pasteable):**

#### Mapping the fractal pattern onto the five-layer architecture (example)

The “growth + cancer safeguard” operation can be expressed in the five-layer architecture:

- **Layer 5 (Embodied Agent):** growth via runtime optimization; safeguard via binding mechanics + proof obligations for high-power actions  
- **Layer 4 (Embodiment):** growth via local learning; safeguard via disposable embart + differential replication + key/infra isolation  
- **Layer 3 (Teleonome):** growth via RSI and telart evolution; safeguard via guarded write access + dreamer/actuator parity + ossification/inertia  
- **Layer 2 (Synomic Agents):** growth via policy evolution across agents; safeguard via bounded apertures + governance constraints + auditability  
- **Layer 1 (Synome):** growth via new commitments/invariants; safeguard via crystallization interface + versioned amendments + override/hard-fork capability

This mapping is illustrative; exact mechanisms may evolve, but the invariant requirement remains: growth cannot weaken cancer safeguards.

---

## Notes / Non-goals

- No new invariants are proposed; these additions clarify enforcement surfaces, audit requirements, and tolerance for contradiction reporting.
- No numeric thresholds are specified; risk classification and thresholds remain degrees of freedom for RSI/governance.
- These blocks are intentionally minimal to reduce design pushback and ease merging into core docs.

---
