# Non-Fungible Allocation Token Standard (NFATS) — Business Requirements

**Status:** Draft
**Last Updated:** 2026-03-01

---

## Executive Summary

The Non-Fungible Allocation Token Standard defines a system for bespoke capital deployment deals between Primes and Halos. Unlike LCTS (which pools users into shared generations), NFATS treats each deal as an individual, non-fungible position represented by an NFAT (Non-Fungible Allocation Token).

Capital flows through **NFAT Facilities** — smart contracts that define a "buybox" of acceptable deal parameters. Primes queue sUSDS into a Facility. The Halo (via an LPHA beacon, e.g. `lpha-nfat`) claims from queues when deals are struck, minting an NFAT that represents a claim on the capital deployment. Each NFAT represents a **Halo Unit** (liability side) — a claim on a **Halo Book** (asset side). The book is the bankruptcy-remote boundary: units sharing a book are pari passu on losses (unless tranched), while units on different books are fully isolated.

Deal terms (APY, duration, maturity conditions) are tracked offchain in the **Synome**, while the onchain NFAT tracks only custody and ownership. Book contents are tracked in the Synome via attestations from an independent **Attestor** operating the `lpha-attest` beacon.

**Key principles:**
- **Onchain** = custody, ownership, facility parameters
- **Offchain (Synome)** = deal terms, yield schedules, maturity conditions, book contents (via attestor)
- **Halo Unit** (NFAT) = liability side — a claim on a Halo Book
- **Halo Book** = asset side — a balanced ledger (assets = liabilities) backing one or more units; bankruptcy-remote boundary

---

## Why NFATS Exists

NFATS solves a different problem than LCTS:

| Scenario | Best Fit |
|----------|----------|
| Many users, same terms, shared capacity | LCTS |
| Individual deals, bespoke terms, named counterparties | NFATS |

### When to Use NFATS

- Asset manager partnerships with negotiated terms
- Deals where each depositor has different yield, duration, or conditions
- Situations requiring transferable positions (secondary market, collateralization)
- Regulated contexts where counterparty identity matters

### When to Use LCTS

- Open participation with uniform terms
- Capacity-constrained strategies where fair distribution matters
- Scenarios where fungibility and pooling are desirable

---

## Halo Class Structure

An **NFAT Facility** is a **Halo Class** — containing both **Halo Units** (liability side — the NFATs) and **Halo Books** (asset side — the balanced ledgers backing those units). All share the same smart contract infrastructure and legal framework (buybox).

### What a Halo Class (NFAT Facility) Shares

| Component | Description |
|-----------|-------------|
| **PAU** | Controller + ALMProxy + RateLimits for the Facility |
| **LPHA Beacons** | `lpha-nfat` manages NFAT claims and redemptions; `lpha-attest` posts attestations |
| **Legal Buybox** | Acceptable parameter ranges, counterparty requirements, recourse mechanisms |
| **Queue + Redeem Contracts** | Shared infrastructure for capital flows |

### Halo Units (Liability Side)

Each NFAT is a **Halo Unit** — a claim on a Halo Book. Units represent the liability side of the Halo Class: what the Halo owes to NFAT holders.

| Parameter | Variation Within Buybox |
|-----------|------------------------|
| **Duration** | e.g., 6-12 months vs 12-24 months |
| **Size** | Different notional amounts per deal |
| **APY** | Within the facility's acceptable range |
| **Counterparty** | Different Primes for each NFAT |
| **Specific Terms** | Bespoke conditions within buybox constraints |

### Halo Books (Asset Side)

Each **Halo Book** is a bankruptcy-remote balanced ledger (assets = liabilities) that backs one or more Halo Units. Books represent the asset side of the Halo Class: what the Halo actually holds.

| Property | Description |
|----------|-------------|
| **Bankruptcy remoteness** | The book is the isolation boundary — units sharing a book share fate; units on different books are fully isolated |
| **Loss distribution** | Pari passu across all units on the same book (unless tranched) |
| **Privacy** | Multiple assets can be blended in a book, preventing outsiders from inferring individual loan terms from NFAT data |
| **Composition** | Whole assets per book — a single asset is not split across books |
| **Recursive** | A book can hold Halo Units from other books as assets, enabling structured layering |

### Unit-to-Book Mapping

The mapping between units and books is flexible:

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **1:1** | One unit, one book, one asset | Simple bilateral deal |
| **Many units : one book** | Multiple NFATs backed by the same blended collateral pool | Privacy protection — individual loan terms can't be inferred |
| **Recursive** | Assets in Book A are Halo Units from Book B | Structured products, tranching across books |

**Privacy example:** A book holds 5 different loans blended together. 10 NFATs are issued against the book. Each NFAT holder knows their own terms (APY, duration, size) but cannot determine the individual terms of the 5 underlying loans — only the blended risk characteristics as attested by the Attestor.

### Terms Source

NFAT terms can come from two sources:

| Mode | Description |
|------|-------------|
| **General buybox** | Halo Class defines acceptable ranges; individual units fall within the buybox without predetermined terms. Halo has flexibility in structuring. |
| **Ecosystem accord** | Pre-negotiated agreement specifying individual unit and book terms. Overrides the general buybox. More constrained, more predictable for the Prime. |

This structure enables scalable bespoke deals: one legal framework, one beacon-operated workflow, many individual positions with varying terms, and flexible asset-side composition with built-in privacy.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              HALO                                        │
│                                                                          │
│   Operates one or more NFAT Facilities (Halo Classes)                    │
│   Each Facility = separate smart contract with its own buybox            │
│                                                                          │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
            ┌────────────────────────┼────────────────────────┐
            ▼                        ▼                        ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│  NFAT Facility A    │  │  NFAT Facility B    │  │  NFAT Facility C    │
│  (Senior Secured)   │  │  (Mezzanine)        │  │  (Structured)       │
│                     │  │                     │  │                     │
│  Buybox params:     │  │  Buybox params:     │  │  Buybox params:     │
│  - 6-12mo term      │  │  - 12-24mo term     │  │  - Custom           │
│  - 8-12% APY        │  │  - 12-18% APY       │  │                     │
│                     │  │                     │  │                     │
│  Queue:             │  │  Queue:             │  │  Queue:             │
│  - Prime X: 50M     │  │  - Prime Y: 20M     │  │  - Prime X: 10M     │
│  - Prime Y: 30M     │  │                     │  │                     │
│                     │  │                     │  │                     │
│  Redeem Contract:   │  │  Redeem Contract:   │  │  Redeem Contract:   │
│  (Halo deposits     │  │  (funds awaiting    │  │  (funds awaiting    │
│   funds here)       │  │   claim)            │  │   claim)            │
└──────────┬──────────┘  └──────────┬──────────┘  └──────────┬──────────┘
           │                        │                        │
           ▼                        ▼                        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           MINTED NFATs                                   │
│                                                                          │
│   NFAT #1: 25M, Prime X, Facility A  →  Halo Unit → Book α              │
│   NFAT #2: 15M, Prime Y, Facility A  →  Halo Unit → Book α              │
│   NFAT #3: 20M, Prime Y, Facility B  →  Halo Unit → Book β              │
│                                                                          │
│   Units on same book (α) are pari passu on losses                        │
│   Units on different books (α vs β) are fully isolated                   │
│   Terms stored in Synome (APY, maturity, payment schedule, book)         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Redemption Flow (Bullet Loan):**
```
At Maturity:

  HALO                           FACILITY                         PRIME
    │                               │                               │
    │  1. Deposit funds into        │                               │
    │     redeem contract           │                               │
    │  ─────────────────────────►   │                               │
    │     (required, penalties      │                               │
    │      if late)                 │                               │
    │                               │                               │
    │                               │   2. Call redeem function,    │
    │                               │      specify NFAT             │
    │                               │   ◄─────────────────────────  │
    │                               │                               │
    │                               │   3. NFAT burned,             │
    │                               │      funds released           │
    │                               │   ─────────────────────────►  │
    │                               │                               │
```

---

## Components

### 1. NFAT Facility

Each NFAT Facility is a **PAU** (Controller + ALMProxy + RateLimits) with NFAT-specific extensions. The PAU holds custody of all capital flowing through that Facility; the NFAT extensions handle queue mechanics and token minting.

```
NFAT Facility = PAU + NFAT Extensions
├── Controller (rate limits on claims, redemptions)
├── ALMProxy (holds custody of sUSDS from all NFATs in this Facility)
├── RateLimits (standard rate limit infrastructure)
│
└── NFAT Extensions:
    ├── Queue contract (share-based, per-depositor)
    ├── NFAT minting (ERC-721)
    └── Redeem contract
```

**Facility parameters (buybox):**
- Asset type / strategy description
- Term range (e.g., 6-12 months)
- APY range (e.g., 8-12%)
- Risk tier / rating requirements
- Any other constraints the Halo commits to

**Onboarding (open question):**

> **Note:** The exact onboarding mechanism for Primes to Facilities is an open design question. The flow is: Prime synomic governance approves the Facility → Prime can deposit into queue → Halo can claim. The specific governance and Configurator integration path needs further specification.

**Key behaviors:**
- One PAU per Facility
- Each Facility has its own queue contract and redeem contract
- All capital from that Facility's NFATs flows through the Facility's ALMProxy

### 2. Facility Queue

The queue uses **share-based accounting** congruent with LCTS, but without generations (since claiming is selective, not batch).

**Queue State:**

| State | Description |
|-------|-------------|
| totalShares | Total shares outstanding across all depositors |
| totalUnderlying | Total sUSDS held in the queue |
| shares[address] | Per-depositor share balance (non-transferable) |

**Subscribe (deposit):**

```
If totalShares == 0:
    shares = amount (1:1)
Else:
    shares = amount × totalShares ÷ totalUnderlying

Update: totalShares, totalUnderlying, user shares
Transfer: sUSDS from depositor to queue
```

**Withdraw:**

```
underlyingOut = shares × totalUnderlying ÷ totalShares

Update: totalShares -= shares, totalUnderlying -= underlyingOut, user shares = 0
Transfer: sUSDS from queue to depositor
```

- Available anytime (no lock period — unlike LCTS, there's no batch settlement lock window)
- Complete withdrawal only (like LCTS "claim and exit")

**Claim (`lpha-nfat` beacon only):**

```
claim(address target, uint256 amount)

sharesToBurn = amount × totalShares ÷ totalUnderlying
Require: target has sufficient shares

Update: totalShares -= sharesToBurn, totalUnderlying -= amount, target shares -= sharesToBurn
Transfer: sUSDS from queue to Facility ALMProxy
Mint: NFAT to target
```

**Comparison with LCTS:**

| Aspect | LCTS | NFATS Queue |
|--------|------|-------------|
| Share calculation | amount × totalShares ÷ totalUnderlying | same |
| Shares transferable | No (internal accounting) | No (internal accounting) |
| Generations | Yes (generation-based batch settlement) | No (selective claiming) |
| Lock period | Yes (13:00 → 16:00 UTC daily) | No |
| Settlement | Batch, proportional to all | Selective: Halo picks (address, amount) |
| Output | Rewards accrue over time | NFAT minted at claim |

### 3. Deal NFAT (ERC-721)

Minted when Halo claims from a queue. Each NFAT is a **Halo Unit** (liability side) — a claim on a **Halo Book** (asset side). Bankruptcy remoteness is at the book level: units sharing a book are pari passu on losses; units on different books are fully isolated.

**Onchain data (minimal):**

| Field | Description |
|-------|-------------|
| `tokenId` | Unique identifier |
| `facility` | Reference to the NFAT Facility contract |
| `principal` | Original sUSDS amount claimed |
| `depositor` | Original Prime address |
| `mintedAt` | Timestamp when deal was struck |

**Offchain data (Synome):**
- Deal terms (APY, duration, special conditions)
- Payment schedule (bullet, amortizing, periodic interest)
- Maturity date and conditions
- Book assignment (which Halo Book backs this unit)
- Book contents (via attestor — risk characteristics, not individual borrower details)

**Transferability:**
- NFATs are transferable by default
- Halo can optionally restrict transfers to whitelisted addresses (for KYC/regulatory requirements)

### 4. Redeem Contract

Each Facility has a redeem contract where the Halo deposits funds to make them available for Prime redemption.

**Flow:**
1. Halo deposits principal + yield into redeem contract (required at maturity, penalties if late)
2. Prime calls redeem function, specifying which NFAT
3. NFAT is burned (or spent for partial redemptions)
4. Funds released to Prime

**Key behaviors:**
- Halo must fund before Prime can redeem
- Prime controls timing of actual redemption (can delay past maturity if desired)
- NFAT acts as a "claim ticket" — burning it releases the funds

### 5. Redemption and Rewards

Redemption is fundamentally a two-way exchange: the NFAT flows one direction, cash (principal + yield) flows the other. The typical flow:

1. **Halo funds the redeem contract** — required at maturity, penalties if late
2. **Prime burns NFAT to claim** — at their convenience, can delay past maturity

The NFAT acts as a **claim ticket**: Halo loads funds, Prime burns ticket to collect.

**Payment Patterns:**

| Pattern | Halo Action | Prime Action | NFAT State |
|---------|-------------|--------------|------------|
| **Bullet loan** | Deposit principal + yield at maturity | Burn NFAT to claim | Burned |
| **Amortizing loan** | Deposit each payment as due | Spend NFAT to claim each payment | Principal reduced each time |
| **Periodic interest** | Deposit interest payments periodically | Claim interest (NFAT unchanged) | Active until final redemption |

**For multi-payment loans:**
- NFAT is "spent" rather than burned — recorded principal is reduced
- Each payment: Halo deposits → Prime spends partial NFAT → receives that tranche
- Final payment: Prime burns remaining NFAT

**Extensible Payment Delivery**

The patterns above describe the core mechanisms, but payment delivery should be extensible to support additional flows — including direct transfers from the Halo's PAU to the Prime's PAU where the Prime takes no action and simply receives funds. The exact mechanics of extended payment flows are intentionally left undefined for now; the standard should accommodate them without requiring changes to the core NFAT structure.

---

## Halo Books and the Attestor

### Book Lifecycle

Books progress through a defined set of phases. Each phase transition requires action from specific beacons.

```
┌──────────┐    NFATs swept in     ┌──────────┐
│ CREATED  │ ─────────────────────▶│ FILLING  │
│ (empty)  │                       │ (USDS)   │◄─── can keep adding NFATs
└──────────┘                       └────┬─────┘
                                        │
                           lpha-attest posts attestation
                           THEN lpha-nfat changes status
                                        │
                                        ▼
                                  ┌───────────┐
                                  │ DEPLOYING │  Schrödinger's risk
                                  │(obfuscated)│  High CRR
                                  └─────┬─────┘
                                        │
                           lpha-attest posts "at rest" attestation
                                        │
                                        ▼
                                  ┌──────────┐
                                  │ AT REST  │  Confirmed characteristics
                                  │(deployed) │  Medium CRR
                                  └─────┬─────┘
                                        │
                           Ongoing re-attestation
                           (cadence per asset type, affects CRR)
                                        │
                           Assets mature / return
                                        │
                                        ▼
                                  ┌──────────┐
                                  │ UNWINDING│  Halo funds Redeem Contract
                                  └─────┬─────┘
                                        │
                           NFAT holders burn to claim
                                        │
                                        ▼
                                  ┌──────────┐
                                  │  CLOSED  │
                                  └──────────┘
```

**Phase: Created** — Book exists but is empty. No assets, no units.

**Phase: Filling** — NFAT subscriptions are swept into the book. Each sweep mints an NFAT (Halo Unit) and adds the capital to the book's asset side. During this phase, the book holds USDS earning agent rate — fully transparent and trackable in the Synome. Additional NFATs can be added as subscriptions come in.

**Phase: Deploying (obfuscated)** — Assets are offboarded (USDS → USDC → deployed to borrowers). The Synome does not receive precise real-time updates about which specific assets have been deployed, to whom, or when. This is intentional: blending multiple deployments in a book prevents outsiders from inferring individual loan terms. From the Synome's perspective, the assets are in a "Schrödinger's risk" state — they could be anywhere from still cash to fully deployed. The deployment phase has a **higher CRR** to compensate for this uncertainty.

**Phase: At Rest** — Fully deployed. The attestor has confirmed the risk characteristics of the deployed assets. The Synome knows the risk profile (credit quality, duration, asset type) but not individual borrower identities or specific deal terms. CRR is lower than during deployment but still reflects the risk characteristics of the deployed assets.

**Phase: Unwinding** — Assets return to the book. Halo funds the Redeem Contract from book proceeds. NFAT holders burn to claim.

**Phase: Closed** — All units redeemed, book wound down.

### The Attestor and `lpha-attest`

The **Attestor** is a company whitelisted by Sky governance to provide risk attestations about book contents. It operates the `lpha-attest` beacon.

| Property | Description |
|----------|-------------|
| **Type** | LPHA (Low Power, High Authority) — deterministic, rule-based |
| **Operator** | Attestor company (whitelisted by Sky governance) |
| **Capability** | Write attestations into Synome |
| **Cannot** | Move capital, mint NFATs, change book status directly |
| **Accountability** | Subject to its own govops supply chain of checks and audits |

**Two-beacon deployment gate:** Neither `lpha-attest` nor `lpha-nfat` can trigger deployment alone. The attestor must first post an attestation into the Synome via `lpha-attest`; only then can `lpha-nfat` change the book's status. This separation of concerns ensures independent validation.

```
ATTESTOR                          SYNOME                          HALO
(lpha-attest)                                                   (lpha-nfat)
    │                                │                               │
    │  1. Upload attestation         │                               │
    │  "Book X: assets will           │                               │
    │   deploy into [characteristics]│                               │
    │   over [timeframe], legal      │                               │
    │   rails confirmed"             │                               │
    │  ─────────────────────────────▶│                               │
    │                                │                               │
    │                                │  2. Attestation present ✓     │
    │                                │     lpha-nfat can now         │
    │                                │     change book status        │
    │                                │  ────────────────────────────▶│
    │                                │                               │
    │                                │  3. Book → deploying          │
    │                                │  ◀────────────────────────────│
    │                                │                               │
```

**Attestation types:**

| Timing | Attestation Content |
|--------|---------------------|
| **Pre-deployment** | "Over the next [timeframe], assets will deploy into assets with [risk characteristics]. Legal rails analyzed and confirmed." |
| **Post-deployment** | "Assets are now deployed and at rest with [confirmed risk characteristics]." |
| **Ongoing (at rest)** | Periodic re-attestation per asset type. Cadence varies by asset and directly affects CRR — more frequent attestation enables lower CRR. |

### CRR Incentive Structure

The risk model creates economic incentives that balance privacy against transparency without mandating specific behavior:

| Book Phase | CRR Impact | Incentive Created |
|---|---|---|
| **Filling** (USDS) | Low CRR | Known asset, no ambiguity |
| **Deploying** (obfuscated) | High CRR | Minimize deployment duration; stagger deployments across books |
| **At Rest** (attested) | Medium CRR | Maintain attestation cadence; encourage frequent re-attestation |
| **Missed re-attestation** | CRR increases | Prompt re-attestation to restore lower capital charge |

> **CRR calibration ownership:** The qualitative incentive structure above (Low/High/Medium) is defined here. Numeric CRR values for each book-phase are owned by the risk-framework (`risk-framework/capital-formula.md`) and will be published there when calibration is complete.

Primes and Halos are economically incentivized to keep the obfuscated deployment phase as short as possible (reducing CRR cost) while still delivering adequate borrower privacy.

---

## Deal Lifecycle

**1. Onboarding**
- Prime synomic governance approves deployment into NFAT Facility
- Govops onboards Facility via configurator (rate limits) or timelock (BEAMstate)

**2. Queue**
- Prime deposits sUSDS into their queue within the Facility
- Queue balance increases; Prime can withdraw anytime before claim

**3. Book creation**
- Halo creates a new book (or uses an existing book in filling phase)

**4. Claim (deal struck)**
- Halo (via `lpha-nfat`) claims from Prime's queue (specifying amount)
- sUSDS transferred to book (via Facility ALMProxy)
- NFAT minted to Prime (Halo Unit — claim on the book)
- Deal terms recorded in Synome (APY, term, maturity date, book assignment)
- Queue balance reduced by claimed amount
- Additional NFATs may be swept into the same book over time

**5. Attestation and deployment**
- Attestor uploads pre-deployment attestation via `lpha-attest` (risk characteristics, timeframe, legal confirmation)
- `lpha-nfat` transitions book to deploying status
- Capital offboarded (USDS → USDC → deployed to borrowers)
- Deployment is obfuscated — Synome does not track individual deployments in real time
- Higher CRR applies during this phase

**6. At rest**
- Attestor uploads post-deployment attestation confirming deployed asset characteristics
- Book transitions to at-rest status; CRR adjusts downward
- Ongoing re-attestation at asset-type-specific cadence

**7. Lifecycle**
- For bullet loans: nothing happens until maturity
- For other structures: Halo deposits payments per Synome schedule, Prime claims as available
- Halo must maintain liquidity in the book to fund maturing units
- NFAT holder can transfer/sell position at any time (subject to whitelist if enabled)

**8. Maturity**
- Halo deposits principal + yield into Facility redeem contract (required, penalties if late)
- Prime burns NFAT to claim funds (at their convenience)
- Deal closed; if all units on a book are redeemed, book closes

---

## Behaviors

### Facility Queue Behaviors

**Prime actions:**
- **Deposit**: Prime adds sUSDS to their queue in a Facility
- **Withdraw**: Prime removes sUSDS from their queue (only possible before Halo claims)
- **View balance**: Anyone can check the queued balance for any Prime in any Facility

### NFAT Behaviors

**Halo actions (via `lpha-nfat`):**
- **Claim**: Take sUSDS from a Prime's queue and mint an NFAT
  - Specifies: which Prime, how much to claim
  - Results in: sUSDS moves to Halo, new NFAT minted, Synome records deal terms
- **Fund redeem**: Deposit funds into Facility redeem contract
  - Specifies: which NFAT, amount (principal + yield)
  - Results in: funds available for Prime to claim
  - Required at maturity, penalties if late

**Prime/Holder actions:**
- **Redeem (burn)**: Burn NFAT to claim funds from redeem contract
  - Specifies: which NFAT
  - Results in: NFAT burned, funds transferred to holder
  - Only works if Halo has funded the redemption
- **Redeem (spend)**: Spend partial NFAT to claim a payment (for multi-payment loans)
  - Specifies: which NFAT, payment amount
  - Results in: NFAT principal reduced, funds transferred to holder
- **Transfer**: Transfer NFAT to another address (standard ERC-721)
  - New holder inherits all rights (future payments, redemption)

**View functions:**
- Get queue balance for a Prime in a Facility
- Get principal amount for an NFAT
- Get original depositor for an NFAT
- Get mint timestamp for an NFAT
- Get Facility reference for an NFAT
- Get funded amount available for redemption

### Optional: Transfer Restrictions

- Halo can enable a whitelist mode where only approved addresses can receive NFAT transfers
- Halo can add/remove addresses from the whitelist
- When whitelist is active, transfers to non-whitelisted addresses are blocked

---

## Scenarios

### Scenario 1: Basic Bullet Loan (Happy Path)

**Setup:** Prime X wants to deploy into Halo 123's senior secured Facility.

1. **Onboarding**
   - Prime X synomic governance approves NFAT Facility 123
   - Govops sets rate limit of 100M for Prime X in Facility 123

2. **Queue**
   - Prime X deposits 50M sUSDS into Facility 123 queue
   - Queue balance: 50M

3. **Claim**
   - Halo 123 `lpha-nfat` claims 25M from Prime X's queue
   - NFAT #1 minted to Prime X (25M principal)
   - Synome records: 6-month term, 10% APY, maturity 2025-07-15
   - Queue balance: 25M remaining

4. **Lifecycle**
   - Nothing happens (bullet loan)
   - Prime X could transfer NFAT #1 if desired

5. **Maturity (2025-07-15)**
   - Halo 123 deposits 26.25M sUSDS into Facility 123 redeem contract (25M principal + 1.25M yield)
   - Prime X burns NFAT #1
   - Prime X receives 26.25M sUSDS

**Result:** Prime X deployed 25M for 6 months, received 10% APY.

---

### Scenario 2: Partial Queue Claim

**Setup:** Prime X has 50M queued, Halo only wants 30M.

1. Prime X deposits 50M into Facility queue
2. Halo claims 30M → NFAT #1 minted (30M principal)
3. Prime X still has 20M in queue
4. Later, Halo claims another 15M → NFAT #2 minted (15M principal)
5. Prime X withdraws remaining 5M from queue

**Result:** Prime X holds two separate NFATs from same Facility, each representing a claim on a distinct Halo Unit.

---

### Scenario 3: Prime Withdraws Before Claim

**Setup:** Prime X queues funds but changes their mind.

1. Prime X deposits 50M into Facility 123 queue
2. Market conditions change; Prime X wants capital elsewhere
3. Prime X withdraws 50M from queue (Halo hasn't claimed yet)
4. Queue balance: 0

**Result:** No deal struck, Prime X retains full capital. Queue is non-binding until claimed.

---

### Scenario 4: Amortizing Loan (Multi-Payment)

**Setup:** NFAT with quarterly principal + interest payments over 12 months.

1. **Claim**
   - Halo claims 40M from Prime X queue
   - NFAT #1 minted (40M principal)
   - Synome records: 4 quarterly payments of 10M principal + interest

2. **Q1 Payment**
   - Halo deposits 10.8M (10M principal + 0.8M interest)
   - Prime X spends NFAT #1 to claim payment
   - NFAT #1 principal reduced to 30M

3. **Q2, Q3 Payments**
   - Same pattern; NFAT principal reduces to 20M, then 10M

4. **Q4 Final Payment**
   - Halo deposits 10.8M
   - Prime X burns NFAT #1 (final redemption)
   - NFAT #1 destroyed

**Result:** Amortizing structure with NFAT "spent" over time rather than burned at once.

---

### Scenario 5: NFAT Transfer (Secondary Market)

**Setup:** Prime X holds an NFAT but wants liquidity before maturity.

1. Prime X holds NFAT #1 (25M principal, 4 months remaining, 10% APY)
2. Prime Y offers to buy NFAT #1 for 25.5M (slight premium)
3. Prime X transfers NFAT #1 to Prime Y (standard ERC-721 transfer)
4. At maturity, Halo funds redemption
5. Prime Y burns NFAT #1 and receives 26.25M

**Result:** Prime X exits early with small profit; Prime Y earns yield for remaining term.

---

### Scenario 6: Halo Late on Funding (Penalty)

**Setup:** Halo doesn't fund redemption by maturity date.

1. NFAT #1 matures on 2025-07-15
2. Halo fails to deposit funds by maturity
3. Penalty mechanism triggers (defined in Synome/Facility terms)
4. Halo deposits funds on 2025-07-20 (5 days late) + penalty amount
5. Prime X burns NFAT and receives principal + yield + penalty

**Result:** Halo penalized for late funding; Prime made whole plus compensation.

---

### Scenario 7: Prime Delays Redemption

**Setup:** Halo funds on time, but Prime doesn't claim immediately.

1. NFAT #1 matures on 2025-07-15
2. Halo deposits 26.25M into redeem contract on 2025-07-14
3. Prime X is busy / wants to batch claims / doesn't need funds yet
4. Prime X burns NFAT #1 on 2025-08-01

**Result:** No penalty to Prime for delayed claim. Funds sit in redeem contract until claimed.

---

### Scenario 8: Multiple Primes, Same Facility

**Setup:** Two Primes deploy into the same Facility.

1. Prime X deposits 50M into Facility 123 queue
2. Prime Y deposits 30M into Facility 123 queue
3. Halo claims 25M from Prime X → NFAT #1
4. Halo claims 30M from Prime Y → NFAT #2
5. Halo claims another 25M from Prime X → NFAT #3

**Result:** Three distinct NFATs, each representing a claim on a separate Halo Unit, all from same Facility.

---

### Scenario 9: Prime Deploys Across Multiple Facilities

**Setup:** Prime X wants exposure to different risk profiles.

1. Prime X onboards to Facility A (senior secured, 8% APY) and Facility B (mezz, 14% APY)
2. Prime X deposits 30M into Facility A queue
3. Prime X deposits 10M into Facility B queue
4. Halo claims from both queues
5. Prime X holds NFAT from Facility A (lower risk) and NFAT from Facility B (higher risk)

**Result:** Prime X has diversified exposure across multiple Facilities/strategies.

---

### Scenario 10: Transfer Restriction (Whitelist)

**Setup:** Facility has KYC requirements; transfers restricted to approved addresses.

1. Facility 123 has whitelist enabled
2. Prime X (whitelisted) receives NFAT #1
3. Prime X tries to transfer to Random Address → blocked
4. Prime X requests Prime Y be added to whitelist
5. Halo adds Prime Y to whitelist
6. Prime X transfers NFAT #1 to Prime Y → succeeds

**Result:** Transfers only between KYC'd/approved parties.

---

### Scenario 11: Halo Never Funds Redemption (Default)

**Setup:** Halo fails to fund and doesn't respond.

1. NFAT #1 matures on 2025-07-15
2. Halo doesn't fund redemption
3. Grace period passes, penalties accumulate
4. Halo still doesn't fund
5. Default procedures trigger (defined in Facility/Synome terms)
6. Recovery process initiated (collateral liquidation, insurance, etc.)

**Result:** Default handling per agreed terms. NFAT holder has claim on recovery proceeds.

---

### Scenario 12: Queue While Holding Existing NFAT

**Setup:** Prime wants to deploy more while already holding an NFAT.

1. Prime X holds NFAT #1 (25M) from previous claim
2. Prime X deposits another 20M into same Facility queue
3. Halo claims 20M → NFAT #2 minted
4. Prime X now holds NFAT #1 and NFAT #2 (claims on separate Halo Units)

**Result:** No limit on concurrent positions; each NFAT is independent.

---

## NFATS vs LCTS Comparison

| Aspect | LCTS | NFATS |
|--------|------|------|
| **Model** | Pool / ETF | Individual deals |
| **Position type** | Fungible shares | Non-fungible NFAT |
| **Terms** | Same for all in generation | Bespoke per deal |
| **Queue** | Shared across generation | Individual per depositor |
| **Capacity allocation** | Proportional distribution | Per-deal (Halo decides) |
| **Settlement** | Batch (daily cycle) | Per-deal (anytime) |
| **Transferability** | Non-transferable shares | Transferable NFAT (optionally restricted) |
| **Exit before settlement** | Withdraw from active generation | Withdraw from queue before claim |
| **Redemption initiation** | Holder-initiated only | Either party (request/fulfill or direct) |
| **Reward mechanism** | rewardPerToken accumulator | Flexible (offchain-driven) |
| **Onchain complexity** | Higher (generations, settlement) | Lower (queue + NFAT) |
| **Offchain complexity** | Lower (uniform terms) | Higher (per-deal tracking) |

---

## NFATS as RiverUSDS Superset

NFATS is designed to cover all RiverUSDS (ERC-7540 async vault) use cases when deposits are pre-agreed and tokens have transfer restrictions:

| RiverUSDS Feature | NFATS Equivalent |
|-------------------|------------------|
| `maxDeposit` whitelist (pre-agreed caps) | Individual queue + Halo claim |
| Transfer restrictions | Optional whitelist mode |
| `requestRedeem` → `fulfillRequest` → `withdraw` | `requestRedeem` → `fulfillRedeem` (Pattern B) |
| Periodic rewards (`grantRewards` → `getReward`) | Pattern C: Periodic Rewards |
| Async rewards (`requestReward` → fulfill → claim) | Pattern D: Claimable Rewards |
| Fungible shares (same terms) | Each deal is an NFAT (explicit non-fungibility) |

**Key insight**: Redemption is a two-way exchange — NFAT in one direction, cash out the other. Either party can initiate by putting their side in first. This matches ERC-7540's request/fulfill pattern while also supporting Halo-initiated redemptions.

When all depositors have identical terms and transfer restrictions, NFATS effectively behaves like a restricted ERC-7540 vault — but with the flexibility to support bespoke terms per position when needed.

---

## Integration Notes

### Halo LPHA Beacon (`lpha-nfat`)

TBD — `lpha-nfat` beacon integration for automated claims, reward distribution, and redemptions.

### ALM Controller Compatibility

NFATS requires custom ALM controller integration (similar to LCTS). The Halo's ALMProxy holds claimed sUSDS and sources redemption/reward payments.

### Halo Artifact

Deal terms should be recorded in the Halo Artifact for transparency and auditability. The NFAT's `tokenId` serves as the key linking onchain position to offchain terms.

---

## Design Rationale

### Why Individual Queues?

Shared queues (like LCTS generations) make sense when all participants receive identical treatment. For bespoke deals, individual queues:
- Allow depositors to signal interest without commitment
- Let the Halo selectively accept deals
- Avoid complexity of proportional distribution
- Enable partial claims (multiple deals with same depositor)

### Why NFATs?

ERC-20 tokens imply fungibility — any token is interchangeable with any other. When deals have different terms, forcing them into a fungible token creates friction:
- Transfer restrictions feel like hacks
- Per-holder accounting becomes complex
- The token doesn't represent what it claims to

NFATs make the non-fungibility explicit:
- Each position is clearly unique
- Transfers are natural (new holder inherits the deal)
- Secondary markets can price deals individually
- No pretense of fungibility

### Why Offchain Terms?

Putting all deal terms onchain would:
- Increase gas costs significantly
- Reduce flexibility for complex arrangements
- Require contract upgrades for new term types

Offchain terms with onchain custody provides:
- Maximum flexibility for bespoke arrangements
- Simple, auditable onchain contracts
- Easy extension to new deal structures

---

## Wrapped NFATs (Fractionalization)

An NFAT can optionally be wrapped in a fungible ERC-20 token, allowing the deal position to be split up and sold in pieces.

### How It Works

- The NFAT holder deposits their NFAT into a wrapper contract
- The wrapper mints fungible tokens representing fractional ownership of that specific NFAT
- Fractional token holders can trade their shares freely
- When the NFAT receives rewards or is redeemed, proceeds are distributed proportionally to fractional holders

### Use Cases

- **Liquidity**: NFAT holder wants partial liquidity without selling the entire position
- **Syndication**: Multiple parties want exposure to a single deal
- **Smaller denominations**: Large deals can be broken into accessible pieces
- **Secondary markets**: Fungible tokens are easier to trade on existing DEX infrastructure

### Key Characteristics

- Each wrapped NFAT has its own separate fungible token (not pooled across deals)
- The wrapper contract becomes the NFAT holder and receives all rewards/redemptions
- Fractional holders claim their proportional share from the wrapper
- Wrapping is optional — NFATs work fine without it

### Relationship to NFATS

| Aspect | Unwrapped NFAT | Wrapped NFAT |
|--------|----------------|--------------|
| **Ownership** | Single holder | Multiple fractional holders |
| **Transferability** | Whole position only | Fractional shares tradeable |
| **Rewards** | Direct to holder | Via wrapper to fractional holders |
| **Complexity** | Simple | Additional wrapper contract |

### Implementation Notes

- Wrapper is a separate contract, not part of core NFATS
- Can be deployed per-NFAT or as a factory pattern
- Reward claiming and redemption flows need to account for wrapper as intermediary
- Transfer restrictions on the underlying NFAT (if any) apply to the wrapper depositing/withdrawing

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| `term-halo.md` | Business overview of Term Halos using NFATS |
| `lcts.md` | Alternative token standard for pooled, fungible positions |
| `sentinel-network.md` | `lpha-nfat` beacon context (LPHA) and relationship to sentinels |
| `portfolio-halo.md` | Portfolio Halo (LCTS-based alternative) |
| `beacon-framework.md` | `lpha-nfat` and `lpha-attest` as LPHA beacons |

---

*Document Version: 0.3*
