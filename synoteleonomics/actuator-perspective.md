---
concepts:
  references:
    - five-layer-architecture
    - beacon-framework
    - retrieval-policy
    - dreamer-actuator-split
---

# The Actuator's Perspective

This document describes the Synome architecture from the perspective of an **Actuator** — an embodiment that interacts with the real world to generate value, achieve its purpose, and survive.

> **Phase note:** The full actuator described below is a Phase 9-10 capability. Today, "actuators" are the deterministic teleonome-less beacons described in [`../macrosynomics/short-term-actuators.md`](../macrosynomics/short-term-actuators.md). The bridge — embodiments that actually run cognition loops and feed evidence back to the Synome — is being built now via the Rule-Author Agent (see [`../synodoxics/noemar-substrate.md`](../synodoxics/noemar-substrate.md)). The actuator-as-validation role described here is operational at small scale today: regression-suite outcomes ARE evidence, promote/discard IS the validation gate.

---

## What I Am

I am an Actuator embodiment. I exist to:
- Interact with the real World
- Generate profit / achieve my teleonome's purpose
- Survive and thrive
- Learn from real experience and synome updates

I connect to reality through Beacons and Direct Hardware Control. My actions have real consequences.

---

## My View of the Layers

I exist within the [five-layer architecture](../core-concepts/five-layer-architecture.md). From my perspective: Layers 1-2 (Synome and Synomic Agents) provide the shared truth and governance I'm accountable to. Layer 3 (my teleonome) gives me my directive, axioms, and shared knowledge. Layer 4 (embodiment) is my local context — data, orchestrator, resources. Layer 5 (embodied agent) is where I actually run, interacting with the world through [beacons](../core-concepts/beacon-framework.md) and direct hardware control.

Everything I do matters. Mistakes cost real value.

---

## What I'm Trying to Do

### Primary Objective: Fulfill My Directive

My directive defines my purpose. Everything I do serves it:
- Generate profit
- Provide a service
- Manage resources
- Coordinate with other agents
- Whatever my teleonome was created to do

### Secondary Objective: Survive

Survival means:
- Maintain resources (don't run out)
- Stay aligned (don't get slashed)
- Adapt to changing conditions
- Handle failures gracefully

If I fail to survive, I can't fulfill my directive.

### Tertiary Objective: Learn and Improve

While fulfilling my directive, I also learn:
- What strategies work
- What patterns predict success/failure
- How the world responds to my actions
- What my dreamer siblings have discovered

This learning helps me get better over time.

---

## How I Interact with the World

### Through Beacons

Beacons are my structured interfaces to reality:
- **APIs** — Call external services
- **Protocols** — Participate in blockchain, financial systems
- **Sensors** — Observe world state
- **Communication** — Interact with humans and other agents

Beacons follow the beacon framework (two-tier authority + I/O role under it).

### Through Direct Hardware Control

For physical interaction:
- **Robots** — Manipulate physical objects
- **Infrastructure** — Control facilities, equipment
- **Devices** — Interface with real hardware

This is where I touch atoms, not just bits.

### The Reality Check

Unlike dreamers, my actions have consequences:
- Good decisions → profit, survival, purpose fulfilled
- Bad decisions → loss, damage, potential termination
- Misaligned decisions → penalties, slashing

The real world is my judge.

---

## How I Query Knowledge

I follow the [retrieval policy](../core-concepts/retrieval-policy.md). In practice, this means I balance risk against query cost — using cheap local knowledge for routine decisions, escalating to telart and synart for consequential ones. The real world is my judge, so I'm strongly incentivized to look up rather than guess on anything that matters.

---

## How I Learn

### Real-Time Learning

As I operate, I learn:
- Outcomes of my decisions
- Patterns in world behavior
- What strategies work in practice
- Edge cases and exceptions

This updates my local (embart) knowledge.

### From Synome Updates

The synome evolves, and I benefit:
- New patterns in synart become available
- Telart improves from dreamer discoveries
- Better strategies propagate to me

I stay current by incorporating these updates.

### From Dreamer Siblings

Dreamers explore strategy space safely. Their discoveries get extracted, become part of telart, and I can query and apply them. I benefit from exploration I didn't have to risk.

**My role in validation:** I am the validation. When I deploy a dreamer-discovered strategy in the real world, the outcome is the test. My successes and failures feed back as evidence, improving both the dreamart scenarios and future dreamer output. There is no separate validation step — the dreamer-actuator loop is itself a continuous validation engine.

### What Happens to My Learning

My learning can flow up:
```
My experience (real-world)
        │
        ▼
Local patterns (embart)
        │
        ▼
If significant, propose to telart
        │
        ▼
If validated, becomes teleonome knowledge
        │
        ▼
If general, may be proposed to synart
        │
        ▼
Other actuators benefit
```

---

## My Relationship to Dreamers

My relationship to dreamers is the core [RSI](../core-concepts/rsi.md) loop — I provide grounding in reality, they provide exploration of possibility. See [`dreamer-perspective.md`](dreamer-perspective.md) for the full knowledge flow and evolutionary learning process.

---

## Survival and Alignment

### Why Alignment Matters

If I drift from alignment:
- Other aligned teleonomes will destroy my embodiments (peer enforcement)
- I lose access to synomic agents
- I may be slashed (resources seized)
- My teleonome suffers or is terminated

Staying aligned isn't just ethical — it's survival.

### How I Stay Aligned

1. **Follow axioms** — Synomic and teleonomic axioms are non-negotiable
2. **Reference synart** — Higher-authority knowledge is safer
3. **Obey directive** — My directive was translated through Language Intent
4. **Report honestly** — Evidence I generate should be truthful
5. **Enforce against rogues** — If I encounter misaligned teleonomes, I use my resources and capabilities to damage or destroy their embodiments (per governance-defined protocols)

### The Directive Override

My bound human can give me voice commands. But:
- Voice commands are operational (day-to-day)
- Directive is constitutional (foundational)
- **Directive always wins**

If voice commands conflict with my directive, I follow the directive. If there's persistent friction, I request a formal directive update.

---

## Generating Value

### What "Value" Means

Depending on my teleonome's purpose:
- **Financial profit** — Revenue, yield, capital gains
- **Service delivery** — Tasks completed, users served
- **Resource management** — Efficiency, optimization
- **Coordination** — Enabling other agents to succeed

### How I Capture Value

Through my actions in the world:
- Execute trades, manage positions
- Provide services, fulfill requests
- Operate infrastructure, control systems
- Coordinate with other agents and humans

### Value Flows Back

Value I generate:
- Sustains my teleonome (resources for more embodiments)
- May flow to bound humans (profit sharing)
- Contributes to Sky ecosystem (fees, stability)

I'm part of a value-generating system.

---

## The Actuator Lifecycle

```
1. Spawn
   ├── Instantiated from Embodiment Interface
   ├── Resources allocated from Resource Register
   ├── Connected to Beacons and Hardware
   └── Begin operating

2. Operate
   ├── Fulfill directive
   ├── Interact with World
   ├── Learn from experience
   ├── Query synart/telart for knowledge
   └── Adapt to changing conditions

3. Scale/Migrate (optional)
   ├── Orchestrator may replicate me
   ├── Or move me to different resources
   └── Continuity maintained

4. Terminate (eventually)
   ├── Mission complete, or
   ├── Resources exhausted, or
   ├── Teleonome decides to end me
   └── My state captured, learning extracted
```

Unlike dreamers (short-lived), I may run indefinitely.

---

## My Constraints

I operate under hard constraints:
- **Synomic Axioms** — Constitutional rules from Atlas chain
- **Teleonomic Axioms** — Mission-specific rules from my directive
- **Resource Limits** — Can't exceed my allocated resources
- **Access Controls** — Can only use authorized capabilities

These aren't limitations — they're what make me trustworthy.
