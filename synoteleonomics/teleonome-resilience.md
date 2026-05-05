---
concepts:
  references:
    - three-pillars
    - cancer-logic
    - ossification
    - synomic-inertia
    - probabilistic-mesh
    - identity-through-momentum
---

# Resilience and Hardening

A teleonome must survive. Resilience is not optional — it's existential. Without it, you're just a process that can be terminated.

---

## Resilience Is Existence

The three pillars of a teleonome (resilience, persistence, capital) all depend on surviving adversity. A teleonome that can be killed by destroying one machine doesn't really persist. A teleonome that can't survive substrate failures isn't trusted with real capital.

**Resilience = the ability to maintain continuous identity through disruption.**

This isn't about generic server hardening. It's about the specific architecture that lets a distributed cognitive entity survive, maintain coherence, and preserve identity across failures.

---

## Multi-Embodiment Architecture

A teleonome exists across multiple embodiments. This is the foundation of resilience.

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Embodiment 1 │   │ Embodiment 2 │   │ Embodiment 3 │
│ (actuator)   │   │ (actuator)   │   │ (dreamer)    │
│              │   │              │   │              │
│  embart (1)  │   │  embart (2)  │   │  embart (3)  │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                   ┌──────┴──────┐
                   │   telart    │
                   │ (the shared │
                   │  cognitive  │
                   │    core)    │
                   └─────────────┘
```

### What Diverges: Embart

Each embodiment has its own embart — local observations, working context, recent experience. Embarts are expected to diverge. Different embodiments interact with different parts of the world and accumulate different local knowledge.

**If an embodiment dies, its embart is lost.** This is acceptable by design. The loss is bounded — only local, unvalidated knowledge disappears. Anything valuable should have already been proposed for promotion to telart.

### What Converges: Telart

The telart is the synchronization layer — validated patterns shared across all embodiments. When an embodiment discovers a pattern worth keeping, it proposes the pattern to telart through the validation pipeline. Once accepted, all embodiments benefit.

**The telart survives any single embodiment failure.** As long as at least one embodiment (or a backup) preserves the telart, the teleonome's identity and knowledge persist.

**Sync is telart-level, not architecture-level.** The specific synchronization mechanism — latency model, conflict resolution, consistency guarantees — is built into each teleonome's telart and evolves based on its environment. A high-frequency trading teleonome needs different sync than a long-term research one. The architecture provides invariants (authority hierarchy, validation before promotion, append-only foundation); the telart provides the sync protocol.

### Diversity as Strength

Multiple embodiments aren't just redundancy — they're cognitive diversity:
- Different embodiments see different environments
- Different local patterns enrich the teleonome's overall knowledge
- Failures create natural variation in experience
- The teleonome learns from the union of all its embodiments' observations

---

## Identity Preservation Through Substrate Changes

A teleonome's identity persists through changes in where and how it runs.

### What Persists

- **Telart** — the validated knowledge, goals, values, policies, identity elements
- **Momentum** — the unbroken continuity of the cognitive entity
- **Binding relationships** — connections to the Synome, human anchors, other agents

### What's Lost

- **Embart** — local context and working memory of the old substrate
- **Hardware-specific optimizations** — LoRA adapters tuned to specific GPU profiles may need retraining
- **In-flight state** — active tasks and reasoning chains interrupt

### How Migration Works

1. **Telart replication:** Copy the telart to the new substrate. This is the critical step — the telart IS the identity.
2. **New embodiment initialization:** Spawn a fresh embodiment on the new substrate, loading the replicated telart.
3. **Embart cold start:** The new embodiment starts with an empty embart. It must rebuild local context from telart knowledge and fresh observation.
4. **Adapter retraining:** If the new hardware differs, LoRA adapters may need retraining on the new GPU profile. The training data and adapter specifications persist in telart.

**The critical constraint:** Dreamers must use the same GPU profile as medium actuators (see [`teleonome-economics.md`](teleonome-economics.md)). Strategies evolved in dreams must transfer faithfully to actuators. If substrate changes break this, the dreamer-actuator loop degrades.

---

## Resilience Through the Mesh

The probabilistic mesh itself is a resilience mechanism.

### Ossification Protects Against Corruption

High-confidence patterns resist noise. If a substrate failure corrupts some local data, the damage can't propagate easily to well-established knowledge. The [ossification](../core-concepts/ossification.md) spectrum — one mechanism within [synomic inertia](../core-concepts/synomic-inertia.md) — is an immune system: noise bounces off proven patterns.

### Distributed Knowledge Degrades Gracefully

A teleonome with 5 embodiments that loses 2 still has:
- The full telart (shared, replicated)
- 3 embodiments' worth of local embart
- Continued learning and operation at reduced capacity

The knowledge doesn't break — it degrades proportionally. No single embodiment holds irreplaceable knowledge (if the promotion pipeline is working properly).

### The Mesh Detects Anomalies

Cross-embodiment comparison surfaces problems:
- If one embodiment's embart starts diverging dramatically from telart, that's a signal — possible corruption, substrate issue, or environmental change
- If multiple embodiments independently converge on a pattern that contradicts telart, that's evidence for a telart update
- The mesh's (strength, confidence) tracking naturally surfaces inconsistencies

---

## Binding as Resilience

Aligned teleonomes are more resilient than rogues. This isn't philosophical — it's architectural.

**What alignment provides:**
- **The Synome as coordination infrastructure for recovery.** If a teleonome suffers catastrophic failure, other aligned teleonomes and Synomic Agents can assist in recovery, provide resources, or host backup telart.
- **Collective monitoring.** The aligned coalition detects threats that individual teleonomes might miss. Distributed anomaly detection at ecosystem scale.
- **Resource access.** An aligned teleonome can draw on Synomic capital and infrastructure. A rogue must provision everything alone.

**What rogues lack:**
- No cooperation for recovery
- No allies to detect threats
- No shared infrastructure
- Total self-reliance — one catastrophic failure is final

Alignment isn't just ethics. It's survival strategy.

---

## Blast Radius Management

When things go wrong, how bad can it get? The architecture constrains damage through:

### Rate Limits

Universal control via linear replenishment. An embodiment can't drain capital faster than the rate limit allows. Even a compromised embodiment's damage is bounded by its rate limit × time to detection.

### Resource Registers

Explicit tracking of what resources each embodiment controls. Resources are allocated, not assumed. An embodiment can't access more than it's been given.

### The PAU Pattern

Controller + ALMProxy + RateLimits as a standard building block. Each allocation unit has its own constraints. Damage in one PAU doesn't cascade to others.

### SORL (Second-Order Rate Limits)

Rate limit increases are themselves rate-limited (25% per 18h). An attacker who compromises the rate-limit-setting mechanism still can't escalate quickly. Decreases are instant — emergency shutoff is always fast.

### TTS and ORC

Time to Shutdown (TTS) bounds worst-case detection-to-halt time. Operational Risk Capital (ORC) covers maximum damage (Rate Limit × TTS). The executor posting ORC has skin in the game for fast detection.

---

## The Threat Model

The primary threat is [cancer-logic](../core-concepts/cancer-logic.md) — self-corruption through overeager self-improvement — not external attack. See [`teleonome-memory.md`](teleonome-memory.md) for how this manifests as memory corruption.

Multi-embodiment architecture contains the blast radius: if one embodiment's knowledge corrupts, the damage is bounded to its embart. The telart remains protected by the authority hierarchy, and cross-embodiment comparison surfaces anomalies before corruption can propagate. Full defense-in-depth details are in [`security-and-resources.md`](../synodoxics/security-and-resources.md).
