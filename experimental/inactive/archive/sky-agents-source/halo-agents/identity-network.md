# Identity Network

**Status:** Draft
**Pillar:** 7
**Last Updated:** 2026-01-27

---

## Executive Summary

An Identity Network is a special type of Halo that operates KYC/identity verification services. Instead of deploying capital into investment strategies, an Identity Network maintains an **on-chain registry** of addresses that have been verified to meet certain criteria (accredited investor, non-US person, qualified purchaser, etc.).

Identity Networks enable permissioned tokens within Sky Ecosystem. When a Halo Unit or Prime token issuer wants to restrict who can hold their token, they configure accepted Identity Networks — only addresses with valid attestations from those networks can receive the token.

**Key properties:**
- Multiple competing Identity Networks can coexist
- On-chain registry for simple address verification
- Legal entity performs actual KYC (documents stored off-chain)
- Restricted Halo type — identity business only, no capital deployment

---

## Why Identity Networks Exist

### The Problem

Sky Ecosystem enables creation of Halo Units that wrap diverse assets — from DeFi positions to private credit to tokenized real-world assets. For many of these products:

- **Issuers prefer known counterparties** — Asset managers and originators often want to know who holds their products
- **Participants prefer verified peers** — Institutional investors typically only transact with other verified institutions
- **Compliance teams require documentation** — Many organizations have internal policies requiring counterparty verification
- **Some jurisdictions have restrictions** — Certain products may have geographic or qualification requirements

Without identity verification, Sky cannot serve participants who require or prefer permissioned markets.

### The Solution

Identity Networks provide **attestations** about addresses:
- "This address belongs to a verified accredited investor"
- "This address belongs to a qualified institutional buyer"
- "This address belongs to a professional client"

Token contracts check these attestations on every transfer. The verification logic is simple: if the recipient has a valid attestation from an accepted Identity Network, the transfer proceeds. This happens at the token level, so any exchange or protocol using these tokens automatically inherits the restrictions.

### Why a Halo Type?

Identity Networks are structured as Halos because:
1. **Governance integration** — Subject to Sky oversight and standards
2. **Economic alignment** — Network operators earn fees, have skin in the game
3. **Composability** — Other Halos and Primes can query attestation status
4. **Accountability** — Slashing and penalty mechanisms apply

---

## Identity Network as a Halo Type

### Restrictions vs Regular Halos

Identity Networks are a **restricted Halo type** with significant limitations compared to standard Halos:

| Aspect | Regular Halo | Identity Network |
|--------|--------------|------------------|
| **Primary activity** | Deploy capital, generate yield | Operate identity registry |
| **Revenue source** | Investment returns | Membership/verification fees |
| **Capital deployment** | Yes (that's the point) | No (prohibited) |
| **Asset custody** | Holds assets via PAU | Minimal (operating capital only) |
| **Risk capital** | Required per Risk Framework | Minimal (operational risk only) |
| **Oversight** | Standard Halo governance | Elevated — compliance-critical |

### Permitted Activities

An Identity Network Halo may:
- Operate an on-chain attestation registry
- Control a legal entity that performs KYC verification
- Charge membership fees and verification fees
- Hold operating capital (not investment capital)
- Issue a governance token for network decisions
- Participate in cross-recognition agreements with other Identity Networks

An Identity Network Halo may NOT:
- Deploy capital into investment strategies
- Accept deposits beyond operating needs
- Issue yield-bearing tokens
- Operate as a Prime or standard Halo

### Economic Model

Identity Networks generate revenue from:

| Fee Type | Description |
|----------|-------------|
| **Membership fee** | Annual/monthly fee for maintaining attestation |
| **Verification fee** | One-time fee for initial KYC processing |
| **Revalidation fee** | Fee for periodic re-verification (e.g., annual) |
| **API access fee** | Fees for high-volume attestation queries |
| **Cross-recognition fee** | Fees from partner networks for mutual recognition |

Fees are set by the Identity Network's governance. Competition between networks creates pressure for reasonable pricing.

---

## On-Chain Registry

### Simple Address List

The on-chain component is intentionally minimal — just a list of addresses managed by lpha-identity:

```
Identity Registry Contract:
  - Storage: set of member addresses
  - Query: isMember(address) → true/false
  - Modify: add(address), remove(address), addBatch([addresses]), removeBatch([addresses])
  - Access: only lpha-identity can modify
```

That's it. A simple address set. No status enums, no metadata, no expiry dates on-chain.

### How It's Used

Restrictions are enforced **at the token level**. The Halo Unit issuer configures which Identity Networks are accepted, and the token contract checks membership on every transfer:

```
Halo Unit transfer check (on every transfer):
  IF restricted transfers enabled:
    FOR each accepted Identity Network:
      IF network.isMember(recipient) → allow transfer
    IF no network accepted recipient → reject transfer
```

This is a first-order restriction. Trading restrictions on exchanges are a second-order effect — if you can't receive the token, exchange settlement will naturally fail.

### Who Sets Accepted Networks?

The **Halo Unit issuer** configures accepted Identity Networks when deploying or updating the token. This is baked into the token contract, not the exchange.

Exchange Halos don't need separate identity checks — they inherit restrictions from the underlying tokens. If a token requires Identity Network membership, exchange settlement will fail for non-members because the token transfer itself fails.

### Beyond Halo Units: Prime Tokens

Identity Networks aren't just for Halo Units. **Institutional Primes** also use Identity Networks to restrict holders of their Prime tokens.

Example: An institutional Prime serving only qualified institutional buyers might require all SPK token holders to be members of an Institutional Identity Network. This ensures the Prime's token holder base meets the Prime's compliance requirements.

### Multiple Addresses Per Entity

When registering for KYC, users can choose to add **one or more addresses** to their attestation. This is managed by the Identity Network and its legal entity:

- User completes KYC once
- User provides list of addresses they control
- All addresses are added to the on-chain registry
- User can request additional addresses later (may require verification)
- If attestation expires or is revoked, ALL linked addresses are removed

This allows institutions with multiple wallets, or individuals using different addresses for different purposes, to maintain a single KYC relationship.

### Heavy Lifting in Synome

All the complexity lives off-chain in the Synome:

| Data | Location | Purpose |
|------|----------|---------|
| **Address list** | On-chain | Simple membership check |
| **Attestation details** | Synome | Type, issue date, expiry, verification level |
| **Linked addresses** | Synome | All addresses belonging to same verified entity |
| **Jurisdiction info** | Synome | Primary jurisdiction of verified entity |
| **KYC documents** | Legal entity (off-chain) | Actual verification records |
| **Personal identity** | Legal entity (off-chain) | Never stored in Synome |

lpha-identity handles the translation: it monitors Synome for attestation changes, expiries, and revocations, then updates the simple on-chain list accordingly.

### Why This Design?

| Concern | Solution |
|---------|----------|
| **Gas efficiency** | Simple boolean check is cheap |
| **Flexibility** | Complex logic can change in Synome without contract upgrades |
| **Privacy** | On-chain only reveals membership, not why or how |
| **Simplicity** | Other contracts just call `isMember()` — no complex integration |

---

## Multiple Networks Model

### Competition and Specialization

Multiple Identity Networks can operate simultaneously, each specializing in different:

**Jurisdictions:**
- US Identity Network (accredited investors, QIBs)
- EU Identity Network (MiFID II professional clients)
- APAC Identity Network (regional qualifications)

**Investor Types:**
- Accredited Investor Network (income/net worth thresholds)
- Institutional Network (banks, funds, registered advisors)
- Qualified Purchaser Network (higher thresholds for private funds)

**Verification Standards:**
- FATF-compliant Network (AML/KYC to FATF standards)
- Enhanced Due Diligence Network (higher verification thresholds)
- Regional Networks (jurisdiction-specific requirements)

### Token Configuration

The **Halo Unit issuer** (or Prime token issuer) configures accepted Identity Networks at deployment:

```
Token Configuration (set by issuer):
  - Accepted Networks: list of Identity Networks whose members can receive the token
  - If empty: unrestricted, anyone can hold/receive
```

**Examples:**

| Token | Accepted Networks | Rationale |
|-------|-------------------|-----------|
| USDS | None (unrestricted) | Open to all |
| SKY | None (unrestricted) | Open to all |
| JAAA-Halo Unit | US Accredited, Non-US QIB | Issuer requires verified holders |
| Private-Credit-Halo Unit | Institutional only | Institutional-only product |
| Institutional-Prime Token | Institutional only | Prime restricts token holder base |

---

## Legal Entity Operations

### Structure

Each Identity Network controls a legal entity that performs actual KYC:

```
┌─────────────────────────────────────────────────────────┐
│                  Identity Network Halo                   │
│                   (On-chain governance)                  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │              Identity Registry                      │ │
│  │         (On-chain: simple address list)             │ │
│  └────────────────────────────────────────────────────┘ │
│                          │                               │
│                    controls                              │
│                          ▼                               │
│  ┌────────────────────────────────────────────────────┐ │
│  │              Legal Entity                           │ │
│  │  (Foundation, LLC, or regulated entity)             │ │
│  │                                                     │ │
│  │  - Receives KYC applications                        │ │
│  │  - Verifies documents                               │ │
│  │  - Stores records (off-chain)                       │ │
│  │  - Updates Synome → lpha-identity syncs to chain     │ │
│  │  - Handles disputes, appeals, revocations           │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### KYC Processing Flow

```
1. APPLY
   User submits application + documents to legal entity

2. VERIFY
   Legal entity reviews documents
   - Identity verification (passport, ID)
   - Qualification verification (income, net worth, professional status)
   - Sanctions/AML screening

3. DECISION
   Legal entity approves or denies
   → If approved: attestation recorded in Synome with expiry date
                  lpha-identity adds address to on-chain list
   → If denied: application rejected, not added

4. MAINTAIN
   Periodic revalidation (e.g., annually)
   → User re-submits required documents
   → Synome attestation extended, address remains on list

5. EXPIRE / REVOKE
   → Expiry: lpha-identity removes address when expiry date passes
   → Revocation: legal entity revokes in Synome, lpha-identity removes address
```

### Regulatory Compliance

The legal entity must comply with:
- **AML/KYC regulations** in its jurisdiction
- **Data protection** (GDPR, CCPA, etc.)
- **Record retention** requirements
- **Sanctions screening** (OFAC, EU, UN lists)

The Identity Network Halo provides the governance framework; the legal entity handles regulatory compliance.

### Revocation Procedures

Attestations can be revoked for:
- **Fraud** — Falsified documents or misrepresentation
- **Change in status** — No longer meets qualification criteria
- **Sanctions listing** — Added to sanctions list
- **Request** — User requests removal
- **Legal order** — Court order or regulatory action

Revocation is immediate — legal entity marks revoked in Synome, lpha-identity removes address from on-chain list.

---

## Beacon Integration (lpha-identity)

### Overview

**lpha-identity** is the LPHA beacon that manages an Identity Network's on-chain address list.

**Level:** Per Identity Network
**Operator:** Identity Network GovOps / Legal Entity Operations

### Role

lpha-identity is the bridge between off-chain verification and on-chain membership:

```
Legal Entity → Synome → lpha-identity → On-chain Registry
   (KYC)      (state)    (executor)      (simple list)
```

1. Legal entity performs KYC, updates attestation in Synome
2. lpha-identity monitors Synome for changes
3. When attestation becomes active → lpha-identity calls `add(address)`
4. When attestation expires/revoked → lpha-identity calls `remove(address)`

### Responsibilities

| Function | Description |
|----------|-------------|
| **Add members** | When Synome shows new valid attestation, add to on-chain list |
| **Remove members** | When Synome shows expiry/revocation, remove from on-chain list |
| **Expiry monitoring** | Watch Synome for upcoming expiries, remove when they hit |
| **Batch updates** | Process multiple adds/removes efficiently |

### Security Model

- **Sole writer** — Only lpha-identity can modify the on-chain registry
- **Synome as source of truth** — lpha-identity only acts on Synome state
- **Audit trail** — All changes logged in Synome with timestamps
- **Rate limits** — Maximum updates per period (prevents spam/abuse)

---

## Connection to Sky Intents

Identity Networks enable restricted tokens to trade on Sky Intents (see `sky-intents.md`).

### How It Works

Restrictions are enforced at the **token level**, not the exchange level:

1. **Token Transfer Check**
   - When exchange settlement executes, the token contract checks if recipient is in an accepted Identity Network
   - If recipient is not a member → token transfer reverts → entire settlement fails
   - Exchange doesn't need separate identity logic — it inherits from token

2. **Order Visibility (Optional)**
   - Exchange Halo may hide orders from non-eligible counterparties
   - Reduces noise, improves UX for restricted tokens
   - This is a UX optimization, not a security check

3. **Attestation Events**
   - lpha-identity emits events when addresses are added/removed
   - lpha-exchange can subscribe to cancel orders from removed addresses proactively

### Settlement Flow

```
Exchange Settlement:
  1. lpha-exchange submits settlement batch
  2. Settlement contract calls token.transfer(seller → buyer)
  3. Token contract checks: buyer in accepted Identity Network?
     - JAAA-Halo checks US-Accredited.isMember(buyer) → true ✓
  4. Transfer succeeds → settlement proceeds

If buyer NOT in any accepted network:
  3. Token contract checks: buyer in accepted Identity Network?
     - JAAA-Halo checks US-Accredited.isMember(buyer) → false
     - JAAA-Halo checks Non-US-QIB.isMember(buyer) → false
  4. Transfer reverts → entire settlement fails
```

The exchange never explicitly checks identity — it just attempts the trade, and the token enforces restrictions.

---

## Governance and Oversight

### Identity Network Governance

Each Identity Network has its own governance:
- **Token-based voting** (if network issues token)
- **Fee setting** — Membership and verification fees
- **Policy updates** — Verification standards, accepted documents
- **Operator appointments** — Legal entity board, lpha-identity operators

### Sky Core Oversight

Identity Networks operate under elevated Sky Core oversight:

| Oversight Area | Mechanism |
|----------------|-----------|
| **Standards compliance** | Minimum KYC standards defined by Sky governance |
| **Legal entity requirements** | Must maintain qualified legal entity |
| **Operational audits** | Periodic audits of verification practices |
| **Revocation review** | Sky can mandate revocation for systemic issues |
| **Delisting** | Sky can remove Identity Network from accepted list |

### Accountability

Identity Networks face consequences for failures:
- **False attestations** — Slashing of network's collateral
- **Security breaches** — Mandatory disclosure, remediation
- **Regulatory violations** — Suspension from Sky ecosystem
- **Repeated failures** — Delisting from all Exchange Halos

---

## Example Identity Networks

### US Accredited Investor Network

**Qualification:** SEC Rule 501 accredited investor
- Income >$200K (individual) or >$300K (joint) for past 2 years
- Net worth >$1M (excluding primary residence)
- Certain professional credentials (Series 7, 65, 82)

**Verification:** Income verification, net worth verification, or professional credential check

**Expiry:** 2 years (annual revalidation optional)

### Non-US Qualified Investor Network

**Qualification:** Non-US person meeting home jurisdiction standards
- Not US person (no US citizenship, residency, or tax status)
- Meets "qualified investor" or equivalent in home jurisdiction

**Verification:** Passport/ID, residency proof, home jurisdiction qualification

**Expiry:** 1 year

### Institutional Network

**Qualification:** Registered institutional investor
- Banks, broker-dealers, insurance companies
- Registered investment advisers
- Pension funds, endowments
- Family offices with >$5M AUM

**Verification:** Entity documentation, registration proof, authorized signatory verification

**Expiry:** 1 year

---

## Open Questions

1. **Minimum standards** — What minimum KYC standards should Sky Core require?

2. **Cross-chain attestations** — How do attestations work for multi-chain addresses?

3. **Attestation portability** — Can users prove attestation to third parties outside Sky?

4. **Privacy enhancements** — Should ZK proofs be added for enhanced privacy?

5. **Liability framework** — What liability does an Identity Network bear for false attestations?

6. **Grace periods** — Should expired attestations have a grace period before trade restriction?

---

## Connection to Other Documents

| Document | Relationship |
|----------|--------------|
| `sky-intents.md` | Identity Networks enable permissioned trading |
| `portfolio-halo.md` | Portfolio Halos may require Identity Networks for counterparty restrictions |
| `sentinel-network.md` | lpha-identity is an LPHA beacon for identity registry management |
| `atlas-synome-separation.md` | Attestation metadata stored in Synome |

---

*This document defines Identity Networks. For trading infrastructure, see sky-intents.md.*
