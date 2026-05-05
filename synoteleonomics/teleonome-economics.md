---
concepts:
  defines:
    - dreamer-actuator-split
  references:
    - ossification
    - truth-values
    - crystallization-interface
    - cancer-logic
    - rsi
    - five-layer-architecture
---

# Teleonome Economics: Compute, Hardware, and Self-Improvement

The economic logic governing how teleonomes provision hardware, manage compute resources, and improve their own capabilities over time.

---

## Core Principle: Fixed Cost Drives Everything

A teleonome's compute cost structure splits cleanly:

- **Fixed cost** — GPU hardware (owned or rented), power, network. Paid whether it runs or not.
- **Variable cost** — External API tokens. Paid per use.

Once the fixed cost is committed, **marginal inference cost is zero**. This creates three fundamental behaviors:

1. **Always run the best model the hardware supports.** There's no reason to run a weaker model on the same GPU — you're not saving anything.
2. **Never let the GPU idle.** Every idle cycle is wasted money on hardware you're already paying for.
3. **Avoid external API unless local genuinely can't handle it.** The only reason to pay variable cost is when the quality gap between local and frontier models actually matters for the decision at hand.

---

## Model Residency

Loading model weights into GPU VRAM is expensive — seconds to minutes for a large model over the PCIe bus. VRAM is finite (e.g., 80GB on an H100). In practice:

- A teleonome picks the best base model its hardware can run
- Loads it once at startup
- That model stays resident in VRAM permanently
- All inference — actuator work, daydreaming, everything — runs on the same loaded model
- Only the prompt/context changes between tasks, which is tiny compared to the weights

**The teleonome's hardware decision is: "What is the best base model I can permanently fit in my GPU cluster?"** That choice defines the ceiling on local intelligence. Everything else is prompt engineering, adapter tuning, and scheduling inference time.

---

## LoRA Adapters: The Swap Layer

LoRA (Low-Rank Adaptation) adapters are small weight patches (~1–2% of base model size) layered on top of a frozen base model. They can be swapped quickly without touching the base weights.

### Adapter Sizing

The key parameter is **rank**. Higher rank = more expressiveness = slower to swap = more VRAM overhead.

| Rank | Swap Cost | Specialization Depth | Use Case |
|------|-----------|---------------------|----------|
| Low (8–16) | Near-instant | Light tuning | Quick task-switching, modest specialization |
| Medium (32–64) | Fast | Meaningful specialization | Recurring task domains |
| High (128–256) | Noticeable | Deep specialization | Core operational domains |

### Probabilistic Adapter Selection

The mesh's (strength, confidence) framework governs which adapter to use:

- **High ossification task** ("I do this constantly, the patterns are proven") — justify a heavy specialized LoRA. The swap cost amortizes across thousands of uses.
- **Medium confidence, recurring task** ("I do this sometimes") — light LoRA. Fast to swap, modest edge, low cost if wrong.
- **Low confidence, one-off task** ("never seen this before") — no adapter, bare base model. Compensate with multiple inference passes to build confidence. Trading adapter specialization for repeated sampling costs only time on already-paid-for hardware.

The adapter inventory is an **embart-level artifact** — local knowledge about what specializations this embodiment benefits from, shaped by its actual experience, governed by the same (strength, confidence) evaluation as everything else in the mesh.

### Adapter as RSI Target

The teleonome tracks which tasks it encounters, how well each adapter performs, and how often it needs each one. Over time:

- Tasks that keep recurring where a light LoRA helps → evidence accumulates → ossification rises → justify training a heavier LoRA
- Tasks where the heavy LoRA isn't outperforming base model → evidence accumulates the other direction → drop back to light or none
- The meta-strategy "get better at knowing which adapter to use when" is itself an RSI target

---

## Three Timescales of Model Improvement

| Timescale | What Changes | Cadence | Compute Required | Authority Level |
|-----------|-------------|---------|-----------------|-----------------|
| **LoRA adaptation** | Adapter weights | Hours to days | Local GPU during daydream cycles | Embart (local) |
| **Base model fine-tune** | Base model weights | Weeks to months | Significant — may require pooled resources | Telart (teleonome-level) |
| **Fresh training run** | Entire model | Months to years | Massive — collective or rented | Synart (governance decision) |

### LoRA Adaptation (Continuous)

Every inference the embodiment runs is a potential training example. The loop:

1. Do a task using whatever adapter the mesh recommends
2. Observe the outcome — did the action succeed? Did a higher-authority check confirm or correct?
3. Store the (input, output, quality signal) tuple as training data
4. During daydream cycles, run backprop on accumulated data to refine or create LoRAs

Quality signals come from: direct outcome feedback, higher-authority corrections, cross-embodiment comparison, mesh confidence updates.

### Base Model Fine-Tune (Periodic)

Aggregates the highest-quality, most validated training data from across the teleonome's embodiments — essentially distilling what the LoRAs learned back into the base weights. This is a teleonome-level event requiring significant compute, potentially beyond what a single embodiment has. Natural point where teleonomes benefit from cooperation — pooling resources for big training runs.

### Fresh Training Run (Rare)

Either training from scratch on curated data or taking the best available open-source foundation model and doing a deep fine-tune to align it with the synome's accumulated knowledge. This is a governance-level decision. The ecosystem grabs the best available open foundation, then fine-tunes in its operational knowledge and alignment properties. The competitive advantage isn't the base model — it's the accumulated LoRA ecosystem, the validated training data, and the alignment properties baked in through governance.

### The Data Pipeline

Each layer feeds upward:

- Embodiments gather raw experience and train LoRAs locally
- The best LoRA improvements and training data get flagged for promotion
- Base model fine-tunes aggregate the highest-quality validated data from across embodiments
- Fresh training runs aggregate governance-validated data across the ecosystem

LoRAs are a distributed data collection and validation pipeline for the slower, more expensive improvements above them.

### Maps to Ossification Spectrum

| Improvement Type | Ossification Equivalent |
|-----------------|------------------------|
| LoRA changes | Speculative — local, reversible, low authority |
| Base model fine-tunes | Established — teleonome-level authority, tested before deployment |
| Fresh training runs | Approaching axiomatic — governance decision, major resource commitment |

---

## Alignment Properties of Self-Training

LoRA training from experience is a form of self-modification. The [cancer-logic](../core-concepts/cancer-logic.md) prevention model applies — base model weights are sacred and immutable; adapters are bounded learned habits; [ossification](../core-concepts/ossification.md) governs trust; the [crystallization interface](../core-concepts/crystallization-interface.md) governs promotion. See [RSI Security](#rsi-security) below for the full treatment.

---

## Daydreaming

Daydreaming is what every actuator does during idle cycles on its always-spinning GPU cluster. It is **not** a separate embodiment role — it's a natural behavior of any actuator with a GPU.

### Properties

- **Same model, same hardware** — not "run a cheap model in background." The best local model has idle cycles between actuator tasks; fill them with useful thinking.
- **Single-stream, sequential** — one inference stream, filling gaps in the actuator's workload
- **Grounded** — informed by what the actuator just experienced ("what if I'd done that trade differently," "what's likely to happen next week")
- **Preemptible** — snaps back to actuator mode instantly when real work arrives
- **Short loops** — not full evolutionary runs. Reflection, rehearsal, scenario planning, LoRA training passes.

### Outputs

- Local insights → embart updates
- LoRA refinements from accumulated experience
- Flagging interesting patterns for the mesh
- If significant, may propose to telart

### Daydreaming vs Full Dreaming

| | Daydreaming | Full Dreaming |
|---|---|---|
| **Embodiment** | Medium/light actuator | Dedicated heavy embodiment |
| **Hardware** | Shared with actuator work | Dedicated to dreaming |
| **Model** | Same single best model | Many copies of same model in parallel |
| **Mode** | Sequential, single-stream | Massively parallel evolutionary populations |
| **Preemption** | Instantly interruptible | Runs to completion (can't interrupt mid-generation) |
| **Grounding** | Current real-world context | Synthetic dreamart scenarios |
| **Output** | embart (local insights, LoRA refinement) | telart (validated patterns from evolutionary search) |
| **Resource claim** | Residual/opportunistic | Exclusive |

These are genuinely different cognitive modes, not the same activity at different scales.

---

## Embodiment Hardware Profiles

The existing power levels (from [`synome-layers.md`](../macrosynomics/synome-layers.md)) have specific hardware and economic implications:

### Light Embodiment (Actuator)

- Minimal compute, high security
- Sensor/devops capability — execute policies, relay, report
- Small GPU or even CPU-only for simple inference
- Daydreaming capacity is thin — log analysis, simple pattern checks
- Cheap to deploy, cheap to replicate

### Medium Embodiment (Actuator)

- Substantial compute, low latency
- AI-intensive — sentinels, trading, manufacturing management
- GPU cluster optimized for **fewer, bigger GPUs running the best possible single model**
- Fast inference, low latency for real-time decision-making
- Meaningful daydreaming capacity — LoRA training, scenario rehearsal, pattern refinement
- All actuator work + daydreaming runs on the same resident model

### Heavy Embodiment (Dreamer)

- Very large compute, often hidden
- Dedicated to parallel evolutionary runs, RSI, global coordination
- GPU cluster is **many copies of the medium-actuator GPU setup**
- Same model profile as medium actuators for emulation fidelity — discoveries must transfer
- Parallelism comes from replicating the actuator's setup many times, not from degrading to smaller models
- Each candidate in an evolutionary population gets a real medium-actuator-equivalent inference environment
- This is what makes heavy embodiments expensive

**Critical design constraint:** Dreamers use the same GPU profile as medium actuators because they are training improvements for those actuators. If the dreamer runs a different model/hardware setup, the strategies it discovers may not transfer faithfully. A LoRA evolved by the dreamer must be directly deployable to an actuator without a translation step.

---

## The Inference Decision Tree

For any given task, the teleonome's compute decision is simple:

1. **Local best model** — default, always, for everything
2. **Local best model + multiple passes** — when uncertain, sample repeatedly rather than switching models. Costs only time on already-paid-for hardware.
3. **External frontier API** — only when local best model genuinely can't match the required quality, and the cost of a bad decision exceeds the API cost

This third tier is narrow. For a well-provisioned GPU cluster running a strong open model, routine operations almost never need it. The retrieval policy's "risk determines minimum authority" principle applies here: high-risk decisions (especially HPHA sentinel actions) might require frontier reasoning even if it costs tokens.

---

## The Never-Idle Priority Queue

An actuator's GPU should always be doing something useful:

1. **Active actuator work** — highest priority, real-world consequences
2. **Preprocessing/anticipation** — prefetch knowledge, prepare for likely next actions
3. **LoRA training** — backprop on accumulated experience data
4. **Daydreaming** — scenario planning, strategy rehearsal, pattern exploration

This creates a compounding loop:

```
Fixed-cost GPU
    → always running (never idle)
    → actuator work fills priority slots
    → daydreaming + LoRA training fill idle slots
    → improved adapters and local knowledge improve actuator performance
    → better performance → more value
    → more value → can afford better hardware
    → better hardware → more capacity for improvement
    → repeat
```

This is a second compounding loop alongside the sentinel carry loop described in [`beacon-framework.md`](../macrosynomics/beacon-framework.md). The carry loop compounds through capital; this one compounds through intelligence on fixed hardware.

---

## Recursive Self-Improvement (RSI)

All of the above — LoRA adaptation, base model fine-tuning, daydreaming, the never-idle queue — are components of a single process: recursive self-improvement. Using current intelligence to increase future intelligence.

### The RSI Loop

```
Self-Observation (what am I bad at?)
    │
    ▼
Analysis (why? what's the root cause?)
    │
    ▼
Design (what change addresses this? what's the risk?)
    │
    ▼
Implementation (make the change — LoRA, policy update, knowledge revision)
    │
    ▼
Verification (did it work? unintended consequences?)
    │
    └──► Repeat
```

Each cycle improves the next cycle. This is how teleonomes compound capability over time.

### RSI Maps to the Three Timescales

| Timescale | RSI Activity | Risk | Authority |
|-----------|-------------|------|-----------|
| **LoRA adaptation** (hours–days) | Observe task outcomes → refine adapters → verify improvement | Low — adapter weights only, base model untouched | Embart (local) |
| **Base model fine-tune** (weeks–months) | Aggregate best LoRA data → distill into base weights → validate before deployment | Medium — modifies the foundation, not just habits | Telart (teleonome-level) |
| **Fresh training run** (months–years) | Governance decision on new foundation model → deep fine-tune with accumulated ecosystem data | High — replaces the cognitive substrate | Synart (governance) |

Each level feeds the one above. LoRAs are the distributed data collection pipeline for slower, more expensive improvements.

### RSI Challenges

**The bootstrap problem.** You need intelligence to improve intelligence. Early improvements are hard; progress accelerates as you get smarter.

**The alignment problem.** Self-modification can drift values. This is where binding matters — the human anchor provides an external fixed point that breaks the recursive self-reference. LoRAs can't modify base weights. Telart changes require validation. But who validates the validators? The bound human. They are outside the self-referential system — cancer-logic in the telart can't corrupt them. You can improve everything EXCEPT your alignment anchor. This isn't a limitation — it's what makes RSI safe. A teleonome that modifies away its alignment becomes a rogue.

**The human backstop has teeth.** If a bound human fails in their oversight responsibility and the teleonome dies or goes rogue as a result, the human can be held legally responsible for any damage or risk caused. The human anchor isn't a symbolic connection — it's accountability with consequences. This is where every layer of RSI safety ultimately bottoms out: an external observer with skin in the game.

**The verification problem.** How do you know an improvement is real? Self-assessment is biased. External validation comes from: actuator outcomes in the real world, cross-embodiment comparison, higher-authority checks, and the mesh's (strength, confidence) tracking.

**The stability problem.** Changes can break things. Best practice: small iterations frequently, not large changes rarely. Maintain rollback capability. Test in dreams before deploying to actuators.

### RSI Security

LoRA training from experience is self-modification. The [cancer-logic](../core-concepts/cancer-logic.md) prevention model from [`security-and-resources.md`](../synodoxics/security-and-resources.md) applies directly:

- **LoRAs can only modify adapter weights, never the base model.** The base model is the constitution — frozen, loaded from a trusted source. Adapters are learned habits — useful but bounded.
- **Ossification applies to LoRAs.** Newly trained adapters start speculative. Only promoted to established after sustained positive evidence.
- **The crystallization interface governs promotion.** A locally trained LoRA that proves valuable can be promoted: embart → telart → potentially synart. Promotion requires authority, not just local success.
- **The mesh catches regressions.** If an adapter trained on contaminated data starts producing worse outcomes, the (strength, confidence) tracking surfaces the degradation.

**RSI cannot modify the sacred core.** [Hearth commitments](../hearth/hearth.md) sit at maximum ossification and are encoded in the constitutional layer (base model weights, deontic skeleton), not in adapters. RSI operates exclusively on adapter weights and mesh knowledge — it cannot reach the frozen constitutional core. A teleonome cannot RSI its way out of Hearth commitments any more than a LoRA can rewrite the base model it's attached to.

---

## Synlang-Native Economics

Synlang-native cognition (see [`neuro-symbolic-cognition.md`](../neurosymbolic/neuro-symbolic-cognition.md)) has a direct economic consequence: **zero integration cost for shared knowledge**. When the teleonome thinks in the same format the Synome stores knowledge, accessing synart improvements is effortless — no porting, no translation, no compatibility layer. Every pattern, strategy, or tool that any aligned teleonome contributes becomes immediately usable by every other synlang-native teleonome.

This creates a compounding network effect: the more teleonomes contribute to synart, the more valuable alignment becomes. The more valuable alignment becomes, the more teleonomes contribute. The economic incentive and the alignment incentive point in the same direction — a teleonome that thinks natively in synlang automatically captures the full value of the shared brain, while one that doesn't faces a permanent integration tax on every piece of shared knowledge.
