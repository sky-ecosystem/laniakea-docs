# Five-Layer Architecture

> The Synome's structural model: five nested levels, each identified with its substrate (an "art").

**Also known as:** 5-layer architecture, the layers, layer model, substrate hierarchy

## Definition

The Synome architecture consists of five nested levels, each identified with a corresponding **artifact** — a tree of Spaces that *is* the level. The hierarchy moves from the public commons down to the unit of agency:

| Level | Substrate | What it is |
|---|---|---|
| **Synome** | **synart** | Public constitution + commons; the whole replicated tree |
| **Synomic Entities** | **entarts** | Ledger-native institutional shells (Primes, Halos, Generator, Guardian, Folio); each owns an entart, a subtree of synart |
| **Teleonomes** | **telarts** | Autonomous willing entities with directives and missions; private tree replicated within own emb fleet |
| **Embodiments** | **embarts** | Physical machines hosting agents and beacons; local tree, never replicated |
| **Agents** | **agarts** | Programs in their own subtree of Spaces (loop body, working memory, scratch, experience, I/O contracts); the unit of agency |

**Each level *is* its art.** A synome is just its synart; a Synomic Entity is just its entart; a teleonome is just its telart in active operation; an embodiment is just its embart on a piece of hardware; an agent is just its agart being evaluated by a runtime. The substrate-correspondence is the identity, not a separable association.

Layers 1-2 are public and replicated; layers 3-5 are private. Below the agent (Layer 5) is hardware and infrastructure that is **off-synomic** — the substrate the teleonome pays for and manages but the synome does not model.

## Key Properties

- **Substrate-as-identity** — each level is identified by its art; no separation between "the thing" and "its substrate of Spaces"
- **Containment-nesting** — entarts are subtrees of synart; agarts live as subtrees within telarts (proven) or embarts (speculative)
- **Layers 1-2 public, 3-5 private** — replication and visibility match the trust gradient
- **Standardization gradient on comms** — syngate (max standard) → telgate (standard spec, per-tel instance) → embgate (deliberately non-standard, per-tel opsec). Visibility is the inverse of standardization at every tier.
- **Embodiment power levels** — light (policy execution), medium (continuous local intelligence, sentinel formations), heavy (deep cognition, dreaming, RSI)
- **All enforcement bottoms out in embodiments** — physical infrastructure is the ultimate enforcement boundary; embodiments are owned by teleonomes, which manage them off-synomically (electricity, hardware rent, opsec, key management)
- **Intelligence private, power regulated** — agents (cognition) live in agarts in private tiers; their action surface is regulated through Beacon Spaces in synart; the call-out / convention-named embart Space pattern is the seam between them
- **Every level has a human-readable directive** translated by Language Intent (Atlas, Entity Directive, Teleonome Directive)
- **Agents are the unit of agency** — below agents is off-synomic infrastructure (runtime, OS, hardware); the architecture stops modeling beneath this level
- **Agarts are constructor/instance** — proven agarts in telart are *templates* (like class definitions or container images); to run, the runtime instantiates the constructor by copying it into a specific emb's embart, where it becomes an active mutable instance. Each emb has its own instance; speculative agarts in embart have no telart constructor until promoted

## Relationships

- **contains:** [artifact-hierarchy](artifact-hierarchy.md) — the levels define the artifact boundaries (synart > entart > telart > embart > agart)
- **implements:** [dual-architecture](dual-architecture.md) — the levels carry both deontic skeleton and probabilistic mesh
- **constrains:** [beacon-framework](beacon-framework.md) — beacon sophistication is constrained by embodiment power level; beacons are how agents act on the world legibly
- **requires:** [language-intent](language-intent.md) — every level's human directive passes through Language Intent
- **defines:** [identity-through-momentum](identity-through-momentum.md) — a teleonome IS its telart in active operation (its agarts running on its embodiments); identity persists through substrate change as long as continuity holds
