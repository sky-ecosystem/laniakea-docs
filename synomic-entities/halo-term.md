# Term Halo

A Term Halo is a Standard Halo Class that uses **NFATS** (Non-Fungible Allocation Token Standard) for bespoke, individual capital deployment deals. Unlike Portfolio Halos (which use LCTS for pooled, fungible positions), Term Halos treat each deal as a distinct, non-fungible position with its own terms.

For the Class / Book / Unit architecture, see [`halo-classes.md`](halo-classes.md). For the NFAT contract spec, see [`../smart-contracts/nfats.md`](../smart-contracts/nfats.md).

---

## Term vs Portfolio

| Aspect | Portfolio | Term |
|---|---|---|
| Token standard | LCTS (pooled, fungible) | NFATS (individual, non-fungible) |
| Terms | Same for all participants | Bespoke per deal |
| Beacon | `lcts-{halo}` | `nfat-{halo}` + `attest-data-{class}` |
| Position type | Shares in a pool | Claim on specific deployment |
| Transferability | Queue-based, generation-locked | NFT — transferable, optionally collateralizable |

### When to use Term Halos

- Asset manager partnerships with negotiated terms
- Deals where each depositor has different yield, duration, conditions
- Situations requiring transferable positions (secondary market, collateralization)
- Regulated contexts where counterparty identity matters
- Complex structured products with varying tranches

---

## Two-Beacon Pattern

A Term Halo is operated by two high-authority beacons. Neither can act alone on deployment — the attestor must post an attestation before the Halo can transition a book.

### nfat-{halo} (relay)

The operational backbone. Manages NFAT issuance, book status transitions, capital deployment, redemption. Class: `relay`.

| Phase | Action |
|---|---|
| Issuance | Monitor Prime queues, validate deal terms against the buybox, claim from queue, mint NFAT, assign to book |
| Deployment | Transition book to deploying (after attestation); transfer via PAU to RWA endpoint |
| Redemption | Receive returned funds; move to Redeem Contract; notify NFAT holder |

### attest-data-{class} (attest-data-beacon)

Operated by an independent Attestor / Oracle Entity whitelisted by Sky governance. Posts risk attestations about book contents into the target exobook Spaces in the Synome. Class: `attest-data-beacon`.

| Property | Description |
|---|---|
| Capability | Write attestations into Synome |
| Cannot | Move capital, mint NFATs, change book status directly |
| Accountability | Subject to its own govops supply chain of checks and audits |

### Two-beacon deployment gate

```
ATTESTOR                          SYNOME                          HALO
(attest-data-{class})                                          (nfat-{halo})
    │                                │                               │
    │  1. Upload attestation         │                               │
    │  ─────────────────────────────▶│                               │
    │                                │  2. Attestation present ✓     │
    │                                │  ────────────────────────────▶│
    │                                │                               │
    │                                │  3. Book → deploying          │
    │                                │  ◀────────────────────────────│
```

`attest-data-{class}` is an attest-data beacon (class `attest-data-beacon`, admin'd by an Oracle Entity); `nfat-{halo}` is a relay beacon (class `relay`). For the canonical taxonomy, see [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md).

---

## Class Structure

A Term Halo organizes into Halo Classes — each Class is an **NFAT Facility** that defines a buybox of acceptable deal parameters. Within a Class, **Halo Units** (NFATs) represent the liability side and **Halo Books** the asset side.

```
HALO CLASS: Senior Secured Facility
(Shared PAU + nfat-{halo} + attest-data-{class} + Buybox)

LIABILITY SIDE (Halo Units / NFATs):
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ NFAT #1  │  │ NFAT #2  │  │ NFAT #3  │  │ NFAT #4  │
│ 6mo,25M  │  │ 12mo,50M │  │ 18mo,30M │  │ 9mo,15M  │
│ Spark    │  │ Grove    │  │ Spark    │  │ Keel     │
└─────┬────┘  └─────┬────┘  └────┬─────┘  └────┬─────┘
      │             │            │             │
      └──────┬──────┘            └──────┬──────┘
             ▼                          ▼
ASSET SIDE (Halo Books):
┌────────────────────┐       ┌────────────────────┐
│ Book α             │       │ Book β             │
│ Loan A + Loan B    │       │ Loan C + Loan D    │
│ (backs #1, #2)     │       │ (backs #3, #4)     │
└────────────────────┘       └────────────────────┘

Units on same book: pari passu on losses
Units on different books: fully isolated
```

### Buybox

| Parameter | Example |
|---|---|
| Duration range | 6-24 months |
| Size range | 5M-100M per NFAT |
| APY range | 8-15% |
| Counterparties | Approved Primes only |
| Asset types | Senior secured loans, investment-grade bonds |
| Jurisdiction | Specified regulatory frameworks |

Any deal within the buybox can be executed by `nfat-{halo}` without additional governance. Outside the buybox requires governance intervention.

### Terms source

| Mode | Description |
|---|---|
| **General buybox** | Halo Class defines ranges; Units fall within. Halo has flexibility. |
| **Ecosystem accord** | Pre-negotiated agreement specifying individual Unit and Book terms. Overrides the general buybox. More constrained, more predictable. |

---

## Book Lifecycle

Books progress through phases with different transparency and capital requirements. The full lifecycle and CRR incentive structure is in [`halo-classes.md`](halo-classes.md). The phases for Term Halos:

| Phase | Action | CRR Impact |
|---|---|---|
| **Filling** | NFATs swept in; book holds USDS earning agent rate | Low |
| **Deploying** | Capital offboarded (USDS → USDC → deployed to borrowers); attestation gates entry | High |
| **At Rest** | Fully deployed; attestor confirms risk characteristics; ongoing re-attestation | Medium |
| **Unwinding** | Assets return; Halo funds Redeem Contract | — |
| **Closed** | All Units redeemed | — |

The high-CRR Deploying phase creates economic incentive to keep deployment short. Re-attestation cadence at At-Rest affects CRR — more frequent attestation enables lower CRR. This balances borrower privacy against capital efficiency without mandating specific behavior.

> **CRR calibration ownership:** Qualitative incentive structure (Low/High/Medium) defined here and in [`halo-classes.md`](halo-classes.md). Numeric CRR values per book-phase are owned by [`../risk-framework/capital-formula.md`](../risk-framework/capital-formula.md).

---

## Capital Flow Lifecycle

```
PRIME
  │
  │ 1. Deposit sUSDS to Queue
  ▼
QUEUE CONTRACT
  │
  │ 2. nfat-{halo} claims, mints NFAT, assigns to book
  ▼
HALO BOOK (asset side)
  │  (USDS earns agent rate while in filling phase)
  │
  │ 3. attest-data-{class} posts attestation; nfat-{halo} transitions book → deploying
  │
  │ 4. Deploy via PAU (obfuscated — high CRR)
  ▼
PAU (rate-limited)
  │
  │ 5. Funds to RWA (Schrödinger's risk during deployment)
  ▼
RWA ENDPOINT
  │  (attest-data-{class} posts "at rest" attestation; book transitions; lower CRR)
  │  (Ongoing re-attestation per asset type)
  │
  │ 6. At maturity: return funds
  ▼
PAU
  │
  │ 7. nfat-{halo} moves to Redeem Contract
  ▼
REDEEM CONTRACT
  │
  │ 8. NFAT holder claims; NFAT burned (or spent for partial redemptions)
  ▼
PRIME (or transferee) receives principal + yield
```

For the on-chain mechanics (Queue Contract, Redeem Contract, NFAT minting, payment patterns — bullet / amortizing / periodic interest), see [`../smart-contracts/nfats.md`](../smart-contracts/nfats.md).

---

## Privacy Mechanism

Multiple assets are blended in a book; multiple NFATs are issued against the blended collateral. Individual loan terms cannot be inferred from NFAT data — only blended risk characteristics (as attested by the Attestor) are visible in the Synome.

This is what the book boundary buys you: privacy + bankruptcy remoteness. Without books, the isolation boundary would be either the Class (too broad — one bad deal contaminates everything) or the Unit (impractical — every NFAT would need its own legal entity). Books sit in between.

---

## Governance Artifacts

| Artifact | Contents |
|---|---|
| **Halo Artifact** | Overall governance, buybox definitions, recourse mechanisms |
| **Unit Artifact** | Per-NFAT operational parameters, legal recourse, deal terms |
| **Book records** | Asset-side composition, attestor attestations, deployment status |
| **Synome records** | Real-time position data, yield schedules, maturity tracking, book assignments |

---

## Comparison with Operating Setups

`nfat-{halo}` follows a similar capital flow pattern to a full Prime operating setup, but operates as a plain relay (deterministic):

| Aspect | Stream-sentinel (e.g. `stream-{prime}-{actor}`) | `nfat-{halo}` (relay) |
|---|---|---|
| Beacon class | Sentinel (stream variant), high call-out density | Relay (deterministic, low call-out density) |
| Intelligence | Proprietary, real-time | Rule-based |
| Ingress | Risk capital from Primes | NFAT capital from Primes |
| Deploy | Leverage into yield opportunities | Funds to RWA endpoints |
| Manage | Trading positions | NFAT positions |
| Egress | Returns to Prime treasury | Returns to Redeem Contract |

Both operate PAUs and are rate-limited. A full operating setup (baseline-relay + warden-relay + stream-sentinel) has warden oversight and stream-driven proprietary calls; plain relays execute predefined rules. See [`../sentinel/sentinel-network.md`](../sentinel/sentinel-network.md) for the operating-setup pattern, and [`../noemar-synlang/synlang-patterns.md`](../noemar-synlang/synlang-patterns.md) §6 for the call-out spectrum that makes the difference.

---

## Launching a Term Halo

| Step | Duration |
|---|---|
| 1. Define buybox (parameter ranges, counterparty requirements, asset types) | 1-2 weeks |
| 2. Legal framework (Halo Artifact, recourse) | 2-4 weeks (reuses templates) |
| 3. Smart contract deployment (PAU, Queue, Redeem, NFAT contracts) | Days (factory deployment) |
| 4. Configure beacons (`nfat-{halo}`, `attest-data-{class}`) | Days |
| 5. Governance approval (Halo Artifact Edit) | ~1 week |
| **Total** | **4-8 weeks** |

---

## Related

- [`halo-classes.md`](halo-classes.md) — Class / Book / Unit architecture; book lifecycle
- [`halo-portfolio.md`](halo-portfolio.md) — LCTS-based alternative
- [`halo-trading.md`](halo-trading.md) — AMM-based alternative
- [`prime.md`](prime.md) — Primes that allocate to Term Halos
- [`../smart-contracts/nfats.md`](../smart-contracts/nfats.md) — NFAT standard
- [`../smart-contracts/architecture-overview.md`](../smart-contracts/architecture-overview.md) — PAU pattern
- [`../sentinel/sentinel-network.md`](../sentinel/sentinel-network.md) — Operating-setup context (operate Primes that allocate to Term Halos)
- [`../risk-framework/halobook-layer.md`](../risk-framework/halobook-layer.md) — Halobook in the risk framework
- [`../risk-framework/asset-type-treatment.md`](../risk-framework/asset-type-treatment.md) — NFAT capital treatment
- [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) — Beacon class taxonomy (relay / attest-data-beacon / etc.)
