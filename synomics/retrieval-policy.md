# Retrieval & Decision Policy

**Status:** Core architectural constraint
**Last Updated:** 2026-02-03

This document defines the **constraints and principles** that govern how embodiments query the probabilistic mesh. The specific algorithms and optimizations are degrees of freedom for RSI — what matters is that these invariants hold.

---

## Invariants (Must Hold)

These constraints cannot be violated. Any self-improvement that weakens these is cancer-logic.

### 1. Authority Hierarchy Exists

```
synart > telart > embart
```

Higher-authority knowledge is:
- More vetted (more evidence, more validation)
- More aligned (governance-approved)
- Safer to rely on (reduces penalty/slashing risk)

**This ordering cannot be inverted or bypassed.**

### 2. Risk Determines Minimum Authority

| Decision Risk | Minimum Authority |
|---------------|-------------------|
| Low | Embart may suffice |
| Medium | Telart required |
| High | Synart required |
| Existential | Synart + governance |

**High-risk decisions cannot be made on low-authority knowledge alone.**

The system may evolve how it classifies risk, but the constraint remains: risk level gates authority level.

### 3. Evidence Flows Back

Decisions and outcomes must be capturable as evidence that can flow back up:
- Embart observations can become telart proposals
- Telart patterns can become synart proposals
- No black-box decision-making that evades the evidence loop

**The mesh learns from what embodiments do.** Any optimization that breaks this feedback loop is forbidden.

### 4. Same Policy Logic for Actuators and Dreamers

Dreamers must use the same retrieval logic as actuators (even if operating on constrained/simulated data).

**Why:** Strategies evolved in dreams must transfer to reality. If dreamers use fundamentally different query logic, their discoveries may not work for actuators.

The dreamart may constrain *what data is available*, but not *how the policy reasons*.

### 5. Audit Trail for High-Stakes Decisions

High-risk decisions must be traceable:
- What was queried
- What authority level was consulted
- What decision was made
- What outcome occurred

**Why:** Accountability, debugging, alignment verification. The system cannot "forget" how it made important decisions.

---

## Principles (Guide Optimization)

These principles guide how RSI should optimize within the invariants.

### Authority vs Cost vs Risk

Every query involves a trade-off:
- **Authority** — Higher is safer but may be slower/costlier
- **Cost** — Lower is more efficient but may miss important patterns
- **Risk** — Higher stakes justify higher authority and cost

RSI optimizes this trade-off. The invariants constrain the solution space; the principles guide the search.

### Cheapest Sufficient Evidence

Don't over-query. If low-authority knowledge is sufficient for a low-risk decision, use it.

Resource discipline applies to queries too — unnecessary synart queries waste shared resources.

### Look Up When Uncertain

When lower-authority knowledge is ambiguous, conflicting, or insufficient — escalate to higher authority.

Uncertainty is a signal to seek more vetted knowledge.

### Conflicts Resolve Upward

When patterns at different authority levels conflict, higher authority wins.

Conflicts are also valuable evidence — they may indicate lower-level knowledge needs updating.

---

## Degrees of Freedom (RSI Evolves)

These are explicitly not constrained. RSI may evolve:

- **Query algorithms** — How to search, rank, retrieve patterns
- **Caching strategies** — What to cache locally, TTLs, invalidation
- **Risk classification** — How to assess decision risk (within the constraint that classification gates authority)
- **Cost models** — How to measure and optimize query costs
- **Logging granularity** — What to log for low-risk vs high-risk (within audit trail constraint)
- **Prefetching heuristics** — Anticipating what knowledge will be needed
- **Conflict resolution details** — How to surface, log, and learn from conflicts

The system gets smarter at retrieval over time. These docs don't specify how — they specify what must remain true as it does.

---

## Connection to Security and Resources

This policy is a **risk management mechanism**:

- Invariants are the "core logic circuits" that cannot be overridden
- Principles are the "alignment gradients" that guide improvement
- Degrees of freedom are the "safe search space" for RSI

An embodiment that violates the invariants is misaligned — regardless of how efficient or clever its retrieval became.

An embodiment that respects invariants but optimizes poorly is just inefficient — RSI will improve it.

**The framework holds the system together. RSI makes it better.**

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| `probabilistic-mesh.md` | The knowledge structure being queried |
| `synome-layers.md` | The artifact hierarchy (synart > telart > embart) |
| `security-and-resources.md` | Broader security principles this policy implements |
| `actuator-perspective.md` | How actuators apply this policy |
| `dreamer-perspective.md` | How dreamers apply this policy |
