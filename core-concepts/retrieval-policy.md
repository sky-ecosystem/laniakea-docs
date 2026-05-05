# Retrieval Policy

> Five invariants governing how embodiments query the probabilistic mesh — authority hierarchy, risk-gated authority, evidence feedback, dreamer/actuator parity, and audit trails.

**Also known as:** retrieval invariants, decision policy, query invariants

## Definition

The retrieval policy defines the constraints that govern how embodiments query the probabilistic mesh. It separates invariants (must hold, cannot be violated by RSI) from principles (guide optimization) from degrees of freedom (RSI evolves these freely). The five invariants are:

1. **Authority hierarchy exists** — synart > telart > embart; this ordering cannot be inverted or bypassed
2. **Risk determines minimum authority** — high-risk decisions cannot be made on low-authority knowledge alone
3. **Evidence flows back** — decisions and outcomes must be capturable as evidence; no black-box decision-making
4. **Same policy logic for actuators and dreamers** — strategies evolved in dreams must transfer to reality
5. **Audit trail for high-stakes decisions** — what was queried, what authority was consulted, what decision was made, what outcome occurred

Any self-improvement that weakens these invariants is cancer-logic by definition.

## Key Properties

- Invariants constrain; principles guide; degrees of freedom are for RSI to evolve
- "Cheapest sufficient evidence" — don't over-query; if low-authority knowledge suffices for a low-risk decision, use it
- Conflicts resolve upward — when patterns at different authority levels conflict, higher authority wins
- Dreamarts may constrain what data is available, but not how the policy reasons
- RSI freely evolves: query algorithms, caching strategies, risk classification, cost models, prefetching heuristics
- The framework holds the system together; RSI makes it better

## Relationships

- **constrains:** [probabilistic-mesh](probabilistic-mesh.md) — governs how the mesh is queried
- **implements:** [artifact-hierarchy](artifact-hierarchy.md) — authority hierarchy in retrieval follows synart > telart > embart
- **defends-against:** [cancer-logic](cancer-logic.md) — an embodiment that violates retrieval invariants is misaligned by definition
- **enables:** [rsi](rsi.md) — degrees of freedom are explicitly the search space for RSI optimization
