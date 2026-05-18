# Dreamer/Actuator Split

> Two complementary cognitive roles — actuators interact with reality through beacons, dreamers explore possibility in simulation — forming the core RSI mechanism.

**Also known as:** actuator/dreamer, dreamer-actuator architecture, embodiment roles

## Definition

The dreamer/actuator split divides teleonome embodiments into two complementary roles optimized for different functions. Actuators interact with the real world through beacons — executing trades, managing systems, monitoring state, making decisions with real consequences. Dreamers run parallel evolutionary simulations on dedicated hardware, exploring possibility spaces and evolving strategies that actuators can deploy.

Actuators operate in real-time with real-world consequences. Their hardware is optimized for fast inference with low latency. Between active tasks, actuators use idle GPU cycles for daydreaming — short reflective loops including scenario rehearsal, LoRA training passes, and pattern refinement. Daydreaming is a natural actuator behavior, not a separate role. It fills the never-idle priority queue: active work → preprocessing/anticipation → LoRA training → daydreaming.

Dreamers operate on dedicated heavy embodiments, running many copies of the same model in parallel evolutionary populations. Each candidate in a population gets a full actuator-equivalent inference environment. This is the critical design constraint: dreamers use the same GPU profile as medium actuators because they are training improvements FOR those actuators. If the dreamer runs a different model/hardware setup, strategies it discovers may not transfer faithfully. A LoRA evolved by the dreamer must be directly deployable to an actuator without a translation step.

Actuators provide grounding — real-world feedback that validates or invalidates strategies. Dreamers provide exploration — searching possibility spaces far larger than any actuator encounters in practice. Together they form the core RSI mechanism: actuators generate experience, dreamers evolve on that experience, improved strategies deploy back to actuators, and the loop repeats.

This maps to the three timescales of model improvement: LoRA adaptation (hours-days, local, embart-level), base model fine-tune (weeks-months, teleonome-level, telart authority), and fresh training run (months-years, governance-level, synart authority). Each feeds the one above. LoRAs are the distributed data collection pipeline for slower, more expensive improvements.

## Key Properties

- Actuators: real-world interaction, fast inference, idle-cycle daydreaming, ground truth
- Dreamers: parallel evolutionary simulation, dedicated hardware, strategy exploration
- Same model profile required: dreamer discoveries must transfer directly to actuators
- Daydreaming is NOT full dreaming — single-stream sequential vs. massively parallel evolutionary
- Three timescales: LoRA adaptation → base model fine-tune → fresh training run
- The never-idle queue ensures fixed-cost hardware is always running useful computation
- Dreamers work on both task-specific strategies AND generalizable epistemic infrastructure (evidence weighting methods, regime-change detectors, neural weight evolution, context assembly strategies)

## Relationships

- **mechanism-of:** [rsi](rsi.md) — the dreamer/actuator loop is how recursive self-improvement operates in practice
- **constrained-by:** [retrieval-policy](retrieval-policy.md) — same policy logic must apply to both actuators and dreamers (invariant 4)
- **operates-within:** [five-layer-architecture](five-layer-architecture.md) — light/medium/heavy embodiment power levels map to actuator/dreamer hardware profiles
- **produces:** [artifact-hierarchy](artifact-hierarchy.md) — actuators produce embart, dreams promote to telart through crystallization
