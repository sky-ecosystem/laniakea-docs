# Diamond PAU

**Status:** Placeholder
**Last Updated:** 2026-01-27

> **Note:** This document is a placeholder awaiting full specification. It provides context for understanding references to Diamond PAU elsewhere in Laniakea documentation.

---

## Overview

Diamond PAU is a modular architecture for Parallelized Allocation Units using the [EIP-2535 Diamond proxy pattern](https://eips.ethereum.org/EIPS/eip-2535). It replaces the legacy single-controller design with a faceted approach where controller actions are deployed as separate contracts.

---

## Legacy PAU vs Diamond PAU

| Aspect | Legacy PAU | Diamond PAU |
|--------|-----------|-------------|
| **Controller** | Single monolithic contract | Diamond proxy + multiple facets |
| **Size limits** | Hits 24KB contract size limit | No practical size limit |
| **Adding functions** | Full controller upgrade required | Deploy new facet, add to diamond |
| **Upgrades** | Replace entire controller | Surgical facet replacement |
| **Risk surface** | All logic in one contract | Isolated facet logic |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       DIAMOND PAU                                │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Diamond Proxy                             ││
│  │                                                              ││
│  │  Routes function calls to appropriate facet                  ││
│  │  Stores facet → selector mappings                           ││
│  └──────────────────────────┬──────────────────────────────────┘│
│                             │                                    │
│         ┌───────────────────┼───────────────────┐               │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Facet A   │    │   Facet B   │    │   Facet C   │   ...   │
│  │             │    │             │    │             │         │
│  │ • deposit   │    │ • withdraw  │    │ • rebalance │         │
│  │ • mint      │    │ • redeem    │    │ • swap      │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                      ALMProxy                                ││
│  │                                                              ││
│  │  Holds custody of funds (unchanged from legacy)              ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                     RateLimits                               ││
│  │                                                              ││
│  │  Enforces rate constraints (unchanged from legacy)           ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## Why Diamond Pattern

### Contract Size Problem

Solidity contracts are limited to ~24KB bytecode. As controller functionality grows:
- More vault integrations
- More token standards
- More deployment strategies

The legacy single-controller design hits this limit, forcing either:
- Splitting logic awkwardly across contracts
- Removing features to make room
- Complex upgrade coordination

### Diamond Solution

The diamond pattern solves this by:

1. **Facets** — Each facet is a separate contract containing related functions
2. **Selector routing** — Diamond proxy maps function selectors to facet addresses
3. **Shared storage** — All facets share the diamond's storage via delegatecall
4. **Unlimited growth** — Add new facets without touching existing ones

---

## Facet Organization

Facets are organized by function type:

| Facet | Functions |
|-------|-----------|
| **ERC4626Facet** | deposit, withdraw, mint, redeem for ERC-4626 vaults |
| **SwapFacet** | swap operations across DEXs |
| **MorphoFacet** | Morpho-specific deposit/withdraw |
| **NFATFacet** | NFAT claim, deploy, redeem operations |
| **AdminFacet** | setRelayer, setFreezer, configuration |

New integrations = new facets, not controller upgrades.

---

## Upgrade Process

### Legacy PAU Upgrade
1. Deploy new controller with all functions
2. Migrate state or ensure compatibility
3. Update proxy to point to new controller
4. All-or-nothing — entire controller replaced

### Diamond PAU Upgrade
1. Deploy only the new/changed facet
2. Call `diamondCut` to add/replace/remove selectors
3. Surgical — only affected functions change
4. Other facets untouched

---

## Storage

Diamond PAU uses [diamond storage pattern](https://eips.ethereum.org/EIPS/eip-2535#storage) to avoid storage collisions between facets:

```solidity
// Each facet uses namespaced storage
bytes32 constant ERC4626_STORAGE = keccak256("diamond.storage.erc4626");

struct ERC4626Storage {
    mapping(address => uint256) vaultBalances;
    // ...
}

function erc4626Storage() internal pure returns (ERC4626Storage storage s) {
    bytes32 position = ERC4626_STORAGE;
    assembly { s.slot := position }
}
```

---

## Configurator Integration

Diamond PAU integrates with Configurator Unit the same as legacy:

- **RateLimits** — Unchanged, still managed via Configurator
- **Relayer/Freezer** — Set via AdminFacet, authorized by Configurator
- **Init controller actions** — Reference specific facet functions

The diamond is transparent to the Configurator — it just sees callable functions.

---

## Migration Path

Existing legacy PAUs can migrate to Diamond PAU:

1. Deploy Diamond proxy with equivalent facets
2. Deploy new ALMProxy pointing to Diamond (or upgrade existing)
3. Migrate RateLimits configuration
4. Transfer custody from old ALMProxy to new
5. Update Configurator PAU registration

Migration can be done per-PAU without affecting others.
