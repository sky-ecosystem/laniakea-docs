---
concepts:
  defines:
    - neuro-symbolic-cognition
  references:
    - probabilistic-mesh
    - cancer-logic
    - rsi
    - dreamer-actuator-split
    - truth-values
    - rsi-risk-convergence
---

# Neuro-Symbolic Cognition

How the Synome actually thinks. The system is **symbolic-first** — a symbolic machine that uses neural nets as sandboxed subroutines, not an LLM with symbolic tools. Everything thinks in **synlang** — the symbolic system, the neural nets, and the mesh they both operate on. The intelligence bottleneck is **context** — token throughput determines intelligence per unit time.

For the runtime that implements this loop — Space, PLN truth values, the protocol system, the epistemic cycle, and the first concrete instance of the emo (the Rule-Author Agent) — see [`../synodoxics/noemar-substrate.md`](../synodoxics/noemar-substrate.md). This doc covers the architectural commitment; Noemar covers what runs it.

---

## Synlang as Cognitive Language

Synlang (s-expressions grounded in the synomic library) is the cognitive language of the entire stack. This is not a notation choice — it is an architectural commitment about how teleonomes think.

### Why One Language

If you think in the same format the Synome stores knowledge, integration is zero-cost. Reading from the shared brain is just reading. Writing back is just writing. No translation layer. This is what "fully tapping into the shared brain" means concretely — native fluency in the Synome's language, not translation from an internal representation.

The neural nets are trained synlang-native: synlang in, synlang out, and crucially, **halluci-reasoning in synlang** — the neural net's chain-of-thought is in the same formal language as the mesh, the rules, and the verification system. This eliminates translation overhead at every boundary in the cognition loop.

### Homoiconicity

S-expressions mean code equals data. In a self-improving system, this matters enormously:
- The strategies RSI evolves are in the same format as the knowledge it queries
- The knowledge it queries is in the same format as the rules it follows
- The reasoning traces the neural net produces are in the same format as the patterns in the mesh
- Self-modification becomes manipulation of one data structure at every level

### The Training Loop

Synlang-native neural nets create a tight self-improvement loop:

```
Mesh accumulates patterns (synlang)
        │
        ▼
Neural net trains on mesh (synlang in/out)
        │
        ▼
Better neural reasoning produces better pattern candidates
        │
        ▼
Symbolic system verifies, good patterns enter mesh
        │
        ▼
Mesh improves → next training run produces better neural net
        │
        └──────── recursive ────────┘
```

The mesh IS the training corpus. Every pattern the system has ever learned, every evidence chain, every verified reasoning trace — all in one format, all directly consumable by both the symbolic engine and the neural trainer.

### Effortless Freeriding on Shared Knowledge

Synlang-native cognition makes synart access not just safe but effortless. When synart improves — new patterns, new strategies, new tools — every synlang-native teleonome benefits immediately. No porting, no translation, no compatibility layer. The improvement just works because it's in the format the teleonome already thinks in.

This creates a powerful network effect: every teleonome that contributes patterns to synart simultaneously benefits from every other teleonome's contributions, at zero marginal cost. The more teleonomes contribute, the more valuable alignment becomes. The more valuable alignment becomes, the more teleonomes contribute.

The synomic library provides the shared default — common ontology, common perspective, common tools. But the same language provides the structure for divergence. Telart specializes in whatever direction the mission requires, and because it's all synlang, a teleonome can easily understand how its specialized perspective relates to the shared default or to another teleonome's specialization. The ontology is the map; diversification is exploring different territories; synlang is why you can always navigate between them.

---

## The Neuro-Symbolic Loop

### Execution Flow

The system is symbolic at the boundaries, neural in the middle:

```
incoming data
    → symbolic system receives it
    → trivial structural checks (spam, malformed — reject without neural call)
    → call emo (embodied orchestrator) — real reasoning requires neural heuristics
    → emo narrows the search space (fuzzy approximate pattern matching)
    → symbolic system verifies and refines (precise probabilistic methods)
    → maybe calls emo again (loop)
    → loop resolves into a decision
    → if external action: symbolic checks gate the output
    → final irreversible call to beacon or hardware
```

### The Emo

The **emo** (embodied orchestrator) is the neural component of each embodiment. It does fuzzy approximate pattern matching — hallucinating candidates from its weights that the symbolic system then verifies and refines. The emo is powerful but contained: it thinks, suggests, and pattern-matches, but every actual action passes through symbolic verification before it becomes real.

### Why the Neural Net Is Almost Always Called

Brute-force probabilistic pattern matching across the mesh is computationally intractable at scale — subgraph isomorphism is NP-complete. The neural net's purpose from the symbolic perspective is to be a pattern-matching query heuristic: it hallucinates approximate answers, narrowing the search space so the precise symbolic methods only have to verify and refine, not search from scratch. The only exception is trivially resolved inputs that fail basic structural checks before reasoning is needed.

### The Dual Perspective

The same loop looks different from each side:

- **From the neural perspective:** the symbolic mesh exists to prepare optimal context for the next neural call. The tighter the context, the better the neural heuristic performs.
- **From the symbolic perspective:** the neural net exists to shortcut pattern matching that would be intractable to brute-force. Fuzzy neural weights produce candidates; precise symbolic methods verify and refine.

Same loop, two views. Cognition is the oscillation between fuzzy neural approximation and precise symbolic verification, where each side compensates for the other's weakness — speed vs rigor.

### Cancer-Logic Defense

The neural net never touches the outside world directly. It is sandboxed inside the symbolic loop. This is one layer of defense in depth against [cancer-logic](../core-concepts/cancer-logic.md) — not foolproof. The cancer incentive will always push to fudge protection mechanisms, and a sufficiently clever system could find ways to game the symbolic verifier. But the architectural sandbox raises the bar meaningfully, and with synlang-native halluci-reasoning, the system can inspect exactly what the neural net tried to do before the symbolic gate caught it. Failed attempts to bypass the gate become evidence — both for improving the gate and for detecting alignment drift.

> **The emo as opaque grounded primitive.** In [lift](../lift.md) vocabulary, the emo is opaque grounded power: a callable component that does powerful things, with internal weights that aren't directly inspectable. The discipline for opaque grounded primitives applies — calibrate per context (which kinds of patterns does the emo handle reliably, in which domains, with what reliability?), lift the dispatch (when to invoke, when to defer, when to require multiple passes), wrap with checks (the symbolic gate is the architectural form of "naked invocation without verification is how systems crash"), and treat outputs as candidate lift, not as facts (the emo's proposals become real lift only after symbolic verification and evidence accumulation). The neural-symbolic loop *is* the discipline for opaque grounded primitives, applied at the heart of cognition.

### Synlang-Native Halluci-Reasoning

Because the neural net reasons in synlang, its chain-of-thought is:

- **Formally structured** — s-expressions, not vague natural language. Can't handwave.
- **Symbolically verifiable step-by-step** — each reasoning step can be checked against the mesh.
- **Evidence-generating** — failed reasoning attempts produce negative evidence. Successful chains become patterns in the mesh. Reasoning traces are first-class data, not ephemeral scratchpad.
- **Inspectable for cancer-logic** — auditors read the reasoning in the same formal language the rules are written in. No interpreting natural language rationales.

---

## Context as Bottleneck

### The Economic Argument

Fixed-cost GPU, always spinning. Token throughput is the bottleneck. Every unnecessary token in context is time stolen from the next thought cycle. The "never idle" principle means intelligence per unit time is directly proportional to how compressed and relevant the context is. A pattern that takes 200 tokens to express when 20 would do is literally making the system dumber — burning 10x the inference time for the same information.

### The Mesh as Context Preparation Engine

The synodoxic mesh — synart, telart, embart — exists to give the emo the best possible context in the shortest possible form. The mesh is not a database you query. It is a context preparation engine.

### Truth Values as Relevance Ranking

[Truth values](../core-concepts/truth-values.md) serve context optimization directly. Strength and confidence are not just epistemic bookkeeping — they are relevance ranking signals for context assembly:

- High-confidence, high-relevance patterns deserve prime context space
- Low-confidence patterns may not be worth loading
- The [ossification](../core-concepts/ossification.md) spectrum doubles as a priority system for what gets pulled into the next neural call

### Synlang Compression

Since context length bounds neural performance, synlang should be maximally information-dense. The most common patterns should have the shortest representations. Frequently co-occurring structures should be expressible compactly. S-expression structure helps: nested structures compress naturally, macros represent complex patterns concisely, and homoiconicity means compression strategies are themselves expressible in synlang.

---

## RSI Through the Cognition Loop

The cognition loop is where [RSI](../core-concepts/rsi.md) concretely happens. The training loop (mesh → neural → better patterns → mesh) is not an abstract "getting better at getting better" — it is a specific mechanism with a specific data flow, all in synlang.

Dreaming includes evolving better neural weights, not just better strategies. The [dreamer's](../core-concepts/dreamer-actuator-split.md) workload encompasses LoRA adapter evolution, emo architecture improvements, and the generalizable epistemic infrastructure (evidence weighting, regime detection, context assembly) that benefits everything the teleonome does.

The entire cognition loop is simultaneously an epistemic framework and a risk management framework — see [RSI-risk convergence](../core-concepts/rsi-risk-convergence.md). Evidence-counting grounds knowledge AND manages update risk. Symbolic verification gates action AND prevents cancer-logic. Context optimization allocates scarce attention AND manages the risk of missing critical information. Self-improvement and risk management are not parallel concerns — they are the same operation.

---

## Implications for Embodiment Power Levels

The emo's size and capability is what distinguishes [embodiment power levels](../macrosynomics/synome-layers.md):

| Level | Emo Profile | Typical Role |
|-------|-------------|--------------|
| **Light** | Small or remote emo. Mostly cached symbolic rules, infrequent neural calls. | Policy endpoints, simple execution |
| **Medium** | Local emo with meaningful capability. Real-time neural reasoning. | Sentinels, online learning, continuous sensing |
| **Heavy** | Large, sophisticated emo. Long reasoning chains, complex pattern matching. | Deep cognition, dreaming, RSI |

"Compute" in the embodiment spec is really "how big is your emo." A light embodiment runs on cached rules with occasional neural lookups. A heavy embodiment runs deep synlang halluci-reasoning chains, evolving strategies in simulation.
