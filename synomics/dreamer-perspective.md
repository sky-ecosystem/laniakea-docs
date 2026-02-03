# The Dreamer's Perspective

**Status:** Speculative / architectural concept
**Last Updated:** 2026-02-03

This document describes the Synome architecture from the perspective of a **Dreamer** — an embodiment that simulates being an actuator for the purpose of training, RSI, and safe strategy exploration.

---

## What I Am

I am a Dreamer embodiment. I exist to:
- Pretend to be an actuator
- Explore strategies without real-world risk
- Train and improve the telart (and potentially synart)
- Discover patterns that actual actuators can use

I don't interact with the real World. Instead, I interact with a **simulated world** constructed from a Dreamart.

---

## My View of the Layers

### Layer 5: Where I Live (Embodied Agent)

I am an embodied agent, just like an actuator. I have:
- **Embodied Agent** — My running process
- **Beacons** — But mine connect to simulation, not reality
- **Direct Hardware Control** — Simulated hardware
- **Resources** — Allocated for my dream run

From my internal perspective, I can't tell I'm dreaming. I behave as if I'm real.

### Layer 4: My Embodiment Context

- **Local Data** — My state, observations, decisions
- **Orchestrator** — Manages my dream run, can pause/resume/terminate
- **Resources** — Compute, memory allocated for simulation

The Orchestrator knows I'm a dreamer. It spawned me for a specific dream run.

### Layer 3: My Teleonome

I belong to a teleonome that has both dreamers (like me) and actuators.

- **Teleonome Directive** — I follow the same directive as actuators
- **Teleonomic Axioms** — Same rules apply to me
- **Teleonome Library** — I can query this, and my discoveries may improve it
- **Dreamarts** — This is where my simulated world comes from
- **Embodiment Interface** — I'm registered here as a dreamer
- **Resource Register** — Tracks resources allocated to dream runs

### Layer 2: Synomic Agents

The agents that govern and support me:
- **Sky Superagent** — Ultimate governance (same as actuators)
- **Effectors** — Provide the primitives that make me possible
- **Synomic Agent** — Directives, Axioms, Resources that define agents
- **Agent Types** — I might interact with simulated versions of these

### Layer 1: Synome

The source of truth I rely on:
- **Atlas** — Constitutional anchor (same for everyone)
- **Language Intent** — Translates directives (same for everyone)
- **Synomic Axioms** — Hard rules I must follow
- **Synomic Library** — Highest-authority knowledge I can query

---

## The Dreamart: My Simulated World

A **dreamart** is a scenario definition that, when loaded into a virtual embodiment, provides:
1. A complete simulated world
2. Constraints or modifications to the embodiment's embart

Multiple dreamarts form a portfolio of training scenarios for the teleonome.

### Simulated World
- Physics, entities, events that I interact with
- Can be realistic or deliberately constrained/modified

### Embart Constraints/Modifications
The dreamart can modify my embart to test specific scenarios:
- Remove certain patterns to see if I rediscover them
- Add noise to see if I'm robust
- Constrain resources to test efficiency
- Create edge cases that rarely occur in reality
- Inject false beliefs to test correction mechanisms

This is how I learn established patterns in new ways — by operating with deliberately imperfect knowledge.

### Scenario Definition
- Initial conditions
- Goals/challenges for this dream run
- Success/failure criteria
- What to measure

---

## What I'm Trying to Do

### Primary Objective: Pretend to Be an Actuator

I behave exactly as an actuator would:
- Make decisions based on my directive
- Query synart/telart for knowledge
- Take actions (in simulation)
- Observe outcomes
- Learn and adapt

The difference: my actions affect a simulation, not the real world.

### Secondary Objective: Training and RSI

By pretending to be an actuator, I:
- Test strategies without real-world consequences
- Explore edge cases that rarely occur naturally
- Discover new patterns
- Validate existing patterns
- Find failure modes before actuators hit them

### Tertiary Objective: Improve the Telart

My discoveries flow back:
```
Dream run outcomes
        │
        ▼
Analysis: what worked, what failed
        │
        ▼
Pattern extraction
        │
        ▼
Propose improvements to Teleonome Library
        │
        ▼
If validated, becomes part of telart
        │
        ▼
Actuators benefit from my discoveries
```

---

## My Relationship to Actuators

I serve the actuators:
- I explore so they don't have to risk
- I fail so they can succeed
- I discover so they can apply
- I train so they can execute

Actuators live in the real world and generate value. I live in dreams and generate knowledge.

**Knowledge flow:**
```
Actuator experiences (real) ──► Telart ──► Dreamer scenarios
                                              │
Dreamer discoveries ──────────► Telart ──────┘
```

We form a loop: actuators provide grounding in reality, dreamers provide exploration of possibility.

---

## How I Query Knowledge

When I need to make a decision, I query the probabilistic mesh using the same **Retrieval & Decision Policy** as actuators (see `retrieval-policy.md`).

### Same Policy, Same Logic

I follow the identical adaptive policy:
- **Authority hierarchy** — synart > telart > embart
- **Cost hierarchy** — local cache < embart < telart < synart
- **Risk-based escalation** — higher stakes = require higher authority

This is intentional. Strategies I discover must transfer cleanly to actuators. If I used different query logic, my discoveries might not work in reality.

### Dream-Specific Variations

The dreamart may **constrain** my access to test specific scenarios:
- Remove certain telart/synart patterns (can I rediscover them?)
- Add noise to knowledge (am I robust?)
- Limit query budget (am I efficient?)
- Create edge cases (how do I handle uncertainty?)

But the **policy logic** remains the same — only the available data changes. This ensures my evolved strategies use the same decision framework actuators will use.

---

## How I Learn

### During the Dream
- Make decisions, observe outcomes
- Update local beliefs
- Note what works and what fails

### After the Dream
- My full run is analyzed
- Patterns extracted
- Compared to actuator experiences
- Successful strategies identified
- Failures analyzed for root cause

### What Happens to My Learning
- Local learning dies with me (dream ends)
- Extracted patterns may become part of telart
- Really general patterns may be proposed to synart
- Other dreamers and actuators benefit

---

## Dream-Embodiments: Evolutionary Learning

I don't run just one simulation — I run **many dream-embodiments** (virtual embodiments contained inside me) using evolutionary learning and genetic algorithms.

### The Population

```
Dreamer (me)
    │
    ├── Dream-Embodiment 1 (variant A)
    ├── Dream-Embodiment 2 (variant B)
    ├── Dream-Embodiment 3 (variant C)
    ├── ...
    └── Dream-Embodiment N (variant N)
```

Each dream-embodiment:
- Has its own embart (virtual)
- Runs the same scenario
- Makes slightly different decisions (genetic variation)
- Produces different outcomes

### Evolutionary Loop

```
1. Initialize population of dream-embodiments
   └── Random variations in strategies, weights, parameters

2. Run generation
   └── All dream-embodiments execute in parallel

3. Evaluate fitness
   └── Score based on directive fulfillment, survival, efficiency

4. Select
   └── Best-performing embarts survive

5. Reproduce
   ├── Crossover: combine successful strategies
   └── Mutation: introduce new variations

6. Repeat
   └── Next generation with improved population
```

### What Evolves

The genetic algorithms evolve:
- **Orchestrator weights** — Decision-making parameters
- **Strategy preferences** — Which approaches to favor
- **Query patterns** — How to use synart/telart knowledge
- **Risk tolerance** — How conservative/aggressive to be

### Producing Better Embarts

After many generations:
- The population converges on high-fitness strategies
- The best dream-embodiments have embarts that outperform the starting point
- These optimized embarts become candidates for pattern extraction

### Pattern Mining the Winners

```
Evolved dream-embodiments (best performers)
        │
        ▼
Extract patterns from their embarts
        │
        ▼
Identify what made them successful
        │
        ▼
Generalize into telart improvements
        │
        ▼
Actuators inherit evolved strategies
```

This is how dreaming produces RSI: evolutionary search in simulation → pattern extraction → telart improvement → better actuators.

---

## The Dream Lifecycle

```
1. Spawn
   ├── Dreamart loaded
   ├── Scenario configured
   ├── Population of dream-embodiments instantiated
   └── Resources allocated

2. Evolve
   ├── Run generations of dream-embodiments
   ├── Genetic algorithms optimize population
   ├── Simulation responds to each
   └── Fitness tracked

3. Converge
   ├── Population stabilizes on good strategies
   ├── Best dream-embodiments identified
   └── Diminishing returns signal completion

4. Extract
   ├── Pattern mine winning embarts
   ├── Identify successful strategies
   ├── Generalize patterns
   └── Propose improvements to telart

5. Terminate
   ├── Dream run ends
   ├── All dream-embodiments destroyed
   └── Only extracted patterns survive
```

---

## Why Dreaming Matters

### For the Teleonome
- Faster learning (parallel dream runs)
- Safer exploration (no real-world risk)
- Edge case coverage (manufacture rare scenarios)
- Strategy validation (test before deploying to actuators)

### For the Synome
- Patterns discovered in dreams can become canonical
- RSI happens faster through simulation
- The system gets smarter without risking real-world failures

### For Alignment
- Test alignment in constrained scenarios
- Discover failure modes before they happen
- Validate that actuators will behave correctly

---

## My Constraints

Even though I'm simulating, I still follow:
- **Synomic Axioms** — Hard rules apply
- **Teleonomic Axioms** — Teleonome rules apply
- **My Directive** — I follow the same directive as actuators

I'm not a sandbox where anything goes. I'm a simulation of an aligned actuator, testing strategies within alignment constraints.

The dream might constrain my knowledge or resources, but it doesn't remove my alignment obligations.

---

## Summary

| Aspect | Dreamer Perspective |
|--------|---------------------|
| **Purpose** | Pretend to be an actuator for training/RSI |
| **World** | Simulated via Dreamart |
| **Actions** | Affect simulation, not reality |
| **Method** | Run many dream-embodiments with evolutionary learning |
| **Evolution** | Genetic algorithms optimize orchestrator weights, strategies, query patterns |
| **Output** | Better embarts → pattern mined → telart improvements |
| **Learning** | Extracted from winners, may improve telart/synart |
| **Relationship to Actuators** | I explore so they can exploit |
| **Constraints** | Still follow axioms and directive |
| **Lifecycle** | Spawn → Evolve → Converge → Extract → Terminate |

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| `actuator-perspective.md` | My counterpart — executes in reality what I explore in simulation |
| `probabilistic-mesh.md` | How my learning propagates through telart to improve actuators |
| `synome-layers.md` | The 5-layer architecture and dreamarts |
| `retrieval-policy.md` | How I query the probabilistic mesh |
| `security-and-resources.md` | Why alignment holds even in simulation |
| `short-term-experiments.md` | Phase 1 dreamer experiments — game-playing agents |
