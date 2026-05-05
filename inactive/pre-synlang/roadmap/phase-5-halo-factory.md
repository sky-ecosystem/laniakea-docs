# Laniakea Phase 5: Halo Factory

**Status:** Draft  
**Last Updated:** 2026-02-12

---

## Executive Summary

Phase 5 introduces the **Halo Factory**: a standardized deployment system for Halo Agents, Halo Classes, and Halo Units using pre-audited templates.

This is the turning point from “each Halo is a bespoke engineering + audit project” to “Halos are assembled from approved building blocks”. It enables rapid onboarding while preserving governance control through:
- template governance (what can be deployed)
- Configurator guardrails (what can be executed)
- rate limits (bounded capital flow)

**Phasing reality:** Prime-side sentinel automation and auctions are still not live. Phase 5 improves *deployment scalability*, not autonomous allocation.

---

## Scope

### Objective

Enable fast, repeatable Halo deployment by:
- Deploying standardized Halo PAU stacks from templates
- Attaching the correct Halo beacon (`lpha-lcts` or `lpha-nfat`)
- Auto-registering contracts and producing the right Synome/Artifact records
- Reducing governance overhead and operational footguns

### In Scope (Phase 5 Deliverables)

1. **Halo Factory contracts**
   - Template registry (what templates are allowed)
   - Deterministic deployment of Halo PAU stacks and associated contracts
   - Emission of canonical deployment metadata for Synome ingestion

2. **Halo Class templates**
   - **LCTS-based Portfolio Halo Class**
     - Pooled capital; fungible shares; queue-based settlement
     - Integrates with `lpha-lcts`
   - **NFAT-based Term Halo Class**
     - Bespoke deals; ERC-721 NFATs; per-Prime queues
     - Integrates with `lpha-nfat`

3. **Factory → Configurator integration**
   - Automatic registration of deployed PAU addresses
   - Pre-creation of standard “init” configurations for rate limits and permissions
   - Streamlined cBEAM grant path for GovOps (still subject to timelocks where required)

4. **Halo Unit deployment within a Class**
   - Ability to deploy multiple Units under one Class
   - Unit-specific parameters (capacity, seniority, yield terms, buybox details)
   - Shared legal and operational infrastructure at the Class level

### Explicit Non-Goals (Deferred)

- Automated Prime deployment (Phase 7)
- Automated Generator deployment (Phase 8)
- Prime-side sentinel formations and automated allocation (Phases 9–10)

---

## Design Overview

### Halo Class vs. Halo Unit (Why the Factory Must Understand Both)

**Halo Class** (shared substrate):
- PAU + permissions
- Beacon integration (`lpha-lcts` or `lpha-nfat`)
- Legal framework and recourse model
- Shared reporting/Artifact format

**Halo Unit** (the product):
- Capacity, pricing/yield terms, seniority
- Underlying manager/counterparty identity and constraints
- Unit-specific reporting requirements

The factory must deploy both:
- Class-level infrastructure once
- Unit-level artifacts and parameters repeatedly

---

## Temporary Measures (Very Detailed)

Phase 5 replaces Phase 1–4's "manual Halo launch" workflow, but it does not eliminate all manual steps. The key is to make what remains manual **explicit**, bounded, and auditable.

### 1) Manual Pre-Factory Halo Inventory (Migration Input)

**Problem:** By Phase 5, there may already be:
- Core Halos (legacy assets wrapped as Units)
- Manually deployed NFAT Facilities
- Manually deployed LCTS Portfolio Halos

**Temporary measure:** Maintain a “pre-factory Halo registry” entry set:
- Each existing Halo Class/Unit is recorded with:
  - contract addresses
  - beacon operator identity
  - Artifact link
  - whether it conforms to a factory template (retroactive compatibility)

**Goal:** Allow factories to become the default path without breaking existing deployments.

### 2) Governance Approval Still Exists (But Becomes Template-Based)

**Problem:** Even with factories, governance must still approve:
- new templates (high impact)
- new Halo Classes in regulated contexts
- major Unit parameter ranges

**Temporary measure:** Split approvals:
- **Template approval** (rare, heavy): audit + governance sign-off
- **Instance approval** (frequent, lighter): “this deployment uses Template X with parameters within allowed ranges”

Over time, the template system can support more “spell-less” instance onboarding where the approval becomes a signed Artifact update rather than bespoke contract review.

### 3) Prime Integration Remains Manual Until Phase 9

**Problem:** Even if a Halo Unit is deployed quickly, Prime allocation into it is not fully autonomous yet.

**Temporary measures in Phase 5–8:**
- Prime GovOps teams (via Configurator + cBEAMs) must:
  - create/init rate limits for the new Unit as a target
  - optionally stage a ramp-up plan consistent with SORL constraints
  - monitor early flows more heavily than steady-state

**Replacement:** In Phase 9, `stl-base` can incorporate new Units into automated allocation decisions (subject to governance constraints), and the Prime-side automation becomes the default.

### 4) Operational “Factory Day-0” Checklist (Interim Safety)

**Problem:** The first days of a new Halo Unit are highest risk.

**Temporary measure:** A required runbook for the first N settlement cycles:
- Verify Artifact completeness (addresses, parameters, oracle sources)
- Verify beacon connectivity and expected lock/settle behavior (LCTS Units)
- Verify redemption paths and legal endpoints (RWA)
- Enforce conservative initial rate limits
- Require daily human review during Processing Window for N days

This checklist becomes less burdensome as telemetry and warden-based monitoring mature (Phase 9+).

---

## Acceptance Criteria (Exit to Phase 6)

Phase 5 is considered complete when:
- A Halo Class and Unit can be deployed from a factory template without bespoke contract engineering
- Deployed contracts are automatically registered for downstream operations (Configurator + Synome/Artifacts)
- Both LCTS-based and NFAT-based templates exist and are usable
- Operational onboarding time is reduced materially vs. Phase 1–3 manual launches

---

## Links (Relevant Specs)

- Roadmap overview: [roadmap-overview.md](./roadmap-overview.md)
- Halo structure and deployment context:
  - [portfolio-halo.md](../sky-agents/halo-agents/portfolio-halo.md)
  - [term-halo.md](../sky-agents/halo-agents/term-halo.md)
- Core contract architecture and factories: [architecture-overview.md](../smart-contracts/architecture-overview.md)
- Halo primitives:
  - LCTS: [lcts.md](../smart-contracts/lcts.md)
  - NFATs: [nfats.md](../smart-contracts/nfats.md)
- Governance execution + guardrails: [configurator-unit.md](../smart-contracts/configurator-unit.md), [diamond-pau.md](../smart-contracts/diamond-pau.md)

