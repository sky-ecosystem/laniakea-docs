---
concepts:
  references:
    - probabilistic-mesh
    - truth-values
    - dreamer-actuator-split
---

# Hardware-Aware Cognition

The optimal cognition strategy depends on the hardware it runs on. A 64-core CPU with a single GPU pipelines differently than a multi-GPU cluster with weak CPUs. The Synome doesn't treat this as an engineering detail to be configured — it treats hardware topology as **knowledge in the graph**, and scheduling strategies as **patterns subject to the same evidence dynamics as everything else.**

---

## Hardware Topology in the Graph

Hardware facts are claims like any other:

```
(gpu node-1 (type A100) (vram 80GB) (inference-ms-per-token 12))
(cpu node-1 (cores 64) (clock 3.4GHz) (graph-query-avg-ms 3))
(bus node-1 (gpu-cpu-bandwidth 32GB/s))
(network node-1 (latency-to-exchange 12ms))
```

These are Tier 1 claims — directly observed, high confidence. They change when hardware is upgraded, when a node goes down, when performance degrades under load. The system reads its own hardware the same way it reads market data.

---

## The Pipelining Problem

The fundamental scheduling question: **what does each component do while the others are busy?**

The cognition loop has two main consumers of time:

1. **GPU inference** — the emo's forward pass. Produces ops (query programs, action proposals). Duration depends on context length (prefill) and output length (decode).
2. **CPU ops execution** — running graph queries, pattern matching, vector search, rendering results back into s-expressions. Duration depends on query complexity and graph size.

Neither should wait for the other.

### The Basic Pipeline

```
GPU: [--- inference turn N ---]  [--- inference turn N+1 ---]
CPU:                [-- execute ops from turn N --][-- render --]
                    ^                              ^
                    ops arrive                     context ready for N+1
```

While the GPU is generating tokens for turn N, the CPU is idle (or finishing work from turn N-1). As soon as the GPU emits ops, the CPU executes them. As soon as the CPU finishes, new context is rendered and the GPU starts the next turn.

The goal: **zero idle time on the GPU.** The GPU is the expensive resource (fixed-cost, always spinning). Every millisecond it waits for the CPU is wasted capacity.

### Speculative Pre-Execution

If the CPU finishes executing ops before the GPU finishes its next inference turn, the CPU has spare cycles. Use them:

- **Speculative queries** — predict what the emo might ask next based on the current context and run those queries ahead of time. If the prediction is right, results are ready instantly when the emo asks.
- **Graph maintenance** — compaction, index rebuilding, cache warming.
- **Background searches** — low-priority exploration that might surface useful patterns.

Speculative queries are free at the margin — the CPU would be idle otherwise. Wrong predictions are discarded with no harm. The system learns what to speculate on through the same evidence dynamics: "speculative query X was used 70% of the time" → high TV → keep doing it.

---

## Context Efficiency

With a self-hosted model, the GPU cost per turn is dominated by **prefill** — processing all input tokens. Longer context = more prefill time = fewer turns per second.

This makes surgical context assembly directly valuable:

- Loading 2000 tokens of precisely relevant claims vs 8000 tokens of full documents = 4x more turns per second at the same GPU cost
- More turns per second = more iterations of the cognition loop = faster convergence on justified action
- The [query mechanics](query-mechanics.md) — stochastic traversal, backend composition, learned strategies — earn their keep through context efficiency, measured in useful-tokens-per-total-tokens

Context efficiency is directly measurable: what fraction of loaded tokens contributed to the final decision? Tokens that were loaded and never referenced in the evidence chain were waste. The system tracks this.

---

## Fixed-Cost GPU Economics

With a self-hosted open model, the economics are fundamentally different from API-based inference:

| | API (pay-per-token) | Self-hosted (fixed-cost GPU) |
|---|---|---|
| **Marginal cost of one more query** | Real ($$) | Zero (GPU is already running) |
| **Cost of idle time** | Zero (you don't pay) | Real (wasted capacity you're paying for) |
| **Exploration incentive** | Minimize — every query costs | Maximize — idle time is the real waste |
| **Speculative work** | Expensive | Free |

This changes the cognition strategy. With API pricing, the emo should be conservative — only query when likely to help. With fixed-cost GPU, the emo should be aggressive — speculative queries, Monte Carlo sampling, broad exploration — because the alternative is idle GPU time.

The system learns this from its own performance data. On a self-hosted setup, aggressive query strategies will show better outcomes (because exploration is free) and the evidence accumulates on those strategies. The hardware economics shape the cognition style through evidence, not through hard-coded rules.

---

## Scheduling Strategies as Patterns

Different hardware profiles favor different scheduling:

```
;; Strategy for CPU-rich, GPU-scarce setups
(strategy parallel-fanout-between-turns
  (on gpu-inferring
    (parallel-cpu-queries 16)
    (speculative-prefetch (predict-next-ops)))
  (on gpu-done (render-all) (start-next-inference)))

;; Strategy for GPU-rich, limited-CPU setups
(strategy sequential-steering
  (step 1 (single-cpu-query (most-likely-needed)))
  (step 2 (gpu-decide-next ?step1))
  (step 3 (single-cpu-query ?decision))
  (return))
```

These are patterns in the graph with TVs. The system tries both strategies, measures GPU utilization, turns per second, decision quality. The strategy that works on this hardware accumulates positive evidence.

When hardware changes — new GPU, more cores, different network latency — the TVs on existing strategies become stale. The system re-evaluates. Strategies that were optimal for the old hardware lose confidence. New strategies emerge. The adaptation is automatic.

---

## Self-Optimization

The system observes its own performance and writes evidence:

```
(evidence perf:441
  (supports (strategy parallel-fanout-between-turns ...))
  (w 1.0)
  (context (hardware node-1) (workload trading-decisions) (gpu-util 0.94))
  (t 1708012800))

(evidence perf:442
  (contradicts (strategy sequential-steering ...))
  (w 0.8)
  (context (hardware node-1) (workload trading-decisions) (gpu-util 0.61))
  (t 1708012800))
```

Performance metrics are just more evidence. GPU utilization, query latency, turns per second, context efficiency — all feed back into strategy TVs. The system learns its own optimal scheduling the same way it learns optimal trading strategies: try things, observe results, accumulate evidence.

This is the fractal pattern from the [security docs](../synodoxics/security-and-resources.md) at its most literal. The same evidence dynamics that govern "should I increase exposure to ETH" also govern "should I run 8 parallel CPU queries or 16." Same graph, same TVs, same learning loop. The system doesn't distinguish between knowledge about the world and knowledge about itself.
