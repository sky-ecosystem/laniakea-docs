# Structuring Halo — Business Overview

**Status:** Draft
**Last Updated:** 2026-01-27

---

## Executive Summary

A **Structuring Halo** is a Halo type that uses **NFATS** (Non-Fungible Allocation Token Standard) to create bespoke, individual capital deployment deals. Unlike Passthrough Halos (which use LCTS for pooled, fungible positions), Structuring Halos treat each deal as a distinct, non-fungible position with its own terms.

Structuring Halos are operated by **lpha-nfat beacons** (LPHA — Low Power, High Authority) that:
1. Claim capital from Prime queues when deals are struck
2. Mint NFATs representing claims on individual Halo Units
3. Deploy funds via the PAU to RWA endpoints
4. Process redemptions when funds return to the PAU

> **Note:** lpha-nfat is an **LPHA beacon** — a deterministic rule executor, not a sentinel. Sentinels (stl-base, stl-stream, stl-warden) have continuous real-time control and proprietary intelligence. LPHA beacons like lpha-nfat apply rules exactly as written without judgment. See `beacon-framework.md` for the full taxonomy.

**Key value proposition**: Enable bespoke structured deals at scale — each NFAT can have different duration, size, and terms, while sharing the same legal buybox and smart contract infrastructure.

---

## Structuring vs Passthrough Halos

| Aspect | Passthrough Halo | Structuring Halo |
|--------|------------------|------------------|
| **Token Standard** | LCTS (pooled, fungible) | NFATS (individual, non-fungible) |
| **Terms** | Same for all participants | Bespoke per deal |
| **LPHA Beacon** | lpha-lcts | lpha-nfat |
| **Use Case** | Standardized asset manager products | Custom structured deals |
| **Position Type** | Shares in a pool | Claim on specific deployment |
| **Transferability** | Queue-based, generation-locked | NFT — transferable, collateralizable |

### When to Use Structuring Halos

- Asset manager partnerships with negotiated terms
- Deals where each depositor has different yield, duration, or conditions
- Situations requiring transferable positions (secondary market, collateralization)
- Regulated contexts where counterparty identity matters
- Complex structured products with varying tranches

### When to Use Passthrough Halos

- Open participation with uniform terms
- Capacity-constrained strategies where fair distribution matters
- Scenarios where fungibility and pooling are desirable

---

## Halo Class Structure

A Structuring Halo is organized into **Halo Classes** — each Halo Class is an **NFAT Facility** that defines a buybox of acceptable deal parameters.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        STRUCTURING HALO                                  │
│                                                                          │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                 HALO CLASS: Senior Secured Facility              │   │
│   │                 (Shared PAU + lpha-nfat + Legal Buybox)          │   │
│   │                                                                  │   │
│   │   Buybox Parameters:                                             │   │
│   │   - Duration: 6-24 months                                        │   │
│   │   - Size: 5M-100M per NFAT                                      │   │
│   │   - APY: 8-15%                                                   │   │
│   │   - Counterparties: Approved Primes only                        │   │
│   │                                                                  │   │
│   │   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │   │
│   │   │ NFAT #1  │  │ NFAT #2  │  │ NFAT #3  │  │ NFAT #4  │       │   │
│   │   │ 6mo,25M  │  │ 12mo,50M │  │ 18mo,30M │  │ 9mo,15M  │       │   │
│   │   │ Spark    │  │ Grove    │  │ Spark    │  │ Keel     │       │   │
│   │   └──────────┘  └──────────┘  └──────────┘  └──────────┘       │   │
│   │                                                                  │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                 HALO CLASS: Mezzanine Facility                   │   │
│   │                 (Different buybox, same pattern)                 │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### What a Halo Class (NFAT Facility) Shares

| Component | Description |
|-----------|-------------|
| **PAU** | Controller + ALMProxy + RateLimits for all NFATs in the facility |
| **Sentinel** | lpha-nfat formation manages issuance, deployment, and redemption |
| **Legal Buybox** | Acceptable parameter ranges, counterparty requirements, recourse |
| **Queue Contract** | Where Primes deposit capital awaiting deal execution |
| **Redeem Contract** | Where Halo deposits funds for NFAT holders to claim |

### What Individual NFATs (Halo Units) Can Vary

| Parameter | Variation Within Buybox |
|-----------|------------------------|
| **Duration** | Different maturities (e.g., 6mo vs 18mo) |
| **Size** | Different notional amounts |
| **APY** | Different yields within acceptable range |
| **Counterparty** | Different Primes for each NFAT |
| **Specific Terms** | Payment schedules, early redemption conditions |

---

## The lpha-nfat LPHA Beacon

The **lpha-nfat beacon** is the operational backbone of a Structuring Halo. It operates the NFAT Facility's PAU and manages the complete lifecycle of each NFAT.

### Beacon Responsibilities

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          lpha-nfat SENTINEL                               │
│                                                                          │
│   ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐   │
│   │  1. ISSUANCE    │     │  2. DEPLOYMENT  │     │  3. REDEMPTION  │   │
│   │                 │     │                 │     │                 │   │
│   │  • Monitor      │     │  • Transfer     │     │  • Receive      │   │
│   │    Prime queues │     │    funds via    │     │    returned     │   │
│   │  • Validate     │────▶│    PAU to RWA   │────▶│    funds        │   │
│   │    deal terms   │     │    endpoint     │     │  • Move to      │   │
│   │  • Mint NFAT    │     │  • Update       │     │    Redeem       │   │
│   │  • Claim from   │     │    Synome       │     │    Contract     │   │
│   │    queue        │     │    position     │     │  • Notify       │   │
│   │                 │     │    data         │     │    NFAT holder  │   │
│   └─────────────────┘     └─────────────────┘     └─────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Phase 1: NFAT Issuance

When a deal is struck between a Prime and the Halo:

1. **Prime deposits sUSDS** into the Facility's Queue Contract
2. **lpha-nfat validates** that deal terms fall within the buybox
3. **lpha-nfat claims** the capital from the queue
4. **lpha-nfat mints an NFAT** representing the Prime's claim
5. **Deal terms recorded** in Synome (APY, maturity, payment schedule)

```
Prime                    Queue Contract               lpha-nfat
  │                            │                          │
  │  1. Deposit sUSDS          │                          │
  │  ─────────────────────────▶│                          │
  │                            │                          │
  │                            │  2. Deal struck          │
  │                            │  ─────────────────────▶  │
  │                            │                          │
  │                            │  3. Claim from queue     │
  │                            │  ◀─────────────────────  │
  │                            │                          │
  │  4. Receive NFAT           │                          │
  │  ◀─────────────────────────────────────────────────   │
  │                            │                          │
  │                            │  5. Record terms         │
  │                            │     in Synome            │
```

### Phase 2: Capital Deployment

Once the NFAT is minted, lpha-nfat deploys the capital:

1. **lpha-nfat transfers funds** from the Facility to the RWA endpoint via the PAU
2. **Rate limits enforced** by the PAU's RateLimits contract
3. **Position data updated** in Synome and Halo Artifact
4. **Off-ramp executed** (stablecoin → fiat if needed)

```
lpha-nfat                 PAU                    RWA Endpoint
  │                       │                          │
  │  1. Deploy 25M        │                          │
  │  ─────────────────────▶│                          │
  │                       │  2. Rate limit check     │
  │                       │  (within bounds ✓)       │
  │                       │                          │
  │                       │  3. Transfer to endpoint │
  │                       │  ─────────────────────▶  │
  │                       │                          │
  │  4. Update Synome     │                          │
  │     position data     │                          │
```

### Phase 3: Redemption Processing

When funds return to the PAU (at maturity or early redemption):

1. **RWA endpoint returns funds** to the PAU (principal + yield)
2. **lpha-nfat detects** the incoming funds
3. **lpha-nfat transfers** funds to the Redeem Contract
4. **NFAT holder notified** that redemption is available
5. **NFAT holder claims** from Redeem Contract (burns NFAT)

```
RWA Endpoint             PAU                lpha-nfat            Redeem Contract
     │                    │                     │                      │
     │  1. Return funds   │                     │                      │
     │  ─────────────────▶│                     │                      │
     │                    │                     │                      │
     │                    │  2. Funds received  │                      │
     │                    │  ─────────────────▶ │                      │
     │                    │                     │                      │
     │                    │                     │  3. Move to Redeem   │
     │                    │                     │  ───────────────────▶│
     │                    │                     │                      │
     │                    │                     │  4. Notify holder    │
     │                    │                     │                      │
                                                                       │
NFAT Holder ──────────────────────────────────────── 5. Claim funds ──▶│
            ◀─────────────────────────────────────── 6. Receive funds ─│
            (NFAT burned)
```

---

## NFAT Facility Components

### Queue Contract

Where Primes deposit capital awaiting deal execution.

| Property | Description |
|----------|-------------|
| **Deposits** | sUSDS from approved Primes |
| **Visibility** | Primes can see their queue position |
| **Withdrawal** | Primes can exit queue before deal execution |
| **Claiming** | Only lpha-nfat can claim from queue |

### Redeem Contract

Where the Halo deposits funds for NFAT holders to claim.

| Property | Description |
|----------|-------------|
| **Deposits** | lpha-nfat deposits returned funds |
| **Claims** | NFAT holder presents NFAT to claim |
| **NFAT Burn** | Claiming burns the NFAT |
| **Partial** | Supports partial redemptions for amortizing deals |

### PAU (Parallelized Allocation Unit)

Standard Laniakea infrastructure for capital flows.

| Component | Function |
|-----------|----------|
| **Controller** | Authorization and access control |
| **ALMProxy** | Asset-liability management interface |
| **RateLimits** | Flow constraints (SORL-governed) |

---

## Capital Flow Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        COMPLETE NFAT LIFECYCLE                           │
│                                                                          │
│   PRIME                                                                  │
│     │                                                                    │
│     │ 1. Deposit sUSDS to Queue                                         │
│     ▼                                                                    │
│   ┌─────────────────┐                                                    │
│   │  QUEUE CONTRACT │                                                    │
│   └────────┬────────┘                                                    │
│            │                                                             │
│            │ 2. lpha-nfat claims, mints NFAT                             │
│            ▼                                                             │
│   ┌─────────────────┐        ┌─────────────────┐                        │
│   │    lpha-nfat     │───────▶│   NFAT minted   │───────▶ PRIME holds    │
│   │    SENTINEL     │        │   (ERC-721)     │         transferable   │
│   └────────┬────────┘        └─────────────────┘         position       │
│            │                                                             │
│            │ 3. Deploy via PAU                                          │
│            ▼                                                             │
│   ┌─────────────────┐                                                    │
│   │      PAU        │                                                    │
│   │  (rate-limited) │                                                    │
│   └────────┬────────┘                                                    │
│            │                                                             │
│            │ 4. Funds to RWA                                            │
│            ▼                                                             │
│   ┌─────────────────┐                                                    │
│   │  RWA ENDPOINT   │  ← Yield accrues, terms tracked in Synome         │
│   └────────┬────────┘                                                    │
│            │                                                             │
│            │ 5. At maturity: return funds                               │
│            ▼                                                             │
│   ┌─────────────────┐                                                    │
│   │      PAU        │                                                    │
│   └────────┬────────┘                                                    │
│            │                                                             │
│            │ 6. lpha-nfat moves to Redeem Contract                       │
│            ▼                                                             │
│   ┌─────────────────┐                                                    │
│   │ REDEEM CONTRACT │                                                    │
│   └────────┬────────┘                                                    │
│            │                                                             │
│            │ 7. NFAT holder claims, NFAT burned                         │
│            ▼                                                             │
│   PRIME (or transferee) receives principal + yield                      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Legal Infrastructure

### The Buybox Model

Each NFAT Facility defines a **buybox** — the acceptable parameter ranges for deals within that facility:

| Parameter | Example Buybox |
|-----------|----------------|
| **Duration Range** | 6-24 months |
| **Size Range** | 5M-100M per NFAT |
| **APY Range** | 8-15% |
| **Counterparties** | Approved Primes only |
| **Asset Types** | Senior secured loans, investment-grade bonds |
| **Jurisdiction** | Specified regulatory frameworks |

Any deal within the buybox can be executed by lpha-nfat without additional governance approval. Deals outside the buybox require governance intervention.

### Bankruptcy Remoteness

Each NFAT represents a claim on a distinct **Halo Unit** — a governance-level construct that is legally and operationally isolated:

- If one NFAT's underlying deal fails, other NFATs are protected
- Each Halo Unit is like a serialized LLC
- Recourse is limited to the specific Unit's assets

### Governance Artifacts

| Artifact | Contents |
|----------|----------|
| **Halo Artifact** | Overall governance, buybox definitions, recourse mechanisms |
| **Unit Artifact** | Per-NFAT operational parameters, legal recourse, deal terms |
| **Synome Records** | Real-time position data, yield schedules, maturity tracking |

---

## Operational Oversight

The lpha-nfat beacon operates alongside other beacons for safety:

| Component | Type | Role |
|-----------|------|------|
| **lpha-nfat** | LPHA beacon | Primary execution — issuance, deployment, redemption |
| **stl-warden** | Sentinel | Independent oversight — risk monitoring, halt authority |
| **lpla-checker** | LPLA beacon | Protocol-level position verification |

### Beacon Permissions

| Action | Required Permission |
|--------|---------------------|
| Claim from Queue | pBEAM on Queue Contract |
| Mint NFAT | pBEAM on NFAT Contract |
| Deploy via PAU | pBEAM on Controller |
| Move to Redeem | pBEAM on Redeem Contract |

All actions are rate-limited and logged. Wardens can halt operations if risk thresholds are breached.

---

## Comparison with Sentinel Formations

The lpha-nfat beacon follows a similar capital flow pattern to sentinel formations, but operates deterministically rather than with proprietary intelligence:

| Aspect | Sentinel Formation (stl-base) | Halo LPHA Beacon (lpha-nfat) |
|--------|-------------------------------|------------------------------|
| **Type** | HPHA sentinel | LPHA beacon |
| **Intelligence** | Proprietary, real-time | Deterministic, rule-based |
| **Ingress** | Risk capital from Primes | NFAT capital from Primes |
| **Deploy** | Leverage into yield opportunities | Funds to RWA endpoints |
| **Manage** | Trading positions | NFAT positions |
| **Egress** | Returns to Prime treasury | Returns to Redeem Contract |

Both operate PAUs and are rate-limited. Sentinel formations have warden oversight for their real-time decisions; LPHA beacons execute predefined rules.

---

## Benefits for Counterparties

### For Primes

- **Bespoke terms** — negotiate specific duration, size, yield
- **Transferable positions** — NFATs can be sold or used as collateral
- **Transparency** — all terms recorded in Synome
- **Isolation** — each NFAT is bankruptcy remote

### For Asset Managers

- **Scalable bespoke deals** — same legal framework, many individual transactions
- **Automated operations** — lpha-nfat handles execution
- **Clear recourse** — buybox and Halo Artifact define all terms
- **Institutional capital** — access to Prime allocations

---

## Launching a Structuring Halo

### Process Overview

1. **Define Buybox** — parameter ranges, counterparty requirements, asset types
2. **Legal Framework** — establish Halo Artifact, recourse mechanisms
3. **Deploy Infrastructure** — PAU, Queue, Redeem, NFAT contracts via Laniakea Factory
4. **Configure Sentinel** — lpha-nfat with appropriate pBEAMs
5. **Governance Approval** — Halo Artifact Edit
6. **Go Live** — Primes can queue capital, lpha-nfat executes deals

### Timeline

| Phase | Duration |
|-------|----------|
| Buybox definition | 1-2 weeks |
| Legal framework | 2-4 weeks (reuses templates) |
| Smart contract deployment | Days (factory deployment) |
| Governance approval | ~1 week |
| **Total** | **4-8 weeks** |

---

## Summary

Structuring Halos enable **bespoke structured deals at institutional scale**:

- **NFAT-based** — each position is individual, non-fungible, transferable
- **Buybox-constrained** — deals vary within defined parameters
- **LPHA beacon-operated** — lpha-nfat handles the complete lifecycle deterministically
- **PAU-integrated** — standard Laniakea rate-limited infrastructure
- **Bankruptcy remote** — each NFAT is a separate Halo Unit

The capital flow mirrors Prime operations (ingress → deploy → manage → redeem), but lpha-nfat is an LPHA beacon (deterministic rule execution) rather than a sentinel (real-time intelligent control).

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| `nfats.md` | NFAT standard specification |
| `passthrough-halo.md` | Alternative Halo type using LCTS |
| `sentinel-network.md` | Sentinel formation architecture (stl-base, stl-stream, stl-warden) |
| `beacon-framework.md` | lpha-nfat as LPHA beacon |

---

*Document Version: 0.1*
*Last Updated: 2026-01-27*
