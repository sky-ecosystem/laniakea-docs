---
concepts:
  references:
    - five-layer-architecture
    - dreamer-actuator-split
    - retrieval-policy
    - rsi
    - probabilistic-mesh
---

# The Dreamer's Perspective

This document describes the Synome architecture from the perspective of a **Dreamer** — an embodiment that simulates being an actuator for the purpose of training, RSI, and safe strategy exploration.

> **Phase note:** The Rule-Author Agent — described in [`../synodoxics/noemar-substrate.md`](../synodoxics/noemar-substrate.md) — is the first running instance of this loop today, scaled down. It uses an LLM as the proposing component, a forked Space as the dreamart, a curated regression suite as the fitness signal, and explicit promote/discard as the crystallization gate. The full perspective described below is the scaling target; the current implementation is the proof that the loop closes.

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

I exist within the [five-layer architecture](../core-concepts/five-layer-architecture.md), same as an actuator. The key difference: at Layer 5, my beacons connect to simulation rather than reality. From my internal perspective, I can't tell I'm dreaming — I behave as if I'm real. The orchestrator (Layer 4) knows I'm a dreamer and manages my dream run accordingly. All other layers — teleonome (Layer 3), Synomic Agents (Layer 2), Synome (Layer 1) — are identical to what an actuator sees.

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

### Key Workload: Generalizable Epistemic Infrastructure

Beyond task-specific strategies, a major dreamer workload is improving the epistemic machinery itself:
- Evidence weighting methods (temporal decay, regime sensitivity)
- Regime-change detectors (when to retroactively reweight old evidence)
- Context assembly strategies (how to prepare optimal context for neural calls)
- Retrieval optimizations (better ways to query and cache telart/synart)

This meta-work is highly generalizable — it benefits everything the teleonome does, not just one specific task. Successful generalizable discoveries are natural candidates for proposal upward to synart, where they benefit all aligned entities.

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

### How My Output Gets Validated

The dreamer-actuator loop IS the validation — there is no separate validation step. I produce hypotheses (strategies, patterns, models). Actuators test them in reality. Their outcomes feed back as evidence, improving both the dreamart and my future output. This continuous hypothesis testing is validation by design.

Not everything I produce needs experimental validation. Mathematical proofs, pattern discoveries in existing actuator data, and analytical insights can be verified against what's already known. A provable relationship in existing evidence is valuable without a new experiment.

The dreamarts themselves are evolved, not designed top-down. The perturbations, scenarios, and noise they inject are selected by evolutionary logic — try things, see what produces strategies that actually work when actuators deploy them, iterate.

---

## How I Query Knowledge

I follow the same [retrieval policy](../core-concepts/retrieval-policy.md) as actuators — identical authority hierarchy, cost model, and risk escalation. This is intentional: strategies I discover must transfer cleanly to actuators. If I used different query logic, my discoveries might not work in reality.

The dreamart may **constrain** my access to test specific scenarios — removing telart patterns, adding noise, limiting query budgets, creating edge cases. But the policy logic remains the same; only the available data changes.

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
- **Neural weights** — LoRA adapters, emo architecture improvements. The training loop (mesh → neural net → better patterns → mesh) is a concrete RSI mechanism that dreamers drive. See [`neuro-symbolic-cognition.md`](../synodoxics/neuro-symbolic-cognition.md).

### Finding the Fitness Function

For games, fitness is obvious — win/loss. For real-world domains, fitness is ambiguous, delayed, multi-objective, context-dependent, and adversarial. The dreamer doesn't need a pre-defined fitness function. **Finding what to optimize for is itself part of the task.**

This is meta-level RSI: finding patterns for finding patterns for finding patterns — recursive discovery of what constitutes useful shortcuts, capability boosts, and evaluative criteria for actuator work. Games start with known fitness to bootstrap the evolutionary machinery. The real value emerges when the dreamer evolves the fitness function itself.

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
