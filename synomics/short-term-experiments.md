# Short-Term Dreamer Experiments

**Status:** Implementation pathway
**Last Updated:** 2026-02-03

This document describes pared-down dreamer experiments and how they evolve toward the full Synome architecture.

---

## Purpose

The full Synome vision involves multi-layer knowledge hierarchies, teleonome networks, and sophisticated RSI. Building this all at once is impractical.

Instead: start with minimal viable experiments that preserve the essential invariants, then evolve toward full complexity.

**Principle:** Design data structures now that can grow into the full architecture without rearchitecting.

---

## The Experiment: Game-Playing Agents

### What We're Building

Agents that learn to play games (Chess, Poker, Zork, Monopoly) through training, accumulating knowledge that transfers across games.

### Simplified Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Agent                                │
└─────────────────────────────┬───────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────┐
│     SYNOME      │ │ KNOWLEDGE GRAPH │ │  TRAINING SESSIONS  │
│   (read-only)   │ │ (append-only)   │ │  (RSI environment)  │
│                 │ │                 │ │                     │
│ • Ontology      │ │ • Learned       │ │ • Configs           │
│ • Game rules    │ │   patterns      │ │ • Session outputs   │
│                 │ │ • Starts EMPTY  │ │ • Metrics           │
└─────────────────┘ └─────────────────┘ └─────────────────────┘
```

### Two Flows

**Training (Learning):**
```
Play games → Observe outcomes → Extract patterns → Validate → Write to KG
```

**Inference (Applying):**
```
Query Synome + KG → Compose context → Execute decision
```

---

## Mapping to Full Synome Architecture

| Experiment Concept | Full Architecture | Notes |
|--------------------|-------------------|-------|
| Synome (read-only rules) | Synart (Layers 1+2) | Same role: immutable ground truth |
| Knowledge Graph | Embart | Learned patterns, single embodiment |
| Training Sessions | Dreamart + Dreamer | Formalized later |
| Synome Police | Validation / Governance | Expands over time |
| Agent | Single-embodiment teleonome | No telart layer initially |

### What's Simplified

- **No telart layer** — Single-embodiment teleonomes only
- **No multi-embodiment coordination** — One agent per teleonome
- **No formal dreamart** — Training sessions are informal for now
- **Binary ossification** — Synome (frozen) vs KG (fluid), not full spectrum
- **No cross-teleonome knowledge sharing** — Each agent learns independently

### What's Preserved

- **Authority hierarchy** — Synome > KG
- **Learned patterns start empty** — Must be discovered, not pre-loaded
- **Validation before writes** — Synome Police checks patterns
- **Append-only knowledge** — Can always roll back
- **Confidence tracking** — Patterns have evidence weights

---

## Critical Design Choices

These choices ensure experiments can evolve toward full Synome without rearchitecting.

### 1. Truth Values: Positive and Negative Weights

**Not this:**
```
(fork, effectiveness, high) @confidence=0.85
```

**This:**
```
(fork, effectiveness) @pos_weight=850 @neg_weight=150
```

**Why:**
- Strength and confidence derive from weights
- Negative evidence is explicit
- Ossification emerges naturally (high total weight = hard to shift)
- Matches the (strength, confidence) model in full architecture

### 2. Append-Only with Periodic Compaction

- Append raw observations continuously
- Periodically summarize/compact to manage resources
- Accept context loss as resource discipline tradeoff

**Why:** Preserves audit trail, enables rollback, matches security model.

### 3. Validation Extends Over Time

**Now:** Synome Police checks syntax + LLM sanity check ("does this drift from synart spirit?")

**Later:** Formal logical consistency — embart must logically extend synart without contradictions.

### 4. Security = Self-Corruption Prevention

The threat model is **internal drift**, not external attackers.

```
Bad pattern enters KG
        │
        ▼
Influences future decisions
        │
        ▼
Generates more bad patterns
        │
        ▼
System corrupts itself
```

**Mitigations:**
- High-weight patterns resist noise (ossification)
- Single observations can't corrupt established patterns
- Append-only enables rollback
- Validation catches obvious drift

---

## Evolution Pathway

### Phase 1: Current Experiments (Now)

```
Synome (immutable) ──────────────────────────────────
                                                     │
Knowledge Graph (append-only, pos/neg weights) ──────┤
                                                     │
Training Sessions (informal) ────────────────────────┘
```

- Single-embodiment teleonomes
- Binary ossification (Synome vs KG)
- LLM-based validation
- Games as training domain

### Phase 2: Dreamart Introduction

```
Synome ──────────────────────────────────────────────
    │                                                │
    └── Dreamart (extends/modifies for testing) ─────┤
                                                     │
Knowledge Graph ─────────────────────────────────────┤
                                                     │
Formalized Training Environment ─────────────────────┘
```

- Dreamart formalizes training scenarios
- Can temporarily extend/delete synart rules for experimentation
- Updates more frequently than synart
- Test new perspectives before committing to synart changes

### Phase 3: Ossification Spectrum

```
Synome (axiomatic, governance-only changes) ─────────
    │                                                │
    └── Dreamart ────────────────────────────────────┤
                                                     │
Knowledge Graph with ossification levels: ───────────┤
    • Speculative (low total weight)                 │
    • Established (medium total weight)              │
    • Proven (high total weight)                     │
                                                     │
Pattern promotion path: KG → Synart ─────────────────┘
```

- Ossification becomes explicit spectrum
- Proven patterns can graduate to synart (via governance)
- Synart begins updating (daily cadence)

### Phase 4: Multi-Embodiment / Telart Layer

```
Synart ──────────────────────────────────────────────
    │                                                │
Telart (teleonome-specific patterns) ────────────────┤
    │                                                │
Embart (embodiment-specific patterns) ───────────────┤
    │                                                │
Multiple embodiments per teleonome ──────────────────┤
    │                                                │
Dreamer/Actuator split ──────────────────────────────┘
```

- Telart layer emerges between synart and embart
- Multiple embodiments share telart
- Dreamers explore, actuators execute
- Cross-teleonome sharing only via synart

---

## Invariants Across All Phases

These must hold regardless of current phase:

1. **Authority hierarchy exists** — Higher layers trump lower layers
2. **Patterns have truth values** — (strength, confidence) or equivalent
3. **Evidence flows back** — Outcomes inform future patterns
4. **Validation before promotion** — Patterns checked before entering higher layers
5. **Security = self-corruption prevention** — Overeager updates are the threat
6. **Append-only foundation** — History preserved, rollback possible

---

## What's Left to Discover

The experiments should reveal:

- Optimal training/inference logic (same path or different?)
- What RSI metadata is most valuable
- How to measure pattern transfer across domains
- When to compact vs preserve granularity
- How aggressive validation should be

These are **degrees of freedom** — the experiments figure them out, not the architecture docs.

---

## Summary

| Aspect | Now | Evolves Toward |
|--------|-----|----------------|
| Knowledge layers | Synome + KG | Synart + Telart + Embart |
| Embodiments | Single | Multiple per teleonome |
| Ossification | Binary | Spectrum with promotion |
| Training | Informal sessions | Formalized dreamart |
| Validation | Syntax + LLM sanity | Logical consistency |
| Update cadence | KG only | Embart > Dreamart > Telart > Synart |

**The goal:** Build the simplest thing that works, but build it so it can grow.

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| `probabilistic-mesh.md` | Full truth value system these experiments build toward |
| `synome-layers.md` | The 5-layer architecture (synart, telart, embart) |
| `dreamer-perspective.md` | Full dreamer embodiment — the evolution target |
| `security-and-resources.md` | Security as self-corruption prevention |
| `short-term-actuators.md` | Parallel actuator pathway (teleonome-less beacons) |
