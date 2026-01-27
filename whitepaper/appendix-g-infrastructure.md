# Appendix G: Infrastructure

Overview of currently deployed contracts, bridges, and legacy systems.

> **Note:** Addresses marked `[TBD]` are pending deployment or verification and will be populated before final publication.

---

## Core Protocol (Ethereum Mainnet)

### Token Contracts

| Token | Address | Notes |
|-------|---------|-------|
| **USDS** | `0xdC035D45d973E3EC169d2276DDab16f1e407384F` | Sky stablecoin |
| **sUSDS** | `0xa3931d71877C0E7a3148CB7Eb4463524FEc27fbD` | Savings token |
| **SKY** | `0x56072C95FAA701256059aa122697B133aDEd9279` | Governance token |
| **DAI** | `0x6B175474E89094C44Da98b954EedeAC495271d0F` | Legacy stablecoin |
| **MKR** | `0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2` | Legacy governance |

### Core Modules

| Contract | Address | Purpose |
|----------|---------|---------|
| **Vat** | `0x35D1b3F3D7966A1DFe207aa4514C12a259A0492B` | Core accounting engine |
| **Pot** | `0x197E90f9FAD81970bA7976f33CbD77088E5D7cf7` | DSR accumulator |
| **Jug** | `0x19c0976f590D67707E62397C87829d896Dc0f1F1` | Stability fee accumulator |
| **Vow** | `0xA950524441892A31ebddF91d3cEEFa04Bf454466` | System surplus/debt |

### PSM (Peg Stability)

| Contract | Address | Asset |
|----------|---------|-------|
| **LitePSM USDC** | *[TBD]* | USDC ↔ USDS |

---

## Prime Agent Infrastructure

### Spark

| Contract | Address | Purpose |
|----------|---------|---------|
| **Spark SubProxy** | `0x3300f198988e4C9C63F75dF86De36421f06af8c4` | Treasury |
| **SparkLend Pool** | *[TBD]* | Lending market |

#### Spark Liquidity Layer (SLL)

**Mainnet:**

| Contract | Address | Purpose |
|----------|---------|---------|
| **ALM Proxy** | *[TBD]* | Custody/execution |
| **MainnetController** | *[TBD]* | Action orchestration |
| **RateLimits** | *[TBD]* | Operation caps |

**Core Operator Multisig:** `0x8Cc0Cb0cfB6B7e548cfd395B833c05C346534795` (2/5)

### Grove

| Contract | Address | Purpose |
|----------|---------|---------|
| **Grove SubProxy** | `0x1369f7b2b38c76B6478c0f0E66D94923421891Ba` | Treasury |

### Keel

| Contract | Address | Purpose |
|----------|---------|---------|
| **Keel SubProxy** | `0x355CD90Ecb1b409Fdf8b64c4473C3B858dA2c310` | Treasury |

### Obex

| Contract | Address | Purpose |
|----------|---------|---------|
| **Obex SubProxy** | `0x8be042581f581E3620e29F213EA8b94afA1C8071` | Treasury |

---

## Multi-Chain Deployments

### SkyLink Supported Chains

| Chain | Status | USDS | sUSDS |
|-------|--------|------|-------|
| **Ethereum** | Active | Native | Native |
| **Base** | Active | Bridged | Bridged |
| **Arbitrum** | Active | Bridged | Bridged |
| **Optimism** | Active | Bridged | Bridged |
| **Unichain** | Active | Bridged | Bridged |
| **Avalanche** | Active | Bridged | Bridged |

### Chain-Specific Contracts

*[To be populated with per-chain addresses]*

---

## Bridge Infrastructure

### CCTP (Circle Cross-Chain Transfer Protocol)

| Route | Status | Notes |
|-------|--------|-------|
| Ethereum ↔ Base | Active | USDC bridging |
| Ethereum ↔ Arbitrum | Active | USDC bridging |
| Ethereum ↔ Optimism | Active | USDC bridging |
| Ethereum ↔ Avalanche | Active | USDC bridging |

---

## DeFi Integrations (Core Halos)

### Morpho

| Instance | Chain | Asset | Address |
|----------|-------|-------|---------|
| Morpho DAI | Ethereum | DAI | *[TBD]* |
| Morpho USDS | Ethereum | USDS | *[TBD]* |
| Morpho USDC | Ethereum | USDC | *[TBD]* |
| Morpho Blue USDC | Base | USDC | *[TBD]* |

### Aave

| Instance | Chain | Asset | Address |
|----------|-------|-------|---------|
| Aave V3 | Ethereum | Various | *[TBD]* |

---

## Governance Infrastructure

### Voting & Execution

| Contract | Address | Purpose |
|----------|---------|---------|
| **Chief** | `0x0a3f6849f78076aefaDf113F5BED87720274dDC0` | Governance voting |
| **Pause** | `0xbE286431454714F511008713973d3B053A2d38f3` | Executive delay |

### Oracles

| Oracle | Address | Purpose |
|--------|---------|---------|
| **PIP_SKY** | *[TBD]* | SKY price oracle |
| **Capped OSM** | *[TBD]* | Price cap wrapper |

---

## Legacy Systems

### Vault Types (Selected)

| Vault | Collateral | Status |
|-------|------------|--------|
| ETH-A | ETH | Active |
| ETH-B | ETH | Active |
| ETH-C | ETH | Active |
| WBTC-A | WBTC | Active |
| WSTETH-A | wstETH | Active |

### Deprecated Contracts

| Contract | Purpose | Replacement |
|----------|---------|-------------|
| *[Legacy PSMs]* | Peg stability | LitePSM |
| *[Old vault types]* | Various | Consolidated |

---

## Emergency Infrastructure

### Emergency Response

| Address | Role | Purpose |
|---------|------|---------|
| **Freezer Multisig** | *[TBD]* | Emergency freeze capability |
| **ERG Contacts** | *[Operational]* | Incident response |

---

## Planned Infrastructure (Post-Laniakea)

| Component | Purpose | Status |
|-----------|---------|--------|
| **Laniakea Factory** | PAU deployment | Development |
| **LCTS Contracts** | Queue-based tokens | Development |
| **Configurator Unit** | BEAM hierarchy | Development |
| **Sentinel Infrastructure** | Autonomous operations | Design |

---

*Note: Addresses marked [TBD] need to be populated. This appendix should be kept current as infrastructure is deployed or deprecated.*
