# Target Model: Guardians as Sole Alignment Conservers

The target governance model consolidates Facilitators, Aligned Delegates, and Guardians into a single alignment-conserver role: **Guardians**. Guardians absorb the interpretation duties of Facilitators and the governance participation of Aligned Delegates, while retaining their existing operational and collateral-backed accountability.

---

## Design Principles

1. **Single accountable role** — One role with unified authority and responsibility, eliminating coordination overhead between three separate roles
2. **Collateral-backed accountability** — All alignment-conserver functions backed by posted collateral, not just discretionary authority
3. **Synome-native** — A single role is simpler to encode in the Synome for autonomous operation
4. **Interpretation + execution unified** — The entity that interprets governance rules is the same entity that executes them, removing the interpretive bottleneck

---

## Consolidated Guardian Role

In the target model, Guardians perform all functions previously split across three roles:

| Function | Legacy Role | Target Role |
|----------|-------------|-------------|
| Interpret Atlas and Artifacts | Facilitator | Guardian |
| Create binding governance precedents | Facilitator | Guardian |
| Participate in governance votes | Aligned Delegate | Guardian |
| Receive delegated voting power | Aligned Delegate | Guardian |
| Execute privileged operations | Guardian | Guardian |
| Post collateral for accountability | Guardian | Guardian |
| Oversee operational compliance | Core Guardian | Guardian (Core) |

---

## Guardian Subtypes (Retained)

The Operational / Core distinction is preserved:

| Subtype | Role in Target Model |
|---------|---------------------|
| **Core Guardian** | Interprets Atlas (absorbing Facilitator role), oversees Operational Guardians, participates in governance (absorbing Delegate role), manages Core Council functions |
| **Operational Guardian** | Executes day-to-day operations within bounds set by Core Guardians, posts collateral, faces slashing |

Core Guardians gain the Facilitator's interpretive authority and the Aligned Delegate's governance participation. Operational Guardians remain focused on execution.

---

## Absorbed Facilitator Functions

Core Guardians absorb all Facilitator responsibilities:

| Facilitator Function | How Guardians Handle It |
|---------------------|------------------------|
| Atlas interpretation | Core Guardians interpret Atlas with same "Spirit of the Atlas" principle |
| Precedent creation | Interpretations documented as Guardian Action Precedents (replacing Facilitator Action Precedents) |
| Discretionary authority | Core Guardians exercise discretion when explicit guidance is absent — now backed by collateral |
| Governance Poll proposals | Core Guardians can propose Governance Polls |

**Key improvement:** Interpretation is now collateral-backed. A Core Guardian who interprets the Atlas in bad faith faces the same slashing and derecognition consequences as one who executes operations incorrectly.

---

## Absorbed Aligned Delegate Functions

Core Guardians absorb Aligned Delegate governance participation:

| Delegate Function | How Guardians Handle It |
|-------------------|------------------------|
| Receive delegated voting power | SKY holders delegate to Core Guardians via existing Delegate Contracts |
| Governance voting | Core Guardians vote on Governance Polls and Executive Votes |
| Ranked participation | Core Guardians ranked by delegated voting power (retaining L1-L3 structure) |
| Compensation | Budget allocations tied to governance activity (same mechanism) |

**Key improvement:** The entity that votes on governance decisions is the same entity accountable for executing them, closing the gap between governance intent and operational reality.

---

## Accountability Model

All alignment-conserver functions are now under a single accountability framework:

| Mechanism | Applies To |
|-----------|-----------|
| **Collateral posting** | All Guardian functions (interpretation, voting, execution) |
| **Slashing** | Incorrect interpretation, voting misalignment, execution failures |
| **Derecognition** | Permanent removal for severe misalignment (same escalation as current Aligned Delegate model) |
| **Guardian Accord** | Formal agreement defining scope, collateral, and derecognition conditions |

**Misalignment escalation (unchanged):**

| Breach | Consequence |
|--------|-------------|
| First mild breach | Warning, no substantial penalty |
| Second breach or severe first breach | Immediate derecognition (permanent) |

---

## Synome Integration

A single Guardian role simplifies Synome encoding:

| Aspect | Legacy (3 roles) | Target (1 role) |
|--------|-------------------|-----------------|
| Role registry | Three separate registries | Single Guardian registry |
| Authority mapping | Complex cross-role dependencies | Unified BEAM authority model |
| Precedent storage | Facilitator Action Precedents (separate) | Guardian Action Precedents (integrated) |
| Delegation tracking | Separate Delegate Contract mapping | Integrated with Guardian identity |
| Automation path | Must coordinate across roles | Single role → direct Sentinel integration |

---

## What Does NOT Change

- **Token holder sovereignty** — SKY holders retain ultimate governance power through Executive Votes
- **Delegation mechanism** — Delegate Contracts work the same way; only the recipient role changes
- **Root Edit Primitive** — Token holders still modify Agent Artifacts directly
- **Atlas supremacy** — The Atlas remains the constitutional governance document
- **Collateral/slashing mechanics** — Same accountability model, extended to cover interpretation and voting
