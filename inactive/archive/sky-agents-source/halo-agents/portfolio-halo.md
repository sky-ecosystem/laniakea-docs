# Portfolio Halo — Business Overview

## Executive Summary

The Portfolio Halo is a key infrastructure component of Sky's 2026 scaling roadmap, designed to enable rapid, scalable deployment of capital into real-world assets (RWA) through partnerships with institutional asset managers.

A Portfolio Halo acts as a specialized intermediary layer that connects Sky's capital allocation infrastructure with external asset managers. It provides standardized legal frameworks, smart contract infrastructure, and operational processes that dramatically reduce the time and complexity required to launch new investment products.

**Key value proposition**: Enable asset managers to offer Sky-compatible investment products with minimal legal overhead, standardized smart contract infrastructure, and rapid time-to-market — with the potential for hundreds of millions in capital deployment on Day 1 as every Prime in the ecosystem simultaneously rebalances into newly launched Units.

---

## The Opportunity

### Current Challenge

Deploying capital into real-world assets through DeFi requires:
- Complex bespoke legal structures for each asset type
- Custom smart contract development and audits
- Extended negotiation cycles with each counterparty
- Duplicated compliance and operational overhead

### The Portfolio Halo Solution

Portfolio Halos create **economies of scale** by:
- Establishing reusable legal infrastructure that multiple asset types can share
- Deploying standardized smart contracts from a pre-audited factory
- Enabling asset managers to launch new products in days rather than months
- Providing Sky with strong, consistent recourse mechanisms across all deployments

---

## The Capital Deployment Mechanism

Understanding why Portfolio Halos deliver immediate capital at scale requires understanding how Sky's allocation infrastructure works:

### Sentinel-Driven Allocation (Phase 9+)

> **Phasing note:** In Phases 1–3, Prime allocations and Halo onboarding are governance-directed and executed manually via spells. Factories begin in Phase 5. Prime-side sentinel formations (`stl-base`, `stl-stream`, `stl-warden`) and auction-based allocation come later.

Once sentinel formations are deployed, every Prime in the Sky ecosystem is operated by a **sentinel formation** (stl-base + stl-stream + stl-warden) — an automated system that continuously optimizes capital allocation across available deployment targets. When a new Halo Unit becomes available, the sentinel formation:

1. **Detects the new Unit** via the Halo Artifact and governance registry
2. **Validates proper onboarding** — factory deployment, Sentinel integration, artifact reporting
3. **Calculates optimal allocation** based on risk parameters, yield, and portfolio balance
4. **Executes rebalancing** through the rate-limited allocation infrastructure

This happens automatically across every Prime. There's no manual decision-making, no relationship management, no capital raising calls. The infrastructure does the work.

### What "Proper Onboarding" Means

For a Halo Unit to trigger automatic Prime rebalancing, it must meet baseline requirements:

| Requirement | Purpose |
|-------------|---------|
| **Factory deployment** | Ensures smart contracts match audited templates |
| **Sentinel integration** | Enables automated Prime rebalancing once sentinels are live (Phase 9+) |
| **Artifact reporting** | Provides transparency on positions, yields, and risks |
| **Rate limit configuration** | Governance-approved bounds on capital flows |

Once these conditions are met, the Unit is indistinguishable from any other properly-onboarded deployment target. Primes treat it as part of their standard allocation universe.

### The Network Effect

Each additional Portfolio Halo amplifies the value for asset managers:

- More Halos → more standardized infrastructure → faster onboarding
- More Units → more Prime demand for diversification → larger per-Unit allocations
- More capital deployed → more institutional credibility → more asset manager interest

This creates a flywheel where established Portfolio Halos become increasingly attractive partners for asset managers seeking immediate, scalable capital deployment.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SKY PROTOCOL                                 │
│                                                                      │
│   ┌─────────────┐                                                   │
│   │   Primes    │  Capital allocation entities within Sky           │
│   └──────┬──────┘                                                   │
│          │                                                          │
│          │  Deploy capital via standardized vaults                  │
│          ▼                                                          │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                    PASSTHROUGH HALO                          │   │
│   │                                                              │   │
│   │   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐ │   │
│   │   │  Halo Unit A  │   │  Halo Unit B  │   │  Halo Unit C  │ │   │
│   │   │  (e.g., CLO)  │   │ (e.g., T-Bill)│   │ (e.g., MMF)   │ │   │
│   │   └───────┬───────┘   └───────┬───────┘   └───────┬───────┘ │   │
│   │           │                   │                   │         │   │
│   └───────────┼───────────────────┼───────────────────┼─────────┘   │
│               │                   │                   │             │
└───────────────┼───────────────────┼───────────────────┼─────────────┘
                │                   │                   │
                ▼                   ▼                   ▼
        ┌───────────────────────────────────────────────────────┐
        │              ASSET MANAGEMENT PARTNERS                 │
        │                                                        │
        │   CLO Manager    T-Bill Provider    Money Market Fund  │
        └───────────────────────────────────────────────────────┘
```

### Core Components

| Component | Description |
|-----------|-------------|
| **Halo Agent** | The governing entity that manages multiple Halo Units, maintains artifacts, and coordinates with Sky governance |
| **Halo Units** | Individual investment products, each consisting of a vault (for deposits/redemptions) and allocation infrastructure |
| **lpha-lcts** | LPHA beacon that maintains governance, executes approved changes, ensures compliance, and handles per-unit operations including deposits, redemptions, yield distribution, and capital allocation |

---

## Halo Class Structure

Portfolio Halos are organized into **Halo Classes** — groupings of Halo Units that share the same smart contract infrastructure (PAU, beacon) and legal framework.

### Why Halo Classes Matter

A Halo Class enables **tranched structures** where multiple Halo Units share operational infrastructure while offering different risk/return profiles:

```
┌─────────────────────────────────────────────────────────────┐
│                    HALO CLASS: CLO Tranched                  │
│              (Shared PAU + lpha-lcts + Legal Buybox)         │
│                                                              │
│   ┌─────────────────┐        ┌─────────────────┐           │
│   │  Halo Unit:     │        │  Halo Unit:     │           │
│   │  Senior Tranche │        │  Junior Tranche │           │
│   │  (Lower yield,  │        │  (Higher yield, │           │
│   │   first claim)  │        │   second claim) │           │
│   └────────┬────────┘        └────────┬────────┘           │
│            │                          │                     │
│            └──────────┬───────────────┘                     │
│                       │                                      │
│              ┌────────▼────────┐                            │
│              │  Shared PAU     │                            │
│              │  + lpha-lcts     │                            │
│              └────────┬────────┘                            │
│                       │                                      │
└───────────────────────┼──────────────────────────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │  Underlying     │
              │  CLO Assets     │
              └─────────────────┘
```

### What a Halo Class Shares

| Component | Description |
|-----------|-------------|
| **PAU** | Single Controller + ALMProxy + RateLimits for all Units in the class |
| **LPHA Beacon** | lpha-lcts manages all Units |
| **Legal Framework** | Shared buybox, counterparty agreements, recourse mechanisms |
| **Factory Template** | All Units deployed from the same template (manual deployment pre-factory; factory deployment once Halo Factory is live) |

> **Note:** lpha-lcts is an **LPHA beacon** (Low Power, High Authority) — a deterministic rule executor, not a sentinel. Sentinels (stl-base, stl-stream, stl-warden) have continuous real-time control and proprietary intelligence. LPHA beacons like lpha-lcts apply rules exactly as written without judgment. See `beacon-framework.md` for the full taxonomy.

### What Halo Units Can Vary

| Parameter | Example Variation |
|-----------|-------------------|
| **Seniority** | Senior vs Junior tranche claims |
| **Yield** | Different return profiles based on risk |
| **Capacity** | Different allocation limits per tranche |
| **LCTS Parameters** | Queue configuration, generation timing |

This structure enables efficient capital deployment: one LPHA beacon, one legal structure, multiple investment products with different risk/return characteristics.

---

## How Halo Units Work

Each Halo Unit represents a specific investment product within a Halo Class and consists of:

### 1. Vault Interface (LCTS)

Halo Units use the **Liquidity Constrained Token Standard (LCTS)** — a queue-based system designed for assets with capacity or liquidity constraints.

**How it works:**
- Investors deposit assets into a queue and receive proportional shares
- lpha-lcts processes deposits and redemptions as capacity allows
- All investors in the same queue cohort share capacity fairly
- Investors can exit the queue at any time before their assets are deployed

**Why LCTS?**
- Many RWA strategies have limited capacity (e.g., specific bond offerings)
- Redemptions may require asset liquidation with delays
- Queue-based design ensures fairness without first-come-first-served competition

### 2. Capital Allocation Infrastructure

Each Halo Unit connects to Sky's Parallelized Allocation System (PAS):
- Rate limits control how much capital can flow in each direction
- All transactions are monitored and constrained by governance-approved parameters
- Emergency controls allow rapid response to market conditions

### 3. Off-ramp to External Assets

lpha-lcts manages the interface with external asset managers:
- Converts stablecoins to fiat via approved on/off-ramps
- Executes subscriptions and redemptions with underlying asset managers
- Reports positions and yields back to the protocol

---

## Legal Infrastructure

### Design Principles

The Portfolio Halo legal structure prioritizes:

1. **Default Ownership to Sky**  
   In absence of legal intervention, Sky's designated entity (the Fortification Conserver) can assume direct control through established supervisory mechanisms. This ensures Sky is never dependent on lengthy legal processes to recover assets.

2. **Standardized, Replicable Structures**  
   Legal frameworks are designed to be copy-paste deployable. New Halo Units can launch quickly using established templates rather than requiring bespoke legal engineering.

3. **Pre-signed Integration**  
   Partners can pre-sign standardized agreements that enable automatic integration with new Halo Units, reducing negotiation cycles for each new product launch.

### Governance Artifacts

Each Halo maintains detailed documentation:

| Artifact | Contents |
|----------|----------|
| **Halo Artifact** | Overall governance processes, generic Unit procedures, recourse mechanisms, migration procedures |
| **Unit Artifact** | Unit-specific operational parameters, legal recourse documentation, Sentinel configuration, risk monitoring procedures |

These artifacts provide complete transparency and serve as operational playbooks for all parties.

---

## Benefits for Asset Management Partners

### Rapid Product Launch

| Traditional Approach | With Portfolio Halo |
|---------------------|----------------------|
| 3-6 months for legal structure | Days using established templates |
| Custom smart contract development | Pre-audited factory deployment |
| Individual negotiations with each allocator | Standardized integration with multiple Primes |
| Bespoke compliance frameworks | Inherited governance and monitoring |

### Immediate Capital at Scale

This is the defining advantage of launching through an established Portfolio Halo:

**When a new Halo Unit is properly onboarded** — meaning it's deployed via the Laniakea Factory, integrated with lpha-lcts, and reporting all required data into the Halo Artifact — **every Prime in the Sky ecosystem will simultaneously rebalance into the new Unit.**

This isn't a gradual ramp-up. It's immediate, coordinated capital deployment across the entire protocol.

| Traditional Asset Launch | Portfolio Halo Launch |
|-------------------------|------------------------|
| Months of investor outreach | Instant access to all Primes |
| Gradual capital accumulation | Hundreds of millions on Day 1 |
| Individual relationship management | Single integration, multiple allocators |
| Uncertain timeline to scale | Predictable, immediate scale |

**Why this happens:**

1. **Standardized risk framework**: Once a Unit is onboarded through an established Portfolio Halo, Primes don't need individual due diligence — the Halo's governance and Sentinel infrastructure provides the assurance layer

2. **Automated rebalancing**: Sentinel formations continuously optimize allocations across available Halo Units. A newly available, properly-onboarded Unit triggers rebalancing across the entire Prime layer

3. **Pre-approved integration**: Primes have pre-signed agreements with established Portfolio Halos, eliminating per-Unit legal negotiation

4. **Unified monitoring**: The Halo Artifact and Sentinel infrastructure means all Units share consistent reporting, risk monitoring, and emergency procedures — reducing operational friction to near zero

**The implication for asset managers**: Your constraint becomes capacity management, not capital raising. The question shifts from "can we attract enough capital?" to "how much capacity can we offer?"

### Access to Diversified Capital Sources

- **Multiple capital sources**: Any Prime within the Sky ecosystem can allocate to Halo Units
- **Predictable inflows**: Queue-based system provides visibility into pending deployments
- **Institutional scale**: Sky's allocation infrastructure is designed for billions in TVL

### Reduced Operational Burden

- **Automated operations**: lpha-lcts handles routine deposit/redemption processing
- **Standardized reporting**: Artifact system ensures consistent, auditable records
- **Shared infrastructure**: Compliance, monitoring, and emergency response handled at the Halo level

---

## Launching a New Halo Unit

### Process Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│  1. DEMAND IDENTIFICATION                                           │
│     • Multiple Primes express interest in asset class               │
│     • Halo contributors identify suitable asset manager partner     │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  2. PREPARATION                                                      │
│     • Asset manager confirms readiness and terms                    │
│     • lpha-lcts configured for asset-specific requirements        │
│     • Smart contracts prepared via Laniakea Factory                 │
│     • GovOps coordinates infrastructure setup                       │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  3. GOVERNANCE APPROVAL                                              │
│     • Halo Artifact Edit proposed with Unit specifications          │
│     • Standard approval process (typically days, not weeks)         │
│     • Smart contracts deployed from factory                         │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  4. LIVE — IMMEDIATE CAPITAL DEPLOYMENT                              │
│     • All Primes automatically rebalance into new Unit              │
│     • Potential for hundreds of millions in Day 1 inflows           │
│     • lpha-lcts processes deposits and manages positions          │
│     • Ongoing monitoring and reporting via artifact system          │
└─────────────────────────────────────────────────────────────────────┘
```

### Timeline Comparison

| Phase | Traditional | Portfolio Halo |
|-------|-------------|------------------|
| Legal structure | 2-4 months | Pre-established |
| Smart contracts | 1-2 months + audit | Factory deployment (days) |
| Integration testing | 2-4 weeks | Standardized (days) |
| Governance approval | Variable | ~1 week |
| **Total** | **4-8 months** | **2-4 weeks** |

---

## Governance and Risk Management

### Halo-Level Governance

- **lpha-lcts** maintains the Halo Artifact and coordinates governance
- Optional governance token allows stakeholder participation in Halo decisions
- Artifact Edits flow through Sky governance (Sky Spells, Prime Spells, Halo Spells)

### Unit-Level Operations

- **lpha-lcts** operates autonomously within parameters defined in the Unit Artifact
- Processes deposits and redemptions based on capacity and liquidity
- Maintains detailed logs of all activities
- Monitors external asset manager for risk signals

### Emergency Procedures

- Unit Artifacts specify warning signals and response procedures
- Migration paths defined for moving assets to alternative structures if needed
- Fortification Conserver can intervene through supervisory mechanisms

---

## Technical Integration

### Smart Contract Stack

Each Halo Unit deploys standardized infrastructure:

| Component | Function |
|-----------|----------|
| **LCTS Vault** | Queue-based deposit/redemption interface |
| **Parallelized Allocation Unit (PAU)** | Controller, ALM Proxy, Rate Limits |
| **Off-ramp Integration** | PSM connection for USDC conversion, restricted endpoints for fiat |

### Laniakea Factory

All smart contract infrastructure deploys from the Laniakea Factory:
- Pre-audited contract templates
- Automatic configuration based on Unit parameters
- Immediate integration with governance systems
- No custom development required for standard deployments

---

## Summary

The Portfolio Halo represents a fundamental shift in how DeFi protocols can partner with traditional asset managers:

- **For Sky**: Scalable, consistent access to diverse RWA yield strategies with strong governance and recourse
- **For Asset Managers**: Immediate access to hundreds of millions in capital the moment a Unit launches — no fundraising, no gradual ramp-up
- **For the Ecosystem**: Standardized infrastructure that compounds in value as more Units launch

The core insight is this: **capital raising becomes a solved problem.** Once an asset manager is integrated with an established Portfolio Halo, their constraint becomes capacity — how much can they deploy? — not capital attraction. Every properly onboarded Halo Unit triggers automatic rebalancing across the entire Prime layer, delivering institutional-scale capital on Day 1.

By establishing reusable legal frameworks, pre-audited smart contracts, and automated operational processes, Portfolio Halos transform what was previously a months-long bespoke integration into a streamlined, repeatable process that can scale to support dozens of investment products across multiple asset managers.

---

## Next Steps for Partners

Interested asset managers should contact Sky to discuss:

1. **Asset types** suitable for Halo Unit deployment
2. **Capacity and liquidity characteristics** for LCTS configuration
3. **Legal entity requirements** and pre-signing arrangements
4. **Technical integration** requirements for position reporting and redemption processing
5. **Timeline** for initial Unit launch

---

*Document Version: 0.1*  
*Last Updated: January 2026*
