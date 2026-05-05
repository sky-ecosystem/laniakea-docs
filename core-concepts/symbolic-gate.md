---
concepts:
  defines:
    - symbolic-gate
  references:
    - neuro-symbolic-cognition
    - cancer-logic
    - probabilistic-mesh
---

# Symbolic Gate

The symbolic gate is the final verification checkpoint in the neuro-symbolic cognition loop. Every action proposal from the emo (embodied orchestrator) must pass through the symbolic gate before becoming a real-world action.

---

## Canonical Definition

**Input:** An action proposal produced by the emo's neural reasoning, plus the current live graph state.

**Operation:** The symbolic system verifies the action proposal against the **live graph** (not the emo's possibly-stale context). Verification checks include:
- Do the premises the emo reasoned from still hold in the live graph?
- Does the proposed action comply with deontic constraints (axioms, rate limits, authority scope)?
- Is the evidence chain supporting the action genuine and sufficient?

**Output:** Either the action proceeds to execution, or it is rejected (bounced) and the emo re-reasons with fresh context.

**Failure modes:**
- **Stale premises** — the graph changed between reasoning and gating; the action is bounced, not dangerous (efficiency cost, not safety cost)
- **Cancer-logic bypass** — a sufficiently clever emo could learn to game the verifier; defense-in-depth (not the gate alone) prevents this
- **Verifier bugs** — flawed gate logic could pass invalid actions; mitigated by the gate itself being subject to evidence dynamics and RSI
- **Authority scope errors** — the gate enforces the wrong constraints; mitigated by deontic skeleton being governance-crystallized and auditable

---

## Key Properties

| Property | Description |
|----------|-------------|
| **Always checks the live graph** | Never a cached view — ensures staleness is an efficiency problem, not a safety problem |
| **Defense-in-depth layer** | One layer of protection against cancer-logic, not foolproof on its own |
| **Inspectable** | Because the emo reasons in synlang, failed gate attempts produce structured evidence — both for improving the gate and for detecting alignment drift |
| **Primary real-time safety layer** | Within the cognition loop, the gate is the boundary between reasoning and reality |

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| [`../neurosymbolic/neuro-symbolic-cognition.md`](../neurosymbolic/neuro-symbolic-cognition.md) | The cognition loop the gate operates within — emo sandboxed inside symbolic verification |
| [`../neurosymbolic/live-graph-context.md`](../neurosymbolic/live-graph-context.md) | Live graph binding — the gate always verifies against live state, making staleness safe |
| [`../neurosymbolic/cognition-as-manipulation.md`](../neurosymbolic/cognition-as-manipulation.md) | The emo's reasoning process that produces action proposals the gate verifies |
| [`../synodoxics/security-and-resources.md`](../synodoxics/security-and-resources.md) | Defense-in-depth security framework the gate implements |
| [`cancer-logic.md`](cancer-logic.md) | The primary threat the gate defends against — self-corruption through overeager updates |
