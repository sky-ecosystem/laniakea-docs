---
concepts:
  defines:
    - five-layer-architecture
    - artifact-hierarchy
    - language-intent
  references:
    - dual-architecture
    - beacon-framework
    - probabilistic-mesh
    - truth-values
    - ossification
    - rsi
    - dreamer-actuator-split
    - retrieval-policy
---

# The Five Layers of the Synome

The Synome architecture consists of five layers, moving from abstract shared truth down to concrete isolated execution.

---

## Layer 1: Synome

The foundational data layer. This is the curated, shared source of truth that all aligned entities have identical copies of. The entire Layer 1+2 artifact is called **synart**.

**Components:**

- **Atlas** — The single human-readable node. A constitutional document that anchors the entire system. Everything else is AI code graphs; Atlas is the one thing humans can directly read and govern.

- **Language Intent** — The system that translates human intent (Atlas, Agent Directives, Teleonome Directives) into machine logic. Grounded by the Synomic Library to ensure honest interpretation and resistance to prompt engineering. All human-readable directives at every layer pass through this single trusted translator.

- **Synomic Axioms** — Machine-readable rules derived from Atlas via Language Intent. The formal deontic interface to constitutional intent. These axioms instantiate Layer 2's Sky Superagent. Axioms are hard (1,1) once set — they form part of the deontic skeleton.

- **Synomic Library** — A subset of synart containing the canonical knowledge base:
  - **Verified knowledge** — Facts, patterns, and models with (strength, confidence) truth values
  - **Tools** — Methods, algorithms, and capabilities for operating aligned
  - **Teleonome seeds** — Programs that bootstrap aligned teleonomes
  - **Best practices** — Governance-approved strategies and approaches
  - **Meta-strategies** — Patterns for effectively mining and using the library itself (RSI layer)

  The Library serves as the highest-authority probabilistic knowledge source. Embodiments that reference synart probabilities are more likely to remain aligned and avoid penalties. The Library also recursively improves its own pattern-mining strategies through RSI.

**The Core Loop:**

```
Atlas → Language Intent → Synomic Axioms → Synomic Library → Language Intent
```

This is self-referential by design. Language Intent needs the Library to translate accurately, but the Library is shaped by what the Axioms say matters. They co-constitute each other.

**Why a single translator.** A single, maximally-scrutinized translation layer is more secure than redundant translators — the same logic as a single root of trust in cryptography. Multiple translators would each receive less scrutiny, might diverge in interpretation, and create attack surface through inconsistency. One translator concentrates all defensive resources on a single point of maximum attention.

**The bootstrapping problem is the known risk.** The co-constitution of Language Intent and the Library is a genuine circular dependency — the deepest vulnerability in the architecture. This is not hidden or downplayed. The security model is to be fully explicit about it: Language Intent's robustness is the single most critical concern in the entire system, warranting extreme public scrutiny, dedicated resources, and permanent status as a shared public concern. Concentrating maximum collective attention on this one vulnerability IS the defense. The alternative — distributing translation across multiple less-scrutinized interpreters — would trade one visible, maximally-defended vulnerability for many hidden, under-defended ones.

**Deontic vs Probabilistic in Layer 1:**
- Atlas, Axioms = deontic (hard, authoritative)
- Library contents = probabilistic (soft, weighted by strength/confidence)
- Language Intent = bridge (translates soft human text into hard machine rules)

---

## Layer 2: Synomic Agents

The governance and operational layer. These are the running agents that make the system actually work.

**Components:**

- **Sky Superagent** — The governance entity containing:
  - *Sky Voters* — Stakeholders who empower governance and align Atlas
  - *Core Council* — Guardian agents selected by Sky Voters that align Language Intent, Synomic Library, and the Effectors

- **Effectors** — Operational outputs that instantiate Synomic Agents:
  - *Stability* — Mechanisms for system stability
  - *Protocol* — Protocol-level operations
  - *Accessibility* — External accessibility interfaces
  - *Agent Primitives* — Base operational components

- **Synomic Agent** — The formula for creating agents: Directives → Axioms + Resources = Agent
  - *Agent Directives* — Human-readable instructions for each synomic agent, voted on by token holders. Translated through Language Intent (Layer 1) to ensure honest interpretation and resistance to prompt engineering.
  - *Agentic Axioms* — Machine-readable rules derived from Agent Directives. The constitutional foundation that the agent's graph is organized around.
  - *Synomic Agent Resources* — The resources (compute, credentials, capabilities) allocated to instantiate agents.

- **Synomic Agent Types** — Instantiated by Agentic Axioms + Synomic Agent Resources, organized into a rank hierarchy based on governance relationship to the Core Council:

  | Rank | Agent Types | Governance Relationship |
  |------|-------------|------------------------|
  | **0** | Core Council | Sovereign |
  | **1** | Guardians, Core Controlled Agents, Recovery Agents | Directly regulated by Core Council |
  | **2** | Primes, Generators | Accordant to a Guardian |
  | **3** | Halos, Folio Agents | Administered by a Prime |

  - *Guardians* (Rank 1) — Execute and guard specific tasks, post collateral
  - *Core Controlled Agents* (Rank 1) — Core Council operational vehicles for legacy asset management; tokenless
  - *Recovery Agents* (Rank 1) — Crisis agents activated when a Guardian collapses; temporary, tokenless
  - *Generators* (Rank 2) — Generate outputs (e.g., USDS)
  - *Primes* (Rank 2) — Capital allocation agents
  - *Halos* (Rank 3) — Regulated endpoint agents (investment products under Prime umbrella)
  - *Folio Agents* (Rank 3) — Standardized supply-side holding structures; tokenless, single owner (the principal)

**Relationships:**

- Synomic Axioms **instantiate** Sky Superagent
- Effectors **instantiate** Synomic Agents
- Agent Directives **translated by** Language Intent (Layer 1)
- Agent Directives **create** Agentic Axioms
- Agentic Axioms **instantiate** Synomic Agent Types
- Synomic Agent Resources **instantiate** Synomic Agent Types
- Sky Voters **align** Atlas and **select** Core Council
- Core Council **aligns** Language Intent, Synomic Library, Stability, Protocol, Accessibility, and Agent Primitives
- Synomic Agent Types **align** Layer 3 (Teleonomes)

---

## Layer 3: Teleonomes

Aligned autonomous entities with their own missions. Instantiated by the Synomic Library (from teleonome seeds).

**Analogy:** A Teleonome is best thought of as a **private person or private company** acting in the world. Its promises must always be discounted because internal rules and self-modification logic are private and mutable. Teleonomes are inherently less scalable than Synomic Agents due to private state, coordination overhead, and trust limits.

**Components:**

- **Teleonome Directive** — Human-readable foundational instruction for this teleonome. Translated through Language Intent (Layer 1) to ensure honest interpretation and resistance to prompt engineering. While teleonomes take day-to-day voice commands from bound humans, the directive always overrides voice commands. Over time, if there's persistent friction, the teleonome requests a formal directive update (which has cost and requires governance approval).

- **Teleonomic Axioms** — Machine-readable rules derived from the Teleonome Directive. The teleonome's entire graph is organized around these axioms.

- **Teleonome Library** — The teleonome's own curated knowledge and patterns

- **Dreamarts** — Experimental overlays for simulating and evolving the teleonome

- **Embodiment Interface** — Global representation of each embodiment, maps to Layer 4

- **Resource Register** — Explains how resources (cryptographic keys, legal authority) map to which embodiments (e.g., multisigs with different access levels). The teleonome's total resources are the sum of what's in each embodiment, compounded from the original resources seeded when created from a teleonome seed.

**Relationships:**

- Synomic Library **instantiates** the entire Teleonome layer
- Teleonome Directive **translated by** Language Intent (Layer 1)
- Teleonome Directive **creates** Teleonomic Axioms
- Synomic Agent Types **align** Teleonomes
- Embodiment Interface **maps to** Layer 4
- Resource Register **maps resources to** Layer 4

---

## Layer 4: Embodiment

A specific instance of a teleonome — an "emb."

**Components:**

- **Local Data** — Embodiment-specific state, logs, cache

- **Orchestrator** — Coordinates and manages the embodied agent, connects to Layer 5

- **Resources** — Local resource allocation, maps to Layer 5 resources

**Relationships:**

- Embodiment Interface (L3) **maps to** this layer
- Resource Register (L3) **maps resources to** this layer
- Orchestrator **connects to** Embodied Agent (L5)
- Resources **map to** Resources (L5)

---

## Layer 5: Embodied Agent

The actual running agent that interacts with the world.

**Components:**

- **Embodied Agent** — The executing agent instance

- **Beacons** — Interfaces for interacting with the world (reporting, execution, monitoring)

- **Direct Hardware Control** — Physical interfaces for robots, infrastructure, devices

- **Resources** — The actual cryptographic keys, credentials, and capabilities available to this agent

**Relationships:**

- Orchestrator (L4) **spawns/manages** Embodied Agent
- Resources (L4) **map to** Resources (L5)
- Embodied Agent **operates through** Beacons and Direct Hardware Control
- Beacons and Hardware **interact with** World
- World **returns evidence to** Synomic Library (L1)

---

## Embodiment Power Levels

Embodiments differ in **local cognitive power**, which constrains what agents they can run and what beacon profiles they can support.

| Level | Compute | Typical Role | Beacon Profiles |
|-------|---------|--------------|-----------------|
| **Light** | Minimal, high security | Legal, economic, and operational endpoints. Execute policies from elsewhere. | LPLA, simple LPHA |
| **Medium** | Substantial, low latency | Continuous sensing and acting. Significant local intelligence, online learning. | Sentinels, HPLA, advanced LPHA |
| **Heavy** | Very large, often hidden | Deep cognition, dreaming, RSI, global coordination. Hosts full teleonome. | Minimal or none |

**Dreamer vs Actuator:**
- **Actuators** typically run on light-to-medium embodiments, interacting with the real world
- **Dreamers** typically run on heavy embodiments, exploring in simulation

See [`actuator-perspective.md`](../synoteleonomics/actuator-perspective.md) and [`dreamer-perspective.md`](../synoteleonomics/dreamer-perspective.md) for first-person views.

---

## World

External reality — not part of the Synome, but the source of evidence and the target of action.

- Receives actions from Beacons and Direct Hardware Control
- Returns evidence to the Synomic Library, closing the loop

---

## The Human Interface Pattern

Human-readable directives are the interface to AI systems at every level.

| Level | Document | Who controls | What it governs |
|-------|----------|--------------|-----------------|
| Layer 1 | **Atlas** | Sky Voters | The entire Synome |
| Layer 2 | **Agent Directives** | Token holders | Each synomic agent's behavior |
| Layer 3 | **Teleonome Directive** | Bound human / stakeholders | The teleonome's foundational instruction |

**How it works:**

```
Human text (Atlas / Agent Directive / Teleonome Directive)
                    │
                    ▼
        ┌───────────────────────┐
        │   Language Intent     │ ◄── single trusted translation layer
        │  (grounded by Library)│
        └───────────────────────┘
                    │
                    ▼
        Machine constraints (resistant to adversarial twisting)
```

All human-readable directives pass through the same Language Intent system, grounded by the Synomic Library. This ensures:
- Honest interpretation of human intent
- Resistance to prompt engineering / adversarial manipulation
- Consistent translation semantics across all levels

**Directive vs Voice Commands:**

Teleonomes (and agents) also take real-time voice commands from bound humans. But:
- Voice commands are operational, day-to-day instructions
- The Directive is constitutional, formally governs behavior
- **Directive always overrides voice commands**
- When persistent friction occurs, the teleonome requests a formal directive update
- Directive updates have cost and require governance approval
- The entire graph reorganizes around the new directive

This creates healthy tension — systems work within their directive, but surface the need for formal updates rather than silently drifting.

---

## Extra-Synomic Data

Not a layer, but an important concept: data that's too real-time/volatile for the Synome itself.

- Accessed via **pointers** stored in the Synome
- Lives in external systems (Sentinel databases, live feeds, operational metrics)
- Gets **summarized/distilled** into the Synome at settlement intervals

Examples:
- Per-Prime Sentinel databases
- Live trading data
- Raw observations before pattern extraction

The Synome stays clean and curated. The messy real-time stuff lives outside but is accessible when needed.

---

## Artifact Mapping

| Layer | Artifact | Shared? |
|-------|----------|---------|
| 1 + 2 | synart | Yes — identical across all aligned entities |
| 1 + 2 + 3 | telart | Yes — across embodiments of this teleonome |
| 1 + 2 + 3 + 4 | embart | No — local to this embodiment |
| 5 | (ephemeral) | No — agent context, not persisted |

**synart** is the entire Layers 1+2 artifact, containing:
- Synomic Library (probabilistic knowledge, tools, patterns)
- Synomic Axioms (hard rules)
- Governance rules (Core Council, delegates, operational executors)
- Atlas (constitutional anchor)
- Language Intent configuration

The Synomic Library is a *subset* of synart — the knowledge base portion. Other synart components handle governance, axioms, and translation.

### Key Term Clarifications

These related concepts are often confused:

| Term | Definition | Layer |
|------|------------|-------|
| **Local Data** | Raw embodiment state: logs, caches, traces, sensor readings, observations. Unstructured or semi-structured. | Layer 4 |
| **Embart** | The curated, structured probabilistic projection *derived from* Local Data. This is what the agent actually queries — patterns, beliefs, learned models with (strength, confidence) values. | Layers 1-4 combined |
| **Ephemeral context** | Runtime scratchpad: working memory, intermediate computations, conversation state. Not intended to persist beyond the current execution. | Layer 5 only |

**The pipeline:**
```
Raw observations (sensors, APIs, outcomes)
        │
        ▼
Local Data (logged, stored)
        │
        ▼
Pattern extraction / curation
        │
        ▼
Embart (queryable probabilistic KB)
        │
        ▼
Ephemeral context (used during execution, discarded)
```

**Why this matters:**
- Embart is what embodiments *reason with* — it's structured for queries
- Local Data is the *evidence source* — it's structured for storage and audit
- Ephemeral context is *working memory* — it's structured for speed, not persistence

---

## Probabilistic-Deontic Architecture

The Synome is a [dual architecture](../core-concepts/dual-architecture.md) — a sparse deontic skeleton of hard, deterministic connections surrounded by a dense [probabilistic mesh](../core-concepts/probabilistic-mesh.md) of soft, informing connections. Governance sits at the [crystallization interface](../core-concepts/crystallization-interface.md) — consuming probabilistic evidence, producing deontic commitments. See [`synome-overview.md`](synome-overview.md) for the canonical treatment of the dual architecture and [`probabilistic-mesh.md`](../synodoxics/probabilistic-mesh.md) for the full mesh specification.

> **Note:** The deontic/probabilistic split is a pedagogical simplification. These are endpoints of a continuous spectrum — an unannotated knowledge graph is a valid Synome where everything is axiomatic, and you soften parts by adding explicit truth values. See [`probabilistic-mesh.md`](../synodoxics/probabilistic-mesh.md).

**Visual convention used in this document:**
- `──────►` Hard (authority, control, instantiation, governance)
- `- - - ►` Soft (knowledge, evidence, alignment, learning)

---

## Structural Invariants

These must hold regardless of implementation details:

1. **Teleonomes think; beacons act** — Cognition is private; action is regulated
2. **Beacons are apertures, not minds** — They externalize intent, they don't have it
3. **All enforcement bottoms out in embodiments** — Physical infrastructure is the ultimate enforcement boundary
4. **Embodiments may host many agents and beacons** — Or none (purely internal operation)
5. **Beacon sophistication is constrained by embodiment power** — Light embodiments can't run sentinels
6. **Intelligence lives privately; power enters the world only through regulated apertures** — The core separation

---

## The Permanent Design Choices

These are the foundational decisions that are hard to change once built:

1. **Directives as universal human interface** — Every level has a human-readable directive (Atlas, Agent Directive, Teleonome Directive) that goes through Language Intent
2. **The core loop structure** — Atlas → Language Intent → Axioms → Library → Language Intent
3. **The layer model** — 5 layers with clear containment
4. **Content addressing** — Identity = hash of content
5. **The truth model** — (strength, confidence) on all assertions
6. **Instantiation semantics** — Axioms instantiate Sky; Library instantiates Teleonomes; Primitives instantiate Agent Types
7. **Alignment semantics** — Sky Voters align Atlas; Core Council aligns Layer 1 components and Effectors; Agent Types align Teleonomes
8. **The primitive types** — entity, relation, event, quantity, context, timestamp
9. **Language Intent as single translation layer** — All human text passes through the same trusted interpreter, grounded by Synomic Library, resistant to prompt engineering
10. **Probabilistic-deontic architecture** — Soft probabilistic connections (knowledge, evidence) inform hard deontic connections (rules, governance). Governance crystallizes probability into authority.

Everything else (storage backend, sync transport, query language) can be swapped.
