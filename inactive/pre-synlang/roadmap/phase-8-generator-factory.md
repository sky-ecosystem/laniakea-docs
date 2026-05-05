# Laniakea Phase 8: Generator Factory

**Status:** Draft  
**Last Updated:** 2026-02-12

---

## Executive Summary

Phase 8 introduces the **Generator Factory** to enable multi-Generator architectures. Different Generators can represent:
- distinct stablecoin contexts
- distinct risk capital structures
- distinct governance scopes
- isolation boundaries (blast-radius reduction)

Phase 8 completes the "factory stack":
Halo Factory (Phase 5) → Generator PAU (Phase 6) → Prime Factory (Phase 7) → Generator Factory (Phase 8).

---

## Scope

### Objective

Enable repeatable deployment of a full Generator stack:
- Generator PAU + governance scope
- MCD ilk integration for that Generator
- associated risk capital token stacks (e.g., per-Generator `srUSDS`)
- standardized Prime connection surfaces (ERC-4626 vaults)

### In Scope (Phase 8 Deliverables)

1. **Generator Factory contracts**
   - Deploy Generator PAUs from audited templates
   - Deploy per-Generator LCTS stacks and Holding Systems (where applicable)
   - Emit canonical deployment metadata for Synome/Artifacts

2. **Per-Generator governance scope**
   - Generator-scope Configurator deployments (or equivalent)
   - Clear separation from Prime-scope and Halo-scope operations

3. **Prime ↔ Generator relationship management**
   - Define which Primes can connect to which Generators
   - Deploy/initialize ERC-4626 vault relationships
   - Enforce any cross-Generator restrictions (if required by governance)

4. **Risk capital token factories**
   - Per-Generator `srUSDS` deployments (or equivalent tokens)
   - Standardized LCTS queue deployments for those tokens

---

## Temporary Measures (Very Detailed)

### 1) Single-Generator Compatibility Period

**Problem:** Even once Generator Factory exists, ecosystem operations may still assume a single default Generator.

**Temporary measure:**
- Establish a “default Generator” policy for a bounded period
- Restrict multi-Generator usage to explicit pilot Primes
- Require clear Synome/Artifact labeling of which Generator a Prime is connected to

This avoids confusion and misrouting of funds while the ecosystem adapts to multi-Generator complexity.

### 2) Manual Policy for Cross-Generator Risk Isolation

**Problem:** Multi-Generator enables isolation, but isolation rules are easy to violate accidentally (shared collateral sources, shared external dependencies).

**Temporary measure:**
- Governance publishes explicit “Generator isolation policies” as Synome constraints
- lpla-checker verifies high-level invariants (e.g., “Prime X cannot borrow from both Generator A and B” if such a rule exists)
- Exceptions require explicit governance labeling

### 3) Migration Runbook (Interim for Seamless Multi-Generator Routing)

**Problem:** Migrating an existing Prime’s relationship from Generator A to Generator B is operationally risky.

**Temporary measure:**
- Require migration only at well-defined epochs
- Require conservative rate limits during the first N epochs post-migration
- Require a rollback plan pre-approved by governance

---

## Acceptance Criteria (Exit to Phase 9)

Phase 8 is considered complete when:
- A new Generator can be deployed via factory with the full required stack (PAU, governance scope, risk capital tokens as applicable)
- Prime ↔ Generator relationships can be deployed/configured in a standardized way
- Multi-Generator operations are possible without bespoke engineering work
- The factory stack is stable enough to support Phase 9 sentinel-scale operations

---

## Links (Relevant Specs)

- Roadmap overview: [roadmap-overview.md](./roadmap-overview.md)
- Architecture context: [architecture-overview.md](../smart-contracts/architecture-overview.md)
- LCTS (per-Generator risk capital): [lcts.md](../smart-contracts/lcts.md)
- Guardrails and permissions: [configurator-unit.md](../smart-contracts/configurator-unit.md), [diamond-pau.md](../smart-contracts/diamond-pau.md)

