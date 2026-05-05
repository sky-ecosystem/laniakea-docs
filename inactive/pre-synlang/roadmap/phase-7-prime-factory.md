# Laniakea Phase 7: Prime Factory

**Status:** Draft  
**Last Updated:** 2026-02-12

---

## Executive Summary

Phase 7 introduces the **Prime Factory**: automated deployment of standardized Prime PAUs (Diamond architecture) with default integrations to the Generator and Halo layers.

The Prime Factory is primarily about:
- reducing bespoke Prime engineering
- standardizing configuration and permission surfaces
- creating a uniform substrate for later sentinel operation (Phase 9+)

It is not the same as “Primes become autonomous”; allocation decisions remain governance-directed until sentinel formations exist.

---

## Scope

### Objective

Enable one-click (template-based) Prime creation with:
- standardized Diamond PAU + facets
- automatic Generator integration (ERC-4626 vault relationship)
- automatic Configurator registration and init creation
- standardized Halo connection primitives (LCTS + NFAT + Core Halos)

### In Scope (Phase 7 Deliverables)

1. **Prime Factory contracts**
   - Deploy Prime Diamond PAU from audited templates
   - Provide deterministic deployment metadata for Synome/Artifacts

2. **Standard Diamond facet set**
   - ERC-4626 interfaces
   - Swap/trading primitives (bounded by rate limits)
   - NFAT and LCTS interaction facets
   - Admin/governance facets for upgrades and permissions

3. **Automatic Generator PAU integration**
   - Establish ERC-4626 vault relationship(s) between Prime and Generator
   - Set conservative initial rate limits and withdrawal policies

4. **Factory → Configurator flow**
   - Register Prime PAU via BEAMTimeLock processes
   - Pre-create init configurations for common operations
   - Provide streamlined cBEAM grant and activation runbooks

---

## Temporary Measures (Very Detailed)

### 1) “Factory-Deployed but Human-Operated” Primes

**Problem:** Prime factories arrive before Prime-side sentinels.

**Temporary measure:** Treat factory-deployed Primes as:
- standardized execution substrates
- still operated by GovOps + deterministic LPHA beacons

**Why this matters:** It prevents premature assumptions (“factory means autonomous”) while still delivering the core benefit: reduced deployment overhead and consistent interfaces.

### 2) Manual Facet Governance (Interim for Mature Upgrade Governance)

Diamond PAUs enable modular upgrades, but early on:
- facet upgrades should be treated as high-risk and relatively rare
- a conservative "facet allowlist" should exist for Phase 7–8 operations

**Temporary measure:**
- pre-approve a small set of facets
- require explicit governance review for adding new external integrations via new facets

This reduces the chance that the factory becomes a rapid pathway for unreviewed risk.

### 3) Transitional Prime Onboarding Checklist

Before sentinel formations exist, a new Prime’s biggest risks are misconfiguration and operational mistakes.

**Temporary measure:** A required onboarding checklist for the first N settlement cycles:
- verify ERC-4626 vault configuration and rate limits
- verify all configured targets exist in Synome/Artifacts
- run a conservative, human-reviewed allocation policy
- ensure emergency removal paths work (instant permission removals, rate limit decreases)

This checklist is partially superseded by warden monitoring in Phase 9+.

---

## Acceptance Criteria (Exit to Phase 8)

Phase 7 is considered complete when:
- A new Prime can be deployed via factory with a standardized Diamond PAU
- The Prime can connect to the Generator via ERC-4626 vaults with functioning rate limits
- Configurator registration and init creation are automatic or near-automatic
- Prime-to-Halo interaction primitives (LCTS/NFAT/Core Halos) are available from template facets

---

## Links (Relevant Specs)

- Roadmap overview: [roadmap-overview.md](./roadmap-overview.md)
- Prime execution substrate: [diamond-pau.md](../smart-contracts/diamond-pau.md)
- Guardrails and timelocks: [configurator-unit.md](../smart-contracts/configurator-unit.md)
- Architecture context: [architecture-overview.md](../smart-contracts/architecture-overview.md)
- Halo primitives:
  - LCTS: [lcts.md](../smart-contracts/lcts.md)
  - NFATs: [nfats.md](../smart-contracts/nfats.md)

