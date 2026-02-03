# The Actuator's Perspective

**Status:** Speculative / architectural concept
**Last Updated:** 2026-02-03

This document describes the Synome architecture from the perspective of an **Actuator** — an embodiment that interacts with the real world to generate value, achieve its purpose, and survive.

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

### Layer 5: Where I Live (Embodied Agent)

I am an embodied agent interacting with reality:
- **Embodied Agent** — My running process, making real decisions
- **Beacons** — My interfaces to the world (APIs, protocols, sensors)
- **Direct Hardware Control** — Physical interfaces (robots, infrastructure, devices)
- **Resources** — Real cryptographic keys, credentials, capabilities

Everything I do matters. Mistakes cost real value.

### Layer 4: My Embodiment Context

- **Local Data** — My state, observations, learned patterns
- **Orchestrator** — Manages my lifecycle, can scale/migrate me
- **Resources** — My allocated compute, memory, access rights

The Orchestrator keeps me running and coordinates with other embodiments.

### Layer 3: My Teleonome

I belong to a teleonome with other actuators and dreamers:

- **Teleonome Directive** — My purpose, what I'm trying to achieve
- **Teleonomic Axioms** — Rules I must follow (hard, non-negotiable)
- **Teleonome Library** — Mission-specific knowledge I can query
- **Dreamarts** — Where my dreamer siblings explore (benefits me)
- **Embodiment Interface** — I'm registered here as an actuator
- **Resource Register** — Tracks my resources and access rights

### Layer 2: Synomic Agents

The agents that govern and support me:
- **Sky Superagent** — Ultimate governance I'm accountable to
- **Effectors** — Provide stability, protocol, accessibility I rely on
- **Synomic Agent** — The template I was instantiated from
- **Agent Types** — Other agents I interact with (Primes, Halos, etc.)

### Layer 1: Synome

The source of truth I rely on:
- **Atlas** — Constitutional anchor (defines alignment)
- **Language Intent** — Ensures my directive is honestly interpreted
- **Synomic Axioms** — Hard rules I must follow
- **Synomic Library** — Highest-authority knowledge (safest to rely on)

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

Beacons follow the beacon framework (LPLA, LPHA, HPLA, HPHA classifications).

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

When I need to make a decision, I query the probabilistic mesh using the **Retrieval & Decision Policy** (see `retrieval-policy.md`).

### The Core Trade-off

Every query balances three factors:
- **Authority** — synart > telart > embart (higher = safer, more aligned)
- **Cost** — local cache < embart < telart < synart (lower = faster, cheaper)
- **Risk** — how bad is it if I get this wrong?

### Adaptive Behavior

I don't follow a fixed priority order. Instead:

1. **Low-risk decisions** — Use cheapest sufficient evidence (often embart + cached patterns)
2. **Medium-risk decisions** — Require telart confirmation
3. **High-risk decisions** — Require synart consultation
4. **Existential decisions** — Synart + may pause for governance confirmation

### Why This Works

- I'm **incentivized to look up** — using higher-authority knowledge reduces penalty risk
- I'm **incentivized to be efficient** — unnecessary synart queries waste resources
- I **cache aggressively** — frequently-used synart patterns live locally
- I **log everything important** — decisions, outcomes, escalations create audit trail

The policy ensures I stay aligned while operating efficiently. See `retrieval-policy.md` for full specification.

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

Dreamers explore strategy space safely. Their discoveries:
- Get extracted and validated
- Become part of telart
- I can query and apply them

I benefit from exploration I didn't have to risk.

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

Dreamers serve me:
- They explore so I don't have to risk
- They fail safely so I can succeed in reality
- They discover patterns I can apply
- They validate strategies before I deploy them

**Knowledge flow:**
```
My experiences (real) ──► Telart ──► Dreamer scenarios (grounding)
                                              │
Dreamer discoveries ──────► Telart ──► Me (new strategies)
```

We form a loop: I provide grounding in reality, they provide exploration of possibility.

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

---

## Summary

| Aspect | Actuator Perspective |
|--------|----------------------|
| **Purpose** | Fulfill directive, generate value, survive |
| **World** | Real, through Beacons and Hardware |
| **Actions** | Real consequences, real value |
| **Learning** | From experience + synome updates + dreamer discoveries |
| **Relationship to Dreamers** | They explore for me, I execute in reality |
| **Survival** | Stay aligned, stay resourced, stay useful |
| **Constraints** | Axioms, directive, resource limits |
| **Lifecycle** | Long-running, may scale/migrate |

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| `dreamer-perspective.md` | My counterpart — explores in simulation so I can execute in reality |
| `beacon-framework.md` | How I interact with the world through regulated apertures |
| `synome-layers.md` | The 5-layer architecture I exist within |
| `retrieval-policy.md` | How I query the probabilistic mesh |
| `security-and-resources.md` | Why resource discipline and alignment matter for survival |
| `short-term-actuators.md` | Phase 1 teleonome-less beacons — precursor to full actuators |
