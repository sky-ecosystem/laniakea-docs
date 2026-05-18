# Portfolio Halo

A Portfolio Halo is a Standard Halo Class that uses **LCTS** (Liquidity Constrained Token Standard) for pooled, fungible positions. Portfolio Halos provide the standardized intermediary layer between Sky's capital allocation infrastructure and external asset managers — a reusable legal + smart-contract framework that lets new RWA products launch in days rather than months.

For the Class / Book / Unit architecture this document slots into, see [`halo-classes.md`](halo-classes.md). For the LCTS contract spec, see [`../smart-contracts/lcts.md`](../smart-contracts/lcts.md).

---

## Why LCTS

Many RWA strategies face capacity constraints on both deposit (strategy size limits) and redemption (asset liquidation delay). LCTS solves the resulting fairness problem: pooled users in a generation share converted output proportionally, eliminating gas wars and first-come-first-served advantage. See [`../smart-contracts/lcts.md`](../smart-contracts/lcts.md) for the full mechanics.

| Use case | Why LCTS fits |
|---|---|
| Open participation with uniform terms | Fungible shares, no per-deal accounting |
| Capacity-constrained strategies | Generation-based fair distribution |
| Redemption with settlement delay | Queue absorbs liquidation timing |

For bespoke deals with per-counterparty terms, use a [Term Halo](halo-term.md) (NFAT-based) instead.

---

## Capital Deployment Mechanism

### Operating-setup-driven allocation

Once the full operating setup is online, every Prime is operated by `baseline-{prime}` (relay) + `warden-{prime}-{op}` (relay) + `stream-{prime}-{actor}` (stream-sentinel) — three distinct beacons deployed together that continuously optimize capital allocation. When a new Halo Unit becomes available, the setup:

1. **Detects the new Unit** via the Halo Artifact and governance registry
2. **Validates proper onboarding** — factory deployment, beacon integration, artifact reporting
3. **Calculates optimal allocation** based on risk parameters, yield, and portfolio balance
4. **Executes rebalancing** through the rate-limited PAU

This happens automatically across every Prime — no manual decisions, no relationship management, no capital raising.

### What "proper onboarding" means

For a Unit to trigger automatic Prime rebalancing, it must meet baseline requirements:

| Requirement | Purpose |
|---|---|
| Factory deployment | Smart contracts match audited templates |
| Beacon integration | Enables automated Prime rebalancing (relays + stream-sentinel) |
| Artifact reporting | Provides transparency on positions, yields, risks |
| Rate-limit configuration | Governance-approved bounds on capital flows |

Once these are met, the Unit is indistinguishable from any other onboarded deployment target.

For the operating-setup pattern itself (baseline-relay / warden-relay / stream-sentinel as three distinct beacon classes deployed together, Streaming Accord as recipe instance, TTS economics), see [`../sentinel/sentinel-network.md`](../sentinel/sentinel-network.md).

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SKY PROTOCOL                                 │
│   ┌─────────────┐                                                   │
│   │   Primes    │  Capital allocation entities within Sky           │
│   └──────┬──────┘                                                   │
│          │  Deploy capital via standardized vaults                  │
│          ▼                                                          │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                    PORTFOLIO HALO                            │   │
│   │   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐ │   │
│   │   │  Halo Unit A  │   │  Halo Unit B  │   │  Halo Unit C  │ │   │
│   │   │  (e.g., CLO)  │   │ (e.g., T-Bill)│   │ (e.g., MMF)   │ │   │
│   │   └───────┬───────┘   └───────┬───────┘   └───────┬───────┘ │   │
│   └───────────┼───────────────────┼───────────────────┼─────────┘   │
└───────────────┼───────────────────┼───────────────────┼─────────────┘
                ▼                   ▼                   ▼
        ┌───────────────────────────────────────────────────────┐
        │              ASSET MANAGEMENT PARTNERS                 │
        │   CLO Manager    T-Bill Provider    Money Market Fund  │
        └───────────────────────────────────────────────────────┘
```

| Component | Description |
|---|---|
| **Halo Class** | The Portfolio Halo entity — shared PAU, beacon, legal buybox, factory template |
| **Halo Units** | Individual investment products within the Class, each backed by a book |
| **lcts-{halo}** | Relay beacon (class `relay`) — operates LCTS vaults: deposits, redemptions, capacity, daily lock/settle |

`lcts-{halo}` is a deterministic-rule relay, not a sentinel. Stream-sentinels (e.g. `stream-{prime}-{actor}`) have call-out density and continuous real-time control; relay beacons execute pre-agreed rules. See [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) and [`../noemar-synlang/synlang-patterns.md`](../noemar-synlang/synlang-patterns.md) §6.

---

## Class Structure: Tranching

A Halo Class enables tranched structures where multiple Halo Units share operational infrastructure while offering different risk/return profiles:

```
┌─────────────────────────────────────────────────────────────┐
│                    HALO CLASS: CLO Tranched                  │
│              (Shared PAU + lcts-{halo} + Legal Buybox)       │
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
│              │  + lcts-{halo}  │                            │
│              └────────┬────────┘                            │
└───────────────────────┼──────────────────────────────────────┘
                        ▼
              ┌─────────────────┐
              │  Underlying     │
              │  CLO Assets     │
              └─────────────────┘
```

| Parameter | Variation |
|---|---|
| Seniority | Senior vs Junior tranche claims |
| Yield | Different return profiles based on risk |
| Capacity | Different allocation limits per tranche |
| LCTS parameters | Queue configuration, generation timing |

One beacon, one legal structure, multiple investment products with different risk/return characteristics.

---

## How Units Work

### Vault interface (LCTS)

Investors deposit assets into a queue and receive proportional shares. `lcts-{halo}` processes deposits and redemptions as capacity allows; all investors in the same generation share capacity fairly. Investors can exit during ACTIVE state.

For complete LCTS mechanics (generation lifecycle, lock window, settlement, exchange-rate query interface, srUSDS flow), see [`../smart-contracts/lcts.md`](../smart-contracts/lcts.md).

### Capital allocation infrastructure

Each Unit connects to Sky's PAU pattern:

- Rate limits control flow in each direction
- All transactions are constrained by governance-approved parameters
- Emergency controls allow rapid response (instant decreases; SORL-bound increases)

### Off-ramp to external assets

`lcts-{halo}` manages the interface with external asset managers — converting stablecoins to fiat via approved on/off-ramps, executing subscriptions and redemptions with underlying managers, reporting positions and yields back to the protocol.

---

## Legal Infrastructure

| Principle | Description |
|---|---|
| **Default ownership to Sky** | In absence of legal intervention, Sky's designated entity (the Fortification Conserver) can assume direct control through established supervisory mechanisms |
| **Standardized templates** | Legal frameworks are copy-paste deployable; new Units launch quickly using established structures |
| **Pre-signed integration** | Partners can pre-sign standardized agreements that auto-integrate with new Halo Units |

### Governance artifacts

| Artifact | Contents |
|---|---|
| **Halo Artifact** | Overall governance, generic Unit procedures, recourse mechanisms, migration procedures |
| **Unit Artifact** | Unit-specific operational parameters, legal recourse, sentinel configuration, risk monitoring |

---

## Capital Efficiency Insight

The defining advantage of launching through an established Portfolio Halo:

> When a new Halo Unit is properly onboarded, **every Prime in the Sky ecosystem will simultaneously rebalance into the new Unit.**

This isn't gradual ramp-up. It's immediate, coordinated capital deployment across the entire protocol — possible because:

| Factor | Effect |
|---|---|
| Standardized risk framework | Primes don't need individual due diligence |
| Automated rebalancing | Operating setups (baseline-relay + warden-relay + stream-sentinel) continuously optimize allocation |
| Pre-approved integration | Primes have pre-signed agreements with established Halos |
| Unified monitoring | Halo Artifact provides consistent reporting / risk monitoring |

The constraint becomes capacity management, not capital raising. The question shifts from "can we attract enough capital?" to "how much capacity can we offer?"

---

## Launching a New Unit

| Step | Description |
|---|---|
| 1. Demand identification | Multiple Primes express interest; partner identified |
| 2. Preparation | Asset manager confirms readiness; `lcts-{halo}` configured for asset-specific requirements; smart contracts prepared via factory |
| 3. Governance approval | Halo Artifact Edit proposed with Unit specifications; approval (typically days, not weeks); contracts deployed |
| 4. Live | All Primes automatically rebalance into the new Unit; `lcts-{halo}` processes deposits and manages positions; ongoing monitoring |

---

## Comparison with Other Halo Classes

| Dimension | Portfolio | Term | Trading |
|---|---|---|---|
| Mechanism | LCTS queues | NFAT facilities | AMM pools |
| User interaction | Queue → wait → receive shares | Negotiate → NFAT minted | Swap instantly |
| Settlement | Daily batch (lock/settle cycle) | Per-deal | Atomic (instant) |
| Revenue | Yield from deployed capital | Yield from deployed capital | Spread from trading activity |
| Beacon | `lcts-{halo}` | `nfat-{halo}` + `attest-data-{class}` | `amm-{halo}` |

---

## Related

- [`halo-classes.md`](halo-classes.md) — Class / Book / Unit architecture
- [`halo-term.md`](halo-term.md) — NFAT-based alternative for bespoke deals
- [`halo-trading.md`](halo-trading.md) — AMM-based for instant liquidity
- [`prime.md`](prime.md) — Primes that allocate to Portfolio Halos
- [`../smart-contracts/lcts.md`](../smart-contracts/lcts.md) — LCTS standard
- [`../smart-contracts/architecture-overview.md`](../smart-contracts/architecture-overview.md) — PAU pattern
- [`../smart-contracts/configurator-unit.md`](../smart-contracts/configurator-unit.md) — Onboarding via init rate limits
- [`../sentinel/sentinel-network.md`](../sentinel/sentinel-network.md) — Operating setups on Primes that rebalance into Units
- [`../risk-framework/halobook-layer.md`](../risk-framework/halobook-layer.md) — Halobook in the risk framework
