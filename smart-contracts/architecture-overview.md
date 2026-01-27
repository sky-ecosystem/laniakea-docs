# Laniakea Upgrade - Architecture Overview

## Executive Summary

The Laniakea Upgrade is Sky Ecosystem's new infrastructure development plan for automated capital deployment across multiple blockchain layers. This document primarily describes the Laniakea Smart Contracts, but reference other essential parts of the Laniakea Upgrade, such as the Sentinel Network. The system extends the existing Spark ALM Controller contracts, using a modular PAU (Parallelized Allocation Unit) pattern for maximum code reuse across all deployment contexts.

---

## Core Principle

Every layer is composed of PAUs using the same contract patterns. The system minimizes code differences between layers to maximize audit reuse and simplify deployment.

---

## The PAU Pattern (Universal Building Block)

Every PAU, regardless of layer, consists of the same core components:

| Component | Purpose |
|-----------|---------|
| **Controller** | Entry point for operations, enforces rate limits (MainnetController or ForeignController) |
| **ALMProxy** | Holds custody of funds, executes calls via `doCall()` |
| **RateLimits** | Linear replenishment rate limits with configurable max and slope |
| **Governance Layer** | Whitelist validation, operational constraints, enumeration |

What differs between PAU deployments:
- Upstream connection (what feeds capital in)
- Approved allocation targets (what the PAU can deploy to)
- Rate limit values (how much can flow)
- **Nothing else** — same contracts, different configuration

---

## The Four Layers

| Layer | Location | Upstream Connection | Downstream Connection |
|-------|----------|--------------------|-----------------------|
| **Generator** | Mainnet | ERC20 stablecoin contract | Prime Layer (via ERC4626 vault) |
| **Prime** | Mainnet | Generator Layer | Halo Layer (including Core Halos) |
| **Halo** | Mainnet | Prime Layer | RWA strategies, custodians, regulated endpoints |
| **Foreign** | Altchains | Mainnet Prime (via bridge) | Foreign Halo Layer |

---

## Layer Details

### Generator Layer

- Manages the interface with the stablecoin ERC20 contract
- Deploys capital into Prime Layer via **ERC4626 vaults** (deposit anytime, redeem if liquidity available)
- Has its own governance scope separate from Prime/Halo

### Prime Layer (Mainnet)

- Receives capital from Generator via ERC4626 vault
- Deploys to:
  - **Halo Layer** — the primary long-term deployment path (includes both Prime-created Halos and Core Halos)
  - **Core Halos** — legacy DeFi (Morpho vaults, Aave pools, SparkLend) wrapped as Halo Units under Core Council governance
  - **Foreign Primes** — via bridge for cross-chain deployment
- Each Prime controls its own vault's liquidity availability

### Halo Layer (Mainnet)

- Receives capital from Prime Layer
- Deploys to **RWA strategies**, custodian vaults, and regulated offramps (not external DeFi)
- Multiple vault types supported:
  - Stablecoin-style (instant deposit/redeem)
  - Request/redeem patterns
  - **LCTS** (Liquidity Constrained Token Standard) — queue-based, most common for capacity-constrained strategies
- LCTS is the natural fit because Halos face capacity/liquidity constraints both on deposit (capacity-limited strategies) and withdrawal (liquidity constraints)

### Foreign Layer (Altchains)

**Foreign Prime:**
- Receives bridged assets from mainnet Prime
- **No vault** between Prime and Foreign Prime — direct ALM Proxy to ALM Proxy transfers via bridge
- Deploys to Foreign Halo Layer on that chain

**Foreign Halo:**
- Works identically to mainnet Halo Layer
- Uses same vault types as mainnet
- Deploys to external yield strategies on that chain

---

## Connection Types Between Layers

| Connection | Mechanism | Control |
|------------|-----------|---------|
| Generator → Prime | ERC4626 vault | Rate limits on deposit/withdraw |
| Prime → Halo | ERC4626 vault (or other vault types) | Rate limits + vault-specific parameters |
| Prime → Core Halos | Via CoreHaloFacet (ERC4626, Aave, Curve interfaces) | Rate limits + protocol-specific parameters |
| Prime → Foreign Prime | Direct bridge transfer (no vault) | Rate limits on LayerZero/CCTP transfers |
| Foreign Prime → Foreign Halo | Various vault types | Rate limits + vault-specific parameters |
| Halo → RWA/Custodian | Asset transfer | Rate limits on transfers to custodian addresses |

---

## Governance Structure

### Per-Layer Governance Scope

Each layer type has its own governance scope for managing approved allocation targets and operational permissions:

| Scope | Controls | Used By |
|-------|----------|---------|
| Generator scope | Generator operations | All Generator PAUs |
| Mainnet scope | Prime + Halo operations | All mainnet Prime and Halo PAUs |
| Per-chain altchain scope | Foreign Prime + Foreign Halo operations | All Foreign Prime and Foreign Halo PAUs on that chain |

### Onboarding Types

**General onboarding**: A target approved for any PAU within the scope to use
- Example: A Morpho vault that any Prime can deploy to

**Limited onboarding**: A target approved for only a specific PAU
- Example: A bridge route from Prime A to Foreign Prime A (other Primes cannot use this route)
- Example: A regulated offramp that only accepts assets from a specific KYC'd Halo

---

## Code Reuse Principle

The same contracts power every layer:

| Component | Generator | Prime | Halo | Foreign Prime | Foreign Halo |
|-----------|-----------|-------|------|---------------|--------------|
| Controller | MainnetController | MainnetController | MainnetController | ForeignController | ForeignController |
| Proxy | ALMProxy | ALMProxy | ALMProxy | ALMProxy | ALMProxy |
| Rate Limits | RateLimits | RateLimits | RateLimits | RateLimits | RateLimits |
| Governance | ✓ | ✓ | ✓ | ✓ | ✓ |

This means:
- No new controller code for new layers
- No new proxy code
- Factories can stamp out identical PAUs
- Adding a new layer = deploying more instances of the same contracts

---

## Capital Flow

```
                    MAINNET                              ALTCHAIN
                    
┌──────────────┐                                    
│   ERC20      │                                    
│  Stablecoin  │                                    
└──────┬───────┘                                    
       │                                            
       ▼                                            
┌──────────────┐                                    
│  Generator   │                                    
│    PAU       │                                    
└──────┬───────┘                                    
       │ ERC4626 vault                              
       ▼                                            
┌──────────────┐         bridge          ┌──────────────┐
│    Prime     │ ──────────────────────► │   Foreign    │
│    PAU       │   (no vault, direct)    │  Prime PAU   │
└──┬───┬───────┘                         └──────┬───────┘
   │   │                                        │
   │   │ ERC4626 vault                          │ various vault types
   │   ▼                                        ▼
   │ ┌──────────────┐                    ┌──────────────┐
   │ │    Halo      │                    │   Foreign    │
   │ │    PAU       │                    │  Halo PAU    │
   │ └──────┬───────┘                    └──────┬───────┘
   │        │                                   │
   │        ▼                                   ▼
   │    RWA/Custodian                      RWA/Custodian
   │    Endpoints                          Endpoints
   │
   └──► Core Halos
        (Morpho, Aave, SparkLend - legacy DeFi wrapped as Halo Units)
```

**Note: Risk Capital Tokens**

The diagram above shows the capital deployment flow. Parallel to this, risk capital tokens (srUSDS, TEJRC, TISRC) provide the risk capital that backs deployments:

- **srUSDS** (Senior Risk Capital) — held by end users, issued by Generators via LCTS
- **TEJRC** (Tokenized External Junior Risk Capital) — held by end users, issued by Primes via LCTS
- **TISRC** (Tokenized Isolated Senior Risk Capital) — held by end users, issued by Primes via LCTS

Primes *ingress* (recognize) this external risk capital as part of their capital base. Risk capital holders don't participate in the deployment flow — they provide the buffer that absorbs losses. See `risk-framework/risk-capital-ingression.md` for details.

---

## Laniakea Factory

A factory system that can deploy standardized PAU infrastructure:

| Deploys | Where |
|---------|-------|
| Generator PAUs | Mainnet |
| Prime PAUs | Mainnet |
| Halo PAUs | Mainnet |
| Foreign Prime PAUs | Altchains |
| Foreign Halo PAUs | Altchains |
| Skylink infrastructure | New altchain deployments |

### Key Benefits

- **Standardized deployment**: All PAUs deploy from audited templates
- **Rapid onboarding**: New Primes/Halos can be deployed without custom development
- **Pre-verification**: Factory-deployed PAUs can be recognized by governance systems for streamlined approval

---

## Sentinel Network Integration

PAUs are designed to be operated by the Sentinel Network — autonomous systems that:
- Execute approved operations within rate-limited bounds
- Monitor positions and trigger rebalancing
- Respond to market conditions within governance-approved parameters

The governance layer defines what Sentinels can do; Sentinels execute within those bounds.

---

## Key Architectural Invariants

1. **Rate limits are the universal control mechanism** — every capital flow is rate-limited
2. **Governance layer sits above deployed contracts** — no redeployment of audited ALM Controller infrastructure
3. **Same contracts, different configuration** — layers differ only in approved targets and rate limit values
4. **Instant decrease, constrained increase** — losses are reflected immediately via exchange rate haircuts; gains accrue gradually over time