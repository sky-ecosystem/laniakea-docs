---
concepts:
  references:
    - probabilistic-mesh
    - truth-values
    - cancer-logic
---

# Live Graph Context

The context window for a synlang-native emo is not a static text buffer. It is a **live reactive view into the probabilistic mesh** — concretely, into Noemar's Space. The s-expressions loaded into context are rendered views of graph nodes, and the underlying graph is alive — other emas are writing to it, evidence is flowing in, truth values are shifting, the orchestrator is updating priorities. Context can go stale between turns.

This is fundamentally different from how current LLMs work. Current LLMs reason over frozen text. The Synome's emos reason over rendered views of a living graph.

For the runtime that supplies the live graph — Space semantics, three-layer query resolution, evidence-stamped beliefs — see [`../synodoxics/noemar-substrate.md`](../synodoxics/noemar-substrate.md).

---

## Context as Rendered View

Each s-expression in the emo's context is not a copy of data — it's a **rendered view with a live binding** to its source in the mesh:

- A **rendered value** — the s-expression tokens the emo sees
- A **binding** to a graph location — where it came from
- A **version** — when it was rendered

The symbolic system manages the rendering. The emo sees s-expressions and reasons over them. The infrastructure underneath is a reactive data binding system, not a text buffer.

When the underlying graph node changes — new evidence, updated truth value, modified by another ema — the rendered view becomes stale. The binding still points to the same graph location, but the rendered value no longer matches the live state.

---

## Staleness Is the Default

In a live multi-agent mesh, things are always changing. The question isn't "did something change?" — it's "did something relevant change enough to matter?" Staleness is normal. Perfect freshness is neither achievable nor necessary.

The symbolic gate — the final check before any real action — always verifies against the **live graph**, never a cached view. This means staleness in the emo's context is an **efficiency problem, not a safety problem.** The worst case of stale context is wasted inference cycles: the emo reasons from outdated premises, produces a conclusion, the symbolic gate catches that the premises changed, the conclusion is discarded, and the emo re-reasons with fresh context.

The cost of staleness is wasted compute. The evidence process naturally optimizes against it — if a particular attention configuration leads to frequent "conclusion rejected, premise stale" events, that's negative evidence on the configuration. The system learns how aggressively to refresh per domain without needing hard invariants.

---

## Between-Turn Reconciliation

Between inference turns, the symbolic system reconciles the emo's context with the live graph:

1. **Check bindings** — which rendered values have gone stale? (Cheap — version comparison on bound graph nodes.)
2. **Classify changes** — how significant? A truth value shifting from (0.81, 0.90) to (0.82, 0.90) is noise. A shift from (0.8, 0.9) to (0.2, 0.95) is a regime change.
3. **Decide response:**
   - **No significant changes** → proceed, maybe annotate "stable since last turn"
   - **Minor changes** → patch context differentially — the emo sees the delta, not just the new value. Deltas are more informative than snapshots.
   - **Major changes** → rebuild the affected portion of context from scratch
   - **Premise invalidation** → flag that a key premise of the current reasoning chain has been undermined

The rebuild-vs-patch tradeoff is itself a learned behavior. Rebuilding every turn is precise but expensive. Patching is fast but can accumulate incoherence if too many small changes pile up. The right strategy is domain- and stakes-dependent, discovered through experience.

---

## Snapshot Isolation Within Turns

Within a single inference pass, the context does not mutate. The emo reasons over a consistent snapshot. Live bindings update between turns, not during. The turn boundary is where the system reconciles its view with reality.

This creates a tradeoff on turn length:
- **Shorter turns** — fresher views, more reconciliation overhead, less reasoning depth per turn
- **Longer turns** — deeper reasoning per turn, higher staleness risk, less reconciliation overhead

Another learned tradeoff. Fast-moving domains favor shorter turns. Deep analytical reasoning favors longer turns. The system discovers the right cadence.

---

## The Navigation Layer Is Also Live

The always-loaded navigation layer (see [`attention-allocation.md`](attention-allocation.md)) is bound to live graph nodes too. If another ema's findings shift a navigation pointer's confidence, or the orchestrator reprioritizes, the navigation layer changes — not because the emo decided to update it, but because the underlying graph changed.

Periodic maintenance handles **structural** updates (add pointers, remove stale ones, recompress). Live bindings handle **value** updates continuously.

---

## Change Provenance

When something changes between turns, the emo benefits from knowing not just *what* changed but *why* and *who*:

- "Credit spread strength dropped because ema-finance-3 observed new market data" → real-world evidence, probably important
- "Credit spread strength dropped because a dreamer updated its model" → model revision, evaluate carefully
- "Credit spread strength dropped because the orchestrator overrode it" → governance action, respect it

Provenance shapes how the emo should respond. The change annotation is itself structured data in the reconciliation — part of the context the emo reasons over.

---

## Multi-Ema Consistency

When multiple emas read from the same graph, they see different states at different times. The graph is shared; the views are per-ema. Two emas reasoning about the same patterns might work from slightly different snapshots.

This is a feature, not a bug — diversity of perspective at the view level, consistency at the graph level. The graph is the single source of truth. Ema views are approximate, local, task-specific renderings of that truth. The symbolic gate ensures consistency at the action boundary — before any real action, the live graph is checked, regardless of which ema's view proposed the action.

---

## Concrete Data Model

The abstract "live reactive view" described above rests on a concrete data model for the graph itself:

- **Claims** are canonical s-expressions: `(rate-limit spark 25% 18h)` or `(price-direction ETH up)`. Identity is the hash of the canonical form.
- **Truth values are an optional overlay**, not baked into the storage model. Any claim can have a TV annotation as another pattern in the graph: `((price-direction ETH up) TV 0.6 0.8)`. Claims without TVs are just facts.
- **The graph is a knowledge graph first.** TVs, evidence logs, and probabilistic update rules are layered on top — not the other way around. Some claims are governance facts with no TV. Some are probabilistic beliefs with rich evidence histories. The storage model handles both.
- **Bindings in rendered context** carry the claim ID, version, and current TV (if any): `(bind claim:a7f3 (ver 91) (expr (price-direction ETH up)) (tv 0.6 0.8))`.

This separation means truth values can come from anywhere — accumulated evidence (e.g., a Beta distribution over support/contradiction counts), governance fiat, external model output, or manual override. The graph doesn't care how the numbers got there. The query engine filters on TVs when they exist and ignores them when they don't.

See [`../synodoxics/probabilistic-mesh.md`](../synodoxics/probabilistic-mesh.md) for the full probabilistic mesh specification.
