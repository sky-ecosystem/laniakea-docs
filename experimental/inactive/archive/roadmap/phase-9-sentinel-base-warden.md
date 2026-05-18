# Laniakea Phase 9: Sentinel Base & Warden

**Status:** Draft  
**Last Updated:** 2026-02-12

---

## Executive Summary

Phase 9 is the point where Laniakea transitions from “governance-directed operations on a daily cadence” to **Prime-side autonomous execution** under strict safety constraints.

The deliverables are:
- **`stl-base`** (Baseline Sentinel): the public execution surface that can hold execution keys and run Prime strategies continuously.
- **`stl-warden`** (Warden Sentinels): independent safety monitors with halt authority.
- **Auction activation** for OSRC (`srUSDS` origination capacity) and liability duration matching capacity, driven by sealed bids from `stl-base`.

This phase explicitly replaces Phase 1–4's temporary measures:
- governance-published OSRC allocations → sealed-bid OSRC auction results
- governance-published Duration allocations → sealed-bid Duration reservation + tug-of-war/excess auction behavior (auction mode)

---

## Scope

### Objective

Deploy sentinel formations for Primes such that:
- execution is continuous and automated within bounded authority
- safety is enforceable by independent operators
- daily settlement includes auction-based allocation inputs produced by Prime behavior, not governance discretion

### In Scope (Phase 9 Deliverables)

1. **Baseline Sentinel (`stl-base-{prime}`)**
   - Holds the Execution Engine (pBEAMs / signing keys for Prime PAU operations)
   - Executes the public “Base Strategy” defined in Prime Artifacts
   - Produces auditable logs into Synome (including counterfactual simulation outputs)

2. **Warden Sentinels (`stl-warden-{prime}-{operator}`)**
   - Independent, third-party operators (not the Baseline operator)
   - Continuous monitoring and invariant enforcement
   - Halt/freeze authority over the Execution Engine

3. **Auction activation (OSRC + Duration)**
   - `stl-base` instances submit sealed bids
   - `lpha-auction` switches from pre-auction publication to sealed-bid matching (auction mode)
   - Outputs are consumed by `lpha-lcts` (OSRC capacity/yield inputs) and published for broader system use

4. **TTS-based safety economics**
   - Formalize Time to Shutdown (TTS) as a parameter bounded by warden quality and diversity
   - Tie rate limits and required risk capital to `RateLimit × TTS`

### Explicit Non-Goals (Deferred)

- Stream Sentinels (`stl-stream`) and streaming accord/carry economics (Phase 10)
- Teleonome layers beyond sentinels (beyond roadmap)

---

## Sentinel Formation Architecture (Why It’s a Formation)

Sentinels are not “one bot with keys”. They are a **coordinated formation**:

| Component | Role | Execution Authority | Operator |
|-----------|------|---------------------|----------|
| **stl-base** | Primary decision-making and execution | **Yes** | Accordant GovOps |
| **stl-stream** | Intelligence + intent streaming | **No** | Ecosystem actor |
| **stl-warden** | Safety monitoring + halt | **Limited (stops only)** | Independent operators |

In Phase 9:
- `stl-base` and `stl-warden` go live.
- `stl-stream` is optional/absent; Baseline runs Base Strategy continuously.

Canonical sentinel formation semantics are defined in `trading/sentinel-network.md`.

---

## Auction Activation (Switching From Phase 4 Pre-Auction)

### What Changes at the Interface

In Phase 4, Core Council sets srUSDS rates and capacity directly.

In Phase 9, `lpha-auction`:
- accepts sealed bids from `stl-base`
- runs matching logic (uniform price where applicable)
- publishes clearing results using the **same output schemas** consumed in earlier phases

### Temporary Measures for Safe Activation

Auction activation is a sensitive cutover. The temporary measures below are intended to reduce discontinuity and preserve auditability.

1. **Dual-Mode Period (“Shadow Outputs”)**
   - For a bounded activation window, governance continues publishing pre-auction allocations *alongside* the auction results as a comparison artifact.
   - Only one is marked “binding” for settlement.
   - This provides an operational sanity check before fully deprecating the governance path.

2. **Participation Policy**
   - Auctions require `stl-base` participation. During early rollout, some Primes may not be sentinel-operated yet.
   - Temporary policy options (must be chosen explicitly):
     - (A) “No sentinel, no participation” (non-participating Primes receive zero auction capacity)
     - (B) “Proxy bid” (governance publishes a proxy bid on behalf of non-sentinel Primes)
   - The policy must be explicit in Synome so results remain interpretable.

3. **Conservative Guardrails on Day 0**
   - Start with conservative rate limits and tight bid bounds.
   - Increase operational bandwidth only after warden performance is validated and TTS assumptions hold.

4. **Emergency Reversion**
   - If auction mode fails, governance can temporarily revert `lpha-auction` to pre-auction mode for a bounded period.
   - Reversions must be explicitly labeled and post-mortemed; they are not “silent fallbacks”.

The bid formats, timing, and auction semantics are specified in:
- `accounting/daily-settlement-cycle.md`

---

## Warden Operations and TTS Economics

### What Wardens Do

Wardens are deliberately narrow:
- monitor Baseline behavior continuously
- check hard invariants (rate limits, guardrails, risk thresholds)
- halt/freeze execution if invariants are violated or compromise is suspected

Wardens **do not** optimize and **do not** stream intent.

### Why TTS Matters

The system’s worst-case damage from a rogue Baseline is bounded by:

```
Maximum Damage = Rate Limit × TTS
Required Risk Capital ≥ Rate Limit × TTS
```

Phase 9 makes TTS real by:
- requiring operator diversity (multiple independent wardens)
- recording warden attestations and halt performance
- using TTS as a first-class input to rate limit governance

---

## Temporary Measures (Very Detailed)

Phase 9 introduces high-autonomy software for the first time. Temporary measures are required to ensure safety and governance legibility.

### 1) “Public Base Strategy Only” (Interim for Stream-Influenced Execution)

Until Phase 10:
- Baseline executes only the public Base Strategy from Prime Artifacts.
- No proprietary stream intents are accepted.

This provides a stable baseline for warden validation and auction behavior before adding additional complexity.

### 2) Tight Execution Surface (Interim for Full Strategy Breadth)

Early Baselines should be deployed with:
- minimal pBEAM scope required for the Base Strategy
- narrow target allowlists
- conservative rate limits and slow ramp-ups (SORL-constrained)

Expansion occurs only after warden operators demonstrate reliable halt performance.

### 3) Human-On-Call Requirement (Interim for Mature Incident Response)

Even with wardens, early operations need human escalation:
- Each formation must have an on-call protocol for GovOps + warden operators.
- Halts must trigger governance notifications and incident tickets.
- Unhalts require explicit acknowledgement and a post-mortem plan.

---

## Acceptance Criteria (Exit to Phase 10)

Phase 9 is considered complete when:
- `stl-base` is operating at least one Prime end-to-end within bounded authority
- Multiple independent `stl-warden` operators are live and demonstrably capable of halting execution
- OSRC and Duration auctions run in auction mode with sealed bids from `stl-base`
- `lpha-auction` outputs are consumed reliably by downstream systems (including `lpha-lcts`)
- TTS is measured/estimated in practice and used to justify operational rate limits and risk capital requirements

---

## Links (Relevant Specs)

- Roadmap overview: [roadmap-overview.md](./roadmap-overview.md)
- Sentinel formations + TTS economics: [sentinel-network.md](../trading/sentinel-network.md)
- Risk framework connection points: [sentinel-integration.md](../risk-framework/sentinel-integration.md)
- Auction timing, bid interfaces, and settlement: [daily-settlement-cycle.md](../accounting/daily-settlement-cycle.md)
- Beacon taxonomy: [beacon-framework.md](../synomics/macrosynomics/beacon-framework.md)

