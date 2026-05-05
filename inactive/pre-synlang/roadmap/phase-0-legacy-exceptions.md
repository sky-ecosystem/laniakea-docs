# Laniakea Phase 0: Legacy & Exceptional Deployments

**Status:** Draft
**Last Updated:** 2026-02-12

---

## Executive Summary

Phase 0 covers legacy and exceptional deployments that must proceed before Phase 1 infrastructure is fully ready. These are primarily Grove deployments that cannot wait for standardized Laniakea infrastructure.

**Key principle:** All Phase 0 deployments are acknowledged technical debt. They operate outside Laniakea's standardized infrastructure (no Diamond PAU, no Configurator, no beacons) and will be converted to Core Halos at a later stage as Phase 1 infrastructure matures.

**Scope:** Grove (Star Prime) only. Other Primes follow the standard Phase 1+ track.

---

## Substages

| Substage | Name | Description |
|----------|------|-------------|
| **0.0** | Planning & Finalization | Inventory all remaining legacy/exception actions; accept technical debt explicitly |
| **0.1** | Custodial Crypto-Backed Lending | USDC → legal entity → offchain custodial crypto-backed lending |
| **0.2** | Crypto-Enabled Lending | USDC → legal entity → crypto-enabled lending |
| **0.3** | Tokenized RWA Trading | Early-stage tokenized RWA trading system (precursor to PSM3-based Halo Class) |
| **0.4** | Blockchain Bridge | Bridge to a new blockchain |
| **0.5** | Star4 Deployment | Initial Star4 deployment only; subsequent onboarding follows standard Phase 1 track |

---

### Phase 0.0: Planning & Finalization

**Objective:** Inventory and explicitly approve all remaining legacy and exceptional actions

- Enumerate every planned Phase 0 deployment with its expected technical debt
- Document what each deployment will look like when converted to a Core Halo
- Establish the understanding that these create non-standard infrastructure that will be standardized later
- Agree on monitoring/reporting requirements in the interim (before lpla-verify exists)

---

### Phase 0.1: Custodial Crypto-Backed Lending

**Objective:** Deploy assets for offchain custodial crypto-backed lending

**Mechanism:** USDC transferred to a legal entity that lends the assets as offchain custodial crypto-backed lending.

**Technical debt:**
- No Diamond PAU — deployed via legacy mechanisms
- No Configurator — operational changes require governance spells
- No beacon monitoring — manual oversight until Phase 1.2 infrastructure is available

**Core Halo path:** Will be wrapped as a Core Halo in Phase 1.3 (Legacy Cleanup & Core Halos).

---

### Phase 0.2: Crypto-Enabled Lending

**Objective:** Deploy assets for crypto-enabled lending

**Mechanism:** USDC transferred to a legal entity that uses it for crypto-enabled lending.

**Technical debt:**
- No Diamond PAU — deployed via legacy mechanisms
- No Configurator — operational changes require governance spells
- No beacon monitoring — manual oversight until Phase 1.2 infrastructure is available

**Core Halo path:** Will be wrapped as a Core Halo in Phase 1.3 (Legacy Cleanup & Core Halos).

---

### Phase 0.3: Tokenized RWA Trading

**Objective:** Deploy an early-stage system for trading tokenized RWAs

**Mechanism:** Initial deployment of a tokenized RWA trading capability. This is a precursor to a new Halo Class based on the PSM3 smart contract, which will be developed as the infrastructure matures.

**Technical debt:**
- Early-stage system, not yet integrated with Laniakea contract infrastructure
- Will require significant development to become a proper PSM3-based Halo Class

**Evolution path:** Does not simply become a Core Halo — instead evolves into a new Halo Class built on PSM3. The initial deployment provides operational experience that informs the PSM3 Halo Class design.

---

### Phase 0.4: Blockchain Bridge

**Objective:** Bridge assets to a new blockchain

**Mechanism:** Deploy a bridge enabling capital deployment on a new chain.

**Technical debt:**
- Bridge deployed outside standard Laniakea infrastructure
- No beacon monitoring of bridged assets until infrastructure matures

**Core Halo path:** Will be wrapped as a Core Halo in Phase 1.3 (Legacy Cleanup & Core Halos).

---

### Phase 0.5: Star4 Deployment

**Objective:** Initial deployment of Star4

**Important distinction:** Star4's *initial deployment* is a Phase 0 exception, but beyond this bootstrap:
- Star4 will **not** receive any further exceptions
- Star4 will use the **standardized Diamond PAU** once it is ready (Phase 1.1)
- All collateral onboarding for Star4 follows the **standard Phase 1 track** (Configurator, beacons, etc.)

**Mechanism:** Star4 is deployed via legacy/bootstrap mechanisms to establish the Prime. Once Phase 1.1 delivers Diamond PAU infrastructure, Star4 migrates to standardized architecture along with the other first-cohort Primes.

**Technical debt:** Minimal and short-lived — Star4 joins the standard track as soon as Diamond PAU is available.

---

## Relationship to Phase 1

```
Phase 0 (Exceptions)              Phase 1 (Standard Infrastructure)
─────────────────────             ──────────────────────────────────

0.0  Planning               ───→  Feeds into 1.3 (what becomes Core Halos)
0.1  Custodial Lending       ───→  Wrapped as Core Halo in 1.3
0.2  Crypto-Enabled Lending  ───→  Wrapped as Core Halo in 1.3
0.3  Tokenized RWA Trading   ───→  Evolves into PSM3-based Halo Class
0.4  Blockchain Bridge       ───→  Wrapped as Core Halo in 1.3
0.5  Star4 Deployment        ───→  Joins standard track from 1.1 onward
```

Phase 0 deployments run **concurrently** with Phase 1 development. They do not block Phase 1 progress — they are the pragmatic exceptions that allow Grove to operate while standardized infrastructure is being built.

---

## End State

At completion of Phase 0:
- All planned Grove exceptional deployments are live
- Each deployment has documented technical debt and a defined standardization path
- Phase 1.3 (Legacy Cleanup & Core Halos) has a clear inventory of assets to wrap
- Star4 is deployed and ready to migrate to Diamond PAU in Phase 1.1

---

## Links

- Roadmap overview: [roadmap-overview.md](./roadmap-overview.md)
- Phase 1 (standardized infrastructure): [phase-1-overview.md](./phase1/phase-1-overview.md)
- Core Halos and legacy cleanup: Phase 1.3 in [phase-1-overview.md](./phase1/phase-1-overview.md#phase-13-legacy-cleanup--core-halos)
