# Atlas/Synome Separation

> Split human-readable constitutional document (Atlas, ~10-20 pages) from machine-readable operational data (Synome, unlimited), with Atlas embedded as the root node of the Synome.

**Also known as:** Atlas/Synome split, two-layer separation, constitutional separation

## Definition

The Atlas/Synome separation resolves the fundamental tension between comprehensive machine-readable documentation and human-readable governance. The Atlas is a short (~10-20 pages), human-readable constitutional document describing WHAT must be true — principles, rules, definitions. The Synome is a graph database containing ALL operational data structured for machine consumption — parameters, state, transactions, rate limits, contract addresses.

The Atlas is embedded IN the Synome as its root node, not separate from it. It's the human-interpretable entry point to a machine-readable system. The Synome can grow arbitrarily complex; the Atlas stays manageable.

This enables Synomic Agents (Primes, Halos) to be fully autonomous: they exist entirely within the Synome, cannot escape their constraints, and can operate without human oversight for individual decisions. The "Mini-Atlas" fractal pattern replicates this at every level — each entity with human stakeholders gets a human-readable summary of its relevant Synome nodes.

## Key Properties

- Atlas describes intent (WHAT); Synome encodes implementation (HOW)
- Atlas: natural language, compact, human-verified through governance votes
- Synome: structured/typed data, unlimited, machine-verified through constraint checking
- Verification model: humans verify Atlas reflects values; machines verify Synome conforms to Atlas
- The Bridge: Atlas assertions map to Synome constraints (e.g., "encumbrance ratio target <= 90%" becomes a formal invariant)
- Synomic Agents cannot deviate — protecting humans from each other, enabling cooperation without trust
- Escalation to human reasonableness: 99% automated, 1% edge cases reach human judgment — "smart contracts with a backstop"

## Relationships

- **requires:** [language-intent](language-intent.md) — Language Intent translates Atlas principles into machine constraints
- **motivates:** [governance-window](governance-window.md) — the urgency of getting the Atlas right while humans can still read and evaluate it
- **enables:** [beacon-framework](beacon-framework.md) — beacons derive authority envelopes from Synome governance
- **implements:** [five-layer-architecture](five-layer-architecture.md) — the separation structures Layers 1 and 2
