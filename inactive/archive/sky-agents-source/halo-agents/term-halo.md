# Term Halo — Business Overview

**Status:** Draft
**Last Updated:** 2026-03-01

---

## Executive Summary

A **Term Halo** is a Halo type that uses **NFATS** (Non-Fungible Allocation Token Standard) to create bespoke, individual capital deployment deals. Unlike Portfolio Halos (which use LCTS for pooled, fungible positions), Term Halos treat each deal as a distinct, non-fungible position with its own terms.

Term Halos separate the **liability side** (Halo Units — the NFATs held by Primes) from the **asset side** (Halo Books — balanced ledgers where assets equal liabilities for the units they back). This separation enables privacy protection: multiple assets can be blended in a book, preventing outsiders from inferring individual loan terms from NFAT data.

Term Halos are operated by two LPHA beacons:
- **lpha-nfat** — claims capital from queues, mints NFATs, manages book status, deploys funds, processes redemptions
- **lpha-attest** — operated by an independent Attestor; posts risk attestations about book contents into the Synome

> **Note:** Both are **LPHA beacons** — deterministic rule executors, not sentinels. Sentinels (stl-base, stl-stream, stl-warden) have continuous real-time control and proprietary intelligence. LPHA beacons apply rules exactly as written without judgment. See `beacon-framework.md` for the full taxonomy.

**Key value proposition**: Enable bespoke structured deals at scale — each NFAT can have different duration, size, and terms, while sharing the same legal buybox and smart contract infrastructure. Halo Books provide asset-side privacy and bankruptcy remoteness.

---

## Term vs Portfolio Halos

| Aspect | Portfolio Halo | Term Halo |
|--------|------------------|------------------|
| **Token Standard** | LCTS (pooled, fungible) | NFATS (individual, non-fungible) |
| **Terms** | Same for all participants | Bespoke per deal |
| **LPHA Beacon** | lpha-lcts | lpha-nfat |
| **Use Case** | Standardized asset manager products | Custom structured deals |
| **Position Type** | Shares in a pool | Claim on specific deployment |
| **Transferability** | Queue-based, generation-locked | NFT — transferable, collateralizable |

### When to Use Term Halos

- Asset manager partnerships with negotiated terms
- Deals where each depositor has different yield, duration, or conditions
- Situations requiring transferable positions (secondary market, collateralization)
- Regulated contexts where counterparty identity matters
- Complex structured products with varying tranches

### When to Use Portfolio Halos

- Open participation with uniform terms
- Capacity-constrained strategies where fair distribution matters
- Scenarios where fungibility and pooling are desirable

---

## Halo Class Structure

A Term Halo is organized into **Halo Classes** — each Halo Class is an **NFAT Facility** that defines a buybox of acceptable deal parameters. Within each class, **Halo Units** (NFATs) represent the liability side and **Halo Books** represent the asset side.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        STRUCTURING HALO                                  │
│                                                                          │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │              HALO CLASS: Senior Secured Facility                 │   │
│   │              (Shared PAU + lpha-nfat + lpha-attest + Buybox)     │   │
│   │                                                                  │   │
│   │   LIABILITY SIDE (Halo Units / NFATs):                           │   │
│   │   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │   │
│   │   │ NFAT #1  │  │ NFAT #2  │  │ NFAT #3  │  │ NFAT #4  │       │   │
│   │   │ 6mo,25M  │  │ 12mo,50M │  │ 18mo,30M │  │ 9mo,15M  │       │   │
│   │   │ Spark    │  │ Grove    │  │ Spark    │  │ Keel     │       │   │
│   │   └─────┬────┘  └─────┬────┘  └────┬─────┘  └────┬─────┘       │   │
│   │         │              │            │              │              │   │
│   │         └──────┬───────┘            └──────┬───────┘              │   │
│   │                ▼                           ▼                      │   │
│   │   ASSET SIDE (Halo Books):                                       │   │
│   │   ┌────────────────────┐       ┌────────────────────┐            │   │
│   │   │ Book α             │       │ Book β             │            │   │
│   │   │ Loan A + Loan B    │       │ Loan C + Loan D    │            │   │
│   │   │ (backs #1, #2)     │       │ (backs #3, #4)     │            │   │
│   │   └────────────────────┘       └────────────────────┘            │   │
│   │                                                                  │   │
│   │   Units on same book: pari passu on losses                       │   │
│   │   Units on different books: fully isolated                       │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │              HALO CLASS: Mezzanine Facility                      │   │
│   │              (Different buybox, same pattern)                    │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### What a Halo Class (NFAT Facility) Shares

| Component | Description |
|-----------|-------------|
| **PAU** | Controller + ALMProxy + RateLimits for all NFATs in the facility |
| **LPHA Beacons** | `lpha-nfat` manages issuance, deployment, and redemption; `lpha-attest` posts attestations |
| **Legal Buybox** | Acceptable parameter ranges, counterparty requirements, recourse |
| **Queue Contract** | Where Primes deposit capital awaiting deal execution |
| **Redeem Contract** | Where Halo deposits funds for NFAT holders to claim |

### Halo Units (Liability Side)

Each NFAT is a Halo Unit — a claim on a Halo Book. Units can vary within the buybox:

| Parameter | Variation Within Buybox |
|-----------|------------------------|
| **Duration** | Different maturities (e.g., 6mo vs 18mo) |
| **Size** | Different notional amounts |
| **APY** | Different yields within acceptable range |
| **Counterparty** | Different Primes for each NFAT |
| **Specific Terms** | Payment schedules, early redemption conditions |

### Halo Books (Asset Side)

Each Halo Book is a balanced ledger — assets on one side, the liabilities owed to its units on the other — providing bankruptcy remoteness for the positions it backs:

| Property | Description |
|----------|-------------|
| **Bankruptcy remoteness** | The book is the isolation boundary — not the unit |
| **Loss distribution** | Pari passu across units on the same book (unless tranched) |
| **Privacy** | Multiple assets blended in a book prevent inference of individual loan terms |
| **Composition** | Whole assets per book |
| **Recursive** | A book can hold Halo Units from other books as assets |

### Terms Source

| Mode | Description |
|------|-------------|
| **General buybox** | Halo Class defines ranges; units fall within the buybox. Halo has flexibility. |
| **Ecosystem accord** | Pre-negotiated agreement specifying individual unit and book terms. Overrides the buybox. |

---

## Beacons: lpha-nfat and lpha-attest

Two LPHA beacons operate a Term Halo. Neither can act alone on deployment — the attestor must post an attestation before the Halo can transition a book.

### lpha-nfat — Halo Operations

The **lpha-nfat beacon** is the operational backbone. It operates the NFAT Facility's PAU and manages the complete lifecycle of each NFAT and book.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          lpha-nfat BEACON                                 │
│                                                                          │
│   ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐   │
│   │  1. ISSUANCE    │     │  2. DEPLOYMENT  │     │  3. REDEMPTION  │   │
│   │                 │     │                 │     │                 │   │
│   │  • Monitor      │     │  • Transition   │     │  • Receive      │   │
│   │    Prime queues │     │    book to      │     │    returned     │   │
│   │  • Validate     │────▶│    deploying    │────▶│    funds        │   │
│   │    deal terms   │     │    (requires    │     │  • Move to      │   │
│   │  • Mint NFAT    │     │    attestation) │     │    Redeem       │   │
│   │  • Assign to    │     │  • Transfer via │     │    Contract     │   │
│   │    book         │     │    PAU to RWA   │     │  • Notify       │   │
│   │                 │     │                 │     │    NFAT holder  │   │
│   └─────────────────┘     └─────────────────┘     └─────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### lpha-attest — Independent Attestor

The **lpha-attest beacon** is operated by an independent Attestor company whitelisted by Sky governance. It posts risk attestations about book contents into the Synome.

| Property | Description |
|----------|-------------|
| **Capability** | Write attestations into Synome |
| **Cannot** | Move capital, mint NFATs, change book status directly |
| **Accountability** | Subject to its own govops supply chain of checks and audits |

**Two-beacon deployment gate:**

```
ATTESTOR                          SYNOME                          HALO
(lpha-attest)                                                   (lpha-nfat)
    │                                │                               │
    │  1. Upload attestation         │                               │
    │  ─────────────────────────────▶│                               │
    │                                │  2. Attestation present ✓     │
    │                                │  ────────────────────────────▶│
    │                                │                               │
    │                                │  3. Book → deploying          │
    │                                │  ◀────────────────────────────│
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
│            │ 2. lpha-nfat claims, mints NFAT, assigns to book            │
│            ▼                                                             │
│   ┌─────────────────┐        ┌─────────────────┐                        │
│   │    lpha-nfat     │───────▶│   NFAT minted   │───────▶ PRIME holds    │
│   │   LPHA BEACON   │        │   (Halo Unit)   │         transferable   │
│   └────────┬────────┘        └─────────────────┘         position       │
│            │                                                             │
│   ┌────────┴────────┐                                                    │
│   │   HALO BOOK     │  ← Book fills (may add more NFATs over time)      │
│   │  (asset side)   │  ← USDS earns agent rate while in filling phase   │
│   └────────┬────────┘                                                    │
│            │                                                             │
│            │ 3. lpha-attest posts attestation (risk characteristics)     │
│            │    lpha-nfat transitions book → deploying                   │
│            │                                                             │
│            │ 4. Deploy via PAU (obfuscated — high CRR)                  │
│            ▼                                                             │
│   ┌─────────────────┐                                                    │
│   │      PAU        │                                                    │
│   │  (rate-limited) │                                                    │
│   └────────┬────────┘                                                    │
│            │                                                             │
│            │ 5. Funds to RWA (Schrödinger's risk during deployment)     │
│            ▼                                                             │
│   ┌─────────────────┐                                                    │
│   │  RWA ENDPOINT   │  ← lpha-attest posts "at rest" attestation        │
│   │                 │  ← Book transitions to at rest (lower CRR)        │
│   │                 │  ← Ongoing re-attestation per asset type           │
│   └────────┬────────┘                                                    │
│            │                                                             │
│            │ 6. At maturity: return funds                               │
│            ▼                                                             │
│   ┌─────────────────┐                                                    │
│   │      PAU        │                                                    │
│   └────────┬────────┘                                                    │
│            │                                                             │
│            │ 7. lpha-nfat moves to Redeem Contract                       │
│            ▼                                                             │
│   ┌─────────────────┐                                                    │
│   │ REDEEM CONTRACT │                                                    │
│   └────────┬────────┘                                                    │
│            │                                                             │
│            │ 8. NFAT holder claims, NFAT burned                         │
│            ▼                                                             │
│   PRIME (or transferee) receives principal + yield                      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Book Lifecycle and Privacy

Halo Books progress through defined phases. See `nfats.md` for full specification.

| Phase | Synome Visibility | CRR Impact |
|-------|-------------------|------------|
| **Filling** | Full transparency — book holds USDS earning agent rate | Low |
| **Deploying** | Obfuscated — attestor forward-looking only (Schrödinger's risk) | **High** |
| **At Rest** | Attestor-confirmed risk characteristics (not individual borrower details) | Medium |
| **Unwinding** | Halo funds Redeem Contract from book proceeds | — |
| **Closed** | All units redeemed | — |

**Privacy mechanism:** Multiple assets are blended in a book, and multiple NFATs issued against the blended collateral. Individual loan terms cannot be inferred from NFAT data — only the blended risk characteristics (as attested by the Attestor) are visible in the Synome.

**CRR incentives:** The higher CRR during deployment encourages Halos to minimize the obfuscated phase duration and stagger deployments across books — balancing borrower privacy against capital efficiency without mandating specific behavior.

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

Bankruptcy remoteness is at the **Halo Book** level — the balanced ledger matching assets to the liabilities owed to its units:

- Units sharing a book are **pari passu** on losses (unless tranched within the book)
- Units on different books are **fully isolated** — if one book's assets fail, other books are protected
- Each book is like a serialized LLC
- In the simplest case (1 unit : 1 book : 1 asset), the effect is the same as per-unit isolation

### Governance Artifacts

| Artifact | Contents |
|----------|----------|
| **Halo Artifact** | Overall governance, buybox definitions, recourse mechanisms |
| **Unit Artifact** | Per-NFAT operational parameters, legal recourse, deal terms |
| **Book Records** | Asset-side composition, attestor attestations, deployment status |
| **Synome Records** | Real-time position data, yield schedules, maturity tracking, book assignments |

---

## Operational Oversight

The beacons operate alongside other beacons for safety:

| Component | Type | Role |
|-----------|------|------|
| **lpha-nfat** | LPHA beacon | Primary execution — issuance, book management, deployment, redemption |
| **lpha-attest** | LPHA beacon | Independent attestations — risk characteristics of book contents |
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

## Launching a Term Halo

### Process Overview

1. **Define Buybox** — parameter ranges, counterparty requirements, asset types
2. **Legal Framework** — establish Halo Artifact, recourse mechanisms
3. **Deploy Infrastructure** — PAU, Queue, Redeem, NFAT contracts (manual w/ spells in Phases 1–3; via Laniakea Factory from Phase 5)
4. **Configure Beacon** — `lpha-nfat` with appropriate pBEAMs
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

Term Halos enable **bespoke structured deals at institutional scale**:

- **NFAT-based** — each position is individual, non-fungible, transferable
- **Asset-liability separated** — Halo Units (NFATs) on liability side, Halo Books on asset side
- **Privacy-preserving** — blended books prevent inference of individual loan terms
- **Buybox-constrained** — deals vary within defined parameters (or via ecosystem accord)
- **Two-beacon operated** — lpha-nfat handles execution, lpha-attest provides independent attestations
- **PAU-integrated** — standard Laniakea rate-limited infrastructure
- **Bankruptcy remote** — at the book level; pari passu within a book, isolated across books
- **CRR-incentivized** — risk model encourages short deployment phases and staggered deployments

The capital flow mirrors Prime operations (ingress → deploy → manage → redeem), but lpha-nfat is an LPHA beacon (deterministic rule execution) rather than a sentinel (real-time intelligent control).

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| `nfats.md` | NFAT standard specification |
| `portfolio-halo.md` | Portfolio Halo (LCTS-based alternative) |
| `sentinel-network.md` | Sentinel formation architecture (stl-base, stl-stream, stl-warden) |
| `beacon-framework.md` | lpha-nfat as LPHA beacon |

---

*Document Version: 0.2*
*Last Updated: 2026-03-01*
