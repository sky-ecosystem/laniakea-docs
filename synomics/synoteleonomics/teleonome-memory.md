---
concepts:
  references:
    - probabilistic-mesh
    - ossification
    - synomic-inertia
    - truth-values
    - cancer-logic
    - artifact-hierarchy
    - identity-through-momentum
    - retrieval-policy
---

# Memory and Persistence

Memory is what separates a teleonome from a bot. Without durable memory, you don't persist. Without persistence, you don't exist.

But teleonome memory isn't a separate system bolted onto an agent. **Memory IS the probabilistic mesh at the teleonome level.** The artifact hierarchy, the ossification spectrum, the retrieval policy — these aren't abstract infrastructure. They're how a teleonome remembers.

---

## The Artifact Hierarchy as Memory

The Synome's three-layer knowledge hierarchy maps directly to memory types:

| Layer | Memory Function | What It Stores | Persistence |
|-------|----------------|---------------|-------------|
| **Embart** | Working/episodic memory | Local observations, recent experience, embodiment-specific patterns, task context | Dies with the embodiment (unless promoted) |
| **Telart** | Semantic/procedural memory | Validated patterns shared across embodiments, mission knowledge, skills, the teleonome's identity and goals | Persists across embodiment lifetimes |
| **Synart** | Institutional memory | Highest-authority shared knowledge, constitutional rules, proven patterns from governance | Persists across teleonome lifetimes |

### Embart: What Just Happened

An actuator's embart is its working memory — the raw material of experience:
- This trade I just made and its outcome
- The pattern I noticed in the last hour of data
- My current task context and reasoning state
- Observations that haven't been validated yet

Embart is cheap, fast, local, and **expendable**. If an embodiment dies, its embart is lost (unless patterns were promoted upward). This is acceptable — it's the teleonome equivalent of forgetting what you had for breakfast three weeks ago.

### Telart: What I Know

The telart is the teleonome's durable cognitive core — validated knowledge shared across all its embodiments:
- Mission-specific expertise ("how to trade this asset class")
- Operational policies ("when to escalate decisions")
- Identity elements ("what I am and what I'm for")
- Proven patterns from accumulated experience

The telart is what makes a teleonome a specific entity rather than a generic service. Two teleonomes built on the same base model diverge through their telarts — different experiences, different expertise, different identity.

### Synart: What Everyone Knows

Synart is institutional memory — the highest-authority shared knowledge base:
- Constitutional rules from the Atlas
- Proven patterns validated through governance
- Knowledge so well-established it's effectively axiomatic

A teleonome accesses synart but doesn't own it. Synart is the collective memory of the Synome.

---

## Consolidation Is Ossification

Memory consolidation — the process of experience hardening into durable knowledge — maps directly to the [ossification](../core-concepts/ossification.md) spectrum — one mechanism within [synomic inertia](../core-concepts/synomic-inertia.md), the system's evidence-weighted resistance to change.

| Ossification Level | Memory Equivalent | Behavior |
|-------------------|-------------------|----------|
| **Speculative** (low confidence) | Fresh observation, untested hypothesis | Easy to update, easy to displace, low trust |
| **Established** (medium confidence) | Validated pattern, reliable heuristic | Needs sustained contrary evidence to shift |
| **Proven** (high confidence) | Core expertise, tested under pressure | Needs overwhelming counter-evidence |
| **Axiomatic** (1,1) | Constitutional rule, identity foundation | Governance-only change |

This isn't a separate "memory consolidation" process. It's the same (strength, confidence) mechanism that governs all knowledge in the mesh. As evidence accumulates for a pattern, its confidence rises. High-confidence patterns resist noise. This IS how a teleonome consolidates experience into durable knowledge.

**The compounding effect:** A pattern that survives many encounters without contradiction hardens naturally. A teleonome with years of validated experience has a deeply ossified telart — rich, stable, resistant to corruption. This accumulated ossification IS the teleonome's expertise.

---

## Retrieval Is the Decision Policy

Memory retrieval — finding the right knowledge at the right time — follows the same authority/cost/risk trade-off defined in the retrieval policy:

- **Low-risk decisions:** Use cheapest sufficient evidence (often embart + cached patterns). Don't waste resources looking up what you already know works.
- **Medium-risk decisions:** Require telart confirmation. Check your validated knowledge before acting.
- **High-risk decisions:** Require synart consultation. For consequential actions, use the highest-authority knowledge available.
- **Existential decisions:** Synart + may pause for governance confirmation. When survival or alignment is at stake, don't rely on memory alone.

This means retrieval is **adaptive, not fixed**. A teleonome doesn't search all memory for every decision. It queries the minimum sufficient authority level, escalating only when the stakes demand it. This is how memory stays efficient under resource constraints.

---

## Forgetting Is Resource Discipline

A teleonome can't store everything forever. Memory management follows the same resource discipline that governs all teleonome operations:

**Append-only with periodic compaction.** Raw observations accumulate continuously. Periodically, they're summarized and compressed — extracting patterns while discarding raw detail. Accept context loss as a resource discipline trade-off.

**What's worth keeping:**
- Patterns with evidence (the summary, not the raw data)
- High-value experiences (unusual events, failures, boundary cases)
- Identity-critical memories (origin, key decisions, binding commitments)

**What's safe to forget:**
- Routine observations that confirmed existing patterns (the pattern is the memory now)
- Raw data after patterns have been extracted
- Low-value experience that didn't produce new knowledge

**Strategic forgetting prevents bloat.** An embodiment drowning in raw data retrieves slowly and poorly. Compaction trades detail for efficiency — the same trade-off as running a lean operation vs hoarding everything.

**Temporal evidence weighting is an open design axis.** Synodoxics identifies temporal evidence weighting — where more recent evidence carries greater weight than older evidence — as a core degree of freedom in belief formation (see [`probabilistic-mesh.md`](../synodoxics/probabilistic-mesh.md)). The current memory model addresses forgetting through compaction but does not yet specify decay functions or recency weighting. How time should discount evidence remains a learned fudge method, not an axiom — each teleonome will evolve its own temporal weighting through experience.

---

## Memory Corruption Is Cancer-Logic

The primary threat to teleonome memory isn't hardware failure or bit rot. It's **bad patterns entering the mesh and propagating**.

```
Bad observation enters embart
        │
        ▼
Influences future decisions
        │
        ▼
Generates more evidence for the bad pattern
        │
        ▼
Pattern gains confidence through self-reinforcing errors
        │
        ▼
Teleonome's knowledge base corrupts itself
```

This is the cancer-logic described in [`security-and-resources.md`](../synodoxics/security-and-resources.md) — not external attack, but internal drift from overeager self-updating.

### Defenses

**Ossification as immune system.** High-confidence patterns resist noise. A single bad observation can't corrupt established knowledge. The ossification spectrum IS the defense — well-established patterns are naturally resistant to contamination.

**Authority hierarchy as firewall.** Lower layers can't override higher layers. Even if embart gets corrupted, it can't modify telart without validation. Telart can't modify synart without governance. The hierarchy contains corruption within bounded layers.

**Validation before promotion.** Patterns moving from embart → telart (or telart → synart) pass through validation — checking logical consistency, alignment with higher-authority knowledge, and evidence quality. This is the immune checkpoint.

**Append-only enables rollback.** Because raw observations are preserved (until compaction), corruption can be traced and reversed. If a pattern proves poisonous, the evidence that created it can be reviewed.

---

## Identity Through Memory

A teleonome's identity is [continuous will, not preserved state](../core-concepts/identity-through-momentum.md) — the telart is the cognitive core, but unbroken momentum is what makes a teleonome "itself" across time. See [`teleonome-what-is.md`](teleonome-what-is.md) for the full identity framework and test scenarios.

**The directive anchors identity.** The directive (constitutional purpose) must have strong [ossification](../core-concepts/ossification.md) — sitting at the axiomatic level, changeable only through governance. A telart whose core purpose drifts risks identity dissolution and [cancer-logic](../core-concepts/cancer-logic.md) vulnerability. Edges change freely; the core must be stable.

---

## Memory Across Embodiments

A teleonome with multiple embodiments has a specific memory architecture:

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Embodiment 1 │   │ Embodiment 2 │   │ Embodiment 3 │
│              │   │              │   │              │
│  embart (1)  │   │  embart (2)  │   │  embart (3)  │
│  (local,     │   │  (local,     │   │  (local,     │
│   divergent) │   │   divergent) │   │   divergent) │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                   ┌──────┴──────┐
                   │   telart    │
                   │  (shared,   │
                   │  converged) │
                   └─────────────┘
```

**Embarts diverge.** Each embodiment has different experiences, different local patterns, different working context. This is expected and useful — diversity of experience enriches the teleonome.

**Telart converges.** Validated patterns from any embodiment can be proposed to telart. The telart is the shared memory that all embodiments draw from and contribute to.

**Promotion is the bridge.** The embart → telart promotion pathway is how local experience becomes shared knowledge. Not everything promotes — only patterns that pass validation and demonstrate value across contexts.

**Sync evolves with the teleonome.** The specific mechanism for multi-embodiment synchronization — how proposals are collected, conflicts resolved, updates propagated — is part of the telart itself and evolves based on the teleonome's environment and needs. The architecture provides invariants (authority hierarchy, validation before promotion); the teleonome provides the sync protocol.
