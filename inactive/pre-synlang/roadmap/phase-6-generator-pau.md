# Laniakea Phase 6: Generator PAU

**Status:** Draft  
**Last Updated:** 2026-02-12

---

## Executive Summary

Phase 6 introduces a unified **USDS Generator PAU** architecture and migrates away from per-Prime ilks toward a **single-ilk** interface layer between MCD and the Prime layer.

This simplifies:
- governance scope separation (Generator vs Prime vs Halo)
- risk accounting and operational controls
- the long-term factory story (Phase 8 multi-Generator)

`srUSDS` (launched in Phase 4) remains a Generator-level product; Phase 6 consolidates the on-chain “Generator surface” so later automation has a stable target.

---

## Scope

### Objective

Replace “N Prime ilks in MCD” with:
- a Generator PAU (Controller + ALMProxy + RateLimits)
- a single MCD ilk for the Generator
- ERC-4626 vault relationships between Generator and each Prime

### In Scope (Phase 6 Deliverables)

1. **Generator PAU deployment**
   - Standard PAU surface for Generator operations
   - Rate-limited deposit/withdraw to/from Prime vaults

2. **Single-ilk MCD integration**
   - One canonical Generator ilk replacing multiple per-Prime ilks
   - Migration plan for legacy ilks (debt, accounting, permissions)

3. **ERC-4626 Prime vault interface**
   - Each Prime connects via an ERC-4626 vault to the Generator
   - Primes can deposit/withdraw subject to available liquidity and rate limits

4. **`srUSDS` integration at the Generator**
   - Generator maintains the issuance interface for senior risk capital tokens
   - Aligns with LCTS lock/settle cadence (Phase 4+)

5. **Generator Configurator scope**
   - Separate operational scope and guardrails for Generator actions
   - Clear separation from Prime and Halo configuration domains

---

## Temporary Measures (Very Detailed)

Phase 6 is a migration-heavy phase. The “temporary measures” here are the guardrails that prevent the migration from becoming a systemic event.

### 1) Dual-Run Migration (Interim Coexistence of Old + New)

**Problem:** You cannot atomically migrate all Primes and all debt positions without operational risk.

**Temporary measure:** Run old and new surfaces concurrently for a bounded period:
- Keep legacy Prime ilks operational while the Generator PAU is introduced
- Migrate Prime-by-Prime using a predictable schedule
- For a given Prime, define a cutover epoch after which new flows go through the Generator vault

**Key requirement:** Accounting must be explicit about what sits where during dual-run.

### 2) Liquidity Management During Cutover

**Problem:** ERC-4626 vaults require clarity on liquidity availability; migration can create “liquidity cliffs”.

**Temporary measure:**
- Conservative initial withdrawal policies for Prime vaults
- Explicit liquidity buffers in the Generator during early epochs
- Operator runbook for temporarily pausing withdrawals (within governance constraints) if a migration incident occurs

### 3) Manual Governance Coordination (Interim for Factory-Based Generator Deployment)

**Problem:** Generator Factory does not exist until Phase 8.

**Temporary measure:**
- Generator PAU deployment and ilk migration are governance-managed
- All changes are staged outside the Processing Window
- Any emergency rollback procedures must be pre-approved as part of the migration plan

---

## Acceptance Criteria (Exit to Phase 7)

Phase 6 is considered complete when:
- A Generator PAU exists and is the canonical interface to MCD for Prime funding
- Per-Prime ilks are eliminated (or reduced to an explicitly temporary compatibility set)
- Each Prime connects via an ERC-4626 vault interface with functioning rate limits
- `srUSDS` issuance and daily settlement integration remain correct and stable

---

## Links (Relevant Specs)

- Roadmap overview: [roadmap-overview.md](./roadmap-overview.md)
- Architecture context: [architecture-overview.md](../smart-contracts/architecture-overview.md)
- LCTS (Generator-level risk capital): [lcts.md](../smart-contracts/lcts.md)
- Guardrails and permissions: [configurator-unit.md](../smart-contracts/configurator-unit.md), [diamond-pau.md](../smart-contracts/diamond-pau.md)
- Daily settlement cadence: [daily-settlement-cycle.md](../accounting/daily-settlement-cycle.md)

