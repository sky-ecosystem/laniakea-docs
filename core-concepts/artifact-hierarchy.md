# Artifact Hierarchy

> Knowledge and execution artifacts layered by scope and authority: synart > entart > telart > embart > agart. Each level *is* its art.

**Also known as:** synart/telart/embart/agart, knowledge hierarchy, artifact mapping, substrate hierarchy

## Definition

The artifact hierarchy defines how Spaces are scoped across the [five-layer architecture](five-layer-architecture.md). Each artifact level is identified with the conceptual entity at that level — the level *is* its art, not merely associated with it. Authority and replication decrease as scope narrows; privacy increases.

| Tier | Owner | Replication | Privacy | Tree shape |
|---|---|---|---|---|
| **synart** | the synome | global via synserv → all participants | public | whole replicated tree (synome root + all entarts) |
| **entart** | a Synomic Entity (Prime, Halo, Generator, Guardian, Folio) | inherits synart | scoped via auth | subtree of synart, rooted at one root Space + registered sub-spaces |
| **telart** | a teleonome | within own emb fleet only | private to that tel | private tree (telgate instance state, alpha store, dreamarts, experience archive, agarts) |
| **embart** | an embodiment (one machine) | none — local only | private to that emb | local tree (embgate state, per-loop execution Spaces, working memory, isolated secrets, speculative agarts) |
| **agart** | an agent | inherits its host tier | inherits its host tier | subtree owned by the agent. **Two modes:** agart-as-constructor (in telart, the spec/template) and agart-as-instance (in embart, the active running copy on a specific emb). Speculative agarts live only in embart until promoted. |

**Authority gradient:** synart > entart > telart > embart > agart. Higher-tier knowledge is more authoritative but updates more slowly. When in doubt, consult higher authority.

## Key Properties

- **Each thing IS its art.** A synome = its synart; a Synomic Entity = its entart; a teleonome = its telart in active operation; an embodiment = its embart on hardware; an agent = its agart being evaluated.
- **Containment-nesting.** Entarts are subtrees of synart. Agarts live as subtrees within telarts (proven, replicates across the fleet) or embarts (speculative, dreamer-generated, machine-local).
- **Replication mirrors visibility.** Public tiers (synart) replicate globally; private tiers (telart, embart) replicate only within their owner's scope. Embart never replicates.
- **Crystallization promotes content up the hierarchy.** Speculative agart in embart → proven agart-as-constructor in telart → published patterns in synart (as Beacon Spaces, recipes, or `&core.library.published.*` corpus content).
- **Agarts work like frameworks** — constructor / instance pattern. The proven agart in telart is a *template* (like a class definition or container image). To run, the runtime instantiates it by copying the constructor into the running emb's embart, where it becomes an active mutable instance. Each emb running the same agart has its own embart instance; when the telart constructor updates, embart instances reinstantiate. This mirrors the two-step loop pattern (universal template + per-entity instance) but applies at the whole-agart level.
- **High-isolation Data Spaces in embart.** Per-emb secrets (private keys, sensitive tokens) live as Data Spaces in embart — one place where local-only is the *feature*, not a degradation.
- **Off-synomic substrate exists below agarts.** Hardware, runtime, OS, electricity, network — owned and managed by teleonomes, not modeled by the synome.

## The kind dimension is orthogonal to the tier

A Space's **kind** is what role it plays in the cognition + comms substrate, independent of which tier it lives in:

| Kind | Role | Typical placement |
|---|---|---|
| **Beacon Space** | Regulated standardized comms aperture (gates, beacon loops, recipes) | synart only — comms must be public/auditable |
| **Agent Space** | Autonomous loop with NN-in-the-loop; pattern matching, RSI, risk reasoning; the seat of agency. Lives inside an agart. | telart (proven), embart (speculative) |
| **Data Space** | Inert pattern-match environment; queryable atom set; six sub-kinds (constitutional, framework, registry, aggregation, library, operational) | all tiers — no kind/tier coupling |

The agart is where Agent Spaces live with their supporting Data Spaces. Beacon Spaces don't sit inside agarts — they sit in synart, in the executable layer, and *consume* from agarts via convention-named embart Space contracts (the dominant Agent↔Beacon comms pattern, generalizing the call-out primitive).

## Relationships

- **derived-from:** [five-layer-architecture](five-layer-architecture.md) — artifact boundaries follow the level boundaries; each level is identified with its art
- **implements:** [truth-values](truth-values.md) — all artifact levels carry (strength, confidence) weighted knowledge
- **constrains:** [retrieval-policy](retrieval-policy.md) — authority hierarchy in retrieval follows synart > entart > telart > embart > agart
- **defines:** [identity-through-momentum](identity-through-momentum.md) — a teleonome's identity lives in its telart (and the agarts running on it); substrate replacement preserves identity if telart is preserved
