# Identity Network Halo

An Identity Network is a **Special Halo** Class that operates KYC/identity verification services. Instead of deploying capital into investment strategies, an Identity Network maintains an on-chain registry of addresses verified to meet certain criteria (accredited investor, non-US person, qualified purchaser, etc.). This enables permissioned tokens within the Sky Ecosystem.

For the Class / Book / Unit architecture, see [`halo-classes.md`](halo-classes.md). For the trading protocol that consumes Identity Network attestations, see [`../trading/sky-intents.md`](sky-intents.md).

---

## Why Identity Networks Exist

Sky Ecosystem enables Halo Units that wrap diverse assets — DeFi positions, private credit, tokenized real-world assets. For many of these:

- Issuers prefer known counterparties (asset managers, originators)
- Participants prefer verified peers (institutional investors)
- Compliance teams require documentation
- Some jurisdictions impose geographic or qualification requirements

Identity Networks provide attestations: "this address belongs to a verified accredited investor", "this address is a qualified institutional buyer", "this address is a professional client". Token contracts check these attestations on every transfer; non-members cannot receive the token.

### Why a Halo type?

| Reason | Description |
|---|---|
| Governance integration | Subject to Sky oversight and standards |
| Economic alignment | Network operators earn fees, have skin in the game |
| Composability | Other Halos and Primes can query attestation status |
| Accountability | Slashing and penalty mechanisms apply |

---

## Restricted Halo Type

| Aspect | Regular Halo | Identity Network Halo |
|---|---|---|
| Primary activity | Deploy capital, generate yield | Operate identity registry |
| Revenue source | Investment returns | Membership / verification fees |
| Capital deployment | Yes | **No** (prohibited) |
| Asset custody | Holds assets via PAU | Minimal (operating capital only) |
| Risk capital | Required per Risk Framework | Minimal (operational risk only) |
| Oversight | Standard Halo governance | Elevated — compliance-critical |

### Permitted activities

- Operate an on-chain attestation registry
- Control a legal entity that performs KYC verification
- Charge membership and verification fees
- Hold operating capital (not investment capital)
- Issue a governance token for network decisions
- Participate in cross-recognition agreements with other Identity Networks

### Prohibited

- Deploy capital into investment strategies
- Accept deposits beyond operating needs
- Issue yield-bearing tokens
- Operate as a Prime or standard Halo

---

## Economic Model

| Fee Type | Description |
|---|---|
| Membership fee | Annual / monthly fee for maintaining attestation |
| Verification fee | One-time fee for initial KYC processing |
| Revalidation fee | Fee for periodic re-verification (e.g., annual) |
| API access fee | Fees for high-volume attestation queries |
| Cross-recognition fee | Fees from partner networks for mutual recognition |

Fees are set by the Identity Network's governance. Competition between networks creates pressure for reasonable pricing.

---

## On-Chain Registry

The on-chain component is intentionally minimal — a list of addresses managed by `identity-{network}`:

```
Identity Registry Contract:
  - Storage: set of member addresses
  - Query:  isMember(address) → true/false
  - Modify: add(address), remove(address), addBatch([addresses]), removeBatch([addresses])
  - Access: only identity-{network} can modify
```

That's it. A simple address set. No status enums, no metadata, no expiry dates on-chain.

### How it's used

Restrictions are enforced at the **token level**:

```
Halo Unit transfer check (on every transfer):
  IF restricted transfers enabled:
    FOR each accepted Identity Network:
      IF network.isMember(recipient) → allow transfer
    IF no network accepted recipient → reject transfer
```

This is a first-order restriction. Trading restrictions on exchanges are a second-order effect — if you can't receive the token, exchange settlement fails because the token transfer reverts.

### Who sets accepted networks?

The **Halo Unit issuer** (or Prime token issuer) configures accepted Identity Networks at deployment. This is baked into the token contract, not at the trading venue layer. Trading venues inherit restrictions automatically.

### Beyond Halo Units: Prime tokens

Identity Networks aren't just for Halo Units. Institutional Primes also use them to restrict holders of their Prime tokens — e.g., an institutional Prime serving only qualified institutional buyers might require all token holders to be members of an Institutional Identity Network.

### Multiple addresses per entity

When registering for KYC, users can add one or more addresses to their attestation. The Identity Network and its legal entity manage this:

- User completes KYC once
- User provides list of addresses they control
- All addresses added to the on-chain registry
- User can request additional addresses later (may require verification)
- If attestation expires or is revoked, ALL linked addresses are removed

### Heavy lifting in Synome

| Data | Location | Purpose |
|---|---|---|
| Address list | On-chain | Simple membership check |
| Attestation details | Synome | Type, issue date, expiry, verification level |
| Linked addresses | Synome | All addresses belonging to same verified entity |
| Jurisdiction info | Synome | Primary jurisdiction of verified entity |
| KYC documents | Legal entity (off-chain) | Actual verification records |
| Personal identity | Legal entity (off-chain) | Never stored in Synome |

`identity-{network}` translates between layers: monitors Synome for attestation changes, expiries, revocations; updates the on-chain list accordingly.

---

## Multiple Networks

Multiple Identity Networks can operate simultaneously, specializing in different jurisdictions, investor types, or verification standards. Examples:

| Network | Qualification | Verification | Expiry |
|---|---|---|---|
| **US Accredited** | SEC Rule 501 (income, net worth, professional credentials) | Income / net worth / credential check | 2 years |
| **Non-US Qualified** | Non-US person meeting home jurisdiction standards | Passport / ID, residency, jurisdiction qualification | 1 year |
| **Institutional** | Banks, broker-dealers, registered advisers, pension funds, family offices >$5M AUM | Entity documentation, registration proof, signatory verification | 1 year |

The **Halo Unit issuer** configures accepted networks at deployment:

```
Token Configuration (set by issuer):
  - Accepted Networks: list of Identity Networks whose members can receive the token
  - If empty: unrestricted, anyone can hold/receive
```

| Token | Accepted Networks |
|---|---|
| USDS, SKY | None — unrestricted |
| JAAA Halo Unit | US Accredited, Non-US QIB |
| Private Credit Halo Unit | Institutional only |
| Institutional Prime Token | Institutional only |

---

## Legal Entity Operations

```
┌─────────────────────────────────────────────────────────┐
│            Identity Network Halo                         │
│            (On-chain governance)                         │
│                                                          │
│   Identity Registry  (On-chain: simple address list)    │
│            │                                             │
│       controls                                           │
│            ▼                                             │
│   Legal Entity  (Foundation, LLC, regulated entity)     │
│   - Receives KYC applications                           │
│   - Verifies documents                                  │
│   - Stores records (off-chain)                          │
│   - Updates Synome → identity-{network} syncs to chain       │
│   - Handles disputes, appeals, revocations              │
└─────────────────────────────────────────────────────────┘
```

### KYC processing flow

| Step | Action |
|---|---|
| 1. Apply | User submits application + documents to legal entity |
| 2. Verify | Legal entity reviews — identity, qualification, AML/sanctions |
| 3. Decision | Approved → attestation in Synome with expiry → `identity-{network}` adds to on-chain list. Denied → not added. |
| 4. Maintain | Periodic revalidation (e.g., annually); user re-submits required documents |
| 5. Expire / revoke | Expiry → `identity-{network}` removes when expiry passes. Revocation → legal entity revokes in Synome → `identity-{network}` removes immediately |

### Regulatory compliance

The legal entity must comply with:
- **AML/KYC regulations** in its jurisdiction
- **Data protection** (GDPR, CCPA, etc.)
- **Record retention** requirements
- **Sanctions screening** (OFAC, EU, UN lists)

The Halo provides the governance framework; the legal entity handles regulatory compliance.

### Revocation triggers

- Fraud — falsified documents or misrepresentation
- Change in status — no longer meets qualification criteria
- Sanctions listing
- User request
- Legal order — court order or regulatory action

Revocation is immediate.

---

## Beacon: identity-{network}

`identity-{network}` is a relay beacon (class `relay`; high authority, low power) — see [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md).

### Role

```
Legal Entity → Synome → identity-{network} → On-chain Registry
   (KYC)      (state)    (executor)      (simple list)
```

| Function | Description |
|---|---|
| Add members | When Synome shows new valid attestation, add to on-chain list |
| Remove members | When Synome shows expiry/revocation, remove from on-chain list |
| Expiry monitoring | Watch Synome for upcoming expiries |
| Batch updates | Process multiple adds/removes efficiently |

### Security model

- **Sole writer** — Only `identity-{network}` can modify the on-chain registry
- **Synome as source of truth** — `identity-{network}` only acts on Synome state
- **Audit trail** — All changes logged in Synome with timestamps
- **Rate limits** — Maximum updates per period (prevents spam/abuse)

---

## Connection to Trading Venues

Identity Networks enable restricted tokens to trade on permissioned venues. Restrictions are enforced at the **token level**, not the venue level — when settlement executes, the token contract checks if the recipient is in an accepted Identity Network; if not, the transfer reverts and the entire settlement fails. Trading venues don't need separate identity logic.

| Optional UX | Description |
|---|---|
| Order visibility | Venues may hide orders from non-eligible counterparties (UX optimization, not a security check) |
| Attestation events | `identity-{network}` emits events on add/remove; venues can subscribe to cancel orders from removed addresses proactively |

---

## Governance and Oversight

### Identity Network governance

Each Network has its own governance — token-based voting (if Network issues token), fee setting, policy updates, operator appointments.

### Sky Core oversight

Identity Networks operate under elevated Core Council oversight:

| Area | Mechanism |
|---|---|
| Standards compliance | Minimum KYC standards defined by Sky governance |
| Legal entity requirements | Must maintain qualified legal entity |
| Operational audits | Periodic audits of verification practices |
| Revocation review | Sky can mandate revocation for systemic issues |
| Delisting | Sky can remove Network from accepted lists |

### Accountability

- **False attestations** — slashing of Network's collateral
- **Security breaches** — mandatory disclosure, remediation
- **Regulatory violations** — suspension from Sky ecosystem
- **Repeated failures** — delisting from all permissioned trading venues

---

## Open Questions

1. Minimum KYC standards Sky should require
2. Cross-chain attestations (multi-chain addresses)
3. Attestation portability outside Sky
4. Privacy enhancements (ZK proofs)
5. Liability framework for false attestations
6. Grace periods for expired attestations before trade restriction

---

## Related

- [`halo-classes.md`](halo-classes.md) — Class / Book / Unit architecture
- [`halo-portfolio.md`](halo-portfolio.md) — Portfolio Halos that may require Identity Network membership
- [`../trading/sky-intents.md`](sky-intents.md) — Trading protocol consuming attestations (canonical)
- [`../sentinel/sentinel-network.md`](../sentinel/sentinel-network.md) — `identity-{network}` as a relay beacon in the operating setup
- [`../macrosynomics/atlas-synome-separation.md`](../macrosynomics/atlas-synome-separation.md) — Attestation metadata in Synome
- [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) — Beacon classification
