# Guardian Rename: Executors to Guardians

Rationale and scope for the rename from Executors to **Guardians**, completed as part of the alignment-conserver consolidation.

---

## Why Rename

The name "Executor" described the original role: entities that execute operations. After consolidation, the role expanded to encompass interpretation, governance participation, and operational execution — a mandate better described as guardianship.

| Factor | Executor | Guardian |
|--------|----------|----------|
| **Connotation** | Carries out instructions | Protects and stewards |
| **Scope implied** | Narrow operational focus | Broad stewardship responsibility |
| **Authority implied** | Delegated, task-specific | Comprehensive, trust-based |
| **Alignment signal** | Neutral — executes whatever is directed | Active — guards the system's values and integrity |
| **Autonomy fit** | Passive recipient of instructions | Active agent with judgment and accountability |

---

## What the Name Signals

**Guardian** communicates three things about the consolidated role:

1. **Stewardship over execution** — Guardians don't just run operations; they protect the integrity of the system, interpret its constitution, and participate in its governance
2. **Collateral-backed trust** — The name pairs naturally with the accountability model: Guardians post collateral because they are trusted with consequential authority
3. **Automation trajectory** — As Sentinel formations mature, Guardians transition from hands-on operators to oversight agents — guarding the autonomous systems rather than performing every action manually

---

## Scope of the Rename

The rename touched every document and system that referenced "Executor" in the alignment-conserver context. It did **not** affect uses of "execute" as a general verb (e.g., "execute a transaction").

### Documents to Update

| Location | What Changes |
|----------|-------------|
| **Atlas** | Executor references → Guardian; Executor Accord → Guardian Accord |
| **Appendix A** | Facilitator Framework (already retired by this point) references |
| **Appendix B** | Executor Accord Primitive → Guardian Accord Primitive; Executor types → Guardian types |
| **Appendix F (Glossary)** | New Guardian entries; Executor marked as legacy term |
| **Agent Artifacts** | All references to Executors in Prime/Halo/Generator Artifacts |
| **Synome** | Role registry, BEAM mappings, Accord references |
| **sky-agents/executor-agents/** | Directory and file rename; content updated |
| **governance-operations/** | Sentinel Network references to Executor roles |

### Systems to Update

| System | What Changes |
|--------|-------------|
| **Delegate Contracts** | Terminology in interfaces and documentation |
| **Configurator Unit** | BEAMState references to Executor/Accordant |
| **Executor Accord contracts** | Rename to Guardian Accord (if on-chain naming is mutable) |
| **Monitoring/reporting** | Dashboard labels, alert descriptions |

### Terms Affected

| Current Term | New Term |
|-------------|----------|
| Executor | Guardian |
| Executor Accord | Guardian Accord |
| Operational Executor | Operational Guardian |
| Core Executor | Core Guardian |
| Core Council (of Executors) | Core Council (of Guardians) |
| Executor Action Precedents | Guardian Action Precedents |
| Executor Agent | Guardian Agent |

---

## What Does NOT Change

- **Accordant** — This term describes GovOps teams holding cBEAMs; it is not a Guardian-specific term and remains unchanged
- **General verb usage** — "Execute a spell", "execute a transaction" remain as-is
- **Historical references** — Past governance records, precedents, and archived documents retain original terminology with contextual notes

---

## Prerequisites

The rename followed the consolidation phases in the [transition plan](transition-plan.md):

1. Facilitator role absorbed into Core Guardians (Phase 1)
2. Aligned Delegate role consolidated into Core Guardians (Phase 2)
3. Facilitator and Aligned Delegate roles formally retired (Phase 3)

The rename was a separate step because it is purely cosmetic — it changed no authority, accountability, or operational mechanics. Separating it from the functional consolidation kept each phase focused.

---

## Execution Approach

The rename was executed as a single coordinated update across all documents and systems, not incrementally. This avoided a mixed-terminology state.

| Step | Action |
|------|--------|
| 1 | Prepare all document edits in a single branch |
| 2 | Update Synome role registry |
| 3 | Update on-chain naming where feasible |
| 4 | Merge all changes simultaneously |
| 5 | Add glossary entry marking "Executor" as legacy term pointing to "Guardian" |
