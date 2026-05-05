# Legacy Alignment Conserver Model

> **Note:** This describes the pre-consolidation model. The current model uses a single Guardian role — see [target-model.md](target-model.md).

Sky governance previously operated with three distinct alignment-conserver roles. Each role had different authority, accountability mechanisms, and governance functions.

---

## Overview

| Role | Function | Accountability |
|------|----------|----------------|
| **Facilitator** | Interpret Atlas on behalf of Guardians | Discretionary authority; precedents documented |
| **Aligned Delegate** | Governance participation with delegated voting power | Ranked L1-L3; derecognition for misalignment |
| **Guardian** | Operate systems with collateral backing | Collateral slashing; Core Guardian oversight |

---

## Facilitators

Facilitators were the interpretive layer of Sky governance. They translated the Atlas and Agent Artifacts into actionable guidance for Guardians.

| Property | Value |
|----------|-------|
| Role | Authoritative interpretation of governance documents |
| Discretion | Broad authority when explicit guidance is absent |
| Documentation | All interpretations recorded as Facilitator Action Precedents |
| Key principle | "Spirit of the Atlas" — rules have underlying intent to serve human values |

**What Facilitators did:**
- Interpret Atlas rules when explicit guidance is absent
- Balance "letter of the rule" against true purpose
- Create binding precedents through documented interpretations
- Propose Governance Polls as recognized Ecosystem Actors

**Limitation:** Facilitators held interpretive authority but no direct operational power. They could not execute on-chain actions or deploy capital.

**Status:** Absorbed into Core Guardians. See [target-model.md](target-model.md).

Source: [Appendix A — Guardian Interpretation Framework](../whitepaper/appendix-a-protocol-features.md), [Appendix B — Guardian Interpretation Framework](../whitepaper/appendix-b-sky-agent-framework-primitives.md)

---

## Aligned Delegates

Aligned Delegates were anonymous Alignment Conservers who received delegated SKY voting power from token holders.

| Property | Value |
|----------|-------|
| Identity | Anonymous |
| Ranking | L1, L2, L3 — based on delegated voting power |
| Compensation | Budget allocations tied to voting activity |
| Accountability | Strict operational security and accountability requirements |

**Delegation mechanism:**
- SKY holders delegate voting power via Delegate Contracts
- Token custody remains with the delegator
- Delegation can be changed or revoked at any time

**Misalignment handling:**

| Breach | Consequence |
|--------|-------------|
| First mild breach | Warning, no substantial penalty |
| Second breach or severe first breach | Immediate derecognition (permanent) |

**Status:** Absorbed into Core Guardians. See [target-model.md](target-model.md).

Source: [Appendix A — Aligned Delegate System](../whitepaper/appendix-a-protocol-features.md)

---

## Guardians

Guardians are Synomic Agents that perform privileged operations with collateral backing. They are the operational backbone of Sky governance. Post-consolidation, they also handle interpretation and governance participation.

### Guardian Subtypes

| Type | Function | Accountability |
|------|----------|----------------|
| **Operational Guardian** | Day-to-day execution within defined bounds | Posts collateral; subject to Core Guardian oversight; slashing for failures |
| **Core Guardian** | Interpret Atlas, oversee Operational Guardians, govern | Accountable to Sky Governance; collateral-backed |

**Core Council** — the group of Core Guardians responsible for Sky Core operations. Holds aBEAM authority for PAU registration, init approval, and cBEAM grants.

### Guardian Lifecycle

1. **Registration** — Post collateral, register for role, receive authority
2. **Operation** — Perform privileged functions, maintain collateral, earn fees
3. **Exit** — Complete pending operations, wait for challenge period, reclaim collateral

### Guardian Accord

The formal agreement between an Agent and a Guardian defining:
- Roles, responsibilities, accountability
- Collateral/insurance requirements
- Derecognition conditions

Source: [Appendix B — Guardian Accord Primitive](../whitepaper/appendix-b-sky-agent-framework-primitives.md), [Guardian Agents](../sky-agents/guardian-agents/agent-type-guardians.md)

---

## How the Three Roles Interacted (Legacy)

```
Atlas (governance constitution)
    │
    ▼
Facilitators ──── interpret ───► Facilitator Action Precedents
    │                                      │
    │                                      ▼
    │                              Guardians (Core + Operational)
    │                                      │
    │                                      ├── execute operations
    │                                      ├── manage PAUs via BEAMs
    │                                      └── supervise Sentinels
    │
    ▼
Aligned Delegates ──── vote ───► Governance Polls / Executive Votes
    │
    └── receive delegated SKY voting power from token holders
```

**Key dependencies (legacy):**
- Facilitators interpret; Guardians execute based on those interpretations
- Core Guardians are accountable to Facilitators for Atlas alignment
- Aligned Delegates participate in governance votes but do not execute operations
- All three roles are subject to derecognition for misalignment

---

## Limitations of the Legacy Model

| Issue | Description |
|-------|-------------|
| **Role fragmentation** | Three separate roles create coordination overhead and unclear boundaries |
| **Interpretive bottleneck** | Facilitators must interpret before Guardians can act, adding latency |
| **Delegation indirection** | Aligned Delegates vote but cannot directly ensure operational alignment |
| **Accountability gaps** | Facilitator interpretive discretion lacks the collateral-backed accountability that Guardians have |
| **Automation friction** | Three-role model is harder to encode in the Synome for autonomous operation |
