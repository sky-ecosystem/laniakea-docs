# Laniakea Phase 10: Sentinel Stream

**Status:** Draft  
**Last Updated:** 2026-02-12

---

## Executive Summary

Phase 10 completes the canonical sentinel formation by adding **Stream Sentinels (`stl-stream`)**: proprietary intelligence providers that can influence Prime execution via intent streaming without holding execution keys.

Key deliverables:
- `stl-stream` integration (intent streaming to Baseline)
- Streaming Accord (governing Baseline ↔ Stream relationship)
- Carry attribution and settlement (Stream earns only on outperformance vs Base Strategy)

This phase enables the “public capital ↔ private intelligence” compounding loop while preserving the safety properties established in Phase 9 (public execution + independent wardens + bounded authority).

---

## Scope

### Objective

Allow proprietary intelligence to influence Prime execution safely by:
- introducing `stl-stream` as an intent-only contributor
- binding intent through explicit risk tolerance intervals
- settling carry based on counterfactual simulation outputs produced by Baseline

### In Scope (Phase 10 Deliverables)

1. **Stream Sentinel (`stl-stream-{prime}-{actor}`)**
   - Private/proprietary operation by ecosystem actors
   - Ingests data and produces trading/positioning intent
   - Cannot execute directly; no pBEAM access

2. **Streaming Accord**
   - Synomic contract governing:
     - acceptable intent bounds (Risk Tolerance Interval)
     - performance fee ratio (carry share)
     - termination and dispute processes

3. **Carry mechanism + attribution tooling**
   - Baseline produces counterfactual Base Strategy simulation outputs
   - Carry is computed only on outperformance:
     ```
     Carry = (Actual PnL - Simulated Baseline PnL) × Performance Fee Ratio
     ```

4. **Operational lifecycle**
   - Accord negotiation → formation assembly → activation → operation → termination

---

## Safety Model (Why Stream Doesn’t Get Keys)

The core safety property is:
- **All execution flows through public Baseline code.**

Stream contributes only intent:
- Baseline validates intent against the Risk Tolerance Interval
- Wardens can halt Baseline execution if invariants are violated
- If Stream disconnects or misbehaves, Baseline falls back to Base Strategy (no disruption of execution)

---

## Temporary Measures (Very Detailed)

Phase 10 adds a new class of private actor to the system. Temporary measures are required to avoid “instant, unbounded stream markets” before governance and operators have lived experience.

### 1) Whitelisted Stream Pilot (Interim for Open Stream Markets)

**Temporary measure:** Start with a small, explicitly whitelisted set of Stream operators:
- each stream must be registered in Synome/Artifacts with operator identity
- each stream must have an explicit Streaming Accord before activation

This is replaced over time by more open participation regimes once warden monitoring and dispute resolution are mature.

### 2) Conservative Risk Tolerance Intervals (Interim for High-Bandwidth Alpha)

**Temporary measure:** Early accords use:
- narrow position limits
- low velocity limits
- strict concentration caps
- conservative allowed-asset allowlists

As performance and safety are demonstrated, these intervals can widen under governance oversight.

### 3) Dispute and Termination Playbooks (Interim for Standardized Arbitration)

Streams introduce disputes:
- did Baseline execute intent correctly?
- were intents rejected appropriately?
- did simulation outputs match the agreed Base Strategy?

**Temporary measure:** Require playbooks that specify:
- what logs are authoritative (Synome counterfactual logs, warden attestations)
- escalation paths and deadlines
- immediate termination conditions (e.g., repeated invalid intent, suspicious behavior)

---

## Acceptance Criteria (Roadmap Completion)

Phase 10 is considered complete when:
- Baseline + wardens can safely accept intent streams from at least one `stl-stream` operator
- Streaming Accords are enforceable and govern intent bounds and carry terms
- Carry attribution is computed from Baseline counterfactual simulation logs and settled transparently
- Formations degrade safely to Base Strategy when streams disconnect or violate constraints

---

## Links (Relevant Specs)

- Roadmap overview: [roadmap-overview.md](./roadmap-overview.md)
- Sentinel formations + Streaming Accord + carry: [sentinel-network.md](../trading/sentinel-network.md)
- Risk framework integration points: [sentinel-integration.md](../risk-framework/sentinel-integration.md)
- Beacon taxonomy: [beacon-framework.md](../synomics/macrosynomics/beacon-framework.md)

